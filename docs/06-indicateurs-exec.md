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
| **IED français** | **0,36 à 0,51** avec l'IRNR en empreinte — jamais proche de 1 (mapping exponentiel) |
| **Verdict IBD** | ⚠️ **Les données ne suffisent pas.** Bouche-trou documenté, pas une mesure |
| **Choix à arbitrer** | Le **mapping** vers [0 ; 2] — IED 2021 de **0,00 à 0,72**. *(L'étalon de l'IEE est tranché : mondial, décision D13.)* |

**Le résultat principal, en une phrase** : sous l'économie homéostatique,
la France aurait été en **régime de création monétaire réduite de moitié
en permanence** depuis 1990 — et sa lente amélioration apparente tient
entièrement au carbone : mesurée en **empreinte**, sa consommation de
matières s'est **aggravée de 26 %** sur la période.

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
| **Empreinte matières, importations incluses** | **EXIOBASE 3.10.2** via `pymrio` | **1995–2024** |
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

#### ⚠️ Correction majeure : le territorial inversait le signe de la tendance

La première version de cet indicateur utilisait le **DMC** d'Eurostat, une
mesure **territoriale** : elle compte le poids des biens qui franchissent
la frontière, pas la matière remuée à l'étranger pour les fabriquer.
EXIOBASE a permis de calculer l'**empreinte** réelle, 1995–2024. Le
résultat ne corrige pas un niveau, il **inverse une conclusion** :

| Mesure | 1995 | 2022 | Tendance |
|---|---:|---:|---|
| DMC territorial — *ce que disait l'IRNR* | 9,99 | 7,77 t/hab | **−22 %** |
| **Empreinte, importations incluses** | 9,58 | **12,12 t/hab** | **+26 %** |

Le DMC disait que la France s'était allégée d'un cinquième. L'empreinte
dit qu'elle s'est **alourdie d'un quart**.

L'écart entre les deux passe de **−4 % en 1995 à +80 % en 2023** (moyenne
+49 %). Cette croissance régulière est la signature de la délocalisation :
*l'« amélioration » que mesurait l'IRNR était, pour l'essentiel, un
déménagement.*

**Conséquences directes :**

- L'IRNR **n'est plus le seul indicateur à atteindre l'équilibre**. En
  territorial il passait sous le seuil de 8 t/hab vers 2014 ; en
  empreinte, **il ne passe jamais sous le seuil**.
- L'IED français baisse d'environ **9 %** (0,54 → 0,49 en 2021). La
  conclusion du jalon P2 tient — mais le récit change : la seule
  amélioration réelle est celle du **carbone**.
- **Correction annexe** : ce document affirmait que l'IBD était « le seul
  des trois indicateurs à violer l'exigence §14.1 » (inclure les
  importations). C'était faux : l'IRNR territorial la violait aussi.
  Depuis le passage à l'empreinte, l'affirmation est devenue vraie.

**Validation** : contrôle croisé du CO₂ entre EXIOBASE et le Global Carbon
Project, deux constructions indépendantes — **1,4 % d'écart en 2019**,
4,4 % en 2020. ⚠️ **Aucun contrôle équivalent n'existe pour les
matières** : EXIOBASE est un modèle, pas une observation directe.

Reproductible : `python scripts/comparer_irnr.py`
(la série : `python scripts/serie_exiobase.py`, ≈ 2 h).

**Ce qui subsiste comme limites**, quelle que soit la mesure :

- **Le poids n'est pas l'impact.** Une tonne de sable et une tonne
  d'uranium comptent pareil.
- **Les minéraux non métalliques dominent** (74 % de l'empreinte 2020) :
  l'indicateur mesure surtout l'activité du bâtiment.
- **L'empreinte démarre en 1995**, contre 1990 pour le DMC. On perd cinq
  ans pour gagner la justesse du concept. Le territorial reste implémenté
  pour la sensibilité et pour couvrir 1990–1994.

### IEE — empreinte écologique, importations incluses (fiche EQ-EXEC-002)

⚠️ **Ce n'est pas l'empreinte écologique demandée** — mais on sait
maintenant de combien on s'en écarte. La synthèse (§14.1) renvoie au
Global Footprint Network (hectares globaux). Son API exige une clé
nominative et répond 403 sans elle.

On substitue l'**empreinte carbone importations incluses**, calculée par
le Global Carbon Project avec un tableau entrées-sorties multirégional
(Eora, même famille de méthode qu'EXIOBASE). C'est la composante
dominante de l'empreinte écologique, et elle satisfait l'exigence
centrale : les importations sont comptées.

**Ce que l'approximation perd** : usage des sols, eau douce, pêche,
forêts, et toute notion de biocapacité. **Grade C.**

#### ✅ L'approximation est maintenant validée — à 15 % près

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
| Biocapacité de la France | 2,910 |
| Biocapacité mondiale par humain | 1,705 |

##### D'abord : quel étalon ? (décision D13)

Le GFN propose **deux** façons de rapporter cette empreinte à un seuil,
et elles ne disent pas du tout la même chose :

| Étalon | France 2013 | Question posée | Ce qu'il note |
|---|---:|---|---|
| **« nombre de Terres »** (÷ biocapacité mondiale) | **2,97** | *Combien de planètes si tout le monde vivait ainsi ?* | le **comportement** |
| « nombre de pays » (÷ biocapacité française) | 1,74 | *La France vit-elle sur ses moyens ?* | la **géographie** |

**L'étalon territorial crée une incitation perverse**, et les chiffres le
montrent sans appel (mapping exponentiel) :

| Pays | Empreinte | IEE, étalon **mondial** | IEE, étalon territorial |
|---|---:|---:|---:|
| Bangladesh | 0,75 | **1,47** | 0,50 |
| France | 5,06 | 0,26 | 0,60 |
| Australie | 8,80 | **0,06** | **1,35** |

L'Australie consomme **74 % de nature de plus** que la France, et serait
pourtant **2,3 fois mieux dotée en monnaie** — parce qu'elle a de
l'espace. Le Bangladesh consomme **7 fois moins** que la France et serait
**moins bien noté** — parce qu'il est dense.

Pour une théorie mondiale dont le mécanisme central est de récompenser la
vertu écologique, récompenser en réalité la faible densité de population
est une faille de premier ordre. → **Étalon retenu : le mondial (D13).**

##### Ensuite : notre approximation tient

Sur l'étalon retenu, pour la même année 2013 :

| Mesure | Pression `x` |
|---|---:|
| Notre approximation (7,26 tCO₂/hab ÷ 2,13 t) | **3,41** |
| GFN, nombre de Terres | **2,97** |

**Écart : 15 %.** Les deux posent la même question — *quelle part des
ressources de la planète, par tête ?* — l'une par le carbone, l'autre par
les hectares globaux. Elles convergent.

Un recalage exact demanderait un seuil de **2,44 tCO₂/hab** au lieu de
2,13 : un ajustement de 15 %, très à l'intérieur de la fourchette 1–4 t
déjà déclarée. Sous mapping exponentiel, l'IEE 2013 passe de 0,19 à 0,26.

⇒ **Le jalon P2 n'a pas à être refait.** L'IED français reste très en
dessous de 1, et le **mapping (D11) redevient le seul choix vraiment
structurant**.

> ⚠️ **Correction actée.** Une version antérieure de cette note concluait
> que « notre seuil était deux fois trop sévère ». Ce facteur 1,96 valait
> contre l'étalon *territorial*, écarté depuis par D13. Contre l'étalon
> retenu, l'écart est de 15 %.

##### Ce que ça ne règle pas

- **Une seule année d'ancrage.** On valide le *niveau* de la série, pas sa
  *forme*. Si le « nombre de Terres » français a évolué autrement que son
  empreinte carbone entre 1990 et 2021, nous ne le voyons pas.
- **44 % de l'empreinte reste hors champ** : cultures, forêts, pâturages,
  pêche, sol bâti. La convergence à 15 % est donc partiellement une
  compensation d'erreurs, pas une mesure de ces composantes.

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

IED français, mapping exponentiel, IRNR en empreinte, 1995–2021 :

| Année | mat. t/hab | IRNR | CO₂ t/hab | IEE | oiseaux | IBD | **IED** | IED sans IBD |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1995 | 9,6 | 0,87 | 8,6 | 0,12 | 75 | 0,84 | **0,45** | 0,32 |
| 2005 | 14,7 | 0,56 | 9,0 | 0,11 | 79 | 0,88 | **0,38** | 0,25 |
| 2010 | 13,3 | 0,63 | 7,9 | 0,15 | 62 | 0,70 | **0,41** | 0,31 |
| 2015 | 13,0 | 0,65 | 6,5 | 0,24 | 62 | 0,70 | **0,48** | 0,39 |
| 2021 | 11,0 | 0,77 | 6,3 | 0,26 | 54 | 0,60 | **0,49** | 0,45 |

**Trois lectures :**

1. **L'IED français n'approche jamais 1.** Il reste entre 0,36 et 0,51.
   Sous l'EH, la France aurait vécu en permanence sous un régime de
   création monétaire réduite de moitié. Le dividende par citoyen aurait
   valu **10 881 €/an (907 €/mois) en 2021**, non 22 000 €.
2. **L'amélioration est faible, et elle tient à un seul terme.** L'IED
   gagne +0,04 point entre 1995 et 2021 (0,45 → 0,49), et il passe même
   par un creux à 0,38 en 2005. **Seul le carbone progresse vraiment**
   (IEE 0,12 → 0,26). L'IRNR, lui, s'est d'abord effondré (0,87 → 0,51 en
   2000) avant de remonter partiellement — sans jamais revenir à son
   niveau de 1995.
3. **La biodiversité se dégrade sans interruption** (IBD 0,84 → 0,60).
   L'écart entre les deux courbes d'IED se referme — non parce que la
   biodiversité va mieux, mais parce qu'elle rejoint les autres par le
   bas.

### La courbe de création monétaire

`sorties/creation_monetaire_eh_france.png`

Elle publie **une bande, pas un trait**, et c'est délibéré :

- **trait plein** : État + citoyens (`DETA + DTCIT`). Cette part ne
  dépend que de l'IED et de la population — aucune ambiguïté de formule.
- **bande** : le total, dont la part entreprises dépend de la formule
  DENT, **non arbitrée** (verrou P0, `docs/05-dent.md`).

En 2021, la création totale va de **1 641 à 2 995 Md€** selon la variante
de DENT retenue — **un facteur 1,8** sur le total, **7,7** sur la seule
part entreprises. *(Chiffres recalculés avec l'IRNR en empreinte ; ils
étaient de 1 794 à 3 275 Md€ avec l'IRNR territorial.)* Cette fourchette n'est pas une incertitude de mesure :
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
| ~~**D13**~~ | ~~**Étalon et seuils**~~ | **TRANCHÉE** : étalon **mondial**, seuil carbone 2,13 t (validé à 15 % près). Reste ouvert : matières 6–12 t | L'étalon territorial est écarté — il récompensait la géographie. Voir `docs/04-decisions.md` D13. |

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
