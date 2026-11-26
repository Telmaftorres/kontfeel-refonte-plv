"""Données partagées par build_p3.py et build_p4.py (réalisations complémentaires, photo bois).

Les réalisations de base sont lues dans p1.html ; ce module les complète avec des réalisations Kontfeel
vérifiées sur kontfeel.fr, et fixe l'ordre des premières cartes de la galerie.
"""
import base64
from pathlib import Path

OUTILS = Path(__file__).resolve().parent

# Photo bois : réalisation Kontfeel publiée (présentoir NOU Ariège Pyrénées pour produits locaux).
BOIS = {
    "src": "data:image/jpeg;base64," + base64.b64encode((OUTILS / "bois-nou-produits-locaux.jpg").read_bytes()).decode(),
    "alt": "Présentoir en bois NOU Ariège Pyrénées pour produits locaux",
    "url": "https://www.kontfeel.fr/realisations-plv/le-presentoir-en-boiscree-lharmonie-avec-vos-produits-locaux",
    "aria": "Voir la réalisation : présentoir en bois pour produits locaux",
}


def completer(products, hero):
    """Ajoute les réalisations alimentaires, relie le présentoir bareMinerals à sa page et ordonne la galerie."""
    out = [dict(p) for p in products]
    by_name = {p["name"]: p for p in out}

    # Présentoir bareMinerals : sa page de réalisation existe sur kontfeel.fr.
    bm = by_name["Présentoir cosmétique en métal pour maquillage"]
    bm["source"] = "https://www.kontfeel.fr/realisations-plv/presentoir-cosmetique-metal-maquillage"
    bm["kind"] = "Réalisation"

    # Réalisations alimentaires (photos de la bannière). Famille déduite de la forme du présentoir, à valider.
    asie = {"name": "Présentoir de comptoir en carton pour produits d’Asie", "typ": "Présentoirs escaliers", "mat": "Carton",
            "sect": "Alimentaire", "img": hero["Présentoir de comptoir pour produits alimentaires asiatiques"],
            "alt": "Présentoir de comptoir en carton à plusieurs niveaux pour produits alimentaires asiatiques",
            "source": "https://www.kontfeel.fr/realisations-plv/presentoir-de-comptoir-en-carton", "kind": "Réalisation"}
    wasabi = {"name": "Présentoir de comptoir Wasabi Store pour sauces", "typ": "Sabots et stop-piles", "mat": "Carton",
              "sect": "Alimentaire", "img": hero["Présentoir de comptoir Wasabi Store pour sauces"],
              "alt": "Présentoir de comptoir en carton Wasabi Store pour sauces"}

    # Ordre : huit premières cartes variées (dont l'alimentaire et le bareMinerals), puis le reste.
    first = [out[0], out[1], out[2], out[3], out[4], asie, bm, out[5]]
    rest = [p for p in out if p not in first]
    rest.insert(2, wasabi)
    return first + rest
