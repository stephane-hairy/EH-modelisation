"""
Le 0 et le 2 des indicateurs EXEC : à quoi correspondent-ils ?

**La question, posée par Stéphane Hairy (2026-08-27).** La synthèse EH
exige que chaque indicateur vaille 1 à l'équilibre et reste dans [0 ; 2].
Elle ne dit **rien** de ce que valent le 0 et le 2. Ce dépôt les avait
remplis sans en faire une décision. Ce script chiffre les options.

Il produit les tableaux de `docs/07-bornes-et-seuils.md`.

Usage : python scripts/bornes_indicateurs.py
"""
from __future__ import annotations

import numpy as np

# Pression x = mesure / seuil, France 2021 (cf. docs/06).
FRANCE_2021 = {"IEE": 2.94, "IRNR": 1.38, "IBD": 1.73}

# Pression carbone x, étalon mondial, GFN 2013 (« nombre de Terres »).
PAYS = {"Bangladesh": 0.44, "Brésil": 1.77, "France": 2.94,
        "Allemagne": 3.20, "Australie": 5.16}

BASE_DETA = 22_000.0     # € par citoyen, constante de conception EH
FONTE_MENSUELLE = 0.01   # 1 %/mois sur les soldes (synthèse §6)


def fr(x: float, dec: int = 2) -> str:
    return f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")


def titre(t: str) -> None:
    print(f"\n{'=' * 74}\n{t}\n{'=' * 74}")


def indicateur(x: float, x_haut: float = 0.0, x_bas: float = np.inf,
               plancher: float = 0.0) -> float:
    """
    Famille d'indicateurs à bornes explicites.

    Trois ancrages au lieu d'un :
    - `I(x_haut) = 2` — la pression en dessous de laquelle on donne le
      maximum ; vaut 0 aujourd'hui (« le pays ne consomme rien ») ;
    - `I(1) = 1` — l'équilibre, seul point fixé par la synthèse ;
    - `I(x_bas) = 0` — la pression à laquelle la création monétaire
      s'arrête. `inf` = elle ne s'arrête jamais (décroissance exponentielle).

    `plancher` impose un minimum, ce qui **interdit par construction
    l'extinction monétaire** — et protège de l'annulation de l'IED par la
    moyenne géométrique (décision D6).
    """
    x = float(x)
    if x <= x_haut:
        valeur = 2.0
    elif x <= 1.0:
        valeur = 2.0 - (x - x_haut) / (1.0 - x_haut)
    elif np.isinf(x_bas):
        valeur = 2.0 * 2.0 ** (-x)
    else:
        valeur = max(0.0, (x_bas - x) / (x_bas - 1.0))
    return max(plancher, valeur)


def ied(valeurs: dict[str, float]) -> float:
    """Moyenne géométrique des trois indicateurs (décision D6)."""
    return float(np.prod(list(valeurs.values())) ** (1 / 3))


def extinction_monetaire() -> None:
    titre("POURQUOI LE 0 EST LA QUESTION GRAVE")
    print("""
Sous l'EH la monnaie n'est créée QUE par le don : plus de crédit bancaire
créateur de monnaie. Si IED = 0, il n'y a aucune création — ni État, ni
citoyens, ni entreprises — pendant que la fonte continue de détruire le
stock existant.
""")
    print(f"  {'hypothèse de fonte':<44}{'demi-vie':>10}{'reste à 5 ans':>15}")
    for libelle, vitesse in (("soldes seuls (1 %/mois)", 0.0),
                             ("+ transactionnelle, vitesse 3/an", 3.0)):
        taux = FONTE_MENSUELLE + (0.01 * vitesse / 12)
        demi = np.log(0.5) / np.log(1 - taux) / 12
        reste = (1 - taux) ** 60
        print(f"  {libelle:<44}{fr(demi, 1) + ' ans':>10}{fr(100 * reste, 0) + ' %':>15}")
    print("""
  ⇒ IED = 0 n'est pas « une forte pénalité » : c'est la disparition
    progressive de la monnaie du pays. La question n'est donc pas
    « quel malus ? » mais :

      À partir de quel niveau de destruction l'économie homéostatique
      décide-t-elle qu'un pays ne doit plus avoir de monnaie du tout ?
""")


def borne_basse() -> None:
    titre("D14 — LA BORNE BASSE : QUAND COUPE-T-ON LA MONNAIE ?")
    print(f"\n  {'option':<40}{'IEE':>6}{'IRNR':>6}{'IBD':>6}{'IED':>7}"
          f"{'€/citoyen':>12}")
    options = [("B1  x₀ = 2 — deux fois le seuil", 2.0, 0.0),
               ("B2  x₀ = 5 — cinq fois le seuil", 5.0, 0.0),
               ("B3  x₀ = 10 — dix fois le seuil", 10.0, 0.0),
               ("B4  jamais atteint (actuel)", np.inf, 0.0),
               ("B5  jamais + plancher à 0,20", np.inf, 0.20)]
    for libelle, x_bas, plancher in options:
        v = {k: indicateur(x, 0.0, x_bas, plancher)
             for k, x in FRANCE_2021.items()}
        total = ied(v)
        print(f"  {libelle:<40}{fr(v['IEE']):>6}{fr(v['IRNR']):>6}"
              f"{fr(v['IBD']):>6}{fr(total):>7}{fr(total * BASE_DETA, 0) + ' €':>12}")

    titre("QUELS PAYS SERAIENT COUPÉS ? (carbone seul, GFN 2013)")
    print(f"\n  {'pays':<12}{'x':>6}" +
          "".join(f"{'x₀ = ' + str(b):>11}" for b in (2, 5, 10)))
    for pays, x in PAYS.items():
        print(f"  {pays:<12}{fr(x):>6}" +
              "".join(f"{fr(indicateur(x, 0.0, b)):>11}" for b in (2, 5, 10)))
    print("""
  ⇒ x₀ = 2 (le mapping linéaire) coupe la France, l'Allemagne ET
    l'Australie — la quasi-totalité des pays riches, pour un dépassement
    banal. À écarter.
  ⇒ x₀ = 5 et 10 sont plus INDULGENTES que l'actuel : elles donnent à la
    France plus que les 0,49 qu'elle obtient aujourd'hui. Elles diluent
    le signal.
  ⇒ le PLANCHER (B5) ne mord pas pour la France, mais il interdit par
    construction l'extinction monétaire — et protège de l'annulation de
    l'IED par la moyenne géométrique.
""")


def borne_haute() -> None:
    titre("D15 — LA BORNE HAUTE : QUE RÉCOMPENSE-T-ON AU MAXIMUM ?")
    print(f"""
Aujourd'hui I = 2 correspond à x = 0 : le pays ne consomme RIEN. Ce n'est
pas « parfaitement soutenable » — ça, c'est I = 1.

Conséquence rarement dite : puisque DETA = IED × {fr(BASE_DETA, 0)} × c, le système
verse le DOUBLE d'argent au pays dont l'activité économique est nulle.
La création monétaire est maximale quand l'économie s'arrête.
""")
    print(f"  {'option (x pour I = 2)':<40}"
          + "".join(f"{p:>12}" for p in ("Bangladesh", "Brésil", "France")))
    for libelle, x_haut in (("H1  x = 0 — ne consomme rien (actuel)", 0.0),
                            ("H2  x = 0,5 — moitié du seuil", 0.5)):
        print(f"  {libelle:<40}" + "".join(
            f"{fr(indicateur(PAYS[p], x_haut, 5.0)):>12}"
            for p in ("Bangladesh", "Brésil", "France")))
    print(f"  {'H4  plafonné à 1 — aucun bonus':<40}" + "".join(
        f"{fr(min(1.0, indicateur(PAYS[p], 0.0, 5.0))):>12}"
        for p in ("Bangladesh", "Brésil", "France")))
    print("""
  H3  [1 ; 2] = RÉGÉNÉRATION — ne se chiffre pas ici, et c'est le point.
      « 1 = ne plus dégrader ; 2 = réparer. » L'intervalle haut n'est plus
      réservé aux pays qui consomment peu, mais à ceux dont la pression
      est NETTE NÉGATIVE : puits de carbone supérieurs aux émissions,
      biodiversité en hausse, matière venant du recyclage.

      C'est la lecture la plus cohérente avec l'homéostasie : un organisme
      en homéostasie ne se contente pas de cesser de s'abîmer, IL SE
      RÉPARE. L'EH est bio-inspirée ; le haut de son échelle devrait
      décrire la régénération, pas l'inexistence.

      Conséquence à assumer : sous cette lecture, [1 ; 2] est AUJOURD'HUI
      VIDE. Aucun pays ne régénère. La moitié haute de l'échelle EH est
      une cible, pas un état observé.
""")


def seuils_incommensurables() -> None:
    titre("D16 — LES TROIS SEUILS NE SE COMPARENT PAS")
    print(f"\n  {'':<7}{'mesure 2021':>16}{'seuil':>9}{'x':>7}   nature du seuil")
    lignes = [("IEE", "6,26 tCO₂/hab", "2,13", 2.94, "budget planétaire (GIEC AR6)"),
              ("IRNR", "11,01 t/hab", "8,00", 1.38, "corridor scientifique (Bringezu)"),
              ("IBD", "indice 53,9", "93,3", 1.73, "⚠️ l'état de la France en 1990")]
    for nom, mesure, seuil, x, nature in lignes:
        print(f"  {nom:<7}{mesure:>16}{seuil:>9}{fr(x):>7}   {nature}")
    print("""
  ⇒ Le seuil de l'IBD N'EST PAS un seuil de soutenabilité : c'est un état
    passé. « IBD = 1 » veut dire « comme en 1990 » ; « IEE = 1 » veut dire
    « dans le budget de la planète ». Ce ne sont pas les mêmes 1, et la
    moyenne géométrique les traite comme s'ils l'étaient.

  ⇒ Prendre 1990 pour référence revient de plus à décréter que la France
    de 1990 était à l'équilibre écologique. Elle ne l'était pas.
    L'IBD est donc structurellement TROP OPTIMISTE.

  LA SOLUTION EXISTE : le Biodiversity Intactness Index (BII) mesure la
  part de biodiversité d'origine encore présente, et le cadre des limites
  planétaires (Steffen et al. 2015) fixe la frontière à BII ≥ 90 %.
  C'est un VRAI seuil, comparable au budget carbone.

  Natural History Museum, « BII country summaries » : 1970–2050,
  licence Creative Commons Non-Commercial.
  ⚠️ Téléchargement automatisé bloqué (Cloudflare 403), y compris par
     navigateur sans affichage depuis cet environnement. Le fichier se
     récupère À LA MAIN en trente secondes :
     data.nhm.ac.uk/dataset/bii-bte → ressource long_data.csv

  ⇒ Bonus : la série remonte à 1970, ce qui ROUVRIRAIT la période 1978
    demandée au cadrage (décision D5).
""")


if __name__ == "__main__":
    extinction_monetaire()
    borne_basse()
    borne_haute()
    seuils_incommensurables()
    print("\n" + "=" * 74)
    print("Options détaillées et recommandation : docs/07-bornes-et-seuils.md")
    print("=" * 74)
