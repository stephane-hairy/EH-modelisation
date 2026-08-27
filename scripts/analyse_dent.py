"""
Analyse critique de la formule DENT (§11.1 de la synthèse EH).

Répond aux quatre questions du verrou P0 (cf. TODO.md) **avec des
chiffres**, et non de mémoire :

  1. Le second terme est-il homogène à des euros ?
  2. Que vaut-il quand r → 0 ?
  3. La règle « moyenne des 3 meilleures années » crée-t-elle un cliquet
     et une rétroaction positive ?
  4. Que donnent les alternatives sur données françaises réelles ?

Usage : python scripts/analyse_dent.py
"""
from __future__ import annotations

from modele.eh.dent import (Entreprise, dent_deux_termes, dent_multiplicative,
                            dent_valeur_ajoutee, simuler_cliquet,
                            terme_correctif_synthese)

Md = 1e9

# --- Données françaises vérifiées -----------------------------------------
# Eurostat nasa_10_nf_tr, geo=FR, unit=CP_MEUR, 2023 (récupéré 2026-08-27)
PROD_SNF   = 3_810.2 * Md   # S11 production (P1)
VA_SNF     = 1_481.1 * Md   # S11 valeur ajoutée brute (B1G)
PROD_SF    =   287.7 * Md   # S12 sociétés financières, production
VA_SF      =    89.5 * Md   # S12 valeur ajoutée brute
PROD_MEN   =   515.6 * Md   # S14 ménages (dont entrepreneurs individuels)
VA_MEN     =   451.9 * Md   # S14 valeur ajoutée brute
PROD_TOT   = 5_310.0 * Md   # S1 économie totale, production
PIB        = 2_833.8 * Md   # INSEE CNA-2020-PIB, 2023

# Eurostat sbs_sc_ovw, geo=FR, nace_r2=B-S_X_O_S94, 2022
ENT_TOTAL  = 4_906_972      # nombre d'entreprises
ENT_0_9    = 4_718_929      # dont 0 à 9 personnes occupées
ENT_GE250  =     5_987      # dont 250 personnes occupées ou plus
OCC_TOTAL  = 20_478_850     # personnes occupées
OCC_0_9    =  5_541_957

DCIT = 22_000.0             # € /an — constante de conception de l'EH


def fr(x: float, dec: int = 0) -> str:
    """Formate un nombre à la française : espace fine pour les milliers,
    virgule décimale. `fr(3810.2, 1)` → « 3 810,2 »."""
    return f"{x:,.{dec}f}".replace(",", "\u202f").replace(".", ",")


def titre(t: str) -> None:
    print(f"\n{'=' * 74}\n{t}\n{'=' * 74}")


# ==========================================================================
def q1_homogeneite() -> None:
    titre("1. LE SECOND TERME EST-IL HOMOGÈNE À DES EUROS ? — NON")

    print("""
Formule :  DENT = IED × P + (e × DCIT) / ((r/e) × 10⁴)

Analyse dimensionnelle, en notant [€] les euros par an et [p] les personnes.

  e        → [p]                nombre de salariés
  DCIT     → [€·p⁻¹]            un revenu, donc des euros PAR personne
  r        → [€·p⁻¹]            un écart entre deux salaires : même nature
  e × DCIT → [p]·[€·p⁻¹] = [€]  une masse salariale.  ✅ correct
  r / e    → [€·p⁻²]
  terme    → [€] / [€·p⁻²] = [p²]

  ⇒ le second terme est homogène à un NOMBRE DE PERSONNES AU CARRÉ.

On l'additionne à IED × P, qui est en euros. **L'addition est invalide.**

Ce résultat ne dépend pas de la façon de lever l'ambiguïté du texte : les
deux lectures possibles (10⁴ multipliant r/e, ou multipliant e) donnent
toutes deux [p²]. Le défaut est structurel, pas typographique.

Il ne dépend pas non plus de la convention sur les personnes : si l'on
traite DCIT et r comme de simples euros, le terme vaut [p²] également.
""")


# ==========================================================================
def q1bis_ambiguite() -> None:
    titre("1 bis. LES DEUX LECTURES DIFFÈRENT D'UN FACTEUR 100 000 000")

    print("""
Le PDF sort la formule en glyphes séparés : « ( r / e × 1 0 ⁴ ) ». On ne
peut pas savoir si 10⁴ multiplie (r/e) ou e seul.

  lecture A :  (e × DCIT) / ((r/e) × 10⁴)  =  (e/100)² × (DCIT/r)
  lecture B :  (e × DCIT) / (r / (e×10⁴))  =  (e×100)² × (DCIT/r)

Le texte d'accompagnement — « r … est divisé par le nombre d'employé de
l'entreprise, lui-même multiplié par 10⁴ » — désigne plutôt la lecture B.
Le dépôt avait retenu la lecture A.
""")
    print(f"  {'effectif':>9} {'salaire max':>12} {'lecture A':>16} {'lecture B':>18}")
    for e, smax in ((10, 60_000), (100, 120_000), (1_000, 300_000),
                    (100_000, 2_000_000)):
        r = smax - DCIT
        ta = terme_correctif_synthese(e, DCIT, r, "A")
        tb = terme_correctif_synthese(e, DCIT, r, "B")
        print(f"  {fr(e):>9} {fr(smax):>12} {fr(ta, 2):>16} {fr(tb):>18}")
    print("""
Rapport B/A = 10⁸, exactement, quels que soient les paramètres.

Conséquence pour chaque lecture, comparée au produit d'exploitation P
(en France, environ 190 000 € de production par personne occupée) :

  • lecture A : le terme est NÉGLIGEABLE partout. Pour 1 000 salariés il
    vaut ~11 €, contre ~190 M€ de production. Il ne fait rien — sauf
    exploser quand r → 0 (question 2).

  • lecture B : le terme DÉPASSE la production entière au-delà d'environ
    70 salariés, et croît ensuite comme le carré de l'effectif. Pour une
    entreprise de 100 000 salariés il atteint des milliers de milliards
    d'euros — plus que la production de la France.

Aucune des deux ne réalise l'intention annoncée (« un dividende
relativement proche du produit d'exploitation »).
""")


# ==========================================================================
def q2_singularite() -> None:
    titre("2. QUE VAUT LE TERME QUAND r → 0 ? — IL DIVERGE")

    print("""
r = « écart entre le plus haut salaire de l'entreprise et DCIT ».
r = 0 signifie : le mieux payé de l'entreprise gagne exactement le revenu
minimum du pays. C'est l'entreprise parfaitement égalitaire.

Ce cas n'est ni théorique ni marginal : une petite coopérative où tout le
monde est au même salaire l'atteint exactement.
""")
    print(f"  {'r (€)':>12} {'terme, lecture A':>22}")
    for r in (100_000, 10_000, 1_000, 100, 10, 1, 0):
        v = terme_correctif_synthese(100, DCIT, r, "A")
        print(f"  {fr(r):>12} {fr(v, 1):>22}")
    print("""
  ⇒ dividende infini pour l'entreprise la plus vertueuse.

Trois problèmes en un :
  • **singularité** : division par zéro à un point atteignable ;
  • **incitation perverse** : la fonction récompense sans borne ce qu'elle
    prétend seulement encourager ;
  • **discontinuité de signe** : si le plus haut salaire passe SOUS le
    revenu minimum (r < 0), le terme bascule de +∞ à −∞. Le dividende
    change de signe pour une variation infinitésimale du salaire.

Et pour e = 0 salarié, r n'est pas défini du tout — or c'est le cas de la
grande majorité des entreprises françaises (question 3 bis).
""")


# ==========================================================================
def q3_cliquet() -> None:
    titre("3. « MOYENNE DES 3 MEILLEURES ANNÉES » — RÉTROACTION POSITIVE")

    print("""
La synthèse anticipe partiellement l'objection : elle précise que la
réactualisation de P se fait « hors DENT », c'est-à-dire sans compter le
dividende que l'entreprise a elle-même reçu. Cela coupe la boucle DIRECTE.

Mais cela ne coupe pas la boucle **macro-économique** : le dividende de
l'entreprise A est dépensé, et devient le chiffre d'affaires de B. Exclure
son propre dividende retire 1/N du flux. Avec N = 4,9 millions
d'entreprises en France, cela ne retire rien.

Récurrence obtenue :  P ← X₀ + g·P   avec  g = α × IED × (1 − 1/N)
où α = part du dividende qui revient aux entreprises en chiffre d'affaires.
""")
    print(f"  {'α':>6} {'g':>8} {'amplification de P':>22} {'DTENT à terme':>18}")
    for alpha in (0.5, 0.7, 0.8, 0.9, 0.95, 1.0):
        r = simuler_cliquet(PROD_SNF, ied=1.0, alpha=alpha, annees=60)
        if r.divergent:
            print(f"  {fr(alpha, 2):>6} {fr(alpha, 3):>8} {'DIVERGE':>22} {'∞':>18}")
        else:
            amp = r.point_fixe / PROD_SNF
            print(f"  {fr(alpha, 2):>6} {fr(alpha, 3):>8} "
                  f"{'×' + fr(amp, 1):>22} {fr(r.point_fixe / Md):>14} Md€")
    print("""
Lecture : avec α = 0,8 — hypothèse modérée, puisque la fonte pousse à
dépenser — la base de référence P se stabilise à **5 fois** la production
initiale. Le dividende total des entreprises suit. À α ≥ 1, le système
diverge.

À α = 1 (tout le dividende revient en chiffre d'affaires), le SEUL frein
restant est la clause « hors DENT » — et il plafonne l'amplification à N,
soit 4,9 MILLIONS de fois. Autrement dit : la précaution prise par la
synthèse ne protège de rien. Elle transforme une divergence en une
explosion finie mais absurde.

C'est une **rétroaction positive**, dans une théorie qui se présente comme
un thermostat sans rétroaction positive. Ce n'est pas un artefact de
simulation : c'est la solution analytique de la règle telle qu'écrite.
""")

    titre("3 bis. L'EFFET CLIQUET : P NE REDESCEND PAS")
    normal = simuler_cliquet(PROD_SNF, alpha=0.8, annees=24)
    avec_choc = simuler_cliquet(PROD_SNF, alpha=0.8, annees=24,
                                choc={t: 0.75 for t in range(12, 18)})
    print("""
On applique une récession de −25 % pendant 6 ans (années 12 à 17), puis
retour à la normale. La règle retient les MEILLEURES années : la base de
référence ignore la récession.
""")
    print(f"  {'année':>6} {'produit (Md€)':>16} {'base P sans choc':>19} "
          f"{'base P avec choc':>19}")
    for t in (9, 12, 15, 17, 18, 21, 23):
        print(f"  {t:>6} {fr(avec_choc.produit[t] / Md):>16} "
              f"{fr(normal.base_P[t] / Md):>19} {fr(avec_choc.base_P[t] / Md):>19}")
    ecart = 100 * (1 - avec_choc.base_P[-1] / normal.base_P[-1])
    print(f"""
  ⇒ après six ans de récession sévère, la base de référence n'a perdu que
    {fr(ecart, 1)} %. La création monétaire reste calée sur un niveau
    d'activité que l'économie n'atteint plus.

  C'est exactement ce qu'un régulateur ne doit pas faire : le thermostat
  continue de chauffer parce qu'il se souvient du meilleur été.
""")


# ==========================================================================
def q4_perimetre() -> None:
    titre("4. LE PÉRIMÈTRE « ENTREPRISE » — CHIFFRÉ SUR LA FRANCE")

    print(f"""
La synthèse dit « entreprise » sans définir le mot. Les périmètres
possibles ne diffèrent pas à la marge : ils changent l'assiette de 39 %.

Comptes nationaux 2023 (Eurostat nasa_10_nf_tr, prix courants) :

  secteur                                    production      valeur ajoutée
  S11  sociétés non financières            {fr(PROD_SNF / Md):>9} Md€    {fr(VA_SNF / Md):>9} Md€
  S12  sociétés financières                {fr(PROD_SF / Md):>9} Md€    {fr(VA_SF / Md):>9} Md€
  S14  ménages (dont entrepreneurs indiv.) {fr(PROD_MEN / Md):>9} Md€    {fr(VA_MEN / Md):>9} Md€
  S1   économie totale                     {fr(PROD_TOT / Md):>9} Md€           —

  Pour mémoire, PIB 2023 : {fr(PIB / Md)} Md€.

Quatre périmètres défendables, et ce qu'ils donnent pour l'assiette :

  a) SNF seules                        {fr(PROD_SNF / Md):>9} Md€  ({fr(PROD_SNF / PIB, 2)} × PIB)
  b) SNF + sociétés financières        {fr((PROD_SNF + PROD_SF) / Md):>9} Md€  ({fr((PROD_SNF + PROD_SF) / PIB, 2)} × PIB)
  c) b) + entrepreneurs individuels    {fr((PROD_SNF + PROD_SF + PROD_MEN) / Md):>9} Md€  ({fr((PROD_SNF + PROD_SF + PROD_MEN) / PIB, 2)} × PIB)
  d) toute production marchande        {fr(PROD_TOT / Md):>9} Md€  ({fr(PROD_TOT / PIB, 2)} × PIB)

  ⇒ du plus étroit au plus large, l'assiette varie de {100 * (PROD_TOT / PROD_SNF - 1):.0f} %,
    soit {fr((PROD_TOT - PROD_SNF) / Md)} Md€ d'écart — la moitié d'un PIB.
    Le choix de périmètre pèse presque autant que le choix de formule.

Trois pièges spécifiques, chacun à trancher explicitement :

  • **Les sociétés financières.** En EH, les banques ne créent plus la
    monnaie. Leur verser un dividende proportionnel à leur « production »
    (essentiellement des marges d'intermédiation) n'a plus de sens
    évident. Recommandation : les exclure, et le dire.

  • **Les entrepreneurs individuels.** Ils sont dans le secteur des
    ménages (S14), donc leurs dirigeants touchent DÉJÀ le DCIT. Leur
    verser en plus un DENT assis sur leur production les avantage
    doublement par rapport à un salarié.

  • **La production de S14 contient les loyers imputés** — le loyer
    fictif que les propriétaires se versent à eux-mêmes. Verser un
    dividende d'entreprise là-dessus n'aurait aucun sens. Le périmètre c)
    est donc inutilisable tel quel.
""")

    titre("4 bis. LA MOITIÉ DES « ENTREPRISES » N'A PAS DE SALARIÉ")
    print(f"""
Démographie des entreprises (Eurostat sbs_sc_ovw, France 2022,
NACE B-S hors administration publique) :

  entreprises, total                      {fr(ENT_TOTAL):>12}
  dont 0 à 9 personnes occupées           {fr(ENT_0_9):>12}   ({fr(100 * ENT_0_9 / ENT_TOTAL, 1)} %)
  dont 250 personnes occupées ou plus     {fr(ENT_GE250):>12}   ({fr(100 * ENT_GE250 / ENT_TOTAL, 2)} %)

  personnes occupées, total               {fr(OCC_TOTAL):>12}
  dont dans les unités de 0 à 9 personnes {fr(OCC_0_9):>12}

  ⇒ soit {fr(OCC_0_9 / ENT_0_9, 2)} personne par entreprise dans la classe 0–9.

L'écrasante majorité des entreprises françaises est donc une personne
seule : l'entrepreneur, sans salarié. Pour elles, **e = 0** et le second
terme de la formule §11.1 n'est pas défini du tout — il n'existe ni
« nombre de salariés », ni « plus haut salaire », ni écart r.

Le calcul « entreprise par entreprise » que prescrit la synthèse est donc
impossible à mener sur 96 % des entreprises françaises.
""")


# ==========================================================================
def q5_nature_de_P() -> None:
    titre("5. QU'EST-CE QUE P ? — COMPTABLE OU COMPTES NATIONAUX")

    print(f"""
« Produit d'exploitation » est un terme de **comptabilité d'entreprise** :
c'est en gros le chiffre d'affaires, plus quelques produits annexes. Ce
n'est pas la « production » des comptes nationaux, et l'écart n'est pas
négligeable.

  production des SNF (comptes nationaux)  {fr(PROD_SNF / Md):>9} Md€
  valeur ajoutée des SNF                  {fr(VA_SNF / Md):>9} Md€
  rapport                                 {fr(PROD_SNF / VA_SNF, 2):>9}

La différence, ce sont les **consommations intermédiaires** : ce que
l'entreprise a acheté à ses fournisseurs pour produire.

Le vrai problème n'est pas de choisir entre deux définitions voisines.
C'est que **la somme des chiffres d'affaires n'est pas une grandeur
économique**. Elle compte plusieurs fois la même valeur, autant de fois
qu'il y a de maillons dans la chaîne de production.

Conséquence directe et vérifiable :

  • deux entreprises FUSIONNENT → la vente de l'une à l'autre disparaît →
    la somme des productions BAISSE → le dividende total BAISSE ;
  • une entreprise SE SCINDE en deux → une vente interne devient une vente
    externe → la somme des productions MONTE → le dividende total MONTE.

Rien n'a changé dans l'économie réelle. La création monétaire du pays
dépendrait de la façon dont les entreprises découpent leurs contrats.
C'est une faille d'optimisation évidente : il suffirait de filialiser pour
créer de la monnaie.

La **valeur ajoutée** n'a pas ce défaut. Elle est additive : sa somme ne
bouge ni en fusionnant ni en scindant, et elle vaut le PIB. C'est ce qui
motive l'alternative 3.

Enfin, « moyenne des trois meilleures années » retient un MAXIMUM, donc
une valeur supérieure à la production courante, en plus du cliquet
démontré en question 3.
""")


# ==========================================================================
def q6_alternatives() -> None:
    titre("6. LES TROIS ALTERNATIVES, SUR UN CAS CONCRET")

    ent = Entreprise(production=190_000 * 500, valeur_ajoutee=74_000 * 500,
                     salaries=500, salaire_max=250_000)
    print(f"""
Entreprise type : 500 salariés · production {fr(ent.production / 1e6)} M€ ·
valeur ajoutée {fr(ent.valeur_ajoutee / 1e6)} M€ · plus haut salaire
{fr(ent.salaire_max)} € (soit {fr(ent.salaire_max / DCIT, 1)} fois le revenu minimum).
IED = 1 (équilibre écologique atteint).
""")
    resultats = {
        "§11.1 lecture A": 1.0 * ent.production
        + terme_correctif_synthese(ent.salaries, DCIT, ent.salaire_max - DCIT, "A"),
        "§11.1 lecture B": 1.0 * ent.production
        + terme_correctif_synthese(ent.salaries, DCIT, ent.salaire_max - DCIT, "B"),
        "alt. 1 multiplicative": dent_multiplicative(1.0, ent, DCIT),
        "alt. 2 deux termes": dent_deux_termes(1.0, ent, DCIT),
        "alt. 3 valeur ajoutée": dent_valeur_ajoutee(1.0, ent, DCIT),
    }
    for nom, v in resultats.items():
        print(f"  {nom:<24} {fr(v / 1e6, 1):>14} M€")

    print("""
Extrapolation à la France entière (périmètre SNF, IED = 1). Ordre de
grandeur seulement : l'agrégation d'une formule non linéaire à partir
d'une entreprise moyenne n'est pas exacte.
""")
    kappa = dent_multiplicative(1.0, ent, DCIT) / ent.production
    part_prime = dent_deux_termes(1.0, ent, DCIT) / ent.production
    print(f"  {'formule':<24} {'assiette':>12} {'DTENT':>14} {'× PIB':>8}")
    totaux = []
    for nom, assiette, coef in (
            ("§11.1 (≈ IED × P)", PROD_SNF, 1.0),
            ("alt. 1 multiplicative", PROD_SNF, kappa),
            ("alt. 2 deux termes θ=0,3", PROD_SNF, part_prime),
            ("alt. 3 valeur ajoutée", VA_SNF, kappa)):
        dtent = assiette * coef
        totaux.append(dtent)
        print(f"  {nom:<24} {fr(assiette / Md):>9} Md€ {fr(dtent / Md):>11} Md€ "
              f"{fr(dtent / PIB, 2):>8}")
    print(f"""
  ⇒ selon la formule retenue, le dividende total des entreprises françaises
    varie d'un facteur {fr(max(totaux) / min(totaux), 1)}. C'est bien cette formule, et non la
    théorie EH, qui décide de l'ordre de grandeur de la création monétaire.
""")


if __name__ == "__main__":
    q1_homogeneite()
    q1bis_ambiguite()
    q2_singularite()
    q3_cliquet()
    q4_perimetre()
    q5_nature_de_P()
    q6_alternatives()
    print("\n" + "=" * 74)
    print("Détail des propositions et fiches de registre : docs/05-dent.md")
    print("=" * 74)
