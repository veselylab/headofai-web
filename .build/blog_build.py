#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator blogu pro headofai.cz.

Jediny zdroj pravdy je .build/blog.json. Tenhle skript z nej vygeneruje pro
kazdy jazyk z bloku "languages":

  <home_file>           karty v sekci #blog na homepage  (mezi <!-- BLOG:CARDS --> a <!-- /BLOG:CARDS -->)
                        pocet omezuje "homepage_limit" v manifestu (hub ukazuje vsechny)
  <hub_file>            karty v hubu /blog/ + ItemList JSON-LD

a dale spolecne:

  sitemap.xml           cely soubor vcetne hreflang alternate pro vsechny jazyky
  llms.txt              seznam clanku      (mezi <!-- BLOG:LINKS --> a <!-- /BLOG:LINKS -->)

Pouziti:
    python3 .build/blog_build.py            zapise zmeny
    python3 .build/blog_build.py --check    jen overi, ze je vse aktualni (exit 1 kdyz ne)

Pridani noveho clanku:
    1. napsat CZ HTML na rootu (kopie sablony z co-je-head-of-ai.html)
    2. napsat mutace do en/ resp. de/  (nebo vynechat, viz nize)
    3. pridat zaznam do .build/blog.json (poradi v poli = poradi na webu)
    4. spustit tenhle skript

Clanek bez mutace v nejakem jazyce: v manifestu nastav "en": null / "de": null.
Nezobrazi se ve vypisech daneho jazyka a v sitemap nedostane jeho hreflang
alternate (falesny alternate je horsi nez zadny).

Clanek s obrazkem jen v nekterych jazycich: obrazek je spolecny ("image"), ale
karta se vykresli jen tam, kde ma jazykova mutace vyplneny "alt". Tim jde nechat
grafiku s vypalenym ceskym textem mimo cizojazycne vypisy.

Pridani dalsiho jazyka:
    1. do "languages" pridat blok (code, home, hub, home_file, hub_file, texty)
    2. do "pages" doplnit URL homepage a hubu pod klicem jazyka
    3. do clanku doplnit jazykovy blok (nebo null)
    4. vytvorit HTML soubory a spustit skript
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, '.build', 'blog.json')


def load():
    with open(MANIFEST, encoding='utf-8') as f:
        return json.load(f)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


def url_for(slug):
    """Slug z manifestu -> absolutni cesta na webu."""
    return '/' + slug.lstrip('/')


def esc(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def languages(data):
    return data['languages']


def x_default(data):
    """Jazyk, na ktery miri hreflang x-default (vychozi = prvni v seznamu)."""
    for lg in languages(data):
        if lg.get('x_default'):
            return lg
    return languages(data)[0]


# ---------------------------------------------------------------- generatory

def homepage_cards(data, lang):
    """Karty do sekce #blog na homepage. Homepage ukazuje jen prvnich N (mrizka 3
    sloupce vypada nejlip pri nasobku 3); kompletni vypis je na /blog/."""
    limit = data.get('homepage_limit')
    out = []
    for a in data['articles']:
        if limit is not None and len(out) >= limit:
            break
        loc = a.get(lang['code'])
        if not loc:
            continue
        img = a.get('image')
        if img and loc.get('alt'):
            thumb = ('            <img class="gthumb" src="%s" alt="%s" width="%d" height="%d" '
                     'loading="lazy" decoding="async">' % (img['card'], esc(loc['alt']), img['w'], img['h']))
        else:
            thumb = '            <span class="gthumb is-empty" aria-hidden="true"></span>'
        out.append(
            '          <a class="guide-card" href="%s">\n%s\n'
            '            <span class="gk">%s</span>\n'
            '            <span class="gt">%s</span>\n'
            '            <span class="gd">%s</span>\n'
            '            <span class="garw">%s</span>\n'
            '          </a>' % (url_for(loc['slug']), thumb, esc(loc['kicker']),
                                esc(loc['title']), esc(loc['card']), lang['read_more']))
    return '\n'.join(out)


def hub_cards(data, lang):
    """Karty do hubu /blog/."""
    out = []
    for a in data['articles']:
        loc = a.get(lang['code'])
        if not loc:
            continue
        img = a.get('image')
        if img and loc.get('alt'):
            thumb = ('          <img class="pthumb" src="%s" alt="%s" width="%d" height="%d" '
                     'loading="lazy" decoding="async">' % (img['card'], esc(loc['alt']), img['w'], img['h']))
        else:
            thumb = '          <span class="pthumb is-empty" aria-hidden="true"></span>'
        out.append(
            '        <a class="post-card" href="%s">\n%s\n'
            '          <span class="pk">%s</span>\n'
            '          <span class="pt">%s</span>\n'
            '          <span class="pd">%s</span>\n'
            '          <span class="pm"><time datetime="%s">%s</time>'
            '<span class="parw" aria-hidden="true">%s</span></span>\n'
            '        </a>' % (url_for(loc['slug']), thumb, esc(loc['kicker']), esc(loc['title']),
                              esc(loc['hub']), a['date'], loc['date_label'], lang['read_more_hub']))
    return '\n\n'.join(out)


def itemlist(data, lang, site):
    """ItemList JSON-LD do hubu."""
    items = []
    pos = 0
    for a in data['articles']:
        loc = a.get(lang['code'])
        if not loc:
            continue
        pos += 1
        items.append({'@type': 'ListItem', 'position': pos,
                      'url': site + url_for(loc['slug']), 'name': loc['title']})
    blob = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': lang['itemlist'],
            'itemListOrder': 'https://schema.org/ItemListOrderAscending',
            'itemListElement': items}
    return json.dumps(blob, ensure_ascii=False, separators=(',', ':'))


def sitemap(data):
    site = data['site']
    default = x_default(data)['code']
    rows = []

    def block(loc, lastmod, changefreq, priority, urls):
        """urls = {kod jazyka: absolutni URL}. Alternate se vypisuje jen kdyz
        existuje vic nez jedna mutace — falesny alternate je horsi nez zadny."""
        alt = ''
        if len(urls) > 1:
            parts = ['    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>\n'
                     % (lg['code'], urls[lg['code']])
                     for lg in languages(data) if lg['code'] in urls]
            if default in urls:
                parts.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>\n'
                             % urls[default])
            alt = ''.join(parts)
        return ('  <url>\n    <loc>%s</loc>\n%s    <lastmod>%s</lastmod>\n'
                '    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>'
                % (loc, alt, lastmod, changefreq, priority))

    for p in data['pages']:
        urls = {lg['code']: site + p[lg['code']] for lg in languages(data) if p.get(lg['code'])}
        for lg in languages(data):
            if lg['code'] in urls:
                rows.append(block(urls[lg['code']], p['lastmod'], p['changefreq'], p['priority'], urls))

    for a in data['articles']:
        urls = {lg['code']: site + url_for(a[lg['code']]['slug'])
                for lg in languages(data) if a.get(lg['code'])}
        for lg in languages(data):
            if lg['code'] in urls:
                rows.append(block(urls[lg['code']], a['lastmod'], 'monthly', a['priority'], urls))

    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + '\n'.join(rows) + '\n</urlset>\n')


def llms_links(data):
    """Vychozi jazyk jako hlavni seznam, ostatni mutace pod vlastnim nadpisem."""
    site = data['site']
    default = x_default(data)
    out = []
    for a in data['articles']:
        loc = a.get(default['code'])
        if loc:
            out.append('- %s%s — %s' % (site, url_for(loc['slug']), loc['llms']))
    for lg in languages(data):
        if lg['code'] == default['code']:
            continue
        rows = ['- %s%s — %s' % (site, url_for(a[lg['code']]['slug']), a[lg['code']]['llms'])
                for a in data['articles'] if a.get(lg['code'])]
        if rows:
            out.append('')
            out.append(lg['llms_heading'])
            out.extend(rows)
    return '\n'.join(out)


# ---------------------------------------------------------------- zapis

def replace_marked(text, marker, payload, path):
    start, end = '<!-- %s -->' % marker, '<!-- /%s -->' % marker
    pat = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.S)
    if not pat.search(text):
        sys.exit('CHYBA: v %s chybi marker %s ... %s' % (path, start, end))
    return pat.sub(lambda _: start + '\n' + payload + '\n' + end, text, count=1)


def replace_itemlist(text, payload, path):
    pat = re.compile(r'(<script type="application/ld\+json">\s*)\{[^\n]*"@type":"ItemList".*?(\s*</script>)', re.S)
    if not pat.search(text):
        sys.exit('CHYBA: v %s nenalezen ItemList JSON-LD blok' % path)
    return pat.sub(lambda m: m.group(1) + payload + m.group(2), text, count=1)


def main():
    check = '--check' in sys.argv
    data = load()
    site = data['site']
    planned = {}

    for lang in languages(data):
        path = lang['home_file']
        planned[path] = replace_marked(read(path), 'BLOG:CARDS', homepage_cards(data, lang), path)

        path = lang['hub_file']
        t = replace_marked(read(path), 'BLOG:POSTS', hub_cards(data, lang), path)
        planned[path] = replace_itemlist(t, itemlist(data, lang, site), path)

    planned['sitemap.xml'] = sitemap(data)
    planned['llms.txt'] = replace_marked(read('llms.txt'), 'BLOG:LINKS', llms_links(data), 'llms.txt')

    changed = []
    for path, new in planned.items():
        if read(path) != new:
            changed.append(path)
            if not check:
                with open(os.path.join(ROOT, path), 'w', encoding='utf-8') as f:
                    f.write(new)

    counts = ', '.join('%d %s' % (sum(1 for a in data['articles'] if a.get(lg['code'])), lg['code'].upper())
                       for lg in languages(data))
    if check:
        if changed:
            print('NEAKTUALNI: ' + ', '.join(sorted(changed)))
            sys.exit(1)
        print('vse aktualni (clanku: %s)' % counts)
    else:
        print('zapsano: ' + (', '.join(sorted(changed)) if changed else 'nic (uz bylo aktualni)'))
        print('clanku: %s' % counts)


if __name__ == '__main__':
    main()
