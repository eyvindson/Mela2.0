from dataclasses import dataclass

import numpy as np

from lukefi.metsi.data.enums.internal import TreeSpecies
from lukefi.metsi.data.vector_model import ReferenceTrees


DEFAULT_COMPONENT_SHARES: dict[str, float] = {
    "stem": 0.55,
    "branch": 0.16,
    "foliage": 0.07,
    "stump": 0.10,
    "roots": 0.12,
}

SUPPORTED_COMPONENTS: tuple[str, ...] = tuple(DEFAULT_COMPONENT_SHARES.keys())


@dataclass(frozen=True)
class RepolaBiomassConverterConfig:
    """Config for phase-2 Repola-style biomass conversion proxy."""

    carbon_fraction: float = 0.5
    component_shares: dict[str, float] | None = None

    def normalized_component_shares(self) -> dict[str, float]:
        shares = self.component_shares or DEFAULT_COMPONENT_SHARES
        unknown = set(shares.keys()) - set(SUPPORTED_COMPONENTS)
        if unknown:
            raise ValueError(f"Unknown biomass component(s): {sorted(unknown)}")

        missing = set(SUPPORTED_COMPONENTS) - set(shares.keys())
        if missing:
            raise ValueError(f"Missing biomass component share(s): {sorted(missing)}")

        values = np.array([float(shares[c]) for c in SUPPORTED_COMPONENTS], dtype=float)
        if np.any(values < 0.0):
            raise ValueError("component shares must be non-negative")

        total = float(np.sum(values))
        if total <= 0.0:
            raise ValueError("component shares sum must be > 0")

        return {name: float(value / total) for name, value in zip(SUPPORTED_COMPONENTS, values, strict=True)}


@dataclass(frozen=True)
class ComponentCarbon:
    stem_c: float
    branch_c: float
    foliage_c: float
    stump_c: float
    roots_c: float

    @property
    def total_c(self) -> float:
        return self.stem_c + self.branch_c + self.foliage_c + self.stump_c + self.roots_c


@dataclass(frozen=True)
class RepolaProxyBiomassConverter:
    """Component-level biomass conversion proxy with explicit Repola naming."""

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

    def species_group_factor(self, species_code: int) -> float:
        group = self.species_group(species_code)
        if group == "pine":
            return 1.00
        if group == "spruce":
            return 1.05
        return 0.95

    def dry_mass_kg_per_ha(self, reference_trees: ReferenceTrees) -> float:
        if reference_trees.size == 0:
            return 0.0

        stems = np.nan_to_num(reference_trees.stems_per_ha, nan=0.0)
        dbh = np.nan_to_num(reference_trees.breast_height_diameter, nan=0.0)
        height = np.nan_to_num(reference_trees.height, nan=0.0)

        species_factors = np.array([self.species_group_factor(s) for s in reference_trees.species], dtype=float)
        dry_mass = stems * (0.11 * (dbh ** 2) * np.maximum(height, 0.1)) * species_factors
        return float(np.sum(np.maximum(dry_mass, 0.0)))

    def component_carbon_kg_per_ha(self, reference_trees: ReferenceTrees) -> ComponentCarbon:
        dry_mass = self.dry_mass_kg_per_ha(reference_trees)
        total_c = dry_mass * self.config.carbon_fraction
        shares = self.config.normalized_component_shares()
        return ComponentCarbon(
            stem_c=total_c * shares["stem"],
            branch_c=total_c * shares["branch"],
            foliage_c=total_c * shares["foliage"],
            stump_c=total_c * shares["stump"],
            roots_c=total_c * shares["roots"],
        )
