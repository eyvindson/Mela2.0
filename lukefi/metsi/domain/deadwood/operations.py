from copy import copy

from lukefi.metsi.data.model import ForestStand
from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.domain.deadwood.collected_data import DeadwoodPoolsData
from lukefi.metsi.domain.deadwood.inflow_builder import DeadwoodInflowConfig, build_deadwood_inflows
from lukefi.metsi.domain.deadwood.types import DeadwoodState
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
        return stand, []

    inflows = build_deadwood_inflows(
        previous_trees=stand.deadwood_previous_trees,
        current_trees=stand.reference_trees,
        removed_trees=_resolve_removed_trees(stand, **operation_parameters),
        config=config,
    )

    pools, fluxes = backend.step(stand.deadwood_state.pools, inflows, years=step_years)
    stand.deadwood_state.pools = pools
    stand.deadwood_state.latest_fluxes = fluxes
    stand.deadwood_previous_trees = _copy_reference_trees(stand.reference_trees)

    return stand, [DeadwoodPoolsData(pools=pools, fluxes=fluxes, inflows=inflows)]


update_deadwood_pools = Treatment(
    update_deadwood_pools_fn,
    name="update_deadwood_pools",
    default_tags={"deadwood"},
    collected_data={DeadwoodPoolsData},
)
