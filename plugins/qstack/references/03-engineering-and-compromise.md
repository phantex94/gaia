# 03 | Engineering Architecture, Backbone-First & Human-Compromised Code

## 1. Round 3: Data-Model & Compute-Graph Skeleton First (`Backbone-Then-Mock-Then-Real`)
**The first engineering deliverable writes ZERO concrete business logic.** Always decompose from **Data Models** and **Computational Graph Routing** so nodes are cleanly reused across CLIs and features.

### Step 1: Round 3 Skeleton Review (Gate 1B — HARD STOP)
- **Greenfield**:
  1. Absorb `reference_architecture` root docs, `README.md`, and `api.py` conventions when provided.
  2. Present the **Layout** mapping core **CLIs** (starting from the most core Phase 1 CLI) to **sub-paths in the big computational graph**, highlighting shared reusable nodes.
  3. Create only active-phase packages (empty `__init__.py`, `api.py` with `__all__`, `README.md`) plus **fill-in-the-blank `.py` files containing typed `class` and `function` stubs** (`NotImplementedError` bodies, zero concrete business math), strict runtime YAML loader shell, Dry-run CLI stubs, and passing acyclic layer check.
  4. **STOP for human review** before filling logic sub-path by sub-path.
- **Brownfield**:
  1. Present the **existing Layout & compute graph** from the codebase.
  2. Explicitly mark on top of that layout which of the **3 change modes** applies: **① Add features/nodes to the graph**, **② Rewire routing relationships**, or **③ Polish node internals without changing routing**.
  3. **STOP for human review** before editing business logic.

### Step 2: Non-Degenerate Synthetic Fill (Gate 2)
Feed a synthetic generator covering multiple sectors, suspensions, listings/delistings, contract rolls, NaNs, constant rows, zero variance, calendar gaps, and warmup. Pass independent hand-calc oracle, future perturbation, and `Batch == Step`.

### Step 3: Real Data & Profile-Guided Scaling (Gate 3)
Connect real fixtures/snapshots, verify parity against pinned legacy baselines where applicable, and profile at target scale.

## 2. Core Engineering Model: Frozen Value Objects + Vertical/Horizontal Extension
- **Immutable value objects & pure compute kernels**: Encapsulate shared domain facts as frozen typed classes (`Calendar`, `VisibleFrame`, `Panel`, `NodeState`, `Params`, `Refusal`). Write core math as pure functions or shallow components bound to those objects—no hidden file I/O, env vars, or wall-clock reads inside domain math.
- **Converge data-structure conversions**: Convert between disk-oriented tables (e.g. Polars) and dense compute panels (e.g. Torch `[..., T, N]`) at one authoritative boundary. Wrap bespoke `reader_code` inside the data adapter boundary.
- **Strictly two extension axes**:
  - **Vertical extension**: Extending the consumer chain (`Data -> Panel -> Factor -> Signal -> Portfolio`) or shallow specialization (`<= 2` levels). Forbid deep inheritance trees and `Manager/Service/Handler` pass-through layers.
  - **Horizontal extension**: Composition + frozen `Params` + module-local registries (`@operator`, `@alpha`, `@proposer`, `@selector`) assembled via runtime YAML. Create a registry only when `>= 2` real implementations exist; call a direct function for 1.
- **Deep Modules**: Pull messy mechanics (PIT selection, partition reads, state serialization, atomic commit) downward inside modules; keep research-affecting policies explicit at the interface/YAML.

## 3. Runtime Config YAML vs Design-Time Intent YAML
- **Design-time Intent YAML** (`templates/*.yaml`): Flexible, semi-structured alignment markup.
- **Runtime Config YAML**: Authoritative reproducibility contract (`YAML + git commit + input revisions = exact reproduction`):
  1. Place frozen `Params` next to the owning algorithm with inline unit/meaning comments; parse via one strict boundary loader (`load_section`) that rejects missing fields, unknown fields, and silent coercions.
  2. Assert cross-section consistency for shared keys (`horizon`, `label_id`, `capital`) at load time. Never scatter `cfg.get(k, default)`.
  3. Zero implicit defaults for semantic parameters; only pure runtime controls (threads, chunk size) may default.
  4. Use one commented template per workflow + explicit overlays for environments/experiments—never copy-paste full configs.
  5. Signature order: `(business_inputs, params_obj, *, runtime_controls)`. Forbid `**kwargs` passthrough; return named immutable records.
  6. Persist a Run Record (effective YAML + `config_digest`, git SHA, input revision IDs, predecessor state ID, numerical environment).

## 4. CLI-First & Script-Orchestrated Execution
- Shape: `<tool> <domain> <action> --config <path.yaml> [--override k=v] [--write]`. CLI is a thin shell containing zero business arithmetic.
- Writing commands default to **Dry-run** (printing plan, logical key, affected paths). Production writes require explicit env + publish authorization; no `--force` bypasses safety gates.
- Standard exit codes: `0` success (including idempotent short-circuit), `1` unexpected error, `2` business `Refusal` (structured reason + evidence to stderr).
- Orchestrate tight in-memory steps inside one CLI command; orchestrate across stages via clean shell/workflow scripts chaining CLIs for independent reruns and checkpointing.

## 5. Human-First Code & Performance Compromise
- **`Math-First-Readability`**: Core math reads linearly like equations. Do not chop cohesive formulas into tiny single-use helpers to chase a line limit. Annotate key tensor/table transforms with `shape / axis / unit / NaN` semantics and explain *why* (domain/numerical rationale), not *what*.
- **`Reference-First-Optimize-Second`**:
  1. Ship a readable Reference implementation first and pass Gate 2.
  2. Profile at target scale (I/O, copies, compute kernels, peak working memory, persistent state). **If budgets pass, stop.**
  3. Eliminate architectural waste first (column projection, date pushdown, eliminating redundant copies/scans) without harming readability.
  4. Before introducing complex vectorization, compiled/GPU kernels, or sharding that hurts readability, present a **Speedup vs Readability Cost** table for human approval, keep Reference as a permanent test anchor, and pass dual equivalence (numeric + discrete decision parity).
