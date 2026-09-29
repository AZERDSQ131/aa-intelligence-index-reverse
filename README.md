# aa-intelligence-index-reverse

An **independent, community reconstruction** of the scoring formula behind the
[Artificial Analysis Intelligence Index](https://artificialanalysis.ai/methodology/intelligence-benchmarking)
(methodology v4.3.2 — v4.1.1 kept as archive) — with code and data that let you **verify it yourself in
under a minute**.

> **Not affiliated with Artificial Analysis.** Weights © Artificial Analysis
> (CC BY 4.0); reconstruction, code and commentary: MIT. See [NOTICE](NOTICE).
> **Status 2026-09-29:** calculator + weights + data at **v4.3.2** — **29 models
> reproduce the published Index with max |Δ| = 0.12** (bands ~14–58, incl.
> out-of-band low-Index models). The v4.1.1 8-model reproduction is archived
> below and still passes via `--weights data/weights_v4.1.1.csv
> --models data/models.csv`.

---

## The result, in one table (v4.3.2)

`Index = 100 × Σ (wᵢ × sᵢ)` over **11 components**, with both Elo ratings
(AA-Briefcase v1.1 + GDPval-AA v2.1) normalized as `s = clamp((Elo − 500) / 2000)`.

Recomputing the Index from the **public Index-page payload (2026-09-29)**
reproduces the published value for all 29 live models, from ~14 to ~58:

```
Model                                Reconstr.  AA publ.   Delta  |Delta|
----------------------------------------------------------------------------------------
Claude Opus 5.5 (max with fallback)      57.62     57.62    0.00     0.00
Claude Opus 5.5 (xhigh with fallback)     55.98     55.99   -0.01     0.01
Claude Sonnet 5.5 (max with fallback)     55.98     55.98   -0.00     0.00
Claude Opus 5.5 (high with fallback)     53.58     53.58    0.00     0.00
Claude Fable 5.1 (max with fallback)     53.35     53.35    0.00     0.00
Claude Fable 5.1 (xhigh with fallback)     53.20     53.20    0.00     0.00
GPT-6 Astra (max)                        52.67     52.67    0.00     0.00
GPT-6 Astra (xhigh)                      52.39     52.39   -0.00     0.00
Claude Sonnet 5.5 (xhigh with fallback)     51.85     51.85    0.00     0.00
Muse Spark 1.3 (max)                     48.01     48.09   -0.08     0.08
GPT-6 Sol (max)                          47.53     47.53   -0.00     0.00
Grok 4.7 (xhigh)                         46.45     46.45   -0.00     0.00
MiMo-V2.6-Pro                            46.28     46.32   -0.04     0.04
Qwen3.8 Max (0902)                       45.30     45.42   -0.12     0.12
GLM-5.3 (max)                            44.66     44.78   -0.12     0.12
Step 5 Preview                           43.73     43.73   -0.00     0.00
Kimi K3 (max)                            43.55     43.59   -0.04     0.04
GLM-5.3-Flash                            41.75     41.81   -0.06     0.06
Gemini 3.8 Flash (high)                  40.93     40.93   -0.00     0.00
DeepSeek V4.1 Flash (max)                39.40     39.46   -0.06     0.06
GPT-6 Luna (max)                         37.26     37.26   -0.00     0.00
Qwen3.8 27B (xhigh)                      33.66     33.70   -0.04     0.04
K2 Horizon 375B A23B                     30.44     30.50   -0.06     0.06
MiniMax-M3                               29.20     29.22   -0.02     0.02
Inkling                                  25.02     24.98    0.04     0.04
Nemotron 3 Ultra                         22.95     22.93    0.02     0.02
Gemini 3.5 Flash-Lite                    22.21     22.17    0.04     0.04
Muse Glimmer (high)                      17.48     17.48   -0.00     0.00
Mistral Medium 3.5                       14.23     14.19    0.04     0.04
----------------------------------------------------------------------------------------
29 models · max |Delta| = 0.12 · internal lock threshold = 1.00
```

*(Exact output of `python src/aa_index.py --all`.)*

<details>
<summary>Archived result (v4.1.1, 8 models, band ~56–63)</summary>

`Index = 100 × Σ (wᵢ × sᵢ)` over 10 components, with GDPval-AA Elo normalized
as `s = clamp((Elo − 500) / 2000)`.

Recomputing the Index from **publicly displayed component scores** reproduced
the published value for all 8 models tested, within the chart-reading margin.
The v4.3.2 formula is the same weighted mean over **11 components**, with the
same Elo mapping `clamp((Elo − 500) / 2000)` applied to **two** Elo ratings
(AA-Briefcase v1.1 + GDPval-AA v2.1) — see [docs/methodology.md](docs/methodology.md) §0.

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

*(Exact output of `python src/aa_index.py --all --weights data/weights_v4.1.1.csv --models data/models.csv`. Hand-rounded values recorded
during the original analysis differ by ≤ 0.02; see [docs/methodology.md](docs/methodology.md).)*

## What is validated — and what is not

| | |
|---|---|
| ✅ **Validated (archive)** | Formula + weights v4.1.1 on the **Index band ~56–63** (8 models, max \|Δ\| 0.30) |
| ❌ **Out of scope** | Speed and cost: they are **separate axes** on AA, not part of the Index |

All deltas are ≤ 0 — consistent with rounding noise in the public component
scores, **not** with a structural formula error.

## Quickstart

No dependencies. Python ≥ 3.9.

```bash
# 1. Verify all 29 models against the published Index (v4.3.2)
python src/aa_index.py --all

# 2. Full per-component breakdown for one model
python src/aa_index.py --model "Kimi K3"

# 3. Archived v4.1.1 verification (8 models, still green)
python src/aa_index.py --all --weights data/weights_v4.1.1.csv --models data/models.csv

# 4. Compute the Index from your own v4.3.2 component dump (JSON)
python src/aa_index.py --model examples/kimi-k3-v4.3.2.json

# 5. Machine-readable output
python src/aa_index.py --all --json
```

### Example: a worked component breakdown

`python src/aa_index.py --model examples/kimi-k3-v4.3.2.json` prints the full
contribution of each benchmark (v4.3.2):

```
Component                 weight       s  contribution
----------------------------------------------------------------
AA-Briefcase v1.1           0.15   0.503         7.539
GDPval-AA v2.1              0.10   0.512         5.120
AutomationBench-AA          0.05   0.583         2.914
Terminal-Bench 4.0          0.10   0.126         1.263
SciCode                     0.10   0.595         5.949
Omniscience Accuracy        0.10   0.476         4.758
Omniscience Non-hallu       0.05   0.468         2.340
GDP.pdf                     0.10   0.220         2.200
</details>

AA-LCR v1.1                 0.05   0.887         4.433
HLE                         0.10   0.469         4.690
CritPt                      0.10   0.234         2.343
----------------------------------------------------------------
Reconstructed Index                              43.55
AA published Index                               43.59
Delta (reconstr - AA)                            -0.04
```

<details>
<summary>Archived example (v4.1.1 — Kimi K3 exact match)</summary>

`python src/aa_index.py --model examples/kimi-k3.json --weights data/weights_v4.1.1.csv --models data/models.csv` prints the full
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
GDPval Elo normalization are right. (Archived v4.1.1 example; v4.3.2 dumps
use `examples/kimi-k3-v4.3.2.json`.)

</details>

### Example: computing from your own JSON dump

```jsonc
// examples/v4.3.2-template.json — same keys as data/models_v4.3.2.csv columns
{
  "model": "Example Model",
  "variant": "max",
  "source": "https://artificialanalysis.ai/models — chart dump YYYY-MM-DD",
  "elo_briefcase": 1000,         // normalized: (1000-500)/2000 = 0.25
  "elo_gdpval": 1600,            // normalized: (1600-500)/2000 = 0.55
  "automationbench_aa": 0.5,     // all other scores are s in [0, 1]
  "terminal_bench_40": 0.5,
  "scicode": 0.5,
  "omniscience_accuracy": 0.5,
  "omniscience_non_hallu": 0.5,
  "gdp_pdf": 0.5,                // All-pass share (headline metric)
  "aa_lcr_11": 0.5,
  "hle": 0.5,
  "critpt": 0.5,
  "published_index_aa": 50.0
}
```

Legacy v4.1.1 dumps (`examples/claude-opus-5.json`, `examples/kimi-k3.json`)
keep working with `--weights data/weights_v4.1.1.csv --models data/models.csv`.

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
│   ├── weights_v4.3.2.csv     the 11 v4.3.2 weights (current default)
│   ├── models_v4.3.2.csv      v4.3.2 sᵢ matrix (29 models, 2026-09-29)
│   ├── weights_v4.1.1.csv     archived v4.1.1 weights
│   └── models.csv             archived v4.1.1 matrix (8 models)
├── src/
│   └── aa_index.py            stdlib-only calculator & verifier
├── tests/
│   └── test_aa_index.py       23 tests: formula, v4.3.2 matrix, v4.1.1 archive
├── examples/                  JSON dumps ready to run
│   ├── v4.3.2-template.json
│   ├── kimi-k3-v4.3.2.json    (real v4.3.2 dump: Kimi K3, Δ −0.04)
│   ├── kimi-k3-v4.3.2.json    (real v4.3.2 dump: Kimi K3, Δ −0.04)
│   ├── claude-opus-5.json     (v4.1.1 archive)
│   └── kimi-k3.json           (v4.1.1 archive)
└── docs/
    └── methodology.md         §0 v4.3.2 + §§2-3 v4.1.1 archive
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

</details>

## Testing

```bash
python -m unittest discover -s tests -v
```

23 tests: Elo anchors (both v4.3.2 components), v4.3.2 weights sum + category
masses + template reconstruction (46.75) + **29-model v4.3.2 reproduction
(max |Δ| = 0.12)**, and — frozen — the **v4.1.1 reproduction for all
8 archived models**. CI runs the same suite on every push
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

- [x] ~~First v4.3.2 dump~~ — done 2026-09-29: 29 models, max |Δ| = 0.12, bands ~14–58.
- [ ] Keep the matrix fresh as AA adds models / re-weights (new `weights_vX.csv`, never edit history).
- [ ] Data files for additional tracked models (v4.3.2 schema).
- [x] ~~A `--weights` version switch once AA ships a v4.2~~ — done: `--weights`/
  `--models` flags ship, v4.3.2 is the default, v4.1.1 archived.

## Contributing

PRs welcome — the bar is **source or it didn't happen**: every new row must
carry the AA dump URL and date. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citing

See [CITATION.cff](CITATION.cff), or:

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
