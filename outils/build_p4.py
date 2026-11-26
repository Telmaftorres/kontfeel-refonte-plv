"""Génère p4.html (découverte interactive) à partir de outils/p4-source.html.

Images, CSS de base, familles et réalisations repris de p1.html (version complète).
Tous les contenus des panneaux sont écrits dans le HTML : l'interaction ne change que leur visibilité.
Usage : python3 outils/build_p4.py
"""
import base64
import html
import json
import re
from pathlib import Path

from donnees_communes import BOIS, completer

ROOT = Path(__file__).resolve().parent.parent
base = (ROOT / "p1.html").read_text(encoding="utf-8")
src = (ROOT / "outils" / "p4-source.html").read_text(encoding="utf-8")
esc = lambda s: html.escape(str(s), quote=True)
one = lambda pat: re.search(pat, base, re.S).group(1)

logo = one(r'class="logo" src="(data:[^"]+)"')
foot = one(r'<footer>.*?src="(data:[^"]+)"')
css = one(r"<style>(.*?)</style>")
products = json.loads(one(r"const products=(\[.*?\]),categories"))
cat_images = json.loads(one(r"catImages=(\[.*?\])"))
hero = {h["alt"]: h["src"] for h in json.loads(one(r"heroThumbItems=(\[.*?\]);"))}
products = completer(products, hero)
by_name = {p["name"]: p for p in products}
HINT = '<span class="hint" aria-hidden="true">Voir les réalisations ↓</span>'


def known(v):
    return bool(v) and v != "À confirmer"


def pick(field, value, img_src, img_alt):
    """Bouton-photo qui filtre la galerie (distinct des liens vers d'autres pages)."""
    return (f'<button class="pick" type="button" data-f="{field}" data-v="{esc(value)}" aria-pressed="false">'
            f'<img alt="{esc(img_alt)}" loading="lazy" src="{img_src}" onerror="safeImage(this)"/>{HINT}</button>')


# ---------- Familles (mêmes textes que la version commerciale) ----------
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
fams = re.findall(
    r'<article class="catwrap"><button class="cat" data-cat="([^"]+)">.*?</button><p>[^<]*</p>'
    r'<a class="familylink" href="([^"]+)" rel="noopener" target="_blank" aria-label="([^"]+)">', base, re.S)
assert len(fams) == 10 and len(cat_images) == 10
fam_html = []
for (name, url, aria), img in zip(fams, cat_images):
    label = esc(name).replace("Porte-documents", '<em class="nw">Porte-documents</em>').replace("stop-piles", '<em class="nw">stop-piles</em>')
    fam_html.append(
        f'<article class="fam">{pick("typ", name, img, "Exemple de " + name[0].lower() + name[1:])}'
        f'<h4><a href="{url}" rel="noopener" target="_blank">{label}</a></h4><p>{esc(SHORT[name])}</p>'
        f'<a class="familylink" href="{url}" rel="noopener" target="_blank" aria-label="{aria}">Découvrir la gamme →</a></article>')

# ---------- Matériaux ----------
metal_src = "data:image/jpeg;base64," + base64.b64encode((ROOT / "outils" / "p3-metal-inox.jpg").read_bytes()).decode()
carton = by_name["Présentoir escalier en carton Naruto à deux étages"]
plast = by_name["Porte-visuel en plexiglas Activ5"]
MATS = [
    ("Carton", pick("mat", "Carton", carton["img"], carton["alt"]),
     "Léger et personnalisable, le présentoir de comptoir en carton est idéal pour les opérations promotionnelles.",
     ("https://www.kontfeel.fr/display-plv/presentoir-de-comptoir-carton", "Découvrir nos présentoirs de comptoir en carton", "Présentoirs en carton →")),
    ("Bois", f'<div class="matimg"><img alt="{BOIS["alt"]}" loading="lazy" src="{BOIS["src"]}"/></div>',
     "Un présentoir de comptoir en bois apporte un rendu chaleureux, pour une présentation durable.",
     (BOIS["url"], BOIS["aria"], "Voir une réalisation en bois →")),
    ("Métal", pick("mat", "Métal", metal_src, "Présentoir inox à deux niveaux pour professionnels"),
     "Robuste et adapté aux installations de longue durée.",
     ("https://www.kontfeel.fr/realisations-plv/presentoir-inox-pour-les-professionnels", "Voir la réalisation : présentoir inox pour professionnels", "Voir une réalisation en métal →")),
    ("Plastique", pick("mat", "Plastique", plast["img"], plast["alt"]),
     "Polyvalent, avec de nombreuses possibilités de formes, de transparence et de finitions.",
     ("https://www.kontfeel.fr/realisations-plv/rappel-de-marque-plastique", "Voir la réalisation : rappel de marque en plexiglas pour opticien", "Voir une réalisation en plastique →")),
]
mat_values = {p["mat"] for p in products if known(p["mat"])}
assert mat_values == {"Carton", "Métal", "Plastique"}, mat_values  # la réalisation bois est un présentoir de sol : pas dans la galerie comptoir
mat_html = []
for name, visual, text, link in MATS:
    a = f'<a class="familylink" href="{link[0]}" rel="noopener" target="_blank" aria-label="{link[1]}">{link[2]}</a>' if link else ""
    mat_html.append(f'<article class="mat">{visual}<h4>{name}</h4><p>{esc(text)}</p>{a}</article>')

# ---------- Secteurs (repris des prototypes précédents, avec de vrais visuels) ----------
SECTORS = [
    ("Cosmétique &amp; beauté", "Cosmétique", "Valorisez vos soins, parfums, produits de beauté et échantillons.",
     "https://www.kontfeel.fr/solutions-metiers/beaute-cosmetique-luxe", "Découvrir la PLV beauté et cosmétique",
     hero["Présentoir de comptoir WAAM pour soins capillaires"], "Présentoir de comptoir WAAM pour soins capillaires"),
    ("Pharmacie &amp; santé", "Pharmacie", "Présentez vos produits de soin, références de parapharmacie et compléments alimentaires.",
     "https://www.kontfeel.fr/plv-pharmacie", "Découvrir la PLV pour pharmacie",
     by_name["Distributeur de comptoir Suvéal Duo Densmore"]["img"], by_name["Distributeur de comptoir Suvéal Duo Densmore"]["alt"]),
    ("Édition &amp; librairie", "Édition", "Mettez en avant vos nouveautés, livres et produits culturels.",
     "https://www.kontfeel.fr/solutions-metiers/edition-culture-loisirs", "Découvrir la PLV édition et culture",
     by_name["Présentoir escalier en carton Psycho-Pop"]["img"], by_name["Présentoir escalier en carton Psycho-Pop"]["alt"]),
    ("Alimentaire", "Alimentaire", "Facilitez la présentation de vos produits alimentaires, nouveautés et offres promotionnelles.",
     "https://www.kontfeel.fr/plv-magasin", "Découvrir la PLV magasin",
     hero["Présentoir de comptoir pour produits alimentaires asiatiques"], "Présentoir de comptoir pour produits alimentaires asiatiques"),
    ("Retail &amp; distribution", "Retail", "Déployez des présentoirs adaptés à vos points de vente et à vos opérations commerciales.",
     "https://www.kontfeel.fr/solutions-metiers", "Découvrir nos solutions métiers",
     by_name["Présentoir à encens trois niveaux"]["img"], by_name["Présentoir à encens trois niveaux"]["alt"]),
    ("Restauration", "Restauration", "Communiquez sur vos menus, offres et nouveautés directement sur les tables et comptoirs.",
     "https://www.kontfeel.fr/solutions-metiers/services-chr-institutionnel", "Découvrir la PLV restauration",
     by_name["Chevalet de table personnalisé KFC"]["img"], by_name["Chevalet de table personnalisé KFC"]["alt"]),
]
sect_values = {p["sect"] for p in products if known(p["sect"])}
sect_html = []
for title, value, text, url, anchor, img, alt in SECTORS:
    assert value is None or value in sect_values, value
    visual = pick("sect", value, img, alt) if value else f'<div class="simg"><img alt="{esc(alt)}" loading="lazy" src="{img}"/></div>'
    sect_html.append(f'<article class="sect">{visual}<div><h4><a href="{url}" rel="noopener" target="_blank">{title}</a></h4>'
                     f'<p>{esc(text)}</p><a class="familylink" href="{url}" rel="noopener" target="_blank">{anchor} →</a></div></article>')
others = sorted(sect_values - {s[1] for s in SECTORS}, key=lambda s: s.lower())
others_html = "".join(f'<button class="pill" type="button" data-f="sect" data-v="{esc(v)}" aria-pressed="false">{esc(v)}</button>' for v in others)


# ---------- Galerie : les 30 réalisations dans le HTML ----------
def card(p, i):
    meta = "<br>".join(esc(x) for x in [" · ".join(v for v in (p.get("mat"), p.get("sect")) if known(v)), p.get("kind")] if x)
    tag, attrs = ("a", f' href="{esc(p["source"])}" target="_blank" rel="noopener"') if p.get("source") else ("button", ' type="button"')
    return (f'<{tag} class="product" data-product="{i}"{attrs}><img src="{p["img"]}" alt="{esc(p["alt"])}" loading="lazy" width="400" height="300" onerror="safeImage(this)">'
            f'<div class="info"><span class="tag">{esc(p["typ"])}</span><strong>{esc(p["name"])}</strong>'
            + (f"<small>{meta}</small>" if meta else "") + f"</div></{tag}>")


mini = lambda imgs: "".join(f'<img alt="" src="{s}"/>' for s in imgs)
dump = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
rep = {
    "__BASECSS__": css, "__LOGO__": logo, "__FOOTLOGO__": foot,
    "__HERO_SRC__": hero["Présentoir de comptoir Wasabi Store pour sauces"], "__HERO_ALT__": "Présentoir de comptoir Wasabi Store pour sauces",
    "__MODE_TYPES__": mini([cat_images[2], cat_images[6], cat_images[3]]),
    "__MODE_SECTS__": mini([SECTORS[0][5], SECTORS[1][5], SECTORS[5][5]]),
    "__FAMILIES__": "\n".join(fam_html), "__MATERIALS__": "\n".join(mat_html),
    "__SECTORS__": "\n".join(sect_html), "__OTHER_SECTORS__": others_html,
    "__GALLERY__": "".join(card(p, i) for i, p in enumerate(products)),
    "/*__PRODUCTS__*/[]": dump([{k: v for k, v in p.items() if k != "img"} for p in products]),
}
out = src
for k, v in rep.items():
    assert out.count(k) >= 1, k
    out = out.replace(k, v)
assert "__" not in re.sub(r"data:[^\"')]+", "", out), "jeton non remplacé"
(ROOT / "p4.html").write_text(out, encoding="utf-8")
print(f"p4.html : {len(out.encode()) / 1e6:.1f} Mo, {len(fams)} familles, {len(SECTORS)} secteurs + {len(others)} autres, {len(products)} réalisations")
