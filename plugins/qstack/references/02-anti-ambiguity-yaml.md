# 02 | Anti-Ambiguity Protocol, Intent YAMLs & Critical Pushback

## 1. Strict Round 1 & Round 2 Protocol (`Read-Before-Asking` -> `interview-me` -> `Return-The-YAML` -> `roadmap.md`)
Before writing business code on any non-trivial task:
1. **Auto-Setup & Triage**:
   - Inspect the starting directory (Greenfield vs Brownfield), read repo `README.md`, `api.py`, contract tests, sibling examples, and any user-provided `reference_architecture`, `reference_data`, `reader_code`, or `reference_code`.
   - **Fast Path (tiny one-off script / isolated edit)**: Skip `.qstack/` ceremony—output a brief plan, implement, and test directly.
2. **Interactive `interview-me` Confirmation (Medium+ Tasks)**:
   - Confirm 3 foundational pillars before generating scaffolding: ① Business Type, ② Engineering Type, ③ Core Mission & Non-Goals.
3. **Gitignored `.qstack/` Scaffold + Pre-Filled Intent YAML (`Return-The-YAML`)**:
   - Ensure `.qstack/` is listed in `.gitignore`.
   - Write `.qstack/intent.yaml` from ONLY the matching template (`templates/greenfield.yaml`, `brownfield-add.yaml`, `brownfield-improve.yaml`, or `brownfield-evolve.yaml`), pre-filled with observed codebase/reference facts, and return it to the human.
   - Design-time Intent YAML is flexible semi-structured markup—accept human edits in YAML or prose without pedantic schema errors.
4. **Round 2 Critique & `.qstack/roadmap.md` (`Challenge-Flaws-Early`)**:
   - Review confirmed YAML for vague intent, internal contradictions, and **future-flexibility hazards** (prevent future full rewrites without premature over-design).
   - Once **zero objections remain**, generate `.qstack/roadmap.md` (`templates/roadmap.md`): state graph-level phases as **`CLI <-> Compute Graph Sub-Path`** (highlighting shared reusable nodes), or direct node contracts for single-node tasks. Mark completed phases `[x]` **in-place** in the same file.

## 2. Five-Point Agent Pushback Checklist (`Challenge-Flaws-Early`)
Check every proposal against these five failure modes and list hits in `open_questions_and_pushback`:
1. **Unclosed I/O**: Final output requires information absent from inputs (e.g., computing contract lots from adjusted `close` without `raw_close` and `multiplier`).
2. **Scale / Data-Structure Mismatch**: Proposed structure or backend will blow latency or memory budgets at `target_scale`.
3. **Priority Inversion**: `P0` pulls in GPU kernels, distributed mining, or plugin frameworks before a single-sample PIT + hand-calc loop works.
4. **Hidden Look-Ahead or Sharding Error**: Inputs lack availability semantics, labels bleed across OOS splits, or cross-sectional operators are naively sharded by instrument.
5. **Premature Abstraction / Layer Violation**: Proposing a registry/ABC/inheritance hierarchy for `< 2` real implementations, or violating acyclic downward-only layering.

## 3. On-Demand Red Slots by Quant Stage (Ask Only What Applies to Active Slice)
- **Data**: Primary key & bar timestamp semantics (start vs end), timezone & trading calendar, Event vs Availability Time, freshness limit, revision policy, missing/stale failure behavior.
- **Factor**: Universe filtering timing (before vs after compute), exact formula & `ddof`, warmup output (`NaN`?), suspension/NaN propagation, time-series vs cross-sectional group key, recursive sufficient state.
- **Alpha Combine / Model**: Label horizon `n` & fill price basis, `label_end(t) = t + n <= split_cutoff` purging & embargo, Train/Valid/Holdout split, train-only scaler/imputer fit, refit schedule & model availability cutoff, RNG derivation.
- **Portfolio**: Objective & risk unit alignment, exposure/leverage/turnover/hysteresis constraints, untradeable (suspended/limit) residual weight policy, lot rounding direction, infeasibility refusal vs fallback.
- **Execution**: Fill price basis & order slicing, fee/tax/slippage/margin rules, partial-fill & cancel state machine, broker timeout reconciliation key & halt procedure.
- **Simulation / Attribution / Risk**: Fill timing (`t+1` open / VWAP / next bar), participation cap, simple vs compound returns & roll costs, attribution dimensions, risk trigger & recovery conditions.

## 4. Two-Sketch Boundary Rule (L2/L3 Consequential Boundaries Only)
When creating or changing a shared base contract, public interface, or module split, sketch **two structurally distinct interfaces** with `<= 10` lines of realistic caller code each. Judge strictly on:
1. Caller cognitive load & pit-of-success against look-ahead mistakes;
2. Explicitness of research-changing policies;
3. Change locality (files touched when adding a factor or swapping a provider);
4. Vertical/horizontal fit without pass-through wrappers;
5. Avoiding needless data copies or long/wide conversions at boundaries.
