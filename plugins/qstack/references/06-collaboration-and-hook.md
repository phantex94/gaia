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
- `<intent folder>/<task>.yaml` (committed, default `docs/intent/`): the confirmed intent per task, its `objections`, `decisions` and living `roadmap` (phases marked `done` with evidence). The builder works from it; the reviewer judges against it.
- `docs/decisions/` (ADR): Major Yellow architectural & readability trade-offs.
- `docs/verification.md`: Executed commands, environment, revision, pass/unverified disclosure.
- `docs/tasks/`: `/qstack:pause` cold-start handoffs (or the host's handoff file, e.g. a board closing note).

## 4. Project Policy Hook (Zero Repo-Specific Pollution)
Keep `qstack` 100% repo-agnostic. Mount repo-specific stack rules, directory maps, intent folder, design sources, docs language, identity rules (including any hashes the repo needs), ops static facts, compute boundaries, and tool bindings via `templates/project-policy-hook.md` inside the target repository's `AGENTS.md`. A hook may tighten rules or bind paths/tools, never silently weaken core quant invariants or Gate 1.

## 5. Running on a Work Board (Host Binding)
qstack names no board; a host binds its roles once, outside the plugin:
- **Intake owner** = the board's coordinator: triage, Read-Before-Asking, interview and Gate 1 *before* the task is added (time-boxed to the high-priority intent, about 5 minutes); the confirmed YAML goes into the task brief, and the task starts with the host plan gate on.
- **Builder** = the task's agent: Round 3 is its plan (Gate 1B); its first commit after approval writes the intent file; mid-build Red questions and perf/ops go/no-go are stop-and-ask (permission) reports.
- **Gate 2/3** = the host's check command and review (on for L2/L3 or Red-touching tasks), then the human's merge approval.
- **Reviewer** reads the task brief, the diff (including the intent file) and `docs/verification.md`; resolved objections and non-goals are notes, never failing findings.
