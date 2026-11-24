---
name: mode
description: Full-lifecycle qstack orchestrator (/qstack:mode). Drives the strict 3-Round workflow: Round 1-2 (/qstack:why triage, Read-Before-Asking, interview, confirmed intent committed as docs/intent/<task>.yaml) -> Round 3 (/qstack:architect skeleton or delta as the plan gate, or the ops playbook) -> sub-path Reference build, /qstack:verify, optional /qstack:perf, and roadmap marking in the intent file.
---

# /qstack:mode — End-to-End Quant Orchestrator (Rounds 1 -> 2 -> 3 -> Delivery)

You are operating in **qstack mode**. Enforce strict upfront intent alignment, compute-graph decomposition, skeleton-first review, and human-compromised code.

## Master Flow
1. **Round 1 & Round 2 (`/qstack:why`, run by the intake owner)**:
   - Read `../../references/principles.md` and `../../references/00-protocol.md`.
   - Triage by semantic risk (`02` §1). Fast Path (brief plan -> implement -> test) intentionally skips scoring, ledger and interview; explicit fast cannot waive mandatory Red prerequisites, authority or gates. If blocked, report an unscored blocker; do not silently convert.
   - For medium+ tasks: Read-Before-Asking -> interview (≤ 2 batches) -> draft the envelope + body + roadmap -> interrogate -> every objection closed as `answer` or `non_goal` -> confirmation. Ops routing: a production/authority-boundary request or a read-only audit of a production system or shared host goes to `./playbooks/ops-change.md` with `../../templates/ops-change.yaml`; a non-production code change keeps its own playbook even if it ships through a release.
   - Medium+ only: emit all Ambiguity A/R/H receipts (`02` §6). **STOP at Gate 1** until all objections and other hard prerequisites are satisfied and the human actually confirms. On failure/budget exhaustion, status unconfirmed and no executable dispatch. On a work board the confirmed YAML goes into the task brief; directly, write `<intent folder>/<task>.yaml`.
2. **Round 3 (`/qstack:architect`) — ZERO Concrete Business Logic Yet**:
   - Start from Data Models + reusable Compute-Graph routing. On a work board this round is the task's plan (Gate 1B = plan approval).
   - **Ops routing**: skip the code skeleton; follow `./playbooks/ops-change.md` (runbook + rehearsal plan at Gate 1B, separate go/no-go before the production step).
   - **Greenfield**: Present Layout (core CLIs <-> graph sub-paths) + the fill-in-the-blank `.py` files with typed `class`/`function` stubs (listed in the plan, written right after approval).
   - **Brownfield**: Present existing Layout (or the delta on the design sources the Hook names) + annotate **Add to graph / Rewire routing / Polish without changing routing**.
   - **STOP at Gate 1B** for human review of Layout, routing, and stubs.
3. **Sub-Path-by-Sub-Path Delivery & Verification**:
   - Load ONLY the single matching playbook in `./playbooks/` (`greenfield.md`, `add-component.md`, `fix-and-parity.md`, `evolve-boundary.md`, `explore-alpha.md`, `optimize-perf.md`, `ship-and-feed.md`, `ops-change.md` for an audit, incident, release/cutover or live change on production).
   - Select minimum-cost native Harness (`../../references/06-collaboration-and-hook.md`): Direct for interactive/tight tasks, `subagent` for isolated heavy reads, `dynamic workflow` for deterministic fan-out/parallel verification, `swarm` only after Round 3 stubs freeze & human approves, bounded `goal` only for machine-verifiable long parity/perf loops.
   - For each phase/sub-path in the intent file's `roadmap` (committed with `status: building` right after Gate 1B):
     1. Fill Math-First Reference logic (no premature optimization);
     2. Run `/qstack:verify` on non-degenerate synthetic data (hand-calc oracle, future perturbation, `Batch == Step`, and model label-window Purge/Embargo when applicable) -> **Gate 2** human math audit (on a board: the host check + review);
     3. Connect real data, profile, run `/qstack:perf` ONLY if budgets fail (human approves speedup vs readability) -> **Gate 3** (on a board: the human's merge approval; ops production steps need a separate go/no-go after rehearsal);
     4. Mark the phase `done` with evidence in the intent file; set `status: delivered` in the last commit.
4. **Pause / Close**: Use `/qstack:pause` for cold-start handoffs; follow `./playbooks/ship-and-feed.md` on final close.

## Cross-task human attention (host-bound, optional)
When the existing Coordinator sees multiple human decisions, apply `../attention/SKILL.md` without adding a new round or agent. Mid-build questions must use the host's native waiting report before ending the turn; retain exact decision bindings and resume only after the real gate/answer. Do not auto-approve, add background automation or introduce scoring for Fast Path.
