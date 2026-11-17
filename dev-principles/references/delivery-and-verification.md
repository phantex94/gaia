# Delivery, verification, and performance

Read when starting a project, creating a reusable component, expanding scale, benchmarking, or preparing go-live. This document owns delivery gates and evidence. Return to the [outline](../SKILL.md).

## Match the gate to the work

PIT, explicit semantics, strict inputs, missing-value rules, split isolation, and versions apply even to exploration. Do not require a full deployment framework before testing an isolated hypothesis. [Check / Review]

| Stage | Required evidence before advancing |
|---|---|
| Exploration | Read-only versioned PIT inputs, code/configuration records, declared splits, basic independent reference; outputs isolated from production |
| Reusable component | Public boundary and state contracts, causal and idempotency tests, reproducible entry point, target-scale budgets |
| Production | Accepted foundation plus publication, recovery, monitoring, operational ownership, and cutover evidence |

## Establish the first reusable capability

Prepare the following foundation without speculative empty packages:

- A human-approved Phase 0 contract for the first capability: layers, boundaries, conventions, layout, and staged delivery. Link it from repository instructions. [Review]
- An allowed-import table covering shipped code, deployment, and operations tools. No forbidden imports, cycles, or unreviewed exemptions. Actual packages have public interfaces and responsibility documentation. [Check / Review]
- Two caller-oriented sketches for consequential boundaries, following [architecture](architecture.md). Record ownership, explicit policies, and the chosen rationale. [Review]
- Boundary contracts for inputs and outputs, including owner and freshness. One implementation point per unit, rounding, calendar, price, and availability convention. Accepting and refusing cases cover each correctness rule. [Test]
- Immutable parameters and a strict loader, a CLI with help and documented exit codes, default Dry-run, and propagated business refusal. Follow [configuration](configuration-and-identity.md) and [publication](publication-and-recovery.md). [Check / Test]
- Test layout, pre-push selection, CI, a seeded nondegenerate reference dataset, and automated mechanical style/boundary checks. Record checker limitations. [Check / Test]

## Expand a meaningful end-to-end slice

| Rung | Scope | Exit evidence |
|---|---|---|
| 1 | Smallest meaningful synthetic sample through every stage | Independent reference, PIT, state, and basic idempotency agree |
| 2 | Small real sample, real output write in a test environment | Independent reference, cutover, rollback, and recovery rehearsals pass |
| 3 | Full universe | Coupling semantics and time/state/working-memory budgets hold |
| 4 | Full history | Batch, Backfill, and Step meet the equivalence contract; budgets hold |
| 5 | Production | Go-live evidence complete; rewrite shadow period accepted |

The first sample must express cross-sectional grouping, warmup, and state transitions where relevant. Include multiple industries, suspended instruments, missing observations, and calendar gaps for cross-sectional projects. Empty, single-row, and single-instrument inputs remain boundary tests, not the sole MVP. Record out-of-scope items. Preserve compatible contracts or explicitly version and migrate changes; do not freeze a mistaken design. [Test / Review]

At reusable delivery, inspect caller burden as well as tests. Demonstrate new-Alpha reuse and provider-change locality. Check duplicated knowledge, pass-through layers, and hidden ordering. Consolidate tightly coupled mechanisms when it reduces total complexity. Do not substitute function or line counts for this review. [Review]

## Verify independent behavior

Expected results come from hand calculations, known formulas, an independent implementation, or a previous system pinned to a revision. Never generate expectations from the code under test or reuse disputed alignment logic. Use small, read-only real fixtures with provenance and fakes for external systems. [Test / Review]

Seeded synthetic data covers lifecycle events, late/revised data, calendar gaps, and state recovery. Expected-value changes require a written reason and new fixture version. Require future-input perturbation and the recovery cases in [publication](publication-and-recovery.md). Permit bounded malformed-input or crash fault injection. Do not use code mutation testing or multi-round adversarial review loops. [Test / Review]

Keep the fast suite within a declared budget and run it before every push. Run acceptance against the final integrated revision at production-representative scale; record commands, environment, and results. Worker-branch checks alone do not prove integrated correctness. Distinguish executed checks from requirements only specified for future implementation. [Check / Test]

## Measure computation and data movement

Before accepting an optimization, prove its numerical and decision behavior under [computation](computation-and-state.md). Separately budget wall time, persistent state, peak temporary memory, and communication at target scale. Benchmark in a named environment and fail declared regression thresholds. [Test]

Bound chunks, accelerator batches, worker pools, and caches. State memory growth in lookback, active universe, dimensions, and state size. Stream working sets independently of total history; explicitly budget full-history fitting. Test beyond expected data scale where relevant. Do not claim exact rolling state is independent of window or universe size. [Check / Test]

Use lazy columnar reads, pushed-down date/column filters, and partitioning matched to dominant read keys. Reuse validated immutable revisions. Avoid repeated historical scans and dataset hashing. Profile measured hot paths, vectorize or compile where useful, and inspect copies, reshapes, serialization, and repeated calls across interfaces. Measure before changing hardware. [Test / Review]

Cross-sectional sharding needs valid grouping, reduction, ordering, and unsharded-reference comparison. Improve interfaces that force wasteful reads or copies rather than optimizing only kernels. See [performance design](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch20.html).

## Complete go-live evidence

Pin the release's exact revision and tag; exclude development-only tools. Define production/research roots, secret location, and artifact retention. Reject production inputs outside approved roots. [Check]

Rehearse actual output-channel writes in a test environment, atomic publication/recovery, stale-input refusal, source failure behavior, cutover, and rollback. A recipient must confirm receiving an alert; generating a local log is insufficient. Record operational owners and separate recovery for irreversible effects. Rewrites require written cutover criteria, a shadow period, and an old-system retirement plan. [Test / Review]

Work is complete after acceptance, not after scheduling or dispatch. Follow [collaboration](agent-collaboration.md) for task evidence and [scenarios](scenarios.md) for change-specific routes.
