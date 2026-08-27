# Prompt de reprise — à coller dans une nouvelle fenêtre

> Ce fichier est le point d'entrée d'une nouvelle session. Le mettre à
> jour en fin de chaque session de travail.
> Dernière mise à jour : 2026-08-27 (fin de session 2).

---

```
Nous modélisons en système dynamique l'économie homéostatique (EH), la
théorie macro-économique bio-inspirée d'Ex Naturae (Albouy, Hairy,
Lavilley, 2020). Je suis Stéphane Hairy, un des co-auteurs.

Le dépôt est déjà cadré. Commence par lire, dans cet ordre :
  1. CLAUDE.md                    — règles de travail. La règle n°1 est
                                    non négociable : toujours vulgariser,
                                    toujours être concis.
  2. docs/04-decisions.md         — les 6 décisions de cadrage actées
  3. TODO.md                      — l'état des tâches et les verrous
  4. JOURNAL.md                   — ce qui a été fait et pourquoi
  5. docs/02-strategie-modelisation.md — la stratégie d'ensemble
  6. docs/03-protocole-rigueur.md — comment on justifie chaque équation

Branche de travail : claude/homeostatic-economy-model-f7kcbq
Développe dessus, commite, pousse. Ne crée pas de pull request sauf
demande explicite.

CE QUI EST DÉJÀ EN PLACE (ne pas refaire)
- Documentation complète de l'EH (docs/01), stratégie (docs/02),
  protocole de rigueur (docs/03), décisions (docs/04).
- Clients de données INSEE / Eurostat / BCE dans modele/donnees/.
  pandasdmx est volontairement écarté : sa v1.10 ne parse pas les
  structures INSEE. Attention, le code pays INSEE est FE, pas FR.
- Cache reproductible avec SHA-256, horodatage et détection des
  révisions de séries (modele/donnees/cache.py + donnees/manifeste.json).
- Registre d'équations avec contrôle automatique (modele/registre.py,
  tests/test_registre.py) : une fiche de catégorie D ne peut pas être
  marquée empirique, une fiche de catégorie S sans réplication est
  refusée. La CI échoue si le registre n'est pas conforme.
- Audit de couverture des données : docs/annexes/couverture-donnees.md
  (regénérable par scripts/audit_couverture.py).

Vérifie que tout tourne : `python -m pytest -q` doit être vert.

TA MISSION, DANS CET ORDRE

【A】 VERROU P0 — Reconstruire la formule DENT (dividende des entreprises)

  Je t'informe que la formule DENT de la synthèse (§11.1) a été construite
  au doigt mouillé. Elle n'est pas fiable. Or DTENT pèse plus de la moitié
  de la création monétaire totale : cette formule décide seule de
  l'essentiel des résultats chiffrés. Rien de quantitatif n'est publiable
  tant qu'elle n'est pas arbitrée.

  Formule actuelle :  DENT = IED × P + (e × DCIT) / ((r/e) × 10⁴)
    P = produit d'exploitation de référence (moyenne des 3 meilleures
        années, réactualisé tous les ~3 ans)
    e = nombre de salariés
    r = écart entre le plus haut salaire de l'entreprise et DCIT

  À faire :
  1. Analyse critique de la formule telle qu'elle est écrite :
     - le terme (e × DCIT) / ((r/e) × 10⁴) est-il homogène à des euros ?
     - que vaut-il quand r → 0 (aucun écart de salaire) ? division par zéro ?
     - la règle « moyenne des 3 meilleures années » crée-t-elle un cliquet
       et un biais haussier auto-amplifiant ? (c'est une rétroaction
       positive dans un modèle qui prétend n'en avoir aucune)
  2. Clarifier le périmètre « entreprise » : SNF seules ? sociétés
     financières ? entrepreneurs individuels ? micro-entreprises ?
     Chiffre-le sur données françaises réelles.
  3. Clarifier P : produit d'exploitation comptable (proche du chiffre
     d'affaires) ou production au sens des comptes nationaux ?
     Repère sourcé : production des SNF françaises 2023 = 3 810 Md€
     (Eurostat nasa_10_nf_tr, S11/P1/RECV, série depuis 1971).
  4. Proposer 2 ou 3 formules alternatives explicites, chacune avec son
     intention, ses propriétés (bornes, monotonie, comportement aux
     limites) et sa fiche de registre en catégorie D avec plan de
     sensibilité. Ne tranche pas seul : présente-moi les options.

【B】 JALON P2 — Reconstituer les indicateurs EXEC de la France, 1978–2023

  C'est le livrable phare et le verrou n°1 du projet. La synthèse ne donne
  AUCUNE formule pour IBD, IEE et IRNR : il faut les créer.

  Contraintes : chaque indicateur vaut 1 à l'équilibre, est borné sur
  [0 ; 2], et se calcule à partir de données publiques annuelles.

  1. IEE  — empreinte écologique, importations incluses (exigence de la
            synthèse §14.1, donc il faut une approche multi-régionale
            type EXIOBASE ou Global Footprint Network)
  2. IRNR — ressources non renouvelables ; le recyclage compte
            positivement. Piste : Eurostat env_ac_mfa (DMC, depuis 1990)
  3. IBD  — biodiversité. LE PLUS DIFFICILE. Les données peuvent ne pas
            suffire. Si c'est le cas, dis-le et documente le trou plutôt
            que de combler au jugé (RÈGLE N°3).
  4. Le mapping vers [0 ; 2] est un choix normatif structurant (linéaire ?
     logarithmique ? plafonné ?). Il changera radicalement la dynamique.
     Présente-moi les options avant de choisir.
  5. Une fois les indicateurs calculés : IED = (IBD × IEE × IRNR)^(1/3),
     puis la courbe « quelle création monétaire l'EH aurait-elle donnée à
     la France depuis 1978 ? ». C'est le graphique que j'attends.

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
- Mets à jour JOURNAL.md et TODO.md en fin de session, et regénère ce
  fichier (docs/PROMPT-SUITE.md) pour la session suivante.
```

---

## Aide-mémoire (hors prompt)

**État au 2026-08-27** — jalons P0 fait, P2 à faire.

| Verrou | Gravité |
|---|---|
| Formule DENT non fiable (aveu de l'auteur) | **P0 — bloque tout résultat chiffré** |
| Aucune formule pour IBD / IEE / IRNR | **P0 — bloque toute simulation** |
| Données de biodiversité peut-être insuffisantes | Élevée |
| Taux de change « à développer » (synthèse §15) | Moyenne, non bloquante à ce stade |

**Résultat provisoire à ne pas sur-interpréter** : à paramètres inchangés,
l'EH converge vers une masse monétaire de 14 à 21 × PIB, contre ≈ 1,1 ×
aujourd'hui. Robuste à la fourchette de DTENT, **pas** à la formule DENT.
