# 00 | Quant Development Brain: Core Protocol & Strict 3-Round Workflow

> **Scope**: Bidirectional engineering contract governing both human quant developers and AI agents across Greenfield system builds and Brownfield strategy/framework evolution.
> **Rule**: Never load the entire `references/` directory upfront. Follow the strict 3-Round interaction protocol and load only the matching template and reference(s).

## 1. Strict 3-Round Interaction Protocol

### Round 1 — Entry (`/qstack:why <one-sentence need>`)
1. **Auto-Setup & Triage**: Agent inspects the starting directory, checks repo Hook / references, and classifies **Greenfield vs Brownfield**, task type, and **effort size**.
   - **Fast Path (one-off script / tiny edit)**: Skip heavy ceremony—return a short plan, execute directly, and run tests.
   - **Medium+ Path (Greenfield or multi-file task)**: Run interactive **`interview-me`** confirmation covering: ① Business Type, ② Engineering Type, ③ Core Mission.
2. **Gitignored Working Scaffold**: Ensure `.qstack/` is in `.gitignore`, generate the matching template at `.qstack/intent.yaml` pre-filled from the user's description + existing repo/reference READMEs, and **return it to the human** (`Return-The-YAML`).

### Round 2 — Refinement, Flexibility Review & `.qstack/roadmap.md`
1. Human edits `.qstack/intent.yaml` (freely adding/removing keys—design-time YAML is semi-structured markup) or expands requirements in prose; agent refines and returns the updated YAML.
2. Once confirmed, agent rigorously reviews the spec (`/qstack:interrogate`): **squeezes out vague intent**, catches **contradictions**, and flags designs harmful to **future flexibility** (goal: prevent future full rewrites without premature over-design).
3. When **zero objections remain**, agent generates **`.qstack/roadmap.md`** listing every Phase's deliverable and marks phases `[x]` **in-place** as each completes:
   - **Graph-level tasks**: State deliverables as **`CLI command <-> Sub-path in the Big Computational Graph`** (highlighting reusable shared nodes).
   - **Single-node tasks**: State node I/O contract & test target directly without forcing CLI/sub-path ceremony.

### Round 3 — Data-Model & Compute-Graph Skeleton First (`/qstack:architect`, ZERO Business Logic)
1. Start strictly from **Data Models** + **Computational Graph Routing** so nodes are reusable across features/CLIs.
2. **Greenfield**: Present **Layout** mapping core CLIs to sub-paths of the big compute graph -> create **fill-in-the-blank `.py` files with typed `class`/`function` stubs** -> **HARD STOP** for human review -> fill and review **sub-path by sub-path**.
3. **Brownfield**: Present **existing Layout & compute graph** -> explicitly mark whether we are **① Adding to the graph**, **② Rewiring routing**, or **③ Polishing node internals without changing routing** -> **HARD STOP** for human review -> execute and mark `.qstack/roadmap.md`.

## 2. Active Defaults (Omit Unless Overriding in `defaults_override`)
1. Acyclic layered dependencies (import strictly lower layers; no sibling domain imports; public `api.py` boundary; static layer checker).
2. Two distinct YAML regimes: **Design-time Intent YAML** (semi-structured markup, flexible) vs **Runtime Config YAML** (strictly validated once into frozen `Params`, zero hidden semantic defaults).
3. CLI-first interface (`<tool> <domain> <action> --config ...`), Dry-run default for writes, dedicated `Refusal` exit code, shell-script cross-task orchestration.
4. Single-point PIT truncation at the data/asset boundary; fail-closed `Refusal`; `NaN / null` preserved.
5. Synthetic -> Real data progression after Round 3 skeleton approval.

## 3. Two-Axis Routing & Three-Tier Authority
- **Axis 1 (Context)**: `A. Greenfield` | `B. Brownfield Add (to graph)` | `C. Brownfield Polish (no routing change)` | `D. Brownfield Rewire (routing/boundary evolution)`.
- **Axis 2 (Maturity)**: `L1 Explore` (PIT, I/O, split isolation, independent oracle, runtime YAML) | `L2 Reusable` (+ skeleton/boundary review, sufficient state, `Batch == Step`, CLI/YAML, scale budgets) | `L3 Production` (+ atomic commit, reconciliation, real channel & human-confirmed alerts, shadow/rollback).
- **Authority**: **Red (Human-Owned)** — I/O, priority slices, PIT/math/NaN/fill/compatibility (agent never guesses & pushes back on flaws); **Yellow (Co-Designed)** — Layout, routing, 2 sketches, speedup-vs-readability; **Green (Agent-Owned)** — internal helpers, validation, tests, profiling, evidence logs.
