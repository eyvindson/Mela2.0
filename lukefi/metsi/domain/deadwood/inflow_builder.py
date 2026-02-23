from dataclasses import dataclass

import numpy as np

from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.domain.deadwood.biomass_conversion import (
    RepolaBiomassConverterConfig,
    RepolaProxyBiomassConverter,
)
from lukefi.metsi.domain.deadwood.types import DeadwoodInflows


DEFAULT_EQUATION_SET = "repola"
DEFAULT_INCLUDE_HARVEST_RESIDUES = True
DEFAULT_CARBON_FRACTION = 0.5
DEFAULT_RESIDUE_SHARE_BY_SPECIES_GROUP = {
    "pine": 0.28,
    "spruce": 0.32,
    "broadleaf": 0.35,
}


@dataclass
class DeadwoodInflowConfig:
    equation_set: str = DEFAULT_EQUATION_SET
    include_harvest_residues: bool = DEFAULT_INCLUDE_HARVEST_RESIDUES
    carbon_fraction: float = DEFAULT_CARBON_FRACTION
    residue_share_of_removed_biomass: float = 0.3
    residue_share_by_species_group: dict[str, float] | None = None

    def validate(self) -> None:
        if self.equation_set.lower() != DEFAULT_EQUATION_SET:
            raise ValueError(
                f"Unsupported equation_set '{self.equation_set}'. "
                f"Currently supported set: '{DEFAULT_EQUATION_SET}'."
            )
        if not (0.0 <= self.carbon_fraction <= 1.0):
            raise ValueError("carbon_fraction must be between 0 and 1")
        if not (0.0 <= self.residue_share_of_removed_biomass <= 1.0):
            raise ValueError("residue_share_of_removed_biomass must be between 0 and 1")

        residue_by_group = self.residue_share_by_species_group or DEFAULT_RESIDUE_SHARE_BY_SPECIES_GROUP
        for group, share in residue_by_group.items():
            if group not in {"pine", "spruce", "broadleaf"}:
                raise ValueError(f"Unsupported species group '{group}'")
            if not (0.0 <= share <= 1.0):
                raise ValueError("residue_share_by_species_group values must be between 0 and 1")


def _scale_stems(reference_trees: ReferenceTrees, new_stems_per_ha: np.ndarray) -> ReferenceTrees:
    scaled = reference_trees[:] if reference_trees.size > 0 else reference_trees
    scaled.stems_per_ha = np.maximum(new_stems_per_ha, 0.0)
    return scaled


def mortality_inflow_from_tree_lists(
    previous_trees: ReferenceTrees,
    current_trees: ReferenceTrees,
    config: DeadwoodInflowConfig,
) -> float:
    converter = RepolaProxyBiomassConverter(
        config=RepolaBiomassConverterConfig(carbon_fraction=config.carbon_fraction)
    )

    prev_by_id = {identifier: i for i, identifier in enumerate(previous_trees.identifier.tolist())}
    curr_by_id = {identifier: i for i, identifier in enumerate(current_trees.identifier.tolist())}

    dead_indices: list[int] = []
    dead_stem_losses: list[float] = []
    for identifier, prev_idx in prev_by_id.items():
        curr_idx = curr_by_id.get(identifier)
        prev_stems = previous_trees.stems_per_ha[prev_idx]
        curr_stems = 0.0 if curr_idx is None else current_trees.stems_per_ha[curr_idx]

        if prev_stems > curr_stems:
            dead_indices.append(prev_idx)
            dead_stem_losses.append(float(prev_stems - curr_stems))

    if not dead_indices:
        return 0.0

    dead_slice = previous_trees[np.array(dead_indices, dtype=int)]
    dead_slice = _scale_stems(dead_slice, np.array(dead_stem_losses, dtype=float))
    return converter.component_carbon_kg_per_ha(dead_slice).total_c


def _residue_share_for_species_group(config: DeadwoodInflowConfig, species_group: str) -> float:
    share_map = config.residue_share_by_species_group or DEFAULT_RESIDUE_SHARE_BY_SPECIES_GROUP
    return float(share_map.get(species_group, config.residue_share_of_removed_biomass))


def harvest_residue_inflow_from_removed_trees(removed_trees: ReferenceTrees, config: DeadwoodInflowConfig) -> float:
    if removed_trees.size == 0 or not config.include_harvest_residues:
        return 0.0

    converter = RepolaProxyBiomassConverter(
        config=RepolaBiomassConverterConfig(carbon_fraction=config.carbon_fraction)
    )

    total = 0.0
    for idx in range(removed_trees.size):
        tree_slice = removed_trees[np.array([idx], dtype=int)]
        group = converter.species_group(int(tree_slice.species[0]))
        residue_share = _residue_share_for_species_group(config, group)
        total += converter.component_carbon_kg_per_ha(tree_slice).total_c * residue_share
    return total


def build_deadwood_inflows(
    previous_trees: ReferenceTrees,
    current_trees: ReferenceTrees,
    removed_trees: ReferenceTrees | None = None,
    config: DeadwoodInflowConfig | None = None,
) -> DeadwoodInflows:
    config = config or DeadwoodInflowConfig()
    config.validate()

    mortality_c = mortality_inflow_from_tree_lists(previous_trees, current_trees, config)
    harvest_c = 0.0
    if removed_trees is not None:
        harvest_c = harvest_residue_inflow_from_removed_trees(removed_trees, config)

    return DeadwoodInflows(
        mortality_c=mortality_c,
        harvest_residue_c=harvest_c,
        disturbance_c=0.0,
    )
