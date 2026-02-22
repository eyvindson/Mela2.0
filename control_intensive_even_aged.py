from lukefi.metsi.domain.conditions import TimePoints
from lukefi.metsi.domain.forestry_types import ForestCondition
from lukefi.metsi.domain.natural_processes.grow_acta import grow_acta_fn
from lukefi.metsi.domain.pre_ops import generate_reference_trees, preproc_filter, scale_area_weight
from lukefi.metsi.sim.generators import Alternatives, Event, Sequence
from lukefi.metsi.sim.sim_configuration import Transition
from lukefi.metsi.sim.simulation_instruction import SimulationInstruction
from lukefi.metsi.sim.treatment import do_nothing

from user_events import FirstThinningMineralSoils, Harvest20percent, Tracks


control_structure = {
    "app_configuration": {
        "state_format": "vmi13",
        "run_modes": ["preprocess", "simulate"],
        "preprocessing_output_file": "prepro_intensive_even_aged",
        "simulation_output_file": "sim_intensive_even_aged",
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
        # 6 alternatives in each decision point -> 216 complete schedules per stand.
        SimulationInstruction(
            conditions=[TimePoints([2025])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"thin_2025_none"}),
                FirstThinningMineralSoils(tags={"thin_2025_first"}),
                Tracks(tags={"thin_2025_tracks_18"}),
                Sequence([Tracks(tags={"thin_2025_tracks_18"}), Event(treatment=do_nothing, tags={"thin_2025_wait"})]),
                Harvest20percent(tags={"thin_2025_20pct"}),
                Harvest20percent(parameters={"cutting_method": 6}, tags={"thin_2025_alt_method"}),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2035])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"thin_2035_none"}),
                FirstThinningMineralSoils(tags={"thin_2035_first"}),
                Tracks(tags={"thin_2035_tracks_18"}),
                Sequence([Tracks(tags={"thin_2035_tracks_then_wait"}), Event(treatment=do_nothing)]),
                Harvest20percent(tags={"thin_2035_20pct"}),
                Sequence([Harvest20percent(tags={"thin_2035_20_then_wait"}), Event(treatment=do_nothing)]),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2045])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"thin_2045_none"}),
                Tracks(tags={"thin_2045_tracks_18"}),
                Harvest20percent(tags={"thin_2045_20pct"}),
                Harvest20percent(parameters={"cutting_method": 6}, tags={"thin_2045_custom_method"}),
                Sequence([Tracks(tags={"thin_2045_tracks"}), Harvest20percent(tags={"thin_2045_followup_20pct"})]),
                Sequence([Harvest20percent(tags={"thin_2045_20pct"}), Harvest20percent(tags={"thin_2045_second_20pct"})]),
            ])],
        ),
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2060),
}


__all__ = ["control_structure"]
