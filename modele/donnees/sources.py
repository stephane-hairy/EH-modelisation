"""
Clients de récupération des données, une fonction par institut.

Choix technique : on n'utilise **pas** `pandasdmx`. Sa version 1.10 échoue
à parser les structures de l'INSEE (`KeyError: 'TIME_PERIOD'`, la
dimension temporelle étant déclarée séparément). Les trois formats dont
nous avons besoin sont simples ; trois petits lecteurs valent mieux
qu'une grosse dépendance fragile :

- **INSEE**  : SDMX-ML « StructureSpecificData » — les valeurs sont des
  attributs XML.
- **Eurostat** : JSON-stat 2.0.
- **BCE**    : CSV (`format=csvdata`).

Toutes les fonctions renvoient un `pandas.DataFrame` en format long :
une ligne = une observation, colonnes `periode`, `valeur`, + les
dimensions.
"""
from __future__ import annotations

import io
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import pandas as pd

from modele.donnees.cache import enregistrer

DELAI = 180  # secondes
INSEE = "https://bdm.insee.fr/series/sdmx"
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
BCE = "https://data-api.ecb.europa.eu/service/data"


def _telecharger(url: str, nom: str, source: str) -> bytes:
    with urllib.request.urlopen(url, timeout=DELAI) as r:
        contenu = r.read()
    enregistrer(nom, url, contenu, source)
    return contenu


# --------------------------------------------------------------------
# INSEE
# --------------------------------------------------------------------
def insee(flux: str, cle: dict[str, str], dimensions: list[str],
          nom: str | None = None) -> pd.DataFrame:
    """
    Récupère une série des comptes nationaux INSEE.

    `dimensions` est l'ordre exact des dimensions du flux (voir
    `insee_dimensions`). `cle` ne fixe que celles qu'on veut contraindre ;
    les autres sont laissées libres.

    Exemple — PIB annuel, 1949 à aujourd'hui :
        insee("CNA-2020-PIB", {"FREQ": "A", "OPERATION": "PIB"},
              insee_dimensions("CNA-2020-PIB"))

    ⚠️ Le code pays de l'INSEE est `FE` (France entière), **pas** `FR`.
    """
    chaine = ".".join(cle.get(d, "") for d in dimensions)
    url = f"{INSEE}/data/{flux}/{chaine}"
    nom = nom or f"insee_{flux}_{chaine.replace('.', '-')}.xml"
    return _lire_sdmx_ml(_telecharger(url, nom, "INSEE"))


def insee_dimensions(flux: str) -> list[str]:
    """Ordre des dimensions d'un flux INSEE (hors dimension temporelle)."""
    url = f"{INSEE}/datastructure/FR1/{flux}"
    with urllib.request.urlopen(url, timeout=DELAI) as r:
        racine = ET.fromstring(r.read())
    ns = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}"
    # Le tag <str:Dimension> sert aussi de simple référence dans les
    # relations d'attributs : on ne garde que les vraies dimensions,
    # celles qui portent un `id` et une `position`.
    dims = [d for d in racine.iter(f"{ns}Dimension")
            if d.get("id") and d.get("position")]
    return [d.get("id") for d in sorted(dims, key=lambda e: int(e.get("position")))]


def _lire_sdmx_ml(contenu: bytes) -> pd.DataFrame:
    """Lit un SDMX-ML StructureSpecificData (INSEE)."""
    racine = ET.fromstring(contenu)
    lignes = []
    for serie in racine.iter():
        if not serie.tag.endswith("Series"):
            continue
        meta = dict(serie.attrib)
        for obs in serie:
            if not obs.tag.endswith("Obs"):
                continue
            valeur = obs.get("OBS_VALUE")
            lignes.append(
                {**meta,
                 "periode": obs.get("TIME_PERIOD"),
                 "valeur": pd.to_numeric(valeur, errors="coerce")}
            )
    return pd.DataFrame(lignes)


# --------------------------------------------------------------------
# Eurostat
# --------------------------------------------------------------------
def eurostat(dataset: str, filtres: dict[str, str],
             nom: str | None = None) -> pd.DataFrame:
    """
    Récupère un jeu Eurostat au format JSON-stat 2.0.

    Exemple — flux de matières en France :
        eurostat("env_ac_mfa", {"geo": "FR", "indic_env": "DMC",
                                "material": "TOTAL", "unit": "THS_T"})
    """
    params = {**filtres, "format": "JSON", "lang": "en"}
    url = f"{EUROSTAT}/{dataset}?{urllib.parse.urlencode(params)}"
    nom = nom or f"eurostat_{dataset}_{'-'.join(sorted(filtres.values()))}.json"
    return _lire_jsonstat(_telecharger(url, nom, "Eurostat"))


def _lire_jsonstat(contenu: bytes) -> pd.DataFrame:
    """
    Lit un JSON-stat 2.0.

    `value` est un dictionnaire indexé sur l'aplatissement du produit de
    toutes les dimensions, dans l'ordre donné par `id`. On décode cet
    indice en coordonnées pour retrouver chaque dimension — y compris
    quand `time` n'est pas la dernière.
    """
    d = json.loads(contenu)
    noms = d["id"]
    tailles = d["size"]
    etiquettes = {
        n: {v: k for k, v in d["dimension"][n]["category"]["index"].items()}
        for n in noms
        if isinstance(d["dimension"][n]["category"].get("index"), dict)
    }
    lignes = []
    for indice, valeur in d.get("value", {}).items():
        reste = int(indice)
        coords = {}
        for n, t in zip(reversed(noms), reversed(tailles)):
            reste, position = divmod(reste, t)
            coords[n] = etiquettes.get(n, {}).get(position, position)
        coords["valeur"] = valeur
        lignes.append(coords)
    df = pd.DataFrame(lignes).rename(columns={"time": "periode"})
    return df.sort_values("periode").reset_index(drop=True)


# --------------------------------------------------------------------
# BCE
# --------------------------------------------------------------------
def bce(flux: str, cle: str, nom: str | None = None) -> pd.DataFrame:
    """
    Récupère une série de la BCE (SDMX, sortie CSV).

    Exemple — comptes financiers trimestriels des ménages français :
        bce("QSA", "Q.N.FR.W0.S1M.S1.N.A.F.F2.T._Z.XDC._T.S.V.N._T")
    """
    url = f"{BCE}/{flux}/{cle}?format=csvdata&detail=dataonly"
    nom = nom or f"bce_{flux}_{cle.replace('.', '-')}.csv"
    contenu = _telecharger(url, nom, "BCE")
    df = pd.read_csv(io.BytesIO(contenu))
    return df.rename(columns={"TIME_PERIOD": "periode", "OBS_VALUE": "valeur"})
