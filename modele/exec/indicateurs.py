"""
Les indicateurs EXEC : IBD, IEE, IRNR, et leur agrégation en IED.

**Le principe, en une phrase.** On mesure une pression sur la nature, on
la divise par le niveau qu'on juge soutenable, et on transforme ce rapport
en une note entre 0 et 2 où 1 = « exactement soutenable ».

    pression mesurée
    ────────────────  =  x     puis     I = mapping(x)
    seuil soutenable

`x = 1` → `I = 1` : l'équilibre. `x = 2` (deux fois trop) → `I` bas.
`x < 1` (sous le seuil) → `I > 1` : le pays peut créer plus de monnaie.

**Deux choix normatifs, et non un seul**, tous deux de catégorie D :

1. **le seuil de soutenabilité** — combien de tonnes, combien de CO₂ ?
2. **le mapping** — comment un dépassement se traduit-il en note ?

Le second est le plus structurant et le moins visible : à seuils
identiques, trois mappings raisonnables donnent à la France 2021 des IED
allant de 0,00 à 0,55. Il change donc la dynamique du modèle du tout au
tout. Il est présenté ici en trois variantes explicites, aucune n'étant
retenue par défaut sans arbitrage (cf. `docs/06-indicateurs-exec.md`).
"""
from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd

BORNE_HAUTE = 2.0

# ======================================================================
# 1. Les trois mappings — le choix normatif structurant
# ======================================================================


def mapping_lineaire(x: float | np.ndarray) -> float | np.ndarray:
    """**M1 — linéaire plafonné** : `I = 2 − x`, écrêté sur [0 ; 2].

    Le plus simple à expliquer : « chaque point de dépassement retire
    autant à la note ». Deux fois le seuil → note **zéro**.

    ⚠️ Conséquence lourde : la note atteint **exactement 0**, et comme
    l'IED est une moyenne géométrique, un seul indicateur à zéro annule
    toute la création monétaire du pays. Pour la France, dont l'empreinte
    carbone vaut environ 2,9 fois le seuil, ce mapping donne IEE = 0 —
    donc IED = 0, donc **zéro euro créé**. Ce n'est pas un bug : c'est ce
    que dit ce choix normatif.
    """
    return np.clip(BORNE_HAUTE - np.asarray(x, dtype=float), 0.0, BORNE_HAUTE)


def mapping_hyperbolique(x: float | np.ndarray,
                         beta: float = 1.0) -> float | np.ndarray:
    """**M2 — hyperbolique** : `I = 2 / (1 + x^β)`.

    Le plus indulgent : la note décroît vite au début puis s'aplatit, et
    **n'atteint jamais zéro**. Dépasser le seuil coûte cher, mais ne
    supprime pas la monnaie.

    `I(0) = 2`, `I(1) = 1` exactement, `I(x) → 0` quand `x → ∞`.
    `β` règle la brutalité : β = 1 est doux, β = 4 approche la falaise.
    """
    return BORNE_HAUTE / (1.0 + np.asarray(x, dtype=float) ** beta)


def mapping_exponentiel(x: float | np.ndarray) -> float | np.ndarray:
    """**M3 — exponentiel** : `I = 2^(1 − x)`.

    Intermédiaire, et le plus lisible en une phrase : **chaque fois qu'on
    dépasse le seuil d'une unité de plus, la note est divisée par deux.**

    `I(0) = 2`, `I(1) = 1` exactement, `I(2) = 0,5`, `I(3) = 0,25`,
    strictement positive partout. Régulateur ferme mais qui ne coupe
    jamais totalement le robinet.
    """
    return BORNE_HAUTE * 2.0 ** (-np.asarray(x, dtype=float))


MAPPINGS: dict[str, Callable] = {
    "lineaire": mapping_lineaire,
    "hyperbolique": mapping_hyperbolique,
    "exponentiel": mapping_exponentiel,
}


# ======================================================================
# 2. Seuils de soutenabilité — l'autre choix normatif
# ======================================================================

# Budget carbone : AR6 du GIEC (WG1, 2021, tableau SPM.2) — 500 GtCO₂
# restants au 1er janvier 2020 pour 50 % de chance de tenir 1,5 °C.
# Réparti par tête sur la population mondiale de 2020 et sur 30 ans.
BUDGET_1_5C_GT = 500.0
POP_MONDE_2020 = 7.84e9
HORIZON_ANS = 30.0
SEUIL_CO2_T_HAB = BUDGET_1_5C_GT * 1e9 / (POP_MONDE_2020 * HORIZON_ANS)
"""≈ 2,13 tCO₂ par habitant et par an. **Choix normatif**, pas une mesure :
il suppose un partage égalitaire par tête, sans tenir compte des émissions
passées ni des capacités. D'autres clés de partage donnent de 1 à 4 t."""

# Matières non renouvelables : corridor cible de Bringezu (2015).
SEUIL_MATIERE_T_HAB = 8.0
"""8 tonnes de matière abiotique par habitant et par an. **Choix
normatif** : Bringezu propose un corridor, pas un point. Fourchette
retenue en sensibilité : 6 à 12 t/hab."""


# ======================================================================
# 3. Les trois indicateurs
# ======================================================================

def irnr(dmc: pd.DataFrame, population: pd.Series,
         seuil_t_hab: float = SEUIL_MATIERE_T_HAB,
         mapping: str = "exponentiel",
         non_renouvelables: tuple[str, ...] = ("MF2", "MF3", "MF4"),
         ) -> pd.DataFrame:
    """
    **IRNR — ressources non renouvelables.**

    Pression mesurée : les tonnes de matière **non renouvelable** (minerais
    métalliques, minéraux non métalliques, énergies fossiles) consommées
    par habitant et par an. La biomasse, renouvelable, est exclue.

    Le recyclage est compté positivement **par construction** : le DMC ne
    compte que la matière vierge, donc recycler le fait baisser. Aucun
    bonus n'est ajouté — ce serait un double comptage (cf.
    `modele.donnees.ecologie.dmc_par_matiere`).

    Renvoie un tableau avec la pression, le rapport au seuil et l'indice.
    """
    tonnes = dmc[list(non_renouvelables)].sum(axis=1) * 1e3   # kt → t
    pression = (tonnes / population).dropna()
    x = pression / seuil_t_hab
    return pd.DataFrame({
        "pression_t_hab": pression,
        "ratio": x,
        "indice": MAPPINGS[mapping](x),
    })


def irnr_empreinte(empreinte: pd.DataFrame,
                   seuil_t_hab: float = SEUIL_MATIERE_T_HAB,
                   mapping: str = "exponentiel") -> pd.DataFrame:
    """
    **IRNR calculé sur l'empreinte matières, importations incluses.**

    Même définition que `irnr`, mais la pression n'est plus le DMC
    territorial : c'est toute la matière non renouvelable remuée **dans le
    monde entier** pour ce que les Français consomment (EXIOBASE, 1995–2024).

    ⚠️ **Ce n'est pas un raffinement, c'est une correction.** Les deux
    mesures ne diffèrent pas seulement en niveau — elles vont **en sens
    contraire** :

    | | 1995 | 2022 | tendance |
    |---|---:|---:|---|
    | DMC territorial | 9,99 | 7,77 t/hab | **−22 %** |
    | Empreinte (EXIOBASE) | 9,58 | 12,12 t/hab | **+26 %** |

    Le DMC dit que la France s'est allégée d'un cinquième. L'empreinte dit
    qu'elle s'est alourdie d'un quart. L'écart entre les deux passe de
    −4 % en 1995 à **+80 % en 2023** : c'est la signature de la
    délocalisation. *L'« amélioration » mesurée par l'IRNR territorial
    était, pour l'essentiel, un déménagement.*

    Le recyclage continue d'être compté positivement : l'empreinte
    matières ne compte que l'extraction primaire.
    """
    pression = empreinte["mat_non_renouv_t_hab"].dropna()
    x = pression / seuil_t_hab
    return pd.DataFrame({
        "pression_t_hab": pression,
        "ratio": x,
        "indice": MAPPINGS[mapping](x),
    })


def iee(co2: pd.DataFrame, seuil_t_hab: float = SEUIL_CO2_T_HAB,
        mapping: str = "exponentiel",
        colonne: str = "empreinte") -> pd.DataFrame:
    """
    **IEE — empreinte écologique, importations incluses.**

    ⚠️ **Approximation documentée.** La synthèse (§14.1) demande une
    empreinte écologique au sens du Global Footprint Network, en hectares
    globaux, comparée à la biocapacité. Cette donnée n'est pas accessible
    sans clé d'API nominative. On lui substitue l'**empreinte carbone
    importations incluses**, qui est la composante dominante de
    l'empreinte écologique mondiale, calculée par tableau
    entrées-sorties multirégional (Global Carbon Project).

    Ce que l'approximation perd : l'usage des sols, l'eau, la pêche, la
    surface forestière. Ce qu'elle garde : le carbone, et le fait
    d'inclure les importations — l'exigence explicite de la synthèse.
    Grade **C**. À remplacer dès qu'une clé GFN est obtenue.
    """
    # Les émissions OWID / Global Carbon Project sont en MILLIONS de
    # tonnes : conversion en tonnes avant division par la population.
    pression = (co2[colonne] * 1e6 / co2["population"]).dropna()
    x = pression / seuil_t_hab
    return pd.DataFrame({
        "pression_t_hab": pression,
        "ratio": x,
        "indice": MAPPINGS[mapping](x),
    })


def ibd(biodiversite: pd.Series, annee_reference: int = 1990,
        mapping: str = "exponentiel") -> pd.DataFrame:
    """
    **IBD — biodiversité.** ⚠️ **Le plus fragile de loin. À lire avec ses
    limites, ou pas du tout.**

    Faute de mieux, on utilise l'indice des oiseaux communs des milieux
    agricoles, seule série d'état de la biodiversité française disponible
    par API. La « pression » est définie comme la dégradation par rapport
    à une année de référence : `x = indice(référence) / indice(année)`.
    Un indice divisé par deux donne `x = 2`.

    **Quatre limites, dont deux sont rédhibitoires** :

    1. *Un taxon, un milieu.* Les oiseaux agricoles ne disent rien des
       sols, des insectes, du milieu marin, ni des forêts.
    2. *Aucune dimension importations.* La déforestation causée à
       l'étranger par la consommation française n'y figure pas du tout —
       alors que c'est l'exigence centrale de la synthèse §14.1.
       **L'IBD est le seul des trois indicateurs à violer cette exigence.**
    3. *Référence glissante.* Prendre 1990 comme référence revient à
       décréter que la France de 1990 était à l'équilibre écologique.
       Elle ne l'était pas. L'IBD est donc structurellement **trop
       optimiste**, d'un facteur inconnu.
    4. *Rupture de série en 2000*, retirée en amont.

    Conclusion honnête : cet IBD est un **bouche-trou explicite**, de
    grade C, publié pour montrer ce qui manque — pas pour mesurer la
    biodiversité. Voir `docs/06-indicateurs-exec.md` §4.
    """
    if annee_reference not in biodiversite.index:
        raise ValueError(f"année de référence {annee_reference} absente "
                         f"de la série ({biodiversite.index.min()}–"
                         f"{biodiversite.index.max()})")
    ref = biodiversite.loc[annee_reference]
    x = ref / biodiversite
    return pd.DataFrame({
        "indice_oiseaux": biodiversite,
        "ratio": x,
        "indice": MAPPINGS[mapping](x),
    })


# ======================================================================
# 4. Agrégation
# ======================================================================

def ied(indicateurs: pd.DataFrame) -> pd.Series:
    """
    **IED — indicateur d'équilibre dynamique** : la moyenne géométrique
    des indicateurs fournis (décision D6).

    `IED = (IBD × IEE × IRNR)^(1/3)`

    La moyenne géométrique est volontaire : un indicateur catastrophique
    ne peut pas être racheté par un excédent ailleurs. Contrepartie, qui
    est aussi son danger : **si un seul indicateur atteint 0, l'IED
    s'annule et la création monétaire du pays s'arrête net.**

    ⚠️ **Calcul strict** : si un seul des indicateurs demandés manque
    cette année-là, l'IED vaut `NaN`. C'est délibéré. Ignorer un
    indicateur manquant reviendrait à le remplacer par « tout va bien » —
    et comme l'indicateur qui manque en fin de période est justement le
    plus contraignant (l'empreinte carbone, publiée avec deux ans de
    retard), cela produirait un IED faussement flatteur.

    Pour comparer un IED à deux et à trois indicateurs, on appelle donc
    cette fonction deux fois sur des sous-ensembles de colonnes
    explicites — jamais en laissant des trous se combler tout seuls.
    """
    d = indicateurs.astype(float)
    n = d.shape[1]
    complet = d.notna().all(axis=1)
    produit = d.prod(axis=1)
    return (produit ** (1.0 / n)).where(complet).rename("IED")


def assembler(irnr_df: pd.DataFrame, iee_df: pd.DataFrame,
              ibd_df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Réunit les trois indicateurs et calcule l'IED, avec et sans IBD.

    Colonnes : `IRNR`, `IEE`, `IBD`, `IED` (les trois) et `IED_sans_IBD`
    (les deux robustes). Publier les deux est délibéré : l'écart entre
    elles mesure exactement ce que le maillon faible fait au résultat.
    """
    cols = {"IRNR": irnr_df["indice"], "IEE": iee_df["indice"]}
    if ibd_df is not None:
        cols["IBD"] = ibd_df["indice"]
    d = pd.DataFrame(cols)
    d["IED_sans_IBD"] = ied(d[["IRNR", "IEE"]])
    if ibd_df is not None:
        d["IED"] = ied(d[["IRNR", "IEE", "IBD"]])
    return d
