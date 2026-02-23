import sqlite3
from dataclasses import dataclass
from typing import override

from lukefi.metsi.domain.deadwood.types import DeadwoodPools, DeadwoodFluxes
from lukefi.metsi.sim.collected_data import CollectedData


@dataclass
class DeadwoodPoolsData(CollectedData):
    pools: DeadwoodPools
    fluxes: DeadwoodFluxes

    @classmethod
    @override
    def init_db_table(cls, db: sqlite3.Connection):
        cur = db.cursor()
        cur.execute(
            """
            CREATE TABLE deadwood_pools(
                node TEXT,
                stand TEXT,
                acid_c REAL,
                water_c REAL,
                ethanol_c REAL,
                non_soluble_c REAL,
                humus_c REAL,
                total_c REAL,
                input_c REAL,
                decomposition_c REAL,
                net_change_c REAL,
                PRIMARY KEY (node, stand),
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                node_str,
                identifier,
                self.pools.acid_c,
                self.pools.water_c,
                self.pools.ethanol_c,
                self.pools.non_soluble_c,
                self.pools.humus_c,
                self.pools.total_c,
                self.fluxes.input_c,
                self.fluxes.decomposition_c,
                self.fluxes.net_change_c,
            ),
        )
