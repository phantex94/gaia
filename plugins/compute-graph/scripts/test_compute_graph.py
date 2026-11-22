"""Checks for compute_graph.py on the sample and on broken copies: uv run --with pyyaml python -m unittest."""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import compute_graph as cg

SAMPLE = Path(__file__).resolve().parent.parent / "sample"


class SampleTest(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp()) / "repo"
        shutil.copytree(SAMPLE, self.repo)
        self.intent = self.repo / "docs" / "intent"

    def tearDown(self):
        shutil.rmtree(self.repo.parent)

    def edit(self, name, old, new):
        path = self.intent / name
        path.write_text(path.read_text().replace(old, new))

    def test_sample_slice_is_found_and_clean(self):
        view = cg.build_view(str(self.repo), "smp-1")
        self.assertEqual((view["slice"], view["errors"]), ("found", []))
        modes = {n["id"]: n["mode"] for n in view["nodes"]}
        self.assertEqual((modes["carry_factor"], modes["alpha_blend"], modes["pit_bars"]), ("add", "rewire", "polish"))
        self.assertIn({"from": "momentum", "to": "alpha_blend", "mode": "remove", "missing": False}, view["edges"])

    def test_broken_graph_is_refused(self):
        self.edit("graph.yaml", "  - { from: momentum, to: risk_report, carries: momentum_score }",
                  "  - { from: momentum, to: risk_report, carries: momentum_score }\n"
                  "  - { from: risk_report, to: pit_bars }\n  - { from: ghost, to: momentum }")
        self.edit("smp-1-carry-factor.yaml", "{ id: pit_bars, mode: polish }",
                  "{ id: pit_bars, mode: polish }\n    - { id: vol_target, mode: add }")
        errors = " | ".join(cg.build_view(str(self.repo), "smp-1")["errors"])
        for expected in ("'ghost' is not in the graph", "has a cycle", "'vol_target' is missing in graph.yaml"):
            self.assertIn(expected, errors)

    def test_no_intent_means_no_slice(self):
        view = cg.build_view(str(self.repo), "smp-2")
        self.assertEqual(view["slice"], "none")
        self.assertIn("no intent file", view["notes"][0])

    def test_two_intents_pick_none(self):
        shutil.copy(self.intent / "smp-1-carry-factor.yaml", self.intent / "smp-1-other.yaml")
        view = cg.build_view(str(self.repo), "smp-1")
        self.assertEqual(view["slice"], "ambiguous")
        self.assertTrue(all(not n["mode"] for n in view["nodes"]))

    def test_page_names_the_task(self):
        page = cg.render_html(cg.build_view(str(self.repo), "smp-1"))
        self.assertTrue(page.startswith("<title>Compute graph SMP-1</title>"))

    def test_malformed_files_become_errors(self):
        (self.intent / "graph.yaml").write_text("nodes: [\n")
        view = cg.build_view(str(self.repo), "smp-1")
        self.assertIn("not valid YAML", view["errors"][0])
        cg.render_html(view)

    def test_missing_fields_and_unknown_stage_are_shown(self):
        (self.intent / "graph.yaml").write_text(
            "nodes:\n  - { stage: data, axis: ts }\n  - { id: odd_node, stage: signal }\n  - plain text\n"
            "clis:\n  - { command: cta x }\n")
        view = cg.build_view(str(self.repo), "")
        errors = " | ".join(view["errors"])
        for expected in ("nodes[0] has no id", "stage 'signal'", "nodes[2] is not a mapping"):
            self.assertIn(expected, errors)
        self.assertIn("odd_node", [n["id"] for n in cg.node_rows(view)["missing"]])
        self.assertIn("odd_node", cg.render_html(view))


class BoardTest(unittest.TestCase):
    """A board task whose files exist only on its branch, in a folder the Hook names."""

    def setUp(self):
        self.top = Path(tempfile.mkdtemp())
        repo, board = self.top / "repo", self.top / "board"
        folder = repo / "plan" / "intent"
        folder.mkdir(parents=True)
        run = lambda *args: subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)
        run("init", "-q", "-b", "main")
        (repo / "AGENTS.md").write_text("- Intent folder: `plan/intent/`; file name: key-n-slug.yaml\n")
        run("add", "-A")
        run("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "hook")
        run("checkout", "-q", "-b", "work/7-carry")
        shutil.copy(SAMPLE / "docs/intent/graph.yaml", folder / "graph.yaml")
        intent = (SAMPLE / "docs/intent/smp-1-carry-factor.yaml").read_text().replace("smp-1-carry-factor", "rpo-7-carry")
        (folder / "rpo-7-carry.yaml").write_text(intent)
        run("add", "-A")
        run("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "intent")
        run("checkout", "-q", "main")
        (board / "tasks" / "repo" / "7").mkdir(parents=True)
        (board / "repo-keys.json").write_text(json.dumps({"had": {"RPO": "repo"}}))
        (board / "repos.json").write_text(json.dumps({"repo": str(repo)}))
        task = {"root": str(repo), "branch": "work/7-carry", "worktree": str(self.top / "gone")}
        (board / "tasks" / "repo" / "7" / "task.json").write_text(json.dumps(task))
        self.saved, cg.BOARD_DATA = cg.BOARD_DATA, board

    def tearDown(self):
        cg.BOARD_DATA = self.saved
        shutil.rmtree(self.top)

    def test_board_id_reads_the_branch(self):
        view = cg.build_view("rpo-7")
        self.assertEqual((view["task"], view["source"], view["slice"]), ("RPO-7", "branch work/7-carry", "found"))
        self.assertEqual(view["intent_file"], "plan/intent/rpo-7-carry.yaml")


if __name__ == "__main__":
    unittest.main()
