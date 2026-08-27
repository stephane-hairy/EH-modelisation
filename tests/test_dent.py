"""
Tests du module DENT.

Deux rôles distincts :

1. **Prouver les défauts** de la formule de la synthèse (§11.1). Ces tests
   ne vérifient pas que le code est correct — ils vérifient que la
   *formule* se comporte bien comme l'analyse critique le dit. Si l'un
   d'eux tombe un jour, c'est l'analyse qu'il faut revoir.
2. **Garantir les propriétés annoncées** des trois alternatives : bornes,
   monotonie, absence de singularité, homogénéité.
"""
import math

import pytest

from modele.eh.dent import (Entreprise, dent_deux_termes, dent_multiplicative,
                            dent_valeur_ajoutee, echelle_salariale,
                            facteur_equite_borne, facteur_equite_decroissant,
                            simuler_cliquet, terme_correctif_synthese)

DCIT = 22_000.0


def entreprise(salaries=500, salaire_max=250_000.0):
    return Entreprise(production=190_000 * salaries,
                      valeur_ajoutee=74_000 * salaries,
                      salaries=salaries, salaire_max=salaire_max)


# ======================================================================
# 1. Les défauts de la formule §11.1
# ======================================================================

def test_les_deux_lectures_different_d_un_facteur_1e8():
    """L'ambiguïté typographique du PDF n'est pas anodine."""
    for e, r in ((10, 38_000), (100, 98_000), (5_000, 480_000)):
        a = terme_correctif_synthese(e, DCIT, r, "A")
        b = terme_correctif_synthese(e, DCIT, r, "B")
        assert b / a == pytest.approx(1e8, rel=1e-9)


def test_le_terme_diverge_quand_l_ecart_de_salaire_s_annule():
    """r = 0 (entreprise parfaitement égalitaire) → dividende infini."""
    assert terme_correctif_synthese(100, DCIT, 0.0, "A") == math.inf
    # La divergence est hyperbolique : le terme varie exactement en 1/r.
    # Diviser l'écart de salaire par 10 000 multiplie le dividende par
    # 10 000. Il n'y a aucun plafond.
    assert (terme_correctif_synthese(100, DCIT, 1.0, "A")
            == pytest.approx(1e4 * terme_correctif_synthese(100, DCIT,
                                                            10_000.0, "A")))


def test_le_terme_n_est_pas_defini_sans_salarie():
    """96 % des entreprises françaises ont moins de 10 personnes occupées,
    donc le plus souvent aucun salarié : la formule ne s'applique pas."""
    assert math.isnan(terme_correctif_synthese(0, DCIT, 50_000.0, "A"))


def test_le_terme_croit_comme_le_carre_de_l_effectif():
    """Doubler l'effectif quadruple le terme, alors que la production ne
    fait que doubler. C'est la source de l'explosion pour les grandes
    entreprises."""
    r = 100_000.0
    t1 = terme_correctif_synthese(100, DCIT, r, "A")
    t2 = terme_correctif_synthese(200, DCIT, r, "A")
    assert t2 / t1 == pytest.approx(4.0, rel=1e-12)


def test_lecture_B_depasse_la_production_des_70_salaries():
    """Sous la lecture B, le « bonus » dépasse le produit d'exploitation
    entier pour une PME ordinaire."""
    e, salaire_max = 100, 100_000.0
    production = 190_000 * e
    terme = terme_correctif_synthese(e, DCIT, salaire_max - DCIT, "B")
    assert terme > production


def test_le_cliquet_amplifie_la_base_de_reference():
    """La règle « moyenne des 3 meilleures années » crée une rétroaction
    positive : la base converge vers X0/(1−g), pas vers X0."""
    r = simuler_cliquet(1_000.0, ied=1.0, alpha=0.8, annees=90)
    assert not r.divergent
    assert r.point_fixe == pytest.approx(5_000.0, rel=1e-4)
    assert r.base_P[-1] == pytest.approx(r.point_fixe, rel=0.02)


def test_la_clause_hors_dent_ne_protege_pas():
    """Exclure son propre dividende retire 1/N du flux : avec N grand,
    l'amplification est inchangée à 6 chiffres près."""
    petit = simuler_cliquet(1_000.0, alpha=0.8, n_entreprises=10, annees=60)
    grand = simuler_cliquet(1_000.0, alpha=0.8, n_entreprises=4_906_972,
                            annees=60)
    assert grand.point_fixe == pytest.approx(5_000.0, rel=1e-5)
    # avec seulement 10 entreprises la clause mordrait un peu
    assert petit.point_fixe < grand.point_fixe


def test_le_cliquet_ignore_une_recession():
    """Après six ans de récession à −25 %, la base de référence ne perd
    qu'une fraction de cela : elle retient les meilleures années."""
    normal = simuler_cliquet(1_000.0, alpha=0.8, annees=24)
    choque = simuler_cliquet(1_000.0, alpha=0.8, annees=24,
                             choc={t: 0.75 for t in range(12, 18)})
    perte = 1 - choque.base_P[-1] / normal.base_P[-1]
    assert 0 < perte < 0.25   # bien moins que le choc de 25 %


# ======================================================================
# 2. Les propriétés annoncées des alternatives
# ======================================================================

def test_facteur_equite_borne_est_dans_zero_deux():
    for s in (1.0, 2.0, 5.0, 20.0, 500.0):
        k = facteur_equite_borne(s)
        assert 0.0 < k < 2.0


def test_facteur_equite_vaut_un_a_la_reference():
    """Au niveau d'écart de référence, le dividende vaut exactement IED×P
    — la cible annoncée par la synthèse."""
    assert facteur_equite_borne(5.0, s_ref=5.0) == pytest.approx(1.0)


def test_facteurs_equite_strictement_decroissants():
    valeurs_k = [facteur_equite_borne(s) for s in range(1, 60)]
    valeurs_p = [facteur_equite_decroissant(s) for s in range(1, 60)]
    assert all(a > b for a, b in zip(valeurs_k, valeurs_k[1:]))
    assert all(a > b for a, b in zip(valeurs_p, valeurs_p[1:]))


def test_facteur_equite_decroissant_vaut_un_pour_l_egalite_parfaite():
    """s = 1 : tout le monde au revenu minimum. Prime entière, mais FINIE
    — c'est exactement le cas où la formule §11.1 divergeait."""
    assert facteur_equite_decroissant(1.0) == pytest.approx(1.0)
    assert facteur_equite_decroissant(1.0) < math.inf


def test_aucune_alternative_ne_diverge_a_l_egalite_parfaite():
    """Le défaut central de la §11.1 est corrigé par les trois."""
    ent = entreprise(salaire_max=DCIT)   # écart de salaire nul
    for f in (dent_multiplicative, dent_deux_termes, dent_valeur_ajoutee):
        v = f(1.0, ent, DCIT)
        assert math.isfinite(v) and v > 0


def test_alternatives_definies_sans_salarie():
    """Une entreprise unipersonnelle doit recevoir un dividende défini."""
    ent = Entreprise(production=80_000, valeur_ajoutee=45_000,
                     salaries=0, salaire_max=DCIT)
    for f in (dent_multiplicative, dent_deux_termes, dent_valeur_ajoutee):
        assert math.isfinite(f(1.0, ent, DCIT))


def test_alternatives_bornees_par_deux_fois_l_assiette():
    ent = entreprise()
    assert 0 < dent_multiplicative(1.0, ent, DCIT) < 2 * ent.production
    assert 0 < dent_valeur_ajoutee(1.0, ent, DCIT) < 2 * ent.valeur_ajoutee
    borne = ent.production * 0.7 + 0.3 * ent.salaries * DCIT
    assert 0 < dent_deux_termes(1.0, ent, DCIT) <= borne


def test_alternatives_decroissantes_en_ecart_de_salaire():
    """Plus le patron gagne, moins l'entreprise touche : l'intention de la
    synthèse est bien réalisée, cette fois de façon monotone et bornée."""
    for f in (dent_multiplicative, dent_deux_termes, dent_valeur_ajoutee):
        vals = [f(1.0, entreprise(salaire_max=w), DCIT)
                for w in (22_000, 60_000, 150_000, 400_000, 2_000_000)]
        assert all(a > b for a, b in zip(vals, vals[1:])), f.__name__


def test_alternatives_proportionnelles_a_l_ied():
    """La création monétaire doit rester pilotée par l'indicateur
    écologique : doubler l'IED doit doubler le dividende."""
    ent = entreprise()
    for f in (dent_multiplicative, dent_deux_termes, dent_valeur_ajoutee):
        assert f(2.0, ent, DCIT) == pytest.approx(2 * f(1.0, ent, DCIT))
        assert f(0.0, ent, DCIT) == 0.0


def test_alternative_deux_termes_croit_lineairement_en_emploi():
    """Contrairement à la §11.1 (croissance en e²), la prime d'emploi est
    linéaire : pas d'avantage explosif aux très grandes entreprises."""
    a = dent_deux_termes(1.0, entreprise(salaries=100), DCIT, theta=1.0)
    b = dent_deux_termes(1.0, entreprise(salaries=200), DCIT, theta=1.0)
    assert b / a == pytest.approx(2.0, rel=1e-12)


def test_assiette_valeur_ajoutee_bien_plus_faible():
    """L'alternative 3 réduit l'assiette d'un facteur ≈ 2,6 — le rapport
    production / valeur ajoutée observé pour les SNF françaises."""
    ent = entreprise()
    assert (dent_multiplicative(1.0, ent, DCIT)
            / dent_valeur_ajoutee(1.0, ent, DCIT)) == pytest.approx(190 / 74,
                                                                    rel=1e-9)


def test_echelle_salariale_refuse_un_dcit_nul():
    with pytest.raises(ValueError):
        echelle_salariale(50_000, 0.0)


def test_theta_hors_bornes_refuse():
    with pytest.raises(ValueError):
        dent_deux_termes(1.0, entreprise(), DCIT, theta=1.5)
