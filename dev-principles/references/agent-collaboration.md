# Coordinator collaboration and project memory

Read for Herdr Projects task assignment, integration, handoff, and long-running work. This document owns agent execution and context management. Return to the [outline](../SKILL.md).

## Choose execution by end-to-end cost

Minimize completion time subject to correctness and acceptance. Count decomposition, context transfer, coordination, integration, and verification. Classify quickly rather than writing a plan merely to classify a small edit. [Review]

| Work | Execution choice |
|---|---|
| Small, bounded, few dependencies | Current agent works directly |
| Medium with independent deliverables | Delegate only when parallel savings exceed coordination cost |
| Large or long-running | Explicit task DAG, critical path, persisted inputs/outputs, and acceptance checkpoints |

This is a decision framework, not standing permission to spawn agents or schedule work. Follow current user authorization, tool availability, and repository rules. Reduce concurrency or merge tasks when coordination dominates. [Review]

When a task has a deadline and every worker slot is busy, say so at once and propose what to pause; a deadline task never waits silently in a queue. A job that runs longer than a few minutes runs detached on a host that stays up, with a log file and a process ID; it never depends on a laptop that may sleep or a session that may close. Check that it is alive before each status message. [Review]

Use available workflows for repeatable steps, transitions, retries, recovery, and handoffs; goals for durable objectives and completion criteria; cron for future wakeups or external checks; bounded loops for measured iteration. Verify actual tool and command support. A schedule does not establish dependency readiness. A loop needs exit conditions, an iteration/time budget, and a no-progress stopping rule. Workflow iteration does not authorize multi-round adversarial review. [Check / Review]

## Assign a capability before files

The coordinator owns decomposition, dependency planning, shared contracts, integration, and acceptance. Workers own bounded implementations and evidence. Prefer one project coordinator per repository when scope and execution need isolation. Cross-project observations go to that project's coordinator; they do not authorize editing another repository. [Review]

Give each task its business goal, representative examples, applicable contracts/instructions, allowed files/modules, dependencies, shared interface decisions, observable acceptance criteria, verification commands, and required memory/handoff updates. [Review]

Give each task one list of authorized actions. That list overrides older or broader boundaries for that task, within its stated limits. A worker that will not or cannot perform an action the outcome requires says so in its first plan, not at the end. [Review]

Before relying on a schedule, prove the real production path end to end once, by hand, with real inputs and the real output channel; a first scheduled run is not the proof. [Test]

A failed precondition stops every destructive step that depends on it. Delete nothing without an explicit approval, and keep rollback targets. [Review]

Machine-local identity never enters commits: host names, home paths, user names, tokens, and local tool configuration stay in uncommitted local files or the environment. Check it mechanically where the project can. [Check]

Define what complexity the capability absorbs, what callers retain, what policies remain explicit, and which changes stay local. PIT reading, visibility filtering, and revision selection need one semantic owner even if workers divide implementation. Separate concurrent writers through independent file ownership or isolated worktrees; shared contracts and integration have one owner. Release dependent tasks after acceptance of their prerequisites. [Check / Review]

Workers must not bypass checks, weaken validation, alter expected values to conceal defects, or report unexecuted tests as passing. Disclose simplifications, deviations, unresolved failures, and missing business context. Continue only independent work when a required answer is missing. Return changes affecting another worker's contract to the coordinator for reconciliation. [Review]

At integration, inspect representative caller code and evidence from the final integrated revision. Reject unexplained complexity pushed onto callers. A worker report or passing branch test is an input to review, not proof of integrated correctness. [Test / Review]

## Keep memory at the right scope

| Location | Authoritative content |
|---|---|
| Root `AGENTS.md` | Short shared invariants and working rules |
| Local `AGENTS.md` | Applicable local requirements that do not weaken global invariants |
| Public interfaces and schemas | Executable data and behavioral contracts |
| Module documentation | Responsibility, inputs/outputs, failures, mechanisms, and local rationale |
| `docs/architecture.md` | Actual cross-module topology and dependency direction |
| `docs/decisions/` | Accepted decisions, rationale, and superseded choices |
| `docs/verification.md` | Invariants, checks, scope, and recorded evidence |
| `docs/tasks/` | Status, hypotheses, versions, artifacts, and unresolved work |
| Repo settings file (for example `.herdr-projects.json`) | Committed per-repo tool facts such as the board check command; never policy text |
| Board user repo entry | Per-repo worker instructions and settings on the human's board, such as the base branch; a pointer to the repo's `AGENTS.md`, not a copy |
| Board global settings | Rules that hold for every repo; never one project's names, paths, or branches |
| Coordinator memory | The coordinator's own working preferences and reminders; pointers to repo docs, never the only copy of a project rule. Remove an entry when the human reverses it |

These are responsibility examples, not instructions to create empty directories. Keep one authoritative definition per fact and reference it elsewhere. A project rule found in a global scope is a leak: move it to the project and leave a pointer. Global caveats that expand on every task suggest information leakage: simplify the boundary before adding more instructions. Never make task logs a competing architecture specification. [Review]

English references in this library are authoritative; [Chinese review](../review.zh-CN.md) records human review prompts rather than a second rule set. Update the owning English reference when a rule changes, then update affected routes and review notes. Do not automatically propagate this library into every project's global agent instructions or install it into a user's skill directory. [Review]

## Preserve resumable evidence

Before handoff/context reset, record revision, completed changes, verification, open questions, and next action. Long tasks also pin dependency status, versioned inputs, output references, checkpoints, retries, and blockers. Resume from verified artifacts. Deduplicate wakeups so retries do not repeat commits, publication, or accounting effects. [Check / Test]

Update contracts and durable rationale in the same change as behavior. Resolve documentation/code discrepancies against approved business requirements; an implementation defect does not redefine the contract. Mark completion only after acceptance. Report scheduled work as scheduled, and disclose unverified production behavior. See [delivery](delivery-and-verification.md).
