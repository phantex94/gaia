---
name: why
description: Strict Round 1 + Round 2 entry point (/qstack:why). Auto-runs setup & triage (Greenfield vs Brownfield, effort size). Fast-paths tiny scripts; for medium+ tasks runs interactive interview-me, creates gitignored .qstack/intent.yaml scaffold, iteratively interrogates for contradictions & future-flexibility hazards, and produces .qstack/roadmap.md before any business code is written.
---

# /qstack:why — Strict Round 1 (Intake & Scaffold) & Round 2 (Review & Roadmap)

**HARD RED LINE: DO NOT WRITE ANY CONCRETE BUSINESS LOGIC IN THIS MODE.**

## Round 1: Auto-Setup, Triage, Interview & Gitignored Scaffold

1. **Silent Context Ingest & Auto-Setup (`Read-Before-Asking`)**:
   - Read `../../references/principles.md` and `../../references/02-anti-ambiguity-yaml.md`.
   - Inspect the starting directory: check if it is an existing repo (Brownfield) or empty/new (Greenfield), read `AGENTS.md` / `Project Policy Hook` (if missing in an existing repo, silently note setup items or fold lightweight setup into triage), and read any referenced `README.md`, `api.py`, `reference_architecture`, `reference_data`, or `reader_code`.
2. **Triage (Context x Type x Effort)**:
   - Classify: **Greenfield vs Brownfield**, task type, and effort size.
   - **Fast Path (One-off script or tiny isolated edit)**: Do NOT create heavy scaffolding. Output a brief plan, execute directly, and verify with a runnable test. Done.
   - **Medium+ Path (Greenfield or multi-file / architectural task)**: Proceed to Step 3.
3. **Interactive Interview (`interview-me` discipline)**:
   - Use structured interactive questions (e.g. `AskUserQuestion` when available, otherwise concise numbered choices) to confirm 3 foundational pillars with the human:
     1. **Business Type** (which quant stages/domain: Data / Factor / Alpha-Model / Portfolio / Execution / Simulation-Risk);
     2. **Engineering Type** (Greenfield vs Brownfield: Add to graph / Rewire routing / Polish node internals; maturity L1/L2/L3);
     3. **Core Mission & Non-Goals** (what success looks like & what is explicitly out of scope).
4. **Round 1 Output — Gitignored `.qstack/` Scaffold + Pre-Filled Intent YAML (`Return-The-YAML`)**:
   - Ensure `.qstack/` is listed in `.gitignore` (add it cleanly if absent) so working scaffolds never pollute git status.
   - Select ONLY the matching template (`../../templates/greenfield.yaml`, `brownfield-add.yaml`, `brownfield-improve.yaml`, or `brownfield-evolve.yaml`).
   - Write `.qstack/intent.yaml` pre-filled with the user's description + facts already read from existing code/references, AND **return the full pre-filled YAML directly to the human in chat** for Round 2 refinement.

## Round 2: Iterative Refinement, Flexibility Review & `roadmap.md`

5. **Refine & Return Updated YAML**:
   - The human may edit `.qstack/intent.yaml` directly (freely adding/removing keys—design-time YAML is flexible markup) OR expand requirements in prose. Update `.qstack/intent.yaml` semantically and return the updated YAML for confirmation.
6. **Squeeze Intent & Flexibility Critique (`Challenge-Flaws-Early`)**:
   - Once the human confirms the YAML draft, rigorously review it (invoke `/qstack:interrogate` discipline):
     - Squeeze out remaining ambiguous business/quant semantics;
     - Surface obvious contradictions and design choices that harm **future flexibility** (aim to prevent future full rewrites without over-designing premature details).
   - Repeat until **zero objections remain** from all reviewing agents and the human signs off.
7. **Generate `.qstack/roadmap.md` (Single Living Phase Tracker)**:
   - Read `../../templates/roadmap.md` and write `.qstack/roadmap.md` listing every Phase's concrete deliverable:
     - **For graph-level / multi-stage goals**: Express each Phase target as **`CLI command <-> Sub-path in the Big Computational Graph`**, explicitly identifying reusable shared nodes across CLIs.
     - **For single-node tasks**: Do NOT force CLI/sub-path framing; state the node I/O contract and verification target directly.
   - As each Phase completes later, mark `[x]` with evidence **in-place inside this same `.qstack/roadmap.md`**.

## Exit & Handoff to Round 3
- Stop at Gate 1 once `.qstack/intent.yaml` and `.qstack/roadmap.md` are approved.
- **Next step**: Hand off to **`/qstack:architect`** for Round 3 (Data Models + Compute-Graph Routing + Skeleton Layout before any business logic).
- **Harness rule**: Run **Direct** (at most 1 read-only `subagent` to scan a large `reference_architecture`). Never launch `swarm` or `goal` in Rounds 1–2.
