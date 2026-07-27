# Anglická verze `/en/` — jak se udržuje

> **Anglické stránky v `en/` jsou od 2026-07-27 plnohodnotné zdrojové soubory.
> Edituj je PŘÍMO, stejně jako české `index.html`. Nic je nepřegenerovává.**

Tohle není build pipeline. Skripty v `i18n-en/` posloužily k jednorázovému
vytvoření anglické větve; leží tu jen jako doklad, čím vznikla, a jako datový
podklad, kdyby se překlad dělal znovu od nuly. **Nespouštěj je nad produkcí** —
přepsaly by ruční úpravy v `en/`, přesně jako by to udělal `i18n_build.py`
u `index.html` (viz `README.md`).

## Párování stránek

| CZ | EN |
|---|---|
| `index.html` | `en/index.html` |
| `co-je-head-of-ai.html` | `en/what-is-head-of-ai.html` |
| `kdy-firma-potrebuje-head-of-ai.html` | `en/when-does-a-company-need-a-head-of-ai.html` |
| `fractional-vs-fulltime-caio.html` | `en/fractional-vs-fulltime-caio.html` |
| `plat-chief-ai-officer.html` | `en/chief-ai-officer-salary.html` |

`zasady-ochrany-osobnich-udaju.html` anglický protějšek **nemá** — je to právní
text a anglická homepage na něj odkazuje v češtině.

## Na co si dát pozor při editaci

- **Změna v CZ = změna i v EN.** Obě verze jsou ruční, nic je nesynchronizuje.
  Když upravíš text na homepage, uprav i `en/index.html`, jinak se rozejdou.
- **Přepínač jazyků** (`<div class="lang-switch">`) je v hlavičce každé stránky.
  Aktivní vlajka se pozná podle `aria-current="true"`. Vlajky jsou inline SVG
  schválně — emoji vlajky se na Windows nevykreslují.
- **`hreflang` + `canonical`** v hlavičce musí ukazovat na správnou dvojici.
  Při přidání nové stránky doplň obojí a přidej ji do `sitemap.xml`.
- **Cesty k assetům v `en/` musí být od kořene** (`/assets/...`), ne relativní —
  z podadresáře by relativní cesta minula cíl.
- **Formulář na EN homepage** se drží selektoru `form[aria-label="Call booking"]`
  v inline `<script>`. Když změníš `aria-label`, změň i selektor, jinak
  odesílání přestane fungovat.

## Obsah `i18n-en/`

- `extract.py` — vytáhne ze stránky překladatelné řetězce (text, atributy,
  meta, JSON-LD, hlášky v inline JS) do JSON
- `apply.py` — dosadí překlady zpět; nahrazuje podle kontextu, ne přes celý
  dokument (jinak by krátký řetězec „je“ rozbil anglická slova jako „project“)
- `navswitch.py` — vloží přepínač jazyků, `hreflang`, `canonical`, `og:url`
- `*.json` — vytěžené české řetězce
- `*.en.json` — jejich anglické překlady, klíčované na `id`
