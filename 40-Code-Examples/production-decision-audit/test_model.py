from __future__ import annotations

import json
import io
import sys
import unittest
from pathlib import Path

import pandas as pd

from run import load_config, minimal_fixed_sample_plan, output_root, reproduce_p03_table

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config.yaml"


class ProductionDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_config(CONFIG)
        cls.out = output_root(CONFIG, cls.config)

    def test_exact_sampling_plans_meet_both_errors(self) -> None:
        cfg = self.config["sampling"]
        for p1 in cfg["alternative_defect_rates"]:
            plan = minimal_fixed_sample_plan(
                cfg["nominal_defect_rate"],
                p1,
                cfg["acceptable_probability_at_nominal"],
                cfg["reject_probability_at_alternative"],
                cfg["maximum_sample_size"],
            )
            self.assertGreaterEqual(plan["accept_probability_p0"], cfg["acceptable_probability_at_nominal"])
            self.assertGreaterEqual(plan["reject_probability_p1"], cfg["reject_probability_at_alternative"])

    def test_p03_no_disassembly_table_matches_reported_precision(self) -> None:
        frame = reproduce_p03_table(self.config)
        self.assertEqual(len(frame), 48)
        self.assertTrue(frame["within_reported_2dp_tolerance"].all())

    def test_saved_runtime_has_seed_and_hashes(self) -> None:
        runtime = json.loads((self.out / "runtime.json").read_text(encoding="utf-8"))
        self.assertEqual(runtime["seed"], self.config["seed"])
        self.assertEqual(len(runtime["config_sha256"]), 64)
        self.assertEqual(len(runtime["code_sha256"]), 64)

    def test_bayesian_counts_equal_configured_draws(self) -> None:
        frame = pd.read_csv(self.out / "beta_binomial_policy_stability.csv")
        self.assertEqual(int(frame["selection_count"].sum()), self.config["bayesian_demo"]["posterior_draws"])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProductionDecisionTests)
    buffer = io.StringIO()
    result = unittest.TextTestRunner(stream=buffer, verbosity=2).run(suite)
    rendered = buffer.getvalue()
    (output_root(CONFIG, load_config(CONFIG)) / "tests.log").write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    raise SystemExit(0 if result.wasSuccessful() else 1)
