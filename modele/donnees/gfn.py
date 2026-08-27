"""
Empreinte écologique et biocapacité — comptes du Global Footprint Network.

**Ce que c'est.** Le GFN convertit toutes les pressions écologiques d'un
pays en une seule unité : l'**hectare global** (gha), c'est-à-dire la
surface de nature moyennement productive qu'il faudrait pour fournir ce
que le pays consomme et absorber ce qu'il rejette. On compare ensuite
cette empreinte à la **biocapacité** : la surface productive dont le pays
dispose réellement. C'est exactement la notion demandée par la synthèse
EH (§14.1), et l'empreinte de *consommation* inclut les importations.

⚠️ **Ce que cette source donne — et ne donne pas.**

- ✅ Elle est **officielle** : c'est le *National Footprint Accounts 2017
  Public Data Package* du GFN, diffusé sous licence Creative Commons avec
  son guide méthodologique.
- ❌ Elle ne contient **qu'une seule année, 2013**. Ce n'est pas une série
  temporelle. Les comptes annuels 1961→ne sont pas librement accessibles :
  l'API du GFN exige une clé nominative (403 sans elle) et les éditions
  récentes sont sous copyright, ce que le GFN indique explicitement.
- ⚠️ Le fichier est servi depuis un **miroir CKAN** (OD Mekong Datahub),
  parce que le portail du GFN ne l'expose pas librement. Le *contenu* est
  bien le paquet officiel ; l'*hébergeur* ne l'est pas. Empreinte SHA-256
  enregistrée au manifeste, comme toute autre source.

À quoi ça sert malgré une seule année : à **calibrer et à valider**
l'approximation carbone qui sert d'IEE (fiche EQ-EXEC-002). Un point
d'ancrage vrai vaut mieux qu'aucun — cf. `scripts/valider_iee_gfn.py`.
"""
from __future__ import annotations

import io
import urllib.request

import pandas as pd

from modele.donnees.cache import enregistrer

DELAI = 600
ANNEE = 2013
"""Seule année couverte par le paquet public 2017."""

URL = ("https://data.opendevelopmentmekong.net/dataset/"
       "2a9c3cf0-1855-4b8c-9735-d8998c5b9bf7/resource/"
       "f825f945-6809-41a8-8084-670ec177f209/download/"
       "nfa-2017-public-data-package_v1_3.xlsx")

FEUILLE = "Country Results 2017 Ed (2013)"
LIGNE_GROUPES = 4      # « Ecological Footprint of Consumption », etc.
LIGNE_ENTETES = 5      # « Carbon Footprint », « Total biocapacity », etc.
PREMIERE_DONNEE = 20   # les lignes 6–19 sont des agrégats régionaux


def _telecharger() -> bytes:
    with urllib.request.urlopen(URL, timeout=DELAI) as r:
        contenu = r.read()
    enregistrer("gfn_nfa_2017_public_data_package.xlsx", URL, contenu,
                "Global Footprint Network (miroir OD Mekong Datahub)")
    return contenu


def comptes_pays() -> pd.DataFrame:
    """Le tableau complet du paquet public, un pays par ligne.

    Les colonnes sont nommées « groupe | grandeur », par exemple
    `Ecological Footprint of Consumption (global hectares per person) |
    Carbon Footprint`. Toutes les valeurs d'empreinte et de biocapacité
    sont en **hectares globaux par personne**.
    """
    d = pd.read_excel(io.BytesIO(_telecharger()), sheet_name=FEUILLE,
                      header=None)
    groupes = d.iloc[LIGNE_GROUPES].ffill()
    entetes = d.iloc[LIGNE_ENTETES]
    colonnes = [f"{str(g).strip()} | {str(h).strip()}"
                for g, h in zip(groupes, entetes)]
    t = d.iloc[PREMIERE_DONNEE:].copy()
    t.columns = colonnes
    t = t.rename(columns={colonnes[0]: "pays"})
    t["pays"] = t["pays"].astype(str).str.strip()
    return t[t["pays"].ne("nan") & t["pays"].ne("")].reset_index(drop=True)


def _nombre(x) -> float:
    """Le GFN note les données manquantes « -- »."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def empreinte_et_biocapacite(pays: str = "France") -> dict[str, float]:
    """
    Empreinte écologique et biocapacité d'un pays, en gha par personne.

    Renvoie notamment :

    - `empreinte_consommation` — l'empreinte **importations incluses**,
      c'est-à-dire ce que demande la synthèse §14.1 ;
    - `empreinte_carbone` — sa composante carbone, celle que notre
      approximation mesure ;
    - `part_carbone` — quelle fraction de l'empreinte totale le carbone
      représente. C'est la mesure directe de ce que l'approximation rate ;
    - `biocapacite` — la surface productive réellement disponible ;
    - `ratio` — empreinte ÷ biocapacité. **C'est le vrai « x » de l'IEE** :
      1 signifie « le pays vit exactement sur ses moyens ».
    """
    t = comptes_pays()
    ligne = t[t["pays"] == pays]
    if ligne.empty:
        raise ValueError(f"pays « {pays} » absent des comptes GFN")
    r = ligne.iloc[0]

    def col(groupe: str, champ: str) -> float:
        return _nombre(r[f"{groupe} | {champ}"])

    conso = "Ecological Footprint of Consumption (global hectares per person)"
    bio = "Biocapacity (global hectares per person)"

    empreinte = col(conso, "Total Ecological Footprint (Consumption)")
    carbone = col(conso, "Carbon Footprint")
    biocapacite = col(bio, "Total biocapacity")

    return {
        "annee": float(ANNEE),
        "population_millions": col("Country Results", "Population (millions)"),
        "empreinte_consommation": empreinte,
        "empreinte_carbone": carbone,
        "empreinte_cropland": col(conso, "Cropland Footprint"),
        "empreinte_paturage": col(conso, "Grazing Footprint"),
        "empreinte_foret": col(conso, "Forest Product Footprint"),
        "empreinte_peche": col(conso, "Fish Footprint"),
        "empreinte_bati": col(conso, "Built up land"),
        "part_carbone": carbone / empreinte,
        "biocapacite": biocapacite,
        "deficit": col(bio, "Biocapacity (Deficit) or Reserve"),
        "ratio": empreinte / biocapacite,
    }


def seuil_carbone_equivalent(co2_par_habitant: float,
                             pays: str = "France") -> float:
    """
    Le seuil carbone qui ferait coïncider notre approximation avec le GFN.

    **L'idée, en une phrase** : on ne connaît la vraie empreinte écologique
    que pour 2013 ; on s'en sert pour régler le curseur de notre indicateur
    de remplacement, au lieu de le poser au jugé.

    Notre IEE vaut `mapping(CO₂ par habitant / seuil)`. Pour que le rapport
    de pression égale celui du GFN cette année-là, il faut

        seuil = CO₂ par habitant ÷ (empreinte GFN / biocapacité GFN)

    `co2_par_habitant` est l'empreinte carbone française de 2013, en
    tonnes par personne (source : Global Carbon Project).

    ⚠️ Ce que ça reste : un **choix normatif** (catégorie D), pas une
    mesure. Il déplace la référence — d'un budget climatique mondial
    partagé par tête vers la biocapacité propre du pays. Les deux sont
    défendables et ne disent pas la même chose.
    """
    return co2_par_habitant / empreinte_et_biocapacite(pays)["ratio"]
