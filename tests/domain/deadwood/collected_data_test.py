import sqlite3

from lukefi.metsi.domain.deadwood.collected_data import DeadwoodPoolsData
from lukefi.metsi.domain.deadwood.types import ChannelAWENH, DeadwoodFluxes, DeadwoodInflows, DeadwoodPools


def _init_nodes_table(db: sqlite3.Connection):
    db.execute(
        """
        CREATE TABLE nodes(
            identifier TEXT,
            stand TEXT,
            PRIMARY KEY(identifier, stand)
        )
        """
    )
    db.execute("INSERT INTO nodes VALUES (?, ?)", ("0-0", "stand_1"))


def test_deadwood_tables_store_year_for_time_series_extraction():
    db = sqlite3.connect(":memory:")
    _init_nodes_table(db)
    DeadwoodPoolsData.init_db_table(db)

    datum = DeadwoodPoolsData(
        pools=DeadwoodPools(),
        fluxes=DeadwoodFluxes(input_c=1.25, decomposition_c=0.5, net_change_c=0.75),
        inflows=DeadwoodInflows(mortality_cwl_c=0.5, harvest_cwl_c=0.75),
        year=2030,
    )
    datum.output_to_db(db, "0-0", "stand_1")

    pools_row = db.execute(
        "SELECT stand, year, input_c, decomposition_c, net_change_c FROM deadwood_pools"
    ).fetchone()
    assert pools_row == ("stand_1", 2030, 1.25, 0.5, 0.75)

    ledger_rows = db.execute(
        "SELECT source, year, input_c, decomposition_c FROM deadwood_source_ledger ORDER BY source"
    ).fetchall()
    assert ledger_rows == [
        ("disturbance", 2030, 0.0, 0.0),
        ("harvest", 2030, 0.75, 0.0),
        ("mortality", 2030, 0.5, 0.0),
    ]


def test_deadwood_pools_store_optional_awenh_channel_columns():
    db = sqlite3.connect(":memory:")
    _init_nodes_table(db)
    DeadwoodPoolsData.init_db_table(db)

    datum = DeadwoodPoolsData(
        pools=DeadwoodPools(cwl=ChannelAWENH(acid_c=1.0, humus_c=2.0)),
        fluxes=DeadwoodFluxes(),
        inflows=DeadwoodInflows(),
        year=2035,
    )
    datum.output_to_db(db, "0-0", "stand_1")

    awenh_row = db.execute(
        "SELECT cwl_acid_c, cwl_humus_c, cwl_c FROM deadwood_pools"
    ).fetchone()
    assert awenh_row == (1.0, 2.0, 3.0)
