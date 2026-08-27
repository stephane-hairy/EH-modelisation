# CLAUDE.md — Règles de travail sur ce dépôt

## ⚠️ RÈGLE N°1 — NON NÉGOCIABLE : VULGARISER ET ÊTRE CONCIS

**Je dois TOUJOURS vulgariser et TOUJOURS être concis.**

Concrètement, à chaque réponse et dans chaque document produit :

1. **Vulgariser systématiquement.** Tout concept technique (économique,
   mathématique, statistique, écologique) doit être expliqué en langage
   courant AVANT ou EN MÊME TEMPS que sa formulation technique. On écrit
   pour quelqu'un d'intelligent mais non spécialiste.
   - Toujours donner l'intuition avant la formule.
   - Toujours traduire un sigle à sa première apparition.
   - Toujours donner un ordre de grandeur ou un exemple concret.
   - Jamais de jargon non expliqué. Jamais de formule sans phrase qui dit
     ce qu'elle raconte.
2. **Être concis.** Pas de préambule, pas de récapitulatif de ce que je
   viens de faire, pas de flatterie, pas de remplissage.
   - Aller droit au résultat.
   - Une idée par phrase, une phrase courte.
   - Un tableau ou une liste plutôt qu'un paragraphe quand c'est possible.
   - Si une réponse tient en 3 lignes, elle fait 3 lignes.
3. **Les deux ensemble.** Vulgariser ≠ être long. Une bonne explication
   simple est plus courte que l'explication technique, pas plus longue.

Ces deux règles priment sur toute autre considération de style.

## Langue

Tout le projet est en **français** : réponses, documentation, commentaires
de code, noms de variables métier, messages de commit.
Exception : les noms de fonctions/paquets techniques peuvent rester en
anglais si c'est l'usage (`pandas`, `fit`, `solve`).

## Objet du projet

Modéliser en **système dynamique** l'économie homéostatique (EH), théorie
macro-économique bio-inspirée d'Ex Naturae (Albouy, Hairy, Lavilley, 2020).

Deux étages :
1. **Modèle « France historique »** — reproduire ce qui s'est réellement
   passé (env. 1995–2023), en particulier comment le système monétaire
   agit sur l'économie réelle.
2. **Modèle « France en EH »** — remplacer les mécanismes monétaires par
   ceux de l'EH et simuler les trajectoires.

## ⚠️ RÈGLE N°2 — Traçabilité de chaque relation

**Aucune équation n'entre dans le modèle sans fiche de traçabilité.**

Toute relation doit relever d'une de ces quatre catégories :

| Catégorie | Signification | Justification exigée |
|---|---|---|
| **I — Identité** | Vraie par construction comptable (ex. : actif = passif) | Aucune : c'est de la comptabilité. Mais il faut le dire. |
| **C — Causale** | Mécanisme causal établi, sourcé et calculable | Étude scientifique ou texte réglementaire + méthode de calcul |
| **S — Statistique** | Corrélation très forte, sourcée et calculable | Étude publiée + test refait sur données (R², cointégration, robustesse) |
| **D — Design** | Choix normatif de l'EH (règle inventée, pas observée) | Référence exacte au document EH + marquage explicite « non empirique » |

Les relations de catégorie **D ne doivent JAMAIS être présentées comme
empiriquement fondées.** Ce sont des choix de conception, à passer en
analyse de sensibilité.

Procédure : voir `docs/03-protocole-rigueur.md`, registre dans
`modele/registre/`.

## ⚠️ RÈGLE N°3 — Honnêteté sur l'incertitude

- Un chiffre non vérifié dans une source est marqué `[À VÉRIFIER]`.
- Un résultat de simulation est toujours accompagné de sa fourchette
  d'incertitude et de ses hypothèses.
- Si une relation est faible ou contestée dans la littérature, on le dit.
- On ne présente jamais une projection comme une prédiction.
- On ne « fait pas marcher » un modèle en bricolant un paramètre : on
  documente l'échec.

## Tenue du dépôt

À mettre à jour **à chaque session de travail** :
- `JOURNAL.md` — journal des actions (quoi, pourquoi, résultat).
- `TODO.md` — tâches, statuts, priorités.

## Pile technique

Python 3.11+ · `pandas`, `numpy`, `scipy` · `statsmodels` (économétrie) ·
`pandasdmx` (récupération reproductible INSEE / Eurostat / BCE) ·
`matplotlib` · `pytest`.
Toute donnée est récupérée **par script**, jamais téléchargée à la main.

## Ce qu'il ne faut pas faire

- Inventer une valeur numérique plausible. Jamais.
- Estimer une relation sur des séries non stationnaires sans test de
  cointégration (régression fallacieuse).
- Calibrer un paramètre sur la période de validation.
- Étendre le périmètre sans le noter dans `TODO.md`.
