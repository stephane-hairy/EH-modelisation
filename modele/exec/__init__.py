"""Indicateurs EXEC — le « capteur » du thermostat de l'économie homéostatique.

Trois indicateurs (IBD biodiversité, IEE empreinte écologique, IRNR
ressources non renouvelables) valant 1 à l'équilibre et bornés sur
[0 ; 2], agrégés en IED = (IBD × IEE × IRNR)^(1/3).

⚠️ La synthèse EH ne donne **aucune formule** pour ces trois indicateurs.
Tout ce qui est ici a été créé pour ce projet : c'est de la **catégorie D**
(choix normatif), à passer en sensibilité, jamais à présenter comme une
mesure objective.
"""
