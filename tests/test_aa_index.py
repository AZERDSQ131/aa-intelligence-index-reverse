"""Tests for the AA Intelligence Index reconstruction (v4.3.2, with v4.1.1 archive).

Run from the repo root:  python -m unittest discover -s tests -v
"""

import csv
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

LEGACY_WEIGHTS = REPO_ROOT / "data" / "weights_v4.1.1.csv"
LEGACY_MODELS = REPO_ROOT / "data" / "models.csv"
WEIGHTS_432 = REPO_ROOT / "data" / "weights_v4.3.2.csv"
MODELS_432 = REPO_ROOT / "data" / "models_v4.3.2.csv"


class TestCoreMath(unittest.TestCase):
    def test_clamp01(self):
        self.assertEqual(aa_index.clamp01(-0.5), 0.0)
        self.assertEqual(aa_index.clamp01(0.42), 0.42)
        self.assertEqual(aa_index.clamp01(1.7), 1.0)

    def test_elo_normalization_anchors(self):
        # (Elo - 500) / 2000, clamped to [0, 1] — shared by both Elo
        # components in v4.3.2 (Briefcase v1.1, GDPval-AA v2.1).
        self.assertAlmostEqual(aa_index.elo_normalize(500), 0.0)
        self.assertAlmostEqual(aa_index.elo_normalize(1000), 0.25)  # Briefcase anchor
        self.assertAlmostEqual(aa_index.elo_normalize(1600), 0.55)  # GDPval v2.1 anchor
        self.assertAlmostEqual(aa_index.elo_normalize(1824), 0.662)
        self.assertAlmostEqual(aa_index.elo_normalize(2500), 1.0)   # clamped
        self.assertAlmostEqual(aa_index.elo_normalize(100), 0.0)    # clamped

    def test_legacy_aliases(self):
        self.assertAlmostEqual(aa_index.gdpval_normalize(1600), 0.55)
        self.assertAlmostEqual(aa_index.briefcase_normalize(1000), 0.25)

    def test_reconstruct_index_known_value(self):
        weights = {"A": 0.6, "B": 0.4}
        components = {"A": 0.5, "B": 1.0}
        index, contributions = aa_index.reconstruct_index(components, weights)
        self.assertAlmostEqual(index, 100 * (0.6 * 0.5 + 0.4 * 1.0))  # 70.0
        self.assertAlmostEqual(sum(contributions.values()), index)

    def test_reconstruct_index_missing_component_raises(self):
        with self.assertRaises(KeyError):
            aa_index.reconstruct_index({"A": 0.5}, {"A": 0.5, "B": 0.5})


class TestWeights432(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.weights = aa_index.load_weights(WEIGHTS_432)

    def test_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(self.weights.values()), 1.0, places=6)

    def test_weights_count(self):
        # 11 score components from 10 evaluations (Omniscience splits in 2).
        self.assertEqual(len(self.weights), 11)

    def test_category_mass(self):
        # Operative masses v4.3.2: Agents 30, Coding 20, General 30,
        # Scientific Reasoning 20 (= 100).
        categories = {}
        with open(WEIGHTS_432, newline="") as f:
            for row in csv.DictReader(f):
                categories[row["category"]] = (
                    categories.get(row["category"], 0.0) + float(row["weight"])
                )
        self.assertAlmostEqual(categories["Agents"], 0.30, places=6)
        self.assertAlmostEqual(categories["Coding"], 0.20, places=6)
        self.assertAlmostEqual(categories["General"], 0.30, places=6)
        self.assertAlmostEqual(categories["Scientific Reasoning"], 0.20, places=6)

    def test_expected_weights(self):
        expected = {
            "AA-Briefcase v1.1": 0.15,
            "GDPval-AA v2.1": 0.10,
            "AutomationBench-AA": 0.05,
            "Terminal-Bench 4.0": 0.10,
            "SciCode": 0.10,
            "Omniscience Accuracy": 0.10,
            "Omniscience Non-hallu": 0.05,
            "GDP.pdf": 0.10,
            "AA-LCR v1.1": 0.05,
            "HLE": 0.10,
            "CritPt": 0.10,
        }
        self.assertEqual(self.weights, expected)

    def test_models_matrix_schema(self):
        # The v4.3.2 matrix exists and carries the new columns (no rows yet).
        with open(MODELS_432, newline="") as f:
            header = next(csv.reader(f))
        for col in [
            "elo_briefcase", "elo_gdpval", "automationbench_aa",
            "terminal_bench_40", "gdp_pdf", "aa_lcr_11",
        ]:
            self.assertIn(col, header)
        rows = aa_index.load_models(MODELS_432)
        self.assertIsInstance(rows, list)

    def test_template_json_reconstructs(self):
        data = aa_index.load_model_json(REPO_ROOT / "examples" / "v4.3.2-template.json")
        row = {k: "" if v is None else str(v) for k, v in data.items()}
        if "index_aa" not in row and data.get("published_index_aa") is not None:
            row["index_aa"] = str(data["published_index_aa"])
        components = aa_index.model_row_to_components(row)
        index, contributions = aa_index.reconstruct_index(components, self.weights)
        # All s = 0.5 except Elos: briefcase 1000 -> 0.25, gdpval 1600 -> 0.55.
        # 100 * (0.15*0.25 + 0.10*0.55 + 0.75*0.5) = 46.75
        self.assertAlmostEqual(index, 46.75, places=6)
        self.assertAlmostEqual(sum(contributions.values()), index)

    def test_all_deltas_within_tolerance(self):
        # The core claim: max |Delta| <= 1.0 on all 29 models, bands 14-58.
        weights = aa_index.load_weights(WEIGHTS_432)
        for row in aa_index.load_models(MODELS_432):
            components = aa_index.model_row_to_components(row)
            index, _ = aa_index.reconstruct_index(components, weights)
            self.assertLessEqual(
                abs(index - float(row["index_aa"])), 1.0,
                msg=f"{row['model']}: |Delta| exceeds lock threshold 1.0",
            )

    def test_max_abs_delta_is_012(self):
        # Exact recomputation over the 29-model matrix: max |Delta| = 0.12
        # (Qwen3.8 Max / GLM-5.3); most rows match to <= 0.06.
        weights = aa_index.load_weights(WEIGHTS_432)
        deltas = []
        for row in aa_index.load_models(MODELS_432):
            components = aa_index.model_row_to_components(row)
            index, _ = aa_index.reconstruct_index(components, weights)
            deltas.append(abs(index - float(row["index_aa"])))
        self.assertAlmostEqual(max(deltas), 0.12, delta=0.011)

    def test_kimi_k432_json_matches_matrix(self):
        data = aa_index.load_model_json(REPO_ROOT / "examples" / "kimi-k3-v4.3.2.json")
        row = {k: "" if v is None else str(v) for k, v in data.items()}
        if "index_aa" not in row and data.get("published_index_aa") is not None:
            row["index_aa"] = str(data["published_index_aa"])
        weights = aa_index.load_weights(WEIGHTS_432)
        components = aa_index.model_row_to_components(row)
        index, _ = aa_index.reconstruct_index(components, weights)
        self.assertAlmostEqual(index, 43.55, delta=0.011)

    def test_json_output_shape(self):
        rows = aa_index.load_models(MODELS_432)
        payload = json.loads(aa_index.to_json(rows, self.weights))
        self.assertEqual(payload["weights_version"], "v4.3.2")
        self.assertEqual(len(payload["models"]), 29)
        self.assertLessEqual(payload["max_abs_delta"], 1.0)


class TestLegacy411Archive(unittest.TestCase):
    """The v4.1.1 reproduction is frozen, not deleted."""

    @classmethod
    def setUpClass(cls):
        cls.weights = aa_index.load_weights(LEGACY_WEIGHTS)
        cls.rows = aa_index.load_models(LEGACY_MODELS)

    def test_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(self.weights.values()), 1.0, places=6)

    def test_weights_count(self):
        self.assertEqual(len(self.weights), 10)

    def test_matrix_has_8_models_with_all_components(self):
        self.assertEqual(len(self.rows), 8)
        for row in self.rows:
            components = aa_index.model_row_to_components(row)
            for component in self.weights:
                self.assertIn(component, components, f"{row['model']}: missing {component}")

    def test_published_deltas_match_bilan(self):
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
        deltas = []
        for row in self.rows:
            components = aa_index.model_row_to_components(row)
            index, _ = aa_index.reconstruct_index(components, self.weights)
            deltas.append(abs(index - float(row["index_aa"])))
        self.assertAlmostEqual(max(deltas), 0.30, delta=0.011)

    def test_json_output_shape(self):
        payload = json.loads(aa_index.to_json(self.rows, self.weights))
        # to_json stamps the *code* version, not the weights file version.
        self.assertEqual(payload["weights_version"], "v4.3.2")
        self.assertEqual(len(payload["models"]), 8)

    def test_legacy_examples_still_reconstruct(self):
        for name, published, target in [
            ("claude-opus-5.json", 63.05, 62.75),
            ("kimi-k3.json", 59.70, 59.70),
        ]:
            data = aa_index.load_model_json(REPO_ROOT / "examples" / name)
            row = {k: "" if v is None else str(v) for k, v in data.items()}
            components = aa_index.model_row_to_components(row)
            index, _ = aa_index.reconstruct_index(components, self.weights)
            self.assertAlmostEqual(index, target, delta=0.011)


if __name__ == "__main__":
    unittest.main()
