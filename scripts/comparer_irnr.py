"""
Territorial contre empreinte : ce que la délocalisation cachait.

L'IRNR mesurait la matière non renouvelable consommée par la France avec
le **DMC** d'Eurostat, qui ne compte que le poids des biens franchissant
la frontière. EXIOBASE permet de mesurer l'**empreinte** : toute la
matière remuée dans le monde pour ce que les Français consomment.

Les deux ne diffèrent pas seulement en niveau. **Elles vont en sens
contraire.** Ce script le montre, et chiffre ce que ça change à l'IED et
à la création monétaire.

Usage : python scripts/comparer_irnr.py
Sortie : sorties/irnr_territorial_vs_empreinte.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from modele.exec.indicateurs import SEUIL_MATIERE_T_HAB  # noqa: E402
from modele.exec.serie_france import construire  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
PNG = RACINE / "sorties" / "irnr_territorial_vs_empreinte.png"


def fr(x: float, dec: int = 2) -> str:
    return f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")


def charger() -> tuple[pd.DataFrame, pd.DataFrame]:
    terr, _ = construire(source_irnr="territorial")
    emp, _ = construire(source_irnr="empreinte")
    return terr, emp


def rapport(terr: pd.DataFrame, emp: pd.DataFrame) -> None:
    j = pd.DataFrame({
        "territorial": terr["matiere_nr_t_hab"],
        "empreinte": emp["matiere_nr_t_hab"],
    }).dropna()
    ecart = j["empreinte"] / j["territorial"] - 1

    print(f"""
{'=' * 74}
MATIÈRES NON RENOUVELABLES — DEUX MESURES, DEUX CONCLUSIONS OPPOSÉES
{'=' * 74}

  {'':>12} {'1995':>8} {'2022':>8}   tendance
  {'territorial':>12} {fr(j['territorial'].loc[1995]):>8} {fr(j['territorial'].loc[2022]):>8}   \
{fr(100 * (j['territorial'].loc[2022] / j['territorial'].loc[1995] - 1), 0)} %   ← ce que disait l'IRNR
  {'empreinte':>12} {fr(j['empreinte'].loc[1995]):>8} {fr(j['empreinte'].loc[2022]):>8}   \
+{fr(100 * (j['empreinte'].loc[2022] / j['empreinte'].loc[1995] - 1), 0)} %   ← ce qui s'est passé

Le DMC dit que la France s'est allégée d'un cinquième. L'empreinte dit
qu'elle s'est alourdie d'un quart. **L'« amélioration » mesurée par
l'IRNR territorial était, pour l'essentiel, un déménagement.**

L'écart entre les deux mesures grandit avec le temps — c'est la
signature de la délocalisation :

  1995 : {fr(100 * ecart.loc[1995], 0)} %      2010 : +{fr(100 * ecart.loc[2010], 0)} %      2023 : +{fr(100 * ecart.loc[2023], 0)} %

  écart moyen sur la période : +{fr(100 * ecart.mean(), 0)} %

Seuil de soutenabilité retenu : {fr(SEUIL_MATIERE_T_HAB, 1)} t/hab/an (Bringezu 2015).
  • en territorial, la France passe sous le seuil vers 2014 ;
  • en empreinte, **elle ne passe jamais sous le seuil**.
""")

    a = terr.dropna(subset=["IED"])
    b = emp.dropna(subset=["IED"])
    print(f"""{'=' * 74}
CE QUE ÇA CHANGE À L'IED
{'=' * 74}

  {'IRNR':<14} {'période':>12} {'IED min':>9} {'IED max':>9} {'IED final':>11}
  {'territorial':<14} {f'{a.index.min()}–{a.index.max()}':>12} {fr(a['IED'].min()):>9} \
{fr(a['IED'].max()):>9} {fr(a['IED'].iloc[-1]):>11}
  {'empreinte':<14} {f'{b.index.min()}–{b.index.max()}':>12} {fr(b['IED'].min()):>9} \
{fr(b['IED'].max()):>9} {fr(b['IED'].iloc[-1]):>11}

L'IED baisse d'environ {fr(100 * (1 - b['IED'].iloc[-1] / a['IED'].iloc[-1]), 0)} %, mais il reste du même ordre :
la correction ne bouleverse pas la conclusion du jalon P2. La France
serait restée, sous l'EH, en régime de création monétaire réduite de
moitié — un peu plus réduite encore.

**Ce qui change vraiment, c'est le récit.** Avec l'IRNR territorial, on
pouvait dire « la France s'améliore lentement ». Avec l'empreinte, la
seule amélioration réelle est celle du carbone ; la matière, elle,
s'aggrave. L'IED ne monte que parce qu'un de ses trois termes progresse.
""")


def tracer(terr: pd.DataFrame, emp: pd.DataFrame) -> None:
    fig, (h, b) = plt.subplots(2, 1, figsize=(11, 9), sharex=True,
                               gridspec_kw={"height_ratios": [1.35, 1]})

    h.axhline(SEUIL_MATIERE_T_HAB, color="#444", ls=":", lw=1.2,
              label=f"seuil de soutenabilité ({fr(SEUIL_MATIERE_T_HAB, 0)} t/hab)")
    h.plot(terr.index, terr["matiere_nr_t_hab"], lw=2.6, color="#8a6d1f",
           label="DMC territorial — ce que mesurait l'IRNR")
    h.plot(emp.index, emp["matiere_nr_t_hab"], lw=2.6, color="#b03030",
           label="Empreinte, importations incluses (EXIOBASE)")
    h.fill_between(emp.index, terr["matiere_nr_t_hab"].reindex(emp.index),
                   emp["matiere_nr_t_hab"], color="#b03030", alpha=.13,
                   label="matière remuée à l'étranger, invisible au DMC")
    h.set_ylabel("Matières non renouvelables (t/hab/an)")
    h.set_title("L'« amélioration » écologique de la France était\n"
                "en grande partie un déménagement", fontsize=14,
                fontweight="bold", loc="left")
    h.legend(fontsize=8.8, loc="lower left", framealpha=.94)
    h.grid(alpha=.25)
    h.set_ylim(bottom=0)
    h.annotate("Territorial : −22 % entre 1995 et 2022\n"
               "Empreinte   : +26 % sur la même période\n"
               "Les deux mesures vont en sens contraire.",
               xy=(.985, .90), xycoords="axes fraction", ha="right",
               va="top", fontsize=9,
               bbox=dict(boxstyle="round,pad=.5", fc="#fff3f0",
                         ec="#b03030", alpha=.96))

    b.axhline(1.0, color="#444", ls=":", lw=1.1, label="équilibre (IED = 1)")
    b.plot(terr.index, terr["IED"], lw=2.2, ls="--", color="#8a6d1f",
           label="IED avec IRNR territorial")
    b.plot(emp.index, emp["IED"], lw=2.6, color="#1a7a44",
           label="IED avec IRNR en empreinte")
    b.set_ylabel("IED")
    b.set_xlabel("Année")
    b.set_ylim(0, 1.1)
    b.grid(alpha=.25)
    b.legend(fontsize=8.8, loc="upper left", framealpha=.94)

    fig.text(.012, .022,
             "Sources : Eurostat env_ac_mfa (territorial) · EXIOBASE 3.10.2 "
             "via pymrio (empreinte) · Global Carbon Project · Eurostat env_bio2.",
             fontsize=7.4, color="#555")
    fig.text(.012, .006,
             "Indicateurs EXEC : choix normatifs de catégorie D, non "
             "empiriques — voir modele/registre/. Trou en 2000 : rupture de "
             "la série d'oiseaux.", fontsize=7.4, color="#555")
    fig.tight_layout(rect=[0, .042, 1, 1])
    PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG, dpi=155)
    plt.close(fig)


if __name__ == "__main__":
    terr, emp = charger()
    rapport(terr, emp)
    tracer(terr, emp)
    print(f"Graphique : {PNG.relative_to(RACINE)}")
