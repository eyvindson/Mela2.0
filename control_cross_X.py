import numpy as np
import sqlite3

from lukefi.metsi.data.model import ForestStand
from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.data.util.select_units import SelectionSet, SelectionTarget
from lukefi.metsi.data.enums.mela import MelaMethodOfTheLastCutting
from lukefi.metsi.domain.conditions import TimeSinceTreatment
from lukefi.metsi.domain.collected_data import RemovedTrees
from lukefi.metsi.domain.forestry_types import ForestCondition
from lukefi.metsi.domain.forestry_treatments.regeneration import regeneration
from lukefi.metsi.domain.natural_processes.grow_acta import grow_acta_fn
from lukefi.metsi.domain.pre_ops import generate_reference_trees, preproc_filter, scale_area_weight
from lukefi.metsi.forestry.volume import tree_volumes
from lukefi.metsi.forestry.harvest.cutting import cutting
from lukefi.metsi.sim.collected_data import CollectedData
from lukefi.metsi.sim.generators import Alternatives, Event, Sequence
from lukefi.metsi.sim.sim_configuration import Transition
from lukefi.metsi.sim.simulation_instruction import SimulationInstruction
from lukefi.metsi.sim.treatment import Treatment, do_nothing


# --- Real treatment wrappers ---
_LAST_REMOVED_BY_STAND: dict[str, ReferenceTrees] = {}


class CrossCutRows(CollectedData):
    stand_id: str
    species: np.ndarray
    timber_grade: np.ndarray
    volume_per_ha: np.ndarray
    value_per_ha: np.ndarray

    @classmethod
    def init_db_table(cls, db: sqlite3.Connection):
        cur = db.cursor()
        cur.execute(
            """
            CREATE TABLE cross_cutting(
                node TEXT,
                stand TEXT,
                species INTEGER,
                timber_grade INTEGER,
                volume_per_ha REAL,
                value_per_ha REAL,
                source TEXT,
                operation TEXT,
                PRIMARY KEY (node, stand, species, timber_grade),
                FOREIGN KEY (node, stand) REFERENCES nodes(identifier, stand)
            )
            """
        )

    def output_to_db(self, db: sqlite3.Connection, node_str: str, identifier: str):
        cur = db.cursor()
        for i in range(len(self.species)):
            cur.execute(
                """
                INSERT INTO cross_cutting
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    node_str,
                    identifier,
                    int(self.species[i]),
                    int(self.timber_grade[i]),
                    float(self.volume_per_ha[i]),
                    float(self.value_per_ha[i]),
                    "harvested",
                    "cross_cut_felled_trees",
                ),
            )


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
    updated, collected = _apply_cut(
        stand,
        removal_share=0.96,
        cutting_method=MelaMethodOfTheLastCutting.CLEARCUTTING.value,
        low_diameter_bias=0.50,
    )
    for datum in collected:
        if isinstance(datum, RemovedTrees):
            _LAST_REMOVED_BY_STAND[str(updated.identifier)] = datum.removed_trees
    return updated, collected


def cross_cut_felled_trees_fn(stand: ForestStand, /, **_kwargs):
    removed = _LAST_REMOVED_BY_STAND.get(str(stand.identifier))
    if removed is None or removed.size == 0:
        return stand, []

    vol_tree = tree_volumes(removed, stand.degree_days or 1200.0)
    vol_per_ha = vol_tree * removed.stems_per_ha

    dbh = removed.breast_height_diameter
    timber_grade = np.where(dbh >= 18.0, 1, np.where(dbh >= 10.0, 2, 3))

    # Simple value model placeholder: update with your price table logic if needed.
    price_by_grade = {1: 75.0, 2: 45.0, 3: 20.0}
    prices = np.vectorize(lambda g: price_by_grade[int(g)])(timber_grade)
    value_per_ha = vol_per_ha * prices

    # aggregate by (species, grade)
    pairs = np.column_stack((removed.species.astype(int), timber_grade.astype(int)))
    uniq, inv = np.unique(pairs, axis=0, return_inverse=True)
    agg_vol = np.zeros(len(uniq), dtype=float)
    agg_val = np.zeros(len(uniq), dtype=float)
    for i, idx in enumerate(inv):
        agg_vol[idx] += float(vol_per_ha[i])
        agg_val[idx] += float(value_per_ha[i])

    cc = CrossCutRows()
    cc.stand_id = str(stand.identifier)
    cc.species = uniq[:, 0]
    cc.timber_grade = uniq[:, 1]
    cc.volume_per_ha = agg_vol
    cc.value_per_ha = agg_val
    return stand, [cc]


thinning_from_below = Treatment(thinning_from_below_fn, "thinning_from_below", collected_data={RemovedTrees})
continuous_cover_cut = Treatment(continuous_cover_cut_fn, "continuous_cover_cut", collected_data={RemovedTrees})
final_felling = Treatment(final_felling_fn, "final_felling", collected_data={RemovedTrees})
cross_cut_felled_trees = Treatment(cross_cut_felled_trees_fn, "cross_cut_felled_trees", collected_data={CrossCutRows})

# Harvest only if stand basal area is above threshold.
basal_area_gt_15 = ForestCondition(
    lambda payload: (payload.computational_unit.basal_area is not None)
    and (payload.computational_unit.basal_area > 15.0),
    name="basal_area_gt_15",
)

continuous_cover_every_15y = TimeSinceTreatment(15, continuous_cover_cut)

no_trees_on_stand = ForestCondition(
    lambda payload: payload.computational_unit.reference_trees.size == 0,
    name="no_trees_on_stand",
)

basal_area_between_7_and_12 = ForestCondition(
    lambda payload: (payload.computational_unit.basal_area is not None)
    and (7.0 <= payload.computational_unit.basal_area <= 12.0),
    name="basal_area_between_7_and_12",
)


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
                        preconditions=[basal_area_gt_15],
                        db_output=True,
                    ),
                    Sequence([
                        Event(
                            treatment=final_felling,
                            static_parameters={"n": 8},
                            tags={"final_felling_then_cross_cut", "style_shortened_rotation"},
                            preconditions=[basal_area_gt_15],
                            db_output=True,
                        ),
                        Event(
                            treatment=cross_cut_felled_trees,
                            static_parameters={"implementation": "py"},
                            file_parameters={"timber_price_table": "data/parameter_files/timber_price_table.csv"},
                            tags={"cross_cut_felled_trees"},
                            db_output=True,
                        ),
                    ]),
                    Event(
                        treatment=continuous_cover_cut,
                        static_parameters={"n": 9},
                        tags={"continuous_cover_cut_only", "style_continuous_cover"},
                        preconditions=[basal_area_gt_15, continuous_cover_every_15y],
                        db_output=True,
                    ),
                    Sequence([
                        Event(
                            treatment=continuous_cover_cut,
                            static_parameters={"n": 10},
                            tags={"continuous_cover_then_cross_cut", "style_continuous_cover"},
                            preconditions=[basal_area_gt_15, continuous_cover_every_15y],
                            db_output=True,
                        ),
                        Event(
                            treatment=cross_cut_felled_trees,
                            static_parameters={"implementation": "py"},
                            file_parameters={"timber_price_table": "data/parameter_files/timber_price_table.csv"},
                            tags={"cross_cut_felled_trees"},
                            db_output=True,
                        ),
                    ]),
                    Event(
                        treatment=regeneration,
                        static_parameters={
                            "origin": 2,
                            "species": 2,  # spruce
                            "stems_per_ha": 1800.0,
                            "height": 0.7,
                            "biological_age": 1.0,
                            "ntrees": 10,
                            "type": "artificial",
                        },
                        tags={"spruce_planting_if_empty"},
                        preconditions=[no_trees_on_stand],
                        db_output=True,
                    ),
                    Event(
                        treatment=thinning_from_below,
                        static_parameters={"n": 11},
                        tags={"thinning_from_below_mid_ba"},
                        preconditions=[basal_area_between_7_and_12],
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
