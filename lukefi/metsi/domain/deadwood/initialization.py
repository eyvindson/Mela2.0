from dataclasses import dataclass

from lukefi.metsi.data.model import ForestStand
from lukefi.metsi.domain.deadwood.inflow_builder import DeadwoodInflowConfig, estimate_initial_deadwood_channels
from lukefi.metsi.domain.deadwood.types import ChannelAWENH, DeadwoodClassState, DeadwoodPools, DeadwoodState

DEFAULT_LEGACY_D_CLASS_WIDTH = 5.0
DEFAULT_LEGACY_MAX_D = 35.0
DEFAULT_LEGACY_SINCE_DEATH_CLASS_WIDTH = 10.0
DEFAULT_LEGACY_MAX_SINCE_DEATH = 40.0

_LEGACY_TABLE_SC_LT4 = {
    (1, 0, 12.5, 5.0): 1.06,
    (1, 0, 12.5, 15.0): 1.39,
    (1, 0, 12.5, 25.0): 0.68,
    (1, 0, 12.5, 35.0): 0.2,
    (1, 0, 17.5, 5.0): 0.41,
    (1, 0, 17.5, 15.0): 0.6,
    (1, 0, 17.5, 25.0): 0.51,
    (1, 0, 17.5, 35.0): 0.23,
    (1, 0, 22.5, 5.0): 0.85,
    (1, 0, 22.5, 15.0): 0.66,
    (1, 1, 17.5, 5.0): 0.1,
    (1, 1, 22.5, 5.0): 0.3,
    (1, 1, 27.5, 5.0): 0.56,
    (2, 0, 7.5, 5.0): 1.0,
    (2, 0, 7.5, 15.0): 1.1,
    (2, 0, 7.5, 25.0): 0.52,
    (2, 0, 12.5, 5.0): 34.9,
    (2, 0, 12.5, 15.0): 89.53,
    (2, 0, 12.5, 25.0): 103.19,
    (2, 0, 17.5, 5.0): 130.25,
    (2, 0, 17.5, 15.0): 257.95,
    (2, 0, 17.5, 25.0): 254.87,
    (2, 0, 22.5, 5.0): 121.57,
    (2, 0, 22.5, 15.0): 104.4,
    (2, 0, 22.5, 25.0): 63.94,
    (2, 0, 27.5, 5.0): 56.18,
    (2, 0, 27.5, 15.0): 24.0,
    (2, 0, 27.5, 25.0): 18.57,
    (2, 0, 32.5, 5.0): 21.85,
    (2, 0, 32.5, 15.0): 4.83,
    (2, 0, 32.5, 25.0): 1.73,
    (2, 1, 12.5, 5.0): 10.24,
    (2, 1, 12.5, 15.0): 20.49,
    (2, 1, 12.5, 25.0): 13.66,
    (2, 1, 17.5, 5.0): 10.4,
    (2, 1, 22.5, 5.0): 504.14,
    (2, 1, 22.5, 15.0): 266.81,
    (2, 1, 27.5, 5.0): 103.75,
    (2, 1, 27.5, 25.0): 8.3,
    (2, 1, 32.5, 15.0): 4.88,
    (3, 0, 12.5, 5.0): 6.1,
    (3, 0, 12.5, 15.0): 6.69,
    (3, 0, 17.5, 5.0): 19.27,
    (3, 0, 17.5, 15.0): 17.35,
    (3, 0, 22.5, 5.0): 7.93,
    (3, 0, 22.5, 15.0): 7.7,
    (3, 0, 27.5, 5.0): 2.34,
    (3, 0, 27.5, 15.0): 2.3,
    (3, 1, 12.5, 15.0): 0.67,
    (3, 1, 17.5, 5.0): 2.42,
    (3, 1, 17.5, 15.0): 6.64,
    (3, 1, 22.5, 5.0): 7.46,
    (3, 1, 22.5, 15.0): 3.59,
    (3, 1, 27.5, 5.0): 8.09,
    (3, 1, 27.5, 15.0): 2.65,
    (3, 1, 32.5, 5.0): 1.13,
}

_LEGACY_TABLE_SC_GTE4 = {
    (1, 0, 7.5, 5.0): 1.0,
    (1, 0, 7.5, 15.0): 1.1,
    (1, 0, 7.5, 25.0): 0.52,
    (1, 0, 12.5, 5.0): 34.9,
    (1, 0, 12.5, 15.0): 89.53,
    (1, 0, 12.5, 25.0): 103.19,
    (1, 0, 17.5, 5.0): 130.25,
    (1, 0, 17.5, 15.0): 257.95,
    (1, 0, 17.5, 25.0): 254.87,
    (1, 0, 22.5, 5.0): 121.57,
    (1, 0, 22.5, 15.0): 104.4,
    (1, 0, 22.5, 25.0): 63.94,
    (1, 0, 27.5, 5.0): 56.18,
    (1, 0, 27.5, 15.0): 24.0,
    (1, 0, 27.5, 25.0): 18.57,
    (1, 0, 32.5, 5.0): 21.85,
    (1, 0, 32.5, 15.0): 4.83,
    (1, 0, 32.5, 25.0): 1.73,
    (1, 1, 12.5, 5.0): 10.24,
    (1, 1, 12.5, 15.0): 20.49,
    (1, 1, 12.5, 25.0): 13.66,
    (1, 1, 17.5, 5.0): 10.4,
    (1, 1, 22.5, 5.0): 504.14,
    (1, 1, 22.5, 15.0): 266.81,
    (1, 1, 27.5, 5.0): 103.75,
    (1, 1, 27.5, 25.0): 8.3,
    (1, 1, 32.5, 15.0): 4.88,
}

_SPECIES_LABEL = {1: "pine", 2: "spruce", 3: "broadleaf"}


@dataclass(frozen=True)
class LegacyDeadwoodSummary:
    total_biomass_kg_per_ha: float
    class_count: int


def _resolve_legacy_site_class(stand: ForestStand, config: DeadwoodInflowConfig) -> int:
    if config.legacy_site_class is not None:
        return int(config.legacy_site_class)
    if stand.site_type_category is not None:
        return int(stand.site_type_category)
    raise ValueError(
        "deadwood initialization mode 'legacy_distribution_model' requires site class: "
        "set stand.site_type_category or deadwood_config.legacy_site_class"
    )


def _legacy_table(site_class: int) -> dict[tuple[int, int, float, float], float]:
    return _LEGACY_TABLE_SC_LT4 if site_class < 4 else _LEGACY_TABLE_SC_GTE4


def initialize_deadwood(stand: ForestStand, config: DeadwoodInflowConfig) -> LegacyDeadwoodSummary | None:
    mode = config.initialization_mode
    if mode == "none":
        return None

    if not hasattr(stand, "deadwood_state"):
        stand.deadwood_state = DeadwoodState()
    if stand.deadwood_state.pools.total_c > 0.0:
        return None

    if mode == "simple_ratio":
        cwl, fwl, nwl = estimate_initial_deadwood_channels(stand.reference_trees, config)
        stand.deadwood_state.pools = DeadwoodPools(
            cwl=ChannelAWENH(non_soluble_c=cwl),
            fwl=ChannelAWENH(non_soluble_c=fwl),
            nwl=ChannelAWENH(non_soluble_c=nwl),
        )
        stand.deadwood_state.source_pools = {
            "mortality": stand.deadwood_state.pools,
            "harvest": DeadwoodPools(),
            "disturbance": DeadwoodPools(),
        }
        return LegacyDeadwoodSummary(total_biomass_kg_per_ha=stand.deadwood_state.pools.total_c, class_count=0)

    if mode != "legacy_distribution_model":
        raise ValueError(f"Unsupported deadwood initialization_mode '{mode}'")

    table = _legacy_table(_resolve_legacy_site_class(stand, config))
    total_biomass = 0.0
    class_state: list[DeadwoodClassState] = []
    for (species_id, snag, diameter, since_death), biomass_kg_ha in table.items():
        carbon_c = biomass_kg_ha * config.carbon_fraction
        total_biomass += biomass_kg_ha
        class_state.append(
            DeadwoodClassState(
                species_group=_SPECIES_LABEL.get(species_id, "unknown"),
                snag=bool(snag),
                diameter_class=f"{diameter:.1f}",
                years_since_death=int(since_death),
                carbon_c=carbon_c,
            )
        )

    snag_c = sum(item.carbon_c for item in class_state if item.snag)
    downed_c = sum(item.carbon_c for item in class_state if not item.snag)
    stand.deadwood_state.class_state = sorted(class_state, key=lambda c: (c.species_group, c.snag, c.diameter_class, c.years_since_death))
    stand.deadwood_state.pools = DeadwoodPools(
        cwl=ChannelAWENH(non_soluble_c=snag_c),
        fwl=ChannelAWENH(non_soluble_c=downed_c),
        nwl=ChannelAWENH(),
    )
    stand.deadwood_state.source_pools = {
        "mortality": stand.deadwood_state.pools,
        "harvest": DeadwoodPools(),
        "disturbance": DeadwoodPools(),
    }
    return LegacyDeadwoodSummary(total_biomass_kg_per_ha=total_biomass, class_count=len(class_state))
