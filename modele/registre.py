"""
Contrôle du registre d'équations (application de la RÈGLE N°2).

Chaque équation du modèle doit avoir une fiche YAML dans
`modele/registre/`. Ce module vérifie que les fiches sont complètes et
cohérentes. Il est appelé par `tests/test_registre.py`, donc par la CI :
une fiche incomplète fait échouer la construction.
"""
from __future__ import annotations

from pathlib import Path

import yaml

DOSSIER = Path(__file__).resolve().parent / "registre"

CATEGORIES = {"I", "C", "S", "D"}
GRADES = {"A", "B", "C", "D"}
COUCHES = {"A", "B", "C"}
STATUTS = {"brouillon", "valide", "rejete"}

OBLIGATOIRES = ("id", "nom", "description", "formule", "categorie",
                "grade", "empirique", "couche", "statut", "limites")


def charger(dossier: Path = DOSSIER) -> dict[str, dict]:
    """Charge toutes les fiches du registre, indexées par identifiant."""
    fiches = {}
    for chemin in sorted(dossier.glob("*.yaml")):
        fiche = yaml.safe_load(chemin.read_text(encoding="utf-8"))
        fiche["_fichier"] = chemin.name
        fiches[fiche.get("id", chemin.stem)] = fiche
    return fiches


def verifier(fiche: dict) -> list[str]:
    """Renvoie la liste des anomalies d'une fiche (vide = conforme)."""
    p = []
    ident = fiche.get("id", fiche.get("_fichier", "?"))

    for champ in OBLIGATOIRES:
        if fiche.get(champ) in (None, ""):
            p.append(f"{ident}: champ obligatoire manquant « {champ} »")

    cat, grade = fiche.get("categorie"), fiche.get("grade")
    if cat not in CATEGORIES:
        p.append(f"{ident}: categorie « {cat} » invalide (I, C, S ou D)")
    if grade not in GRADES:
        p.append(f"{ident}: grade « {grade} » invalide (A, B, C ou D)")
    if fiche.get("couche") not in COUCHES:
        p.append(f"{ident}: couche « {fiche.get('couche')} » invalide (A, B ou C)")
    if fiche.get("statut") not in STATUTS:
        p.append(f"{ident}: statut « {fiche.get('statut')} » invalide")

    # Règle : une relation de design n'est jamais empirique, et réciproquement.
    if cat == "D" and fiche.get("empirique") is not False:
        p.append(f"{ident}: categorie D (design) mais empirique n'est pas false. "
                 "Une règle inventée par l'EH ne peut pas être présentée "
                 "comme empiriquement fondée.")
    if cat in {"C", "S"} and fiche.get("empirique") is not True:
        p.append(f"{ident}: categorie {cat} mais empirique n'est pas true")

    # Règle : toute relation non comptable doit citer au moins une source.
    if cat in {"C", "S", "D"} and not fiche.get("sources"):
        p.append(f"{ident}: categorie {cat} sans aucune source")
    for src in fiche.get("sources") or []:
        if not src.get("doi_ou_url"):
            p.append(f"{ident}: une source sans DOI ni URL "
                     f"({str(src.get('ref'))[:40]})")

    # Règle : une corrélation doit être re-testée par nous.
    if cat == "S":
        est = fiche.get("estimation") or {}
        for champ in ("methode", "donnees", "periode", "stationnarite", "script"):
            if not est.get(champ):
                p.append(f"{ident}: categorie S, « estimation.{champ} » manquant")

    # Règle : un choix de design passe en analyse de sensibilité.
    if cat == "D" and not (fiche.get("sensibilite") or {}).get("balayage"):
        p.append(f"{ident}: categorie D sans plan de sensibilité "
                 "(sensibilite.balayage)")

    return p


def verifier_tout(dossier: Path = DOSSIER) -> list[str]:
    """Contrôle l'ensemble du registre ; renvoie toutes les anomalies."""
    fiches = charger(dossier)
    anomalies = []
    vus: dict[str, str] = {}
    for ident, fiche in fiches.items():
        anomalies += verifier(fiche)
        if ident in vus:
            anomalies.append(f"{ident}: identifiant dupliqué "
                             f"({vus[ident]} et {fiche['_fichier']})")
        vus[ident] = fiche["_fichier"]
    return anomalies
