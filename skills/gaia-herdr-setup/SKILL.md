---
name: gaia-herdr-setup
description: Inspect a repository, user goals, and an installed Herdr Projects version; customize agent collaboration around Gaia principles. Use when setting up Herdr with Claude Code or Codex, choosing upstream configuration versus a local fork, or adapting workflows to research, reusable, or production features.
---

# Gaia Herdr Setup

Treat the repository's development principles as requirements. Adapt Herdr to them.

## Inspect before asking

- Read applicable `AGENTS.md`, development principles, manifests, checks, and current diff. Locate the target feature. Preserve user changes.
- Inspect installed versions, executable/plugin paths, local patches, configuration scopes, hooks, and active work. Avoid secrets and full environment dumps. Prefer file inspection; live board queries can perform housekeeping.
- Read [compatibility.md](references/compatibility.md). The user's declared pair is Herdr host 0.9.5 plus herdr-projects plugin 1.2.27. Record host CLI/server and plugin checkout/launcher/keeper separately; do not ask the user to repeat these versions. Treat the pinned source as evidence, not proof of the local runtime. Probe actual help/schema before generating commands or settings. Mark unverified capabilities `unknown`; do not silently upgrade, downgrade, or substitute current upstream main.
- Inspect every rule scope: board global settings, user repo entries, coordinator scopes (`--main-coordinator`, `--machine-coordinator`, `--project-coordinator <repo>`), the repo file, repo `AGENTS.md`, and coordinator memory. A project rule found in a global scope is a leak to move, not a rule to copy. Folders registered by mistake are archived with `archive --repo`, never deleted.
- Classify each target feature separately as research, reusable, or production. Do not infer readiness from directory names or test-file existence.

## Resolve missing decisions

- Ask at most three short questions per round. Resolve the outcome and acceptance evidence, then missing execution authority, deployment boundary, budgets, or willingness to maintain a fork.
- Reuse observed facts and existing authorization. Distinguish facts, user decisions, and proposals. Never invent business defaults or treat silence as approval.

## Select the smallest sufficient route

- Execute small local work directly when permitted. Delegate independent medium tasks when overhead is justified. Use a persistent task DAG for large or restartable work; add schedules and bounded loops only when needed.
- Keep the development task DAG, quant data DAG, and trading state machine separate. Do not equate board completion with valid downstream artifacts.
- Classify requirements as `native`, `configurable`, `advisory`, `patch-required`, `unsupported`, or `unknown`. Explain the enforcement boundary.
- Use upstream configuration where sufficient; use a thin fork for missing hard guarantees. Never call prompt text access control or invent upstream settings for proposed features.
- Optimize delivery time subject to correctness. Keep one task authority and one writer per worktree; budget nested harness agents together with board workers.

## Produce a reviewable plan

- Follow [setup-contract.md](references/setup-contract.md). Map each change to a principle, exact path/setting, effective scope, rollback, and `Check`, `Test`, or `Review`.
- Keep shared policy in the repository. Adapt Claude Code and Codex entry points without competing policy copies or overwriting upstream's `herdr-projects` skill and existing hooks.
- Preserve PIT single availability stamping and future perturbation tests; separate DAGs from execution state; parse strictly once at boundaries; prohibit business defaults and zero-filled missing values; allow stale inputs only within a declared bounded degradation; preserve a business-refusal exit code distinct from the usage-error code 2, child exit codes that reflect business state, and default dry-run CLI behavior.
- Preserve append-only run evidence, idempotent logical outputs under readable logical publication keys, immutable As-Traded history, and state updates anchored to the confirmed previous snapshot.
- Use no hashes in any form: no content hashes, checksums, fingerprints, hash manifests, hash-based keys, or hash-like names. Name configurations as readable `param_set@seq`; logical keys are readable business fields; a Git commit ID is recorded as a value, never used as a name. A third-party download that verifies its own integrity is outside this rule.
- Require stage-appropriate evidence. A documentation repo needs documentation/skill validation, not invented quant tests. Missing required checks block readiness; never create pass-only test stubs.

## Apply within scope

- For a proposal request, return the plan and a reviewable diff when original content is available; otherwise label the output a proposed change list and state what prevents a real diff. Do not install, change live configuration, or activate schedules. For authorized execution, apply reversible changes without asking again.
- Use owned regions or narrow edits. Record original values and effective overrides. Preserve user additions; flag concurrent edits instead of replacing whole files.
- Rehearse runtime changes in a disposable repository with isolated state, harness configuration, and Herdr server/socket. Never attach a test keeper to live tasks.
- Make setup idempotent: unchanged reruns create no duplicate hooks, tasks, schedules, worktrees, or instructions. Resume from a receipt and reconcile effects before retrying.
- Verify a local fork's CLI, launcher, and keeper use the intended build. Reject silent upstream fallback. Plan migration and rollback before switching live binaries.
- Never activate production jobs as an incidental setup step.

## Verify and report

- Check final effective settings. For mutating setup, repeat application and test interrupted recovery in isolation.
- Report changed paths, observed build identity, checks actually run, limitations, and rollback. Separate document evaluation from runtime integration testing.
- Never infer production readiness from successful installation; require the feature's causal, idempotency, and operational evidence.
