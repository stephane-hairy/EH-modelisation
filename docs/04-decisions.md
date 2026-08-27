# Registre des décisions

Une décision par section. Format : **contexte → décision → raison →
conséquences**. Une décision prise ne se rediscute que si un fait
nouveau apparaît ; dans ce cas on ajoute une section « Révision ».

---

## D1 — Formalisme : modèle Stock-Flux Cohérent (SFC)

**Décidé le** 2026-08-27 · **Statut** : adopté

**Décision** : le cœur du modèle est un modèle **Stock-Flux Cohérent**
(Godley & Lavoie, *Monetary Economics*, 2007), et non un système
dynamique générique.

**Raison** : c'est le seul cadre où « créer de la monnaie » a un sens
comptable précis — or l'EH est *entièrement* une théorie de la création et
de la destruction monétaire. Bénéfice secondaire : environ deux tiers des
équations deviennent des identités comptables, ce qui rend la RÈGLE N°2
(traçabilité) tenable au lieu d'écrasante.

**Conséquences** : deux matrices obligatoires (bilan, flux de
transactions), testées automatiquement à zéro à chaque période. Lignée
écologique à suivre : Dafermos, Nikolaidi & Galanis (2017), Jackson &
Victor (2020), EUROGREEN (2020).

---

## D2 — Priorité : les indicateurs EXEC historiques avant le modèle complet

**Décidé le** 2026-08-27 · **Statut** : adopté

**Décision** : ordre des jalons **P0 → P2 → P1 → P3 → P4 → P5 → P6 → P7**.
Le jalon P2 (reconstituer IBD, IEE, IRNR et IED pour la France) passe
avant le modèle SFC lui-même.

**Raison** : P2 est autonome, entièrement empirique, et lève le verrou n°1
du projet (aucune formule d'indicateur n'existe dans la synthèse). Il
produit tôt un résultat lisible : la courbe de création monétaire que
l'EH aurait donnée à la France.

---

## D3 — Périmètre : France seule, Reste du Monde agrégé

**Décidé le** 2026-08-27 · **Statut** : adopté

**Décision** : six secteurs — ménages, sociétés non financières, banques,
banque centrale, administrations publiques, **reste du monde agrégé**.
Pas de zone euro explicitement désagrégée.

**Conséquence à assumer** : la France ne crée pas sa monnaie depuis 1999.
Avec un Reste du Monde agrégé, la contrainte de l'euro est représentée de
façon **réduite** (le secteur bancaire est preneur des conditions
extérieures) et non structurelle. C'est une simplification, à écrire noir
sur blanc dans toute publication de résultat.

---

## D4 — Fréquence : cœur annuel, sous-pas mensuel pour la monnaie

**Décidé le** 2026-08-27 · **Statut** : adopté, **en amendement de la
préférence initiale pour le mensuel**

**Contexte.** La préférence exprimée était « plutôt mensuel ». L'audit des
sources (`scripts/audit_couverture.py`,
`docs/annexes/couverture-donnees.md`) montre que ce n'est pas praticable :

| Ce qu'il faut | Fréquence réellement disponible | Depuis |
|---|---|---|
| PIB, consommation, investissement | **annuelle** (trimestrielle au mieux) | 1949 |
| Comptes financiers par secteur (qui détient quoi) | annuelle / trimestrielle | 1995 / 1998-Q4 |
| Crédits et monnaie | **mensuelle** | 2003 |
| Prix | **mensuelle** | 1970 |
| Émissions, matières, biodiversité | **annuelle** | 1990 |

Il n'existe **aucune** donnée mensuelle de PIB, d'investissement ou de
patrimoine sectoriel en France. Un modèle mensuel complet serait calé sur
des séries interpolées, c'est-à-dire sur des chiffres inventés — exclu par
la RÈGLE N°3.

**Décision — deux horloges** :
1. **Cœur du modèle : pas annuel.** C'est la fréquence de la contrainte
   dure (écologie et comptes financiers).
2. **Bloc monétaire : sous-pas mensuel analytique à l'intérieur du pas
   annuel.** La fonte est définie mensuellement (1 % en fin de mois) ; on
   la calcule exactement en 12 sous-pas plutôt que de l'approximer par un
   taux annuel. C'est indispensable : l'ordre des versements et des fontes
   dans l'année change le résultat, et la synthèse le souligne (§10.3).
3. Les relations purement monétaires (transmission des taux, crédit)
   peuvent être **estimées** sur données mensuelles, puis agrégées.

**Ce qu'on obtient** : la préférence pour le mensuel est satisfaite là où
elle a un sens — le mécanisme de fonte — sans caler le modèle sur des
données qui n'existent pas.

---

## D5 — Période : 1978 pour le bloc réel, 1995 pour le modèle complet

**Décidé le** 2026-08-27 · **Statut** : adopté, **avec la restriction que
les données imposent**

**Contexte.** Demande : « 1978 si possible ». Résultat de l'audit :

- **PIB et agrégats réels : disponibles depuis 1949.** 1978 est donc
  largement possible côté économie réelle.
- **Comptes financiers par secteur : 1995 au plus tôt** (INSEE, base
  2014 ; BCE trimestriel à partir de 1998-Q4). Or ces comptes *sont* la
  colonne vertébrale d'un modèle SFC : sans eux, on ne sait pas qui
  détient quoi, donc on ne peut pas boucler les matrices.
- **Écologie : 1990** (matières, inventaire GES) ; comptes d'émissions
  par branche seulement **2008**.

**Décision — deux périmètres temporels** :

| Périmètre | Période | Usage |
|---|---|---|
| **Long** | **1978–2023** | Bloc réel + monétaire : la question « comment le système monétaire agit sur l'économie réelle ». Estimation des relations de comportement |
| **Complet** | **1995–2023** | Modèle SFC bouclé + couplage écologique + scénarios EH |

**Pourquoi c'est une bonne nouvelle et pas seulement une contrainte** :
la période 1978–1998 contient l'**encadrement du crédit** (supprimé en
1987) et le passage à la déréglementation financière. C'est une
**expérience naturelle** sur exactement notre question : que se passe-t-il
quand on change le mécanisme par lequel la monnaie est créée ? Peu de
travaux l'exploitent. C'est un actif du projet.

**Ruptures structurelles à traiter explicitement** : 1987 (fin de
l'encadrement du crédit), 1993 (crise du SME), 1999 (euro), 2008, 2020.
Chaque estimation sur la période longue devra tester la stabilité des
coefficients autour de ces dates.

**À explorer** (noté au `TODO.md`, non bloquant) : la Banque de France a
publié des comptes financiers nationaux antérieurs à 1995, hors API
propre. S'ils sont exploitables et raccordables, le périmètre complet
pourrait remonter. À vérifier, sans en dépendre.

---

## D6 — IED : moyenne géométrique conservée

**Décidé le** 2026-08-27 · **Statut** : adopté

**Décision** : l'indicateur d'équilibre dynamique reste
`IED = (IBD × IEE × IRNR)^(1/3)`, conformément à la synthèse (§8.2).

**Raison** : le choix est mathématiquement solide. Un indicateur
catastrophique reste catastrophique et n'est pas rachetable par un
excédent ailleurs — ce qu'une moyenne arithmétique permettrait.

**Conséquence à surveiller** : la moyenne géométrique s'annule dès qu'un
indicateur atteint zéro, et sa pente devient très raide près de zéro. Si
un indicateur s'effondre, la création monétaire s'effondre d'un coup.
Ce comportement sera examiné au jalon P5 (analyse de stabilité). Si une
variante s'avère nécessaire pour la stabilité, elle sera proposée comme
**alternative documentée**, pas substituée en silence.

---

## D13 — IEE : l'étalon est mondial, pas territorial

**Décidé le** 2026-08-27 · **Statut** : adopté

**Contexte.** L'IEE compare une pression à un seuil. Le Global Footprint
Network en propose deux, et ils ne disent pas du tout la même chose :

| Étalon | Question posée | Ce qu'il note |
|---|---|---|
| **« nombre de Terres »** — empreinte ÷ biocapacité **mondiale** par humain | *Combien faudrait-il de planètes si tout le monde vivait comme ce pays ?* | le **comportement** |
| **« nombre de pays »** — empreinte ÷ biocapacité **du pays** | *Ce pays vit-il sur ses propres moyens ?* | la **géographie** |

**Décision** : l'IEE utilise l'étalon **mondial par tête**.

**Raison — l'étalon territorial crée une incitation perverse.** Chiffres
2013 (GFN), mapping exponentiel :

| Pays | Empreinte (gha/pers) | IEE, étalon mondial | IEE, étalon territorial |
|---|---:|---:|---:|
| Bangladesh | 0,75 | **1,47** | 0,50 |
| France | 5,06 | 0,26 | 0,60 |
| Australie | 8,80 | **0,06** | **1,35** |

Sous l'étalon territorial, **l'Australie — qui consomme 74 % de nature de
plus que la France — recevrait 2,3 fois plus de monnaie**, parce qu'elle
dispose d'espace. Et le **Bangladesh, qui consomme 7 fois moins que la
France, serait moins bien noté qu'elle**, parce qu'il est densément
peuplé.

Pour une théorie mondiale dont le mécanisme central est de récompenser la
vertu écologique par la création monétaire, récompenser en réalité la
faible densité de population est une faille de conception majeure.

**Conséquences** :

1. Le seuil carbone actuel (2,13 tCO₂/hab, budget 1,5 °C du GIEC partagé
   par tête) relève **déjà** de cette logique. Il est **validé à 15 %
   près** contre le point d'ancrage GFN 2013 : notre approximation donne
   `x = 3,41`, le GFN donne `x = 2,97`. Un recalage exact donnerait
   2,44 t/hab — un ajustement mineur, très à l'intérieur de la fourchette
   1–4 t déjà déclarée en sensibilité.
2. **Le jalon P2 n'a donc pas à être refait.** Les conclusions tiennent.
3. L'étalon territorial reste implémenté (`ratio_territorial`) et passe en
   analyse de sensibilité — jamais en série principale.
4. **Correction actée** : une note antérieure concluait que « notre seuil
   était deux fois trop sévère ». Cette conclusion ne valait que contre
   l'étalon territorial, désormais écarté. Contre l'étalon retenu, l'écart
   est de 15 %.

**Ce qui reste ouvert** : nous n'avons qu'**une année** d'ancrage (2013).
Elle valide le *niveau* de la série, pas sa *forme*. Et 44 % de
l'empreinte (cultures, forêts, pâturages, pêche, sol bâti) reste hors du
champ de l'approximation carbone.
