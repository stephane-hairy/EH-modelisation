"""Le registre d'équations doit rester conforme (RÈGLE N°2)."""
from pathlib import Path

import pytest
import yaml

from modele.registre import DOSSIER, charger, verifier, verifier_tout


def test_registre_conforme():
    anomalies = verifier_tout()
    assert not anomalies, "Registre non conforme :\n  - " + "\n  - ".join(anomalies)


def test_registre_non_vide():
    assert charger(), "Aucune fiche dans modele/registre/"


def test_une_fiche_design_ne_peut_pas_etre_empirique(tmp_path: Path):
    """Garde-fou central : une règle inventée par l'EH n'est jamais un fait."""
    fiche = {
        "id": "EQ-EH-999", "nom": "test", "description": "test",
        "formule": "x = 1", "categorie": "D", "grade": "D",
        "empirique": True,                      # ← la faute
        "couche": "B", "statut": "brouillon", "limites": "test",
        "sources": [{"ref": "Synthèse EH v1.7 §11.1", "doi_ou_url": "https://exnaturae.ong"}],
        "sensibilite": {"balayage": [0, 1]},
    }
    problemes = verifier(fiche)
    assert any("empirique" in p for p in problemes)


def test_une_correlation_exige_un_test_refait(tmp_path: Path):
    """Une catégorie S sans réplication de notre part est refusée."""
    fiche = {
        "id": "EQ-XXX-998", "nom": "test", "description": "test",
        "formule": "y = a*x", "categorie": "S", "grade": "B",
        "empirique": True, "couche": "A", "statut": "brouillon",
        "limites": "test",
        "sources": [{"ref": "Une étude", "doi_ou_url": "https://doi.org/10.0/x"}],
    }
    problemes = verifier(fiche)
    assert any("estimation." in p for p in problemes)


@pytest.mark.parametrize("chemin", sorted(DOSSIER.glob("*.yaml")), ids=lambda p: p.name)
def test_yaml_lisible(chemin: Path):
    assert yaml.safe_load(chemin.read_text(encoding="utf-8")) is not None
