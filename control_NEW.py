import numpy as np

from lukefi.metsi.data.model import ForestStand
from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.data.util.select_units import SelectionSet, SelectionTarget
from lukefi.metsi.data.enums.mela import MelaMethodOfTheLastCutting
from lukefi.metsi.domain.collected_data import RemovedTrees
from lukefi.metsi.domain.forestry_types import ForestCondition
from lukefi.metsi.domain.natural_processes.grow_acta import grow_acta_fn
from lukefi.metsi.domain.pre_ops import generate_reference_trees, preproc_filter, scale_area_weight
from lukefi.metsi.forestry.harvest.cutting import cutting
from lukefi.metsi.sim.generators import Alternatives, Event, Sequence
from lukefi.metsi.sim.sim_configuration import Transition
from lukefi.metsi.sim.simulation_instruction import SimulationInstruction
from lukefi.metsi.sim.treatment import Treatment, do_nothing


# --- Real treatment wrappers ---
def _apply_cut(
    stand: ForestStand,
    /,
    *,
    removal_share: float,
    cutting_method: int,
    low_diameter_bias: float,
):
    def s_all(_stand: ForestStand, trees: ReferenceTrees) -> np.ndarray:
        return np.ones(trees.size, dtype=bool)

    tree_selection = {
        "target": SelectionTarget("relative", "stems_per_ha", removal_share),
        "sets": [
            SelectionSet[ForestStand, ReferenceTrees](
                s_all,
                "breast_height_diameter",
                "stems_per_ha",
                "relative",
                1.0,
                profile_x=[0, 1],
                profile_y=[low_diameter_bias, max(0.02, 1.0 - low_diameter_bias)],
                profile_xmode="relative",
            )
        ],
    }

    return cutting.treatment_fn(
        stand,
        tree_selection=tree_selection,
        cutting_method=cutting_method,
        mode="odds_units",
    )


def thinning_from_below_fn(stand: ForestStand, /, **_kwargs):
    return _apply_cut(
        stand,
        removal_share=0.22,
        cutting_method=MelaMethodOfTheLastCutting.THINNING.value,
        low_diameter_bias=0.75,
    )


def continuous_cover_cut_fn(stand: ForestStand, /, **_kwargs):
    return _apply_cut(
        stand,
        removal_share=0.14,
        cutting_method=MelaMethodOfTheLastCutting.SHELTERWOOD_CUTTING.value,
        low_diameter_bias=0.40,
    )


def final_felling_fn(stand: ForestStand, /, **_kwargs):
    return _apply_cut(
        stand,
        removal_share=0.96,
        cutting_method=MelaMethodOfTheLastCutting.CLEARCUTTING.value,
        low_diameter_bias=0.50,
    )


thinning_from_below = Treatment(thinning_from_below_fn, "thinning_from_below", collected_data={RemovedTrees})
continuous_cover_cut = Treatment(continuous_cover_cut_fn, "continuous_cover_cut", collected_data={RemovedTrees})
final_felling = Treatment(final_felling_fn, "final_felling", collected_data={RemovedTrees})


control_structure = {
    "app_configuration": {
        "state_format": "vmi13",
        "run_modes": ["preprocess", "export_prepro", "simulate"],
        "preprocessing_output_file": "preprocessing_results_NEW",
        "simulation_output_file": "simulation_results_NEW",
    },
    "preprocessing_operations": [
        scale_area_weight,
        generate_reference_trees,
        preproc_filter,
    ],
    "preprocessing_params": {
        generate_reference_trees: [
            {
                "n_trees": 10,
                "method": "weibull",
                "debug": False,
            }
        ],
        preproc_filter: [
            {
                "remove trees": (lambda trees: (trees.sapling != 0) | (trees.stems_per_ha == 0)),
                "remove stands": (lambda stand: (stand.site_type_category is None) or (stand.site_type_category == 0)),
            }
        ],
    },
    # Keep structure close to original control.py: one SimulationInstruction with one Alternatives tree.
    "simulation_instructions": [
        SimulationInstruction(
            events=[
                Alternatives([
                    Event(treatment=do_nothing, static_parameters={"n": 1}, tags={"first_type", "do_nothing"}),
                    Event(
                        treatment=final_felling,
                        static_parameters={"n": 7},
                        tags={"final_felling_only", "style_shortened_rotation"},
                        db_output=True,
                    ),
                ])
            ]
        )
    ],
    "transition": Transition(grow_acta_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2050),
    "post_processing": {
        "operation_params": {
            do_nothing: [
                {"param": "value"}
            ]
        },
        "post_processing": [
            do_nothing
        ],
    },
    "export_prepro": {
        "csv": {},
    },
}

__all__ = ["control_structure"]
