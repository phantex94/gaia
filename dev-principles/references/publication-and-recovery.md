# Publication and recovery

Read when writing signals, state, or orders; retrying an ambiguous action; or preparing production recovery. This document owns commit semantics and external-effect reconciliation. Return to the [outline](../SKILL.md).

## Commit one logical result

Use the logical snapshot identity and lineage defined in [configuration and identity](configuration-and-identity.md). Enforce uniqueness using an atomic conditional commit or equivalent sink transaction. A matching retry may short-circuit or atomically point to content-identical artifacts. Conflicting lineage or content under the same key triggers `business refusal`. Numerical tolerance does not authorize replacement. [Test]

Stage immutable output and state together. Publish them through one committed manifest reference so readers never observe a mixed pair. Use rename only when the storage backend guarantees the required atomicity. Never advance committed state in place. [Check / Test]

Keep physical attempt records append-only. Recovery appends a new attempt and staged artifacts without rewriting earlier evidence or completed artifacts. New attempts retain the logical publication key. Ensure row-key uniqueness and prevent repeated rows, aggregate weights, accounting, and downstream publications. [Check / Test]

## Reconcile before resending

After a crash or ambiguous response, inspect the sink's committed status using a stable action or idempotency key. Missing local success evidence does not establish remote failure. A crash after remote acceptance but before local acknowledgement must not publish or advance state twice. [Test]

A broker timeout is not a rejected order. An adapter can guarantee remote idempotency only with supporting service semantics or reconciliation that establishes the action status. Record those limits. Do not claim exactly-once external execution based on a local database transaction alone. Use the declared execution state machine for partial fills, rejections, acknowledgements, and subsequent actions. [Test / Review]

Code rollback does not undo external trades or publications. Rehearse a separate recovery procedure for irreversible effects. [Test / Review]

## Reduce avoidable errors without concealing real failures

Make matching retries a normal operation returning the committed result. Make atomic output/state reads a normal interface guarantee. Keep absent or stale required inputs, unavailable models, conflicting lineage, invalid transitions, infeasible optimization, and nonfinite results explicit failures. Do not silently fill defaults or report a refusal as success. [Test / Review]

Use an independent business-refusal type and exit code. Ordinary programming errors remain ordinary exceptions. Broad handlers must propagate refusal or map it explicitly at the application entry point. Catch exceptions at real I/O, application-entry, or task-supervision boundaries with a declared recovery/reporting policy. Preserve reasons and evidence. [Check / Test]

This applies [defining errors out of existence](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch10.html) to API semantics without weakening quantitative correctness.

## Expose one operational capability

Provide a thin CLI shaped `<tool> <domain> <action>`. Schedulers may call the same application API when justified; they must not duplicate domain logic or bypass guards. Operational business capabilities need CLI workflows, not a command for every internal helper. Keep development-only tools outside the shipped operational package. [Check / Review]

Writing commands default to Dry-run and report the plan, logical publication key, and affected destination. No business writes occur without an explicit write flag. Production writes additionally require explicit production-environment and publishing values; no force option bypasses them. Share reusable option definitions. Document exit codes for success, retryable failure, permanent failure, and business refusal. [Check / Test]

## Prove recovery through public behavior

From the first reusable stateful slice, exercise same-day reruns, concurrent attempts, failure before commit, and failure after sink commit but before local acknowledgement. Check one logical result, one committed state transition, unique rows, unchanged aggregate weights, and the publication count. Test the public capability, not only its helpers. [Test]

Compare full Batch with segmented Batch, daily Step, Backfill, and repeated dates under the [computation contract](computation-and-state.md). [Delivery](delivery-and-verification.md) owns release evidence and alert rehearsals. The [scenario playbook](scenarios.md) describes investigation and recovery decisions.
