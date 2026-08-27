# Stratégie de modélisation

> Document de cadrage. Il fixe **quoi** on construit, **avec quoi**, **dans
> quel ordre**, et **comment on prouve que c'est juste**.
> Statut : proposition v1. À valider avant tout code de modèle.

---

## 1. Ce que je propose de changer à votre plan initial

Votre plan : (1) modèle France historique centré sur le système monétaire,
(2) calibration empirique, (3) greffe des mécanismes EH. **Ce plan est
bon et je le garde.** Je propose quatre modifications.

### Modif. 1 — Choisir explicitement le formalisme : SFC

Un « système dynamique » peut vouloir dire beaucoup de choses. Je propose
un **modèle Stock-Flux Cohérent** (SFC — *Stock-Flow Consistent*, Godley &
Lavoie, *Monetary Economics*, Palgrave, 2007).

**Vulgarisation** : un modèle SFC, c'est une comptabilité complète de
l'économie où **chaque euro vient de quelque part et va quelque part**.
La dépense de l'un est le revenu de l'autre ; la dette de l'un est
l'actif de l'autre. Rien ne disparaît par magie.

Quatre raisons, dont une décisive :

1. **C'est le seul formalisme où « créer de la monnaie » veut dire quelque
   chose de précis.** L'EH est *entièrement* une théorie de la création et
   de la destruction monétaire. Dans un modèle SFC, la monnaie-don est une
   ligne d'entrée dans les comptes des secteurs, et la fonte est une ligne
   de sortie. C'est direct. Dans un modèle de croissance standard ou un
   DSGE, la monnaie est souvent un voile sans bilan — on ne peut
   littéralement pas écrire l'EH.
2. **Le maximum de rigueur pour le minimum d'estimation.** Dans un SFC,
   ~2/3 des équations sont des **identités comptables** : vraies par
   construction, aucune étude nécessaire. Seul le tiers restant
   (comportements) demande un fondement empirique. Votre exigence de
   traçabilité devient réalisable au lieu d'être écrasante.
3. **Garde-fou anti-erreur.** Un SFC impose une contrainte redoutable :
   toutes les lignes et colonnes du tableau des flux doivent sommer à
   zéro. Si on se trompe, ça ne boucle pas. C'est un test automatisable —
   on le mettra dans la CI.
4. **Précédents publiés sur exactement notre problème.** Il existe une
   littérature évaluée par les pairs de SFC **écologiques** :
   - Dafermos, Nikolaidi & Galanis, *A stock-flow-fund ecological
     macroeconomic model*, **Ecological Economics** 131 (2017) — matrice
     bilancielle + flux de matière et d'énergie couplés. Modèle DEFINE.
   - Jackson & Victor, *LowGrow SFC* (Canada), Ecological Economics, 2020.
   - D'Alessandro et al., *EUROGREEN*, **Nature Sustainability** 3 (2020) —
     scénarios post-croissance pour la France, justement.
   - Cahen-Fourot & Lavoie, *Ecological monetary economics*, Ecological
     Economics 126 (2016).

   → On ne part pas de zéro, on se greffe sur une lignée validée.

### Modif. 2 — Séparer strictement trois couches

C'est le point le plus important. Votre règle « chaque relation doit être
fondée scientifiquement » **ne peut pas s'appliquer aux règles de l'EH
elles-mêmes** : le « 22 000 € par citoyen » ou le « 1 % de fonte par
mois » ne sont pas des faits observés, ce sont des **choix de conception**.
Les traiter comme des relations empiriques serait une faute
méthodologique — et la critique la plus facile à nous faire.

| Couche | Nature | Exigence | Exemples |
|---|---|---|---|
| **A — Positive** | Comment la France fonctionne réellement | Identité comptable, ou étude/estimation sourcée. **Falsifiable, backtestable** | Loi d'Okun, élasticité crédit→PIB, intensité carbone du PIB |
| **B — Design** | Règles inventées par l'EH | **Aucune** — mais marquage explicite « non empirique » + analyse de sensibilité obligatoire | `DETA = IED × 22 000 × c` ; fonte 1 %/mois ; rendements PCED |
| **C — Transmission** | Comment les instruments B se propagent dans le monde A | **La plus exigeante** : c'est ici qu'on peut se tromper sans le voir | Propension à consommer un dividende universel ; effet d'une fonte sur la vitesse de circulation |

**Conséquence** : nos résultats ne se présenteront jamais comme
« l'EH produira X ». Ils se présenteront comme :
> « Sous les règles de conception B (arbitraires, documentées) et les
> élasticités de transmission C (sourcées, avec intervalle de confiance),
> le modèle A calibré sur la France 1995–2023 produit X ± Y. »

C'est la seule formulation défendable devant un économiste.

### Modif. 3 — Un livrable intermédiaire à forte valeur, avant tout le reste

Avant de simuler l'EH, il y a un résultat que **personne n'a jamais
produit** et qui est atteignable vite :

> **Reconstituer IBD, IEE, IRNR et IED pour la France, année par année,
> de 1995 à aujourd'hui.**

Intérêt :
- C'est le **verrou n°1** du projet (aucune formule d'indicateur n'existe
  dans la synthèse — il faut les créer).
- C'est 100 % empirique, donc conforme à votre exigence de rigueur.
- Ça donne immédiatement la courbe « quelle aurait été la création
  monétaire française sous EH depuis 1995 ? » — un graphique parlant, sans
  aucune hypothèse comportementale.
- Ça teste très tôt la question de la **stabilité de la boucle** : si l'IED
  français s'est effondré de 1995 à 2023, l'EH aurait imposé une
  contraction monétaire continue. Est-ce soutenable ? C'est une vraie
  question, et on l'aura posée avec des chiffres.

C'est le jalon **P2** ci-dessous. Je recommande de le viser en priorité.

### Modif. 4 — Traiter l'EH comme un système asservi, pas seulement comme une économie

L'EH est, littéralement, un **régulateur automatique** : un capteur (les
indicateurs), une consigne (IED = 1), un actionneur (la création
monétaire). C'est de l'automatique, et l'automatique a des théorèmes.

Le risque n'est pas idéologique, il est technique : **une boucle de
rétroaction avec un long délai oscille au lieu de converger** (Sterman,
*Business Dynamics*, 2000, ch. 17 ; effet coup de fouet / *bullwhip*).
Or les délais de l'EH sont énormes :
- une politique écologique met 3 à 10 ans à modifier la biodiversité ;
- les indicateurs sont mesurés annuellement ;
- l'économie réagit au dividende en quelques trimestres.

Un système qui corrige aujourd'hui une dégradation d'il y a 5 ans peut
parfaitement **amplifier** les cycles au lieu de les amortir. La synthèse
affirme la stabilité (§10.1) sans la démontrer.

→ On produira une **analyse de stabilité formelle** : linéarisation autour
du point d'équilibre, valeurs propres du jacobien, marge de phase,
cartographie des zones (gain de rétroaction × délai) stables /
oscillantes / divergentes.

**C'est probablement la contribution scientifique la plus forte que ce
dépôt puisse apporter à l'EH** — et si le résultat est « instable pour
ces paramètres », c'est une information précieuse qui permet de corriger
le modèle (ex. : lisser l'IED, ajouter un terme dérivé — un régulateur PID
plutôt que proportionnel).

---

## 2. Architecture du modèle

### 2.1 Secteurs (matrice de bilan)

Six secteurs, standard de la comptabilité nationale française :

| Secteur | Code INSEE | Rôle |
|---|---|---|
| Ménages | S14+S15 | consomment, épargnent, empruntent, travaillent |
| Sociétés non financières | S11 | produisent, investissent, empruntent, émettent |
| Sociétés financières (banques) | S12 | **créent la monnaie par le crédit** (modèle A) |
| Banque centrale | S121 | Banque de France / Eurosystème |
| Administrations publiques | S13 | dépensent, taxent, s'endettent |
| Reste du monde | S2 | importe, exporte, détient des actifs |

Plus, pour la version écologique, **deux registres non monétaires**
(Dafermos et al. 2017) :
- **stocks de matière** : réserves, matière en usage, déchets ;
- **stocks d'énergie / émissions** : énergie utilisée, CO₂ atmosphérique.

### 2.2 Les deux tableaux obligatoires

Tout SFC repose sur deux tableaux que l'on doit publier :
1. **Matrice de bilan** — qui détient quoi (stocks). Chaque actif est le
   passif de quelqu'un ; les lignes somment à zéro.
2. **Matrice des flux de transactions** — qui paye quoi à qui. Lignes ET
   colonnes somment à zéro.

Ces deux tableaux sont le **contrat de cohérence** du modèle. Ils sont
testés automatiquement à chaque exécution (`pytest`).

### 2.3 Blocs comportementaux et leur ancrage empirique (couche A)

Liste de travail — chaque ligne deviendra une ou plusieurs fiches du
registre. Les références sont des **pistes à vérifier et à re-tester sur
données françaises**, pas des acquis.

| Bloc | Relation | Piste d'ancrage | Cat. |
|---|---|---|---|
| Consommation | C = f(revenu disponible, richesse) | Effets de richesse en France : Arrondel, Lamarche & Savignac (Banque de France) ; cointégration conso-revenu-patrimoine | S |
| Investissement | I = f(accélérateur, profit, coût du capital, crédit) | Bond & Van Reenen (Handbook of Econometrics) ; travaux BdF | S |
| **Création monétaire** | Les crédits font les dépôts | McLeay, Radia & Thomas, *Money creation in the modern economy*, **BoE Quarterly Bulletin 2014 Q1** ; test empirique : Werner (2014), *Int. Rev. Fin. Analysis* | **C** |
| Crédit → activité | Le crédit précède et amplifie le cycle | Schularick & Taylor, *Credit Booms Gone Bust*, **AER 102(2), 2012** — 14 pays, 140 ans | S |
| Transmission BCE | taux directeur → taux bancaires → crédit | Littérature *pass-through* BCE ; règle de Taylor estimée zone euro | S |
| Emploi | Loi d'Okun (croissance ↔ chômage) | Corrélation très forte, réestimable directement sur INSEE. **Cas idéal pour votre critère** | S |
| Prix | Inflation | ⚠️ **Point faible** : la courbe de Phillips s'est aplatie post-2008 (débat ouvert). Alternative : inflation de conflit / marges, usuelle en SFC | S (grade C) |
| Budget public | Multiplicateurs budgétaires | Ramey (*J. Econ. Lit.* 2019, revue) ; Blanchard & Leigh (**AER P&P 2013**) ; Auerbach & Gorodnichenko (dépendance à l'état du cycle) | S |
| Commerce extérieur | Élasticités import/export | Imbs & Méjean pour la France ; élasticités-prix et -revenu | S |
| **Couplage écologique** | PIB / production → émissions, matière | Comptes d'émissions Eurostat (AEA) ; décomposition Kaya-LMDI ; empreinte via MRIO **EXIOBASE / Exiobase-FR** (indispensable pour compter les importations, exigé par l'EH §14.1) | S |
| **Biodiversité** | pressions → état de la biodiversité | ⚠️ **Le maillon le plus faible.** IPBES (2019) ; Living Planet Index ; indicateurs ONB. Relations qualitatives, rarement chiffrables | S (grade C) |

### 2.4 Les élasticités de transmission (couche C) — les plus critiques

Ce sont elles qui décident du résultat. Elles doivent venir
d'**expériences réelles**, aussi proches que possible du mécanisme EH :

| Mécanisme EH | Où trouver l'élasticité empirique |
|---|---|
| Dividende universel (DCIT) → consommation | **Alaska Permanent Fund Dividend** (Jones & Marinescu, *AEJ: Economic Policy* 2022) ; transferts iraniens ; expérimentations de revenu de base (Finlande, Kenya/GiveDirectly — Egger et al., **Econometrica** 2022) |
| Fonte (demurrage) → vitesse de circulation | **Wörgl** (Autriche, 1932–33) ; **banque WIR** suisse (Stodder, *J. Econ. Behavior & Org.* 2009) ; monnaies locales fondantes contemporaines |
| Suppression des impôts → comportements | Littérature élasticité du revenu imposable (Saez, Slemrod & Giertz, *JEL* 2012) |
| PCED → réallocation de l'épargne | Littérature sur les rendements et l'arbitrage de portefeuille |

**Attention explicite** : ces expériences sont **locales et de petite
échelle**. Extrapoler l'élasticité de Wörgl (village, 1932) à la France
entière est une hypothèse forte. Elle sera marquée comme telle, et
soumise à sensibilité large.

### 2.5 La couche EH (couche B) — modules à greffer

| Module | Ce qu'il remplace | Fichier prévu |
|---|---|---|
| Indicateurs EXEC (IBD, IEE, IRNR, IED) | *(n'existe pas aujourd'hui)* | `modele/exec/` |
| Monnaie-don (DETA, DCIT, DENT, DG) | La création monétaire par le crédit bancaire | `modele/eh/don.py` |
| Fonte | Le remboursement des crédits | `modele/eh/fonte.py` |
| PCED | *(n'existe pas)* | `modele/eh/pced.py` |
| Crédit sans création monétaire | Le crédit bancaire actuel | `modele/eh/credit.py` |
| Import/export à 4 régimes | Le commerce extérieur standard | `modele/eh/exterieur.py` |

---

## 3. Le problème n°1 : opérationnaliser les indicateurs

Sans IBD, IEE et IRNR calculables, **rien n'est simulable**. La synthèse
n'en donne aucune formule. C'est notre premier vrai travail de recherche.

Contrainte de conception : chaque indicateur doit valoir **1 à
l'équilibre**, être borné entre 0 et 2, et se calculer sur données
publiques annuelles françaises.

Proposition de départ (à débattre, **couche B** = choix, pas mesure) :
construire chaque indicateur comme un **ratio à un seuil de soutenabilité**,
puis le mapper sur [0 ; 2].

| Indicateur | Numérateur (mesuré) | Dénominateur (seuil soutenable) | Sources de données |
|---|---|---|---|
| **IEE** | Empreinte écologique de la France, importations incluses | Biocapacité disponible | Global Footprint Network ; Eurostat AEA ; EXIOBASE |
| **IRNR** | Consommation intérieure de matières non renouvelables (DMC/RMC) | Part « soutenable » par habitant compte tenu des stocks mondiaux | Eurostat *Material Flow Accounts* ; SDES |
| **IBD** | Indice d'état de la biodiversité | État de référence / climax | ONB ; Living Planet Index ; INPN. ⚠️ Le plus difficile |

Le mapping vers [0 ; 2] est un choix normatif majeur (linéaire ?
logarithmique ? plafonné ?) : il **changera radicalement la dynamique**
et sera donc testé en sensibilité, pas fixé arbitrairement.

---

## 4. Données : tout par API, rien à la main

| Domaine | Source | Accès |
|---|---|---|
| Comptes nationaux, PIB, emploi, prix | **INSEE** (base 2020) | API SDMX / `pandasdmx` |
| Comptes financiers par secteur (stocks & flux) | **BCE — QSA** (*Quarterly Sector Accounts*) | SDMX BCE |
| Monnaie, crédit, bilans bancaires | **BCE — BSI** ; Banque de France (Webstat) | SDMX |
| Taux d'intérêt, politique monétaire | BCE (MIR, FM) | SDMX |
| Comparaisons européennes | Eurostat, AMECO | SDMX |
| Émissions, énergie, matières | Eurostat (AEA, MFA), CITEPA | SDMX / CSV |
| Empreinte importations | **EXIOBASE** (MRIO) | téléchargement scripté |
| Biodiversité | ONB, INPN, Living Planet Index | à instrumenter |

**Règle** : chaque série est récupérée par un script versionné, avec
horodatage et empreinte SHA-256 du fichier obtenu. Une exécution du dépôt
en 2027 doit produire les mêmes chiffres qu'en 2026, ou signaler la
révision.

### Point d'attention majeur : la France n'a pas de souveraineté monétaire

Depuis 1999, la France ne crée pas sa monnaie. La création monétaire est
le fait des banques commerciales de la zone euro et de l'Eurosystème.
Le modèle historique **doit** représenter cela correctement (refinancement
BCE, TARGET2, contrainte de la zone monétaire).

C'est aussi une limite honnête à poser d'emblée : passer à l'EH signifie
pour la France sortir de l'euro **et** confier sa monnaie à une BCI. Le
saut de régime est tel qu'aucune comparaison quantitative directe
« France 2023 réelle vs. France 2023 en EH » n'est rigoureusement valide.
Nous parlerons de **scénarios contrastés**, jamais de contrefactuel exact.

---

## 5. Validation : comment on prouve que le modèle A est bon

Protocole **pré-enregistré** (fixé avant de voir les résultats) :

1. **Découpage temporel figé une fois pour toutes**
   - Estimation : 1995–2012
   - Validation (jamais touchée pendant le calage) : 2013–2019
   - Test de résistance : 2020–2023 (COVID + choc énergétique)
2. **Référence de comparaison** : le modèle doit battre des repères naïfs
   (marche aléatoire, AR(1), tendance linéaire). Un modèle complexe qui ne
   bat pas une marche aléatoire est un modèle inutile — on le dira.
3. **Métriques publiées** : RMSE, MAE, **U de Theil**, et décomposition de
   l'erreur (biais / variance / covariance).
4. **Reproduction des faits stylisés** : le modèle doit reproduire sans
   qu'on le lui ait demandé — la récession de 2009, la corrélation
   crédit/investissement, la part salariale, le comportement du chômage.
5. **Sensibilité systématique** : Monte-Carlo + indices de Sobol sur tous
   les paramètres. On publie **quels paramètres décident du résultat**.
6. **Cohérence SFC** : test automatique — toutes les lignes et colonnes
   des matrices somment à zéro à chaque période. Non négociable.

**Interdit** : recalibrer sur la période de validation. Si le modèle échoue
en validation, on le documente dans `JOURNAL.md` et on révise la
structure — on ne bricole pas les paramètres.

### La critique de Lucas — à traiter, pas à esquiver

**Vulgarisation** : les comportements qu'on mesure aujourd'hui dépendent
des règles du jeu actuelles. Si on change les règles (et l'EH les change
toutes), les gens ne se comporteront plus pareil. Un modèle calibré sur
l'ancien monde peut donc mal prédire le nouveau.

C'est **la** faiblesse structurelle de tout ce projet. Atténuations :
- privilégier les paramètres « profonds » (techniques, physiques,
  démographiques) sur les paramètres comportementaux ;
- pour la couche C, aller chercher les élasticités dans les expériences
  **les plus proches du régime EH** (§2.4), pas dans le régime actuel ;
- présenter des **fourchettes larges** et des scénarios, jamais un chiffre
  central seul ;
- publier la sensibilité : si le résultat tient quel que soit le paramètre
  comportemental, il est robuste ; sinon, on le dit.

---

## 6. Feuille de route

| Jalon | Contenu | Livrable vérifiable |
|---|---|---|
| **P0** — Fondations | Structure du dépôt, registre d'équations, pipeline de données, CI, tests | Un `pytest` vert ; une série INSEE récupérée par script |
| **P1** — SFC France minimal | 6 secteurs, ~40 équations, annuel, **sans écologie**. Reproduit les comptes 1995–2023 | Matrices bilan + flux qui bouclent à zéro ; backtest publié |
| **P2** — Indicateurs EXEC historiques ⭐ | IBD, IEE, IRNR, IED pour la France 1995–2023 + courbe « création monétaire EH implicite » | Graphique + note méthodologique. **Livrable phare, à viser tôt** |
| **P3** — Couplage écologique | Blocs matière/énergie/émissions branchés sur le SFC (lignée DEFINE) | Le modèle reproduit les émissions françaises observées |
| **P4** — Modules EH | Monnaie-don, fonte, PCED, crédit EH, import/export 4 régimes | Modules isolés, testés unitairement |
| **P5** — Analyse de stabilité ⭐ | La boucle EH converge-t-elle ? Cartographie gain × délai | Diagramme de stabilité + recommandation de régulation |
| **P6** — Scénarios | France sous EH, avec fourchettes d'incertitude et Sobol | Rapport de scénarios |
| **P7** — Publication | Note méthodologique complète, reproductible de bout en bout | Dépôt clonable → résultats identiques |

⭐ = livrables à forte valeur ajoutée, indépendants du reste, prioritaires.

**Ordre recommandé** : P0 → **P2** → P1 → P3 → P4 → P5 → P6 → P7.
P2 avant P1 : il est autonome, rapide, et il informe tout le reste.

---

## 7. Risques identifiés

| Risque | Gravité | Traitement |
|---|---|---|
| Les données de biodiversité ne permettent pas de construire un IBD sérieux | **Élevée** | Traiter l'IBD en scénarios ; publier explicitement l'incertitude ; ne pas masquer le trou |
| La boucle EH s'avère instable | Moyenne | **C'est un résultat, pas un échec.** Proposer des correctifs (lissage, régulateur PID) |
| Critique de Lucas invalidant les extrapolations | **Élevée** | Fourchettes, scénarios, sensibilité, honnêteté (§5) |
| Périmètre qui explose (modèle qui veut tout faire) | Élevée | Jalons courts et livrables autonomes ; refuser d'ajouter un secteur sans passage par `TODO.md` |
| Confusion couches A / B | **Critique** | Le registre d'équations rend la confusion impossible : le champ `categorie` est obligatoire |
| Sur-ajustement | Moyenne | Protocole pré-enregistré, période de validation sanctuarisée |

---

## 8. Décisions à valider par vous avant de coder

1. **Formalisme SFC** — d'accord ?
2. **Ordre P0 → P2 en priorité** (indicateurs EXEC historiques avant le
   modèle complet) — d'accord ?
3. **Périmètre géographique** : France seule (avec le Reste du Monde
   agrégé), ou France + zone euro explicite ?
4. **Fréquence** : annuelle (données écologiques disponibles) ou
   trimestrielle (meilleure économétrie monétaire) ? Je penche pour
   **annuel** pour le cœur, trimestriel pour les blocs monétaires estimés
   séparément.
5. **Point de départ historique** : 1995 (comptes financiers complets) ou
   1978 (séries longues, mais avant l'euro et les comptes harmonisés) ?
6. **L'IED tel que défini est-il figé** ou peut-on proposer des variantes
   (IED lissé, IED avec terme dérivé) si l'analyse de stabilité l'exige ?
