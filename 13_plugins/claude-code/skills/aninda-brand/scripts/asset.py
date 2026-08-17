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

# The mark's own size floor. Derived here, not taken from the mark manifest,
# which states the stroke rule and the safe field but no minimum size.
#
# At 16 px the heavy stroke (15 of 100 units) renders at 2.4 px and the circle's
# counter — the enclosed space inside it — is about 5.6 px across. Below that the
# counter closes and the mark reads as a filled blob.
MARK_FLOOR_PX = 16

# The stroke rule, from 04_mark/manifest.json.
STROKE_SWITCH_PX = 24

# The em box a wordmark must reach before its Bangla conjuncts stop being
# legible. It is the system's own 12 px Bangla floor, applied to an outline.
WORDMARK_EM_FLOOR_PX = 12

# The one size Apple asks for, and the one this file exists to satisfy.
APPSTORE_SIZE = 1024

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
    """The seventeen role names, without their `color.` prefix."""
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
    if size < MARK_FLOOR_PX:
        raise Refused(
            f"The mark may not be made smaller than {MARK_FLOOR_PX} px.",
            f"Asked for {size:g} px. At {MARK_FLOOR_PX} px the heavy stroke renders at 2.4 px and "
            "the circle's counter is about 5.6 px across. Below that the counter closes and the "
            "mark reads as a filled blob.",
            f"Use --size {MARK_FLOOR_PX} or larger. For anything smaller than a favicon, use no "
            "mark at all rather than an unreadable one.",
        )
    if size < STROKE_SWITCH_PX and weight == "regular":
        raise Refused(
            f"The regular weight may not be used below {STROKE_SWITCH_PX} px.",
            f"Asked for the regular weight at {size:g} px. Its stroke is 9 of 100 units, which "
            f"renders at {size * 0.09:.2f} px here and thins away.",
            f"Use --weight heavy below {STROKE_SWITCH_PX} px. That is the whole reason the heavy "
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
        "clear space": (
            f"{clear:g} px on all four sides — half the mark's own height, from "
            "assets/marks/manifest.json. NOTE: the marks card in 08_components says one stroke "
            "width instead. The two statements in the system disagree and the owner needs to "
            "settle it; this script follows the manifest."
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
                "For a rounded icon use `asset.py icon` without --appstore. That is the everyday "
                "icon and it is used on every other surface, Apple included.",
            )
        if int(args.size) != APPSTORE_SIZE:
            raise Refused(
                f"The App Store master is {APPSTORE_SIZE} x {APPSTORE_SIZE} px and nothing else.",
                f"Asked for {int(args.size)} px. Apple asks for 1024 x 1024 (1088 for watchOS), "
                "and Icon Composer expects that exact master.",
                f"Use --size {APPSTORE_SIZE}, or drop --appstore if you want another size.",
            )
        svg = read_mark("icon-appstore-square-1024.svg")
        where = write_out(svg, args.out)
        return {
            "made": f"the App Store master, {APPSTORE_SIZE} x {APPSTORE_SIZE} px, square and unmasked",
            "written to": where,
            "shape": "square, fully opaque, 0.0 % background showing",
            "use": "an App Store submission through Icon Composer, and nothing else",
        }

    size = int(args.size)
    if size < MARK_FLOOR_PX:
        raise Refused(
            f"An icon may not be made smaller than {MARK_FLOOR_PX} px.",
            f"Asked for {size} px. The mark inside it would fall below its own floor.",
            f"Use --size {MARK_FLOOR_PX} or larger.",
        )
    published = {192: "icon-192.svg", 512: "icon-512.svg", 1024: "icon-1024.svg", 1088: "icon-1088-watch.svg"}
    source = published.get(size, "icon-1024.svg")
    svg = resized(read_mark(source), size, size)
    where = write_out(svg, args.out)
    return {
        "made": f"the everyday rounded icon, {size} x {size} px",
        "written to": where,
        "from": source + ("" if size in published else " scaled — no file is published at that size"),
        "corner radius": (
            "24 % of the width, from this system's own radius-hero token. Apple publishes no "
            "app-icon corner radius; this number is the studio's and is not attributed to Apple."
        ),
        "safe field": (
            "the mark's worst corner sits 45.00 of 45 units from the centre, inside both the "
            "90-unit field and the circle watchOS and visionOS mask to"
        ),
        "if you submit to the App Store": "use `asset.py icon --appstore` instead, not this file",
    }


def make_tile(args) -> dict:
    size = int(args.size)
    if size < MARK_FLOOR_PX:
        raise Refused(
            f"A tile may not be made smaller than {MARK_FLOOR_PX} px.",
            f"Asked for {size} px. The mark inside it would fall below its own floor.",
            f"Use --size {MARK_FLOOR_PX} or larger.",
        )
    svg = resized(read_mark("tile-web.svg"), size, size)
    where = write_out(svg, args.out)
    return {
        "made": f"the web tile, {size} x {size} px",
        "written to": where,
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
        "mark size floor": f"{MARK_FLOOR_PX} px",
        "wordmark scripts": "latin, bangla",
        "published icon sizes": "192, 512, 1024, 1088 (watchOS)",
        "the one exception": (
            "`icon --appstore` gives the square unmasked 1024 px master. It is the only file for "
            "an App Store submission, and a radius on it is refused."
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
    p_icon.add_argument("--appstore", action="store_true", help="the square unmasked master")
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
