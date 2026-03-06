# Plan: Integrate growth-model natural mortality into deadwood pools

## Objective

Create a robust, testable, and model-agnostic workflow where natural mortality produced by growth models is consistently routed into deadwood carbon pools (CWL/FWL/NWL), decomposed via backend stepping, and reported with clear source attribution.

## Current baseline in this repository

The project already has the essential hooks:

1. `grow_metsi` captures negative stem deltas (`fdelta < 0`) and stores a mortality snapshot on the stand as `deadwood_growth_mortality_trees` before pruning dead trees from the living list.
2. `update_deadwood_pools` consumes `deadwood_growth_mortality_trees` (when available) via `build_deadwood_inflows`, then clears the transient field.
3. The deadwood operation tracks mortality/harvest/disturbance source pools separately and aggregates them into stand-level flux outputs.

This plan focuses on hardening those hooks into a complete integration contract across all growth pathways and edge cases.

---

## Scope

### In scope
- Natural mortality transfer from growth models to deadwood inflow channels.
- Consistent event ordering and lifecycle of transient mortality data on `ForestStand`.
- Mass-balance verification for mortality inflow and pool updates.
- Reporting/diagnostics so mortality-derived deadwood can be audited.

### Out of scope (for this work package)
- New biodiversity metrics.
- New decomposition science model development.
- Major redesign of harvest residue logic.

---

## Integration architecture (target)

1. **Growth step emits mortality payload**
   - Each growth model writes mortality trees to `stand.deadwood_growth_mortality_trees` using a common schema (`ReferenceTrees` semantics with stems representing dead stems/ha for the step).

2. **Deadwood step ingests and clears payload**
   - `update_deadwood_pools` always resolves mortality payload first.
   - If payload is missing, it can fall back to tree-list differencing for backward compatibility.
   - After read, payload is cleared to avoid double counting.

3. **Inflow builder converts payload to carbon channels**
   - Mortality biomass -> carbon conversion.
   - Channelization into CWL/FWL/NWL via configured component fractions.

4. **Backend step updates source pools and aggregate pool**
   - Mortality source pool stepped independently, then recombined with other sources for totals.

5. **Collected data reports source and aggregate fluxes**
   - Mortality contribution visible in per-step outputs.

---

## Phase plan

## Phase 1 — Define and freeze the mortality handoff contract

**Deliverables**
- Short developer spec in code comments/docstrings for `deadwood_growth_mortality_trees`:
  - units,
  - expected fields,
  - lifecycle (set by growth, consumed once by deadwood).
- Align all growth operations (`grow_metsi`, `grow_motti`, others) to emit this field when they can produce explicit mortality.

**Acceptance criteria**
- Every supported growth operation either:
  - emits `deadwood_growth_mortality_trees`, or
  - explicitly documents fallback behavior.

## Phase 2 — Strengthen inflow assembly and fallback rules

**Deliverables**
- Deterministic precedence in inflow builder:
  1. explicit growth mortality payload,
  2. tree-list differencing fallback.
- Structured diagnostics counters (e.g., `used_explicit_mortality`, `used_fallback_diff`).

**Acceptance criteria**
- No path can apply both explicit and fallback mortality in one step.
- Re-running deadwood operation without a new growth step produces zero repeated mortality inflow.

## Phase 3 — Mass-balance and non-regression tests

**Deliverables**
- Unit tests:
  - explicit mortality payload -> expected channel inflows,
  - fallback differencing path,
  - no double counting when payload consumed,
  - pruning edge case (`stems < 1`) does not lose mortality carbon.
- Integration test over a multi-step stand simulation with growth + deadwood enabled.

**Acceptance criteria**
- Mortality inflow carbon equals converted dead-tree carbon within tolerance.
- Deadwood pool delta equals inflow minus decomposition for each step/source.

## Phase 4 — Reporting and traceability

**Deliverables**
- Extend collected data payload (or log metadata) with mortality provenance fields:
  - source path used (`explicit`/`fallback`),
  - mortality inflow per channel.
- Add an example control scenario showcasing natural mortality to deadwood transfer.

**Acceptance criteria**
- Analysts can audit a timestep and see exactly how much mortality entered deadwood and by which route.

## Phase 5 — Operational safeguards

**Deliverables**
- Runtime guards for malformed payloads (NaN/negative anomalies after preprocessing).
- Optional strict mode to fail fast in development when payload contract is violated.

**Acceptance criteria**
- Invalid mortality payloads are either sanitized with warnings or rejected (strict mode), with deterministic behavior.

---

## Recommended sequencing in simulation event trees

For each timestep:
1. growth operation (`grow_*`) runs,
2. harvest/removal operations run,
3. `update_deadwood_pools` runs,
4. reporting/export operations run.

This ensures mortality is captured before living-tree pruning side effects can obscure source signals.

---

## Risks and mitigations

- **Risk: double counting mortality** if both explicit payload and fallback differencing are applied.
  - **Mitigation:** strict precedence + one-time payload clearing + dedicated tests.

- **Risk: missed mortality for growth models without explicit payload support.**
  - **Mitigation:** maintain fallback differencing until all growth models implement explicit handoff.

- **Risk: silent contract drift across teams.**
  - **Mitigation:** codify contract near operation code and validate in CI tests.

---

## Definition of done

This integration is complete when:
- all targeted growth models provide explicit mortality payloads or documented fallback;
- deadwood inflow routing is deterministic and non-duplicative;
- mass-balance tests pass;
- per-step outputs clearly expose mortality contribution into deadwood pools.
