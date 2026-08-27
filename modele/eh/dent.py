"""
DENT — le dividende versé à une entreprise.

**En une phrase** : chaque année, la banque centrale *donne* de l'argent à
chaque entreprise ; ce module calcule combien.

Pourquoi ce fichier existe. La formule de la synthèse (§11.1) a été
construite « au doigt mouillé » — de l'aveu d'un de ses auteurs
(Stéphane Hairy, 2026-08-27). Or le total des dividendes d'entreprises
(DTENT) pèse plus de la moitié de la création monétaire d'un pays : cette
formule décide à elle seule de l'essentiel des résultats chiffrés.

Le module contient donc deux choses :

1. **La formule de la synthèse, telle qu'elle est écrite**, dans ses deux
   lectures possibles (le texte est ambigu — voir `LECTURES`), pour qu'on
   puisse la critiquer sur pièces plutôt que de mémoire.
2. **Trois formules alternatives**, chacune conçue pour corriger un défaut
   identifié, à arbitrer par les auteurs.

⚠️ Catégorie **D** (design) pour tout ce fichier : ce sont des choix
normatifs, jamais des relations observées. Fiches : `modele/registre/`.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# --------------------------------------------------------------------
# 1. La formule de la synthèse, telle quelle
# --------------------------------------------------------------------

LECTURES = {
    "A": "DENT = IED×P + (e×DCIT) / ((r/e) × 10⁴)",
    "B": "DENT = IED×P + (e×DCIT) / (r / (e × 10⁴))",
}
"""Les deux façons de lire le second terme de la formule §11.1.

Le PDF sort la formule en glyphes séparés : `( r / e × 1 0 ⁴ )`. On ne
sait donc pas si `10⁴` multiplie `r/e` (lecture **A**) ou `e` seul
(lecture **B**). Le texte qui accompagne la formule dit « *r* … est divisé
par le nombre d'employé de l'entreprise, lui-même multiplié par 10⁴ »,
ce qui désigne plutôt la lecture **B**.

Ce n'est pas un détail : **les deux lectures diffèrent d'un facteur 10⁸**
(cf. `ecart_entre_lectures`).
"""


def terme_correctif_synthese(e: float, dcit: float, r: float,
                             lecture: str = "A") -> float:
    """
    Le second terme de la formule §11.1 — celui censé « récompenser
    l'emploi et pénaliser les écarts de salaires ».

    Paramètres
    ----------
    e     : nombre de salariés de l'entreprise.
    dcit  : dividende d'un citoyen (€/an) — le « revenu minimum du pays ».
    r     : écart entre le plus haut salaire de l'entreprise et DCIT (€/an).
    lecture : "A" ou "B", cf. `LECTURES`.

    ⚠️ Trois défauts, démontrés dans `scripts/analyse_dent.py` :

    - **Il n'est pas homogène à des euros.** Sa dimension est un *nombre
      de personnes au carré*. On ne peut donc pas l'additionner à `IED×P`,
      qui est en €/an.
    - **Il diverge quand `r → 0`.** Une entreprise parfaitement égalitaire
      (le plus haut salaire vaut exactement le revenu minimum) reçoit un
      dividende infini.
    - **Il croît comme le carré de l'effectif**, alors que `P` croît à peu
      près linéairement. Les très grandes entreprises sont donc favorisées
      de façon explosive — l'inverse de l'intention affichée.
    """
    if e == 0:
        # Une entreprise sans salarié : le terme n'est pas défini
        # (« l'écart entre le plus haut salaire et DCIT » n'existe pas).
        # C'est le cas de la grande majorité des entreprises françaises.
        return float("nan")
    if r == 0:
        return float("inf")
    if lecture == "A":
        denominateur = (r / e) * 1e4
    elif lecture == "B":
        denominateur = r / (e * 1e4)
    else:
        raise ValueError(f"lecture inconnue : {lecture!r} (attendu 'A' ou 'B')")
    return (e * dcit) / denominateur


def ecart_entre_lectures() -> float:
    """Rapport entre la lecture B et la lecture A : exactement 10⁸.

    Les deux valent `e² × DCIT / r` à un facteur près :
    lecture A → divise par 10⁴, lecture B → multiplie par 10⁴.
    """
    return 1e8


def dent_synthese(ied: float, produit: float, e: float, dcit: float,
                  r: float, lecture: str = "A") -> float:
    """`DENT = IED × P + terme correctif` — la formule §11.1 telle quelle.

    ⚠️ **Ne pas utiliser pour produire un résultat publiable.** Fournie
    pour l'analyse critique uniquement (fiche EQ-EH-001, statut `rejete`).
    """
    return ied * produit + terme_correctif_synthese(e, dcit, r, lecture)


# --------------------------------------------------------------------
# 2. Facteurs d'équité — briques communes aux alternatives
# --------------------------------------------------------------------

def echelle_salariale(salaire_max: float, dcit: float) -> float:
    """L'écart de salaire exprimé **sans unité** : « le plus haut salaire
    vaut *s* fois le revenu minimum ».

    C'est la correction de fond par rapport à la synthèse, qui utilise un
    écart en euros (`r`) et se retrouve avec une formule inhomogène. Un
    *rapport* de deux salaires est un nombre pur : on peut le passer dans
    n'importe quelle fonction sans casser les unités.
    """
    if dcit <= 0:
        raise ValueError("dcit doit être strictement positif")
    return salaire_max / dcit


def facteur_equite_borne(s: float, s_ref: float = 5.0,
                         gamma: float = 2.0) -> float:
    """Facteur **multiplicatif** d'équité salariale, borné sur ]0 ; 2[.

    Intuition : on multiplie le dividende par un coefficient qui vaut
    - **2** quand l'entreprise est parfaitement égalitaire,
    - **1** quand son écart de salaires vaut l'écart de référence `s_ref`,
    - **→ 0** quand l'écart devient extrême.

    `κ(s) = 2 / (1 + (s / s_ref)^γ)`

    Propriétés (toutes vérifiées dans `tests/test_dent.py`) :
    strictement décroissante · bornée sur ]0 ; 2[ · `κ(s_ref) = 1`
    exactement · aucune division par zéro (`s ≥ 1 > 0`) · sans dimension.

    `s_ref` (écart de salaires jugé acceptable) et `γ` (brutalité de la
    pénalité) sont des **choix de conception**, à passer en sensibilité.
    """
    if s <= 0:
        raise ValueError("s doit être strictement positif")
    return 2.0 / (1.0 + (s / s_ref) ** gamma)


def facteur_equite_decroissant(s: float, s_0: float = 4.0,
                               gamma: float = 2.0) -> float:
    """Facteur d'équité borné sur ]0 ; 1], version « prime qui s'éteint ».

    `ψ(s) = 1 / (1 + ((s − 1) / s₀)^γ)`

    Vaut **1** pour une entreprise parfaitement égalitaire (`s = 1`, tout
    le monde au revenu minimum), décroît, et tend vers **0** quand l'écart
    explose. Sert à pondérer une prime, pas à moduler le tout.
    """
    if s < 1.0:
        # Un salaire sous le revenu minimum du pays : hors du cadre EH.
        # On sature plutôt que d'extrapoler.
        s = 1.0
    return 1.0 / (1.0 + ((s - 1.0) / s_0) ** gamma)


# --------------------------------------------------------------------
# 3. Les trois alternatives proposées
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Entreprise:
    """Les caractéristiques d'une entreprise dont dépend son dividende."""
    production: float          # produit d'exploitation de référence, €/an
    valeur_ajoutee: float      # production − consommations intermédiaires, €/an
    salaries: int              # effectif
    salaire_max: float         # plus haut salaire de l'entreprise, €/an


def dent_multiplicative(ied: float, ent: Entreprise, dcit: float,
                        s_ref: float = 5.0, gamma: float = 2.0) -> float:
    """**Alternative 1 — modulation multiplicative.**

    `DENT = IED × P × κ(s)`

    *Intention* : garder l'idée « le dividende est proche du produit
    d'exploitation », et faire jouer l'équité salariale comme un
    **coefficient** plutôt que comme un terme ajouté. C'est la correction
    minimale : elle rend la formule homogène par construction, puisqu'on
    multiplie des euros par un nombre sans unité.

    *Propriétés* : bornée entre 0 et `2 × IED × P` · décroissante en `s` ·
    aucune singularité · vaut exactement `IED × P` quand `s = s_ref`.

    *Ce qu'elle abandonne* : la récompense explicite de l'emploi. `P`
    croît déjà avec l'effectif, mais rien ne favorise l'intensité en
    main-d'œuvre à production égale.
    """
    s = echelle_salariale(ent.salaire_max, dcit)
    return ied * ent.production * facteur_equite_borne(s, s_ref, gamma)


def dent_deux_termes(ied: float, ent: Entreprise, dcit: float,
                     theta: float = 0.3, s_0: float = 4.0,
                     gamma: float = 2.0) -> float:
    """**Alternative 2 — deux termes, tous deux en euros.**

    `DENT = IED × [ (1−θ)·P + θ · e · DCIT · ψ(s) ]`

    *Intention* : rester au plus près des **mots** de la synthèse tout en
    réparant les mathématiques. Le produit `e × DCIT` figure littéralement
    dans le texte d'origine : c'est « la masse salariale si tout le monde
    était au revenu minimum ». C'est bien une somme d'euros. Le défaut de
    la formule d'origine ne venait pas de ce produit mais de la **division
    par `r/e`** qui suit.

    Ici l'écart de salaires ne divise plus : il **pondère** la prime, via
    `ψ(s) ∈ ]0 ; 1]`. Une entreprise égalitaire touche la prime entière ;
    une entreprise très inégalitaire n'en touche rien.

    *Propriétés* : homogène à des €/an · bornée par
    `IED × [(1−θ)·P + θ·e·DCIT]` · croissante en `e` (linéairement, pas au
    carré) · décroissante en `s` · aucune singularité en `s = 1`.

    `θ` arbitre entre « on récompense la taille économique » (θ = 0) et
    « on récompense l'emploi » (θ = 1). C'est le paramètre de conception
    le plus structurant de cette variante.
    """
    if not 0.0 <= theta <= 1.0:
        raise ValueError("theta doit être dans [0 ; 1]")
    s = echelle_salariale(ent.salaire_max, dcit)
    prime_emploi = ent.salaries * dcit * facteur_equite_decroissant(s, s_0, gamma)
    return ied * ((1.0 - theta) * ent.production + theta * prime_emploi)


def dent_valeur_ajoutee(ied: float, ent: Entreprise, dcit: float,
                        s_ref: float = 5.0, gamma: float = 2.0) -> float:
    """**Alternative 3 — assise sur la valeur ajoutée, pas la production.**

    `DENT = IED × VA × κ(s)`

    *Intention* : corriger un défaut **économique**, plus profond que le
    défaut mathématique. Le produit d'exploitation d'une entreprise
    contient ce qu'elle a acheté à ses fournisseurs. En sommant `P` sur
    toutes les entreprises, on compte donc plusieurs fois la même valeur —
    autant de fois qu'il y a de maillons dans la chaîne.

    Conséquence concrète : **deux entreprises qui fusionnent font baisser
    le dividende total**, alors que rien n'a changé dans l'économie
    réelle ; deux entreprises qui se scindent le font monter. La création
    monétaire dépendrait de la façon dont les entreprises découpent leurs
    contrats — une faille d'optimisation évidente.

    La valeur ajoutée n'a pas ce défaut : elle est *additive*. La somme
    des valeurs ajoutées ne bouge pas quand on fusionne ou scinde, et elle
    vaut le PIB. L'assiette de la création monétaire devient une grandeur
    macro-économique stable et interprétable.

    *Propriétés* : mêmes bonnes propriétés que l'alternative 1 · invariante
    au découpage juridique des entreprises · **assiette environ 2,6 fois
    plus faible** en France (VA des SNF 1 481 Md€ contre production
    3 810 Md€ en 2023, Eurostat `nasa_10_nf_tr`).

    *Ce qu'elle abandonne* : la phrase de la synthèse « un dividende
    relativement proche du produit d'exploitation ». C'est assumé — cette
    phrase est précisément ce qui produit la faille.
    """
    s = echelle_salariale(ent.salaire_max, dcit)
    return ied * ent.valeur_ajoutee * facteur_equite_borne(s, s_ref, gamma)


# --------------------------------------------------------------------
# 4. Le cliquet : que fait la règle « moyenne des 3 meilleures années » ?
# --------------------------------------------------------------------

@dataclass
class ResultatCliquet:
    """Trajectoire simulée de la base de référence `P`."""
    annees: np.ndarray
    base_P: np.ndarray          # base de référence en vigueur, €
    produit: np.ndarray         # produit d'exploitation observé, €
    dividende: np.ndarray       # DTENT versé, €
    point_fixe: float | None    # valeur d'équilibre analytique, si elle existe
    divergent: bool


def simuler_cliquet(produit_initial: float, ied: float = 1.0,
                    alpha: float = 0.8, n_entreprises: int = 4_906_972,
                    annees: int = 30, periode_reactualisation: int = 3,
                    choc: dict[int, float] | None = None,
                    meilleures_annees: int = 3) -> ResultatCliquet:
    """
    Simule la règle « `P` = moyenne des 3 meilleures années, réactualisée
    tous les 3 ans » au niveau macro-économique.

    **La question posée.** La synthèse précise que la réactualisation de
    `P` se fait « hors DENT », c'est-à-dire sans compter le dividende que
    l'entreprise a elle-même reçu. Cette précaution suffit-elle à
    empêcher un emballement ?

    **La réponse est non**, et la raison tient en une phrase : *le
    dividende d'une entreprise devient le chiffre d'affaires des autres*.
    Exclure son propre dividende retire `1/N` du flux — avec N ≈ 4,9
    millions d'entreprises en France, cela ne retire rien.

    Mécanique simulée
    -----------------
    - Produit d'exploitation observé : `X_t = X₀ + α × DTENT_t × (1 − 1/N)`
      où `α` est la part du dividende qui revient aux entreprises sous
      forme de chiffre d'affaires (le reste part en épargne, en impôts,
      en importations, en fonte).
    - Tous les `periode_reactualisation` ans, `P` est refixé à la moyenne
      des `meilleures_annees` meilleures années observées.
    - `DTENT_t = IED × P`.

    Résultat analytique
    -------------------
    La récurrence est `P ← X₀ + g·P` avec `g = α × IED × (1 − 1/N)`.
    - si `g < 1` : `P` converge vers `X₀ / (1 − g)` — une **amplification
      permanente** de facteur `1/(1−g)` ;
    - si `g ≥ 1` : `P` **diverge**.

    Avec `IED = 1` et `α = 0,8`, l'amplification est de **×5**. Avec
    `α = 0,9`, elle est de **×10**. Ce n'est pas une instabilité de calcul :
    c'est une **rétroaction positive** dans une théorie qui affirme n'en
    comporter aucune.

    Paramètres
    ----------
    choc : `{année: multiplicateur}` — applique un choc au produit
        d'exploitation cette année-là. Sert à montrer l'**effet cliquet** :
        `P` ne redescend pas après une récession, parce que la règle
        retient les *meilleures* années.
    """
    g = alpha * ied * (1.0 - 1.0 / n_entreprises)
    divergent = g >= 1.0
    point_fixe = None if divergent else produit_initial / (1.0 - g)

    base = produit_initial
    historique: list[float] = []
    a, bP, X, D = [], [], [], []

    for t in range(annees):
        dividende = ied * base
        x = produit_initial + alpha * dividende * (1.0 - 1.0 / n_entreprises)
        if choc and t in choc:
            x *= choc[t]
        historique.append(x)

        a.append(t); bP.append(base); X.append(x); D.append(dividende)

        if (t + 1) % periode_reactualisation == 0:
            meilleures = sorted(historique, reverse=True)[:meilleures_annees]
            # ⚠️ Le cliquet est ici : on prend les MEILLEURES années, donc
            # la base ne peut pratiquement jamais redescendre.
            base = float(np.mean(meilleures))

    return ResultatCliquet(np.array(a), np.array(bP), np.array(X),
                           np.array(D), point_fixe, divergent)
