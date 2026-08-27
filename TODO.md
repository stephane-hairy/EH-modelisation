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
- [ ] **P1** Vérifier les `[À VÉRIFIER]` restants de
      `scripts/ordre_grandeur_eh_france.py` : population, M3 France,
      produits d'exploitation cumulés des entreprises (**c'est `DTENT` qui
      domine le total : c'est le chiffre le plus important à sourcer**)
- [ ] **P2** Vérifier si la Banque de France publie des comptes financiers
      par secteur **antérieurs à 1995**, et s'ils sont raccordables
      (permettrait de remonter le modèle complet avant 1995 — cf. D5)
- [ ] **P1** Estimer les blocs monétaires sur données mensuelles, puis
      agréger vers le pas annuel (cf. D4)
- [ ] **P1** Traiter les ruptures 1987 / 1993 / 1999 / 2008 / 2020 dans
      toute estimation sur la période longue (cf. D5)

---

## Jalon P2 ⭐ — Indicateurs EXEC historiques (France 1995–2023)

*Livrable phare : « quelle création monétaire l'EH aurait-elle donnée à la
France depuis 1995 ? »*

- [!] **P0 VERROU** Définir une formule calculable pour **IEE**
      (empreinte écologique, importations incluses) bornée sur [0 ; 2]
- [!] **P0 VERROU** Idem pour **IRNR** (ressources non renouvelables)
- [!] **P0 VERROU** Idem pour **IBD** (biodiversité) — *le plus difficile,
      les données peuvent ne pas suffire*
- [ ] **P0** Choisir et justifier le **mapping vers [0 ; 2]**
      (linéaire / log / plafonné) — décision structurante
- [ ] **P1** Récupérer : Global Footprint Network, Eurostat AEA + MFA,
      EXIOBASE (empreinte importations), ONB / INPN / Living Planet Index
- [ ] **P1** Calculer IBD, IEE, IRNR, IED — série annuelle 1995–2023
- [ ] **P1** Calculer DETA / DTCIT / DCIT / DTENT / DG_FR sur la période
- [ ] **P1** Graphique + note méthodologique
- [ ] **P2** Sensibilité au mapping et aux seuils de soutenabilité

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
- [ ] Réactualisation de `P` dans DENT tous les 3 ans sur les meilleures
      années → rétroaction **positive** cachée dans un modèle qui les refuse
- [ ] Niveau des prix : la §10.1 affirme l'absence d'hyperinflation sans le
      démontrer — cf. calcul d'ordre de grandeur (16 × M3 actuel)
- [ ] Psychologie économique : « à développer » (§20)
