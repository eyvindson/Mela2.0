from lukefi.metsi.domain.conditions import TimePoints
from lukefi.metsi.domain.forestry_types import ForestCondition
from lukefi.metsi.domain.natural_processes.grow_acta import grow_acta_fn
from lukefi.metsi.domain.pre_ops import generate_reference_trees, preproc_filter, scale_area_weight
from lukefi.metsi.sim.generators import Alternatives, Event, Sequence
from lukefi.metsi.sim.sim_configuration import Transition
from lukefi.metsi.sim.simulation_instruction import SimulationInstruction
from lukefi.metsi.sim.treatment import do_nothing

from user_events import Harvest20percent, MarkRetentionTrees, Mounding, PlantingPines


control_structure = {
    "app_configuration": {
        "state_format": "vmi13",
        "run_modes": ["preprocess", "simulate"],
        "preprocessing_output_file": "prepro_regeneration_pathways",
        "simulation_output_file": "sim_regeneration_pathways",
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
        # Regeneration decision: six pathways.
        SimulationInstruction(
            conditions=[TimePoints([2030])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"regen_2030_none"}),
                Harvest20percent(tags={"regen_2030_light_thin"}),
                Sequence([MarkRetentionTrees(tags={"regen_2030_retention"}), Harvest20percent(tags={"regen_2030_retention_plus_thin"})]),
                Sequence([Mounding(tags={"regen_2030_mound"}), PlantingPines(tags={"regen_2030_plant_pine"})]),
                Sequence([MarkRetentionTrees(tags={"regen_2030_retention"}), Mounding(tags={"regen_2030_mound"}), PlantingPines(tags={"regen_2030_plant"})]),
                Sequence([Mounding(tags={"regen_2030_mound"}), PlantingPines(parameters={"species": 2, "stems_per_ha": 1800.0}, tags={"regen_2030_plant_spruce"})]),
            ])],
        ),
        # Follow-up decisions provide additional combinatorics (6 * 5 * 4 = 120 pathways).
        SimulationInstruction(
            conditions=[TimePoints([2040])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"followup_2040_none"}),
                Harvest20percent(tags={"followup_2040_thin"}),
                MarkRetentionTrees(tags={"followup_2040_retention"}),
                Sequence([Mounding(tags={"followup_2040_mound"}), PlantingPines(tags={"followup_2040_replant"})]),
                Sequence([Harvest20percent(tags={"followup_2040_thin"}), MarkRetentionTrees(tags={"followup_2040_retention"})]),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2050])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"followup_2050_none"}),
                Harvest20percent(tags={"followup_2050_thin"}),
                MarkRetentionTrees(tags={"followup_2050_retention"}),
                Sequence([Harvest20percent(tags={"followup_2050_thin"}), Harvest20percent(tags={"followup_2050_second_thin"})]),
            ])],
        ),
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2065),
}


__all__ = ["control_structure"]
