# Setup contract

## Interview

Inspect repository path, principles, installed versions, effective settings, active work, target feature, acceptance evidence, and execution authority. Record unknowns.

For this user's target, retain the declared pair Herdr 0.9.5 / herdr-projects 1.2.27. Track declaration, source evidence, and local observation separately. Verify the running host server as well as host CLI, plugin checkout/launcher/keeper, and harness versions. A valid minimum-version comparison is not an integration-test result. For other users, discover their actual pair rather than applying this target universally.

Ask only decisions that change the plan, at most three per round:

1. Which feature and observable outcome are required; is delivery research, reusable, or production?
2. Which actions are authorized: edits, delegates, PR, merge, deployment, recurring execution?
3. Can the installation carry a maintained local patch, and what resource/time constraints are fixed?

Skip answered questions. Classify each feature separately. Production elsewhere in a repo does not force a documentation edit through deployment gates.

## Output

| Field | Required content |
|---|---|
| Evidence | Observed version/path/commit, feature stage, checks found |
| Decisions | Goal, authority, route, unknowns, proposed choices |
| Capability matrix | Requirement, status, source, enforcement boundary, blocked actions |
| Changes | Exact file/key, original/proposed value, effective scope, reason, rollback |
| Checks | Check/Test/Review per rule, procedure and observable expected result |
| Limits | Unimplemented patches, missing tests, runtime checks not performed |

Use Check for static/schema inspection, Test for executed assertions, Review for judgment. A Review alone cannot enforce a runtime invariant.

Keep one repo policy source. Connect AGENTS and the compatible Claude entry point without deleting existing rules. Keep this skill distinct from upstream's generated `herdr-projects` skill.

## Bounded repair contract for a proposed fork

Keep this separate from existing upstream settings. Declare the authorized repair scope, selected check commands, attempt/time/cost limits, and stop conditions before launching a repair. Preserve existing explicit limits; ask for material missing limits rather than inventing them. Stop on business refusal, unauthorized scope expansion, exhausted budget, or repeated failure with no relevant progress. Infrastructure retries must not consume or reset business state. Re-run checks against the final changed tree; reuse narrower checks only when coverage rules justify it. Record the attempt, failure, change, final code version, and evidence by readable names; use no hashes. Deterministic repair does not require an adversarial reviewer exchange. Test each stop path and interrupted recovery in isolation.

## Receipt

Create a receipt only when applying changes, at an agreed repo-local metadata path. This is a proposed Gaia schema, not Herdr configuration:

```json
{
  "schema": "gaia-herdr-setup/1",
  "setup_id": "gaia-herdr-setup-2026-11-19-1",
  "mode": "upstream",
  "phase": "planned",
  "declared_host_version": "0.9.5",
  "declared_plugin_version": "1.2.27",
  "observed_host_server_version": null,
  "observed_plugin_runtime_version": null,
  "observed_upstream_commit": null,
  "feature": "alpha-cli",
  "feature_stage": "research",
  "param_set": "alpha-cli-board@1",
  "changes": [],
  "checks": [],
  "unresolved": []
}
```

Fill observed values only. Exclude credentials. Record each owned target, original value/content, desired value, completion state, and verification. Phases: planned, applying, applied, verified, failed; record rollback and its outcome separately. Use readable IDs: the setup is named by tool, date, and sequence number, and its settings by `param_set@seq`; a changed value takes the next `seq`. Record a Git commit ID only as a value such as `observed_upstream_commit`, never as a name. Use no hashes in any form; verify by comparing recorded and observed values directly.

Identify datasets by source, immutable revision/vintage, cutoff, and schema metadata. Metadata does not prove byte integrity: require controlled immutable storage and reject mutable/unversioned inputs when reproducibility requires immutability.

## Apply and recover

- Compare each target with its observed original before writing. Modify owned regions/keys only; preserve concurrent user changes.
- Record intent before each effect. On retry, inspect and adopt an already-applied matching effect instead of recreating it.
- Read effective settings through all scopes; reject unknown keys. Change a conflicting upper scope only within authorized scope.
- Roll back only owned writes whose current values still match. Preserve receipts and concurrent edits; report incomplete rollback.
- Do not activate production schedules incidentally. A separate scheduling request needs timezone, misfire, overlap, stop, and publication policies.
- Isolate repository, state home, harness configuration, and server/socket for runtime rehearsals. `HERDR_PROJECTS_HOME` alone does not isolate all installation effects.
- Quiesce live work and snapshot compatible state before runtime migration. Do not roll an old binary onto migrated state; retain or reconcile new events before backup restoration.

## Acceptance by scope

| Scope | Required evidence when applicable |
|---|---|
| Documentation/setup proposal | Links, schemas/examples, version-qualified capabilities, honest limitations |
| Research feature | Minimal runnable slice, input contract, PIT read boundary and causal checks |
| Reusable quant operator | Axes, units, missing semantics, boundary validation, causal/restart semantics, resource budget |
| Daily production | Same-day rerun; crash/recovery rerun; batch vs segmented batch + step; confirmed prior state; immutable As-Traded; atomic output/state; publication key; refusal and dry-run tests |
| Mutating setup | Apply twice without duplicates; interrupt/resume; preserve user edits; verify overrides and rollback |
| Local runtime fork | Strict identity across CLI/keeper/launcher, migration/replay, existing hook/lock regressions, patch acceptance |

Compare identical execution paths under a pinned environment exactly where promised. For different numerical algorithms require justified tolerances and separately check downstream decisions. Missing required evidence blocks corresponding readiness, even when installation succeeds.
