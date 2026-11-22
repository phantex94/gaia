# Playbook: Brownfield Polish Internals / Fix / Parity (Case C)

Use for bug fixes, Batch/Step drift debugging, historical revisions, or polishing node characteristics **without changing graph routing**.

## Ordered Execution DAG
1. **Round 1 — Baseline, Blast Radius & Triage (`/qstack:how` -> `/qstack:why`)** `[Harness: Direct]`
   - Binary-search the compute graph for the first diverging node (for parity/drift bugs); map existing Layout, callers, and tests.
   - Fast-path if trivial isolated fix (brief plan -> repro test -> fix -> verify). For medium+ tasks, run `interview-me`, create gitignored `.qstack/intent.yaml` (`templates/brownfield-improve.yaml`), and return it to the human.
2. **Round 2 — Delta Critique & Roadmap (`/qstack:interrogate`)** `[Harness: Direct]`
   - Confirm exact before/after Delta, compatibility policy (`preserve_repro` vs `version_bump` vs `new_vintage`), and write `.qstack/roadmap.md` (single-node target—no artificial CLI ceremony).
   - **GATE 1 (Stop)**: Human approves Delta & compatibility.
3. **Round 3 — Existing Layout Delta View (`/qstack:architect` Path B)** `[Harness: Direct]`
   - Show the **existing Layout**, explicitly marking **Mode ③: Polish Internals (Zero Routing Change)** so the human confirms graph topology and public contracts stay untouched.
   - **GATE 1B (Stop)**: Human confirms scope.
4. **Repro-First Fix & Verification (`/qstack:verify`)** `[Harness: Direct | dynamic workflow]`
   - Write minimal failing reproduction test first -> apply minimal readable fix -> run regression, PIT, and parity checks.
   - Mark phase `[x]` in `.qstack/roadmap.md` and log evidence in `docs/verification.md`.
