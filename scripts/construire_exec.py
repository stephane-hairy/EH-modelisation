"""
Construit les indicateurs EXEC de la France, année par année.

Produit `donnees/traite/exec_france.csv` et affiche la couverture réelle
des données — y compris ce qui manque.

Usage : python scripts/construire_exec.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from modele.exec.indicateurs import (MAPPINGS, SEUIL_CO2_T_HAB,
                                     SEUIL_MATIERE_T_HAB)
from modele.exec.serie_france import DEBUT_DEMANDE, construire

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "donnees" / "traite" / "exec_france.csv"

def fr(x: float, dec: int = 2) -> str:
    return f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")


def titre(t: str) -> None:
    print(f"\n{'=' * 74}\n{t}\n{'=' * 74}")


def rapport_couverture(couverture: dict) -> None:
    titre("CE QUE LES DONNÉES PERMETTENT RÉELLEMENT")
    print(f"""
Le cadrage (décision D5) demande **{DEBUT_DEMANDE}–2023**. Voici ce qui existe.
""")
    print(f"  {'série':<22} {'début':>7} {'fin':>7} {'années':>8}   source")
    sources = {
        "DMC (matières)": "Eurostat env_ac_mfa",
        "CO₂ empreinte": "Global Carbon Project (MRIO Eora)",
        "Oiseaux agricoles": "Eurostat env_bio2",
        "Taux circulaire": "Eurostat cei_srm030",
    }
    debuts = []
    fins = []
    for nom, idx in couverture.items():
        print(f"  {nom:<22} {idx.min():>7} {idx.max():>7} {len(idx):>8}   "
              f"{sources[nom]}")
        debuts.append(idx.min())
        fins.append(idx.max())

    debut, fin = max(debuts[:3]), min(fins[:3])
    print(f"""
  ⇒ fenêtre où les TROIS indicateurs existent : **{debut}–{fin}**.

MANQUE : {DEBUT_DEMANDE}–{debut - 1}, soit {debut - DEBUT_DEMANDE} ans, et {fin + 1}–2023, soit {2023 - fin} ans.

Ce trou n'est pas contournable, et il ne s'agit pas d'un défaut de notre
collecte :

  • Les comptes de flux de matières français (Eurostat, SDES) **commencent
    en 1990**. Rien n'existe avant à l'échelle nationale harmonisée.
  • L'indice d'oiseaux communs français **commence en 1989-1990** : c'est
    l'année de lancement du protocole STOC.
  • Les émissions importations incluses **commencent en 1990** : avant,
    les tableaux entrées-sorties mondiaux nécessaires n'existent pas.

Conformément à la RÈGLE N°3, on documente le trou au lieu de le combler.
Reconstituer 1978–1989 exigerait d'inventer douze années de données pour
les trois indicateurs à la fois : ce ne serait pas un modèle, ce serait
un dessin.

Une seule série remonte avant 1990 : les émissions de CO₂ **territoriales**
(depuis 1802). Elles excluent les importations, donc violent l'exigence
§14.1 de la synthèse. Elles sont fournies dans le CSV à titre de
diagnostic, jamais comme substitut à l'empreinte.
""")


def rapport_indicateurs(table: pd.DataFrame) -> None:
    titre("LES INDICATEURS EXEC DE LA FRANCE")
    print(f"""
Seuils de soutenabilité retenus (choix normatifs, catégorie D) :
  • CO₂      : {fr(SEUIL_CO2_T_HAB)} t/hab/an — budget 1,5 °C du GIEC (AR6),
               partagé également par tête sur 30 ans
  • matières : {fr(SEUIL_MATIERE_T_HAB, 1)} t/hab/an de matière non renouvelable
               — corridor de Bringezu (2015)
  • biodiv.  : état de 1990 pris pour référence (⚠️ voir limites)

Mapping : exponentiel (I = 2^(1−x)) — chaque unité de dépassement divise
la note par deux.
""")
    cols = ["matiere_nr_t_hab", "ratio_IRNR", "IRNR",
            "co2_empreinte_t_hab", "ratio_IEE", "IEE",
            "oiseaux_agricoles", "ratio_IBD", "IBD", "IED", "IED_sans_IBD"]
    d = table[cols].dropna(subset=["IRNR", "IEE"])
    print(f"  {'année':>5} {'mat.':>6} {'x':>5} {'IRNR':>6} │ "
          f"{'CO₂':>5} {'x':>5} {'IEE':>6} │ {'ois.':>6} {'x':>5} {'IBD':>6} │ "
          f"{'IED':>6} {'IED s/IBD':>10}")
    for an in d.index:
        r = d.loc[an]
        def v(c, dec=2):
            return "  —  " if pd.isna(r[c]) else fr(r[c], dec)
        print(f"  {an:>5} {v('matiere_nr_t_hab', 1):>6} {v('ratio_IRNR'):>5} "
              f"{v('IRNR'):>6} │ {v('co2_empreinte_t_hab', 1):>5} "
              f"{v('ratio_IEE'):>5} {v('IEE'):>6} │ "
              f"{v('oiseaux_agricoles', 0):>6} {v('ratio_IBD'):>5} "
              f"{v('IBD'):>6} │ {v('IED'):>6} {v('IED_sans_IBD'):>10}")


def rapport_mappings() -> None:
    titre("LE MAPPING VERS [0 ; 2] — LE CHOIX QUI DÉCIDE DE TOUT")
    print("""
À seuils identiques, trois mappings raisonnables donnent des résultats
radicalement différents. Ce n'est pas un réglage fin : c'est LA décision.
""")
    lignes = []
    for nom in MAPPINGS:
        table, _ = construire(mapping=nom)
        # dernière année où les TROIS indicateurs existent : c'est la
        # seule où l'IED est défini (le calcul est strict, cf. EQ-EXEC-005)
        d = table.dropna(subset=["IRNR", "IEE", "IBD"])
        derniere = d.index.max()
        lignes.append((nom, d.loc[derniere], derniere))

    print(f"  {'mapping':<14} {'formule':<20} {'IRNR':>7} {'IEE':>7} "
          f"{'IBD':>7} {'IED':>7}")
    formules = {"lineaire": "I = 2 − x (écrêté)",
                "hyperbolique": "I = 2 / (1 + x)",
                "exponentiel": "I = 2^(1−x)"}
    for nom, r, an in lignes:
        def v(c):
            return "  —  " if pd.isna(r[c]) else fr(r[c])
        print(f"  {nom:<14} {formules[nom]:<20} {v('IRNR'):>7} {v('IEE'):>7} "
              f"{v('IBD'):>7} {v('IED'):>7}")
    print(f"""
  (année {lignes[0][2]}, la dernière où les trois indicateurs existent —
   l'empreinte carbone est publiée avec deux ans de retard et l'indice
   d'oiseaux s'arrête en 2021)

Lecture :

  • **linéaire** : l'empreinte carbone française vaut ~2,9 fois le seuil,
    donc IEE = 0. La moyenne géométrique s'annule → **IED = 0** → la
    France ne créerait **plus aucune monnaie**. Ce n'est pas une erreur
    de calcul, c'est ce que ce choix normatif affirme.
    La pente au point d'équilibre vaut −1,00 contre −0,50 (hyperbolique)
    et −0,69 (exponentiel) : c'est le gain du régulateur EH, donc
    l'entrée directe de l'analyse de stabilité (jalon P5).
  • **hyperbolique** : le plus indulgent, l'IED reste dans une plage
    exploitable.
  • **exponentiel** : intermédiaire, et le seul dont la règle s'énonce en
    une phrase (« dépasser d'une unité divise la note par deux »).

⚠️ Aucun de ces trois n'est « le bon ». Le choix appartient aux auteurs
(cf. docs/06-indicateurs-exec.md §5).
""")


if __name__ == "__main__":
    table, couverture = construire()
    rapport_couverture(couverture)
    rapport_indicateurs(table)
    rapport_mappings()

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(SORTIE, float_format="%.6f")
    print(f"\nTableau écrit : {SORTIE.relative_to(RACINE)}")
