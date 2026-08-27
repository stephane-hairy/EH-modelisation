"""
Séries écologiques françaises nécessaires aux indicateurs EXEC.

Une fonction par série, chacune renvoyant une `pandas.Series` indexée par
année (entier). Tout passe par le cache reproductible de
`modele.donnees.cache` : chaque téléchargement laisse son empreinte
SHA-256 dans `donnees/manifeste.json`.

⚠️ **Ce que ce module ne peut PAS fournir**, et pourquoi c'est important :

- **L'empreinte écologique du Global Footprint Network** (en hectares
  globaux, biocapacité comprise). Son API exige une clé nominative
  (`api.footprintnetwork.org` répond 403 sans elle). On lui substitue
  l'**empreinte carbone importations incluses**, qui en est la composante
  dominante — c'est une approximation documentée, pas un équivalent.
- **Quoi que ce soit avant 1990.** Les comptes de flux de matières et
  l'indice d'oiseaux communs français démarrent tous deux en 1990. Il n'y
  a pas de contournement : la donnée n'existe pas.
"""
from __future__ import annotations

import io
import urllib.request
from pathlib import Path

import pandas as pd

from modele.donnees.cache import enregistrer
from modele.donnees.sources import eurostat

DELAI = 300
OWID_CO2 = ("https://nyc3.digitaloceanspaces.com/owid-public/data/co2/"
            "owid-co2-data.csv")

# Nomenclature des flux de matières (Eurostat env_ac_mfa, dimension
# `material`). MF1 est renouvelable, les trois autres ne le sont pas.
MATIERES = {
    "MF1": "biomasse",
    "MF2": "minerais métalliques",
    "MF3": "minéraux non métalliques",
    "MF4": "énergies fossiles",
}
NON_RENOUVELABLES = ("MF2", "MF3", "MF4")


def _serie(df: pd.DataFrame) -> pd.Series:
    """Convertit la sortie longue des clients en série indexée par année."""
    s = df.copy()
    s["periode"] = s["periode"].astype(str).str.slice(0, 4).astype(int)
    return (s.set_index("periode")["valeur"].sort_index()
             .dropna().astype(float))


# --------------------------------------------------------------------
# Flux de matières — assiette de l'IRNR
# --------------------------------------------------------------------
def dmc_par_matiere(materiaux: tuple[str, ...] = tuple(MATIERES)) -> pd.DataFrame:
    """
    Consommation intérieure de matières (DMC), en milliers de tonnes.

    **Ce que DMC mesure** : extraction sur le sol national + importations
    − exportations, en poids. Autrement dit : la matière *neuve* que
    l'économie française avale chaque année.

    **Pourquoi le recyclage y est déjà compté positivement** — c'est le
    point qui évite un double comptage. DMC ne compte que la matière
    vierge. Une tonne recyclée en interne n'y figure pas. Un pays qui
    recycle davantage a donc, à service rendu égal, un DMC plus faible.
    *Le recyclage réduit mécaniquement l'indicateur, sans qu'on ait à
    ajouter un bonus.* En ajouter un reviendrait à le compter deux fois.

    Source : Eurostat `env_ac_mfa`. Couverture France : **1990–2024**.
    """
    return pd.DataFrame({
        m: _serie(eurostat("env_ac_mfa", {"geo": "FR", "indic_env": "DMC",
                                          "material": m, "unit": "THS_T"}))
        for m in materiaux})


def rmc_total() -> pd.Series:
    """
    Consommation de matières en **équivalent matières premières** (RMC),
    en milliers de tonnes.

    Différence avec DMC : RMC compte aussi la matière remuée à l'étranger
    pour fabriquer ce que la France importe (le minerai qu'il a fallu
    extraire pour un téléphone, pas seulement le poids du téléphone).
    C'est le bon concept — c'est l'« empreinte matières ».

    Source : Eurostat `env_ac_rme`. Couverture France : **2008–2025
    seulement**. C'est pourquoi l'IRNR est construit sur DMC, avec RMC en
    variante de contrôle sur la fenêtre courte.
    """
    return _serie(eurostat("env_ac_rme", {"geo": "FR", "indic_env": "RMC",
                                          "material": "TOTAL",
                                          "unit": "THS_T"}))


def taux_circulaire() -> pd.Series:
    """
    Taux d'utilisation circulaire de matière, en %.

    Part de la matière consommée qui provient du recyclage plutôt que
    d'une extraction neuve. Sert de **diagnostic** : il montre l'effort de
    recyclage, mais n'est pas ajouté à l'IRNR (cf. `dmc_par_matiere`).

    Source : Eurostat `cei_srm030`. Couverture France : **2010–2024**.
    """
    return _serie(eurostat("cei_srm030", {"geo": "FR", "unit": "PC"}))


# --------------------------------------------------------------------
# Empreinte carbone importations incluses — assiette de l'IEE
# --------------------------------------------------------------------
def co2_empreinte() -> pd.DataFrame:
    """
    Émissions de CO₂ de la France, **territoriales** et **importations
    incluses**, en millions de tonnes, plus la population.

    « Importations incluses » (*consumption-based*) veut dire : on compte
    le CO₂ émis en Chine pour fabriquer ce que les Français achètent, et
    on retire celui émis en France pour ce qui part à l'export. C'est la
    seule notion compatible avec l'exigence de la synthèse (§14.1).

    Elle est calculée par le **Global Carbon Project** à partir d'un
    tableau entrées-sorties multirégional (MRIO Eora) — la même famille
    de méthode qu'EXIOBASE.

    Couverture : territoriales depuis 1802, **importations incluses
    seulement depuis 1990**, et publiées jusqu'en **2022**.

    Colonnes : `territorial`, `empreinte`, `population`.
    """
    with urllib.request.urlopen(OWID_CO2, timeout=DELAI) as r:
        contenu = r.read()
    enregistrer("owid_co2_data.csv", OWID_CO2, contenu,
                "Global Carbon Project / Our World in Data")

    d = pd.read_csv(io.BytesIO(contenu), low_memory=False)
    d = d[d["country"] == "France"]
    out = pd.DataFrame({
        "territorial": d.set_index("year")["co2"],
        "empreinte": d.set_index("year")["consumption_co2"],
        "population": d.set_index("year")["population"],
    }).sort_index()
    return out.loc[out.index >= 1900]


# --------------------------------------------------------------------
# Biodiversité — assiette de l'IBD
# --------------------------------------------------------------------
def oiseaux_agricoles() -> pd.Series:
    """
    Indice des oiseaux communs des milieux agricoles, France, base 2000 = 100.

    ⚠️ **C'est le seul indicateur d'état de la biodiversité française
    disponible en série longue par API.** Il ne mesure qu'un taxon
    (les oiseaux) dans un seul milieu (les terres agricoles). Il ne dit
    rien des sols, des insectes, du milieu marin, ni de la biodiversité
    détruite à l'étranger pour la consommation française.

    ⚠️ **La valeur 2000 = 100 est une rupture, pas une observation.**
    Ses voisines valent 69,5 (1999) et 72,7 (2001) : un bond de +40 % en
    un an suivi d'une chute équivalente n'a aucun sens biologique. C'est
    un artefact de raccordement de série. `serie_biodiversite` la retire
    par défaut.

    Source : Eurostat `env_bio2`. Couverture France : **1990–2021**.
    """
    return _serie(eurostat("env_bio2", {"geo": "FR", "unit": "I00"}))


def serie_biodiversite(retirer_rupture_2000: bool = True) -> pd.Series:
    """L'indice d'oiseaux agricoles, débarrassé de sa rupture de 2000.

    Voir `oiseaux_agricoles` pour la justification du retrait.
    """
    s = oiseaux_agricoles()
    if retirer_rupture_2000 and 2000 in s.index:
        s = s.drop(index=2000)
    return s


# --------------------------------------------------------------------
def population() -> pd.Series:
    """Population moyenne de la France (Eurostat `demo_gind`, 1982–2025)."""
    return _serie(eurostat("demo_gind", {"geo": "FR", "indic_de": "AVG"}))


def tout_recuperer() -> dict[str, pd.DataFrame | pd.Series]:
    """Récupère toutes les séries d'un coup. Utilisé par les scripts."""
    return {
        "dmc": dmc_par_matiere(),
        "rmc": rmc_total(),
        "taux_circulaire": taux_circulaire(),
        "co2": co2_empreinte(),
        "biodiversite": serie_biodiversite(),
        "population": population(),
    }


# --------------------------------------------------------------------
# Empreintes calculées depuis EXIOBASE (importations incluses)
# --------------------------------------------------------------------
CHEMIN_EXIOBASE = (Path(__file__).resolve().parents[2] / "donnees"
                   / "traite" / "empreinte_exiobase_france.csv")


def empreinte_exiobase() -> pd.DataFrame:
    """
    Empreinte de consommation de la France, **importations incluses**,
    calculée depuis EXIOBASE. Série annuelle **1995–2024**.

    Contrairement au DMC d'Eurostat, qui ne compte que le poids des biens
    franchissant la frontière, cette empreinte compte **toute la matière
    remuée à l'étranger** pour fabriquer ce que les Français consomment.

    Colonnes utiles (toutes par habitant) :
    `mat_non_renouv_t_hab`, `co2_t_hab`, `sol_cultures_ha_hab`,
    `sol_paturages_ha_hab`, `sol_foret_ha_hab`.

    Le fichier est produit par `scripts/serie_exiobase.py` (≈ 2 h de
    calcul). Il est versionné dans le dépôt : le recalculer donne le même
    résultat, mais coûte deux heures.
    """
    if not CHEMIN_EXIOBASE.exists():
        raise FileNotFoundError(
            f"{CHEMIN_EXIOBASE} absent — lancer d'abord "
            "`python scripts/serie_exiobase.py` (environ 2 h).")
    return (pd.read_csv(CHEMIN_EXIOBASE)
              .set_index("annee").sort_index().astype(float))
