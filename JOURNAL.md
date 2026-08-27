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
