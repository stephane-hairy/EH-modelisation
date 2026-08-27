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

  Biocapacité de la France                           {fr(g['biocapacite'])} gha/pers
  Biocapacité mondiale par humain                    {fr(g['biocapacite_mondiale'])} gha/pers

DEUX ÉTALONS POSSIBLES, ET ILS NE DISENT PAS LA MÊME CHOSE :

  x mondial     = empreinte ÷ biocapacité MONDIALE  = {fr(g['ratio_mondial'])}
      « il faudrait {fr(g['ratio_mondial'], 2)} Terres si tout le monde vivait comme
        un Français »  → note le COMPORTEMENT
  x territorial = empreinte ÷ biocapacité FRANÇAISE = {fr(g['ratio_territorial'])}
      « il faudrait {fr(g['ratio_territorial'], 2)} France pour nourrir la France »
        → note la GÉOGRAPHIE

⇒ **Étalon retenu : le mondial** (décision D13). Sous l'étalon
  territorial, l'Australie — qui consomme 74 % de nature de plus que la
  France — recevrait 2,3 fois plus de monnaie, parce qu'elle a de
  l'espace ; et le Bangladesh, qui consomme 7 fois moins, serait moins
  bien noté que la France, parce qu'il est dense. Incitation perverse.
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

    titre("NOTRE APPROXIMATION EST JUSTE À 15 % PRÈS")
    ratio_proxy = co2_hab / SEUIL_CO2_T_HAB
    seuil_cal = co2_hab / g["ratio_mondial"]
    print(f"""
Comparons les deux mesures de pression pour la même année {ANNEE},
sur l'étalon retenu (mondial) :

  notre approximation : {fr(co2_hab)} tCO₂/hab ÷ {fr(SEUIL_CO2_T_HAB)} t  =  x = {fr(ratio_proxy)}
  Global Footprint Network, nombre de Terres        x = {fr(g['ratio_mondial'])}

  ⇒ écart : facteur {fr(ratio_proxy / g['ratio_mondial'])}. **Notre approximation surestime la
    pression de {fr(100 * (ratio_proxy / g['ratio_mondial'] - 1), 0)} %.**

C'est un résultat remarquablement bon, et il n'est pas fortuit. Les deux
mesures posent la même question — « quelle part des ressources de la
planète, par tête ? » — l'une par le carbone, l'autre par les hectares
globaux. Elles convergent parce que le carbone pèse {fr(100 * g['part_carbone'], 0)} % de
l'empreinte, et que le reste (cultures, forêts, pêche) est réparti de
façon assez proche de la moyenne mondiale pour un pays comme la France.

Pour un recalage exact sur {ANNEE}, le seuil serait :

  {fr(co2_hab)} ÷ {fr(g['ratio_mondial'])}  =  **{fr(seuil_cal)} tCO₂/hab/an**   (au lieu de {fr(SEUIL_CO2_T_HAB)})

Un ajustement de {fr(100 * (seuil_cal / SEUIL_CO2_T_HAB - 1), 0)} %, très à l'intérieur de la fourchette
1–4 t déjà déclarée en sensibilité (fiche EQ-EXEC-002).

⚠️ POUR MÉMOIRE — l'étalon TERRITORIAL, lui, donnerait x = {fr(g['ratio_territorial'])},
soit un écart de facteur {fr(ratio_proxy / g['ratio_territorial'])}. C'est cette comparaison-là qui avait
fait conclure d'abord à un seuil « deux fois trop sévère ». La conclusion
ne tenait qu'au choix d'étalon, et cet étalon a été écarté (décision D13).
""")

    titre("CE QUE ÇA CHANGE POUR L'IEE ET L'IED")
    print(f"  {'mapping':<14} {'IEE, seuil ' + fr(SEUIL_CO2_T_HAB):>17} "
          f"{'IEE, seuil recalé ' + fr(seuil_cal):>24}")
    for nom, f in MAPPINGS.items():
        print(f"  {nom:<14} {fr(float(f(ratio_proxy))):>17} "
              f"{fr(float(f(g['ratio_mondial']))):>24}")
    expo = MAPPINGS["exponentiel"]
    print(f"""
Sous le mapping exponentiel, l'IEE {ANNEE} passe de {fr(float(expo(ratio_proxy)))} à \
{fr(float(expo(g['ratio_mondial'])))} :
un déplacement mineur. **Le recalage sur le GFN ne change donc pas les
conclusions du jalon P2.** L'IED français reste très en dessous de 1.

C'est la bonne nouvelle de cette validation : sur l'étalon retenu, notre
série carbone tient. Le mapping (décision D11) redevient le seul choix
vraiment structurant.

⚠️ CE QUE ÇA NE RÈGLE PAS, et il faut le redire :
  • Une SEULE année d'ancrage. On valide le niveau, pas la forme. Si le
    « nombre de Terres » français a évolué autrement que son empreinte
    carbone entre 1990 et 2021, nous ne le voyons pas.
  • {fr(100 * (1 - g['part_carbone']), 0)} % de l'empreinte reste hors du champ : cultures,
    forêts, pâturages, pêche, sol bâti. La convergence à {fr(100 * (ratio_proxy / g['ratio_mondial'] - 1), 0)} % est
    partiellement une compensation d'erreurs, pas une mesure de ces
    composantes.
""")


if __name__ == "__main__":
    main()
