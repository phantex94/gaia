# Configuration, identity, and reproducibility

Read for parameters, run records, artifact keys, lineage, caches, and data validation. This document owns identity and the project-specific hashing policy. Return to the [outline](../SKILL.md).

## Parse configuration once

Place an immutable parameter class next to its algorithm. Explain every field's meaning and unit. Pydantic, frozen dataclasses, or equivalent typed contracts may implement the boundary. Strict loaders reject missing fields, unknown fields, and incorrect types where coercion would conceal an error. Internal code trusts parsed types while still checking invariants that computation can invalidate. [Check / Test]

Semantic parameters have no defaults. Engineering controls such as chunk size or worker count may have defaults; record effective values when they affect numerical results. Keep one complete commented template per purpose, validate cross-section agreement, and express environment differences through explicit overlays, not copied files. [Check / Test]

Order function arguments as business inputs, the parameter object, then keyword-only runtime controls. Do not pass through `**kwargs`; return named immutable records for multiple results. Each option needs a real business choice or justified operational purpose. Keep storage and recovery mechanisms inside their modules instead of exporting unnecessary switches. [Check / Review]

## Name logical results separately from attempts

Use readable names, dates, sequence numbers, immutable revision IDs, and parameter-set names. Avoid bare-hash directory names. A physical attempt and a logical publication are different identities. [Check]

Identify a logical output snapshot by `(node_id, decision_time, vintage, config_digest)`. Pin implementation, schema, input revisions, model, and initial state in its lineage. Explicitly version the identity when lineage changes. Declare unique row keys, including instrument identity for panel rows. A retry cannot create a new logical result merely by using a new attempt directory. [Check / Test]

[Publication and recovery](publication-and-recovery.md) owns uniqueness and same-key conflict enforcement. [Data and PIT](data-and-pit.md) owns visibility and As-Traded versus revised vintages.

## Follow the hashing boundary

The dataset-hashing prohibition is a project requirement, not a universal software-design principle. [Check / Review]

- Permit a `config_digest` only for canonically serialized effective parameters and configuration. Declare field ordering, numeric representation, serialization, and hash algorithm. Equivalent configurations produce the same digest; changed values change identity. [Check / Test]
- Never hash or checksum raw or derived datasets, rows, or partition contents. This includes market data, financial data, features, Alpha outputs, and dataset contents embedded in configuration. Do not disguise data as configuration to hash it. [Check / Review]
- Identify data and state snapshots through explicit immutable revision IDs, partition manifests, schema versions, and source/predecessor references. Dataset references in configuration may be revision IDs. Recording Git commit IDs is allowed. [Check]

Validate datasets through schema contracts, row-key uniqueness, counts, time coverage, lineage, and targeted acceptance-time content comparisons. These checks do not establish cryptographic content integrity. Do not add full-history byte comparisons, repeated full rereads, or fingerprints to every run. [Check / Test]

## Preserve evidence and cache validity

A run record includes effective configuration and its permitted digest, exact code revision and tag when present, schema and implementation versions, input dataset and partition revisions, model and predecessor-state IDs, split definitions, random sources, numerical environment, and append-only attempt logs. The record must select the original inputs and state, not just describe their names. Disclose external or nondeterministic dependencies that prevent exact reproduction. [Check / Review]

Reuse a cache only when input, implementation, schema, effective configuration, model, and initial-state identities match. Any changed dependency creates a new cache version. Never refresh a published version in place. A parameter-set name alone is not a cache key. [Check / Test]

Declare retention and reference rules when run roots are created. Preserve referenced inputs, state, and model artifacts needed for reported results; cleanup must not remove them while referenced. Separate production roots, research outputs, and secrets. Production inputs resolve only within approved roots. [Check / Review]

For stale caches, late revisions, and repeat runs, use the [scenario playbook](scenarios.md). [Delivery](delivery-and-verification.md) defines acceptance evidence; knowledge-library checks are not a substitute for implementing these contracts.
