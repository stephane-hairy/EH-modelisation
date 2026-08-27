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
                                     SEUIL_MATIERE_T_HAB, assembler, ibd,
                                     ied, iee, irnr, irnr_empreinte,
                                     mapping_exponentiel, mapping_hyperbolique,
                                     mapping_lineaire)

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

# Chiffres France 2013, Global Footprint Network, National Footprint
# Accounts 2017 Public Data Package (gha par personne).
GFN_EMPREINTE = 5.06279562828119
GFN_CARBONE = 2.85153448374666
GFN_BIOCAP_FRANCE = 2.91042466596524
GFN_RATIO_MONDIAL = 2.96886710450647      # « nombre de Terres »  — étalon retenu (D13)
GFN_RATIO_TERRITORIAL = 1.73953845549963  # « nombre de pays »    — écarté (D13)
CO2_HAB_2013 = 7.2599                     # tCO₂/hab, Global Carbon Project


def test_les_deux_etalons_gfn_different_d_un_facteur_deux():
    """Le GFN publie deux façons de rapporter l'empreinte à un seuil, et
    elles ne disent pas la même chose. C'est le choix tranché par D13."""
    assert GFN_RATIO_MONDIAL / GFN_RATIO_TERRITORIAL == pytest.approx(1.71,
                                                                      abs=0.02)


def test_l_etalon_territorial_recompenserait_la_geographie():
    """Pourquoi D13 a écarté l'étalon territorial : l'Australie consomme
    74 % de nature de plus que la France, et serait pourtant bien mieux
    notée, parce qu'elle a de l'espace. Incitation perverse pour une
    théorie qui prétend récompenser la vertu écologique."""
    australie_empreinte, australie_biocap = 8.80246730610426, 15.6667670253919
    assert australie_empreinte / GFN_EMPREINTE == pytest.approx(1.74, abs=0.02)

    iee_fr = mapping_exponentiel(GFN_EMPREINTE / GFN_BIOCAP_FRANCE)
    iee_au = mapping_exponentiel(australie_empreinte / australie_biocap)
    assert iee_au > 2 * iee_fr          # l'Australie récompensée du double

    # sous l'étalon mondial, l'ordre s'inverse — et c'est le bon sens
    biocap_monde = GFN_EMPREINTE / GFN_RATIO_MONDIAL
    assert mapping_exponentiel(australie_empreinte / biocap_monde) < \
        mapping_exponentiel(GFN_EMPREINTE / biocap_monde)


def test_notre_approximation_carbone_tient_a_15_pourcent():
    """Résultat central de la validation : sur l'étalon retenu (mondial),
    l'approximation carbone ne surestime la pression que de 15 %.

    C'est la raison pour laquelle le jalon P2 n'a pas eu à être refait.
    Une régression silencieuse de ce chiffre voudrait dire qu'on a cassé
    la conversion d'unité ou changé le seuil sans le documenter."""
    ratio_proxy = CO2_HAB_2013 / SEUIL_CO2_T_HAB
    assert ratio_proxy / GFN_RATIO_MONDIAL == pytest.approx(1.15, abs=0.03)


def test_seuil_recale_sur_l_etalon_mondial():
    """Le seuil qui ferait coïncider exactement notre série avec le GFN
    en 2013 vaut 2,44 t — un ajustement de 15 %, bien à l'intérieur de la
    fourchette 1–4 t déclarée en sensibilité (fiche EQ-EXEC-002)."""
    seuil = CO2_HAB_2013 / GFN_RATIO_MONDIAL
    assert CO2_HAB_2013 / seuil == pytest.approx(GFN_RATIO_MONDIAL)
    assert seuil == pytest.approx(2.44, abs=0.05)
    assert 1.0 < seuil < 4.0


def test_le_recalage_ne_change_pas_les_conclusions():
    """Le déplacement de l'IEE dû au recalage est mineur : l'IED français
    reste très en dessous de 1. C'est ce qui a permis de ne pas refaire
    le jalon P2."""
    avant = mapping_exponentiel(CO2_HAB_2013 / SEUIL_CO2_T_HAB)
    apres = mapping_exponentiel(GFN_RATIO_MONDIAL)
    assert abs(apres - avant) < 0.10
    assert avant < 0.5 and apres < 0.5


def test_le_carbone_est_dominant_mais_pas_ecrasant():
    """L'approximation carbone repose sur l'hypothèse « le carbone domine
    l'empreinte écologique ». Vérifié sur la France 2013 : 56 %.
    Dominant, oui ; mais l'approximation laisse tomber 44 % du sujet."""
    part = GFN_CARBONE / GFN_EMPREINTE
    assert 0.50 < part < 0.60


# ======================================================================
# 5. IRNR en empreinte — la correction du biais territorial
# ======================================================================

# Chiffres France, matières non renouvelables, t/hab/an.
# territorial : Eurostat env_ac_mfa (DMC) · empreinte : EXIOBASE 3.10.2
IRNR_TERRITORIAL = {1995: 9.99, 2010: 8.44, 2022: 7.77, 2023: 7.35}
IRNR_EMPREINTE = {1995: 9.58, 2010: 13.34, 2022: 12.12, 2023: 13.20}


def test_les_deux_mesures_de_matiere_vont_en_sens_contraire():
    """Le résultat central de l'intégration d'EXIOBASE, et le plus
    dérangeant : entre 1995 et 2022, le DMC territorial BAISSE de 22 %
    tandis que l'empreinte MONTE de 26 %.

    L'« amélioration » que mesurait l'IRNR était pour l'essentiel un
    déménagement. Si ce test tombe un jour, c'est que les données ou le
    calcul ont changé — pas que la conclusion s'est adoucie."""
    terr = IRNR_TERRITORIAL[2022] / IRNR_TERRITORIAL[1995] - 1
    emp = IRNR_EMPREINTE[2022] / IRNR_EMPREINTE[1995] - 1
    assert terr < 0, "le territorial doit baisser"
    assert emp > 0, "l'empreinte doit monter"
    assert terr == pytest.approx(-0.22, abs=0.02)
    assert emp == pytest.approx(+0.26, abs=0.02)


def test_le_biais_d_importation_grandit_avec_le_temps():
    """Signature de la délocalisation : l'écart entre les deux mesures
    passe de −4 % en 1995 à +80 % en 2023."""
    def ecart(a):
        return IRNR_EMPREINTE[a] / IRNR_TERRITORIAL[a] - 1
    assert ecart(1995) == pytest.approx(-0.04, abs=0.02)
    assert ecart(2023) == pytest.approx(+0.80, abs=0.03)
    assert ecart(1995) < ecart(2010) < ecart(2023)


def test_en_empreinte_la_france_ne_passe_jamais_sous_le_seuil():
    """En territorial, la France franchit le seuil de 8 t/hab vers 2014,
    ce qui faisait de l'IRNR le seul indicateur à atteindre l'équilibre.
    En empreinte, elle reste au-dessus sur toute la période."""
    assert IRNR_TERRITORIAL[2022] < SEUIL_MATIERE_T_HAB
    assert all(v > SEUIL_MATIERE_T_HAB for v in IRNR_EMPREINTE.values())


def test_irnr_empreinte_a_les_memes_proprietes_que_irnr():
    """La correction ne doit rien casser : bornes, monotonie, valeur 1 au
    seuil."""
    d = pd.DataFrame({"mat_non_renouv_t_hab": [4.0, 8.0, 16.0, 24.0]},
                     index=[2000, 2001, 2002, 2003])
    r = irnr_empreinte(d)
    assert r["indice"].loc[2001] == pytest.approx(1.0)   # pile au seuil
    assert r["indice"].is_monotonic_decreasing
    assert r["indice"].min() >= 0.0
    assert r["indice"].max() <= BORNE_HAUTE


def test_irnr_empreinte_est_plus_severe_que_le_territorial():
    """À seuil identique, l'empreinte donne un indicateur plus bas —
    parce qu'elle voit la matière que le territorial ignore."""
    for a in (2010, 2022, 2023):
        i_terr = mapping_exponentiel(IRNR_TERRITORIAL[a] / SEUIL_MATIERE_T_HAB)
        i_emp = mapping_exponentiel(IRNR_EMPREINTE[a] / SEUIL_MATIERE_T_HAB)
        assert i_emp < i_terr, a
