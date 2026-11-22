# Project Policy Hook (Paste into target repository's root AGENTS.md / PROJECT_POLICY.md)
# Extends qstack with repo-specific facts without weakening core quant invariants or Gate 1.

## Project Policy Hook (qstack)

1. **Stack & Reference Style**
   - Language & core engines: `<e.g., Python 3.12+, Polars, PyTorch float64, Typer>`
   - Reference exemplar modules to imitate: `<paths>`
   - Forbidden dependencies: `<e.g., no pandas in production packages>`

2. **Package Layers & CLI**
   - Allowed-import table & layer checker command: `<e.g., python -m dev.layers check>`
   - CLI entry command: `<e.g., uv run <tool> <domain> <action>>`

3. **Intent & Design Sources**
   - Intent folder: `<default docs/intent/>`; file name: `<board key + slug | yyyy-mm-dd-slug>.yaml`
   - Design sources read before asking, and which wins on conflict: `<e.g., ADRs over design pages; contract crate is the only definition source>`
   - How Round 3 is expressed here: `<existing package layout | delta on named design/component pages | contract type first, then codegen>`
   - Repo-specific medium+ triggers: `<e.g., frozen contract change, version bump, live root>`
   - Docs language for intent values: `<e.g., English | Chinese>` (keys stay English)

4. **Storage, Identity & Project-Specific Policies**
   - Research vs production data roots: `<paths>`
   - Identity & versioning rules: `<e.g., readable integer versions, content compared directly; any hashes this repo needs and why>`
   - Retention & lineage rules: `<explicit rules>`

5. **Ops Static Facts** (read by `ops-change.md`; a missing key is asked, never guessed)
   - `ops.hosts`: `<production hosts; compute host for long jobs>`
   - `ops.scheduler`: `<where the job list lives, or none>`
   - `ops.live_roots`: `<live roots>`
   - `ops.production_location_rule`: `<where production may and may not live>`
   - `ops.windows`: `<required and forbidden windows + time zone>`
   - `ops.alerts`: `<channel; recipient; block-or-warn policy; how to send a test>`
   - `ops.owners`: `<data, consumer, ops and release owners; who can rerun each upstream>`
   - `ops.standing_authority`: `<what may run without a fresh OK, e.g. incident containment>`
   - `ops.privileged_steps`: `<sudo or another owner's steps, and who runs them>`
   - `ops.scan_budget`: `<default time and IO budget for audits>`

6. **External Channels & Compute Guardrails**
   - Local vs remote compute boundary: `<e.g., small unit tests locally; full runs on remote workstation>`
   - Broker/sink reconciliation limits and live write guardrails: `<rules>`

7. **Harness & Workflow Bindings**
   - Active orchestration tools & branching/PR policy: `<e.g., subagent / workflow / swarm / board rules>`
   - Check command the host runs (Gate 2): `<e.g., repo test + lint command>`
