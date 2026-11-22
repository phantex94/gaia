# Playbook: Profile-Guided Performance Optimization

Use when an already-verified Reference implementation violates latency, throughput, working-memory, or persistent-state budgets.

## Ordered Execution DAG
1. **Confirm Gate 2 Baseline**: Ensure Reference passes all semantic, PIT, and `Batch == Step` tests first.
2. **Profile & Triage (`/qstack:perf`)** `[Harness: Direct]`
   - Benchmark at target scale in a named environment; separate I/O, copies/reshapes, compute kernels, peak working set, and persistent state.
   - If budgets already pass -> **STOP** (zero extra complexity).
3. **Zero-Readability-Cost Wins First**: Apply column projection, date pushdown, eliminating redundant copies/scans, and immutable artifact reuse; re-benchmark.
4. **Human Compromise Approval (Yellow Gate)** `[Harness: Direct]`
   - If deeper optimization (complex vectorization, compiled/GPU kernels, sharding) is needed, present `templates/brownfield-improve.yaml` (`optimization_tradeoff`: speedup vs readability cost + keeping Reference as permanent anchor).
   - **STOP** until human approves.
5. **Optimize & Dual-Equivalence Verify (`/qstack:perf` -> `/qstack:verify`)** `[Harness: Direct | bounded goal with explicit stop cap]`
   - Prove numeric tolerance + discrete decision parity (ranking ties, thresholds, positions, lots) + `state_t` parity against Reference.
   - Log before/after benchmarks in `docs/verification.md` and readability rationale in ADR.
