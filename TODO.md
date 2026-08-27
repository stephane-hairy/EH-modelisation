# TODO

Statuts : `[ ]` à faire · `[~]` en cours · `[x]` fait · `[!]` **verrou** ·
`[?]` décision attendue de Stéphane

Priorités : **P0** bloquant · **P1** important · **P2** utile

---

## 🔴 Décisions attendues (bloquent la suite)

- [?] **P0** Valider le formalisme **SFC** (Stock-Flux Cohérent) —
      `docs/02-strategie-modelisation.md` §1.1
- [?] **P0** Valider l'ordre des jalons : **P0 → P2 → P1 → …**
      (indicateurs EXEC historiques avant le modèle complet) — §6
- [?] **P0** Périmètre : France seule + Reste du Monde agrégé, ou
      France + zone euro explicite ? — §8
- [?] **P0** Fréquence : annuelle, trimestrielle, ou mixte ? — §8
- [?] **P1** Début de période : 1995 ou 1978 ? — §8
- [?] **P1** L'IED (moyenne géométrique) est-il figé, ou peut-on tester
      des variantes si l'analyse de stabilité l'exige ? — §8

---

## Jalon P0 — Fondations

- [x] Créer `CLAUDE.md`, `TODO.md`, `JOURNAL.md`
- [x] Récupérer et dépouiller la synthèse EH v1.7 (60 p.)
- [x] Rédiger `docs/01-economie-homeostatique.md`
- [x] Rédiger `docs/02-strategie-modelisation.md`
- [x] Rédiger `docs/03-protocole-rigueur.md` + schéma du registre
- [ ] **P0** Environnement Python (`pyproject.toml`, versions figées)
- [ ] **P0** Pipeline de données : `pandasdmx` → INSEE / BCE / Eurostat,
      avec horodatage + SHA-256 de chaque série
- [ ] **P0** `pytest` + intégration continue
- [ ] **P0** Contrôle automatique du registre (fiche ⇄ code)
- [ ] **P1** Vérifier les entrées `[À VÉRIFIER]` de
      `scripts/ordre_grandeur_eh_france.py` sur données réelles
      (population, PIB, M3 France, produits d'exploitation cumulés)

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
