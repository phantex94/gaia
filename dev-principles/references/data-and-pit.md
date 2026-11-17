# Data and point-in-time contracts

Read for ingestion, alignment, historical queries, revisions, universe membership, and evaluation splits. This document owns temporal visibility and data semantics. Return to the [outline](../SKILL.md).

## Define what was knowable

Every decision uses only information available at its cutoff. Distinguish event time from availability time. Specify time zones, calendars, publication delays, source revisions, and same-timestamp ordering. Apply the contract to raw data, universe membership, corporate actions, features, preprocessing, models, portfolio construction, and execution. Models cannot participate before their inputs and training process could have produced them. Event-driven processing alone does not establish PIT correctness. [Check / Test]

For each input, declare schema, row key, units, temporal coverage, availability rule, missing-value semantics, owner job, freshness limit, and failure behavior. Missing or ambiguous required temporal information must fail closed. Stale production inputs block publication unless an explicit authorized degradation policy applies. An external source declares whether failure means retry, record a gap, or refuse. [Check / Test]

Normalize and mark availability once at an authoritative boundary. Refuse repeated marking or lag application. Distinguish normalization from repeatable as-of queries at different cutoffs: a marker does not prove that every row is visible at every cutoff. Record the query cutoff, availability policy, and selected revisions. A scattered `shift(1)` or a shift flag does not replace the contract. [Check / Test]

Expose this through the PIT capability defined in [architecture](architecture.md). Strategies declare policy and requested inputs; they do not reimplement revision selection or visibility filtering.

## Revise without rewriting history

New observations, corrections, and compaction create new immutable revisions. Referenced old revisions remain readable. Declare revision propagation per node: finite-window invalidation, recursive replay, and model refitting have different recomputation scopes. Lookback alone cannot establish the affected range. [Check / Test]

Keep As-Traded history immutable. Reproduce the originally published signal from its original cutoff and pinned inputs, model, code, configuration, and predecessor state. Late-data and corrected recomputations use a new `vintage`; they never overwrite the original ledger. See [identity](configuration-and-identity.md) and [state](computation-and-state.md) for lineage and recovery requirements. [Check / Test]

The project's dataset-hashing prohibition and revision-based validation are defined in [configuration and identity](configuration-and-identity.md). Do not introduce a separate content-fingerprinting scheme here.

## Keep evaluation independent

Declare temporal splits and their purpose before model selection. Fit learned preprocessing and model parameters only on the permitted training data for each fold. Validation can guide selection within the stated protocol; final out-of-sample evaluation remains isolated. Account for overlapping labels and forward return horizons. Use purging or embargo where dependencies require them. [Test / Review]

Record split boundaries, fitting windows, and the selection protocol with each result. An evaluated holdout cannot silently become an untouched test set. Reusing a final set changes its status and must be disclosed. [Check / Review]

## Preserve numerical and missing-value meaning

Define units, currencies, price and quantity conventions, tick and lot sizes, numeric representations, and rounding rules at actual interfaces. Put each conversion in one implementation location and reject invalid units or repeated normalization. Missing values remain missing, not zero or sentinels. Do not invent defaults for missing specifications, invalid values, or stale inputs. [Check / Test]

Parse external data strictly once; avoid repeated internal type parsing. Still check nonfinite results, infeasible solutions, and invalid transitions where computation creates them. Parameters and numerical equivalence are owned by [configuration](configuration-and-identity.md) and [computation](computation-and-state.md).

## Demonstrate the contract

Require future-input perturbation tests: changing information available only after a cutoff must not change the earlier decision. Cover late publication, revised observations, historical universe changes, calendar boundaries, malformed inputs, repeated marking, and stale required inputs. Each correctness rule needs accepting and refusing cases. Use independent expected values; do not reuse disputed alignment logic in the reference. [Test]

For a concrete revision or provider change, follow the [scenario playbook](scenarios.md). Production-scale evidence belongs to the [delivery guide](delivery-and-verification.md), not to a claim that this specification itself proves correctness.
