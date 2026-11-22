# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Render a repo's compute graph (graph.yaml) with one task's graph_slice highlighted; nothing is inferred."""

import argparse
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

STAGES = ["data", "factor", "model", "portfolio", "execution", "sim"]
STAGE_TITLES = {
    "data": "Data",
    "factor": "Factor",
    "model": "Signal / Model",
    "portfolio": "Portfolio",
    "execution": "Execution",
    "sim": "Sim / Risk",
}
AXES = ["ts", "cs"]
NODE_MODES = ["add", "rewire", "polish"]
EDGE_MODES = ["add", "rewire", "remove"]
CLI_MODES = ["add", "rewire", "polish", "remove"]
DEFAULT_INTENT_FOLDER = "docs/intent"
GRAPH_FILE = "graph.yaml"
BOARD_DATA = Path(os.environ.get("HERDR_PROJECTS_DATA", Path.home() / ".herdr-projects" / "data"))
BOARD_ID = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*?)[-/](\d+)$")
SAMPLE = Path(__file__).resolve().parent.parent / "sample"
SAMPLE_TASK = "smp-1"
HOOK_INTENT_FOLDER = re.compile(r"Intent folder:\s*`([^`<>]+)`")

NO_GRAPH = "This repo has no {path} yet. Bootstrap it: /qstack:how prints a draft, and the bootstrap task commits it."
NO_TASK = "No task picked: showing the repo graph only."
NO_INTENT = "{task}: no graph slice (no intent file in {folder})."
NO_SLICE = "{task}: no graph slice (the intent has no graph_slice section)."
MANY_INTENTS = "{task}: no graph slice (several intent files match: {names}). Keep one."


class Refusal(Exception):
    """A target that cannot be resolved; the message says why."""


class Source:
    """Reads repo files from a folder (worktree or checkout) or from a git branch."""

    def __init__(self, kind, root, branch=""):
        self.kind, self.root, self.branch = kind, Path(root), branch

    def label(self):
        return f"branch {self.branch}" if self.kind == "branch" else f"{self.kind} {self.root.name}"

    def read(self, rel):
        if self.kind == "branch":
            done = git(self.root, "show", f"{self.branch}:{rel}")
            return done.stdout if done.returncode == 0 else None
        path = self.root / rel
        return path.read_text() if path.is_file() else None

    def names(self, folder):
        if self.kind == "branch":
            done = git(self.root, "ls-tree", "--name-only", f"{self.branch}:{folder}")
            return done.stdout.split() if done.returncode == 0 else []
        path = self.root / folder
        return sorted(p.name for p in path.iterdir()) if path.is_dir() else []


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def load_json(path):
    return json.loads(path.read_text()) if path.is_file() else {}


def board_maps():
    """Key -> repo name and repo name -> root, from the board's own files (read only)."""
    keys = load_json(BOARD_DATA / "repo-keys.json")
    keys = keys.get("had", keys) if isinstance(keys, dict) else {}
    repos = load_json(BOARD_DATA / "repos.json")
    return {k.upper(): v for k, v in keys.items() if isinstance(v, str)}, repos


def board_task(repo, n):
    return load_json(BOARD_DATA / "tasks" / repo / str(n) / "task.json")


def resolve_board(key, n):
    keys, repos = board_maps()
    repo = keys.get(key.upper()) or next((r for r in repos if r.lower() == key.lower()), None)
    if repo is None:
        raise Refusal(f"Unknown board key {key!r}. Known keys: {', '.join(sorted(keys)) or 'none'}.")
    task = board_task(repo, n)
    root = task.get("root") or repos.get(repo)
    if not root:
        raise Refusal(f"Board repo {repo!r} has no folder in repos.json.")
    short = next((k for k, v in keys.items() if v == repo), key.upper())
    name = f"{short.lower()}-{n}"
    worktree, branch = task.get("worktree"), task.get("branch")
    if worktree and Path(worktree).is_dir():
        return Source("worktree", worktree), repo, name, f"{short}-{n}"
    if branch and git(root, "rev-parse", "--verify", "--quiet", branch).returncode == 0:
        return Source("branch", root, branch), repo, name, f"{short}-{n}"
    return Source("checkout", root), repo, name, f"{short}-{n}"


def worktree_task(path):
    """The board task whose worktree is this folder, as (short key, n), or None."""
    keys, _ = board_maps()
    top = git(path, "rev-parse", "--show-toplevel").stdout.strip()
    if not top or Path(top).resolve() != path.resolve():
        return None
    for task_file in (BOARD_DATA / "tasks").glob("*/*/task.json"):
        task = load_json(task_file)
        if task.get("worktree") == top:
            short = next((k for k, v in keys.items() if v == task.get("repo")), task.get("repo", ""))
            return short, task.get("n")
    return None


def resolve(target, task_name=""):
    """Turn a board id or a repo path into (source, repo, task name, board label)."""
    if target == "sample":
        target, task_name = str(SAMPLE), task_name or SAMPLE_TASK
    target = target or os.getcwd()
    path = Path(target).expanduser()
    if path.is_dir():
        found = None if task_name else worktree_task(path)
        if found:
            return resolve_board(*found)
        return Source("checkout", path.resolve()), path.resolve().name, task_name.lower(), task_name.upper()
    match = BOARD_ID.match(target)
    if not match:
        raise Refusal(f"{target!r} is neither a folder nor a board id like AMC-56.")
    return resolve_board(match.group(1), match.group(2))


def intent_folder(source):
    hook = source.read("AGENTS.md") or ""
    found = HOOK_INTENT_FOLDER.search(hook)
    return (found.group(1) if found else DEFAULT_INTENT_FOLDER).strip("/")


def parse(text, where, errors):
    """YAML text as a dict, or None with the reason added to errors."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as error:
        errors.append(f"{where} is not valid YAML: {str(error).splitlines()[0]}")
        return None
    if data is not None and not isinstance(data, dict):
        errors.append(f"{where} is not a mapping")
        return None
    return data


def as_list(value):
    return value if isinstance(value, list) else []


def clean_graph(raw, errors):
    """The graph's three lists with every field the views read present; bad entries reported."""
    graph = {"nodes": [], "edges": [], "clis": []}
    for key in graph:
        for k, item in enumerate(as_list(raw.get(key))):
            if not isinstance(item, dict):
                errors.append(f"{key}[{k}] is not a mapping")
                continue
            graph[key].append(item)
    for k, node in enumerate(graph["nodes"]):
        if not node.get("id"):
            errors.append(f"nodes[{k}] has no id")
        graph["nodes"][k] = {**node, "id": str(node.get("id") or f"nodes[{k}]"), "stage": str(node.get("stage") or ""),
                             "axis": str(node.get("axis") or ""), "inputs": as_list(node.get("inputs")),
                             "outputs": as_list(node.get("outputs"))}
    graph["edges"] = [{**e, "from": str(e.get("from") or ""), "to": str(e.get("to") or "")} for e in graph["edges"]]
    graph["clis"] = [{**c, "command": str(c.get("command") or ""), "path": [str(p) for p in as_list(c.get("path"))]}
                     for c in graph["clis"]]
    return graph


def clean_slice(raw, errors):
    """graph_slice entries as mappings with string fields; bad entries reported."""
    slice_ = {}
    for key in ("nodes", "edges", "clis"):
        items = []
        for k, item in enumerate(as_list(raw.get(key))):
            if isinstance(item, dict):
                items.append({f: str(v) for f, v in item.items()})
            else:
                errors.append(f"graph_slice.{key}[{k}] is not a mapping")
        slice_[key] = items
    return slice_


def find_intent(source, folder, task, errors):
    """Intent files whose name and task: field both start with the task name."""
    picks = []
    for name in source.names(folder):
        stem = name.lower().removesuffix(".yaml")
        if name == GRAPH_FILE or not name.endswith(".yaml") or not (stem == task or stem.startswith(task + "-")):
            continue
        data = parse(source.read(f"{folder}/{name}") or "", f"{folder}/{name}", errors) or {}
        field = str(data.get("task", "")).lower()
        if field == task or field.startswith(task + "-"):
            picks.append((name, data))
    return picks


def check_graph(graph, errors):
    ids = [n.get("id") for n in graph["nodes"]]
    known = set(ids)
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"node id {dup!r} appears more than once")
    for node in graph["nodes"]:
        nid = node.get("id")
        if node.get("stage") not in STAGES:
            errors.append(f"node {nid!r}: stage {node.get('stage')!r} is not one of {'|'.join(STAGES)}")
        if node.get("axis") not in AXES:
            errors.append(f"node {nid!r}: axis {node.get('axis')!r} is not ts or cs")
        if node.get("group_by") and node.get("axis") != "cs":
            errors.append(f"node {nid!r}: group_by is for cs nodes only")
    for edge in graph["edges"]:
        for end in ("from", "to"):
            if edge.get(end) not in known:
                errors.append(f"edge {edge.get('from')} -> {edge.get('to')}: {end} node {edge.get(end)!r} is not in the graph")
    pairs = {(e.get("from"), e.get("to")) for e in graph["edges"]}
    for cli in graph["clis"]:
        steps = cli.get("path") or []
        for a, b in zip(steps, steps[1:]):
            if (a, b) not in pairs:
                errors.append(f"cli {cli.get('command')!r}: step {a} -> {b} is not an edge")
    cycle = find_cycle(known, pairs)
    if cycle:
        errors.append("the graph has a cycle: " + " -> ".join(cycle))


def find_cycle(nodes, pairs):
    after = {n: [b for a, b in pairs if a == n] for n in nodes}
    state, stack = {}, []

    def visit(n):
        state[n] = "open"
        stack.append(n)
        for m in after.get(n, []):
            if state.get(m) == "open":
                return stack[stack.index(m):] + [m]
            if m not in state and (found := visit(m)):
                return found
        stack.pop()
        state[n] = "done"
        return None

    for n in sorted(nodes):
        if n not in state and (found := visit(n)):
            return found
    return None


def check_slice(slice_, graph, errors):
    known = {n.get("id") for n in graph["nodes"]}
    pairs = {(e.get("from"), e.get("to")) for e in graph["edges"]}
    commands = {c.get("command") for c in graph["clis"]}
    for node in slice_.get("nodes") or []:
        if node.get("mode") not in NODE_MODES:
            errors.append(f"slice node {node.get('id')!r}: mode {node.get('mode')!r} is not one of {'|'.join(NODE_MODES)}")
        if node.get("id") not in known:
            errors.append(f"slice node {node.get('id')!r} is missing in graph.yaml")
    for edge in slice_.get("edges") or []:
        mode, pair = edge.get("mode"), (edge.get("from"), edge.get("to"))
        if mode not in EDGE_MODES:
            errors.append(f"slice edge {pair[0]} -> {pair[1]}: mode {mode!r} is not one of {'|'.join(EDGE_MODES)}")
        if mode == "remove" and pair in pairs:
            errors.append(f"slice edge {pair[0]} -> {pair[1]} is marked remove but is still in graph.yaml")
        if mode != "remove" and pair not in pairs:
            errors.append(f"slice edge {pair[0]} -> {pair[1]} is missing in graph.yaml")
    for cli in slice_.get("clis") or []:
        if cli.get("mode") not in CLI_MODES:
            errors.append(f"slice cli {cli.get('command')!r}: mode {cli.get('mode')!r} is not one of {'|'.join(CLI_MODES)}")
        if cli.get("mode") != "remove" and cli.get("command") not in commands:
            errors.append(f"slice cli {cli.get('command')!r} is missing in graph.yaml")


def build_view(target, task_name=""):
    """Everything both views draw, as one plain dict."""
    source, repo, task, label = resolve(target, task_name)
    folder = intent_folder(source)
    graph_path = f"{folder}/{GRAPH_FILE}"
    errors, notes = [], []
    text = source.read(graph_path)
    raw = parse(text, graph_path, errors) if text is not None else None
    graph = {"nodes": [], "edges": [], "clis": []}
    if text is None:
        notes.append(NO_GRAPH.format(path=graph_path))
    elif raw is not None:
        graph = clean_graph(raw, errors)
        repo = raw.get("repo") or repo
        check_graph(graph, errors)
    slice_, slice_state, intent_name = {}, "none", ""
    if not task:
        notes.append(NO_TASK)
    else:
        picks = find_intent(source, folder, task, errors)
        if not picks:
            notes.append(NO_INTENT.format(task=label, folder=folder))
        elif len(picks) > 1:
            notes.append(MANY_INTENTS.format(task=label, names=", ".join(n for n, _ in picks)))
            slice_state = "ambiguous"
        else:
            intent_name, data = picks[0]
            raw_slice = data.get("graph_slice")
            slice_ = clean_slice(raw_slice, errors) if isinstance(raw_slice, dict) else {}
            if not any(slice_.values()):
                slice_ = {}
                notes.append(NO_SLICE.format(task=label))
            else:
                slice_state = "found"
                check_slice(slice_, graph, errors)
    return assemble(repo, label, source, graph_path, folder, intent_name, slice_state, graph, slice_, errors, notes)


def assemble(repo, label, source, graph_path, folder, intent_name, slice_state, graph, slice_, errors, notes):
    node_mode = {n.get("id"): n.get("mode") for n in slice_.get("nodes") or []}
    edge_mode = {(e.get("from"), e.get("to")): e.get("mode") for e in slice_.get("edges") or []}
    cli_mode = {c.get("command"): c.get("mode") for c in slice_.get("clis") or []}
    known = {n.get("id") for n in graph["nodes"]}
    nodes = [{**n, "mode": node_mode.get(n.get("id"), "")} for n in graph["nodes"]]
    nodes += [{"id": i, "stage": "", "axis": "", "mode": m, "missing": True} for i, m in node_mode.items() if i not in known]
    edges = [{**e, "mode": edge_mode.get((e.get("from"), e.get("to")), "")} for e in graph["edges"]]
    pairs = {(e.get("from"), e.get("to")) for e in graph["edges"]}
    edges += [{"from": a, "to": b, "mode": m, "missing": m != "remove"} for (a, b), m in edge_mode.items() if (a, b) not in pairs]
    clis = [{**c, "mode": cli_mode.get(c.get("command"), "")} for c in graph["clis"]]
    commands = {c.get("command") for c in graph["clis"]}
    clis += [{"command": c, "path": [], "mode": m, "missing": m != "remove"} for c, m in cli_mode.items() if c not in commands]
    return {
        "repo": repo,
        "task": label,
        "source": source.label(),
        "graph_file": graph_path,
        "intent_file": f"{folder}/{intent_name}" if intent_name else "",
        "slice": slice_state,
        "stages": [{"id": s, "title": STAGE_TITLES[s]} for s in STAGES],
        "nodes": nodes,
        "edges": edges,
        "clis": clis,
        "errors": errors,
        "notes": notes,
    }


PAGE_STYLE = """
:root {
  --bg: #f6f7f5; --panel: #ffffff; --fg: #1d2421; --muted: #66706b; --line: #c9cfcb;
  --add: #1f7a4d; --rewire: #b26a00; --polish: #2b5fae; --remove: #b3261e;
  --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --sans: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #121614; --panel: #1a201d; --fg: #e4e9e6; --muted: #93a09a; --line: #3a4440;
  --add: #4cc38a; --rewire: #f0a43a; --polish: #7aa7ff; --remove: #ff7a70; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #121614; --panel: #1a201d; --fg: #e4e9e6; --muted: #93a09a; --line: #3a4440;
  --add: #4cc38a; --rewire: #f0a43a; --polish: #7aa7ff; --remove: #ff7a70; color-scheme: dark }
body { background: var(--bg); color: var(--fg); font-family: var(--sans); line-height: 1.45;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
main { max-width: 1180px; margin: 0 auto; padding-block: 24px 48px; display: grid; gap: 20px; }
main > * { min-width: 0; }
h1 { font-size: 1.5rem; margin: 0; text-wrap: balance; }
h2 { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin: 0 0 8px; }
.meta { color: var(--muted); font-family: var(--mono); font-size: 0.78rem; display: grid; gap: 2px; min-width: 0; overflow-wrap: anywhere; }
.notes p, .errors p { margin: 0; }
.notes { border-left: 3px solid var(--line); padding: 6px 12px; }
.errors { border-left: 3px solid var(--remove); padding: 6px 12px; color: var(--remove); }
.legend { display: flex; flex-wrap: wrap; gap: 8px 16px; font-size: 0.82rem; color: var(--muted); }
.legend span { display: inline-flex; align-items: center; gap: 6px; }
.chip { width: 14px; height: 10px; border-radius: 2px; border: 2px solid var(--line); display: inline-block; }
.diagram { overflow-x: auto; background: var(--panel); border: 1px solid var(--line); border-radius: 6px; }
.diagram svg { display: block; max-width: none; }
.narrow { display: none; }
@media (max-width: 720px) { .wide { display: none; } .narrow { display: block; } .narrow svg { width: 100%; height: auto; } }
svg text { fill: var(--fg); font-family: var(--mono); }
svg .lane { fill: var(--bg); }
svg .lane-title { fill: var(--muted); font-family: var(--sans); font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; }
svg .node rect { fill: var(--panel); stroke: var(--line); stroke-width: 1.5; }
svg .node .sub { fill: var(--muted); font-size: 10px; }
svg .edge { fill: none; stroke: var(--line); stroke-width: 1.4; }
svg .head { fill: var(--line); }
svg .add rect { stroke: var(--add); stroke-width: 2.5; } svg .edge.add { stroke: var(--add); stroke-width: 2.2; } svg .head.add { fill: var(--add); }
svg .rewire rect { stroke: var(--rewire); stroke-width: 2.5; } svg .edge.rewire { stroke: var(--rewire); stroke-width: 2.2; } svg .head.rewire { fill: var(--rewire); }
svg .polish rect { stroke: var(--polish); stroke-width: 2.5; }
svg .edge.remove { stroke: var(--remove); stroke-dasharray: 5 4; stroke-width: 2; } svg .head.remove { fill: var(--remove); }
.chip.add { border-color: var(--add); } .chip.rewire { border-color: var(--rewire); } .chip.polish { border-color: var(--polish); }
.chip.remove { border-style: dashed; border-color: var(--remove); }
svg .missing rect { stroke: var(--remove); stroke-dasharray: 3 3; }
svg .dim { opacity: 0.55; }
table { border-collapse: collapse; width: 100%; font-size: 0.85rem; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { color: var(--muted); font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; }
td code { font-family: var(--mono); font-size: 0.8rem; white-space: nowrap; }
.tablewrap { overflow-x: auto; }
.mode { font-family: var(--mono); font-size: 0.75rem; font-weight: 700; }
.mode.add { color: var(--add); } .mode.rewire { color: var(--rewire); } .mode.polish { color: var(--polish); } .mode.remove { color: var(--remove); }
"""
LEGEND = [("add", "added"), ("rewire", "rewired"), ("polish", "polished"), ("remove", "removed edge"), ("", "untouched")]
NODE_W, NODE_H, GAP_Y, LANE_W, TOP = 168, 46, 16, 196, 34


def node_rows(view):
    """Nodes grouped by stage in file order; nodes no stage lane takes go last, in their own lane."""
    rows = {s: [n for n in view["nodes"] if n.get("stage") == s] for s in STAGES}
    rows["missing"] = [n for n in view["nodes"] if n.get("stage") not in STAGES]
    return rows


def axis_text(node):
    if node.get("missing"):
        return "missing in graph.yaml"
    if node.get("stage") not in STAGES:
        return f"stage {node.get('stage') or 'none'}?"
    axis = (node.get("axis") or "").upper()
    return f"{axis}({node['group_by']})" if node.get("group_by") else axis


def svg_node(node, x, y, has_slice):
    cls = " ".join(c for c in ["node", node.get("mode", ""), "missing" if node.get("missing") else "",
                               "dim" if has_slice and not node.get("mode") else ""] if c)
    title = html.escape(f"{node['id']} — {', '.join(node.get('inputs') or [])} → {', '.join(node.get('outputs') or [])}")
    return (f'<g class="{cls}"><title>{title}</title><rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="5"/>'
            f'<text x="{x + 10}" y="{y + 19}" font-size="12">{html.escape(node["id"])}</text>'
            f'<text class="sub" x="{x + 10}" y="{y + 35}">{html.escape(axis_text(node))}</text></g>')


def svg_edge(edge, spot, has_slice, horizontal):
    a, b = spot.get(edge["from"]), spot.get(edge["to"])
    if not a or not b:
        return ""
    mode = edge.get("mode", "")
    cls = " ".join(c for c in ["edge", mode, "dim" if has_slice and not mode else ""] if c)
    if horizontal:
        x1, y1, x2, y2 = a[0] + NODE_W, a[1] + NODE_H / 2, b[0], b[1] + NODE_H / 2
        if x2 <= x1:
            x1, x2 = a[0] + NODE_W / 2, b[0] + NODE_W / 2
            y1, y2 = (a[1] + NODE_H, b[1]) if b[1] > a[1] else (a[1], b[1] + NODE_H)
        bend = max(30, abs(x2 - x1) / 2)
        path = f"M{x1},{y1} C{x1 + bend},{y1} {x2 - bend},{y2} {x2},{y2}"
        head = f"{x2},{y2} {x2 - 7},{y2 - 4} {x2 - 7},{y2 + 4}"
    else:
        x1, y1, x2, y2 = a[0] + NODE_W / 2, a[1] + NODE_H, b[0] + NODE_W / 2, b[1]
        bend = max(20, abs(y2 - y1) / 2)
        path = f"M{x1},{y1} C{x1},{y1 + bend} {x2},{y2 - bend} {x2},{y2}"
        head = f"{x2},{y2} {x2 - 4},{y2 - 7} {x2 + 4},{y2 - 7}"
    label = html.escape(f"{edge['from']} → {edge['to']}" + (f" ({edge['carries']})" if edge.get("carries") else ""))
    head_cls = " ".join(c for c in ["head", mode, "dim" if has_slice and not mode else ""] if c)
    return f'<g><title>{label}</title><path class="{cls}" d="{path}"/><polygon class="{head_cls}" points="{head}"/></g>'


def svg_wide(view, has_slice):
    rows = node_rows(view)
    lanes = [s for s in STAGES] + (["missing"] if rows["missing"] else [])
    tallest = max([len(rows[s]) for s in lanes] + [1])
    width, height = LANE_W * len(lanes) + 14, TOP + tallest * (NODE_H + GAP_Y) + 10
    spot, parts = {}, []
    for i, lane in enumerate(lanes):
        x = 8 + i * LANE_W
        title = STAGE_TITLES.get(lane, "Not placed")
        parts.append(f'<rect class="lane" x="{x}" y="6" width="{LANE_W - 10}" height="{height - 12}" rx="4"/>'
                     f'<text class="lane-title" x="{x + 10}" y="24">{title}</text>')
        for j, node in enumerate(rows[lane]):
            spot[node["id"]] = (x + 9, TOP + j * (NODE_H + GAP_Y))
    edges = [svg_edge(e, spot, has_slice, True) for e in view["edges"]]
    nodes = [svg_node(n, *spot[n["id"]], has_slice) for lane in lanes for n in rows[lane]]
    return (f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" '
            f'aria-label="Compute graph by stage">{"".join(parts + edges + nodes)}</svg>')


def svg_narrow(view, has_slice):
    rows = node_rows(view)
    lanes = [s for s in STAGES if rows[s]] + (["missing"] if rows["missing"] else [])
    width, per_row, y, spot, parts = 2 * NODE_W + 40, 2, 6, {}, []
    for lane in lanes:
        count = len(rows[lane])
        lines = (count + per_row - 1) // per_row
        lane_h = 26 + lines * (NODE_H + GAP_Y)
        parts.append(f'<rect class="lane" x="4" y="{y}" width="{width - 8}" height="{lane_h}" rx="4"/>'
                     f'<text class="lane-title" x="14" y="{y + 18}">{STAGE_TITLES.get(lane, "Not placed")}</text>')
        for j, node in enumerate(rows[lane]):
            spot[node["id"]] = (14 + (j % per_row) * (NODE_W + 12), y + 28 + (j // per_row) * (NODE_H + GAP_Y))
        y += lane_h + 22
    edges = [svg_edge(e, spot, has_slice, False) for e in view["edges"]]
    nodes = [svg_node(n, *spot[n["id"]], has_slice) for lane in lanes for n in rows[lane]]
    return (f'<svg viewBox="0 0 {width} {y}" role="img" aria-label="Compute graph by stage, stacked">'
            f'{"".join(parts + edges + nodes)}</svg>')


def mode_cell(mode):
    return f'<span class="mode {mode}">{mode}</span>' if mode else ""


def tables(view):
    def code(text):
        return f"<code>{html.escape(str(text))}</code>"

    nodes = "".join(
        f"<tr><td>{code(n['id'])}</td><td>{html.escape(STAGE_TITLES.get(n.get('stage'), '—'))}</td>"
        f"<td>{html.escape(axis_text(n))}</td><td>{code(', '.join(n.get('inputs') or []))}</td>"
        f"<td>{code(', '.join(n.get('outputs') or []))}</td><td>{mode_cell(n.get('mode'))}</td></tr>"
        for n in view["nodes"])
    clis = "".join(
        f"<tr><td>{code(c['command'])}</td><td>{code(' → '.join(c.get('path') or []))}</td><td>{mode_cell(c.get('mode'))}</td></tr>"
        for c in view["clis"])
    return (f'<section><h2>Nodes</h2><div class="tablewrap"><table><tr><th>Node</th><th>Stage</th><th>Axis</th>'
            f'<th>Inputs</th><th>Outputs</th><th>Slice</th></tr>{nodes}</table></div></section>'
            f'<section><h2>CLI ↔ sub-path</h2><div class="tablewrap"><table><tr><th>Command</th><th>Path</th>'
            f'<th>Slice</th></tr>{clis}</table></div></section>')


def render_html(view):
    has_slice = view["slice"] == "found"
    name = view["task"] or view["repo"]
    meta = [f"repo {view['repo']}", f"read from {view['source']}", f"graph {view['graph_file']}"]
    meta += [f"intent {view['intent_file']}"] if view["intent_file"] else []
    notes = "".join(f"<p>{html.escape(n)}</p>" for n in view["notes"])
    errors = "".join(f"<p>{html.escape(e)}</p>" for e in view["errors"])
    legend = "".join(f'<span><i class="chip {m}"></i>{t}</span>' for m, t in LEGEND)
    return (
        f'<title>Compute graph {html.escape(name)}</title>\n'
        '<meta name="claude:viewport-fit-sides" content="cover">\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap">\n'
        f"<style>{PAGE_STYLE}</style>\n<main>"
        f"<header><h1>Compute graph {html.escape(name)}</h1>"
        f'<div class="meta">{"".join(f"<span>{html.escape(m)}</span>" for m in meta)}</div></header>'
        + (f'<div class="errors">{errors}</div>' if errors else "")
        + (f'<div class="notes">{notes}</div>' if notes else "")
        + f'<div class="legend">{legend}</div>'
        f'<div class="diagram wide">{svg_wide(view, has_slice)}</div>'
        f'<div class="diagram narrow">{svg_narrow(view, has_slice)}</div>'
        f"{tables(view)}</main>\n"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["json", "check", "html"])
    parser.add_argument("target", nargs="?", default="", help="board id (AMC-56), repo folder or sample; default: cwd")
    parser.add_argument("--task", default="", help="task name for a repo folder, e.g. smp-1")
    parser.add_argument("-o", "--out", default="", help="html: output file (default: stdout)")
    args = parser.parse_args(argv)
    try:
        view = build_view(args.target, args.task)
    except Refusal as refusal:
        print(json.dumps({"refusal": str(refusal)}) if args.action == "json" else str(refusal), file=sys.stdout if args.action == "json" else sys.stderr)
        return 2
    if args.action == "json":
        print(json.dumps(view, indent=1))
    elif args.action == "check":
        for line in view["errors"] + view["notes"]:
            print(line)
        return 1 if view["errors"] else 0
    else:
        page = render_html(view)
        if args.out:
            Path(args.out).write_text(page)
            print(args.out)
        else:
            print(page)
    return 0


if __name__ == "__main__":
    sys.exit(main())
