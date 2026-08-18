<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# Naming

One name for one thing, everywhere. If it is the *mark*, it is never also the
*logo* in a different paragraph.

**Licence:** PolyForm Noncommercial 1.0.0.

---

## The vocabulary — use exactly these words

| Word | Means | Never call it |
| --- | --- | --- |
| **mark** | The `a` glyph on its own | logo, icon, symbol, logomark |
| **wordmark** | The set name, Latin or Bangla | logotype, text logo |
| **tile** | The mark on a rounded coloured square | badge, avatar |
| **icon** | An app or platform icon file | logo, favicon |
| **lockup** | Mark and wordmark placed together | combined logo |
| **role** | A semantic colour name such as `ink.default` | variable, colour |
| **ramp** | A primitive scale of eleven steps | palette, family |
| **step** | One value in a ramp, such as `700` | shade, tone, weight |
| **theme** | One of light, dark, hc-light, hc-dark | mode, scheme |
| **card** | One documentation page in the system | doc, page, spec |

---

## Token paths — DTCG

Dot-separated, lowercase, hyphens inside a segment.

```
color.ramp.ground.900
color.surface.base
dimension.space.4
dimension.type.bangla-min
number.scale.bangla.body
duration.motion.colour
cubicBezier.motion.standard
```

An alias is a path in braces: `{color.ramp.ground.950}`.

`$type` may sit on a group and be inherited by every leaf under it. Do not repeat
it on every leaf.

---

## CSS custom properties

Prefix `--as-`, then the role with dots replaced by hyphens, and the `color.` and
`dimension.` prefixes dropped.

| Token | CSS |
| --- | --- |
| `color.surface.base` | `--as-surface-base` |
| `color.ink.muted` | `--as-ink-muted` |
| `dimension.space.4` | `--as-space-4` |
| `dimension.type.body` | `--as-text-body` |
| `dimension.radius.card` | `--as-radius-card` |
| `duration.motion.move` | `--as-duration-move` |
| `cubicBezier.motion.enter` | `--as-ease-enter` |

`--as-` and nothing else. A second prefix means two systems.

---

## Figma

Variables use `/` for grouping, mirroring the token path exactly:
`color/surface/base`, `dimension/space/4`.

Styles use a readable form: `Theme/Surface/Base`, `Latin/Body`, `Bangla/H2`,
`Mono/Caption`, `Focus/Ring`, `Layout/12 column`.

Component variants use Figma's own `Property=Value` form: `Tone=Accent,
Script=Bangla`.

---

## Files

Lowercase, hyphens, no spaces, no capitals, no underscores in a shipped name.

```
mark-regular.svg
icon-appstore-square-1024.svg
semantic.hc-light.tokens.json
forced-colors.map.json
space-and-shape.html
```

A leading underscore means "generated or internal, not a card":
`_cards.json`, `_shot.png`.

Numbered folders keep the pipeline in reading order: `04_mark`, `07_tokens`,
`13_plugins`. Two digits, then an underscore, then a lowercase name.

---

## Skills, commands and packages

| Thing | Form | Example |
| --- | --- | --- |
| Plugin name | lowercase, hyphens | `aninda-studio` |
| Skill name | plugin prefix, then the unit of work | `aninda-brand`, `aninda-repo`, `aninda-review` |
| Command | `/plugin:verb-or-noun` | `/aninda-studio:asset` |
| npm package | lowercase, hyphens, and it says what it holds | `aninda-studio-tokens` |
| PyPI package | the same name as the npm one | `aninda-studio-tokens` |
| GitHub repository | lowercase, hyphens | `GRU-953/aninda-studio` |

The GitHub username `anindastudio` is taken, which is why the repository is the
hyphenated `aninda-studio`. Checked 14 August 2026.

The packages carry `-tokens` on the end because they hold the tokens and nothing
else — not the mark, not the guidebook, not the components. This table used to
give both of them as `aninda-studio`, which is the repository's name, so a reader
following it typed an install command for a package that does not exist. The rule
at the top of this file cuts both ways: one name for one thing means the packages
may not borrow the repository's name either.

---

## The name itself

- English: **Aninda Studio**. Two words, both capitalised.
- Bangla: **অনিন্দ্য স্টুডিও**. Verified string wm-1.
- "Aninda" is the romanised form of অনিন্দ্য. Never write "Anindya" in English
  running text, and never write the English form inside Bangla text.
- Domain: `anindastudio.com`. No hyphen.
