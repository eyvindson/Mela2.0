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
    return {
        "origin": 2,
        "method": 2,
        "species": species,
        "stems_per_ha": stems,
        "height": height,
        "biological_age": age,
        "type": "artificial",
    }


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
        preproc_filter: [{
            "remove trees": (lambda trees: (trees.sapling != 0) | (trees.stems_per_ha == 0)),
            "remove stands": (lambda stand: (stand.site_type_category is None) or (stand.site_type_category == 0)),
        }],
    },
    "simulation_instructions": [
        # 7 options at regeneration start
        SimulationInstruction(
            conditions=[TimePoints([2030])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"rp_2030_wait"}),
                Event(treatment=regeneration, static_parameters=regen(1, 1400.0), tags={"rp_2030_pine_1400"}),
                Event(treatment=regeneration, static_parameters=regen(1, 2000.0), tags={"rp_2030_pine_2000"}),
                Event(treatment=regeneration, static_parameters=regen(2, 1400.0), tags={"rp_2030_spruce_1400"}),
                Event(treatment=regeneration, static_parameters=regen(2, 2000.0), tags={"rp_2030_spruce_2000"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(1, 1800.0), tags={"rp_2030_mound_pine"})]),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(2, 1800.0), tags={"rp_2030_mound_spruce"})]),
            ])],
        ),
        # 6 options for follow-up
        SimulationInstruction(
            conditions=[TimePoints([2040])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"rp_2040_wait"}),
                Event(treatment=soil_surface_preparation, tags={"rp_2040_mound"}),
                Event(treatment=regeneration, static_parameters=regen(1, 600.0), tags={"rp_2040_pine_fill_600"}),
                Event(treatment=regeneration, static_parameters=regen(2, 600.0), tags={"rp_2040_spruce_fill_600"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(1, 900.0), tags={"rp_2040_mound_pine_fill"})]),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(2, 900.0), tags={"rp_2040_mound_spruce_fill"})]),
            ])],
        ),
        # 5 options for late corrective action => 7*6*5=210
        SimulationInstruction(
            conditions=[TimePoints([2050])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"rp_2050_wait"}),
                Event(treatment=regeneration, static_parameters=regen(1, 400.0), tags={"rp_2050_pine_fill"}),
                Event(treatment=regeneration, static_parameters=regen(2, 400.0), tags={"rp_2050_spruce_fill"}),
                Event(treatment=soil_surface_preparation, tags={"rp_2050_mound_only"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters=regen(1, 700.0), tags={"rp_2050_mound_pine_fill"})]),
            ])],
        ),
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2065),
}


__all__ = ["control_structure"]
