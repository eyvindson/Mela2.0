from dataclasses import dataclass

from lukefi.metsi.domain.ecosystem_services.bilberry import calculate_bilberry_yield_fn
from lukefi.metsi.domain.ecosystem_services.bilberry_jyu import bilberry_yield_jyu


@dataclass
class DummyTrees:
    size: int
    species: list[int]
    breast_height_diameter: list[float]
    stems_per_ha: list[float]


@dataclass
class DummyStand:
    identifier: str
    site_type_category: int
    main_tree_species_dominant_storey: int
    dominant_storey_age: float
    geo_location: tuple[float, float, float, str]
    basal_area: float
    reference_trees: DummyTrees


def _stand_for_bilberry() -> DummyStand:
    return DummyStand(
        identifier="stand_1",
        site_type_category=3,
        main_tree_species_dominant_storey=1,
        dominant_storey_age=50,
        geo_location=(0.0, 0.0, 120.0, "EPSG:2393"),
        basal_area=18.0,
        reference_trees=DummyTrees(
            size=3,
            species=[1, 2, 3],
            breast_height_diameter=[20.0, 18.0, 12.0],
            stems_per_ha=[400.0, 250.0, 120.0],
        ),
    )


def test_bilberry_yield_jyu_returns_non_negative_value():
    stand = _stand_for_bilberry()
    result = bilberry_yield_jyu(stand)

    assert result >= 0.0


def test_calculate_bilberry_yield_fn_collects_value_per_ha():
    stand = _stand_for_bilberry()
    updated, collected = calculate_bilberry_yield_fn(stand, berry_price_per_kg=8.0)

    assert updated is stand
    assert len(collected) == 1
    assert collected[0].yield_kg_ha >= 0.0
    assert collected[0].value_per_ha == collected[0].yield_kg_ha * 8.0
