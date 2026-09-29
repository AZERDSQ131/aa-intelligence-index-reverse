# Contributing to aa-intelligence-index-reverse

Thank you for helping validate and extend the reconstruction. The project's
one rule is: **source or it didn't happen.**

## Adding a model (the most useful contribution)

1. Get the 10 component scores from the publicly displayed charts on
   [artificialanalysis.ai](https://artificialanalysis.ai/models)
   (the model's page shows each benchmark score; GDPval-AA is an Elo).
2. Note the **date** of your reading and the **URL** of the model page.
3. Add **one row** to [`data/models.csv`](data/models.csv):
   - `elo_gdpval`: the GDPval-AA Elo (e.g. `1824`) — the calculator
     normalizes it;
   - the 9 other components as `s` in `[0, 1]` (percentage ÷ 100);
   - `index_aa`: the Index value displayed by AA at the same date;
   - leave `delta` and `delta_bilan` empty — the tests compute `delta`;
   - `dump_date`: `YYYY-MM-DD`.
4. Run the verification:

   ```bash
   python src/aa_index.py --all
   python -m unittest discover -s tests
   ```

5. Open a PR titled `Add <model name> (<variant>) [v4.3.2]` with the URL + date in
   the description.

**Priority:** the first complete 11-component dump — any model. A mismatch is
welcome too: it falsifies the extrapolation and will be documented in
`docs/methodology.md`.

## Priority: first v4.3.2 validation

The v4.3.2 weights + calculator ship without a single full public dump yet.
The first PR that adds a complete 11-component row (any Index band) is the
single most valuable contribution right now. Note: if it does **not** match,
that is still a valuable PR — it falsifies the extrapolation and we will
document it in `docs/methodology.md`.

## Archived v4.1.1 data (frozen)

`data/models.csv`, `data/weights_v4.1.1.csv` and `examples/claude-opus-5.json` /
`examples/kimi-k3.json` reproduce the 8-model band ~56–63 and must not be
edited except to fix a proven transcription error (open an issue first with
URL + date). Verify them with:

```bash
python src/aa_index.py --all --weights data/weights_v4.1.1.csv --models data/models.csv
```

## Correcting an existing row

- Open an issue first with the URL + date supporting the correction.
- Never edit a `sᵢ` value without updating `dump_date`.

## Reporting a methodology change

If AA ships new weights (v4.4, v5…):

- Do **not** edit `data/weights_v4.3.2.csv` (nor `data/weights_v4.1.1.csv`).
- Add a new `data/weights_v4.x.y.csv` + update the source links, and open an
  issue titled `Methodology update: vX.Y.Z`.

## Code changes

- Stdlib only — no third-party dependencies.
- `python -m unittest discover -s tests` must pass.
- Keep the CLI output stable: tests and README embed it.

## PR checklist

- [ ] Every new data row carries a source URL and a dump date (v4.3.2 rows: `source` + `dump_date`)
- [ ] `python src/aa_index.py --all` (+ archived v4.1.1 `--all` if touched) output included in the PR description
- [ ] Tests pass locally
- [ ] No scraped raw HTML, no paywalled or private data — public chart
      readings only
