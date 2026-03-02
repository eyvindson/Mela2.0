from dataclasses import dataclass

import numpy as np

from lukefi.metsi.data.vector_model import ReferenceTrees
from lukefi.metsi.domain.deadwood.biomass_conversion import RepolaBiomassConverter, RepolaBiomassConverterConfig
from lukefi.metsi.domain.deadwood.types import DeadwoodInflowDiagnostics, DeadwoodInflows


DEFAULT_EQUATION_SET = "repola"
DEFAULT_INCLUDE_HARVEST_RESIDUES = True
DEFAULT_CARBON_FRACTION = 0.5
DEFAULT_FINE_ROOT_FRACTION = 0.3
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
    fine_root_fraction: float = DEFAULT_FINE_ROOT_FRACTION
    residue_share_of_removed_biomass: float = 0.3
    residue_share_by_species_group: dict[str, float] | None = None
    initial_deadwood_share_of_living_biomass: float = 0.02
    initialization_mode: str = "simple_ratio"
    legacy_site_class: int | None = None

    def validate(self) -> None:
        if self.equation_set.lower() != DEFAULT_EQUATION_SET:
            raise ValueError(f"Unsupported equation_set '{self.equation_set}'. Currently supported set: '{DEFAULT_EQUATION_SET}'.")
        if not (0.0 <= self.carbon_fraction <= 1.0):
            raise ValueError("carbon_fraction must be between 0 and 1")
        if not (0.0 <= self.fine_root_fraction <= 1.0):
            raise ValueError("fine_root_fraction must be between 0 and 1")
        if not (0.0 <= self.residue_share_of_removed_biomass <= 1.0):
            raise ValueError("residue_share_of_removed_biomass must be between 0 and 1")
        if not (0.0 <= self.initial_deadwood_share_of_living_biomass <= 1.0):
            raise ValueError("initial_deadwood_share_of_living_biomass must be between 0 and 1")
        if self.initialization_mode not in {"simple_ratio", "legacy_distribution_model", "none"}:
            raise ValueError(
                "initialization_mode must be one of: 'simple_ratio', 'legacy_distribution_model', 'none'"
            )


def _scale_stems(reference_trees: ReferenceTrees, new_stems_per_ha: np.ndarray) -> ReferenceTrees:
    scaled = reference_trees[:] if reference_trees.size > 0 else reference_trees
    scaled.stems_per_ha = np.maximum(new_stems_per_ha, 0.0)
    return scaled


def _to_channelized_inflow(components, residue_share: float = 1.0) -> tuple[float, float, float]:
    # MVP mapping policy:
    # stem + stump + coarse roots -> cwl
    # branches + fine roots -> fwl
    # foliage -> nwl
    cwl_c = (components.stem_c + components.stump_c + components.coarse_root_c) * residue_share
    fwl_c = (components.branch_c + components.fine_root_c) * residue_share
    nwl_c = components.foliage_c * residue_share
    return cwl_c, fwl_c, nwl_c


def estimate_initial_deadwood_channels(reference_trees: ReferenceTrees, config: DeadwoodInflowConfig) -> tuple[float, float, float]:
    if reference_trees.size == 0 or config.initial_deadwood_share_of_living_biomass <= 0.0:
        return 0.0, 0.0, 0.0

    converter = RepolaBiomassConverter(
        config=RepolaBiomassConverterConfig(
            carbon_fraction=config.carbon_fraction,
            fine_root_fraction=config.fine_root_fraction,
        )
    )
    return _to_channelized_inflow(
        converter.component_carbon_kg_per_ha(reference_trees),
        residue_share=config.initial_deadwood_share_of_living_biomass,
    )


def mortality_inflow_from_tree_lists(previous_trees: ReferenceTrees, current_trees: ReferenceTrees, config: DeadwoodInflowConfig) -> tuple[float, float, float]:
    converter = RepolaBiomassConverter(
        config=RepolaBiomassConverterConfig(
            carbon_fraction=config.carbon_fraction,
            fine_root_fraction=config.fine_root_fraction,
        )
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
        return 0.0, 0.0, 0.0

    dead_slice = previous_trees[np.array(dead_indices, dtype=int)]
    dead_slice = _scale_stems(dead_slice, np.array(dead_stem_losses, dtype=float))
    return _to_channelized_inflow(converter.component_carbon_kg_per_ha(dead_slice))


def mortality_inflow_from_growth_model(mortality_trees: ReferenceTrees, config: DeadwoodInflowConfig) -> tuple[float, float, float]:
    if mortality_trees.size == 0:
        return 0.0, 0.0, 0.0

    converter = RepolaBiomassConverter(
        config=RepolaBiomassConverterConfig(
            carbon_fraction=config.carbon_fraction,
            fine_root_fraction=config.fine_root_fraction,
        )
    )
    return _to_channelized_inflow(converter.component_carbon_kg_per_ha(mortality_trees))


def _residue_share_for_species_group(config: DeadwoodInflowConfig, species_group: str) -> float:
    share_map = config.residue_share_by_species_group or DEFAULT_RESIDUE_SHARE_BY_SPECIES_GROUP
    return float(share_map.get(species_group, config.residue_share_of_removed_biomass))


def harvest_residue_inflow_from_removed_trees(removed_trees: ReferenceTrees, config: DeadwoodInflowConfig) -> tuple[float, float, float]:
    if removed_trees.size == 0 or not config.include_harvest_residues:
        return 0.0, 0.0, 0.0

    converter = RepolaBiomassConverter(
        config=RepolaBiomassConverterConfig(
            carbon_fraction=config.carbon_fraction,
            fine_root_fraction=config.fine_root_fraction,
        )
    )

    cwl = fwl = nwl = 0.0
    for idx in range(removed_trees.size):
        tree_slice = removed_trees[np.array([idx], dtype=int)]
        group = converter.species_group(int(tree_slice.species[0]))
        residue_share = _residue_share_for_species_group(config, group)
        channelized = _to_channelized_inflow(converter.component_carbon_kg_per_ha(tree_slice), residue_share=residue_share)
        cwl += channelized[0]
        fwl += channelized[1]
        nwl += channelized[2]
    return cwl, fwl, nwl


def build_deadwood_inflows(
    previous_trees: ReferenceTrees,
    current_trees: ReferenceTrees,
    removed_trees: ReferenceTrees | None = None,
    growth_mortality_trees: ReferenceTrees | None = None,
    config: DeadwoodInflowConfig | None = None,
    return_diagnostics: bool = False,
) -> DeadwoodInflows | tuple[DeadwoodInflows, DeadwoodInflowDiagnostics]:
    config = config or DeadwoodInflowConfig()
    config.validate()

    diagnostics = DeadwoodInflowDiagnostics(
        mortality_source="explicit_growth_model" if growth_mortality_trees is not None else "tree_list_diff_fallback",
        used_explicit_mortality=growth_mortality_trees is not None,
        used_fallback_diff=growth_mortality_trees is None,
    )

    if growth_mortality_trees is not None:
        mortality_cwl, mortality_fwl, mortality_nwl = mortality_inflow_from_growth_model(growth_mortality_trees, config)
    else:
        mortality_cwl, mortality_fwl, mortality_nwl = mortality_inflow_from_tree_lists(previous_trees, current_trees, config)
    harvest_cwl = harvest_fwl = harvest_nwl = 0.0
    if removed_trees is not None:
        harvest_cwl, harvest_fwl, harvest_nwl = harvest_residue_inflow_from_removed_trees(removed_trees, config)

    inflows = DeadwoodInflows(
        mortality_cwl_c=mortality_cwl,
        mortality_fwl_c=mortality_fwl,
        mortality_nwl_c=mortality_nwl,
        harvest_cwl_c=harvest_cwl,
        harvest_fwl_c=harvest_fwl,
        harvest_nwl_c=harvest_nwl,
    )
    if return_diagnostics:
        return inflows, diagnostics
    return inflows
