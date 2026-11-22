---
name: interrogate
description: Round 2 adversarial spec review & flexibility critique (/qstack:interrogate). Squeezes remaining ambiguity out of .qstack/intent.yaml, exposes contradictions, and catches design flaws that threaten future flexibility (preventing future full rewrites without premature over-engineering). Never writes business code.
---

# /qstack:interrogate — Round 2 Intent Squeeze & Future-Flexibility Review

**Goal**: Align intent thoroughly enough to **prevent future full rewrites**—without drifting into premature implementation detail. Be direct, evidence-backed, and constructive (`Challenge-Flaws-Early`). Never edit business code.

## Steps
1. Read `../../references/principles.md`, `../../references/02-anti-ambiguity-yaml.md`, and `../../references/04-invariants-and-verification.md`.
2. Review `.qstack/intent.yaml` (or active proposal) through 6 sharp lenses:
   - **Vague Intent Remaining**: Any human-owned Red semantics still hand-waved (time/PIT, `n`-day label-window purge/embargo `label_end(t)=t+n <= split_cutoff` & `model_available_time`, missing/suspension, price basis, state sufficiency, refusal vs fallback)?
   - **Internal Contradictions**: Conflicting assumptions between inputs, outputs, CLI goals, or priority slices?
   - **Future-Flexibility Hazards**: Tight coupling that will force a full rewrite later (e.g., hardcoding raw-file paths inside compute nodes, fusing cross-sectional and per-instrument state, leaking provider quirks into factors, non-reusable graph nodes)?
   - **I/O Closure (`Pin-The-Ends`)**: Can outputs genuinely be computed from declared inputs/reference data?
   - **Scale & Priority Sanity**: Does the data model survive `target_scale`? Is `P0` clean of premature GPU/distributed scope?
   - **Over-Engineering Check**: Any speculative abstractions (`< 2` real implementations) or non-graph single-node tasks forced into heavy CLI ceremony?
3. Output a ranked **Review Table**: `Severity (Blocker / Flexibility Risk / Clarify) | Principle | Exact Issue | Concrete Fix`.
4. Update `open_questions_and_pushback` in `.qstack/intent.yaml` and state clearly whether **zero objections remain** (ready for `.qstack/roadmap.md` + Round 3) or another alignment round is needed.
