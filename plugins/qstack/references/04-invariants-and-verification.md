# 04 | Quant Invariants & Independent Verification

Every invariant follows **Red Line -> Common Illusion -> Mandatory Proof**.

## 0. Data Structure Contract (`Pin-The-Ends`)
- **Red Line**: Lock schema/shape, primary keys or tensor axes, exact dtypes (`float64`, `Date`), units, missing-value representation (`NaN / null`), and validity masks at system ends (Greenfield) or changed boundaries (Brownfield). Keep vocabulary canonical (`raw_close` for lots/margin vs adjusted `close` for returns—never overload one column name with two meanings).
- **Illusion**: Passing untyped dicts or mixing int/float across history and daily updates until silent drift appears.
- **Proof**: Positive and refusal schema/shape/unit contract tests; single-boundary conversion tests.

## 1. Point-in-Time & Historical Integrity (`Zero-Lookahead`)
- **Event Time != Availability Time**: At cutoff `t`, only inputs, universe members, specs, preprocessors, and models with `available_time <= t` are visible. Apply availability lag **once** at the authoritative data/asset boundary; reject double application (`LAG_ALREADY_APPLIED`); forbid manual `shift()` for data lag in downstream nodes.
- **Mandatory Proof (Future-Input Perturbation)**: Mutate all data with `available_time > cutoff` (to extremes or NaN) and assert all outputs and decisions at `<= cutoff` remain bit-for-bit identical.
- **Immutable As-Traded & Vintages**: Corrections and late data create new immutable revisions/vintages; never overwrite originally published As-Traded history. Determine recomputation scope by node invalidation/replay/refit policy, not lookback alone.
- **Split Isolation, Label-Window Purge & Embargo (Model Training)**:
  - **Exact Leakage Geometry**: When a training sample at feature date `t` uses an `n`-day forward label, that sample implicitly observes market information up through its **label maturity date `label_end(t) = t + n`**.
  - **Mandatory Purge / Embargo Rule**: All training samples must satisfy `label_end(t) <= split_cutoff`, leaving at least the full `n`-day label window between the last training feature date and the validation/OOS start (plus any configured extra embargo buffer for serial correlation in features/residuals).
  - **Model & Preprocessor Availability**: Scalers, imputers, feature selectors, hyperparameters, and model weights are fit strictly inside the purged training fold; a fitted model's earliest legal prediction date is `>= max(label_end)` across its training set.
  - **Mandatory Proof**: Assert `max(train.label_end) <= split_cutoff < min(eval.feature_date)`, physically isolate OOS via self-contained evaluation bundles where possible, and run a post-split perturbation test confirming mutations after `split_cutoff` leave fitted weights and earlier predictions unchanged. Never silently reuse an evaluated holdout as untouched test data.
- **Units & Missing Semantics**: Convert units in one authoritative module with range assertions. Preserve `NaN / null`; fail closed on non-finite corruption or missing required specs.

## 2. Computation & Sufficient State (`Batch-Equals-Step`)
- **Separate output from sufficient state**:
  ```text
  (inputs_t, state_{t-1}, params) -> (outputs_t, state_t)
  ```
  `state_t` holds everything required to advance `t+1` (counts, moments, recursive carry, window buffers)—not merely `outputs_{t-1}`. Load committed `state_{t-1}` read-only; never mutate committed state in place.
- **Execution-Mode Parity**: Verify full Batch, segmented Batch, daily Step, overlapping Backfill, and repeated days on non-degenerate multi-asset data; compare both outputs and `state_t`.
- **Numeric Closeness != Decision Equivalence (`Numbers-Are-Not-Decisions`)**: Test ranking ties, discrete thresholds, portfolio constraints, lot rounding, and orders separately from floating-point tolerances.
- **Deterministic Randomness**: Derive RNG streams from stable control keys `(seed, node_id, decision_time, subkey)`—never global sequential RNG or worker scheduling order.
- **Cross-Sectional Sharding**: Never shard cross-sectional ops arbitrarily by instrument. Declare valid grouping/reduction rules and verify against an unsharded reference.

## 3. Idempotency, Atomic Commit & External Reconciliation (L2/L3)
- **Logical Identity vs Physical Attempt**: Identify logical results by `(node_id, decision_time, vintage, config_digest)`. Retries append physical attempts under the same logical key. Matching retries short-circuit idempotently; conflicting content/lineage raises `Refusal` (never masked by numeric tolerance).
- **Atomic Output + State Visibility**: Stage immutable `outputs_t` and `state_t` together and publish via one atomic commit/manifest swap so readers never see mixed pairs.
- **External Side Effects**: A broker/sink timeout is not a rejection. Reconcile using stable external idempotency keys before resending. Local DB transactions do not guarantee external exactly-once; code rollback does not undo executed trades.
- **Refusal vs Programming Error (`Fail-Closed-Refusal`)**: Raise a dedicated `Refusal` (exiting cleanly and uncatchable by `except Exception`) for domain failures; keep `ValueError`/`TypeError` for programming bugs.

## 4. Independent Verification Ladder
- **Independent Oracles Only**: Expected values come from hand calculations, analytical identities, the clear Reference implementation, or a pinned legacy system—**never** generated by running the code under test.
- **Stage A (Synthetic Non-Degenerate Data)**: Multiple sectors, suspensions, listings/delistings, rolls, NaNs, constant rows, zero variance, calendar gaps, warmup, and multi-day recursion.
- **Stage B (Real Data Ladder)**:
  1. Small read-only real fixtures + fake external sinks (legacy same-day parity: zero diff or itemized attribution);
  2. Full universe cross-section (coupling + latency/peak memory budget);
  3. Full history (`Batch == Backfill == Step` + state growth budget);
  4. L3 Go-live: test-env real sink write, stale-input refusal, crash recovery, **human-confirmed alert receipt**, shadow period & rollback plan.
- **Honest Disclosure**: Branch tests passing != integrated acceptance. Record exact commands, environment, revision, pass results, and unverified items in `docs/verification.md`.
