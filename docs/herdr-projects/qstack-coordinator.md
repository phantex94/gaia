# qstack on the herdr-projects board: Coordinator and reviewer text

Binds qstack's roles (`plugins/qstack/references/00-protocol.md` §1, `06` §5) to the board. The Coordinator is qstack's **intake owner**: it runs Rounds 1–2 before `board add`. The task's agent is the **builder**: its plan is Round 3, Gate 1B.

## Coordinator instructions

[`qstack-coordinator-instructions.txt`](qstack-coordinator-instructions.txt) is the **full new value** of `coordinator.instructions`. Your current bullets stay word for word, except for these changes:

| Change | Text |
| :--- | :--- |
| Replaced | "Long or complex work: map the whole DAG first, list every decision that could block any lane, and interview the human in one batch …". Its DAG and no-open-yes/no parts move into the new interview bullet. |
| Added | Seven bullets: intake triage, medium+ intake, interview, add after confirmation, ops routing, ctrl+s/autopilot, and gates. |
| Extended | The repo-specific rules bullet now also names the intent folder, the design sources and the qstack Hook. |

Install after this PR merges. It is your step, not the agent's:

```bash
board=/Users/frank/.herdr-projects/data/bin/herdr-projects
$board set coordinator.instructions "$(cat docs/herdr-projects/qstack-coordinator-instructions.txt)"
$board show | grep coordinator.instructions    # check the value
claude plugin marketplace update qstack        # then /reload-plugins: the Coordinator needs qstack v0.3
```

Roll back with `board set coordinator.instructions "<previous value>"`. Copy the previous value from `board show` before installing.

## Reviewer sentence (optional)

This was not asked for in the task. The reviewer runs on Codex and has no qstack skills, so it can judge against the intent only if its instructions say so. To use it, append this sentence to `reviewer.instructions`:

> If the diff contains an intent file (the repo's intent folder, default docs/intent/), judge the work against it: every Red item in it honoured, every roadmap phase done with evidence or marked deferred in the file. Objections it records as resolved or as non-goals are not findings.

## Where each qstack gate lands

| qstack | Board |
| :--- | :--- |
| Triage, Gate 1 (intent confirmed, every objection closed) | Coordinator, before `board add` |
| Gate 1B (Round 3 skeleton or delta; ops: runbook and rehearsal plan) | `--plan.approve you`, then `board approve` |
| Ops go/no-go after rehearsal | The agent's `report --state blocked --kind permission`; your yes releases the production step |
| Gate 2 (math and semantics audit) | The repo's `check.command`, plus review when `--review.when always` (L2/L3 or a Red item) |
| Gate 3 (real data, perf trade-off) | Perf trade-off: permission stop. Acceptance: your merge approval (`merge.by you`) |
| `/qstack:pause` | The task's closing note |
