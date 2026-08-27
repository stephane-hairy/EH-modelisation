"""
Cache de données reproductible.

Principe : toute série récupérée est écrite sur disque avec son empreinte
SHA-256, son horodatage et l'URL exacte qui l'a produite. Une exécution
ultérieure doit soit retrouver le même fichier, soit signaler que la
source a été révisée.

Sans cela, un résultat de simulation n'est pas reproductible : les
instituts révisent leurs séries en permanence (changements de base,
corrections). On doit pouvoir dire « ce graphique a été produit avec la
version de la série téléchargée le tant, empreinte telle ».
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
DOSSIER_BRUT = RACINE / "donnees" / "brut"
MANIFESTE = RACINE / "donnees" / "manifeste.json"


def empreinte(contenu: bytes) -> str:
    """SHA-256 du contenu, en hexadécimal."""
    return hashlib.sha256(contenu).hexdigest()


def _lire_manifeste() -> dict:
    if MANIFESTE.exists():
        return json.loads(MANIFESTE.read_text(encoding="utf-8"))
    return {}


def _ecrire_manifeste(m: dict) -> None:
    MANIFESTE.parent.mkdir(parents=True, exist_ok=True)
    MANIFESTE.write_text(
        json.dumps(m, indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )


def enregistrer(nom: str, url: str, contenu: bytes, source: str) -> dict:
    """
    Écrit `contenu` dans donnees/brut/<nom> et met à jour le manifeste.

    Renvoie la fiche du manifeste, avec `revision: True` si l'empreinte a
    changé depuis le dernier téléchargement — c'est le signal qu'il faut
    vérifier ce qui a bougé avant de refaire tourner un résultat.
    """
    DOSSIER_BRUT.mkdir(parents=True, exist_ok=True)
    chemin = DOSSIER_BRUT / nom
    sha = empreinte(contenu)

    manifeste = _lire_manifeste()
    precedent = manifeste.get(nom)
    revision = precedent is not None and precedent.get("sha256") != sha

    chemin.write_bytes(contenu)
    fiche = {
        "source": source,
        "url": url,
        "sha256": sha,
        "octets": len(contenu),
        "recupere_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256_precedent": precedent.get("sha256") if revision else None,
        "revision": revision,
    }
    manifeste[nom] = fiche
    _ecrire_manifeste(manifeste)
    return fiche
