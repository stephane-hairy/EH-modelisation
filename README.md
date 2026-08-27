# EH-modelisation

Modélisation en système dynamique de l'**économie homéostatique** (EH),
et modèle de référence de l'économie française pour la comparer au
système monétaire actuel.

## En deux phrases

Aujourd'hui, la monnaie est créée par la dette bancaire et la richesse
d'un pays vient de ce qu'il extrait de la nature. L'EH propose l'inverse :
la monnaie est **donnée** en fonction de l'état écologique du pays, et
elle **fond** lentement au lieu d'être remboursée. Ce dépôt cherche à
savoir, chiffres à l'appui, si ça peut marcher.

## Par où commencer

| Document | Contenu |
|---|---|
| [`docs/01-economie-homeostatique.md`](docs/01-economie-homeostatique.md) | **Comment marche l'EH** — explication détaillée et vulgarisée |
| [`docs/02-strategie-modelisation.md`](docs/02-strategie-modelisation.md) | **La stratégie** — quoi construire, dans quel ordre, comment le valider |
| [`docs/03-protocole-rigueur.md`](docs/03-protocole-rigueur.md) | **Les règles de preuve** — comment chaque équation est justifiée |
| [`docs/04-decisions.md`](docs/04-decisions.md) | **Les décisions prises** — formalisme, périmètre, fréquence, période |
| [`docs/annexes/couverture-donnees.md`](docs/annexes/couverture-donnees.md) | Jusqu'où remontent les données (généré par script) |
| [`TODO.md`](TODO.md) | Tâches, verrous, décisions en attente |
| [`JOURNAL.md`](JOURNAL.md) | Journal des actions |
| [`CLAUDE.md`](CLAUDE.md) | Règles de travail (vulgariser, être concis, tracer) |

## Principe méthodologique

Aucune équation n'entre dans le modèle sans **fiche de traçabilité**
(`modele/registre/`) indiquant sa catégorie :

- **I** identité comptable · **C** relation causale sourcée ·
  **S** corrélation forte sourcée et re-testée · **D** choix de conception
  de l'EH (**non empirique**, marqué comme tel).

Les règles inventées par l'EH (le « 22 000 € par citoyen », la fonte à
1 %/mois) ne sont **jamais** présentées comme empiriquement fondées.

## Structure

```
docs/       documentation de référence et décisions
sources/    documents primaires (synthèse EH v1.7)
scripts/    outils (extraction, audit de couverture, calculs)
modele/     le modèle, ses clients de données, son registre d'équations
tests/      contrôles automatiques (dont la conformité du registre)
donnees/    données brutes et traitées (récupérées par script)
```

## Installation

```bash
pip install -e ".[dev]"
python -m pytest -q                        # tests hors réseau
python -m pytest -q -m reseau              # tests nécessitant le réseau
python3 scripts/audit_couverture.py        # audit des sources de données
```

## Source primaire

Albouy B., Hairy S., Lavilley V., *Vers une économie bio-intégrée :
Théorie de l'économie homéostatique — Document de synthèse*, v1.7,
Ex Naturae, octobre 2020. CC BY-NC-ND 2.0 FR.
<https://exnaturae.ong>
