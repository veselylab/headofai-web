# Build tooling pro headofai.cz (i18n)

`../index.html` (produkce) je **GENEROVANÝ**. Needituj ho přímo — přepíše se při dalším buildu.

## Architektura
- **`../.source.html`** = zdroj = čistá česká verze webu (builder export). Tady se edituje layout a český text.
- **`i18n_build.py`** = nakeyuje texty ve `.source.html` na `{{ t.KEY }}`, vloží `STRINGS`/`LANGS` + přepínač
  jazyků + `dir` (RTL pro arabštinu) do builder frameworku a zapíše výsledek do `../index.html`.
- Překlady: klíče se definují v `i18n_build.py` funkcí `k(key, cs, en, sk, de, uk, ar)`;
  `extra.py` = doplňkové SK/DE/UK/AR překlady; `TM.json` = translation memory ze starší 6-jazyčné verze.

## Jak iterovat
1. **Layout / český text** → edituj `../.source.html`.
2. **Překlady** → `i18n_build.py` (`k(...)`) nebo `extra.py`.
3. **Přegeneruj** (z rootu repa):  `python3 .build/i18n_build.py index.html`
4. `git add .source.html index.html && git commit && git push`  → Pages nasadí za ~1 min.

## Pozor
- Builder renderuje `{{ t.KEY }}` jako **textContent** → `&amp;` se zobrazí doslova (ve STRINGS musí být `&`);
  odkazy uvnitř textu nejdou → text se dělí na segmenty s `<a>` mezi (viz bio projekty).
- `../.nojekyll` je nutné (Pages jinak ignoruje `_ds/` kvůli podtržítku).
- Jazyky: CZ / EN / SK / DE / UK / AR.
