#!/usr/bin/env python3
"""Contact page rollout: Contact link in every site footer + sitemap entry. Idempotent."""
import re, glob, os
assert open("CNAME").read().strip() == "dirk.it"
LABEL = {"en": "Contact", "de": "Kontakt", "es": "Contacto", "pt": "Contato", "it": "Contatti"}
changed = 0
for path in sorted(glob.glob("**/*.html", recursive=True)):
    if path.startswith("google"): continue
    s = open(path, encoding="utf-8").read()
    loc = path.split("/")[0] if path.split("/")[0] in LABEL else "en"
    m = re.search(r'<footer class="site">.*?</footer>', s, re.S)
    if not m or 'href="/contact/"' in m.group(0): continue
    f = m.group(0)
    anchor = '<a href="/privacy/"'
    if anchor not in f: continue
    f = f.replace(anchor, f'<a href="/contact/" style="font-size:14px;color:#9B958A">{LABEL[loc]}</a>\n      ' + anchor, 1)
    s = s[:m.start()] + f + s[m.end():]
    open(path, "w", encoding="utf-8").write(s); changed += 1
sm = open("sitemap.xml", encoding="utf-8").read()
if "https://dirk.it/contact/" not in sm:
    sm = sm.replace("</urlset>", "  <url><loc>https://dirk.it/contact/</loc><lastmod>2026-09-02</lastmod></url>\n</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write(sm); changed += 1
print(f"{changed} files changed")
