# aninda-studio-tokens

The Aninda Studio design tokens: colour, type, space, shape and motion, in four themes — light, dark, and a high-contrast pair. Every colour pairing was measured rather than chosen, against WCAG 2.2 AA in the ordinary themes and AAA in the high-contrast ones.

## Install

```
pip install aninda-studio-tokens
```

## Use the stylesheet

```python
import 'aninda-studio-tokens/css';
```

That gives you every theme. The light values apply by default, the reader's system
setting is followed when nobody has chosen, and an explicit choice anywhere in the
tree wins:

```html
<html>                          <!-- follows the system -->
<div data-theme="dark">         <!-- an island, anywhere in the page -->
<div data-theme="hc-light">     <!-- high contrast -->
```

`[data-theme]` is scoped to the attribute and never to `:root`, so a dark panel can
sit inside a light page.

## Use the tokens directly

```python
import tokens from 'aninda-studio-tokens/tokens.json';
```

That file is [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/),
a Final Community Group Report of the W3C Design Tokens Community Group. It is a
Community Group specification and **not** a W3C Standard.

Each colour carries its proof under `$extensions["studio.aninda"].proof` — the
ratio required, the ratio measured, the worst case under a one-bit perturbation of
both colours, which surface it was hardest against, and the WCAG criterion it
meets. You can check the claim rather than trust it.

## What is in here

| Path | What it is |
|---|---|
| `tokens.json` | The DTCG source. Authoritative |
| `css` | Every theme in one stylesheet |
| `css/light`, `css/dark`, `css/hc-light`, `css/hc-dark` | One theme each |
| `typography.css`, `layout.css` | Type and layout properties |

## Fonts are not included

The system uses Literata, Noto Serif Bengali and IBM Plex Mono, all under the SIL
Open Font Licence 1.1. They are not bundled: it would triple the size of this
package, and an OFL font inside an Apache-2.0 package muddies the licence
declaration. `typography.css` declares the families and leaves the loading to you.

One thing to know if you subset IBM Plex Mono yourself: it carries the Reserved
Font Name "IBM Plex", and subsetting counts as modifying it under OFL 1.1 clause 3,
so a subset has to be renamed. The design system's own subset is called
"Aninda Mono" for exactly that reason.

## Licence

Apache-2.0. The name, the mark and the wordmark are **not** licensed — use the
system, put your own identity on it.

Questions: aninda.sh15@gmail.com
