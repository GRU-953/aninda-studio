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
| **wordmark** | The set name | logotype, text logo |
| **tile** | The mark on a rounded coloured square | badge, avatar |
| **icon** | An app or platform icon file | logo, favicon |
| **lockup** | Mark and wordmark placed together | combined logo |

**One exception, and it is deliberate: platform-facing FILENAMES follow the
platform's word, not this one.** A browser looks for `favicon.ico`; LinkedIn's
own interface says "logo"; a profile picture is an avatar everywhere it is
uploaded. So `10_assets/` ships `favicon.ico`, `favicon-16.png`, `avatar-512.png`
and `linkedin-company-logo.png`, and that is right — the person downloading the
file is served better by the name the destination uses than by this table's
vocabulary. The rule above governs PROSE: what these things are called when
written about, in this kit and anywhere else. Without this paragraph the rule was
refuted seven times by the studio's own delivery.
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
dimension.type.caption
number.scale.ratio
duration.motion.colour
cubicBezier.motion.standard
```

An alias is a path in braces: `{color.ramp.ground.950}`.

`$type` may sit on a group and be inherited by every leaf under it. Do not repeat
it on every leaf.

---

## CSS custom properties

The CSS name is not the token path with hyphens. Applied mechanically, that rule
produces a name that does not exist for about half the token set — and it is the
rule that produced `--as-accent-default`, a property no stylesheet defines, which
resolves to nothing and drops the text back to inherited black. The four places
that used the wrong names were corrected; this sentence, which generates them,
was left standing for a round.

`07_tokens/emit_css.py` is the only authority. It does two things to a colour
path and nothing at all to the rest:

- drop a leading `color.` or `status.` segment
- drop a trailing `default` segment

So `color.ink.default` is `--as-ink`, `color.status.danger` is `--as-danger`, and
`color.accent.default` is `--as-accent`. Role names keep both parts, which is why
`asset.py contrast --fg accent-default` is right while `--as-accent-default` is not
a property.

Everything that is not a colour has a fixed family name, not a derived one:

| Token | CSS | Why it is not derivable |
| --- | --- | --- |
| `color.surface.base` | `--as-surface-base` | colour, `color.` dropped |
| `color.ink.default` | `--as-ink` | colour, trailing `default` dropped |
| `color.status.danger` | `--as-danger` | colour, leading `status.` dropped |
| `color.accent.hover` | `--as-accent-hover` | colour, nothing to drop |
| `dimension.space.4` | `--as-space-4` | family `space` |
| `dimension.type.body` | `--as-text-body` | family renamed `type` to `text` |
| `dimension.radius.card` | `--as-radius-card` | family `radius` |
| `fontFamily.mono` | `--as-font-mono` | family renamed to `font` |
| `duration.motion.move` | `--as-duration-move` | `motion` dropped, family `duration` |
| `cubicBezier.motion.enter` | `--as-ease-enter` | `motion` dropped, family renamed `ease` |
| `number.scale.ratio` | `--as-scale-ratio` | family `scale` |

When in doubt, read the property out of `assets/css/tokens.css` rather than
deriving it. `check_plugin.py` compares every `var(--as-…)` in all three skills
against that file, so a name invented here fails the plugin check — but it cannot
read prose, which is why this section had to be corrected by hand.

`--as-` and nothing else. A second prefix means two systems.

---

## Figma

Variables use `/` for grouping, mirroring the token path exactly:
`color/surface/base`, `dimension/space/4`.

Styles use a readable form: `Theme/Surface/Base`, `Latin/Body`, `Latin/H2`,
`Mono/Caption`, `Focus/Ring`, `Layout/12 column`.

Component variants use Figma's own `Property=Value` form: `Tone=Accent,
State=Hover`. A `Script=` property existed until the Bangla left on 27 August
2026; there is one script now, so nothing needs to say which.

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
- "Aninda" is the romanised form of **অনিন্দ্য**, which is why it is not spelled
  "Anindya" — never write "Anindya" in English running text. The Bengali form of
  the name is not set anywhere in this system: the Bengali face left with the
  Bangla on 27 August 2026, so a Bengali run would fall back to whatever font
  the reader's machine happens to have.
- Domain: `anindastudio.com`. No hyphen.
