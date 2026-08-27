<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# The mark and the wordmark

**The name, the mark, the wordmark, the tile and any lockup of them are not
licensed at all.** No licence is granted to any of it, by this file or any other.
The system around them is Apache-2.0 and free to reuse; the identity is not.
Fork the system and put your own name and mark on it — that is the intended use,
and it costs nothing.

**Licence of this document:** PolyForm Noncommercial 1.0.0.

---

## What the mark is

A single-storey lowercase `a`: a circle tangent to a stem that overruns
**downward**. Running the stem upward makes a `d`, which was the flaw in the
first draft.

Drawn on a 100 × 100 grid:

| Part | Value |
| --- | --- |
| Circle centre | 44, 58 |
| Circle radius | 28 |
| Stem x | 72 |
| Stem top | 30 |
| Stem bottom | 94 |
| Safe field | 90 of 100 |

---

## Stroke weight — two, and the rule is a size

| Weight | Stroke | When |
| --- | --- | --- |
| Regular | 9 | at 24 px and above |
| Heavy | 15 | below 24 px |

At small sizes a 9-unit stroke thins to nothing, so the heavy weight exists to
hold the shape. This is a rendering rule, not a stylistic choice: below 24 px,
use heavy.

---

## The size floor

`scripts/asset.py` refuses the mark below **16 px**. At 16 px the heavy stroke
renders at 2.4 px and the circle's counter — the enclosed white space — is about
5.6 px across. Below that the counter closes and the mark reads as a filled blob.

**This floor is the studio's own, derived from the stroke geometry above.** It is
not in `04_mark/manifest.json`; the manifest states the stroke rule and the safe
field but no minimum size. It is stated here so that a refusal can name where it
came from.

---

## Clear space

**Clear space is half the mark's own height on all four sides.** At the regular
weight the drawn mark is 73 units tall on the 100-unit grid, so the clear space is
36.5 units; at the heavy weight the mark is 79 units and the clear space is 39.5.
`04_mark/manifest.json` is where that rule lives, and `scripts/asset.py` reads it
from there.

This was stated two incompatible ways until 18 August 2026. The marks card in
`08_components/` said **one stroke width** — 9 units at the regular weight, about
four times smaller — presented under the same green tick the system uses for a
verified fact. The manifest won, because it is the output of the builder that owns
the mark, and `08_components/build.py` now reads the sentence out of the manifest
instead of carrying its own copy. If you find two statements of a rule in this
system again, do not quietly follow one: say which file each came from.

---

## Colour: the mark has none

The mark is drawn in `currentColor`. It takes whatever theme it lands in, and in
forced-colors mode it yields to the operating system's palette.

Three things are never done to it:

1. **Never recolour it.** No brand colour fills, no gradients, no two-tone.
2. **Never add a shadow.**
3. **Never stretch it.** The aspect ratio is 1:1 and stays 1:1.

`scripts/asset.py` refuses all three.

---

## The wordmarks

| File | What it is | Advance |
| --- | --- | --- |
| `wordmark-latin.svg` | "aninda studio", 13 code points, 13 glyphs. Recolourable. | 653.2 |
| `wordmark-latin-colour.svg` | The same, one primary per letter. Not recolourable. | 653.2 |
| `wordmark-latin-colour-on-white.svg` | Four colours on a pure white plate. | 793.2 |
| `wordmark-latin-black-on-white.svg` | Black on a pure white plate. | 793.2 |
| `wordmark-latin-white-on-black.svg` | White on a pure black plate. | 793.2 |

A **plate** is the wordmark with a ground behind it, for handing to somebody who
needs one file rather than a transparent asset and a surface to put it on. The
padding is half the wordmark's own drawn height, which is the clear-space rule
applied to the wordmark; it is derived, not chosen. None of them carries a corner
radius: the tile radius is 24 units per 100 of an **icon's** side, and a plate
2.84 times wider than it is tall has no side to take a proportion of.

A Bangla wordmark stood beside these until 27 August 2026, shaped through HarfBuzz
with a negative control proving the conjuncts formed. It went with the Bangla.

All of them are outlines, so none needs a font installed. Never re-typeset a
wordmark from live text.

---

## Verified against

- `04_mark/manifest.json`, generated 14 August 2026, with HarfBuzz 14.3.0.
- The clear-space contradiction above is a finding, not a rule. Dated
  14 August 2026.
