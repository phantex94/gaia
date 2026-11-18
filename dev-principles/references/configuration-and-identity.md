# Configuration, identity, and reproducibility

Read for parameters, run records, artifact keys, lineage, caches, and data validation. This document owns identity and the no-hash policy. Return to the [outline](../SKILL.md).

## Parse configuration once

Place an immutable parameter class next to its algorithm. Explain every field's meaning and unit. Pydantic, frozen dataclasses, or equivalent typed contracts may implement the boundary. Strict loaders reject missing fields, unknown fields, and incorrect types where coercion would conceal an error. Internal code trusts parsed types while still checking invariants that computation can invalidate. [Check / Test]

Semantic parameters have no defaults. Engineering controls such as chunk size or worker count may have defaults; record effective values when they affect numerical results. Keep one complete commented template per purpose, validate cross-section agreement, and express environment differences through explicit overlays, not copied files. [Check / Test]

Order function arguments as business inputs, the parameter object, then keyword-only runtime controls. Do not pass through `**kwargs`; return named immutable records for multiple results. Each option needs a real business choice or justified operational purpose. Keep storage and recovery mechanisms inside their modules instead of exporting unnecessary switches. [Check / Review]

## Name logical results separately from attempts

Use readable names, dates, sequence numbers, immutable revision IDs, and parameter-set names. Never use a hash or a hash-like ID, including a Git commit ID, as a file, directory, branch, tag, run, or key name. A physical attempt and a logical publication are different identities. [Check]

Identify a logical output snapshot by `(node_id, decision_time, vintage, param_set@seq)`: readable business fields only. Pin implementation, schema, input revisions, model, and initial state in its lineage. Explicitly version the identity when lineage changes. Declare unique row keys, including instrument identity for panel rows. A retry cannot create a new logical result merely by using a new attempt directory. [Check / Test]

[Publication and recovery](publication-and-recovery.md) owns uniqueness and same-key conflict enforcement. [Data and PIT](data-and-pit.md) owns visibility and As-Traded versus revised vintages.

## Use no hashes

No hashes in any form is the default for projects that follow this library. It covers content hashes, checksums, fingerprints, hash manifests, hash-based keys, and hash-like names. Third-party software downloads that verify their own integrity are outside this rule. [Check / Review]

- Name each effective configuration as a readable `param_set@seq`, for example `momentum_daily@3`. The parameter-set name is the business choice; `seq` increases by one for every change of any effective value. The same `param_set@seq` always means the same effective values. [Check / Test]
- Register each `param_set@seq` once with its full effective values. Registering an existing `param_set@seq` with different values is a business refusal, found by comparing the values field by field; registering identical values again returns the existing entry. Never derive the name from the content. [Check / Test]
- Never hash or checksum raw or derived datasets, rows, partition contents, or configuration. This includes market data, financial data, features, Alpha outputs, and data embedded in configuration. [Check / Review]
- Identify data and state snapshots through explicit immutable revision IDs, partition manifests listing readable partition names, schema versions, and source/predecessor references. A Git commit ID may be recorded as a value in lineage; it is never used as a name. [Check]

Validate datasets through schema contracts, row-key uniqueness, counts, time coverage, lineage, and targeted acceptance-time content comparisons. Compare content directly when equality matters. These checks do not establish cryptographic content integrity. Do not add full-history byte comparisons or repeated full rereads to every run. [Check / Test]

## Preserve evidence and cache validity

A run record includes the effective configuration and its `param_set@seq`, the exact code revision recorded as a value and its tag when present, schema and implementation versions, input dataset and partition revisions, model and predecessor-state IDs, split definitions, random sources, numerical environment, and append-only attempt logs. The record must select the original inputs and state, not just describe their names. Disclose external or nondeterministic dependencies that prevent exact reproduction. [Check / Review]

Reuse a cache only when input, implementation, schema, effective configuration, model, and initial-state identities match. Any changed dependency creates a new cache version with a readable sequence number. Never refresh a published version in place. A parameter-set name without its `seq` is not a cache key. [Check / Test]

Declare retention and reference rules when run roots are created. Preserve referenced inputs, state, and model artifacts needed for reported results; cleanup must not remove them while referenced. Separate production roots, research outputs, and secrets. Production inputs resolve only within approved roots. Keep a checked inventory of every production read, including tokens, credentials files, and vendor mirrors; a read outside the approved roots fails the check until it is moved or explicitly approved. [Check / Review]

For stale caches, late revisions, and repeat runs, use the [scenario playbook](scenarios.md). [Delivery](delivery-and-verification.md) defines acceptance evidence; knowledge-library checks are not a substitute for implementing these contracts.
