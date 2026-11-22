---
name: pause
description: Cold-start safe handoff checkpoint (/qstack:pause). Persists exact git revision, frozen Intent YAML link, verified evidence, unverified items, open Red/Yellow decisions, and the exact next command so a fresh session resumes with zero context loss.
---

# /qstack:pause — Cold-Start Safe Handoff

## Steps
1. Read `../../templates/pause-handoff.md` and `../../references/06-collaboration-and-hook.md`.
2. Collect ground-truth workspace state (never guess from memory):
   - Exact branch & git commit SHA (and whether dirty changes exist);
   - Active context (`A/B/C/D` x `L1/L2/L3`) and active slice (`P0 / P1 / P2`);
   - Path to `.qstack/intent.yaml` and `.qstack/roadmap.md`;
   - Verified items (with exact commands & pass results) vs in-progress/unverified items;
   - Unresolved Red/Yellow decisions or external blockers;
   - Exact next `/qstack:<verb>` or CLI command to run on resume.
3. Write the handoff note to `docs/tasks/<task>-handoff.md` (or `.qstack/handoff.md` if the repo has no `docs/tasks/` convention) and confirm no background/remote side effects are left in an ambiguous state.
