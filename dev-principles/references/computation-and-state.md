# Computation, numerical meaning, and state

Read when implementing an Alpha, rolling calculation, model update, or Batch/Backfill/Step driver. This document owns computational semantics and state equivalence. Return to the [outline](../SKILL.md).

## Declare the computational node

Record inputs, outputs, dependencies, parameters, computation kind (incremental, recursive, or full history), lookback, sufficient state, and spatial coupling. Declare `per-instrument` or `cross-sectional`, grouping keys, tensor axes, units, degrees of freedom, and missing-value propagation as applicable. Derive execution order from the computational DAG. Execution feedback belongs in a state machine, not an artificial DAG. [Check / Review]

A node reads only its declared inputs. A shared storage adapter cannot bypass dependency declarations. Compose domains through approved public interfaces. Keep arithmetic in its owning domain module and external effects in adapters. See [architecture](architecture.md). [Check / Test]

## Separate business output from sufficient state

Define a stateful calculation as:

```text
(inputs_t, state_{t-1}, params) -> (outputs_t, state_t)
```

For an Alpha node, the business output is `alpha_t`. The next state may require counts, moments, Gram matrices, or window buffers. Alpha values or coefficients alone may not be sufficient to continue the computation. State has a version, lineage, and explicit compatibility contract. [Check / Test]

Batch, Backfill, and Step share mathematical, history, and state contracts, not necessarily one function implementation. Permit optimized implementations when they satisfy the declared equivalence checks. Identical information, warmup, parameters, and initial state must describe the same computation. [Test / Review]

Load the committed `state_{t-1}` read-only. Rerunning time `t` always starts from the same predecessor, never an already advanced `state_t` or an unconfirmed attempt. Stage output and state together and expose them through one atomic committed manifest. Do not mutate committed state in place. [Check / Test]

[Publication and recovery](publication-and-recovery.md) owns the commit protocol. [Data and PIT](data-and-pit.md) owns late revisions and recomputation scope. A recursive correction may require replay; changing only a recent window is not automatically sufficient.

## Make randomness independent of execution order

Derive streams through a declared stable method from `(seed, node_id, decision_time)`. Use stable instrument or purpose subkeys, or canonical item ordering, where required. Do not select random draws through a sequential global RNG, process-dependent hashing, worker order, chunk boundaries, or earlier attempts. These are control keys, not dataset content hashes. Record the derivation and seed. [Check / Test]

## Distinguish repetition, equivalence, and decisions

Require deterministic reruns of the same implementation with pinned inputs, state, and numerical environment. Compare integer and discrete outputs exactly. For different implementations, machines, or thread counts, declare justified floating-point tolerances before measuring. Require bitwise equality where the contract demands it; pin threads and seeds accordingly. [Test / Review]

Test ranking, thresholds, constraints, rounding, and order consequences separately. Small numeric error does not prove equal decisions. Numerical tolerance never authorizes replacing a conflicting same-key committed artifact. Compare state as well as business outputs. [Test]

Verify full Batch against segmented Batch followed by Step, Backfill, overlapping intervals, and repeated days. Include warmup, missing observations, recursive state, and lifecycle transitions. [Delivery](delivery-and-verification.md) owns the integrated acceptance process; the [playbook](scenarios.md) gives practical change and recovery scenarios.

## Respect coupling and cost

Do not blindly shard cross-sectional operators by instrument. Declare valid groups, cross-shard reductions, and ordering requirements. Prove merged results against an unsharded reference. [Check / Test]

Incremental work reads new data, its declared tail, and sufficient state rather than rescanning growing history. Full-history fitting declares its complexity, frequency, and budget. Bound temporary working sets, but express persistent rolling state in lookback, universe, and dimensions; it is not generally constant. Use the performance budgets in [delivery](delivery-and-verification.md). [Test / Review]

Keep comments sufficient to explain the mathematics. Short functions and one-line docstrings are not correctness conditions. Explain a nonobvious algorithm before implementation and use the explanation to review its interface. See [useful comments](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch13.html) and [writing comments first](https://cactus-proj.github.io/A-Philosophy-of-Software-Design-zh/ch15.html).
