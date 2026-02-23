import numpy as np
import pytest

from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.domain.deadwood.inflow_builder import DeadwoodInflowConfig, build_deadwood_inflows
from lukefi.metsi.domain.deadwood.types import DeadwoodInflows, DeadwoodPools
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


def test_inflow_builder_mass_balance_and_partial_stem_loss():
    prev = make_reference_trees(["t1", "t2"], [100.0, 80.0], [18.0, 22.0], [15.0, 18.0], [1, 2])
    cur = make_reference_trees(["t1", "t2"], [70.0, 80.0], [18.0, 22.0], [15.0, 18.0], [1, 2])
    removed = make_reference_trees(["h1"], [30.0], [20.0], [16.0], [2])

    inflows = build_deadwood_inflows(prev, cur, removed_trees=removed, config=DeadwoodInflowConfig())

    assert inflows.total_c == inflows.mortality_c + inflows.harvest_residue_c + inflows.disturbance_c
    assert inflows.mortality_c > 0.0
    assert inflows.harvest_residue_c > 0.0

    # mortality should reflect 30 stem loss from t1, not a full 100-stem removal
    cur_zero = make_reference_trees(["t2"], [80.0], [22.0], [18.0], [2])
    inflow_full = build_deadwood_inflows(prev, cur_zero, removed_trees=None, config=DeadwoodInflowConfig())
    assert inflows.mortality_c < inflow_full.mortality_c


def test_invalid_equation_set_rejected():
    prev = make_reference_trees(["t1"], [100.0], [18.0], [15.0], [1])
    cur = make_reference_trees(["t1"], [100.0], [18.0], [15.0], [1])
    with pytest.raises(ValueError, match="Unsupported equation_set"):
        build_deadwood_inflows(prev, cur, config=DeadwoodInflowConfig(equation_set="marklund"))


def test_zero_input_no_change_backend():
    backend = Yasso07Adapter(annual_decay_rate=0.0)
    pools = DeadwoodPools()
    updated, fluxes = backend.step(pools, DeadwoodInflows(), years=1)

    assert updated.total_c == 0.0
    assert fluxes.input_c == 0.0
    assert fluxes.decomposition_c == 0.0
    assert fluxes.net_change_c == 0.0


def test_deterministic_one_step_decomposition_contract():
    backend = Yasso07Adapter(annual_decay_rate=0.03)
    pools = DeadwoodPools(acid_c=10.0, water_c=5.0, ethanol_c=4.0, non_soluble_c=8.0, humus_c=3.0)
    inflows = DeadwoodInflows(mortality_c=2.0, harvest_residue_c=1.0)

    first = backend.step(pools, inflows, years=1)
    second = backend.step(pools, inflows, years=1)

    np.testing.assert_allclose(first[0].total_c, second[0].total_c)
    np.testing.assert_allclose(first[1].decomposition_c, second[1].decomposition_c)
