# Deadwood integration plan for Mela2.0

## Purpose

This note translates the uploaded `dead/` material into an implementable roadmap for this repository.
The source files come from a different simulator architecture, so this plan focuses on **reusing concepts and equations**, not direct drop-in integration.

## What we have in `dead/`

- `yasso07.py` + binary wrappers (`y07.so`, `y07.pyd`): a Python frontend that advances Yasso pools (AWENH) for coarse woody litter, fine woody litter, and non-woody litter.
- `BiomassmodelLibrary.[ch]`: biomass equations (Marklund, Repola, Petersson–Ståhl variants) and biomass component structures.
- `NaturalremovalmodelLibrary.[ch]`: natural mortality / removal functions (legacy C API style).
- `DistributiondeadtreemodelLibrary.[ch]`: dead-tree distribution state by species, snag/downed state, diameter class, and years-since-death class.
- `deadwood_diversity_jyu.py`: deadwood biodiversity index based on deadwood volume and decay-class diversity.
- `harvest.py`: legacy simulator harvest logic (not directly reusable due to external dependencies and data contracts).

## Compatibility assessment vs this repo

### Current Mela2.0 capabilities relevant to deadwood

1. Growth updates and mortality effects exist in growth modules:
   - `grow_metsi` computes stem deltas and prunes trees with `stems < 1.0`.
   - `grow_motti_dll` treats missing returned tree IDs as dead/removed (`stems -> 0`).
2. Harvest removals are captured via collected data (`RemovedTrees`).
3. Biomass reporting is documented (`stem_waste`, `dead_branches`, etc.), but no full deadwood + soil decomposition bookkeeping is currently integrated in this repo.

### Reuse potential of uploaded assets

#### High reuse potential (concept/equation level)

- **`yasso07.py` model interface and AWENH pool bookkeeping logic**: strong candidate to port into a clean Mela2.0 adapter.
- **Biomass equations from `BiomassmodelLibrary`**: useful for converting mortality and harvest residues into dead organic matter inputs.
- **Dead-tree class/state ideas from `DistributiondeadtreemodelLibrary`**: useful for stand-level deadwood state representation and biodiversity indicators.
- **`deadwood_diversity_jyu.py`**: can be implemented as a post-processing indicator operation once deadwood states exist.

#### Medium reuse potential (requires substantial reframing)

- **Natural removal C models**: logic may help calibrate or split mortality pools, but API/signatures need full translation.

#### Low direct reuse potential

- **`harvest.py`**: tightly coupled to SIMO-style operation signatures and modules (`HarvestData`, `HarvestOperation`, etc.); use only as reference for flow logic.

## Proposed target architecture in Mela2.0

## 1) New domain module layer

Create a new namespace under `lukefi/metsi/domain/deadwood/`:

- `types.py`
  - Dataclasses for deadwood pool state and fluxes.
  - Example: `DeadwoodPools`, `DeadwoodInflows`, `DeadwoodOutflows`, `DeadwoodDiagnostics`.
- `biomass_conversion.py`
  - Species/component biomass conversion helpers.
  - Initial implementation can be table-driven with configurable coefficients.
- `mortality_inputs.py`
  - Build deadwood inflows from natural mortality and optionally from harvest residues.
- `yasso_adapter.py`
  - Thin adapter around selected Yasso backend.
  - Supports backend strategy: `python_impl | native_binary | external_service`.
- `distribution.py`
  - Optional snag/downed + diameter + age-since-death class transitions.
- `diversity.py`
  - Deadwood diversity indicator calculation(s).

## 2) Integration operation(s)

Add one or two operations in simulation chains:

- `update_deadwood_pools`
  - Reads stand state and collected removals.
  - Converts biomass to litter/wood inputs.
  - Advances Yasso pools.
  - Updates stand-attached deadwood state and emits collected outputs.
- `report_deadwood`
  - Emits diagnostics for outputs/DB export.

## 3) Data persistence and output

- Extend collected data structures for deadwood pools/fluxes.
- Add DB table(s) for pool states by node + stand + time point.
- Add optional biodiversity index output.

## 4) Configuration strategy

Introduce declarative params in `control*.py` operation params:

- biomass equation set / coefficients
- transfer fractions (mortality -> snag/downed/fine)
- carbon fraction defaults
- Yasso climate forcing source and timestep handling
- class discretization choices for deadwood distribution

## MVP implementation plan (phased)

### Phase 0 — Scaffolding

- Add deadwood data classes and no-op operation hooks.
- Add tests validating that operations can run without changing existing workflows.

### Phase 1 — Mortality + harvest inflow accounting

- Implement inflow computation from:
  - natural mortality signals in growth outputs,
  - `RemovedTrees` harvest outputs where configured as residue/non-merchantable.
- Implement species-group and component splits.
- Unit tests for mass-balance on inflow builder.

### Phase 2 — Biomass conversion

- Implement configurable biomass converter.
- Add regression tests from known coefficient cases.

### Phase 3 — Yasso integration

- Implement Yasso backend adapter and pool-step function.
- Support AWENH pool mapping for cwl/fwl/nwl-like compartments.
- Add deterministic tests with fixed climate and infall.

### Phase 4 — Deadwood distribution + diversity indicator

- Implement optional distribution classes (species × snag/downed × diameter × years-since-death).
- Add `deadwood_diversity` indicator calculation.

### Phase 5 — Reporting and scenario controls

- Add DB export tables and optional report operations.
- Add example control configuration and documentation.

## Technical risks and mitigations

- **Binary dependency risk (Yasso `.so`/`.pyd`)**: encapsulate backend behind adapter; provide pure-Python fallback path.
- **Double counting risk (harvest + mortality + biomass outputs)**: enforce explicit input-source flags and a mass-balance validator.
- **Time-step mismatch risk (5-year growth vs annual decomposition)**: standardize internal decomposition stepping (substepping if needed).
- **Species/equation mismatch risk**: use a small, explicit species-group mapping table with validation.

## Decisions needed from product/science side

1. Preferred Yasso backend and deployment constraints (Python-only vs compiled library allowed).
2. Which biomass equation family to treat as default.
3. Carbon fraction constants and whether species-specific values are required.
4. Should harvest residues enter deadwood pools in MVP, or only natural mortality.
5. Whether to implement deadwood class distribution in MVP or postpone.
6. Required outputs for calibration/validation and their aggregation level.

## Suggested first sprint scope (practical)

If we want fast progress with low risk, start with:

- Phase 0 + Phase 1 + minimal Phase 3 (single pooled Yasso bucket per stand/species-group),
- and postpone class distribution/diversity to Sprint 2.

This gives immediate deadwood pool estimates and enables iterative calibration.

## Handoff checklist for next agent

- [ ] Confirm scientific defaults from user (backend, coefficients, transfer fractions).
- [ ] Implement deadwood dataclasses and operation skeletons.
- [ ] Add unit tests for inflow mass-balance and deterministic pool stepping.
- [ ] Add one example `control_*.py` scenario using new operation.
- [ ] Document operation parameters in `README.md`.

---

## Status update after initial scaffold PR (for next agent)

### What is now implemented

- New deadwood package exists under `lukefi/metsi/domain/deadwood/` with:
  - state and pool dataclasses,
  - inflow builder,
  - placeholder Yasso adapter,
  - DB collected data writer,
  - `update_deadwood_pools` treatment skeleton.
- Example control profile `control_deadwood_mvp.py` exists.
- README has a deadwood MVP section.
- User decisions captured:
  - default equation set: **Repola**,
  - include harvest residues in MVP: **yes**,
  - binary Yasso backend acceptable: **yes**,
  - output granularity now: **stand total first**,
  - biodiversity indicator: **postpone**.

### Gaps identified from scaffold review

1. Inflow assembly still uses a Repola **proxy** rather than documented equation coefficients from deadwood source material.
2. Operation-level wiring to consume `RemovedTrees` directly from simulation event outputs is still manual and should be made explicit.
3. Yasso adapter currently uses a deterministic placeholder decay model; real binary-backed stepping is not yet integrated.
4. Climate forcing path for Yasso is still missing.
5. Tests cover contracts, but no end-to-end simulation test asserts DB deadwood rows after a growth/harvest sequence.

### Proposed next-agent work plan (priority order)

#### Step A — Biomass conversion hardening (Phase 2 entry)
- Add `biomass_conversion.py` with explicit `RepolaBiomassConverter` interface.
- Move current proxy formula behind a clearly named fallback implementation.
- Add coefficient-table loading and source-version logging in outputs.
- Add tests for known tuples from literature/reference implementation.

#### Step B — Event/output wiring for residues (finish Phase 1)
- Define how `RemovedTrees` collected data is passed into `update_deadwood_pools` without manual parameter plumbing.
- Add integration tests for natural mortality + harvest residues in the same step.
- Add a per-source inflow ledger (`mortality`, `harvest`, `disturbance`) persisted in DB.

#### Step C — Real Yasso backend integration (Phase 3)
- Implement binary adapter for `dead/y07.so` (and Windows `.pyd` guard).
- Keep deterministic pure-Python fallback for testability and portability.
- Add climate adapter inputs `(temperature, precipitation, amplitude)` and 5x annual sub-stepping for 5-year growth steps.

#### Step D — Output shaping for MVP
- Keep stand-total outputs as default.
- Add optional species-group (`pine/spruce/broadleaf`) breakdown flag for next phase, but keep disabled by default.
- Document output table schema and version in README.

### Questions for user before next implementation PR

1. For Repola implementation, should the next PR target **stem + branch + foliage + stump + roots** immediately, or start with **stem + branch only** and expand next?
2. For harvest residues, do you want a single global residue fraction (current style) or species-group specific defaults already in next PR?
3. For Yasso climate forcing in MVP, should we start with one static Finland-wide default profile, or derive climate per stand from available stand metadata first?
4. For stand-total output, do you want only `total_c` and `net_change_c`, or also keep AWENH columns visible in DB from the beginning?
5. Should the next PR include a migration/backward-compatibility note for existing consumers of simulation DB outputs?


---

## Plan update after PR review + historical dead/ code re-check

### Reflection on what was implemented vs plan

What moved forward:
- Phase 1/2 direction is in place: stand-level inflow accounting exists, harvest residues are included, and component-level bookkeeping now explicitly covers `stem + branch + foliage + stump + roots`.
- Species-group residue defaults were added (`pine/spruce/broadleaf`) as requested.
- A climate-ready Yasso interface exists with a static Finland default profile and a hook for future stand-wise forcing.
- AWENH pool columns are visible in DB output.

What is still not aligned with the intended science-level integration:
1. Repola support is still a **proxy mass equation**, not the explicit Repola function family from `BiomassmodelLibrary`.
2. Yasso integration is still a **placeholder decay routine**, not a native `y07`/`mod5c` bridge.
3. Historical `yasso07.py` structure uses **three litter channels** (`cwl`, `fwl`, `nwl`) each with AWENH stocks/inputs; current implementation still mixes inputs into one aggregate AWENH bucket.
4. Historical dead-tree distribution (`species × snag/down × diameter × since_death`) is not yet represented in Mela2.0 state.
5. Inflow source accounting lacks a persistent per-source ledger table (`mortality/harvest/disturbance`) and therefore still has double-counting risk in audits.

### Historical integration notes (from `dead/` core files)

- `dead/yasso07.py` runs `mod5c` separately for `cwl`, `fwl`, `nwl`, with climate tuple `(temp, rain, amplitude)` and per-channel AWENH stocks/infall.
- `dead/BiomassmodelLibrary.c` function family `Biomass_tree_JKK` composes species-specific Repola components (living/dead branches, needles/leaves, stump, roots) and uses density models where needed.
- `dead/DistributiondeadtreemodelLibrary.[ch]` defines dead-tree classes with dimensions: species, diameter class, years-since-death, and snag state.
- `dead/NaturalremovalmodelLibrary.c` exposes competition/aging mortality probabilities by species/site context; this can later inform mortality-source splitting and calibration priors.

### Updated next-step plan (priority order)

#### Step 1 — Replace Repola proxy with explicit coefficient-backed component conversion
- Build a coefficient-backed converter module that maps Mela species -> Repola variant (`pine/spruce/birch+other broadleaf`).
- Keep component outputs explicit: stem, branch, foliage, stump, roots.
- Add reference regression tests using frozen tuples extracted from `BiomassmodelLibrary` outputs.

#### Step 2 — Reshape Yasso state to channel-aware bookkeeping
- Add channel state model: `cwl_awenh`, `fwl_awenh`, `nwl_awenh` (each with A/W/E/N/H).
- Define deterministic mapping from components to channels:
  - coarse woody -> `cwl` (mainly stem, stump, coarse roots),
  - fine woody -> `fwl` (branches, fine roots share),
  - non-woody -> `nwl` (foliage and fine litter share).
- Preserve stand-total outputs while keeping channel/pool values in DB columns.

#### Step 3 — Integrate real Yasso backend behind adapter
- Implement binary adapter path for `dead/y07.so` (`y07.pyd` guard on Windows).
- Retain pure-Python fallback for CI portability.
- Keep 5-year timestep as annual substeps and document exact stepping semantics.

#### Step 4 — Explicit source-ledger output
- Add DB table for source-specific inflows (`mortality`, `harvest`, `disturbance`) and net decomposition for auditability.
- Add mass-balance validation checks at operation level.

#### Step 5 — Begin distribution-state MVP (pre-diversity)
- Add optional deadwood class state container (species × snag/down × diameter × since_death) without full biodiversity indicator yet.
- Wire one minimal transition rule so the structure can be validated and exported.

### Questions for user before next implementation PR

1. **Repola source of truth:** Do you want the next PR to directly port equations from `BiomassmodelLibrary` now (for pine/spruce/broadleaf), or to first add a validated coefficient table that reproduces it numerically and port C formulas in the following PR?
2. **Channel mapping policy:** Please confirm component-to-channel defaults:
   - `stem + stump + coarse roots -> cwl`
   - `branches + fine roots -> fwl`
   - `foliage -> nwl`
   Is this acceptable for MVP?
3. **Roots split default:** For roots, should we use a fixed coarse/fine split in MVP (e.g. 70/30), and if yes, what default split do you prefer?
4. **Yasso backend rollout:** For the next PR, should binary `y07` be the default backend when available (with automatic fallback), or should fallback remain default until parity tests are complete?
5. **Climate source for now:** Confirm that the static Finland profile should remain default, and whether you want the code to already accept per-stand climate arrays from metadata (even if not yet populated).
6. **Source-ledger schema:** Do you want the new ledger as one row per source per timestep, or one row with separate `mortality_c/harvest_c/disturbance_c` columns?
7. **Distribution-state timing:** Should we include the initial deadwood class-state table already in next PR, or keep that for the following PR after binary Yasso is in place?
8. **Validation targets:** Do you have any historical scenario/case (stand data + expected trends) we should use as acceptance checks for the next PR?

---

## Plan refresh after unsatisfied PR review (current cycle)

### What likely went wrong in the previous PR (technical reflection)

After re-reading the implementation and the historical `dead/` sources, the previous PR appears to have moved in the right direction conceptually, but there are still integration risks that can explain dissatisfaction:

1. **Scientific parity is not yet proven**
   - Repola equations were ported, but there is still no parity harness that numerically compares Python outputs against the legacy C implementation across representative `(species, dbh, height, stems)` tuples.
   - Without this, we cannot guarantee equation-family correctness and unit consistency end-to-end.

2. **Yasso stepping semantics are still incomplete against historical flow**
   - The `dead/yasso07.py` reference runs channel-specific `mod5c` with `infall / dur` and relies on model-internal handling for duration.
   - The current adapter does call `mod5c`, but we still lack a validated parity check against reference trajectories (including 5-year steps, channel diameters, and climate settings).

3. **Channelized state is present, but reporting contract is still under-specified**
   - DB schema now stores channel totals and source-ledger rows, but consumers and migration expectations are not yet documented as a versioned contract.
   - There is no agreed compatibility strategy for existing readers expecting previous deadwood columns.

4. **Testing remains too shallow for this integration stage**
   - Unit-style tests exist, but there is still no scenario-level acceptance test that executes growth + removals + deadwood update and verifies DB outputs and mass balance for each source.

5. **Event wiring still depends on ad-hoc stand attributes**
   - Residue and climate inputs can be injected through stand attributes (`deadwood_removed_trees`, `deadwood_climate`), but there is no finalized pipeline contract from collected simulation outputs to deadwood operation inputs.

### Research notes from source re-check (what still must be mirrored)

1. **`dead/BiomassmodelLibrary.c`**
   - The Repola family includes species-specific formulas with different predictors (some require `log(h)`, some `h/(h+k)`, and birch roots depend on both `d` and `h`).
   - This means acceptance tests must cover low/high DBH and height edge ranges per species, not just one nominal value.

2. **`dead/yasso07.py`**
   - Explicitly maintains three channels (`cwl`, `fwl`, `nwl`) each with AWENH stock vectors and channel-specific diameter handling.
   - Any MVP claiming parity should at minimum validate channel-wise behavior and not only stand-total carbon.

3. **`dead/DistributiondeadtreemodelLibrary.[ch]`**
   - Class-state dimensions are already defined in legacy logic, so the next realistic step is table/schema scaffolding and state persistence before indicator formulas.

4. **`dead/NaturalremovalmodelLibrary.[ch]`**
   - Even if not directly ported now, this can provide priors/logic for future separation of mortality sources (competition vs background vs disturbance).

### Core tasks remaining (ordered)

#### Task 1 — Build parity harnesses before new logic expansion
- Add executable parity tests for Repola formulas against frozen reference values derived from legacy functions.
- Add Yasso parity smoke tests for one-step and multi-step channel trajectories (with static Finland climate).

#### Task 2 — Finalize data contracts for deadwood outputs
- Version and document DB schema for:
  - `deadwood_pools` (channel totals + optional channel AWENH columns),
  - `deadwood_source_ledger` (one row per source per timestep).
- Add migration notes and compatibility policy for downstream consumers.

#### Task 3 — Solidify operation input wiring
- Replace implicit stand-attribute handoff with an explicit operation contract from simulation events/collected data.
- Ensure no double counting between mortality signal and removed-tree residues.

#### Task 4 — Add scenario-level integration validation
- Introduce one deterministic integration scenario (mortality + harvest in same step).
- Assert:
  - per-source inflow sums,
  - decomposition + stock mass balance,
  - DB row existence and schema-level correctness.

#### Task 5 — Prepare distribution-state scaffolding (next PR after parity)
- Add class-state storage schema only (no full indicator yet).
- Include minimal transition placeholder to validate persistence and future integration path.

### Updated questions for user (to unlock the next PR cleanly)

1. **Parity threshold policy:**
   - What numeric tolerance should we require for Repola parity tests vs legacy reference values (e.g. relative error ≤ 1e-6, 1e-4, or other)?

2. **Reference set scope:**
   - Do you prefer a small curated parity set (fast CI) or a broader grid across DBH/height/species (slower but more robust)?

3. **Output contract strictness:**
   - Should we freeze `deadwood_pools` as channel totals only for MVP, or include optional per-channel AWENH columns now to avoid future schema churn?

4. **Ledger semantics:**
   - Confirm that the source ledger should remain **one row per source per timestep** and whether decomposition should also be source-attributed or remain stand-level aggregate for now.

5. **Operation wiring policy:**
   - Do you want deadwood update to consume removals/climate only through explicit operation parameters (strict), or keep metadata fallback paths for transitional compatibility?

6. **Acceptance scenario definition:**
   - Can you provide one canonical stand scenario (or even rough expected trend constraints) for acceptance, e.g. “post-harvest deadwood rises sharply then declines over the next two steps”?

7. **Distribution-state start point:**
   - Should the next PR include only schema + persistence for class-state, or also a minimal deterministic transition rule to validate dynamics?

8. **Backend rollout guardrail:**
   - If binary `y07` and fallback disagree beyond tolerance, should simulation fail fast, log warning and continue, or force fallback for that run?
