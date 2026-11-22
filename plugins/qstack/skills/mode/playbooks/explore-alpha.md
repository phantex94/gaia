# Playbook: L1 Fast Alpha / Strategy Exploration

Use for rapid hypothesis falsification (single factor idea, model prototype, ad-hoc attribution). Keeps engineering ceremony minimal while guarding quantitative truth.

## Mandatory Guardrails (Never Exempted Even in L1)
- `Zero-Lookahead` (read-only versioned PIT inputs; future-input perturbation check);
- Explicit math, axis, unit, and NaN/suspension semantics;
- Strict Train/Valid/Holdout split isolation + `n`-day label-window Purge/Embargo (`label_end(t)=t+n <= split_cutoff`);
- Independent hand-calc or analytical oracle;
- Runtime YAML recording exact experiment parameters + outputs isolated from production roots.

## Deliberate Exemptions
- Skip Backbone, full CLI wrapper, atomic publication, broker reconciliation, and speculative abstract classes.
- Keep code compact and `Math-First-Readability` so the human can audit and falsify fast.

## Ordered Steps
1. `/qstack:why` (lightweight `.qstack/intent.yaml` confirmation) -> Gate 1.
2. Write clean Reference script/module + runtime YAML + future perturbation & oracle check.
3. Report honest findings (including falsification). Promote to L2 via `evolve-boundary.md` only after the capability proves reusable (`>= 2` consumers) or moves toward live trading.
