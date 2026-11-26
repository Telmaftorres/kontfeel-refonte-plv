"""Génère p3.html (version commerciale simplifiée) à partir de outils/p3-source.html.

Les images (logo, bannière, familles, réalisations) et le CSS de base sont repris de p1.html (version complète).
La photo du métal (présentoir inox, réalisation publiée sur kontfeel.fr) est dans outils/p3-metal-inox.jpg.
Usage : python3 outils/build_p3.py
"""
import base64
import html
import json
import re
from pathlib import Path

from donnees_communes import BOIS, completer

ROOT = Path(__file__).resolve().parent.parent
base = (ROOT / "p1.html").read_text(encoding="utf-8")
src = (ROOT / "outils" / "p3-source.html").read_text(encoding="utf-8")

esc = lambda s: html.escape(str(s), quote=True)
one = lambda pat: re.search(pat, base, re.S).group(1)

logo = one(r'class="logo" src="(data:[^"]+)"')
foot = one(r'<footer>.*?src="(data:[^"]+)"')
css = one(r"<style>(.*?)</style>")
products = json.loads(one(r"const products=(\[.*?\]),categories"))
cat_images = json.loads(one(r"catImages=(\[.*?\])"))
hero = json.loads(one(r"heroThumbItems=(\[.*?\]);"))
products = completer(products, {h["alt"]: h["src"] for h in hero})

# Descriptions courtes (une phrase) intégrant le vocabulaire recherché par les prospects.
SHORT = {
    "Totems de comptoir": "Un totem personnalisé pour attirer le regard dans un espace réduit.",
    "Porte-documents": "Présentez vos flyers, brochures et catalogues en libre-service.",
    "Chevalets et cavaliers": "Des chevalets de comptoir pour communiquer sur vos offres.",
    "Distributeurs et vrac": "Des distributeurs en libre-service, notamment pour la pharmacie.",
    "Sabots et stop-piles": "Valorisez vos produits dans un support compact.",
    "Prêts à vendre": "Simplifiez la mise en rayon de vos produits.",
    "Présentoirs escaliers": "Des présentoirs à plusieurs niveaux pour valoriser vos références.",
    "Présentoirs à empreintes": "Des découpes adaptées à vos produits cosmétiques ou pharmaceutiques.",
    "Rappels de marque": "Renforcez la visibilité de votre marque en point de vente.",
    "Glorifiers": "Des présentoirs personnalisés pour sublimer vos produits phares.",
}

# Familles : nom, lien et aria-label repris de P1 (version complète).
# La photo filtre les réalisations ; le titre et le lien rose mènent à la page de la gamme.
fams = re.findall(
    r'<article class="catwrap"><button class="cat" data-cat="([^"]+)">.*?</button><p>[^<]*</p>'
    r'<a class="familylink" href="([^"]+)" rel="noopener" target="_blank" aria-label="([^"]+)">',
    base, re.S)
assert len(fams) == 10 and len(cat_images) == 10, (len(fams), len(cat_images))
fam_html = []
for (name, url, aria), img in zip(fams, cat_images):
    label = esc(name).replace("Porte-documents", '<em class="nw">Porte-documents</em>').replace("stop-piles", '<em class="nw">stop-piles</em>')
    fam_html.append(
        f'<article class="fam"><button class="pick" type="button" data-cat="{esc(name)}" aria-label="Afficher les réalisations : {esc(name)}">'
        f'<img alt="Exemple de {esc(name[0].lower() + name[1:])}" loading="lazy" src="{img}"/><span class="hint" aria-hidden="true">Voir les réalisations ↓</span></button>'
        f'<h3 class="nm"><a href="{url}" rel="noopener" target="_blank">{label}</a></h3>'
        f'<p>{esc(SHORT[name])}</p>'
        f'<a class="familylink" href="{url}" rel="noopener" target="_blank" aria-label="{aria}">Découvrir la gamme →</a></article>')


def known(v):
    return bool(v) and v != "À confirmer"


def card(p, i):
    """Carte statique : les 30 réalisations sont dans le HTML, le script se contente de les afficher ou masquer."""
    meta = "<br>".join(esc(x) for x in [" · ".join(v for v in (p.get("mat"), p.get("sect")) if known(v)), p.get("kind")] if x)
    if p.get("source"):
        tag, attrs = "a", f' href="{esc(p["source"])}" target="_blank" rel="noopener"'
    else:
        tag, attrs = "button", ' type="button"'
    return (f'<{tag} class="product" data-product="{i}"{attrs}><img src="{p["img"]}" alt="{esc(p["alt"])}" loading="lazy" width="400" height="300" onerror="safeImage(this)">'
            f'<div class="info"><span class="tag">{esc(p["typ"])}</span><strong>{esc(p["name"])}</strong>'
            + (f"<small>{meta}</small>" if meta else "") + f"</div></{tag}>")


by_name = {p["name"]: p for p in products}
carton = by_name["Présentoir escalier en carton Naruto à deux étages"]
plast = by_name["Porte-visuel en plexiglas Activ5"]
metal_src = "data:image/jpeg;base64," + base64.b64encode((ROOT / "outils" / "p3-metal-inox.jpg").read_bytes()).decode()
assert carton["mat"] == "Carton" and plast["mat"] == "Plastique"

dump = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
rep = {
    "__BASECSS__": css,
    "__LOGO__": logo,
    "__FOOTLOGO__": foot,
    "__HERO_SRC__": hero[0]["src"],
    "__HERO_ALT__": esc(hero[0]["alt"]),
    "__FAMILIES__": "\n".join(fam_html),
    "__GALLERY__": "".join(card(p, i) for i, p in enumerate(products)),
    "__MAT_CARTON__": carton["img"], "__MAT_CARTON_ALT__": esc(carton["alt"]),
    "__MAT_PLAST__": plast["img"], "__MAT_PLAST_ALT__": esc(plast["alt"]),
    "__MAT_BOIS__": BOIS["src"], "__MAT_BOIS_ALT__": BOIS["alt"], "__MAT_BOIS_URL__": BOIS["url"], "__MAT_BOIS_ARIA__": BOIS["aria"],
    "__MAT_METAL__": metal_src, "__MAT_METAL_ALT__": "Présentoir inox à deux niveaux pour professionnels",
    "/*__PRODUCTS__*/[]": dump([{k: v for k, v in p.items() if k != "img"} for p in products]),
    "/*__HEROTHUMBS__*/[]": dump(hero),
}
out = src
for k, v in rep.items():
    assert out.count(k) >= 1, k
    out = out.replace(k, v)
assert "__" not in re.sub(r"data:[^\"')]+", "", out).replace("__proto__", ""), "jeton non remplacé"
(ROOT / "p3.html").write_text(out, encoding="utf-8")
print(f"p3.html : {len(out.encode()) / 1e6:.1f} Mo, {len(fams)} familles, {len(products)} réalisations")
