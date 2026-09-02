"""Tests for the AA Intelligence Index reconstruction.

Run from the repo root:  python -m unittest discover -s tests -v
"""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Make src/aa_index.py importable as aa_index.
import importlib.util
import sys

spec = importlib.util.spec_from_file_location(
    "aa_index", REPO_ROOT / "src" / "aa_index.py"
)
aa_index = importlib.util.module_from_spec(spec)
sys.modules["aa_index"] = aa_index
spec.loader.exec_module(aa_index)


class TestCoreMath(unittest.TestCase):
    def test_clamp01(self):
        self.assertEqual(aa_index.clamp01(-0.5), 0.0)
        self.assertEqual(aa_index.clamp01(0.42), 0.42)
        self.assertEqual(aa_index.clamp01(1.7), 1.0)

    def test_gdpval_normalization_anchors(self):
        # (Elo - 500) / 2000, clamped to [0, 1]
        self.assertAlmostEqual(aa_index.gdpval_normalize(500), 0.0)
        self.assertAlmostEqual(aa_index.gdpval_normalize(1000), 0.25)  # human anchor
        self.assertAlmostEqual(aa_index.gdpval_normalize(1824), 0.662)  # Opus 5
        self.assertAlmostEqual(aa_index.gdpval_normalize(2500), 1.0)   # clamped
        self.assertAlmostEqual(aa_index.gdpval_normalize(100), 0.0)    # clamped

    def test_reconstruct_index_known_value(self):
        # Hand-computed example: two components only.
        weights = {"A": 0.6, "B": 0.4}
        components = {"A": 0.5, "B": 1.0}
        index, contributions = aa_index.reconstruct_index(components, weights)
        self.assertAlmostEqual(index, 100 * (0.6 * 0.5 + 0.4 * 1.0))  # 70.0
        self.assertAlmostEqual(sum(contributions.values()), index)

    def test_reconstruct_index_missing_component_raises(self):
        with self.assertRaises(KeyError):
            aa_index.reconstruct_index({"A": 0.5}, {"A": 0.5, "B": 0.5})


class TestDataFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.weights = aa_index.load_weights()
        cls.rows = aa_index.load_models()

    def test_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(self.weights.values()), 1.0, places=6)

    def test_weights_count(self):
        self.assertEqual(len(self.weights), 10)

    def test_category_mass(self):
        # Operative masses of the formula that reproduces the Index:
        # Agents 34, Coding 16, Scientific 32, General 18 (= 100).
        # NOTE: some AA summary materials annotate Coding/Scientific as 24/24;
        # those labels do not match the operative per-component weights and
        # appear to be v4.0 leftovers. See docs/methodology.md.
        import csv

        categories = {}
        with open(REPO_ROOT / "data" / "weights_v4.1.1.csv", newline="") as f:
            for row in csv.DictReader(f):
                categories[row["category"]] = (
                    categories.get(row["category"], 0.0) + float(row["weight"])
                )
        self.assertAlmostEqual(categories["Agents"], 0.34, places=6)
        self.assertAlmostEqual(categories["Coding"], 0.16, places=6)
        self.assertAlmostEqual(categories["Scientific"], 0.32, places=6)
        self.assertAlmostEqual(categories["General"], 0.18, places=6)

    def test_matrix_has_8_models_with_all_components(self):
        self.assertEqual(len(self.rows), 8)
        for row in self.rows:
            components = aa_index.model_row_to_components(row)
            self.assertEqual(
                set(components), set(self.weights),
                f"{row['model']}: missing components",
            )


class TestVerification(unittest.TestCase):
    """The core claim: max |Delta| <= 1.0 on the 8-model band 56-63."""

    @classmethod
    def setUpClass(cls):
        cls.weights = aa_index.load_weights()
        cls.rows = aa_index.load_models()

    def test_published_deltas_match_bilan(self):
        # Deltas hand-recorded in bilan.md. The hand computation rounded
        # intermediate values, so exact recomputation may differ by up to
        # ~0.02 (e.g. Opus 5: exact -0.30 vs hand-recorded -0.31).
        expected = {
            "Claude Opus 5 (max)": -0.31,
            "Grok 4.6 (high)": -0.23,
            "Kimi K3 (max)": 0.00,
            "GLM-5.3 (max)": -0.12,
            "Qwen3.8 2.4T": -0.04,
            "GLM-5.3-Flash": -0.08,
            "Muse Spark 1.2": -0.16,
            "Gemini 3.7 Flash": -0.09,
        }
        for row in self.rows:
            components = aa_index.model_row_to_components(row)
            index, _ = aa_index.reconstruct_index(components, self.weights)
            delta = round(index - float(row["index_aa"]), 2)
            self.assertAlmostEqual(
                delta, expected[aa_index.display_name(row)], delta=0.02,
                msg=f"{row['model']}: delta {delta} != {expected[aa_index.display_name(row)]}",
            )

    def test_all_deltas_within_tolerance(self):
        for row in self.rows:
            components = aa_index.model_row_to_components(row)
            index, _ = aa_index.reconstruct_index(components, self.weights)
            self.assertLessEqual(
                abs(index - float(row["index_aa"])), 1.0,
                msg=f"{row['model']}: |Delta| exceeds lock threshold 1.0",
            )

    def test_max_abs_delta_is_030(self):
        # Exact recomputation gives max |Delta| = 0.30 (Opus 5);
        # the bilan hand-recorded 0.31 (intermediate rounding, see above).
        deltas = []
        for row in self.rows:
            components = aa_index.model_row_to_components(row)
            index, _ = aa_index.reconstruct_index(components, self.weights)
            deltas.append(abs(index - float(row["index_aa"])))
        self.assertAlmostEqual(max(deltas), 0.30, delta=0.011)

    def test_json_output_shape(self):
        payload = json.loads(aa_index.to_json(self.rows, self.weights))
        self.assertEqual(payload["weights_version"], "v4.1.1")
        self.assertEqual(len(payload["models"]), 8)
        self.assertLessEqual(payload["max_abs_delta"], 1.0)


class TestJsonInput(unittest.TestCase):
    """The examples/ JSON files produce the same result as the CSV rows."""

    @classmethod
    def setUpClass(cls):
        cls.weights = aa_index.load_weights()

    def test_opus5_json_matches_published(self):
        data = aa_index.load_model_json(REPO_ROOT / "examples" / "claude-opus-5.json")
        row = {k: "" if v is None else str(v) for k, v in data.items()}
        components = aa_index.model_row_to_components(row)
        index, _ = aa_index.reconstruct_index(components, self.weights)
        self.assertAlmostEqual(index - 63.05, -0.30, delta=0.011)

    def test_kimi3_json_is_exact_match(self):
        data = aa_index.load_model_json(REPO_ROOT / "examples" / "kimi-k3.json")
        row = {k: "" if v is None else str(v) for k, v in data.items()}
        components = aa_index.model_row_to_components(row)
        index, _ = aa_index.reconstruct_index(components, self.weights)
        self.assertAlmostEqual(index, 59.70, delta=0.011)


if __name__ == "__main__":
    unittest.main()
