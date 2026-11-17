# Architecture and interface design

Read when defining ownership, splitting packages, changing an interface, or reviewing caller complexity. For the routing outline, return to [SKILL.md](../SKILL.md).

## Assign knowledge before directories

A module owns knowledge and the design decisions that depend on it. State what it encapsulates, what callers must understand, and which changes should remain local. Do not create a package merely because a step occurs at a different time. Historical querying and production replay can share a PIT capability because both depend on availability and revision semantics. [Review]

Keep these structures distinct:

| Structure | Responsibility |
|---|---|
| Computational DAG | Data and computation dependencies |
| Module map | Ownership of knowledge and public contracts |
| Execution state machine | Lifecycle transitions and feedback |
| Agent task DAG | Delivery dependencies and acceptance readiness |

Allow declared, acyclic public-interface dependencies. Reject private imports, cycles, and undeclared reads. Keep experiments and development tools outside shipped dependencies. A shared adapter does not authorize a node to bypass its declared inputs. [Check / Test]

Prefer composition. Establish a narrow interface for a real external boundary even with one implementation. Add factories, registries, or discovery only when concrete consumers need them. Keep mechanisms together if splitting would duplicate knowledge or make callers coordinate tightly related objects. Similar code with different business meaning is not automatically a DRY violation. [Review]

## Design deep capabilities

A deep module provides substantial capability behind an interface that is easy to use correctly. Evaluate the full caller contract, including ordering, preconditions, and failure handling, not just parameter count. [Review]

| Capability | Encapsulated mechanisms | Explicit caller decisions |
|---|---|---|
| PIT data access | Revision selection, visibility enforcement, physical reads, lineage | Cutoff, required data, freshness and revision policies |
| Stateful computation | Mathematics, warmup, sufficient state, compatibility | Inputs, semantic parameters, committed predecessor |
| Publication and recovery | Conditional commit, output/state visibility, duplicate attempts, reconciliation | Logical identity, destination, authorization, conflict policy |

Hide implementation mechanics without hiding policy that changes research results. Do not export uncertain mechanisms as a growing list of configuration switches. Keep CLI and adapters thin when they translate genuine boundaries; avoid pass-through layers that add no meaning. Drivers and runners compose capabilities and contain no business arithmetic. [Review]

Keep domain computations independent of files, environment variables, clocks, and broker APIs where practical. Pass inputs and state explicitly. External effects belong in adapters; application entry points compose them. [Check / Review]

## Compare designs through their callers

For consequential boundaries, sketch two structurally different interfaces. Compare representative caller code, semantic explicitness, change locality, failure handling, and plausible performance. Sketch enough to expose tradeoffs; two complete implementations or parallel agents are unnecessary. Record the choice and revisit it when repeated implementation friction contradicts the design. Routine edits do not need this ceremony. [Review]

Before implementation, explain behavior, preconditions, temporal and numerical semantics, side effects, and failures. Difficulty explaining a contract is design feedback. Keep necessary mathematical comments, units, tensor axes, degrees of freedom, and missing-value propagation. Prefer cohesive functions and shallow nesting; do not fragment mathematics into one-use wrappers to meet a line limit. [Review]

Until the project has a stable style, name a reference repository or module. Apply mechanical style checks where useful and retain review for mathematical meaning. [Check / Review]

Use change scenarios from the [playbook](scenarios.md) to inspect change amplification, cognitive load, and hidden dependencies. Ask whether a new Alpha reuses PIT, identity, recovery, and publication, and whether a provider change remains local. File counts alone do not measure design quality. [Review]

## Apply the layout without freezing it

Use `schemas/` for executable contracts, `core/` for domain computation and composition, `cli/` for commands, and `adapters/` for external effects. Define boundaries inside `core/`; it is not a home for unrelated code. Create packages with real content, public interfaces, and responsibility documentation. Do not scaffold empty packages for hypothetical needs. [Check / Review]

Separate required domain invariants from approved architecture and default style. Version and migrate contracts when necessary instead of preserving a mistaken first design. See [delivery](delivery-and-verification.md) for staged acceptance and [collaboration](agent-collaboration.md) for ownership and memory.

Design references: [deep modules](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch04.html), [information hiding](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch05.html), [pulling complexity downwards](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch08.html), [splitting and combining](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch09.html), and [design it twice](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch11.html). Quantitative applications here are project engineering judgments, not claims made by the book.
