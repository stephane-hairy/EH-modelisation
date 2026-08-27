# Schéma d'une fiche d'équation

Un fichier YAML par équation, nommé `EQ-<BLOC>-<NNN>.yaml`.
Blocs : `MEN` (ménages), `SNF`, `BAN` (banques), `BCE`, `APU`, `EXT`
(extérieur), `EMP` (emploi), `PRI` (prix), `ECO` (écologie),
`EXEC` (indicateurs EH), `EH` (mécanismes EH).

```yaml
id: EQ-XXX-000                # obligatoire, unique
nom: ...                      # nom court en français
description: ...              # 1-2 phrases, VULGARISÉES
formule: "..."                # notation lisible
variables:                    # chaque symbole expliqué + unité + source
  X: {sens: ..., unite: ..., source: ...}
parametres:
  a: {valeur: ..., intervalle: [..., ...], origine: estime|calibre|design}

categorie: I | C | S | D      # obligatoire (cf. docs/03)
grade: A | B | C | D          # obligatoire
empirique: true | false       # obligatoire

sources:                      # >= 1 sauf catégorie I
  - {ref: ..., doi_ou_url: ..., ce_qu_elle_etablit: ...}

estimation:                   # obligatoire si categorie == S
  methode: ...
  donnees: ...
  periode: ...
  stationnarite: ...
  cointegration: ...
  r2: ...
  stabilite: ...
  script: chemin/vers/test.py

limites: |                    # obligatoire : ce qu'on ne sait pas
  ...

sensibilite:                  # obligatoire si categorie == D
  balayage: [..., ...]
  impact_attendu: ...

couche: A | B | C             # positive | design | transmission
statut: brouillon | valide | rejete
maj: AAAA-MM-JJ
```
