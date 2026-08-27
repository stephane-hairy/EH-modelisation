"""
Construit la série d'empreintes françaises 1995–2024 à partir d'EXIOBASE.

**Ce que ça produit.** Pour chaque année, l'empreinte de consommation de
la France — c'est-à-dire tout ce qui a été extrait, cultivé ou émis
**dans le monde entier** pour ce que les Français consomment, moins ce
qui l'a été pour l'export :

- **sols** (cultures, pâturages, forêt, surfaces artificielles) → les
  44 % de l'empreinte écologique que l'IEE actuel ne voit pas ;
- **matières non renouvelables** (fossiles, minerais, minéraux) → un IRNR
  en empreinte au lieu du DMC territorial, qui sous-estime de 44 % ;
- **CO₂** → contrôle croisé permanent avec le Global Carbon Project.

**Coût mesuré** : ≈ 70 s de téléchargement + 162 s de calcul par année,
soit environ **2 heures** pour les 30 années, et 7,1 Go de disque.

**Reprise après interruption.** Le fichier de sortie est écrit **année
par année**. Relancer le script reprend là où il s'est arrêté : rien
n'est jamais perdu, et rien n'est recalculé pour rien.

Usage :
    python scripts/serie_exiobase.py                  # 1995–2024
    python scripts/serie_exiobase.py --debut 2015     # une sous-période
    python scripts/serie_exiobase.py --supprimer-zip  # économise 7 Go
"""
from __future__ import annotations

import argparse
import time
import urllib.request
from pathlib import Path

import pandas as pd

from modele.donnees.cache import enregistrer

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_ZIP = RACINE / "donnees" / "brut" / "exiobase"
SORTIE = RACINE / "donnees" / "traite" / "empreinte_exiobase_france.csv"

ZENODO = ("https://zenodo.org/api/records/20051562/files/"
          "IOT_{annee}_pxp.zip/content")
"""EXIOBASE 3.10.2 (mai 2026) — DOI 10.5281/zenodo.3583070.
Tables produit × produit, 1995–2024, 49 régions, 200 produits."""

PREMIERE, DERNIERE = 1995, 2024

# Retirer ces comptes satellites allège fortement l'inversion de Leontief
# (matrice 9 800 × 9 800) sans rien coûter à ce qu'on calcule.
EXTENSIONS_INUTILES = ("nutrients", "water", "Satellite Accounts_copy",
                       "employment", "energy_use")

# poste EXIOBASE → (extension, motif de recherche, facteur vers l'unité
# voulue). EXIOBASE donne les sols en km², les matières en kt, l'air en kg.
POSTES = {
    "sol_cultures_ha":      ("land", "Cropland", 100.0),
    "sol_paturages_ha":     ("land", "Pasture", 100.0),
    "sol_foret_ha":         ("land", "Forest", 100.0),
    "sol_artificiel_ha":    ("land", "Artificial", 100.0),
    "mat_fossiles_t":       ("material", "Fossil", 1e3),
    "mat_minerais_t":       ("material", "Metal Ores", 1e3),
    "mat_mineraux_t":       ("material", "Non-Metallic Minerals", 1e3),
    "mat_biomasse_t":       ("material", "Biomass", 1e3),
    "co2_t":                ("air_emissions", "CO2", 1e-3),
}
NON_RENOUVELABLES = ("mat_fossiles_t", "mat_minerais_t", "mat_mineraux_t")


def population_france() -> pd.Series:
    """Population annuelle, pour passer les empreintes par habitant."""
    from modele.donnees.ecologie import co2_empreinte, population
    return co2_empreinte()["population"].combine_first(population()).dropna()


def telecharger(annee: int) -> Path:
    """Récupère une année d'EXIOBASE, avec empreinte SHA-256 au manifeste."""
    chemin = DOSSIER_ZIP / f"IOT_{annee}_pxp.zip"
    if chemin.exists():
        return chemin
    url = ZENODO.format(annee=annee)
    DOSSIER_ZIP.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, chemin)
    # Le fichier fait ~240 Mo : on l'enregistre au manifeste pour la
    # traçabilité, sans le relire en mémoire une seconde fois.
    enregistrer(f"exiobase_IOT_{annee}_pxp.zip", url,
                chemin.read_bytes(), "EXIOBASE 3.10.2 (Zenodo)")
    return chemin


def empreinte_annee(chemin: Path) -> dict[str, float]:
    """Empreinte de consommation de la France pour une année."""
    import pymrio

    ex = pymrio.parse_exiobase3(path=str(chemin))
    for nom in EXTENSIONS_INUTILES:
        try:
            ex.remove_extension(nom)
        except Exception:
            pass
    ex.calc_all()

    resultats = {}
    for cle, (extension, motif, facteur) in POSTES.items():
        d = getattr(ex, extension).D_cba["FR"]
        lignes = d.index.get_level_values(0).str.contains(
            motif, case=False, regex=False)
        resultats[cle] = float(d[lignes].sum().sum()) * facteur
    return resultats


def deja_faites() -> set[int]:
    """Années déjà présentes dans le fichier de sortie."""
    if not SORTIE.exists():
        return set()
    return set(pd.read_csv(SORTIE)["annee"].astype(int))


def ecrire(ligne: dict) -> None:
    """Ajoute une année au fichier, en le créant au besoin."""
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    d = pd.DataFrame([ligne])
    d.to_csv(SORTIE, mode="a", header=not SORTIE.exists(), index=False,
             float_format="%.6f")


def fr(x: float, dec: int = 2) -> str:
    return f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")


def main(debut: int, fin: int, supprimer_zip: bool) -> None:
    pop = population_france()
    faites = deja_faites()
    annees = [a for a in range(debut, fin + 1) if a not in faites]

    if faites:
        print(f"déjà calculées : {len(faites)} années "
              f"({min(faites)}–{max(faites)})")
    if not annees:
        print("rien à faire, la série est complète.")
        return
    print(f"à calculer : {len(annees)} années ({annees[0]}–{annees[-1]})")
    print(f"durée estimée : {len(annees) * 232 / 3600:.1f} h\n")

    t_debut = time.time()
    for i, annee in enumerate(annees, 1):
        t0 = time.time()
        try:
            chemin = telecharger(annee)
            valeurs = empreinte_annee(chemin)
        except Exception as e:                       # noqa: BLE001
            # Une année qui échoue ne doit pas emporter la série entière.
            print(f"[{i}/{len(annees)}] {annee} ÉCHEC : "
                  f"{type(e).__name__} {e}", flush=True)
            continue

        habitants = pop.get(annee)
        ligne = {"annee": annee, "population": habitants, **valeurs}
        if habitants:
            for cle, v in valeurs.items():
                ligne[f"{cle}_hab"] = v / habitants
            ligne["mat_non_renouv_t_hab"] = sum(
                valeurs[c] for c in NON_RENOUVELABLES) / habitants
        ecrire(ligne)

        if supprimer_zip:
            chemin.unlink(missing_ok=True)

        nr = ligne.get("mat_non_renouv_t_hab")
        co2 = ligne.get("co2_t_hab")
        print(f"[{i}/{len(annees)}] {annee}  "
              f"matières NR {fr(nr, 2) if nr else '—':>6} t/hab · "
              f"CO₂ {fr(co2, 2) if co2 else '—':>5} t/hab · "
              f"{time.time() - t0:.0f}s", flush=True)

    print(f"\nterminé en {(time.time() - t_debut) / 60:.0f} min")
    print(f"série écrite : {SORTIE.relative_to(RACINE)}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--debut", type=int, default=PREMIERE)
    p.add_argument("--fin", type=int, default=DERNIERE)
    p.add_argument("--supprimer-zip", action="store_true",
                   help="supprime chaque archive après calcul (économise 7 Go)")
    a = p.parse_args()
    main(a.debut, a.fin, a.supprimer_zip)
