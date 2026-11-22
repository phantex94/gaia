# gaia — Quant Development Knowledge & `qstack` Plugin

This repository manages **`qstack` (`v0.2.0`)**, a `pstack`-inspired, strict 3-Round Claude Code plugin and cross-harness skill stack for human-agent quantitative framework and strategy development.

- Active plugin source: [`plugins/qstack/`](plugins/qstack/)
- Marketplace manifest: [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- Legacy v1 monolithic guide: [`dev-principles/`](dev-principles/) (kept intact for history)

## Strict 3-Round Workflow (`qstack`)

1. **Round 1 — `/qstack:why <one-sentence need>`**:
   - Auto-runs setup & triage (`Greenfield vs Brownfield`, task type, effort size).
   - **Tiny one-off script**: fast-path plan -> execute -> test.
   - **Medium+ task**: runs interactive `interview-me` (business type, engineering type, core mission) -> creates gitignored `.qstack/` scaffold with pre-filled `.qstack/intent.yaml` -> returns YAML to the human.
2. **Round 2 — Iterative Refinement, Flexibility Review & `.qstack/roadmap.md`**:
   - Human edits `.qstack/intent.yaml` freely (flexible semi-structured markup) or expands in prose -> agent updates & runs flexibility critique (`/qstack:interrogate`) to eliminate contradictions and future-rewrite hazards.
   - With zero objections, agent generates `.qstack/roadmap.md` stating graph-level deliverables as **`CLI <-> Sub-path in Big Compute Graph`** (or direct node target for single-node tasks) and marks phases `[x]` in-place as they finish.
3. **Round 3 — `/qstack:architect` (Skeleton First, ZERO Business Logic)**:
   - Starts from **Data Models + Reusable Compute-Graph Routing**.
   - **Greenfield**: presents Layout mapping core CLIs to graph sub-paths -> generates **fill-in-the-blank `.py` files with typed `class`/`function` stubs** -> **HARD STOP** for human review -> fills and verifies sub-path by sub-path (`/qstack:verify`, optional `/qstack:perf`).
   - **Brownfield**: presents **existing Layout** -> annotates **① Add to graph / ② Rewire routing / ③ Polish without changing routing** -> **HARD STOP** for human review -> executes & marks `.qstack/roadmap.md`.

## Slash Commands (`/qstack:<verb>`)

| Command | Role | Hard Guardrail |
| :--- | :--- | :--- |
| `/qstack:why` | Primary entry (Round 1 + Round 2): auto-setup, triage, `interview-me`, gitignored `.qstack/intent.yaml` & `.qstack/roadmap.md` | Fast-paths tiny scripts; **zero business code** for medium+ tasks |
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
