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
- Every worker brief includes: frozen `.qstack/intent.yaml` slice, extension direction, allowed file ownership, complexity absorbed vs explicit caller policies, runnable acceptance commands, and stop-on-ambiguity rule.
- Passing branch tests are an input to review, **not** proof of integrated correctness. Coordinator verifies caller ergonomics and integrated revision tests.

## 3. Scoped Project Memory (Avoid Prompt Bloat)
Growing global caveats signal leaky module boundaries—fix the boundary before adding more rules.
- Root `AGENTS.md`: Short shared invariants + `Project Policy Hook` (`templates/project-policy-hook.md`).
- Module `README.md`: Responsibility, I/O contract, refusal codes.
- Executable code/schemas: Authoritative parameter and data contracts.
- `.qstack/` (gitignored working scaffold): Active `intent.yaml` and living `roadmap.md` (marked `[x]` in-place).
- `docs/decisions/` (ADR): Major Yellow architectural & readability trade-offs.
- `docs/verification.md`: Executed commands, environment, revision, pass/unverified disclosure.
- `docs/tasks/`: Active checkpoints & `/qstack:pause` cold-start handoffs.

## 4. Project Policy Hook (Zero Repo-Specific Pollution)
Keep `qstack` 100% repo-agnostic. Mount repo-specific stack rules, directory maps, storage/hashing policies, compute boundaries, and tool bindings via `templates/project-policy-hook.md` inside the target repository's `AGENTS.md`. A hook may tighten rules or bind paths/tools, never silently weaken core quant invariants or Gate 1.
