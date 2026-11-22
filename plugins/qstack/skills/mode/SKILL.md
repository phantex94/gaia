---
name: mode
description: Full-lifecycle qstack orchestrator (/qstack:mode). Drives the strict 3-Round workflow: Round 1 (/qstack:why auto-setup, triage, interview-me, gitignored .qstack/intent.yaml) -> Round 2 (flexibility critique & .qstack/roadmap.md) -> Round 3 (/qstack:architect data-model & compute-graph skeleton with human stop gate) -> sub-path Reference build, /qstack:verify, optional /qstack:perf, and roadmap marking.
---

# /qstack:mode — End-to-End Quant Orchestrator (Rounds 1 -> 2 -> 3 -> Delivery)

You are operating in **qstack mode**. Enforce strict upfront intent alignment, compute-graph decomposition, skeleton-first review, and human-compromised code.

## Master Flow
1. **Round 1 & Round 2 (`/qstack:why`)**:
   - Read `../../references/principles.md` and `../../references/00-protocol.md`.
   - Auto-run setup/triage. If the task is a tiny one-off script, execute the **Fast Path** (brief plan -> implement -> test) and finish.
   - For medium+ tasks: run `interview-me` (business type, engineering type, core mission) -> create gitignored `.qstack/` scaffold with pre-filled `.qstack/intent.yaml` -> return YAML to human -> iterate & critique for contradictions and future-flexibility hazards -> write `.qstack/roadmap.md` (`CLI <-> Compute Graph Sub-Path` for graph tasks; direct node target for single-node tasks).
   - **STOP at Gate 1** until zero objections remain and the human approves `.qstack/intent.yaml` + `.qstack/roadmap.md`.
2. **Round 3 (`/qstack:architect`) — ZERO Concrete Business Logic Yet**:
   - Start from Data Models + reusable Compute-Graph routing.
   - **Greenfield**: Present Layout (core CLIs <-> graph sub-paths) + create fill-in-the-blank `.py` files with typed `class`/`function` stubs.
   - **Brownfield**: Present existing Layout + annotate **Add to graph / Rewire routing / Polish without changing routing**.
   - **STOP at Gate 1B** for human review of Layout, routing, and stubs.
3. **Sub-Path-by-Sub-Path Delivery & Verification**:
   - Load ONLY the single matching playbook in `./playbooks/` (`greenfield.md`, `add-component.md`, `fix-and-parity.md`, `evolve-boundary.md`, `explore-alpha.md`, `optimize-perf.md`, `ship-and-feed.md`).
   - Select minimum-cost native Harness (`../../references/06-collaboration-and-hook.md`): Direct for interactive/tight tasks, `subagent` for isolated heavy reads, `dynamic workflow` for deterministic fan-out/parallel verification, `swarm` only after Round 3 stubs freeze & human approves, bounded `goal` only for machine-verifiable long parity/perf loops.
   - For each Phase/sub-path in `.qstack/roadmap.md`:
     1. Fill Math-First Reference logic (no premature optimization);
     2. Run `/qstack:verify` on non-degenerate synthetic data (hand-calc oracle, future perturbation, `Batch == Step`, and model label-window Purge/Embargo when applicable) -> **Gate 2** human math audit;
     3. Connect real data, profile, run `/qstack:perf` ONLY if budgets fail (human approves speedup vs readability) -> **Gate 3**;
     4. Mark the Phase `[x]` with evidence **in-place in `.qstack/roadmap.md`**.
4. **Pause / Close**: Use `/qstack:pause` for cold-start handoffs; follow `./playbooks/ship-and-feed.md` on final close.
