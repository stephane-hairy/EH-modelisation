# Indicateurs EXEC de la France — IBD, IEE, IRNR, IED

> **Jalon P2, le livrable phare.** La synthèse EH exige trois indicateurs
> valant 1 à l'équilibre et bornés sur [0 ; 2], mais **n'en donne aucune
> formule**. Il fallait les créer. Ce document dit comment, avec quelles
> données, et surtout **ce qui manque**.
>
> Reproductible : `python scripts/construire_exec.py` puis
> `python scripts/courbe_creation_monetaire.py`.
> Testé : `tests/test_exec.py` (26 tests).
> Fiches : `EQ-EXEC-001` à `005`, toutes en **catégorie D**.

---

## En une page

| | |
|---|---|
| **Période demandée** | 1978–2023 (décision D5) |
| **Période livrée** | **1990–2021**, l'année 2000 exclue |
| **Pourquoi** | Les données écologiques françaises **n'existent pas avant 1990** |
| **IED français** | **0,41 à 0,57** sur toute la période — jamais proche de 1 (mapping exponentiel) |
| **Verdict IBD** | ⚠️ **Les données ne suffisent pas.** Bouche-trou documenté, pas une mesure |
| **Choix à arbitrer** | Le **mapping** (IED 2021 de **0,00 à 0,72**) **et** le **seuil carbone** (facteur **1,96** entre GIEC et GFN) |

**Le résultat principal, en une phrase** : sous l'économie homéostatique,
la France aurait été en **régime de création monétaire réduite de moitié
en permanence** depuis 1990 — et cela sans jamais s'améliorer beaucoup,
l'IED passant seulement de 0,45 à 0,54 en trente ans.

---

## 1. Le principe, en une image

On mesure une pression sur la nature, on la divise par ce qu'on juge
soutenable, et on transforme ce rapport en note :

```
   pression mesurée
   ─────────────────  =  x        puis      I = mapping(x)
   seuil soutenable
```

- `x = 1` → `I = 1` : l'équilibre. Le pays crée sa monnaie « normalement ».
- `x = 3` (trois fois trop) → `I` bas. Le pays s'appauvrit.
- `x < 1` → `I > 1`. Le pays peut créer plus.

**Il y a donc deux choix normatifs, pas un** : le *seuil* et le *mapping*.
Le second est le moins visible et le plus décisif (§5).

---

## 2. Ce que les données permettent réellement

C'est le point le plus important de ce document.

| Série | Source | Couverture |
|---|---|---|
| Flux de matières (DMC) | Eurostat `env_ac_mfa` | **1990**–2024 |
| Empreinte carbone importations incluses | Global Carbon Project (MRIO Eora) | **1990**–**2022** |
| Oiseaux communs agricoles | Eurostat `env_bio2` | **1990**–**2021** |
| Empreinte matières (RMC) | Eurostat `env_ac_rme` | 2008–2025 |
| Taux d'utilisation circulaire | Eurostat `cei_srm030` | 2010–2024 |

⇒ **Fenêtre où les trois indicateurs existent : 1990–2021.**

### Le trou 1978–1989 n'est pas comblé

Douze ans manquent par rapport au cadrage. Ce n'est **pas** un défaut de
notre collecte :

- Les **comptes de flux de matières** français commencent en 1990. Rien
  d'harmonisé n'existe avant à l'échelle nationale.
- L'**indice d'oiseaux communs** français commence en 1989-1990 : c'est
  l'année de lancement du protocole STOC. Personne n'a compté avant.
- Les **émissions importations incluses** commencent en 1990 : les
  tableaux entrées-sorties mondiaux nécessaires n'existent pas plus tôt.

Combler ce trou exigerait d'inventer douze années de données pour les
trois indicateurs à la fois. Ce ne serait pas un modèle, ce serait un
dessin. **RÈGLE N°3 : on documente le trou.**

Une seule série remonte plus loin : les émissions de CO₂ **territoriales**
(depuis 1802). Elles excluent les importations et violent donc l'exigence
§14.1. Elles figurent dans le CSV en colonne de diagnostic, **jamais**
comme substitut.

### Et 2022–2023 ?

L'empreinte carbone est publiée avec deux ans de retard, l'indice
d'oiseaux s'arrête en 2021. Un IED 2023 exigerait de remplacer les
indicateurs manquants par une valeur neutre — ce qui produit un IED
**faussement flatteur**, l'indicateur manquant étant justement le plus
contraignant. Le calcul est donc **strict** : un indicateur absent
donne `NaN`, pas un IED optimiste. *(Piège rencontré et corrigé en cours
de développement ; verrouillé par un test.)*

---

## 3. Les trois indicateurs

### IRNR — ressources non renouvelables (fiche EQ-EXEC-001)

**Mesure** : tonnes de matière non renouvelable par habitant et par an —
minerais métalliques, minéraux non métalliques, énergies fossiles. La
biomasse, renouvelable, est exclue.

**Le recyclage compte positivement — sans qu'on ajoute rien.** C'est le
point à ne pas rater. Le DMC ne compte que la matière **vierge** : une
tonne recyclée en interne n'y figure pas. Un pays qui recycle davantage a
donc mécaniquement un DMC plus faible à service rendu égal. *Ajouter un
bonus de recyclage serait un double comptage.* Le taux d'utilisation
circulaire est publié à part, comme diagnostic.

**Seuil** : 8 t/hab/an (Bringezu 2015, corridor 6–12).

**Résultat** : la France passe de **10,9 t/hab** (1990) à **7,8 t/hab**
(2022) — elle traverse le seuil vers 2014. C'est le seul des trois
indicateurs à atteindre l'équilibre.

⚠️ **Deux limites lourdes.** D'abord, le DMC est *territorial* : il compte
le poids des biens importés, pas la matière remuée à l'étranger pour les
produire. La France, gros importateur, est flattée. Ensuite, les minéraux
non métalliques (essentiellement les granulats du BTP) font **79 %** du
total : l'indicateur mesure surtout l'activité du bâtiment.

### IEE — empreinte écologique, importations incluses (fiche EQ-EXEC-002)

⚠️ **Ce n'est pas l'empreinte écologique demandée.** La synthèse (§14.1)
renvoie au Global Footprint Network — hectares globaux, comparés à la
biocapacité. Son API exige une clé nominative et répond 403 sans elle.

On substitue l'**empreinte carbone importations incluses**, calculée par
le Global Carbon Project avec un tableau entrées-sorties multirégional
(Eora, même famille de méthode qu'EXIOBASE). C'est la composante
dominante de l'empreinte écologique, et elle satisfait l'exigence
centrale : les importations sont comptées.

**Ce que l'approximation perd** : usage des sols, eau douce, pêche,
forêts, et toute notion de biocapacité. **Grade C.**

#### ⚠️ L'ampleur de l'approximation est maintenant mesurée

Le **paquet public officiel du GFN** a été retrouvé via Dateno (*National
Footprint Accounts 2017*, licence Creative Commons). Il ne contient
qu'**une seule année, 2013** — ce n'est pas la série. Mais une année
suffit à répondre à la seule question qui compte : *de combien se
trompe-t-on ?*

**France 2013, chiffres officiels du GFN** (hectares globaux par personne) :

| | gha/pers |
|---|---:|
| **Empreinte de consommation** (importations incluses) | **5,063** |
| dont carbone | 2,852 (**56,3 %**) |
| dont cultures | 1,041 |
| dont forêt | 0,523 |
| dont pâturage | 0,267 |
| dont pêche | 0,196 |
| dont sol bâti | 0,184 |
| **Biocapacité disponible** | **2,910** |
| Déficit | −2,152 |
| **Rapport empreinte / biocapacité** | **1,740** |

*Il faudrait 1,74 France pour soutenir le mode de vie français.*

Deux enseignements :

1. **L'hypothèse « le carbone domine » est vérifiée — de peu.** 56,3 %.
   L'approximation rate donc **43,7 %** du sujet, soit 2,21 gha/pers.
2. **Notre seuil était deux fois trop sévère.** Pour la même année 2013 :

   | Référentiel | Pression `x` |
   |---|---:|
   | Notre approximation (7,26 tCO₂/hab ÷ 2,13 t) | **3,41** |
   | Global Footprint Network | **1,74** |

   **Facteur 1,96.** Ce n'est pas une erreur de calcul : les deux
   référentiels ne posent pas la même question.
   - Le seuil GIEC demande : *« quelle part du budget climatique mondial
     chaque humain peut-il utiliser ? »* — planétaire, égalitaire.
   - Le rapport du GFN demande : *« la France vit-elle sur sa propre
     biocapacité ? »* — territorial.

   Pour reproduire le niveau du GFN, il faudrait un seuil de
   **4,17 tCO₂/hab** — précisément le bord supérieur de la fourchette
   1–4 t déjà déclarée en sensibilité.

**Ce que ça change** :

| Mapping | IEE 2013, seuil 2,13 | IEE 2013, seuil GFN 4,17 |
|---|---:|---:|
| linéaire | **0,00** | 0,26 |
| hyperbolique | 0,45 | 0,73 |
| exponentiel | 0,19 | 0,60 |

Sous le mapping linéaire, l'IEE **cesse d'être nul** — ce qui supprime
l'annulation totale de la création monétaire française.

⚠️ **Conséquence pour l'arbitrage : le seuil (D13) pèse autant que le
mapping (D11).** Les deux doivent être tranchés ensemble.

⚠️ **Ce que ça ne règle pas** : une seule année d'ancrage recale le
*niveau*, pas la *forme*. Si le rapport empreinte/biocapacité français a
évolué autrement que son empreinte carbone entre 1990 et 2021, nous ne le
voyons pas. Obtenir la série GFN complète (1961→) reste la seule vraie
solution, et exige une clé d'API nominative.

Reproductible : `python scripts/valider_iee_gfn.py`.

**Seuil** : 2,13 tCO₂/hab/an — budget 1,5 °C du GIEC (AR6, 500 Gt),
partagé également par tête sur 30 ans. Le partage égalitaire est un
**choix politique** : il ignore les émissions historiques. D'autres clés
donnent de 1 à 4 t.

**Résultat** : la France passe de **8,7** à **6,2 tCO₂/hab** (1990→2022),
soit **2,9 fois** le seuil. C'est **l'indicateur qui pilote l'IED
français** — de loin le plus dégradé des trois.

### IBD — biodiversité (fiche EQ-EXEC-003) ⚠️

**Verdict : les données ne suffisent pas.** C'était le risque annoncé au
cadrage ; il s'est réalisé.

Seule série disponible : l'indice des oiseaux communs des milieux
agricoles, 1990–2021. Elle recule de **93 à 54, soit −42 %**.

**Deux limites rédhibitoires**, à citer dans toute publication :

1. **Aucune dimension importations.** La déforestation provoquée à
   l'étranger par la consommation française (soja, huile de palme, bois)
   n'y figure pas *du tout*. C'est pourtant l'exigence centrale de la
   synthèse §14.1. **L'IBD est le seul des trois indicateurs à violer
   cette exigence, et il la viole totalement.**
2. **Référence glissante.** Prendre 1990 comme référence revient à
   décréter que la France de 1990 était à l'équilibre écologique. Elle ne
   l'était pas — le déclin des oiseaux agricoles avait déjà des
   décennies. **L'IBD est donc structurellement trop optimiste**, d'un
   facteur inconnu et non estimable avec les données disponibles.

Trois limites de plus : un seul taxon dans un seul milieu (rien sur les
sols, insectes, mer, forêts, outre-mer) ; une **rupture de série en
2000** (valeur publiée 100,0 encadrée par 69,5 et 72,7 — un bond de 40 %
suivi d'une chute équivalente n'a aucun sens biologique, l'année est
retirée) ; et une série arrêtée en 2021.

**Ce qu'on fait de ce trou.** Conformément à la RÈGLE N°3 : on le
documente au lieu de le combler. Concrètement, **toutes les sorties
publient deux IED** — avec et sans biodiversité. L'écart entre les deux
mesure exactement ce que le maillon faible fait au résultat : environ
**+0,15 point** dans les années 1990, **quasi nul depuis 2019**.

Trois issues restent ouvertes, aucune n'étant tranchée : approximation
documentée (l'état actuel), paramètre libre balayé, ou **retrait pur et
simple de l'IBD** — la colonne `IED_sans_IBD` existe pour cela.

---

## 4. Résultats

IED français, mapping exponentiel, 1990–2021 :

| Année | mat. t/hab | IRNR | CO₂ t/hab | IEE | oiseaux | IBD | **IED** | IED sans IBD |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1990 | 10,9 | 0,78 | 8,7 | 0,12 | 93 | 1,00 | **0,45** | 0,30 |
| 1995 | 10,0 | 0,84 | 8,6 | 0,12 | 75 | 0,84 | **0,44** | 0,32 |
| 2005 | 9,6 | 0,87 | 9,0 | 0,11 | 79 | 0,88 | **0,44** | 0,31 |
| 2010 | 8,4 | 0,96 | 7,9 | 0,15 | 62 | 0,70 | **0,47** | 0,38 |
| 2015 | 7,6 | 1,04 | 6,5 | 0,24 | 62 | 0,70 | **0,56** | 0,50 |
| 2021 | 7,9 | 1,01 | 6,3 | 0,26 | 54 | 0,60 | **0,54** | 0,51 |

**Trois lectures :**

1. **L'IED français n'approche jamais 1.** Il oscille entre 0,41 et 0,57.
   Sous l'EH, la France aurait vécu en permanence sous un régime de
   création monétaire réduite de moitié. Le dividende par citoyen aurait
   valu **11 900 €/an (991 €/mois) en 2021**, non 22 000 €.
2. **L'amélioration est réelle mais lente** : +0,09 point en trente ans,
   portée par la baisse de l'empreinte carbone et de la consommation de
   matières.
3. **Elle est freinée par la biodiversité.** IRNR et IEE s'améliorent,
   IBD se dégrade continûment. L'écart entre les deux courbes d'IED se
   referme — non parce que la biodiversité va mieux, mais parce qu'elle
   rejoint les autres par le bas.

### La courbe de création monétaire

`sorties/creation_monetaire_eh_france.png`

Elle publie **une bande, pas un trait**, et c'est délibéré :

- **trait plein** : État + citoyens (`DETA + DTCIT`). Cette part ne
  dépend que de l'IED et de la population — aucune ambiguïté de formule.
- **bande** : le total, dont la part entreprises dépend de la formule
  DENT, **non arbitrée** (verrou P0, `docs/05-dent.md`).

En 2021, la création totale va de **1 794 à 3 275 Md€** selon la variante
de DENT retenue — **un facteur 1,8** sur le total, **7,7** sur la seule
part entreprises. Cette fourchette n'est pas une incertitude de mesure :
c'est **l'effet d'une décision de conception non prise**. Elle se
refermera quand D7–D10 seront tranchées, pas avec de meilleures données.

---

## 5. Le mapping vers [0 ; 2] — le choix qui décide de tout

Voilà la décision structurante, invisible dans les formules de la
synthèse. Trois règles également défendables :

| Mapping | Formule | En une phrase | Pente en x = 1 |
|---|---|---|---:|
| **M1 linéaire** | `I = 2 − x`, écrêté | « chaque point de dépassement retire autant » | −1,00 |
| **M2 hyperbolique** | `I = 2 / (1 + x)` | « on réduit fort, mais on ne coupe jamais » | −0,50 |
| **M3 exponentiel** | `I = 2^(1−x)` | « dépasser d'une unité divise la note par deux » | −0,69 |

Toutes trois valent **2 à pression nulle**, **1 exactement à l'équilibre**,
et décroissent. Elles diffèrent sur ce qui compte : ce qu'on fait d'un
pays qui dépasse largement.

**Ce que ça donne pour la France 2021**, dernière année où les trois
indicateurs existent (ratio carbone 2,94) :

| Mapping | IRNR | IEE | IBD | **IED** |
|---|---:|---:|---:|---:|
| linéaire | 1,01 | **0,00** | 0,27 | **0,00** |
| hyperbolique | 1,00 | 0,51 | 0,73 | **0,72** |
| exponentiel | 1,01 | 0,26 | 0,60 | **0,54** |

**Le mapping linéaire annule la création monétaire française.** Pas
« la réduit » : l'annule. L'empreinte carbone dépasse deux fois le seuil,
donc IEE = 0, donc la moyenne géométrique s'annule, donc **la France ne
crée plus un euro**. Ce n'est pas un bug — c'est ce que cette règle
normative affirme. Il faut décider si l'on assume cette affirmation.

### Pourquoi ce choix ne peut pas attendre le jalon P5

La **pente du mapping au point d'équilibre est le gain du régulateur EH**.
Un thermostat, c'est un capteur, une consigne et un actionneur : ici la
pente du capteur décide si la boucle converge, oscille ou diverge
(Sterman 2000, ch. 17). Les pentes vont de −0,50 à −1,00, soit **un
facteur 2 sur le gain de boucle**.

⇒ **Le mapping doit être arbitré avant l'analyse de stabilité, pas
après.** Le choisir, c'est déjà décider en partie du résultat de P5.

---

## 6. Ce qu'il reste à trancher — trois décisions

| # | Question | Options | Enjeu |
|---|---|---|---|
| **D11** | **Mapping** | linéaire / hyperbolique / exponentiel | IED 2021 de **0,00 à 0,72**. Fixe aussi le gain de boucle pour P5. |
| **D12** | **Sort de l'IBD** | garder en grade C / paramètre libre / **retirer** | ±0,15 point d'IED, et une exigence §14.1 violée s'il est gardé. |
| **D13** | **Seuils** | carbone **2,13 t (GIEC)** ou **4,17 t (calibré GFN)** · matières 6–12 t | ⚠️ **Facteur 1,96** sur la pression carbone — davantage que l'écart entre deux mappings. À trancher avec D11. |

**Recommandation, à discuter** : mapping **exponentiel** (M3) — c'est le
seul dont la règle s'énonce en une phrase, il ne s'annule jamais, et sa
pente est intermédiaire. Et **retirer l'IBD** de l'IED publié, en le
gardant comme diagnostic séparé : un indicateur qui viole l'exigence
d'inclure les importations et dont la référence est arbitraire fait plus
de mal que de bien à l'intérieur d'une moyenne géométrique.

---

## 7. Ce qu'il faudrait pour faire mieux

Par ordre d'utilité décroissante :

1. **Une clé d'API Global Footprint Network** (gratuite sur demande).
   Elle remplacerait l'approximation carbone par la vraie empreinte
   écologique, biocapacité comprise, et remonterait à **1961** — ce qui
   couvrirait enfin 1978. *C'est la seule action qui pourrait rouvrir la
   période demandée.* La recherche via Dateno a confirmé qu'aucune série
   GFN complète n'est librement accessible : seul le paquet public 2017
   (année 2013) l'est, et il sert désormais de point d'ancrage.
2. **EXIOBASE** (Zenodo, téléchargement lourd) : empreintes matières,
   sols et eau importations incluses, 1995–2022. Permettrait un IRNR en
   empreinte plutôt qu'en territorial.
3. **Une empreinte biodiversité importations incluses** — travaux type
   Chaudhary & Kastner, ou l'indicateur *Biodiversity Footprint*. C'est
   la seule voie pour un IBD conforme à §14.1.
4. **Les indicateurs de l'ONB et de l'INPN**, non exposés en API : à
   instrumenter à la main pour élargir l'IBD au-delà des oiseaux.

---

## Annexe — fiches de registre

| Fiche | Objet |
|---|---|
| `EQ-EXEC-001` | IRNR — ressources non renouvelables |
| `EQ-EXEC-002` | IEE — empreinte écologique, importations incluses |
| `EQ-EXEC-003` | IBD — biodiversité (bouche-trou documenté) |
| `EQ-EXEC-004` | Mapping vers [0 ; 2] |
| `EQ-EXEC-005` | IED — agrégation par moyenne géométrique |

Toutes en **catégorie D** : ce sont des choix normatifs créés pour ce
projet, jamais des mesures objectives. Aucun résultat ne doit être publié
sans son analyse de sensibilité.
