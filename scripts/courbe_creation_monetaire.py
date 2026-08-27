"""
LE LIVRABLE PHARE : quelle création monétaire l'économie homéostatique
aurait-elle donnée à la France ?

Assemble les indicateurs EXEC (jalon P2) et les formules de monnaie-don
(§11.1) pour produire la courbe année par année.

⚠️ **Deux honnêtetés obligatoires, portées par le graphique lui-même** :

1. **La courbe ne peut pas commencer en 1978.** Les données écologiques
   françaises commencent en 1990, et l'empreinte matières en 1995. Le
   graphique s'arrête là où les données s'arrêtent.
2. **Le dividende des entreprises n'est pas un trait, c'est une bande.**
   La formule DENT n'est pas arbitrée (verrou P0, `docs/05-dent.md`).
   Publier un trait unique laisserait croire à une précision qui n'existe
   pas. On publie donc la part État + citoyens en trait plein — elle, on
   la connaît — et la part entreprises en fourchette.

Usage : python scripts/courbe_creation_monetaire.py
Sorties : sorties/creation_monetaire_eh_france.png
          donnees/traite/creation_monetaire_eh.csv
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from modele.donnees.comptes import assiettes_dent  # noqa: E402
from modele.eh.dent import (Entreprise, dent_deux_termes,  # noqa: E402
                            dent_multiplicative, dent_valeur_ajoutee)
from modele.exec.serie_france import construire  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
PNG = RACINE / "sorties" / "creation_monetaire_eh_france.png"
CSV = RACINE / "donnees" / "traite" / "creation_monetaire_eh.csv"

Md = 1e9
BASE_DETA = 22_000.0      # € par citoyen — constante de conception EH

# Entreprise « moyenne » servant à calibrer le coefficient de chaque
# variante de DENT. Voir docs/05-dent.md §7 : l'agrégation d'une formule
# non linéaire depuis une entreprise moyenne est approximative, et c'est
# une des raisons pour lesquelles on publie une fourchette.
ENT_TYPE = Entreprise(production=190_000 * 500, valeur_ajoutee=74_000 * 500,
                      salaries=500, salaire_max=250_000.0)


def fr(x: float, dec: int = 0) -> str:
    return f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")


def coefficients_dent(dcit_reference: float = 22_000.0) -> dict[str, tuple]:
    """Pour chaque variante de DENT : (assiette à utiliser, coefficient).

    Le coefficient est le rapport dividende / assiette obtenu sur
    l'entreprise type, à IED = 1. Il est ensuite appliqué à l'assiette
    macro-économique de chaque année.
    """
    p, va = ENT_TYPE.production, ENT_TYPE.valeur_ajoutee
    return {
        "§11.1 (≈ IED × P)":
            ("production_SNF", 1.0),
        "alt. 1 multiplicative":
            ("production_SNF",
             dent_multiplicative(1.0, ENT_TYPE, dcit_reference) / p),
        "alt. 2 deux termes (θ=0,3)":
            ("production_SNF",
             dent_deux_termes(1.0, ENT_TYPE, dcit_reference) / p),
        "alt. 3 valeur ajoutée":
            ("va_SNF",
             dent_valeur_ajoutee(1.0, ENT_TYPE, dcit_reference) / va),
    }


def construire_courbe(mapping: str = "exponentiel",
                      source_irnr: str = "empreinte") -> pd.DataFrame:
    """Création monétaire annuelle qu'aurait produite l'EH, en euros.

    `source_irnr` vaut « empreinte » par défaut : le DMC territorial
    inversait le signe de la tendance matières (cf. `comparer_irnr.py`).
    """
    exec_fr, _ = construire(mapping=mapping, source_irnr=source_irnr)
    assiettes = assiettes_dent()

    from modele.donnees.ecologie import co2_empreinte
    pop = co2_empreinte()["population"].dropna()

    d = pd.DataFrame({"IED": exec_fr["IED"],
                      "IED_sans_IBD": exec_fr["IED_sans_IBD"]})
    d["population"] = pop
    d = d.join(assiettes, how="left").dropna(subset=["population",
                                                     "production_SNF",
                                                     "IED"])

    # ⚠️ Aucun rebouchage. L'IED de référence est celui à TROIS
    # indicateurs, et il est absent là où l'un des trois manque : en 2000
    # (rupture de la série d'oiseaux) et après 2021. Un trou dans la
    # courbe est une information ; un trou rebouché est un mensonge.
    d["IED_retenu"] = d["IED"]

    # --- État et citoyens : pas d'ambiguïté de formule ---
    d["DETA"] = d["IED_retenu"] * BASE_DETA * d["population"]
    d["DTCIT"] = d["DETA"]
    d["DCIT"] = d["IED_retenu"] * BASE_DETA
    d["socle_etat_citoyens"] = d["DETA"] + d["DTCIT"]

    # --- Entreprises : une colonne par variante non arbitrée ---
    for nom, (assiette, coef) in coefficients_dent().items():
        d[f"DTENT — {nom}"] = d["IED_retenu"] * d[assiette] * coef

    # Réindexation sur toutes les années : l'année 2000, écartée pour
    # rupture de série, devient un trou VISIBLE dans la courbe au lieu
    # d'un segment tracé par-dessus.
    d = d.reindex(range(int(d.index.min()), int(d.index.max()) + 1))

    variantes = [c for c in d.columns if c.startswith("DTENT — ")]
    d["DTENT_min"] = d[variantes].min(axis=1)
    d["DTENT_max"] = d[variantes].max(axis=1)
    d["DG_min"] = d["socle_etat_citoyens"] + d["DTENT_min"]
    d["DG_max"] = d["socle_etat_citoyens"] + d["DTENT_max"]
    return d


def tracer(d: pd.DataFrame) -> None:
    fig, (h, b) = plt.subplots(2, 1, figsize=(11, 9.5), sharex=True,
                               gridspec_kw={"height_ratios": [2.1, 1]})

    # ---- Haut : la création monétaire -------------------------------
    h.fill_between(d.index, d["DG_min"] / Md, d["DG_max"] / Md,
                   where=d["DG_min"].notna(), alpha=.22, color="#b03030",
                   label="Création totale — fourchette due à DENT non arbitrée")
    for nom in [c for c in d.columns if c.startswith("DTENT — ")]:
        h.plot(d.index, (d["socle_etat_citoyens"] + d[nom]) / Md,
               lw=1.1, ls="--", alpha=.75, label=nom.replace("DTENT — ", "dont "))
    h.plot(d.index, d["socle_etat_citoyens"] / Md, lw=3, color="#14456e",
           label="État + citoyens (sans ambiguïté de formule)")

    h.set_ylabel("Création monétaire annuelle (Md€ courants)")
    h.set_title("Quelle création monétaire l'économie homéostatique\n"
                "aurait-elle donnée à la France ?", fontsize=14,
                fontweight="bold", loc="left")
    h.legend(fontsize=8.5, loc="upper left", framealpha=.93)
    h.grid(alpha=.25)
    h.set_ylim(bottom=0)

    der = d.dropna(subset=["DG_min"]).iloc[-1]
    ecart = der["DG_max"] / der["DG_min"]
    h.annotate(
        f"En {int(der.name)}, la fourchette va de {fr(der['DG_min'] / Md)}"
        f" à {fr(der['DG_max'] / Md)} Md€\n"
        f"— un facteur {fr(ecart, 1)}. C'est la formule DENT qui décide,\n"
        f"pas la théorie. Verrou P0, docs/05-dent.md.",
        xy=(.985, .30), xycoords="axes fraction", ha="right", fontsize=8.6,
        bbox=dict(boxstyle="round,pad=.5", fc="#fff3f0", ec="#b03030",
                  alpha=.95))

    # ---- Bas : l'IED qui pilote tout --------------------------------
    b.axhline(1.0, color="#444", lw=1.1, ls=":", label="équilibre (IED = 1)")
    b.plot(d.index, d["IED_retenu"], lw=2.4, color="#1a7a44",
           label="IED (3 indicateurs)")
    b.plot(d.index, d["IED_sans_IBD"], lw=1.4, ls="--", color="#8a6d1f",
           label="IED sans la biodiversité (2 indicateurs)")
    b.set_ylabel("IED")
    b.set_xlabel("Année")
    b.set_ylim(0, 1.15)
    b.grid(alpha=.25)
    b.legend(fontsize=8.5, loc="upper left", framealpha=.93)
    b.annotate("L'IED français reste très en dessous de 1 sur toute la\n"
               "période : sous l'EH, la France aurait été en régime de\n"
               "création monétaire réduite en permanence.",
               xy=(.985, .06), xycoords="axes fraction", ha="right",
               fontsize=8.6,
               bbox=dict(boxstyle="round,pad=.45", fc="#f2f7f4",
                         ec="#1a7a44", alpha=.95))

    fig.text(.012, .022,
             "Sources : Eurostat env_ac_mfa, env_bio2, nasa_10_nf_tr · "
             "Global Carbon Project · EXIOBASE 3.10.2 "
             "(empreintes, importations incluses).",
             fontsize=7.4, color="#555")
    fig.text(.012, .006,
             "Indicateurs EXEC et formules DENT : choix normatifs de "
             "catégorie D, non empiriques — voir modele/registre/. "
             "Trou en 2000 : rupture de la série d'oiseaux.",
             fontsize=7.4, color="#555")
    fig.tight_layout(rect=[0, .042, 1, 1])
    PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG, dpi=155)
    plt.close(fig)


def rapport(d: pd.DataFrame) -> None:
    print(f"""
{'=' * 74}
CRÉATION MONÉTAIRE QU'AURAIT DONNÉE L'EH À LA FRANCE
{'=' * 74}

Période couverte : {d.dropna(subset=["DG_min"]).index.min()}–{d.dropna(subset=["DG_min"]).index.max()} (2000 écarté : rupture de série).
Demandée au cadrage : 1978–2023. **Écart assumé et documenté** : les
données écologiques françaises n'existent pas avant 1990.
""")
    print(f"  {'année':>5} {'IED':>6} {'DETA':>9} {'DTCIT':>9} "
          f"{'DTENT min':>11} {'DTENT max':>11} {'total min':>11} "
          f"{'total max':>11}")
    for an in d.dropna(subset=["DG_min"]).index:
        r = d.loc[an]
        print(f"  {an:>5} {fr(r['IED_retenu'], 2):>6} "
              f"{fr(r['DETA'] / Md):>9} {fr(r['DTCIT'] / Md):>9} "
              f"{fr(r['DTENT_min'] / Md):>11} {fr(r['DTENT_max'] / Md):>11} "
              f"{fr(r['DG_min'] / Md):>11} {fr(r['DG_max'] / Md):>11}")

    der = d.dropna(subset=["DG_min"]).iloc[-1]
    print(f"""
En {int(der.name)} :
  • dividende par citoyen : {fr(der['DCIT'])} €/an, soit {fr(der['DCIT'] / 12)} €/mois
    (contre 22 000 €/an si l'IED valait 1 — la France est loin du compte)
  • création totale : entre {fr(der['DG_min'] / Md)} et {fr(der['DG_max'] / Md)} Md€,
    soit un facteur {fr(der['DG_max'] / der['DG_min'], 1)} selon la formule DENT retenue.

⚠️ Cette fourchette n'est PAS une incertitude de mesure. C'est l'effet
d'une décision de conception non prise (verrou P0). Elle se refermera
quand D7–D10 seront tranchées, pas avec de meilleures données.
""")


if __name__ == "__main__":
    d = construire_courbe()
    rapport(d)
    tracer(d)
    CSV.parent.mkdir(parents=True, exist_ok=True)
    d.to_csv(CSV, float_format="%.2f")
    print(f"Graphique : {PNG.relative_to(RACINE)}")
    print(f"Données   : {CSV.relative_to(RACINE)}")
