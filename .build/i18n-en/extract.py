#!/usr/bin/env python3
"""Vytahne prekladatelne retezce z HTML stranky headofai.cz.

Nesaha na markup - jen vypise, co je videt uzivateli nebo vyhledavaci.
Vystup: JSON {"strings": [{"id": n, "kind": ..., "ctx": ..., "cs": ...}]}
"""
import json
import re
import sys

# atributy, jejichz hodnota je viditelny/indexovany text
ATTRS = ("alt", "title", "aria-label", "placeholder", "aria-labelledby-text")
META_NAMES = ("description", "keywords", "twitter:title", "twitter:description", "author")
META_PROPS = ("og:title", "og:description", "og:site_name", "og:image:alt")

# JSON-LD klice, jejichz hodnota je lidsky text
LD_TEXT_KEYS = {"name", "description", "text", "headline", "jobTitle", "articleBody",
                "alternateName", "disambiguatingDescription", "abstract", "caption"}


def has_letters(s):
    return bool(re.search(r"[A-Za-zÁ-Žá-ž]", s))


def walk_ld(node, out, path="ld"):
    """Rekurzivne posbira textove hodnoty z JSON-LD."""
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str) and k in LD_TEXT_KEYS and has_letters(v):
                out.append((f"{path}.{k}", v))
            else:
                walk_ld(v, out, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk_ld(v, out, f"{path}[{i}]")


def extract(html):
    found = []  # (kind, ctx, text)

    # 1) <title>
    for m in re.finditer(r"<title>(.*?)</title>", html, re.S):
        found.append(("title", "<title>", m.group(1).strip()))

    # 2) meta content
    for m in re.finditer(r"<meta\b[^>]*>", html):
        tag = m.group(0)
        nm = re.search(r'name="([^"]+)"', tag)
        pr = re.search(r'property="([^"]+)"', tag)
        key = (nm or pr).group(1) if (nm or pr) else None
        if key and (key in META_NAMES or key in META_PROPS):
            c = re.search(r'content="([^"]*)"', tag)
            if c and has_letters(c.group(1)):
                found.append(("meta", key, c.group(1)))

    # 3) JSON-LD
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            found.append(("ld-raw", "NEPARSOVATELNE", m.group(1)[:200]))
            continue
        out = []
        walk_ld(data, out)
        for path, val in out:
            found.append(("ld", path, val))

    # 4) atributy v tele
    body = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", html, flags=re.S)
    for attr in ATTRS:
        for m in re.finditer(rf'\b{attr}="([^"]*)"', body):
            v = m.group(1)
            if has_letters(v) and not v.startswith(("http", "/", "#")):
                found.append(("attr", attr, v))

    # 4b) retezce uvnitr inline <script> - hlasky formulare, popisky prepinacu.
    # Bereme jen literaly, ktere vypadaji jako veta pro uzivatele, ne jako kod.
    for sm in re.finditer(r"<script(?![^>]*ld\+json)[^>]*>(.*?)</script>", html, re.S):
        for lm in re.finditer(r"'([^'\\\n]{3,200})'|\"([^\"\\\n]{3,200})\"", sm.group(1)):
            v = (lm.group(1) or lm.group(2)).strip()
            if not has_letters(v) or "<" in v or ">" in v:
                continue
            # prozaicky text ma mezeru a nevypada jako selektor/URL/klic
            if " " not in v or re.match(r"^[a-z-]+$", v) or v.startswith(("http", ".", "#", "/")):
                continue
            found.append(("js", "inline <script>", v))

    # 5) textove uzly
    for m in re.finditer(r">([^<>]+)<", body):
        t = m.group(1)
        stripped = t.strip()
        if stripped and has_letters(stripped) and len(stripped) > 1:
            found.append(("text", "", stripped))

    # deduplikace se zachovanim poradi
    seen, uniq = set(), []
    for kind, ctx, text in found:
        if text in seen:
            continue
        seen.add(text)
        uniq.append({"id": len(uniq), "kind": kind, "ctx": ctx, "cs": text})
    return uniq


if __name__ == "__main__":
    src = sys.argv[1]
    html = open(src, encoding="utf-8").read()
    strings = extract(html)
    words = sum(len(s["cs"].split()) for s in strings)
    json.dump({"source": src, "strings": strings},
              open(sys.argv[2], "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"{src}: {len(strings)} unikatnich retezcu, ~{words} slov -> {sys.argv[2]}")
