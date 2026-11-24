---
name: architect
description: Strict Round 3 skeleton-first design (/qstack:architect). Writes ZERO concrete business logic. Starts from data models and reusable computational-graph routing. For Greenfield, outputs Layout mapping core CLIs to graph sub-paths plus fill-in-the-blank .py files and typed class/function stubs, then STOPS for human review. For Brownfield, presents existing Layout and explicitly marks Add-to-graph vs Rewire-routing vs Polish-internals, then STOPS for human review (on a work board: the task's plan is this review, Gate 1B).
---

# /qstack:architect — Round 3: Data Models, Compute-Graph Routing & Skeleton First

**HARD RED LINE: ZERO CONCRETE BUSINESS LOGIC IN ROUND 3. NO REAL DATASETS. NO PREMATURE OPTIMIZATION.**

The first deliverable always models **data structures** and **routing across the computational graph** so that graph nodes are cleanly reused across different features and CLIs.

## Steps
1. Read `../../references/principles.md`, `../../references/03-engineering-and-compromise.md`, and the confirmed intent (the task brief's `## Intent (confirmed)` or `<intent folder>/<task>.yaml`), including its `roadmap` and `ambiguity` ledger for new Medium+ tasks. Do not proceed on an unconfirmed intent. If a material clarification is required, use `02` §6 before/after A/R/H receipts and the existing stop-and-ask/gates; do not rewrite the confirmed ledger. Historical intents without scores remain readable.
   - **Ops routing**: a request that crosses the production/authority boundary (triage rule 3), or a read-only audit of a production system or shared host, routes to `../mode/playbooks/ops-change.md` with `../../templates/ops-change.yaml` instead of the code skeleton; a non-production code change keeps its own playbook even if it ships through a release—stop here and follow it (runbook + rehearsal plan).
   - **Design sources** the Hook names (design/component pages, ADRs, a contract crate): Round 3 may reduce to a **delta on those sources**—list which pages/contracts change and propose an ADR or contract change instead of editing pages you do not own.
2. **Start from Data Models & Reusable Compute-Graph Nodes (`Pin-The-Ends`)**:
   - Define the core immutable data models (I/O contracts, state objects, frozen `Params` shells, `Refusal`).
   - Decompose required features from the **computational graph perspective**: show the big graph, which nodes are shared/reusable across features, and which sub-path each feature/CLI traverses.
   - For consequential L2/L3 boundaries, briefly compare **2 caller sketches** before freezing signatures.

3. **Branch Strictly by Greenfield vs Brownfield**:

   **Host plan gate**: when a host forbids repo changes before the plan is approved, the Round 3 output *is* the plan: Layout, routing, and the exact stub files with typed signatures written out in the plan. After approval, write the stubs exactly as planned as the first build step, together with the intent file (`status: building`).

   ### Path A: Greenfield (Skeleton + Fill-in-the-Blank Stubs)
   - **Step A1 — Present Layout & CLI-to-Subpath Map**:
     - Draw the repository directory **Layout** and narrow vertical dependency DAG (import strictly lower layers; zero sibling imports).
     - Explicitly map each core **CLI command** (starting from the most core Phase 1 CLI) to its **sub-path inside the big computational graph** and list the shared nodes it traverses.
   - **Step A2 — Create Fill-in-the-Blank Skeleton Files**:
     - Generate only the active-phase packages (each with empty `__init__.py`, `api.py` with `__all__`, and `README.md`).
     - Create the **fill-in-the-blank `.py` files** containing the **typed `class` and `function` stubs** (exact signatures, frozen dataclasses, docstrings, `raise NotImplementedError` placeholders—**no concrete business math yet**), plus strict runtime YAML loader & Dry-run CLI stubs.
     - Verify the static layer checker passes cleanly on the skeleton.
   - **Step A3 — HARD STOP (Gate 1B Human Review)**:
     - Present the Layout, CLI-to-subpath routing, `.py` file list, and stub signatures to the human.
     - **WAIT for human approval** before filling any business logic. After approval, implement and review **sub-path by sub-path**, marking each phase `done` with evidence in the intent file's `roadmap`.

   ### Path B: Brownfield (Existing Layout + 3-Way Delta Annotation)
   - **Step B1 — Present Existing Layout & Graph Routing**:
     - Display the **current repository Layout** and existing computational graph / CLI routing (from `/qstack:how` inspection).
   - **Step B2 — Annotate the Exact Change Mode on the Existing Layout**:
     Explicitly declare which of the **3 Brownfield modes** applies (and highlight exact files/nodes touched):
     1. **Add to Graph**: Add new reusable node(s) or a new sub-path/CLI onto the existing graph without breaking existing routes;
     2. **Rewire Routing**: Adjust graph edges, stage boundaries, or intermediate data contracts (include local stubs + migration steps);
     3. **Polish Internals (No Routing Change)**: Keep graph topology and public contracts untouched while fixing bugs, improving numerical rigor, or optimizing node internals.
   - **Step B3 — HARD STOP (Gate 1B Human Review)**:
     - Wait for human confirmation on the annotated existing layout and change scope before writing business code.

4. **Emit Execution DAG & Native Harness Plan (`Minimal-Harness-Cost`)**:
   - Refine the intent file's `roadmap` phases into `CLI <-> Sub-path` (graph tasks) or node contracts (single-node tasks).
   - **Fill `graph_slice`** (graph tasks; `../../templates/intent-envelope.yaml`): every node, edge and CLI the Layout delta touches, by its id in `<intent folder>/graph.yaml` (`../../templates/graph.yaml`), with mode `add | rewire | polish` (edges and CLIs also `remove`). Add and Rewire tasks list the `graph.yaml` change in the plan and commit it in the same PR; Polish leaves `graph.yaml` unchanged. A repo without `graph.yaml` gets it from `/qstack:how`'s draft first, as its own task or an approved first step.
   - Outline the post-review build DAG (sub-path by sub-path: Math-First Reference -> synthetic verification -> real data) and recommend the minimal Harness mode (`Direct` vs `dynamic workflow` for parallel horizontal nodes/verification vs `swarm` for approved multi-package concurrent work).

At a real human Gate 1B decision, provide the exact current plan/revision and evidence to the Coordinator's attention view when available (`06` §6). Keep the native Plan Gate; a batched reply is not itself proof that the host approved this plan. A changed plan needs renewed binding.
