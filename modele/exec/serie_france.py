"""
Assemble les indicateurs EXEC de la France à partir des données brutes.

Séparé des scripts pour être importable et testable. Les scripts
`construire_exec.py` et `courbe_creation_monetaire.py` s'appuient dessus.
"""
from __future__ import annotations

import pandas as pd

from modele.donnees.ecologie import (co2_empreinte, dmc_par_matiere,
                                     empreinte_exiobase, population,
                                     serie_biodiversite, taux_circulaire)
from modele.exec.indicateurs import (assembler, ibd, iee, irnr,
                                     irnr_empreinte)

DEBUT_DEMANDE = 1978   # ce que demande le cadrage (décision D5)


def construire(mapping: str = "exponentiel",
               source_irnr: str = "territorial") -> tuple[pd.DataFrame, dict]:
    """Récupère les données et calcule les trois indicateurs + l'IED.

    `source_irnr` :

    - `"territorial"` — DMC d'Eurostat, **1990–2024**. Ne compte que le
      poids des biens importés, pas la matière remuée à l'étranger pour
      les produire. C'est le défaut historique de l'indicateur.
    - `"empreinte"` — EXIOBASE, **1995–2024**. Importations incluses.
      Conceptuellement juste, mais démarre cinq ans plus tard.

    ⚠️ Le choix n'est pas cosmétique : les deux séries vont **en sens
    contraire** entre 1995 et 2022 (−22 % contre +26 %). Voir
    `modele.exec.indicateurs.irnr_empreinte`.

    Renvoie `(tableau, couverture)` où `couverture` donne, pour chaque
    série source, les années réellement disponibles. C'est ce second
    élément qui permet de dire honnêtement ce qui manque.
    """
    if source_irnr not in {"territorial", "empreinte"}:
        raise ValueError(f"source_irnr inconnue : {source_irnr!r}")
    dmc = dmc_par_matiere()
    co2 = co2_empreinte()
    bio = serie_biodiversite()
    pop = population()

    # La population Eurostat démarre en 1982 ; celle du Global Carbon
    # Project remonte plus loin et complète les années manquantes.
    pop_complete = co2["population"].combine_first(pop).dropna()

    if source_irnr == "empreinte":
        d_irnr = irnr_empreinte(empreinte_exiobase(), mapping=mapping)
    else:
        d_irnr = irnr(dmc, pop_complete, mapping=mapping)
    d_iee = iee(co2, mapping=mapping)
    d_ibd = ibd(bio, mapping=mapping)

    table = assembler(d_irnr, d_iee, d_ibd)
    table["ratio_IRNR"] = d_irnr["ratio"]
    table["ratio_IEE"] = d_iee["ratio"]
    table["ratio_IBD"] = d_ibd["ratio"]
    table["matiere_nr_t_hab"] = d_irnr["pression_t_hab"]
    table["co2_empreinte_t_hab"] = d_iee["pression_t_hab"]
    table["co2_territorial_t_hab"] = (co2["territorial"] * 1e6
                                      / co2["population"])
    table["oiseaux_agricoles"] = d_ibd["indice_oiseaux"]

    couverture = {
        f"Matières ({source_irnr})": d_irnr.dropna().index,
        "CO₂ empreinte": d_iee.dropna().index,
        "Oiseaux agricoles": d_ibd["indice_oiseaux"].dropna().index,
        "Taux circulaire": taux_circulaire().index,
    }
    return table, couverture
