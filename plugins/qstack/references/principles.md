# Quant Principles (Shorthand Reference Library)

Do not invoke this file directly as a command. Cite these named principles explicitly when challenging flaws, comparing sketches, making trade-offs, or reviewing code.

1. **`Read-Before-Asking`** — Inspect existing code (`README.md`, `api.py`, sibling modules) and any human-provided `reference_architecture`, `reference_data`, `reader_code`, or `reference_code` first. Never ask the human for facts already present in those artifacts.
2. **`Return-The-YAML`** — After reading references and checking for gaps, always return the assembled semi-structured Intent YAML to the human for review and sign-off before writing business code.
3. **`Challenge-Flaws-Early`** — Push back immediately with concrete evidence and alternatives whenever a proposal fails I/O closure, scaling math, priority ordering, PIT visibility, or layering rules.
4. **`Pin-The-Ends`** — Data structure is Invariant #0. Lock at least the top-level input and bottom-level output (or upstream/downstream boundary in Brownfield) before coding; avoid untyped raw dicts across domain boundaries.
5. **`Backbone-Then-Mock-Then-Real`** — For Greenfield (A) and boundary evolutions (D), deliver a data-free Backbone (Layout + acyclic dependency DAG + CLI/YAML shell) for human review first, then validate on non-degenerate synthetic data, and only then connect real data.
6. **`Zero-Lookahead`** — Every decision at cutoff `t` uses only data, universe membership, contract specs, and models with `available_time <= t`. Apply availability lag once at the data/asset boundary; never scatter `shift()` in downstream nodes.
7. **`Batch-Equals-Step`** — Separate business output from sufficient state: `(inputs_t, state_{t-1}, params) -> (outputs_t, state_t)`. Full Batch, segmented Backfill, and daily Step must agree at the same decision time; retries start from read-only committed `state_{t-1}`.
8. **`Numbers-Are-Not-Decisions`** — Floating-point closeness does not guarantee identical rankings, thresholds, constraints, lot rounding, or orders. Verify numeric tolerances and discrete decision consequences separately.
9. **`Math-First-Readability`** — Core quantitative math (factors, models, objectives, accounting) must read linearly like equations with explicit `shape / axis / unit / NaN` annotations. Never fragment cohesive math into single-use helpers to satisfy a line-count rule.
10. **`Reference-First-Optimize-Second`** — Write a clear, auditable Reference implementation first. Profile at target scale before optimizing. If budgets hold, stop. Any optimization that degrades readability requires explicit human approval of the speedup-vs-readability trade-off and must pass dual equivalence against Reference.
11. **`Fail-Closed-Refusal`** — Missing required inputs, stale data, missing specs, infeasible optimization, and same-key lineage conflicts raise a dedicated `Refusal` (never swallowed by `except Exception`). Preserve `NaN / null`; never silently fill zero or sentinels.
12. **`Minimal-Harness-Cost`** — Count decomposition, handoff, merge, and verification overhead. Default to Direct execution; use `subagent` for isolated heavy reads, `dynamic workflow` for deterministic fan-out/pipelines, `swarm` only after shared interfaces are frozen, and bounded `goal` only for machine-verifiable long loops.

Style preferences (recommended, not mandatory; repo rules win): `style-preferences.md`.
