# Couverture des données — jusqu'où peut-on remonter ?

> Généré par `scripts/audit_couverture.py` le 2026-08-27.
> Ne pas modifier à la main : relancer le script.

| Bloc | Série | Fréquence | Début | Fin | Obs. |
|---|---|---|---|---|---|
| Réel | PIB, euros courants (INSEE CNA-2020-PIB) | annuelle | **1949** | 2025 | 77 |
| Réel | PIB (Eurostat nama_10_gdp) | annuelle | **1975** | 2025 | 51 |
| Financier | Comptes financiers, SNF crédits F4 (INSEE CNA-2014-TOF) | annuelle | **1995** | 2021 | 27 |
| Financier | Comptes financiers ménages, dépôts F2 (BCE QSA) | trimestrielle | **1998-Q4** | 2026-Q1 | 110 |
| Monétaire | Crédits des IFM au secteur privé, France (BCE BSI) | mensuelle | **2003-01** | 2026-07 | 283 |
| Écologie | Émissions de GES (Eurostat env_ac_ainah_r2) | annuelle | **2008** | 2024 | 17 |
| Écologie | Inventaire GES national (Eurostat env_air_gge) | annuelle | **1990** | 2024 | 35 |
| Écologie | Consommation intérieure de matières (Eurostat env_ac_mfa) | annuelle | **1990** | 2025 | 36 |

## Ce que ça implique

- L'**économie réelle** (PIB et agrégats) remonte à **1949**.
- Les **comptes financiers par secteur** — qui détient quoi, la
  colonne vertébrale d'un modèle Stock-Flux Cohérent — ne commencent
  qu'en **1995** (annuel INSEE) ou **1998-Q4** (trimestriel BCE).
  C'est la contrainte qui décide de la période de départ.
- L'**écologie** : matières depuis 1990, inventaire national des gaz à
  effet de serre depuis 1990, mais les *comptes d'émissions par
  branche* (ceux qu'il faut pour relier émissions et production)
  seulement depuis 2008.
- Le **mensuel** n'existe que pour la monnaie, le crédit et les prix.
  Il n'existe aucune donnée mensuelle de PIB, d'investissement ou de
  patrimoine sectoriel : un modèle mensuel complet est impossible à
  caler sur données françaises.
