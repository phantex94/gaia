---
name: pause
description: Cold-start safe handoff checkpoint (/qstack:pause). Persists exact git revision, intent file path, verified evidence, unverified items, open Red/Yellow decisions, and the exact next command so a fresh session resumes with zero context loss.
---

# /qstack:pause — Cold-Start Safe Handoff

## Steps
1. Read `../../templates/pause-handoff.md` and `../../references/06-collaboration-and-hook.md`.
2. Collect ground-truth workspace state (never guess from memory):
   - Exact branch & git commit SHA (and whether dirty changes exist);
   - Active context (`A/B/C/D` x `L1/L2/L3`) and active slice (`P0 / P1 / P2`);
   - Path to the intent file `<intent folder>/<task>.yaml`, its `status`, and its open `roadmap` phases;
   - Verified items (with exact commands & pass results) vs in-progress/unverified items;
   - Unresolved Red/Yellow decisions or external blockers;
   - Exact next `/qstack:<verb>` or CLI command to run on resume.
3. Write the handoff note to the host's handoff file when it names one (e.g. a work board's closing note), else `docs/tasks/<task>-handoff.md`, and confirm no background/remote side effects are left in an ambiguous state.

For a real human-decision wait, preserve the current request ID/version, exact question/options, target revision/wait identity, outstanding authorization and any uncertain delivery receipt in the existing handoff record. Re-read host state before resume. On Herdr, the actual native blocked report must be issued before ending the waiting turn; a handoff note alone does not block the finish pipeline. Do not add an ambiguity score/ledger to Fast Path.
