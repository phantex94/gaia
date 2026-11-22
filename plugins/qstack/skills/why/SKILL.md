---
name: why
description: Strict Round 1 + Round 2 intake (/qstack:why). Triages the request (fast path vs medium+ by semantic risk, not size), reads the repo and its design sources before asking, interviews the human in at most 2 batches plus 1 confirmation, closes every objection as answer or non-goal, and produces the confirmed intent YAML (envelope + body + roadmap) committed as docs/intent/<task>.yaml. Runs at a work board's coordinator before the task exists, or directly in a repo. Never writes business code.
---

# /qstack:why — Strict Round 1 (Triage & Interview) & Round 2 (Interrogate & Confirm)

**HARD RED LINE: DO NOT WRITE ANY CONCRETE BUSINESS LOGIC IN THIS MODE.**

You are the **intake owner** (`../../references/00-protocol.md` §1): either a work board's coordinator before the task is added (you have no worktree: write no repo files, hand the confirmed YAML over in the task brief), or an agent working directly in the repo (you write the intent file yourself).

## Round 1: Triage, Read-Before-Asking & Interview

1. **Load**: `../../references/principles.md` and `../../references/02-anti-ambiguity-yaml.md` §1–3.
2. **Triage** (`02` §1 step 1): medium+ on an unconfirmed Red item, a public contract change, a production/authority boundary, a new component, or cross-package work—plus the repo Hook's own triggers.
   - **Fast Path**: brief plan -> execute -> runnable test. No intent file. Done.
   - **Ops routing**: continue the interview below; a request that crosses the production/authority boundary (triage rule 3), or a read-only audit of a production system or shared host, routes to `../mode/playbooks/ops-change.md` with `../../templates/ops-change.yaml` instead of the code skeleton; a non-production code change keeps its own playbook even if it ships through a release. The ops template's body sits inside the same envelope.
3. **Read-Before-Asking** (read-only, about 5 minutes; 1 read-only `subagent` for a large scan): `AGENTS.md` + Project Policy Hook, earlier intent files, touched `README.md`/`api.py`, `reference_*` inputs, and every design source the Hook names. Record what you read in `sources`. Ask only what they leave open; if a named source cannot be read, ask for it. Do not ask for host inventory—the builder measures it.
4. **Interview** (`AskUserQuestion` when available, else numbered choices): ≤ 4 questions per batch, 2–4 options, **recommended option first**, a "make it a non-goal" option where meaningful. Priority: ① Red items that change the output, ② production/authority boundary, ③ scope & non-goals (Business Type, Engineering Type, Core Mission), ④ acceptance oracle. **At most 2 batches.**

## Round 2: Draft, Interrogate & Confirm (Gate 1)

5. **Draft** from `../../templates/intent-envelope.yaml` wrapping ONLY the matching body (`greenfield.yaml`, `brownfield-add.yaml`, `brownfield-improve.yaml`, `brownfield-evolve.yaml`, or `ops-change.yaml` for ops routing), pre-filled with observed facts and the answers. Keys English; values in the repo's docs language.
6. **Interrogate** (`/qstack:interrogate` lenses): every finding becomes an objection `O<n>`; ask the open ones within the 2-batch budget.
7. **Confirm** (the last question call): show a short intent summary, the outcome-level `roadmap`, and every objection closed as `non_goal`. Options: "Confirm" / "Change …". Each objection must end as `answer` or `non_goal`—only the human closes one. No further rounds.
8. **Hand off** with `status: confirmed`:
   - **Board coordinator**: put the YAML in the task brief under `## Intent (confirmed)` and add the task with the host plan gate on.
   - **Direct**: write `<intent folder>/<task>.yaml` (Hook folder, default `docs/intent/`) and commit it with the work.

## Exit & Handoff to Round 3
- **Next step**: the builder runs **`/qstack:architect`** (or the ops playbook) as its plan—Gate 1B—then commits the intent file unchanged with `status: building`.
- **Harness rule**: Run **Direct** (at most 1 read-only `subagent`). Never launch `swarm` or `goal` in Rounds 1–2.
