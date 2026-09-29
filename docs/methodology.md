# Methodology — reconstructing the AA Intelligence Index (v4.3.2, with v4.1.1 archive)

> **Current methodology: v4.3.2** (retrieved 2026-09-29). The v4.1.1 derivation
> below is kept as an archive (§2–§3 frozen; legacy files:
> `data/weights_v4.1.1.csv`, `data/models.csv`, `examples/claude-opus-5.json`,
> `examples/kimi-k3.json`). New dumps go to `data/models_v4.3.2.csv`
> (see `examples/v4.3.2-template.json`).

## 0. What changed in v4.3.2 (2026-09-29)

AA now versions the Index as **v4.3.2** with **10 evaluations / 11 score
components** (Omniscience splits into Accuracy 10% + Non-hallucination 5%)
and four categories **Agents 30 / Coding 20 / Scientific Reasoning 20 /
General 30**:

| # | Component (Index weight) | Category | Scoring → s |
|---|---|---|---|
| 1 | AA-Briefcase v1.1 — 15% | Agents | Elo → `clamp((Elo − 500) / 2000)`; anchored GPT-5.5 (medium) = 1000, frozen at model-addition time |
| 2 | GDPval-AA v2.1 — 10% | Agents | Elo → `clamp((Elo − 500) / 2000)`; anchored DeepSeek V4.1 Flash (max) = 1600, frozen at model-addition time |
| 3 | AutomationBench-AA — 5% | Agents | mean objective completion; 0 on guardrail violation / error |
| 4 | Terminal-Bench 4.0 — 10% | Coding | pass@1 over 3 repeats (66 tasks) |
| 5 | SciCode — 10% | Coding | pass@1, sub-problem scoring |
| 6 | Omniscience Accuracy — 10% | General | proportion correct (6000 q.) |
| 7 | Omniscience Non-hallu — 5% | General | `1 − hallucination rate` |
| 8 | GDP.pdf — 10% | General | **All-pass** share over 500 attempts (100 tasks × 5); Mean Pass is secondary |
| 9 | AA-LCR v1.1 — 5% | General | pass@1; v1.1 NOT comparable to v1.0 (prompt + 16 keys + judge changed) |
| 10 | HLE — 10% | Scientific Reasoning | pass@1 |
| 11 | CritPt — 10% | Scientific Reasoning | pass@1, challenge level (70 × 5 repeats) |

Formula unchanged: `Index = 100 × Σ (wᵢ × sᵢ)`, Σwᵢ = 1.
Old → new mapping: GDPval-AA (20%) splits into Briefcase 15% + GDPval v2.1
10% + AutomationBench 5% on the agent side; Terminal-Bench 2.1 (16%) →
Terminal-Bench 4.0 (10%) + SciCode held at 10%; τ³-Banking (14%) retired to
additional evals; GPQA (6%) retired in v4.2; AA-LCR (6%) → AA-LCR v1.1 (5%);
HLE 12% → 10%; CritPt held at 10%; Omniscience 8+4 → 10+5; new GDP.pdf 10%.

### Open point: GDP.pdf metric

AA reports two GDP.pdf numbers: headline **All-pass** (share of the 500
attempts where *every* criterion passes) and secondary task-macro **Mean
Pass** (mean criterion pass rate). The weights table lists both. This
reconstruction takes **All-pass** as `s` — it is the headline metric and the
closest analogue of pass@1 (an attempt counts iff fully correct). If a future
reproduction shows Mean Pass fits better, the weights note + code will be
updated and the change recorded here. Flag it in your PR if you test this.

### Validation status v4.3.2

No complete public component dump exists in this repo yet
(`data/models_v4.3.2.csv` is header-only). The calculator, weights file,
template (`examples/v4.3.2-template.json`, reconstructs 46.75 on all-0.5
inputs) and tests (20) are in place; the next step is ≥ 1 full 11-component
dump with Index + URL + date (see CONTRIBUTING.md). A mismatch is welcome
too — it falsifies the extrapolation and will be documented here.

This document is the full derivation behind the reconstruction. It records
what the formula is, where each number comes from, and every discrepancy we
found along the way.

Sources (published by Artificial Analysis):

- Methodology: <https://artificialanalysis.ai/methodology/intelligence-benchmarking>
- Index page: <https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index>
- v4.1 article: <https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-1>

All component scores were read from publicly displayed charts on
artificialanalysis.ai on **2026-09-01/02** (chart dumps, no raw-HTML
redistribution).

---

## 1. What the Index is — and is not

### It is

- A score of **pure intelligence** on a ~0–100 scale.
- A **weighted mean** of 9 public evals (10 score components).
- Formula: `Index = 100 × Σ (wᵢ × sᵢ)` with `Σ wᵢ = 1` and `sᵢ ∈ [0, 1]`.

### It is not

- Quality × speed × cost — those are **separate axes** on AA
  (tok/s, time-per-task, $/MTok, cost-per-task) and do **not** enter the Index.
- An officially recomputable score for a home-made model not tracked by AA
  (AA evaluates internally the models it tracks).

---

## 2. The formula — ARCHIVE (v4.1.1, superseded by §0 above)

| # | Component | Weight | Category | Normalization |
|---|---|---|---|---|
| 1 | GDPval-AA | 20% | Agents | Elo: `s = clamp((Elo − 500) / 2000, 0, 1)` |
| 2 | Terminal-Bench 2.1 | 16% | Coding | pass@1: `s = score% / 100` |
| 3 | τ³-Banking | 14% | Agents | pass@1 |
| 4 | HLE | 12% | Scientific | pass@1 |
| 5 | Omniscience Accuracy | 8% | General | pass@1 |
| 6 | Omniscience Non-hallu | 4% | General | pass@1 |
| 7 | SciCode | 8% | Scientific | pass@1 |
| 8 | GPQA | 6% | Scientific | pass@1 |
| 9 | CritPt | 6% | Scientific | pass@1 |
| 10 | AA-LCR | 6% | General | pass@1 |

Developed form:

```
Index ≈ 100 × (
  0.20·GDPval + 0.16·TB + 0.14·τ³ + 0.12·HLE
  + 0.08·OmniAcc + 0.04·NonHallu + 0.08·SciCode
  + 0.06·GPQA + 0.06·CritPt + 0.06·LCR
)
```

### GDPval-AA normalization

GDPval-AA is reported as an **Elo rating**, not a percentage. The
normalization that reproduces the published Index is:

```
s_GDPval = clamp((Elo − 500) / 2000, 0, 1)
```

The human anchor (Elo 1000) maps to `s = 0.25`.

### Category masses — a documented discrepancy

Summing the operative per-component weights gives:

| Category | Operative mass |
|---|---|
| Agents | 34% (0.20 + 0.14) |
| Scientific | 32% (0.12 + 0.08 + 0.06 + 0.06) |
| Coding | 16% (0.16) |
| General | 18% (0.08 + 0.04 + 0.06) |

Some AA summary materials annotate the categories as *Agents 34 / Coding 24 /
Scientific 24 / General 18*. Those labels **do not match** the operative
per-component weights (Coding 24 vs 16, Scientific 24 vs 32) — they appear to
be v4.0 leftovers. The operative weights above are the ones that reproduce
the published Index; that is the test that matters, and it is encoded in
`tests/test_aa_index.py`.

> Also outdated: the AA FAQ's "4 pillars × 25%" description. The v4.1.1
> methodology table is authoritative.

---

## 3. Evidence — ARCHIVE: 8-model reproduction v4.1.1 (band ~56–63)

Source of the `sᵢ`: chart dumps from AA (public display), **not** the
Multiverse blog. The full matrix ships as
[`data/models.csv`](../data/models.csv) with the dump date.

Reproduction results (exact recomputation):

| Model (AA variant) | Elo GDPval | Î reconstructed | Index AA | Δ |
|---|---|---|---|---|
| Claude Opus 5 (max) | 1824 | 62.75 | 63.05 | −0.30 |
| Grok 4.6 (high) | 1730 | 60.68 | 60.92 | −0.24 |
| Kimi K3 (max) | 1668 | 59.70 | 59.70 | 0.00 |
| GLM-5.3 (max) | 1758 | 59.39 | 59.51 | −0.12 |
| Qwen3.8 2.4T | 1718 | 57.65 | 57.70 | −0.05 |
| GLM-5.3-Flash | 1765 | 57.38 | 57.46 | −0.08 |
| Muse Spark 1.2 | 1615 | 56.59 | 56.76 | −0.17 |
| Gemini 3.7 Flash | 1516 | 55.94 | 56.03 | −0.09 |

**Max |Δ| = 0.30** (internal lock threshold = 1.0).

### Note on hand-recorded deltas

The original analysis (recorded in the internal bilan) hand-computed the
weighted sum from rounded intermediates and logged a max |Δ| of 0.31. Exact
recomputation from the same `sᵢ` matrix gives **0.30** (Opus 5: −0.30 exact
vs −0.31 hand-recorded; Grok: −0.24 vs −0.23). The difference is ≤ 0.02 and
changes nothing: the formula reproduces the Index within chart-reading
precision. Both values are preserved in `data/models.csv`
(`delta` = exact, `delta_bilan` = hand-recorded).

### Interpretation of the sign of Δ

All deltas are ≤ 0. If the formula were structurally wrong, we would expect
mixed signs. A systematic small negative bias is consistent with the public
component scores being displayed **rounded to 3 decimals** while the published
Index is computed from unrounded values — averaging 10 rounded-down-ish
components loses a small amount of mass. This is rounding noise, not a
formula hole.

### Elo ↔ variant mapping risk

Mapping a published Elo to the right model variant (e.g. "Grok 4.6 (high)")
was done by hand from AA's charts. A wrong mapping would fail loudly in the
recomputation of **that** row; the other rows would be unaffected. None failed.

---

## 4. Limits — do not oversell

- **Out-of-band models are NOT validated.** The reconstruction is proven only
  on the band ~56–63. Models around Index ~30 (e.g. smaller/cheaper models)
  could not be checked at analysis time because their component dumps were
  incomplete. Extending the validation is the top roadmap item.
- The GDPval normalization is inferred, not officially documented; it could
  differ for Elo values far outside the tested range (the clamp boundaries
  are untested).
- AA re-weights periodically. When a v4.2 (or v5) lands, add a new
  `weights_v4.x.y.csv` rather than editing history.

## 5. What this enables

- Verify any tracked model's published Index from public component scores.
- Immediately propagate new component dumps into Index estimates.
- Track methodology changes as versioned weights files.

## 6. Next step

Add **≥ 1 low-Index (~30) model** with a complete dump of all 10 `sᵢ` to
extend validation out of band.
