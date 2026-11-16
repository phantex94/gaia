# Starting a new project: skeleton, efficiency, and incremental delivery

Use this guideline when starting a new project or a rewrite. It complements `quant-development-and-agent-collaboration.md` (called "the principles" below), which owns the domain invariants, dependency design, reproducibility, repository memory, and coordinator roles. This document does not restate those. It names the concrete artifacts to create on day zero, the budgets that keep computation efficient, and the ladder from a first working slice to full scope.

Three failure modes motivate it:
- growing feature by feature without contracts;
- stopping short of the real output channel;
- adding operations after go-live.

Each produces systems that work in tests but fail in production, or that end up wrapped around the systems they were meant to replace.

Vocabulary follows the principles' responsibility map: `schemas/` (contracts), `core/` (domain computation and composition), `cli/` (commands), `adapters/` (external effects).

## 1. Day-zero artifacts

### Before the first domain commit

| Artifact | Done when | Enforced by |
|---|---|---|
| A phase-zero contract document: layers, boundary contracts, conventions, layout, and the delivery ladder (section 7), approved by the human | Approved and linked from the repository instructions | Review |
| Layer table with downward-only imports, covering all shipped code including deployment and operations tooling | The import checker reports zero violations with an empty baseline | Check |
| Package shape: each package that exists has a public `api` module whose exports are its contract, and a README with responsibility, inputs and outputs, and failure reasons. No package is created before it has content | A check confirms every package has both | Check |
| Failure model: one business-refusal type that broad error handlers cannot swallow, with its own exit code. Programming errors use ordinary exceptions | A contract test shows a refusal passing through a broad handler | Test |
| Boundary contracts for every input and the output (principles §1, §4), including each input's owning job and freshness limit | Each rule has an accepting case and a refusing case | Test |
| One implementation point for each convention, such as units, rounding, calendar, and price basis | Each guard has a refusing test | Test |
| Parameter template (section 4) and strict loader | The loader refuses a missing field, an unknown field, and a wrong type | Test |
| CLI skeleton with the exit-code table (section 5) | `<tool> --help` runs and the table is in the CLI README | Review |
| Test layout, pre-push selection, CI, and a seeded synthetic reference dataset | Pre-push checks and CI pass | Check |
| Style checks for every rule that can be checked mechanically | The style checker reports zero findings | Check |

### Before go-live

| Artifact | Done when | Enforced by |
|---|---|---|
| Environment layout: production root, research root, secret location, and retention rules for run outputs | No production input resolves outside the production root. The release is built from a tag and excludes tests, docs, and dev tools | Check |
| The thin slice (section 7) writing to the real output channel in a test environment, with build, cutover, and rollback scripts | One rehearsed cutover and one rehearsed rollback | Rehearsal |
| Operations: stale required inputs block publishing; every external source declares its failure behaviour (retry, record a gap, or block); alerts reach a person | Each failure is rehearsed once, and a person confirms receiving the alert | Rehearsal |
| For a rewrite: a shadow-run period, written cutover criteria, and a retirement date for the old system | The criteria are met and recorded | Review |

## 2. Data flow

Principles §1–3 define the rules. These are the artifacts that carry them.

- **A node table.** One table lists each computation node with its inputs, kind (incremental, recursive, or full history), and lookback. Execution order and revision impact are computed from it.
- **One availability function.** Each dataset's availability rule lives in its contract in `schemas/`, and a single function applies it. Its result carries a marker, so a second application is refused.
- **Append-only revisions.** New data or corrections add a version. Compaction writes a new version and leaves the old one readable until nothing references it.
- **Pure nodes with a seed.** Batch and incremental runs call the same function. An incremental step passes a shorter window, plus a seed of the node's earlier output for recursive nodes.
- **Domains meet in the composition layer.** Domain modules do not import each other. The composition code passes one domain's output to another as an argument or a stored artifact.

## 3. Layers and composition

- The composition layer (drivers, runners) contains no arithmetic on business data. When a driver starts computing, move that code into the domain module that owns it.
- Validate once at the boundary, then trust the contract inside. Internal code carries no defensive type checks or silent defaults.
- Use one vocabulary for fields across modules, and represent missing values as missing, never as zero or a sentinel.
- Add a registry or extension point only where at least two implementations already exist.

## 4. Parameter template

- Each algorithm has one immutable parameter class next to it. Every field carries a one-line comment with its unit and meaning.
- Semantic parameters have no defaults. Engineering parameters such as chunk size or worker count may have defaults.
- Each purpose has one configuration file that lists every field, with comments. The loader validates it against the parameter classes, and fields that must agree across sections are checked together. An environment differs from the template only by an explicit overlay of the fields that differ, never by a copied file.
- The signature order is business inputs, then the parameter object, then keyword-only runtime switches. There are no pass-through keyword dictionaries, and multiple results come back as named, immutable records.
- Writes to production require literal values (production environment and publishing explicitly enabled). No force flag bypasses this.

## 5. Command-line interface

- One entry point shaped `<tool> <domain> <action>`. Schedulers and operators call only the CLI.
- Shared options are defined once as reusable option types and imported by every domain.
- Commands that write show their plan by default and act only with an explicit write flag.
- Each run writes to a new run directory named by section 6. A completed run is never overwritten. An interrupted run resumes in place according to its declared restart rule (principles §4).
- One documented exit-code table separates success, retryable failure, permanent failure, and business refusal.
- Development tools live outside the shipped package and are not CLI commands.

## 6. Identity and run records

- Identify runs, caches, and artifacts with readable parts: a name, a date, a sequence number, the input revision numbers, and the parameter-set name. Never use hashes or content checksums. Verify by comparing content directly.
- Every run directory holds its effective configuration, the code tag, the input revisions it read, and its own log. This record is what reproduction starts from.
- A cache is valid for the input revisions and parameter set named in its directory. Changing either produces a new cache name, not an in-place refresh.

## 7. Efficiency and memory

Correctness comes first. Every optimisation is then proven equal to the result before it, within that output's declared exactness class.

1. **Declare budgets.** For each stage, write down a time and peak-memory budget at target scale. A benchmark script records wall time and peak memory. Its results are kept with the run records, and a stated regression threshold fails the check.
2. **Make incremental cost scale with new data.** A daily step reads only its declared tail window, and its cost must not grow with history length. Test at several times the expected data size.
3. **Bound every batch.** Chunked computations, accelerator batches, worker pools, and caches each have a named size or byte limit. Peak memory does not grow with window length or universe size.
4. **Read only what is needed.** Scan columnar storage lazily, and push date and column filters down.
5. **Lay out storage for its readers.** Each dataset contract names its dominant read key, and storage is partitioned by it. Writes go to a temporary file followed by a rename.
6. **Profile before optimising.** Hot paths are vectorised with no per-row interpreter loops. Choose precision per array, and watch for hidden copies and reshapes.
7. **Shard where nothing crosses shards.** Parallelise along an axis with no cross-shard dependency, and prove that the merged result matches the single-process result. Measure before moving work to different hardware.
8. **State exactness per output class.** Integer outputs such as quantities, memberships, and dates match exactly. Floating outputs match bit for bit on the same machine and configuration, or within a declared tolerance across machines and thread counts. Pin threads and seeds where exactness is required.
9. **Do not build overhead you will later optimise away.** Checks that re-read or re-verify content at every step cost more than the computation they protect.

## 8. From MVP to full scope

Climb a ladder. Each rung has an exit criterion. The boundary contracts stay frozen while scope widens, and a written out-of-scope list says what is deliberately left out.

| Rung | Scope | Exit criterion |
|---|---|---|
| 1 | One instrument, one date, synthetic data, every stage end to end | The output passes the output contract |
| 2 | Small real sample, every stage, real write in a test environment | Matches independent references. Cutover and rollback rehearsed |
| 3 | Full universe | Within time and memory budgets |
| 4 | Full history | Batch equals incremental. Budgets hold at full size |
| 5 | Production | Before-go-live artifacts complete. Shadow period passed for a rewrite |

Testing rules for every rung:
- Expected values come from an independent source: hand calculation, a known formula, a second implementation, or a previous system frozen at a tag. They never come from the code under test.
- Contract tests cover boundary contracts and correctness rules. Module tests cover mechanics. Fixtures are small, read-only real samples with a record of their origin. Fakes stand in for external systems.
- Every rule has an accepting case and a refusing case. Include edge sizes: empty input, a single row, a single instrument.
- The seeded synthetic dataset covers the domain's hard cases, such as instrument lifecycle events, late or revised data, and calendar gaps. Changing its expected values requires a written reason and a version entry.
- Perturbing inputs after the decision time is a behavioural test and is required (principles §1). Mutating code to test the tests, and adversarial review loops, are not used.
- The fast suite has a time budget and runs before every push. Acceptance runs on the machine and data scale the system runs in production, and the run record names that machine.

## 9. Code style

Follow the human's standing rules:
- the Zen of Python;
- light comments: a header of at most five lines and one-line docstrings;
- no hashes in any form;
- short, shallow functions;
- exceptions caught only at real I/O boundaries, with the reason recovery is safe.

A greenfield repository names one reference repository or module as its style model until its own code can serve. Every rule says whether a checker or a reviewer enforces it. Rules left to review drift, so check them from day zero wherever possible.
