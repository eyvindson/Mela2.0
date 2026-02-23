from dataclasses import dataclass

import numpy as np

from lukefi.metsi.data.enums.internal import TreeSpecies
from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.domain.deadwood.types import DeadwoodInflows


DEFAULT_EQUATION_SET = "repola"
DEFAULT_INCLUDE_HARVEST_RESIDUES = True
DEFAULT_CARBON_FRACTION = 0.5


@dataclass
class DeadwoodInflowConfig:
    equation_set: str = DEFAULT_EQUATION_SET
    include_harvest_residues: bool = DEFAULT_INCLUDE_HARVEST_RESIDUES
    carbon_fraction: float = DEFAULT_CARBON_FRACTION
    residue_share_of_removed_biomass: float = 0.3

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


def _species_group_factor(species_code: int) -> float:
    try:
        species = TreeSpecies(int(species_code))
    except ValueError:
        return 0.95
    if species == TreeSpecies.PINE:
        return 1.00
    if species == TreeSpecies.SPRUCE:
        return 1.05
    return 0.95


def _repola_proxy_carbon(reference_trees: ReferenceTrees, carbon_fraction: float) -> float:
    if reference_trees.size == 0:
        return 0.0

    stems = np.nan_to_num(reference_trees.stems_per_ha, nan=0.0)
    dbh = np.nan_to_num(reference_trees.breast_height_diameter, nan=0.0)
    height = np.nan_to_num(reference_trees.height, nan=0.0)

    species_factors = np.array([_species_group_factor(s) for s in reference_trees.species], dtype=float)

    # Phase-1 proxy mass term (kg dry mass / ha), to be replaced by full Repola eq package in phase 2.
    dry_mass = stems * (0.11 * (dbh ** 2) * np.maximum(height, 0.1)) * species_factors
    return float(np.sum(np.maximum(dry_mass, 0.0)) * carbon_fraction)


def _scale_stems(reference_trees: ReferenceTrees, new_stems_per_ha: np.ndarray) -> ReferenceTrees:
    scaled = reference_trees[:] if reference_trees.size > 0 else reference_trees
    scaled.stems_per_ha = np.maximum(new_stems_per_ha, 0.0)
    return scaled


def mortality_inflow_from_tree_lists(
    previous_trees: ReferenceTrees,
    current_trees: ReferenceTrees,
    config: DeadwoodInflowConfig,
) -> float:
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
    return _repola_proxy_carbon(dead_slice, config.carbon_fraction)


def harvest_residue_inflow_from_removed_trees(removed_trees: ReferenceTrees, config: DeadwoodInflowConfig) -> float:
    if removed_trees.size == 0 or not config.include_harvest_residues:
        return 0.0
    removed_carbon = _repola_proxy_carbon(removed_trees, config.carbon_fraction)
    return removed_carbon * config.residue_share_of_removed_biomass


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
