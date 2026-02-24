import numpy as np
import pytest

from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.domain.deadwood.biomass_conversion import RepolaBiomassConverter
from lukefi.metsi.domain.deadwood.inflow_builder import DeadwoodInflowConfig, build_deadwood_inflows
from lukefi.metsi.domain.deadwood.types import ChannelAWENH, DeadwoodInflows, DeadwoodPools
from lukefi.metsi.domain.deadwood.yasso_backend import FINLAND_STATIC_CLIMATE, Yasso07Adapter, YassoClimate


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
    assert inflows.cwl_c > inflows.fwl_c > inflows.nwl_c


def test_growth_model_mortality_signal_overrides_tree_list_diff():
    prev = make_reference_trees(["t1"], [100.0], [18.0], [15.0], [1])
    cur = make_reference_trees(["t1"], [100.0], [18.0], [15.0], [1])
    growth_mortality = make_reference_trees(["t1"], [12.0], [18.0], [15.0], [1])

    inflows = build_deadwood_inflows(
        prev,
        cur,
        growth_mortality_trees=growth_mortality,
        config=DeadwoodInflowConfig(),
    )

    assert inflows.mortality_c > 0.0
    assert inflows.harvest_residue_c == 0.0


def test_species_group_specific_residue_defaults():
    removed_pine = make_reference_trees(["p"], [30.0], [20.0], [16.0], [1])
    removed_spruce = make_reference_trees(["s"], [30.0], [20.0], [16.0], [2])

    config = DeadwoodInflowConfig()
    pine = build_deadwood_inflows(removed_pine, removed_pine, removed_trees=removed_pine, config=config)
    spruce = build_deadwood_inflows(removed_spruce, removed_spruce, removed_trees=removed_spruce, config=config)

    assert spruce.harvest_residue_c > pine.harvest_residue_c


def test_repola_converter_exposes_all_components_and_root_split():
    trees = make_reference_trees(["t1"], [100.0], [18.0], [15.0], [1])
    components = RepolaBiomassConverter().component_carbon_kg_per_ha(trees)

    assert components.stem_c > 0
    assert components.branch_c > 0
    assert components.foliage_c > 0
    assert components.stump_c > 0
    assert components.coarse_root_c > 0
    assert components.fine_root_c > 0
    np.testing.assert_allclose(components.fine_root_c / components.roots_c, 0.3, rtol=1e-6)


def test_invalid_equation_set_rejected():
    prev = make_reference_trees(["t1"], [100.0], [18.0], [15.0], [1])
    cur = make_reference_trees(["t1"], [100.0], [18.0], [15.0], [1])
    with pytest.raises(ValueError, match="Unsupported equation_set"):
        build_deadwood_inflows(prev, cur, config=DeadwoodInflowConfig(equation_set="marklund"))


def test_zero_input_no_change_backend():
    backend = Yasso07Adapter(annual_decay_rate=0.0, prefer_binary=False)
    pools = DeadwoodPools()
    updated, fluxes = backend.step(pools, DeadwoodInflows(), years=1)

    assert updated.total_c == 0.0
    assert fluxes.input_c == 0.0
    assert fluxes.decomposition_c == 0.0
    assert fluxes.net_change_c == 0.0


def test_deterministic_one_step_decomposition_contract():
    backend = Yasso07Adapter(annual_decay_rate=0.03, prefer_binary=False)
    pools = DeadwoodPools(cwl=ChannelAWENH(acid_c=10.0), fwl=ChannelAWENH(water_c=5.0), nwl=ChannelAWENH(ethanol_c=4.0))
    inflows = DeadwoodInflows(mortality_cwl_c=2.0, harvest_fwl_c=1.0)

    first = backend.step(pools, inflows, years=1)
    second = backend.step(pools, inflows, years=1)

    np.testing.assert_allclose(first[0].total_c, second[0].total_c)
    np.testing.assert_allclose(first[1].decomposition_c, second[1].decomposition_c)


def test_climate_configurable_but_finland_default_available():
    pools = DeadwoodPools(cwl=ChannelAWENH(acid_c=10.0))
    inflows = DeadwoodInflows()

    colder = Yasso07Adapter(climate_default=YassoClimate(temperature_c=-2.0, precipitation_mm=500.0, temperature_amplitude_c=15.0), prefer_binary=False)
    warmer = Yasso07Adapter(climate_default=YassoClimate(temperature_c=8.0, precipitation_mm=650.0, temperature_amplitude_c=12.0), prefer_binary=False)

    cold_updated, _ = colder.step(pools, inflows, years=5)
    warm_updated, _ = warmer.step(pools, inflows, years=5)

    assert FINLAND_STATIC_CLIMATE.temperature_c == 3.5
    assert warm_updated.total_c < cold_updated.total_c
