"""
Abondance moyenne des espèces (AMAE) — OCDE, Perspectives 2050.

**Ce que c'est.** L'AMAE — *Mean Species Abundance*, MSA — mesure la
population des espèces **par rapport à un écosystème intact**. L'OCDE
l'écrit noir sur blanc : *« une AMAE de 100 % correspond à l'absence de
perturbation »*.

**Pourquoi c'est intéressant ici.** C'est exactement la construction qui
manque à notre IBD. Notre indicateur de biodiversité compare la France
d'aujourd'hui à **la France de 1990** — un état passé, déjà dégradé, qui
n'est pas un seuil de soutenabilité. L'AMAE, elle, compare à **l'état
d'origine**. C'est un vrai référentiel.

Source : OCDE (2012), *Perspectives de l'environnement de l'OCDE à
l'horizon 2050*, chapitre 4. Données issues du modèle **GLOBIO**
(Alkemade *et al.*, 2009) couplé au cadre IMAGE, récupérées par les
StatLinks du rapport.

⚠️ **TROIS RÉSERVES, à lire avant tout usage.**

1. **L'AMAE n'est PAS le BII.** Ce sont des cousins conceptuels — tous
   deux en pourcentage de l'état intact — mais pas des synonymes. La
   **frontière planétaire de 90 %** a été définie sur le *Biodiversity
   Intactness Index* (Steffen *et al.*, 2015), **pas** sur l'AMAE. La
   transférer telle quelle serait une erreur de catégorie.
2. **Pas de France.** L'OCDE ne descend qu'à l'échelle « Europe ».
3. **Ce sont des PROJECTIONS de modèle**, pas des observations, et sur
   quatre points seulement (2010, 2020, 2030, 2050). Le BII, lui, donne
   une série 1970–2050 par pays.

⇒ Cette source **documente le concept** et donne un ordre de grandeur
européen. Elle **ne remplace pas** le BII pour construire l'IBD.
"""
from __future__ import annotations

import io
import urllib.request

import pandas as pd

from modele.donnees.cache import enregistrer

DELAI = 300
STATLINK = "https://dx.doi.org/10.1787/{identifiant}"

# StatLinks du chapitre 4 des Perspectives 2050.
AMAE_PAR_REGION = "888932594294"    # graphique 4.9 — terrestre, par région
AMAE_PAR_BIOME = "888932594256"     # graphique 4.3 — mondiale, par biome


def _tableau(identifiant: str, nom_cache: str) -> pd.DataFrame:
    """Récupère un StatLink OCDE (classeur Excel) et le met en cache."""
    url = STATLINK.format(identifiant=identifiant)
    with urllib.request.urlopen(url, timeout=DELAI) as reponse:
        contenu = reponse.read()
    enregistrer(nom_cache, url, contenu,
                "OCDE, Perspectives de l'environnement à l'horizon 2050")
    return pd.read_excel(io.BytesIO(contenu), sheet_name="Data", header=None)


def _entete_annees(d: pd.DataFrame) -> int:
    """Trouve la ligne d'en-tête : celle qui contient des années."""
    for i in range(len(d)):
        valeurs = [v for v in d.iloc[i] if isinstance(v, (int, float))
                   and not pd.isna(v) and 1900 < v < 2100]
        if len(valeurs) >= 2:
            return i
    raise ValueError("aucune ligne d'en-tête avec des années")


def _lire(d: pd.DataFrame) -> pd.DataFrame:
    """Extrait « libellé × années » d'un classeur StatLink."""
    i = _entete_annees(d)
    annees = {j: int(v) for j, v in enumerate(d.iloc[i])
              if isinstance(v, (int, float)) and not pd.isna(v)
              and 1900 < v < 2100}
    lignes = {}
    for k in range(i + 1, len(d)):
        libelles = [v for v in d.iloc[k][:2]
                    if isinstance(v, str) and v.strip()]
        if not libelles:
            continue
        valeurs = {an: d.iloc[k, j] for j, an in annees.items()}
        if all(isinstance(v, (int, float)) and not pd.isna(v)
               for v in valeurs.values()):
            lignes[libelles[-1].strip()] = valeurs
    return pd.DataFrame(lignes).T.sort_index(axis=1)


def amae_par_region() -> pd.DataFrame:
    """
    AMAE **terrestre** par région du monde, en part de l'état intact.

    Colonnes : 2010, 2020, 2030, 2050. Valeurs entre 0 et 1.

    Chiffre marquant : **l'Europe est à 0,384 en 2010** — il ne reste que
    38 % de l'abondance d'espèces d'un écosystème intact. C'est la région
    la plus dégradée de l'OCDE, et la projection descend à 0,293 en 2050.
    """
    return _lire(_tableau(AMAE_PAR_REGION, "ocde_amae_par_region.xls"))


def amae_par_biome() -> pd.DataFrame:
    """
    AMAE **mondiale** par biome, en pourcentage de l'état intact.

    Colonnes : 1970 et 2010. Valeurs entre 0 et 100.

    Le biome qui concerne la France est « Forêts tempérées » : il passe de
    **49,7 % en 1970 à 37,3 % en 2010**. Autrement dit, dès 1970 les
    forêts tempérées avaient déjà perdu la moitié de leur abondance
    d'origine — ce qui montre à quel point prendre une année récente pour
    référence rend un indicateur de biodiversité trop optimiste.
    """
    return _lire(_tableau(AMAE_PAR_BIOME, "ocde_amae_par_biome.xls"))
