---
name: interrogate
description: Round 2 adversarial spec review & flexibility critique (/qstack:interrogate). Squeezes remaining ambiguity out of the draft or committed intent YAML, exposes contradictions, and catches design flaws that threaten future flexibility. Every finding becomes an objection the human closes as answer or non-goal; no unbounded rounds. Never writes business code.
---

# /qstack:interrogate — Round 2 Intent Squeeze & Future-Flexibility Review

**Goal**: Align intent thoroughly enough to **prevent future full rewrites**—without drifting into premature implementation detail. Be direct, evidence-backed, and constructive (`Challenge-Flaws-Early`). Never edit business code.

## Steps
1. Read `../../references/principles.md`, `../../references/02-anti-ambiguity-yaml.md` (including §6), and `../../references/04-invariants-and-verification.md`.
2. Review the intent YAML (draft at intake, or `<intent folder>/<task>.yaml` later) through 6 sharp lenses:
   - **Vague Intent Remaining**: Any human-owned Red semantics still hand-waved (time/PIT, `n`-day label-window purge/embargo `label_end(t)=t+n <= split_cutoff` & `model_available_time`, missing/suspension, price basis, state sufficiency, refusal vs fallback)?
   - **Internal Contradictions**: Conflicting assumptions between inputs, outputs, CLI goals, priority slices, or the design sources listed in `sources`?
   - **Future-Flexibility Hazards**: Tight coupling that will force a full rewrite later (e.g., hardcoding raw-file paths inside compute nodes, fusing cross-sectional and per-instrument state, leaking provider quirks into factors, non-reusable graph nodes)?
   - **I/O Closure (`Pin-The-Ends`)**: Can outputs genuinely be computed from declared inputs/reference data?
   - **Scale & Priority Sanity**: Does the data model survive `target_scale`? Is `P0` clean of premature GPU/distributed scope?
   - **Over-Engineering Check**: Any speculative abstractions (`< 2` real implementations) or non-graph single-node tasks forced into heavy CLI ceremony?
3. Output a ranked **Review Table**: `Severity (Blocker / Flexibility Risk / Clarify) | Principle | Exact Issue | Concrete Fix`.
4. Write each substantive finding as an objection `O<n>` in `objections`; delegated Green details are not objections. Return user-visible `interrogate` A/R/H before -> after, including newly discovered material slots and coverage gaps; turn open ones into interview questions within the shared budget (`02` §1 steps 4–5, §6).
5. **Convergence**: objections already closed (`answer` or `non_goal`) are not raised again unless new repo evidence appears; then once, as a stop-and-ask whose answer goes to `decisions`. Return `reopened` / `reconfirmed` receipts at permitted new-evidence stop-and-ask and append to `decisions`. State whether every objection is closed and other Gate 1 prerequisites hold, or report BLOCKED with A/R/H and reasons. Never close by score.
