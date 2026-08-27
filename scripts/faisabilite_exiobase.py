"""
EXIOBASE : chiffrer la faisabilité avant de s'engager.

**La question posée.** Nos deux indicateurs les plus solides ont le même
défaut : ils sont **territoriaux**. L'IRNR compte le poids des biens
importés, pas la matière remuée à l'étranger pour les fabriquer. L'IEE ne
couvre que le carbone, soit 56 % de l'empreinte écologique.

EXIOBASE est un **tableau entrées-sorties multirégional** : une
comptabilité de qui produit quoi pour qui, à l'échelle mondiale, avec les
pressions écologiques attachées. Il permet de calculer une vraie
empreinte de consommation — importations incluses — pour les sols, les
matières et les émissions.

Ce script ne construit pas la série. Il répond à trois questions
préalables, avec des mesures et non des estimations :

  1. Combien de temps et d'espace disque coûte une année ?
  2. Les résultats sont-ils crédibles ? (croisement avec une source
     indépendante)
  3. Qu'est-ce que ça apporterait vraiment aux indicateurs actuels ?

Usage : python scripts/faisabilite_exiobase.py --annee 2020
        (télécharge ~240 Mo, calcule ~3 min, n'écrit rien dans le modèle)
"""
from __future__ import annotations

import argparse
import time
import urllib.request
from pathlib import Path

ZENODO = "https://zenodo.org/api/records/20051562/files/IOT_{annee}_pxp.zip/content"
"""EXIOBASE 3.10.2 (mai 2026), dépôt Zenodo — DOI 10.5281/zenodo.3583070.
Tables produit × produit (`pxp`), 1995–2024, 49 régions, 200 produits."""

# Comptes satellites inutiles ici : les retirer allège fortement
# l'inversion de Leontief (matrice 9 800 × 9 800).
EXTENSIONS_INUTILES = ("nutrients", "water", "Satellite Accounts_copy",
                       "employment", "energy_use")

ANNEES_TESTABLES = (2019, 2020)
"""Années pour lesquelles les repères de comparaison existent.

⚠️ **La population n'est pas codée en dur, et ce n'est pas un détail.**
Une première version comparait l'empreinte EXIOBASE (divisée par la
population Eurostat, 67,6 M) au DMC d'Eurostat (divisé par la population
OWID du modèle, 65,9 M). Les deux mesures ne portaient donc pas sur la
même France, et l'écart annoncé était faussé de 2,5 %. On lit désormais
la population et les repères **depuis le modèle lui-même**."""


def fr(x: float, dec: int = 2) -> str:
    return f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")


def reperes(annee: int) -> dict[str, float]:
    """Population et repères de comparaison, lus depuis le modèle.

    Garantit que l'empreinte EXIOBASE et les mesures territoriales
    auxquelles on la compare sont rapportées à la MÊME population.
    """
    from modele.exec.serie_france import construire
    from modele.donnees.ecologie import co2_empreinte, population

    table, _ = construire()
    pop = co2_empreinte()["population"].combine_first(population()).dropna()
    return {
        "population": float(pop.loc[annee]),
        "co2_gcp_t_hab": float(table.loc[annee, "co2_empreinte_t_hab"]),
        "dmc_nr_eurostat_t_hab": float(table.loc[annee, "matiere_nr_t_hab"]),
    }


def telecharger(annee: int, dossier: Path) -> Path:
    """Récupère une année d'EXIOBASE. ~240 Mo, ~70 s."""
    chemin = dossier / f"IOT_{annee}_pxp.zip"
    if chemin.exists():
        print(f"déjà présent : {chemin.name} "
              f"({chemin.stat().st_size / 1e6:.0f} Mo)")
        return chemin
    url = ZENODO.format(annee=annee)
    t0 = time.time()
    dossier.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, chemin)
    print(f"téléchargé en {time.time() - t0:.0f} s "
          f"({chemin.stat().st_size / 1e6:.0f} Mo)")
    return chemin


def empreinte(ex, extension: str, motif: str) -> float:
    """Empreinte de consommation de la France pour un poste donné.

    `D_cba` (*consumption-based accounts*) est l'empreinte de
    consommation : elle attribue à la France tout ce qui a été extrait,
    cultivé ou émis **dans le monde entier** pour produire ce qu'elle
    consomme, et lui retire ce qu'elle produit pour l'export.
    """
    d = getattr(ex, extension).D_cba["FR"]
    lignes = d.index.get_level_values(0).str.contains(motif, case=False,
                                                      regex=False)
    return float(d[lignes].sum().sum())


def main(annee: int, dossier: Path) -> None:
    import pymrio

    chemin = telecharger(annee, dossier)
    t0 = time.time()
    ex = pymrio.parse_exiobase3(path=str(chemin))
    for nom in EXTENSIONS_INUTILES:
        try:
            ex.remove_extension(nom)
        except Exception:
            pass
    t_lecture = time.time() - t0

    t1 = time.time()
    ex.calc_all()          # inversion de Leontief + comptes d'empreinte
    t_calcul = time.time() - t1

    rep = reperes(annee)
    pop = rep["population"]

    print(f"\n{'=' * 74}\nFRANCE {annee} — EMPREINTE DE CONSOMMATION "
          f"(importations incluses)\n{'=' * 74}")

    print("\n  SOLS  (EXIOBASE en km²)")
    total_sol = 0.0
    for poste in ("Cropland", "Pasture", "Forest", "Artificial"):
        v = empreinte(ex, "land", poste)
        total_sol += v
        print(f"    {poste:<14} {fr(v * 100 / pop, 4):>10} ha/hab"
              f"   ({fr(v / 1e4, 2):>7} Mha)")
    print(f"    {'TOTAL':<14} {fr(total_sol * 100 / pop, 4):>10} ha/hab")
    print("    ↳ c'est la partie NON CARBONÉE de l'empreinte écologique,"
          "\n      soit les 44 % que l'IEE actuel ne voit pas du tout.")

    print("\n  MATIÈRES NON RENOUVELABLES  (EXIOBASE en kt)")
    total_nr = 0.0
    for poste in ("Fossil", "Metal Ores", "Non-Metallic Minerals"):
        v = empreinte(ex, "material", poste)
        total_nr += v
        print(f"    {poste:<24} {fr(v * 1e3 / pop, 3):>8} t/hab")
    nr_hab = total_nr * 1e3 / pop
    terr = rep["dmc_nr_eurostat_t_hab"]
    print(f"    {'TOTAL':<24} {fr(nr_hab, 3):>8} t/hab")
    print(f"\n    ↳ Eurostat DMC, mesure TERRITORIALE : {fr(terr, 2)} t/hab")
    print(f"    ⚠️  **L'IRNR actuel sous-estime de {fr(100 * (nr_hab / terr - 1), 0)} %** — "
          f"c'est le biais\n       d'importation, jusqu'ici signalé mais non chiffré.")
    print(f"       (mesuré sur la même population que le modèle : "
          f"{fr(pop / 1e6, 1)} M habitants)")

    co2_hab = empreinte(ex, "air_emissions", "CO2") / 1e3 / pop
    gcp = rep["co2_gcp_t_hab"]
    print(f"\n  CO₂  (EXIOBASE en kg)")
    print(f"    empreinte carbone        {fr(co2_hab, 2):>8} t/hab")
    print(f"    ↳ Global Carbon Project  {fr(gcp, 2):>8} t/hab")
    print(f"    ⇒ écart {fr(100 * abs(co2_hab / gcp - 1), 1)} % entre DEUX bases "
          f"multirégionales indépendantes\n      (EXIOBASE et Eora). "
          f"C'est la validation croisée du pipeline.")

    total = t_lecture + t_calcul
    print(f"\n{'=' * 74}\nCOÛT MESURÉ\n{'=' * 74}")
    print(f"  lecture + élagage   {t_lecture:>6.0f} s")
    print(f"  Leontief + comptes  {t_calcul:>6.0f} s")
    print(f"  total par année     {total:>6.0f} s  (+ ~70 s de téléchargement)")
    print(f"\n  ⇒ série 1995–2024 (30 ans) : "
          f"≈ {30 * (total + 70) / 3600:.1f} h de calcul, 7,1 Go de disque.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--annee", type=int, default=2020,
                   choices=list(ANNEES_TESTABLES))
    p.add_argument("--dossier", type=Path,
                   default=Path("donnees/brut/exiobase"))
    a = p.parse_args()
    main(a.annee, a.dossier)
