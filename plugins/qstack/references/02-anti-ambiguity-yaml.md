# 02 | Anti-Ambiguity Protocol, Intent YAMLs & Critical Pushback

## 1. Strict Round 1 & Round 2 Protocol (`Triage` -> `Read-Before-Asking` -> `interview-me` -> `Return-The-YAML` -> Gate 1)
Run by the **intake owner** (`00` §1): a work board's coordinator before the task exists, or the agent itself via `/qstack:why`.
1. **Triage (medium+ on any one; size alone never decides)**:
   - An **unconfirmed Red item**: a definition that changes the delivered number or behavior and that no source fixes yet (PIT/availability, price series or basis, holdings/position semantics, label window, units/money/lots, fills, metric definition);
   - A **public contract** change (`api.py`, schema/contract type, frozen interface, CLI shape, config semantics);
   - A **production or authority boundary** (live roots/data, deletion, cutover, scheduler, external writes, release);
   - A **new package/component**, or work across more than one package or layer;
   - The human says "interview" (forces medium+) — "fast" always forces the Fast Path.
   - **Fast Path**: brief plan -> implement -> test; no intent file. A research-only task is fast unless a Red item decides its number; then its confirmed intent lives only in the task brief.
   - **Ops routing**: same interview; then a request that crosses the production/authority boundary (triage rule 3), or a read-only audit of a production system or shared host, routes to `skills/mode/playbooks/ops-change.md` with `templates/ops-change.yaml` instead of the code skeleton; a non-production code change keeps its own playbook even if it ships through a release.
2. **Read-Before-Asking (time-boxed, read-only)**: repo `AGENTS.md` + Project Policy Hook, earlier intent files, touched `README.md`/`api.py`, sibling examples, user-provided `reference_*`, and every design source the Hook names (design docs, ADRs, component pages). If a named source cannot be read, ask for it—never guess its content. Host inventory (what runs, where, how big) is measured by the builder after it starts, not asked at intake.
3. **Draft the Intent YAML** using `templates/intent-envelope.yaml` plus ONLY the matching body template (`templates/greenfield.yaml`, `brownfield-add.yaml`, `brownfield-improve.yaml`, `brownfield-evolve.yaml`, or `ops-change.yaml`), pre-filled with observed facts. Run the `/qstack:interrogate` lenses and the Red slots of the active slice (§3; or §5 for production ops/audit); each finding is an objection `O<n>`.
4. **Interview (`AskUserQuestion` when available; otherwise numbered choices)**: at most 4 questions per batch, 2–4 options each, **recommended option first**, and a "make it a non-goal" option where meaningful. Priority: ① Red items that change the output; ② production/authority boundary; ③ scope & non-goals; ④ acceptance oracle. **At most 2 question batches**, then **1 confirmation** showing the intent summary and every objection closed as `non_goal`.
5. **Convergence**: every objection ends as `resolution: answer` (the human chose) or `resolution: non_goal` (the human accepted it as out of scope); only the human closes one. After Gate 1 an objection may be reopened only with new repo evidence, once, as a stop-and-ask; the answer is appended to `decisions`. Reviewers do not reopen closed objections.
6. **Gate 1 & Handoff**: the confirmed YAML (`status: confirmed`) travels with the task—on a board, in the task description. The builder commits it unchanged as `<intent folder>/<task>.yaml` (default `docs/intent/`; `<task>` is the board key + slug, or `<yyyy-mm-dd>-<slug>`; never a hash-like name) right after Gate 1B. Design-time YAML stays flexible markup: accept edits in YAML or prose without pedantic schema errors. Keys stay English; values follow the repo's docs language.

## 2. Five-Point Agent Pushback Checklist (`Challenge-Flaws-Early`)
Check every proposal against these five failure modes and list hits as `objections`:
1. **Unclosed I/O**: Final output requires information absent from inputs (e.g., computing contract lots from adjusted `close` without `raw_close` and `multiplier`).
2. **Scale / Data-Structure Mismatch**: Proposed structure or backend will blow latency or memory budgets at `target_scale`.
3. **Priority Inversion**: `P0` pulls in GPU kernels, distributed mining, or plugin frameworks before a single-sample PIT + hand-calc loop works.
4. **Hidden Look-Ahead or Sharding Error**: Inputs lack availability semantics, labels bleed across OOS splits, or cross-sectional operators are naively sharded by instrument.
5. **Premature Abstraction / Layer Violation**: Proposing a registry/ABC/inheritance hierarchy for `< 2` real implementations, or violating acyclic downward-only layering.

## 3. On-Demand Red Slots by Quant Stage (Ask Only What Applies to Active Slice)
- **Data**: Primary key & bar timestamp semantics (start vs end), timezone & trading calendar, Event vs Availability Time, freshness limit, revision policy, missing/stale failure behavior.
- **Factor**: Universe filtering timing (before vs after compute), exact formula & `ddof`, warmup output (`NaN`?), suspension/NaN propagation, time-series vs cross-sectional group key, recursive sufficient state.
- **Alpha Combine / Model**: Label horizon `n` & fill price basis, `label_end(t) = t + n <= split_cutoff` purging & embargo, Train/Valid/Holdout split, train-only scaler/imputer fit, refit schedule & model availability cutoff, RNG derivation.
- **Portfolio**: Objective & risk unit alignment, exposure/leverage/turnover/hysteresis constraints, untradeable (suspended/limit) residual weight policy, lot rounding direction, infeasibility refusal vs fallback.
- **Execution**: Fill price basis & order slicing, fee/tax/slippage/margin rules, partial-fill & cancel state machine, broker timeout reconciliation key & halt procedure.
- **Simulation / Attribution / Risk**: Fill timing (`t+1` open / VWAP / next bar), participation cap, simple vs compound returns & roll costs, attribution dimensions, risk trigger & recovery conditions.
- **Operations on production** (incident, release, live change, production audit): use the Ops/Infra slots in §5.

## 4. Two-Sketch Boundary Rule (L2/L3 Consequential Boundaries Only)
When creating or changing a shared base contract, public interface, or module split, sketch **two structurally distinct interfaces** with `<= 10` lines of realistic caller code each. Judge strictly on:
1. Caller cognitive load & pit-of-success against look-ahead mistakes;
2. Explicitness of research-changing policies;
3. Change locality (files touched when adding a factor or swapping a provider);
4. Vertical/horizontal fit without pass-through wrappers;
5. Avoiding needless data copies or long/wide conversions at boundaries.

## 5. Ops/Infra Red Slots (Operations on Production Systems)
Core is C1–C7; Conditional is A, I, U, Q, M, D, H by operation class. Ask only what applies: all of Core for a change to production, only C1, C2, C3, C7 and A for a read-only audit, plus the matching Conditional slots. Take facts about what runs from measurement; take authority, windows and scope from the human. Playbook: `../skills/mode/playbooks/ops-change.md`; template: `../templates/ops-change.yaml`.
- **C1 Production Boundary & Live Source**: What runs, read from the scheduler or host rather than the brief? What does each job read and write, shown by a trace (a config that merely names a path is not a read)? Is the target the live root or a copy, shown by its path? Was each fact checked against the live source rather than a config, wrapper or stale copy? "Nothing deployed yet" is a valid answer.
- **C2 Authority & Executor**: Who approves and who executes each step, by name? What does "stop" halt, and what may continue? Which privileges, credentials or other owners are needed, and are they arranged before dispatch?
- **C3 Time Windows**: Required and forbidden windows, held for the whole run (not just its start); latest safe time; behaviour on overrun.
- **C4 Undo or Forward Fix**: What cannot be undone (served outputs, consumer effects, deletions)? Which existing rollbacks does this end? Trigger, command and executor? Was the undo path rehearsed on a copy?
- **C5 Blast Radius & Concurrent Changes**: Downstream jobs, consumers and repos; who approves a coverage loss; other changes to the same target or host in the window, and their order.
- **C6 Half-Done & Rerun**: State left when a step fails partway, is killed or overlaps itself; whether a rerun is safe and what must be checked first; which mechanism gives idempotency (a run id only attributes).
- **C7 Done Evidence**: The artifacts or exit codes that prove it, against a before-inventory; can each check run within the task (else a verify-at-time item with an owner); does this change's alert reach the channel the Hook names, with a test received?
- **A Audit**: Read-only red line (no write, move, delete, restart or schedule edit); measure the real source; scan time & IO budget with a fallback; report out-of-scope risks without fixing them.
- **I Incident**: Did the symptom start before the blamed event? First bad input? Which logs are normal noise? What may the Hook's standing authority contain before the cause is known?
- **U Upstream Late/Missing**: Producer, schedule and who can rerun it; is "no data" reported as success; refillable or permanent gap; which past outputs used the bad input?
- **Q External Quota**: Real call count per endpoint and date, against the waiver and other tenants of the same quota.
- **M Data/Path Move**: Move only what a live scheduled job reads; where production may live; what blocks non-production writes to the new root.
- **D Deletion**: Before-inventory (path, size, owner); references from live jobs, configs, provenance and rollbacks; reversible form first; guard dry-run against an active case.
- **H Shared Host / Scheduled Job**: Tenants sharing disk, compute, caches, locks and quota; which processes of the old, new and rolled-back release touch each shared resource or schedule; what holds if the switch fails halfway.
