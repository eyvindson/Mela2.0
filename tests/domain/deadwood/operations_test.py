import numpy as np

from lukefi.metsi.data.model import ForestStand
from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.domain.deadwood.inflow_builder import DeadwoodInflowConfig
from lukefi.metsi.domain.deadwood.operations import update_deadwood_pools_fn
from lukefi.metsi.domain.deadwood.yasso_backend import Yasso07Adapter


def make_reference_trees(ids: list[str], stems: list[float], dbh: list[float], h: list[float], species: list[int]) -> ReferenceTrees:
    rt = ReferenceTrees()
    rt.vectorize(
        {
            "identifier": ids,
            "tree_number": list(range(1, len(ids) + 1)),
            "species": species,
            "breast_height_diameter": dbh,
            "height": h,
            "stems_per_ha": stems,
            "origin": [0] * len(ids),
        }
    )
    return rt


def test_update_deadwood_seeds_initial_pool_from_living_biomass():
    stand = ForestStand(identifier="s1", year=2022)
    stand.reference_trees = make_reference_trees(["t1"], [120.0], [22.0], [18.0], [1])

    out_stand, collected = update_deadwood_pools_fn(
        stand,
        enabled=True,
        backend=Yasso07Adapter(prefer_binary=False),
        deadwood_config=DeadwoodInflowConfig(initial_deadwood_share_of_living_biomass=0.02),
    )

    assert out_stand.deadwood_state.pools.total_c > 0.0
    assert len(collected) == 1
    assert collected[0].pools.total_c > 0.0
    assert collected[0].fluxes.input_c == 0.0


def test_update_deadwood_without_initial_share_keeps_previous_bootstrap_behavior():
    stand = ForestStand(identifier="s2", year=2022)
    stand.reference_trees = make_reference_trees(["t1"], [120.0], [22.0], [18.0], [1])

    _, collected = update_deadwood_pools_fn(
        stand,
        enabled=True,
        deadwood_config=DeadwoodInflowConfig(initial_deadwood_share_of_living_biomass=0.0),
        backend=Yasso07Adapter(prefer_binary=False),
    )

    assert collected == []


def test_update_deadwood_consumes_growth_model_mortality_on_first_call():
    stand = ForestStand(identifier="s2b", year=2022)
    stand.reference_trees = make_reference_trees(["t1"], [120.0], [22.0], [18.0], [1])
    stand.deadwood_growth_mortality_trees = make_reference_trees(["t1"], [5.0], [22.0], [18.0], [1])

    _, collected = update_deadwood_pools_fn(
        stand,
        enabled=True,
        deadwood_config=DeadwoodInflowConfig(initial_deadwood_share_of_living_biomass=0.02),
        backend=Yasso07Adapter(prefer_binary=False),
    )

    assert len(collected) == 1
    assert collected[0].inflows.mortality_c > 0.0
    assert collected[0].source_fluxes["mortality"].input_c > 0.0


def test_seeded_no_management_branch_decomposes_without_new_inputs():
    stand = ForestStand(identifier="s3", year=2022)
    stand.reference_trees = make_reference_trees(["t1"], [120.0], [22.0], [18.0], [1])
    backend = Yasso07Adapter(prefer_binary=False, annual_decay_rate=0.03)

    update_deadwood_pools_fn(
        stand,
        enabled=True,
        deadwood_config=DeadwoodInflowConfig(initial_deadwood_share_of_living_biomass=0.02),
        backend=backend,
    )
    prev_total = stand.deadwood_state.pools.total_c

    _, collected = update_deadwood_pools_fn(
        stand,
        enabled=True,
        deadwood_config=DeadwoodInflowConfig(initial_deadwood_share_of_living_biomass=0.02),
        backend=backend,
    )

    assert len(collected) == 1
    assert np.isclose(collected[0].fluxes.input_c, 0.0)
    assert collected[0].fluxes.decomposition_c > 0.0
    assert stand.deadwood_state.pools.total_c < prev_total


def test_operation_tracks_source_pools_and_updates_class_state_deterministically():
    stand = ForestStand(identifier="s4", year=2022)
    stand.reference_trees = make_reference_trees(["t1"], [120.0], [22.0], [18.0], [1])
    stand.deadwood_removed_trees = make_reference_trees(["h1"], [30.0], [18.0], [16.0], [1])

    update_deadwood_pools_fn(
        stand,
        enabled=True,
        deadwood_config=DeadwoodInflowConfig(initial_deadwood_share_of_living_biomass=0.02),
        backend=Yasso07Adapter(prefer_binary=False, annual_decay_rate=0.01),
    )
    _, collected = update_deadwood_pools_fn(
        stand,
        enabled=True,
        deadwood_config=DeadwoodInflowConfig(initial_deadwood_share_of_living_biomass=0.02),
        backend=Yasso07Adapter(prefer_binary=False, annual_decay_rate=0.01),
    )

    assert len(collected) == 1
    assert set(stand.deadwood_state.source_pools.keys()) == {"mortality", "harvest", "disturbance"}
    assert sum(item.carbon_c for item in stand.deadwood_state.class_state) > 0.0


def test_acceptance_trend_harvest_spike_then_decline_within_15_years():
    stand = ForestStand(identifier="s5", year=2020)
    stand.reference_trees = make_reference_trees(["t1", "t2"], [150.0, 120.0], [24.0, 20.0], [20.0, 17.0], [1, 2])
    backend = Yasso07Adapter(prefer_binary=False, annual_decay_rate=0.08)

    update_deadwood_pools_fn(stand, enabled=True, backend=backend, deadwood_config=DeadwoodInflowConfig())
    baseline = stand.deadwood_state.pools.total_c

    stand.deadwood_removed_trees = make_reference_trees(["h1"], [80.0], [22.0], [18.0], [1])
    _, harvest_collected = update_deadwood_pools_fn(stand, enabled=True, backend=backend, deadwood_config=DeadwoodInflowConfig())
    post_harvest = stand.deadwood_state.pools.total_c
    assert harvest_collected[0].inflows.harvest_residue_c > 0.0
    assert post_harvest > baseline

    totals = []
    for _ in range(3):
        update_deadwood_pools_fn(stand, enabled=True, backend=backend, deadwood_config=DeadwoodInflowConfig())
        totals.append(stand.deadwood_state.pools.total_c)

    assert totals[2] < post_harvest
