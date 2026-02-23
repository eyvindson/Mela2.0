import numpy as np

from lukefi.metsi.data.model import ForestStand
from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.data.util.select_units import SelectionSet, SelectionTarget
from lukefi.metsi.data.enums.mela import MelaMethodOfTheLastCutting
from lukefi.metsi.domain.conditions import TimePoints
from lukefi.metsi.domain.forestry_types import ForestCondition
from lukefi.metsi.domain.natural_processes.grow_acta import grow_acta_fn
from lukefi.metsi.domain.pre_ops import generate_reference_trees, preproc_filter, scale_area_weight
from lukefi.metsi.forestry.harvest.cutting import cutting
from lukefi.metsi.sim.generators import Alternatives, Event
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

    return cutting(
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


thinning_from_below = Treatment(thinning_from_below_fn, "thinning_from_below")
continuous_cover_cut = Treatment(continuous_cover_cut_fn, "continuous_cover_cut")
final_felling = Treatment(final_felling_fn, "final_felling")


# --- Time structure ---
START_YEAR = 2020
END_YEAR = 2050
STEP_YEARS = 5

TIME_POINTS = list(range(START_YEAR, END_YEAR + 1, STEP_YEARS))
LAST4 = TIME_POINTS[-4:]  # final felling allowed here
PRE_FINAL_YEARS = sorted({y - 15 for y in LAST4 if (y - 15) in TIME_POINTS})
CCC_YEARS = sorted({START_YEAR + 15 * k for k in range(1, 100) if (START_YEAR + 15 * k) in TIME_POINTS})


def management_alternatives_for_year(year: int):
    alts = [
        Event(treatment=do_nothing, static_parameters={"n": 1}, tags={"do_nothing", f"year_{year}"}),
    ]

    if year in CCC_YEARS:
        alts.append(
            Event(
                treatment=continuous_cover_cut,
                tags={"continuous_cover_cut", f"year_{year}", "style_continuous_cover"},
                db_output=True,
            )
        )

    if year in PRE_FINAL_YEARS:
        alts.append(
            Event(
                treatment=thinning_from_below,
                tags={"thinning_from_below", f"year_{year}", "style_thinning_dominated"},
                db_output=True,
            )
        )

    if year in LAST4:
        alts.append(
            Event(
                treatment=final_felling,
                tags={"final_felling", f"year_{year}", "style_shortened_rotation"},
                db_output=True,
            )
        )

    return Alternatives(alts)


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
    "simulation_instructions": [
        SimulationInstruction(
            conditions=[TimePoints([year])],
            events=[management_alternatives_for_year(year)],
        )
        for year in TIME_POINTS
    ],
    "transition": Transition(grow_acta_fn, step=STEP_YEARS),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= END_YEAR),
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
