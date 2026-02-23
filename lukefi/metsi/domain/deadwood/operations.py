from copy import copy

from lukefi.metsi.data.model import ForestStand
from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.domain.deadwood.collected_data import DeadwoodPoolsData
from lukefi.metsi.domain.deadwood.inflow_builder import DeadwoodInflowConfig, build_deadwood_inflows
from lukefi.metsi.domain.deadwood.types import DeadwoodState
from lukefi.metsi.domain.deadwood.yasso_backend import Yasso07Adapter
from lukefi.metsi.sim.collected_data import OpTuple
from lukefi.metsi.sim.treatment import Treatment


def _copy_reference_trees(trees: ReferenceTrees) -> ReferenceTrees:
    return trees[:] if trees.size > 0 else copy(trees)


def update_deadwood_pools_fn(input_: ForestStand, /, **operation_parameters) -> OpTuple[ForestStand]:
    stand = input_
    if not operation_parameters.get("enabled", False):
        return stand, []

    if stand.reference_trees is None:
        return stand, []

    step_years = int(operation_parameters.get("step", 5))
    config = operation_parameters.get("deadwood_config", DeadwoodInflowConfig())
    backend = operation_parameters.get("backend", Yasso07Adapter())

    if not hasattr(stand, "deadwood_state"):
        stand.deadwood_state = DeadwoodState()

    if not hasattr(stand, "deadwood_previous_trees"):
        stand.deadwood_previous_trees = _copy_reference_trees(stand.reference_trees)
        return stand, []

    removed_trees = operation_parameters.get("removed_trees")
    inflows = build_deadwood_inflows(
        previous_trees=stand.deadwood_previous_trees,
        current_trees=stand.reference_trees,
        removed_trees=removed_trees,
        config=config,
    )

    pools, fluxes = backend.step(stand.deadwood_state.pools, inflows, years=step_years)
    stand.deadwood_state.pools = pools
    stand.deadwood_state.latest_fluxes = fluxes
    stand.deadwood_previous_trees = _copy_reference_trees(stand.reference_trees)

    return stand, [DeadwoodPoolsData(pools=pools, fluxes=fluxes)]


update_deadwood_pools = Treatment(
    update_deadwood_pools_fn,
    name="update_deadwood_pools",
    default_tags={"deadwood"},
    collected_data={DeadwoodPoolsData},
)
