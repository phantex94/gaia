---
name: verify
description: Independent quantitative verification (/qstack:verify). Builds non-degenerate synthetic tests, future-input perturbation, Batch == Step parity, n-day label-window Purge/Embargo checks, numeric + discrete decision equivalence, and real/legacy parity, writing honest evidence to docs/verification.md.
---

# /qstack:verify — Independent Quant Verification & Evidence

**HARD RED LINE: NEVER GENERATE EXPECTED VALUES FROM THE CODE UNDER TEST (`Prove It Works`).**

## Steps
1. Read `../../references/principles.md` and `../../references/04-invariants-and-verification.md`.
2. Inspect the frozen `.qstack/intent.yaml` (maturity tier `L1 / L2 / L3` and `independent_oracle`) and the implemented Reference/optimized code.
3. Build and run the verification suite matching the maturity tier:
   - **Data Structure Contracts (`Pin-The-Ends`)**: Positive + `Refusal` tests for missing columns, wrong dtypes, invalid units, and boundary conversions.
   - **Independent Oracle**: Hand-calculated small case, analytical identity, clear Reference, or pinned legacy revision.
   - **Non-Degenerate Synthetic Data (Stage A)**: Multi-sector panel with suspensions, listings/delistings, contract rolls, NaNs, constant rows, zero variance, calendar gaps, warmup, and recursive carry.
   - **Mandatory Quant Proofs (Always Required)**:
     - **Anti-Lookahead (`Zero-Lookahead`)**: Future-input perturbation (`available_time > cutoff` mutated to extremes/NaN -> `<= cutoff` outputs bit-identical); single-lag guard (double truncation raises `Refusal`; no ad-hoc `.shift()` for data lag in downstream nodes).
     - **Full vs Incremental Parity (`Batch-Equals-Step`)**: `Full Batch == Segmented Batch == Daily Step == Overlapping Backfill` on non-degenerate multi-asset data, comparing BOTH `outputs_t` AND sufficient `state_t`, plus read-only `state_{t-1}` rerun safety.
     - **Model Training Purge & Embargo (Whenever Labels / Learned Models Are Used)**:
       - For an `n`-day forward label, a training sample at feature date `t` has seen market data through its maturity date `label_end(t) = t + n`.
       - Assert every training sample satisfies `label_end(t) <= split_cutoff` (enforcing at least the full `n`-day label-window purge/embargo gap between the last training feature date and the first validation/OOS date, plus any extra serial-correlation embargo).
       - Assert preprocessors (scalers/imputers/selectors) and model weights are fit strictly inside the purged training fold, and that **model availability time `>= max(label_end)`** (a model never predicts dates earlier than its latest training label maturity).
       - Run **post-split perturbation**: mutate prices/labels after `split_cutoff` and assert fitted model weights, preprocessing params, and earlier predictions remain unchanged.
     - **Dual Equivalence (`Numbers-Are-Not-Decisions`)**: Separate numeric tolerance AND discrete decision parity (ranking ties, thresholds, portfolio constraints, lot rounding, orders).
   - **L2/L3 Extras**: Same-day rerun idempotency, concurrent attempts, pre/post-commit crash recovery, stale-input refusal, and (L3) real test-channel write + human-confirmed alert receipt.
4. **Harness Execution**:
   - Run small/fast suites Direct; use **`dynamic workflow`** to fan out independent verification axes (PIT, `Batch==Step`, legacy parity, boundaries) and aggregate results; use bounded **`goal`** only for long full-history parity loops.
5. **Write Honest Evidence**: Record exact commands, git revision, environment, pass counts, and any **unverified items** in `docs/verification.md`.

## Exit & Handoff
- Semantic mismatch -> return to implementation (or `/qstack:why` if spec was ambiguous).
- All green, budgets exceeded -> hand off to `/qstack:perf`.
- All green, budgets met -> ready to ship/archive and mark `[x]` in `.qstack/roadmap.md`.
