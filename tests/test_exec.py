"""
Tests des indicateurs EXEC.

Aucun accès réseau : les données sont synthétiques. On teste les
**propriétés** exigées par la synthèse (valoir 1 à l'équilibre, rester
dans [0 ; 2], décroître avec la pression) et les pièges que le calcul
doit refuser (rebouchage silencieux d'un indicateur manquant).
"""
import numpy as np
import pandas as pd
import pytest

from modele.exec.indicateurs import (BORNE_HAUTE, MAPPINGS, SEUIL_CO2_T_HAB,
                                     assembler, ibd, ied, iee,
                                     mapping_exponentiel, mapping_hyperbolique,
                                     mapping_lineaire, irnr)

ANNEES = list(range(1990, 2000))


def faux_dmc():
    n = len(ANNEES)
    return pd.DataFrame({
        "MF1": np.linspace(200_000, 230_000, n),   # biomasse : à ignorer
        "MF2": np.linspace(30_000, 20_000, n),
        "MF3": np.linspace(450_000, 400_000, n),
        "MF4": np.linspace(146_000, 120_000, n),
    }, index=ANNEES)


def fausse_pop():
    return pd.Series(np.linspace(57e6, 60e6, len(ANNEES)), index=ANNEES)


def faux_co2():
    n = len(ANNEES)
    return pd.DataFrame({
        "territorial": np.linspace(390, 380, n),
        "empreinte": np.linspace(493, 500, n),      # millions de tonnes
        "population": np.linspace(57e6, 60e6, n),
    }, index=ANNEES)


def fausse_bio():
    return pd.Series(np.linspace(93.0, 70.0, len(ANNEES)), index=ANNEES)


# ======================================================================
# 1. Les mappings : les propriétés exigées par la synthèse
# ======================================================================

@pytest.mark.parametrize("nom", list(MAPPINGS))
def test_mapping_vaut_un_a_l_equilibre(nom):
    """L'exigence centrale : à la pression soutenable, l'indicateur = 1."""
    assert MAPPINGS[nom](1.0) == pytest.approx(1.0)


@pytest.mark.parametrize("nom", list(MAPPINGS))
def test_mapping_vaut_deux_a_pression_nulle(nom):
    """Borne haute atteinte quand la pression est nulle."""
    assert MAPPINGS[nom](0.0) == pytest.approx(BORNE_HAUTE)


@pytest.mark.parametrize("nom", list(MAPPINGS))
def test_mapping_reste_dans_zero_deux(nom):
    x = np.linspace(0, 50, 400)
    v = np.asarray(MAPPINGS[nom](x))
    assert v.min() >= 0.0
    assert v.max() <= BORNE_HAUTE + 1e-12


@pytest.mark.parametrize("nom", list(MAPPINGS))
def test_mapping_decroissant(nom):
    """Plus de pression ne doit jamais donner une meilleure note."""
    v = np.asarray(MAPPINGS[nom](np.linspace(0, 10, 200)))
    assert np.all(np.diff(v) <= 1e-12)


def test_seul_le_mapping_lineaire_atteint_zero():
    """C'est la différence qui décide de tout : atteindre zéro annule la
    moyenne géométrique, donc toute la création monétaire."""
    assert mapping_lineaire(2.5) == 0.0
    assert mapping_hyperbolique(2.5) > 0.0
    assert mapping_exponentiel(2.5) > 0.0
    # et elles ne s'annulent jamais, même très loin
    assert mapping_hyperbolique(1e6) > 0.0
    assert mapping_exponentiel(50.0) > 0.0


def test_mapping_exponentiel_divise_par_deux_par_unite():
    """La règle doit s'énoncer en une phrase : +1 de dépassement = /2."""
    for x in (0.0, 1.0, 2.0, 3.5):
        assert mapping_exponentiel(x + 1) == pytest.approx(
            mapping_exponentiel(x) / 2)


# ======================================================================
# 2. Les indicateurs
# ======================================================================

def test_irnr_ignore_la_biomasse():
    """La biomasse est renouvelable : elle ne doit pas peser sur l'IRNR."""
    dmc, pop = faux_dmc(), fausse_pop()
    a = irnr(dmc, pop)
    dmc2 = dmc.copy()
    dmc2["MF1"] *= 10          # dix fois plus de biomasse
    b = irnr(dmc2, pop)
    pd.testing.assert_frame_equal(a, b)


def test_irnr_baisse_quand_la_consommation_baisse():
    dmc, pop = faux_dmc(), fausse_pop()
    normal = irnr(dmc, pop)["indice"]
    sobre = irnr(dmc[["MF1"]].assign(MF2=dmc["MF2"] / 2, MF3=dmc["MF3"] / 2,
                                     MF4=dmc["MF4"] / 2), pop)["indice"]
    assert (sobre > normal).all()


def test_iee_utilise_bien_l_empreinte_et_pas_le_territorial():
    """L'exigence §14.1 : importations incluses. Les deux colonnes
    doivent donner des résultats différents, sinon on s'est trompé."""
    co2 = faux_co2()
    empreinte = iee(co2, colonne="empreinte")["indice"]
    territorial = iee(co2, colonne="territorial")["indice"]
    assert not np.allclose(empreinte, territorial)
    # l'empreinte française dépasse les émissions territoriales,
    # donc l'indicateur doit être PLUS sévère
    assert (empreinte < territorial).all()


def test_iee_conversion_d_unite_correcte():
    """Les émissions sont en millions de tonnes : une erreur d'unité
    d'un facteur 10⁶ donnerait un indicateur toujours égal à 2."""
    co2 = faux_co2()
    d = iee(co2)
    # 493 Mt pour 57 M d'habitants ≈ 8,6 t/hab
    assert d["pression_t_hab"].iloc[0] == pytest.approx(493 / 57, rel=1e-3)
    assert d["ratio"].iloc[0] == pytest.approx(493e6 / 57e6 / SEUIL_CO2_T_HAB,
                                               rel=1e-6)


def test_ibd_vaut_un_a_l_annee_de_reference():
    d = ibd(fausse_bio(), annee_reference=1990)
    assert d["indice"].loc[1990] == pytest.approx(1.0)


def test_ibd_se_degrade_quand_les_oiseaux_disparaissent():
    d = ibd(fausse_bio(), annee_reference=1990)
    assert d["indice"].iloc[-1] < d["indice"].iloc[0]


def test_ibd_refuse_une_annee_de_reference_absente():
    with pytest.raises(ValueError):
        ibd(fausse_bio(), annee_reference=1975)


# ======================================================================
# 3. L'agrégation — et le piège du rebouchage silencieux
# ======================================================================

def test_ied_est_bien_la_moyenne_geometrique():
    d = pd.DataFrame({"IRNR": [0.8], "IEE": [0.2], "IBD": [0.5]})
    assert ied(d).iloc[0] == pytest.approx((0.8 * 0.2 * 0.5) ** (1 / 3))


def test_ied_s_annule_si_un_seul_indicateur_s_annule():
    """La contrepartie assumée de la moyenne géométrique (décision D6)."""
    d = pd.DataFrame({"IRNR": [1.5], "IEE": [0.0], "IBD": [1.8]})
    assert ied(d).iloc[0] == 0.0


def test_ied_refuse_de_reboucher_un_indicateur_manquant():
    """Le piège corrigé en cours de route : si l'empreinte carbone manque
    (elle est publiée avec deux ans de retard), l'ignorer reviendrait à
    la remplacer par « tout va bien » et produirait un IED flatteur.
    L'IED doit valoir NaN, pas 1,06."""
    d = pd.DataFrame({"IRNR": [1.06, 0.9], "IEE": [np.nan, 0.3],
                      "IBD": [0.6, 0.6]}, index=[2023, 2022])
    r = ied(d)
    assert np.isnan(r.loc[2023])
    assert r.loc[2022] == pytest.approx((0.9 * 0.3 * 0.6) ** (1 / 3))


def test_assembler_publie_les_deux_ied():
    """On publie l'IED à trois et à deux indicateurs : l'écart mesure
    exactement ce que le maillon faible fait au résultat."""
    dmc, pop, co2, bio = faux_dmc(), fausse_pop(), faux_co2(), fausse_bio()
    t = assembler(irnr(dmc, pop), iee(co2), ibd(bio))
    assert {"IRNR", "IEE", "IBD", "IED", "IED_sans_IBD"} <= set(t.columns)
    assert t["IED"].notna().all()
    assert not np.allclose(t["IED"], t["IED_sans_IBD"])


def test_tous_les_indicateurs_restent_dans_les_bornes():
    dmc, pop, co2, bio = faux_dmc(), fausse_pop(), faux_co2(), fausse_bio()
    for nom in MAPPINGS:
        t = assembler(irnr(dmc, pop, mapping=nom), iee(co2, mapping=nom),
                      ibd(bio, mapping=nom))
        for c in ("IRNR", "IEE", "IBD", "IED"):
            assert t[c].min() >= 0.0, (nom, c)
            assert t[c].max() <= BORNE_HAUTE + 1e-12, (nom, c)


# ======================================================================
# 4. Calibration sur les comptes du Global Footprint Network
# ======================================================================

def test_seuil_calibre_gfn_reproduit_le_ratio_gfn():
    """Le seuil calibré doit, par construction, faire coïncider notre
    rapport de pression avec celui du GFN pour l'année d'ancrage.

    Valeurs France 2013 (GFN, National Footprint Accounts 2017 Public
    Data Package) : empreinte de consommation 5,063 gha/pers, biocapacité
    2,910 gha/pers, donc un rapport de 1,740.
    """
    empreinte_gfn, biocapacite_gfn = 5.06279562828119, 2.91042466596524
    ratio_gfn = empreinte_gfn / biocapacite_gfn
    co2_hab_2013 = 7.2599   # tCO₂/hab, Global Carbon Project

    seuil = co2_hab_2013 / ratio_gfn
    assert co2_hab_2013 / seuil == pytest.approx(ratio_gfn)
    # le seuil calibré tombe dans la fourchette 1-4 t déjà déclarée en
    # sensibilité dans la fiche EQ-EXEC-002 — il en désigne le bord haut
    assert 3.5 < seuil < 4.5


def test_le_seuil_giec_est_environ_deux_fois_plus_severe_que_le_gfn():
    """Constat central de la validation : les deux référentiels diffèrent
    d'un facteur ~2, soit plus que l'écart entre deux mappings. Ce test
    fige le résultat pour qu'une régression silencieuse soit visible."""
    ratio_gfn = 5.06279562828119 / 2.91042466596524
    ratio_proxy = 7.2599 / SEUIL_CO2_T_HAB
    assert ratio_proxy / ratio_gfn == pytest.approx(1.96, abs=0.05)


def test_le_carbone_est_dominant_mais_pas_ecrasant():
    """L'approximation carbone repose sur l'hypothèse « le carbone domine
    l'empreinte écologique ». Vérifié sur la France 2013 : 56 %.
    Dominant, oui ; mais l'approximation laisse tomber 44 % du sujet."""
    part = 2.85153448374666 / 5.06279562828119
    assert 0.50 < part < 0.60
