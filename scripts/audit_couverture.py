"""
Audit de couverture des données : jusqu'où peut-on vraiment remonter ?

Cette question n'est pas cosmétique. Elle décide de deux choix de
conception du modèle :
  - la **période de départ** (1978 ? 1995 ?) ;
  - la **fréquence** (annuelle ? trimestrielle ? mensuelle ?).

Le script interroge les sources et écrit `docs/annexes/couverture-donnees.md`.

Usage : python3 scripts/audit_couverture.py
"""
from __future__ import annotations

import sys
import traceback
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modele.donnees import bce, eurostat, insee, insee_dimensions  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
SORTIE = RACINE / "docs" / "annexes" / "couverture-donnees.md"


def _insee(flux, cle):
    df = insee(flux, cle, insee_dimensions(flux))
    return df["periode"]


CONTROLES = [
    # (bloc, libellé, fréquence, fonction)
    ("Réel", "PIB, euros courants (INSEE CNA-2020-PIB)", "annuelle",
     lambda: _insee("CNA-2020-PIB", {"FREQ": "A", "OPERATION": "PIB",
                                     "UNIT_MEASURE": "EUROS_COURANTS",
                                     "CNA_PRODUIT": "NNTOTAL"})),
    ("Réel", "PIB (Eurostat nama_10_gdp)", "annuelle",
     lambda: eurostat("nama_10_gdp", {"geo": "FR", "na_item": "B1GQ",
                                      "unit": "CP_MEUR"})["periode"]),
    ("Financier", "Comptes financiers, SNF crédits F4 (INSEE CNA-2014-TOF)", "annuelle",
     lambda: _insee("CNA-2014-TOF", {"FREQ": "A", "SECT-INST": "S11",
                                     "OPERATION": "F4"})),
    ("Financier", "Comptes financiers ménages, dépôts F2 (BCE QSA)", "trimestrielle",
     lambda: bce("QSA", "Q.N.FR.W0.S1M.S1.N.A.F.F2.T._Z.XDC._T.S.V.N._T")["periode"]),
    ("Monétaire", "Crédits des IFM au secteur privé, France (BCE BSI)", "mensuelle",
     lambda: bce("BSI", "M.FR.N.A.A20.A.1.U2.2240.Z01.E")["periode"]),
    ("Écologie", "Émissions de GES (Eurostat env_ac_ainah_r2)", "annuelle",
     lambda: eurostat("env_ac_ainah_r2", {"geo": "FR", "airpol": "GHG",
                                          "nace_r2": "TOTAL", "unit": "T"})["periode"]),
    ("Écologie", "Inventaire GES national (Eurostat env_air_gge)", "annuelle",
     lambda: eurostat("env_air_gge", {"geo": "FR", "airpol": "GHG",
                                      "src_crf": "TOTX4_MEMO",
                                      "unit": "MIO_T"})["periode"]),
    ("Écologie", "Consommation intérieure de matières (Eurostat env_ac_mfa)", "annuelle",
     lambda: eurostat("env_ac_mfa", {"geo": "FR", "indic_env": "DMC",
                                     "material": "TOTAL", "unit": "THS_T"})["periode"]),
]


def executer() -> list[dict]:
    resultats = []
    for bloc, libelle, freq, fn in CONTROLES:
        try:
            periodes = sorted(str(p) for p in fn().dropna().unique())
            resultats.append({"bloc": bloc, "libelle": libelle, "freq": freq,
                              "debut": periodes[0], "fin": periodes[-1],
                              "n": len(periodes), "erreur": None})
            print(f"OK   {libelle[:58]:<58} {periodes[0]} → {periodes[-1]}")
        except Exception as exc:  # noqa: BLE001
            resultats.append({"bloc": bloc, "libelle": libelle, "freq": freq,
                              "debut": None, "fin": None, "n": 0,
                              "erreur": f"{type(exc).__name__}: {exc}"})
            print(f"ÉCHEC {libelle[:58]:<58} {type(exc).__name__}")
            traceback.print_exc(limit=1)
    return resultats


def rediger(resultats: list[dict]) -> str:
    lignes = [
        "# Couverture des données — jusqu'où peut-on remonter ?",
        "",
        f"> Généré par `scripts/audit_couverture.py` le {date.today().isoformat()}.",
        "> Ne pas modifier à la main : relancer le script.",
        "",
        "| Bloc | Série | Fréquence | Début | Fin | Obs. |",
        "|---|---|---|---|---|---|",
    ]
    for r in resultats:
        if r["erreur"]:
            lignes.append(f"| {r['bloc']} | {r['libelle']} | {r['freq']} "
                          f"| — | — | ⚠️ {r['erreur'][:60]} |")
        else:
            lignes.append(f"| {r['bloc']} | {r['libelle']} | {r['freq']} "
                          f"| **{r['debut']}** | {r['fin']} | {r['n']} |")
    lignes += [
        "",
        "## Ce que ça implique",
        "",
        "- L'**économie réelle** (PIB et agrégats) remonte à **1949**.",
        "- Les **comptes financiers par secteur** — qui détient quoi, la",
        "  colonne vertébrale d'un modèle Stock-Flux Cohérent — ne commencent",
        "  qu'en **1995** (annuel INSEE) ou **1998-Q4** (trimestriel BCE).",
        "  C'est la contrainte qui décide de la période de départ.",
        "- L'**écologie** : matières depuis 1990, inventaire national des gaz à",
        "  effet de serre depuis 1990, mais les *comptes d'émissions par",
        "  branche* (ceux qu'il faut pour relier émissions et production)",
        "  seulement depuis 2008.",
        "- Le **mensuel** n'existe que pour la monnaie, le crédit et les prix.",
        "  Il n'existe aucune donnée mensuelle de PIB, d'investissement ou de",
        "  patrimoine sectoriel : un modèle mensuel complet est impossible à",
        "  caler sur données françaises.",
    ]
    return "\n".join(lignes) + "\n"


if __name__ == "__main__":
    res = executer()
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(rediger(res), encoding="utf-8")
    print(f"\n→ {SORTIE.relative_to(RACINE)}")
