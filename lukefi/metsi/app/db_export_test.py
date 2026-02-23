import csv
import sqlite3

from lukefi.metsi.app.db_export import export_stand_performance_table


def test_export_stand_performance_table(tmp_path):
    db_path = "tests/robot/DynamicHarvest/output/ref/simulation_results.db"
    output = tmp_path / "stand_performance.csv"

    export_stand_performance_table(db_path, output)

    with output.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) > 0
    required_columns = {
        "stand_identifier",
        "alternative_identifier",
        "node_identifier",
        "year",
        "done_treatment",
        "harvested_stems_per_ha",
        "harvested_basal_area",
        "extracted_value",
        "stand_basal_area",
    }
    assert required_columns.issubset(rows[0].keys())
    assert all(float(row["harvested_stems_per_ha"]) >= 0 for row in rows)
    assert all(row["node_identifier"] != "0" for row in rows)


def test_export_stand_performance_table_ignores_treatments_and_extracts_value(tmp_path):
    db_path = tmp_path / "sim.db"
    output = tmp_path / "stand_performance.csv"

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE nodes(identifier TEXT, stand TEXT, done_treatment TEXT, treatment_params TEXT, tags TEXT, leaf INTEGER)")
    cur.execute("CREATE TABLE stands(node TEXT, identifier TEXT, year INTEGER, basal_area REAL)")
    cur.execute("CREATE TABLE removed_trees(node TEXT, stand TEXT, stems_per_ha REAL, breast_height_diameter REAL)")
    cur.execute("CREATE TABLE node_npv(node TEXT, stand TEXT, npv REAL)")

    cur.executemany(
        "INSERT INTO nodes VALUES (?, ?, ?, '{}', '{}', ?)",
        [
            ("0", "stand_1", "do_nothing", 0),
            ("0-1", "stand_1", "grow_acta", 0),
            ("0-1-1", "stand_1", "cross_cut_felled_trees", 0),
            ("0-1-1-1", "stand_1", "calculate_npv", 1),
        ])
    cur.executemany(
        "INSERT INTO stands VALUES (?, ?, ?, ?)",
        [
            ("0", "stand_1", 2020, 15.0),
            ("0-1", "stand_1", 2025, 16.0),
            ("0-1-1", "stand_1", 2030, 16.0),
            ("0-1-1-1", "stand_1", 2035, 16.0),
        ])
    cur.execute("INSERT INTO node_npv VALUES ('0-1-1-1', 'stand_1', 1234.5)")
    con.commit()
    con.close()

    export_stand_performance_table(
        db_path,
        output,
        ignored_treatments=("cross_cut_felled_trees", "calculate_npv"),
    )

    with output.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 1
    assert rows[0]["done_treatment"] == "grow_acta"

    export_stand_performance_table(db_path, output)
    with output.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    npv_rows = [r for r in rows if r["done_treatment"] == "calculate_npv"]
    assert len(npv_rows) == 1
    assert float(npv_rows[0]["extracted_value"]) == 1234.5
