#!/usr/bin/env python3
"""Aninda Studio — make one asset, and refuse the ones that break a rule.

A document that warns is read once and forgotten. A script that refuses teaches
the rule every time it is run, so this one refuses. Every refusal names the rule,
the measured number, the threshold it missed, and the nearest thing that would
have been allowed.

Run `python asset.py list` to see what can be made.

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"
TOKENS = ASSETS / "tokens"
MARKS = ASSETS / "marks"

THEMES = ("light", "dark", "hc-light", "hc-dark")

def mark_floor_px() -> float:
    """The mark's size floor, READ from the manifest rather than typed here.

    It was `mark_floor_px() = 16`, a constant in this consumer with its derivation in
    a comment — so the number deciding whether an asset may be made lived beside
    the code that refuses, and not with the artwork it describes. That was gap
    G-REC-3, and the fix it asked for was "computed rather than typed".

    04_mark/build.py now computes it from three figures already in that manifest:
    the heavy stroke, the grid, and the circle's radius. What closes first at small
    sizes is the circle's COUNTER — the enclosed space inside the bowl — and the
    build reports it at 6.56 px at the floor. The comment that used to sit here
    said "about 5.6 px"; nobody had recomputed it, which is the argument for not
    keeping arithmetic in prose.
    """
    path = MARKS / "manifest.json"
    if not path.exists():
        raise NotEquipped(f"{path} is missing. This skill needs its assets/marks folder.")
    return float(json.loads(path.read_text("utf-8"))["minimum_px"]["value"])

# The stroke rule is READ from assets/marks/manifest.json, not typed here. See
# stroke_rule() below. It used to be the constant `STROKE_SWITCH_PX = 24` with a
# comment saying where it came from, and guard_mark_size applied it to the
# standalone mark only — so `asset.py mark --size 16 --weight regular` refused
# with exit 2 while `asset.py icon --size 16` wrote a file carrying that exact
# forbidden stroke, one command later.

# The em box a wordmark must reach before its Bangla conjuncts stop being
# legible. It is the system's own 12 px Bangla floor, applied to an outline.
WORDMARK_EM_FLOOR_PX = 12

# The one size Apple asks for, and the one this file exists to satisfy.
APPSTORE_SIZE = 1024

# Each platform's masters, and the only sizes each is delivered at. Owner's
# decision of 26 August 2026: every platform gets the geometry it asks for, so
# Apple and Android receive square, unmasked artwork and the web keeps the rounded
# tile. The sizes are the platforms' own figures, not this kit's.
PLATFORM_MASTERS = {
    "apple": {
        1024: {"default": "icon-apple-1024.svg",
               "dark": "icon-apple-1024-dark.svg",
               "mono": "icon-apple-1024-mono.svg"},
        1088: {"default": "icon-apple-1088-watch.svg"},
    },
}
# Android delivers the same 108 dp layer at five densities: px = dp x dpi / 160.
# Google publishes the formula and not the table, so this is derived and says so.
ANDROID_DENSITIES = {"mdpi": 108, "hdpi": 162, "xhdpi": 216,
                     "xxhdpi": 324, "xxxhdpi": 432}


def guard_unmasked(svg: str, name: str) -> None:
    """Read the artwork, rather than trusting the flag that asked for it.

    The refusal below is keyed on what was requested. That is one rename or one
    re-glob away from handing out a rounded file while still reporting it as the
    square master, so the bytes are checked too.
    """
    low = svg.lower()
    for banned in ("rx=", "ry=", "clip-path", "filter"):
        if banned in low:
            raise Refused(
                f"{name} is not unmasked: it carries '{banned}'.",
                "Apple derives its Liquid Glass specular highlights from the layer "
                "edges, and Google Play applies a corner mask of 30 per cent of the "
                "icon size and adds the drop shadow itself. Baked-in rounding sends "
                "both of those after the wrong geometry.",
                "Re-run 04_mark/build.py, which writes these masters square, and "
                "sync the skill with check_plugin.py --sync.",
            )

# Which roles the mark itself may be drawn in. The marks card in the system
# shows the regular weight in the ink and the heavy weight in the accent, and a
# knock-out onto a bright surface is how it sits on a dark ground. Everything
# else is a recolour.
MARK_COLOUR_ROLES = (
    "ink.default",
    "ink.muted",
    "accent.default",
    "surface.bright",
    "surface.lowest",
)

# How each role is judged. WCAG 1.4.3 Contrast (Minimum) covers text; 1.4.11
# Non-text Contrast covers borders, focus rings and meaningful graphics.
TEXT_ROLES = (
    "ink.default",
    "ink.muted",
    "accent.default",
    "status.success",
    "status.warning",
    "status.danger",
    "status.info",
)
NON_TEXT_ROLES = ("line.default", "accent.edge", "focus.ring")


class Refused(Exception):
    """An impermissible combination. Not an error in the script — an answer."""

    def __init__(self, rule: str, measured: str, remedy: str) -> None:
        super().__init__(rule)
        self.rule = rule
        self.measured = measured
        self.remedy = remedy


class NotEquipped(Exception):
    """Something the script needs is missing. Different from a refusal."""


# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------


def _flatten(node, prefix: str, out: dict) -> dict:
    for key, value in node.items():
        if key.startswith("$"):
            continue
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict) and "$value" in value:
            out[path] = value["$value"]
        elif isinstance(value, dict):
            _flatten(value, path, out)
    return out


def load_tokens() -> tuple[dict, dict]:
    """Return (primitives, {theme: {role: value}}). Aliases stay unresolved."""
    primitive_path = TOKENS / "primitive.tokens.json"
    if not primitive_path.exists():
        raise NotEquipped(
            f"{primitive_path} is missing. This skill needs its assets/tokens folder."
        )
    primitives = _flatten(json.loads(primitive_path.read_text("utf-8")), "", {})
    semantic: dict[str, dict] = {}
    for theme in THEMES:
        path = TOKENS / f"semantic.{theme}.tokens.json"
        if not path.exists():
            raise NotEquipped(f"{path} is missing. All four themes are needed.")
        semantic[theme] = _flatten(json.loads(path.read_text("utf-8")), "", {})
    return primitives, semantic


def theme_targets(theme: str) -> tuple[float, float]:
    """The text and non-text ratios this theme was measured against."""
    path = TOKENS / f"semantic.{theme}.tokens.json"
    extensions = json.loads(path.read_text("utf-8")).get("$extensions", {})
    studio = extensions.get("studio.aninda", {})
    return float(studio.get("textTarget", 4.5)), float(studio.get("nonTextTarget", 3.0))


def hex_of(value, primitives: dict) -> str:
    if isinstance(value, str):
        target = value.strip().strip("{}")
        if target not in primitives:
            raise NotEquipped(f"the alias {{{target}}} points at a token that is missing")
        return hex_of(primitives[target], primitives)
    return value["hex"]


def roles(semantic: dict) -> list[str]:
    """Every role name in the semantic set, without its `color.` prefix.

    Read from the token document, so it is however many there are. The docstring
    said "seventeen" and the count changed the moment a role was added.
    """
    return [key[len("color.") :] for key in semantic["light"] if key.startswith("color.")]


def resolve(role: str, theme: str, primitives: dict, semantic: dict) -> str:
    known = roles(semantic)
    if role not in known:
        raise Refused(
            f"There is no colour role called {role!r}.",
            f"The system has exactly {len(known)} roles.",
            "Use one of: " + ", ".join(known),
        )
    if theme not in THEMES:
        raise Refused(
            f"There is no theme called {theme!r}.",
            "The system has exactly four themes.",
            "Use one of: " + ", ".join(THEMES),
        )
    return hex_of(semantic[theme][f"color.{role}"], primitives)


# ---------------------------------------------------------------------------
# Contrast
# ---------------------------------------------------------------------------


def to_rgb(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)


def luminance(rgb) -> float:
    def channel(v: int) -> float:
        c = v / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2])


def ratio(a: str, b: str) -> float:
    la, lb = luminance(to_rgb(a)), luminance(to_rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def surface_roles(semantic: dict) -> list[str]:
    return [r for r in roles(semantic) if r.startswith("surface.")]


def criterion_for(role: str) -> tuple[str, str]:
    """Return (kind, the WCAG criterion this role is judged by, if any)."""
    if role in TEXT_ROLES:
        return "text", "WCAG 2.2 success criterion 1.4.3 Contrast (Minimum)"
    if role in NON_TEXT_ROLES:
        return "non-text", "WCAG 2.2 success criterion 1.4.11 Non-text Contrast"
    return "surface", ""


def check_ground(
    role: str,
    ground: str,
    theme: str,
    primitives: dict,
    semantic: dict,
    house_rule: bool = False,
) -> dict:
    """Measure a foreground against a ground, and refuse if it falls short."""
    if not ground.startswith("surface."):
        raise Refused(
            f"{ground!r} is not a ground.",
            "Only a surface role can be a ground. "
            "Every text pairing in this system was measured against surfaces and nothing else.",
            "Use one of: " + ", ".join(surface_roles(semantic)),
        )
    fg = resolve(role, theme, primitives, semantic)
    bg = resolve(ground, theme, primitives, semantic)
    text_target, non_text_target = theme_targets(theme)
    kind, criterion = criterion_for(role)
    # A mark is a graphic, so it is held to this theme's graphic figure whatever
    # role it happens to be drawn in. WCAG exempts it altogether; the studio
    # does not, and holding it to the graphic number is the studio's choice.
    target = non_text_target if house_rule else (text_target if kind == "text" else non_text_target)
    measured = ratio(fg, bg)

    if measured + 1e-9 < target:
        passing = []
        for candidate in surface_roles(semantic):
            candidate_hex = resolve(candidate, theme, primitives, semantic)
            if ratio(fg, candidate_hex) + 1e-9 >= target:
                passing.append(f"{candidate} ({ratio(fg, candidate_hex):.2f}:1)")
        remedy = (
            "Grounds this role does pass on, in the " + theme + " theme: " + ", ".join(passing)
            if passing
            else (
                f"In the {theme} theme this role passes on no surface at all. "
                "That is a gap in the system, not something to work around."
            )
        )
        raise Refused(
            f"{role} on {ground} is not a measured pairing in the {theme} theme.",
            f"Measured {measured:.2f}:1 against a target of {target:.1f}:1. "
            + (
                "This is the studio's own legibility rule, not a WCAG requirement: "
                "WCAG 1.4.11 exempts a logotype from any contrast requirement."
                if house_rule
                else criterion + "."
            ),
            remedy,
        )

    return {
        "foreground": f"{role} {fg}",
        "ground": f"{ground} {bg}",
        "theme": theme,
        "measured": round(measured, 2),
        "target": target,
        "judged_by": (
            "the studio's own legibility rule, held to this theme's graphic figure. "
            "WCAG 1.4.11 exempts a logotype from any contrast requirement, so this is not a "
            "conformance claim."
            if house_rule
            else criterion
        ),
    }


# ---------------------------------------------------------------------------
# SVG
# ---------------------------------------------------------------------------


def stroke_rule() -> dict:
    """The mark's stroke rule, read from the manifest this skill bundles.

    The manifest carries `switch_px`, the two stroke widths, and `stroke_by_file`
    measured off each artefact by 04_mark/build.py. Reading it means this script
    cannot disagree with the artwork about which file carries which weight.
    """
    path = MARKS / "manifest.json"
    if not path.exists():
        raise NotEquipped(f"{path} is missing. This skill needs its assets/marks folder.")
    strokes = json.loads(path.read_text("utf-8"))["strokes"]
    for key in ("regular", "heavy", "switch_px", "stroke_by_file"):
        if key not in strokes:
            raise NotEquipped(
                f"assets/marks/manifest.json has no strokes.{key}, so the stroke "
                f"rule cannot be read. Re-run 04_mark/build.py and rebuild this "
                f"skill's assets."
            )
    return strokes


def rounded_source(size: int, default: str) -> tuple[str, dict]:
    """Which rounded artefact a request at this size must use, and the rule.

    Below the switch the answer is the heavy artwork; at or above it, `default`.
    A caller that asks for a size the rule cannot serve gets a Refused, not a
    quietly-wrong file.
    """
    strokes = stroke_rule()
    if size >= strokes["switch_px"]:
        return default, strokes
    heavy = sorted(name for name, width in strokes["stroke_by_file"].items()
                   if width == strokes["heavy"] and name.startswith(("tile", "icon")))
    if not heavy:
        raise Refused(
            f"No rounded artwork carries the heavy stroke, so nothing can be made "
            f"below {strokes['switch_px']} px.",
            f"Asked for {size} px. The rule is \"{strokes['rule']}\", and "
            f"assets/marks/manifest.json records no rounded file at stroke "
            f"{strokes['heavy']:g}.",
            "Re-run 04_mark/build.py and rebuild this skill's assets.",
        )
    return heavy[0], strokes


def read_mark(name: str) -> str:
    path = MARKS / name
    if not path.exists():
        raise NotEquipped(f"{path} is missing. This skill needs its assets/marks folder.")
    return path.read_text("utf-8")


def view_box(svg: str) -> tuple[float, float, float, float]:
    match = re.search(r'viewBox="([^"]+)"', svg)
    if not match:
        raise NotEquipped("that SVG has no viewBox, so it cannot be resized safely")
    parts = [float(p) for p in match.group(1).replace(",", " ").split()]
    return parts[0], parts[1], parts[2], parts[3]


def resized(svg: str, width: float, height: float) -> str:
    svg = re.sub(r'\bwidth="[^"]*"', f'width="{width:g}"', svg, count=1)
    svg = re.sub(r'\bheight="[^"]*"', f'height="{height:g}"', svg, count=1)
    return svg


def recoloured(svg: str, colour: str) -> str:
    """Set the value currentColor will resolve to, on the root element only.

    Two shapes are handled, because the mark files have both. A file that already
    carries style="color:..." on its root has that value replaced. A file drawn to
    be recolourable carries no colour at all, so one is added. Either way this
    raises rather than returning the SVG unchanged: a colour that silently failed
    to apply is the exact kind of quiet wrong answer this whole skill exists to
    stop.
    """
    if re.search(r'<svg[^>]*\bstyle="color:#[0-9A-Fa-f]{6}"', svg):
        return re.sub(r'style="color:#[0-9A-Fa-f]{6}"', f'style="color:{colour}"', svg, count=1)

    updated, changes = re.subn(r"<svg\b", f'<svg style="color:{colour}"', svg, count=1)
    if changes != 1:
        raise NotEquipped(
            "that file has no <svg> root element, so the colour could not be applied. "
            "Nothing was written."
        )
    # The recolourable masters carry a comment reading "Recolourable: drawn in
    # currentColor, with no colour on the root." Once a colour is on the root that
    # sentence is false, and it is the sentence telling the recipient how to theme
    # the file — so every asset this command handed out carried a false instruction
    # about itself. Rewritten to say what the file now is.
    updated = re.sub(
        r"<!--\s*Recolourable:[^>]*?-->",
        f"<!-- Recoloured to {colour} on the root by asset.py. The shapes are still "
        f"drawn in currentColor, so overriding `color` on this element or an "
        f"ancestor still works; the master with no root colour is in 04_mark/svg. -->",
        updated, count=1)
    return updated


def write_out(svg: str, out: str | None) -> str:
    if not out:
        sys.stdout.write(svg.rstrip("\n") + "\n")
        return "standard output"
    path = Path(out).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg.rstrip("\n") + "\n", "utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# The refusals that are about geometry, not colour
# ---------------------------------------------------------------------------


def guard_never_recolour(role: str) -> None:
    if role not in MARK_COLOUR_ROLES:
        raise Refused(
            f"The mark may not be drawn in {role}.",
            "The mark carries no colour of its own. It is drawn in currentColor and takes the "
            "theme it lands in. A status colour or a raw ramp step on the mark is a recolour.",
            "The mark may be drawn in: " + ", ".join(MARK_COLOUR_ROLES),
        )


def guard_never_stretch(width: float, height: float) -> None:
    if abs(width - height) > 1e-9:
        raise Refused(
            "The mark may not be stretched.",
            f"Asked for {width:g} x {height:g}, which is not square. "
            "The mark's aspect ratio is 1:1 and stays 1:1.",
            f"Use --size {max(width, height):g} for a square, or scale the whole thing evenly.",
        )


def guard_no_shadow(shadow: bool) -> None:
    if shadow:
        raise Refused(
            "The mark may not carry a shadow.",
            "The marks card states three things that are never done to it: never recolour it, "
            "never add a shadow, never stretch it.",
            "Put the mark on a surface that already gives it enough contrast, and measure it "
            "with `asset.py contrast` rather than adding a shadow to rescue it.",
        )


def guard_mark_size(size: float, weight: str) -> None:
    if size < mark_floor_px():
        raise Refused(
            f"The mark may not be made smaller than {mark_floor_px():g} px.",
            f"Asked for {size:g} px. At {mark_floor_px():g} px the heavy stroke renders at 2.4 px and "
            "the circle's counter is about 5.6 px across. Below that the counter closes and the "
            "mark reads as a filled blob.",
            f"Use --size {mark_floor_px()} or larger. For anything smaller than a favicon, use no "
            "mark at all rather than an unreadable one.",
        )
    strokes = stroke_rule()
    switch, regular = strokes["switch_px"], strokes["regular"]
    if size < switch and weight == "regular":
        raise Refused(
            f"The regular weight may not be used below {switch} px.",
            f"Asked for the regular weight at {size:g} px. Its stroke is "
            f"{regular:g} of 100 units, which renders at "
            f"{size * regular / 100:.2f} px here and thins away.",
            f"Use --weight heavy below {switch} px. That is the whole reason the heavy "
            "weight exists.",
        )


# ---------------------------------------------------------------------------
# The makers
# ---------------------------------------------------------------------------


def make_mark(args, primitives, semantic) -> dict:
    size = float(args.size)
    guard_no_shadow(args.shadow)
    guard_never_stretch(size, float(args.height) if args.height else size)
    guard_mark_size(size, args.weight)
    guard_never_recolour(args.on_colour)

    measurement = check_ground(
        args.on_colour, args.on, args.theme, primitives, semantic, house_rule=True
    )
    svg = read_mark(f"mark-{args.weight}.svg")
    svg = resized(svg, size, size)
    svg = recoloured(svg, resolve(args.on_colour, args.theme, primitives, semantic))
    where = write_out(svg, args.out)
    clear = size / 2.0
    return {
        "made": f"the mark, {args.weight} weight, {size:g} x {size:g} px",
        "written to": where,
        "drawn in": measurement["foreground"],
        "on": measurement["ground"],
        "contrast": f"{measurement['measured']}:1 against a target of {measurement['target']}:1",
        "judged by": measurement["judged_by"],
        "stroke": "9 of 100 units" if args.weight == "regular" else "15 of 100 units",
        # The NOTE that used to sit here said the marks card in 08_components stated
        # one stroke width instead, and that the owner had to settle the two. It is
        # settled: the manifest wins, and 08_components/build.py now reads the rule
        # out of the manifest rather than carrying its own copy.
        "clear space": (
            f"{clear:g} px on all four sides — half the mark's own height, from "
            "assets/marks/manifest.json"
        ),
    }


def make_wordmark(args, primitives, semantic) -> dict:
    guard_no_shadow(args.shadow)
    guard_never_recolour(args.on_colour)
    name = f"wordmark-{args.script}.svg"
    svg = read_mark(name)
    _, _, vb_width, vb_height = view_box(svg)

    width = float(args.size)
    height = width * vb_height / vb_width
    # The em box is 100 units of the viewBox's own height.
    em_px = height * 100.0 / vb_height
    if em_px + 1e-9 < WORDMARK_EM_FLOOR_PX:
        needed = WORDMARK_EM_FLOOR_PX * vb_height / 100.0 * vb_width / vb_height
        raise Refused(
            f"The {args.script} wordmark may not be set below a {WORDMARK_EM_FLOOR_PX} px em.",
            f"At {width:g} px wide the em box is {em_px:.2f} px, which is under the system's "
            f"{WORDMARK_EM_FLOOR_PX} px Bangla floor. Below it the conjuncts and the মাত্রা close up.",
            f"Use --size {needed:.0f} or larger for the {args.script} wordmark.",
        )

    measurement = check_ground(
        args.on_colour, args.on, args.theme, primitives, semantic, house_rule=True
    )
    svg = resized(svg, round(width, 2), round(height, 2))
    svg = recoloured(svg, resolve(args.on_colour, args.theme, primitives, semantic))
    where = write_out(svg, args.out)
    return {
        "made": f"the {args.script} wordmark, {width:g} x {height:.2f} px",
        "written to": where,
        "drawn in": measurement["foreground"],
        "on": measurement["ground"],
        "contrast": f"{measurement['measured']}:1 against a target of {measurement['target']}:1",
        "judged by": measurement["judged_by"],
        "em box": f"{em_px:.2f} px, against a {WORDMARK_EM_FLOOR_PX} px floor",
        "note": (
            "This is an outline, not live text, so it needs no font. Never re-typeset it: the "
            "Bangla shapes 16 code points into 11 glyphs and re-typesetting loses the conjuncts."
        ),
    }


def make_icon(args) -> dict:
    if args.appstore:
        if args.radius is not None or args.rounded:
            raise Refused(
                "The App Store master may not have a radius applied.",
                "That one file is square, full-bleed and unmasked by definition. Apple's system "
                "applies the mask itself and derives its specular highlights from the layer "
                "edges, so a pre-rounded edge sits inside the mask and the highlight follows the "
                "wrong geometry. Apple's own wording is that pre-masked artwork 'negatively "
                "impacts specular highlight effects' and makes edges 'look jagged'.",
                "For the rounded icon use `asset.py icon` without --appstore. Since "
                "26 August 2026 that is the WEB icon only — a browser will not round "
                "a favicon for you, and Apple and Google both round for themselves.",
            )
        if int(args.size) not in PLATFORM_MASTERS["apple"]:
            raise Refused(
                "Apple's masters come at two sizes and nothing else.",
                f"Asked for {int(args.size)} px. Apple's app icon layout size is "
                "1024 x 1024 px for iOS, iPadOS, macOS and visionOS, and 1088 x 1088 "
                "px for watchOS. Icon Composer expects those exact masters.",
                "Use --size 1024 or --size 1088, or drop --appstore for the rounded "
                "web icon at any size.",
            )
        size = int(args.size)
        appearance = getattr(args, "appearance", None) or "default"
        available = PLATFORM_MASTERS["apple"].get(size, {})
        if appearance not in available:
            raise Refused(
                f"There is no {appearance} appearance at {size} px.",
                "Apple's masters are 1024 px for iOS, iPadOS, macOS and visionOS, "
                "with Default, Dark and Mono appearances, and 1088 px for watchOS "
                "with Default only. Apple generates clear light, clear dark, tinted "
                "light and tinted dark from those three; they are not authored here.",
                f"At {size} px the appearances are: "
                f"{', '.join(sorted(available)) or 'none — use 1024 or 1088'}.",
            )
        name = available[appearance]
        svg = read_mark(name)
        guard_unmasked(svg, name)
        where = write_out(svg, args.out)
        return {
            "made": f"the Apple master, {size} x {size} px, {appearance} appearance, "
                    f"square and unmasked",
            "written to": where,
            "from": name,
            "shape": ("no ground; the alpha carries the shape" if appearance == "mono"
                      else "square, fully opaque"),
            "use": "Icon Composer, which expects unmasked layers and applies the mask "
                   "and the Liquid Glass effects itself",
        }

    size = int(args.size)
    if size < mark_floor_px():
        raise Refused(
            f"An icon may not be made smaller than {mark_floor_px():g} px.",
            f"Asked for {size} px. The mark inside it would fall below its own floor.",
            f"Use --size {mark_floor_px()} or larger.",
        )
    published = {192: "icon-192.svg", 512: "icon-512.svg", 1024: "icon-1024.svg", 1088: "icon-1088-watch.svg"}
    # THE STROKE RULE APPLIES HERE TOO. It did not, and that is why the studio's
    # own 16 px favicon carried the regular stroke that this same script refuses
    # to make as a standalone mark: `asset.py mark --size 16 --weight regular`
    # exited 2 with "The regular weight may not be used below 24 px", and
    # `asset.py icon --size 16` then wrote stroke-width="9" and exited 0.
    source, strokes = rounded_source(size, published.get(size, "icon-1024.svg"))
    svg = resized(read_mark(source), size, size)
    where = write_out(svg, args.out)
    stroke = strokes["stroke_by_file"][source]
    return {
        "made": f"the everyday rounded icon, {size} x {size} px",
        "written to": where,
        "from": source + ("" if size in published and stroke == strokes["regular"]
                          else " scaled — no file is published at that size"),
        "stroke": (
            f"{stroke:g} of 100 units, the "
            f"{'heavy' if stroke == strokes['heavy'] else 'regular'} weight. "
            f"Rule: {strokes['rule']}, from assets/marks/manifest.json"
        ),
        "corner radius": (
            "24 % of the width, from this system's own radius-hero token. Apple publishes no "
            "app-icon corner radius; this number is the studio's and is not attributed to Apple."
        ),
        "safe field": (
            "the mark's worst corner sits 45.00 of 45 units from the centre, inside both the "
            "90-unit field and the circle watchOS and visionOS mask to"
        ),
        "if you submit to a store": "use `asset.py icon --appstore` for Apple's "
                                    "square unmasked master. This rounded file is "
                                    "for the web.",
    }


def make_tile(args) -> dict:
    size = int(args.size)
    if size < mark_floor_px():
        raise Refused(
            f"A tile may not be made smaller than {mark_floor_px():g} px.",
            f"Asked for {size} px. The mark inside it would fall below its own floor.",
            f"Use --size {mark_floor_px()} or larger.",
        )
    strokes = stroke_rule()
    svg = resized(read_mark("tile-web.svg"), size, size)
    where = write_out(svg, args.out)
    stroke = strokes["stroke_by_file"]["tile-web.svg"]
    if size < strokes["switch_px"] and stroke != strokes["heavy"]:
        raise Refused(
            f"The web tile artwork no longer carries the heavy stroke, so it "
            f"cannot be made below {strokes['switch_px']} px.",
            f"tile-web.svg is at stroke {stroke:g} and the rule is "
            f"\"{strokes['rule']}\".",
            "Re-run 04_mark/build.py and rebuild this skill's assets.",
        )
    return {
        "made": f"the web tile, {size} x {size} px",
        "written to": where,
        "stroke": (
            f"{stroke:g} of 100 units, the "
            f"{'heavy' if stroke == strokes['heavy'] else 'regular'} weight. "
            f"Rule: {strokes['rule']}, from assets/marks/manifest.json"
        ),
        "corner radius": "24 % of the width, from radius-hero",
        "background showing": "4.7 % at the corners, which is what tells you the rounding is baked in",
    }


def make_swatch(args, primitives, semantic) -> dict:
    measurement = check_ground(args.role, args.on, args.theme, primitives, semantic)
    fg = resolve(args.role, args.theme, primitives, semantic)
    bg = resolve(args.on, args.theme, primitives, semantic)
    size = int(args.size)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
        f'width="{size}" height="{size}" role="img">'
        f"<title>Aninda Studio — {args.role} on {args.on}, {args.theme} theme, "
        f"{measurement['measured']}:1</title>"
        f'<rect width="{size}" height="{size}" rx="8" fill="{bg}"/>'
        f'<rect x="{size // 6}" y="{size // 6}" width="{size - size // 3}" '
        f'height="{size - size // 3}" rx="4" fill="{fg}"/>'
        "</svg>"
    )
    where = write_out(svg, args.out)
    return {
        "made": f"a swatch of {args.role} on {args.on}, {args.theme} theme",
        "written to": where,
        "foreground": measurement["foreground"],
        "ground": measurement["ground"],
        "contrast": f"{measurement['measured']}:1 against a target of {measurement['target']}:1",
        "judged by": measurement["judged_by"],
    }


def report_contrast(args, primitives, semantic) -> dict:
    fg = resolve(args.fg, args.theme, primitives, semantic)
    bg = resolve(args.bg, args.theme, primitives, semantic)
    text_target, non_text_target = theme_targets(args.theme)
    kind, criterion = criterion_for(args.fg)
    target = text_target if kind == "text" else non_text_target
    measured = ratio(fg, bg)
    result = {
        "foreground": f"{args.fg} {fg}",
        "ground": f"{args.bg} {bg}",
        "theme": args.theme,
        "measured": f"{measured:.2f}:1",
        "target": f"{target:.1f}:1",
        "verdict": "passes" if measured + 1e-9 >= target else "FALLS SHORT",
        "judged by": criterion or "nothing — a surface is a ground, not a foreground",
    }
    if kind == "text":
        result["also"] = f"AAA (7:1) {'met' if measured >= 7.0 else 'not met'}."
    elif kind == "non-text":
        result["also"] = (
            "There is no level above this one. WCAG defines no AAA level for non-text contrast, "
            "so a border or a focus ring that meets 3:1 has fully met 1.4.11."
        )
    passing = [
        f"{candidate} ({ratio(fg, resolve(candidate, args.theme, primitives, semantic)):.2f}:1)"
        for candidate in surface_roles(semantic)
        if ratio(fg, resolve(candidate, args.theme, primitives, semantic)) + 1e-9 >= target
    ]
    result["grounds it passes on"] = ", ".join(passing) if passing else "none in this theme"
    return result


def do_list(semantic) -> dict:
    return {
        "assets": (
            "mark, wordmark, icon, tile, swatch. `contrast` reports a measurement and makes "
            "nothing."
        ),
        "themes": ", ".join(THEMES),
        "colour roles": ", ".join(roles(semantic)),
        "grounds": ", ".join(surface_roles(semantic)),
        "the mark may be drawn in": ", ".join(MARK_COLOUR_ROLES),
        "mark weights": "regular (stroke 9, at 24 px and above), heavy (stroke 15, below 24 px)",
        "mark size floor": f"{mark_floor_px():g} px",
        "wordmark scripts": "latin, bangla",
        "published icon sizes": "192, 512, 1024, 1088 (watchOS)",
        "the one exception": (
            "`icon --appstore` gives Apple's square unmasked masters: --size 1024 with "
            "--appearance default, dark or mono, and --size 1088 for watchOS. A radius "
            "on any of them is refused."
        ),
        "examples": (
            "asset.py mark --weight heavy --size 20 --on surface-base --theme dark --out mark.svg | "
            "asset.py wordmark --script bangla --size 320 --on surface-bright | "
            "asset.py icon --appstore | "
            "asset.py contrast --fg accent-default --bg surface-dim --theme light"
        ),
    }


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="asset.py",
        description="Make one Aninda Studio asset. Refuses an impermissible combination.",
    )
    sub = parser.add_subparsers(dest="what", required=True)

    def ground_args(p, default_role: str) -> None:
        p.add_argument("--on", default="surface.base", help="the ground it will sit on")
        p.add_argument(
            "--as",
            dest="on_colour",
            default=default_role,
            help="the role it is drawn in",
        )
        p.add_argument("--theme", default="light", choices=list(THEMES))
        p.add_argument("--out", default=None, help="where to write it; omitted prints to the screen")
        p.add_argument("--shadow", action="store_true", help="refused, and says why")

    p_list = sub.add_parser("list", help="what can be made, and with what")
    p_list.set_defaults(kind="list")

    p_mark = sub.add_parser("mark", help="the mark on its own")
    p_mark.add_argument("--weight", default="regular", choices=["regular", "heavy"])
    p_mark.add_argument("--size", default=64, type=float, help="width and height in px")
    p_mark.add_argument("--height", default=None, type=float, help="refused unless it equals --size")
    ground_args(p_mark, "ink.default")

    p_word = sub.add_parser("wordmark", help="the set name, Latin or Bangla")
    p_word.add_argument("--script", default="latin", choices=["latin", "bangla"])
    p_word.add_argument("--size", default=240, type=float, help="width in px")
    ground_args(p_word, "ink.default")

    p_icon = sub.add_parser("icon", help="an app or platform icon")
    p_icon.add_argument("--size", default=1024, type=int)
    p_icon.add_argument("--appstore", action="store_true",
                        help="Apple's square unmasked master")
    p_icon.add_argument("--appearance", default="default",
                        choices=("default", "dark", "mono"),
                        help="which Apple appearance; 1024 only")
    p_icon.add_argument("--radius", default=None, type=float, help="refused with --appstore")
    p_icon.add_argument("--rounded", action="store_true", help="refused with --appstore")
    p_icon.add_argument("--out", default=None)

    p_tile = sub.add_parser("tile", help="the web tile")
    p_tile.add_argument("--size", default=512, type=int)
    p_tile.add_argument("--out", default=None)

    p_swatch = sub.add_parser("swatch", help="one role on one ground")
    p_swatch.add_argument("--role", required=True)
    p_swatch.add_argument("--on", default="surface.base")
    p_swatch.add_argument("--theme", default="light", choices=list(THEMES))
    p_swatch.add_argument("--size", default=96, type=int)
    p_swatch.add_argument("--out", default=None)

    p_contrast = sub.add_parser("contrast", help="measure a pairing and make nothing")
    p_contrast.add_argument("--fg", required=True)
    p_contrast.add_argument("--bg", required=True)
    p_contrast.add_argument("--theme", default="light", choices=list(THEMES))

    return parser


def normalise(value: str | None) -> str | None:
    """Accept accent-default as well as accent.default. One less thing to get wrong."""
    if value is None:
        return None
    return value.replace("-", ".") if "." not in value else value


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    for field in ("on", "on_colour", "role", "fg", "bg"):
        if hasattr(args, field):
            setattr(args, field, normalise(getattr(args, field)))

    try:
        primitives, semantic = load_tokens()
        if args.what == "list":
            result = do_list(semantic)
        elif args.what == "mark":
            result = make_mark(args, primitives, semantic)
        elif args.what == "wordmark":
            result = make_wordmark(args, primitives, semantic)
        elif args.what == "icon":
            result = make_icon(args)
        elif args.what == "tile":
            result = make_tile(args)
        elif args.what == "swatch":
            result = make_swatch(args, primitives, semantic)
        else:
            result = report_contrast(args, primitives, semantic)
    except Refused as refusal:
        out = [
            "",
            "REFUSED",
            "-------",
            f"  Rule      {refusal.rule}",
            f"  Measured  {refusal.measured}",
            f"  Instead   {refusal.remedy}",
            "",
            "  Nothing was written. This is the answer, not a failure — the combination asked",
            "  for is one the system does not allow.",
            "",
        ]
        sys.stderr.write("\n".join(out))
        return 2
    except NotEquipped as problem:
        sys.stderr.write(f"\nNOT EQUIPPED: {problem}\n\n")
        return 3

    width = max(len(key) for key in result)
    lines = [""]
    for key, value in result.items():
        lines.append(f"  {key.ljust(width)}  {value}")
    lines.append("")
    sys.stdout.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
