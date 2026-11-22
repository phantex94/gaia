# 01 | Quant Domain Model & DAG Problem Decomposition

## 1. Six-Stage Quant Consumer Chain
Every quantitative trading system decomposes into six stages forming a unidirectional consumer chain:

| Stage | Consumes | Typical Sufficient State | Produces | Primary Dimension |
| :--- | :--- | :--- | :--- | :--- |
| **1. Data** | Raw market, fundamental, contract specs, calendar, events | Immutable revisions, partition manifests, availability index | Standardized PIT data views | Time-series + Panel |
| **2. Factor / Feature** | Standardized PIT data + universe | Rolling buffers, recursive stats (counts, moments, EMA) | Factor panels | Time-series & Cross-sectional |
| **3. Alpha Combine / Model** | Factor panels + aligned labels (train only) + split spec | Model weights, fitted scalers, refit window, RNG derivation keys | Combined signals / alpha scores | Panel fit + CS/TS inference |
| **4. Portfolio Construction** | Signals + risk/cov model + current holdings + constraints | Current positions, turnover/hysteresis state, warm-start state | Target weights / positions | Cross-sectional opt + path state |
| **5. Execution** | Target positions + market microstructure + account + fee rules | Order lifecycle state machine, external idempotency keys | Orders, fills, position ledger | Event-driven state machine |
| **6. Simulation / Attribution / Risk** | Target/actual positions + fills + benchmarks + As-Traded history | Equity curve, cash ledger, drawdown/exposure watermarks | Performance, factor/cost attribution, risk halts | Time-series ledger + CS attribution |

**Consumer-chain rule**: Factors consume Data -> Signals consume Factors -> Positions consume Signals -> Fills & Attribution consume Positions. Downstream stages consume explicit upstream contracts—never bypass a layer to patch raw inputs silently.

## 2. Four Universal Cross-Stage Invariants
1. **Data Structure Contract (`Pin-The-Ends`)**: Lock schema/shape, primary keys or tensor axes, dtypes, units, and missing-value conventions at system ends (Greenfield) or changed boundaries (Brownfield).
2. **No Look-Ahead (`Zero-Lookahead`)**: Decisions at cutoff `t` see only inputs, universe members, specs, and models with `available_time <= t`.
3. **Acyclic Compute DAG + Explicit Spatial Coupling**: Single-run execution order derives from an acyclic dependency DAG. Every node explicitly declares `per-instrument (time-series)` vs `cross-sectional` (with grouping key and reduction rules).
4. **Full vs Incremental Consistency (`Batch-Equals-Step`)**: Full Batch, segmented Backfill, and daily Step must agree at the same decision time `t`, and retries must be idempotent.

## 3. Harmonizing Acyclic Execution DAGs with Nested Research Loops
Keep four graphs strictly separate:
1. **Computational DAG** (strictly acyclic): Single-run data -> factor -> signal -> position dependencies.
2. **Execution State Machine** (feedback transitions): Order fills, partial fills, account updates, risk halts.
3. **Research & Architecture Loops** (versioned across runs: `v1 -> v2`):
   - *Intra-stage loop*: Refine a factor formula or model hyperparameters by creating a new runtime YAML/code version and running a fresh acyclic DAG.
   - *Cross-stage loop*: Simulation/attribution diagnoses turnover, slippage, or risk leaks -> opens a new scoped task (`N0`) feeding back into earlier stages.
4. **Delivery Task DAG** (strictly acyclic): Per-task design, Backbone, Reference, verification, and optimization steps with explicit Gates.
