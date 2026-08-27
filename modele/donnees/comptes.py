"""
Comptes nationaux français par secteur — assiettes du dividende
d'entreprise.

Une fonction par grandeur, en euros courants, indexée par année.
Source unique : Eurostat `nasa_10_nf_tr` (comptes non financiers annuels
par secteur), couverture France **1971–2024** — donc largement suffisante
pour toute la fenêtre du projet.

Secteurs utilisés :
  `S11` sociétés non financières · `S12` sociétés financières ·
  `S14` ménages (dont entrepreneurs individuels) · `S1` économie totale.
"""
from __future__ import annotations

import pandas as pd

from modele.donnees.sources import eurostat

MEUR = 1e6   # les séries Eurostat sont en millions d'euros


def _grandeur(secteur: str, na_item: str, direct: str = "RECV") -> pd.Series:
    d = eurostat("nasa_10_nf_tr", {"geo": "FR", "sector": secteur,
                                   "na_item": na_item, "direct": direct,
                                   "unit": "CP_MEUR"})
    d["periode"] = d["periode"].astype(str).str.slice(0, 4).astype(int)
    return (d.set_index("periode")["valeur"].sort_index()
             .dropna().astype(float) * MEUR)


def production(secteur: str = "S11") -> pd.Series:
    """Production (P1) du secteur, en euros courants.

    En clair : tout ce que le secteur a vendu, y compris ce qu'il a acheté
    à ses fournisseurs pour le produire. C'est l'assiette la plus proche
    du « produit d'exploitation » de la synthèse — avec le défaut de
    double comptage décrit dans `docs/05-dent.md` §5.
    """
    return _grandeur(secteur, "P1")


def valeur_ajoutee(secteur: str = "S11") -> pd.Series:
    """Valeur ajoutée brute (B1G) du secteur, en euros courants.

    En clair : la production **moins** ce qui a été acheté aux
    fournisseurs. C'est ce que le secteur a réellement ajouté. Additive
    entre entreprises : insensible aux fusions et aux scissions.
    """
    return _grandeur(secteur, "B1G")


def assiettes_dent() -> pd.DataFrame:
    """Les deux assiettes possibles du dividende d'entreprise, en euros.

    Colonnes : `production_SNF`, `va_SNF`, `production_SF`, `va_SF`.
    Le périmètre par défaut recommandé (`docs/05-dent.md` §4) est SNF
    seules ; les sociétés financières sont fournies pour la sensibilité.
    """
    return pd.DataFrame({
        "production_SNF": production("S11"),
        "va_SNF": valeur_ajoutee("S11"),
        "production_SF": production("S12"),
        "va_SF": valeur_ajoutee("S12"),
    })
