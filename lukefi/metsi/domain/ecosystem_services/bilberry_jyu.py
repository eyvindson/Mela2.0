import math
from typing import TYPE_CHECKING

from lukefi.metsi.data.enums.internal import TreeSpecies

if TYPE_CHECKING:
    from lukefi.metsi.data.model import ForestStand


def _species_basal_areas(stand: "ForestStand") -> tuple[float, float, float, float, float]:
    """Returns (total, pine, spruce, birch, other_deciduous) basal areas from reference trees."""
    trees = stand.reference_trees
    if getattr(trees, "size", 0) == 0:
        total = float(getattr(stand, "basal_area", 0.0) or 0.0)
        return total, 0.0, 0.0, 0.0, 0.0

    total = pine_ba = spruce_ba = birch_ba = other_dec_ba = 0.0
    for i in range(trees.size):
        dbh = float(trees.breast_height_diameter[i])
        stems = float(trees.stems_per_ha[i])
        species = int(trees.species[i])
        ba = stems * (math.pi * ((dbh / 200.0) ** 2))
        total += ba
        if species == int(TreeSpecies.PINE):
            pine_ba += ba
        elif species == int(TreeSpecies.SPRUCE):
            spruce_ba += ba
        elif species in (int(TreeSpecies.SILVER_BIRCH), int(TreeSpecies.DOWNY_BIRCH)):
            birch_ba += ba
        else:
            other_dec_ba += ba

    return total, pine_ba, spruce_ba, birch_ba, other_dec_ba


def bilberry_yield_jyu(stand: "ForestStand") -> float:
    """University of Jyväskylä bilberry model, adapted to Metsi stand-like input."""
    sc = int(getattr(stand, "site_type_category", 0) or 0)
    main_sp = int(getattr(stand, "main_tree_species_dominant_storey", TreeSpecies.PINE) or TreeSpecies.PINE)
    age = float(getattr(stand, "dominant_storey_age", 0.0) or 0.0)
    location = getattr(stand, "geo_location", None)
    alt = float(location[2]) if (location is not None and len(location) > 2 and location[2] is not None) else 0.0

    ba_total, ba_pine, ba_spruce, ba_birch, ba_other_dec = _species_basal_areas(stand)
    if ba_total <= 0.0:
        ba_total = float(getattr(stand, "basal_area", 0.0) or 0.0)
    if ba_total <= 0.0:
        return 0.0

    ba_prop_sp = ba_pine / ba_total
    ba_prop_ns = ba_spruce / ba_total
    ba_prop_b = ba_birch / ba_total
    ba_prop_dec = (ba_other_dec / ba_total) + ba_prop_b

    mixed = int(ba_prop_sp < 0.80 and ba_prop_ns < 0.80 and ba_prop_dec < 0.80)

    bilberry_pine_birch_yield = 0.0
    bilberry_spruce_yield = 0.0

    if main_sp in [1, 3, 4, 5, 6, 7, 8, 9] or mixed == 1:
        a0 = -3.8470
        a1 = -2.1815
        a2 = -0.4809
        a3 = -0.4807
        a4 = -1.5053
        a5 = 0.1209
        a6 = -0.4770
        a7 = -0.2588
        a8 = 0.0
        a9 = 0.0029
        a10 = 0.0080
        a11 = -0.0021
        a12 = 0.0947
        a13 = -0.1916
        a14 = -0.6781
        a15 = 0.1422
        a16 = 0.2398
        a17 = -0.2812

        if main_sp == 1:
            a6 = 0.0
        elif main_sp != 1 and sc == 2:
            a5 = 0.0

        if sc == 2:
            a1 = a3 = a4 = 0.0
        elif sc == 3:
            a1 = a2 = a3 = a4 = 0.0
        elif sc == 4:
            a1 = a2 = a4 = 0.0
        elif sc == 5:
            a1 = a2 = a3 = 0.0
        else:
            a2 = a3 = a4 = 0.0

        cov = 100.0 * (1.0 / (1.0 + math.exp(-(a0 + a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8
                                                + a9 * alt + a10 * age + a11 * (age * age / 100.0)
                                                + a12 * ba_total + a13 * (ba_total * ba_total / 100.0)))))
        bilberry_pine_birch_yield = math.exp(a14 + a15 + a16 * cov + a17 * ((cov * cov) / 100.0))
        bilberry_pine_birch_yield *= 0.8 * 10000.0 * 0.35 / 1000.0

    if main_sp == 2 or mixed == 1:
        a0 = -3.8470
        a1 = -2.1815
        a2 = -0.4809
        a3 = -0.4807
        a4 = -1.5053
        a5 = 0.0
        a6 = 0.0
        a7 = -0.2588
        a8 = 0.0
        a9 = 0.0029
        a10 = 0.0080
        a11 = -0.0021
        a12 = 0.0947
        a13 = -0.1916
        a14 = -4.7474
        a15 = 0.5450
        a16 = 0.3635
        a17 = -0.4798
        a18 = 0.3742
        a19 = -1.3447

        if sc == 2:
            a1 = a3 = a4 = 0.0
        elif sc == 3:
            a1 = a2 = a3 = a4 = 0.0
        elif sc == 4:
            a1 = a2 = a4 = 0.0
        elif sc == 5:
            a1 = a2 = a3 = 0.0
        else:
            a2 = a3 = a4 = 0.0

        cov = 100.0 * (1.0 / (1.0 + math.exp(-(a0 + a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8
                                                + a9 * alt + a10 * age + a11 * (age * age / 100.0)
                                                + a12 * ba_total + a13 * (ba_total * ba_total / 100.0)))))
        bilberry_spruce_yield = math.exp(a14 + a15 + a16 * cov + a17 * (cov * cov / 100.0)
                                         + a18 * ba_total + a19 * (ba_total * ba_total / 100.0))
        bilberry_spruce_yield *= 0.8 * 10000.0 * 0.35 / 1000.0

    if main_sp in [1, 3, 4, 5, 6, 7, 8, 9] and mixed == 0:
        bilberry = bilberry_pine_birch_yield
    elif main_sp == 2 and mixed == 0:
        bilberry = bilberry_spruce_yield
    elif mixed == 1:
        bilberry = (
            bilberry_pine_birch_yield * ba_prop_sp
            + bilberry_pine_birch_yield * ba_prop_dec
            + bilberry_spruce_yield * ba_prop_ns
        )
    else:
        bilberry = 0.0

    return round(float(max(bilberry, 0.0)), 4)
