---
name: setup
description: Initialize qstack in a target quant repository (/qstack:setup). Scans repo layout and reference docs, creates or updates the Project Policy Hook in AGENTS.md, and checks layer/spec scaffolding without adding repo-specific clutter to qstack itself.
---

# /qstack:setup — Repository Onboarding & Project Policy Hook

## Steps
1. Read `../../references/06-collaboration-and-hook.md` and `../../templates/project-policy-hook.md`.
2. Inspect the target repository root (`AGENTS.md`, `CLAUDE.md`, `pyproject.toml`, existing package `README.md`, layer checker scripts, and CLI entrypoint). If a large `reference_architecture` path is supplied, summarize its package conventions first (use a read-only `subagent` if >15 files).
3. Draft a concise, repo-specific **Project Policy Hook** pre-filled with real observed facts (language/engines, allowed-import table & checker command, CLI command shape, research vs production roots, compute/channel guardrails, harness rules).
4. **Return the drafted Hook to the human for confirmation** before writing it into the repository's `AGENTS.md` or `PROJECT_POLICY.md`.
5. Ensure `.qstack/` is listed in `.gitignore` if the human adopts the gitignored working scaffold convention.

## Guardrails
- Keep `qstack` itself 100% repo-agnostic; all project quirks belong strictly in the target repo's Hook.
- A Hook may tighten rules or bind paths/tools, never silently weaken `Zero-Lookahead`, `Batch-Equals-Step`, `Fail-Closed-Refusal`, or Gate 1.
- **Next step**: Hand off to `/qstack:why` or `/qstack:mode` once the Hook is confirmed.
