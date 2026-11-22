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

3. **Storage, Identity & Project-Specific Policies**
   - Research vs production data roots: `<paths>`
   - Retention, lineage, or project-specific hashing/validation rules: `<explicit rules>`

4. **External Channels & Compute Guardrails**
   - Local vs remote compute boundary: `<e.g., small unit tests locally; full runs on remote workstation>`
   - Broker/sink reconciliation limits, alert recipients, and live write guardrails: `<rules>`

5. **Harness & Workflow Bindings**
   - Active orchestration tools & branching/PR policy: `<e.g., subagent / workflow / swarm / board rules>`
