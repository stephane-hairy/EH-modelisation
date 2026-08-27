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

---

**Deux étalons, et le choix n'est pas neutre.** Le GFN publie deux façons
de rapporter l'empreinte à un seuil, et elles ne disent pas du tout la
même chose :

- **« nombre de Terres »** — empreinte ÷ biocapacité **mondiale** par
  humain. *Combien faudrait-il de planètes si tout le monde vivait
  comme ce pays ?* Note le **comportement**.
- **« nombre de pays »** — empreinte ÷ biocapacité **du pays**. *Ce pays
  vit-il sur ses propres moyens ?* Note la **géographie**.

L'écart est spectaculaire. Chiffres 2013, sous mapping exponentiel :

| pays | empreinte | IEE, étalon mondial | IEE, étalon territorial |
|---|---:|---:|---:|
| Bangladesh | 0,75 | **1,47** | 0,50 |
| France | 5,06 | 0,26 | 0,60 |
| Australie | 8,80 | **0,06** | **1,35** |

Sous l'étalon territorial, **l'Australie — qui consomme 74 % de nature de
plus que la France — recevrait 2,3 fois plus de monnaie**, parce qu'elle
a de l'espace. Et le **Bangladesh, qui consomme 7 fois moins que la
France, serait moins bien noté qu'elle**, parce qu'il est dense.

Pour une théorie mondiale qui prétend récompenser la vertu écologique,
c'est une incitation perverse de premier ordre. **Décision D13 : l'étalon
retenu est le mondial.**
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
    - `biocapacite_mondiale` — la biocapacité moyenne disponible **par
      humain sur Terre** ;
    - `ratio_mondial` — empreinte ÷ biocapacité mondiale. C'est le
      « nombre de Terres » : *combien faudrait-il de planètes si tout le
      monde vivait comme ce pays ?* **C'est l'étalon retenu (décision
      D13)** ;
    - `ratio_territorial` — empreinte ÷ biocapacité du pays. C'est le
      « nombre de pays » : *ce pays vit-il sur ses propres moyens ?*
      Fourni pour la sensibilité, **pas retenu** — il note la géographie
      plutôt que le comportement (voir la note du module).
    - `ratio` — alias de `ratio_mondial`, l'étalon retenu.
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
    ratio_mondial = col(bio, "Number of Earths required")
    ratio_territorial = col(bio, "Number of Countries required")
    # Le GFN ne publie pas la biocapacité mondiale par tête directement ;
    # elle se déduit exactement : empreinte / nombre de Terres.
    biocapacite_mondiale = empreinte / ratio_mondial

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
        "biocapacite_mondiale": biocapacite_mondiale,
        "deficit": col(bio, "Biocapacity (Deficit) or Reserve"),
        "ratio_mondial": ratio_mondial,
        "ratio_territorial": ratio_territorial,
        "ratio": ratio_mondial,      # étalon retenu — décision D13
    }


def seuil_carbone_equivalent(co2_par_habitant: float,
                             pays: str = "France",
                             etalon: str = "mondial") -> float:
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

    Par défaut on cale sur l'étalon **mondial** (décision D13) : le
    « nombre de Terres ». Passer `etalon="territorial"` donne l'autre
    référence, pour la sensibilité.

    ⚠️ Ce que ça reste : un **choix normatif** (catégorie D), pas une
    mesure.
    """
    cle = "ratio_mondial" if etalon == "mondial" else "ratio_territorial"
    return co2_par_habitant / empreinte_et_biocapacite(pays)[cle]
