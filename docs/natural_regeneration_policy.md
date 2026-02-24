# Natural regeneration policy proposal (continuous cover + low basal area)

This note proposes a practical way to include `regeneration(type="natural")` in Mela2.0 workflows.

## 1) When to trigger natural regeneration

Use natural regeneration only when at least one of these conditions is true:

1. **Continuous-cover management has been used** (e.g. selection/partial cuts in the recent period).
2. **Basal area is low after treatment**, indicating a regeneration gap.

Recommended trigger variables:

- `G` = stand basal area (m²/ha)
- `N_small` = stems/ha in small trees (for example `d < 8 cm`)
- management history tags (e.g. `cc_*`, or explicit event tags)

Proposed trigger:

- Trigger natural regeneration if:
  - `continuous_cover_recent == True` AND `G < G_cc_min`, or
  - `G < G_open_min` regardless of method.

Suggested starting thresholds (tune by site):

- `G_cc_min = 10..14 m²/ha`
- `G_open_min = 8..10 m²/ha`

And add one more guard:

- skip regeneration if `N_small` already exceeds a target (example `>= 1500 stems/ha`).

## 2) Species choice rules (simple and robust)

For a first implementation, use rule-based species choice:

- **Dry/sub-dry mineral soils**: favor pine (`species=1`)
- **Mesic/herb-rich soils**: favor spruce (`species=2`) and/or birch (`species=3/4`)
- **Peatland or wet patches**: increase deciduous share

Use a mixed strategy rather than one species only, for example:

- pine 60%, birch 40% on drier sites
- spruce 70%, birch 30% on fresher sites

## 3) Event-level implementation in this repository

The repository already supports natural regeneration by setting:

- `treatment=regeneration`
- `static_parameters["type"] = "natural"`

and passing species + stem count etc.

### Example control snippet

```python
Event(
    treatment=regeneration,
    static_parameters={
        "origin": 1,
        "method": 1,
        "species": 2,           # spruce
        "stems_per_ha": 500.0,
        "height": 0.4,
        "biological_age": 2.0,
        "type": "natural",
        "ntrees": 10,
    },
    tags={"natural_regen_gapfill"},
)
```

## 4) Practical scheduling pattern

For each decision year:

1. Run harvest / continuous-cover operation.
2. Recompute stand state.
3. If trigger condition is true, add one or more natural regeneration events (possibly by species share).
4. Continue growth transition.

A conservative first policy:

- Only allow one natural regeneration pulse per 10-year window.
- Limit added stems to a cap (example 300–800 stems/ha per pulse).

## 5) Calibration approach

Calibrate by comparing simulated outcomes to local targets:

- post-treatment basal area trajectory
- species composition after 20–30 years
- density of recruit/sapling cohorts

Tune in this order:

1. Trigger threshold (`G_cc_min`, `G_open_min`)
2. Added stems/ha per pulse
3. Species split by site type

## 6) Notes on literature

In this execution environment, external web access was blocked, so this document is a pragmatic implementation template based on commonly used Finnish silvicultural principles (continuous cover, site-adapted species choice, and gap-filling under low basal area).

When internet access is available, validate the thresholds against:

- Tapio “Hyvän metsänhoidon suositukset” (latest version)
- Luke / Metsäkeskus material on natural regeneration under continuous-cover forestry
- Recent Nordic/Finnish studies on ingrowth response to residual basal area
