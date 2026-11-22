# compute-graph

A view of a task's compute graph: the repo's whole graph in qstack's stages, with the task's slice highlighted (the nodes, edges and CLIs it adds, rewires, polishes or removes). Rendering only: it draws two committed files and infers nothing.

- **Pane** beside the chat: `/graph <target>`. It refreshes every 5 s and after each edit.
- **Page**: `/compute-graph:graph-page <target>` publishes one private artifact per task, readable on a phone.

## Install (any machine)

```bash
claude plugin marketplace add phantex94/gaia     # or a local checkout: claude plugin marketplace add /path/to/gaia
claude plugin install compute-graph@qstack
```

Then `/reload-plugins` (or a new session). Needs `uv` on the PATH (it fetches PyYAML for the script); without `uv`, `python3` with PyYAML installed works too. Update with `claude plugin marketplace update qstack`, `claude plugin update compute-graph@qstack`, then `/reload-plugins`.

## Targets

| Target | Reads |
| :--- | :--- |
| `AMC-56`, `amc/56`, `alpha_mining_cta/56` | the herdr board's task: its worktree, else its branch, else the repo checkout |
| `/path/to/repo --task endless-12` | a repo folder (any repo, on the board or not) and one task name |
| `sample` | this plugin's sample (`sample/`, task `smp-1`) |
| nothing | the current folder; a board worktree's top folder picks its own task |

Board lookups read `~/.herdr-projects/data` (`repo-keys.json`, `repos.json`, `tasks/<repo>/<n>/task.json`) and never write there; set `HERDR_PROJECTS_DATA` to use another folder. These are the board's own files, not a published interface.

## The two files it draws

1. `<intent folder>/graph.yaml` (default `docs/intent/`; the repo's AGENTS.md Hook line `Intent folder:` can rename it): nodes with stage (`data | factor | model | portfolio | execution | sim`), axis (`ts | cs`), I/O, explicit edges, and CLI <-> sub-path. Schema: qstack `templates/graph.yaml`.
2. `<intent folder>/<task>.yaml`: the task's intent; its `graph_slice` section lists node, edge and CLI ids with a mode. Schema: qstack `templates/intent-envelope.yaml`.

No intent file, no `graph_slice`, or two intent files for one task: the view shows the repo graph and says the task has no slice. A slice id missing in `graph.yaml` is shown and reported, never dropped.

## Check a graph by hand

```bash
uv run -q --script plugins/compute-graph/scripts/compute_graph.py check AMC-56     # exit 1 on errors
uv run -q --script plugins/compute-graph/scripts/compute_graph.py json /path/to/repo --task smp-1
```

## Develop

```bash
claude plugin validate plugins/compute-graph
claude plugin test plugins/compute-graph
cd plugins/compute-graph/scripts && uv run -q --no-project --with pyyaml python -m unittest test_compute_graph
```
