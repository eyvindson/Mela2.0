from copy import copy, deepcopy

from lukefi.metsi.data.model import ForestStand
from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.domain.deadwood.class_dynamics import update_class_state
from lukefi.metsi.domain.deadwood.collected_data import DeadwoodPoolsData
from lukefi.metsi.domain.deadwood.inflow_builder import DeadwoodInflowConfig, build_deadwood_inflows
from lukefi.metsi.domain.deadwood.initialization import initialize_deadwood
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
        initialize_deadwood(stand, config)
        stand.deadwood_previous_trees = _copy_reference_trees(stand.reference_trees)

    if stand.deadwood_state.pools.total_c <= 0.0 and stand.deadwood_previous_trees.size == 0:
        return stand, []

    if stand.deadwood_state.pools.total_c > 0.0 and not stand.deadwood_state.source_pools:
        stand.deadwood_state.source_pools = {
            "mortality": deepcopy(stand.deadwood_state.pools),
            "harvest": DeadwoodState().pools,
            "disturbance": DeadwoodState().pools,
        }

    measured_inflows = build_deadwood_inflows(
        previous_trees=stand.deadwood_previous_trees,
        current_trees=stand.reference_trees,
        removed_trees=_resolve_removed_trees(stand, **operation_parameters),
        growth_mortality_trees=_resolve_growth_mortality_trees(stand),
        config=config,
    )
    inflows = DeadwoodInflows(
        mortality_cwl_c=measured_inflows.mortality_cwl_c,
        mortality_fwl_c=measured_inflows.mortality_fwl_c,
        mortality_nwl_c=measured_inflows.mortality_nwl_c,
        harvest_cwl_c=measured_inflows.harvest_cwl_c,
        harvest_fwl_c=measured_inflows.harvest_fwl_c,
        harvest_nwl_c=measured_inflows.harvest_nwl_c,
        disturbance_cwl_c=measured_inflows.disturbance_cwl_c,
        disturbance_fwl_c=measured_inflows.disturbance_fwl_c,
        disturbance_nwl_c=measured_inflows.disturbance_nwl_c,
    )

    if stand.deadwood_state.pools.total_c <= 0.0 and inflows.total_c <= 0.0:
        return stand, []

    source_inflows = {
        "mortality": DeadwoodInflows(
            mortality_cwl_c=inflows.mortality_cwl_c,
            mortality_fwl_c=inflows.mortality_fwl_c,
            mortality_nwl_c=inflows.mortality_nwl_c,
        ),
        "harvest": DeadwoodInflows(
            harvest_cwl_c=inflows.harvest_cwl_c,
            harvest_fwl_c=inflows.harvest_fwl_c,
            harvest_nwl_c=inflows.harvest_nwl_c,
        ),
        "disturbance": DeadwoodInflows(
            disturbance_cwl_c=inflows.disturbance_cwl_c,
            disturbance_fwl_c=inflows.disturbance_fwl_c,
            disturbance_nwl_c=inflows.disturbance_nwl_c,
        ),
    }
    source_fluxes = {}
    stand.deadwood_state.source_pools = stand.deadwood_state.source_pools or {}
    pools = None
    for source, source_inflow in source_inflows.items():
        source_pool = stand.deadwood_state.source_pools.get(source, DeadwoodState().pools)
        updated_source_pool, flux = backend.step(source_pool, source_inflow, years=step_years)
        stand.deadwood_state.source_pools[source] = updated_source_pool
        source_fluxes[source] = flux
        pools = updated_source_pool if pools is None else pools.add(updated_source_pool)

    fluxes = DeadwoodFluxes(
        input_c=inflows.total_c,
        decomposition_c=sum(item.decomposition_c for item in source_fluxes.values()),
        net_change_c=(pools.total_c if pools is not None else 0.0) - stand.deadwood_state.pools.total_c,
    )
    stand.deadwood_state.class_state = update_class_state(stand.deadwood_state.class_state, inflows, step_years)
    stand.deadwood_state.pools = pools
    stand.deadwood_state.latest_fluxes = fluxes
    stand.deadwood_previous_trees = _copy_reference_trees(stand.reference_trees)

    stand_year = int(getattr(stand, "year", 0) or 0)
    return stand, [DeadwoodPoolsData(pools=pools, fluxes=fluxes, inflows=inflows, source_fluxes=source_fluxes, year=stand_year)]


update_deadwood_pools = Treatment(
    update_deadwood_pools_fn,
    name="update_deadwood_pools",
    default_tags={"deadwood"},
    collected_data={DeadwoodPoolsData},
)
