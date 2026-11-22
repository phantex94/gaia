# Playbook: Ship, Archive & Compounding Feedback Loop

Use when Gate 3 passes and a slice (`P0`, `P1`, or Brownfield change) is ready to close cleanly.

## Ordered Steps
1. **Integrated Verification Audit**: Confirm checks ran on the final integrated revision (not just worker branches) and `docs/verification.md` lists exact commands, environment, revision, pass results, and any unverified production items.
2. **Reproducibility Check**: Confirm runtime YAML template + Run Record (effective config digest, git SHA, input revision IDs, predecessor state ID) reproduce the delivered artifact cleanly.
3. **Architecture & Decision Memory**:
   - Update affected module `README.md` (current facts only, no changelog prose);
   - Write an ADR in `docs/decisions/` for any major Yellow trade-off (2-Sketch choice, readability-vs-speed compromise, contract version bump);
   - Mark final Phase `[x]` in `.qstack/roadmap.md`.
4. **Compounding Feedback**: Note any newly discovered semantic pitfall to add to `02` Red slots for future runs.
5. **Next-Loop Transition**: If closing a Greenfield `P0`, mark the repo as **Brownfield** and propose the next `/qstack:why` entry for `P1` (or run `/qstack:pause` if stopping here).
