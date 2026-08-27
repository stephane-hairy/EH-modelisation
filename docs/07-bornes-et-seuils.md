# Les bornes 0 et 2, et les seuils des trois indicateurs

> **Ce document répond à une question de Stéphane Hairy (2026-08-27) :
> « le 0 et le 2 correspondent à quoi ? »**
>
> Réponse courte : **la synthèse ne le dit pas**. Elle exige seulement
> « vaut 1 à l'équilibre, borné sur [0 ; 2] ». Le 0 et le 2 ont donc été
> remplis par ce dépôt, sans que ce choix soit posé comme une décision.
> C'est un trou, et ce document le comble.
>
> Reproductible : `python scripts/bornes_indicateurs.py`.

---

## En une page

| | |
|---|---|
| **Ce qui est ancré** | **Le 1 seulement** : pression = seuil de soutenabilité |
| **Ce que vaut 2 aujourd'hui** | **x = 0** — le pays ne consomme *rien*. Absurde économiquement |
| **Ce que vaut 0 aujourd'hui** | Dépend du mapping : **x = 2** (linéaire) ou **jamais** (exponentiel) |
| **Enjeu du 0** | ⚠️ **IED = 0 n'est pas une pénalité, c'est l'extinction monétaire** |
| **Second problème** | Les trois seuils **ne sont pas commensurables** — celui de l'IBD n'en est pas un |
| **À trancher** | **D14** borne basse · **D15** borne haute · **D16** seuil de l'IBD |

---

## 1. Pourquoi le 0 est la question grave

Sous l'EH, la monnaie n'est créée **que** par le don. Il n'y a plus de
crédit bancaire créateur de monnaie. Donc si `IED = 0`, il n'y a
**aucune** création — ni pour l'État, ni pour les citoyens, ni pour les
entreprises — pendant que la fonte, elle, continue de détruire le stock.

Ce que ça donne, avec la fonte de 1 %/mois de la synthèse (§6) :

| Hypothèse | Demi-vie de la masse monétaire | Reste après 5 ans |
|---|---:|---:|
| Fonte sur les soldes seule | **5,7 ans** | 55 % |
| + fonte transactionnelle (vitesse 3/an) | **4,6 ans** | 47 % |

**`IED = 0` n'est donc pas « une forte pénalité ». C'est la disparition
progressive de la monnaie du pays.** En une décennie, il ne reste presque
rien.

Cela change complètement la nature de la question. Elle ne se lit pas
« quel malus pour un mauvais élève ? » mais :

> **À partir de quel niveau de destruction écologique l'économie
> homéostatique décide-t-elle qu'un pays ne doit plus avoir de monnaie
> du tout ?**

Posée ainsi, elle mérite une décision explicite.

### Le mapping linéaire coupe presque tout l'OCDE

Le mapping linéaire (`I = 2 − x`) met `I = 0` à `x = 2`, soit **deux fois
le seuil**. Ce n'est pas un cas extrême : c'est la situation ordinaire
d'un pays riche.

Indice carbone seul, données GFN 2013 :

| Pays | `x` | `x₀ = 2` | `x₀ = 5` | `x₀ = 10` |
|---|---:|---:|---:|---:|
| Bangladesh | 0,44 | 1,56 | 1,56 | 1,56 |
| Brésil | 1,77 | 0,23 | 0,81 | 0,91 |
| **France** | 2,94 | **0,00** | 0,52 | 0,78 |
| Allemagne | 3,20 | **0,00** | 0,45 | 0,76 |
| Australie | 5,16 | **0,00** | **0,00** | 0,54 |

*(`x₀` = la pression à laquelle l'indicateur atteint 0.)*

Avec `x₀ = 2`, **la France, l'Allemagne et l'Australie sont coupées** —
c'est-à-dire la quasi-totalité des pays riches. Avec `x₀ = 5`, seule
l'Australie l'est.

---

## 2. Les options pour la borne basse (D14)

Effet sur la France 2021 (les trois indicateurs, mapping recalé) :

| Option | IEE | IRNR | IBD | **IED** | €/citoyen |
|---|---:|---:|---:|---:|---:|
| **B1** `x₀ = 2` — deux fois le seuil | 0,00 | 0,62 | 0,27 | **0,00** | **0 €** |
| **B2** `x₀ = 5` — cinq fois le seuil | 0,52 | 0,91 | 0,82 | **0,72** | 15 949 € |
| **B3** `x₀ = 10` — dix fois le seuil | 0,78 | 0,96 | 0,92 | **0,88** | 19 444 € |
| **B4** jamais atteint *(actuel)* | 0,26 | 0,77 | 0,60 | **0,49** | 10 874 € |
| **B5** jamais + **plancher explicite** à 0,20 | 0,26 | 0,77 | 0,60 | **0,49** | 10 874 € |

**Lecture.**

- **B1 est à écarter.** Elle annule la monnaie de presque tous les pays
  riches, pour un dépassement banal.
- **B2 et B3 sont indulgentes** : elles donnent à la France plus qu'elle
  n'obtient aujourd'hui (0,49), alors qu'elle consomme près de trois fois
  le budget planétaire. Elles diluent le signal.
- **B4** (l'actuel) est le plus sévère des trois raisonnables, et ne coupe
  jamais totalement.
- **B5** ajoute une garantie utile : un **plancher explicite**. Il ne mord
  pas pour la France (0,49 > 0,20), mais il **interdit par construction
  l'extinction monétaire**, y compris pour un pays très dégradé.

⚠️ **B5 protège aussi contre un effet de la moyenne géométrique** : sans
plancher, un seul indicateur à zéro annule l'IED entier (décision D6). Un
plancher par indicateur borne l'IED par le bas automatiquement.

---

## 3. Les options pour la borne haute (D15)

Aujourd'hui `I = 2` correspond à `x = 0` : le pays **ne consomme rien**.
Ce n'est pas « parfaitement soutenable » — ça, c'est `I = 1`.

Conséquence directe, rarement dite : puisque `DETA = IED × 22 000 × c`,
**le système verse le double d'argent au pays dont l'activité économique
est nulle.** La création monétaire est maximale quand l'économie s'arrête.

Trois lectures possibles :

### H1 — `x = 0`, la lecture actuelle
« Le maximum récompense l'absence de consommation. »
*Simple, mais le haut de l'échelle est économiquement absurde.*

### H2 — `x = 0,5`, la moitié du seuil
« Consommer deux fois moins que le soutenable donne le maximum. »
*Atteignable et désirable. Mais plusieurs pays pauvres saturent à 2 et
deviennent indistinguables — le Bangladesh (x = 0,44) y est déjà.*

### H3 — la régénération ⭐
« **1 = ne plus dégrader. 2 = réparer.** »

L'intervalle `[1 ; 2]` n'est plus réservé aux pays qui consomment peu,
mais à ceux dont la pression est **nette négative** : puits de carbone
supérieurs aux émissions, indice de biodiversité en hausse, stock de
matière alimenté par le recyclage plutôt que par l'extraction.

**Pourquoi c'est la lecture la plus cohérente avec la théorie.**
L'homéostasie n'est pas l'arrêt : un organisme en homéostasie ne se
contente pas de cesser de s'abîmer, **il se répare**. L'EH est
explicitement bio-inspirée ; le haut de son échelle devrait décrire la
régénération, pas l'inexistence.

**Conséquence à assumer** : sous cette lecture, `[1 ; 2]` est
**aujourd'hui vide**. Aucun pays ne régénère. C'est honnête, et ça dit
quelque chose : la moitié haute de l'échelle EH est une **cible**, pas un
état observé.

### H4 — plafonner à 1
Pas de bonus au-dessus du seuil. *Contredit le [0 ; 2] explicite de la
synthèse et supprime toute incitation à faire mieux que soutenable.*

---

## 4. Le second problème : les trois seuils ne se comparent pas

C'est l'autre moitié de la question, et c'est un défaut de ma
construction que je n'avais pas assez signalé.

| | Mesure France 2021 | Seuil | `x` | **Nature du seuil** |
|---|---:|---:|---:|---|
| **IEE** | 6,26 tCO₂/hab | 2,13 | 2,94 | budget planétaire (GIEC AR6) |
| **IRNR** | 11,01 t/hab | 8,00 | 1,38 | corridor scientifique (Bringezu 2015) |
| **IBD** | indice 53,9 | 93,3 | 1,73 | ⚠️ **l'état de la France en 1990** |

**Le seuil de l'IBD n'est pas un seuil de soutenabilité. C'est un état
passé.**

Donc « IBD = 1 » signifie *« comme en 1990 »*, tandis que « IEE = 1 »
signifie *« dans le budget de la planète »*. Ce ne sont pas les mêmes 1 —
et la moyenne géométrique les traite comme s'ils l'étaient.

C'était mentionné dans la fiche `EQ-EXEC-003` sous le terme « référence
glissante », rangé parmi les limites de l'IBD. **C'est plus grave que
cela : c'est une incohérence d'échelle entre les trois termes de l'IED.**

De plus, prendre 1990 pour référence revient à décréter que la France de
1990 était à l'équilibre écologique. Elle ne l'était pas — le déclin des
oiseaux agricoles avait déjà des décennies. **L'IBD est donc
structurellement trop optimiste**, d'un facteur inconnu.

### La solution existe, et la donnée aussi (D16)

Le **Biodiversity Intactness Index** (BII) mesure la part de la
biodiversité d'origine encore présente. Le cadre des **limites
planétaires** (Steffen *et al.* 2015) fixe la frontière de sécurité à
**BII ≥ 90 %**. C'est un **vrai seuil**, comparable au budget carbone.

| Source | Couverture | Licence | Statut |
|---|---|---|---|
| Natural History Museum, *BII country summaries* | **1970–2050** | CC Non-Commercial | ⚠️ téléchargement bloqué par Cloudflare |

⚠️ **Deux bonnes nouvelles et un obstacle.** C'est le bon concept, et la
série **remonte à 1970** — ce qui rouvrirait la période 1978 demandée au
cadrage. Mais le portail bloque le téléchargement automatisé (Cloudflare,
403), et le contournement par navigateur échoue aussi depuis cet
environnement. **Le fichier se récupère à la main en trente secondes dans
un navigateur** : `data.nhm.ac.uk/dataset/bii-bte`, ressource
`long_data.csv`.

#### Un adossement complémentaire : l'AMAE de l'OCDE

Source apportée par Stéphane : *Perspectives de l'environnement de l'OCDE
à l'horizon 2050* (2012, ch. 4). L'OCDE y utilise l'**AMAE** (abondance
moyenne des espèces), et la définit exactement comme il faut :
*« une AMAE de 100 % correspond à l'absence de perturbation »* — un
pourcentage de l'**état d'origine**, pas d'un état passé arbitraire.

Chiffres extraits par script (`modele/donnees/ocde_amae.py`) :

| AMAE terrestre, part de l'état intact | 2010 | 2050 (projeté) |
|---|---:|---:|
| **Europe** | **38,4 %** | 29,3 % |
| Monde | 67,5 % | 60,4 % |
| Amérique du Nord | 70,4 % | 65,3 % |

Et par biome — celui de la France est « forêts tempérées » :

| Biome | 1970 | 2010 |
|---|---:|---:|
| **Forêts tempérées** | **49,7 %** | **37,3 %** |
| Total monde | 75,8 % | 67,5 % |

**Ce que ça démontre.** Dès **1970**, le biome français n'avait déjà plus
que la **moitié** de son abondance d'origine. Prendre 1990 pour référence,
comme le fait notre IBD, revient donc à déclarer à l'équilibre un
écosystème déjà amputé de moitié. Le biais est chiffré, il n'est plus
seulement soupçonné.

⚠️ **Trois réserves, pour ne pas aller trop vite.**

1. **L'AMAE n'est pas le BII.** Cousins conceptuels, pas synonymes. La
   frontière de 90 % a été définie sur le **BII** (Steffen *et al.* 2015),
   pas sur l'AMAE. La transférer serait une erreur de catégorie.
2. **Pas de France** : l'OCDE ne descend qu'à « Europe ».
3. **Ce sont des projections de modèle** (GLOBIO/IMAGE), sur quatre points
   seulement, pas des observations annuelles.

⇒ L'AMAE **documente le concept** et donne l'ordre de grandeur européen.
Elle ne remplace pas le BII pour construire l'indicateur.

Trois options pour D16 :

- **S1 — BII avec la frontière planétaire à 90 %.** Le bon seuil, et la
  période 1978 redevient possible. *Demande un téléchargement manuel.*
- **S2 — garder l'état de 1990**, en écrivant noir sur blanc que l'IBD est
  sur une échelle différente des deux autres.
- **S3 — retirer l'IBD de l'IED** (c'est la décision D12), et le publier
  comme diagnostic séparé.

---

## 5. Recommandation, à discuter

| Décision | Recommandation | Motif |
|---|---|---|
| **D14** borne basse | **B5** — jamais 0, plus un plancher explicite | L'extinction monétaire ne doit pas être un effet de bord d'un mapping. Le plancher protège aussi de l'annulation par la moyenne géométrique. |
| **D15** borne haute | **H3** — `[1 ; 2]` = régénération | Seule lecture cohérente avec l'homéostasie. Assumer que l'intervalle est aujourd'hui vide. |
| **D16** seuil IBD | **S1** — BII, frontière à 90 % | Rend les trois seuils commensurables, et rouvre 1978. |

**Ce que ces trois décisions ne règlent pas** : le choix du mapping lui-même
(**D11**) reste ouvert. Mais il devient moins dangereux — une fois la
borne basse bornée par un plancher, le mapping ne décide plus de la
survie monétaire d'un pays, seulement de la sévérité de la pénalité.

⚠️ Ces trois décisions sont de **catégorie D** : des choix normatifs, pas
des mesures. Elles passeront en analyse de sensibilité comme les autres.
