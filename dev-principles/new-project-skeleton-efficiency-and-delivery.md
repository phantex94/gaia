# Starting a new project: skeleton, efficiency, and incremental delivery

Use this guideline when starting a new project or a rewrite. It complements `quant-development-and-agent-collaboration.md` (called "the principles" below), which owns domain invariants, dependency design, reproducibility, project memory, and agent responsibilities. This document specifies artifacts, budgets, and delivery gates.

Prevent three failure modes: accumulating features without contracts, stopping before the real output channel, and adding operations after go-live. Use `schemas/` for contracts, `core/` for domain computation and composition, `cli/` for commands, and `adapters/` for external effects.

Read enforcement labels as follows: **Check** means an automated structural or policy check; **Test** means an executable behavioral or performance test; **Review** means inspection of meaning, scope, or evidence.

## 1. Day-zero artifacts

### Match the gate to the work

Keep PIT, strict inputs, explicit parameters, missing-value semantics, and declared evaluation splits in every stage. Apply the foundation checklist to the first reusable slice; do not require a deployment framework before exploring an isolated hypothesis. [Check / Review]

| Stage | Required before advancing | Enforced by |
|---|---|---|
| Exploration | Read-only versioned PIT inputs, code and effective configuration records, declared splits, and a basic independent reference; keep experimental outputs separate from production | Check / Test |
| Reusable component | Boundary and state contracts, causal and idempotency tests, reproducible entry points, and target-scale budgets | Check / Test |
| Production | Complete the foundation and go-live checklists, including publication, recovery, monitoring, and operational ownership | Check / Test / Review |

### Before the first reusable domain slice

| Artifact | Done when | Enforced by |
|---|---|---|
| Human-approved phase-zero contract covering layers, the first slice's boundaries, conventions, layout, and delivery ladder (§8) | Approved and linked from repository instructions | Review |
| Allowed import table covering shipped code, deployment, and operations tooling | No forbidden imports or cycles; no unreviewed exemptions | Check |
| Explicit public interfaces and responsibility documentation for actual packages | Inputs, outputs, and failure reasons are documented; no empty speculative packages | Check / Review |
| Interface sketches for consequential boundaries (principles §2, §8) | Compare two alternatives with caller examples; record knowledge ownership, explicit policies, and the chosen rationale | Review |
| A business-refusal type and its own exit code; ordinary exceptions for programming errors | Broad handlers propagate refusal or map it explicitly; none convert it to success | Test |
| Boundary contracts for the slice's inputs and output, including input owner and freshness | Each rule has an accepting and a refusing case | Test |
| One implementation point for each convention, including units, rounding, calendars, price basis, and availability marking | Guards reject invalid inputs and repeated normalization | Test |
| Immutable parameter definitions and a strict loader (§4) | Missing fields, unknown fields, and wrong types are refused | Test |
| CLI skeleton, documented exit codes, and default Dry-run behavior (§5) | Help runs; a command without an explicit write flag has no business write | Test |
| Test layout, pre-push selection, CI, and a seeded nondegenerate reference dataset | Relevant checks pass and their scope is recorded | Check / Test |
| Mechanically enforceable style and boundary rules | Checkers report no violations | Check |

### Before go-live

| Artifact | Done when | Enforced by |
|---|---|---|
| Environment layout, secret location, and run-retention rules | Production inputs resolve within approved production roots; the release pins a tag and exact code revision and excludes development tools | Check |
| Thin slice writing to the real output channel in a test environment; build, cutover, and rollback scripts | Cutover and rollback rehearsals pass; irreversible external effects have a separate recovery procedure | Test / Review |
| Input freshness, failure behavior, alerts, and operational owners | Stale required inputs block publication; retries, gaps, and refusal are exercised; a recipient confirms alerts | Test / Review |
| Atomic publication and recovery protocol (§5–6) | Duplicate, concurrent, and interrupted attempts cannot duplicate outputs or publications | Test |
| Rewrite cutover criteria, shadow-run period, and old-system retirement plan | Criteria are met and recorded | Review |

## 2. Data flow

- **Declare each node.** Record inputs, outputs, computation kind (incremental, recursive, or full history), lookback, sufficient state, and coupling axes (`per-instrument` or `cross-sectional`, with grouping keys). Derive execution order from the computational DAG. Keep execution feedback in the state machine defined by principles §2. [Check / Review]
- **Mark availability once.** Keep each dataset's availability rule in `schemas/`; apply it through one canonical function and attach a marker. Refuse repeated marking or lag application. Distinguish that normalization from repeatable as-of queries at different decision cutoffs; never treat a marker as proof that all rows are visible at every cutoff. [Check / Test]
- **Version revisions.** Add a new immutable revision for new or corrected data. Compaction creates a new version; keep referenced old versions readable. Declare each node's revision-impact and recomputation rule, including propagation through recursive state and model refits; lookback alone is insufficient. [Check / Test]
- **Separate outputs and state.** Define stateful computation as `(inputs_t, state_{t-1}, params) -> (outputs_t, state_t)`; for an Alpha node, the output is `alpha_t`. Preserve sufficient state, such as counts, moments, Gram matrices, or window buffers, rather than only the previous business output. Batch, Backfill, and Step share mathematical and state contracts, not necessarily one function implementation. [Test / Review]
- **Anchor recovery.** Load the committed `state_{t-1}` snapshot read-only, pinned to its declared lineage. Rerunning time `t` must use that same predecessor, never an already advanced `state_t`. Stage output and state together and expose them through one atomic manifest commit (§6); never advance state in place. [Check / Test]
- **Key randomness.** Derive reproducible random streams from `(seed, node_id, decision_time)` using a declared stable derivation; add stable instrument or purpose subkeys when needed. Do not use a sequential global RNG, process-dependent hashing, worker order, or chunk boundaries to choose draws. These are control keys, not hashes of dataset contents. [Check / Test]
- **Keep As-Traded immutable.** Reproduce historical published signals from the original decision cutoff, input revisions, code, configuration, model, and predecessor state. Write late-data or correction results to a new `vintage`; never overwrite the historical As-Traded ledger. [Check / Test]
- **Compose through declared interfaces.** Pass outputs through explicit public dependencies or the composition layer. Reject cycles, private-interface imports, and undeclared data reads; a shared adapter does not authorize a higher-level node to bypass its declared inputs. [Check / Test]

## 3. Layers and composition

- Keep business arithmetic out of drivers and runners; move it to the owning domain module. [Check / Review]
- Strictly parse and normalize external data and configuration once at the boundary. Do not repeat defensive type parsing inside or introduce silent defaults. Still check invariants that can fail during computation, such as nonfinite results, infeasible solutions, or invalid state transitions. [Check / Test]
- Use one field vocabulary across modules. Represent missing values as missing, never as zero or a sentinel. [Check / Test]
- Introduce abstractions for demonstrated variation or a meaningful external boundary. Prefer narrow interfaces; add a registry only when actual consumers need discovery or selection. Do not require two implementations before defining a necessary interface. [Review]

- Assign shared knowledge to one owner. Do not split a dataset's format, visibility, or revision rules among packages merely because reading, filtering, and replay happen at different times. Keep the computational DAG, module map, execution state machine, and agent task DAG separate. [Review]
- For PIT access and publication/recovery, sketch a representative caller first. Keep storage mechanics, visibility enforcement, duplicate handling, and reconciliation inside the responsible capability. Keep cutoff, revision policy, authorization, and conflict semantics explicit. Do not remove CLI or adapter boundaries merely because they are thin; they translate between genuine abstractions. [Review]

## 4. Parameter template

- Place one immutable parameter class next to each algorithm. Explain every field's unit and meaning. [Check / Review]
- Give semantic parameters no defaults. Engineering parameters such as chunk size or worker count may have defaults; record their effective values when they affect numerical results. [Check / Test]
- Maintain one complete configuration template per purpose. Validate it against parameter classes, check cross-section consistency, and use explicit environment overlays rather than copied files. [Check / Test]
- Order function arguments as business inputs, the parameter object, then keyword-only runtime switches. Do not pass through `**kwargs`; return named immutable records for multiple results. [Check]
- Permit a `config_digest` of canonical effective parameters and configuration. Declare serialization, field order, numeric representation, and hash algorithm; verify that equivalent configurations produce the same digest and changed values change the identity. Dataset references may be explicit revision IDs; never embed dataset contents for indirect hashing. Apply the dataset prohibition in §6. [Check / Test]
- Require explicit production environment and publishing values for production writes. Do not provide a force flag that bypasses these guards. [Check / Test]

- Every new option must express a real business choice or a justified operational control. Keep storage and recovery mechanics inside their modules instead of exporting a collection of switches to callers. Preserve explicit semantic parameters; simplify the mechanism without silently choosing research policy. [Review]

## 5. Command-line interface

- Provide one operational entry point shaped `<tool> <domain> <action>`. Keep it thin. A scheduler may call the same application API when needed; do not duplicate domain logic or bypass publication guards. [Check / Review]
- Define shared options once and reuse their types across domains. [Check]
- Make writing commands default to Dry-run: show the plan and perform no business writes without an explicit write flag. Report the logical publication key and affected destination. [Test]
- Create append-only run records with readable names (§6). Resume an interrupted run by appending a new attempt record and new staged artifacts; never rewrite earlier evidence or completed artifacts. A new attempt is not a new logical publication. [Check / Test]
- Separate success, retryable failure, permanent failure, and `business refusal` in the documented exit-code table. Propagate refusal to the application entry point and map it to its own code; never report it as success. [Test]
- Require a publication idempotency key at the sink. After a crash or ambiguous response, reconcile the sink's committed status before retrying; do not infer failure from a missing local success record. Refuse unauthorized replacement and conflicting same-key publication. [Test]
- Keep development-only tools outside the shipped package and operational CLI. [Check]

## 6. Identity and run records

- Use human-readable names, dates, sequence numbers, revision IDs, and parameter-set names for runs and artifacts. Do not use bare-hash directory names. Distinguish the physical attempt ID from the logical publication key. [Check]
- Identify one logical output snapshot by `(node_id, decision_time, vintage, config_digest)`. Pin the node implementation, schema, input revisions, model, and initial state in its lineage; version the identity explicitly when that lineage changes. Within each snapshot, enforce the declared row key, including instrument identity for a panel, so retries cannot add duplicate rows or double weights. [Check / Test]
- Enforce uniqueness with an atomic conditional commit or equivalent sink transaction. An identical rerun may short-circuit or atomically point to a content-identical artifact. Publish output and state through one committed manifest reference; readers must never observe a mixed pair. Refuse conflicting lineage or content under the same key with `business refusal`; numerical tolerance does not authorize replacement of a committed result. [Test]
- Store effective configuration and its permitted digest, exact code revision and tag when present, schema and implementation versions, dataset and partition revisions, model and predecessor-state IDs, numerical environment, and attempt logs in the run record. Make the record sufficient to select the original inputs and state. [Check]
- **Do not hash datasets.** Prohibit content hashes, checksums, row hashes, and partition fingerprints for raw or derived datasets, including market data, financial data, features, and Alpha outputs. Identify data and state snapshots through explicit immutable revision IDs, partition manifests, schemas, and source/predecessor references. Do not disguise data as configuration to hash it. This rule does not prohibit Git's code revision identifiers. [Check / Review]
- Validate data using contracts, row-key uniqueness, row counts, time coverage, lineage, and targeted content comparisons in acceptance tests. These checks do not establish cryptographic content integrity. Do not require full-history byte comparisons or repeated complete rereads on each run. [Check / Test]
- Reuse a cache only when input revisions, node implementation, schema, effective configuration, model, and initial state identity all match. Changing any dependency creates a new cache version; never refresh a published version in place. A parameter-set name alone is not a cache key. [Check / Test]

- Exercise the publication capability through its public contract, not only its internal helpers. Matching retries return the committed result; conflicting lineage refuses; readers never receive mixed output/state. For broker or other remote actions, test ambiguous responses against the actual adapter contract and reconcile before resending. A local transaction cannot promise exactly-once remote execution without supporting service semantics. [Test / Review]

## 7. Efficiency and memory

Prove each optimization against the declared numerical and decision contract before accepting its performance gain. [Test]

1. **Declare budgets.** Record target-scale wall time, persistent state size, peak temporary memory, and relevant communication cost separately. Benchmark on a named environment and fail declared regression thresholds. [Check / Test]
2. **Classify historical cost.** For incremental nodes, read only declared new data, tail windows, and sufficient state; do not rescan growing history. For full-history training or refits, declare scan complexity, frequency, and budget instead of promising constant cost. [Test / Review]
3. **Bound working sets.** Set byte or count limits for chunks, accelerator batches, worker pools, and caches. Express memory growth in lookback, active universe, feature dimensions, and state size. Keep streamed working memory independent of total history; explicitly budget full-history stages. Do not claim that exact rolling state is independent of window or universe size. [Check / Test]
4. **Read only what is needed.** Scan columnar storage lazily and push date and column filters down. [Check / Test]
5. **Match storage to readers.** Declare dominant read keys and partition accordingly. Stage immutable writes, then atomically commit their manifest reference; use rename only where the storage backend guarantees the required atomicity. [Test / Review]
6. **Profile before optimizing.** Vectorize or compile measured hot paths. Choose precision per array and measure hidden copies and reshapes. [Test / Review]
7. **Respect coupling.** Do not blindly split cross-sectional operators along the instrument axis. Declare valid groups and any cross-shard reduction, preserve required ordering, and test merged results against the unsharded reference. Measure before changing hardware. [Check / Test]
8. **Separate repeatability from equivalence.** Require deterministic reruns of the same implementation under pinned inputs, state, and numerical environment. Compare discrete outputs exactly. For different implementations or environments, declare justified floating-point tolerances before measuring; require bitwise equality only where the contract demands it. Test downstream ranking, thresholds, constraints, rounding, and order decisions separately; a small numeric error does not prove equal decisions. [Test / Review]
9. **Avoid repeated validation overhead.** Reuse validated immutable revisions and their lineage metadata. Apply §6 validation at declared boundaries; do not add repeated full-data scans or dataset hashing. [Check / Test]

Review performance across module boundaries as well as inside kernels. Measure unnecessary reads, copies, serialization, and repeated interface calls before adding hardware or abstraction. Improve an interface when it forces wasteful usage, while preserving PIT, state, and numerical contracts. This applies [chapter 20's performance design](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch20.html). [Test / Review]

## 8. From MVP to full scope

Deliver a verifiable capability at each rung. Preserve compatibility or explicitly version and migrate changed contracts; do not freeze a mistaken first design. Record what remains out of scope. [Test / Review]

| Rung | Scope | Exit criterion | Enforced by |
|---|---|---|---|
| 1 | Smallest nondegenerate synthetic sample, all stages; enough instruments and dates for cross-sectional structure, warmup, and state transitions | Independent reference agrees; PIT, state, and basic idempotency checks pass | Test |
| 2 | Small real sample, all stages, real write in a test environment | Independent references agree; cutover, rollback, and recovery rehearsals pass | Test |
| 3 | Full universe | Coupling semantics and time, state, and working-memory budgets hold | Test |
| 4 | Full history | Batch, Backfill, and Step satisfy their declared equivalence contract; full-scale budgets hold | Test |
| 5 | Production | Go-live artifacts complete; a rewrite passes the shadow period | Check / Test / Review |

For cross-sectional projects, include multiple industries, suspended instruments, missing observations, and relevant market-calendar gaps in the first sample. Retain empty, single-row, and single-instrument cases as boundary tests rather than using them as the sole MVP. [Test / Review]

Apply these verification rules at each relevant rung:

- Take expected values from hand calculations, known formulas, an independent implementation, or a previous system frozen at a revision. Do not generate expectations from the code under test or silently reuse its disputed alignment logic in the reference. [Test / Review]
- Test boundary contracts, node mechanics, and the intended operational entry point. Use small read-only real fixtures with provenance, and fakes for external systems. Give each correctness rule accepting and refusing cases. [Test]
- Cover instrument lifecycle events, late or revised data, calendar gaps, and state recovery in the seeded synthetic dataset. Require a written reason and a new fixture version when expected values change. [Test / Review]
- Perturb inputs available only after the decision and verify that the earlier decision is unchanged. Test repeated availability marking and malformed boundary inputs as refusal cases. Permit bounded input or crash fault injection; do not use code mutation testing or multi-round adversarial review loops. [Test / Review]
- Run the three idempotency scenarios below from the first stateful reusable slice onward. Compare outputs, state, row uniqueness, aggregate weights, and publication counts; apply §7 numerical contracts without weakening same-key publication rules. [Test]

| Scenario | Required observation | Enforced by |
|---|---|---|
| Same decision day twice, including concurrent attempts | One logical result and one committed state transition; no duplicate rows, weights, or downstream publication | Test |
| Crash and recovery before commit, and after sink commit but before local acknowledgement | No mixed output/state pair; retry reconciles committed status and does not publish or advance twice | Test |
| Full Batch versus segmented Batch plus daily Step, Backfill, and repeated days | Overlapping outputs and state agree under identical warmup, PIT view, lineage, and the declared numerical contract | Test |

- Keep the fast suite within its time budget and run it before every push. Run acceptance at production-representative scale and record the environment and exact integrated revision. Worker-branch evidence alone is insufficient after integration. Distinguish executed checks from tests only specified for future implementation. [Check / Test]
- Choose the fastest viable execution mode using principles §7: do small tasks directly, delegate independent medium tasks only when parallel savings exceed coordination costs, and use a persistent task DAG for large or long-running work. Keep the task DAG distinct from the platform's computational DAG and execution state machines. [Review]
- For persistent work, record dependency status, versioned inputs, outputs, checkpoints, retry rules, and acceptance conditions. Use available workflows for repeatable steps, goals for durable objectives, cron for future wakeups, and bounded loops for iteration. Cron does not establish dependency readiness; a loop needs an exit condition and iteration or time budget. Verify capabilities before use, deduplicate repeated wakeups, and report a scheduled task as scheduled rather than completed. Reduce concurrency when coordination becomes slower than direct work. [Check / Test / Review]

- At each reusable delivery, run a design review alongside acceptance tests. Show how a new Alpha reuses the platform and how a provider change stays local. Inspect caller burden, duplicated knowledge, pass-through layers, and undocumented ordering assumptions. Consolidate tightly coupled code when that reduces total complexity; preserve or version public contracts during the change. Do not substitute function-count or line-count targets for this review. [Review]

## 9. Code style

- Follow the Zen of Python and keep nesting shallow. Prefer cohesive functions that a reader can understand in context; split when doing so hides a coherent mechanism or removes unrelated responsibilities. Do not fragment a mathematical computation into one-use wrappers solely to satisfy a length limit. [Review]
- Keep comments concise, but explain nonobvious mathematics and temporal semantics. Allow multiline docstrings in `schemas/` and quantitative operators; document tensor axes, units, degrees of freedom, and missing-value propagation where applicable. Do not trade necessary meaning for a line-count rule. [Check / Review]
- Permit parameter and configuration hashing only within §4 and §6. Enforce the dataset-hashing prohibition in every layer. [Check]
- Catch exceptions at real I/O, application-entry, or task-supervision boundaries with an explicit recovery or reporting policy. Preserve business refusal and record failures; do not swallow errors or silently substitute results. [Test / Review]
- Name a reference repository or module until the project has its own stable style. Assign each rule a checker, test, or reviewer; automate mechanical rules early and record the limits of each check. [Check / Review]

Write the interface explanation and caller example before implementing a consequential module. Document behavior, preconditions, units, tensor axes, time semantics, side effects, and failure cases that are not evident from the signature. Use difficulty explaining an interface as feedback on the design. This follows [chapter 13 on useful comments](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch13.html) and [chapter 15 on writing comments first](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch15.html). The principles' §§2, 7–9 define the corresponding boundary, coordination, and review requirements; these book-derived practices supplement rather than replace quantitative correctness gates. [Review]
