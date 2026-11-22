"""Checks for compute_graph.py on the sample and on broken copies: uv run --with pyyaml python -m unittest."""

import shutil
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


if __name__ == "__main__":
    unittest.main()
