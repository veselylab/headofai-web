#!/usr/bin/env python3
"""Vlozi do navigace prepinac jazyku CZ/EN a do hlavicky hreflang odkazy.

Spousti se nad ceskymi i anglickymi strankami. Kazda stranka zna svuj protejsek,
takze prepnuti jazyka drzi uzivatele na stejnem obsahu, ne na homepage.

Vlajky jsou inline SVG zamerne: emoji vlajky se na Windows nevykresluji
(zobrazi se misto nich pismena "CZ"), coz by v navigaci vypadalo rozbite.
"""
import re
import sys

BASE = "https://headofai.cz"

# cz_soubor, cz_url, en_soubor, en_url
PAGES = [
    ("index.html", "/", "en/index.html", "/en/"),
    ("co-je-head-of-ai.html", "/co-je-head-of-ai",
     "en/what-is-head-of-ai.html", "/en/what-is-head-of-ai"),
    ("kdy-firma-potrebuje-head-of-ai.html", "/kdy-firma-potrebuje-head-of-ai",
     "en/when-does-a-company-need-a-head-of-ai.html", "/en/when-does-a-company-need-a-head-of-ai"),
    ("fractional-vs-fulltime-caio.html", "/fractional-vs-fulltime-caio",
     "en/fractional-vs-fulltime-caio.html", "/en/fractional-vs-fulltime-caio"),
    ("plat-chief-ai-officer.html", "/plat-chief-ai-officer",
     "en/chief-ai-officer-salary.html", "/en/chief-ai-officer-salary"),
]

FLAG_CZ = ('<svg viewBox="0 0 6 4" aria-hidden="true" focusable="false">'
           '<path fill="#fff" d="M0 0h6v2H0z"/>'
           '<path fill="#d7141a" d="M0 2h6v2H0z"/>'
           '<path fill="#11457e" d="M0 0l3 2-3 2z"/></svg>')

FLAG_EN = ('<svg viewBox="0 0 60 30" aria-hidden="true" focusable="false">'
           '<path fill="#012169" d="M0 0h60v30H0z"/>'
           '<path stroke="#fff" stroke-width="6" d="M0 0l60 30M60 0L0 30"/>'
           '<path stroke="#c8102e" stroke-width="4" d="M0 0l60 30M60 0L0 30"/>'
           '<path stroke="#fff" stroke-width="10" d="M30 0v30M0 15h60"/>'
           '<path stroke="#c8102e" stroke-width="6" d="M30 0v30M0 15h60"/></svg>')

CSS = """
    .lang-switch { display: flex; align-items: center; gap: 8px; }
    .lang-switch a { display: block; width: 26px; height: 18px; border-radius: 3px; overflow: hidden; line-height: 0; opacity: 0.45; box-shadow: 0 0 0 1px rgba(255,255,255,0.16); transition: opacity 180ms ease, box-shadow 180ms ease; }
    .lang-switch a:hover, .lang-switch a:focus-visible { opacity: 0.9; }
    .lang-switch a[aria-current="true"] { opacity: 1; box-shadow: 0 0 0 1px var(--color-accent); }
    .lang-switch svg { display: block; width: 100%; height: 100%; }"""

OLD_MOBILE = ('@media (max-width: 768px) { #nav-links { display: none !important; } '
              'header nav > a.btn { margin-left: auto; } }')
NEW_MOBILE = ('@media (max-width: 768px) { #nav-links { display: none !important; } '
              'header nav > .lang-switch { margin-left: auto; } }')


def switcher(lang, cz_url, en_url):
    group = "Jazyk" if lang == "cs" else "Language"
    cz = (f'<a href="{cz_url}" hreflang="cs" title="Česky" aria-label="Česky"'
          + (' aria-current="true"' if lang == "cs" else "") + f'>{FLAG_CZ}</a>')
    en = (f'<a href="{en_url}" hreflang="en" title="English" aria-label="English"'
          + (' aria-current="true"' if lang == "en" else "") + f'>{FLAG_EN}</a>')
    return f'<div class="lang-switch" role="group" aria-label="{group}">{cz}{en}</div>'


def process(path, lang, cz_url, en_url):
    html = open(path, encoding="utf-8").read()
    orig = html
    notes = []

    if "lang-switch" in html:
        return "uz obsahuje prepinac - preskoceno"

    # 1) CSS - pripoj za mobilni media query uvnitr <style>
    if OLD_MOBILE in html:
        html = html.replace(OLD_MOBILE, NEW_MOBILE + CSS, 1)
    else:
        return "NENALEZENO mobilni pravidlo - preskoceno"

    # 2) markup - tesne pred CTA tlacitko v <header>
    # homepage ma CTA jako "#kontakt", podstranky jako "/#kontakt", EN jako "/en/#kontakt"
    m = re.search(r'(<header\b.*?)(<a href="[^"]*#kontakt" class="btn btn-primary")', html, re.S)
    if not m:
        return "NENALEZENO CTA v hlavicce - preskoceno"
    html = html[:m.start(2)] + switcher(lang, cz_url, en_url) + html[m.start(2):]

    # 3) canonical na vlastni jazykovou verzi
    self_url = cz_url if lang == "cs" else en_url
    html, n = re.subn(r'<link rel="canonical" href="[^"]*">',
                      f'<link rel="canonical" href="{BASE}{self_url}">', html)
    notes.append(f"canonical={n}")

    # 4) hreflang alternativy hned za canonical
    alts = (f'<link rel="alternate" hreflang="cs" href="{BASE}{cz_url}">'
            f'<link rel="alternate" hreflang="en" href="{BASE}{en_url}">'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{cz_url}">')
    html = re.sub(r'(<link rel="canonical" href="[^"]*">)', r"\1" + alts, html, count=1)

    # 5) og:url na vlastni jazykovou verzi
    html, n = re.subn(r'<meta property="og:url" content="[^"]*">',
                      f'<meta property="og:url" content="{BASE}{self_url}">', html)
    notes.append(f"og:url={n}")

    if html == orig:
        return "beze zmeny"
    open(path, "w", encoding="utf-8").write(html)
    return "ok (" + ", ".join(notes) + ")"


if __name__ == "__main__":
    for cz_file, cz_url, en_file, en_url in PAGES:
        print(f"  {cz_file:40} {process(cz_file, 'cs', cz_url, en_url)}")
        print(f"  {en_file:40} {process(en_file, 'en', cz_url, en_url)}")
