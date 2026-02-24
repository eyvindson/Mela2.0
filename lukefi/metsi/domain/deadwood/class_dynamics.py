from collections import defaultdict

from lukefi.metsi.domain.deadwood.types import DeadwoodClassState, DeadwoodInflows


def update_class_state(
    class_state: list[DeadwoodClassState],
    inflows: DeadwoodInflows,
    years: int,
    downing_rate_per_year: float = 0.1,
) -> list[DeadwoodClassState]:
    """Deterministic MVP transition rule for deadwood classes.

    - Existing classes age by `years`.
    - A fixed fraction of snags transitions to downed state per step.
    - New inflows are added as fresh snag entries by source.
    """

    transitioned: defaultdict[tuple[str, bool, str, int], float] = defaultdict(float)
    for state in class_state:
        aged_years = state.years_since_death + years
        downed_fraction = 1.0 - (1.0 - downing_rate_per_year) ** years if state.snag else 1.0
        snag_carbon = max(0.0, state.carbon_c * (1.0 - downed_fraction)) if state.snag else 0.0
        downed_carbon = state.carbon_c - snag_carbon
        if snag_carbon > 0.0:
            transitioned[(state.species_group, True, state.diameter_class, aged_years)] += snag_carbon
        if downed_carbon > 0.0:
            transitioned[(state.species_group, False, state.diameter_class, aged_years)] += downed_carbon

    inflow_total = {
        "mortality": inflows.mortality_c,
        "harvest": inflows.harvest_residue_c,
        "disturbance": inflows.disturbance_c,
    }
    for source, carbon_c in inflow_total.items():
        if carbon_c > 0.0:
            transitioned[(source, True, "mixed", 0)] += carbon_c

    return [
        DeadwoodClassState(
            species_group=species_group,
            snag=snag,
            diameter_class=diameter_class,
            years_since_death=years_since_death,
            carbon_c=carbon_c,
        )
        for (species_group, snag, diameter_class, years_since_death), carbon_c in sorted(transitioned.items())
    ]
