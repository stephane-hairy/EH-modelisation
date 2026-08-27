# TODO

Statuts : `[ ]` à faire · `[~]` en cours · `[x]` fait · `[!]` **verrou** ·
`[?]` décision attendue de Stéphane

Priorités : **P0** bloquant · **P1** important · **P2** utile

---

## ✅ Décisions tranchées

Toutes actées dans `docs/04-decisions.md` (2026-08-27).

- [x] **D1** Formalisme **SFC** (Stock-Flux Cohérent)
- [x] **D2** Ordre des jalons : **P0 → P2 → P1 → …**
- [x] **D3** Périmètre : France seule + Reste du Monde agrégé
- [x] **D4** Fréquence : **cœur annuel + sous-pas mensuel pour la fonte**
      *(amendement : le mensuel complet est impossible, aucune donnée
      mensuelle de PIB ni de patrimoine sectoriel n'existe)*
- [x] **D5** Période : **1978–2023** pour le bloc réel+monétaire,
      **1995–2023** pour le modèle complet
      *(restriction : les comptes financiers par secteur démarrent en 1995)*
- [x] **D6** IED : moyenne géométrique conservée

---

## Jalon P0 — Fondations

- [x] Créer `CLAUDE.md`, `TODO.md`, `JOURNAL.md`
- [x] Récupérer et dépouiller la synthèse EH v1.7 (60 p.)
- [x] Rédiger `docs/01-economie-homeostatique.md`
- [x] Rédiger `docs/02-strategie-modelisation.md`
- [x] Rédiger `docs/03-protocole-rigueur.md` + schéma du registre
- [x] **P0** Environnement Python (`pyproject.toml`)
- [x] **P0** Clients de données INSEE / Eurostat / BCE
      *(`pandasdmx` écarté : sa v1.10 ne parse pas les structures INSEE)*
- [x] **P0** Cache reproductible : SHA-256 + horodatage + détection des
      révisions de séries (`modele/donnees/cache.py`)
- [x] **P0** `pytest` + intégration continue GitHub Actions
- [x] **P0** Contrôle automatique du registre d'équations
- [x] **P0** Audit de couverture des données
      → `docs/annexes/couverture-donnees.md`
- [x] **P1** PIB vérifié : 2 833,8 Md€ en 2023 (INSEE CNA-2020-PIB)
- [x] **P1** Production des SNF 2023 sourcée : 3 810 Md€
      (Eurostat `nasa_10_nf_tr`, série depuis 1971)
- [x] **P0 — la formule DENT a été analysée, et trois alternatives proposées**
      → `docs/05-dent.md` · `scripts/analyse_dent.py` · `tests/test_dent.py`
  - [x] **Périmètre chiffré** : SNF 3 810 Md€ / +finance 4 098 /
        +entrepreneurs individuels 4 614 / marchand total 5 310
        (Eurostat 2023) → **±39 %**, soit 1 500 Md€. Et **96 % des
        entreprises françaises n'ont pas de salarié** (1,17 personne par
        entreprise dans la classe 0–9, Eurostat `sbs_sc_ovw` 2022) : la
        formule §11.1 n'y est **pas définie**
  - [x] **`P` clarifié** : le vrai problème n'est pas « comptable vs
        comptes nationaux », c'est que **la somme des chiffres d'affaires
        n'est pas additive** — deux entreprises qui fusionnent font
        baisser la création monétaire du pays. VA des SNF 1 481 Md€
        contre production 3 810 Md€ : **rapport 2,57**
  - [x] **Dimension examinée** : le terme vaut **[personnes²]**, pas des
        euros, et ce pour les DEUX lectures possibles du PDF — lesquelles
        diffèrent entre elles d'un facteur **10⁸**. Diverge en `r → 0`
        (dividende infini pour l'entreprise parfaitement égalitaire)
  - [x] **Cliquet et rétroaction positive démontrés** : amplification ×5
        pour α = 0,8 ; la clause « hors DENT » ne retire que 1/N du flux,
        donc ne protège de rien → fiche `EQ-EH-005`
  - [x] **Trois alternatives** fichées en catégorie D avec plan de
        sensibilité : `EQ-EH-002` multiplicative · `EQ-EH-003` deux termes
        homogènes · `EQ-EH-004` valeur ajoutée. Écart **7,9×** sur DTENT
- [?] **D7–D10 — quatre décisions attendues de Stéphane** (`docs/05-dent.md` §8)
      ⚠️ Tant qu'elles ne sont pas prises, **aucun résultat quantitatif sur
      la masse monétaire en EH n'est publiable**.
  - [?] **D7 assiette** : production ou valeur ajoutée (facteur 2,6)
  - [?] **D8 forme** : alternative 1, 2, 3, ou combinaison
  - [?] **D9 périmètre** : SNF / +finance / +entrepreneurs individuels
  - [?] **D10 base `P`** : 3 meilleures années / moyenne glissante / exogène
- [ ] **P1** Vérifier les `[À VÉRIFIER]` restants de
      `scripts/ordre_grandeur_eh_france.py` : population, contribution
      française à M3, vitesse de circulation
- [ ] **P2** Vérifier si la Banque de France publie des comptes financiers
      par secteur **antérieurs à 1995**, et s'ils sont raccordables
      (permettrait de remonter le modèle complet avant 1995 — cf. D5)
- [ ] **P1** Estimer les blocs monétaires sur données mensuelles, puis
      agréger vers le pas annuel (cf. D4)
- [ ] **P1** Traiter les ruptures 1987 / 1993 / 1999 / 2008 / 2020 dans
      toute estimation sur la période longue (cf. D5)

---

## Jalon P2 ⭐ — Indicateurs EXEC historiques (France **1990–2021**)

*Livrable phare, LIVRÉ* → `docs/06-indicateurs-exec.md`,
`sorties/creation_monetaire_eh_france.png`

⚠️ **Période réduite, et c'est irréductible.** Le cadrage demandait
1978–2023. Les trois séries écologiques françaises **commencent toutes en
1990** (flux de matières, protocole STOC pour les oiseaux, tableaux
entrées-sorties mondiaux). Le trou est documenté, pas comblé (RÈGLE N°3).

- [x] **IEE** défini et calculé → `EQ-EXEC-002`. ⚠️ **Approximation** :
      empreinte **carbone** importations incluses (Global Carbon Project,
      MRIO Eora) et non empreinte écologique GFN — l'API du GFN exige une
      clé nominative (403 sans elle). Grade C
- [x] **IRNR** défini et calculé → `EQ-EXEC-001`. Le recyclage y compte
      positivement **par construction** (le DMC ne compte que la matière
      vierge) : ajouter un bonus serait un double comptage
- [x] **IBD** — ⚠️ **les données ne suffisent pas, et c'est le résultat**.
      Seule série : oiseaux communs agricoles 1990–2021, un taxon, un
      milieu, **aucune dimension importations** (viole §14.1), référence
      1990 arbitraire. Bouche-trou documenté → `EQ-EXEC-003`.
      Toutes les sorties publient l'IED **avec et sans IBD**
- [x] **Mapping vers [0 ; 2]** : trois variantes implémentées et testées
      → `EQ-EXEC-004`. **Non tranché** : voir D11
- [x] Séries récupérées par script, avec cache SHA-256
      (`modele/donnees/ecologie.py`, `modele/donnees/comptes.py`)
- [x] IBD, IEE, IRNR, IED calculés 1990–2021 → `donnees/traite/exec_france.csv`
- [x] DETA / DTCIT / DCIT / DTENT / DG_FR calculés
      → `donnees/traite/creation_monetaire_eh.csv`
- [x] **Graphique** + note méthodologique
- [x] Sensibilité au mapping publiée dans `scripts/construire_exec.py`
- [?] **D11–D13 — trois décisions attendues** (`docs/06-indicateurs-exec.md` §6)
  - [?] **D11 mapping** : linéaire / hyperbolique / exponentiel.
        IED 2021 de **0,00 à 0,72**. Fixe aussi le gain de boucle du P5
  - [?] **D12 sort de l'IBD** : garder en grade C / paramètre libre / retirer
  - [x] **D13 TRANCHÉE — étalon de l'IEE : MONDIAL par tête**
      (`docs/04-decisions.md` D13). L'étalon territorial est écarté : il
      récompense la géographie, pas le comportement. L'Australie, qui
      consomme 74 % de nature de plus que la France, y serait 2,3× mieux
      dotée ; le Bangladesh, qui consomme 7× moins, moins bien noté.
      ✅ **Conséquence : notre seuil carbone est validé à 15 % près**
      (notre x = 3,41 contre 2,97 pour le GFN en 2013). Un recalage exact
      donnerait 2,44 t/hab au lieu de 2,13. **Le jalon P2 tient.**
- [ ] **P2** Reste ouvert sur les seuils : matières 6–12 t/hab
- [x] **Empreinte écologique GFN retrouvée via Dateno** — paquet public
      officiel *National Footprint Accounts 2017* (licence CC).
      ⚠️ **Une seule année, 2013** : ce n'est pas la série. Sert de point
      d'ancrage → `modele/donnees/gfn.py`, `scripts/valider_iee_gfn.py`.
      France 2013 : empreinte 5,063 gha/pers (dont carbone 56,3 %),
      biocapacité 2,910, rapport **1,740** contre **3,41** pour notre
      approximation. Notre seuil était **deux fois trop sévère**
- [ ] **P1** Demander une **clé d'API Global Footprint Network** (gratuite).
      Confirmé par la recherche Dateno : **aucune série GFN complète
      n'est librement accessible**. La clé reste la seule action qui
      pourrait rouvrir la période 1978–1989 (comptes GFN depuis **1961**)
- [ ] **P2** Empreinte matières ODD 8.4.1 (UNEP/IRP) : **écartée**,
      l'ONU ne la publie qu'au niveau régional, pas par pays (vérifié)
- [x] **P1 EXIOBASE 3.10.2 intégré** — série 1995–2024 calculée
      (30 années, 111 min) → `donnees/traite/empreinte_exiobase_france.csv`,
      versionnée. Scripts : `serie_exiobase.py` (reprenable),
      `comparer_irnr.py`, `faisabilite_exiobase.py`.
      ⚠️ **Résultat : le DMC territorial inversait le signe de la
      tendance.** Territorial −22 % entre 1995 et 2022, empreinte **+26 %**.
      L'écart passe de −4 % (1995) à +80 % (2023) : signature de la
      délocalisation. L'IRNR n'atteint plus jamais l'équilibre, et l'IED
      baisse de ~9 %. Contrôle croisé CO₂ avec le Global Carbon Project :
      1,4 % d'écart en 2019
- [ ] **P1** Exploiter les **comptes « sols » d'EXIOBASE** (déjà dans la
      série : cultures, pâturages, forêt) pour couvrir les **44 % non
      carbonés** de l'IEE. C'est la suite logique et la donnée est là
- [ ] **P2** Chercher une empreinte biodiversité importations incluses
      (Chaudhary & Kastner) — seule voie pour un IBD conforme à §14.1

---

## Jalon P1 — Modèle SFC France (sans écologie)

- [ ] **P1** Matrice de bilan (6 secteurs) à partir des comptes financiers BCE/INSEE
- [ ] **P1** Matrice des flux de transactions
- [ ] **P1** Test automatique : lignes et colonnes somment à zéro
- [ ] **P1** Solveur (Gauss-Seidel / Newton) ou adoption de `sfctools`
- [ ] **P1** Blocs comportementaux + fiches de registre :
  - [ ] consommation des ménages
  - [ ] investissement des SNF
  - [ ] création monétaire par le crédit (McLeay et al. 2014)
  - [ ] crédit → activité (Schularick & Taylor 2012)
  - [ ] transmission BCE → taux bancaires
  - [ ] loi d'Okun (fiche exemple déjà rédigée)
  - [ ] formation des prix ⚠️ *maillon faible : Phillips aplatie*
  - [ ] budget public / multiplicateurs
  - [ ] commerce extérieur
- [ ] **P1** Backtest pré-enregistré : estimation 1995–2012, validation
      2013–2019, stress 2020–2023
- [ ] **P1** Comparaison aux repères naïfs (marche aléatoire, AR(1))

---

## Jalon P3 — Couplage écologique

- [ ] **P1** Registres matière et énergie (lignée Dafermos et al. 2017)
- [ ] **P1** Intensités carbone et matière par branche
- [ ] **P1** Empreinte importations via MRIO
- [ ] **P2** Vérifier que le modèle reproduit les émissions observées

---

## Jalon P4 — Modules EH

- [ ] **P1** Monnaie-don (DETA, DCIT, DENT, DG)
- [ ] **P1** Fonte (1 %/mois soldes + 1 %/transaction)
- [ ] **P1** PCED (4 catégories, rendements indexés sur la fonte)
- [ ] **P2** Crédit sans création monétaire
- [ ] **P2** Import/export à 4 régimes
- [ ] **P2** Élasticités de transmission (couche C) : dividende→conso
      (Alaska PFD, GiveDirectly), fonte→vitesse (Wörgl, WIR)

---

## Jalon P5 ⭐ — Analyse de stabilité

- [ ] **P1** Linéariser la boucle EXEC ↔ ENEC autour de IED = 1
- [ ] **P1** Valeurs propres, marge de phase, délais
- [ ] **P1** Cartographie (gain × délai) : stable / oscillant / divergent
- [ ] **P2** Si instable : proposer des correctifs (IED lissé, terme
      dérivé — régulateur PID plutôt que proportionnel)

---

## Jalons P6–P7

- [ ] **P2** Scénarios France sous EH + Monte-Carlo + indices de Sobol
- [ ] **P2** Note méthodologique reproductible de bout en bout

---

## Questions ouvertes à documenter (issues de la synthèse)

- [ ] Taux de change : « à développer » (§15) — bloquant pour l'ouverture
- [x] Réactualisation de `P` dans DENT sur les meilleures années →
      rétroaction positive **confirmée et chiffrée** (×5 pour α = 0,8),
      plus un effet cliquet (six ans de récession à −25 % ne font baisser
      la base que de 11 %) → `EQ-EH-005`, `docs/05-dent.md` §6
- [ ] Niveau des prix : la §10.1 affirme l'absence d'hyperinflation sans le
      démontrer — cf. calcul d'ordre de grandeur (16 × M3 actuel)
- [ ] Psychologie économique : « à développer » (§20)
