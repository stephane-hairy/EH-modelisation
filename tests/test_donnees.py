"""Cache de données : reproductibilité et détection des révisions."""
import json

import pytest

from modele.donnees import cache, empreinte


def test_empreinte_stable():
    assert empreinte(b"abc") == empreinte(b"abc")
    assert empreinte(b"abc") != empreinte(b"abd")


def test_revision_detectee(tmp_path, monkeypatch):
    """Si l'institut révise une série, le manifeste doit le signaler."""
    monkeypatch.setattr(cache, "DOSSIER_BRUT", tmp_path / "brut")
    monkeypatch.setattr(cache, "MANIFESTE", tmp_path / "manifeste.json")

    f1 = cache.enregistrer("serie.csv", "http://x", b"1;2;3", "TEST")
    assert f1["revision"] is False

    f2 = cache.enregistrer("serie.csv", "http://x", b"1;2;3", "TEST")
    assert f2["revision"] is False, "contenu identique : pas de révision"

    f3 = cache.enregistrer("serie.csv", "http://x", b"1;2;4", "TEST")
    assert f3["revision"] is True, "contenu modifié : révision à signaler"
    assert f3["sha256_precedent"] == f1["sha256"]

    m = json.loads((tmp_path / "manifeste.json").read_text())
    assert m["serie.csv"]["url"] == "http://x"


@pytest.mark.reseau
def test_insee_pib_remonte_a_1949():
    from modele.donnees import insee, insee_dimensions
    d = insee_dimensions("CNA-2020-PIB")
    df = insee("CNA-2020-PIB", {"FREQ": "A", "OPERATION": "PIB",
                                "UNIT_MEASURE": "EUROS_COURANTS",
                                "CNA_PRODUIT": "NNTOTAL"}, d)
    assert df["periode"].min() == "1949"
    assert len(df) > 70
