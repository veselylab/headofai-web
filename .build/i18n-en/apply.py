#!/usr/bin/env python3
"""Vytvori anglicky klon stranky.

Zasadni pravidlo: nahrazuje se podle KONTEXTU, ne slepe pres cely dokument.
Kratky retezec jako "je" se smi trefit jen jako cely textovy uzel (>je<),
jinak by rozbil kazde anglicke slovo, ktere ho obsahuje (project -> proforct).
"""
import json
import re
import sys

# CZ soubor -> EN soubor (pro prepis internich odkazu)
SLUGS = {
    "co-je-head-of-ai": "what-is-head-of-ai",
    "kdy-firma-potrebuje-head-of-ai": "when-does-a-company-need-a-head-of-ai",
    "fractional-vs-fulltime-caio": "fractional-vs-fulltime-caio",
    "plat-chief-ai-officer": "chief-ai-officer-salary",
}

CZ_DIACRITICS = "ěščřžýáíéůúňťďóĚŠČŘŽÝÁÍÉŮÚŇŤĎÓ"


def sub_count(pattern, repl, html):
    """Nahrad a vrat (novy_html, pocet)."""
    new, n = re.subn(pattern, repl, html)
    return new, n


def replace_one(html, kind, cs, en):
    """Vrati (html, pocet_nahrad).

    Zamerne zkousi VSECHNY bezpecne kontexty, ne jen ten, ve kterem extraktor
    retezec poprve nasel: tataz veta byva soucasne v JSON-LD i ve viditelnem
    FAQ, nebo v aria-label i v nadpisu. Kazdy vzor je vazany na kontext,
    takze i dvoupismenny retezec ("je") se trefi jen jako cely uzel.
    """
    e = re.escape(cs)
    lit = en.replace("\\", "\\\\")  # aby se \1 apod. v prekladu nebral jako backreference
    total = 0

    # kompletni textovy uzel, vcetne pripadnych mezer kolem
    html, n = sub_count(rf"(>)(\s*){e}(\s*)(<)", rf"\g<1>\g<2>{lit}\g<3>\g<4>", html)
    total += n
    # hodnota atributu
    html, n = sub_count(rf'="{e}"', f'="{lit}"', html)
    total += n
    # <title>
    html, n = sub_count(rf"<title>\s*{e}\s*</title>", f"<title>{lit}</title>", html)
    total += n
    # hodnoty v JSON-LD a literaly v JS - vzdy v uvozovkach
    html, n = sub_count(rf'"{e}"', f'"{lit}"', html)
    total += n
    html, n = sub_count(rf"'{e}'", f"'{lit}'", html)
    total += n
    return html, total


def main():
    src, ext_path, en_path, dst = sys.argv[1:5]
    html = open(src, encoding="utf-8").read()
    data = json.load(open(ext_path, encoding="utf-8"))
    en_map = json.load(open(en_path, encoding="utf-8"))

    extra = en_map.pop("_extra", {})  # doslovne nahrady (hlasky slepene s HTML v JS)

    missing = [s["id"] for s in data["strings"] if str(s["id"]) not in en_map]
    if missing:
        print(f"  CHYBI preklad u {len(missing)} retezcu: {missing[:12]}")
        sys.exit(1)

    # nejdriv nejdelsi - kratky retezec by jinak ukousl kus delsiho
    strings = sorted(data["strings"], key=lambda s: len(s["cs"]), reverse=True)

    not_found = []
    for s in strings:
        en = en_map[str(s["id"])]
        html, n = replace_one(html, s["kind"], s["cs"], en)
        if n == 0:
            not_found.append((s["id"], s["kind"], s["cs"][:60]))

    for cs, en in sorted(extra.items(), key=lambda kv: -len(kv[0])):
        if cs not in html:
            not_found.append(("extra", "-", cs[:60]))
        html = html.replace(cs, en)

    # jazyk dokumentu
    html = html.replace('<html lang="cs">', '<html lang="en">', 1)
    # interni odkazy na CZ podstranky -> EN protejsky
    for cz, en in SLUGS.items():
        html = html.replace(f'href="/{cz}"', f'href="/en/{en}"')
        html = html.replace(f'href="/{cz}.html"', f'href="/en/{en}.html"')
    # odkazy na homepage a jeji kotvy musi zustat v anglicke vetvi,
    # jinak by navigace anglicke podstranky shodila navstevnika do cestiny
    html = html.replace('href="/"', 'href="/en/"')
    html = re.sub(r'href="/#', 'href="/en/#', html)
    # diagram setupu v anglicke verzi
    html = html.replace("assets/my_setup_cze.png", "/assets/setup_eng.png")
    # /en/ je o uroven niz - kazdy relativni asset musi jit od korene,
    # vcetne zapisu "./neco" (ten by z /en/ miril na /en/neco)
    html = re.sub(r'(src|href)="\./', r'\1="/', html)
    html = re.sub(
        r'(src|href)="(?!/)(assets/|david_560|hero-boardroom|profile_pic|logo_veselyai|'
        r'favicon|styles\.css|script\.js|support\.js|_ds/)',
        r'\1="/\2', html)

    open(dst, "w", encoding="utf-8").write(html)

    print(f"  {dst}")
    print(f"    nahrazeno: {len(strings) - len(not_found)}/{len(strings)}")
    if not_found:
        print(f"    NEDOSAZENO ({len(not_found)}):")
        for i, k, t in not_found[:15]:
            print(f"      [{i}] ({k}) {t}")

    # kontrola: co v anglicke verzi zbylo cesky
    body = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", html, flags=re.S)
    left = set()
    for m in re.finditer(r">([^<>]*[" + CZ_DIACRITICS + r"][^<>]*)<", body):
        t = m.group(1).strip()
        if t:
            left.add(t)
    if left:
        print(f"    ZBYVA CESKY TEXT ({len(left)}):")
        for t in sorted(left)[:15]:
            print(f"      {t[:70]}")


if __name__ == "__main__":
    main()
