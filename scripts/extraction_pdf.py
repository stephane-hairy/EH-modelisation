"""
Extrait et remet en forme le texte de la synthèse EH.

Le PDF d'origine sort en un-mot-par-ligne : ce script recolle les
paragraphes et retire les en-têtes/pieds de page répétés.

Usage : python3 scripts/extraction_pdf.py
Sortie : sources/synthese_EH.txt (brut) et sources/synthese_EH_clean.txt
"""
import re
from pathlib import Path

from pypdf import PdfReader

RACINE = Path(__file__).resolve().parent.parent
PDF = RACINE / "sources" / "Synthese-Economie-homeostatique.pdf"
BRUT = RACINE / "sources" / "synthese_EH.txt"
PROPRE = RACINE / "sources" / "synthese_EH_clean.txt"

# Lignes répétées sur chaque page, sans intérêt
BRUIT = (
    "Ce document est mis à disposition",
    "Licence Creative Commons",
    "Retour à la Table des matières",
    "Vers une économie bio-intégrée : Théorie",
)


def extraire() -> str:
    lecteur = PdfReader(PDF)
    morceaux = []
    for i, page in enumerate(lecteur.pages, start=1):
        morceaux.append(f"===PAGE {i}===")
        morceaux.append(page.extract_text() or "")
    return "\n".join(morceaux)


def nettoyer(texte: str) -> str:
    sortie, tampon = [], []
    for ligne in texte.split("\n"):
        s = ligne.strip()
        if any(bruit in s for bruit in BRUIT):
            continue
        if s.startswith("===PAGE"):
            if tampon:
                sortie.append(" ".join(tampon))
                tampon = []
            sortie.append("\n" + s)
            continue
        if s in ("", "​"):
            if tampon:
                sortie.append(" ".join(tampon))
                tampon = []
            continue
        tampon.append(s)
    if tampon:
        sortie.append(" ".join(tampon))
    res = "\n".join(sortie)
    res = res.replace("​", "")          # espaces de largeur nulle
    return re.sub(r" +", " ", res)


if __name__ == "__main__":
    brut = extraire()
    BRUT.write_text(brut, encoding="utf-8")
    PROPRE.write_text(nettoyer(brut), encoding="utf-8")
    print(f"{BRUT.name} et {PROPRE.name} écrits dans sources/")
