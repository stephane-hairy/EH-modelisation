"""
Calcul d'ordre de grandeur : que donneraient les formules de création
monétaire de l'EH appliquées à la France ?

⚠️ AVERTISSEMENT MAJEUR — lire avant d'utiliser un seul de ces chiffres.

La formule du dividende des entreprises (DENT, §11.1 de la synthèse) a été
construite « au doigt mouillé » — de l'aveu même d'un de ses auteurs
(Stéphane Hairy, 2026-08-27). Or c'est **elle qui domine entièrement le
résultat** : DTENT pèse à lui seul plus de la moitié de la création
monétaire totale, et donc l'essentiel de la masse monétaire d'équilibre.

Conclusion à retenir : le chiffre de sortie n'est **pas** une propriété
de l'économie homéostatique. C'est une propriété d'une formule provisoire.
Le calcul sert à montrer l'ampleur de l'enjeu, pas à évaluer la théorie.

Source des formules : Synthèse EH v1.7 (oct. 2020), §11.1 et §10.3.
"""

# --- Entrées ---------------------------------------------------------------
# VÉRIFIÉES (scripts/audit_couverture.py)
c         = 68.1e6        # habitants France 2023 (INSEE)            [À VÉRIFIER]
PIB       = 2_833.826e9   # PIB France 2023, € courants — INSEE CNA-2020-PIB
P1_SNF    = 3_810.239e9   # Production des sociétés non financières 2023,
                          # € courants — Eurostat nasa_10_nf_tr (S11, P1, RECV)

# NON VÉRIFIÉES
M3_FR     = 3_000e9       # contribution française à M3, en €        [À VÉRIFIER]

# Constantes de conception de l'EH (catégorie D — non empiriques)
IED         = 1.0         # indicateur d'équilibre dynamique à l'optimum
BASE_DETA   = 22_000      # € / citoyen (constante fixée par l'EH)
FONTE_MENS  = 0.01        # 1 % / mois sur tous les soldes
FONTE_TRANS = 0.01        # 1 % sur chaque transaction
VITESSE     = 3.0         # transactions annuelles / stock de monnaie [À VÉRIFIER]

# --- Création monétaire annuelle (§11.1) -----------------------------------
DETA  = IED * BASE_DETA * c        # dividende de l'État
DTCIT = DETA                       # dividende total des citoyens
DCIT  = DETA / c                   # dividende par citoyen

# DTENT : le terme problématique.
# DENT ≈ IED × P, où P est le « produit d'exploitation de référence » d'une
# entreprise, pris sur ses trois meilleures années. Sommé sur toutes les
# entreprises, P s'approche de la production totale — mais :
#   - la synthèse retient les MEILLEURES années, donc plus que l'année en cours ;
#   - le périmètre « entreprises » n'est pas défini (SNF seules ? finance ?
#     entrepreneurs individuels ?) ;
#   - le second terme de DENT (emploi et écarts de salaires) est ignoré ici.
# On ne retient donc PAS un point, mais une fourchette.
DTENT_BAS   = 0.7 * P1_SNF   # périmètre étroit, P sous la production courante
DTENT_CENTR = 1.0 * P1_SNF   # P ≈ production des SNF
DTENT_HAUT  = 1.5 * P1_SNF   # meilleures années + périmètre large

fonte_annuelle_stock = 1 - (1 - FONTE_MENS) ** 12   # ≈ 11,4 % / an


def etat_stationnaire(dtent: float) -> tuple[float, float]:
    """Création annuelle et masse monétaire d'équilibre pour un DTENT donné."""
    dg = DETA + DTCIT + dtent
    # création annuelle = destruction annuelle
    #   DG = f_stock × M + f_transaction × (vitesse × M)
    return dg, dg / (fonte_annuelle_stock + FONTE_TRANS * VITESSE)


if __name__ == "__main__":
    Md = 1e9
    print(f"Population                     : {c/1e6:>9.1f} M hab.")
    print(f"PIB 2023 (INSEE)               : {PIB/Md:>9.0f} Md€")
    print(f"Production des SNF (Eurostat)  : {P1_SNF/Md:>9.0f} Md€"
          f"  = {P1_SNF/PIB:.2f} × PIB")
    print()
    print("CRÉATION MONÉTAIRE ANNUELLE (IED = 1)")
    print(f"  DETA  (État)                 : {DETA/Md:>9.0f} Md€")
    print(f"  DTCIT (citoyens)             : {DTCIT/Md:>9.0f} Md€")
    print(f"  DCIT  (par citoyen)          : {DCIT:>9.0f} €/an"
          f"  = {DCIT/12:.0f} €/mois")
    print(f"  DTENT (entreprises)          :  fourchette, formule non fiable")
    print()
    print(f"Fonte : {fonte_annuelle_stock*100:.2f} %/an sur les soldes"
          f" + {FONTE_TRANS*100:.0f} % par transaction")
    print()
    print("SENSIBILITÉ À DTENT — le paramètre qui décide de tout")
    print(f"  {'hypothèse':<12} {'DTENT':>10} {'création/an':>13} "
          f"{'M équilibre':>13} {'× PIB':>8} {'× M3 actuel':>12}")
    for nom, dtent in (("basse", DTENT_BAS), ("centrale", DTENT_CENTR),
                       ("haute", DTENT_HAUT)):
        dg, m = etat_stationnaire(dtent)
        print(f"  {nom:<12} {dtent/Md:>9.0f}  {dg/Md:>12.0f}  {m/Md:>12.0f} "
              f"{m/PIB:>8.1f} {m/M3_FR:>12.1f}")
    print()
    print("→ Même dans l'hypothèse basse, la masse monétaire d'équilibre reste")
    print("  d'un ordre de grandeur au-dessus de l'actuelle. Le résultat est")
    print("  ROBUSTE à la fourchette de DTENT, mais PAS à la formule DENT")
    print("  elle-même, qui est à reconstruire (cf. TODO.md, verrou).")
