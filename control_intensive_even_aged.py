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


PINE_BASE = {
    "origin": 2,
    "method": 2,
    "species": 1,
    "stems_per_ha": 1600.0,
    "height": 0.7,
    "biological_age": 3.0,
    "type": "artificial",
}


control_structure = {
    "app_configuration": {
        "state_format": "vmi13",
        "run_modes": ["preprocess", "simulate"],
        "preprocessing_output_file": "prepro_intensive_even_aged",
        "simulation_output_file": "sim_intensive_even_aged",
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
        # 8 options
        SimulationInstruction(
            conditions=[TimePoints([2025])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"ia_2025_wait"}),
                Event(treatment=soil_surface_preparation, tags={"ia_2025_mound"}),
                Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 1200.0}, tags={"ia_2025_plant_1200"}),
                Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 1600.0}, tags={"ia_2025_plant_1600"}),
                Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 2200.0}, tags={"ia_2025_plant_2200"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 1600.0}, tags={"ia_2025_mound_then_plant_1600"})]),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 2200.0}, tags={"ia_2025_mound_then_plant_2200"})]),
                Sequence([Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 1200.0}), Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 600.0}, tags={"ia_2025_two_stage"})]),
            ])],
        ),
        # 6 options
        SimulationInstruction(
            conditions=[TimePoints([2035])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"ia_2035_wait"}),
                Event(treatment=soil_surface_preparation, tags={"ia_2035_mound"}),
                Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 900.0}, tags={"ia_2035_fill_900"}),
                Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 1400.0}, tags={"ia_2035_fill_1400"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 900.0}, tags={"ia_2035_mound_fill_900"})]),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 1400.0}, tags={"ia_2035_mound_fill_1400"})]),
            ])],
        ),
        # 4 options => 8*6*4 = 192 alternatives
        SimulationInstruction(
            conditions=[TimePoints([2045])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"ia_2045_wait"}),
                Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 700.0}, tags={"ia_2045_fill_700"}),
                Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 1200.0}, tags={"ia_2045_fill_1200"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=PINE_BASE | {"stems_per_ha": 1200.0}, tags={"ia_2045_mound_fill_1200"})]),
            ])],
        ),
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2060),
}


__all__ = ["control_structure"]
