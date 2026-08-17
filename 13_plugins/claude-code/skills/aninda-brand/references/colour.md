<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# Colour

Not one colour in this system was typed by a person. Every value was computed in
OKLCH, gamut-mapped into sRGB, and then measured against every surface it can
land on.

**Licence:** PolyForm Noncommercial 1.0.0. The token files this describes are
Apache-2.0.

---

## The two layers

**Primitives** are six ramps of eleven steps: `ground`, `accent`, `success`,
`warning`, `danger`, `info`. Steps run 50, 100, 200 … 900, 950. Never use a
primitive directly in a design. It cannot follow a theme.

**Semantic roles** are the seventeen names below. These are what you use. Each
one holds a different value in each of the four themes, so a design written in
roles works in all four without being rewritten.

The Bangla names of the ramps are brand names and are exempt from the spelling
rules: মোহনা (ground, "estuary"), জোয়ার (accent, "tidewater"), পলি (success,
"silt"), কাশ (warning), লাল মাটি (danger, "laterite"), বর্ষা (info, "monsoon").

---

## The seventeen roles, in all four themes

| Role | light | dark | hc-light | hc-dark |
|---|---|---|---|---|
| `color.surface.lowest` | #FDFFFE | #0B0C0B | #FCFDFC | #070807 |
| `color.surface.low` | #FBFCFC | #0E100F | #FAFAFA | #0C0C0C |
| `color.surface.base` | #F8FAF9 | #111212 | #F7F8F7 | #0E0F0E |
| `color.surface.high` | #F6F7F7 | #111312 | #F5F5F5 | #111111 |
| `color.surface.highest` | #F3F5F4 | #121313 | #F2F3F2 | #111211 |
| `color.surface.dim` | #F1F2F2 | #060707 | #F1F1F1 | #030303 |
| `color.surface.bright` | #FFFFFF | #121413 | #FFFFFF | #121212 |
| `color.ink.default` | #0D1A17 | #F2F9F7 | #0D1A17 | #F2F9F7 |
| `color.ink.muted` | #41655C | #6F9B90 | #2E4B43 | #8BB5AA |
| `color.line.default` | #578076 | #578076 | #41655C | #6F9B90 |
| `color.accent.default` | #126974 | #42A0AE | #054D56 | #65BAC7 |
| `color.accent.edge` | #278492 | #278492 | #126974 | #42A0AE |
| `color.focus.ring` | #278492 | #278492 | #126974 | #42A0AE |
| `color.status.success` | #2D6C42 | #59A46F | #1D502E | #77BE8B |
| `color.status.warning` | #7C5414 | #B8863E | #5D3C07 | #D2A15F |
| `color.status.danger` | #9B3728 | #E16551 | #752519 | #FB836F |
| `color.status.info` | #316189 | #5C96C8 | #214767 | #7AB1E1 |

In CSS the same roles are `--as-surface-base`, `--as-ink-default`,
`--as-accent-default` and so on. Use those, not the hexes above. The hexes are
here so you can answer a question without running anything; they are not for
pasting into a design.

---

## What each theme is measured against

Contrast ratio — how far apart two colours are in brightness, on a scale from
1:1 to 21:1.

| Theme | Text | Non-text |
| --- | --- | --- |
| light | 4.5:1 | 3.0:1 |
| dark | 4.5:1 | 3.0:1 |
| hc-light | 7.0:1 | 4.5:1 |
| hc-dark | 7.0:1 | 4.5:1 |

The two high-contrast themes are held to the AAA text figure. This is a house
rule, not a WCAG level: **WCAG defines no AAA level for non-text contrast**, so
the 4.5:1 in the last column is the studio's own choice and is not a conformance
claim.

To check a pairing, do not guess:

```
python scripts/asset.py contrast --fg accent-default --bg surface-dim --theme light
```

It prints the measured ratio, the target, and every ground that role does pass on.

---

## Roles that are not in this system

There is **no "on accent" or "on danger" text colour**. Nothing in the system
defines what colour a label should be on top of a filled accent button, so a
filled button is not something you can build correctly from these tokens alone.
Outline it instead: the label sits on a surface, which is the pairing that was
measured.

There are also no elevation or shadow tokens. If a design needs a shadow,
that is a gap in the system, not something to fill in by eye.

---

## Forced colours

`assets/tokens/forced-colors.map.json` maps every role to an operating-system
keyword. It is deliberately not DTCG: these values have no colour space, no
components and no hex, and none of DTCG's thirteen types fits them.

Three rules come out of it:

1. **Every brand colour must be overridden.** A hex that survives forced-colors
   mode defeats the whole point of the mode.
2. `forced-color-adjust: none` is forbidden unless it is explicitly allow-listed
   with a stated reason.
3. All four status colours resolve to `CanvasText`, so **nothing may rely on
   colour alone**. Every state carries a glyph and a word regardless.

---

## Verified against

- WCAG 2.2, a W3C Recommendation of 12 December 2024. AA is 4.5:1 for text,
  3:1 for large text and non-text. AAA is 7:1 for text.
- APCA is **not** in WCAG 3.0 and is not normative. WCAG 3.0 is a Working Draft.
- Checked 14 August 2026.
