---
name: how
description: Strictly read-only subsystem walkthrough & existing-layout mapper (/qstack:how). Inspects the current repository layout, computational graph routing, CLI-to-subpath mappings, and blast radius—producing the exact existing-layout baseline needed for Brownfield Round 3 (Add vs Rewire vs Polish). Zero file edits.
---

# /qstack:how — Read-Only Existing Layout & Compute-Graph Walkthrough

**HARD RED LINE: STRICTLY READ-ONLY. ZERO FILE EDITS.**

## Steps
1. Read `../../references/01-domain-model-and-dag.md`.
2. Inspect the current repository:
   - Map the **existing directory Layout** and layered package dependencies (`README.md`, `api.py`, layer checker).
   - Trace the **existing computational graph** across the 6 quant stages (`Data -> Factor -> Signal/Model -> Portfolio -> Execution -> Sim/Attribution/Risk`) and map existing CLI commands to their graph sub-paths.
   - Identify shared reusable nodes, data models at boundaries, PIT truncation points, state objects, and downstream tests/callers in the blast radius.
3. Return a crisp **Existing Layout & Graph Baseline** answering:
   - What is the current Layout and routing?
   - For the proposed task, does it **① Add to graph**, **② Rewire routing**, or **③ Polish node internals without changing routing**?
   - Which existing nodes can be reused and which invariants (PIT, `Batch == Step`, schema, units) sit in the blast radius?

## Exit & Handoff
- Feed directly into `/qstack:why` (to pre-fill `.qstack/intent.yaml`) and `/qstack:architect` (Round 3 Brownfield delta-on-layout review).
- **Harness rule**: Direct for focused scopes; 1 read-only `subagent` if scanning a large multi-package repo.
