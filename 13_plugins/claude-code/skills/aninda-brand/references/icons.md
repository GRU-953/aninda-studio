<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# Icons, tiles and app icons

Ten files, one decision, and one exception that exists for exactly one purpose.

**Licence of this document:** PolyForm Noncommercial 1.0.0. The icon artwork
itself is **not licensed at all** — see `references/logo.md`.

---

## The decision, and what it costs

**One rounded icon is used on every surface, Apple included.** Owner's decision,
14 August 2026.

This knowingly departs from Apple's current guidance, which asks for **square,
full-bleed, unmasked, layered** artwork at 1024 × 1024 (1088 for watchOS). The
system applies the mask itself — a rounded rectangle on iOS, iPadOS and macOS, a
**circle on watchOS and visionOS** — and derives its Liquid Glass specular
highlights from the layer edges. Apple's own wording is that pre-masked artwork
"negatively impacts specular highlight effects" and makes edges "look jagged".

What was actually measured here: in a static render the difference is small, and
on watchOS and visionOS it is **nil**, because the circular mask cuts well inside
the rounding. The dynamic cost could not be measured outside Apple's own
renderer, and is not claimed either way.

---

## The files

| File | Size | Shape | Use |
| --- | --- | --- | --- |
| `icon-1024.svg` | 1024 | rounded | the everyday icon, every platform |
| `icon-1088-watch.svg` | 1088 | rounded | watchOS |
| `icon-512.svg` | 512 | rounded | general |
| `icon-192.svg` | 192 | rounded | web manifest, Android |
| `tile-web.svg` | 100 | rounded | the web tile and favicon source |
| `icon-appstore-square-1024.svg` | 1024 | **square, fully opaque** | App Store submission only |

The five rounded files each show 4.7 % background at the corners, which is what
tells you the rounding is baked in. The App Store file shows 0.0 %, because it is
square and full-bleed.

---

## The one exception

**If you ever submit to the App Store, use `icon-appstore-square-1024.svg`.**
Icon Composer expects unmasked layers. Handing it a pre-rounded file is the case
where the trade-off above stops being small.

`scripts/asset.py` **refuses** to produce the App Store master with a radius
applied. That file is square by definition, and a rounded version of it is not a
variant — it is the wrong file.

---

## Corner radius

The rounded files use 24 % of the width, which comes from this system's own
`radius.hero` token.

**Apple publishes no app-icon corner radius.** Any percentage attributed to
Apple is invented. Apple's icon geometry is concentric with the hardware bezel,
so no fixed percentage can be right for every device; SwiftUI's
`ConcentricRectangle` exists precisely to avoid a hard-coded value.

---

## Safe field

Every icon keeps the mark inside a 90-unit field on the 100-unit grid, and the
worst corner sits 45.00 of 45 units from the centre. That is inside both the
90-unit field and the circle that watchOS and visionOS mask to, at both stroke
weights. Those numbers are from `assets/marks/manifest.json` and were computed,
not estimated.

---

## Variant counts, and why sources disagree

Apple's own material is inconsistent about how many icon variants exist: the
Human Interface Guidelines spec table lists **6**, the prose says **4**, and Icon
Composer authors **3** (Default, Dark, Mono). If you need a number, say which of
the three you are quoting.

---

## Verified against

- Apple Human Interface Guidelines, checked 14 August 2026.
- `assets/marks/manifest.json`, generated 14 August 2026.
- Apple states no WCAG version and makes no conformance claim.
