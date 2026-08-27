# L'économie homéostatique (EH) — comment ça marche

> **Source principale** : *Vers une économie bio-intégrée : Théorie de
> l'économie homéostatique — Document de synthèse*, v1.7, B. Albouy,
> S. Hairy, V. Lavilley, Ex Naturae, octobre 2020 (60 p.).
> Licence CC BY-NC-ND 2.0 FR. Copie locale : `sources/`.
> Compléments vulgarisés : <https://exnaturae.ong>.
>
> Ce document résume le modèle **tel qu'il est écrit**. Les critiques et
> points à trancher pour la modélisation sont en fin de document (§10) et
> détaillés dans `docs/02-strategie-modelisation.md`.

---

## 1. L'idée en un paragraphe

Aujourd'hui, la monnaie est créée par les banques quand elles prêtent
(monnaie-dette), et détruite quand on rembourse. La richesse d'un pays se
mesure à ce qu'il produit — donc à ce qu'il extrait de la nature.

L'EH inverse cela : **la monnaie est créée non pas par le crédit mais par
un don, et le montant de ce don dépend de l'état écologique du pays.**
Si le pays préserve sa nature, il reçoit plus de monnaie. S'il la dégrade,
il en reçoit moins et s'appauvrit. La monnaie n'est plus détruite par le
remboursement mais par la **fonte** : elle s'évapore lentement, comme tout
objet physique s'use.

Formule mentale : *plus tu préserves, plus tu es riche.* C'est le
renversement exact du système actuel.

---

## 2. D'où vient l'idée : l'homéostasie

**Vulgarisation.** Votre corps maintient sa température autour de 37 °C.
Trop chaud → vous transpirez. Trop froid → vous frissonnez. Ce mécanisme
qui ramène toujours vers la bonne valeur s'appelle une **rétroaction
négative**, et l'état d'équilibre obtenu s'appelle l'**homéostasie**
(Claude Bernard 1865, Walter Cannon 1932, cybernétique de Wiener 1948).

L'EH applique cette logique à l'économie :
- L'économie de croissance fonctionne en **rétroaction positive** :
  plus on produit, plus on investit, plus on produit. Ça explose ou ça
  se bloque. C'est mathématiquement insoutenable dans un monde fini.
- L'EH veut une **rétroaction négative** : quand l'économie déborde des
  limites écologiques, un mécanisme automatique la ramène en arrière.

**Filiation théorique** : Soddy (1926), Georgescu-Roegen (1971), Daly
(1991), Odum (émergie, 1996), Roddier (2018), et très proche de la théorie
du *donut* de Kate Raworth (2017) — un plancher social, un plafond
écologique, et l'économie doit tenir entre les deux.

---

## 3. Deux moitiés : exo-économie et endo-économie

| | Définition | Contenu |
|---|---|---|
| **EXEC** — exo-économie | Ce qui est *hors* de l'économie marchande | Biodiversité, ressources, pollutions, écosystèmes |
| **ENEC** — endo-économie | L'économie humaine actuelle | Salaires, production, échanges, épargne, crédit |

**L'idée clé** : aujourd'hui l'EXEC est invisible pour l'économie (une
espèce non exploitée a une valeur économique de zéro : « cécité
économique »). Dans l'EH, **l'EXEC pilote l'ENEC** : l'état de la nature
détermine combien de monnaie est créée.

Justification donnée : la monnaie est notre *capacité d'action* sur le
monde. Il est donc logique de l'indexer sur l'état du monde.

---

## 4. Les trois indicateurs qui pilotent tout

Trois indicateurs mesurent l'état écologique d'un pays, **notés de 0 à 2** :

| Sigle | Nom | Ce qu'il mesure |
|---|---|---|
| **IBD** | Indice de biodiversité | Niveau de biodiversité et taille des populations d'espèces du territoire |
| **IEE** | Indice d'empreinte écologique | Pollutions, consommation de renouvelables vs. leur taux de renouvellement, anthropisation. **Importations incluses** (pas de pollution délocalisée) |
| **IRNR** | Indice de ressources non renouvelables | Consommation de non-renouvelables ; le recyclage compte positivement |

**Lecture de l'échelle** (c'est contre-intuitif, attention) :
- `0` = pire situation possible
- `1` = **cible** : équilibre dynamique atteint
- `2` = meilleure situation possible (le pays « sous-exploite »)
- En dessous de 1 → le pays surexploite et dégrade.

### L'IED : l'indicateur de synthèse

$$\text{IED} = \sqrt[3]{\text{IBD} \times \text{IEE} \times \text{IRNR}}$$

C'est la **moyenne géométrique** des trois. Pourquoi pas une moyenne
simple ? Parce qu'un indicateur catastrophique doit rester
catastrophique.

*Exemple du document (Tableau 1)* : un pays avec (0,9 ; 0,1 ; 2) a une
moyenne arithmétique de **1** — il a l'air à l'équilibre. Sa moyenne
géométrique est **0,56** — la catastrophe sur l'IEE n'est pas rachetable
par un excédent ailleurs. C'est le bon choix mathématique.

---

## 5. La création monétaire : la monnaie-don

**Principe** : la monnaie n'est pas prêtée, elle est **donnée**, sans
contrepartie, comme la nature nous donne ses ressources. Elle est créée
par une **Banque Centrale Internationale (BCI)**, pas par les banques
commerciales.

Elle est distribuée à **trois acteurs** : l'État, les citoyens, les
entreprises.

### Les formules (§11.1 de la synthèse)

| Bénéficiaire | Formule | Lecture |
|---|---|---|
| État | `DETA = IED × 22 000 × c` | 22 000 € par citoyen (`c`), modulé par l'IED |
| Citoyens (total) | `DTCIT = DETA` | Autant que l'État |
| Un citoyen | `DCIT = DETA / c` | = `IED × 22 000` €/an |
| Une entreprise | `DENT = IED × P + (e × DCIT) / ((r/e) × 10⁴)` | voir ci-dessous |
| Entreprises (total) | `DTENT = Σ DENT` | somme sur toutes les entreprises |
| **Zone économique** | `DG_FR = DETA + DTCIT + DTENT` | création monétaire annuelle du pays |

**D'où vient le 22 000 ?** C'est la moyenne des dépenses publiques par
habitant des 10 pays européens qui dépensent le plus. C'est une constante
**choisie**, pas mesurée.

**La formule des entreprises, décodée** :
- `P` = produit d'exploitation de référence (ex. moyenne des 3 meilleures
  années), réactualisé tous les ~3 ans ;
- `e` = nombre de salariés ;
- `r` = écart entre le plus haut salaire de l'entreprise et le DCIT.
- Le second terme **récompense l'emploi et pénalise les écarts de
  salaires** : plus le patron gagne par rapport au minimum, plus `r` est
  grand, plus le bonus fond.
- Quand IED = 1, le dividende est proche du produit d'exploitation.

### Ce que ça donne

- IED **augmente** → plus de monnaie → plus de consommation et de
  production → plus de pression écologique → les indicateurs baissent…
- IED **baisse** → moins de monnaie → le pays s'appauvrit → moins de
  consommation, moins de production → moins de pression → les indicateurs
  remontent.

C'est exactement le thermostat : la boucle est bouclée.

---

## 6. La destruction monétaire : la monnaie fondante

Si on ne fait que créer de la monnaie, elle s'accumule à l'infini. Il faut
un mécanisme de destruction. Dans le système actuel c'est le
remboursement des crédits. Dans l'EH c'est la **fonte**.

**Vulgarisation** : votre argent rouille. Tout dans le monde physique se
dégrade (la nourriture pourrit, les objets s'usent) — sauf la monnaie.
La fonte lui rend cette propriété. C'est une « entropie simulée ».

**Paramètres retenus dans la synthèse** :
- **1 % par mois** sur tous les soldes bancaires, en fin de mois ;
- **1 % sur chaque transaction**.

Filiation : Silvio Gesell, *L'ordre économique naturel* (1916) — la
monnaie franche/fondante ; expérience du **Wära** (Schwanenkirchen, 1931).

**Conséquences attendues** :
1. **Les soldes bancaires plafonnent.** On ne peut plus accumuler
   indéfiniment. Un compte se stabilise quand `revenus = dépenses + fonte`.
2. **La monnaie circule plus vite** (la garder coûte cher).
3. **La sobriété devient la voie de l'enrichissement** : comme il est plus
   facile de baisser ses dépenses que d'augmenter ses revenus, économiser
   devient la stratégie gagnante.
4. **Elle impose une monnaie 100 % électronique** (impossible de faire
   fondre des billets à grande échelle).
5. Elle **rend impossible la spéculation financière** — la monnaie ne peut
   pas être placée sur les marchés (interdiction légale ou fonctionnelle
   nécessaire, sinon tout le monde y placerait son argent pour fuir la
   fonte).

---

## 7. Le second mécanisme : les PCED

**PCED = Projet Certifié d'Équilibre Dynamique.** C'est la deuxième source
de création monétaire, et le mécanisme le plus original du modèle.

**Le problème résolu** : dépolluer une rivière, restaurer une forêt, ça
coûte de l'argent et ça ne rapporte rien. C'est une perte pure. Donc
personne ne le fait.

**La solution** : la BCI **rentabilise la perte**. Un projet écologique
certifié rembourse ses financeurs **plus une plus-value**, créée
*ex nihilo* par la BCI.

**Procédure** : dossier → certification par la BCI → financement →
réalisation → **contrôle sur place** → remboursement + plus-value. Pas de
contrôle validé, pas d'argent.

**Les quatre catégories et leur rendement** (indexé sur le taux de fonte
global de la zone) :

| Catégorie | Objectif | Rendement |
|---|---|---|
| **A** | Accroître la biodiversité | 80 % du taux de fonte |
| **B** | Dépolluer / réduire les émissions | 60 % |
| **C** | Réduire l'empreinte écologique | 40 % |
| **D** | Réduire la conso. de non-renouvelables | 20 % |

*Exemple du document* : avec une fonte globale de 5 %, 1 M€ investi en
catégorie A rapporte 40 000 €.

**Le rendement est toujours inférieur au taux de fonte.** C'est
volontaire : sinon on créerait plus de monnaie qu'on n'en détruit.

**L'effet visé** : les gros capitaux, pour échapper à la fonte, se
précipitent sur les PCED. L'argent va massivement vers la réparation
écologique — non par vertu, mais par intérêt.

Les PCED sont à but non lucratif, ponctuels et uniques.

---

## 8. Les autres mécanismes

### Crédit (§13)
Les banques ne créent **plus** de monnaie. Elles intermédient. Un prêteur
(privé ou public) qui a un excédent le prête pour échapper à la fonte.
L'emprunteur ne rembourse pas avec son travail : **son dividende mensuel
est versé au prêteur** jusqu'à extinction de la dette.
→ Conséquence forte : **la durée de remboursement dépend des indicateurs
écologiques.** Nature en bonne santé = dettes remboursées plus vite.

### Import / export (§14)
Quatre cas, pour empêcher la délocalisation de la pollution :

| Cas | Change | Fonte | Effet sur les indicateurs |
|---|---|---|---|
| EH → hors-EH (export) | oui | à la conversion | aucun (sauf export de déchets) |
| EH → EH (export) | non | à l'échange | aucun (déjà compté à la production) |
| EH ← EH (import) | non | à l'échange | seulement le **transport** |
| EH ← hors-EH (import) | oui | à la conversion | **oui, tout compté** |

→ Importer d'un pays non-EH dégrade vos propres indicateurs, donc appauvrit
votre pays. Relocalisation obtenue **sans droits de douane ni loi**.

### Biens communs (§17)
Plus besoin de gouvernance ni de propriété (Ostrom). Comme la santé des
communs détermine le dividende de tout le monde, **tout le monde a un
intérêt financier direct à les préserver**.

### État (§19.2)
L'État reçoit sa monnaie sans dette. Il peut donc rembourser sa dette
existante et **supprimer impôts et taxes**. Ses pouvoirs régaliens sont
inchangés ; seule la souveraineté monétaire est abandonnée à la BCI.

### Organisation internationale (§18)
Une OI indépendante mesure les indicateurs (un pays ne peut pas noter
lui-même sa copie), certifie et contrôle les PCED, et abrite la BCI qui
émet la monnaie. Elle **n'a aucun pouvoir politique** sur les États.

---

## 9. Effets annoncés

**Avantages revendiqués** : fin de l'extrême pauvreté (dividende) ;
réduction des inégalités (fonte) ; suppression des impôts ; rentabilisation
de l'écologie (PCED) ; fin de la concurrence entre États (la richesse ne
dépend plus des autres) ; le dividende devient un **signal public** — s'il
baisse, tout le monde sait que l'écologie du pays se dégrade.

**Inconvénients reconnus par les auteurs** : non testable à petite échelle
(→ *« l'EH nécessite donc des modélisations économétriques »*, §21.2 — le
présent dépôt) ; abandon de souveraineté monétaire ; refonte du système
bancaire ; risques de spéculation sur les stocks de matières premières et
l'immobilier ; expatriation fiscale ; bouleversements brutaux de richesse
relative entre pays au démarrage.

---

## 10. Ce qu'il faudra trancher pour modéliser

Points que le document laisse ouverts ou insuffisamment spécifiés — ce
sont nos chantiers, pas des objections :

| # | Question ouverte | Enjeu pour le modèle |
|---|---|---|
| 1 | **Comment calcule-t-on IBD, IEE, IRNR sur 0–2 ?** Aucune formule n'est donnée | Bloquant. Sans opérationnalisation, rien n'est simulable |
| 2 | **Le taux de change** est explicitement « à développer » (§15) | Bloquant pour l'ouverture aux échanges |
| 3 | **Stabilité de la boucle** : les indicateurs écologiques ont une inertie de plusieurs années. Une boucle de rétroaction à long délai **oscille** typiquement au lieu de converger | Question scientifique centrale. À tester en théorie du contrôle |
| 4 | **Niveau des prix** : rien n'est dit sur l'inflation hors d'une affirmation (§10.1 : « il ne peut y avoir d'hyperinflation ») | Voir calcul ci-dessous |
| 5 | **`P`, produit d'exploitation** : réactualisé tous les 3 ans sur les meilleures années → mécanisme potentiellement auto-amplifiant | Rétroaction positive cachée dans un modèle qui les refuse |
| 6 | **Comportements** : la §20 reconnaît que la psychologie économique « est à développer » | Nos élasticités viendront de la littérature sur les transferts monétaires et les monnaies fondantes |

### Premier calcul d'ordre de grandeur — pourquoi cette question n°4 est sérieuse

Script : `scripts/ordre_grandeur_eh_france.py`. Entrées à **[VÉRIFIER]**,
résultat purement illustratif :

```
CRÉATION MONÉTAIRE ANNUELLE (IED = 1, France, 68,1 M hab.)
  DETA  (État)      1 498 Md€      DCIT   22 000 €/an = 1 833 €/mois
  DTCIT (citoyens)  1 498 Md€      DTENT  ~4 000 Md€  [très incertain]
  DG_FR             ~7 000 Md€  =  2,5 × PIB

ÉTAT STATIONNAIRE (création annuelle = destruction par la fonte)
  Fonte : 11,4 %/an sur les soldes + 1 % par transaction
  Masse monétaire d'équilibre   ~48 700 Md€  =  17 × PIB
  M3 France aujourd'hui          ~3 000 Md€  =  1,1 × PIB
  → rapport ≈ 16 ×
```

**Traduction** : à paramètres inchangés, l'EH converge vers une masse
monétaire de l'ordre de **16 fois** l'actuelle, pour la même économie
réelle. Soit les prix montent massivement, soit la vitesse de circulation
et la demande de monnaie se comportent très différemment de ce qu'on
observe — c'est précisément ce qu'un modèle sérieux doit trancher.

⚠️ Ce calcul est **grossier** : `DTENT` domine le total et repose sur une
estimation non vérifiée des produits d'exploitation français. Il ne
constitue pas une réfutation, mais **il justifie à lui seul le projet** :
les paramètres (22 000 €, 1 %/mois) doivent être calibrés, pas postulés.
