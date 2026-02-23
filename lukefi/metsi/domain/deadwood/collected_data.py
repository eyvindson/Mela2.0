import sqlite3
from dataclasses import dataclass
from typing import override

from lukefi.metsi.domain.deadwood.types import DeadwoodFluxes, DeadwoodInflows, DeadwoodPools
from lukefi.metsi.sim.collected_data import CollectedData


@dataclass
class DeadwoodPoolsData(CollectedData):
    pools: DeadwoodPools
    fluxes: DeadwoodFluxes
    inflows: DeadwoodInflows
    year: int

    @classmethod
    @override
    def init_db_table(cls, db: sqlite3.Connection):
        cur = db.cursor()
        cur.execute(
            """
            CREATE TABLE deadwood_pools(
                node TEXT,
                stand TEXT,
                year INTEGER,
                cwl_c REAL,
                fwl_c REAL,
                nwl_c REAL,
                total_c REAL,
                input_c REAL,
                decomposition_c REAL,
                net_change_c REAL,
                PRIMARY KEY (node, stand),
                FOREIGN KEY (node, stand) REFERENCES nodes(identifier, stand)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE deadwood_source_ledger(
                node TEXT,
                stand TEXT,
                source TEXT,
                year INTEGER,
                input_c REAL,
                PRIMARY KEY (node, stand, source),
                FOREIGN KEY (node, stand) REFERENCES nodes(identifier, stand)
            )
            """
        )

    @override
    def output_to_db(self, db: sqlite3.Connection, node_str: str, identifier: str):
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO deadwood_pools
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                node_str,
                identifier,
                self.year,
                self.pools.cwl.total_c,
                self.pools.fwl.total_c,
                self.pools.nwl.total_c,
                self.pools.total_c,
                self.fluxes.input_c,
                self.fluxes.decomposition_c,
                self.fluxes.net_change_c,
            ),
        )
        cur.executemany(
            """
            INSERT INTO deadwood_source_ledger
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (node_str, identifier, "mortality", self.year, self.inflows.mortality_c),
                (node_str, identifier, "harvest", self.year, self.inflows.harvest_residue_c),
                (node_str, identifier, "disturbance", self.year, self.inflows.disturbance_c),
            ],
        )
