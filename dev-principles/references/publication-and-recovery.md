# Publication and recovery

Read when writing signals, state, or orders; retrying an ambiguous action; or preparing production recovery. This document owns commit semantics and external-effect reconciliation. Return to the [outline](../SKILL.md).

## Commit one logical result

Use the logical snapshot identity and lineage defined in [configuration and identity](configuration-and-identity.md). Enforce uniqueness using an atomic conditional commit or equivalent sink transaction. A matching retry may short-circuit or atomically point to content-identical artifacts. Conflicting lineage or content under the same key triggers `business refusal`. Numerical tolerance does not authorize replacement. [Test]

Stage immutable output and state together. Publish them through one committed manifest reference so readers never observe a mixed pair. Use rename only when the storage backend guarantees the required atomicity. Never advance committed state in place. [Check / Test]

Keep physical attempt records append-only. Recovery appends a new attempt and staged artifacts without rewriting earlier evidence or completed artifacts. New attempts retain the logical publication key: a readable tuple of business fields, such as `(strategy, trading_day, round)`, never a hash. Ensure row-key uniqueness and prevent repeated rows, aggregate weights, accounting, and downstream publications. [Check / Test]

## Reconcile before resending

After a crash or ambiguous response, inspect the sink's committed status using the readable logical publication key or the sink's own client-action identity. Missing local success evidence does not establish remote failure. A crash after remote acceptance but before local acknowledgement must not publish or advance state twice. [Test]

A broker timeout is not a rejected order. An adapter can guarantee remote idempotency only with supporting service semantics or reconciliation that establishes the action status. Record those limits. Do not claim exactly-once external execution based on a local database transaction alone. Use the declared execution state machine for partial fills, rejections, acknowledgements, and subsequent actions. [Test / Review]

Code rollback does not undo external trades or publications. Rehearse a separate recovery procedure for irreversible effects. [Test / Review]

## Reduce avoidable errors without concealing real failures

Make matching retries a normal operation returning the committed result. Make atomic output/state reads a normal interface guarantee. Keep absent required inputs, stale inputs beyond a declared degradation bound (see [data and PIT](data-and-pit.md)), unavailable models, conflicting lineage, invalid transitions, infeasible optimization, and nonfinite results explicit failures. Do not silently fill defaults or report a refusal as success. [Test / Review]

Use an independent business-refusal type and exit code. Ordinary programming errors remain ordinary exceptions. Broad handlers must propagate refusal or map it explicitly at the application entry point. Catch exceptions at real I/O, application-entry, or task-supervision boundaries with a declared recovery/reporting policy. Preserve reasons and evidence. [Check / Test]

Declare one exit-code table per project and test every row through the real entry point. Each code has exactly one meaning; the project chooses the numbers within these constraints: [Check / Test]

| Outcome | Constraint |
|---|---|
| Success | `0`, and only when the business state is the intended one |
| Ordinary failure | A non-zero code that is neither refusal nor usage error |
| Usage error | `2`, reserved for the CLI framework's own argument errors; never reused |
| Business refusal | A dedicated code distinct from `2` and from every other row |
| Retryable or waiting states | Each its own code when callers act on them; two states never share one code |

A parent process, scheduler, or watchdog reads a child's business state, not merely whether it ran. A child exits `0` only when its business outcome succeeded; a failed round reports failure even when the process itself ended cleanly. One failed round is reported and alerted on its own: it must not silently block later rounds, and later rounds must not hide it. [Test]

This applies [defining errors out of existence](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch10.html) to API semantics without weakening quantitative correctness.

## Expose one operational capability

Provide a thin CLI shaped `<tool> <domain> <action>`. Schedulers may call the same application API when justified; they must not duplicate domain logic or bypass guards. Operational business capabilities need CLI workflows, not a command for every internal helper. Keep development-only tools outside the shipped operational package. [Check / Review]

Writing commands default to Dry-run and report the plan, logical publication key, and affected destination. No business writes occur without an explicit write flag. Production writes additionally require explicit production-environment and publishing values; no force option bypasses them. Share reusable option definitions. Document the exit codes in the table above. [Check / Test]

## Prove recovery through public behavior

From the first reusable stateful slice, exercise same-day reruns, concurrent attempts, failure before commit, and failure after sink commit but before local acknowledgement. Check one logical result, one committed state transition, unique rows, unchanged aggregate weights, and the publication count. Test the public capability, not only its helpers. [Test]

Compare full Batch with segmented Batch, daily Step, Backfill, and repeated dates under the [computation contract](computation-and-state.md). [Delivery](delivery-and-verification.md) owns release evidence and alert rehearsals. The [scenario playbook](scenarios.md) describes investigation and recovery decisions.
