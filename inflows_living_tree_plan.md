# Plan: Add living-tree and understory litter inflows to deadwood/soil-carbon input accounting

## 1) Problem statement

Current deadwood inflow accounting focuses on episodic sources:
- tree mortality,
- harvest residues,
- disturbance residues.

This misses **continuous litter inputs** from living vegetation (foliage turnover, branch turnover, fine-root turnover, etc.) and **understory litter**, which can produce unrealistic `input_c = 0` periods in unmanaged stands.

## 2) Target outcome

For every simulation step, add explicit inflow terms for:
1. Living-tree litterfall/turnover
2. Understory litterfall/turnover

and expose them in outputs so that:
- total `input_c` reflects both episodic and continuous inputs,
- source-level outputs distinguish living-tree and understory contributions,
- unmanaged stands receive non-zero background inputs in biologically plausible conditions.

## 3) Scope decisions (recommended)

### In-scope (Phase 1)
- Add new modeled inflow sources:
  - `living_tree_litter`
  - `understory_litter`
- Route these to channels (`cwl`, `fwl`, `nwl`) with an MVP policy.
- Store source-level results in `deadwood_source_ledger`.
- Include in stand-level `deadwood_pools.input_c`.
- Add configurable parameters and conservative defaults.

### Out-of-scope (Phase 1)
- Dynamic understory growth submodel.
- Site/process coupling to external nutrient/water models.
- Species- and climate-calibrated turnover for all Finnish vegetation classes (can be Phase 2+).

## 4) Conceptual accounting model

For each stand and time step `dt` years:

`input_c_total = input_c_mortality + input_c_harvest + input_c_disturbance + input_c_living_tree_litter + input_c_understory_litter`

Where the two new terms are built from stock × turnover (or trait-based surrogates):

- `living_tree_component_input = component_carbon_stock * annual_turnover_rate * dt`
- `understory_input = understory_carbon_stock_or_proxy * annual_turnover_rate * dt`

### Recommended channel mapping (MVP)

- `cwl`: coarse woody fraction from branch/coarse-woody turnover (usually small in annual litterfall)
- `fwl`: fine woody + fine-root turnover
- `nwl`: foliage + herbaceous/non-woody litter

If needed, start with simplified mapping:
- living-tree foliage -> `nwl`
- living-tree fine roots -> `fwl`
- living-tree branch turnover -> `fwl` (or partial `cwl` by branch size threshold)
- understory litter -> `nwl`

## 5) Implementation architecture

## 5.1 Data model changes

### `DeadwoodInflows` extension
Add fields (or equivalent grouped structure):
- `living_tree_cwl_c`
- `living_tree_fwl_c`
- `living_tree_nwl_c`
- `understory_cwl_c`
- `understory_fwl_c`
- `understory_nwl_c`

and ensure `total_c` includes these.

### Source-ledger source enum expansion
Add two new source labels in source flux breakdown:
- `living_tree_litter`
- `understory_litter`

## 5.2 Configuration changes

Extend `DeadwoodInflowConfig` with toggles + defaults:
- `include_living_tree_litter: bool = True`
- `include_understory_litter: bool = True`
- `living_tree_turnover_rates: dict[str, float]`
  - e.g. `{"foliage": 0.20, "fine_root": 0.60, "branch": 0.02}` annual
- `understory_litter_c_kg_ha_yr: float`
  - conservative default by site class (or global default if site class unavailable)
- optional `branch_turnover_to_cwl_share` for channel split.

Include validation bounds `[0, 1]` for rates and non-negative checks for mass flux settings.

## 5.3 Inflow builder logic

In `build_deadwood_inflows(...)` path:
1. Keep existing episodic pathways unchanged.
2. Compute living-tree litter from **current living tree biomass** using existing biomass converter outputs.
3. Compute understory litter from:
   - lookup table by stand/site type (preferred), or
   - global fixed default (MVP fallback).
4. Convert both to channelized C inflows.
5. Return combined `DeadwoodInflows`.

Pseudo-flow:

1. `living_components = converter.component_carbon_kg_per_ha(current_trees)`
2. `living_litter = apply_turnover(living_components, turnover_rates, dt)`
3. `understory_litter = understory_proxy(site_type, dt)`
4. `channelize + add to inflows`

## 5.4 Deadwood operation integration

In `update_deadwood_pools_fn(...)`:
- Add source buckets to `source_inflows` and `source_pools`:
  - `living_tree_litter`
  - `understory_litter`
- Run backend step per source as already done.
- Aggregate source fluxes as today.

Backward compatibility:
- If new sources disabled, behavior should match old outputs (except for any intentional bugfixes).

## 5.5 Output/schema updates

Ensure both tables carry interpretable results:
- `deadwood_pools.input_c` includes new terms.
- `deadwood_source_ledger.source` includes new source names.

No column changes are strictly required if using existing `(source, input_c, decomposition_c, net_change_c)` pattern.

## 6) Parameterization strategy

## 6.1 MVP defaults (pragmatic)
- Use literature-informed but conservative turnover defaults.
- Keep these in one config module with provenance comments.
- Provide easy overrides in control profile.

## 6.2 Improvement path (Phase 2)
- Species-group specific turnover rates (pine/spruce/broadleaf).
- Climate or age modifiers.
- Site fertility dependence for understory litter.

## 7) Validation and tests

## 7.1 Unit tests
1. **Living-tree litter inflow positive** when trees exist and feature enabled.
2. **Understory inflow positive** with default understory setting.
3. **Disabled flags** produce zero for corresponding sources.
4. **Total consistency**: `input_c_total == sum(all source inputs)`.
5. **Backward compatibility mode**: with new flags off, old baseline snapshots match.

## 7.2 Integration tests
- Run unmanaged stand scenario across multiple periods and verify:
  - `input_c > 0` in biologically active periods,
  - new source rows appear in `deadwood_source_ledger`.

## 7.3 Sanity checks
- Mass balance trend checks for extreme stands.
- No negative inflows from turnover.
- Reasonable magnitude relative to living biomass.

## 8) Rollout plan

### Step A: Plumbing
- Add config + data structure fields.
- Add source names and source-pool handling.

### Step B: Living-tree litter implementation
- Implement turnover computation using existing biomass converter.
- Add tests.

### Step C: Understory implementation
- Implement simple proxy (global/site-class default).
- Add tests.

### Step D: Documentation + example profile
- Update README deadwood section with formulas and defaults.
- Add control example showing how to tune new parameters.

### Step E: Calibration pass
- Compare outputs against expected regional ranges.
- Adjust defaults as needed.

## 9) Risks and mitigations

1. **Risk: double counting with mortality pathways**
   - Mitigation: define living-tree litter as turnover of *surviving* biomass components only, exclude mortality/removed trees.

2. **Risk: overestimated inputs due to aggressive defaults**
   - Mitigation: conservative rates, parameter bounds, scenario sensitivity tests.

3. **Risk: conceptual mismatch (deadwood vs soil-litter pools)**
   - Mitigation: document that this is currently an aggregated litter-to-Yasso input stream; optionally split destination pools in later phases.

4. **Risk: missing understory state variables**
   - Mitigation: start with fixed/site-class proxy and replace later with dynamic understory model.

## 10) Deliverables checklist

- [ ] Data model supports living-tree + understory inflow channels.
- [ ] Config supports enabling and tuning both pathways.
- [ ] Inflow builder computes and channelizes new inputs.
- [ ] Operation and source-ledger include two new sources.
- [ ] Unit/integration tests added and passing.
- [ ] README/docs updated with assumptions and limitations.

## 11) Suggested first implementation PR split

1. **PR 1: data+config scaffolding** (no behavior change if disabled)
2. **PR 2: living-tree litter calculations + tests**
3. **PR 3: understory proxy + tests + docs**
4. **PR 4: calibration defaults + scenario validation notes**

This staged approach minimizes regression risk and keeps reviewable increments.


## 12) What data and models are required (and what makes implementation easier)

This section answers the practical question: what is minimally required vs. what would materially improve realism and reduce development effort.

### 12.1 Minimum viable inputs (to implement quickly)

1. **Tree-level state already in simulation**
   - Species, DBH, height, stems/ha (already used by biomass conversion).
2. **Turnover-rate parameter table for living trees**
   - Annual fractions for at least foliage, fine roots, and branches.
   - Can start as species-group constants (`pine/spruce/broadleaf`).
3. **Understory litter model output (stand-level)**
   - Preferred input: `kgC/ha/year` (or convertible from dry mass).
4. **Carbon conversion factor**
   - If understory model is dry mass: need C fraction (e.g. 0.45–0.5).

With these, implementation can proceed without adding new growth engines.

### 12.2 Data/models that would make the task much easier (recommended)

1. **A callable understory litter model** (you already have this)
   - Interface suggestion:
     - Inputs: stand/site descriptors + year/climate (optional)
     - Output: annual litter C flux by component or total (`kgC/ha/year`)
   - Biggest accelerator: avoids inventing fixed proxies and improves unmanaged-stand realism immediately.

2. **Component-resolved understory outputs**
   - If model gives separate fractions (e.g. dwarf shrubs, herbs/graminoids, mosses, fine woody), channel mapping to `fwl/nwl` is much cleaner.

3. **Species-group litter turnover coefficients for trees**
   - Separate rates for foliage, fine roots, and branch turnover by pine/spruce/broadleaf.
   - Optional modifiers by age/site fertility/climate.

4. **Site-type keyed lookup tables**
   - For fallback behavior when model inputs are missing.
   - Enables robust operation even with partial stand metadata.

5. **Calibration dataset / benchmarks**
   - Independent expected ranges of annual litter C input by site and dominant species.
   - Useful for unit tests + plausibility gates.

### 12.3 Proposed integration path for your understory model

Given you have understory litter production models, use them as the primary source in Phase 1:

1. Add an adapter interface in deadwood inflow code, e.g. `UnderstoryLitterProvider`.
2. In config, allow either:
   - `understory_litter_provider` (model-based), or
   - `understory_litter_c_kg_ha_yr` fallback constant.
3. At runtime:
   - If provider exists and returns valid value -> use provider output.
   - Else -> use fallback default and log a warning counter.
4. Convert to channel inflows:
   - If output is total litter only -> route mainly to `nwl` (MVP).
   - If output has woody/non-woody split -> map woody to `fwl`/`cwl`, non-woody to `nwl`.

### 12.4 Suggested provider contract (simple)

```python
class UnderstoryLitterProvider(Protocol):
    def annual_litter_c_kg_ha(
        self,
        stand: ForestStand,
        year: int,
        climate: YassoClimate | None = None,
    ) -> float | dict[str, float]:
        ...
```

Accepted outputs:
- `float`: total annual `kgC/ha/year`
- `dict`: component-wise annual `kgC/ha/year`, e.g. `{"non_woody": x, "fine_woody": y}`

### 12.5 Unit harmonization checklist (important)

To avoid integration bugs, standardize before plugging in:
- Time basis: annual vs. per-step (convert with `dt_years`).
- Area basis: per ha.
- Carbon basis: carbon mass (not dry biomass unless converted).
- Sign convention: positive values are inputs to litter/deadwood pathway.

### 12.6 If data are limited right now

Start with this robust fallback stack:
1. Fixed living-tree turnover coefficients by species group.
2. Your understory model where available.
3. Site-type constant understory fallback where model cannot run.
4. Global constant as final fallback.

This gives immediate non-zero unmanaged inputs while keeping a clear upgrade path.
