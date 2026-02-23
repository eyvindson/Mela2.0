from dataclasses import dataclass
from math import exp, log

import numpy as np

from lukefi.metsi.data.enums.internal import TreeSpecies
from lukefi.metsi.data.vector_model import ReferenceTrees


@dataclass(frozen=True)
class RepolaBiomassConverterConfig:
    carbon_fraction: float = 0.5
    fine_root_fraction: float = 0.3


@dataclass(frozen=True)
class ComponentCarbon:
    stem_c: float
    branch_c: float
    foliage_c: float
    stump_c: float
    coarse_root_c: float
    fine_root_c: float

    @property
    def roots_c(self) -> float:
        return self.coarse_root_c + self.fine_root_c

    @property
    def total_c(self) -> float:
        return self.stem_c + self.branch_c + self.foliage_c + self.stump_c + self.roots_c


@dataclass(frozen=True)
class RepolaBiomassConverter:
    """Direct Repola equations (ported from dead/BiomassmodelLibrary.c)."""

    config: RepolaBiomassConverterConfig = RepolaBiomassConverterConfig()

    def species_group(self, species_code: int) -> str:
        try:
            species = TreeSpecies(int(species_code))
        except ValueError:
            return "broadleaf"
        if species == TreeSpecies.PINE:
            return "pine"
        if species == TreeSpecies.SPRUCE:
            return "spruce"
        return "broadleaf"

    def _components_per_tree_kg(self, species_group: str, d_cm: float, h_m: float) -> tuple[float, float, float, float, float]:
        d = max(d_cm, 0.0)
        h = max(h_m, 0.1)
        d_s = 2.0 + 1.25 * d

        if species_group == "pine":
            stem = exp(-3.721 + 8.103 * (d_s / (d_s + 14.0)) + 5.066 * (h / (h + 12.0)) + (0.002 + 0.009 / 2.0))
            stem_bark = exp(-4.548 + 7.997 * (d_s / (d_s + 12.0)) + 0.357 * log(h) + (0.015 + 0.061 / 2.0))
            living_branches = exp(-6.162 + 15.075 * (d_s / (d_s + 12.0)) - 2.618 * (h / (h + 12.0)) + (0.041 + 0.089 / 2.0))
            dead_branches = exp(-5.201 + 10.574 * (d_s / (d_s + 16.0)) + (0.253 + 0.362 / 2.0))
            foliage = exp(-6.303 + 14.472 * (d_s / (d_s + 6.0)) - 3.976 * (h / (h + 1.0)) + (0.109 + 0.118 / 2.0))
            stump = exp(-6.753 + 12.681 * (d_s / (d_s + 12.0)) + (0.01 + 0.044 / 2.0))
            roots = exp(-5.55 + 13.408 * (d_s / (d_s + 15.0)) + (0.000 + 0.079 / 2.0))
        elif species_group == "spruce":
            stem = exp(-3.555 + 8.042 * (d_s / (d_s + 14.0)) + 0.869 * log(h) + 0.015 * h + (0.009 + 0.009 / 2.0))
            stem_bark = exp(-4.548 + 9.448 * (d_s / (d_s + 18.0)) + 0.436 * log(h) + (0.023 + 0.041 / 2.0))
            living_branches = exp(-4.214 + 14.508 * (d_s / (d_s + 13.0)) - 3.277 * (h / (h + 5.0)) + (0.039 + 0.081 / 2.0))
            dead_branches = exp(-4.85 + 7.702 * (d_s / (d_s + 18.0)) + 0.513 * log(h) + (0.367 + 0.352 / 2.0))
            foliage = exp(-2.994 + 12.251 * (d_s / (d_s + 10.0)) - 3.215 * (h / (h + 1.0)) + (0.107 + 0.089 / 2.0))
            stump = exp(-3.964 + 11.73 * (d_s / (d_s + 26.0)) + (0.065 + 0.058 / 2.0))
            roots = exp(-2.294 + 10.646 * (d_s / (d_s + 24.0)) + (0.105 + 0.114 / 2.0))
        else:
            stem = exp(-4.879 + 9.651 * (d_s / (d_s + 12.0)) + 1.012 * log(h) + (0.003 + 0.005 / 2.0))
            stem_bark = exp(-5.401 + 10.061 * (d_s / (d_s + 12.0)) + 2.657 * (h / (h + 20.0)) + (0.01 + 0.044 / 2.0))
            living_branches = exp(-4.152 + 15.874 * (d_s / (d_s + 16.0)) - 4.407 * (h / (h + 10.0)) + (0.027 + 0.077 / 2.0))
            dead_branches = exp(-8.335 + 12.402 * (d_s / (d_s + 16.0)) + (1.115 + 2.679 / 2.0))
            foliage = exp(-29.566 + 33.372 * (d_s / (d_s + 2.0)) + (0.000 + 0.077 / 2.0))
            stump = exp(-3.574 + 11.304 * (d_s / (d_s + 26.0)) + (0.022 + 0.045 / 2.0))
            roots = exp(-3.223 + 6.497 * (d_s / (d_s + 22.0)) + 1.033 * log(h) + (0.048 + 0.027 / 2.0))

        return stem + stem_bark, living_branches + dead_branches, foliage, stump, roots

    def component_carbon_kg_per_ha(self, reference_trees: ReferenceTrees) -> ComponentCarbon:
        if reference_trees.size == 0:
            return ComponentCarbon(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        stem_kg = branch_kg = foliage_kg = stump_kg = roots_kg = 0.0
        for idx in range(reference_trees.size):
            stems = float(np.nan_to_num(reference_trees.stems_per_ha[idx], nan=0.0))
            if stems <= 0.0:
                continue
            group = self.species_group(int(reference_trees.species[idx]))
            stem_t, branch_t, foliage_t, stump_t, roots_t = self._components_per_tree_kg(
                group,
                float(np.nan_to_num(reference_trees.breast_height_diameter[idx], nan=0.0)),
                float(np.nan_to_num(reference_trees.height[idx], nan=0.0)),
            )
            stem_kg += stems * stem_t
            branch_kg += stems * branch_t
            foliage_kg += stems * foliage_t
            stump_kg += stems * stump_t
            roots_kg += stems * roots_t

        cf = self.config.carbon_fraction
        fine = self.config.fine_root_fraction
        coarse = 1.0 - fine
        return ComponentCarbon(
            stem_c=stem_kg * cf,
            branch_c=branch_kg * cf,
            foliage_c=foliage_kg * cf,
            stump_c=stump_kg * cf,
            coarse_root_c=roots_kg * coarse * cf,
            fine_root_c=roots_kg * fine * cf,
        )


RepolaProxyBiomassConverter = RepolaBiomassConverter
