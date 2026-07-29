# Blog: jak přidat článek

Jediný zdroj pravdy je `.build/blog.json`. Karty na obou homepage, oba huby,
`sitemap.xml` i `llms.txt` se z něj **generují** — needituj je ručně, přepíše se to.

## Postup

1. **CZ článek** — zkopíruj `co-je-head-of-ai.html` na root pod novým slugem,
   přepiš obsah, meta, canonical a 3 bloky JSON-LD.
2. **EN článek** — totéž do `en/`. Když EN mutaci zatím nechceš, přeskoč
   a v manifestu nastav `"en": null` (článek se pak neobjeví v EN výpisech
   a v sitemap dostane jen CZ URL bez hreflang).
3. **Obrázek** (volitelný) — do `assets/blog/`. Karta i hero jsou 3:2
   (`object-fit: cover`). Bez obrázku se vykreslí prázdný placeholder.
4. **Záznam do `.build/blog.json`** — pořadí v poli `articles` = pořadí na webu.
5. **Spusť generátor:**

       python3 .build/blog_build.py

## Kontrola

    python3 .build/blog_build.py --check

Skončí s kódem 1, když vygenerované soubory nesedí s manifestem — hodí se
před commitem nebo v CI.

## Co generátor NEdělá

- **Nepřekládá.** EN soubor musí existovat; překlad je samostatný krok.
- **Nesahá do těla článků.** Hreflang, přepínač jazyků a breadcrumb v samotném
  článku si drží každý soubor sám (kopíruje se ze šablony).

## Pozor

- Značky `<!-- BLOG:CARDS -->`, `<!-- BLOG:POSTS -->` a `<!-- BLOG:LINKS -->`
  v souborech musí zůstat — bez nich generátor skončí chybou.
- `ItemList` JSON-LD v hubech se nahrazuje celý podle `"@type":"ItemList"`.
- Thumbnail `<img>` potřebuje v CSS `height: auto` **a** `max-width: none`,
  jinak vyjde menší než placeholder a karty v řádku se rozjedou.
