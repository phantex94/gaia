# Scenario playbook

Read the scenario that matches the current change, then its linked contract owner. This playbook routes decisions and evidence; it does not redefine the contracts. Return to the [outline](../SKILL.md).

## Add an Alpha or quantitative operator

Read [computation and state](computation-and-state.md), [data and PIT](data-and-pit.md), and [configuration](configuration-and-identity.md). Define mathematics, inputs, axes, units, grouping, missing values, warmup, semantic parameters, sufficient state, and independent expected values.

Reuse the platform's PIT access, identity, recovery, and publication. Demonstrate the caller before adding abstraction. Test nondegenerate cross-sectional samples, future-data perturbation, execution-mode equivalence, and decision-sensitive rounding/ranking. Extra registries or a new platform framework need an actual consumer. [Test / Review]

## Change a provider format or availability rule

Read [data and PIT](data-and-pit.md) and [architecture](architecture.md). Determine whether the change affects transport only, business meaning, or historical availability. Update the provider adapter and owning contract; do not scatter field remapping or `shift` patches through strategies.

Test old/new format boundaries, actual availability timestamps, late publication, and historical universe membership. If meaning changes, version the contract and affected inputs. Explain unavoidable caller migrations. A format change should not ordinarily require rewriting unrelated Alpha logic. [Test / Review]

## Correct old data or invalidate a cache

Read [data and PIT](data-and-pit.md), [computation](computation-and-state.md), and [identity](configuration-and-identity.md). Create an immutable input revision. Compute the affected range from node-specific invalidation, recursive replay, and refit policies, not lookback alone.

Write recomputed results to a new vintage and retain original As-Traded records. Check all cache dependencies, including implementation, schema, model, and predecessor state; changed dependencies require a new cache version. Preserve referenced old inputs and state. [Check / Test]

## Rerun a day, handle concurrency, or recover after a crash

Read [publication and recovery](publication-and-recovery.md). Keep the logical key stable and create a new physical attempt. Start from the same committed predecessor. Inspect sink status before retrying an ambiguous commit.

Exercise concurrent identical attempts, failure before commit, and failure after remote commit but before local acknowledgement. Observe one logical result/state transition, no mixed output/state, unique rows, unchanged aggregate weights, and one downstream publication. Conflict is a refusal, not a tolerated overwrite. [Test]

## Handle an order timeout or partial execution

Read [publication and recovery](publication-and-recovery.md). Use the broker's actual client-action identity and query/reconciliation support. A timeout leaves status uncertain; it does not establish rejection. Reconcile before resending and preserve partial-fill state transitions.

State the adapter's guarantees and limits, including what happens if reconciliation cannot establish status. Code rollback does not reverse a trade. Test the declared refusal or recovery path with a broker fake, then obtain the required integration evidence before claiming production behavior. [Test / Review]

## Optimize or move to different hardware

Read [delivery](delivery-and-verification.md) and [computation](computation-and-state.md). Measure the actual limiting work, including I/O, copies, serialization, and repeated boundary calls. Set numerical and downstream decision tolerances before comparing implementations.

Do not shard cross-sectional operations without valid grouping/reduction. Compare merged results and state against an independent unsharded reference. Record environment and thread settings; require bitwise equality only where the contract demands it. Verify published same-key immutability independently of numeric tolerance. [Test / Review]

## Refactor a boundary or split a module

Read [architecture](architecture.md). Describe the knowledge being moved and show two caller sketches when the boundary is consequential. Compare total caller burden and change locality, not just shorter files.

Preserve behavior or explicitly version changed contracts. Record why tightly coupled pieces belong together or why separation hides useful knowledge. Verify affected CLI/API workflows, PIT/state behavior, public dependencies, and final integrated results. Do not combine unrelated improvements merely because the files are open. [Check / Test / Review]

## Start a project or take research to production

Read [architecture](architecture.md) and [delivery](delivery-and-verification.md). Use a sample large enough to express the actual mathematics. Keep exploration outputs isolated; add reusable contracts and recovery as the capability stabilizes.

Before go-live, rehearse the real output channel in a test environment, stale-input refusal, alerts received by a person, publication/recovery, cutover, and rollback. For a rewrite, record shadow acceptance and old-system retirement. Before dispatching workers or handing off a long task, use [collaboration](agent-collaboration.md) to bound ownership and preserve evidence. [Test / Review]
