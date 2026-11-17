# Compatibility and enforcement boundaries

Baseline: upstream `v1.0.0`, peeled commit `75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0`. The original `eliasstravik/herdr-projects` repository redirects to `eliasstravik/shepherdr`. Probe the actual installation; “1.0-ish” is insufficient. Legacy `PROJECT.md`/`thread_agent` workflows are not this configuration model.

Paths below refer to [the pinned source tree](https://github.com/eliasstravik/shepherdr/tree/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0).

| Requirement | v1.0.0 evidence | Setup boundary |
|---|---|---|
| Effective configuration | `crates/core/src/store/settings/lookup.rs`: task → user repo entry → global user → repo file → default; instructions accumulate, `none` resets broader instructions | Inspect all scopes. Repository config alone cannot guarantee effective settings. Settings are read per step, not frozen for the task. |
| Repo-supported fields | `crates/core/src/store/settings_list.rs`: `.repo()` marks eligibility | Use installed schema, not a hardcoded field count. Board/coordinator/watcher settings are user-only. |
| Roles and access | Default worker Claude, reviewer Codex; access `full` or `ask` | Preserve user preference. Neither a reviewer prompt nor `ask` establishes a read-only runtime. |
| Repair and review | `review.rounds` defaults to 3 and controls several send-back paths | `0` stops automatic send-backs, including failed-check fallback. It does not provide an independent check-repair budget or change adversarial reviewer wording. Service/quota recovery is separate. |
| Review selection | `review.when`: `repos`, `always`, `never` | Use proportional review, not compulsory agent review of every tiny edit. |
| Merge and planning | `merge.by`: `you`/`itself`; `plan.approve`: `none`/`you`/`reviewer` | Reuse authorization. Do not require approval for every deterministic repair. Automatic merge requires explicit authority. |
| Limits | `limit.time` per run; `limit.tokens` task aggregate checked at turn boundaries; `board.agents` board workers | Do not advertise an instantaneous hard cap or complete accounting for nested harness agents. |
| Direct execution | `crates/flow/src/coordinator/rules.rs` defaults to task creation, direct execution on explicit request | Automatic small-task routing requires a patch, including a safe project CWD and writer ownership. Appended instructions alone do not override fixed rules reliably. |
| Dependencies | `crates/flow/src/after.rs`, `after/pass.rs` use board completion semantics | Preserve cycle checks. Artifact/commit/evidence-sensitive edges require schema and start-time validation. Reports can legitimately satisfy report edges without merges. |
| Completion | `crates/flow/src/finish/turn_ended.rs` uses hooks/transcripts, stale-round guards, event watermarks, locks, and stage | Preserve existing guards. Do not claim screen idle alone completes a task. |
| Check purity | `crates/flow/src/finish/pipeline.rs` may commit tracked modifications after passing a check | Separate intentional generation from verification. Patch enforcement to reject unexpected changes and verify the final tree. |
| PR recovery | Pipeline creates PR before persisting its ID | Reconcile remote state after crashes. This is a source-derived recovery risk, not a reproduced duplicate-PR bug. |
| Reviewer brief | `crates/flow/src/finish/review_brief.rs` uses adversarial wording and commit-pinned verdicts | Keep commit attribution; separate verification from bounded repair. |
| Harness hooks | `crates/core/src/agents/adapter.rs` preserves Claude user hooks; existing Codex notify can use transcript fallback | Reuse adapters, preserve hooks, avoid two completion owners. Probe installed harness versions. |
| Automations | `docs/automations.md`: local timezone; missed events over five minutes skipped; overlap/loop guards exist | Declare timezone and missed-run policy. Do not promise catch-up. Goal/workflow/loop are proposed concepts here, not asserted v1.0.0 commands. |
| Local builds | `bin/run.sh` chooses fresh local build, downloaded version, or download/fallback | Local source edits can change selection. Require strict-local selection/build identity for a reliable fork. `HERDR_PROJECTS_RELEASES` selects a release source, not proof of integrity. |

Do not ship universal copy-paste settings: feature stage, upper-scope overrides, and authorization change suitable values. In this baseline, `review.rounds`, `review.when`, `merge.by`, and `plan.approve` lack `.repo()`; do not write them into a repository settings file. A user-level repository entry is a different scope. `check.again` is repo-eligible. Re-probe these permissions for other versions.

The pinned installation documentation uses `herdr plugin install eliasstravik/herdr-projects --ref v1.0.0`; local checkouts use `herdr plugin link "$PWD"` and `sh bin/run.sh install`. These mutate installation state. Verify support and rehearse in isolation; do not use them as probes. A checkout is not proof of which executable a running keeper uses.
