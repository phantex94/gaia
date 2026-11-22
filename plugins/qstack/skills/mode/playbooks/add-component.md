# Playbook: Brownfield Add to Graph (Case B)

Use for adding new reusable nodes, factors, operators, data feeds, models, or a new CLI sub-path onto an existing quant architecture.

## Ordered Execution DAG
1. **Round 1 — Existing Layout Trace & Scaffold (`/qstack:how` -> `/qstack:why`)** `[Harness: Direct]`
   - Read existing Layout, `README.md`, `api.py`, and 1–2 closest siblings.
   - Fast-path if tiny/one-off; otherwise run `interview-me`, ensure `.qstack/` is gitignored, pre-fill `.qstack/intent.yaml` (`templates/brownfield-add.yaml`), and return it to the human.
2. **Round 2 — Critique & Roadmap (`/qstack:interrogate`)** `[Harness: Direct]`
   - Resolve Red semantics, verify future flexibility, and write `.qstack/roadmap.md` (single-node contract if it is a node task, or `CLI <-> Sub-path` if adding a new graph path).
   - **GATE 1 (Stop)**: Human signs off `.qstack/intent.yaml` + `.qstack/roadmap.md`.
3. **Round 3 — Existing Layout Delta View (`/qstack:architect` Path B)** `[Harness: Direct]`
   - Present the **existing Layout & compute graph**, explicitly marking **Mode ①: Add to Graph** (which existing nodes are reused, which new `.py` / class / function stub is added).
   - **GATE 1B (Stop)**: Human confirms placement before business logic is written.
4. **Reference Fill & Independent Verification (`/qstack:verify`)** `[Harness: Direct | dynamic workflow if adding >= 4 independent siblings]`
   - Implement Math-First Reference + runtime YAML entry -> verify hand-calc oracle, future perturbation, non-degenerate `Batch == Step`, label-window Embargo (if model), and rank/decision stability.
   - Mark completed phase `[x]` in `.qstack/roadmap.md` and record evidence in `docs/verification.md`.
