#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator blogu pro headofai.cz.

Jediny zdroj pravdy je .build/blog.json. Tenhle skript z nej vygeneruje:

  index.html            karty v sekci #blog          (mezi <!-- BLOG:CARDS --> a <!-- /BLOG:CARDS -->)
                        pocet omezuje "homepage_limit" v manifestu (hub ukazuje vsechny)
  en/index.html         totez anglicky
  blog/index.html       karty v hubu + ItemList JSON-LD
  en/blog/index.html    totez anglicky
  sitemap.xml           cely soubor vcetne hreflang paru
  llms.txt              seznam clanku      (mezi <!-- BLOG:LINKS --> a <!-- /BLOG:LINKS -->)

Pouziti:
    python3 .build/blog_build.py            zapise zmeny
    python3 .build/blog_build.py --check    jen overi, ze je vse aktualni (exit 1 kdyz ne)

Pridani noveho clanku:
    1. napsat CZ HTML na rootu (kopie sablony z co-je-head-of-ai.html)
    2. napsat EN HTML do en/  (nebo vynechat -> clanek bude jen CZ, viz nize)
    3. pridat zaznam do .build/blog.json (poradi v poli = poradi na webu)
    4. spustit tenhle skript

Clanek bez EN mutace: v manifestu nastav "en": null. Nezobrazi se v EN vypisech
a v sitemap dostane jen CZ URL bez hreflang alternate (falesny alternate je horsi
nez zadny).
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


# ---------------------------------------------------------------- generatory

def homepage_cards(data, lang):
    """Karty do sekce #blog na homepage. Homepage ukazuje jen prvnich N (mrizka 3
    sloupce vypada nejlip pri nasobku 3); kompletni vypis je na /blog/."""
    limit = data.get('homepage_limit')
    out = []
    for a in data['articles']:
        if limit is not None and len(out) >= limit:
            break
        loc = a.get(lang)
        if not loc:
            continue
        img = a.get('image')
        if img and loc.get('alt'):
            thumb = ('            <img class="gthumb" src="%s" alt="%s" width="%d" height="%d" '
                     'loading="lazy" decoding="async">' % (img['card'], esc(loc['alt']), img['w'], img['h']))
        else:
            thumb = '            <span class="gthumb is-empty" aria-hidden="true"></span>'
        read_more = 'Číst článek →' if lang == 'cs' else 'Read article →'
        out.append(
            '          <a class="guide-card" href="%s">\n%s\n'
            '            <span class="gk">%s</span>\n'
            '            <span class="gt">%s</span>\n'
            '            <span class="gd">%s</span>\n'
            '            <span class="garw">%s</span>\n'
            '          </a>' % (url_for(loc['slug']), thumb, esc(loc['kicker']),
                                esc(loc['title']), esc(loc['card']), read_more))
    return '\n'.join(out)


def hub_cards(data, lang):
    """Karty do hubu /blog/."""
    out = []
    for a in data['articles']:
        loc = a.get(lang)
        if not loc:
            continue
        img = a.get('image')
        if img and loc.get('alt'):
            thumb = ('          <img class="pthumb" src="%s" alt="%s" width="%d" height="%d" '
                     'loading="lazy" decoding="async">' % (img['card'], esc(loc['alt']), img['w'], img['h']))
        else:
            thumb = '          <span class="pthumb is-empty" aria-hidden="true"></span>'
        read_more = 'Číst →' if lang == 'cs' else 'Read →'
        out.append(
            '        <a class="post-card" href="%s">\n%s\n'
            '          <span class="pk">%s</span>\n'
            '          <span class="pt">%s</span>\n'
            '          <span class="pd">%s</span>\n'
            '          <span class="pm"><time datetime="%s">%s</time>'
            '<span class="parw" aria-hidden="true">%s</span></span>\n'
            '        </a>' % (url_for(loc['slug']), thumb, esc(loc['kicker']), esc(loc['title']),
                              esc(loc['hub']), a['date'], loc['date_label'], read_more))
    return '\n\n'.join(out)


def itemlist(data, lang, site):
    """ItemList JSON-LD do hubu."""
    items = []
    pos = 0
    for a in data['articles']:
        loc = a.get(lang)
        if not loc:
            continue
        pos += 1
        items.append({'@type': 'ListItem', 'position': pos,
                      'url': site + url_for(loc['slug']), 'name': loc['title']})
    name = 'Články na headofai.cz' if lang == 'cs' else 'Articles on headofai.cz'
    blob = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': name,
            'itemListOrder': 'https://schema.org/ItemListOrderAscending',
            'itemListElement': items}
    return json.dumps(blob, ensure_ascii=False, separators=(',', ':'))


def sitemap(data):
    site = data['site']
    rows = []

    def block(loc, lastmod, changefreq, priority, cs=None, en=None):
        alt = ''
        if cs and en:
            alt = ('    <xhtml:link rel="alternate" hreflang="cs" href="%s"/>\n'
                   '    <xhtml:link rel="alternate" hreflang="en" href="%s"/>\n'
                   '    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>\n' % (cs, en, cs))
        return ('  <url>\n    <loc>%s</loc>\n%s    <lastmod>%s</lastmod>\n'
                '    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>'
                % (loc, alt, lastmod, changefreq, priority))

    for p in data['pages']:
        cs_url, en_url = site + p['cs'], site + p['en'] if p.get('en') else None
        rows.append(block(cs_url, p['lastmod'], p['changefreq'], p['priority'], cs_url, en_url))
        if en_url:
            rows.append(block(en_url, p['lastmod'], p['changefreq'], p['priority'], cs_url, en_url))

    for a in data['articles']:
        cs_url = site + url_for(a['cs']['slug'])
        en_url = site + url_for(a['en']['slug']) if a.get('en') else None
        rows.append(block(cs_url, a['lastmod'], 'monthly', a['priority'], cs_url, en_url))
        if en_url:
            rows.append(block(en_url, a['lastmod'], 'monthly', a['priority'], cs_url, en_url))

    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + '\n'.join(rows) + '\n</urlset>\n')


def llms_links(data):
    site = data['site']
    out = []
    for a in data['articles']:
        out.append('- %s%s — %s' % (site, url_for(a['cs']['slug']), a['cs']['llms']))
    out.append('')
    out.append('Anglické mutace:')
    for a in data['articles']:
        if a.get('en'):
            out.append('- %s%s — %s' % (site, url_for(a['en']['slug']), a['en']['llms']))
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

    for path, lang in (('index.html', 'cs'), ('en/index.html', 'en')):
        planned[path] = replace_marked(read(path), 'BLOG:CARDS', homepage_cards(data, lang), path)

    for path, lang in (('blog/index.html', 'cs'), ('en/blog/index.html', 'en')):
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

    n_cs = len(data['articles'])
    n_en = sum(1 for a in data['articles'] if a.get('en'))
    if check:
        if changed:
            print('NEAKTUALNI: ' + ', '.join(sorted(changed)))
            sys.exit(1)
        print('vse aktualni (%d clanku CZ, %d EN)' % (n_cs, n_en))
    else:
        print('zapsano: ' + (', '.join(sorted(changed)) if changed else 'nic (uz bylo aktualni)'))
        print('%d clanku CZ, %d EN' % (n_cs, n_en))


if __name__ == '__main__':
    main()
