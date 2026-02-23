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


control_structure = {
    "app_configuration": {
        "state_format": "vmi13",
        "run_modes": ["preprocess", "simulate"],
        "preprocessing_output_file": "prepro_continuous_cover",
        "simulation_output_file": "sim_continuous_cover",
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
        # small repeated interventions, 5*5*5*5 = 625 portfolios
        SimulationInstruction(
            conditions=[TimePoints([2025])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"cc_2025_wait"}),
                Event(treatment=soil_surface_preparation, tags={"cc_2025_mound"}),
                Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 1, "stems_per_ha": 400.0, "height": 0.6, "biological_age": 2.0, "type": "artificial"}, tags={"cc_2025_light_pine"}),
                Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 2, "stems_per_ha": 400.0, "height": 0.6, "biological_age": 2.0, "type": "artificial"}, tags={"cc_2025_light_spruce"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 1, "stems_per_ha": 500.0, "height": 0.6, "biological_age": 2.0, "type": "artificial"}, tags={"cc_2025_mound_pine"})]),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2035])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"cc_2035_wait"}),
                Event(treatment=soil_surface_preparation, tags={"cc_2035_mound"}),
                Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 1, "stems_per_ha": 350.0, "height": 0.7, "biological_age": 3.0, "type": "artificial"}, tags={"cc_2035_pine_fill"}),
                Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 2, "stems_per_ha": 350.0, "height": 0.7, "biological_age": 3.0, "type": "artificial"}, tags={"cc_2035_spruce_fill"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 2, "stems_per_ha": 500.0, "height": 0.7, "biological_age": 3.0, "type": "artificial"}, tags={"cc_2035_mound_spruce"})]),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2045])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"cc_2045_wait"}),
                Event(treatment=soil_surface_preparation, tags={"cc_2045_mound"}),
                Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 1, "stems_per_ha": 300.0, "height": 0.8, "biological_age": 4.0, "type": "artificial"}, tags={"cc_2045_pine_fill"}),
                Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 2, "stems_per_ha": 300.0, "height": 0.8, "biological_age": 4.0, "type": "artificial"}, tags={"cc_2045_spruce_fill"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 1, "stems_per_ha": 450.0, "height": 0.8, "biological_age": 4.0, "type": "artificial"}, tags={"cc_2045_mound_pine"})]),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2055])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"cc_2055_wait"}),
                Event(treatment=soil_surface_preparation, tags={"cc_2055_mound"}),
                Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 1, "stems_per_ha": 250.0, "height": 0.9, "biological_age": 5.0, "type": "artificial"}, tags={"cc_2055_pine_fill"}),
                Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 2, "stems_per_ha": 250.0, "height": 0.9, "biological_age": 5.0, "type": "artificial"}, tags={"cc_2055_spruce_fill"}),
                Sequence([Event(treatment=soil_surface_preparation), Event(treatment=regeneration, static_parameters={"origin": 2, "method": 2, "species": 2, "stems_per_ha": 400.0, "height": 0.9, "biological_age": 5.0, "type": "artificial"}, tags={"cc_2055_mound_spruce"})]),
            ])],
        ),
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2070),
}


__all__ = ["control_structure"]
