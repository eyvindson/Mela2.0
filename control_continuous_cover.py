from lukefi.metsi.domain.conditions import TimePoints
from lukefi.metsi.domain.forestry_types import ForestCondition
from lukefi.metsi.domain.natural_processes.grow_acta import grow_acta_fn
from lukefi.metsi.domain.pre_ops import generate_reference_trees, preproc_filter, scale_area_weight
from lukefi.metsi.sim.generators import Alternatives, Event, Sequence
from lukefi.metsi.sim.sim_configuration import Transition
from lukefi.metsi.sim.simulation_instruction import SimulationInstruction
from lukefi.metsi.sim.treatment import do_nothing

from user_events import FirstThinningMineralSoils, Harvest20percent, MarkRetentionTrees, Tracks


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
        # Frequent small interventions (5 x 5 x 5 x 4 = 500 portfolios).
        SimulationInstruction(
            conditions=[TimePoints([2025])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"ccf_2025_none"}),
                Tracks(tags={"ccf_2025_tracks"}),
                Harvest20percent(tags={"ccf_2025_20pct"}),
                MarkRetentionTrees(tags={"ccf_2025_retention"}),
                FirstThinningMineralSoils(tags={"ccf_2025_structural"}),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2035])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"ccf_2035_none"}),
                Tracks(tags={"ccf_2035_tracks"}),
                Harvest20percent(tags={"ccf_2035_20pct"}),
                MarkRetentionTrees(tags={"ccf_2035_retention"}),
                Sequence([Tracks(tags={"ccf_2035_tracks"}), MarkRetentionTrees(tags={"ccf_2035_retention"})]),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2045])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"ccf_2045_none"}),
                Tracks(tags={"ccf_2045_tracks"}),
                Harvest20percent(tags={"ccf_2045_20pct"}),
                MarkRetentionTrees(tags={"ccf_2045_retention"}),
                Sequence([Harvest20percent(tags={"ccf_2045_20pct"}), MarkRetentionTrees(tags={"ccf_2045_retention"})]),
            ])],
        ),
        SimulationInstruction(
            conditions=[TimePoints([2055])],
            events=[Alternatives([
                Event(treatment=do_nothing, tags={"ccf_2055_none"}),
                Tracks(tags={"ccf_2055_tracks"}),
                Harvest20percent(tags={"ccf_2055_20pct"}),
                MarkRetentionTrees(tags={"ccf_2055_retention"}),
            ])],
        ),
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2070),
}


__all__ = ["control_structure"]
