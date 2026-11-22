# 00 | Quant Development Brain: Core Protocol & Strict 3-Round Workflow

> **Scope**: Bidirectional engineering contract governing both human quant developers and AI agents across Greenfield system builds and Brownfield strategy/framework evolution.
> **Rule**: Never load the entire `references/` directory upfront. Follow the strict 3-Round interaction protocol and load only the matching template and reference(s).

## 1. Strict 3-Round Interaction Protocol

Two roles carry the rounds:
- **Intake owner** — runs Rounds 1–2 and talks to the human. On a work board this is the board's coordinator, *before the task exists*; without a board it is the agent itself via `/qstack:why`.
- **Builder** — the agent that owns the task. It runs Round 3 under the host's **plan gate** (a plan the human approves before any repo change; without a host gate, `/qstack:architect`'s own HARD STOP) and then delivers.

### Round 1 — Entry & Triage (`/qstack:why <one-sentence need>`)
1. **Triage** (`02` §1): a request is **medium+** when it touches an unconfirmed Red item, a public contract, a production/authority boundary, a new component, or more than one package/layer — size alone never decides. Everything else takes the **Fast Path** (short plan -> execute -> test, no intent file). The human's "fast" always wins; "interview" always forces medium+.
2. **Read-Before-Asking**: read the repo `AGENTS.md` + Project Policy Hook, earlier intent files, touched module `README.md`/`api.py`, and every design source the Hook names (design docs, ADRs, component pages). Ask only what they leave open.
3. **Interview**: one structured batch confirming ① Business Type, ② Engineering Type, ③ Core Mission & Non-Goals, plus the Red slots of the active slice (`02` §1 step 4).

### Round 2 — Interrogate, Converge & Confirm (Gate 1)
1. Draft the **Intent YAML** from the matching template and run `/qstack:interrogate`: every finding becomes an **objection** `O<n>`.
2. **Convergence rule**: each objection is closed by the human as `answer` or `non_goal`; nothing else closes it. At most 2 question batches + 1 confirmation (`02` §1). No unbounded rounds.
3. Add the **`roadmap`** section (`templates/intent-envelope.yaml`) at outcome level: one phase per deliverable with acceptance.
4. **Gate 1** = the human's confirmation. The confirmed YAML travels with the task (on a board: in the task description) and is committed by the builder as the **intent file** `<intent folder>/<task>.yaml` (default `docs/intent/`; the Hook may rename it).

### Round 3 — Data-Model & Compute-Graph Skeleton First (`/qstack:architect`, ZERO Business Logic, Gate 1B)
1. Start strictly from **Data Models** + **Computational Graph Routing** so nodes are reusable across features/CLIs.
2. **Greenfield**: Present **Layout** mapping core CLIs to sub-paths of the big compute graph + the exact **fill-in-the-blank `.py` stub files and typed signatures** -> **Gate 1B** -> write the stubs as the first build step, then fill **sub-path by sub-path**.
3. **Brownfield**: Present **existing Layout & compute graph** (or the delta on the design source pages the Hook names) -> mark **① Add to graph**, **② Rewire routing**, or **③ Polish internals** per file/node -> **Gate 1B**.
4. Refine the intent file's `roadmap` into `CLI <-> Sub-path` (graph tasks) or node contracts (single-node tasks). Gate 1B lands on the host's plan gate when there is one.
5. **Ops routing**: a request that crosses the production/authority boundary (triage rule 3), or a read-only audit of a production system or shared host, routes to `skills/mode/playbooks/ops-change.md` with `templates/ops-change.yaml` instead of the code skeleton; a non-production code change keeps its own playbook even if it ships through a release (variants: incident, release/cutover, live change, read-only audit). Gate 1B then reviews the runbook and rehearsal plan; host inventory is measured by the builder after it starts, never asked at intake.

### Intent File Lifecycle
Envelope fields shared by every intent template: `task`, `status`, `confirmed`, `sources`, `objections`, `decisions`, `roadmap`.
`confirmed` (intake) -> `building` (builder's first commit after Gate 1B, confirmed fields copied unchanged) -> roadmap phases marked `done` with evidence -> `delivered` (last commit; the file merges with the work). A later change is a new task with a new file and `supersedes:`. Red answers given mid-build are appended to `decisions` with their date.

### Gate Map
| Gate | Lands on |
| :--- | :--- |
| Triage | Intake owner, before the task exists |
| Gate 1 (intent confirmed, every objection closed) | Intake owner's confirmation question |
| Gate 1B (Round 3 layout/delta/stubs) | Host plan gate (board: plan approval) |
| Gate 2 (math & semantics audit) | Host check (repo tests + `/qstack:verify` suite) + review when the task is L2/L3 or touches Red items |
| Ops go/no-go (after rehearsal) | Builder stops for permission; the human's yes releases the production step |
| Gate 3 (real data, perf trade-off, go-live) | Perf trade-off: builder stops for permission; real-data acceptance: the human's merge approval; live actions: the ops go/no-go above |

## 2. Active Defaults (Omit Unless Overriding in `defaults_override`)
1. Acyclic layered dependencies (import strictly lower layers; no sibling domain imports; public `api.py` boundary; static layer checker).
2. Two distinct YAML regimes: **Design-time Intent YAML** (semi-structured markup, flexible) vs **Runtime Config YAML** (strictly validated once into frozen `Params`, zero hidden semantic defaults).
3. CLI-first interface (`<tool> <domain> <action> --config ...`), Dry-run default for writes, dedicated `Refusal` exit code, shell-script cross-task orchestration.
4. Single-point PIT truncation at the data/asset boundary; fail-closed `Refusal`; `NaN / null` preserved.
5. Synthetic -> Real data progression after Round 3 skeleton approval.
6. Readable identity: logical keys are business fields and readable versions; equality is checked by comparing content directly. A repo that needs hashes declares them in its Hook.

## 3. Two-Axis Routing & Three-Tier Authority
- **Axis 1 (Context)**: `A. Greenfield` | `B. Brownfield Add (to graph)` | `C. Brownfield Polish (no routing change)` | `D. Brownfield Rewire (routing/boundary evolution)` | `O. Ops Change / Production Audit (ops-change.md)`.
- **Axis 2 (Maturity)**: `L1 Explore` (PIT, I/O, split isolation, independent oracle, runtime YAML) | `L2 Reusable` (+ skeleton/boundary review, sufficient state, `Batch == Step`, CLI/YAML, scale budgets) | `L3 Production` (+ atomic commit, reconciliation, real channel & human-confirmed alerts, shadow/rollback).
- **Authority**: **Red (Human-Owned)** — I/O, priority slices, PIT/math/NaN/fill/compatibility (agent never guesses & pushes back on flaws); **Yellow (Co-Designed)** — Layout, routing, 2 sketches, speedup-vs-readability; **Green (Agent-Owned)** — internal helpers, validation, tests, profiling, evidence logs.
