# gaia — Quant Development Knowledge & `qstack` Plugin

This repository manages **`qstack` (`v0.3.0`)**, a `pstack`-inspired, strict 3-Round Claude Code plugin and cross-harness skill stack for human-agent quantitative framework and strategy development.

- Active plugin source: [`plugins/qstack/`](plugins/qstack/)
- Marketplace manifest: [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- Legacy v1 monolithic guide: [`dev-principles/`](dev-principles/) (kept intact for history)

## Strict 3-Round Workflow (`qstack`)

1. **Round 1 — Triage & Interview (`/qstack:why <one-sentence need>`)**, run by the **intake owner** (a work board's coordinator before the task exists, or the agent itself):
   - Triage by semantic risk, not size: an unconfirmed Red item, a public contract, a production/authority boundary, a new component or cross-package work makes a task **medium+**; everything else takes the **Fast Path** (plan -> execute -> test).
   - Read-Before-Asking: the repo `AGENTS.md` + Project Policy Hook, earlier intent files, and the design sources the Hook names; then one bounded interview (recommended option first).
2. **Round 2 — Interrogate & Confirm (Gate 1)**:
   - Draft the intent from `templates/intent-envelope.yaml` + the matching body; every `/qstack:interrogate` finding is an objection the human closes as `answer` or `non_goal` (at most 2 question batches + 1 confirmation).
   - The confirmed intent is committed as **`docs/intent/<task>.yaml`** (the Hook may name another folder); its `roadmap` section tracks phase progress. The builder works from it and the reviewer judges against it.
3. **Round 3 — `/qstack:architect` (Skeleton First, ZERO Business Logic, Gate 1B)**: the builder's plan.
   - **Greenfield**: Layout mapping core CLIs to graph sub-paths + exact typed stub files, written right after approval.
   - **Brownfield**: existing Layout (or a delta on the repo's design sources) annotated **① Add / ② Rewire / ③ Polish**.
   - **Ops**: production/authority-boundary requests and read-only audits of production systems or shared hosts go to `skills/mode/playbooks/ops-change.md` (runbook + rehearsal at Gate 1B, separate go/no-go before the production step).
   - Then sub-path delivery with `/qstack:verify` (Gate 2) and optional `/qstack:perf` (Gate 3).

On the herdr-projects board the Coordinator does Rounds 1–2 and the task's plan gate is Gate 1B: see [`docs/herdr-projects/qstack-coordinator.md`](docs/herdr-projects/qstack-coordinator.md).

## Slash Commands (`/qstack:<verb>`)

| Command | Role | Hard Guardrail |
| :--- | :--- | :--- |
| `/qstack:why` | Primary entry (Round 1 + Round 2): triage, Read-Before-Asking, bounded interview, confirmed `docs/intent/<task>.yaml` with `roadmap` | Fast-paths low-risk work; **zero business code**; every objection closed by the human |
| `/qstack:architect` | Round 3 skeleton: Data Models, compute-graph routing, Greenfield fill-in-the-blank stubs / Brownfield 3-way Layout delta | **Zero concrete business logic**; stops at Gate 1B for human review |
| `/qstack:mode` | Full-lifecycle orchestrator marching through Rounds 1 -> 2 -> 3 -> sub-path delivery & Harness selection | Stops at every Gate; loads only 1 matching playbook |
| `/qstack:how` | Strictly read-only walkthrough producing existing Layout, compute graph & blast radius | Zero file edits |
| `/qstack:interrogate` | Round 2 adversarial review: squeezes vague intent, exposes contradictions & future-flexibility hazards | Evidence-backed findings only |
| `/qstack:verify` | Independent verification: PIT perturbation, `Batch == Step`, `n`-day label-window Purge/Embargo, dual equivalence | Never generates ground truth from code under test |
| `/qstack:perf` | Profiling + explicit Speedup-vs-Readability human approval + dual-equivalence optimization | Stops immediately if Reference already meets budgets |
| `/qstack:setup` | Standalone repo onboarding (`Project Policy Hook` in `AGENTS.md`) | Never weakens core quant invariants |
| `/qstack:pause` | Cold-start safe handoff checkpoint | Zero hidden context |

## Install in Claude Code

```bash
# Local checkout
claude plugin marketplace add /Users/frank/workspace/gaia
claude plugin install qstack@qstack

# Or via GitHub once pushed
claude plugin marketplace add phantex94/gaia
claude plugin install qstack@qstack

# Helper script (also supports .agents/skills/)
bash scripts/install-qstack.sh [claude|agents]
```
