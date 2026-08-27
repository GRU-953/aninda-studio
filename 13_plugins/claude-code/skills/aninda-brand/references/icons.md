<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# Icons, tiles and app icons

Fourteen files in four groups, and one decision behind all of them.

**Licence of this document:** PolyForm Noncommercial 1.0.0. The icon artwork
itself is **not licensed at all** — see `references/logo.md`.

---

## The decision, and what it costs

**Each platform gets the icon geometry it asks for.** Owner's decision, 26 August
2026, reversing a decision of 14 August that used one rounded icon everywhere.

Both stores ask for unmasked artwork and both derive something from the edges of
what they are given: Apple its Liquid Glass specular highlights, Google its own
corner mask and drop shadow. Google publishes a figure where Apple does not — a
radius of 30 per cent of the icon size, applied by Play. Supplying pre-rounded
artwork means both follow the wrong geometry, and the cost of that could not be
measured outside their renderers. Supplying what each asks for removes the unknown
rather than accepting it.

The corner shape therefore differs between surfaces. **The size does not**, and
that is measured: the mark fills 59.850 × 67.216 per cent of the Apple frame and
60.958 × 68.461 per cent of Android's visible 72 dp viewport, and the build fails
if that gap ever exceeds two percentage points.

---

## The files

Fourteen, in four groups.

**The web — rounded, because a browser will not round a favicon for you.**

| File | Size | Use |
| --- | --- | --- |
| `tile-web.svg` | 100 | the web tile and the favicon source, at the heavy stroke |
| `icon-1024.svg` | 1024 | the everyday web icon |
| `icon-512.svg` | 512 | avatars and PWA |
| `icon-192.svg` | 192 | web manifest |

**Apple — square, unmasked, three authored appearances.** Apple generates clear
light, clear dark, tinted light and tinted dark from these.

| File | Size | Appearance |
| --- | --- | --- |
| `icon-apple-1024.svg` | 1024 | Default — four colours on white |
| `icon-apple-1088-watch.svg` | 1088 | watchOS |
| `icon-apple-1024-dark.svg` | 1024 | Dark — white on black, opaque |
| `icon-apple-1024-mono.svg` | 1024 | Mono — no ground; the alpha carries the shape |

**Android — three layers on a 108 dp canvas with a 66 dp safe zone.**

| File | Layer |
| --- | --- |
| `icon-android-background-108.svg` | background, flat and opaque |
| `icon-android-foreground-108.svg` | foreground, alpha-driven |
| `icon-android-monochrome-108.svg` | monochrome, alpha-driven, for themed icons |

**The three treatments, for hand-off.** No platform asks for these; they exist so
that the coloured version and both monochromes are available in one place.

| File | Ground | Artwork | Corner |
| --- | --- | --- | --- |
| `icon-1024-black-on-white.svg` | white | black | rounded |
| `icon-1024-white-on-black.svg` | black | white | rounded |
| `icon-square-1024-black-on-white.svg` | white | black | square |

The rounded files each show 4.7 per cent background at the corners, which is what
tells you the rounding is baked in. The square and opaque ones show 0.0. The two
alpha layers show 82.6 and 91.7, because most of the frame is background by
design — the system composites them over something it supplies.

**The coloured mark is never put on black.** Measured against the 3:1 non-text
floor: on white all four primaries clear it, and on black Natural Blue falls to
2.12 and Natural Green to 2.58. That is why the dark appearance is white on black
rather than colour on black.

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
