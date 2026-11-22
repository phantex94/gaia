# Roadmap: <project_or_task_name>

> Generated after Round 2 Gate 1 sign-off on `.qstack/intent.yaml` (gitignored working tracker).  
> **Rule**: Mark completed phases `[x]` **in-place** in this file with exact verification evidence.

- **Context**: `<Greenfield | Brownfield: Add / Rewire / Polish>`
- **Maturity**: `<L1 | L2 | L3>`
- **Task Shape**: `<Graph Sub-Path Delivery (CLI <-> Sub-Path) | Single-Node Task>`

## Big Computational Graph & Reusable Nodes *(omit for pure single-node tasks)*
- **Shared Reusable Nodes**:
  - `N1`: `<e.g., pit_panel_view (reused by panel build, factor run, evaluate)>`
  - `N2`: `<e.g., alpha_program_eval (reused by batch, step, search)>`
- **Graph Overview**:
  ```text
  Raw/L1 -> [N1: PIT Panel] -> [N2: Factor Program] -> [N3: Member Signal] -> [N4: Evaluate/Export]
  ```

## Phase Deliverables (Mark `[x]` In-Place Upon Verification)

### Phase 0 — Round 3 Skeleton (Zero Concrete Business Logic)
- [ ] **Greenfield**: Layout + CLI-to-subpath map + fill-in-the-blank `.py` files with typed `class`/`function` stubs + layer checker pass -> **Human Gate 1B Sign-Off**
- [ ] **Brownfield**: Existing Layout + annotated change mode (`Add / Rewire / Polish`) -> **Human Gate 1B Sign-Off**
- *Evidence*: `<commit / human approval note>`

### Phase 1 (P0) — `<Core CLI <-> Compute Graph Sub-Path 1>` *(or direct Node Target for single-node tasks)*
- [ ] **CLI Entrypoint**: `<e.g., cta alpha run --config ... [--write]>`
- [ ] **Graph Sub-Path**: `<e.g., N1(mock panel) -> N2(min ops + Program batch/step) -> N3(xs_signal)>`
- [ ] **Acceptance**: `<hand-calc oracle + future perturbation + Batch==Step on non-degenerate synthetic data>`
- *Evidence*: `<test command + pass result + revision>`

### Phase 2 (P1) — `<Next CLI <-> Compute Graph Sub-Path 2>`
- [ ] **CLI Entrypoint**: `<e.g., cta alpha evaluate --config ...>`
- [ ] **Graph Sub-Path**: `<e.g., N1 -> N2(reused) -> N3(reused) -> N4(eval bundle + gate)>`
- [ ] **Acceptance**: `<split isolation + label-window embargo + real fixture parity>`
- *Evidence*: `<pending>`

### Phase 3 (P2) — `<Scaling / Real Data / Perf>`
- [ ] **CLI Entrypoint / Target**: `<real snapshot + legacy parity + optional approved /qstack:perf>`
- [ ] **Acceptance**: `<full-scale budgets + docs/verification.md + ADR>`
- *Evidence*: `<pending>`
