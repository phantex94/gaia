# Attention scheduler MVP (pure JavaScript, Node >=18 CLI)

This directory is a host-independent advisory policy, not a task scheduler, approval engine, native event listener, or authentication service. It never calls the board or modifies files. The existing Coordinator collects trustworthy observations, uses the helper or manual equivalent, and retains all native gate obligations. Keep Fast Path unscored.

## Run

```bash
node test_attention.mjs
node cli.mjs schedule example.json
node cli.mjs validate answer.json
# use - for stdin instead of a file
```

`schedule` receives a snapshot with `requests` (see [template](../../../templates/decision-request.yaml)), `now_min` (same origin as created/deadline), explicit `batch_limit` (1–4), `max_wait_min`, `delay_weight` (cost units per minute) and `intakes` mapping draft ID to batches_used, questions_used, confirmation_ready and confirmation_used. These are explicit policy inputs, not production defaults. `selected` contains advisory groups with original members; `remaining`, `blocked`, `deferred`, and `intake_questions` preserve outstanding items/estimated batch charges. Nothing is spent until actually asked. Unknown mandatory costs are allowed and surfaced; optional unknown/nonpositive costs are deferred. Verified equal share metadata, question, choices, owner and semantic kind are necessary for grouping; no fuzzy merge, no authority reuse. Conflicts stay blocked. Aging is heuristic, not guaranteed service under unlimited urgent load. The coordinator must independently check urgency/critical path and avoid delay while filling a batch.

`validate` receives `{presented,live,reply}`, where presented/live are full request objects and reply contains source=human, explicit=true, owner, id, version, choice, receipt_id, delivered_receipts (known per-target receipt IDs). For a shared request validate every member separately, after binding the human's actual explicit answer to all target IDs. This is a structural check on caller-supplied assertions, **not authentication, approval, transactional compare-and-act, durable deduplication or proof of delivery**. The Coordinator must re-read the real host object, check prerequisites, authority, actual human reply, receipt/delivery and native wait type; it must refuse or use direct human UI if they cannot be established. Never use a route string as authority. Gate 1 is record-only here, not runnable dispatch. Plan/merge native manual approval, permission/auth/pick/failure manual-only, ordinary questions only candidate tell. For unverified, stale or already delivered requests no action is proposed. No automatic replay. Fast blockers may be shown but are never scored or interviewed.

## Executed offline evaluation

The 37 assertions and the 12 synthetic scenarios × 4 strategies (48 deterministic replays) were executed in a V8 isolate using the same pure JS function bodies that generate the source/test files. [Full machine-readable results](evaluation.json) preserve test names and all scenario rows. Node CLI filesystem/argv integration and live Herdr/Claude/Codex execution were not run in that isolate.

All scenarios have answerable mandatory requests; each batch costs 2 minutes overhead + 1 minute per question. Fixed batches occur at 10-minute ticks; Priority and Adaptive are event-driven; Priority disables sharing. Human offline intervals are synthetic and the same within each scenario. Independent remaining tails approximate project completion as max(answer time + tail). Total completion times sum per-scenario makespans, not wall time for a single project. This is not a full resource-constrained DAG simulator, real LLM benchmark, or calibrated labor estimate.

| Policy | Batches | Questions | Human min | Sum decision wait min | Sum project finish min | Requests answered |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Immediate | 41 | 41 | 123 | 560 | 1108 | 41 |
| Fixed | 20 | 41 | 81 | 622 | 1130 | 41 |
| Priority | 21 | 41 | 83 | 490 | 1066 | 41 |
| Adaptive | 20 | 36 | 76 | 470 | 1063 | 41 |

The result demonstrates only behavior under chosen synthetic assumptions: deduplication and batch overhead can lower communication; priority can reduce delay; relative benefit versus fixed/priority is smaller than versus immediate. It does not estimate actual improvement in user time. Security regression assertions include unverified/conflicting sharing, separate permissions and approvals, exhausted intake, Fast unscored, wrong machine/target, changed revision/wait/options, vague or non-human reply, stale/duplicate receipt and native action separation. A later independent natural-language and live host test is required. No real approvals or external side effects were exercised.
