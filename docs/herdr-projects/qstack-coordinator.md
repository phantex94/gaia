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
claude plugin marketplace update qstack        # then /reload-plugins: the Coordinator needs qstack v0.5.0 for attention
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

### Quantified intake (Medium+ only)

Apply `plugins/qstack/references/02-anti-ambiguity-yaml.md` §6 before board add. Return A/R/H at every applicable clarification checkpoint, preserve the ledger in the confirmed brief and append later receipts to decisions. Fast Path intentionally skips scoring, ledger and interview, but cannot bypass mandatory prerequisites or permissions. Unconfirmed/blocked Medium+ work (including autopilot) is not dispatched; plan approval is not Gate 1.

## Human Attention Scheduler (qstack v0.5)

The portable `/qstack:attention` skill runs in the existing Coordinator, not in a new task. The binding is tested offline against synthetic snapshots; no host patch or runtime service. Baseline: Herdr 0.9.5 / herdr-projects 1.2.27 (previous local observation, not re-probed).

| Operation | v1.2.27 binding |
| --- | --- |
| Collect | `herdr-projects list`, `herdr-projects details <id>`, existing intake context; use exact live objects, partial if inaccessible |
| Worker waits | `herdr-projects report <id> --state blocked --kind question\|permission\|auth --msg "<actual reason>"` then stop the turn; a plain question is not a wait |
| Normal question | `herdr-projects tell <id> <explicit bound human answer>`, only with current question state and authority; reconcile outcome |
| Plan / merge | native human approval UI or user's explicit native action; never generic tell/auto-approve |
| Permission/auth/pick/failure | human's native action, no generic fan-out |
| Wake | manual attention/status, existing applicable authorized autopilot wake; no new daemon, automation or setting change |

Tasks waiting for humans hold no `board.agents` slot already. They can still count toward `autopilot.tasksAtOnce`. Autopilot's stuck event only covers tasks it may look after; approval wake coverage is not complete with approve disabled. Do not enable `autopilot.approve yes` to make attention work. `board.notify` supplies coarse events; an event adapter, durable approval inbox, or host compare-and-act is outside this release. The main Coordinator may read a cross-project view; actual actions remain scoped, no cross-coordinator bus. Do not write external notes during autopilot's board-only-memory wake.

### Install and smoke-test (human-controlled)

Keep your current binary versions and effective coordinator settings. Inspect the current value and its scope before applying; back it up and merge any local-only customization instead of blindly replacing it. Use the existing `set coordinator.instructions` command only for the intended scope (e.g. `--main-coordinator`, `--project-coordinator <repo>`), update/reload the qstack plugin from the configured marketplace, and start/reload the appropriate Coordinator as needed. No new background task is required. In the existing chat type `/qstack:attention` (Claude Code) or `attention` (Coordinator instructions); for Codex ensure the repository's linked skill is available. If the helper cannot run, apply the policy manually and disclose that.

From the Gaia checkout:
```bash
node plugins/qstack/skills/attention/scripts/test_attention.mjs
node plugins/qstack/skills/attention/scripts/cli.mjs schedule plugins/qstack/skills/attention/scripts/example.json
```
Verify a real isolated board task reports blocked instead of finished; the slot is released; a read-only attention view includes that question plus an independent plan approval; no action occurs on a bare yes; explicit correct question reply resumes only that task; native approval stays manual. Inject changed plan/PR/wait and duplicate reply, confirm refusal/reconciliation; check pre-Gate-1 no dispatch and Fast no scoring. These runtime tests remain to be run locally.

Pinned sources: [waiting-for-you](https://github.com/eliasstravik/shepherdr/blob/v1.2.27/docs/waiting-for-you.md), [work and slots](https://github.com/eliasstravik/shepherdr/blob/v1.2.27/docs/how-work-gets-done.md), [autopilot](https://github.com/eliasstravik/shepherdr/blob/v1.2.27/docs/autopilot.md), [coordinator](https://github.com/eliasstravik/shepherdr/blob/v1.2.27/docs/coordinator.md), [settings](https://github.com/eliasstravik/shepherdr/blob/v1.2.27/docs/settings.md).
