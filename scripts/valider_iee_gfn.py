"""
Confronte notre IEE de remplacement à la vraie empreinte écologique.

**Pourquoi ce script existe.** L'IEE du jalon P2 n'est pas l'empreinte
écologique demandée par la synthèse (§14.1) : c'est l'empreinte *carbone*
importations incluses, faute d'accès aux comptes du Global Footprint
Network. On a fini par mettre la main sur le paquet public officiel du
GFN — une seule année, 2013 — via Dateno. Une année suffit pour répondre
à la seule question qui compte : **de combien notre approximation se
trompe-t-elle ?**

Usage : python scripts/valider_iee_gfn.py
"""
from __future__ import annotations

from modele.donnees.ecologie import co2_empreinte
from modele.donnees.gfn import ANNEE, empreinte_et_biocapacite
from modele.exec.indicateurs import MAPPINGS, SEUIL_CO2_T_HAB


def fr(x: float, dec: int = 2) -> str:
    return f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")


def titre(t: str) -> None:
    print(f"\n{'=' * 74}\n{t}\n{'=' * 74}")


def main() -> None:
    g = empreinte_et_biocapacite("France")
    co2 = co2_empreinte()
    co2_hab = co2.loc[ANNEE, "empreinte"] * 1e6 / co2.loc[ANNEE, "population"]

    titre(f"LA VRAIE EMPREINTE ÉCOLOGIQUE DE LA FRANCE, {ANNEE}")
    print(f"""
Source : Global Footprint Network, National Footprint Accounts 2017
Public Data Package (licence Creative Commons). Unité : hectare global
par personne — la surface de nature moyennement productive qu'il faudrait
pour soutenir le mode de vie d'un Français.

  EMPREINTE DE CONSOMMATION (importations incluses)  {fr(g['empreinte_consommation'])} gha/pers
     dont carbone                                    {fr(g['empreinte_carbone'])}
     dont cultures                                   {fr(g['empreinte_cropland'])}
     dont forêt                                      {fr(g['empreinte_foret'])}
     dont pâturage                                   {fr(g['empreinte_paturage'])}
     dont pêche                                      {fr(g['empreinte_peche'])}
     dont sol bâti                                   {fr(g['empreinte_bati'])}

  BIOCAPACITÉ DISPONIBLE                             {fr(g['biocapacite'])} gha/pers
  DÉFICIT                                            {fr(g['deficit'])} gha/pers

  ⇒ RAPPORT EMPREINTE / BIOCAPACITÉ  =  {fr(g['ratio'])}

En clair : il faudrait **{fr(g['ratio'], 2)} France** pour soutenir le mode de vie
français. C'est le « x » que l'IEE doit transformer en note.
""")

    titre("CE QUE NOTRE APPROXIMATION RATE")
    print(f"""
Le carbone pèse **{fr(100 * g['part_carbone'], 1)} %** de l'empreinte française.
Notre approximation en capture donc un peu plus de la moitié, et ignore
le reste : cultures, forêts, pâturages, pêche, sol bâti — soit
{fr(g['empreinte_consommation'] - g['empreinte_carbone'])} gha/pers.

C'était l'hypothèse annoncée (« le carbone est la composante dominante »).
Elle est **vérifiée** : dominante, oui — majoritaire de peu.
""")

    titre("ET SURTOUT : NOTRE SEUIL ÉTAIT DEUX FOIS TROP SÉVÈRE")
    ratio_proxy = co2_hab / SEUIL_CO2_T_HAB
    seuil_cal = co2_hab / g["ratio"]
    print(f"""
Comparons les deux mesures de pression pour la même année {ANNEE} :

  notre approximation : {fr(co2_hab)} tCO₂/hab ÷ {fr(SEUIL_CO2_T_HAB)} t  =  x = {fr(ratio_proxy)}
  Global Footprint Network                          x = {fr(g['ratio'])}

  ⇒ notre approximation SURESTIME la pression d'un facteur {fr(ratio_proxy / g['ratio'])}.

Ce n'est pas une erreur de calcul : les deux mesurent des choses
différentes.

  • Notre seuil ({fr(SEUIL_CO2_T_HAB)} t) vient du budget climatique mondial 1,5 °C
    partagé également par tête. C'est une référence **planétaire et
    morale** : « quelle part du ciel chaque humain peut-il utiliser ? »
  • Le rapport du GFN compare l'empreinte à la biocapacité **du pays
    lui-même**. C'est une référence **territoriale** : « la France
    vit-elle sur ses propres moyens ? »

Les deux sont défendables. Elles ne disent pas la même chose, et l'écart
entre elles est d'un facteur 2 — c'est-à-dire davantage que l'écart entre
deux mappings.

Pour que notre série carbone reproduise le niveau du GFN en {ANNEE}, il
faudrait un seuil de :

  {fr(co2_hab)} ÷ {fr(g['ratio'])}  =  **{fr(seuil_cal)} tCO₂/hab/an**

C'est-à-dire le HAUT de la fourchette 1–4 t déjà déclarée en sensibilité
dans la fiche EQ-EXEC-002. La calibration GFN ne sort donc pas du cadre
prévu : elle en désigne le bord supérieur.
""")

    titre("CE QUE ÇA CHANGE POUR L'IEE ET L'IED")
    print(f"  {'mapping':<14} {'IEE seuil ' + fr(SEUIL_CO2_T_HAB):>16} "
          f"{'IEE seuil GFN ' + fr(seuil_cal):>20}")
    for nom, f in MAPPINGS.items():
        print(f"  {nom:<14} {fr(float(f(ratio_proxy))):>16} "
              f"{fr(float(f(g['ratio']))):>20}")
    expo = MAPPINGS["exponentiel"]
    lin = MAPPINGS["lineaire"]
    print(f"""
Sous le mapping exponentiel, l'IEE {ANNEE} passe de {fr(float(expo(ratio_proxy)))} à \
{fr(float(expo(g['ratio'])))} —
il reste dégradé, mais il n'est plus catastrophique. Sous le mapping
linéaire il passe de {fr(float(lin(ratio_proxy)))} à {fr(float(lin(g['ratio'])))} : \
il cesse d'être NUL, ce qui
supprime l'annulation totale de la création monétaire française.

⚠️ CONSÉQUENCE POUR L'ARBITRAGE : le seuil (décision D13) pèse autant que
le mapping (décision D11). Les deux doivent être tranchés ensemble.

⚠️ CE QUE ÇA NE RÈGLE PAS : nous n'avons qu'UNE année. On peut recaler le
niveau de la série, pas sa forme. Si le rapport empreinte/biocapacité
français a évolué autrement que son empreinte carbone entre 1990 et 2021,
nous ne le voyons pas. Obtenir la série complète du GFN (1961→) reste la
seule vraie solution, et exige une clé d'API nominative.
""")


if __name__ == "__main__":
    main()
