"""Regression tests: formulas, risk gates, bad inputs, escaping and examples."""
import copy
import json
import math
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "five-step-optimizer" / "scripts"))
from process_metrics import analyze_case, analyze_line
from validate_case import validate
from render_flow import render


class OptimizerTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads((ROOT / "examples/gigacasting-synthetic.json").read_text(encoding="utf-8"))

    def test_examples_pass(self):
        self.assertEqual(validate(self.case), [])
        other = json.loads((ROOT / "examples/software-bugflow-synthetic.json").read_text(encoding="utf-8"))
        self.assertEqual(validate(other), [])

    def test_model_returns_positive_values(self):
        result = analyze_case(self.case)
        self.assertGreater(result["baseline"]["good_units_per_hour_upper_bound"], 0)
        self.assertGreater(result["proposed"]["variable_cost_per_good"], 0)
        self.assertEqual(result["classification"], "synthetic")

    def test_exact_two_step_formula(self):
        line = {"name": "test", "steps": [
            {"id": "A", "name": "A", "cycle_seconds": 60, "machines": 1, "availability": 1, "yield": .5, "variable_cost_per_attempt": 5},
            {"id": "B", "name": "B", "cycle_seconds": 120, "machines": 1, "availability": 1, "yield": .8, "variable_cost_per_attempt": 10},
        ]}
        out = analyze_line(line)
        self.assertAlmostEqual(out["good_units_per_hour_upper_bound"], 24)
        self.assertAlmostEqual(out["variable_cost_per_good"], 5 / (.5 * .8) + 10 / .8)
        self.assertEqual(out["bottleneck_step"], "B")

    def test_economics_reconciles(self):
        result = analyze_case(self.case)
        savings = result["baseline"]["variable_cost_per_good"] - result["proposed"]["variable_cost_per_good"]
        annual = 150000 * savings - 1300000
        self.assertAlmostEqual(result["economics"]["annual_net_operating_benefit"], annual)

    def test_forbid_deleting_mandatory(self):
        self.case["requirements"][1]["decision"] = "delete"
        self.assertTrue(validate(self.case))
        with self.assertRaises(ValueError):
            analyze_case(self.case)

    def test_missing_proposed_blocked(self):
        del self.case["proposed"]
        self.assertTrue(validate(self.case))
        with self.assertRaises(ValueError):
            render(self.case)

    def test_invalid_yields_rejected(self):
        for bad in (0, -1, 1.1, float("nan"), float("inf"), "0.9", True):
            modified = copy.deepcopy(self.case)
            modified["baseline"]["steps"][0]["yield"] = bad
            self.assertTrue(validate(modified), str(bad))

    def test_invalid_machines_rejected(self):
        for bad in (0, -1, 1.5, "2", False):
            modified = copy.deepcopy(self.case)
            modified["proposed"]["steps"][0]["machines"] = bad
            self.assertTrue(validate(modified), str(bad))

    def test_negative_economics_rejected(self):
        self.case["economics"]["incremental_capex"] = -1
        self.assertTrue(validate(self.case))

    def test_fake_observed_evidence_rejected(self):
        self.case["evidence"][0]["classification"] = "observed"
        self.assertTrue(validate(self.case))

    def test_empty_evidence_rejected(self):
        self.case["evidence"] = []
        self.assertTrue(validate(self.case))

    def test_duplicate_requirement_rejected(self):
        self.case["requirements"].append(copy.deepcopy(self.case["requirements"][0]))
        self.assertTrue(validate(self.case))

    def test_wrong_step_type_rejected(self):
        self.case["baseline"]["steps"] = "bad"
        self.assertTrue(validate(self.case))

    def test_wrong_case_type_rejected(self):
        self.assertTrue(validate("bad"))

    def test_xml_sanitization(self):
        self.case["baseline"]["steps"][0]["name"] = "<script>alert(1)</script>"
        svg = render(self.case)
        self.assertIn("&lt;script&gt;", svg)
        self.assertNotIn("<script>", svg)
        ET.fromstring(svg)

    def test_software_metrics(self):
        other = json.loads((ROOT / "examples/software-bugflow-synthetic.json").read_text(encoding="utf-8"))
        self.assertGreater(analyze_case(other)["proposed"]["good_units_per_hour_upper_bound"], 0)


if __name__ == "__main__":
    unittest.main()
