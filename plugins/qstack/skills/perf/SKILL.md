---
name: perf
description: Profile-guided, human-compromised performance optimization (/qstack:perf). Measures real bottlenecks at target scale, requires human approval on Speedup vs Readability Cost before complex optimization, and proves numeric + discrete decision parity against Reference.
---

# /qstack:perf — Profile-Guided Optimization & Human Compromise

**HARD RED LINE: DO NOT INTRODUCE READABILITY-DEGRADING OPTIMIZATIONS BEFORE PROFILING AND EXPLICIT HUMAN APPROVAL (`Reference-First-Optimize-Second`).**

## Steps
1. Read `../../references/principles.md`, `../../references/03-engineering-and-compromise.md` (Section 5), and `../../references/04-invariants-and-verification.md`.
2. **Confirm Gate 2 is green**: Never optimize code whose Reference semantics are not yet verified.
3. **Profile at Target Scale (Named Environment)**:
   - Measure and break down: wall time (I/O vs copy/reshape vs compute kernel vs serialization), peak temporary working memory, and persistent state size.
   - **Early Exit**: If Reference already meets `scale_and_perf.budgets`, **STOP immediately** and report success—zero extra complexity added.
4. **Eliminate Zero-Readability-Cost Waste First**:
   - Apply lazy columnar reads, date/column predicate pushdown, eliminating redundant copies/rescans, and reusing immutable validated artifacts. Re-measure.
5. **Human Approval Gate (Yellow Trade-off)**:
   - If budgets still fail and complex vectorization, compiled/GPU kernels, caching, or sharding is required, fill `optimization_tradeoff` (per `../../templates/brownfield-improve.yaml`) and present to the human:
     - Measured bottleneck breakdown;
     - Expected speedup / memory drop;
     - Readability & maintenance cost + confirmation that Reference stays as permanent test anchor.
   - Wait for explicit human approval.
6. **Implement & Prove Dual Equivalence**:
   - Implement approved optimization (bounded `goal` loop allowed only if exit criteria and dual checks are machine-verifiable).
   - Hand off to `/qstack:verify` to prove **numeric tolerance + discrete decision parity (ranks/thresholds/positions) + state parity** against Reference.
