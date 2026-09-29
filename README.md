# aa-intelligence-index-reverse

An **independent, community reconstruction** of the scoring formula behind the
[Artificial Analysis Intelligence Index](https://artificialanalysis.ai/methodology/intelligence-benchmarking)
(methodology v4.1.1) — with code and data that let you **verify it yourself in
under a minute**.

> **Not affiliated with Artificial Analysis.** Weights © Artificial Analysis
> (CC BY 4.0); reconstruction, code and commentary: MIT. See [NOTICE](NOTICE).

---

## The result, in one table

`Index = 100 × Σ (wᵢ × sᵢ)` over 10 components, with GDPval-AA Elo normalized
as `s = clamp((Elo − 500) / 2000)`.

Recomputing the Index from **publicly displayed component scores** reproduces
the published value for all 8 models tested, within the chart-reading margin:

```
Model                      Reconstr.  AA publ.   Delta  |Delta|
------------------------------------------------------------------------------
Claude Opus 5 (max)            62.75     63.05   -0.30     0.30
Grok 4.6 (high)                60.68     60.92   -0.24     0.24
Kimi K3 (max)                  59.70     59.70    0.00     0.00
GLM-5.3 (max)                  59.39     59.51   -0.12     0.12
Qwen3.8 2.4T                   57.65     57.70   -0.05     0.05
GLM-5.3-Flash                  57.38     57.46   -0.08     0.08
Muse Spark 1.2                 56.59     56.76   -0.17     0.17
Gemini 3.7 Flash               55.94     56.03   -0.09     0.09
------------------------------------------------------------------------------
8 models · max |Delta| = 0.30 · internal lock threshold = 1.00
```

*(Exact output of `python src/aa_index.py --all`. Hand-rounded values recorded
during the original analysis differ by ≤ 0.02; see [docs/methodology.md](docs/methodology.md).)*

## What is validated — and what is not

| | |
|---|---|
| ✅ **Validated** | Formula + weights v4.1.1 on the **Index band ~56–63** (8 models, max \|Δ\| 0.30) |
| ❌ **Not yet** | **Out-of-band** models (e.g. Index ~30) — component dumps unavailable at analysis time |
| ❌ **Out of scope** | Speed and cost: they are **separate axes** on AA, not part of the Index |

All deltas are ≤ 0 — consistent with rounding noise in the public component
scores, **not** with a structural formula error.

## Quickstart

No dependencies. Python ≥ 3.9.

```bash
# 1. Verify all 8 models against the published Index
python src/aa_index.py --all

# 2. Full per-component breakdown for one model (from data/models.csv)
python src/aa_index.py --model "Kimi K3"

# 3. Compute the Index from your own component dump (JSON)
python src/aa_index.py --model examples/claude-opus-5.json

# 4. Machine-readable output
python src/aa_index.py --all --json
```

### Example: a worked component breakdown

`python src/aa_index.py --model examples/kimi-k3.json` prints the full
contribution of each benchmark:

```
Component                 weight       s  contribution
----------------------------------------------------------------
GDPval-AA                   0.20   0.584        11.680
Terminal-Bench 2.1          0.16   0.850        13.600
tau3-Banking                0.14   0.460         6.440
HLE                         0.12   0.469         5.628
Omniscience Accuracy        0.08   0.476         3.808
Omniscience Non-hallu       0.04   0.468         1.872
SciCode                     0.08   0.587         4.696
GPQA                        0.06   0.935         5.610
CritPt                      0.06   0.234         1.404
AA-LCR                      0.06   0.827         4.962
----------------------------------------------------------------
Reconstructed Index                              59.70
AA published Index                               59.70
Delta (reconstr - AA)                             0.00
```

Kimi K3 is an **exact match** — a good sanity check that the formula and the
GDPval Elo normalization are right.

### Example: computing from your own JSON dump

```jsonc
// examples/claude-opus-5.json — same keys as data/models.csv columns
{
  "model": "Claude Opus 5",
  "variant": "max",
  "source": "https://artificialanalysis.ai/models — chart dump 2026-09-01",
  "elo_gdpval": 1824,              // normalized: (1824-500)/2000 = 0.662
  "terminal_bench_21": 0.891,      // all other scores are s in [0, 1]
  "tau3_banking": 0.421,
  "hle": 0.549,
  "omniscience_accuracy": 0.609,
  "omniscience_non_hallu": 0.392,
  "scicode": 0.557,
  "gpqa": 0.932,
  "critpt": 0.291,
  "aa_lcr": 0.757,
  "published_index_aa": 63.05
}
```

Add a model the same way → one CSV row / one JSON file + a PR
(see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Repository layout

```
aa-intelligence-index-reverse/
├── README.md                  ← you are here (English)
├── README.fr.md               ← version française
├── LICENSE                    MIT + data-provenance notice
├── NOTICE                     non-affiliation, provenance, known limits
├── CITATION.cff               how to cite this reconstruction
├── CONTRIBUTING.md            how to add a model / a correction
├── data/
│   ├── weights_v4.1.1.csv     the 10 weights + categories + normalization
│   └── models.csv             sᵢ matrix for 8 models + published Index
├── src/
│   └── aa_index.py            stdlib-only calculator & verifier
├── tests/
│   └── test_aa_index.py       14 tests: formula, data files, reproduction
├── examples/                  JSON dumps ready to run
│   ├── claude-opus-5.json
│   └── kimi-k3.json
└── docs/
    └── methodology.md         full derivation, sources, discrepancies
```

## The weights (v4.3.2 — current)

| Component | Weight | Category |
|---|---|---|
| AA-Briefcase v1.1 | 15% | Agents |
| GDPval-AA v2.1 | 10% | Agents |
| AutomationBench-AA | 5% | Agents |
| Terminal-Bench 4.0 | 10% | Coding |
| SciCode | 10% | Coding |
| Omniscience Accuracy | 10% | General |
| GDP.pdf | 10% | General |
| Omniscience Non-hallu | 5% | General |
| AA-LCR v1.1 | 5% | General |
| HLE | 10% | Scientific Reasoning |
| CritPt | 10% | Scientific Reasoning |

Operative category masses: **Agents 30 · Coding 20 · Scientific Reasoning 20 · General 30**.
Both Elo ratings normalize as `s = clamp((Elo − 500) / 2000)`; Briefcase anchored
at GPT-5.5 (medium) = 1000, GDPval v2.1 at DeepSeek V4.1 Flash (max) = 1600.

<details>
<summary>Archived weights (v4.1.1)</summary>

| Component | Weight | Category |
|---|---|---|
| GDPval-AA | 20% | Agents |
| Terminal-Bench 2.1 | 16% | Coding |
| τ³-Banking | 14% | Agents |
| HLE | 12% | Scientific |
| Omniscience Accuracy | 8% | General |
| Omniscience Non-hallu | 4% | General |
| SciCode | 8% | Scientific |
| GPQA | 6% | Scientific |
| CritPt | 6% | Scientific |
| AA-LCR | 6% | General |

Operative category masses: **Agents 34 · Scientific 32 · Coding 16 · General 18**.
(Some AA summary materials annotate Coding/Scientific as 24/24; those labels do
not match the operative per-component weights — details in
[docs/methodology.md](docs/methodology.md).)

> The AA FAQ's older "4 pillars × 25%" description is **outdated**; the v4.3.2
> methodology table is authoritative.

## Testing

```bash
python -m unittest discover -s tests -v
```

20 tests: Elo anchors (both v4.3.2 components), v4.3.2 weights sum + category
masses + template reconstruction (46.75), and — frozen — the **v4.1.1
reproduction for all 8 archived models**. CI runs the same suite on every push
([.github/workflows/ci.yml](.github/workflows/ci.yml)) plus both `--all`
verifications.

## Why this exists

Artificial Analysis publishes the Index and its methodology, but **no public
tool recomputes the Index end-to-end** from component scores (their
[Stirrup](https://github.com/ArtificialAnalysis/Stirrup) is an agent harness,
not an Index calculator). This repo fills that gap so that:

- anyone can check that a model's published Index matches its component scores;
- researchers can propagate new component dumps into the Index immediately;
- methodology changes (AA re-weights periodically) can be tracked as
  versioned weights files (`weights_v4.x.y.csv`).

## Roadmap

- [ ] **v0.2 — first v4.3.2 dump**: add ≥ 1 model with all **11 components**
  + Index + URL + date (the single most valuable contribution right now;
  a mismatch is welcome too — it falsifies the extrapolation).
- [ ] Data files for additional tracked models (v4.3.2 schema).
- [x] ~~A `--weights` version switch once AA ships a v4.2~~ — done: `--weights`/
  `--models` flags ship, v4.3.2 is the default, v4.1.1 archived.

## Contributing

PRs welcome — the bar is **source or it didn't happen**: every new row must
carry the AA dump URL and date. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citing

See [CITATION.cff](CITATION.cff), or:
</details>


```bibtex
@software{jules_2026_aa_index_reverse,
  author  = {Jules},
  title   = {aa-intelligence-index-reverse: independent reconstruction of the
             Artificial Analysis Intelligence Index formula (v4.3.2, v4.1.1 archived)},
  year    = {2026},
  url     = {https://github.com/AZERDSQ131/aa-intelligence-index-reverse}
}
```

## License

Code: MIT. Benchmark weights and methodology: © Artificial Analysis, CC BY 4.0.
Not affiliated with or endorsed by Artificial Analysis or any model provider —
see [NOTICE](NOTICE).
