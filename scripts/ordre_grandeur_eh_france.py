"""
Calcul d'ordre de grandeur : que donneraient les formules de création
monétaire de l'EH appliquées à la France ?

⚠️ Calcul ILLUSTRATIF. Les entrées marquées [À VÉRIFIER] doivent être
remplacées par des données sourcées (INSEE, Banque de France) avant toute
utilisation. Objectif : montrer pourquoi la modélisation est nécessaire.

Source des formules : Synthèse EH v1.7 (oct. 2020), §11.1 et §10.3.
"""

# --- Entrées -----------------------------------------------------------
c            = 68.1e6      # habitants France 2023 (INSEE)            [À VÉRIFIER]
PIB          = 2_833.826e9 # PIB France 2023, € courants — VÉRIFIÉ :
                           # INSEE CNA-2020-PIB, 2 833 826 M€
                           # (scripts/audit_couverture.py)
M3_FR        = 3_000e9     # contribution française à M3, en €        [À VÉRIFIER]
PROD_EXPL    = 4_000e9     # produits d'exploitation cumulés des
                           # entreprises françaises, en €             [À VÉRIFIER]
IED          = 1.0         # indicateur d'équilibre dynamique à l'optimum
BASE_DETA    = 22_000      # € / citoyen (constante fixée par l'EH)
FONTE_MENS   = 0.01        # 1 % / mois sur tous les soldes
FONTE_TRANS  = 0.01        # 1 % sur chaque transaction
VITESSE      = 3.0         # transactions annuelles / stock de monnaie [À VÉRIFIER]

# --- Création monétaire annuelle (§11.1) -------------------------------
DETA  = IED * BASE_DETA * c        # dividende de l'État
DTCIT = DETA                       # dividende total des citoyens
DCIT  = DETA / c                   # dividende par citoyen
DTENT = IED * PROD_EXPL            # dividende des entreprises (terme dominant)
DG_FR = DETA + DTCIT + DTENT       # dividende global de la zone France

# --- Destruction monétaire annuelle par la fonte (§10.3) ---------------
fonte_annuelle_stock = 1 - (1 - FONTE_MENS) ** 12   # ~11,4 % / an

# Équilibre : création annuelle = destruction annuelle
#   DG = f_stock * M + f_trans * (VITESSE * M)
M_equilibre = DG_FR / (fonte_annuelle_stock + FONTE_TRANS * VITESSE)

# --- Sortie ------------------------------------------------------------
Md = 1e9
print(f"Population                        : {c/1e6:>8.1f} M hab.")
print(f"PIB de référence                  : {PIB/Md:>8.0f} Md€")
print()
print("CRÉATION MONÉTAIRE ANNUELLE (IED = 1)")
print(f"  DETA  (État)                    : {DETA/Md:>8.0f} Md€")
print(f"  DTCIT (citoyens)                : {DTCIT/Md:>8.0f} Md€")
print(f"  DCIT  (par citoyen)             : {DCIT:>8.0f} €/an "
      f"= {DCIT/12:.0f} €/mois")
print(f"  DTENT (entreprises)             : {DTENT/Md:>8.0f} Md€")
print(f"  DG_FR (total)                   : {DG_FR/Md:>8.0f} Md€ "
      f"= {DG_FR/PIB:.2f} x PIB")
print()
print("DESTRUCTION PAR LA FONTE")
print(f"  Taux annuel équivalent (soldes) : {fonte_annuelle_stock*100:>8.2f} %")
print()
print("ÉTAT STATIONNAIRE (création = destruction)")
print(f"  Masse monétaire d'équilibre     : {M_equilibre/Md:>8.0f} Md€")
print(f"                                  : {M_equilibre/PIB:>8.1f} x PIB")
print(f"  Comparaison M3 France actuel    : {M3_FR/Md:>8.0f} Md€ "
      f"({M3_FR/PIB:.2f} x PIB)")
print(f"  Rapport EH / actuel             : {M_equilibre/M3_FR:>8.1f} x")
