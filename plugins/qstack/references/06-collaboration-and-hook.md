# 06 | Multi-Agent Harness Orchestration, Project Memory & Policy Hook

## 1. Native Harness Selection Rules (`Minimal-Harness-Cost`)
Optimize end-to-end wall time subject to correctness, counting decomposition, context handoff, merge conflicts, and integrated verification:

| Harness Mode | When to Use | When Forbidden | Typical Verbs |
| :--- | :--- | :--- | :--- |
| **Direct (Single Agent)** | High-interaction gates, tightly coupled edits (`< 3` files), L1 exploration | Large independent fan-out (`> 4` uncoupled siblings) | `why`, `how`, `interrogate`, `architect`, `perf` (profile/approval) |
| **`subagent`** | Single isolated heavy read/task (scanning a large `reference_architecture` repo's READMEs, syncing external docs/Notion) | Ambiguous human-owned semantic alignment | `setup`, `why` (read-only research), `ship` |
| **`dynamic workflow`** | Deterministic multi-stage pipeline or clean horizontal fan-out (implement + verify N uncoupled factors; parallel multi-axis verification aggregating into one report) | Exploratory work where modules must negotiate changing interfaces dynamically | `build` (horizontal fan-out), `verify` (parallel verification axes) |
| **`swarm`** | Medium/large L2/L3 concurrent multi-package development (each worker in isolated `share` worktree, coordinator owns shared contracts & integration) | Before Gate 1/1B freezes shared interfaces; small tasks where coordination dominates | `build` (only after `/qstack:architect` freezes stubs & human approves) |
| **`goal`** | Machine-verifiable long loops (full-history backfill/parity across many operators, bounded approved perf tuning) with explicit max iterations & no-progress stop rule | Missing objective exit criteria or unresolved human-owned Red decisions | `verify` (long full-history runs), `perf` (bounded approved tuning) |

## 2. Delegation & Integration Discipline
- Assign by **capability boundary** before files. One owner per shared semantic contract (PIT, state, YAML schema, atomic commit).
- Every worker brief includes: frozen intent-file slice, extension direction, allowed file ownership, complexity absorbed vs explicit caller policies, runnable acceptance commands, and stop-on-ambiguity rule.
- Passing branch tests are an input to review, **not** proof of integrated correctness. Coordinator verifies caller ergonomics and integrated revision tests.

## 3. Scoped Project Memory (Avoid Prompt Bloat)
Growing global caveats signal leaky module boundaries—fix the boundary before adding more rules.
- Root `AGENTS.md`: Short shared invariants + `Project Policy Hook` (`templates/project-policy-hook.md`).
- Module `README.md`: Responsibility, I/O contract, refusal codes.
- Executable code/schemas: Authoritative parameter and data contracts.
- `<intent folder>/<task>.yaml` (committed, default `docs/intent/`): the confirmed intent per task, its `objections`, `ambiguity` ledger (new Medium+), `decisions` and living `roadmap` (phases marked `done` with evidence). The builder works from it; the reviewer judges against it.
- `docs/decisions/` (ADR): Major Yellow architectural & readability trade-offs.
- `docs/verification.md`: Executed commands, environment, revision, pass/unverified disclosure.
- `docs/tasks/`: `/qstack:pause` cold-start handoffs (or the host's handoff file, e.g. a board closing note).

## 4. Project Policy Hook (Zero Repo-Specific Pollution)
Keep `qstack` 100% repo-agnostic. Mount repo-specific stack rules, directory maps, intent folder, design sources, docs language, identity rules (including any hashes the repo needs), ops static facts, compute boundaries, and tool bindings via `templates/project-policy-hook.md` inside the target repository's `AGENTS.md`. A hook may tighten rules or bind paths/tools, never silently weaken core quant invariants or Gate 1.

## 5. Running on a Work Board (Host Binding)
qstack names no board; a host binds its roles once, outside the plugin:
- **Intake owner** = the board's coordinator: triage, Read-Before-Asking, interview and Gate 1 *before* the task is added (time-boxed to the high-priority intent, about 5 minutes); return all Medium+ A/R/H checkpoints (`02` §6); Fast Path intentionally skips scoring. Only confirmed YAML goes into a runnable task brief, and the task starts with the host plan gate on. Budget exhaustion with open blockers leaves an unconfirmed, non-dispatched note, including in autopilot.
- **Builder** = the task's agent: Round 3 is its plan (Gate 1B); its first commit after approval writes the intent file; mid-build Red questions and perf/ops go/no-go are stop-and-ask (permission) reports.
- **Gate 2/3** = the host's check command and review (on for L2/L3 or Red-touching tasks), then the human's merge approval.
- **Reviewer** reads the task brief, the diff (including the intent file) and `docs/verification.md`; resolved objections and non-goals are notes, never failing findings.

## 6. Human Attention Scheduler (Coordinator skill)

Use `/qstack:attention` on demand across the task lifecycle, not as Round 4. It shares the existing Coordinator and board; QStack provides semantic policy, not an alternative task-state store or always-on runtime. The single-task `why` / `interrogate` still owns objection discovery, A/R/H and Gate 1.

1. **Collect** verified pending intake drafts and real board questions/gates (including plan, merge, permission and failure), normalize with `templates/decision-request.yaml`, preserve exact targets and decision owners. Incomplete identity or unknown wait kind stays manual/blocked. Never dispatch a pre-Gate-1 draft.
2. **Deduplicate** only identical, evidence-backed semantic definitions with matching scope, source revision, owner, options, and applicability. Different definitions/owners remain separate, conflicts are surfaced. Approval/authority never fan out. Green optional preferences are not mandatory objections.
3. **Prioritize** urgent safety/deadline, critical-path and aged mandatory requests, other mandatory questions, other approvals, then optional positive-value questions. For comparable estimates, use V = EVSI + delay_weight * marginal_project_delay_minutes - human_cost. Do not double-count shared downstream effects, invent estimates, or use the score to drop mandatory items. Aging promotes requests but is not a proven starvation bound. No wait to fill a batch for an urgent blocker.
4. **Batch** at most 4 separately bound decisions per interaction and one decision owner per batch. Use existing A/R/H for Medium+ at each actual clarification, accounting against each affected intake's actual budget (2 batches, 8 questions, separate ready confirmation); no new intake rounds. Fast Path skips scoring, ledger, interview and optional scheduling; its unavoidable blockers may be listed unscored. A queue preview is not an interview. Unresolved mandatory items remain blocked.
5. **Route** explicit human replies by request ID/version and member targets; re-read current exact prompt, scope, revision, dependencies and authority before any native action, then reconcile actual delivery. Generic yes, retrieved notes, and autopilot wakes are not approval. Plan/merge and permission remain native/manual; no generic tell into permission or approval. Only the original intake owner performs the usual confirmed Gate 1 handoff. No automatic task creation, approval or setting changes.
6. **MVP execution**: pure advisory scheduler and answer-binding checker in `skills/attention/scripts/`, using JSON snapshots, never invoking a host command. Without Node, apply rules manually. No background service, durable queue, or guaranteed event coverage; read the authoritative board every time. For post-Gate-1 waits, use the existing native blocked report and pause receipt, then resume from real state. No new mandatory pause or score for Fast Path.

The host binding belongs outside the portable QStack protocol. Use the main Coordinator for cross-project views and project Coordinators for local context; no cross-Coordinator writes or communication bus assumed. Existing autopilot scope/permissions, human approval gates, and board-only memory remain intact. See the Gaia Herdr binding and the deterministic offline evaluation; do not claim actual runtime integration or model accuracy from it.
