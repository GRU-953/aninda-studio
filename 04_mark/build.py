#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
It draws every Aninda Studio mark, wordmark, lockup and icon artefact, and it
refuses to draw any of them if it cannot do so correctly.

TWO THINGS THE DRAFT GOT WRONG, BOTH FIXED HERE
-----------------------------------------------
1. **The stem ran above the bowl.** A vertical stroke rising above a bowl is an
   ascender, and a bowl with an ascender is a lowercase 'd'. Rendering the draft
   showed it immediately: the mark read as "d aninda studio". The overrun that
   makes this a mark rather than a glyph has to go DOWNWARD.

2. **A 22.46% squircle was baked into the Apple icon.** Verified against Apple's
   current Human Interface Guidelines on 14 August 2026: Apple publishes no corner
   radius, no percentage, and the word "squircle" appears nowhere in its guidance.
   The system applies the mask now, and Apple states plainly that pre-masked
   artwork "negatively impacts specular highlight effects" and makes edges "look
   jagged". So the Apple master here is a SQUARE, fully opaque, unmasked 1024 —
   and the checks below fail the build if a radius ever creeps back in.

   The web tile is different, and the difference is mechanical rather than
   aesthetic: a browser will not round a favicon for you, so that artefact must
   carry its own corner radius. Its radius is 24 units per 100, taken from the
   system's own `radius-hero` token — our decision, derived from our own scale,
   with no claim that it is Apple's number.

WHY watchOS AND visionOS CHANGE THE SAFE AREA
---------------------------------------------
Apple masks to a rounded rectangle on iOS, iPadOS and macOS, but to a CIRCLE on
watchOS and visionOS. A layout that survives a rounded rectangle can still lose
its corners to a circle, so every essential shape here is checked against the
inscribed circle as well as the 90-of-100 safe field.

BANGLA IS SHAPED, NEVER MAPPED
------------------------------
The Bangla wordmark goes through HarfBuzz. Conjuncts join and some vowel signs are
written before the consonant they follow, so pulling glyphs out of a font by code
point produces nonsense that still looks like Bangla to someone who cannot read it.
Gate 3 below is a NEGATIVE control: it runs the naive path deliberately and fails
if the shaped result is identical, because that would mean HarfBuzz is present but
not actually shaping.

EXIT CODES
----------
    0  everything drawn and checked
    1  a real failure — a check did not pass
    2  could not run — a font, a library or Chromium is missing

Nothing is written on 1 or 2. Every artefact is buffered until the last gate has
passed, because writing as it went left rewritten SVGs beside a stale manifest
after a failing build. A missing Chromium is exit 2 rather than a note, because
the render gate is the only check that sees what a renderer produces, and it used
to disappear behind an "ok" line and a successful exit.

RUN
---
    cd <the repository folder>
    export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
    ./.venv/bin/python 04_mark/build.py
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOKENS = ROOT / "07_tokens" / "build"
PALETTE_PROOF = ROOT / "05_colour" / "generated" / "natural.proof.json"
FONTS = ROOT / "06_type" / "candidates"
OUT = HERE / "svg"
RASTER = HERE / "png"

GRID = 100.0
STROKE_REGULAR = 9.0     # at STROKE_SWITCH_PX and above
STROKE_HEAVY = 15.0      # below it
STROKE_SWITCH_PX = 24    # the size the weight changes at
SAFE = 90.0              # essential shapes live inside 90 of the 100 units

# Android's adaptive icon is a different canvas with a different rule, and both
# numbers are Google's rather than this kit's: every layer is 108x108 dp, the outer
# 18 dp on each side is reserved for masking and motion effects, and the 66x66 dp
# centre is the zone no launcher mask may clip.
# developer.android.com/develop/ui/views/launch/icon_design_adaptive,
# page updated 13 August 2026, read 26 August 2026.
ANDROID_GRID = 108.0
ANDROID_SAFE = 66.0
# Read from the token at build time by tile_radius_pct() below, never typed.
TILE_RADIUS_PCT: float | None = None

LATIN_FONT = FONTS / "latin" / "literata" / "Literata[opsz,wght].ttf"
BANGLA_FONT = FONTS / "bangla" / "notoserifbengali" / "NotoSerifBengali[wdth,wght].ttf"

WORD_LATIN = "aninda studio"
WORD_BANGLA = "অনিন্দ্য স্টুডিও"

# The Latin wordmark's own axis settings. Named here because the ligature gate
# proves shaping under the same conditions the artwork is drawn at, and a second
# copy of these two numbers would let the gate and the drawing drift apart.
LATIN_WORDMARK_AXES = {"opsz": 72, "wght": 500}

# The ligature gate's probes. Single words, no spaces, so the glyph count is clean.
#
# Each must collapse AND must produce a glyph that no code point maps to. The
# second half is the half that matters, and it is why "fi" is NOT on this list:
# Literata's cmap maps U+FB01 straight to the `fi` glyph, so a shaper that did
# nothing but look up code points could still produce that collapse. U+FB03 and
# U+FB04 are absent from the same cmap, so `f_f_i` and `f_f_l` can only have
# arrived through a substitution. Measured 27 August 2026:
#
#     cmap maps 1163 code points onto 1163 distinct glyph ids
#     U+FB01 -> 'fi' gid 513        (reachable — useless as evidence)
#     U+FB03 -> None                (unreachable — `f_f_i` gid 505 is evidence)
#     'office'        6 cp ->  4 glyphs, unreachable [505]
#     'fi'            2 cp ->  1 glyph,  unreachable []
#     'aninda studio' 13 cp -> 13 glyphs, unreachable []
LIGATURE_PROBES = ("office", "difficult", "waffle")


class Fail(Exception):
    """A check did not pass. Nothing is written."""


class NotEquipped(Exception):
    """A tool or font is missing. Distinct from a failure."""


# ---------------------------------------------------------------------------
# The mark
# ---------------------------------------------------------------------------

CIRCLE = {"cx": 44.0, "cy": 58.0, "r": 28.0}
STEM_X = CIRCLE["cx"] + CIRCLE["r"]     # tangent to the bowl, by construction
STEM_TOP = CIRCLE["cy"] - CIRCLE["r"]   # the top of the bowl
STEM_BOTTOM = 94.0                      # the overrun, downward


def mark_paths(stroke: float, colours: list[str] | None = None) -> str:
    """The mark: a circle and a tangent stem.

    With no colours it is ONE shape in currentColor, which is what every
    recolourable artefact and every monochrome needs.

    With four colours the bowl is cut into three equal 120-degree arcs and the stem
    stays whole, giving exactly four strokes for four colours. The geometry does not
    move: the arcs trace the same circle at the same radius, so every measurement
    already proven of this mark — the safe field, the inscribed-circle fit, the
    cross-platform size parity — holds without being re-derived. Owner's decision,
    26 August 2026.

    The arcs start at -90 degrees, the top of the bowl, so the first cut falls where
    the stem meets it rather than in the middle of a curve.
    """
    if not colours:
        return (
            f'<circle cx="{CIRCLE["cx"]:g}" cy="{CIRCLE["cy"]:g}" r="{CIRCLE["r"]:g}" '
            f'fill="none" stroke="currentColor" stroke-width="{stroke:g}"/>'
            f'<path d="M{STEM_X:g} {STEM_TOP:g}V{STEM_BOTTOM:g}" stroke="currentColor" '
            f'stroke-width="{stroke:g}" stroke-linecap="round"/>'
        )
    if len(colours) != 4:
        raise Fail(f"the four-colour mark takes exactly four colours, not "
                   f"{len(colours)}")

    cx, cy, r = CIRCLE["cx"], CIRCLE["cy"], CIRCLE["r"]
    parts = []
    for i in range(3):
        a0 = math.radians(-90 + i * 120)
        a1 = math.radians(-90 + (i + 1) * 120)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        # large-arc-flag 0 because each sweep is 120 degrees, sweep-flag 1 to run
        # clockwise, which is the direction the angles above advance in.
        parts.append(
            f'<path d="M{x0:.4f} {y0:.4f}A{r:g} {r:g} 0 0 1 {x1:.4f} {y1:.4f}" '
            f'fill="none" stroke="{colours[i]}" stroke-width="{stroke:g}" '
            f'stroke-linecap="butt"/>')
    parts.append(
        f'<path d="M{STEM_X:g} {STEM_TOP:g}V{STEM_BOTTOM:g}" stroke="{colours[3]}" '
        f'stroke-width="{stroke:g}" stroke-linecap="round"/>')
    return "".join(parts)


def mark_extent(stroke: float) -> tuple[float, float, float, float]:
    """The mark's true drawn bounds, including half the stroke on every side."""
    h = stroke / 2
    return (
        CIRCLE["cx"] - CIRCLE["r"] - h,
        CIRCLE["cy"] - CIRCLE["r"] - h,
        STEM_X + h,
        STEM_BOTTOM + h,
    )


# ---------------------------------------------------------------------------
# Text shaping — the Inkscape replacement
# ---------------------------------------------------------------------------

def shape_to_path(text: str, font_path: Path, size: float,
                  variations: dict | None = None,
                  colours: list[str] | None = None) -> tuple[str, float, float]:
    """Shape `text` through HarfBuzz and return it as SVG paths.

    One group per glyph, always. `colours` cycles through a list, one colour per
    DRAWN glyph, which is what makes a four-colour wordmark possible without
    re-typesetting anything: the shaping is identical and only the fill changes.
    A space draws nothing, so it takes no turn in the cycle and the rhythm of the
    colours follows the letters rather than the string.

    Returns (path_data, advance_width, glyph_count).
    """
    try:
        import uharfbuzz as hb
        from fontTools.ttLib import TTFont
        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.varLib import instancer
    except ImportError as e:
        raise NotEquipped(f"shaping is unavailable: {e}") from e

    if not font_path.exists():
        raise NotEquipped(f"font not found: {font_path}")

    tt = TTFont(str(font_path))
    if variations and "fvar" in tt:
        tt = instancer.instantiateVariableFont(tt, variations, inplace=False)

    upem = tt["head"].unitsPerEm
    scale = size / upem

    # Coverage gate: every code point must be in the cmap. A missing glyph renders
    # as .notdef, which is a visible box no check would otherwise catch.
    cmap = tt.getBestCmap()
    missing = sorted({c for c in text if c != " " and ord(c) not in cmap})
    if missing:
        raise Fail(f"{font_path.name} has no glyph for: "
                   f"{', '.join(f'{c!r} U+{ord(c):04X}' for c in missing)}")

    blob = hb.Blob.from_file_path(str(font_path))
    face = hb.Face(blob)
    hb_font = hb.Font(face)
    if variations:
        hb_font.set_variations(variations)

    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf)

    glyph_order = tt.getGlyphOrder()
    glyph_set = tt.getGlyphSet()

    parts: list[str] = []
    x = 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = glyph_order[info.codepoint]
        pen = SVGPathPen(glyph_set)
        glyph_set[name].draw(pen)
        d = pen.getCommands()
        if d:
            # Font units are y-up, SVG is y-down. The flip is baked into the
            # transform we apply to the coordinates rather than left as an SVG
            # attribute, because an attribute is something a downstream optimiser
            # can drop — and losing it produces upside-down artwork that still
            # passes every "does this parse" check.
            tx = (x + pos.x_offset) * scale
            ty = -pos.y_offset * scale
            fill = ""
            if colours:
                fill = f' fill="{colours[len(parts) % len(colours)]}"'
            parts.append(f'<g transform="translate({tx:.3f},{ty:.3f}) '
                         f'scale({scale:.6f},{-scale:.6f})"{fill}>'
                         f'<path d="{d}"/></g>')
        x += pos.x_advance

    return "".join(parts), x * scale, len(buf.glyph_infos)


def naive_to_glyphs(text: str, font_path: Path) -> list[int]:
    """The WRONG way, on purpose. Used only as a negative control."""
    from fontTools.ttLib import TTFont
    tt = TTFont(str(font_path))
    cmap = tt.getBestCmap()
    order = {n: i for i, n in enumerate(tt.getGlyphOrder())}
    return [order.get(cmap[ord(c)], 0) for c in text if ord(c) in cmap]


def shaped_glyph_ids(text: str, font_path: Path,
                     variations: dict | None = None) -> list[int]:
    """The glyph ids HarfBuzz produces, at the axis settings the artwork uses."""
    import uharfbuzz as hb
    font = hb.Font(hb.Face(hb.Blob.from_file_path(str(font_path))))
    if variations:
        font.set_variations(variations)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf)
    return [g.codepoint for g in buf.glyph_infos]


def cmap_glyph_ids(font_path: Path) -> set[int]:
    """Every glyph id that some code point maps to directly.

    A glyph OUTSIDE this set cannot be reached by looking up code points at all,
    so a shaped run containing one is evidence that substitution happened. This
    is the difference between a ligature that proves something and one that does
    not: a precomposed ligature with its own code point proves nothing.
    """
    from fontTools.ttLib import TTFont
    tt = TTFont(str(font_path))
    order = {n: i for i, n in enumerate(tt.getGlyphOrder())}
    return {order[n] for n in tt.getBestCmap().values() if n in order}


def shaping_gates() -> list[str]:
    """Every shaping gate. All must pass before a single byte is written.

    Two of these were Bangla until 27 August 2026, when the kit stopped shipping
    it. The Latin wordmark cannot do their job: "aninda studio" shapes to 13
    glyphs from 13 code points and the naive cmap path returns the SAME 13, so it
    passes identically whether or not shaping happens. That is precisely the hole
    the Bangla gates were covering, and it is why the replacements use probe words
    rather than the artwork.
    """
    import uharfbuzz as hb
    notes = []

    # G1 — the library is present and reports a version.
    notes.append(f"uharfbuzz present, HarfBuzz {hb.version_string()}")

    # G2/G3 — coverage and shaping, via a positive control on real strings.
    for text, font, label in ((WORD_BANGLA, BANGLA_FONT, "Bangla wordmark"),
                              (WORD_LATIN, LATIN_FONT, "Latin wordmark")):
        _, adv, n = shape_to_path(text, font, 100.0)
        if adv <= 0:
            raise Fail(f"{label}: shaping produced zero advance width")
        notes.append(f"{label}: {len(text)} code points → {n} glyphs, advance {adv:.1f}")

    # G4 — a ligature actually formed, which is what proves GSUB is applied.
    # Two assertions per probe, and the second is the one that carries the weight.
    reachable = cmap_glyph_ids(LATIN_FONT)
    for probe in LIGATURE_PROBES:
        ids = shaped_glyph_ids(probe, LATIN_FONT, LATIN_WORDMARK_AXES)
        if len(ids) >= len(probe):
            raise Fail(
                f"{probe!r} shaped to {len(ids)} glyphs from {len(probe)} code "
                f"points — no ligature formed. HarfBuzz is present but the font's "
                f"GSUB table is not being applied.")
        made = sorted(g for g in ids if g not in reachable)
        if not made:
            raise Fail(
                f"{probe!r} collapsed to {len(ids)} glyphs, but every one of them "
                f"is reachable straight from the cmap, so looking code points up "
                f"one at a time could have produced this. The collapse is real and "
                f"it is not evidence of substitution.")
        notes.append(f"ligature formed: {probe}, {len(probe)} code points → "
                     f"{len(ids)} glyphs, one of them gid {made[0]}, which no code "
                     f"point maps to")

    # G5 — THE NEGATIVE CONTROL. The naive path must produce a different result.
    # A positive control alone cannot catch a fallback shaper that silently does
    # nothing; this can.
    probe = LIGATURE_PROBES[0]
    naive = naive_to_glyphs(probe, LATIN_FONT)
    shaped = shaped_glyph_ids(probe, LATIN_FONT, LATIN_WORDMARK_AXES)
    if naive == shaped:
        raise Fail(
            f"NEGATIVE CONTROL FAILED: mapping each code point of {probe!r} "
            f"straight through the cmap produced exactly the same glyphs as "
            f"HarfBuzz. Shaping is not happening, and every ligature in the "
            f"wordmark would be drawn as separate letters.")
    notes.append(f"negative control passed: naive {len(naive)} glyphs ≠ shaped "
                 f"{len(shaped)} glyphs for {probe}")
    return notes


# ---------------------------------------------------------------------------
# Artefacts
# ---------------------------------------------------------------------------

def svg_doc(body: str, w: float, h: float, colour: str, title: str,
            view: str | None = None, recolourable: bool = False) -> str:
    """One SVG document. Two kinds, and the difference matters.

    `recolourable=True` — the marks and wordmarks. These are drawn entirely in
    `currentColor` and the root carries NO colour of its own, so they take the
    colour of wherever they are placed. That is what lets one file serve all four
    themes.

    The first version put `style="color:#0D1A17"` on the root of every file,
    including these. Inside a page that strips the attribute it looked fine, which
    is exactly why it survived: the marks were invisible on any dark ground for
    every OTHER consumer — a README, a slide, someone else's site — and nothing in
    this repository would ever have noticed. A default that only works because one
    caller patches it is not a default.

    A file with no root colour inherits `currentColor` from its context, and falls
    back to the browser's own text colour when opened on its own. Both are right.

    `recolourable=False` — the tile and the icons. These are fixed artwork: a dark
    ground carrying a light mark, meant to look identical everywhere. Their colours
    are explicit on purpose, and recolouring them would break them.
    """
    root_style = "" if recolourable else f' style="color:{colour}"'
    note = ("<!-- Recolourable: drawn in currentColor, with no colour on the root. "
            "Set `color` on this element or an ancestor. -->") if recolourable else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view or f"0 0 {w:g} {h:g}"}" '
        f'width="{w:g}" height="{h:g}" role="img" fill="none"{root_style}>'
        f"<title>{title}</title>{note}{body}</svg>\n"
    )


def check_apple_master(svg: str) -> None:
    """Apple's current rules, enforced rather than described."""
    lowered = svg.lower()
    for banned, why in (
        ("rx=", "a corner radius is baked in — the system applies the mask now"),
        ("ry=", "a corner radius is baked in — the system applies the mask now"),
        ("opacity", "the master must be fully opaque"),
        ("filter", "blurs and shadows must be stripped; the platform adds them"),
        ("fegaussianblur", "blurs must be stripped"),
        ("clip-path", "masking is the system's job, not the artwork's"),
    ):
        if banned in lowered:
            raise Fail(f"Apple master: {why} (found '{banned}')")


def check_transparent_layer(svg: str, name: str) -> None:
    """A layer whose shape is carried by its alpha must not have a ground drawn
    behind it.

    Apple's Mono appearance and Android's foreground and monochrome layers are all
    composited by the system over something it supplies. A background rect baked
    into any of them defeats that: on Android the launcher's own background layer
    is hidden, and the monochrome silhouette the system tints becomes a filled
    square. This is cheap to get wrong by copying the square master and cheap to
    catch here.
    """
    if "<rect" in svg.lower():
        raise Fail(f"{name}: carries a <rect> ground. This layer is composited over "
                   f"something the system supplies, so its shape has to be carried "
                   f"by the alpha channel alone.")


def icon_placement(stroke: float, grid: float = GRID,
                   safe: float = SAFE) -> tuple[float, float, float, str]:
    """Derive the scale and offset that put the mark safely inside an icon.

    The 90-of-100 safe field is a constraint on an ICON, not on the mark drawn on
    its own — a wordmark lockup has no masking to survive. The first version of
    this check applied it to the bare mark and failed the build for a mark that was
    fine; the constraint belongs here, on the composition.

    The binding constraint is the CIRCLE, not the rounded rectangle, because
    watchOS and visionOS mask to a circle. Fitting the mark's diagonal inside the
    inscribed circle therefore satisfies both masks at once. The scale is computed
    from the mark's own measured bounds rather than chosen by eye, so it stays
    correct if the geometry ever changes.
    """
    x0, y0, x1, y1 = mark_extent(stroke)
    w, h = x1 - x0, y1 - y0
    radius = safe / 2

    half_diagonal = math.hypot(w, h) / 2
    scale = radius / half_diagonal
    if scale > 1.0:
        scale = 1.0

    # Place the mark's centre at the icon's centre.
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    tx = grid / 2 - cx * scale
    ty = grid / 2 - cy * scale

    # Prove it, rather than trusting the arithmetic above.
    corners = [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]
    worst = max(math.hypot(px * scale + tx - grid / 2, py * scale + ty - grid / 2)
                for px, py in corners)
    if worst > radius + 1e-6:
        raise Fail(f"icon placement at stroke {stroke:g}: a corner still sits "
                   f"{worst:.2f} units from centre, outside the {radius:g}-unit "
                   f"inscribed circle")
    # The band was written as the literal 5 to 95, which is (grid - safe) / 2 on
    # the 100-unit grid and silently wrong on any other. Android's canvas is 108
    # with a 66-unit safe zone, where the band is 21 to 87.
    lo, hi = (grid - safe) / 2, grid - (grid - safe) / 2
    for px, py in corners:
        sx, sy = px * scale + tx, py * scale + ty
        if not (lo - 1e-6 <= sx <= hi + 1e-6 and lo - 1e-6 <= sy <= hi + 1e-6):
            raise Fail(f"icon placement at stroke {stroke:g} on a {grid:g}-unit grid: "
                       f"a corner lands at ({sx:.2f},{sy:.2f}), outside the "
                       f"{lo:g}-to-{hi:g} band of the {safe:g}-unit safe field")

    # The figure is worth stating and worth not overstating. The scale above is
    # radius / half-diagonal, so the worst corner lands EXACTLY on the circle
    # whenever the mark is scaled down at all — it is a tautology, not a finding,
    # and the guidebook used to offer it as the evidence that the rounding costs
    # nothing under a circular mask, which is a different question entirely. What
    # the check does earn is the box constraint on the next line: the corners have
    # to fall inside the 5-to-95 band, and that can fail.
    fit = "exactly on" if abs(worst - radius) < 1e-6 else f"{worst:.2f} of {radius:g} from"
    where = "" if grid == GRID else f" on the {grid:g}-unit grid"
    note = (f"icon at stroke {stroke:g}{where}: mark {w:.1f}×{h:.1f} scaled ×{scale:.4f}, "
            f"worst corner {fit} the {radius:g}-unit inscribed circle — the scale is "
            f"derived from the mark's own diagonal, so this is a fit by construction; "
            f"what is tested is that all four corners also land inside the "
            f"{safe:g}-unit field")
    return scale, tx, ty, note


def render_check(docs: dict[str, str], place: dict[float, tuple[float, float, float]],
                 a_scale: float) -> list[str]:
    """Render each icon artefact over a garish background and measure what covers it.

    An Apple master must cover 100% of its frame: square, full-bleed, fully opaque.
    A web tile must NOT, because its rounded corners are the whole point of it —
    a browser will not round a favicon for you.

    It is handed the documents rather than reading 04_mark/svg, because nothing is
    on disk yet when this runs. Writing before the last gate had passed left
    rewritten SVGs beside a stale manifest after a failing build, which broke the
    one promise that makes the manifest worth reading.
    """
    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image
    except ImportError as e:
        raise NotEquipped(f"render check unavailable: {e}") from e
    import io

    notes: list[str] = []

    # A recolourable file must carry NO colour on its root. If it does, it is
    # invisible on any ground that matches that colour, for every consumer that
    # does not happen to strip the attribute — a README, a slide, someone else's
    # page. This is checked by reading the file rather than by rendering, because
    # the failure is in the file and a render inside a page that patches it looks
    # perfectly fine.
    for name in ("mark-regular.svg", "mark-heavy.svg",
                 "wordmark-latin.svg", "wordmark-bangla.svg"):
        head = docs[name][:400]
        if "style=\"color:" in head.split("<title>")[0]:
            raise Fail(
                f"{name} sets a colour on its root element. It is meant to be "
                f"recolourable, so it must inherit currentColor — otherwise it "
                f"disappears on a ground of that colour everywhere except in pages "
                f"that strip the attribute."
            )
        if "currentColor" not in head:
            raise Fail(f"{name} is not drawn in currentColor, so it cannot recolour")
    notes.append(f"4 recolourable files carry no root colour and draw in currentColor")

    PROBE = (255, 0, 255)
    # Three kinds of artefact, three bands.
    #   rounded  — a web tile, whose transparent corners are the point of it
    #   opaque   — a platform master, which must cover its whole frame
    #   alpha    — a layer the system composites, whose shape IS its alpha, so most
    #              of the frame is background BY DESIGN. The band still has to be
    #              two-sided: near 100 would mean nothing was drawn at all, which is
    #              exactly the failure a one-sided check would pass.
    expectations = {
        "tile-web.svg": (2.0, 12.0, "rounded"),
        "icon-1024.svg": (2.0, 12.0, "rounded — the web icon"),
        "icon-512.svg": (2.0, 12.0, "rounded"),
        "icon-192.svg": (2.0, 12.0, "rounded"),
        "icon-apple-1024.svg": (0.0, 0.5, "square and fully opaque — Apple, Default"),
        "icon-apple-1088-watch.svg": (0.0, 0.5,
                                      "square and fully opaque — Apple, watchOS"),
        "icon-apple-1024-dark.svg": (0.0, 0.5,
                                     "square and fully opaque — Apple, Dark"),
        "icon-android-background-108.svg": (0.0, 0.5,
                                            "flat and fully opaque — Android background"),
        # Measured on 26 August 2026 and then pinned to +/- 1.0 percentage point:
        # Mono 82.6, both Android layers 91.7. The bands were wide while the figures
        # were unknown; leaving them wide would let the mark shrink or grow by a
        # third without any gate noticing.
        "icon-apple-1024-mono.svg": (81.6, 83.6,
                                     "no ground; the alpha carries the shape — Apple, Mono"),
        "icon-android-foreground-108.svg": (90.7, 92.7,
                                            "no ground; the alpha carries the shape — Android foreground"),
        "icon-android-monochrome-108.svg": (90.7, 92.7,
                                            "no ground; the alpha carries the shape — Android monochrome"),
    }
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as e:
            raise NotEquipped(f"chromium unavailable: {e}") from e
        for name, (lo, hi, why) in expectations.items():
            page = browser.new_page(viewport={"width": 256, "height": 256})
            doc = docs[name].replace(
                "<svg ", '<svg style="width:256px;height:256px;display:block" ', 1)
            page.set_content(f'<body style="margin:0;background:rgb(255,0,255)">{doc}</body>')
            page.wait_for_timeout(250)
            im = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
            W, H = im.size
            showing = sum(1 for x in range(0, W, 2) for y in range(0, H, 2)
                          if im.getpixel((x, y)) == PROBE)
            pct = 100 * showing / ((W // 2) * (H // 2))
            page.close()
            if not (lo <= pct <= hi):
                browser.close()
                raise Fail(
                    f"{name}: {pct:.1f}% of the frame is still background, expected "
                    f"between {lo}% and {hi}% ({why}). A value near 100 usually means "
                    f"the viewBox does not match the grid the artwork is drawn on."
                )
            notes.append(f"{name}: {pct:.1f}% background showing — {why}")

        # The one part of the icon decision that CAN be measured from here.
        #
        # watchOS and visionOS mask to a CIRCLE, and the decision to ship one
        # rounded icon everywhere rests on the rounded file and the square master
        # being the same image once that circle is applied. The guidebook asserted
        # that as "Measured here" while nothing measured it, and offered the
        # placement check's "worst corner 45.00 of 45" as the evidence — a different
        # quantity, and one that equals 45.00 by construction. So the two documents
        # are rendered under the same inscribed circle and differenced.
        #
        # What this can and cannot catch, stated so it is not mistaken for more than
        # it is. The corner material a radius removes always lies outside a circle
        # inscribed in the same square — for side 100 and radius r the nearest
        # removed point sits sqrt(2)(50-r)+r from the centre, which stays above 50
        # for every r up to a full circle — so the radius alone can never make these
        # two differ. What the difference does catch is the two files drifting apart
        # in anything else: the mark placed at a different scale, a different stroke
        # weight, or a different ink or ground in one of them. That is a real risk,
        # because they are two separate strings built from two separate bodies.
        #
        # The rounded-rectangle case is deliberately NOT measured. Apple publishes
        # no corner radius, so there is no mask to composite against, and using our
        # own radius as a stand-in for theirs would be circular.
        clipped = {}
        for name in ("icon-1024.svg", "icon-apple-1024.svg"):
            page = browser.new_page(viewport={"width": 256, "height": 256})
            doc = docs[name].replace(
                "<svg ",
                '<svg style="width:256px;height:256px;display:block;'
                'clip-path:circle(50%)" ', 1)
            page.set_content(f'<body style="margin:0;background:rgb(255,0,255)">{doc}</body>')
            page.wait_for_timeout(250)
            clipped[name] = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
            page.close()
        rounded, square = clipped["icon-1024.svg"], clipped["icon-apple-1024.svg"]
        if rounded.size != square.size:
            browser.close()
            raise Fail(f"the two icons rendered at different sizes, {rounded.size} "
                       f"against {square.size}, so they cannot be differenced")
        total = rounded.size[0] * rounded.size[1]
        left, right = rounded.tobytes(), square.tobytes()
        differing = sum(1 for i in range(0, len(left), 3) if left[i:i + 3] != right[i:i + 3])
        if differing:
            browser.close()
            raise Fail(
                f"under a circle inscribed in the frame the rounded icon and the square "
                f"master differ in {differing} of {total} pixels. The decision to use one "
                f"rounded icon everywhere rests on those two being the same image under a "
                f"circular mask, which is what watchOS and visionOS apply."
            )
        notes.append(
            f"under a circle inscribed in the frame, icon-1024.svg and "
            f"icon-apple-1024.svg are the same image in all {total} pixels — "
            f"the corner rounding lies entirely outside the circle watchOS and visionOS "
            f"mask to, and the artwork inside it has not drifted between the two files"
        )

        # Visual parity between the two platforms, measured rather than hoped for.
        #
        # Following each platform's own geometry means the corner SHAPE now differs
        # between Apple and Android. The thing that must NOT differ is how big the
        # mark reads, and the two canvases make that easy to get wrong: Apple's mark
        # is placed inside 100 units of which all 100 are shown, while Android's is
        # placed inside 108 units of which only the middle 72 are ever displayed.
        # Comparing the two raw scales would say they are wildly different and mean
        # nothing. What matters is the fraction of the VISIBLE area the mark fills.
        ax0, ay0, ax1, ay1 = mark_extent(STROKE_REGULAR)
        aw, ah = (ax1 - ax0), (ay1 - ay0)
        apple_w = 100.0 * aw * place[STROKE_REGULAR][0] / GRID
        apple_h = 100.0 * ah * place[STROKE_REGULAR][0] / GRID
        visible = ANDROID_GRID - 2 * 18.0          # Google's own reserved margin
        android_w = 100.0 * aw * a_scale / visible
        android_h = 100.0 * ah * a_scale / visible
        dw, dh = abs(android_w - apple_w), abs(android_h - apple_h)
        TOLERANCE_PP = 2.0
        if dw > TOLERANCE_PP or dh > TOLERANCE_PP:
            browser.close()
            raise Fail(
                f"the mark reads at a different size on the two platforms: "
                f"{apple_w:.3f}x{apple_h:.3f} per cent of the Apple frame against "
                f"{android_w:.3f}x{android_h:.3f} per cent of Android's visible 72 dp, "
                f"a difference of {dw:.2f} and {dh:.2f} percentage points against a "
                f"tolerance of {TOLERANCE_PP:g}. Following each platform's geometry is "
                f"meant to change the corner shape, not the size of the mark."
            )
        notes.append(
            f"visual parity: the mark fills {apple_w:.3f}x{apple_h:.3f} per cent of the "
            f"Apple frame and {android_w:.3f}x{android_h:.3f} per cent of Android's "
            f"visible 72 dp viewport — a difference of {dw:.2f} and {dh:.2f} percentage "
            f"points. The corner shape differs between the platforms by decision; the "
            f"size does not"
        )
        browser.close()
    return notes


# The contact sheet. Sizes are in the sheet's own user units.
SHEET_CELL_W = 300.0
SHEET_CELL_H = 340.0
SHEET_ART = 200.0
SHEET_PAD = 30.0
SHEET_COLUMNS = 5


def sheet_facts(name: str, doc: str) -> list[str]:
    """What the artwork itself says about itself. Read, never typed.

    Every fact on the contact sheet comes from here, which is the whole point:
    04_mark/proof.png captioned two panels "Apple 1024 · square, unmasked" and
    "watchOS 1088" and drew them with hard corners, while the shipped SVGs have
    carried rx="24" since the owner's 14 August 2026 decision. A caption that is
    measured out of the artwork cannot describe artwork that is not there.
    """
    facts: list[str] = []
    width = re.search(r'\swidth="([0-9.]+)"', doc)
    if width:
        facts.append(f"{float(width.group(1)):g} px delivered")
    radius = re.search(r'\srx="([0-9.]+)"', doc)
    if radius:
        facts.append(f"rounded, radius {float(radius.group(1)):g} of {GRID:g}")
    elif "<rect" in doc:
        facts.append("square, unmasked")
    stroke = re.search(r'stroke-width="([0-9.]+)"', doc)
    if stroke:
        facts.append(f"stroke {float(stroke.group(1)):g}")
    root = doc.split(">", 1)[0]
    facts.append("fixed artwork" if 'style="color:' in root else "recolourable")
    return facts


def proof_sheet(docs: dict[str, str], ink: str, paper: str) -> tuple[str, str]:
    """Assemble one contact sheet from the artwork that was just drawn.

    04_mark/proof.png was a hand-made PNG that no script wrote and no document
    linked, so the marks CI job — which diffs 04_mark/svg and 04_mark/manifest.json
    — could not see that it contradicted the shipped icons. It is replaced by this,
    which is generated from the same strings that become the SVG files, is plain
    deterministic text, and is therefore diffable like everything else here.
    """
    rows = (len(docs) + SHEET_COLUMNS - 1) // SHEET_COLUMNS
    width = SHEET_COLUMNS * SHEET_CELL_W + 2 * SHEET_PAD
    height = rows * SHEET_CELL_H + 2 * SHEET_PAD
    cells: list[str] = []
    for index, (name, doc) in enumerate(docs.items()):
        column, row = index % SHEET_COLUMNS, index // SHEET_COLUMNS
        x = SHEET_PAD + column * SHEET_CELL_W
        y = SHEET_PAD + row * SHEET_CELL_H
        art_x = x + (SHEET_CELL_W - SHEET_ART) / 2
        # The artefact is nested as-is, with only its box overridden, so what the
        # sheet shows is the file itself and not a redrawing of it.
        nested = re.sub(r'^<svg ', "<svg ", doc.strip(), count=1)
        nested = re.sub(r'\swidth="[0-9.]+"', "", nested, count=1)
        nested = re.sub(r'\sheight="[0-9.]+"', "", nested, count=1)
        nested = nested.replace(
            "<svg ",
            f'<svg x="{art_x:g}" y="{y:g}" width="{SHEET_ART:g}" height="{SHEET_ART:g}" '
            f'preserveAspectRatio="xMidYMid meet" ',
            1,
        )
        captions = "".join(
            f'<text x="{x + SHEET_CELL_W / 2:g}" y="{y + SHEET_ART + 30 + line * 22:g}" '
            f'text-anchor="middle" font-size="{13 if line == 0 else 12:g}" '
            f'fill="{ink}" opacity="{1 if line == 0 else 0.7:g}">{text}</text>'
            for line, text in enumerate([name] + sheet_facts(name, doc))
        )
        cells.append(
            f'<g><rect x="{x + 4:g}" y="{y - 8:g}" width="{SHEET_CELL_W - 8:g}" '
            f'height="{SHEET_CELL_H - 8:g}" rx="14" fill="none" stroke="{ink}" '
            f'stroke-width="0.5" opacity="0.25"/>{nested}{captions}</g>'
        )
    body = (
        f'<rect width="{width:g}" height="{height:g}" fill="{paper}"/>'
        f'<g style="color:{ink}" font-family="ui-monospace, monospace">'
        + "".join(cells)
        + "</g>"
    )
    sheet = svg_doc(
        body, width, height, ink,
        "Aninda Studio — contact sheet, generated from the artwork in 04_mark/svg",
    )
    return sheet, (f"contact sheet: {len(docs)} artefacts nested from the same strings "
                   f"written to 04_mark/svg, every caption read out of the artwork")


def tile_radius_pct(prim: dict) -> float:
    """The icon tile's corner radius, in units of the 100-unit grid.

    This was the typed constant 24.0 with a comment saying it came "from the
    system's own radius-hero token". It did not. The token is 24 PIXELS; the icon
    uses 24 units per 100 on a 0 0 100 100 grid delivered at 1024px, which is
    245.8px of rounding. The agreement was between the digit 24 and the digit 24,
    and a citation the build cannot verify is worth less than no citation at all.

    So the numeral is now genuinely read from the token, and what it means is
    stated exactly: this system reuses radius-hero's NUMBER as a percentage, on
    purpose, so the icon's corner belongs to the same family as every other
    rounded corner in the kit. It is a deliberate echo, not a unit conversion.

    The load-bearing half is unchanged and still true: the figure is ours. Apple
    publishes no corner radius, and none is claimed from them.
    """
    try:
        token = prim["dimension"]["radius"]["hero"]["$value"]
    except (KeyError, TypeError) as exc:
        raise Fail(
            f"dimension.radius.hero is missing from the token build ({exc}), so the "
            f"icon's corner radius has nothing to come from. It must not fall back "
            f"to a typed number — that is the state this function replaced."
        )
    if token.get("unit") != "px":
        raise Fail(f"dimension.radius.hero is in {token.get('unit')!r}, not px. The "
                   f"echo this build relies on is of the px numeral.")
    return float(token["value"])


def main() -> int:
    global TILE_RADIUS_PCT
    try:
        light = json.loads((TOKENS / "semantic.light.tokens.json").read_text())
        dark = json.loads((TOKENS / "semantic.dark.tokens.json").read_text())
        prim = json.loads((TOKENS / "primitive.tokens.json").read_text())
    except FileNotFoundError as e:
        print(f"could not run: {e}. Run 07_tokens/build.py first.", file=sys.stderr)
        return 2
    TILE_RADIUS_PCT = tile_radius_pct(prim)

    def resolve(v):
        if isinstance(v, str) and v.startswith("{"):
            node = prim
            for part in v.strip("{}").split("."):
                node = node[part]
            return node["$value"]["hex"]
        return v["hex"]

    # The four primary colours, in the order they are drawn: three arcs of the
    # bowl and then the stem. Read from the palette proof rather than typed, so the
    # mark cannot drift from the brand it is drawn in.
    try:
        palette = json.loads(PALETTE_PROOF.read_text())
    except FileNotFoundError as e:
        print(f"could not run: {e}. Run 05_colour/engine.py first.", file=sys.stderr)
        return 2
    BRAND_ORDER = ("accent", "success", "danger", "ground")
    brand = []
    for fam_key in BRAND_ORDER:
        fam = palette["families"][fam_key]
        brand.append(fam["ramp"][str(fam["anchor_step"])])
    brand_labels = [palette["families"][k]["label"] for k in BRAND_ORDER]

    # The two anchors, read from the direction's own fixed block rather than typed,
    # so the mark cannot disagree with the palette about what pure means.
    PURE_BLACK = palette["fixed"]["ink_light"]
    PURE_WHITE = palette["fixed"]["ink_dark"]

    ink = resolve(light["color"]["ink"]["default"]["$value"])
    paper = light["color"]["surface"]["bright"]["$value"]["hex"]
    # The Dark appearance is drawn from the dark theme's own tokens rather than
    # from a darkened copy of the light ones, so it cannot drift away from the
    # rest of the system.
    dark_ground = resolve(dark["color"]["surface"]["lowest"]["$value"])
    dark_mark = resolve(dark["color"]["ink"]["default"]["$value"])

    notes: list[str] = []
    place: dict[float, tuple[float, float, float]] = {}
    try:
        notes += shaping_gates()
        for s in (STROKE_REGULAR, STROKE_HEAVY):
            scale, tx, ty, note = icon_placement(s)
            place[s] = (scale, tx, ty)
            notes.append(note)
        a_scale, a_tx, a_ty, a_note = icon_placement(
            STROKE_REGULAR, grid=ANDROID_GRID, safe=ANDROID_SAFE)
        notes.append(a_note)
    except NotEquipped as e:
        print(f"could not run: {e}", file=sys.stderr)
        return 2
    except Fail as e:
        print(f"FAILED — nothing written:\n  {e}", file=sys.stderr)
        return 1

    # Every artefact is buffered in memory and nothing touches the disk until the
    # last gate has passed. The earlier version wrote each file as it was drawn, so
    # a failure in check_apple_master or render_check left five rewritten SVGs on
    # disk beside a manifest that still described the old ones — `git status` showed
    # five modified files and the script had said "nothing further written". The
    # manifest is what every downstream reader treats as the description of the
    # SVGs next to it, so the two disagreeing is the worst state this can end in.
    docs: dict[str, str] = {}
    written: list[tuple[str, str]] = []

    def write(name: str, content: str) -> None:
        docs[name] = content
        written.append((name, f"{len(content)} bytes"))

    # --- the mark, two weights, one geometry -------------------------------
    # These stay RECOLOURABLE and single-colour. They are the monochromes: set
    # `color` to pure black or pure white and the mark follows. Apple's appearance
    # variants and every reversed use are served from here.
    for label, stroke in (("regular", STROKE_REGULAR), ("heavy", STROKE_HEAVY)):
        write(f"mark-{label}.svg",
              svg_doc(mark_paths(stroke), GRID, GRID, ink,
                      f"Aninda Studio — the mark, {label} weight",
                      recolourable=True))

    # The four-colour mark. Three arcs of the bowl and the stem, one primary each,
    # in the order accent, success, danger, ground — Natural Blue, Green, Red, Gray.
    # It carries fixed colours by definition, so it is not recolourable and the
    # regression guard that refuses a root colour on the recolourable files does not
    # apply to it.
    write("mark-colour.svg",
          svg_doc(mark_paths(STROKE_REGULAR, brand), GRID, GRID, brand[0],
                  "Aninda Studio — the mark in the four primary colours"))

    # --- wordmarks, from real shaped outlines ------------------------------
    for name, text, font, var in (
        ("wordmark-latin", WORD_LATIN, LATIN_FONT, LATIN_WORDMARK_AXES),
        ("wordmark-bangla", WORD_BANGLA, BANGLA_FONT, {"wght": 500}),
    ):
        try:
            body, adv, _ = shape_to_path(text, font, 100.0, var)
            colour_body, _, _ = shape_to_path(text, font, 100.0, var, brand)
        except (Fail, NotEquipped) as e:
            print(f"FAILED — nothing written:\n  {e}", file=sys.stderr)
            return 1
        write(f"{name}.svg",
              svg_doc(f'<g fill="currentColor">{body}</g>', adv, 140.0, ink,
                      f"Aninda Studio — wordmark, {text}",
                      view=f"0 -100 {adv:g} 140", recolourable=True))
        # The four-colour wordmark. Each letter takes the next primary in turn, the
        # way Google's own wordmark carries its colours across letters rather than
        # inside one glyph. It is NOT recolourable: the colours are the point.
        write(f"{name}-colour.svg",
              svg_doc(colour_body, adv, 140.0, brand[0],
                      f"Aninda Studio — wordmark in the four primary colours, {text}",
                      view=f"0 -100 {adv:g} 140"))

    # --- the web tile: rounded, because a browser will not round it for you --
    s, tx, ty = place[STROKE_HEAVY]
    ts, ttx, tty = place[STROKE_HEAVY]
    tile_body = (
        f'<rect width="{GRID:g}" height="{GRID:g}" rx="{TILE_RADIUS_PCT:g}" '
        f'ry="{TILE_RADIUS_PCT:g}" fill="{PURE_WHITE}"/>'
        f'<g transform="translate({ttx:.4f},{tty:.4f}) '
        f'scale({ts:.6f})">{mark_paths(STROKE_HEAVY, brand)}</g>'
    )
    write("tile-web.svg", svg_doc(tile_body, GRID, GRID, paper,
                                  "Aninda Studio — web tile"))

    # --- the delivery icons -------------------------------------------------
    # OWNER'S DECISION, 26 August 2026, REVERSING the decision of 14 August 2026.
    #
    # The earlier rule was one rounded icon on every surface, Apple included. It is
    # reversed because this kit now ships to two developer accounts, and BOTH
    # platforms ask for unmasked artwork and derive something from the edges of what
    # they are given: Apple its Liquid Glass specular highlights, Google its own
    # corner mask and drop shadow. Google publishes a figure where Apple does not —
    # a radius of 30% of the icon size, applied by Play. Supplying pre-rounded
    # artwork means both of those follow the wrong geometry, and the cost of that
    # could not be measured outside their renderers. Supplying what each asks for
    # removes the unknown rather than accepting it.
    #
    # The web keeps the rounded tile, because a browser will not round a favicon.
    #
    # The superseded decision and its whole trade-off text are preserved in the
    # manifest under icon_policy.superseded, because a reversed decision that
    # vanishes teaches nobody anything.
    s, tx, ty = place[STROKE_REGULAR]

    def square(ground: str, mark: str) -> str:
        """A monochrome square. One colour on one ground."""
        return (f'<rect width="{GRID:g}" height="{GRID:g}" fill="{ground}"/>'
                f'<g style="color:{mark}" transform="translate({tx:.4f},{ty:.4f}) '
                f'scale({s:.6f})">{mark_paths(STROKE_REGULAR)}</g>')

    def square_colour(ground: str) -> str:
        """The four-colour mark on a ground.

        The ground is pure white and not a choice of taste. Measured on
        26 August 2026 against the 3:1 non-text floor of WCAG 1.4.11: on pure white
        every one of the four clears it — Natural Blue 9.47, Natural Green 7.80,
        Natural Red 5.56, Natural Gray 3.83. On pure black two of them do not —
        Blue falls to 2.12 and Green to 2.58. So the coloured mark can sit on white
        and cannot sit on black, and the monochromes exist for the dark side.
        """
        return (f'<rect width="{GRID:g}" height="{GRID:g}" fill="{ground}"/>'
                f'<g transform="translate({tx:.4f},{ty:.4f}) '
                f'scale({s:.6f})">{mark_paths(STROKE_REGULAR, brand)}</g>')

    rounded_body = (
        f'<rect width="{GRID:g}" height="{GRID:g}" rx="{TILE_RADIUS_PCT:g}" '
        f'ry="{TILE_RADIUS_PCT:g}" fill="{PURE_WHITE}"/>'
        f'<g transform="translate({tx:.4f},{ty:.4f}) '
        f'scale({s:.6f})">{mark_paths(STROKE_REGULAR, brand)}</g>'
    )
    # The web set. The 1088 that used to sit here was for watchOS and has moved to
    # the Apple set below, square and unmasked, so nothing rounded is delivered to
    # a platform that masks for itself.
    for name, size, what in (
        ("icon-1024", 1024, "the icon, 1024px — rounded, for the web"),
        ("icon-512", 512, "the icon, 512px — avatars and PWA"),
        ("icon-192", 192, "the icon, 192px — PWA"),
    ):
        # The artwork is drawn on the 100-unit grid, so the viewBox stays
        # 0 0 100 100 while width and height carry the delivery size. Setting the
        # viewBox to the delivery size instead put a 100-unit square inside a
        # 1024-unit frame and produced a tiny mark in the corner of a white field —
        # which every structural check passed, because the file was valid SVG.
        write(f"{name}.svg",
              svg_doc(rounded_body, size, size, paper,
                      f"Aninda Studio — {what}", view=f"0 0 {GRID:g} {GRID:g}"))

    # --- Apple: square, unmasked, three authored appearances ----------------
    # Apple's own material gives three different counts and all three are right in
    # their own context: the specification table lists six appearances, the prose
    # says four, and Icon Composer has you author three. Three are authored here;
    # Apple's renderer generates clear light, clear dark, tinted light and tinted
    # dark from them, and this build cannot show what those four look like.
    # Default and watchOS carry the four colours on pure white, the way Google's
    # own mark does. Dark is a MONOCHROME — pure white on pure black — because the
    # coloured mark measurably cannot sit on black: Natural Blue falls to 2.12 and
    # Natural Green to 2.58 against a 3:1 floor. Apple's own appearance variants are
    # the right place for a monochrome, so the two conventions meet here rather than
    # fighting.
    apple = [
        ("icon-apple-1024.svg", 1024, square_colour(PURE_WHITE), brand[0],
         "square unmasked master, Default appearance — the four primary colours on "
         "pure white — iOS, iPadOS, macOS, visionOS"),
        ("icon-apple-1088-watch.svg", 1088, square_colour(PURE_WHITE), brand[0],
         "square unmasked master, 1088px for watchOS — the four primary colours on "
         "pure white"),
        ("icon-apple-1024-dark.svg", 1024, square(PURE_BLACK, PURE_WHITE), PURE_WHITE,
         "square unmasked master, Dark appearance — monochrome, pure white on pure "
         "black"),
    ]
    for name, size, body, colour, what in apple:
        doc = svg_doc(body, size, size, colour, f"Aninda Studio — {what}",
                      view=f"0 0 {GRID:g} {GRID:g}")
        try:
            check_apple_master(doc)
        except Fail as e:
            print(f"FAILED — nothing written:\n  {e}", file=sys.stderr)
            return 1
        write(name, doc)

    # The Mono appearance carries no ground: Apple composites it and derives the
    # clear and tinted appearances from it, so its shape is its alpha.
    mono_body = (f'<g style="color:{PURE_WHITE}" '
                 f'transform="translate({tx:.4f},{ty:.4f}) '
                 f'scale({s:.6f})">{mark_paths(STROKE_REGULAR)}</g>')
    mono = svg_doc(mono_body, 1024, 1024, paper,
                   "Aninda Studio — Mono appearance, no ground; the alpha carries "
                   "the shape",
                   view=f"0 0 {GRID:g} {GRID:g}")
    try:
        check_apple_master(mono)
        check_transparent_layer(mono, "icon-apple-1024-mono.svg")
    except Fail as e:
        print(f"FAILED — nothing written:\n  {e}", file=sys.stderr)
        return 1
    write("icon-apple-1024-mono.svg", mono)

    # --- Android: three layers on the 108-unit canvas -----------------------
    # The background is flat and full-bleed; the foreground and the monochrome
    # silhouette carry their shape in the alpha, because the launcher composites
    # them over the background and the system tints the monochrome one.
    write("icon-android-background-108.svg",
          svg_doc(f'<rect width="{ANDROID_GRID:g}" height="{ANDROID_GRID:g}" '
                  f'fill="{PURE_WHITE}"/>',
                  ANDROID_GRID, ANDROID_GRID, PURE_WHITE,
                  "Aninda Studio — Android adaptive icon, background layer, "
                  "pure white",
                  view=f"0 0 {ANDROID_GRID:g} {ANDROID_GRID:g}"))

    android_mark = (f'<g transform="translate({a_tx:.4f},{a_ty:.4f}) '
                    f'scale({a_scale:.6f})">'
                    f'{mark_paths(STROKE_REGULAR, brand)}</g>')
    # The monochrome layer is a SILHOUETTE the system tints, so it is one colour
    # and never four. Pure black: the launcher supplies the tint and reads the alpha.
    android_mono = (f'<g style="color:{PURE_BLACK}" '
                    f'transform="translate({a_tx:.4f},{a_ty:.4f}) '
                    f'scale({a_scale:.6f})">{mark_paths(STROKE_REGULAR)}</g>')
    for name, body, what in (
        ("icon-android-foreground-108.svg", android_mark,
         "Android adaptive icon, foreground layer — the four primary colours"),
        ("icon-android-monochrome-108.svg", android_mono,
         "Android adaptive icon, monochrome layer — one colour, the system tints it"),
    ):
        doc = svg_doc(body, ANDROID_GRID, ANDROID_GRID, brand[0],
                      f"Aninda Studio — {what}",
                      view=f"0 0 {ANDROID_GRID:g} {ANDROID_GRID:g}")
        try:
            check_transparent_layer(doc, name)
        except Fail as e:
            print(f"FAILED — nothing written:\n  {e}", file=sys.stderr)
            return 1
        write(name, doc)

    # --- render the icons and MEASURE them ---------------------------------
    # Every check above reads the source. None of them can see what a renderer
    # actually produces, and that gap hid a real bug: the Apple master was written
    # with a 1024-unit viewBox around 100-unit artwork, so it rendered as a tiny
    # mark in the corner of a white field. The file was valid SVG, the geometry
    # checks passed, and the artefact was useless.
    # The render gate is the one that caught a bug no source read could see: the
    # Apple master was written with a 1024-unit viewBox around 100-unit artwork.
    # It also hosts the recolourable-root regression guard. A missing Chromium used
    # to become an `ok    NOT CHECKED — ...` line and exit 0, so forgetting to
    # export PLAYWRIGHT_BROWSERS_PATH silently skipped both and reported success.
    # The docstring has always documented 2 as "could not run"; it now returns it.
    try:
        notes += render_check(docs, place, a_scale)
    except NotEquipped as e:
        print(f"could not run: {e}\n"
              f"  The render gate is not optional: it is the only check that sees what a\n"
              f"  renderer produces. Nothing was written. Did you export\n"
              f"  PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers ?", file=sys.stderr)
        return 2
    except Fail as e:
        print(f"FAILED — nothing written:\n  {e}", file=sys.stderr)
        return 1

    sheet, sheet_note = proof_sheet(docs, ink, paper)
    notes.append(sheet_note)

    # Read the stroke out of each artefact that was written, so the manifest
    # cannot claim a weight the file does not carry.
    stroke_by_file: dict[str, float] = {}
    for _name, _text in docs.items():
        _widths = {float(w) for w in re.findall(r'stroke-width="([0-9.]+)"', _text)}
        if len(_widths) > 1:
            print(f"FAILED — nothing written:\n  {_name} mixes stroke widths "
                  f"{sorted(_widths)}. One artefact carries one weight.",
                  file=sys.stderr)
            return 1
        if _widths:
            stroke_by_file[_name] = _widths.pop()

    manifest = {
        "generated_by": "04_mark/build.py",
        "warning": "Generated. Do not hand-edit — change the script and re-run.",
        "grid": GRID,
        "geometry": {"circle": CIRCLE, "stem_x": STEM_X, "stem_top": STEM_TOP,
                     "stem_bottom": STEM_BOTTOM},
        # switch_px and stroke_by_file are machine-readable on purpose. The rule
        # used to exist here only as the prose sentence below, so every consumer
        # retyped the switch point or ignored it — and 10_assets/build.py rendered
        # every favicon, including the 16 px one and the 16 px plane of
        # favicon.ico, from icon-192.svg at the regular weight, which is the one
        # place in the whole system that the heavy weight exists for. A consumer
        # can now ask this file which artwork carries which stroke instead of
        # hard-coding a filename.
        "strokes": {
            "regular": STROKE_REGULAR,
            "heavy": STROKE_HEAVY,
            "switch_px": STROKE_SWITCH_PX,
            "rule": (f"stroke {STROKE_REGULAR:g} at {STROKE_SWITCH_PX} px and "
                     f"above; stroke {STROKE_HEAVY:g} below"),
            "stroke_by_file": stroke_by_file,
        },
        "shaping_proof": {
            "gate": ("Three probe words are shaped through HarfBuzz at the "
                     "wordmark's own axis settings. Each must collapse to fewer "
                     "glyphs than it has code points, and each must produce a glyph "
                     "that no code point maps to — the second condition being the "
                     "one that distinguishes a substitution from a lookup. A "
                     "negative control then requires the naive cmap path to differ "
                     "from the shaped result."),
            "probes": list(LIGATURE_PROBES),
            "axes": dict(LATIN_WORDMARK_AXES),
            "why_not_fi": ("'fi' collapses too, and proves nothing: Literata's cmap "
                           "maps U+FB01 straight to that glyph, so a shaper doing "
                           "nothing but code-point lookup could produce it. U+FB03 "
                           "and U+FB04 are absent from that cmap, which is what "
                           "makes f_f_i and f_f_l evidence."),
            "why_not_the_wordmark": ("'aninda studio' shapes to 13 glyphs from 13 "
                                     "code points and the naive path returns the "
                                     "same 13, so the artwork passes either way. "
                                     "The proof has to use something that does not."),
            "superseded": [{
                "decision": ("The shaping proof was Bangla. Two gates ran the Bangla "
                             "wordmark through HarfBuzz — one requiring conjuncts to "
                             "form, one a negative control — because Bangla reorders "
                             "pre-base vowels and joins consonants, so glyphs pulled "
                             "out by code point produce nonsense that still looks "
                             "like Bangla to someone who cannot read it."),
                "taken": "14 August 2026",
                "superseded": "27 August 2026",
                "why": "This kit no longer ships Bangla.",
                "what_is_preserved": ("The mechanism: that HarfBuzz is present, that "
                                      "the font's GSUB table is applied, and that the "
                                      "naive path is measurably different."),
                "what_is_lost": ("The stakes. A Latin ligature is cosmetic, so a "
                                 "shaper failing here produces ugly type rather than "
                                 "wrong words. The Bangla gate caught a failure that "
                                 "changed meaning. This is a weaker proof of a "
                                 "smaller consequence, and it is recorded rather "
                                 "than hidden."),
            }],
        },
        "clear_space": "half the mark's own height on all four sides",
        "safe_field": SAFE,
        "tile_radius_percent": TILE_RADIUS_PCT,
        "tile_radius_grid_units_per_100": TILE_RADIUS_PCT,
        "tile_radius_px_at_1024": round(TILE_RADIUS_PCT / 100.0 * 1024.0, 1),
        "tile_radius_source": ("read at build time from dimension.radius.hero. That "
                               "token is 24 px; this is 24 units per 100 on the "
                               "icon grid, which is 245.8 px of rounding on the "
                               "1024 px icon. The numeral is reused deliberately, "
                               "so the icon corner belongs to the same family as "
                               "every other rounded corner in the kit — it is an "
                               "echo, not a unit conversion. Apple publishes no "
                               "corner radius; this number is ours and is not "
                               "claimed to be theirs."),
        "icon_policy": {
            "decision": (
                "Each platform's own icon geometry is followed. Apple and Google "
                "receive square, unmasked artwork and apply their own masks. The web "
                "keeps the rounded tile, because a browser will not round a favicon "
                "for you. Owner's decision, 26 August 2026."),
            "reason": (
                "This kit now ships to two developer accounts. Both platforms ask for "
                "unmasked artwork and both derive something from the edges of what "
                "they are given: Apple its Liquid Glass specular highlights, Google "
                "its own corner mask and drop shadow. Google publishes a figure where "
                "Apple does not — a radius of 30 per cent of the icon size, applied by "
                "Play. Supplying pre-rounded artwork means both of those follow the "
                "wrong geometry, and the cost of that could not be measured outside "
                "their renderers. Supplying what each asks for removes the unknown "
                "instead of accepting it."),
            "accepted_consequence": (
                "The corner shape now differs between surfaces: rounded on the web, "
                "and whatever each platform draws on Apple and Android. The SIZE does "
                "not differ with it, and that is measured rather than hoped for — see "
                "the visual-parity line in 'checks'."),
            "surfaces": {
                "web": ["tile-web.svg", "icon-1024.svg", "icon-512.svg",
                        "icon-192.svg"],
                "apple": ["icon-apple-1024.svg", "icon-apple-1088-watch.svg",
                          "icon-apple-1024-dark.svg", "icon-apple-1024-mono.svg"],
                "android": ["icon-android-background-108.svg",
                            "icon-android-foreground-108.svg",
                            "icon-android-monochrome-108.svg"],
            },
            "apple_appearances": {
                "authored_here": ["default", "dark", "mono"],
                "derived_by_apple": ["clear light", "clear dark", "tinted light",
                                     "tinted dark"],
                "note": (
                    "Apple's own material is inconsistent about the count, and all "
                    "three counts are right in their own context: the specification "
                    "table lists six appearances, the prose says four, and Icon "
                    "Composer has you author three. Three are authored here. The other "
                    "four are generated by Apple's renderer from them, and this build "
                    "cannot show what they look like."),
            },
            "android_geometry": {
                "grid": ANDROID_GRID,
                "safe_zone": ANDROID_SAFE,
                "reserved_margin_each_side": (ANDROID_GRID - ANDROID_SAFE - 24.0) / 2 + 12.0,
                "source": ("developer.android.com/develop/ui/views/launch/"
                           "icon_design_adaptive, page updated 13 August 2026, read "
                           "26 August 2026. Both figures are Google's: every layer is "
                           "108x108 dp, the outer 18 dp per side is reserved for "
                           "masking and motion effects, and the 66x66 dp centre is the "
                           "zone no launcher mask may clip."),
            },
            "superseded": [{
                "decision": ("One rounded icon is used on every surface, Apple "
                             "included."),
                "taken": "14 August 2026",
                "reversed": "26 August 2026",
                "why_reversed": ("This kit now ships to both stores, and both ask for "
                                 "unmasked artwork."),
                "trade_off_as_recorded_then": (
                    "Apple's current guidance asks for square, unmasked artwork: the "
                    "system applies the mask and derives Liquid Glass specular "
                    "highlights from the layer edges, so a pre-rounded edge sits "
                    "inside the mask and the highlight follows the wrong geometry. "
                    "Apple's own wording is that pre-masked artwork 'negatively "
                    "impacts specular highlight effects' and makes edges 'look "
                    "jagged'. Measured here: under the circle watchOS and visionOS "
                    "mask to, the rounded icon and the square master are the same "
                    "image in every pixel. Judged rather than measured: in a static "
                    "render under Apple's rounded-rectangle mask the difference looks "
                    "slight. That one is not a measurement, because Apple publishes no "
                    "corner radius, so there is no mask to composite against without "
                    "substituting our own radius for theirs. The dynamic cost — the "
                    "moving specular highlight — could not be measured outside Apple's "
                    "own renderer and is not known."),
                "what_of_it_still_holds": (
                    "The measured half still holds: under a circular mask the rounded "
                    "icon and the square master were the same image in every pixel. "
                    "What changed is the judged half and the unknown half — and the "
                    "unknown one is now removed rather than carried, because each "
                    "platform is given the geometry it asks for."),
            }],
            "verified_against": ("Apple Human Interface Guidelines and the Google Play "
                                 "icon design specifications, checked 26 August 2026"),
        },
        "files": [n for n, _ in written],
        "contact_sheet": ("proof.svg — generated from the same strings written to "
                          "04_mark/svg, with every caption read out of the artwork"),
        "checks": notes,
    }

    # Everything above only computed and checked. This is the only place that
    # touches the disk, and it is reached only when every gate has passed.
    OUT.mkdir(parents=True, exist_ok=True)
    # Remove anything this build no longer writes. Until 26 August 2026 this script
    # only ever added files, so retiring one left it on disk: the rounded
    # icon-1088-watch.svg and icon-appstore-square-1024.svg would both have survived
    # every gate here and gone on flowing into 10_assets, the guidebook's figure
    # list and two plugin bundles, all of which glob this directory. A generator
    # that cannot remove is a generator whose output is only ever a superset of
    # what it means.
    removed: list[str] = []
    for stale in sorted(OUT.glob("*.svg")):
        if stale.name not in docs:
            stale.unlink()
            removed.append(stale.name)
    for name, content in docs.items():
        (OUT / name).write_text(content)
    (HERE / "proof.svg").write_text(sheet)
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    for n in notes:
        print(f"  ok    {n}")
    print()
    for name in removed:
        print(f"  removed {name:<26} no longer written by this build")
    for name, size in written:
        print(f"  wrote {name:<28} {size}")
    print(f"  wrote {'proof.svg':<28} {len(sheet)} bytes")
    print(f"  wrote manifest.json")
    print("\nThis script CANNOT check: whether the mark is any good, whether the "
          "Bangla wordmark reads correctly to a Bangla reader, or how the icon looks "
          "once Apple's own materials are composited over it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
