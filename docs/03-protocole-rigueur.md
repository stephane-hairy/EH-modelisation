# Protocole de rigueur — comment on fonde chaque relation

> Traduction opérationnelle de la règle : *« chaque relation du modèle doit
> être fondée soit par une étude scientifique, soit par une relation
> causale sourcée et calculable, soit par une corrélation très forte
> sourcée et calculable. »*

---

## 1. Les quatre catégories

Toute équation porte **une** catégorie. Sans catégorie, elle n'entre pas
dans le modèle.

### I — Identité comptable
Vraie par construction. `Épargne = Revenu − Consommation`. Aucune source
nécessaire, mais il faut **écrire** que c'est une identité.
→ Toujours préférer une identité à une relation estimée quand c'est
possible. C'est de la rigueur gratuite.

### C — Causale
Un mécanisme causal établi, sourcé, et calculable.
**Preuve exigée** : étude publiée avec identification causale
(expérience, quasi-expérience, discontinuité, variable instrumentale,
règle institutionnelle) **ou** texte réglementaire (ex. : le taux de
réserves obligatoires est une règle, pas une corrélation).
*Exemple* : « les crédits font les dépôts » — mécanisme institutionnel
documenté (Banque d'Angleterre, 2014) et testé empiriquement
(Werner, 2014).

### S — Statistique
Corrélation très forte, sourcée et calculable.
**Preuve exigée, cumulative** :
1. une étude publiée qui établit la relation ;
2. **le test refait par nous** sur données françaises ;
3. les diagnostics : stationnarité (ADF/KPSS), **cointégration si les
   séries sont I(1)**, R², stabilité des coefficients (test de Chow /
   CUSUM), robustesse au choix de période.

⚠️ **Piège central** : deux séries macro qui montent toutes les deux dans
le temps sont corrélées à 0,95 sans aucun lien. C'est la *régression
fallacieuse* (Granger & Newbold, 1974). Une corrélation de niveau sur
séries non stationnaires **ne compte pas** comme preuve.

### D — Design (choix normatif de l'EH)
Règle inventée par la théorie, non observée dans le monde.
**Preuve exigée** : référence exacte (document, version, section) + le
marqueur `empirique: false`.
**Obligation** : toute relation D passe en analyse de sensibilité. On ne
publie jamais un résultat qui dépend d'un paramètre D sans montrer ce
qu'il devient quand ce paramètre varie.

---

## 2. Les grades de confiance

En plus de la catégorie, chaque relation reçoit un grade :

| Grade | Signification |
|---|---|
| **A** | Identité comptable, ou relation causale identifiée + répliquée par nous |
| **B** | Corrélation forte et stable, littérature convergente, nos tests passent |
| **C** | Relation plausible mais contestée, fragile, ou données insuffisantes |
| **D** | Choix de conception (couche EH) — non empirique par nature |

**Règle de publication** : tout résultat dont la conclusion dépend d'une
relation de grade **C** doit l'annoncer explicitement, et montrer le
résultat avec et sans cette relation.

---

## 3. Le registre d'équations

Chaque équation = un fichier YAML dans `modele/registre/`.
Schéma : `modele/registre/SCHEMA.md`. Exemple complet :
`modele/registre/exemple-EQ-EMP-001.yaml`.

**Contrôles automatiques** (CI, `pytest`) :
- toute équation du code a une fiche (et réciproquement) ;
- tout champ obligatoire est rempli ;
- toute fiche de catégorie `S` a un test de réplication exécutable ;
- toute source a une URL ou un DOI résoluble ;
- toute fiche de catégorie `D` est référencée dans le plan de sensibilité.

---

## 4. Ce qui est interdit

| Interdit | Pourquoi |
|---|---|
| Un nombre « plausible » sans source | C'est une invention, pas un modèle |
| Une régression de niveaux sur séries I(1) sans cointégration | Régression fallacieuse |
| Citer une étude sans en avoir lu la méthode | On ne sait pas ce qu'on cite |
| Calibrer sur la période de validation | Sur-ajustement déguisé |
| Présenter une relation D comme empirique | Faute méthodologique majeure |
| Supprimer une équation qui « donne un mauvais résultat » | Ajustement du monde au modèle |
| Un `p < 0,05` seul comme preuve | Taille d'effet et robustesse d'abord |

---

## 5. Quand une relation manque

Il y aura des trous — notamment sur la biodiversité. Procédure :

1. Le noter dans `TODO.md` comme **verrou**, pas le combler au jugé.
2. Trois issues acceptables :
   - **Approximation documentée** : on utilise un proxy, on dit lequel et
     pourquoi, grade C.
   - **Paramètre libre** : on ne fixe rien, on balaie une fourchette et on
     publie la sensibilité.
   - **Périmètre réduit** : on retire le bloc du modèle et on dit ce que
     ça enlève aux conclusions.
3. **Jamais** : inventer une valeur et continuer.
