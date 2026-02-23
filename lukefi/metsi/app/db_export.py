import csv
import sqlite3
from pathlib import Path
from typing import Iterable


BASE_STAND_PERFORMANCE_SQL = """
WITH RECURSIVE
leaf_paths(stand, alternative, node) AS (
    SELECT stand, identifier, identifier
    FROM nodes
    WHERE leaf = 1

    UNION ALL

    SELECT
        stand,
        alternative,
        substr(node, 1, length(node) - instr(reverse(node), '-'))
    FROM leaf_paths
    WHERE instr(node, '-') > 0
),
unique_paths AS (
    SELECT DISTINCT stand, alternative, node
    FROM leaf_paths
),
harvest AS (
    {harvest_sql}
),
extracted_values AS (
    {extracted_value_sql}
),
bilberry AS (
    {bilberry_sql}
),
jyu_ecosystem_services AS (
    {jyu_ecosystem_services_sql}
)
SELECT
    p.stand AS stand_identifier,
    p.alternative AS alternative_identifier,
    p.node AS node_identifier,
    length(p.node) - length(replace(p.node, '-', '')) AS node_depth,
    s.year,
    n.done_treatment,
    COALESCE(h.harvested_stems_per_ha, 0.0) AS harvested_stems_per_ha,
    COALESCE(h.harvested_basal_area, 0.0) AS harvested_basal_area,
    COALESCE(jes.cowberry_yield_kg_ha, 0.0) AS cowberry_yield_kg_ha,
    COALESCE(jes.cowberry_yield_kg_ha * COALESCE(s.area, 0.0), 0.0) AS cowberry_yield_kg_stand,
    COALESCE(jes.cep_yield_kg_ha, 0.0) AS cep_yield_kg_ha,
    COALESCE(jes.cep_yield_kg_ha * COALESCE(s.area, 0.0), 0.0) AS cep_yield_kg_stand,
    COALESCE(jes.mushroom_yield_kg_ha, 0.0) AS mushroom_yield_kg_ha,
    COALESCE(jes.mushroom_yield_kg_ha * COALESCE(s.area, 0.0), 0.0) AS mushroom_yield_kg_stand,
    COALESCE(jes.siberian_flying_squirrel_hsi, 0.0) AS siberian_flying_squirrel_hsi,
    COALESCE(jes.long_tailed_tit_hsi, 0.0) AS long_tailed_tit_hsi,
    COALESCE(jes.hazel_grouse_hsi, 0.0) AS hazel_grouse_hsi,
    COALESCE(jes.capercaillie_hsi, 0.0) AS capercaillie_hsi,
    COALESCE(jes.three_toed_woodpecker_hsi, 0.0) AS three_toed_woodpecker_hsi,
    ev.extracted_value AS extracted_value,
    COALESCE(b.bilberry_yield_kg_ha, 0.0) AS bilberry_yield_kg_ha,
    COALESCE(b.bilberry_yield_kg_ha * COALESCE(s.area, 0.0), 0.0) AS bilberry_yield_kg_stand,
    s.basal_area AS stand_basal_area
FROM unique_paths p
JOIN stands s
    ON s.node = p.node
   AND s.identifier = p.stand
JOIN nodes n
    ON n.identifier = p.node
   AND n.stand = p.stand
LEFT JOIN harvest h
    ON h.node = p.node
   AND h.stand = p.stand
LEFT JOIN extracted_values ev
    ON ev.node = p.node
   AND ev.stand = p.stand
LEFT JOIN bilberry b
    ON b.node = p.node
   AND b.stand = p.stand
LEFT JOIN jyu_ecosystem_services jes
   ON jes.node = p.node
   AND jes.stand = p.stand
WHERE p.node <> "0"
{ignored_treatments_clause}
ORDER BY stand_identifier, alternative_identifier, s.year, node_depth, node_identifier
"""


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _list_tables(connection: sqlite3.Connection) -> list[str]:
    rows = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    return [name for (name,) in rows]


def _table_columns(connection: sqlite3.Connection, table: str) -> set[str]:
    rows = connection.execute(f"PRAGMA table_info({_quote_identifier(table)})").fetchall()
    return {row[1] for row in rows}


def _build_extracted_value_sql(connection: sqlite3.Connection) -> str:
    candidate_value_columns = (
        "npv",
        "net_present_value",
        "value_per_ha",
        "value",
        "harvest_value",
        "present_value",
    )

    subqueries: list[str] = []
    for table in _list_tables(connection):
        if table in {"nodes", "stands", "trees", "strata", "removed_trees"}:
            continue
        cols = _table_columns(connection, table)
        if not {"node", "stand"}.issubset(cols):
            continue
        value_column = next((name for name in candidate_value_columns if name in cols), None)
        if value_column is None:
            continue
        table_q = _quote_identifier(table)
        col_q = _quote_identifier(value_column)
        subqueries.append(
            f"SELECT node, stand, SUM({col_q}) AS extracted_value FROM {table_q} GROUP BY node, stand"
        )

    if len(subqueries) == 0:
        return "SELECT NULL AS node, NULL AS stand, NULL AS extracted_value WHERE 1=0"

    union_sql = " UNION ALL ".join(subqueries)
    return (
        "SELECT node, stand, SUM(extracted_value) AS extracted_value "
        f"FROM ({union_sql}) GROUP BY node, stand"
    )


def _build_harvest_sql(connection: sqlite3.Connection) -> str:
    tables = set(_list_tables(connection))
    if "removed_trees" not in tables:
        return "SELECT NULL AS node, NULL AS stand, 0.0 AS harvested_stems_per_ha, 0.0 AS harvested_basal_area WHERE 1=0"
    return (
        "SELECT node, stand, SUM(stems_per_ha) AS harvested_stems_per_ha, "
        "SUM(stems_per_ha * (3.141592653589793 * ((breast_height_diameter / 200.0) * (breast_height_diameter / 200.0)))) "
        "AS harvested_basal_area FROM removed_trees GROUP BY node, stand"
    )


def _build_bilberry_sql(connection: sqlite3.Connection) -> str:
    tables = set(_list_tables(connection))
    if "bilberry_yield" not in tables:
        return "SELECT NULL AS node, NULL AS stand, 0.0 AS bilberry_yield_kg_ha WHERE 1=0"

    cols = _table_columns(connection, "bilberry_yield")
    if not {"node", "stand", "yield_kg_ha"}.issubset(cols):
        return "SELECT NULL AS node, NULL AS stand, 0.0 AS bilberry_yield_kg_ha WHERE 1=0"

    return "SELECT node, stand, SUM(yield_kg_ha) AS bilberry_yield_kg_ha FROM bilberry_yield GROUP BY node, stand"


def _build_jyu_ecosystem_services_sql(connection: sqlite3.Connection) -> str:
    tables = set(_list_tables(connection))
    if "jyu_ecosystem_services" not in tables:
        return (
            "SELECT NULL AS node, NULL AS stand, "
            "0.0 AS cowberry_yield_kg_ha, 0.0 AS cep_yield_kg_ha, 0.0 AS mushroom_yield_kg_ha, "
            "0.0 AS siberian_flying_squirrel_hsi, 0.0 AS long_tailed_tit_hsi, 0.0 AS hazel_grouse_hsi, "
            "0.0 AS capercaillie_hsi, 0.0 AS three_toed_woodpecker_hsi WHERE 1=0"
        )

    cols = _table_columns(connection, "jyu_ecosystem_services")
    required = {
        "node", "stand", "cowberry_yield_kg_ha", "cep_yield_kg_ha", "mushroom_yield_kg_ha",
        "siberian_flying_squirrel_hsi", "long_tailed_tit_hsi", "hazel_grouse_hsi",
        "capercaillie_hsi", "three_toed_woodpecker_hsi",
    }
    if not required.issubset(cols):
        return (
            "SELECT NULL AS node, NULL AS stand, "
            "0.0 AS cowberry_yield_kg_ha, 0.0 AS cep_yield_kg_ha, 0.0 AS mushroom_yield_kg_ha, "
            "0.0 AS siberian_flying_squirrel_hsi, 0.0 AS long_tailed_tit_hsi, 0.0 AS hazel_grouse_hsi, "
            "0.0 AS capercaillie_hsi, 0.0 AS three_toed_woodpecker_hsi WHERE 1=0"
        )

    return (
        "SELECT node, stand, "
        "SUM(cowberry_yield_kg_ha) AS cowberry_yield_kg_ha, "
        "SUM(cep_yield_kg_ha) AS cep_yield_kg_ha, "
        "SUM(mushroom_yield_kg_ha) AS mushroom_yield_kg_ha, "
        "AVG(siberian_flying_squirrel_hsi) AS siberian_flying_squirrel_hsi, "
        "AVG(long_tailed_tit_hsi) AS long_tailed_tit_hsi, "
        "AVG(hazel_grouse_hsi) AS hazel_grouse_hsi, "
        "AVG(capercaillie_hsi) AS capercaillie_hsi, "
        "AVG(three_toed_woodpecker_hsi) AS three_toed_woodpecker_hsi "
        "FROM jyu_ecosystem_services GROUP BY node, stand"
    )

def export_stand_performance_table(db_path: str | Path,
                                   output_csv_path: str | Path,
                                   ignored_treatments: Iterable[str] = ()) -> None:
    """Export stand x alternative x period table from a simulation sqlite database.

    - Root node `0` is always skipped.
    - `extracted_value` is filled from DB tables that include (`node`, `stand`) and
      one of the known value columns (e.g. `npv`, `value_per_ha`, `value`).
    - Specific treatment rows can be excluded with `ignored_treatments`.
    - `bilberry_yield_kg_ha` and `bilberry_yield_kg_stand` are filled from `bilberry_yield`.
    """
    con = sqlite3.connect(str(db_path))
    con.create_function("reverse", 1, lambda value: str(value)[::-1])
    try:
        ignored_treatments = tuple(ignored_treatments)
        ignored_clause = ""
        if len(ignored_treatments) > 0:
            placeholders = ", ".join("?" for _ in ignored_treatments)
            ignored_clause = f"  AND n.done_treatment NOT IN ({placeholders})"

        query = BASE_STAND_PERFORMANCE_SQL.format(
            harvest_sql=_build_harvest_sql(con),
            extracted_value_sql=_build_extracted_value_sql(con),
            bilberry_sql=_build_bilberry_sql(con),
            jyu_ecosystem_services_sql=_build_jyu_ecosystem_services_sql(con),
            ignored_treatments_clause=ignored_clause,
        )
        rows = con.execute(query, ignored_treatments)

        output_path = Path(output_csv_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([col[0] for col in rows.description])
            writer.writerows(rows)
    finally:
        con.close()
