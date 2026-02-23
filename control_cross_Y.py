import csv
import numpy as np
import sqlite3
import json
from pathlib import Path

from lukefi.metsi.data.model import ForestStand
from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.data.util.select_units import SelectionSet, SelectionTarget
from lukefi.metsi.data.enums.mela import MelaMethodOfTheLastCutting
from lukefi.metsi.domain.conditions import TimeSinceTreatment
from lukefi.metsi.domain.collected_data import RemovedTrees
from lukefi.metsi.domain.forestry_types import ForestCondition
from lukefi.metsi.domain.ecosystem_services.jyu_ecosystem_services import calculate_jyu_ecosystem_services
from lukefi.metsi.domain.forestry_treatments.regeneration import regeneration
from lukefi.metsi.domain.natural_processes.grow_acta import grow_acta_fn
from lukefi.metsi.domain.natural_processes.grow_metsi import grow_metsi_fn
from lukefi.metsi.domain.pre_ops import generate_reference_trees, preproc_filter, scale_area_weight
from lukefi.metsi.forestry.volume import tree_volumes
from lukefi.metsi.forestry.harvest.cutting import cutting
from lukefi.metsi.sim.collected_data import CollectedData
from lukefi.metsi.sim.generators import Alternatives, Event, Sequence
from lukefi.metsi.sim.sim_configuration import Transition
from lukefi.metsi.sim.simulation_instruction import SimulationInstruction
from lukefi.metsi.sim.treatment import Treatment, do_nothing


PARAM_DIR = Path("data/parameter_files")
PARAM_FILES = {
    "timber_price_table": str(PARAM_DIR / "timber_price_table.csv"),
    "thinning_limits": str(PARAM_DIR / "Thin.txt"),
    "min_stems": str(PARAM_DIR / "min_stems.csv"),
    "planting_instructions": str(PARAM_DIR / "planting_instructions.txt"),
    "renewal_ages": str(PARAM_DIR / "renewal_ages_southernFI.txt"),
    "renewal_diameters": str(PARAM_DIR / "renewal_diameters_southernFI.txt"),
}


def _load_default_planting_stems(path: str) -> float:
    vals: list[float] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                vals.append(float(row["min_stems"]))
            except (ValueError, KeyError):
                continue
    return max(vals) if vals else 1200.0


DEFAULT_SPRUCE_STEMS = _load_default_planting_stems(PARAM_FILES["min_stems"])


_LAST_REMOVED_BY_STAND: dict[str, ReferenceTrees] = {}
_LAST_CROSSCUT_VALUE_BY_STAND: dict[str, float] = {}
_LAST_RENEWAL_COST_BY_STAND: dict[str, float] = {}
_RENEWAL_COST_TABLE_CACHE: dict[str, dict[str, float]] = {}
_LAND_VALUE_TABLE_CACHE: dict[str, dict] = {}


class CrossCutRows(CollectedData):
    species: np.ndarray
    timber_grade: np.ndarray
    volume_per_ha: np.ndarray
    value_per_ha: np.ndarray

    @classmethod
    def init_db_table(cls, db: sqlite3.Connection):
        db.cursor().execute(
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
                "INSERT INTO cross_cutting VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
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


class NPVRow(CollectedData):
    interest_rate: float
    harvest_revenue_per_ha: float
    renewal_cost_per_ha: float
    land_value_per_ha: float
    npv_per_ha: float

    @classmethod
    def init_db_table(cls, db: sqlite3.Connection):
        db.cursor().execute(
            """
            CREATE TABLE npv_results(
                node TEXT,
                stand TEXT,
                interest_rate REAL,
                harvest_revenue_per_ha REAL,
                renewal_cost_per_ha REAL,
                land_value_per_ha REAL,
                npv_per_ha REAL,
                PRIMARY KEY (node, stand),
                FOREIGN KEY (node, stand) REFERENCES nodes(identifier, stand)
            )
            """
        )

    def output_to_db(self, db: sqlite3.Connection, node_str: str, identifier: str):
        db.cursor().execute(
            "INSERT INTO npv_results VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                node_str,
                identifier,
                float(self.interest_rate),
                float(self.harvest_revenue_per_ha),
                float(self.renewal_cost_per_ha),
                float(self.land_value_per_ha),
                float(self.npv_per_ha),
            ),
        )


def _read_renewal_costs(path: str) -> dict[str, float]:
    if path in _RENEWAL_COST_TABLE_CACHE:
        return _RENEWAL_COST_TABLE_CACHE[path]
    out: dict[str, float] = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            op = str(row.get("operation", "")).strip()
            try:
                c = float(str(row.get("cost_per_ha", "")).strip())
            except ValueError:
                continue
            if op:
                out[op] = c
    _RENEWAL_COST_TABLE_CACHE[path] = out
    return out


def _read_land_values(path: str) -> dict:
    if path in _LAND_VALUE_TABLE_CACHE:
        return _LAND_VALUE_TABLE_CACHE[path]
    obj = json.load(open(path, encoding="utf-8"))
    _LAND_VALUE_TABLE_CACHE[path] = obj
    return obj


def _land_value_for_stand(stand: ForestStand, rate: float, table: dict) -> float:
    # conservative default mapping for common mineral soil stands
    site_map = {
        1: "very_rich_sites",
        2: "rich_sites",
        3: "damp_sites",
        4: "sub_dry_sites",
        5: "dry_sites",
        6: "barren_sites",
        7: "rocky_or_sandy_sites",
    }
    site_key = site_map.get(int(stand.site_type_category or 4), "sub_dry_sites")
    bucket = table.get("mineral_soils", {})
    rates = bucket.get(site_key, {})
    return float(rates.get(str(int(rate)), 0.0))


def _apply_cut(stand: ForestStand, /, *, removal_share: float, cutting_method: int, low_diameter_bias: float):
    def s_all(_stand: ForestStand, trees: ReferenceTrees) -> np.ndarray:
        return np.ones(trees.size, dtype=bool)

    tree_selection = {
        "target": SelectionTarget("relative", "stems_per_ha", removal_share),
        "sets": [SelectionSet[ForestStand, ReferenceTrees](
            s_all,
            "breast_height_diameter",
            "stems_per_ha",
            "relative",
            1.0,
            # Use absolute x-scale to avoid zero-width relative intervals when
            # all trees in a set have identical diameter.
            profile_x=[0.0, 100.0],
            profile_y=[low_diameter_bias, max(0.02, 1.0 - low_diameter_bias)],
            profile_xmode="absolute",
        )],
    }
    # Use scale mode to avoid odds-space singularities when probabilities hit 0/1.
    return cutting.treatment_fn(stand, tree_selection=tree_selection, cutting_method=cutting_method, mode="scale")


def thinning_from_below_fn(stand: ForestStand, /, **_kwargs):
    return _apply_cut(stand, removal_share=0.22, cutting_method=MelaMethodOfTheLastCutting.THINNING.value, low_diameter_bias=0.75)


def continuous_cover_cut_fn(stand: ForestStand, /, **_kwargs):
    return _apply_cut(stand, removal_share=0.14, cutting_method=MelaMethodOfTheLastCutting.SHELTERWOOD_CUTTING.value, low_diameter_bias=0.40)


def final_felling_fn(stand: ForestStand, /, **_kwargs):
    updated, collected = _apply_cut(stand, removal_share=0.96, cutting_method=MelaMethodOfTheLastCutting.CLEARCUTTING.value, low_diameter_bias=0.50)
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
    timber_grade = np.where(removed.breast_height_diameter >= 18.0, 1, np.where(removed.breast_height_diameter >= 10.0, 2, 3))
    prices = np.vectorize(lambda g: {1: 75.0, 2: 45.0, 3: 20.0}[int(g)])(timber_grade)
    value_per_ha = vol_per_ha * prices

    pairs = np.column_stack((removed.species.astype(int), timber_grade.astype(int)))
    uniq, inv = np.unique(pairs, axis=0, return_inverse=True)
    agg_vol = np.zeros(len(uniq), dtype=float)
    agg_val = np.zeros(len(uniq), dtype=float)
    for i, idx in enumerate(inv):
        agg_vol[idx] += float(vol_per_ha[i])
        agg_val[idx] += float(value_per_ha[i])

    cc = CrossCutRows()
    cc.species = uniq[:, 0]
    cc.timber_grade = uniq[:, 1]
    cc.volume_per_ha = agg_vol
    cc.value_per_ha = agg_val
    _LAST_CROSSCUT_VALUE_BY_STAND[str(stand.identifier)] = float(np.sum(agg_val))
    return stand, [cc]


def calculate_npv_fn(stand: ForestStand, /, **_kwargs):
    interest_rates = _kwargs.get("interest_rates", [3])
    r = float(interest_rates[0]) if interest_rates else 3.0
    renewal_costs_file = _kwargs.get("renewal_costs")
    land_values_file = _kwargs.get("land_values")

    stand_id = str(stand.identifier)
    h = _LAST_CROSSCUT_VALUE_BY_STAND.get(stand_id, 0.0)

    c = _LAST_RENEWAL_COST_BY_STAND.get(stand_id, 0.0)
    if c == 0.0 and stand.artificial_regeneration_year is not None and renewal_costs_file:
        ctab = _read_renewal_costs(str(renewal_costs_file))
        c = float(ctab.get("planting", 0.0))

    lv = 0.0
    if land_values_file:
        lv = _land_value_for_stand(stand, r, _read_land_values(str(land_values_file)))

    npv = h - c + lv

    row = NPVRow()
    row.interest_rate = r
    row.harvest_revenue_per_ha = h
    row.renewal_cost_per_ha = c
    row.land_value_per_ha = lv
    row.npv_per_ha = npv
    return stand, [row]


def regeneration_with_cost_fn(stand: ForestStand, /, **_kwargs):
    updated, collected = regeneration.treatment_fn(stand, **_kwargs)
    renewal_costs_file = _kwargs.get("renewal_costs")
    if renewal_costs_file:
        ctab = _read_renewal_costs(str(renewal_costs_file))
        _LAST_RENEWAL_COST_BY_STAND[str(updated.identifier)] = float(ctab.get("planting", 0.0))
    return updated, collected


thinning_from_below = Treatment(thinning_from_below_fn, "thinning_from_below", collected_data={RemovedTrees})
continuous_cover_cut = Treatment(continuous_cover_cut_fn, "continuous_cover_cut", collected_data={RemovedTrees})
final_felling = Treatment(final_felling_fn, "final_felling", collected_data={RemovedTrees})
cross_cut_felled_trees = Treatment(cross_cut_felled_trees_fn, "cross_cut_felled_trees", collected_data={CrossCutRows})
calculate_npv = Treatment(calculate_npv_fn, "calculate_npv", collected_data={NPVRow})
regeneration_with_cost = Treatment(regeneration_with_cost_fn, "regeneration")


basal_area_gt_15 = ForestCondition(lambda payload: (payload.computational_unit.basal_area is not None) and (payload.computational_unit.basal_area > 15.0), name="basal_area_gt_15")
basal_area_between_7_and_12 = ForestCondition(lambda payload: (payload.computational_unit.basal_area is not None) and (7.0 <= payload.computational_unit.basal_area <= 12.0), name="basal_area_between_7_and_12")
continuous_cover_every_15y = TimeSinceTreatment(15, continuous_cover_cut)
no_trees_on_stand = ForestCondition(lambda payload: payload.computational_unit.reference_trees.size == 0, name="no_trees_on_stand")


control_structure = {
    "app_configuration": {
        "state_format": "vmi13", # options: fdm, vmi12, vmi13, xml, gpkg
        "run_modes": ["preprocess", "export_prepro", "simulate"],
        "preprocessing_output_file": "preprocessing_results_Y",
        "simulation_output_file": "simulation_results_Y",
    },
    "preprocessing_operations": [scale_area_weight, generate_reference_trees, preproc_filter],
    "preprocessing_params": {
        generate_reference_trees: [{"n_trees": 10, "method": "weibull", "debug": False}],
        preproc_filter: [{
            "remove trees": (lambda trees: (trees.sapling != 0) | (trees.stems_per_ha == 0)),
            "remove stands": (lambda stand: (stand.site_type_category is None) or (stand.site_type_category == 0)),
        }],
    },
    "operation_file_params": {
        "cross_cut_felled_trees": {"timber_price_table": PARAM_FILES["timber_price_table"]},
        "continuous_cover_cut": {"thinning_limits": PARAM_FILES["thinning_limits"]},
        "final_felling": {
            "clearcutting_limits_ages": PARAM_FILES["renewal_ages"],
            "clearcutting_limits_diameters": PARAM_FILES["renewal_diameters"],
        },
        "regeneration": {"planting_instructions": PARAM_FILES["planting_instructions"]},
        "calculate_npv": {
            "renewal_costs": str(PARAM_DIR / "renewal_operation_pricing.csv"),
            "land_values": str(PARAM_DIR / "land_values_per_site_type_and_interest_rate.json"),
        },
    },
    "operation_params": {
        "calculate_npv": [
            {"interest_rates": [3]}
        ]
    },
    "simulation_instructions": [
    SimulationInstruction(
        events=[
            Sequence(
                [
                    Alternatives(
                        [
                            Event(treatment=do_nothing, static_parameters={"n": 1}, tags={"first_type", "do_nothing"}),

                            Event(treatment=final_felling, static_parameters={"n": 7}, tags={"final_felling_only"},
                                  preconditions=[basal_area_gt_15], db_output=True),

                            Sequence([
                                Event(treatment=final_felling, static_parameters={"n": 8},
                                      tags={"final_felling_then_cross_cut"}, preconditions=[basal_area_gt_15], db_output=True),
                                Event(treatment=cross_cut_felled_trees, static_parameters={"implementation": "py"},
                                      file_parameters={"timber_price_table": PARAM_FILES["timber_price_table"]},
                                      tags={"cross_cut_felled_trees"}, db_output=True),
                                Event(treatment=calculate_npv,
                                      static_parameters={"interest_rates": [3]},
                                      file_parameters={
                                          "renewal_costs": str(PARAM_DIR / "renewal_operation_pricing.csv"),
                                          "land_values": str(PARAM_DIR / "land_values_per_site_type_and_interest_rate.json"),
                                      },
                                      tags={"npv"}, db_output=True),
                            ]),

                            Event(treatment=continuous_cover_cut, static_parameters={"n": 9},
                                  file_parameters={"thinning_limits": PARAM_FILES["thinning_limits"]},
                                  tags={"continuous_cover_cut_only"},
                                  preconditions=[basal_area_gt_15, continuous_cover_every_15y], db_output=True),

                            Sequence([
                                Event(treatment=continuous_cover_cut, static_parameters={"n": 10},
                                      file_parameters={"thinning_limits": PARAM_FILES["thinning_limits"]},
                                      tags={"continuous_cover_then_cross_cut"},
                                      preconditions=[basal_area_gt_15, continuous_cover_every_15y], db_output=True),
                                Event(treatment=cross_cut_felled_trees, static_parameters={"implementation": "py"},
                                      file_parameters={"timber_price_table": PARAM_FILES["timber_price_table"]},
                                      tags={"cross_cut_felled_trees"}, db_output=True),
                                Event(treatment=calculate_npv,
                                      static_parameters={"interest_rates": [3]},
                                      file_parameters={
                                          "renewal_costs": str(PARAM_DIR / "renewal_operation_pricing.csv"),
                                          "land_values": str(PARAM_DIR / "land_values_per_site_type_and_interest_rate.json"),
                                      },
                                      tags={"npv"}, db_output=True),
                            ]),

                            Event(treatment=regeneration_with_cost,
                                  static_parameters={
                                      "origin": 2,
                                      "species": 2,
                                      "stems_per_ha": DEFAULT_SPRUCE_STEMS,
                                      "height": 0.7,
                                      "biological_age": 1.0,
                                      "ntrees": 10,
                                      "type": "artificial",
                                  },
                                  file_parameters={
                                      "planting_instructions": PARAM_FILES["planting_instructions"],
                                      "renewal_costs": str(PARAM_DIR / "renewal_operation_pricing.csv"),
                                  },
                                  tags={"spruce_planting_if_empty"},
                                  preconditions=[no_trees_on_stand],
                                  db_output=True),

                            Event(treatment=thinning_from_below, static_parameters={"n": 11},
                                  file_parameters={"thinning_limits": PARAM_FILES["thinning_limits"]},
                                  tags={"thinning_from_below_mid_ba"},
                                  preconditions=[basal_area_between_7_and_12], db_output=True),
                        ]
                    ),

                    # Runs after whichever alternative was taken
                    Event(
                        treatment=calculate_jyu_ecosystem_services,
                        static_parameters={"berry_price_per_kg": 8.0},
                        tags={"jyu_ecosystem_service", "bilberry"},
                        db_output=True,
                    ),
                ]
            )
        ]
    )
],
    "transition": Transition(grow_metsi_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2050),

    
    "export_prepro": {"csv": {}},
}


__all__ = ["control_structure"]
