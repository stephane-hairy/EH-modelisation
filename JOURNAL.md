# Journal des actions

Une entrée par session. Format : **quoi** · **pourquoi** · **résultat** ·
**ce que ça change**.

---

## 2026-08-27 — Session 1 : cadrage du projet

### Contexte
Demande initiale : modéliser en système dynamique l'économie homéostatique
(EH). D'abord un modèle empirique de la France et de l'action du système
monétaire sur l'économie ; ensuite la greffe des mécanismes EH. Exigence
transverse : **chaque relation doit être fondée** (étude scientifique,
relation causale sourcée et calculable, ou corrélation très forte sourcée
et calculable).

### Actions

**1. Mise en place du dépôt**
- `CLAUDE.md` — règles de travail. Règle n°1 explicite : **toujours
  vulgariser, toujours être concis**. Plus : traçabilité obligatoire de
  chaque équation, honnêteté sur l'incertitude, français partout.
- `TODO.md`, `JOURNAL.md` (ce fichier).

**2. Documentation de l'EH**
- Téléchargé la synthèse officielle (`exnaturae.ong`, v1.7, oct. 2020,
  60 p., CC BY-NC-ND) → `sources/`.
- Extraction texte via `pypdf` + reflux (`scripts/extraction_pdf.py`).
  Le PDF sort en un-mot-par-ligne ; un nettoyage était nécessaire.
- Lu l'intégralité, y compris les notes de bas de page (elles contiennent
  les références scientifiques du modèle).
- Vérifié le site `exnaturae.ong` : contenu vulgarisé, **aucune formule
  supplémentaire** par rapport au PDF. La v1.7 reste la référence.
- → `docs/01-economie-homeostatique.md`.

**3. Premier calcul d'ordre de grandeur**
- `scripts/ordre_grandeur_eh_france.py` : formules §11.1 appliquées à la
  France, entrées marquées `[À VÉRIFIER]`.
- Résultat : création monétaire ≈ **7 000 Md€/an** (2,5 × PIB), et masse
  monétaire d'équilibre (création = fonte) ≈ **48 700 Md€**, soit
  **≈ 16 fois** M3 France actuel.
- **Ce que ça change** : la question du niveau des prix devient centrale.
  La synthèse (§10.1) affirme qu'« il ne peut y avoir d'hyperinflation »
  sans le démontrer. Ce calcul ne réfute rien (`DTENT` domine et repose
  sur une estimation non vérifiée) mais il **justifie le projet** : les
  paramètres 22 000 € et 1 %/mois doivent être calibrés, pas postulés.

**4. Stratégie de modélisation** → `docs/02-strategie-modelisation.md`
Quatre modifications proposées au plan initial :
1. **Formalisme SFC** (Godley & Lavoie 2007) plutôt qu'un système
   dynamique générique. Motif principal : c'est le seul cadre où
   « créer de la monnaie » a un sens comptable précis — or l'EH est
   entièrement une théorie de création/destruction monétaire. Bonus : ~2/3
   des équations deviennent des identités comptables, ce qui rend
   l'exigence de traçabilité tenable. Lignée écologique existante :
   Dafermos et al. (2017), Jackson & Victor (2020), EUROGREEN (2020).
2. **Séparation stricte en trois couches** — A (positive, empirique) /
   B (design EH, normatif) / C (transmission, empirique et critique).
   Motif : le « 22 000 € par citoyen » et la « fonte à 1 % » ne sont pas
   des faits observés. Les présenter comme empiriquement fondés serait la
   faute méthodologique la plus facile à nous reprocher.
3. **Prioriser un livrable autonome** : reconstituer IBD/IEE/IRNR/IED pour
   la France 1995–2023 (jalon P2), avant le modèle complet. 100 % empirique,
   rapide, et donne la courbe « création monétaire EH implicite ».
4. **Traiter l'EH comme un système asservi** : analyser formellement la
   stabilité de la boucle. Les délais écologiques (3–10 ans) sont longs ;
   une rétroaction à long délai **oscille** typiquement au lieu de
   converger (Sterman 2000). La synthèse affirme la stabilité (§10.1) sans
   la démontrer. C'est sans doute la contribution scientifique la plus
   forte que ce dépôt puisse apporter.

**5. Protocole de rigueur** → `docs/03-protocole-rigueur.md`
Quatre catégories (I/C/S/D), quatre grades (A/B/C/D), registre YAML avec
une fiche par équation, contrôles automatiques en CI.
Point technique insisté : interdiction des régressions de niveaux sur
séries non stationnaires sans cointégration (régression fallacieuse,
Granger & Newbold 1974) — c'est le principal piège de l'exigence
« corrélation très forte ».
Fiche d'exemple rédigée : loi d'Okun (`exemple-EQ-EMP-001.yaml`).

### Verrous identifiés
1. **Aucune formule d'indicateur** dans la synthèse. IBD, IEE et IRNR
   doivent être créés de toutes pièces. Sans eux, rien n'est simulable.
   L'IBD (biodiversité) est le plus incertain — les données peuvent ne pas
   suffire.
2. **Taux de change** explicitement « à développer » (§15).
3. **La France n'a pas de souveraineté monétaire** depuis 1999. Le modèle
   historique doit représenter l'Eurosystème. Et le passage à l'EH implique
   sortie de l'euro + délégation à une BCI : saut de régime tel qu'aucun
   contrefactuel exact n'est rigoureux. On parlera de scénarios.
4. **Critique de Lucas** : les comportements estimés sous le régime actuel
   peuvent ne pas tenir sous l'EH. Atténuation, pas résolution.

### Prochaine étape
6 décisions de cadrage attendues (`TODO.md`, section rouge) avant tout
code de modèle.

---

## 2026-08-27 — Session 2 : décisions de cadrage et fondations P0

### Décisions reçues et actées
Les six questions de cadrage ont été tranchées → `docs/04-decisions.md`.
Deux ont demandé une vérification préalable, car la réponse dépendait de
ce que les données permettent réellement.

### Audit de couverture des données (nouveau)
`scripts/audit_couverture.py` interroge INSEE, Eurostat et la BCE et écrit
`docs/annexes/couverture-donnees.md`. Résultats :

| Bloc | Fréquence disponible | Début |
|---|---|---|
| PIB et agrégats réels (INSEE) | annuelle | **1949** |
| Comptes financiers par secteur (INSEE) | annuelle | **1995** |
| Comptes financiers par secteur (BCE QSA) | trimestrielle | **1998-Q4** |
| Crédits des IFM France (BCE BSI) | mensuelle | **2003-01** |
| Inventaire GES, flux de matières (Eurostat) | annuelle | **1990** |
| Comptes d'émissions par branche (Eurostat) | annuelle | **2008** |

### Ce que l'audit a changé aux deux réponses

**Fréquence (D4).** La préférence était « plutôt mensuel ». Ce n'est pas
praticable : il n'existe aucune donnée mensuelle de PIB, d'investissement
ou de patrimoine sectoriel en France. Un modèle mensuel complet serait
calé sur des séries interpolées — des chiffres inventés, exclus par la
RÈGLE N°3.
→ Décision **amendée** : cœur annuel, **plus un sous-pas mensuel
analytique pour la fonte**. La fonte est définie mensuellement (1 % en fin
de mois) et l'ordre des versements dans l'année change le résultat
(synthèse §10.3) : on la calcule exactement en 12 sous-pas au lieu de
l'approximer. La préférence pour le mensuel est ainsi satisfaite là où
elle a un sens.

**Période (D5).** « 1978 si possible » : possible pour l'économie réelle
(données depuis 1949), **impossible pour un SFC bouclé** — les comptes
financiers par secteur, qui disent qui détient quoi, démarrent en 1995.
→ Décision **à deux périmètres** : 1978–2023 pour le bloc réel+monétaire,
1995–2023 pour le modèle complet et l'écologie.
→ **Bénéfice inattendu** : 1978–1998 contient l'encadrement du crédit
(supprimé en 1987) et la déréglementation financière. C'est une
expérience naturelle sur exactement notre question — comment le mécanisme
de création monétaire agit sur l'économie réelle. C'est un actif, pas une
consolation.

### Fondations P0 construites
- `pyproject.toml`, arborescence `modele/` + `tests/`.
- **Clients de données** `modele/donnees/sources.py` — INSEE (SDMX-ML),
  Eurostat (JSON-stat 2.0), BCE (CSV).
  *Choix technique* : `pandasdmx` **écarté**. Sa version 1.10 échoue à
  parser les structures INSEE (`KeyError: 'TIME_PERIOD'`, la dimension
  temporelle étant déclarée à part). Trois petits lecteurs valent mieux
  qu'une grosse dépendance fragile. Deux pièges rencontrés et corrigés :
  le code pays de l'INSEE est `FE` (France entière) et non `FR` ; et dans
  JSON-stat l'indice doit être décodé en coordonnées, `time` n'étant pas
  toujours la dernière dimension.
- **Cache reproductible** `modele/donnees/cache.py` — chaque série est
  stockée avec son SHA-256, son horodatage et l'URL exacte. Un manifeste
  signale toute **révision** de série par l'institut. Sans cela un
  résultat n'est pas reproductible : les instituts révisent en permanence.
- **Contrôle du registre** `modele/registre.py` + `tests/test_registre.py`.
  Applique la RÈGLE N°2 automatiquement. En particulier : une fiche de
  catégorie `D` (design EH) ne peut pas être marquée `empirique: true`,
  et une fiche de catégorie `S` sans réplication de notre part est
  refusée. La CI échoue si le registre n'est pas conforme.
- **CI GitHub Actions** : tests + contrôle du registre à chaque poussée.

### Chiffre vérifié
PIB France 2023 = **2 833,8 Md€** courants (INSEE CNA-2020-PIB, série
1949–2025). Remplace une estimation `[À VÉRIFIER]` dans le calcul d'ordre
de grandeur. Conclusion inchangée : masse monétaire d'équilibre ≈ 17 × PIB.

### Ce qui reste le plus incertain
`DTENT` (dividende des entreprises) domine la création monétaire totale et
repose encore sur une estimation non sourcée des produits d'exploitation
cumulés des entreprises françaises. **C'est le chiffre le plus important à
sourcer**, avant toute affirmation sur le niveau des prix en EH.

### Prochaine étape
Jalon **P2** : opérationnaliser IBD, IEE, IRNR — le verrou n°1.
