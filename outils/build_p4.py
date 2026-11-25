"""Construit p4.html (constructeur de page) à partir de outils/p4-source.html.

Les images, les styles de base et les données produits sont repris de p1.html,
pour que le prototype 4 reste identique visuellement aux trois autres.
Utilisation : python3 outils/build_p4.py
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
p1 = (ROOT / "p1.html").read_text(encoding="utf-8")
src = (ROOT / "outils" / "p4-source.html").read_text(encoding="utf-8")

h = lambda u: hashlib.md5(u.encode()).hexdigest()
assets, names = {}, {}


def name(uri, key):
    k = h(uri)
    if k not in names:
        names[k] = key
        assets[key] = uri
    return names[k]


name(re.search(r'class="logo" src="(data:[^"]+)"', p1).group(1), "logo")
name(re.search(r'<footer>.*?src="(data:[^"]+)"', p1, re.S).group(1), "foot")
hero = json.loads(re.search(r"heroThumbItems=(\[.*?\]);", p1).group(1))
hero_out = [{"k": name(x["src"], f"h{i}"), "alt": x["alt"]} for i, x in enumerate(hero)]
for i, u in enumerate(json.loads(re.search(r"catImages=(\[.*?\])", p1).group(1))):
    name(u, f"c{i}")
products = json.loads(re.search(r"const products=(\[.*?\]),categories", p1).group(1))
for i, p in enumerate(products):
    if p["img"].startswith("data:"):
        p["img"] = "@" + name(p["img"], f"p{i}")

css = re.search(r"<style>(.*?)</style>", p1, re.S).group(1)
css = re.sub(r"@media\([^)]*\)\{#galerie[^{]*\{[^}]*\}\}", "", css)
css = re.sub(r"#galerie[^{]*\{[^}]*\}", "", css)

dump = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
out = (
    src.replace("/*__ASSETS__*/{}", dump(assets))
    .replace("/*__PRODUCTS__*/[]", dump(products))
    .replace("/*__HERO__*/[]", dump(hero_out))
    .replace("/*__BASECSS__*/''", dump(css))
)
assert "/*__" not in out, "un marqueur n'a pas été remplacé"
(ROOT / "p4.html").write_text(out, encoding="utf-8")
print(f"p4.html : {len(out) / 1e6:.1f} Mo, {len(assets)} images, {len(products)} réalisations")
