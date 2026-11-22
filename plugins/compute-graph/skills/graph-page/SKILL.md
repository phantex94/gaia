---
name: graph-page
description: Publish one private, phone-friendly page (artifact) per task showing the repo's compute graph (docs/intent/graph.yaml) with the task's graph_slice highlighted. Use when the human asks for the compute-graph page of a task, e.g. "/compute-graph:graph-page AMC-56", or of a repo folder.
---

# /compute-graph:graph-page — one private page per task

The page is rendering only: it draws `graph.yaml` and the task intent's `graph_slice` as committed, and says so when there is no slice. Never add, guess or edit nodes, edges or slices for the page.

## Steps
1. **Target**: the argument as given: a board id (`AMC-56`), a repo folder plus `--task <name>`, or `sample` (this plugin's sample repo, task `smp-1`). No argument: the current folder.
2. **Generate** (the plugin root is two folders above this skill's base directory):
   `uv run -q --script <plugin root>/scripts/compute_graph.py html <target> -o "$TMPDIR/graph-<task or repo>.html"`
   (no `uv`: `python3` with PyYAML runs the same script). Exit 2 means the target did not resolve: show the message and stop.
3. **Find the page**: `Artifact` `action: "list"` and look for the title `Compute graph <KEY-n>` (the file's `<title>`). Found: read it once with `action: "read"`, then publish with its `url` so the same link updates. Not found: publish new, `icon: "graph"`.
4. **Publish** the generated file with the `Artifact` tool. The file already holds the page contract (title, viewport-fit meta, tokens for light and dark, phone layout below 720px); do not hand-edit it, and do not load another design pass for it.
5. **Reply** with the link and one line: repo, task, slice state (found / none / ambiguous), and any check errors the page lists.
