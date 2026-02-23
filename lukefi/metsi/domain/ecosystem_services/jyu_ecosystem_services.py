from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
import sqlite3
from typing import TYPE_CHECKING, Any
import numpy as np

from lukefi.metsi.data.enums.internal import TreeSpecies
from lukefi.metsi.forestry.volume import tree_volumes
from lukefi.metsi.sim.collected_data import CollectedData, OpTuple
from lukefi.metsi.sim.treatment import Treatment


if TYPE_CHECKING:
    from lukefi.metsi.data.model import ForestStand


class _Matrix:
    def __init__(self, rows: int, cols: int, fill: float = 0.0):
        self.data = [[fill for _ in range(cols)] for _ in range(rows)]

    def __getitem__(self, idx):
        i, j = idx
        return self.data[i][j]

    def __setitem__(self, idx, value):
        i, j = idx
        self.data[i][j] = value


@dataclass
class _LegacyModelArgs:
    variables: _Matrix
    mem: _Matrix
    num_of_res_objs: list[int]
    errors: list[str]


def _load_model_function(module_name: str, function_name: str):
    root = Path(__file__).resolve().parents[4]
    module_path = root / "ES_models" / f"{module_name}.py"
    source = module_path.read_text(encoding="utf-8-sig")
    source = source.replace("	", "    ")
    module_globals: dict[str, Any] = {}
    exec(compile(source, str(module_path), "exec"), module_globals)
    return module_globals[function_name]


def _species_metrics(stand: "ForestStand") -> dict[str, float]:
    trees = stand.reference_trees
    out = {
        "ba_total": 0.0,
        "ba_pine": 0.0,
        "ba_spruce": 0.0,
        "ba_birch": 0.0,
        "ba_aspen": 0.0,
        "ba_dec_other": 0.0,
        "vol_total": 0.0,
        "vol_pine": 0.0,
        "vol_spruce": 0.0,
        "vol_birch": 0.0,
        "vol_aspen": 0.0,
        "stems_total": 0.0,
    }

    tree_count = getattr(trees, "size", 0)
    volumes = getattr(trees, "volume", None)

    tree_volumes_m3 = np.full(tree_count, np.nan, dtype=float)
    if volumes is not None and len(volumes) >= tree_count:
        # Ensure the array is always writable. Some upstream vectorized slices can be read-only,
        # and we patch missing/non-finite values in-place below.
        tree_volumes_m3 = np.array(volumes[:tree_count], dtype=float, copy=True)

    missing_volume = ~np.isfinite(tree_volumes_m3)
    if tree_count > 0 and np.any(missing_volume):
        estimated_volumes = tree_volumes(trees, float(getattr(stand, "degree_days", 0.0) or 0.0))
        tree_volumes_m3[missing_volume] = estimated_volumes[missing_volume]

    tree_volumes_m3[~np.isfinite(tree_volumes_m3)] = 0.0

    for i in range(tree_count):
        stems = float(trees.stems_per_ha[i])
        species = int(trees.species[i])
        dbh = float(trees.breast_height_diameter[i])
        ba = stems * (math.pi * (dbh / 200.0) ** 2)
        vol = stems * float(tree_volumes_m3[i])

        out["ba_total"] += ba
        out["vol_total"] += vol
        out["stems_total"] += stems

        if species == int(TreeSpecies.PINE):
            out["ba_pine"] += ba
            out["vol_pine"] += vol
        elif species == int(TreeSpecies.SPRUCE):
            out["ba_spruce"] += ba
            out["vol_spruce"] += vol
        elif species in (int(TreeSpecies.SILVER_BIRCH), int(TreeSpecies.DOWNY_BIRCH)):
            out["ba_birch"] += ba
            out["vol_birch"] += vol
        elif species == int(TreeSpecies.ASPEN):
            out["ba_aspen"] += ba
            out["vol_aspen"] += vol
            out["ba_dec_other"] += ba
        else:
            try:
                if TreeSpecies(species).is_deciduous():
                    out["ba_dec_other"] += ba
            except ValueError:
                pass

    if out["ba_total"] <= 0.0:
        out["ba_total"] = float(getattr(stand, "basal_area", 0.0) or 0.0)

    if out["ba_total"] <= 0.0:
        strata = stand.tree_strata
        stratum_count = getattr(strata, "size", 0)
        for i in range(stratum_count):
            species = int(strata.species[i])
            ba = float(strata.basal_area[i] if np.isfinite(strata.basal_area[i]) else 0.0)
            height = float(strata.mean_height[i] if np.isfinite(strata.mean_height[i]) else 0.0)

            # Form-factor approximation for stand-level volume when only strata are available.
            vol = ba * height * 0.45

            out["ba_total"] += ba
            out["vol_total"] += vol

            if species == int(TreeSpecies.PINE):
                out["ba_pine"] += ba
                out["vol_pine"] += vol
            elif species == int(TreeSpecies.SPRUCE):
                out["ba_spruce"] += ba
                out["vol_spruce"] += vol
            elif species in (int(TreeSpecies.SILVER_BIRCH), int(TreeSpecies.DOWNY_BIRCH)):
                out["ba_birch"] += ba
                out["vol_birch"] += vol
            elif species == int(TreeSpecies.ASPEN):
                out["ba_aspen"] += ba
                out["vol_aspen"] += vol
                out["ba_dec_other"] += ba
            else:
                try:
                    if TreeSpecies(species).is_deciduous():
                        out["ba_dec_other"] += ba
                except ValueError:
                    pass

    return out


def _run_legacy_model(function: Any, variables: list[float], n_outputs: int) -> list[float]:
    vars_matrix = _Matrix(len(variables), 1)
    for i, value in enumerate(variables):
        vars_matrix[i, 0] = float(value)

    arg = _LegacyModelArgs(
        variables=vars_matrix,
        mem=_Matrix(n_outputs, 1),
        num_of_res_objs=[0],
        errors=[""],
    )
    function(arg, 0)
    return [float(arg.mem[i, 0]) for i in range(n_outputs)]


def _stand_age(stand: "ForestStand") -> float:
    age = float(getattr(stand, "dominant_storey_age", 0.0) or 0.0)
    if age > 0.0:
        return age

    trees = stand.reference_trees
    tree_count = getattr(trees, "size", 0)
    biological_ages = getattr(trees, "biological_age", None)
    weighted_age_sum = 0.0
    weight_sum = 0.0

    for i in range(tree_count):
        tree_age = float((biological_ages[i] if biological_ages is not None else 0.0) or 0.0)
        if tree_age <= 0.0:
            continue

        stems = float(trees.stems_per_ha[i])
        if stems <= 0.0:
            continue

        weighted_age_sum += tree_age * stems
        weight_sum += stems

    if weight_sum > 0.0:
        return weighted_age_sum / weight_sum

    return age

class JyuEcosystemServices(CollectedData):
    stand_id: str
    bilberry_yield_kg_ha: float
    cowberry_yield_kg_ha: float
    cep_yield_kg_ha: float
    mushroom_yield_kg_ha: float
    siberian_flying_squirrel_hsi: float
    long_tailed_tit_hsi: float
    hazel_grouse_hsi: float
    capercaillie_hsi: float
    three_toed_woodpecker_hsi: float

    @classmethod
    def init_db_table(cls, db: sqlite3.Connection):
        db.execute(
            """
            CREATE TABLE jyu_ecosystem_services(
                node TEXT,
                stand TEXT,
                identifier TEXT,
                bilberry_yield_kg_ha REAL,
                cowberry_yield_kg_ha REAL,
                cep_yield_kg_ha REAL,
                mushroom_yield_kg_ha REAL,
                siberian_flying_squirrel_hsi REAL,
                long_tailed_tit_hsi REAL,
                hazel_grouse_hsi REAL,
                capercaillie_hsi REAL,
                three_toed_woodpecker_hsi REAL,
                PRIMARY KEY (node, identifier),
                FOREIGN KEY (node, stand) REFERENCES nodes(identifier, stand)
            )
            """
        )

    def output_to_db(self, db: sqlite3.Connection, node_str: str, identifier: str):
        db.execute(
            """
            INSERT INTO jyu_ecosystem_services VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                node_str,
                identifier,
                f"{identifier}_jyu_ecosystem_services",
                self.bilberry_yield_kg_ha,
                self.cowberry_yield_kg_ha,
                self.cep_yield_kg_ha,
                self.mushroom_yield_kg_ha,
                self.siberian_flying_squirrel_hsi,
                self.long_tailed_tit_hsi,
                self.hazel_grouse_hsi,
                self.capercaillie_hsi,
                self.three_toed_woodpecker_hsi,
            ),
        )


def calculate_jyu_ecosystem_services_fn(input_: "ForestStand", /, **_operation_parameters) -> OpTuple["ForestStand"]:
    metrics = _species_metrics(input_)
    ba_total = max(metrics["ba_total"], 0.0001)
    vol_total = max(metrics["vol_total"], 0.0001)

    site = float(getattr(input_, "site_type_category", 0) or 0)
    main_species = float(getattr(input_, "main_tree_species_dominant_storey", TreeSpecies.PINE) or TreeSpecies.PINE)
    temp_sum = float(getattr(input_, "degree_days", 1200.0) or 1200.0)
    age = _stand_age(input_)
    altitude = float((getattr(input_, "geo_location", None) or (0.0, 0.0, 0.0))[2] or 0.0)

    ba_prop_sp = 100.0 * metrics["ba_pine"] / ba_total
    ba_prop_ns = 100.0 * metrics["ba_spruce"] / ba_total
    ba_prop_birch = 100.0 * metrics["ba_birch"] / ba_total

    bilberry_fn = _load_model_function("bilberry_jyu", "Bilberry_jyu")
    cowberry_fn = _load_model_function("cowberry_jyu", "Cowberry_jyu")
    cep_fn = _load_model_function("cep_jyu", "Cep_jyu")
    mushroom_fn = _load_model_function("mushroom_jyu", "Mushroom_jyu")
    collectables_fn = _load_model_function("collectables_jyu", "Collectables_jyu")
    squirrel_fn = _load_model_function("siberian_flying_squirrel_jyu", "Siberian_flying_squirrel_jyu")
    tit_fn = _load_model_function("long_tailed_tit_jyu", "Long_tailed_tit_jyu")
    hazel_fn = _load_model_function("hazel_grouse_jyu", "Hazel_grouse_jyu")
    caper_fn = _load_model_function("capercaillie_jyu", "Capercaillie_jyu")
    woodpecker_fn = _load_model_function("three_toed_woodpecker", "Three_toed_woodpecker_jyu")

    bilberry_yield = _run_legacy_model(
        bilberry_fn,
        [site, main_species, temp_sum, ba_total, age, ba_prop_sp, ba_prop_ns, ba_prop_birch, metrics["ba_dec_other"], altitude],
        n_outputs=1,
    )[0]
    cowberry_yield = _run_legacy_model(cowberry_fn, [site, main_species, temp_sum, ba_total, age, altitude], n_outputs=1)[0]
    cep_yield = _run_legacy_model(cep_fn, [ba_total, age], n_outputs=1)[0]
    mushroom_vals = _run_legacy_model(mushroom_fn, [ba_total, age], n_outputs=3)
    mushroom_yield = mushroom_vals[2]

    collectables_vals = _run_legacy_model(
        collectables_fn,
        [site, main_species, temp_sum, ba_total, age, ba_prop_sp, ba_prop_ns, ba_prop_birch, metrics["ba_dec_other"]],
        n_outputs=3,
    )
    
    squirrel_hsi = _run_legacy_model(
        squirrel_fn,
        [vol_total, metrics["vol_spruce"], metrics["vol_birch"], 0.0, metrics["vol_aspen"]],
        n_outputs=1,
    )[0]
    
    long_tailed_tit_hsi = _run_legacy_model(
        tit_fn,
        [vol_total, metrics["vol_birch"], 0.0, metrics["vol_aspen"], ba_total, age],
        n_outputs=1,
    )[0]
    hazel_hsi = _run_legacy_model(
        hazel_fn,
        [vol_total, metrics["vol_spruce"], metrics["vol_birch"], 0.0, metrics["vol_aspen"], metrics["vol_aspen"], age],
        n_outputs=1,
    )[0]
    
    caper_hsi = _run_legacy_model(caper_fn, [metrics["vol_pine"], metrics["vol_spruce"], metrics["stems_total"]], n_outputs=1)[0]
    woodpecker_hsi = _run_legacy_model(woodpecker_fn, [vol_total, 0.0], n_outputs=1)[0]

    out = JyuEcosystemServices()
    out.stand_id = str(input_.identifier)
    out.bilberry_yield_kg_ha = max(0.0, float(collectables_vals[0] if collectables_vals[0] > 0 else bilberry_yield))
    out.cowberry_yield_kg_ha = max(0.0, float(collectables_vals[1] if collectables_vals[1] > 0 else cowberry_yield))
    out.cep_yield_kg_ha = max(0.0, float(collectables_vals[2] if collectables_vals[2] > 0 else cep_yield))
    out.mushroom_yield_kg_ha = max(0.0, float(mushroom_yield))
    out.siberian_flying_squirrel_hsi = float(squirrel_hsi)
    out.long_tailed_tit_hsi = float(long_tailed_tit_hsi)
    out.hazel_grouse_hsi = float(hazel_hsi)
    out.capercaillie_hsi = float(caper_hsi)
    out.three_toed_woodpecker_hsi = float(woodpecker_hsi)

    return input_, [out]


calculate_jyu_ecosystem_services = Treatment(
    calculate_jyu_ecosystem_services_fn,
    "calculate_jyu_ecosystem_services",
    collected_data={JyuEcosystemServices},
)
