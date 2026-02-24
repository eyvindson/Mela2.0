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
    source_fluxes: dict[str, DeadwoodFluxes] | None = None

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
                cwl_acid_c REAL,
                cwl_water_c REAL,
                cwl_ethanol_c REAL,
                cwl_non_soluble_c REAL,
                cwl_humus_c REAL,
                cwl_c REAL,
                fwl_acid_c REAL,
                fwl_water_c REAL,
                fwl_ethanol_c REAL,
                fwl_non_soluble_c REAL,
                fwl_humus_c REAL,
                fwl_c REAL,
                nwl_acid_c REAL,
                nwl_water_c REAL,
                nwl_ethanol_c REAL,
                nwl_non_soluble_c REAL,
                nwl_humus_c REAL,
                nwl_c REAL,
                total_c REAL,
                input_c REAL,
                decomposition_c REAL,
                net_change_c REAL,
                PRIMARY KEY (node, stand, year),
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
                decomposition_c REAL,
                net_change_c REAL,
                PRIMARY KEY (node, stand, source, year),
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                node_str,
                identifier,
                self.year,
                self.pools.cwl.acid_c,
                self.pools.cwl.water_c,
                self.pools.cwl.ethanol_c,
                self.pools.cwl.non_soluble_c,
                self.pools.cwl.humus_c,
                self.pools.cwl.total_c,
                self.pools.fwl.acid_c,
                self.pools.fwl.water_c,
                self.pools.fwl.ethanol_c,
                self.pools.fwl.non_soluble_c,
                self.pools.fwl.humus_c,
                self.pools.fwl.total_c,
                self.pools.nwl.acid_c,
                self.pools.nwl.water_c,
                self.pools.nwl.ethanol_c,
                self.pools.nwl.non_soluble_c,
                self.pools.nwl.humus_c,
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
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    node_str,
                    identifier,
                    "mortality",
                    self.year,
                    self.inflows.mortality_c,
                    (self.source_fluxes or {}).get("mortality", DeadwoodFluxes()).decomposition_c,
                    (self.source_fluxes or {}).get("mortality", DeadwoodFluxes()).net_change_c,
                ),
                (
                    node_str,
                    identifier,
                    "harvest",
                    self.year,
                    self.inflows.harvest_residue_c,
                    (self.source_fluxes or {}).get("harvest", DeadwoodFluxes()).decomposition_c,
                    (self.source_fluxes or {}).get("harvest", DeadwoodFluxes()).net_change_c,
                ),
                (
                    node_str,
                    identifier,
                    "disturbance",
                    self.year,
                    self.inflows.disturbance_c,
                    (self.source_fluxes or {}).get("disturbance", DeadwoodFluxes()).decomposition_c,
                    (self.source_fluxes or {}).get("disturbance", DeadwoodFluxes()).net_change_c,
                ),
            ],
        )
