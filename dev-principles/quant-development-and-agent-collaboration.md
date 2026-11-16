# Quantitative development principles and coordinator collaboration

Use this document as the engineering baseline for quantitative trading projects developed through the Herdr Projects coordinator workflow. Apply it when planning work, assigning tasks, implementing changes, and reviewing delivery.

The objective is to preserve quantitative correctness while keeping the system understandable, reproducible, and adaptable. Project knowledge must survive individual agent conversations through explicit contracts, repository instructions, and executable checks.

## 1. Establish the domain invariants

Before implementing a capability, identify its business meaning, inputs, outputs, failure behavior, and applicable invariants. Carry these requirements through architecture, task briefs, implementation, and acceptance checks.

### Preserve point-in-time correctness

Every decision must use only information available at the decision time. Distinguish an observation's event time from the time the system could actually access it. Define time zones, trading calendars, publication delays, revision policies, and same-timestamp ordering where they affect results.

Apply these rules to raw data, universe membership, corporate actions, features, preprocessing, model artifacts, portfolio construction, and execution. Historical queries must select the data vintage that was available then. A model artifact must not be used before its inputs and training process could have produced it.

An event-driven architecture can represent these constraints, but event processing alone does not guarantee point-in-time correctness. Enforce availability rules at data interfaces and decision boundaries. Fail closed when required temporal information is missing or ambiguous.

Test causality directly. Changing data that becomes available after a decision must not change that decision. Include revised data, delayed publications, and boundary timestamps in the relevant scenarios.

### Separate training, validation, and final evaluation

Declare temporal splits and their purpose before running model selection. Fit learned preprocessing and model parameters only on the permitted training data for each fold. Validation may guide selection within the declared protocol. Keep the final out-of-sample evaluation isolated from that selection process.

Account for overlapping labels and forward return horizons. Use purging or embargo periods when those dependencies require them. Record split boundaries, fitting windows, and the selection protocol with each result. Do not silently reuse an evaluated holdout as an untouched test set.

### Make numerical semantics explicit

Define units, currencies, price conventions, quantity conventions, numeric representations, and rounding policies at physical interfaces. Declare where conversions occur and prevent repeated conversion or unintended precision loss.

Choose representations according to the domain. Specify tick and lot constraints for orders and a justified error tolerance for floating-point calculations. Do not substitute arbitrary defaults for missing specifications, invalid values, or stale required inputs.

Parse and validate external data and configuration at entry points. Pydantic models, frozen data classes, or equivalent typed contracts may provide these checks. Use strict parsing where coercion would hide an error. Normalize inputs once, then let internal code rely on the validated contracts.

## 2. Design dependencies and data flow explicitly

Model research and computational pipelines as directed acyclic graphs where the work has acyclic dependencies. Each node must declare its inputs, outputs, dependencies, configuration, and relevant history or state requirements. Derive execution order from those dependencies instead of maintaining separate manual sequences.

Use state machines or explicit state transitions for execution lifecycles and other feedback processes. Do not force a live trading system's entire behavior into a DAG.

Separate modules by distinct reasons for change. Data ingestion, feature computation, model fitting, portfolio construction, execution, and evaluation need explicit ownership. Avoid classes or modules that combine these responsibilities merely because one workflow uses them together.

Keep domain computations independent of files, environment variables, wall clocks, and broker APIs where practical. Pass required inputs and state explicitly. Put external effects behind adapters and compose them at a defined application entry point.

Apply dependency inversion at meaningful external boundaries. Prefer composition to inheritance. Introduce factories, registries, and other extension mechanisms when real variation requires them. Use KISS, DRY, and Clean Code principles to reduce complexity without merging concepts that have different business meanings.

## 3. Preserve backtesting and live trading semantics

Backtesting and live trading must share core decision logic and domain contracts. Isolate data delivery, clock behavior, persistence, broker connectivity, and simulated execution behind explicit adapters.

Define the conditions under which the two modes must produce equivalent decisions. Model unavoidable differences such as latency, partial fills, slippage, rejected orders, and data revisions. Do not hide those differences inside an assumed equivalence.

Where both vectorized batch computation and incremental processing exist, define their shared state and history contract. Verify equivalent outputs on identical information and initial state. Compare exactly when the contract requires exactness. Otherwise, declare and justify numerical tolerances before evaluating results.

## 4. Make results reproducible and operations inspectable

Record the effective configuration, code revision, input dataset names and revision numbers, model artifacts, split definitions, and sources of randomness. Preserve the artifacts required to reproduce a reported result. Declare external or nondeterministic dependencies that prevent exact reproduction.

Give production inputs an owner, freshness limit, and explicit behavior when missing or stale. Define safe retry and restart behavior for workflows with side effects. Preserve enough state to distinguish a completed action from an interrupted attempt.

Every operational business capability must have a corresponding CLI workflow. Keep CLI commands thin and delegate business behavior to reusable application logic. Specify inputs, outputs, exit behavior, and side effects. Add commands with real use cases rather than creating an unused command for every internal function.

The CLI gives humans and agents a common way to run the system, inspect state, reproduce results, and demonstrate acceptance scenarios.

## 5. Organize the repository as durable project memory

Give each contract, rule, and decision one authoritative location. Store durable knowledge in version control and link to it from task briefs. Keep temporary task status separate from enduring domain knowledge.

Use the following as a target responsibility map. Adapt paths to the existing package structure. These directories describe intended ownership; this document does not instruct an agent to create empty packages or reorganize a working project without a concrete task.

```text
AGENTS.md                 Repository-wide invariants and working rules
schemas/                  Canonical data contracts and validation
  AGENTS.md               Local rules for contract changes
core/                     Domain computation and pipeline composition
  README.md               Responsibilities, data flow, dependency direction
  AGENTS.md               Local domain constraints
cli/                      Command entry points and application wiring
  AGENTS.md               Command contracts and verification rules
adapters/                 External data, storage, clocks, and brokers
docs/
  architecture.md         System topology and module boundaries
  decisions/              Accepted architectural decisions and rationale
  verification.md         Invariants and the checks that enforce them
  tasks/                  Task briefs, evidence, handoffs, and open questions
tests/                    Behavioral and contract verification
```

`schemas/` contains executable contracts for data shape, temporal availability, units, validation, and relevant compatibility rules. Keep domain objects immutable when their meaning requires it. Runtime immutability does not mean schemas can never change. Evolve contracts explicitly and migrate their consumers together.

`core/` contains actual domain logic and composition with explicit internal boundaries. Its documentation explains the structure that the code implements. The name `core` does not permit unrelated responsibilities or unrestricted imports.

`cli/` owns user interaction and command composition. `adapters/` owns external effects. Neither location should duplicate domain calculations.

`docs/architecture.md` explains cross-module relationships. Decision records explain why a consequential choice was made and identify superseded decisions. Task records contain current hypotheses, progress, evidence, and unresolved work. Do not turn task logs into competing architectural specifications.

When documentation, contracts, and behavior disagree, identify and resolve the discrepancy against the approved business requirement. An implementation defect does not redefine the intended contract.

## 6. Provide context at the scope where it applies

Keep repository-wide instructions short enough for every agent to use. Put local requirements near the code they govern. Local instructions may specialize broader rules, but must not silently weaken domain invariants.

For each important invariant, record its authoritative definition, affected components, verification command, and failure meaning. Reference that definition instead of copying its wording across multiple instruction files.

The coordinator must assemble a task's context from current repository artifacts. A worker must read the applicable instructions and contracts before implementation. If a task depends on missing business information, state the gap and continue only with independent work that does not assume an answer.

Before a handoff or context reset, record the current revision, completed changes, verification evidence, unresolved questions, and next action. A new agent should be able to resume from these records without reconstructing an entire conversation.

## 7. Define coordinator and worker responsibilities

The coordinator owns decomposition, dependency planning, task assignment, shared contract decisions, integration, and acceptance review. Workers own bounded changes and the evidence that those changes meet their assigned requirements.

Use one project coordinator per repository when projects need independent scope and execution. Cross-project observations should be reported to the responsible coordinator. They do not authorize edits in another repository.

Give each worker a task brief that contains:

- The business objective and representative domain scenarios.
- The relevant contracts, instructions, and architectural decisions.
- The permitted scope and ownership of files or modules.
- Dependencies on other tasks and shared interface decisions.
- Observable acceptance criteria and the commands that verify them.
- Any required memory updates and the expected handoff artifacts.

Separate concurrent writers through independent file ownership or isolated worktrees. Assign one owner to shared contracts and integration changes. Coordinate contract changes before dependent workers implement against incompatible assumptions.

Workers must not bypass checks, weaken validation, alter expected results to conceal a defect, or claim completion from an unexecuted test. They must disclose simplifications, unresolved failures, and deviations from the brief. Broader changes that affect another worker's contract must return to the coordinator for reconciliation.

The coordinator must inspect integration evidence. A worker's completion report is an input to review, not sufficient proof of correctness. Use the installed Herdr Projects capabilities and verify commands before relying on them. Do not assume that an example command from another version is available.

## 8. Evolve architecture through executable checks

Define a target architecture and move toward it in verifiable increments. Each increment must deliver an observable capability or enforce a required boundary. Avoid speculative abstractions and temporary compatibility layers without identified consumers and a removal plan.

Use architectural fitness functions, meaning executable checks of architectural properties. Relevant checks include permitted imports, dependency cycles, contract compatibility, point-in-time behavior, reproducibility, and equivalence across execution modes.

Document each check's scope and limitations. A passing dependency check does not establish quantitative correctness. A passing unit test does not demonstrate a working operational workflow.

Choose verification according to the change and its risk. Use behavioral tests, boundary cases, CLI acceptance scenarios, and relevant integration checks. Where appropriate, perturb input data after the decision time or inject failing inputs to prove that the checks detect the prohibited behavior. Change inputs, not code: mutation testing and adversarial review loops are not used.

## 9. Require evidence before declaring completion

For each task, the worker and coordinator must establish that:

- The requested business behavior works through its intended entry point.
- The applicable temporal, statistical, and numerical invariants hold.
- The change preserves declared dependency and ownership boundaries.
- Relevant checks ran against the delivered revision, with results recorded.
- Contract, architecture, and operating documentation match the delivered behavior.
- Remaining limitations, unverified behavior, and blocked dependencies are explicit.

Update durable project memory in the same change when implementation changes a contract, workflow, or architectural decision. Keep the evidence specific enough for another engineer or agent to repeat the verification.
