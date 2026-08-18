# aninda-studio-tokens

The Aninda Studio design tokens: colour, type, space, shape and motion, in four themes — light, dark, and a high-contrast pair. Every colour pairing was measured rather than chosen, against WCAG 2.2 AA in the ordinary themes and AAA in the high-contrast ones.

## Install

```
pip install aninda-studio-tokens
```

**Not published yet.** On 2026-08-18 I checked the npm registry and the Python Package Index, and neither holds this package. It is built and it works from a checkout of https://github.com/GRU-953/aninda-studio; the command above will work once it is published. I would rather tell you that here than let you find out at the terminal.

## Use it

```python
from aninda_studio_tokens import css, css_path, THEMES

print(THEMES)            # ['light', 'dark', 'hc-light', 'hc-dark']
print(css()[:40])        # every theme, as text
print(css('dark')[:40])  # one theme
print(css_path())        # a pathlib.Path, for copying
```

`css()` returns the stylesheet text; `css_path()` returns a `pathlib.Path`, which is
what you want when copying the file into a build rather than reading it.

```python
from aninda_studio_tokens import TOKENS, THEME_TOKENS

ink = THEME_TOKENS['dark']['color']['ink']['default']
print(ink['$value'])                       # an alias into the ramps
print(TOKENS['color']['ramp']['ground']['950']['$value']['hex'])
```

`TOKENS` is the primitive document — the ramps, scales, families and durations.
`THEME_TOKENS` holds one document per theme, with identical token paths in each.

Each is [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/),
a Final Community Group Report of the W3C Design Tokens Community Group. It is a
Community Group specification and **not** a W3C Standard.

**There is no single combined token document, and that is deliberate.** DTCG has no
theming concept, so each theme is its own file with identical token paths. One
consequence worth knowing: a semantic theme document resolves only when it is merged
with the primitive one, because its role colours are aliases into the ramps.

Each colour carries its proof under `$extensions["studio.aninda"].proof` — the
ratio required, the ratio measured, the worst case under a one-bit perturbation of
both colours, which surface it was hardest against, and the WCAG criterion it
meets. You can check the claim rather than trust it.

## Applying a theme

The stylesheet defines light values on `:root`, follows the reader's system setting
where nobody has chosen, and lets an explicit choice anywhere in the tree win:

```html
<html>                          <!-- follows the system -->
<div data-theme="dark">         <!-- an island, anywhere in the page -->
<div data-theme="hc-light">     <!-- high contrast -->
```

`[data-theme]` is scoped to the attribute and never to `:root`, so a dark panel can
sit inside a light page.

## What the wheel contains

| File | What it is |
|---|---|
| `index.tokens.json` | An index of the token documents. **Not** a token document |
| `tokens/forced-colors.map.json` | The forced-colours map. Deliberately **not** DTCG |
| `tokens/primitive.tokens.json` | The ramps, scales, families and durations. DTCG |
| `tokens/semantic.dark.tokens.json` | The dark theme's roles. DTCG, aliases into the primitives |
| `tokens/semantic.hc-dark.tokens.json` | The hc-dark theme's roles. DTCG, aliases into the primitives |
| `tokens/semantic.hc-light.tokens.json` | The hc-light theme's roles. DTCG, aliases into the primitives |
| `tokens/semantic.light.tokens.json` | The light theme's roles. DTCG, aliases into the primitives |
| `tokens.css` | Every theme in one stylesheet |
| `tokens.dark.css` | The dark theme alone |
| `tokens.hc-dark.css` | The hc-dark theme alone |
| `tokens.hc-light.css` | The hc-light theme alone |
| `tokens.light.css` | The light theme alone |
| `__init__.py`, `py.typed` | The module itself, typed |

There are no `typography.css` or `layout.css` files here. Those two are npm subpath
exports and there is no Python equivalent of a subpath export; the families and the
container widths they set are in the token documents, under `fontFamily` and
`dimension`.

## Fonts are not included

The system uses Literata, Noto Serif Bengali and IBM Plex Mono, all under the SIL
Open Font Licence 1.1. They are not bundled: it would triple the size of this
package, and an OFL font inside an Apache-2.0 package muddies the licence
declaration. The families are named in the token documents; loading them is yours.

One thing to know if you subset IBM Plex Mono yourself: it carries the Reserved
Font Name **"Plex"** — that is the exact string, from the first line of its own
licence file — and subsetting counts as modifying it under OFL 1.1 clause 3, so a
subset may not use that name. The design system's own subset is called
"Aninda Mono" for exactly that reason.

## Licence

Apache-2.0. The name, the mark and the wordmark are **not** licensed — use the
system, put your own identity on it.

Questions: aninda.sh15@gmail.com
