#!/usr/bin/env python3
"""Reconstruct the Artificial Analysis Intelligence Index from public component scores.

Formula (methodology v4.1.1, published by Artificial Analysis):

    Index = 100 * sum_i (w_i * s_i),   with sum(w_i) = 1 and s_i in [0, 1]

Ten components enter the Index. Nine of them are pass@1 style scores
(their s_i is simply the published percentage divided by 100). One of them,
GDPval-AA, is an Elo rating and needs a dedicated normalization:

    s_GDPval = clamp((Elo - 500) / 2000, 0, 1)      # human Elo anchored at 1000

Usage:
    python src/aa_index.py --all
    python src/aa_index.py --model "Kimi K3"
    python src/aa_index.py --model examples/kimi-k3.json
    python src/aa_index.py --all --json

No third-party dependencies: standard library only (Python >= 3.9).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

WEIGHTS_VERSION = "v4.1.1"

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WEIGHTS_CSV = REPO_ROOT / "data" / "weights_v4.1.1.csv"
DEFAULT_MODELS_CSV = REPO_ROOT / "data" / "models.csv"

# GDPval-AA normalization: s = clamp((Elo - 500) / 2000, 0, 1)
GDPVAL_COMPONENT = "GDPval-AA"
GDPVAL_OFFSET = 500.0
GDPVAL_SCALE = 2000.0

# Mapping: column name in data/models.csv -> component name in weights CSV.
# Order matters for display only; the math is a plain weighted sum.
COLUMN_TO_COMPONENT = {
    "terminal_bench_21": "Terminal-Bench 2.1",
    "tau3_banking": "tau3-Banking",
    "hle": "HLE",
    "omniscience_accuracy": "Omniscience Accuracy",
    "omniscience_non_hallu": "Omniscience Non-hallu",
    "scicode": "SciCode",
    "gpqa": "GPQA",
    "critpt": "CritPt",
    "aa_lcr": "AA-LCR",
}


# --------------------------------------------------------------------------
# Core math
# --------------------------------------------------------------------------

def clamp01(value: float) -> float:
    """Clamp a value into the [0, 1] interval."""
    return max(0.0, min(1.0, value))


def gdpval_normalize(elo: float) -> float:
    """Convert a GDPval-AA Elo rating into an s in [0, 1].

    Example: an Elo of 1824 gives s = (1824 - 500) / 2000 = 0.662.
    """
    return clamp01((elo - GDPVAL_OFFSET) / GDPVAL_SCALE)


def load_weights(path: Path = DEFAULT_WEIGHTS_CSV) -> dict[str, float]:
    """Load the component weights from data/weights_v4.1.1.csv.

    Raises ValueError if the weights do not sum to ~1.
    """
    weights: dict[str, float] = {}
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            weights[row["component"]] = float(row["weight"])

    total = sum(weights.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(
            f"Weights must sum to 1.0, got {total:.6f} (from {path}). "
            "Check data/weights_v4.1.1.csv against the methodology page."
        )
    return weights


def model_row_to_components(row: dict[str, str]) -> dict[str, float]:
    """Convert one row of data/models.csv into {component: s} with s in [0, 1].

    The GDPval column holds an Elo rating and is normalized with
    gdpval_normalize(); every other column is already an s in [0, 1].
    """
    components: dict[str, float] = {}
    elo = row.get("elo_gdpval")
    if elo not in (None, ""):
        components[GDPVAL_COMPONENT] = gdpval_normalize(float(elo))
    for column, component in COLUMN_TO_COMPONENT.items():
        value = row.get(column)
        if value not in (None, ""):
            components[component] = float(value)
    return components


def reconstruct_index(
    components: dict[str, float], weights: dict[str, float]
) -> tuple[float, dict[str, float]]:
    """Compute the reconstructed Index = 100 * sum(w_i * s_i).

    Returns (index, contributions) where contributions maps each component
    to 100 * w_i * s_i, so the breakdown sums exactly to the index.

    Raises KeyError if a weighted component is missing from `components`.
    """
    contributions: dict[str, float] = {}
    for component, weight in weights.items():
        if component not in components:
            raise KeyError(
                f"Missing component '{component}' — cannot reconstruct the Index. "
                "Provide all 10 components (see data/models.csv for the format)."
            )
        contributions[component] = 100.0 * weight * components[component]
    return sum(contributions.values()), contributions


# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------

def load_models(path: Path = DEFAULT_MODELS_CSV) -> list[dict[str, str]]:
    """Load the model matrix from data/models.csv."""
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_model_json(path: Path) -> dict[str, float]:
    """Load a single model's component scores from a JSON file.

    Accepted format (see examples/claude-opus-5.json):

        {
          "model": "Claude Opus 5 (max)",
          "elo_gdpval": 1824,
          "terminal_bench_21": 0.891, ...
        }

    Keys use the same names as the columns of data/models.csv.
    """
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object at top level.")
    return data


# --------------------------------------------------------------------------
# Display
# --------------------------------------------------------------------------

def display_name(row: dict[str, str]) -> str:
    """"Claude Opus 5" + "max" -> "Claude Opus 5 (max)". """
    variant = row.get("variant") or ""
    return f"{row['model']} ({variant})" if variant else row["model"]


def print_summary(rows: list[dict[str, str]], weights: dict[str, float]) -> None:
    """Print the verification table: reconstructed Index vs published Index."""
    print(f"Reconstructed AA Intelligence Index — weights {WEIGHTS_VERSION}")
    print("-" * 78)
    print(f"{'Model':<26}{'Reconstr.':>10}{'AA publ.':>10}{'Delta':>8}{'|Delta|':>9}")
    print("-" * 78)

    deltas: list[float] = []
    for row in rows:
        components = model_row_to_components(row)
        index, _ = reconstruct_index(components, weights)
        published = float(row["index_aa"])
        delta = index - published
        deltas.append(delta)
        flag = "" if abs(delta) <= 1.0 else "  <-- OUT OF TOLERANCE"
        print(
            f"{display_name(row):<26}{index:>10.2f}{published:>10.2f}"
            f"{delta:>8.2f}{abs(delta):>9.2f}{flag}"
        )

    print("-" * 78)
    print(
        f"{len(rows)} models · max |Delta| = {max(abs(d) for d in deltas):.2f}"
        " · internal lock threshold = 1.00"
    )


def print_detail(
    row: dict[str, str], weights: dict[str, float], components: dict[str, float]
) -> None:
    """Print the full per-component breakdown for one model."""
    index, contributions = reconstruct_index(components, weights)
    published = float(row["index_aa"])

    print(f"{display_name(row)} — weights {WEIGHTS_VERSION}")
    print("-" * 64)
    print(f"{'Component':<24}{'weight':>8}{'s':>8}{'contribution':>14}")
    print("-" * 64)
    for component, weight in weights.items():
        print(
            f"{component:<24}{weight:>8.2f}{components[component]:>8.3f}"
            f"{contributions[component]:>14.3f}"
        )
    print("-" * 64)
    print(f"{'Reconstructed Index':<24}{'':>8}{'':>8}{index:>14.2f}")
    print(f"{'AA published Index':<24}{'':>8}{'':>8}{published:>14.2f}")
    print(f"{'Delta (reconstr - AA)':<24}{'':>8}{'':>8}{index - published:>14.2f}")


def to_json(rows: list[dict[str, str]], weights: dict[str, float]) -> str:
    """Serialize the verification of every model as JSON."""
    results = []
    for row in rows:
        components = model_row_to_components(row)
        index, contributions = reconstruct_index(components, weights)
        published = float(row["index_aa"])
        results.append(
            {
                "model": display_name(row),
                "reconstructed_index": round(index, 4),
                "published_index": published,
                "delta": round(index - published, 4),
                "components": {c: round(s, 4) for c, s in components.items()},
                "contributions": {c: round(v, 4) for c, v in contributions.items()},
                "dump_date": row.get("dump_date", ""),
            }
        )
    max_abs_delta = max(abs(r["delta"]) for r in results)
    return json.dumps(
        {
            "weights_version": WEIGHTS_VERSION,
            "max_abs_delta": round(max_abs_delta, 4),
            "tolerance": 1.0,
            "models": results,
        },
        indent=2,
        ensure_ascii=False,
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct the Artificial Analysis Intelligence Index "
            f"(methodology {WEIGHTS_VERSION}) from public component scores."
        )
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument(
        "--all",
        action="store_true",
        help="verify every model in data/models.csv",
    )
    target.add_argument(
        "--model",
        metavar="NAME_OR_JSON",
        help=(
            'either a model name from data/models.csv (e.g. "Kimi K3") '
            "or a path to a JSON file with component scores "
            "(see examples/ for the format)"
        ),
    )
    parser.add_argument(
        "--json", action="store_true", help="machine-readable JSON output"
    )
    parser.add_argument(
        "--weights",
        type=Path,
        default=DEFAULT_WEIGHTS_CSV,
        help="path to the weights CSV (default: data/weights_v4.1.1.csv)",
    )
    parser.add_argument(
        "--models",
        type=Path,
        default=DEFAULT_MODELS_CSV,
        help="path to the models CSV (default: data/models.csv)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    weights = load_weights(args.weights)

    if args.all:
        rows = load_models(args.models)
        if args.json:
            print(to_json(rows, weights))
        else:
            print_summary(rows, weights)
        return 0

    # --model: either a JSON file or a model name from data/models.csv
    candidate = Path(args.model)
    if candidate.suffix == ".json" and candidate.exists():
        data = load_model_json(candidate)
        row = {key: ("" if value is None else str(value)) for key, value in data.items()}
        # examples/*.json use "published_index_aa"; the CSV column is "index_aa".
        if "index_aa" not in row and data.get("published_index_aa") is not None:
            row["index_aa"] = str(data["published_index_aa"])
    else:
        matches = [
            row
            for row in load_models(args.models)
            if row["model"].lower() == args.model.lower()
            or display_name(row).lower() == args.model.lower()
        ]
        if not matches:
            print(f"error: model not found in {args.models}: {args.model}", file=sys.stderr)
            return 1
        if len(matches) > 1:
            names = ", ".join(sorted(display_name(r) for r in matches))
            print(
                f"error: ambiguous model name, use one of: {names}",
                file=sys.stderr,
            )
            return 1
        row = matches[0]

    components = model_row_to_components(row)
    if args.json:
        index, contributions = reconstruct_index(components, weights)
        published = row.get("index_aa")
        print(
            json.dumps(
                {
                    "model": row.get("model", ""),
                    "reconstructed_index": round(index, 4),
                    "published_index": float(published) if published else None,
                    "components": {c: round(s, 4) for c, s in components.items()},
                    "contributions": {c: round(v, 4) for c, v in contributions.items()},
                },
                indent=2,
            )
        )
    else:
        print_detail(row, weights, components)
    return 0


if __name__ == "__main__":
    sys.exit(main())
