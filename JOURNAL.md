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

---

## 2026-08-27 — Session 2 (suite) : DTENT remis à sa place

### Information reçue de l'auteur
La formule du dividende des entreprises (DENT, §11.1) **a été construite
« au doigt mouillé »**. C'est une information de première main, et elle
change le statut de nos chiffres.

### Pourquoi c'est un problème de premier ordre
DTENT pèse **plus de la moitié** de la création monétaire totale d'un pays
comme la France. Cette formule décide donc à elle seule de l'essentiel de
tout résultat quantitatif sur l'EH.

### Ce qui a été fait
1. **Chiffre sourcé** : production des sociétés non financières françaises
   2023 = **3 810 Md€** (Eurostat `nasa_10_nf_tr`, S11/P1/RECV, série
   depuis 1971). L'estimation antérieure de 4 000 Md€ tenait à 5 % près —
   mais cela ne sauve pas le calcul, puisque c'est la *formule* qui est en
   cause, pas son entrée.
2. **Le script ne publie plus un point mais une fourchette** sur DTENT
   (0,7 × / 1,0 × / 1,5 × la production des SNF), avec la sensibilité
   affichée.
3. **Résultat de la sensibilité** :

   | Hypothèse DTENT | Création/an | M équilibre | × PIB | × M3 actuel |
   |---|---|---|---|---|
   | basse (2 667 Md€) | 5 664 Md€ | 39 436 Md€ | 13,9 | 13,1 |
   | centrale (3 810 Md€) | 6 807 Md€ | 47 395 Md€ | 16,7 | 15,8 |
   | haute (5 715 Md€) | 8 712 Md€ | 60 660 Md€ | 21,4 | 20,2 |

### Conclusion, honnêtement formulée
- ✅ Le constat est **robuste à la fourchette de DTENT** : même
  l'hypothèse basse donne ≈ 14 × PIB. Il ne tient pas à un chiffre mal
  choisi de notre part.
- ❌ Il n'est **pas robuste à la formule DENT elle-même**. Donner chaque
  année à chaque entreprise l'équivalent de son produit d'exploitation est
  un choix structurant qui n'a pas été arbitré.

Le chiffre de sortie n'est donc pas une propriété de l'économie
homéostatique : c'est une propriété d'une formule provisoire.

### Nouveau verrou (P0)
**Reconstruire DENT.** Questions à trancher, notées au `TODO.md` :
périmètre des « entreprises » ; nature de `P` (comptable ou comptes
nationaux) ; effet de la règle « moyenne des trois meilleures années »
(biais haussier et cliquet) ; homogénéité dimensionnelle du terme
`(e × DCIT) / ((r/e) × 10⁴)` et son comportement quand `r → 0`.

---

## 2026-08-27 — Session 3 : verrou DENT levé, indicateurs EXEC construits

### Ce qui a été fait
Les deux missions du prompt de reprise : **【A】** reconstruire DENT,
**【B】** reconstituer les indicateurs EXEC de la France.

---

### 【A】 DENT — six défauts démontrés, pas argumentés

La formule §11.1 `DENT = IED × P + (e × DCIT) / ((r/e) × 10⁴)` ne peut pas
être utilisée telle quelle. Tout est reproductible
(`scripts/analyse_dent.py`) et testé (`tests/test_dent.py`, 21 tests).

1. **Elle n'est pas homogène.** Le second terme a la dimension d'un
   **nombre de personnes au carré**, pas d'euros. On ne peut pas
   l'additionner à `IED × P`. Le résultat tient pour les deux lectures
   possibles du texte et pour les deux conventions sur la dimension
   « personne » : le défaut est **structurel**, pas typographique.
   La faute vient de la **division par `r/e`** ; le produit `e × DCIT`,
   lui, était juste (c'est une masse salariale). C'est ce qui rend la
   réparation possible.
2. **On ne sait pas la lire.** Le PDF sort la formule en glyphes séparés
   (`( r / e × 1 0 ⁴ )`). Les deux lectures diffèrent d'un facteur
   **10⁸ exactement**. Le texte d'accompagnement (« *r* est divisé par le
   nombre d'employé, **lui-même** multiplié par 10⁴ ») désigne plutôt la
   lecture que le dépôt n'avait *pas* retenue. Sous la lecture A le terme
   est négligeable partout (8 € pour 1 000 salariés) ; sous la lecture B
   il dépasse la production entière dès ~70 salariés. Aucune des deux ne
   réalise l'intention affichée.
3. **Elle diverge en `r → 0`.** Une entreprise où le mieux payé gagne
   exactement le revenu minimum reçoit un dividende **infini** — et le
   signe bascule si ce salaire passe en dessous. La singularité est sur
   le versant *vertueux* : incitation perverse.
4. **Elle n'est pas définie pour 96 % des entreprises françaises.**
   4 718 929 des 4 906 972 entreprises ont moins de 10 personnes
   occupées, soit **1,17 personne par entreprise** (Eurostat
   `sbs_sc_ovw` 2022) : pas de salarié, donc ni `e`, ni `r`. Le calcul
   « entreprise par entreprise » que prescrit la synthèse est
   **impossible** sur l'écrasante majorité du tissu français.
5. **Elle explose avec la taille.** Le terme croît en `e²`, la production
   en `e`.
6. **Son assiette n'est pas additive.** La somme des chiffres d'affaires
   compte plusieurs fois la même valeur. Conséquence vérifiable : deux
   entreprises qui **fusionnent** font *baisser* la création monétaire du
   pays ; une qui se **scinde** la fait monter. Il suffirait de
   filialiser pour créer de la monnaie. La valeur ajoutée n'a pas ce
   défaut (SEC 2010) : production des SNF 3 810 Md€ contre VA 1 481 Md€,
   **rapport 2,57**.

#### La règle « 3 meilleures années » : rétroaction positive + cliquet

À porter au crédit de la synthèse : elle **anticipe partiellement**
l'objection, en précisant que `P` est réactualisé « hors DENT ». Cela
coupe bien la boucle *directe*.

Mais pas la boucle **macro-économique** : le dividende de l'entreprise A
devient le chiffre d'affaires de B. Exclure son propre dividende ne
retire que `1/N` du flux — avec N = 4,9 millions d'entreprises, cela ne
retire rien. La récurrence `P ← X₀ + α·IED·P` converge vers `X₀/(1−α)` :
**×5 pour α = 0,8**, ×10 pour α = 0,9. À α = 1, la clause « hors DENT »
est le seul frein restant et plafonne l'amplification à **4,9 millions de
fois** : elle ne protège de rien.

Effet cliquet mesuré : six ans de récession à −25 % ne font baisser la
base de référence que de **11,3 %**. *Le thermostat continue de chauffer
parce qu'il se souvient du meilleur été.*

#### Trois alternatives proposées, non départagées

Toutes homogènes, bornées, définies à `e = 0` et `r = 0`, monotones,
proportionnelles à l'IED. Clé de la réparation : remplacer l'écart de
salaire **en euros** (`r`) par un **rapport** `s = salaire_max / DCIT`,
qui est un nombre pur.

| | Formule | Corrige |
|---|---|---|
| `EQ-EH-002` | `IED × P × κ(s)` | défauts 1–5 |
| `EQ-EH-003` | `IED × [(1−θ)·P + θ·e·DCIT·ψ(s)]` | 1–5, et garde les mots de la synthèse |
| `EQ-EH-004` | `IED × VA × κ(s)` | 1–6, **y compris la filialisation** |

Écart sur DTENT France : **facteur 7,9** (3 810 Md€ pour la §11.1, 480 Md€
pour l'alternative 3). C'est bien la formule, et non la théorie EH, qui
décide de l'ordre de grandeur.

→ **Quatre décisions attendues : D7 assiette · D8 forme · D9 périmètre ·
D10 base `P`.**

---

### 【B】 Indicateurs EXEC — livrés sur 1990–2021, et pas plus

#### Le résultat le plus important est une absence

Le cadrage demandait **1978–2023**. Livré : **1990–2021**. Ce n'est pas un
manque de zèle, c'est un fait vérifié :

| Série | Début |
|---|---|
| Flux de matières (Eurostat `env_ac_mfa`) | **1990** |
| Empreinte carbone importations incluses (Global Carbon Project) | **1990** |
| Oiseaux communs agricoles (Eurostat `env_bio2`) | **1990** |

Les trois commencent en 1990, pour trois raisons indépendantes : les
comptes de flux de matières français démarrent là ; le protocole STOC de
comptage des oiseaux a été lancé en 1989 ; et les tableaux entrées-sorties
mondiaux nécessaires au calcul des empreintes n'existent pas plus tôt.
Combler 1978–1989 exigerait d'inventer douze années pour les trois
indicateurs à la fois. **RÈGLE N°3 : on documente le trou.**

Une seule action pourrait rouvrir la période : obtenir une **clé d'API du
Global Footprint Network** (gratuite sur demande) — leurs comptes
remontent à **1961**. Noté au `TODO.md` en P1.

#### Ce qui a été construit

- **IRNR** (`EQ-EXEC-001`) — matière non renouvelable par habitant
  rapportée à 8 t/hab (Bringezu 2015). Point notable : **le recyclage y
  compte positivement par construction**, puisque le DMC ne compte que la
  matière vierge. Ajouter un bonus de recyclage aurait été un **double
  comptage** — c'est le piège évité. La France passe de 10,9 à 7,8 t/hab
  et traverse le seuil vers 2014.
- **IEE** (`EQ-EXEC-002`) — ⚠️ **approximation assumée**. Le GFN exige une
  clé (403 sans elle) ; on substitue l'empreinte **carbone** importations
  incluses (Global Carbon Project, MRIO Eora), rapportée au budget 1,5 °C
  du GIEC partagé par tête (2,13 tCO₂/hab). Grade C. La France est à
  **2,9 fois le seuil** : c'est l'indicateur qui pilote tout.
- **IBD** (`EQ-EXEC-003`) — ⚠️ **les données ne suffisent pas, et c'est le
  résultat**. Seule série : oiseaux agricoles, −42 % de 1990 à 2021. Deux
  limites rédhibitoires : **aucune dimension importations** (l'IBD est le
  seul des trois à violer §14.1, et il la viole totalement), et une
  **référence 1990 arbitraire** qui revient à décréter la France de 1990 à
  l'équilibre — elle ne l'était pas, donc l'IBD est structurellement trop
  optimiste. Plus une **rupture de série en 2000** (valeur 100,0 encadrée
  par 69,5 et 72,7), retirée, et qui laisse un trou visible.
  → Toutes les sorties publient l'IED **avec et sans IBD**.
- **Mapping vers [0 ; 2]** (`EQ-EXEC-004`) — trois variantes.

#### Le résultat

**L'IED français reste entre 0,41 et 0,57 sur toute la période.** Sous
l'EH, la France aurait vécu en permanence sous un régime de création
monétaire réduite de moitié : **11 900 €/an par citoyen en 2021** au lieu
de 22 000 €. L'amélioration existe mais est lente (+0,09 point en trente
ans), portée par le carbone et les matières, freinée par la biodiversité.

Graphique : `sorties/creation_monetaire_eh_france.png`. Il publie **une
bande, pas un trait** — la part entreprises dépendant de DENT, non
arbitrée. En 2021, la création totale va de **1 794 à 3 275 Md€**.

#### Le mapping est LE choix structurant, et il n'est pas tranché

À seuils identiques, pour la France 2021 :

| Mapping | IED 2021 | Pente en x = 1 |
|---|---:|---:|
| linéaire `2 − x` | **0,00** | −1,00 |
| hyperbolique `2/(1+x)` | **0,72** | −0,50 |
| exponentiel `2^(1−x)` | **0,54** | −0,69 |

Le mapping **linéaire annule** la création monétaire française : IEE = 0,
donc la moyenne géométrique s'annule. Ce n'est pas un bug, c'est ce que
cette règle normative affirme.

Point qui engage la suite : **la pente au point d'équilibre est le gain du
régulateur EH**. Elle varie d'un facteur 2 selon le mapping. Le mapping
doit donc être arbitré **avant** l'analyse de stabilité du jalon P5, pas
après.

→ **Trois décisions attendues : D11 mapping · D12 sort de l'IBD ·
D13 seuils.**

---

### Deux erreurs commises et corrigées

Notées parce qu'elles sont instructives.

1. **Erreur d'unité sur l'empreinte carbone.** Les émissions du Global
   Carbon Project sont en *millions* de tonnes ; je les ai d'abord
   divisées par la population sans conversion, ce qui donnait un IEE
   constant à 2,00 — c'est-à-dire « la France est parfaitement
   soutenable ». Un test verrouille désormais la conversion.
2. **Rebouchage silencieux d'un indicateur manquant.** L'agrégation
   ignorait les indicateurs absents. En 2023, l'empreinte carbone n'étant
   pas encore publiée, l'IED affichait **1,06** — la France à l'équilibre
   écologique — parce que l'indicateur le plus contraignant avait
   simplement disparu du calcul. Le calcul est désormais **strict** : un
   indicateur absent donne `NaN`. Test :
   `test_ied_refuse_de_reboucher_un_indicateur_manquant`.

La leçon est la même dans les deux cas : **les bugs de ce projet ne font
pas planter le programme, ils rendent la France plus verte qu'elle n'est.**
Ils doivent être cherchés activement, pas attendus.

### Correctif technique
`pyproject.toml` ne déclarait pas ses paquets : `pip install -e .` échouait
(`Multiple top-level packages discovered in a flat-layout`). Corrigé.

### État
`python -m pytest -q` : **64 tests verts**. Registre : **conforme**
(11 fiches). Sept décisions attendues : **D7–D13**.


---

## 2026-08-27 — Session 3 (suite) : l'empreinte écologique retrouvée via Dateno

### Ce qui a été cherché
Stéphane a fourni une clé d'API **Dateno** (moteur de recherche de jeux de
données) pour tenter de débloquer l'empreinte écologique du Global
Footprint Network, inaccessible jusque-là (API à clé nominative, 403).

*La clé est passée en variable d'environnement et n'est écrite nulle part
dans le dépôt.*

### Ce qui a été trouvé — et ce qui ne l'a pas été

| Cherché | Résultat |
|---|---|
| Série GFN 1961→ | ❌ **N'existe pas en accès libre.** Confirmé. Les résultats Dateno sont des copies Kaggle (authentification requise) ou des cartes `.jpg` |
| Paquet public officiel GFN | ✅ **Trouvé** : *National Footprint Accounts 2017 Public Data Package v1.3*, licence Creative Commons, avec son guide méthodologique |
| Empreinte matières ODD 8.4.1 (UNEP/IRP) | ❌ **Écartée** : l'ONU ne la publie qu'au niveau régional. France absente (vérifié : 36 zones, toutes des agrégats) |
| Base de séries statistiques Dateno | ❌ Ne contient qu'ILOSTAT et Banque mondiale |

⚠️ Le paquet GFN ne contient **qu'une seule année, 2013**. Ce n'est pas la
série espérée. Il est de plus servi depuis un **miroir CKAN** (OD Mekong
Datahub), le portail du GFN ne l'exposant pas librement : le *contenu* est
officiel, l'*hébergeur* ne l'est pas. Empreinte SHA-256 au manifeste.

### Ce que cette seule année a révélé

Une année suffisait pour répondre à la seule question qui comptait : **de
combien notre approximation se trompe-t-elle ?**

**France 2013, chiffres officiels du GFN** (hectares globaux par personne) :

| | gha/pers |
|---|---:|
| Empreinte de consommation (importations incluses) | **5,063** |
| dont carbone | 2,852 (**56,3 %**) |
| Biocapacité disponible | **2,910** |
| **Rapport empreinte / biocapacité** | **1,740** |

Il faudrait 1,74 France pour soutenir le mode de vie français.

**Deux enseignements, dont un qui corrige le jalon P2 :**

1. **L'hypothèse « le carbone domine l'empreinte » est vérifiée — de peu.**
   56,3 %. L'approximation rate donc 43,7 % du sujet (cultures, forêts,
   pâturages, pêche, sol bâti), soit 2,21 gha/pers.

2. ⚠️ **Notre seuil était deux fois trop sévère.** Pour la même année 2013,
   notre approximation donne une pression `x = 3,41` ; le GFN donne
   `x = 1,74`. **Facteur 1,96.**

   Ce n'est pas une erreur de calcul : les deux référentiels ne posent pas
   la même question. Le seuil GIEC demande « quelle part du budget
   climatique mondial chaque humain peut-il utiliser ? » — planétaire et
   égalitaire. Le rapport du GFN demande « la France vit-elle sur sa
   propre biocapacité ? » — territorial. Les deux sont défendables.

   Pour reproduire le niveau du GFN, il faudrait un seuil de
   **4,17 tCO₂/hab**, soit exactement le bord supérieur de la fourchette
   1–4 t que la fiche EQ-EXEC-002 déclarait déjà en sensibilité. La
   calibration ne sort donc pas du cadre prévu : elle en désigne le bord.

**Ce que ça change concrètement** : sous le mapping linéaire, l'IEE 2013
passe de **0,00 à 0,26** — il cesse d'être nul, ce qui **supprime
l'annulation totale de la création monétaire française**. Sous le mapping
exponentiel, de 0,19 à 0,60.

### Ce que ça change à l'arbitrage
**Le seuil (D13) pèse autant que le mapping (D11)** — un facteur 1,96
contre un facteur allant de 0,00 à 0,72. Les deux décisions doivent être
tranchées **ensemble**, pas l'une après l'autre. D13 est requalifiée en
conséquence.

### Ce que ça ne règle pas
Une seule année d'ancrage recale le **niveau**, pas la **forme**. Si le
rapport empreinte/biocapacité français a évolué autrement que son
empreinte carbone entre 1990 et 2021, nous ne le voyons pas. Obtenir la
série GFN complète reste la seule vraie solution — et la recherche Dateno
a confirmé qu'elle exige la clé nominative.

### État
`python -m pytest -q` : **67 tests verts**. Registre conforme (11 fiches).


---

## 2026-08-27 — Session 3 (fin) : EXIOBASE, et une conclusion inversée

### Ce qui a été fait
Stéphane a demandé de chiffrer EXIOBASE avant de dépendre d'une licence
GFN. Chiffrage fait, puis série complète calculée.

### Faisabilité, mesurée et non estimée
EXIOBASE 3.10.2 (Zenodo, ouvert) : **1995–2024**, 7,1 Go, `pymrio` lit le
format nativement. Une année coûte ~70 s de téléchargement et ~162 s de
calcul (inversion d'une matrice 9 800 × 9 800). **Série complète : 111
minutes.** Comptes satellites disponibles : matières, sols, émissions
air, eau, énergie, emploi.

### Le résultat, qui inverse une conclusion du jalon P2

| Matières non renouvelables | 1995 | 2022 | Tendance |
|---|---:|---:|---|
| DMC territorial — *ce que mesurait l'IRNR* | 9,99 | 7,77 t/hab | **−22 %** |
| Empreinte, importations incluses | 9,58 | **12,12 t/hab** | **+26 %** |

Les deux mesures ne diffèrent pas en niveau : **elles vont en sens
contraire**. Le DMC disait que la France s'était allégée d'un cinquième ;
l'empreinte dit qu'elle s'est alourdie d'un quart.

L'écart passe de **−4 % en 1995 à +80 % en 2023** (moyenne +49 %). Cette
croissance régulière est la signature de la délocalisation :
**l'« amélioration » que mesurait l'IRNR était, pour l'essentiel, un
déménagement.**

**Conséquences :**
- L'IRNR n'est plus le seul indicateur à atteindre l'équilibre. En
  territorial il passait sous le seuil de 8 t/hab vers 2014 ; en
  empreinte, il ne passe **jamais** sous le seuil.
- L'IED baisse de ~9 % (0,54 → 0,49 en 2021). La conclusion du jalon P2
  tient, mais le récit change : **seul le carbone progresse vraiment**
  (IEE 0,12 → 0,26 entre 1995 et 2021). L'IRNR s'est effondré à 0,51 en
  2000 avant de remonter partiellement, sans revenir à son niveau de 1995.
- Le dividende par citoyen 2021 passe de 11 900 à **10 881 €/an**.

### Validation
Contrôle croisé du CO₂ entre EXIOBASE et le Global Carbon Project, deux
constructions indépendantes : **1,4 % d'écart en 2019**, 4,4 % en 2020.
⚠️ Aucun contrôle équivalent n'existe pour les matières. EXIOBASE est un
modèle, pas une observation directe — c'est écrit dans la fiche.

### Une erreur de comparaison, trouvée et corrigée
Le script de faisabilité comparait l'empreinte EXIOBASE divisée par la
population **Eurostat** (67,6 M) au DMC divisé par la population **OWID**
utilisée partout ailleurs (65,9 M) : deux France différentes. L'écart
annoncé était faussé de 2,5 %. Les repères sont désormais lus **depuis le
modèle lui-même**, ce qui rend l'erreur impossible à refaire.

### Une affirmation antérieure corrigée
`docs/06` affirmait que l'IBD était « le seul des trois indicateurs à
violer l'exigence §14.1 » (inclure les importations). C'était **faux** :
l'IRNR territorial la violait aussi. Depuis le passage à l'empreinte,
l'affirmation est devenue vraie.

### Ce que ça ne règle pas
L'empreinte démarre en **1995**, contre 1990 pour le DMC : cinq ans perdus
pour gagner la justesse du concept. Le territorial reste implémenté pour
la sensibilité et pour couvrir 1990–1994. Le trou 1978–1989 reste entier.

### Prochaine étape évidente
Les comptes **« sols »** d'EXIOBASE sont déjà dans la série calculée
(cultures, pâturages, forêt). Ils couvriraient les **44 % non carbonés**
qui manquent à l'IEE. La donnée est là, il reste à la brancher.

### État
`python -m pytest -q` : **75 tests verts**. Registre conforme (11 fiches).
Décisions en attente : **D7–D12** (D13 tranchée).


---

## 2026-08-27 — Session 3 (suite) : à quoi correspondent le 0 et le 2 ?

### La question
Stéphane : « les chiffres me semblent bizarres. Dans ton calcul le 0 et
le 2 correspondent à quoi au niveau de IBD, IEE et IRNR ? »

### La réponse, et le trou qu'elle révèle
**Seul le 1 est ancré.** La synthèse exige « vaut 1 à l'équilibre, borné
sur [0 ; 2] » et s'arrête là. Le 0 et le 2 avaient été remplis
implicitement par le choix de mapping, sans jamais être posés comme une
décision. C'était un trou dans le livrable P2.

Ce qu'ils valent réellement :
- **I = 2 ↔ x = 0** pour les trois mappings : le pays ne consomme *rien*.
  Ce n'est pas « parfaitement soutenable » — ça, c'est I = 1.
- **I = 0** dépend du mapping : x = 2 (linéaire) ou jamais (exponentiel,
  hyperbolique).

### Pourquoi le 0 est la question grave
Sous l'EH, la monnaie n'est créée **que** par le don. IED = 0 signifie
donc aucune création, pendant que la fonte continue de détruire le stock.
**Demi-vie de la masse monétaire : 5,7 ans** (fonte sur soldes seule),
**4,6 ans** avec la fonte transactionnelle.

⇒ IED = 0 n'est pas une pénalité, c'est l'**extinction monétaire** du
pays. La question devient : *à partir de quel niveau de destruction
l'EH décide-t-elle qu'un pays ne doit plus avoir de monnaie du tout ?*

Et le mapping linéaire y répond « deux fois le seuil » — ce qui **coupe
la France, l'Allemagne et l'Australie**, soit la quasi-totalité des pays
riches. À écarter.

### Une conséquence symétrique, rarement dite
Puisque `DETA = IED × 22 000 × c` et que IED est maximal à pression nulle,
**le système verse le double d'argent au pays dont l'activité économique
est nulle**. La création monétaire est maximale quand l'économie s'arrête.

### Le second défaut : les trois seuils ne se comparent pas

| | Seuil | Nature |
|---|---|---|
| IEE | 2,13 tCO₂/hab | budget planétaire (GIEC) |
| IRNR | 8 t/hab | corridor scientifique (Bringezu) |
| IBD | l'état de 1990 | ⚠️ **un état passé, pas un seuil** |

« IBD = 1 » veut dire *« comme en 1990 »* ; « IEE = 1 » veut dire *« dans
le budget de la planète »*. Ce ne sont pas les mêmes 1, et la moyenne
géométrique les traite comme s'ils l'étaient. C'était rangé dans les
limites de l'IBD sous le terme « référence glissante » — c'est en réalité
une **incohérence d'échelle entre les trois termes de l'IED**.

### La solution identifiée, et un obstacle
Le **Biodiversity Intactness Index** (BII) mesure la part de biodiversité
d'origine restante, et le cadre des limites planétaires (Steffen et al.
2015) fixe la frontière à **BII ≥ 90 %** : un vrai seuil, comparable au
budget carbone. Série du Natural History Museum, **1970–2050**, CC-NC.

⚠️ Téléchargement automatisé **bloqué par Cloudflare** (403), y compris
via navigateur sans affichage depuis cet environnement. **À récupérer à
la main en trente secondes** : `data.nhm.ac.uk/dataset/bii-bte`.
Bonus : la série remonte à 1970 et **rouvrirait la période 1978**.

### Livrables
- `docs/07-bornes-et-seuils.md` — les options chiffrées
- `scripts/bornes_indicateurs.py` — tout est reproductible
- Fiches `EQ-EXEC-003` et `EQ-EXEC-004` mises à jour

### Trois décisions de plus attendues
**D14** borne basse · **D15** borne haute · **D16** seuil de l'IBD.
Recommandation : plancher explicite (jamais d'extinction monétaire) ·
`[1 ; 2]` = régénération · BII à 90 %.

### État
`python -m pytest -q` : **75 tests verts**. Registre conforme (11 fiches).
Décisions en attente : **D7–D12, D14–D16**.


---

## 2026-08-27 — Session 3 (fin) : l'AMAE de l'OCDE chiffre le biais de l'IBD

### Ce qui s'est passé
Stéphane a transmis les *Perspectives de l'environnement de l'OCDE à
l'horizon 2050* (2012) en demandant si c'était le document dont je
parlais. **Non** — je parlais du BII du Natural History Museum et de
Steffen *et al.* (2015) pour la frontière à 90 %. Mais le document est
utile, et il a été versé au dépôt.

### Ce qu'il apporte
L'OCDE utilise l'**AMAE** (abondance moyenne des espèces, modèle GLOBIO)
et la définit exactement comme il faut : *« une AMAE de 100 % correspond
à l'absence de perturbation »* — un pourcentage de l'**état d'origine**,
pas d'un état passé arbitraire. C'est la construction qui manque à l'IBD.

Chiffres récupérés **par script** via les StatLinks du rapport
(`modele/donnees/ocde_amae.py`) :

| AMAE terrestre | 2010 | 2050 (projeté) |
|---|---:|---:|
| **Europe** | **38,4 %** | 29,3 % |
| Monde | 67,5 % | 60,4 % |

| Biome | 1970 | 2010 |
|---|---:|---:|
| **Forêts tempérées** (celui de la France) | **49,7 %** | **37,3 %** |

### Ce que ça démontre
**Dès 1970, le biome français n'avait déjà plus que la moitié de son
abondance d'origine.** Prendre 1990 comme référence, comme le fait notre
IBD, revient donc à déclarer à l'équilibre un écosystème déjà amputé de
moitié. Le biais était soupçonné et documenté ; il est maintenant
**chiffré**.

### Trois réserves, écrites dans le module et la fiche
1. **L'AMAE n'est pas le BII.** Cousins conceptuels, pas synonymes. La
   frontière de 90 % porte sur le **BII** (Steffen et al. 2015). La
   transférer à l'AMAE serait une erreur de catégorie — pas faite.
2. **Pas de France** : l'OCDE ne descend qu'à « Europe ».
3. **Projections de modèle** (GLOBIO/IMAGE) sur quatre points, pas des
   observations annuelles.

⇒ L'AMAE documente le concept et donne l'ordre de grandeur européen.
Elle **ne remplace pas** le BII pour construire l'IBD. Le téléchargement
manuel du BII reste noté en P0.

### État
`python -m pytest -q` : **78 tests verts**. Registre conforme (11 fiches).
Décisions en attente : **D7–D12, D14–D16**.
