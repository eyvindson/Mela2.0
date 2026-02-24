# Bark beetle disturbance integration plan (Romeiro–Strimbu–Honkaniemi case)

## Goal and scope

This plan defines a practical case for adding **bark beetle damage** into the Mela/Metsi simulation workflow so that disturbance impacts can be represented in:

1. standing stock dynamics,
2. deadwood inflow accounting,
3. harvest/salvage decisions,
4. scenario-level risk and uncertainty outputs.

The design is aligned with a phased approach so the team can start with a lightweight scenario implementation and then move toward dynamic risk modeling.

---

## Scientific basis to encode

Use the workstreams by **Joyce Romeiro**, **Victor Strimbu**, and **Juha Honkaniemi** as model families to parameterize and validate:

- **Probability of attack / disturbance occurrence** (stand susceptibility and regional pressure),
- **Severity / mortality share conditional on attack**,
- **Post-disturbance management response** (especially salvage timing and intensity),
- **Carbon/deadwood consequences** from disturbance-caused tree death.

> Implementation rule: keep all coefficients/curves in external parameter tables so published updates can be integrated without code changes.

---

## Three implementation options

### Option A (fastest): exogenous disturbance scenarios

Inject bark beetle events from an external scenario file (year, region, species focus, severity class).

- Pros: rapid deployment, transparent assumptions, easy stress testing.
- Cons: no endogenous feedback from stand structure/climate.

Recommended for first delivery and policy stress-tests.

### Option B (recommended baseline): stand-level stochastic hazard model

At each time step, compute per-stand attack probability and severity using stand/site predictors (e.g., host share, age/DBH structure, prior stress, climate indicator, neighborhood pressure).

- Pros: realistic heterogeneity, integrates with alternative management pathways.
- Cons: requires calibrated coefficients and QA data.

Recommended as the default research-grade implementation.

### Option C (advanced): dynamic spread + management feedback

Add explicit infestation state and neighborhood transmission between stands (graph- or distance-based), with salvage affecting future spread pressure.

- Pros: best realism for outbreak dynamics.
- Cons: highest complexity and runtime; strongest data demand.

Recommended only after Option B is stable.

---

## Recommended phased roadmap

### Phase 1 — Disturbance schema + exogenous case (Option A)

1. Create a disturbance event schema (CSV/Parquet) with fields:
   - `year`, `region_id`, `species_group`, `attack_probability`, `severity_class`, `mortality_share`, `salvage_policy_id`.
2. Add a simulation operation `apply_bark_beetle_disturbance` that:
   - selects affected stands,
   - computes killed stems/biomass by tree group,
   - transfers killed biomass to deadwood disturbance channels,
   - tags stand state with disturbance metadata.
3. Add one reference scenario case:
   - historical-like outbreak period,
   - no-outbreak counterfactual,
   - intensified-climate outbreak stress case.

### Phase 2 — Endogenous hazard/severity (Option B)

1. Implement `estimate_bark_beetle_attack_probability(stand, context, params)`.
2. Implement `estimate_bark_beetle_severity(stand, context, params)`.
3. Draw stochastic outcomes with fixed random seeds per simulation branch for reproducibility.
4. Add model calibration package (parameter file + notebook/script) based on Romeiro/Strimbu/Honkaniemi datasets and equations.

### Phase 3 — Salvage behavior + economics

1. Add policy-specific salvage rules (immediate, delayed, constrained by capacity).
2. Route salvaged vs unsalvaged biomass separately in accounting.
3. Extend NPV calculation to include:
   - salvage revenues,
   - quality degradation penalties,
   - additional harvesting/logistics costs,
   - potential regeneration acceleration costs.

### Phase 4 — Spatial feedback (Option C, optional)

1. Add stand connectivity metric (adjacency/distance kernel).
2. Update attack pressure with lagged infestation prevalence.
3. Validate spread behavior against outbreak trajectories.

---

## Proposed integration points in current codebase

- **New natural-process operation** under `lukefi/metsi/domain/natural_processes/`:
  - `bark_beetle.py` for hazard/severity + mortality realization.
- **Deadwood routing** via existing disturbance inflow fields in `DeadwoodInflows`:
  - populate `disturbance_cwl_c`, `disturbance_fwl_c`, `disturbance_nwl_c`.
- **Data collection/output**:
  - include disturbance source rows (`source='disturbance'`) and new disturbance KPI outputs.
- **Control pipeline**:
  - expose operation in control files with parameter references (`operation_params` + `operation_file_params`).

---

## Minimal data model additions

### Stand state additions

- `bark_beetle_risk_index: float`
- `bark_beetle_last_attack_year: int | None`
- `bark_beetle_attack_count: int`
- `bark_beetle_current_severity: float`

### Scenario/context additions

- climate stress indicator (annual)
- regional infestation pressure index
- salvage capacity constraints by period/region

### Parameter tables (versioned)

- `beetle_attack_params.csv`
- `beetle_severity_params.csv`
- `beetle_salvage_policies.csv`
- `beetle_quality_loss_curves.csv`

---

## Core equations (template form)

### Attack probability

\[
P(attack_{s,t}) = \sigma(\beta_0 + \beta_1 host_{s,t} + \beta_2 structure_{s,t} + \beta_3 climate_t + \beta_4 pressure_{r,t} + \beta_5 management_{s,t-1})
\]

### Severity conditional on attack

\[
severity_{s,t} = g(\gamma_0 + \gamma_1 host_{s,t} + \gamma_2 stress_{s,t} + \gamma_3 pressure_{r,t})
\]

### Disturbance mortality biomass

\[
mortality\_biomass_{s,t} = standing\_biomass_{host,s,t} \times severity_{s,t}
\]

Then split mortality biomass into deadwood channels (CWL/FWL/NWL) using existing converter logic and species-specific shares.

---

## Case design for first analysis run

Build a 30-year case set with 3 scenarios and 100 stochastic replicates each:

1. **Baseline**: no beetle disturbance module active.
2. **Moderate outbreak**: calibrated pressure pathway with current climate trend.
3. **Severe outbreak**: elevated pressure and higher climate stress.

For each scenario, run 3 management policies:

- BAU thinning/harvest,
- proactive risk-reduction thinning,
- reactive salvage-priority strategy.

This yields 9 policy-scenario combinations × 100 replicates.

---

## Outputs and KPIs

### Disturbance ecology KPIs

- attacked area share (% area/year)
- disturbance-killed stems/ha
- disturbance-killed biomass and carbon (kgC/ha)
- time to outbreak peak and recovery

### Production/economy KPIs

- merchantable volume losses
- salvage harvest volume and timing
- NPV distribution (mean, p10, p90)
- value-at-risk under severe outbreak

### Carbon/deadwood KPIs

- disturbance inflow to deadwood (CWL/FWL/NWL)
- total deadwood stock trajectory
- net ecosystem carbon balance proxy (if enabled)

---

## Validation protocol

1. **Face validation** with domain experts (trajectory shape, species response, management realism).
2. **Internal checks**:
   - mass balance of biomass/carbon,
   - monotonicity checks for severity limits [0,1],
   - reproducibility by seed.
3. **Historical back-cast** on known outbreak years/areas.
4. **Sensitivity/uncertainty**:
   - perturb key coefficients ±10–30%,
   - report elasticity of NPV and carbon outcomes.

---

## Implementation checklist

- [ ] Define disturbance schema and parameter files.
- [ ] Implement `apply_bark_beetle_disturbance` operation.
- [ ] Wire disturbance mortality to deadwood inflows.
- [ ] Add control-file configuration examples.
- [ ] Add scenario runner for replicate ensembles.
- [ ] Add validation and sensitivity scripts.
- [ ] Document assumptions, coefficient provenance, and versioning.

---

## Practical recommendation

Start with **Option A + Phase 1** immediately to deliver decision-useful scenarios fast, while preparing **Option B** calibration in parallel as the long-term default. This balances delivery speed and scientific rigor and fits naturally with existing disturbance-aware deadwood accounting.
