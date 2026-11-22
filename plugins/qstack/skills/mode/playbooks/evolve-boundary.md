# Playbook: Brownfield Rewire Routing / Boundary Evolution (Case D)

Use for adjusting compute-graph routing relationships, adding intermediate layers, changing shared I/O data models, or promoting L1 strategies into L2 framework modules.

## Ordered Execution DAG
1. **Round 1 — Existing Layout & Friction Trace (`/qstack:how` -> `/qstack:why`)** `[Harness: Direct]`
   - Inspect existing Layout, compute-graph edges, and every caller touching the boundary.
   - Run `interview-me`, create gitignored `.qstack/intent.yaml` (`templates/brownfield-evolve.yaml`) with 2 caller sketches, and return it to the human.
2. **Round 2 — Flexibility Critique & Roadmap (`/qstack:interrogate`)** `[Harness: Direct]`
   - Stress-test the new routing for future flexibility and migration safety; write `.qstack/roadmap.md` mapping affected CLIs <-> updated graph sub-paths.
   - **GATE 1 (Stop)**: Human selects sketch, confirms new I/O models, and approves migration strategy (`cutover` vs `dual_path_transition`).
3. **Round 3 — Existing Layout + Rewire Annotation (`/qstack:architect` Path B)** `[Harness: Direct]`
   - Present the **existing Layout** and explicitly mark **Mode ②: Rewire Routing** (before/after edges, new data models, and fill-in-the-blank boundary stubs with passing layer check).
   - **GATE 1B (Stop)**: Human approves rewired skeleton before logic migration begins.
4. **Incremental Migration & Parity (`/qstack:verify`)** `[Harness: Direct | swarm for approved multi-caller migration]`
   - Migrate callers sub-path by sub-path; verify behavior parity on synthetic + real tests; remove legacy paths (`Subtract Before You Add`); mark each phase `[x]` in `.qstack/roadmap.md`.
