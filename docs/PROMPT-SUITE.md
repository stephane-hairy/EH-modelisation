# Prompt de reprise — session suivante

> À copier-coller tel quel pour reprendre le travail.
> Régénéré le 2026-08-27, fin de session 3.

---

```
Nous modélisons en système dynamique l'économie homéostatique (EH), la
théorie macro-économique bio-inspirée d'Ex Naturae (Albouy, Hairy,
Lavilley, 2020). Je suis Stéphane Hairy, un des co-auteurs.

Le dépôt est déjà bien avancé. Commence par lire, dans cet ordre :
  1. CLAUDE.md                  — règles de travail. La règle n°1 est
                                  non négociable : toujours vulgariser,
                                  toujours être concis.
  2. docs/04-decisions.md       — les 6 décisions de cadrage actées
  3. TODO.md                    — état des tâches, et les 7 décisions
                                  en attente (D7–D13)
  4. JOURNAL.md                 — session 3 en particulier
  5. docs/05-dent.md            — l'analyse critique de DENT
  6. docs/06-indicateurs-exec.md — les indicateurs EXEC et leurs trous

Branche de travail : claude/homeostatic-economy-model-f7kcbq
Développe dessus, commite, pousse. Pas de pull request sauf demande.

Vérifie que tout tourne : `python -m pytest -q` doit être vert (64 tests).

CE QUI EST DÉJÀ FAIT (ne pas refaire)
- Documentation EH, stratégie, protocole de rigueur, décisions (docs/01-04)
- Clients de données INSEE / Eurostat / BCE + comptes nationaux +
  séries écologiques, tous avec cache SHA-256 reproductible
- Registre d'équations à contrôle automatique (11 fiches, CI verte)
- VERROU DENT LEVÉ : six défauts démontrés, trois alternatives fichées
  (docs/05-dent.md). pandasdmx reste écarté. Code pays INSEE = FE.
- JALON P2 LIVRÉ : indicateurs EXEC de la France 1990–2021, IED, et la
  courbe de création monétaire (sorties/creation_monetaire_eh_france.png)

⚠️ CE QUI BLOQUE : SEPT DÉCISIONS M'APPARTIENNENT
Tant que D7–D13 ne sont pas tranchées, aucun résultat quantitatif sur la
masse monétaire en EH n'est publiable. Si je ne te les ai pas données
dans ce message, DEMANDE-LES-MOI avant de calculer quoi que ce soit.

  D7  assiette de DENT      production (3 810 Md€) ou valeur ajoutée
                            (1 481 Md€) — facteur 2,6
  D8  forme de DENT         alternative 1 / 2 / 3 / combinaison
  D9  périmètre entreprise  SNF / +finance / +entrepreneurs individuels
  D10 base P                3 meilleures années / moyenne glissante /
                            grandeur exogène
  D11 mapping vers [0 ; 2]  linéaire / hyperbolique / exponentiel
                            → IED 2021 de 0,00 à 0,72
  D12 sort de l'IBD         garder en grade C / paramètre libre / retirer
  D13 seuils                carbone 1–4 t/hab · matières 6–12 t/hab

TA MISSION, DANS CET ORDRE

【A】 Une fois D7–D13 tranchées : figer les formules retenues, regénérer
     la courbe de création monétaire, et publier la sensibilité complète
     aux décisions écartées. Les fiches de registre existent déjà : il
     s'agit de passer les fiches retenues en statut `valide` et les
     autres en `rejete`, en gardant la trace.

【B】 JALON P5 — analyse de stabilité de la boucle EH.
     C'est probablement la contribution scientifique la plus forte du
     projet, et le prochain gros morceau.
     - Linéariser la boucle EXEC ↔ ENEC autour de IED = 1.
     - Le gain proportionnel du régulateur est la PENTE DU MAPPING en
       x = 1 : −1,00 (linéaire), −0,50 (hyperbolique), −0,69 (exponentiel).
       C'est pourquoi D11 doit être tranchée avant.
     - Les délais écologiques sont de 3 à 10 ans, les indicateurs sont
       annuels : c'est la configuration type d'une boucle qui OSCILLE au
       lieu de converger (Sterman 2000, ch. 17). La synthèse affirme la
       stabilité (§10.1) sans la démontrer.
     - Livrable : valeurs propres, marge de phase, cartographie
       (gain × délai) des zones stable / oscillante / divergente.
     - Si c'est instable, C'EST UN RÉSULTAT, pas un échec. Proposer des
       correctifs documentés (IED lissé, terme dérivé — un régulateur PID
       plutôt que proportionnel).

【C】 P1 — demander/obtenir une clé d'API Global Footprint Network.
     C'est la SEULE action qui pourrait rouvrir la période 1978–1989 :
     les comptes GFN remontent à 1961, et remplaceraient l'approximation
     carbone par la vraie empreinte écologique. Si tu ne peux pas
     l'obtenir toi-même, dis-le-moi, je la demanderai.

【D】 Puis JALON P1 — le modèle SFC France proprement dit (voir TODO.md).

RAPPELS QUI COMPTENT
- Vulgarise toujours. Sois toujours concis. C'est la règle n°1.
- Aucune équation sans fiche de traçabilité dans modele/registre/.
- N'invente jamais une valeur numérique plausible. Un chiffre non vérifié
  se marque [À VÉRIFIER].
- Ne présente jamais une règle de conception de l'EH comme empiriquement
  fondée. Ce sont des choix, à passer en sensibilité.
- Pas de régression de niveaux sur séries non stationnaires sans test de
  cointégration.
- Si une relation manque, documente le trou. Ne le comble pas au jugé.
- ⚠️ LEÇON DE LA SESSION 3 : les bugs de ce projet ne font pas planter le
  programme, ils rendent la France plus verte qu'elle n'est. Deux ont été
  trouvés (erreur d'unité sur l'empreinte carbone ; rebouchage silencieux
  d'un indicateur manquant, qui donnait IED = 1,06 pour 2023). Cherche-les
  activement, ne les attends pas.
- Mets à jour JOURNAL.md et TODO.md en fin de session, et regénère ce
  fichier (docs/PROMPT-SUITE.md) pour la session suivante.
```

---

## Aide-mémoire — l'état chiffré du dépôt

### Ce qui est sourcé et vérifié

| Grandeur | Valeur | Source |
|---|---|---|
| PIB France 2023 | 2 833,8 Md€ | INSEE CNA-2020-PIB |
| Production SNF 2023 | 3 810,2 Md€ | Eurostat `nasa_10_nf_tr` (1971–2024) |
| Valeur ajoutée SNF 2023 | 1 481,1 Md€ | idem |
| Production sociétés financières | 287,7 Md€ | idem |
| Production économie totale | 5 310,0 Md€ | idem |
| Entreprises France 2022 | 4 906 972 | Eurostat `sbs_sc_ovw` |
| … dont 0–9 personnes | 4 718 929 (96,2 %) | idem |
| Empreinte carbone 2022 | 6,16 tCO₂/hab | Global Carbon Project |
| Matière non renouvelable 2022 | 7,8 t/hab | Eurostat `env_ac_mfa` |
| Oiseaux agricoles 1990→2021 | 93 → 54 (−42 %) | Eurostat `env_bio2` |

### Les trous documentés, à ne pas combler au jugé

| Trou | Raison |
|---|---|
| Écologie avant **1990** | Les trois séries commencent en 1990 |
| Empreinte carbone après **2022** | Publication à deux ans de retard |
| Oiseaux après **2021** | Série arrêtée |
| Année **2000** des oiseaux | Rupture de série (100,0 entre 69,5 et 72,7) |
| Empreinte écologique GFN | API à clé nominative (403) |
| Biodiversité importations incluses | N'existe pas en accès ouvert |
| Comptes financiers avant **1995** | Bloque le SFC bouclé (décision D5) |

### Les fiches de registre

| Fiche | Objet | Statut |
|---|---|---|
| `EQ-EMP-001` | Loi d'Okun (exemple) | brouillon |
| `EQ-EH-001` | DENT §11.1 telle quelle | **rejete** |
| `EQ-EH-002` | DENT alt. 1 — multiplicative | brouillon |
| `EQ-EH-003` | DENT alt. 2 — deux termes | brouillon |
| `EQ-EH-004` | DENT alt. 3 — valeur ajoutée | brouillon |
| `EQ-EH-005` | Base `P` — 3 meilleures années | brouillon |
| `EQ-EXEC-001` | IRNR | brouillon |
| `EQ-EXEC-002` | IEE | brouillon |
| `EQ-EXEC-003` | IBD (bouche-trou) | brouillon |
| `EQ-EXEC-004` | Mapping vers [0 ; 2] | brouillon |
| `EQ-EXEC-005` | IED — moyenne géométrique | brouillon |

### Commandes utiles

```bash
pip install -e ".[dev]"                        # installation
python -m pytest -q                            # 64 tests
python scripts/analyse_dent.py                 # l'analyse critique de DENT
python scripts/construire_exec.py              # les indicateurs EXEC
python scripts/courbe_creation_monetaire.py    # le graphique phare
python scripts/audit_couverture.py             # couverture des données
```
