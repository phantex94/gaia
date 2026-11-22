# Playbook: Ops Change & Production Audit (Case O)

Use for any operation on a running production system or shared host: a read-only **audit**, an **incident**, a **release/cutover**, or a **live change** (data or path move, config, deletion, scheduled-job change). A code change that later ships through a release uses its own playbook; this one covers the operation on production.

- Slots: `../../../references/02-anti-ambiguity-yaml.md` §5 (Core C1–C7, Conditional A/I/U/Q/M/D/H).
- Intent: `docs/intent/<task>.yaml` from `../../../templates/ops-change.yaml`.
- Standing facts come from the repo Hook's Ops block: `ops.hosts`, `ops.scheduler`, `ops.live_roots`, `ops.production_location_rule`, `ops.windows`, `ops.alerts`, `ops.owners`, `ops.standing_authority`, `ops.privileged_steps`, `ops.scan_budget`. A missing key is asked as a question, never guessed.

## Variants
| Variant | Slots | Rehearsal | Go/no-go | Ends with |
| :--- | :--- | :--- | :--- | :--- |
| **Audit** (read-only) | C1, C2, C3, C7, A | none | none | report: measured sources, budget kept, out-of-scope risks |
| **Incident** | Core + I (+ U if an input is late) | short, or stated why impossible | yes | cause, fix, verified next run |
| **Release / cutover** | Core + H (+ M, Q) | forward and undo | yes | new release serving, undo path intact |
| **Live change** | Core + matching M, D, H, U, Q | forward and undo | yes | change verified, before-inventory kept |

## Ordered Execution DAG
1. **Intent (before the task exists, about 5 minutes)** `[Harness: Direct; no host access]`
   - Ask only the high-priority intent: variant, target as the human sees it, who executes, red line or allowed actions, window or deadline, non-goals.
   - Fill the envelope's `confirmed`, `ops.variant`, `ops.authority` and `ops.windows`. Leave measured facts empty.
2. **Measured Inventory (after the task starts, read-only)** `[Harness: Direct | one read-only subagent for a large scan]`
   - From the scheduler and the host: what runs, what each job reads and writes (traced), current state, concurrent changes, whether alerting is healthy now.
   - Fill C1 and C5–C7 from what was measured; list it under `sources`. Run long scans detached on the Hook's compute host with a log and process id, within the scan budget.
   - Ask the open slots in one batch; each unresolved answer becomes an objection closed as `answer` or `non_goal`.
3. **Runbook & Rehearsal Plan → GATE 1B (board plan gate)** `[Harness: Direct]`
   - The plan carries the inventory, the runbook (forward steps, stop rule, undo or forward fix, half-done states) and the rehearsal plan (which copy, what is rehearsed, pass criteria).
   - Approval releases the rehearsal only, never the production step.
   - **Audit**: the plan carries the read set and scan budget; approval releases the scan, and the flow jumps to step 7.
4. **Rehearsal on a Copy** `[Harness: Direct]`
   - Run the forward path and the undo path on a copy root, dry-run every guard (including against an active case), and record the evidence.
5. **Go/No-Go → GATE 2 (separate stop after rehearsal)**
   - Re-check preconditions: live state still matches the inventory, no concurrent change, window open, privileged steps arranged.
   - Stop as blocked with a permission request naming the step and time, with the rehearsal evidence. Only the human's answer releases the production step; record it under `decisions`.
6. **Execute** `[Harness: Direct]`
   - Run inside the window under the stop rule: on stop, halt what the rule says and report; never continue with irreversible steps.
   - On a failed check, run the rehearsed undo or forward fix and report at once.
7. **Verify → GATE 3**
   - Run the C7 checks now against the before-inventory, including this change's alert test.
   - A check that needs a future window becomes a `deferred` roadmap item with owner and time; the task does not claim it as done.
   - Close with `./ship-and-feed.md`; add any new pitfall as a slot in `02` §5.

## Incident Variant
- Contain first, only with actions listed under `ops.standing_authority`; nothing irreversible before the cause is known.
- Find the cause (slot I): check whether the symptom predates the blamed event and find the first bad input before changing anything.
- The fix then follows steps 3–7, compressed: a short rehearsal, or a stated reason why none is possible, and always the go/no-go.

## Audit Variant
- Red line: no write, move, delete, restart or schedule edit, on any host, for the whole task.
- Measure the real source (scheduler, process table, traced reads, files on disk), not configs, copies or earlier reports.
- Keep the scan budget; when it cannot finish, report the partial result and what was skipped.
- Report risks outside the scope with evidence; do not fix them.

## Examples (marked: from board history, not rules)
- **AMC-45 (live data move)**: 10 review rounds hardening a move of data no live job read; C1 + M ("which scheduled job reads it, by trace?") would have kept it in place.
- **HOME-2 (deletion on a shared host)**: steps kept running after sudo failed because "stop" was undefined; C2's stop rule and D's reversible form would have held them.
- **DVN-1 (production design)**: the named service was not what ran; C1 read from the host scheduler finds the real crontab job.
- **AMC-51 (cutover)**: a model brief, with go time, stop preconditions, rollback trigger and command, forbidden windows and fixes not to undo; it passed first try.
