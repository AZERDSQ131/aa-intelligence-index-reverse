# aa-intelligence-index-reverse

Une **reconstruction indépendante et communautaire** de la formule de score de
l'[Artificial Analysis Intelligence Index](https://artificialanalysis.ai/methodology/intelligence-benchmarking)
(méthodologie v4.3.2 — v4.1.1 conservée en archive) — avec le code et les données pour **la vérifier
toi-même en moins d'une minute**.

> **Non affilié à Artificial Analysis.** Poids © Artificial Analysis (CC BY 4.0) ;
> reconstruction, code et commentaires : MIT. Voir [NOTICE](NOTICE).
> **Statut au 2026-09-29 :** calculateur + poids + données en **v4.3.2** — **29 modèles
> reproduisent l'Index publié avec max |Δ| = 0,12** (bandes ~14–58, modèles
hors bande inclus). La reproduction v4.1.1 à 8 modèles est archivée ci-dessous
et passe toujours via `--weights data/weights_v4.1.1.csv --models data/models.csv`.

---

## Le résultat, en un tableau (v4.3.2)

`Index = 100 × Σ (wᵢ × sᵢ)` sur **11 composantes**, avec les deux Elo
(AA-Briefcase v1.1 + GDPval-AA v2.1) normalisés par `s = clamp((Elo − 500) / 2000)`.

Recalculer l'Index depuis le **payload public de la page Index (2026-09-29)**
reproduit la valeur publiée pour les 29 modèles suivis, de ~14 à ~58 :

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
29 modèles · max |Delta| = 0.12 · seuil de lock interne = 1.00
```

*(Sortie exacte de `python src/aa_index.py --all`.)*

<details>
<summary>Résultat archivé (v4.1.1, 8 modèles, bande ~56–63)</summary>

`Index = 100 × Σ (wᵢ × sᵢ)` sur 10 composantes, avec l'Elo GDPval-AA normalisé
par `s = clamp((Elo − 500) / 2000)`.

Recalculer l'Index à partir des **scores de composantes affichés publiquement**
a reproduit la valeur publiée pour les 8 modèles testés, dans la marge de
lecture des charts. La formule v4.3.2 est la même moyenne pondérée sur **11
composantes**, avec la même normalisation Elo `clamp((Elo − 500) / 2000)`
appliquée à **deux** Elo (AA-Briefcase v1.1 + GDPval-AA v2.1) — voir
[docs/methodology.md](docs/methodology.md) §0.

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
8 modèles · max |Delta| = 0.30 · seuil de lock interne = 1.00
```

*(Sortie exacte de `python src/aa_index.py --all --weights data/weights_v4.1.1.csv --models data/models.csv`. Les valeurs à la main
enregistrées pendant l'analyse diffèrent de ≤ 0.02 ; voir
[docs/methodology.md](docs/methodology.md).)*

</details>
## Ce qui est validé — et ce qui ne l'est pas

| | |
|---|---|
| ✅ **Validé (archive)** | Formule + poids v4.1.1 sur la **bande Index ~56–63** (8 modèles, max \|Δ\| 0.30) |
| ✅ **Validé** | Formule + poids **v4.3.2** sur **29 modèles, Index ~14–58** (max \|Δ\| 0,12, hors bande inclus) |
| ❌ **Pas encore** | Modèles **hors bande** (ex. Index ~30) — dumps de composantes indisponibles au moment de l'analyse |
| ❌ **Hors scope** | Vitesse et coût : axes **séparés** sur AA, ils n'entrent pas dans l'Index |

Tous les Δ sont ≤ 0 — cohérent avec un bruit d'arrondi des scores publics,
**pas** avec un trou de formule.

## Démarrage rapide

Aucune dépendance. Python ≥ 3.9.

```bash
# 1. Vérifier les 29 modèles contre l'Index publié (v4.3.2)
python src/aa_index.py --all

# 2. Décomposition complète composante par composante
python src/aa_index.py --model "Kimi K3"

# 3. Vérification archivée v4.1.1 (8 modèles, toujours verte)
python src/aa_index.py --all --weights data/weights_v4.1.1.csv --models data/models.csv

# 4. Calculer l'Index depuis ton propre dump JSON v4.3.2
python src/aa_index.py --model examples/kimi-k3-v4.3.2.json

# 5. Sortie lisible par machine
python src/aa_index.py --all --json
```

### Exemple : une décomposition détaillée

`python src/aa_index.py --model examples/kimi-k3-v4.3.2.json` affiche la
contribution de chaque benchmark (v4.3.2) :

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
AA-LCR v1.1                 0.05   0.887         4.433
HLE                         0.10   0.469         4.690
CritPt                      0.10   0.234         2.343
----------------------------------------------------------------
Reconstructed Index                              43.55
AA published Index                               43.59
Delta (reconstr - AA)                            -0.04
```

<details>
<summary>Exemple archivé (v4.1.1 — Kimi K3, match exact)</summary>

`python src/aa_index.py --model examples/kimi-k3.json --weights data/weights_v4.1.1.csv --models data/models.csv` affiche la contribution
de chaque benchmark :

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

Kimi K3 est un **match exact** — bon test de sanité que la formule et la
normalisation Elo GDPval sont correctes. (Exemple v4.1.1 archivé ; les dumps
v4.3.2 utilisent `examples/kimi-k3-v4.3.2.json`.)

</details>

### Exemple : calculer depuis ton propre dump JSON

```jsonc
// examples/v4.3.2-template.json — mêmes clés que les colonnes de data/models_v4.3.2.csv
{
  "model": "Example Model",
  "variant": "max",
  "source": "https://artificialanalysis.ai/models — dump de chart AAAA-MM-JJ",
  "elo_briefcase": 1000,         // normalisé : (1000-500)/2000 = 0.25
  "elo_gdpval": 1600,            // normalisé : (1600-500)/2000 = 0.55
  "automationbench_aa": 0.5,     // tous les autres scores sont des s dans [0, 1]
  "terminal_bench_40": 0.5,
  "scicode": 0.5,
  "omniscience_accuracy": 0.5,
  "omniscience_non_hallu": 0.5,
  "gdp_pdf": 0.5,                // part All-pass (métrique headline)
  "aa_lcr_11": 0.5,
  "hle": 0.5,
  "critpt": 0.5,
  "published_index_aa": 50.0
}
```

Les dumps v4.1.1 (`examples/claude-opus-5.json`, `examples/kimi-k3.json`)
fonctionnent toujours avec `--weights data/weights_v4.1.1.csv --models data/models.csv`.

Ajouter un modèle se fait de la même façon → une ligne CSV / un fichier JSON +
une PR (voir [CONTRIBUTING.md](CONTRIBUTING.md)).

## Organisation du dépôt

```
aa-intelligence-index-reverse/
├── README.md                  ← version anglaise
├── README.fr.md               ← tu es ici (français)
├── LICENSE                    MIT + notice de provenance des données
├── NOTICE                     non-affiliation, provenance, limites connues
├── CITATION.cff               comment citer cette reconstruction
├── CONTRIBUTING.md            comment ajouter un modèle / une correction
├── data/
│   ├── weights_v4.3.2.csv     les 11 poids v4.3.2 (défaut actuel)
│   ├── models_v4.3.2.csv      matrice sᵢ v4.3.2 (29 modèles, 2026-09-29)
│   ├── weights_v4.1.1.csv     poids v4.1.1 archivés
│   └── models.csv             matrice 8 modèles v4.1.1 archivée
├── src/
│   └── aa_index.py            calculateur sans dépendance
├── tests/
│   └── test_aa_index.py       23 tests : formule, matrice v4.3.2, archive v4.1.1
├── examples/                  dumps JSON prêts à l'emploi
│   ├── v4.3.2-template.json
│   ├── kimi-k3-v4.3.2.json    (vrai dump v4.3.2 : Kimi K3, Δ −0,04)
│   ├── claude-opus-5.json     (archive v4.1.1)
│   └── kimi-k3.json           (archive v4.1.1)
└── docs/
    └── methodology.md         §0 v4.3.2 + §§2-3 archive v4.1.1
```

## Les poids (v4.3.2 — actuels)

| Composante | Poids | Catégorie |
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

Masses de catégories opérantes : **Agents 30 · Coding 20 · Scientific Reasoning 20 ·
General 30**. Les deux Elo se normalisent par `s = clamp((Elo − 500) / 2000)` ;
Briefcase ancrée à GPT-5.5 (medium) = 1000, GDPval v2.1 à DeepSeek V4.1 Flash (max) = 1600.

<details>
<summary>Poids archivés (v4.1.1)</summary>

| Composante | Poids | Catégorie |
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

Masses de catégories opérantes : **Agents 34 · Scientific 32 · Coding 16 ·
General 18**. (Certains documents de synthèse AA annotent
Coding/Scientific comme 24/24 ; ces libellés ne correspondent pas aux poids
opérants — détails dans [docs/methodology.md](docs/methodology.md).)

> L'ancienne description « 4 piliers × 25% » de la FAQ AA est **périmée** ;
> la table méthodo v4.3.2 fait foi.

</details>

## Tests

```bash
python -m unittest discover -s tests -v
```

23 tests couvrent les ancres de normalisation Elo (les deux composantes v4.3.2), la somme des poids et
les masses de catégories, la reconstruction du template (46.75), la **reproduction v4.3.2 sur 29 modèles
(max |Δ| = 0,12)** et — gelée — la **reproduction de l'Index publié
pour les 8 modèles archivés**. La CI exécute la même suite à chaque push
([.github/workflows/ci.yml](.github/workflows/ci.yml)).

## Pourquoi ce dépôt existe

Artificial Analysis publie l'Index et sa méthodologie, mais **aucun outil
public ne recalcule l'Index de bout en bout** à partir des scores de
composantes (leur [Stirrup](https://github.com/ArtificialAnalysis/Stirrup)
est un harness agent, pas un recalculeur d'Index). Ce dépôt comble ce vide
pour que :

- chacun puisse vérifier que l'Index publié d'un modèle correspond à ses
  scores de composantes ;
- les chercheurs propagent immédiatement de nouveaux dumps de composantes
  dans l'Index ;
- les changements de méthodologie (AA repondère périodiquement) soient
  suivis via des fichiers de poids versionnés (`weights_v4.x.y.csv`).

## Feuille de route

- [x] ~~Premier dump v4.3.2~~ — fait le 2026-09-29 : 29 modèles, max |Δ| = 0,12, bandes ~14–58.
- [ ] Garder la matrice à jour quand AA ajoute des modèles / repondère (nouveau `weights_vX.csv`, jamais d'édition d'historique).
- [ ] Fichiers de données pour d'autres modèles trackés (schéma v4.3.2).
- [x] ~~Un switch `--weights` quand AA publiera une v4.2~~ — fait : flags `--weights` /
  `--models`, v4.3.2 par défaut, v4.1.1 archivée.

## Contribuer

PRs bienvenues — la barre est **source ou ça n'a pas eu lieu** : chaque
nouvelle ligne doit porter l'URL du dump AA et la date. Voir
[CONTRIBUTING.md](CONTRIBUTING.md).

## Citer

Voir [CITATION.cff](CITATION.cff), ou :

```bibtex
@software{jules_2026_aa_index_reverse,
  author  = {Jules},
  title   = {aa-intelligence-index-reverse: reconstruction indépendante de la
             formule de l'Artificial Analysis Intelligence Index (v4.3.2, v4.1.1 archivée)},
  year    = {2026},
  url     = {https://github.com/AZERDSQ131/aa-intelligence-index-reverse}
}
```

## Licence

Code : MIT. Poids et méthodologie des benchmarks : © Artificial Analysis,
CC BY 4.0. Non affilié à ni approuvé par Artificial Analysis ou un fournisseur
de modèles — voir [NOTICE](NOTICE).
