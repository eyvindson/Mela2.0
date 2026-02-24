from copy import copy

from lukefi.metsi.data.model import ForestStand
from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.domain.deadwood.collected_data import DeadwoodPoolsData
from lukefi.metsi.domain.deadwood.inflow_builder import DeadwoodInflowConfig, build_deadwood_inflows, estimate_initial_deadwood_channels
from lukefi.metsi.domain.deadwood.types import DeadwoodFluxes, DeadwoodInflows, DeadwoodState
from lukefi.metsi.domain.deadwood.yasso_backend import Yasso07Adapter, YassoClimate
from lukefi.metsi.sim.collected_data import OpTuple
from lukefi.metsi.sim.treatment import Treatment


def _copy_reference_trees(trees: ReferenceTrees) -> ReferenceTrees:
    return trees[:] if trees.size > 0 else copy(trees)


def _resolve_removed_trees(stand: ForestStand, **operation_parameters) -> ReferenceTrees | None:
    if operation_parameters.get("removed_trees") is not None:
        return operation_parameters["removed_trees"]
    removed_trees = getattr(stand, "deadwood_removed_trees", None)
    if removed_trees is not None:
        stand.deadwood_removed_trees = None
    return removed_trees


def _resolve_growth_mortality_trees(stand: ForestStand) -> ReferenceTrees | None:
    mortality_trees = getattr(stand, "deadwood_growth_mortality_trees", None)
    if mortality_trees is not None:
        stand.deadwood_growth_mortality_trees = None
    return mortality_trees


def _climate_provider_from_metadata(stand: ForestStand):
    climate = getattr(stand, "deadwood_climate", None)
    if isinstance(climate, (list, tuple)) and len(climate) >= 3:
        return lambda: YassoClimate(float(climate[0]), float(climate[1]), float(climate[2]))
    return None


def update_deadwood_pools_fn(input_: ForestStand, /, **operation_parameters) -> OpTuple[ForestStand]:
    stand = input_
    if not operation_parameters.get("enabled", False):
        return stand, []
    if stand.reference_trees is None:
        return stand, []

    step_years = int(operation_parameters.get("step", 5))
    config = operation_parameters.get("deadwood_config", DeadwoodInflowConfig())
    backend = operation_parameters.get("backend")
    if backend is None:
        backend = Yasso07Adapter(climate_provider=_climate_provider_from_metadata(stand))

    if not hasattr(stand, "deadwood_state"):
        stand.deadwood_state = DeadwoodState()

    if not hasattr(stand, "deadwood_previous_trees"):
        stand.deadwood_previous_trees = _copy_reference_trees(stand.reference_trees)
        if stand.deadwood_state.pools.total_c <= 0.0:
            seed_cwl, seed_fwl, seed_nwl = estimate_initial_deadwood_channels(stand.reference_trees, config)
            awenh_share = getattr(backend, "awenh_share", Yasso07Adapter().awenh_share)
            if seed_cwl > 0.0:
                stand.deadwood_state.pools.cwl.add_inflow(seed_cwl, awenh_share)
            if seed_fwl > 0.0:
                stand.deadwood_state.pools.fwl.add_inflow(seed_fwl, awenh_share)
            if seed_nwl > 0.0:
                stand.deadwood_state.pools.nwl.add_inflow(seed_nwl, awenh_share)
            stand_year = int(getattr(stand, "year", 0) or 0)
            return stand, [
                DeadwoodPoolsData(
                    pools=stand.deadwood_state.pools,
                    fluxes=DeadwoodFluxes(input_c=0.0, decomposition_c=0.0, net_change_c=0.0),
                    inflows=DeadwoodInflows(),
                    year=stand_year,
                )
            ]
        return stand, []

    inflows = build_deadwood_inflows(
        previous_trees=stand.deadwood_previous_trees,
        current_trees=stand.reference_trees,
        removed_trees=_resolve_removed_trees(stand, **operation_parameters),
        growth_mortality_trees=_resolve_growth_mortality_trees(stand),
        config=config,
    )

    pools, fluxes = backend.step(stand.deadwood_state.pools, inflows, years=step_years)
    stand.deadwood_state.pools = pools
    stand.deadwood_state.latest_fluxes = fluxes
    stand.deadwood_previous_trees = _copy_reference_trees(stand.reference_trees)

    stand_year = int(getattr(stand, "year", 0) or 0)
    return stand, [DeadwoodPoolsData(pools=pools, fluxes=fluxes, inflows=inflows, year=stand_year)]


update_deadwood_pools = Treatment(
    update_deadwood_pools_fn,
    name="update_deadwood_pools",
    default_tags={"deadwood"},
    collected_data={DeadwoodPoolsData},
)
