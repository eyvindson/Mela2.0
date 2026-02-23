from lukefi.metsi.domain.conditions import TimePoints
from lukefi.metsi.domain.forestry_types import ForestCondition
from lukefi.metsi.domain.natural_processes.grow_acta import grow_acta_fn
from lukefi.metsi.domain.pre_ops import generate_reference_trees, preproc_filter, scale_area_weight
from lukefi.metsi.domain.forestry_treatments.regeneration import regeneration
from lukefi.metsi.domain.forestry_treatments.soil_surface_preparation import soil_surface_preparation
from lukefi.metsi.sim.generators import Alternatives, Event, Sequence
from lukefi.metsi.sim.sim_configuration import Transition
from lukefi.metsi.sim.simulation_instruction import SimulationInstruction
from lukefi.metsi.sim.treatment import do_nothing


def planting(species: int, stems: float, h: float, age: float):
    return {
        "origin": 2,
        "method": 2,
        "species": species,
        "stems_per_ha": stems,
        "height": h,
        "biological_age": age,
        "type": "artificial",
    }


control_structure = {
    "app_configuration": {
        "state_format": "vmi13",
        "run_modes": ["preprocess", "simulate"],
        "preprocessing_output_file": "prepro_portfolio_balanced",
        "simulation_output_file": "sim_portfolio_balanced",
    },
    "preprocessing_operations": [scale_area_weight, generate_reference_trees, preproc_filter],
    "preprocessing_params": {
        generate_reference_trees: [{"n_trees": 10, "method": "weibull", "debug": False}],
        preproc_filter: [{
            "remove trees": (lambda trees: (trees.sapling != 0) | (trees.stems_per_ha == 0)),
            "remove stands": (lambda stand: (stand.site_type_category is None) or (stand.site_type_category == 0)),
        }],
    },
    "simulation_instructions": [
        SimulationInstruction(
            conditions=[TimePoints([2025])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"pb_2025_wait"}),
                Event(treatment=soil_surface_preparation, tags={"pb_2025_mound"}),
                Event(treatment=regeneration, static_parameters=planting(1, 1200.0, 0.7, 3.0), tags={"pb_2025_pine_1200"}),
                Event(treatment=regeneration, static_parameters=planting(2, 1200.0, 0.7, 3.0), tags={"pb_2025_spruce_1200"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=planting(1, 1600.0, 0.7, 3.0), tags={"pb_2025_mound_pine_1600"})]),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=planting(2, 1600.0, 0.7, 3.0), tags={"pb_2025_mound_spruce_1600"})]),
                Sequence([Event(treatment=regeneration, static_parameters=planting(1, 900.0, 0.7, 3.0)), Event(treatment=regeneration, static_parameters=planting(2, 600.0, 0.7, 3.0), tags={"pb_2025_mix"})]),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2040])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"pb_2040_wait"}),
                Event(treatment=soil_surface_preparation, tags={"pb_2040_mound"}),
                Event(treatment=regeneration, static_parameters=planting(1, 800.0, 0.8, 4.0), tags={"pb_2040_pine_fill"}),
                Event(treatment=regeneration, static_parameters=planting(2, 800.0, 0.8, 4.0), tags={"pb_2040_spruce_fill"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=planting(1, 1000.0, 0.8, 4.0), tags={"pb_2040_mound_pine"})]),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=planting(2, 1000.0, 0.8, 4.0), tags={"pb_2040_mound_spruce"})]),
                Sequence([Event(treatment=regeneration, static_parameters=planting(1, 500.0, 0.8, 4.0)), Event(treatment=regeneration, static_parameters=planting(2, 500.0, 0.8, 4.0), tags={"pb_2040_mix"})]),
            ])],
        ),
        # 7*7*6 = 294 combinations
        SimulationInstruction(
            conditions=[TimePoints([2055])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"pb_2055_wait"}),
                Event(treatment=soil_surface_preparation, tags={"pb_2055_mound"}),
                Event(treatment=regeneration, static_parameters=planting(1, 500.0, 0.9, 5.0), tags={"pb_2055_pine_fill"}),
                Event(treatment=regeneration, static_parameters=planting(2, 500.0, 0.9, 5.0), tags={"pb_2055_spruce_fill"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=planting(1, 700.0, 0.9, 5.0), tags={"pb_2055_mound_pine"})]),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=planting(2, 700.0, 0.9, 5.0), tags={"pb_2055_mound_spruce"})]),
            ])],
        ),
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2070),
}


__all__ = ["control_structure"]
