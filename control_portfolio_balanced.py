from lukefi.metsi.domain.conditions import TimePoints
from lukefi.metsi.domain.forestry_types import ForestCondition
from lukefi.metsi.domain.natural_processes.grow_acta import grow_acta_fn
from lukefi.metsi.domain.pre_ops import generate_reference_trees, preproc_filter, scale_area_weight
from lukefi.metsi.sim.generators import Alternatives, Event, Sequence
from lukefi.metsi.sim.sim_configuration import Transition
from lukefi.metsi.sim.simulation_instruction import SimulationInstruction
from lukefi.metsi.sim.treatment import do_nothing

from user_events import (
    FirstThinningMineralSoils,
    Harvest20percent,
    MarkRetentionTrees,
    Mounding,
    PlantingPines,
    Tracks,
)


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
        # Balanced portfolios with different objectives per period (7 x 7 x 6 = 294 pathways).
        SimulationInstruction(
            conditions=[TimePoints([2025])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"bal_2025_wait"}),
                FirstThinningMineralSoils(tags={"bal_2025_first_thin"}),
                Tracks(tags={"bal_2025_tracks"}),
                Harvest20percent(tags={"bal_2025_light_harvest"}),
                MarkRetentionTrees(tags={"bal_2025_retention"}),
                Sequence([FirstThinningMineralSoils(tags={"bal_2025_first"}), MarkRetentionTrees(tags={"bal_2025_retention"})]),
                Sequence([Harvest20percent(tags={"bal_2025_light"}), Tracks(tags={"bal_2025_tracks"})]),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2040])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"bal_2040_wait"}),
                Tracks(tags={"bal_2040_tracks"}),
                Harvest20percent(tags={"bal_2040_light_harvest"}),
                MarkRetentionTrees(tags={"bal_2040_retention"}),
                Sequence([Mounding(tags={"bal_2040_mound"}), PlantingPines(tags={"bal_2040_replant_pine"})]),
                Sequence([MarkRetentionTrees(tags={"bal_2040_retention"}), Harvest20percent(tags={"bal_2040_followup_harvest"})]),
                Sequence([Harvest20percent(tags={"bal_2040_harvest"}), PlantingPines(parameters={"species": 2, "stems_per_ha": 1800.0}, tags={"bal_2040_enrich_spruce"})]),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2055])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"bal_2055_wait"}),
                Tracks(tags={"bal_2055_tracks"}),
                Harvest20percent(tags={"bal_2055_light_harvest"}),
                MarkRetentionTrees(tags={"bal_2055_retention"}),
                Sequence([Harvest20percent(tags={"bal_2055_harvest"}), MarkRetentionTrees(tags={"bal_2055_retention"})]),
                Sequence([Mounding(tags={"bal_2055_mound"}), PlantingPines(tags={"bal_2055_replant_pine"})]),
            ])],
        ),
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2070),
}


__all__ = ["control_structure"]
