<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# WCAG 2.2 AA — the criteria this checker touches

**WCAG 2.2 is a W3C Recommendation of 12 December 2024.** Verified against the
primary source on 14 August 2026.

**Licence:** PolyForm Noncommercial 1.0.0.

---

## What the checker measures, and under which criterion

| Criterion | Level | The number | What the checker does |
| --- | --- | --- | --- |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 for body text, 3:1 for large text | Measures every foreground and background pair it can resolve in the source, in all four themes |
| 1.4.11 Non-text Contrast | AA | 3:1 | Applies this to borders, focus rings and meaningful graphics |
| 1.4.6 Contrast (Enhanced) | AAA | 7:1 | Reported only with `--aaa` |
| 2.4.7 Focus Visible | AA | — | Flags `outline: none` on a focus selector with nothing put back |
| 2.5.8 Target Size (Minimum) | AA | 24 × 24 CSS px | Flags a declared height or width below the floor on an interactive selector |
| 2.3.1 Three Flashes or Below Threshold | A | 3 per second | Not measurable from source. Named as a blind spot |
| 2.3.3 Animation from Interactions | AAA | — | Flags a transition or animation with no `prefers-reduced-motion` block |

---

## Four things that are commonly got wrong

**1. WCAG defines no AAA level for non-text contrast.** There is 1.4.11 at AA
and nothing above it. A border measuring 3.9:1 has **fully met** 1.4.11 — it is
not "close to AAA", because no such level exists. Reporting it as a near-miss is
a false failure.

**2. APCA is not normative and is not in WCAG 3.0.** WCAG 3.0 is a Working
Draft. Any tool reporting an APCA figure as a WCAG result is reporting something
that is not a WCAG result. This checker uses the relative-luminance formula from
WCAG 2.2 and nothing else.

**3. 2.4.11 Focus Not Obscured (Minimum) says *entirely*, not *partly*.** A focus
indicator half hidden behind a sticky header has met the AA criterion. The AAA
version, 2.4.12, is the one that asks for no obscuring at all. Do not report the
AA criterion as failed when part of the ring is visible.

**4. Target size is 24 × 24 CSS px at AA, not 44.** 44 is Apple's stated default
and 48 dp is Android's minimum. Both are platform guidance, not WCAG. This system
uses 44 as its own default, and that is a house choice — say which one you are
quoting.

---

## The four themes and the two targets

| Theme | Text | Non-text |
| --- | --- | --- |
| light | 4.5:1 | 3.0:1 |
| dark | 4.5:1 | 3.0:1 |
| hc-light | 7.0:1 | 4.5:1 |
| hc-dark | 7.0:1 | 4.5:1 |

The high-contrast themes are held to the AAA text figure of 7:1. **The 4.5:1 in
the last column is a house rule and not a WCAG level**, because WCAG has no AAA
level for non-text. Do not describe it as AAA conformance.

---

## Forced colours

Not a WCAG criterion, and a system rule instead. Three parts:

1. Every brand colour must be overridden. A hex that survives forced-colors mode
   defeats the point of the mode.
2. `forced-color-adjust: none` is forbidden unless explicitly allow-listed with a
   stated reason.
3. All four status colours resolve to `CanvasText`, so nothing may rely on colour
   alone. Every state carries a glyph and a word regardless.

The third of these overlaps 1.4.1 Use of Color (level A), and goes further: 1.4.1
asks that colour is not the only means of conveying information, and this asks for
a word **and** a glyph, every time.

---

## What no platform gives you

- **Apple states no WCAG version and makes no conformance claim.** It publishes
  no contrast ratio for text over materials, no app-icon corner radius, and no
  motion durations or easing curves. A number attributed to Apple for any of
  those is invented.
- **Material's own accessibility figures** are its own, not WCAG's. Android's
  48 dp minimum is Material guidance.
- Neither Apple nor Google publishes a brand book. Both publish a design system
  and keep brand identity private. A design system and a brand book are two
  different artefacts.

---

## When a script is not enough

Measure a rendered page in a real browser rather than from source whenever the
answer matters. `08_components/check.py` in the main project drives Chromium,
measures the focus ring from actual pixels, and checks each card at 360, 768 and
1280 CSS px. It reports its own blind spots too, and one of them is worth
repeating: transitions are frozen for the whole run, so every reading is of a
resting state.

Past both of those, some things need a person. Whether a heading structure makes
sense, whether an `alt` text describes the right thing, and whether someone can
finish the task — none of those is measurable, and no script should imply
otherwise.
