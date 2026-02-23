# Deadwood integration plan for Mela2.0

## Purpose

This document reframes the uploaded legacy deadwood material in `dead/` into a concrete implementation plan for this repository.
The goal is to reuse **scientific content** (equations, state concepts, decomposition workflows), while replacing simulator-specific APIs.

---

## 1) Uploaded source material and how to reuse it

| Uploaded file(s) | What it contains | Directly reusable? | Planned reuse in Mela2.0 |
|---|---|---:|---|
| `yasso07.py`, `y07.so`, `y07.pyd` | Yasso07 AWENH pool stepping (cwl/fwl/nwl + climate inputs) | Partial | Build a backend adapter that accepts Mela2.0 deadwood inflows and returns updated AWENH pools + C fluxes. |
| `BiomassmodelLibrary.c/.h` | Biomass equations and component-level structures (Marklund/Repola/Petersson-Ståhl style family) | Concept-level | Implement a configurable biomass conversion module; keep equation set pluggable and testable. |
| `NaturalremovalmodelLibrary.c/.h` | Natural removal/mortality logic in legacy C signatures | Concept-level | Use model logic to define mortality-to-deadwood transfer rules and optional calibration priors. |
| `DistributiondeadtreemodelLibrary.c/.h` | Deadwood state classes by species, diameter class, snag/downed, years since death | Concept-level | Implement optional deadwood class state layer for biodiversity indicators and reporting. |
| `deadwood_diversity_jyu.py` | Deadwood diversity indicator from deadwood volume + class diversity | Yes (formula-level) | Port formula as a standalone indicator operation fed by deadwood class states. |
| `harvest.py` | Legacy harvest operation flow tightly coupled to another simulator | Low | Use only as conceptual reference for residue bookkeeping; do not port code paths. |

---

## 2) Current Mela2.0 hooks we can attach to

1. **Natural mortality signals already exist in growth paths**
   - Metsi growth path: negative stem trajectories and pruning (`stems < 1`) remove dead trees from living list.
   - Motti DLL path: missing returned tree IDs interpreted as dead/removed (`stems -> 0`).
2. **Harvest removals are captured** via `RemovedTrees` collected data.
3. **Biomass outputs are available conceptually** in the operation model set, but no integrated deadwood-pool + decomposition accounting layer is wired yet.

Implication: Mela2.0 already produces the key *events*; we need a deadwood-carbon bookkeeping layer to convert events into pool dynamics.

---

## 3) Target design to implement in this repo

### 3.1 New deadwood package

Create `lukefi/metsi/domain/deadwood/`:

- `types.py`
  - `DeadwoodPools` (AWENH by pool category),
  - `DeadwoodInflows` (mortality, harvest residue, optional disturbance),
  - `DeadwoodFluxes` (decomposition, transfers, net stock change),
  - `DeadwoodClassState` (species × snag/downed × diameter × years-since-death).
- `biomass_conversion.py`
  - Conversion from stand tree states/removals -> dry mass by component.
- `inflow_builder.py`
  - Builds deadwood inputs from growth mortality and `RemovedTrees`.
- `yasso_backend.py`
  - Backend strategy interface and one implementation (`Yasso07Adapter`).
- `class_dynamics.py`
  - Optional class transitions for snag/downed/decay progression.
- `indicators.py`
  - Deadwood diversity indicator (JYU formula port + optional variants).

### 3.2 New simulation operations

- `update_deadwood_pools`
  - Called each time step after growth and harvesting.
  - Collect mortality/residue inputs, convert to carbon pools, run decomposition step, update stand-attached deadwood state.
- `report_deadwood`
  - Exposes deadwood stocks/fluxes for DB export and report operations.
- (Optional) `report_deadwood_diversity`
  - Computes biodiversity indicator from class state.

### 3.3 Data output

Add collected-data classes and DB table(s):

- `deadwood_pools(node, stand, time_point, species_group, pool, a, w, e, n, h, total_c)`
- `deadwood_fluxes(node, stand, time_point, source, input_c, decomposition_c, net_change_c)`
- optional `deadwood_classes(...)` for biodiversity and diagnostics.

---

## 4) Mapping legacy variable conventions to Mela2.0 conventions

### 4.1 Yasso mapping

From legacy `yasso07.py` style:
- `cwl` → coarse woody litter channel
- `fwl` → fine woody litter channel
- `nwl` → non-woody litter channel
- each with AWENH pools and climate driver `(temp, rain, amplitude)`

Proposed Mela2.0 map:
- `coarse_deadwood` inputs -> `cwl`
- `fine_woody_residue` inputs -> `fwl`
- `foliage/fine-litter` inputs -> `nwl`

### 4.2 Species grouping

Initial MVP grouping (to avoid overfitting early):
- `pine`
- `spruce`
- `broadleaf`

Later: optionally expand to finer species mapping if calibration data supports it.

### 4.3 Time-step handling

If simulation uses 5-year growth steps:
- run decomposition with annual sub-steps (`n=5`) for numerical stability,
- aggregate fluxes back to timepoint output.

---

## 5) Phase plan (implementation, not just concept)

## Phase 0 — Contract and scaffolding (1 sprint)

Deliverables:
- Deadwood dataclasses and serialization stubs.
- New operation tags wired but no-op behavior behind feature flag.
- Unit tests confirming no regression when feature disabled.

## Phase 1 — Inflow accounting (1 sprint)

Deliverables:
- Mortality extraction logic from growth outcomes.
- Harvest residue pathway from `RemovedTrees` with configurable residue fractions.
- Mass-balance tests on inflow assembly.

## Phase 2 — Biomass conversion (1 sprint)

Deliverables:
- Configurable converter interface (`equation_set`, `coeff_table`, `species_map`).
- Initial coefficient package (documented assumptions).
- Regression tests for known input-output tuples.

## Phase 3 — Yasso integration (1 sprint)

Deliverables:
- Yasso backend adapter with deterministic stepping API.
- AWENH pool updates and decomposition flux output.
- Climate input adapter (static defaults + external lookup option).

## Phase 4 — Class dynamics + diversity indicator (1 sprint, optional for MVP)

Deliverables:
- Class-state tracker (snag/downed + d-class + years-since-death).
- JYU diversity indicator operation.
- Tests for class transitions and indicator stability.

## Phase 5 — Reporting and controls (1 sprint)

Deliverables:
- DB exports and report helpers.
- Example control profile enabling deadwood workflow.
- README operation docs and parameter reference.

---

## 6) Defaults proposed for first technical implementation

These are defaults to start coding quickly; they can be changed once you confirm:

- Backend: `Yasso07Adapter` with runtime detection (binary backend when available, fallback backend otherwise).
- Species groups: `pine/spruce/broadleaf`.
- Carbon fraction default: one global default at MVP, per-species override supported.
- Inflow policy in MVP: include natural mortality **and** configurable harvest residues.
- Distribution classes: postpone to Phase 4 unless biodiversity output is needed immediately.

---

## 7) Risks and guardrails

- **Binary/backend portability risk** (`y07.so`/`y07.pyd`): isolate via adapter and keep backend-agnostic operation contracts.
- **Double counting risk** (mortality + harvest + biomass report overlap): add source-tagged inflow ledger and test mass balance each step.
- **Step-size mismatch risk** (5-year growth vs annual decomposition): enforce explicit sub-stepping and test invariance.
- **Equation uncertainty risk**: version equation sets and log coefficient source in outputs.

---

## 8) Immediate next tasks for the next coding PR

1. Add `lukefi/metsi/domain/deadwood/types.py` and `inflow_builder.py`.
2. Add `update_deadwood_pools` operation skeleton with feature flag.
3. Add unit tests:
   - inflow mass balance,
   - zero-input no-change behavior,
   - deterministic one-step decomposition contract.
4. Add one example control configuration using deadwood operation.
5. Add README section for deadwood configuration parameters.

---

## 9) Questions that must be confirmed before Phase 2/3 coding

1. Which biomass equation set should be default in this repo (Repola vs Marklund vs mixed policy)?
2. Do you want harvest residues included in MVP or postponed after natural-mortality-only baseline?
3. Is binary Yasso backend acceptable in deployment, or must MVP be pure Python?
4. What output granularity is required first: stand total only, or species-group and pool-wise output?
5. Do you need biodiversity indicator in MVP, or can it wait for Phase 4?

