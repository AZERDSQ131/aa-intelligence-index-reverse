# aa-intelligence-index-reverse

Une **reconstruction indépendante et communautaire** de la formule de score de
l'[Artificial Analysis Intelligence Index](https://artificialanalysis.ai/methodology/intelligence-benchmarking)
(méthodologie v4.1.1) — avec le code et les données pour **la vérifier
toi-même en moins d'une minute**.

> **Non affilié à Artificial Analysis.** Poids © Artificial Analysis (CC BY 4.0) ;
> reconstruction, code et commentaires : MIT. Voir [NOTICE](NOTICE).

---

## Le résultat, en un tableau

`Index = 100 × Σ (wᵢ × sᵢ)` sur 10 composantes, avec l'Elo GDPval-AA normalisé
par `s = clamp((Elo − 500) / 2000)`.

Recalculer l'Index à partir des **scores de composantes affichés publiquement**
reproduit la valeur publiée pour les 8 modèles testés, dans la marge de
lecture des charts :

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

*(Sortie exacte de `python src/aa_index.py --all`. Les valeurs à la main
enregistrées pendant l'analyse diffèrent de ≤ 0.02 ; voir
[docs/methodology.md](docs/methodology.md).)*

## Ce qui est validé — et ce qui ne l'est pas

| | |
|---|---|
| ✅ **Validé** | Formule + poids v4.1.1 sur la **bande Index ~56–63** (8 modèles, max \|Δ\| 0.30) |
| ❌ **Pas encore** | Modèles **hors bande** (ex. Index ~30) — dumps de composantes indisponibles au moment de l'analyse |
| ❌ **Hors scope** | Vitesse et coût : axes **séparés** sur AA, ils n'entrent pas dans l'Index |

Tous les Δ sont ≤ 0 — cohérent avec un bruit d'arrondi des scores publics,
**pas** avec un trou de formule.

## Démarrage rapide

Aucune dépendance. Python ≥ 3.9.

```bash
# 1. Vérifier les 8 modèles contre l'Index publié
python src/aa_index.py --all

# 2. Décomposition complète composante par composante (depuis data/models.csv)
python src/aa_index.py --model "Kimi K3"

# 3. Calculer l'Index depuis ton propre dump JSON
python src/aa_index.py --model examples/claude-opus-5.json

# 4. Sortie lisible par machine
python src/aa_index.py --all --json
```

### Exemple : une décomposition détaillée

`python src/aa_index.py --model examples/kimi-k3.json` affiche la contribution
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
normalisation Elo GDPval sont correctes.

### Exemple : calculer depuis ton propre dump JSON

```jsonc
// examples/claude-opus-5.json — mêmes clés que les colonnes de data/models.csv
{
  "model": "Claude Opus 5",
  "variant": "max",
  "source": "https://artificialanalysis.ai/models — dump de chart 2026-09-01",
  "elo_gdpval": 1824,              // normalisé : (1824-500)/2000 = 0.662
  "terminal_bench_21": 0.891,      // tous les autres scores sont des s dans [0, 1]
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
│   ├── weights_v4.1.1.csv     les 10 poids + catégories + normalisation
│   └── models.csv             matrice sᵢ de 8 modèles + Index publié
├── src/
│   └── aa_index.py            calculateur sans dépendance
├── tests/
│   └── test_aa_index.py       14 tests : formule, données, reproduction
├── examples/                  dumps JSON prêts à l'emploi
│   ├── v4.3.2-template.json
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

20 tests couvrent les ancres de normalisation Elo (les deux composantes v4.3.2), la somme des poids et
les masses de catégories, la reconstruction du template (46.75) et — gelée — la **reproduction de l'Index publié
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

- [ ] **v0.2 — premier dump v4.3.2** : ajouter ≥ 1 modèle avec les **11 composantes**
  + Index + URL + date (la contribution la plus utile en ce moment ; un mismatch
  est bienvenu aussi — il falsifie l'extrapolation).
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
