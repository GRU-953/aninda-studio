---
name: aninda-brand
description: >-
  Make ONE thing to the Aninda Studio brand and design system — a logo, mark,
  icon, app icon, favicon, wordmark, tile, colour swatch, button, card, page,
  component, email, slide, document or piece of copy. Holds every rule: the
  Estuary colour ramps and the seventeen semantic roles across light, dark,
  hc-light and hc-dark; the Literata, Noto Serif Bengali and Aninda Mono type
  scale with the measured Bangla multiplier and its 12 px floor; the 4 px
  spacing scale and four radii; clear space and stroke weight on the mark; the
  motion durations and easing curves; the plain-English voice with its banned
  words; the verified Bangla strings; the Apache-2.0, PolyForm Noncommercial,
  SIL OFL and unlicensed-identity split; and the naming conventions. Use when
  asked to design, draw, generate, brand, style, theme, write copy for, or make
  an asset, and when asked "what colour", "which font", "how big", "what
  spacing", "is this on-brand", "brand guidelines", "design tokens",
  "tokens.css", "our accent colour", "the mark", "the logo", "app icon", "App
  Store icon", "favicon", "dark mode", "high contrast", "forced colors", or
  "Bangla text". Ships scripts/asset.py, which REFUSES an impermissible
  combination rather than warning about it. For setting up or upgrading a whole
  REPOSITORY — licences, NOTICE, a bilingual README, a CI brand check — use the
  aninda-repo skill instead. For checking something that ALREADY EXISTS against
  the system or WCAG 2.2 AA, use the aninda-review skill instead.
---

<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->

# Aninda Studio — make one asset

This skill makes one thing at a time, correctly. It is the only skill that holds
the rules; the other two point back here.

**Licence:** the scripts, tokens and marks metadata in this skill are
Apache-2.0. The written reference files are PolyForm Noncommercial 1.0.0. The
name, mark, wordmark, tile and lockups are **not licensed at all**. See `NOTICE`.

---

## Read this much, and no more

Reading all ten reference files for every job wastes your context. Read the
short list for the job in front of you.

| The job | Read |
| --- | --- |
| Anything at all | this file, to the end of "The seven rules" |
| Choosing or checking a colour | `references/colour.md` |
| Setting type, or any Bangla text | `references/typography.md`, `references/bangla.md` |
| Spacing, radii, target sizes, grid | `references/layout.md` |
| The mark, the wordmark, clear space | `references/logo.md` |
| An app icon, favicon or tile | `references/icons.md` |
| Anything that moves | `references/motion.md` |
| Any English word that ships | `references/voice.md` |
| A licence header, or a NOTICE line | `references/licence.md` |
| Naming a file, token, class or variable | `references/naming.md` |

---

## The seven rules

These seven cover most of what goes wrong. Everything else is in the references.

1. **Never write a raw value.** Use a token. `var(--as-accent-default)`, never
   `#126974`. `var(--as-space-4)`, never `24px`. A raw value cannot follow a
   theme, and there are four themes.
2. **Four themes, always.** Light, dark, high-contrast light, high-contrast
   dark. Plus `forced-colors`, where every brand colour must yield to the
   operating system's own palette. A colour that survives forced-colors mode
   defeats the point of it.
3. **Never rely on colour alone.** In forced-colors mode all four status
   colours resolve to `CanvasText`, so a red dot carries nothing. Every state
   needs a word and a glyph as well.
4. **Bangla is not translated English.** Use only a string listed as verified in
   `references/bangla.md`. If none fits, leave the English and say so. Writing
   new Bangla here is not allowed.
5. **The words *simply*, *just*, *easy*, *obviously*, *of course* and *clearly*
   are banned**, and so are exclamation marks. British spelling, plain
   international vocabulary, first person singular. `references/voice.md` has
   the rest.
6. **The mark carries no colour of its own.** It is drawn in `currentColor` and
   takes the theme it lands in. Never recolour it, never add a shadow, never
   stretch it.
7. **Four licences, not one.** System and scripts Apache-2.0; written
   documentation PolyForm Noncommercial 1.0.0; fonts SIL OFL 1.1; the identity
   not licensed at all. `references/licence.md` has the exact wording.

---

## Making an asset: use the script

`scripts/asset.py` is the point of this skill. It does not warn — it refuses.

```
python scripts/asset.py list
python scripts/asset.py mark      --weight regular --size 64 --on surface-base --theme light --out mark.svg
python scripts/asset.py wordmark  --script latin --size 240 --on surface-bright --theme light
python scripts/asset.py icon      --size 1024
python scripts/asset.py icon      --appstore
python scripts/asset.py tile      --size 512
python scripts/asset.py swatch    --role accent-default --theme dark --on surface-base
python scripts/asset.py contrast  --fg accent-default --bg surface-dim --theme light
```

It refuses, with the rule and the number, when:

- **the mark is asked for below its size floor.** Below 24 px the stroke changes
  from 9 to 15, and below 16 px the heavy stroke falls under 2.4 px and the
  circle's counter closes up.
- **a colour is asked for on a ground it was never measured against.** Every
  pairing in the system was measured. If yours was not, or it falls below the
  theme's own target, the script says the measured ratio, the target, and which
  grounds do pass.
- **the App Store master is asked for with a radius.** That one file must be
  square and unmasked. Apple's system applies the mask and derives its highlights
  from the layer edges; a pre-rounded edge sits inside the mask and the highlight
  follows the wrong geometry.
- **the mark is asked for in a colour, with a shadow, or at a non-square aspect
  ratio.**

A refusal is the answer. Pass it on in full, offer the nearest permitted option
it named, and do not work around it.

**One honest note about the pairing check.** Against the token files shipped in
this skill, no role fails on any surface in any theme — every one of the 17 × 7 ×
4 pairings was measured and passes. So that particular refusal cannot fire here,
and its passing is the proof the token set is sound rather than proof the check
works. It will fire if the skill is pointed at a different token set, and it does
fire today on a ground that is not a surface at all, or a role that does not
exist.

---

## What is in `assets/`

| Path | What it is |
| --- | --- |
| `assets/tokens/primitive.tokens.json` | 110 primitive tokens. DTCG 2025.10. |
| `assets/tokens/semantic.{light,dark,hc-light,hc-dark}.tokens.json` | 17 semantic roles per theme, identical token paths in each. |
| `assets/tokens/forced-colors.map.json` | Deliberately **not** DTCG. Forced-colors values are operating-system keywords with no colour space, and DTCG's thirteen types hold nothing that fits. |
| `assets/css/tokens.css` | Every token as a CSS custom property, four themes plus a forced-colors block. |
| `assets/marks/*.svg` | The ten mark files, and `manifest.json` with the geometry and the checks it passed. |
| `assets/fonts/*.woff2` | Subset web fonts, each with its own `-OFL.txt` beside it. |

---

## Before you hand anything over

Run the `aninda-review` skill's checker over it. Making something and checking
it are two jobs, and the second one is not this skill's.
