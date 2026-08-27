# DENT — analyse critique et propositions

> **Verrou P0.** Le dividende des entreprises (DTENT) pèse plus de la
> moitié de la création monétaire d'un pays. Sa formule décide donc seule
> de l'essentiel des résultats chiffrés. Elle a été construite « au doigt
> mouillé » (Stéphane Hairy, co-auteur, 2026-08-27).
>
> Ce document répond à quatre questions, **avec des chiffres** :
> la formule est-elle homogène ? que fait-elle aux limites ? crée-t-elle
> une rétroaction positive ? par quoi la remplacer ?
>
> Tout est reproductible : `python scripts/analyse_dent.py`.
> Tout est testé : `tests/test_dent.py` (21 tests).

---

## En une page

**La formule §11.1 ne peut pas être utilisée telle quelle.** Six défauts,
tous démontrés, pas argumentés :

| # | Défaut | En clair |
|---|---|---|
| 1 | **Inhomogène** | Le second terme n'est pas en euros. Sa dimension est un *nombre de personnes au carré*. On ne peut pas l'ajouter à `IED × P`. |
| 2 | **Ambiguë** | Le PDF sort la formule en glyphes séparés. Les deux lectures possibles diffèrent d'un facteur **10⁸**. |
| 3 | **Singulière** | Une entreprise parfaitement égalitaire (`r = 0`) reçoit un dividende **infini**. |
| 4 | **Inapplicable** | **96 %** des entreprises françaises n'ont pas de salarié : ni `e`, ni `r`. |
| 5 | **Explosive** | Le bonus croît en `e²`, la production en `e`. Les géants sont favorisés sans borne. |
| 6 | **Assiette non additive** | Deux entreprises qui fusionnent font *baisser* la création monétaire du pays. Filialiser en crée. |

Et une septième, qui touche **toutes** les variantes (fiche EQ-EH-005) :
la règle « moyenne des 3 meilleures années » est une **rétroaction
positive** — la base de référence converge vers 5 fois sa valeur initiale
pour une hypothèse modérée — **et** un **cliquet** — six ans de récession
à −25 % ne la font baisser que de 11 %.

**Trois alternatives sont proposées** (§7). Elles corrigent toutes les
défauts 1 à 5 ; seule l'alternative 3 corrige le défaut 6. Elles ne sont
pas départagées ici : c'est un arbitrage d'auteur, pas un résultat.

---

## 1. Le second terme n'est pas en euros

Rappel de la formule :

```
DENT = IED × P + (e × DCIT) / ((r/e) × 10⁴)
```

En notant `[€]` les euros par an et `[p]` les personnes :

| Élément | Dimension | Commentaire |
|---|---|---|
| `e` | `[p]` | un effectif |
| `DCIT` | `[€·p⁻¹]` | un revenu : des euros **par personne** |
| `r` | `[€·p⁻¹]` | un écart entre deux salaires : même nature |
| `e × DCIT` | `[€]` | ✅ une masse salariale, correcte |
| `r / e` | `[€·p⁻²]` | |
| **le terme entier** | **`[p²]`** | ❌ |

Le second terme est homogène à un **nombre de personnes au carré**. On
l'additionne à `IED × P`, qui est en euros.

Ce n'est pas une subtilité de convention : le résultat tient quelle que
soit la façon de lever l'ambiguïté typographique, et quelle que soit la
façon de traiter la dimension « personne ». **Le défaut est structurel.**

D'où vient-il ? De la **division par `r/e`**. Le produit `e × DCIT` était
juste ; c'est le diviseur qui casse tout. C'est réparable (§7).

---

## 2. On ne sait pas lire la formule — et l'écart est de 10⁸

Le PDF sort la formule en glyphes séparés : `( r / e × 1 0 ⁴ )`. Deux
lectures :

| Lecture | Écriture | Forme simplifiée |
|---|---|---|
| **A** (retenue par le dépôt) | `(e × DCIT) / ((r/e) × 10⁴)` | `(e/100)² × (DCIT/r)` |
| **B** (suggérée par le texte) | `(e × DCIT) / (r / (e × 10⁴))` | `(e × 100)² × (DCIT/r)` |

Le texte d'accompagnement dit : « *r* … est divisé par le nombre d'employé
de l'entreprise, **lui-même multiplié par 10⁴** ». Grammaticalement,
« lui-même » désigne le nombre d'employés — donc la lecture **B**. Le
dépôt avait retenu la **A**.

**Rapport B/A = 100 000 000**, exactement, pour tout jeu de paramètres.

Valeurs du terme (en supposant qu'on le lise comme des euros) :

| Effectif | Salaire max | Lecture A | Lecture B |
|---:|---:|---:|---:|
| 10 | 60 000 € | 0,01 € | 578 947 € |
| 100 | 120 000 € | 0,22 € | 22 448 980 € |
| 1 000 | 300 000 € | 7,91 € | 791 366 906 € |
| 100 000 | 2 000 000 € | 11 122 € | 1 112 234 580 384 € |

Aucune des deux ne réalise l'intention affichée (« un dividende
relativement proche du produit d'exploitation ») :

- **Lecture A** : le terme est **négligeable partout**. Pour 1 000
  salariés il vaut 8 €, contre ~190 M€ de production. Il ne fait rien —
  sauf exploser quand `r → 0`.
- **Lecture B** : le terme **dépasse la production entière** dès ~70
  salariés, puis croît comme le carré de l'effectif. Pour 100 000
  salariés il atteint **1 112 Md€ pour une seule entreprise** — soit 58
  fois sa propre production, et 39 % du PIB français.

---

## 3. Quand l'écart de salaire s'annule, le dividende devient infini

`r = 0` signifie : *le mieux payé de l'entreprise gagne exactement le
revenu minimum du pays*. C'est l'entreprise parfaitement égalitaire — une
petite coopérative, par exemple. Ce n'est pas un cas d'école.

| `r` | Terme (lecture A) |
|---:|---:|
| 100 000 € | 0,2 |
| 1 000 € | 22 |
| 10 € | 2 200 |
| 1 € | 22 000 |
| **0 €** | **∞** |

La divergence est hyperbolique : diviser l'écart par 10 000 multiplie le
dividende par 10 000. **Il n'y a aucun plafond.**

Trois problèmes en un :

1. **Singularité** à un point atteignable.
2. **Incitation perverse** : la fonction récompense *sans borne* ce
   qu'elle prétend seulement encourager. Une entreprise a intérêt à
   aligner tous ses salaires au centime près sur le revenu minimum, non
   par équité mais pour capter une création monétaire illimitée.
3. **Discontinuité de signe** : si le plus haut salaire passe *sous* le
   revenu minimum, le terme bascule de `+∞` à `−∞`.

Et si l'entreprise n'a **aucun salarié**, `r` n'est pas défini du tout.

---

## 4. Le périmètre « entreprise » : ±39 % d'assiette, et 96 % de cas non calculables

### 4.1 Quel secteur ?

Comptes nationaux France 2023 (Eurostat `nasa_10_nf_tr`, prix courants) :

| Secteur | Production | Valeur ajoutée |
|---|---:|---:|
| S11 sociétés non financières | 3 810 Md€ | 1 481 Md€ |
| S12 sociétés financières | 288 Md€ | 90 Md€ |
| S14 ménages (dont entrepreneurs individuels) | 516 Md€ | 452 Md€ |
| S1 économie totale | 5 310 Md€ | — |

*PIB 2023 : 2 834 Md€.*

| Périmètre | Assiette | × PIB |
|---|---:|---:|
| a) SNF seules | 3 810 Md€ | 1,34 |
| b) + sociétés financières | 4 098 Md€ | 1,45 |
| c) + entrepreneurs individuels | 4 614 Md€ | 1,63 |
| d) toute production marchande | 5 310 Md€ | 1,87 |

**Écart du plus étroit au plus large : 1 500 Md€, soit +39 %** — la moitié
d'un PIB. Le choix de périmètre pèse presque autant que le choix de
formule.

Trois pièges à trancher explicitement :

- **Sociétés financières.** En EH, les banques ne créent plus la monnaie.
  Leur verser un dividende assis sur leur « production » (des marges
  d'intermédiation) n'a plus de sens évident. → *Recommandation : les
  exclure, et l'écrire.*
- **Entrepreneurs individuels.** Ils sont dans le secteur des ménages :
  leur dirigeant touche **déjà** le DCIT. Un DENT en plus les avantage
  doublement face à un salarié.
- **Loyers imputés.** La production de S14 contient le loyer fictif que
  les propriétaires se versent à eux-mêmes. Verser un dividende
  d'entreprise là-dessus n'a aucun sens → **le périmètre c) est
  inutilisable tel quel.**

### 4.2 La quasi-totalité des entreprises n'a pas de salarié

Démographie des entreprises (Eurostat `sbs_sc_ovw`, France 2022,
NACE B-S hors administration publique) :

| | |
|---|---:|
| Entreprises, total | 4 906 972 |
| dont 0 à 9 personnes occupées | 4 718 929 (**96,2 %**) |
| dont 250 personnes occupées ou plus | 5 987 (0,12 %) |
| Personnes occupées, total | 20 478 850 |
| dont dans les unités de 0 à 9 personnes | 5 541 957 |

Soit **1,17 personne par entreprise** dans la classe 0–9 : l'entreprise
française typique est une personne seule, sans salarié.

Pour elle, `e = 0`, et le second terme de la §11.1 n'existe pas. **Le
calcul « entreprise par entreprise » que prescrit la synthèse est donc
impossible sur 96 % des entreprises françaises.** Toute formule retenue
doit être définie à `e = 0`.

---

## 5. Qu'est-ce que `P` ? Le vrai problème n'est pas celui qu'on croit

« Produit d'exploitation » est un terme de **comptabilité d'entreprise** :
en gros le chiffre d'affaires. Ce n'est pas la « production » des comptes
nationaux. Mais l'écart entre ces deux définitions voisines n'est pas le
problème.

Le problème est que **la somme des chiffres d'affaires n'est pas une
grandeur économique**. Elle compte plusieurs fois la même valeur, autant
de fois qu'il y a de maillons dans la chaîne.

Production des SNF 3 810 Md€ contre valeur ajoutée 1 481 Md€ : **rapport
2,57**. La différence, ce sont les consommations intermédiaires.

Conséquence directe et vérifiable :

- deux entreprises **fusionnent** → la vente de l'une à l'autre disparaît
  → la somme des productions **baisse** → le dividende du pays **baisse** ;
- une entreprise **se scinde** → une vente interne devient externe →
  la somme des productions **monte** → le dividende du pays **monte**.

Rien n'a changé dans l'économie réelle. **La création monétaire du pays
dépendrait du découpage juridique des entreprises.** C'est une faille
d'optimisation évidente : il suffirait de filialiser pour créer de la
monnaie.

La **valeur ajoutée** n'a pas ce défaut. Elle est *additive* : sa somme ne
bouge ni en fusionnant ni en scindant, et elle vaut le PIB (SEC 2010).
C'est le motif de l'alternative 3.

S'ajoute la règle « **moyenne des trois meilleures** années », qui retient
un maximum — donc une valeur supérieure à la production courante — en plus
de l'effet cliquet démontré ci-dessous.

---

## 6. La règle « 3 meilleures années » est une rétroaction positive

La synthèse anticipe partiellement l'objection : la réactualisation de `P`
se fait « **hors DENT** », sans compter le dividende que l'entreprise a
elle-même reçu. Cela coupe la boucle **directe**. Il faut le reconnaître.

**Mais cela ne coupe pas la boucle macro-économique** : le dividende de
l'entreprise A est dépensé, et devient le chiffre d'affaires de B.
Exclure son propre dividende retire `1/N` du flux. Avec N = 4,9 millions
d'entreprises, **cela ne retire rien**.

Récurrence obtenue : `P ← X₀ + g·P` avec `g = α × IED × (1 − 1/N)`, où `α`
est la part du dividende qui revient aux entreprises en chiffre
d'affaires.

| `α` | Amplification de `P` | DTENT à terme (SNF) |
|---:|---:|---:|
| 0,50 | ×2,0 | 7 620 Md€ |
| 0,70 | ×3,3 | 12 701 Md€ |
| **0,80** | **×5,0** | **19 051 Md€** |
| 0,90 | ×10,0 | 38 102 Md€ |
| 0,95 | ×20,0 | 76 204 Md€ |
| 1,00 | ×4 906 972 | absurde |

À `α = 1`, le **seul** frein restant est la clause « hors DENT » — et elle
plafonne l'amplification à N, soit 4,9 millions de fois. Autrement dit :
**la précaution prise par la synthèse ne protège de rien.** Elle
transforme une divergence en une explosion finie mais absurde.

Avec `α = 0,8` — hypothèse modérée, puisque la fonte pousse à dépenser —
la base de référence se stabilise à **5 fois** la production initiale.

C'est une **rétroaction positive**, dans une théorie qui se présente comme
un thermostat sans rétroaction positive. Ce n'est pas un artefact de
simulation : c'est la solution analytique de la règle telle qu'écrite.

### L'effet cliquet

Récession de −25 % pendant six ans, puis retour à la normale. La règle
retient les **meilleures** années :

| Année | Produit observé | Base `P` sans choc | Base `P` avec choc |
|---:|---:|---:|---:|
| 9 | 12 808 | 11 248 | 11 248 |
| 15 | 10 543 | 14 057 | 12 808 |
| 18 | 14 057 | 15 056 | 12 808 |
| 23 | 15 056 | 15 855 | 14 057 |

Après six ans de récession sévère, la base n'a perdu que **11,3 %**. La
création monétaire reste calée sur un niveau d'activité que l'économie
n'atteint plus.

C'est exactement ce qu'un régulateur ne doit pas faire : *le thermostat
continue de chauffer parce qu'il se souvient du meilleur été.*

---

## 7. Trois alternatives — à arbitrer

Toutes trois : homogènes en euros · bornées · définies à `e = 0` et à
`r = 0` · monotones décroissantes en écart de salaire · proportionnelles à
l'IED (le pilotage écologique est préservé).

Notation commune : `s = salaire_max / DCIT`, le plus haut salaire exprimé
**en multiples du revenu minimum**. C'est un nombre pur — c'est là toute
la réparation : on remplace un écart en euros par un *rapport*.

### Alternative 1 — modulation multiplicative (fiche EQ-EH-002)

```
DENT = IED × P × κ(s)        κ(s) = 2 / (1 + (s / s_ref)^γ)
```

**Intention** : correction minimale. L'équité salariale devient un
*coefficient sans unité* au lieu d'un terme ajouté — la formule est
homogène par construction.

**Propriétés** : `κ` vaut **2** pour l'égalité parfaite, **1** exactement
à l'écart de référence `s_ref` (on retrouve `DENT = IED × P`, la cible de
la synthèse), et tend vers **0** pour les écarts extrêmes. Bornée sur
`]0 ; 2[`, strictement décroissante, aucune singularité.

**Ce qu'elle abandonne** : la récompense explicite de l'emploi. Elle
conserve l'assiette « production », donc la faille de filialisation.

### Alternative 2 — deux termes, tous deux en euros (fiche EQ-EH-003)

```
DENT = IED × [ (1−θ)·P + θ · e · DCIT · ψ(s) ]     ψ(s) = 1 / (1 + ((s−1)/s₀)^γ)
```

**Intention** : rester au plus près des **mots** de la synthèse. Le
produit `e × DCIT` y figure littéralement — « la masse salariale si tout
le monde était au revenu minimum » — et c'est bien une somme d'euros. Le
défaut venait de la division qui suivait, pas de ce produit. Ici l'écart
de salaire ne divise plus : il **pondère** la prime.

**Propriétés** : homogène · bornée · prime **linéaire** en effectif (plus
de croissance en `e²`) · `ψ(1) = 1` (égalité parfaite → prime entière,
mais **finie**).

**Le paramètre décisif est `θ`** : à `θ = 0` on récompense la taille
(assiette 3 810 Md€) ; à `θ = 1` on récompense l'emploi (assiette
`e × DCIT` ≈ 450 Md€ pour 20,5 M de personnes occupées). **Facteur 8 entre
les deux extrêmes.** C'est un arbitrage politique, à assumer comme tel.

### Alternative 3 — assise sur la valeur ajoutée (fiche EQ-EH-004)

```
DENT = IED × VA × κ(s)
```

**Intention** : corriger le défaut **économique** (§5), plus profond que
le défaut mathématique. La valeur ajoutée est additive : insensible aux
fusions et aux scissions, et sa somme vaut le PIB.

**Propriétés** : celles de l'alternative 1, **plus** l'invariance au
découpage juridique. **Assiette divisée par 2,57** (1 481 Md€ au lieu de
3 810 Md€ pour les SNF).

**Ce qu'elle abandonne** : la phrase « un dividende relativement proche du
produit d'exploitation ». C'est assumé — cette phrase *est* la faille.

### Ce que ça donne

Entreprise type : 500 salariés · production 95 M€ · valeur ajoutée 37 M€ ·
plus haut salaire 250 000 € (11,4 × le revenu minimum). IED = 1.

| Formule | Dividende |
|---|---:|
| §11.1 lecture A | 95,0 M€ |
| §11.1 lecture B | 336,2 M€ |
| Alternative 1 | 30,8 M€ |
| Alternative 2 (θ = 0,3) | 66,9 M€ |
| Alternative 3 | 12,0 M€ |

Extrapolé à la France (SNF, IED = 1) — ordre de grandeur seulement,
l'agrégation d'une formule non linéaire depuis une entreprise moyenne
n'étant pas exacte :

| Formule | Assiette | DTENT | × PIB |
|---|---:|---:|---:|
| §11.1 (≈ IED × P) | 3 810 Md€ | 3 810 Md€ | 1,34 |
| Alternative 1 | 3 810 Md€ | 1 236 Md€ | 0,44 |
| Alternative 2 (θ = 0,3) | 3 810 Md€ | 2 684 Md€ | 0,95 |
| Alternative 3 | 1 481 Md€ | 480 Md€ | 0,17 |

**Facteur 7,9 entre les extrêmes.** C'est bien cette formule, et non la
théorie EH, qui décide de l'ordre de grandeur de la création monétaire
française.

---

## 8. Ce qu'il reste à trancher — quatre décisions

Aucune n'est tranchée ici. Ce sont des choix d'auteur.

| # | Question | Options | Enjeu |
|---|---|---|---|
| **D7** | **Assiette** | production / valeur ajoutée | Facteur **2,6** sur DTENT. La production expose à la filialisation. |
| **D8** | **Forme** | alt. 1 / alt. 2 / alt. 3 / combinaison | Faut-il récompenser l'emploi en plus de la taille ? |
| **D9** | **Périmètre** | SNF / +finance / +entrepreneurs individuels | ±39 %, soit 1 500 Md€. |
| **D10** | **Base `P`** | 3 meilleures années / moyenne glissante / grandeur exogène | La règle actuelle amplifie ×5 et cliquette. |

**Recommandation, à discuter** : alternative 3 (valeur ajoutée) sur le
périmètre SNF, avec une base `P` en moyenne glissante simple sur 3 ans.
C'est la combinaison qui supprime les six défauts et le cliquet. Elle
divise DTENT par 7,9 par rapport à la §11.1 — ce qui change radicalement
la conclusion du calcul d'ordre de grandeur, et c'est précisément
pourquoi la décision ne m'appartient pas.

⚠️ **Tant que D7–D10 ne sont pas tranchées, aucun résultat quantitatif sur
la masse monétaire en EH n'est publiable.**
