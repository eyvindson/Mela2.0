import sqlite3
from typing import TYPE_CHECKING

from lukefi.metsi.domain.ecosystem_services.bilberry_jyu import bilberry_yield_jyu
from lukefi.metsi.sim.collected_data import CollectedData, OpTuple
from lukefi.metsi.sim.treatment import Treatment

if TYPE_CHECKING:
    from lukefi.metsi.data.model import ForestStand


class BilberryYield(CollectedData):
    stand_id: str
    yield_kg_ha: float
    value_per_ha: float

    @classmethod
    def init_db_table(cls, db: sqlite3.Connection):
        cur = db.cursor()
        cur.execute(
            """
            CREATE TABLE bilberry_yield(
                node TEXT,
                stand TEXT,
                identifier TEXT,
                yield_kg_ha REAL,
                value_per_ha REAL,
                PRIMARY KEY (node, identifier),
                FOREIGN KEY (node, stand) REFERENCES nodes(identifier, stand)
            )
            """
        )

    def output_to_db(self, db: sqlite3.Connection, node_str: str, identifier: str):
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO bilberry_yield
            VALUES
                (?, ?, ?, ?, ?)
            """,
            (node_str, identifier, f"{identifier}_bilberry", self.yield_kg_ha, self.value_per_ha),
        )


def calculate_bilberry_yield_fn(input_: "ForestStand", /, **operation_parameters) -> OpTuple["ForestStand"]:
    """Calculate bilberry yield (kg/ha) and optional value per hectare for the stand."""
    yield_kg_ha = bilberry_yield_jyu(input_)
    price_per_kg = float(operation_parameters.get("berry_price_per_kg", 0.0) or 0.0)
    value_per_ha = yield_kg_ha * price_per_kg

    result = BilberryYield()
    result.stand_id = str(input_.identifier)
    result.yield_kg_ha = yield_kg_ha
    result.value_per_ha = value_per_ha

    return input_, [result]


calculate_bilberry_yield = Treatment(
    calculate_bilberry_yield_fn,
    "calculate_bilberry_yield",
    collected_data={BilberryYield},
)
