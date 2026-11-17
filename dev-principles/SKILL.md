---
name: dev-principles
description: Design, implement, and review quantitative trading software with explicit PIT, numerical, state, and publication contracts. Use for quantitative platform architecture, reusable research components, production workflows, and coordinator task design.
---

# Quant development brain

Use this entry point first, then read only the references relevant to the current task. English is authoritative. The [Chinese review guide](review.zh-CN.md) helps the human inspect decisions; it is not a parallel specification.

## Core commitments

1. Use only information available at the decision cutoff. Isolate training, validation, and final evaluation.
2. Make mathematical meaning explicit: units, axes, missing values, numerical tolerances, and downstream decision effects.
3. Own knowledge in modules. Build deep capabilities that hide mechanisms while keeping business policy explicit.
4. Share mathematical and state contracts across Batch, Backfill, and Step. Preserve sufficient state and immutable As-Traded history.
5. Commit outputs and state consistently. Reconcile retries and remote effects; prevent duplicate rows, weights, and publications.
6. Reproduce results from pinned inputs, code, configuration, model, and state. Follow the project's explicit dataset-hashing prohibition.
7. Deliver a small, meaningful end-to-end capability before expanding scale. Verify the final integrated revision.
8. Give each agent a bounded capability, the relevant contracts, and observable acceptance criteria. Count coordination costs before delegating.

These commitments guide routing; the linked references own their detailed rules. Correctness invariants are mandatory. Architecture constraints express the approved design. Directory names, function lengths, and patterns are defaults that may change when doing so reduces complexity without weakening correctness.

## Read by task

| Current work | Read next |
|---|---|
| Define or revise module boundaries and public interfaces | [Architecture and interface design](references/architecture.md) |
| Ingest, align, revise, or query historical data; define evaluation splits | [Data and PIT contracts](references/data-and-pit.md) |
| Implement an Alpha, rolling operator, model update, or execution mode | [Computation and state](references/computation-and-state.md) |
| Publish, recover, reconcile, or prevent duplicate effects | [Publication and recovery](references/publication-and-recovery.md) |
| Define parameters, artifact identity, lineage, or caches | [Configuration and identity](references/configuration-and-identity.md) |
| Start a project, increase scale, benchmark, test, or prepare go-live | [Delivery and verification](references/delivery-and-verification.md) |
| Assign work, hand off context, integrate workers, or maintain project memory | [Coordinator collaboration](references/agent-collaboration.md) |
| Handle a concrete change or incident | [Scenario playbook](references/scenarios.md), then its linked contract owner |

For a new project, read architecture and delivery first, then follow their links for the first capability. For a narrow edit, open its owning contract and relevant scenario. Do not load the whole library by default.

## Apply the knowledge

Identify the business behavior, its contract owner, relevant invariants, and acceptance evidence. For a consequential boundary, compare two interface sketches with caller examples; routine edits need no design ceremony. Select direct or coordinated execution according to the collaboration guide. Implement within scope and verify the integrated behavior. Record unresolved assumptions and update only the authoritative reference when a rule changes.

Use **Check** for automated structural or policy checks, **Test** for executable behavior or performance checks, and **Review** for engineering judgment. Record the applicable commands, environment, revision, and results in the target project's `docs/verification.md`. Requirements in this library are not evidence that a platform already implements them.

Run `python3 scripts/check_links.py` from this directory after editing the knowledge structure. This checks navigation, not quantitative software correctness.
