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


def planting(species: int, stems: float, h: float, age: float, origin: int = 2) -> dict:
    return {
        "origin": origin,
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
        "preprocessing_output_file": "prepro_portfolio_balanced_varied",
        "simulation_output_file": "sim_portfolio_balanced_varied",
    },
    "preprocessing_operations": [
        scale_area_weight,
        generate_reference_trees,
        preproc_filter,
    ],
    "preprocessing_params": {
        generate_reference_trees: [{"n_trees": 10, "method": "weibull", "debug": False}],
        preproc_filter: [{
            "remove trees": (lambda trees: (trees.sapling != 0) | (trees.stems_per_ha == 0)),
            "remove stands": (lambda stand: (stand.site_type_category is None) or (stand.site_type_category == 0)),
        }],
    },
    "simulation_instructions": [
        # Establishment phase (2025): mixed establishment choices
        SimulationInstruction(
            conditions=[TimePoints([2025])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"pbv_2025_wait", "style_passive"}),
                Event(treatment=soil_surface_preparation, tags={"pbv_2025_mound", "style_siteprep_regen"}),
                Event(treatment=regeneration, static_parameters=planting(1, 1200.0, 0.7, 3.0), tags={"pbv_2025_pine_1200", "style_shortened_rotation"}),
                Event(treatment=regeneration, static_parameters=planting(2, 1200.0, 0.7, 3.0), tags={"pbv_2025_spruce_1200", "style_extended_rotation"}),
                Sequence([
                    Event(treatment=soil_surface_preparation, tags={"pbv_2025_mound", "style_siteprep_regen"}),
                    Event(treatment=regeneration, static_parameters=planting(1, 1600.0, 0.7, 3.0), tags={"pbv_2025_mound_pine_1600", "style_regeneration_path"}),
                ]),
                Sequence([
                    Event(treatment=regeneration, static_parameters=planting(1, 700.0, 0.7, 3.0), tags={"pbv_2025_mix_a", "style_regeneration_path"}),
                    Event(treatment=regeneration, static_parameters=planting(2, 600.0, 0.7, 3.0), tags={"pbv_2025_mix_b", "style_regeneration_path"}),
                ]),
            ])],
        ),
        # Reinforcement phase (2032): delayed top-up and contrasting paths
        SimulationInstruction(
            conditions=[TimePoints([2032])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"pbv_2032_wait", "style_extended_rotation"}),
                Event(treatment=soil_surface_preparation, tags={"pbv_2032_mound", "style_siteprep_regen"}),
                Event(treatment=regeneration, static_parameters=planting(1, 600.0, 0.78, 4.0), tags={"pbv_2032_pine_fill_600", "style_shortened_rotation"}),
                Event(treatment=regeneration, static_parameters=planting(2, 600.0, 0.78, 4.0), tags={"pbv_2032_spruce_fill_600", "style_extended_rotation"}),
                Sequence([
                    Event(treatment=soil_surface_preparation, tags={"pbv_2032_mound", "style_siteprep_regen"}),
                    Event(treatment=regeneration, static_parameters=planting(2, 900.0, 0.78, 4.0), tags={"pbv_2032_mound_spruce", "style_regeneration_path"}),
                ]),
                Sequence([
                    Event(treatment=do_nothing, tags={"pbv_2032_buffer", "style_continuous_cover"}),
                    Event(treatment=regeneration, static_parameters=planting(3, 500.0, 0.78, 4.0), tags={"pbv_2032_birch_understory", "style_continuous_cover"}),
                ]),
            ])],
        ),
        # Transition phase (2043): contrasting late-rotation interventions
        SimulationInstruction(
            conditions=[TimePoints([2043])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"pbv_2043_wait", "style_extended_rotation"}),
                Event(treatment=regeneration, static_parameters=planting(1, 450.0, 0.9, 5.0), tags={"pbv_2043_pine_fill", "style_shortened_rotation"}),
                Event(treatment=regeneration, static_parameters=planting(2, 450.0, 0.9, 5.0), tags={"pbv_2043_spruce_fill", "style_extended_rotation"}),
                Event(treatment=soil_surface_preparation, tags={"pbv_2043_siteprep", "style_siteprep_regen"}),
                Sequence([
                    Event(treatment=soil_surface_preparation, tags={"pbv_2043_mound", "style_siteprep_regen"}),
                    Event(treatment=regeneration, static_parameters=planting(1, 650.0, 0.9, 5.0), tags={"pbv_2043_mound_pine", "style_regeneration_path"}),
                ]),
                Sequence([
                    Event(treatment=do_nothing, tags={"pbv_2043_hold", "style_continuous_cover"}),
                    Event(treatment=regeneration, static_parameters=planting(3, 300.0, 0.9, 5.0), tags={"pbv_2043_birch_enrich", "style_continuous_cover"}),
                ]),
            ])],
        ),
        # Late phase (2058): keep options open for optimization
        SimulationInstruction(
            conditions=[TimePoints([2058])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"pbv_2058_wait", "style_extended_rotation"}),
                Event(treatment=soil_surface_preparation, tags={"pbv_2058_mound", "style_siteprep_regen"}),
                Event(treatment=regeneration, static_parameters=planting(1, 250.0, 1.05, 6.0), tags={"pbv_2058_pine_fill", "style_shortened_rotation"}),
                Event(treatment=regeneration, static_parameters=planting(2, 250.0, 1.05, 6.0), tags={"pbv_2058_spruce_fill", "style_extended_rotation"}),
                Sequence([
                    Event(treatment=soil_surface_preparation, tags={"pbv_2058_mound", "style_siteprep_regen"}),
                    Event(treatment=regeneration, static_parameters=planting(2, 350.0, 1.05, 6.0), tags={"pbv_2058_mound_spruce", "style_regeneration_path"}),
                ]),
            ])],
        ),
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2075),
}


__all__ = ["control_structure"]
