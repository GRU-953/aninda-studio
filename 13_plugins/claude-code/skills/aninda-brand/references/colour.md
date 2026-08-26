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

**Primitives** are four ramps of eleven steps: `ground`, `accent`, `success`,
`danger` — Natural Gray, Natural Blue, Natural Green and Natural Red. Steps run
50, 100, 200 … 900, 950. Never use a primitive directly in a design. It cannot
follow a theme.

Each ramp CONTAINS its brand colour exactly. The step nearest the anchor is
overwritten with the anchor itself, so `#224959` is literally in the accent ramp
rather than approximated by a neighbour of it.

**Pure Black and Pure White are anchors, not ramps.** Neither has eleven distinct
steps to give: black is the floor of the lightness axis and white its ceiling.
They are used directly — as the body text colour and as the page — which is what
makes the light theme's prose a measured 21:1.

**Semantic roles** are the names below. These are what you use. Each one holds a
different value in each of the four themes, so a design written in roles works in
all four without being rewritten.

Two roles double up, because four hues cannot fill six jobs, and both say so:

- **`color.status.warning` is Natural Gray.** The palette has no amber. Warning
  takes the first grey step beyond the muted text colour, so a caution is visibly
  heavier than quiet prose without becoming the body text colour.
- **`color.status.info` is the accent.** Natural Blue carries links, focus, the
  primary action and information. With four hues there is no fifth colour to
  separate a note from a link, and deriving a near-identical second blue to avoid
  saying so would be worse than saying so.

Both were the owner's decisions on 26 August 2026, and the colour engine refuses
any OTHER pair of roles that resolves to one colour unless the direction spec
declares it with a reason.

---

## Every colour value, in all four themes

| Role | light | dark | hc-light | hc-dark |
|---|---|---|---|---|
| `color.surface.lowest` | #FCFBFB | #060505 | #FCFBFB | #060505 |
| `color.surface.low` | #F9F9F8 | #0A0A09 | #F7F7F7 | #0A0A09 |
| `color.surface.base` | #F8F7F7 | #0E0D0D | #F4F3F3 | #0F0E0E |
| `color.surface.high` | #F5F5F4 | #10100F | #EFEFEF | #10100F |
| `color.surface.highest` | #F4F3F3 | #111010 | #ECEBEB | #131212 |
| `color.surface.dim` | #F1F1F0 | #000000 | #E7E7E7 | #000000 |
| `color.surface.bright` | #FFFFFF | #111110 | #FFFFFF | #151515 |
| `color.surface.page` | #FFFFFF | #000000 | #FFFFFF | #000000 |
| `color.ink.default` | #000000 | #FFFFFF | #000000 | #FFFFFF |
| `color.ink.muted` | #605C59 | #84807C | #464341 | #AEAAA6 |
| `color.line.default` | #84807C | #84807C | #605C59 | #84807C |
| `color.accent.default` | #224959 | #6F98AA | #224959 | #8BB2C3 |
| `color.accent.edge` | #577D8D | #577D8D | #426271 | #6F98AA |
| `color.accent.hover` | #1B2D35 | #8BB2C3 | #1B2D35 | #AACBD9 |
| `color.accent.on` | #FCFBFB | #060505 | #FCFBFB | #060505 |
| `color.focus.ring` | #577D8D | #577D8D | #426271 | #6F98AA |
| `color.status.success` | #2C5A3A | #6E9E7A | #1B3020 | #8AB895 |
| `color.status.warning` | #464341 | #94908C | #2C2A28 | #C7C4C1 |
| `color.status.danger` | #A14F39 | #CC765E | #693223 | #E6927B |
| `color.status.info` | #224959 | #6F98AA | #224959 | #8BB2C3 |

In CSS the same roles are `--as-surface-base`, `--as-ink`, `--as-accent` and so
on. Use those, not the hexes above. The hexes are here so you can answer a
question without running anything; they are not for pasting into a design.

The CSS name is not always the role name. `07_tokens/emit_css.py` drops a
trailing `default` segment and a leading `status` one, so `color.ink.default`
becomes `--as-ink` and `color.status.danger` becomes `--as-danger`. Role names
keep both parts, which is why `asset.py contrast --fg accent-default` is right
while a property called `--as-accent-default` does not exist and resolves to
nothing.
`check_plugin.py` measures every `var(...)` reference in every text file across
the three skills — markdown, Python, JSON, CSS and HTML — against the properties
`07_tokens/css/tokens.css` defines. It reads more than markdown now because the
first version read only `*.md`: this document and `SKILL.md` were corrected, and
`aninda-review/scripts/check.py` went on assembling the same nonexistent name at
run time and offering it to a reader as the fix. A name a script builds from parts
is still outside a static sweep, so that script now derives the property with the
rule `emit_css.py` uses and then checks it against the stylesheet before printing
it.

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

## The colour that sits on a fill

`color.accent.on` is the label colour for a filled control. It was added on
26 August 2026; until then there was none, and this page told you to outline the
button instead.

Its value is `surface.lowest`, which is not a new colour — it is what
`components.css` was already painting those labels with. What is new is that it
carries a proof. It is measured as ink against **every** fill that carries it —
`accent`, `accent-hover` and `danger` — and the published figure is the worst of
those, not the flattering one.

That distinction is not academic. In both dark themes the hardest ground turns out
to be `danger` rather than `accent`, so a role proven only against the accent would
publish 6.2931:1 where the true worst is 5.6640:1.

Use it for the label on a filled button and for nothing else. It is not a general
light-on-dark text colour: it is proven against three specific fills, and adding a
fourth fill without measuring it here would leave that fill's label unproven.

## Roles that are not in this system

There are no elevation or shadow tokens. If a design needs a shadow,
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
