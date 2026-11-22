# Playbook: Greenfield System Build (Case A)

Use for building a new quant framework, full rewrite, or standalone subsystem from scratch.

## Strict 3-Round Execution DAG
1. **Round 1 — Auto-Setup, Interview & Scaffold (`/qstack:why`)** `[Harness: Direct; optional read-only subagent for large reference_architecture]`
   - Auto-check repo setup, scan `reference_architecture` (`README.md`/`api.py`) and `reference_data`/`reader_code`.
   - Run interactive `interview-me` confirming: **Business Type**, **Engineering Type**, **Core Mission**.
   - Draft & pre-fill the intent (`templates/intent-envelope.yaml` + `greenfield.yaml`) and return it to the human.
2. **Round 2 — Refine, Flexibility Critique & Roadmap (`/qstack:why` + `/qstack:interrogate`)** `[Harness: Direct]`
   - Refine the intent with the human's answers; review for vague intent, contradictions, and **future-flexibility hazards** until **every objection is closed** (`answer` or `non_goal`; at most 2 question batches + 1 confirmation).
   - Fill the intent's `roadmap`, expressing graph-level phase targets as **`CLI <-> Sub-path in Big Compute Graph`** (highlighting reusable shared nodes).
   - **GATE 1 (Stop)**: Human confirms the intent; it is committed as `<intent folder>/<task>.yaml` after Gate 1B.
3. **Round 3 — Data Models, CLI-to-Subpath Layout & Fill-in-the-Blank Stubs (`/qstack:architect`)** `[Harness: Direct]`
   - **ZERO concrete business logic.** Start from Data Models + reusable Compute-Graph routing.
   - Present the **Layout** mapping core CLIs (starting from the most core) to sub-paths of the big compute graph.
   - Create **fill-in-the-blank `.py` files** with typed `class`/`function` stubs, package trios, runtime YAML loader shell, Dry-run CLI stubs, and passing layer checks.
   - **GATE 1B (Stop)**: Human reviews Layout, routing, `.py` files, and stubs before any logic is filled. Mark phase `P0` `done` in the intent file.
4. **Sub-Path-by-Sub-Path Fill & Verification (`build` + `/qstack:verify` + optional `/qstack:perf`)** `[Harness: Direct | dynamic workflow for horizontal ops/verification | swarm if approved]`
   - Implement Math-First Reference logic one sub-path at a time -> verify on non-degenerate synthetic data (hand-calc oracle, future perturbation, `Batch == Step`, and model label-window Purge/Embargo) -> **GATE 2** human math audit.
   - Connect real data, run legacy parity & Profiling; invoke `/qstack:perf` ONLY if budgets fail (human approves speedup vs readability) -> **GATE 3**.
   - Mark each completed phase `done` with evidence in the intent file's `roadmap`.
5. **Ship & Transition (`ship-and-feed.md`)**: Archive Run Record & ADR; future phases operate in Brownfield mode.
