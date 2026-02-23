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


def regen(species: int, stems: float, height: float = 0.7, age: float = 3.0):
    return {"origin": 2, "method": 2, "species": species, "stems_per_ha": stems, "height": height,
            "biological_age": age, "type": "artificial"}


control_structure = {
    "app_configuration": {
        "state_format": "vmi13",
        "run_modes": ["preprocess", "simulate"],
        "preprocessing_output_file": "prepro_regeneration_pathways",
        "simulation_output_file": "sim_regeneration_pathways",
    },
    "preprocessing_operations": [scale_area_weight, generate_reference_trees, preproc_filter],
    "preprocessing_params": {
        generate_reference_trees: [{"n_trees": 10, "method": "weibull", "debug": False}],
        preproc_filter: [{"remove trees": (lambda trees: (trees.sapling != 0) | (trees.stems_per_ha == 0)),
                          "remove stands": (lambda stand: (stand.site_type_category is None) or (stand.site_type_category == 0))}],
    },
    "simulation_instructions": [
        SimulationInstruction(conditions=[TimePoints([2030])], events=[Alternatives([
            Event(treatment=do_nothing, tags={"rp_2030_wait"}),
            Event(treatment=regeneration, static_parameters=regen(1, 1200.0), tags={"rp_2030_pine_1200"}),
            Event(treatment=regeneration, static_parameters=regen(1, 1800.0), tags={"rp_2030_pine_1800"}),
            Event(treatment=regeneration, static_parameters=regen(2, 1200.0), tags={"rp_2030_spruce_1200"}),
            Event(treatment=regeneration, static_parameters=regen(2, 1800.0), tags={"rp_2030_spruce_1800"}),
            Event(treatment=regeneration, static_parameters=regen(3, 1600.0), tags={"rp_2030_birch_1600"}),
            Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(1, 1800.0), tags={"rp_2030_mound_pine"})]),
            Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(2, 1800.0), tags={"rp_2030_mound_spruce"})]),
        ])]),
        SimulationInstruction(conditions=[TimePoints([2040])], events=[Alternatives([
            Event(treatment=do_nothing, tags={"rp_2040_wait"}),
            Event(treatment=soil_surface_preparation, tags={"rp_2040_mound"}),
            Event(treatment=regeneration, static_parameters=regen(1, 500.0, 0.75, 4.0), tags={"rp_2040_pine_fill_500"}),
            Event(treatment=regeneration, static_parameters=regen(2, 500.0, 0.75, 4.0), tags={"rp_2040_spruce_fill_500"}),
            Event(treatment=regeneration, static_parameters=regen(3, 500.0, 0.75, 4.0), tags={"rp_2040_birch_fill_500"}),
            Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(1, 800.0, 0.75, 4.0), tags={"rp_2040_mound_pine_fill"})]),
            Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(2, 800.0, 0.75, 4.0), tags={"rp_2040_mound_spruce_fill"})]),
        ])]),
        SimulationInstruction(conditions=[TimePoints([2050])], events=[Alternatives([
            Event(treatment=do_nothing, tags={"rp_2050_wait"}),
            Event(treatment=soil_surface_preparation, tags={"rp_2050_mound"}),
            Event(treatment=regeneration, static_parameters=regen(1, 350.0, 0.9, 5.0), tags={"rp_2050_pine_fill"}),
            Event(treatment=regeneration, static_parameters=regen(2, 350.0, 0.9, 5.0), tags={"rp_2050_spruce_fill"}),
            Event(treatment=regeneration, static_parameters=regen(3, 350.0, 0.9, 5.0), tags={"rp_2050_birch_fill"}),
            Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(1, 600.0, 0.9, 5.0), tags={"rp_2050_mound_pine_fill"})]),
        ])]),
        # 8 x 7 x 6 x 5 = 1680 alternatives
        SimulationInstruction(conditions=[TimePoints([2060])], events=[Alternatives([
            Event(treatment=do_nothing, tags={"rp_2060_wait"}),
            Event(treatment=soil_surface_preparation, tags={"rp_2060_mound"}),
            Event(treatment=regeneration, static_parameters=regen(1, 250.0, 1.0, 6.0), tags={"rp_2060_pine_fill"}),
            Event(treatment=regeneration, static_parameters=regen(2, 250.0, 1.0, 6.0), tags={"rp_2060_spruce_fill"}),
            Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(2, 450.0, 1.0, 6.0), tags={"rp_2060_mound_spruce"})]),
        ])]),
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2070),
}

__all__ = ["control_structure"]
