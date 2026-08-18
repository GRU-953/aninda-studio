#!/usr/bin/env python3
"""Aninda Studio — the component and pattern card library, generator.

This script is the ONLY writer of 08_components/cards/, 08_components/fonts/ and
08_components/_cards.json. Nothing in those places is hand-written, and nothing
there should ever be hand-edited: the next run overwrites it.

    Build:   ./.venv/bin/python 08_components/build.py
    Verify:  ./.venv/bin/python 08_components/build.py --check

`--check` regenerates every byte in memory and compares it against what is on
disk. It writes nothing and exits non-zero on the first difference. That is the
drift guard: if a card has been edited by hand, or the tokens have moved and the
cards have not been rebuilt, --check fails.

What a card is
    A single self-contained HTML file. tokens.css and components.css are inlined,
    the three fonts are inlined as base64 woff2. A card opens from a file:// URL
    with no network at all. Line 1 is exactly the Claude Design index contract:

        <!-- @dsCard group="Foundations" -->

Fail-closed
    Every guard runs against the whole build held in memory. If any guard fails,
    the script writes nothing and exits 1. A half-written library is worse than
    no library.

Fonts and the licence point
    All three fonts are SIL OFL 1.1. Subsetting a font is modifying it under
    clause 3 of that licence. IBM Plex Mono carries the Reserved Font Name
    "Plex" — the exact string from its own licence, not "IBM Plex" — so the subset MUST NOT present itself under that name: its name
    table is rewritten to "Aninda Mono". Literata and Noto Serif Bengali carry no
    Reserved Font Name, so they keep their real names — renaming those would make
    the system harder to trace, not safer. Each OFL.txt is copied next to the
    subset it covers.

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import base64
import html
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

TOKENS_CSS = ROOT / "07_tokens" / "css" / "tokens.css"
COMPONENTS_CSS = HERE / "src" / "components.css"
TOKENS_BUILD = ROOT / "07_tokens" / "build"
# 04_mark/svg, not 03_directions/marks. This card — the one whose subject is the
# identity — was the only consumer in the system reading from the EXPLORATION
# stage, which 03_directions/build.py documents as writing rejected material and
# which is deliberately outside the rebuild chain. Proved by changing the circle
# radius in 04_mark/build.py: all ten SVGs updated, every gate passed, the cards
# rebuilt still drawing the superseded shape, --check reporting "No drift. 38
# files match", and the 138-second harness printing PASS. The two drawings were
# geometrically identical at the time, so nothing wrong ever shipped; any future
# redraw would have shipped everywhere except the page that teaches it.
MARKS_DIR = ROOT / "04_mark" / "svg"
# The mark's own rules live with the mark. This card used to state "Clear space:
# one stroke width", typed here by hand, against the manifest's "half the mark's
# own height on all four sides" — a factor of about four, presented on the card
# with the same green tick the system uses for a verified fact. Reading the rule
# from the manifest is what stops the two drifting apart again.
MARK_MANIFEST = ROOT / "04_mark" / "manifest.json"

CARDS_DIR = HERE / "cards"
FONTS_DIR = HERE / "fonts"
REGISTRY = HERE / "_cards.json"

# The Claude Code plugin bundles these same subsets and renders its own approved
# Bangla with them, so its Bangla is part of the character set. See the charset
# union in build() for what went wrong when it was not.
_SKILL = ROOT / "13_plugins" / "claude-code" / "skills" / "aninda-brand"
PLUGIN_BANGLA_JSON = _SKILL / "assets" / "bangla-verified.json"
PLUGIN_BANGLA_MD = _SKILL / "references" / "bangla.md"

# The shaping test set from 06_type. 06_type/review_bangla.py shows it in the
# shipped face, so it belongs in the charset the shipped face is subset to.
MEASUREMENTS_JSON = ROOT / "06_type" / "_data" / "measurements.json"

GENERATOR = "08_components/build.py"

# The one line that separates the generated token stylesheet — the only place in a
# card a literal colour is allowed — from everything the markup guard inspects.
# It is a constant rather than two copies of a string, because the copies drifting
# apart silently disabled the guard.
TOKENS_CSS_END = "/* <<< end 07_tokens/css/tokens.css */"

THEMES = [
    ("light", "Light", "আলো"),
    ("dark", "Dark", "অন্ধকার"),
    ("hc-light", "High contrast, light", ""),
    ("hc-dark", "High contrast, dark", ""),
]

FONT_SOURCES = {
    "latin": {
        "path": ROOT / "06_type/candidates/latin/literata/Literata[opsz,wght].ttf",
        "ofl": ROOT / "06_type/candidates/latin/literata/OFL.txt",
        "out": "literata-subset.woff2",
        "ofl_out": "literata-OFL.txt",
        "family": "Literata",
        "rename": None,
        # The layer uses 400, 500, 600 and 700 and nothing else, so the rest of
        # the weight axis is deadweight in every card. opsz is kept whole: the
        # type measurements confirmed browsers apply optical sizing on their own.
        "pin": {"wght": (400, 700)},
        "css_weight": "400 700",
    },
    "bangla": {
        "path": ROOT / "06_type/candidates/bangla/notoserifbengali/NotoSerifBengali[wdth,wght].ttf",
        "ofl": ROOT / "06_type/candidates/bangla/notoserifbengali/OFL.txt",
        "out": "notoserifbengali-subset.woff2",
        "ofl_out": "notoserifbengali-OFL.txt",
        "family": "Noto Serif Bengali",
        "rename": None,
        "pin": {"wdth": 100.0, "wght": (400, 700)},
        "css_weight": "400 700",
    },
    "mono": {
        "path": ROOT / "06_type/candidates/mono/ibmplexmono/IBMPlexMono-Regular.ttf",
        "ofl": ROOT / "06_type/candidates/mono/ibmplexmono/OFL.txt",
        "out": "anindamono-subset.woff2",
        "ofl_out": "anindamono-OFL.txt",
        "family": "Aninda Mono",
        "rename": "Aninda Mono",
        "pin": {},
        "css_weight": "400",
    },
}

FONT_DESCRIPTION = (
    "Subset generated by " + GENERATOR + " for the Aninda Studio card library. "
    "Do not hand-edit; the next build overwrites it."
)

PLACEHOLDER = "@@FONT_{}_BASE64@@"


# =========================================================================
# Guards
# =========================================================================

NAMED_COLOURS = {
    "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque",
    "black", "blanchedalmond", "blue", "blueviolet", "brown", "burlywood",
    "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue", "cornsilk",
    "crimson", "cyan", "darkblue", "darkcyan", "darkgoldenrod", "darkgray",
    "darkgreen", "darkgrey", "darkkhaki", "darkmagenta", "darkolivegreen",
    "darkorange", "darkorchid", "darkred", "darksalmon", "darkseagreen",
    "darkslateblue", "darkslategray", "darkslategrey", "darkturquoise",
    "darkviolet", "deeppink", "deepskyblue", "dimgray", "dimgrey", "dodgerblue",
    "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro",
    "ghostwhite", "gold", "goldenrod", "gray", "green", "greenyellow", "grey",
    "honeydew", "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender",
    "lavenderblush", "lawngreen", "lemonchiffon", "lightblue", "lightcoral",
    "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey",
    "lightpink", "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray",
    "lightslategrey", "lightsteelblue", "lightyellow", "lime", "limegreen",
    "linen", "magenta", "maroon", "mediumaquamarine", "mediumblue",
    "mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue",
    "mediumspringgreen", "mediumturquoise", "mediumvioletred", "midnightblue",
    "mintcream", "mistyrose", "moccasin", "navajowhite", "navy", "oldlace",
    "olive", "olivedrab", "orange", "orangered", "orchid", "palegoldenrod",
    "palegreen", "paleturquoise", "palevioletred", "papayawhip", "peachpuff",
    "peru", "pink", "plum", "powderblue", "purple", "rebeccapurple", "red",
    "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen",
    "seashell", "sienna", "silver", "skyblue", "slateblue", "slategray",
    "slategrey", "snow", "springgreen", "steelblue", "tan", "teal", "thistle",
    "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke", "yellow",
    "yellowgreen",
}

# `currentColor` is a reference, not a value. `transparent` is the only way CSS
# has to say "no colour here", and there is no token for the absence of a colour.
ALLOWED_COLOUR_KEYWORDS = {"currentcolor", "transparent"}

_HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
# (?i) because CSS colour functions are case-insensitive and RGB(255 0 0) is
# valid CSS. Without it this guard let every uppercase form through while
# reporting a clean pass — the worst kind of check.
_FUNC = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\s*\(",
                   re.IGNORECASE)
_DECL = re.compile(r"[-a-zA-Z][-a-zA-Z0-9]*\s*:\s*([^;{}]+)[;}]")


class BuildError(Exception):
    pass


def strip_css_comments(text: str) -> str:
    """Remove /* … */ while keeping the line count, so line numbers still mean
    something in the error message."""
    out: list[str] = []
    i = 0
    while True:
        start = text.find("/*", i)
        if start < 0:
            out.append(text[i:])
            break
        out.append(text[i:start])
        end = text.find("*/", start + 2)
        if end < 0:
            out.append("\n" * text.count("\n", start))
            break
        out.append("\n" * text.count("\n", start, end))
        i = end + 2
    return "".join(out)


def guard_stylesheet(text: str, name: str) -> None:
    """Refuse to build if the hand-authored stylesheet contains a literal colour."""
    problems: list[str] = []
    stripped = strip_css_comments(text)
    for lineno, line in enumerate(stripped.splitlines(), 1):
        if _HEX.search(line):
            problems.append(f"{name}:{lineno}: hex colour — {line.strip()}")
        if _FUNC.search(line):
            problems.append(f"{name}:{lineno}: colour function — {line.strip()}")

    for decl in _DECL.finditer(stripped):
        value = decl.group(1)
        for word in re.findall(r"[A-Za-z][A-Za-z0-9-]*", value):
            low = word.lower()
            if low in NAMED_COLOURS and low not in ALLOWED_COLOUR_KEYWORDS:
                problems.append(f"{name}: named colour '{word}' in value — {value.strip()}")
    if problems:
        raise BuildError(
            "The no-literal-colour rule failed in " + name + ":\n  " + "\n  ".join(problems)
        )


# The markup guard cannot look for a bare colour literal anywhere in the page,
# because the colour card legitimately PRINTS every hex as running text — that is
# the whole card. So it looks in the two places where a literal can actually paint
# something: inside a style attribute, and in an SVG paint attribute.
#
# The earlier version matched a nine-item property whitelist instead
# (fill|stroke|stop-color|flood-color|lighting-color|color|background|
# background-color|border-color|outline-color). Round 1 of the convergence review
# walked straight past it with style="box-shadow: 0 0 0 2px #ff0000" and the build
# reported a clean run. Every declaration inside a style attribute is now checked,
# whatever its property, so text-shadow, caret-color, accent-color,
# text-decoration-color and a gradient in background-image are all covered.
_STYLE_ATTR = re.compile(r"""\sstyle\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)
# The SVG presentation attributes that carry paint. This IS a closed set: SVG 2
# defines no others, and a value here is a colour by definition rather than by
# property name.
_SVG_PAINT_ATTR = re.compile(
    r"""\s(fill|stroke|stop-color|flood-color|lighting-color|color|solid-color)"""
    r"""\s*=\s*(?:"([^"]*)"|'([^']*)')""",
    re.IGNORECASE,
)


def colour_literal_in(value: str) -> str | None:
    """The literal colour in a CSS value, or None. Names what it found, so the
    build error says which form slipped through."""
    hit = _HEX.search(value)
    if hit:
        return hit.group(0)
    hit = _FUNC.search(value)
    if hit:
        return hit.group(0)
    for word in re.findall(r"[A-Za-z][A-Za-z0-9-]*", value):
        low = word.lower()
        if low in NAMED_COLOURS and low not in ALLOWED_COLOUR_KEYWORDS:
            return word
    return None


def guard_markup(markup: str, name: str) -> None:
    """Refuse to build if generated markup paints with a literal instead of a token."""
    problems: list[str] = []
    for match in _STYLE_ATTR.finditer(markup):
        declarations = match.group(1) or match.group(2) or ""
        for part in declarations.split(";"):
            if ":" not in part:
                continue
            prop, _, value = part.partition(":")
            found = colour_literal_in(value)
            if found:
                problems.append(f"style attribute {prop.strip()}: {value.strip()} "
                                f"(literal {found})")
    for match in _SVG_PAINT_ATTR.finditer(markup):
        value = match.group(2) or match.group(3) or ""
        found = colour_literal_in(value)
        if found:
            problems.append(f'{match.group(1)}="{value}" (literal {found})')
    if problems:
        raise BuildError(
            f"{name}: literal colour in generated markup, {len(problems)} of them:\n  "
            + "\n  ".join(problems)
        )


# =========================================================================
# Fonts
# =========================================================================


def is_bangla(ch: str) -> bool:
    # The Bengali block, plus the daṛi (U+0964, shared with Devanagari) and the
    # two zero-width joiners that conjunct formation depends on.
    return "ঀ" <= ch <= "৿" or ch in "।॥‌‍"


def chars_for(key: str, chars: str) -> str:
    """Each font carries only what it is actually asked to draw. Handing the
    Bangla face the whole Latin alphabet would double its size for nothing."""
    if key == "bangla":
        keep = {ch for ch in chars if is_bangla(ch)}
        keep |= set("  .,:;!?()[]-—…0123456789")
    elif key == "mono":
        keep = {ch for ch in chars if " " <= ch <= "~"}
        keep |= set("—…‘’“”·×")
    else:
        keep = {ch for ch in chars if not is_bangla(ch)}
        keep |= set("".join(chr(c) for c in range(0x20, 0x7F)))
    return "".join(sorted(keep))


def build_font(key: str, chars: str) -> bytes:
    import logging

    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    logging.getLogger("fontTools").setLevel(logging.ERROR)
    chars = chars_for(key, chars)
    spec = FONT_SOURCES[key]
    src = spec["path"]
    if not src.exists():
        raise BuildError(f"Font not found: {src}")

    font = TTFont(str(src), recalcTimestamp=False)
    font.recalcTimestamp = False

    options = subset.Options()
    options.layout_features = ["*"]      # Bangla conjuncts live in GSUB. Keep all of it.
    options.name_IDs = ["*"]             # Keep the copyright and licence records.
    options.name_legacy = True
    options.name_languages = ["*"]
    options.recalc_bounds = False
    options.recalc_timestamp = False
    options.glyph_names = False
    options.hinting = True
    options.desubroutinize = False
    options.retain_gids = False

    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text=chars)
    subsetter.subset(font)

    # Narrow the variation axes AFTER subsetting. Doing it first leaves gvar with
    # no entry for glyphs that no longer vary, and the subsetter then fails on the
    # missing key. This order avoids that entirely.
    if spec["pin"] and "fvar" in font:
        font = instancer.instantiateVariableFont(
            font, spec["pin"], updateFontNames=False, inplace=False
        )
        font.recalcTimestamp = False

    if spec["rename"]:
        rename_family(font, spec["rename"])

    set_description(font, FONT_DESCRIPTION)

    # OFL clause 3 — the primary name of a modified font must not carry the
    # original's Reserved Font Name. Assert it rather than trust it.
    if spec["rename"]:
        for nid in (1, 3, 4, 6, 16, 17):
            record = font["name"].getDebugName(nid)
            if record and "plex" in record.lower():
                raise BuildError(
                    f"{key}: name record {nid} still says '{record}'. The Reserved "
                    "Font Name survived the rename, which would breach OFL 1.1 clause 3."
                )

    font.flavor = "woff2"
    buf = io.BytesIO()
    font.save(buf, reorderTables=False)
    font.close()
    return buf.getvalue()


def rename_family(font, family: str, style: str = "Regular",
                  what: str = "subset of a SIL OFL 1.1 font") -> None:
    """Rewrite the primary name records. Copyright, trademark and licence stay.

    `what` describes the modification, and it is a parameter because the desktop
    face is renamed whole rather than subset. Name ID 3 said "subset of" on a font
    that is not one, which is a small untrue statement inside a licence-relevant
    record.
    """
    full = family if style == "Regular" else f"{family} {style}"
    postscript = family.replace(" ", "") + "-" + style.replace(" ", "")
    unique = f"{full}; {what}, generated by {GENERATOR}"
    new = {1: family, 2: style, 3: unique, 4: full, 6: postscript, 16: family, 17: style}
    name = font["name"]
    for record in list(name.names):
        if record.nameID in new:
            name.setName(new[record.nameID], record.nameID, record.platformID,
                         record.platEncID, record.langID)
    for nid, value in new.items():
        if name.getDebugName(nid) is None and nid in (1, 2, 4, 6):
            name.setName(value, nid, 3, 1, 0x409)


def set_description(font, text: str) -> None:
    """Name ID 10 is the description field. A woff2 cannot open with a comment
    header the way a text file can, so the header goes here instead."""
    name = font["name"]
    for record in list(name.names):
        if record.nameID == 10:
            name.setName(text, 10, record.platformID, record.platEncID, record.langID)
    if name.getDebugName(10) is None:
        name.setName(text, 10, 3, 1, 0x409)


DESKTOP_FONT_OUT = "AnindaMono-Regular.ttf"
DESKTOP_FONT_DESCRIPTION = (
    "IBM Plex Mono Regular, renamed 'Aninda Mono' by " + GENERATOR + " because "
    "'Plex' is a Reserved Font Name under SIL OFL 1.1 clause 3. Unsubset, so it is "
    "usable as an installed desktop font. Do not hand-edit; the next build "
    "overwrites it. Licence: anindamono-OFL.txt beside this file."
)


def desktop_font() -> bytes:
    """The renamed monospace face as an installable .ttf, whole rather than subset.

    13_plugins/figma requires "Aninda Mono" as a font the operating system has
    installed, and 13_plugins/figma/src/plan.ts stops the build if it is absent.
    Until 18 August 2026 the only file this project produced under that name was a
    woff2, which is a web format and does not install as a system font — so step 1
    of the Figma instructions ended in a refusal with no documented way forward, on
    the one required input that only this project can supply.

    It is deliberately NOT subset. The card library subsets because it knows every
    character it will ever draw; a designer typing into Figma does not, and a
    subset desktop font drops to a fallback the moment they type a character it
    does not carry.
    """
    from fontTools.ttLib import TTFont

    spec = FONT_SOURCES["mono"]
    if not spec["path"].exists():
        raise BuildError(f"Font not found: {spec['path']}")
    font = TTFont(str(spec["path"]), recalcTimestamp=False)
    font.recalcTimestamp = False
    rename_family(font, spec["rename"], what="renamed, unsubset SIL OFL 1.1 font")
    set_description(font, DESKTOP_FONT_DESCRIPTION)

    # OFL clause 3, asserted rather than trusted — the same gate build_font applies.
    for nid in (1, 3, 4, 6, 16, 17):
        record = font["name"].getDebugName(nid)
        if record and "plex" in record.lower():
            raise BuildError(
                f"desktop font: name record {nid} still says '{record}'. The Reserved "
                "Font Name survived the rename, which would breach OFL 1.1 clause 3."
            )
    buf = io.BytesIO()
    font.save(buf, reorderTables=False)
    return buf.getvalue()


def font_face_css(faces: dict[str, bytes]) -> str:
    blocks = []
    for key in ("latin", "bangla", "mono"):
        spec = FONT_SOURCES[key]
        blocks.append(
            "@font-face {\n"
            f"  font-family: \"{spec['family']}\";\n"
            "  font-style: normal;\n"
            f"  font-weight: {spec['css_weight']};\n"
            "  font-display: block;\n"
            f"  src: url(data:font/woff2;base64,{PLACEHOLDER.format(key.upper())}) format(\"woff2\");\n"
            "}"
        )
    return "\n".join(blocks)


# =========================================================================
# Small HTML helpers
# =========================================================================


def e(text: str) -> str:
    return html.escape(str(text), quote=True)


ICON_PATHS = {
    "check": '<path d="M3 8.6 6.4 12 13 4.6"/>',
    "cross": '<path d="M4 4 12 12M12 4 4 12"/>',
    "warn": '<path d="M8 2.2 15 13.8H1Z"/><path d="M8 6.4v3.1"/><path d="M8 11.9h.01"/>',
    "info": '<circle cx="8" cy="8" r="6.2"/><path d="M8 7.4v4"/><path d="M8 4.9h.01"/>',
    "chevron": '<path d="M3.5 6 8 10.5 12.5 6"/>',
    "arrow": '<path d="M2.5 8h10.5"/><path d="M9.2 4.2 13 8l-3.8 3.8"/>',
    "plus": '<path d="M8 3v10M3 8h10"/>',
    "search": '<circle cx="7" cy="7" r="4.6"/><path d="M10.4 10.4 14 14"/>',
    "dot": '<circle cx="8" cy="8" r="3.2" fill="currentColor" stroke="none"/>',
    "doc": '<path d="M4 1.8h5l3 3v9.4H4Z"/><path d="M9 1.8v3h3"/><path d="M6 8.5h4M6 11h4"/>',
    "spark": '<path d="M8 2v12M2 8h12M4 4l8 8M12 4l-8 8"/>',
    "lock": '<rect x="3" y="7" width="10" height="7" rx="1.6"/><path d="M5.5 7V5.2a2.5 2.5 0 0 1 5 0V7"/>',
    "gear": '<circle cx="8" cy="8" r="2.6"/><path d="M8 1.6v1.8M8 12.6v1.8M14.4 8h-1.8M3.4 8H1.6M12.5 3.5 11.2 4.8M4.8 11.2 3.5 12.5M12.5 12.5 11.2 11.2M4.8 4.8 3.5 3.5"/>',
    "chart": '<path d="M2 14V2"/><path d="M2 14h12"/><path d="M5 11V7M8.5 11V4M12 11V8.5"/>',
}


def icon(name: str, cls: str = "as-icon") -> str:
    return (
        f'<svg class="{cls}" viewBox="0 0 16 16" width="16" height="16" '
        'aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
        f"{ICON_PATHS[name]}</svg>"
    )


def bn(text: str, large: bool = False) -> str:
    cls = ' class="as-bn-large"' if large else ""
    return f'<span lang="bn"{cls}>{e(text)}</span>'


def walk_language_scopes(doc: str):
    """Borrowed, not copied, from 09_guidebook/build.py.

    That file holds the one implementation of "what language is this text run in",
    with its own account of the three earlier versions that each got scope tracking
    wrong. A third copy would be a third thing to keep right, so this imports it.

    The import is by path rather than by package because these generators are
    scripts in numbered folders, not a package. It costs about 0.1 s at module
    load and reads no card data, so it does not invert the build order — the
    guidebook still runs after this file and reads _cards.json.
    """
    import importlib.util

    global _GUIDEBOOK
    if _GUIDEBOOK is None:
        source = ROOT / "09_guidebook" / "build.py"
        if not source.exists():
            raise BuildError(
                f"{source} is missing. This build reads its language-scope walker "
                f"from there rather than keeping a second copy of it."
            )
        spec = importlib.util.spec_from_file_location("_aninda_guidebook", source)
        module = importlib.util.module_from_spec(spec)
        sys.modules["_aninda_guidebook"] = module
        spec.loader.exec_module(module)
        _GUIDEBOOK = module
    return _GUIDEBOOK.walk_language_scopes(doc)


_GUIDEBOOK = None


def guard_language_of_parts(pages: dict[str, str]) -> None:
    """No Bangla may ship outside a lang="bn" element, and no English inside one.

    WCAG 2.2 SC 3.1.2 Language of Parts, Level AA. The site has this guard
    (11_site/build.py) and the guidebook has it (guard_inline_bangla), and the
    largest surface — 30 cards — had none, so `grep -n lang 08_components/check.py`
    returned nothing at all.

    What it cost: two cards shipped a bare Bangla word inside an English paragraph,
    five times each across the theme panels. Chromium reported the containing
    paragraph as lang='en' with fontFamily 'Literata, Georgia, serif', and
    CSS.getPlatformFontsForNode showed the Bangla glyphs drawn by macOS's Kohinoor
    Bangla — a system face — rather than by the Noto Serif Bengali subset the card
    inlines. So the card footer's "Fonts are subset and inlined; this card needs no
    network" was untrue of that text, and on a machine with no Bengali font it is
    tofu. On typography.html the run sat at 12.0032px and weight 400, which is
    precisely the case the sentence containing it says must gain a weight step.

    The scope walker skips script, style, title and textarea, which is why this can
    run over a card that inlines components.css — that stylesheet has মাত্রা in two
    comments. Running 11_site/check.py's expression verbatim over the cards counted
    those two as faults on all thirty, and a guard that reports one false positive
    per file is a guard somebody switches off.
    """
    bangla = re.compile(r"[\u0980-\u09FF]")
    problems: list[str] = []
    for name, markup in pages.items():
        for token, lang in walk_language_scopes(markup):
            if lang == "skip" or not token.strip():
                continue
            if bangla.search(token) and lang != "bn":
                problems.append(
                    f'{name}: Bangla outside lang="bn" — {token.strip()[:44]}')
            if lang == "bn" and not bangla.search(token) \
                    and re.search(r"[A-Za-z]{4}", token):
                problems.append(
                    f'{name}: English inside lang="bn" — {token.strip()[:44]}')
    if problems:
        raise BuildError(
            f"WCAG 2.2 SC 3.1.2 Language of Parts failed in {len(problems)} "
            f"place(s):\n  " + "\n  ".join(problems[:10]) +
            ("\n  …" if len(problems) > 10 else "") +
            "\n  Bangla must sit inside lang=\"bn\". Nothing else applies the "
            "Bengali family, the measured multiplier, the 12 px floor or the "
            "weight step below 14 px, because all four are keyed to "
            ":lang(bn), [lang=\"bn\"] in tokens.css."
        )


def guard_field_descriptions(pages: dict[str, str]) -> None:
    """Every hint or error beside a control must be in that control's description.

    WCAG 2.2 SC 1.3.1 Info and Relationships, Level A: text positioned as help for
    a control states a relationship visually, and that relationship has to be
    programmatically determinable too. `aria-describedby` is how.

    Twenty-five of the fifty-five such spans were referenced and thirty were not,
    which is why this is a generator guard rather than a rewrite: the technique was
    already in the file, applied inconsistently. Chromium's
    Accessibility.getPartialAXTree reported description=None on 'Account number',
    'Language', 'Plan' and 'Group'. On 'Group' the entire success state reached
    sighted users only — the words were unlinked and the green tick is
    aria-hidden="true" like every icon() in this file, so nothing announced that
    the field had validated.

    A hint inside the <label> is exempt: it is already part of the accessible name.
    That is the .as-choice pattern, where the label wraps the control.
    """
    import re as _re

    problems: list[str] = []
    for name, markup in pages.items():
        # Only the primary stage is inspected. The quad panels repeat the same
        # markup with the same ids per panel prefix, so a fault would be reported
        # five times and fixed once.
        for block in _re.findall(r'<div class="as-field">(.*?)</div>', markup, _re.S):
            if "<label" in block and "</label>" not in block:
                continue
            described = set()
            for value in _re.findall(r'aria-describedby="([^"]+)"', block):
                described.update(value.split())
            controls = _re.findall(r"<(input|select|textarea)\b[^>]*", block)
            if not controls:
                continue
            for span in _re.findall(r'<span class="as-(?:hint|error)"[^>]*>', block):
                ident = _re.search(r'id="([^"]+)"', span)
                if ident is None:
                    problems.append(f"{name}: a hint or error with no id at all — {span}")
                elif ident.group(1) not in described:
                    problems.append(
                        f'{name}: {span} is not in any aria-describedby in its field')
    if problems:
        raise BuildError(
            f"WCAG 2.2 SC 1.3.1 Info and Relationships failed in {len(problems)} "
            f"place(s):\n  " + "\n  ".join(problems[:10]) +
            ("\n  …" if len(problems) > 10 else "") +
            "\n  Give the span an id and name it in the control's "
            "aria-describedby. Text placed under a control is help for that "
            "control, and a screen reader is told so only by that attribute."
        )


def e_mixed(text: str) -> str:
    """Escape a sentence that has a Bangla word inside it, tagging the word.

    Bangla inside an English sentence has to declare its own language. WCAG 2.2
    SC 3.1.2 Language of Parts (Level AA) asks for it, and in this system it also
    decides whether the text gets the Bengali family at all: the whole Bangla half
    of tokens.css is keyed to `:lang(bn), [lang="bn"]`, so an untagged run gets
    Literata, which has no Bengali glyphs, and falls back to whatever the reader's
    machine has. Chromium drew the two runs that shipped this way in macOS's
    Kohinoor Bangla, at 12.0032px and weight 400 — the exact case one of those very
    sentences says must gain a weight step.

    The card text is written as plain strings and escaped on the way out, so a
    hand-written <span> in a string would be escaped into visible markup. This
    escapes the sentence and then wraps each unbroken Bangla run in the span.
    """
    escaped = e(text)
    return re.sub(r"[\u0980-\u09FF\u200c\u200d।॥]+",
                  lambda m: f'<span lang="bn">{m.group(0)}</span>', escaped)


def code_block(name: str, body: str, copy_label: str = "", copy_lang: str = "") -> str:
    # e_mixed rather than e, because a sample that shows how to mark Bangla up
    # contains Bangla. Untagged, that run is announced as English and set in
    # Aninda Mono, which is subset from IBM Plex Mono and carries no Bengali glyph
    # at all — so the sample teaching the lang attribute was itself unable to draw
    # its own example. The span changes nothing a reader sees or copies.
    lines = []
    for line in body.strip("\n").split("\n"):
        if line.lstrip().startswith("<!--") or line.lstrip().startswith("/*"):
            lines.append(f'<span class="as-code__comment">{e_mixed(line)}</span>')
        else:
            lines.append(e_mixed(line))
    label = copy_label or "Copy the code"
    lang_attr = f' lang="{copy_lang}"' if copy_lang else ""
    return (
        '<div class="as-code">'
        f'<div class="as-code__head"><span class="as-code__name">{e(name)}</span>'
        f'<button type="button" class="as-btn as-btn--small"{lang_attr}>{e(label)}</button></div>'
        f'<pre class="as-code__pre"><code>{chr(10).join(lines)}</code></pre>'
        '<p class="as-code__said as-visually-hidden" role="status" aria-live="polite"></p>'
        "</div>"
    )


# =========================================================================
# Verified Bangla. Every string in this dictionary is taken verbatim from the
# recommended-strings table of 06_type/BANGLA-STANDARD.md, which is the governing
# document. Nothing in it was written by me.
#
# It is not the whole story: 06_type/bangla-strings.json is the register written
# under those rules, and it supplies the card names, the card subtitles and the
# theme labels further down this file. Where neither holds a string, the card uses
# English and the gap is reported.
# =========================================================================

BN = {
    "wm-1": "অনিন্দ্য স্টুডিও",
    "wm-2": "অনিন্দ্য",
    "th-1": "আলো",
    "th-2": "অন্ধকার",
    "th-3": "বেশি কনট্রাস্ট",
    "col-1": "মোহনা",
    "col-2": "জোয়ার",
    "col-3": "পলি",
    "col-4": "কাশ",
    "col-5": "লাল মাটি",
    "col-6": "বর্ষা",
    "bt-1": "লেখাটি সংরক্ষণ করুন",
    "bt-2": "বাতিল করুন",
    "bt-3": "ফাইলটি মুছে ফেলুন",
    "bt-4": "আবার চেষ্টা করুন",
    "bt-5": "কোডটি কপি করুন",
    "ms-1": "সংরক্ষণ করা যায়নি। আপনার লেখা এখনো আছে — একটু পরে আবার চেষ্টা করুন।",
    "ms-2": "ফাইলটি অনেক বড়ো। সর্বোচ্চ ১০ মেগাবাইট।",
    "ms-3": "এখনো কিছু নেই। শুরু করতে প্রথম লেখাটি যোগ করুন।",
    "ms-4": "সংরক্ষিত হয়েছে",
    "vc-1": "আমি ছোটো, যত্নে গড়া সফটওয়্যার বানাই। কোনো কিছুর সীমা থাকলে সেটা এখানেই লেখা থাকবে — লুকিয়ে রাখা হবে না।",
    "gb-1": "স্বাগতম",
    "gb-2": "নাম",
    "gb-3": "চিহ্ন",
    "gb-4": "রং",
    "gb-5": "হরফ",
    "gb-6": "ফাঁক ও আকার",
    "gb-7": "উপাদান",
    "gb-8": "গতি",
    "gb-9": "কণ্ঠস্বর",
    "gb-10": "যা এই পদ্ধতি করে না",
}

BANGLA_NOTE = (
    "Bangla appears only where an approved string exists. Two files, and they are "
    "not interchangeable: 06_type/BANGLA-STANDARD.md governs — it holds the Bangla "
    "Academy spelling rules with their primary sources, and the 31 strings reviewed "
    "against them — while 06_type/bangla-strings.json is the register of 94 "
    "approved keys written under those rules, each carrying the rule number or "
    "dictionary page it rests on, and it is the file these cards actually read. "
    "The fields listed here are empty because neither holds an entry for them. "
    "Writing new Bangla to fill them is not allowed, so they stay in English and "
    "are named here instead, for review."
)


def bangla_gaps() -> dict:
    return {
        "note": BANGLA_NOTE,
        "name_bn": [c["slug"] for c in CARDS if not c["name_bn"]],
        "subtitle_bn": [c["slug"] for c in CARDS if not c["subtitle_bn"]],
    }


# =========================================================================
# Token data
# =========================================================================


def load_tokens() -> dict:
    primitive = json.loads((TOKENS_BUILD / "primitive.tokens.json").read_text("utf-8"))
    semantic = {}
    for key, _, _ in THEMES:
        semantic[key] = json.loads((TOKENS_BUILD / f"semantic.{key}.tokens.json").read_text("utf-8"))
    mark = json.loads(MARK_MANIFEST.read_text("utf-8"))
    return {"primitive": primitive, "semantic": semantic, "mark": mark}


ROLE_ORDER = [
    ("ink", "default", "--as-ink", "Body text and headings"),
    ("ink", "muted", "--as-ink-muted", "Secondary text, hints, captions"),
    ("line", "default", "--as-line", "Borders, rules, dividers"),
    ("accent", "default", "--as-accent", "Links, the primary action"),
    ("accent", "edge", "--as-accent-edge", "The line around an accent surface"),
    ("accent", "hover", "--as-accent-hover", "The hovered primary action, "
     "measured against the label it carries"),
    ("focus", "ring", "--as-focus-ring", "The focus indicator"),
    ("status", "success", "--as-success", "Something finished"),
    ("status", "warning", "--as-warning", "Something needs attention"),
    ("status", "danger", "--as-danger", "Something failed"),
    ("status", "info", "--as-info", "Something worth knowing"),
]

SURFACE_ORDER = ["lowest", "low", "base", "high", "highest", "dim", "bright"]


def ramp_names(primitive: dict) -> dict[str, tuple[str, str]]:
    out = {}
    for family, node in primitive["color"]["ramp"].items():
        if family.startswith("$"):
            continue
        desc = node.get("$description", "")
        match = re.match(r"^([A-Za-z ]+)\s*\(([^)]+)\)", desc)
        if match:
            out[family] = (match.group(1).strip(), match.group(2).strip())
    return out


def role_rows(tokens: dict, theme: str) -> list[dict]:
    data = tokens["semantic"][theme]["color"]
    names = ramp_names(tokens["primitive"])
    rows = []
    for group, key, var, use in ROLE_ORDER:
        node = data[group][key]
        ext = node.get("$extensions", {}).get("studio.aninda", {})
        proof = ext.get("proof", {})
        alias = node.get("$value", "")
        family = ""
        step = ""
        match = re.match(r"\{color\.ramp\.([a-z]+)\.(\d+)\}", str(alias))
        if match:
            family, step = match.group(1), match.group(2)
        latin, bangla = names.get(family, ("", ""))
        rows.append({
            "var": var,
            "use": use,
            "family": family,
            "family_name": latin,
            "family_name_bn": bangla,
            "step": step,
            "required": proof.get("required"),
            "measured": proof.get("measured"),
            "worst": proof.get("worstCaseLsb"),
            "level": proof.get("level", ""),
            "criterion": proof.get("criterion", ""),
            "hardest": proof.get("hardestGround", ""),
        })
    return rows


def surface_rows(tokens: dict, theme: str) -> list[dict]:
    data = tokens["semantic"][theme]["color"]["surface"]
    rows = []
    for key in SURFACE_ORDER:
        node = data[key]
        ext = node.get("$extensions", {}).get("studio.aninda", {})
        rows.append({
            "var": f"--as-surface-{key}",
            "name": key,
            "hex": node["$value"]["hex"],
            "luminance": ext.get("luminance"),
        })
    return rows


TYPE_STEPS = [
    ("--as-text-caption", "caption", "caption"),
    ("--as-text-body", "body", "body"),
    ("--as-text-lead", "lead", "heading"),
    ("--as-text-h3", "h3", "heading"),
    ("--as-text-h2", "h2", "title"),
    ("--as-text-h1", "h1", "title"),
    ("--as-text-display", "display", "display"),
]


# =========================================================================
# Demos
# =========================================================================


def d_button(p, th, T):
    return f"""
<div class="as-stack">
  <div class="as-row">
    <button type="button" class="as-btn as-btn--primary">Save the entry</button>
    <button type="button" class="as-btn">Cancel the change</button>
    <button type="button" class="as-btn as-btn--danger">Delete the file</button>
    <a class="as-btn as-btn--quiet" href="#">Read the guidance</a>
  </div>
  <div class="as-row">
    <button type="button" class="as-btn as-btn--small">Copy the code</button>
    <button type="button" class="as-btn as-btn--icon" aria-label="Add an entry">{icon('plus')}</button>
    <button type="button" class="as-btn as-btn--primary">{icon('check')}<span>Publish the card</span></button>
  </div>
  <div class="as-row">
    <button type="button" class="as-btn" disabled>Save the entry</button>
    <span class="as-hint">Off until a title is typed.</span>
  </div>
  <div class="as-row">
    <button type="button" class="as-btn as-btn--primary" lang="bn">{e(BN['bt-1'])}</button>
    <button type="button" class="as-btn" lang="bn">{e(BN['bt-2'])}</button>
    <button type="button" class="as-btn as-btn--danger" lang="bn">{e(BN['bt-3'])}</button>
  </div>
</div>"""


def d_input(p, th, T):
    return f"""
<div class="as-stack">
  <div class="as-field">
    <label class="as-label" for="{p}-name">Your name</label>
    <input class="as-input" id="{p}-name" type="text" value="Aninda Sundar Howlader">
  </div>
  <div class="as-field">
    <label class="as-label" for="{p}-mail">Email address <span class="as-label__optional">(optional)</span></label>
    <input class="as-input" id="{p}-mail" type="email" placeholder="you@example.com" aria-describedby="{p}-mail-hint">
    <span class="as-hint" id="{p}-mail-hint">I use this to reply, and for nothing else.</span>
  </div>
  <div class="as-field">
    <label class="as-label" for="{p}-size">File size</label>
    <input class="as-input" id="{p}-size" type="text" value="18 MB" aria-invalid="true" aria-describedby="{p}-size-err">
    <span class="as-error" id="{p}-size-err">{icon('warn')}<span>That file is too large. The maximum is 10 MB, so choose a smaller one.</span></span>
  </div>
  <div class="as-field">
    <label class="as-label" for="{p}-locked">Account number</label>
    <input class="as-input" id="{p}-locked" type="text" value="6041 2288" disabled aria-describedby="{p}-locked-hint">
    <span class="as-hint" id="{p}-locked-hint">Off because this cannot be changed after the account opens.</span>
  </div>
</div>"""


def d_select(p, th, T):
    return f"""
<div class="as-stack">
  <div class="as-field">
    <label class="as-label" for="{p}-theme">Theme</label>
    <span class="as-select-wrap">
      <select class="as-select" id="{p}-theme">
        <option>Follow the system</option>
        <option selected>Light</option>
        <option>Dark</option>
        <option>High contrast, light</option>
        <option>High contrast, dark</option>
      </select>
      <span class="as-select-wrap__arrow">{icon('chevron')}</span>
    </span>
  </div>
  <div class="as-field">
    <label class="as-label" for="{p}-lang">Language</label>
    <span class="as-select-wrap">
      <select class="as-select" id="{p}-lang" aria-describedby="{p}-lang-hint">
        <option selected>English</option>
        <option lang="bn">{e(BN['wm-2'])}</option>
      </select>
      <span class="as-select-wrap__arrow">{icon('chevron')}</span>
    </span>
    <span class="as-hint" id="{p}-lang-hint">The arrow is drawn, not a character, so it keeps the theme colour.</span>
  </div>
  <div class="as-field">
    <label class="as-label" for="{p}-plan">Plan</label>
    <span class="as-select-wrap">
      <select class="as-select" id="{p}-plan" disabled aria-describedby="{p}-plan-hint">
        <option>Studio</option>
      </select>
      <span class="as-select-wrap__arrow">{icon('chevron')}</span>
    </span>
    <span class="as-hint" id="{p}-plan-hint">Off until the account is verified.</span>
  </div>
</div>"""


def d_choice(p, th, T):
    return f"""
<div class="as-stack">
  <fieldset class="as-fieldset">
    <legend>What to include</legend>
    <div class="as-stack as-stack--tight">
      <label class="as-choice" for="{p}-c1">
        <input class="as-choice__control" id="{p}-c1" type="checkbox" checked>
        <span class="as-choice__text"><span class="as-choice__label">The measured contrast figures</span>
        <span class="as-choice__hint">Read from the token file, not typed by hand.</span></span>
      </label>
      <label class="as-choice" for="{p}-c2">
        <input class="as-choice__control" id="{p}-c2" type="checkbox">
        <span class="as-choice__text"><span class="as-choice__label">The Bangla specimen</span></span>
      </label>
      <label class="as-choice" for="{p}-c3">
        <input class="as-choice__control" id="{p}-c3" type="checkbox" disabled>
        <span class="as-choice__text"><span class="as-choice__label">The print edition</span>
        <span class="as-choice__hint">Off until the guidebook is finished.</span></span>
      </label>
    </div>
  </fieldset>
  <fieldset class="as-fieldset">
    <legend>How wide</legend>
    <div class="as-stack as-stack--tight">
      <label class="as-choice" for="{p}-r1">
        <input class="as-choice__control" id="{p}-r1" type="radio" name="{p}-width" checked>
        <span class="as-choice__text"><span class="as-choice__label">Narrow, 360 px</span></span>
      </label>
      <label class="as-choice" for="{p}-r2">
        <input class="as-choice__control" id="{p}-r2" type="radio" name="{p}-width">
        <span class="as-choice__text"><span class="as-choice__label">Medium, 768 px</span></span>
      </label>
      <label class="as-choice" for="{p}-r3">
        <input class="as-choice__control" id="{p}-r3" type="radio" name="{p}-width">
        <span class="as-choice__text"><span class="as-choice__label">Wide, 1280 px</span></span>
      </label>
    </div>
  </fieldset>
</div>"""


def d_textarea(p, th, T):
    return f"""
<div class="as-stack">
  <div class="as-field">
    <label class="as-label" for="{p}-note">What changed</label>
    <textarea class="as-textarea" id="{p}-note" rows="4" aria-describedby="{p}-note-hint">I moved the focus ring out to a 2 px offset so it sits on the page rather than on the button.</textarea>
    <span class="as-hint" id="{p}-note-hint">Drag the bottom edge to make this taller. It never gets wider, so the line length stays readable.</span>
  </div>
  <div class="as-field">
    <label class="as-label" for="{p}-empty">A note in Bangla</label>
    <textarea class="as-textarea" id="{p}-empty" rows="3" lang="bn">{e(BN['vc-1'])}</textarea>
  </div>
</div>"""


def d_badge(p, th, T):
    return f"""
<div class="as-stack">
  <div class="as-row">
    <span class="as-badge as-badge--success">{icon('check', 'as-icon')}<span>Passed</span></span>
    <span class="as-badge as-badge--warning">{icon('warn', 'as-icon')}<span>Check this</span></span>
    <span class="as-badge as-badge--danger">{icon('cross', 'as-icon')}<span>Failed</span></span>
    <span class="as-badge as-badge--info">{icon('info', 'as-icon')}<span>Note</span></span>
    <span class="as-badge as-badge--accent">{icon('dot', 'as-icon')}<span>New</span></span>
    <span class="as-badge">{icon('dot', 'as-icon')}<span>Draft</span></span>
  </div>
  <div class="as-row">
    <span class="as-badge as-badge--solid as-badge--success">{icon('check', 'as-icon')}<span>Passed</span></span>
    <span class="as-badge as-badge--solid as-badge--warning">{icon('warn', 'as-icon')}<span>Check this</span></span>
    <span class="as-badge as-badge--solid as-badge--danger">{icon('cross', 'as-icon')}<span>Failed</span></span>
    <span class="as-badge as-badge--solid as-badge--info">{icon('info', 'as-icon')}<span>Note</span></span>
    <span class="as-badge as-badge--solid as-badge--accent">{icon('dot', 'as-icon')}<span>New</span></span>
  </div>
  <p class="as-hint">Each badge carries a glyph and a word. Without the colour, each one still says what it means.</p>
</div>"""


def d_card(p, th, T):
    return f"""
<div class="as-grid as-grid--wide">
  <article class="as-card">
    <p class="as-card__meta">Foundation</p>
    <h3 class="as-card__title">Colour</h3>
    <p class="as-card__body">Every colour role, four themes, and a measured contrast ratio behind every one of them.</p>
    <div class="as-card__foot">
      <a class="as-btn as-btn--small as-btn--primary" href="#">Open the card</a>
      <span class="as-badge as-badge--success">{icon('check')}<span>Measured</span></span>
    </div>
  </article>
  <article class="as-card as-card--flat">
    <p class="as-card__meta">Foundation</p>
    <h3 class="as-card__title">{bn(BN['gb-5'], large=True)} Typography</h3>
    <p class="as-card__body">One scale, two scripts. Bangla is corrected by a measured multiplier and then held at a 12 px floor.</p>
    <div class="as-card__foot">
      <a class="as-btn as-btn--small" href="#">Open the card</a>
    </div>
  </article>
</div>"""


def d_alert(p, th, T):
    return f"""
<div class="as-stack">
  <div class="as-alert as-alert--danger" role="alert">
    {icon('cross', 'as-icon as-alert__glyph')}
    <div class="as-alert__body">
      <p class="as-alert__title">Couldn't save the entry</p>
      <p class="as-alert__text">Your work is still here. Try again in a moment.</p>
      <p class="as-alert__text" lang="bn">{e(BN['ms-1'])}</p>
    </div>
  </div>
  <div class="as-alert as-alert--warning">
    {icon('warn', 'as-icon as-alert__glyph')}
    <div class="as-alert__body">
      <p class="as-alert__title">That file is too large</p>
      <p class="as-alert__text">The maximum is 10 MB. Choose a smaller file and try again.</p>
      <p class="as-alert__text" lang="bn">{e(BN['ms-2'])}</p>
    </div>
  </div>
  <div class="as-alert as-alert--success">
    {icon('check', 'as-icon as-alert__glyph')}
    <div class="as-alert__body">
      <p class="as-alert__title">Saved</p>
      <p class="as-alert__text">Your entry is stored and the card has been rebuilt.</p>
    </div>
  </div>
  <div class="as-alert as-alert--info">
    {icon('info', 'as-icon as-alert__glyph')}
    <div class="as-alert__body">
      <p class="as-alert__title">This is a preview</p>
      <p class="as-alert__text">Nothing here is published yet. Publishing is a separate step you take.</p>
    </div>
  </div>
</div>"""


def d_dialog(p, th, T):
    return f"""
<div class="as-dialog-stage">
  <div class="as-dialog-stage__scrim"></div>
  <dialog class="as-dialog" open aria-labelledby="{p}-dlg-title">
    <h3 class="as-dialog__title" id="{p}-dlg-title">Delete this file?</h3>
    <p class="as-dialog__text">The file and its history are deleted with it. I cannot restore them.</p>
    <div class="as-dialog__foot">
      <button type="button" class="as-btn">Keep the file</button>
      <button type="button" class="as-btn as-btn--danger">Delete the file</button>
    </div>
  </dialog>
</div>"""


def d_table(p, th, T):
    rows = [
        ("Colour", "Foundations", "15.90", "success", "check", "Passed"),
        ("Typography", "Foundations", "8.44", "success", "check", "Passed"),
        ("Button", "Components", "6.34", "success", "check", "Passed"),
        ("Badge", "Components", "5.61", "warning", "warn", "Check this"),
        ("Dashboard", "Patterns", "4.19", "danger", "cross", "Failed"),
    ]
    body = "".join(
        f"<tr><th scope=\"row\">{e(n)}</th><td>{e(g)}</td><td class=\"as-num\">{e(r)}</td>"
        f"<td><span class=\"as-badge as-badge--{k}\">{icon(ic)}<span>{e(label)}</span></span></td></tr>"
        for n, g, r, k, ic, label in rows
    )
    return f"""
<div class="as-scroll-x">
  <table class="as-table as-table--numeric">
    <caption>Smallest measured contrast ratio on each card, light theme.</caption>
    <thead><tr><th scope="col">Card</th><th scope="col">Group</th><th scope="col" class="as-num">Ratio</th><th scope="col">Result</th></tr></thead>
    <tbody>{body}</tbody>
  </table>
</div>"""


# Each tab and the panel it controls, so the two cannot be emitted out of step.
# The card used to declare three tabs and emit ONE panel, which left ten
# aria-controls attributes across the five theme stages naming ids that were not
# in the document, and gave the two unselected tabs tabindex="-1" with no
# arrow-key handler to reach them — ten visible, enabled buttons that no key
# could focus, a WCAG 2.2 SC 2.1.1 failure. Round 1 of the convergence review
# found it by exhausting Tab, ArrowRight, ArrowDown and End in Chromium.
TAB_PANELS = [
    ("Foundations",
     "Six cards. Colour, typography, space and shape, motion, the marks, and accessibility.",
     "The selected tab is bold, underlined and marked with aria-selected. Three signals, "
     "and only one of them is a colour."),
    ("Components",
     "Sixteen cards. Buttons, fields, alerts, badges, tables, tabs and the rest of the set.",
     "Arrow keys move between the tabs and Home and End jump to the ends, which is what "
     "the roving tabindex on this pattern requires."),
    ("Patterns",
     "Eight cards. Whole layouts assembled from the components, each one measured.",
     "Every panel is in the document. A tab that points at a panel which is not there "
     "tells a screen reader about content it can never reach."),
]


def d_tabs(p, th, T):
    tabs = []
    panels = []
    for index, (label, body, hint) in enumerate(TAB_PANELS, start=1):
        selected = index == 1
        # Roving tabindex: exactly one tab is in the tab sequence, and the arrow
        # keys in SWITCHER_JS move both the focus and the selection.
        roving = "" if selected else ' tabindex="-1"'
        tabs.append(
            f'<button type="button" class="as-tab" role="tab" id="{p}-t{index}" '
            f'aria-selected="{str(selected).lower()}" aria-controls="{p}-p{index}"{roving}>'
            f"{e(label)}</button>"
        )
        # The panels carry no tabindex. The ARIA Authoring Practices offer
        # tabindex="0" on a panel with no focusable content, but that would add a
        # tab stop to every card that check.py would then hold to the focus-ring
        # floor, and a paragraph is not a control. Reachability of the tabs is
        # the accessibility failure; a focusable paragraph is not.
        panels.append(
            f'<div class="as-tabpanel" role="tabpanel" id="{p}-p{index}" '
            f'aria-labelledby="{p}-t{index}"{"" if selected else " hidden"}>'
            f"<p>{e(body)}</p><p class=\"as-hint\">{e(hint)}</p></div>"
        )
    return f"""
<div class="as-stack">
  <div class="as-tabs" role="tablist" aria-label="Card groups">
    {"".join(tabs)}
  </div>
  {"".join(panels)}
</div>"""


CURRENT = ' aria-current="page"'


def d_nav(p, th, T):
    items = [
        ("Colour", True, "dot"),
        ("Typography", False, "dot"),
        ("Space and shape", False, "dot"),
        ("Motion", False, "dot"),
        ("Accessibility", False, "dot"),
    ]
    vertical = "".join(
        '<li><a class="as-nav__link" href="#"' + (CURRENT if cur else "") + ">"
        + icon(ic) + "<span>" + e(label) + "</span></a></li>"
        for label, cur, ic in items
    )
    horizontal = "".join(
        '<li><a class="as-nav__link" href="#"' + (CURRENT if cur else "") + ">"
        + e(label) + "</a></li>"
        for label, cur in [("Cards", True), ("Tokens", False), ("Guidebook", False)]
    )
    return f"""
<div class="as-grid as-grid--wide">
  <nav class="as-nav" aria-label="Foundations">
    <ul class="as-nav__list">{vertical}</ul>
  </nav>
  <div class="as-stack">
    <nav class="as-nav as-nav--horizontal" aria-label="Sections">
      <ul class="as-nav__list">{horizontal}</ul>
    </nav>
    <p class="as-hint">The current item has a bar, a heavier weight and aria-current="page". Remove the colour and the bar and the weight still say which one you are on.</p>
  </div>
</div>"""


def d_breadcrumb(p, th, T):
    return f"""
<div class="as-stack">
  <nav class="as-breadcrumb" aria-label="Breadcrumb">
    <ol class="as-breadcrumb__list">
      <li class="as-breadcrumb__item"><a class="as-breadcrumb__link" href="#">Aninda Studio</a><span class="as-breadcrumb__sep" aria-hidden="true">/</span></li>
      <li class="as-breadcrumb__item"><a class="as-breadcrumb__link" href="#">Components</a><span class="as-breadcrumb__sep" aria-hidden="true">/</span></li>
      <li class="as-breadcrumb__item"><span class="as-breadcrumb__current" aria-current="page">Breadcrumb</span></li>
    </ol>
  </nav>
  <p class="as-hint">The last item is not a link, because you are already on it. It is marked with aria-current="page" and set in bold.</p>
</div>"""


def d_toast(p, th, T):
    return f"""
<div class="as-stack">
  <div class="as-toast as-toast--success" role="status">
    {icon('check', 'as-icon as-toast__glyph')}
    <div class="as-toast__body">
      <p class="as-toast__title">Saved</p>
      <p class="as-toast__text" lang="bn">{e(BN['ms-4'])}</p>
    </div>
    <button type="button" class="as-toast__dismiss" aria-label="Dismiss this message">{icon('cross')}</button>
  </div>
  <div class="as-toast as-toast--danger" role="alert">
    {icon('cross', 'as-icon as-toast__glyph')}
    <div class="as-toast__body">
      <p class="as-toast__title">Couldn't save the entry</p>
      <p class="as-toast__text">Your work is still here. Try again in a moment.</p>
    </div>
    <button type="button" class="as-toast__dismiss" aria-label="Dismiss this message">{icon('cross')}</button>
  </div>
  <div class="as-toast as-toast--info" role="status">
    {icon('info', 'as-icon as-toast__glyph')}
    <div class="as-toast__body">
      <p class="as-toast__title">The card was rebuilt</p>
      <p class="as-toast__text">Three files changed.</p>
    </div>
    <button type="button" class="as-toast__dismiss" aria-label="Dismiss this message">{icon('cross')}</button>
  </div>
</div>"""


def d_empty(p, th, T):
    return f"""
<div class="as-stack">
  <div class="as-empty">
    {icon('doc', 'as-icon as-empty__glyph')}
    <p class="as-empty__title">Nothing here yet</p>
    <p class="as-empty__text">Add your first entry to begin. It takes one line, and you can change it afterwards.</p>
    <p class="as-empty__text" lang="bn">{e(BN['ms-3'])}</p>
    <button type="button" class="as-btn as-btn--primary">{icon('plus')}<span>Add an entry</span></button>
  </div>
  <div class="as-empty">
    {icon('search', 'as-icon as-empty__glyph')}
    <p class="as-empty__title">No card matches "gradient"</p>
    <p class="as-empty__text">This system has no gradients. Try a role name instead, such as accent or danger.</p>
    <button type="button" class="as-btn">Clear the search</button>
  </div>
</div>"""


def d_code(p, th, T):
    first = code_block(
        "components.css",
        """/* The primary action. Three states, three different colours. */
.as-btn--primary {
  background-color: var(--as-accent);
  border-color: var(--as-accent);
  color: var(--as-surface-lowest);
}
.as-btn--primary:hover  { background-color: var(--as-accent-hover); }
.as-btn--primary:active { box-shadow: inset 0 0 0 1px var(--as-surface-lowest); }""",
    )
    second = code_block(
        "tokens.css",
        """/* The Bangla rule and its exception in one declaration, so nobody
   has to remember the exception. */
:lang(bn), [lang="bn"] {
  font-family: var(--as-font-bangla);
  font-size: clamp(var(--as-text-bangla-min),
                   calc(1em * var(--as-bangla-scale-body)), 100em);
}""",
        copy_label=BN["bt-5"],
        copy_lang="bn",
    )
    return (
        '<div class="as-stack">' + first + second
        + '<p class="as-hint">The block scrolls sideways rather than wrapping, because a '
        'wrapped line of code stops being the line you would copy.</p></div>'
    )


# ---- Foundations --------------------------------------------------------


def d_colour(p, th, T):
    theme = th or "light"
    rows = role_rows(T, theme)
    surfaces = surface_rows(T, theme)
    chips = "".join(
        f'<div class="as-doc-swatch">'
        f'<span class="as-doc-swatch__chip" style="background-color: var({r["var"]})"></span>'
        f'<span class="as-doc-swatch__body"><span class="as-doc-swatch__name">{e(r["use"])}</span>'
        f'<span class="as-doc-swatch__meta">{e(r["var"])} · {r["measured"]:.2f}:1 · needs {r["required"]}:1</span></span>'
        f"</div>"
        for r in rows
    )
    surf = "".join(
        f'<div class="as-doc-swatch">'
        f'<span class="as-doc-swatch__chip" style="background-color: var({s["var"]})"></span>'
        f'<span class="as-doc-swatch__body"><span class="as-doc-swatch__name">Surface {e(s["name"])}</span>'
        f'<span class="as-doc-swatch__meta">{e(s["hex"])}</span></span></div>'
        for s in surfaces
    )
    return f"""
<div class="as-stack">
  <p class="as-hint">Ten text and line roles, measured against the hardest surface each one can land on in this theme.</p>
  <div class="as-grid as-grid--wide">{chips}</div>
  <hr class="as-divider">
  <p class="as-hint">Seven surfaces. Each rung is at least &Delta;E2000 0.9 from the one before it, so the steps are visible without being loud.</p>
  <div class="as-grid">{surf}</div>
</div>"""


def colour_tables(T) -> str:
    out = []
    for key, label, label_bn in THEMES:
        rows = role_rows(T, key)
        body = "".join(
            f"<tr><th scope=\"row\">{e(r['use'])}</th>"
            f"<td><code>{e(r['var'])}</code></td>"
            f"<td>{e(r['family_name'])}{(' ' + bn(r['family_name_bn'])) if r['family_name_bn'] else ''} {e(r['step'])}</td>"
            f"<td class=\"as-num\">{r['required']}:1</td>"
            f"<td class=\"as-num\">{r['measured']:.4f}:1</td>"
            f"<td class=\"as-num\">{r['worst']:.4f}:1</td>"
            f"<td>{e(r['level'])}</td><td>{e(r['criterion'])}</td>"
            f"<td>{e(r['hardest'])}</td></tr>"
            for r in rows
        )
        out.append(
            f'<h3 class="as-h3">{e(label)}{(" " + bn(label_bn)) if label_bn else ""}</h3>'
            '<div class="as-scroll-x"><table class="as-table as-table--numeric">'
            '<caption>Every figure is read from 07_tokens/build/semantic.'
            f'{e(key)}.tokens.json at build time. None of it is typed here.</caption>'
            '<thead><tr><th scope="col">Role</th><th scope="col">Token</th>'
            '<th scope="col">Ramp step</th><th scope="col" class="as-num">Needs</th>'
            '<th scope="col" class="as-num">Measured</th><th scope="col" class="as-num">Worst case &plusmn;1 LSB</th>'
            '<th scope="col">Level</th><th scope="col">Criterion</th>'
            '<th scope="col">Hardest surface</th></tr></thead>'
            f"<tbody>{body}</tbody></table></div>"
        )
    return '<div class="as-stack as-stack--loose">' + "".join(out) + "</div>"


def d_typography(p, th, T):
    prim = T["primitive"]
    rows = []
    for var, name, band in TYPE_STEPS:
        rem = prim["dimension"]["type"][name]["$value"]["value"]
        px = rem * 16
        mult = prim["number"]["scale"]["bangla"][band]["$value"]
        rows.append((var, name, rem, px, band, mult, px * mult))
    scale = "".join(
        f"<tr><th scope=\"row\">{e(n)}</th><td><code>{e(v)}</code></td>"
        f"<td class=\"as-num\">{r:.4f} rem</td><td class=\"as-num\">{px:.2f} px</td>"
        f"<td>{e(b)}</td><td class=\"as-num\">{m}</td>"
        f"<td class=\"as-num\">{max(bpx, 12):.2f} px</td></tr>"
        for v, n, r, px, b, m, bpx in rows
    )
    return f"""
<div class="as-stack">
  <p class="as-display">Ag</p>
  <p class="as-h1">Estuary</p>
  <p class="as-h2">A studio of one</p>
  <p class="as-h3">Measured, not assumed</p>
  <p class="as-lead">A perfect fourth, 1.333 &mdash; the name comes from music, where the same ratio separates two notes. The jumps are large on purpose, so the hierarchy is unmistakable and fewer levels are needed to express it.</p>
  <p class="as-body">Literata carries an optical-size axis from 7 to 72, so the letterforms are redrawn for the size rather than scaled. Browsers apply that automatically.</p>
  <p class="as-caption">Caption size is 12 px. Nothing in this system is smaller.</p>
  <hr class="as-divider">
  <p class="as-lead as-bn-large" lang="bn">{e(BN['gb-5'])}</p>
  <p lang="bn">{e(BN['vc-1'])}</p>
  <p class="as-hint">Bangla is set in Noto Serif Bengali, never uppercased, never letter-spaced, never synthetically emboldened. Below 14 px it gains one weight step, because its <span lang="bn">মাত্রা</span> — the headline stroke along the top of the letters — goes pale before the letters do.</p>
  <hr class="as-divider">
  <div class="as-scroll-x">
    <table class="as-table as-table--numeric">
      <caption>The scale, and what the Bangla multiplier does to each step. The last column is held at the 12 px floor.</caption>
      <thead><tr><th scope="col">Step</th><th scope="col">Token</th><th scope="col" class="as-num">rem</th><th scope="col" class="as-num">Latin px</th><th scope="col">Multiplier band</th><th scope="col" class="as-num">Multiplier</th><th scope="col" class="as-num">Bangla px</th></tr></thead>
      <tbody>{scale}</tbody>
    </table>
  </div>
</div>"""


def d_space(p, th, T):
    prim = T["primitive"]
    steps = [(f"--as-space-{i}", prim["dimension"]["space"][str(i)]["$value"]["value"]) for i in range(10)]
    bars = "".join(
        f'<div class="as-stack as-stack--tight"><div class="as-doc-ruler" style="inline-size: var({v})"></div>'
        f'<span class="as-doc-swatch__meta">{e(v)} · {px} px</span></div>'
        for v, px in steps
    )
    radii = "".join(
        f'<div class="as-stack as-stack--tight">'
        f'<div style="block-size: var(--as-space-7); border: 1px solid var(--as-line); '
        f'background-color: var(--as-surface-highest); border-radius: var(--as-radius-{n})"></div>'
        f'<span class="as-doc-swatch__meta">--as-radius-{e(n)} · {prim["dimension"]["radius"][n]["$value"]["value"]} px</span></div>'
        for n in ("badge", "control", "card", "hero")
    )
    return f"""
<div class="as-stack">
  <p class="as-hint">A 4 px scale. Ten steps, and everything in the system sits on one of them.</p>
  <div class="as-stack as-stack--tight">{bars}</div>
  <hr class="as-divider">
  <p class="as-hint">Four radii. A badge is nearly square, a hero is generous, and nothing in between is invented on the spot.</p>
  <div class="as-grid">{radii}</div>
</div>"""


def d_motion(p, th, T):
    prim = T["primitive"]
    dur_c = prim["duration"]["motion"]["colour"]["$value"]["value"]
    dur_m = prim["duration"]["motion"]["move"]["$value"]["value"]

    def curve(name, points):
        x1, y1, x2, y2 = points
        return (
            f'<figure class="as-stack as-stack--tight" style="margin: 0">'
            f'<svg viewBox="0 0 100 100" width="100%" height="120" role="img" '
            f'aria-label="The {e(name)} easing curve" style="border: 1px solid var(--as-line); '
            f'border-radius: var(--as-radius-control); background-color: var(--as-surface-bright)">'
            f'<path d="M0 100 C {x1 * 100:.1f} {100 - y1 * 100:.1f} {x2 * 100:.1f} {100 - y2 * 100:.1f} 100 0" '
            f'fill="none" stroke="currentColor" stroke-width="3" vector-effect="non-scaling-stroke"/></svg>'
            f'<figcaption class="as-doc-swatch__meta">--as-ease-{e(name)}</figcaption></figure>'
        )

    curves = "".join(
        curve(n, prim["cubicBezier"]["motion"][n]["$value"])
        for n in ("standard", "enter", "exit")
    )
    return f"""
<div class="as-stack">
  <div class="as-row">
    <button type="button" class="as-btn as-btn--primary">Hover to see {dur_c} ms</button>
    <button type="button" class="as-btn">Hover to see {dur_c} ms</button>
  </div>
  <p class="as-hint">Colour changes take {dur_c} ms. Things that move take {dur_m} ms. Two durations, and that is the whole vocabulary. Something that moves may overshoot &mdash; travel a little past where it is going and settle back &mdash; while something that only changes colour never does.</p>
  <div class="as-grid as-grid--wide">{curves}</div>
  <div class="as-alert as-alert--info">
    {icon('info', 'as-icon as-alert__glyph')}
    <div class="as-alert__body">
      <p class="as-alert__title">Reduced motion is honoured at the root</p>
      <p class="as-alert__text">When the reader has asked their system for less motion, both durations drop to 1 ms. Nothing is removed, so a state change is still visible. It stops travelling instead.</p>
    </div>
  </div>
</div>"""


def d_marks(p, th, T):
    regular = read_mark("mark-regular.svg")
    heavy = read_mark("mark-heavy.svg")
    sizes = "".join(
        f'<div class="as-stack as-stack--tight" style="align-items: center">'
        f'{mark_at(regular, s)}<span class="as-doc-swatch__meta">{s} px</span></div>'
        for s in (24, 40, 64, 96)
    )
    return f"""
<div class="as-stack">
  <div class="as-grid as-grid--wide">
    <div class="as-stack as-stack--tight">
      {mark_at(regular, 120)}
      <p class="as-doc-swatch__meta">The mark, regular weight</p>
    </div>
    <div class="as-stack as-stack--tight">
      {mark_at(heavy, 120, accent=True)}
      <p class="as-doc-swatch__meta">The mark, heavy weight, drawn in the accent</p>
    </div>
  </div>
  <hr class="as-divider">
  <p class="as-hint">The mark is drawn in currentColor, so it takes the theme it lands in and yields to the system palette in forced colours. It carries no colour of its own.</p>
  <div class="as-row" style="align-items: flex-end">{sizes}</div>
  <hr class="as-divider">
  <div class="as-row">
    <span class="as-badge as-badge--danger">{icon('cross')}<span>Never recolour it</span></span>
    <span class="as-badge as-badge--danger">{icon('cross')}<span>Never add a shadow</span></span>
    <span class="as-badge as-badge--danger">{icon('cross')}<span>Never stretch it</span></span>
    <span class="as-badge as-badge--success">{icon('check')}<span>Clear space, always</span></span>
  </div>
  <!-- The rule is a hint rather than the badge's own label because .as-badge is
       white-space: nowrap, and a sentence long enough to state the rule without
       ambiguity overflows a 360 px viewport. It used to read "Clear space: one
       stroke width", which fitted and was about four times too small. -->
  <p class="as-hint">Clear space is {e(T['mark']['clear_space'])} — read from
  04_mark/manifest.json when this card is built, so it cannot drift from the rule the
  mark builder and asset.py both follow.</p>
  <p class="as-lead">{bn(BN['wm-1'], large=True)}</p>
</div>"""


def d_a11y(p, th, T):
    prim = T["primitive"]
    targets = [
        ("--as-target-min", "min", "WCAG 2.2 SC 2.5.8, Level AA"),
        ("--as-target-apple-min", "apple-min", "Apple HIG minimum, iOS and iPadOS"),
        ("--as-target-comfortable", "comfortable", "Apple HIG default, iOS and iPadOS"),
        ("--as-target-android-min", "android-min", "Android guidance, in dp"),
    ]
    boxes = "".join(
        f'<div class="as-stack as-stack--tight">'
        f'<div style="inline-size: var({v}); block-size: var({v}); border: 1px solid var(--as-line); '
        f'background-color: var(--as-surface-highest); border-radius: var(--as-radius-badge)"></div>'
        f'<span class="as-doc-swatch__meta">{prim["dimension"]["target"][k]["$value"]["value"]} px</span>'
        f'<span class="as-hint">{e(src)}</span></div>'
        for v, k, src in targets
    )
    fw = prim["dimension"]["focus"]["ring-width"]["$value"]["value"]
    fo = prim["dimension"]["focus"]["ring-offset"]["$value"]["value"]
    return f"""
<div class="as-stack">
  <p class="as-hint">Four target sizes, each with the guidance it comes from. Nothing in this system is smaller than the first.</p>
  <div class="as-row" style="align-items: flex-end">{boxes}</div>
  <hr class="as-divider">
  <p class="as-hint">The focus ring is {fw} px wide with a {fo} px offset. The offset matters: it puts the ring on the page rather than on the control, so the ring is measured against the surface behind it and not against a filled button.</p>
  <div class="as-row">
    <button type="button" class="as-btn">Move focus here</button>
    <button type="button" class="as-btn as-btn--primary">And here</button>
    <input class="as-input" style="inline-size: var(--as-space-9)" aria-label="A field to focus" value="And here">
  </div>
  <p class="as-hint">The ring is drawn from :focus, not :focus-visible. :focus-visible is a heuristic, and a heuristic can decide not to draw it.</p>
  <hr class="as-divider">
  <div class="as-alert as-alert--warning">
    {icon('warn', 'as-icon as-alert__glyph')}
    <div class="as-alert__body">
      <p class="as-alert__title">Never colour alone</p>
      <p class="as-alert__text">Every state here carries a glyph and a word as well as a colour. Remove the colour and the meaning survives.</p>
    </div>
  </div>
  <div class="as-row">
    <span class="as-badge as-badge--success">{icon('check')}<span>Passed</span></span>
    <span class="as-badge as-badge--danger">{icon('cross')}<span>Failed</span></span>
  </div>
</div>"""


# ---- Patterns -----------------------------------------------------------


def d_signin(p, th, T):
    return f"""
<div class="as-card" style="max-inline-size: 420px; margin-inline: auto">
  <div class="as-stack as-stack--tight">
    <p class="as-card__meta">{bn(BN['wm-1'])}</p>
    <h3 class="as-card__title">Sign in</h3>
    <p class="as-card__body">Use the email address you gave me. If you have not set a password, ask for a link instead.</p>
  </div>
  <form class="as-stack">
    <div class="as-field">
      <label class="as-label" for="{p}-si-mail">Email address</label>
      <input class="as-input" id="{p}-si-mail" type="email" autocomplete="username" placeholder="you@example.com">
    </div>
    <div class="as-field">
      <label class="as-label" for="{p}-si-pass">Password</label>
      <input class="as-input" id="{p}-si-pass" type="password" autocomplete="current-password" value="0000000000">
    </div>
    <label class="as-choice" for="{p}-si-keep">
      <input class="as-choice__control" id="{p}-si-keep" type="checkbox">
      <span class="as-choice__text"><span class="as-choice__label">Keep me signed in</span>
      <span class="as-choice__hint">Only on a machine you trust.</span></span>
    </label>
    <button type="submit" class="as-btn as-btn--primary">{icon('lock')}<span>Sign in</span></button>
    <a class="as-btn as-btn--quiet" href="#">Send me a sign-in link instead</a>
  </form>
</div>"""


def d_settings(p, th, T):
    return f"""
<div class="as-stack">
  <div class="as-split">
    <h3 class="as-h3">Settings</h3>
    <div class="as-row">
      <button type="button" class="as-btn">Cancel the change</button>
      <button type="button" class="as-btn as-btn--primary">Save the entry</button>
    </div>
  </div>
  <div class="as-grid as-grid--wide">
    <fieldset class="as-fieldset">
      <legend>Appearance</legend>
      <div class="as-stack">
        <div class="as-field">
          <label class="as-label" for="{p}-set-theme">Theme</label>
          <span class="as-select-wrap">
            <select class="as-select" id="{p}-set-theme" aria-describedby="{p}-set-theme-hint">
              <option selected>Follow the system</option>
              <option>Light</option>
              <option>Dark</option>
              <option>High contrast, light</option>
              <option>High contrast, dark</option>
            </select>
            <span class="as-select-wrap__arrow">{icon('chevron')}</span>
          </span>
          <span class="as-hint" id="{p}-set-theme-hint">Following the system also follows a request for more contrast, without a second choice here.</span>
        </div>
        <label class="as-choice" for="{p}-set-motion">
          <input class="as-choice__control" id="{p}-set-motion" type="checkbox" checked>
          <span class="as-choice__text"><span class="as-choice__label">Reduce motion</span>
          <span class="as-choice__hint">Already on, because your system asks for it.</span></span>
        </label>
      </div>
    </fieldset>
    <fieldset class="as-fieldset">
      <legend>What I keep</legend>
      <div class="as-stack as-stack--tight">
        <label class="as-choice" for="{p}-set-k1">
          <input class="as-choice__control" id="{p}-set-k1" type="checkbox" checked>
          <span class="as-choice__text"><span class="as-choice__label">Your cards and their history</span></span>
        </label>
        <label class="as-choice" for="{p}-set-k2">
          <input class="as-choice__control" id="{p}-set-k2" type="checkbox">
          <span class="as-choice__text"><span class="as-choice__label">Anonymous usage counts</span>
          <span class="as-choice__hint">Off by default. Nothing leaves your machine unless you turn this on.</span></span>
        </label>
      </div>
    </fieldset>
  </div>
  <div class="as-alert as-alert--danger">
    {icon('warn', 'as-icon as-alert__glyph')}
    <div class="as-alert__body">
      <p class="as-alert__title">Deleting the account removes everything</p>
      <p class="as-alert__text">Your cards, their history and your settings are deleted with it. I cannot restore them.</p>
      <div class="as-card__foot"><button type="button" class="as-btn as-btn--danger">Delete the account</button></div>
    </div>
  </div>
</div>"""


def d_dashboard(p, th, T):
    tiles = [
        ("Cards built", "30", "success", "check", "All passed"),
        ("Contrast floor", "4.19:1", "warning", "warn", "Above 3:1"),
        ("Widths checked", "3", "info", "info", "360, 768, 1280"),
        ("Themes", "4", "accent", "dot", "Every card"),
    ]
    grid = "".join(
        f'<article class="as-card as-card--tight"><p class="as-card__meta">{e(label)}</p>'
        f'<p class="as-h3">{e(value)}</p>'
        f'<p><span class="as-badge as-badge--{kind}">{icon(ic)}<span>{e(note)}</span></span></p></article>'
        for label, value, kind, ic, note in tiles
    )
    return f"""
<div class="as-stack">
  <div class="as-split">
    <h3 class="as-h3">Build report</h3>
    <div class="as-row">
      <button type="button" class="as-btn as-btn--small">{icon('search')}<span>Filter the rows</span></button>
      <button type="button" class="as-btn as-btn--small as-btn--primary">{icon('chart')}<span>Run the check</span></button>
    </div>
  </div>
  <div class="as-grid">{grid}</div>
  {d_table(p + '-dash', th, T)}
  <div class="as-alert as-alert--info">
    {icon('info', 'as-icon as-alert__glyph')}
    <div class="as-alert__body">
      <p class="as-alert__title">These figures come from check.py</p>
      <p class="as-alert__text">The numbers on this card are an example, not a live reading. A real dashboard would say when it last measured.</p>
    </div>
  </div>
</div>"""


FOCUS_SNIPPET = (
    ".as-root :is(a, button, input, select, textarea):focus {\n"
    "  outline: var(--as-focus-ring-width) solid var(--as-focus-ring);\n"
    "  outline-offset: var(--as-focus-ring-offset);\n"
    "}"
)


def d_docs(p, th, T):
    return f"""
<div class="as-stack">
  <nav class="as-breadcrumb" aria-label="Breadcrumb">
    <ol class="as-breadcrumb__list">
      <li class="as-breadcrumb__item"><a class="as-breadcrumb__link" href="#">Guidebook</a><span class="as-breadcrumb__sep" aria-hidden="true">/</span></li>
      <li class="as-breadcrumb__item"><a class="as-breadcrumb__link" href="#">{bn(BN['gb-7'])}</a><span class="as-breadcrumb__sep" aria-hidden="true">/</span></li>
      <li class="as-breadcrumb__item"><span class="as-breadcrumb__current" aria-current="page">Focus</span></li>
    </ol>
  </nav>
  <div class="as-grid as-grid--wide">
    <nav class="as-nav" aria-label="On this page">
      <ul class="as-nav__list">
        <li><a class="as-nav__link" href="#" aria-current="page">Why the ring is offset</a></li>
        <li><a class="as-nav__link" href="#">What the ring must clear</a></li>
        <li><a class="as-nav__link" href="#">Where it comes from</a></li>
      </ul>
    </nav>
    <article class="as-stack as-prose">
      <h3 class="as-h3">Why the ring is offset</h3>
      <p>The focus ring sits 2 px outside the control it belongs to. That gap is not decoration. It puts the ring on the page surface rather than on the control, so its contrast is measured against the surface behind it.</p>
      <p>A ring drawn tight against a filled button would be measured against the fill, and against the accent that gives roughly 1.5:1 — nowhere near the 3:1 a focus indicator needs.</p>
      <p><strong>Contrast ratio</strong> — how far apart two colours are in brightness, written as a ratio. 4.5:1 is the minimum for body text; 3:1 is the minimum for a focus indicator.</p>
      {code_block("components.css", FOCUS_SNIPPET)}
      <div class="as-alert as-alert--info">
        {icon('info', 'as-icon as-alert__glyph')}
        <div class="as-alert__body">
          <p class="as-alert__title">Where the figures come from</p>
          <p class="as-alert__text">Every ratio in this guidebook is read from the token file at build time. If the palette moves, the prose moves with it.</p>
        </div>
      </div>
    </article>
  </div>
</div>"""


def d_landing(p, th, T):
    features = [
        ("Measured, not assumed", "Every contrast figure in this system was computed and re-checked with each channel nudged by one, and the worst of those is the number published.", "chart"),
        ("Two scripts, one system", "Bangla is corrected by a measured multiplier and then held at a 12 px floor, so it never shrinks past the point its মাত্রা survives.", "doc"),
        ("Four themes, one attribute", "Light, dark and both high-contrast themes are chosen with a data-theme attribute on any element, so a dark panel can sit inside a light page.", "gear"),
    ]
    cards = "".join(
        f'<article class="as-card"><p class="as-card__meta">{icon(ic)}</p>'
        f'<h3 class="as-card__title">{e(t)}</h3>'
        f'<p class="as-card__body">{e_mixed(b)}</p></article>'
        for t, b, ic in features
    )
    return f"""
<div class="as-stack as-stack--loose">
  <div class="as-stack">
    <p class="as-card__meta">{bn(BN['wm-1'])}</p>
    <h3 class="as-h2">Software made carefully, for two languages</h3>
    <p class="as-lead as-prose">I build small, careful software. Where something has a limit, the limit is written down here rather than hidden.</p>
    <p class="as-prose" lang="bn">{e(BN['vc-1'])}</p>
    <div class="as-row">
      <a class="as-btn as-btn--primary" href="#">{icon('arrow')}<span>Read the guidebook</span></a>
      <a class="as-btn" href="#">See the tokens</a>
    </div>
  </div>
  <div class="as-grid as-grid--wide">{cards}</div>
  <nav class="as-nav as-nav--horizontal" aria-label="Footer">
    <ul class="as-nav__list">
      <li><a class="as-nav__link" href="#">Cards</a></li>
      <li><a class="as-nav__link" href="#">Tokens</a></li>
      <li><a class="as-nav__link" href="#">Licence</a></li>
    </ul>
  </nav>
</div>"""


def d_pricing(p, th, T):
    plans = [
        ("Reader", "Free", ["Every card", "Every token", "The guidebook"], False),
        ("Studio", "£12 a month", ["Everything in Reader", "The Figma library", "The check harness"], True),
        ("Team", "£40 a month", ["Everything in Studio", "Five people", "A shared token build"], False),
    ]
    out = []
    for name, price, items, featured in plans:
        marker = (
            '<span class="as-badge as-badge--solid as-badge--accent">'
            + icon("dot")
            + "<span>Recommended</span></span>"
            if featured
            else '<span class="as-badge">' + icon("dot") + "<span>Plan</span></span>"
        )
        lis = "".join(f"<li>{icon('check')} {e(i)}</li>" for i in items)
        btn = (
            '<button type="button" class="as-btn as-btn--primary">Choose Studio</button>'
            if featured
            else f'<button type="button" class="as-btn">Choose {e(name)}</button>'
        )
        out.append(
            f'<article class="as-card"><p>{marker}</p>'
            f'<h3 class="as-card__title">{e(name)}</h3>'
            f'<p class="as-h3">{e(price)}</p>'
            f'<ul class="as-doc-list" style="list-style: none; padding-inline-start: 0">{lis}</ul>'
            f'<div class="as-card__foot">{btn}</div></article>'
        )
    return f"""
<div class="as-stack">
  <div class="as-grid as-grid--wide">{''.join(out)}</div>
  <p class="as-hint">The recommended plan is marked with a badge and a word, not with a colour on its own. Prices include tax.</p>
</div>"""


def d_notfound(p, th, T):
    return f"""
<div class="as-stack">
  <div class="as-empty">
    {icon('search', 'as-icon as-empty__glyph')}
    <p class="as-h2">404</p>
    <p class="as-empty__title">That page is not here</p>
    <p class="as-empty__text">The address may have changed, or I may have moved the page. Here is where most people are going instead.</p>
    <div class="as-row" style="justify-content: center">
      <a class="as-btn as-btn--primary" href="#">Go to the card index</a>
      <a class="as-btn" href="#">Search the guidebook</a>
    </div>
  </div>
  <nav class="as-nav as-nav--horizontal" aria-label="Popular pages">
    <ul class="as-nav__list">
      <li><a class="as-nav__link" href="#">{bn(BN['gb-4'])} Colour</a></li>
      <li><a class="as-nav__link" href="#">{bn(BN['gb-5'])} Typography</a></li>
      <li><a class="as-nav__link" href="#">{bn(BN['gb-8'])} Motion</a></li>
    </ul>
  </nav>
</div>"""


def d_validation(p, th, T):
    return f"""
<form class="as-stack">
  <div class="as-alert as-alert--danger" role="alert">
    {icon('cross', 'as-icon as-alert__glyph')}
    <div class="as-alert__body">
      <p class="as-alert__title">Two things need fixing before this can be saved</p>
      <p class="as-alert__text">Nothing has been lost. Both fields are below, and both say what to do.</p>
    </div>
  </div>
  <div class="as-field">
    <label class="as-label" for="{p}-v1">Card name</label>
    <input class="as-input" id="{p}-v1" type="text" value="" aria-invalid="true" aria-describedby="{p}-v1-err">
    <span class="as-error" id="{p}-v1-err">{icon('warn')}<span>A card needs a name. Type one, and it becomes the file name too.</span></span>
  </div>
  <div class="as-field">
    <label class="as-label" for="{p}-v2">Attachment</label>
    <input class="as-input" id="{p}-v2" type="text" value="specimen-18mb.pdf" aria-invalid="true" aria-describedby="{p}-v2-err {p}-v2-bn">
    <span class="as-error" id="{p}-v2-err">{icon('warn')}<span>That file is too large. The maximum is 10 MB, so choose a smaller one.</span></span>
    <span class="as-hint" lang="bn" id="{p}-v2-bn">{e(BN['ms-2'])}</span>
  </div>
  <div class="as-field">
    <label class="as-label" for="{p}-v3">Group</label>
    <span class="as-select-wrap">
      <select class="as-select" id="{p}-v3" aria-describedby="{p}-v3-hint">
        <option>Foundations</option>
        <option selected>Components</option>
        <option>Patterns</option>
      </select>
      <span class="as-select-wrap__arrow">{icon('chevron')}</span>
    </span>
    <span class="as-hint" id="{p}-v3-hint">{icon('check')} This one is fine.</span>
  </div>
  <div class="as-row">
    <button type="submit" class="as-btn as-btn--primary">Save the entry</button>
    <button type="button" class="as-btn">Cancel the change</button>
    <button type="button" class="as-btn as-btn--quiet" lang="bn">{e(BN['bt-4'])}</button>
  </div>
</form>"""


def read_mark(name: str) -> str:
    """The shipped mark, stripped of everything mark_at() sets for itself.

    width and height are stripped too: the 04_mark masters carry them and mark_at
    adds its own, and two of each on one element is a silent, valid-looking way to
    draw the wrong size.
    """
    path = MARKS_DIR / name
    if not path.exists():
        raise BuildError(
            f"{path} is missing. This card draws the shipped mark; run "
            f"04_mark/build.py first. It must never fall back to another folder."
        )
    raw = path.read_text("utf-8")
    raw = re.sub(r'\s*style="color:[^"]*"', "", raw)
    raw = re.sub(r"<title>.*?</title>", "", raw, flags=re.S)
    raw = re.sub(r'\s(?:width|height)="[^"]*"', "", raw, count=2)
    raw = raw.replace('role="img"', "")
    return raw.strip()


def mark_at(svg: str, size: int, accent: bool = False) -> str:
    cls = "as-doc-mark as-doc-mark--accent" if accent else "as-doc-mark"
    out = svg.replace(
        "<svg ",
        f'<svg class="{cls}" width="{size}" height="{size}" role="img" '
        f'aria-label="The Aninda Studio mark" ',
        1,
    )
    return out


# =========================================================================
# The card register
# =========================================================================

CARDS = [
    # ---- Foundations ----
    dict(slug="colour", group="Foundations", name="Colour", name_bn=BN["gb-4"],
         subtitle="Every colour role across four themes, each with the contrast ratio it was measured at and the criterion it was measured against, over the seven surfaces they are measured against.",
         subtitle_bn="", demo=d_colour, wide=True, height=2400,
         extra=lambda T: [("Every role, measured",
                           "Nothing in these tables was typed. Every figure is read from the token files at build time, so the prose cannot drift away from the palette.",
                           colour_tables(T))],
         usage=("markup", '<span class="as-badge as-badge--danger">\n  <svg class="as-icon">…</svg><span>Failed</span>\n</span>\n<!-- The colour is the third signal, never the only one. -->')),
    dict(slug="typography", group="Foundations", name="Typography", name_bn=BN["gb-5"],
         subtitle="One scale of a perfect fourth, two scripts, a measured multiplier for Bangla and a floor it never goes below.",
         subtitle_bn="", demo=d_typography, wide=True, height=1900,
         usage=("markup", '<p lang="bn">অনিন্দ্য স্টুডিও</p>\n<!-- The lang attribute is enough. tokens.css switches the family,\n     applies the multiplier and clamps it at 12px in one declaration. -->')),
    dict(slug="space-and-shape", group="Foundations", name="Space and shape", name_bn=BN["gb-6"],
         subtitle="A 4 px scale in ten steps, and four radii. Everything in the system sits on one of them.",
         subtitle_bn="", demo=d_space, height=1500,
         usage=("markup", '<div class="as-stack">…</div>\n<!-- .as-stack, .as-row and .as-grid all take their gap from the scale. -->')),
    dict(slug="motion", group="Foundations", name="Motion", name_bn=BN["gb-8"],
         subtitle="Two durations and three easing curves. Things that move may overshoot; things that only change colour never do.",
         subtitle_bn="", demo=d_motion, wide=True, height=1500,
         usage=("markup", 'transition: background-color var(--as-duration-colour) var(--as-ease-standard);')),
    dict(slug="the-marks", group="Foundations", name="The marks", name_bn=BN["gb-3"],
         subtitle="The mark in two weights, drawn in currentColor so it takes whatever theme it lands in.",
         subtitle_bn="", demo=d_marks, wide=True, height=1400,
         usage=("markup", '<svg class="as-doc-mark" viewBox="0 0 100 100">…</svg>\n<!-- currentColor throughout. The mark carries no colour of its own. -->')),
    dict(slug="accessibility", group="Foundations", name="Accessibility", name_bn="",
         subtitle="Target sizes with the guidance each one comes from, the anatomy of the focus ring, and what happens in forced colours &mdash; the mode where the operating system replaces every colour with its own.",
         subtitle_bn="", demo=d_a11y, wide=True, height=1700,
         usage=("markup", '<button class="as-btn as-btn--small">Copy the code</button>\n<!-- The small button is never smaller than 24px tall: WCAG 2.2 SC 2.5.8, Level AA. -->')),

    # ---- Components ----
    dict(slug="button", group="Components", name="Button", name_bn="",
         subtitle="Four kinds, two sizes and an icon-only form, each with a label that says what will happen.",
         subtitle_bn="", demo=d_button, height=1500,
         usage=("markup", '<button type="button" class="as-btn as-btn--primary">Save the entry</button>\n<button type="button" class="as-btn">Cancel the change</button>\n<button type="button" class="as-btn as-btn--danger">Delete the file</button>')),
    dict(slug="input", group="Components", name="Input", name_bn="",
         subtitle="A label, an optional hint, and an error that says what happened and then what to do next.",
         subtitle_bn="", demo=d_input, height=1500,
         usage=("markup", '<div class="as-field">\n  <label class="as-label" for="size">File size</label>\n  <input class="as-input" id="size" aria-invalid="true"\n         aria-describedby="size-hint size-err">\n  <span class="as-hint" id="size-hint">…</span>\n  <span class="as-error" id="size-err">…</span>\n</div>\n<!-- A hint is described-by too, not only an error. Without it the words are\n     next to the field for a sighted reader and absent for a screen reader. -->')),
    dict(slug="select", group="Components", name="Select", name_bn="",
         subtitle="A native select with a drawn arrow, so the arrow follows the theme instead of the operating system.",
         subtitle_bn="", demo=d_select, height=1300,
         usage=("markup", '<div class="as-field">\n  <label class="as-label" for="plan">Plan</label>\n  <span class="as-select-wrap">\n    <select class="as-select" id="plan" aria-describedby="plan-hint">…</select>\n    <span class="as-select-wrap__arrow"><svg class="as-icon">…</svg></span>\n  </span>\n  <span class="as-hint" id="plan-hint">…</span>\n</div>')),
    dict(slug="checkbox-radio", group="Components", name="Checkbox and radio", name_bn="",
         subtitle="Native controls at 24 px, wrapped in a label so the words are part of the target.",
         subtitle_bn="", demo=d_choice, height=1500,
         usage=("markup", '<label class="as-choice" for="c1">\n  <input class="as-choice__control" id="c1" type="checkbox">\n  <span class="as-choice__text"><span class="as-choice__label">…</span></span>\n</label>')),
    dict(slug="textarea", group="Components", name="Textarea", name_bn="",
         subtitle="You can drag it taller but never wider, so the line length stays comfortable to read.",
         subtitle_bn="", demo=d_textarea, height=1300,
         usage=("markup", '<textarea class="as-textarea" rows="4"></textarea>\n/* resize: vertical — the width is a layout decision, not the reader\'s. */')),
    dict(slug="badge", group="Components", name="Badge", name_bn="",
         subtitle="Five meanings, each carrying a glyph and a word so the colour is the third signal and never the only one.",
         subtitle_bn="", demo=d_badge, height=1200,
         usage=("markup", '<span class="as-badge as-badge--danger">\n  <svg class="as-icon">…</svg><span>Failed</span>\n</span>')),
    dict(slug="card", group="Components", name="Card", name_bn="",
         subtitle="A surface a step brighter than the page, with a shadow in the light theme and none in the dark ones.",
         subtitle_bn="", demo=d_card, wide=True, height=1200,
         usage=("markup", '<article class="as-card">\n  <p class="as-card__meta">Foundation</p>\n  <h3 class="as-card__title">Colour</h3>\n  <p class="as-card__body">…</p>\n</article>')),
    dict(slug="alert", group="Components", name="Alert", name_bn="",
         subtitle="Four kinds. Each says what happened, then what happens next, and never blames the reader.",
         subtitle_bn="", demo=d_alert, wide=True, height=1600,
         usage=("markup", '<div class="as-alert as-alert--danger" role="alert">\n  <svg class="as-icon as-alert__glyph">…</svg>\n  <div class="as-alert__body">\n    <p class="as-alert__title">Couldn\'t save the entry</p>\n    <p class="as-alert__text">Your work is still here. Try again in a moment.</p>\n  </div>\n</div>')),
    dict(slug="dialog", group="Components", name="Dialog", name_bn="",
         subtitle="A real dialog element over a dimmed backdrop, with the destructive action named rather than called OK.",
         subtitle_bn="", demo=d_dialog, wide=True, height=1200,
         usage=("markup", '<dialog class="as-dialog" open aria-labelledby="t">…</dialog>\n<!-- In a product this opens with showModal(), which traps focus\n     and adds the ::backdrop. The card shows it open in place. -->')),
    dict(slug="table", group="Components", name="Table", name_bn="",
         subtitle="Row headers, a caption saying what the numbers are, and a sideways scroll when the table is wider than the space.",
         subtitle_bn="", demo=d_table, wide=True, height=1200,
         usage=("markup", '<div class="as-scroll-x">\n  <table class="as-table as-table--numeric">\n    <caption>…</caption>\n    <thead><tr><th scope="col">Card</th>…</tr></thead>\n  </table>\n</div>')),
    dict(slug="tabs", group="Components", name="Tabs", name_bn="",
         subtitle="The selected tab is bold, underlined and marked with aria-selected. Three signals, one of which is a colour.",
         subtitle_bn="", demo=d_tabs, height=1200,
         usage=("markup", '<div class="as-tabs" role="tablist" aria-label="Card groups">\n'
                          '  <button class="as-tab" role="tab" id="t1" aria-selected="true"\n'
                          '          aria-controls="p1">Foundations</button>\n'
                          '  <button class="as-tab" role="tab" id="t2" aria-selected="false"\n'
                          '          aria-controls="p2" tabindex="-1">Components</button>\n'
                          '</div>\n'
                          '<div class="as-tabpanel" role="tabpanel" id="p1" aria-labelledby="t1">…</div>\n'
                          '<div class="as-tabpanel" role="tabpanel" id="p2" aria-labelledby="t2" hidden>…</div>\n'
                          '<!-- Every panel has to be in the document, and the arrow keys have to\n'
                          '     move the selection. tabindex="-1" without them takes the tab off\n'
                          '     the keyboard entirely. -->')),
    dict(slug="nav", group="Components", name="Nav", name_bn="",
         subtitle="Vertical and horizontal. The current item carries a bar, a heavier weight and aria-current.",
         subtitle_bn="", demo=d_nav, wide=True, height=1200,
         usage=("markup", '<nav class="as-nav" aria-label="Foundations">\n  <ul class="as-nav__list">\n    <li><a class="as-nav__link" href="#" aria-current="page">Colour</a></li>\n  </ul>\n</nav>')),
    dict(slug="breadcrumb", group="Components", name="Breadcrumb", name_bn="",
         subtitle="The last item is not a link, because you are already on it.",
         subtitle_bn="", demo=d_breadcrumb, height=1000,
         usage=("markup", '<nav class="as-breadcrumb" aria-label="Breadcrumb">\n  <ol class="as-breadcrumb__list">…\n    <li><span class="as-breadcrumb__current" aria-current="page">Breadcrumb</span></li>\n  </ol>\n</nav>')),
    dict(slug="toast", group="Components", name="Toast", name_bn="",
         subtitle="A short message with a dismiss button that has a name of its own, not only a cross.",
         subtitle_bn="", demo=d_toast, wide=True, height=1200,
         usage=("markup", '<div class="as-toast as-toast--success" role="status">\n  …\n  <button class="as-toast__dismiss" aria-label="Dismiss this message">…</button>\n</div>')),
    dict(slug="empty-state", group="Components", name="Empty state", name_bn="",
         subtitle="Says what is missing, and then exactly what to do about it.",
         subtitle_bn="", demo=d_empty, wide=True, height=1300,
         usage=("markup", '<div class="as-empty">\n  <svg class="as-icon as-empty__glyph">…</svg>\n  <p class="as-empty__title">Nothing here yet</p>\n  <p class="as-empty__text">Add your first entry to begin.</p>\n</div>')),
    dict(slug="code-block", group="Components", name="Code block", name_bn="",
         subtitle="Aninda Mono, a horizontal scroll rather than a wrap, and a copy button that says what it copies.",
         subtitle_bn="", demo=d_code, wide=True, height=1100,
         usage=("markup", '<div class="as-code">\n  <div class="as-code__head">…</div>\n  <pre class="as-code__pre"><code>…</code></pre>\n</div>')),

    # ---- Patterns ----
    dict(slug="sign-in", group="Patterns", name="Sign in", name_bn="",
         subtitle="One card, two fields, and an option for someone who has no password.",
         subtitle_bn="", demo=d_signin, wide=True, height=1500),
    dict(slug="settings", group="Patterns", name="Settings", name_bn="",
         subtitle="Grouped in fieldsets, with the destructive action kept apart and named.",
         subtitle_bn="", demo=d_settings, wide=True, height=1900),
    dict(slug="dashboard", group="Patterns", name="Dashboard", name_bn="",
         subtitle="Four figures, one table, and a note saying where the numbers came from.",
         subtitle_bn="", demo=d_dashboard, wide=True, height=1900),
    dict(slug="docs-page", group="Patterns", name="Docs page", name_bn="",
         subtitle="Breadcrumb, page navigation and prose held to a readable line length.",
         subtitle_bn="", demo=d_docs, wide=True, height=1900),
    dict(slug="landing", group="Patterns", name="Landing", name_bn="",
         subtitle="A claim, the reason to believe it, and two ways forward.",
         subtitle_bn="", demo=d_landing, wide=True, height=1900),
    dict(slug="pricing", group="Patterns", name="Pricing", name_bn="",
         subtitle="Three plans, with the recommended one marked by a badge and a word.",
         subtitle_bn="", demo=d_pricing, wide=True, height=1600),
    dict(slug="not-found", group="Patterns", name="Not found", name_bn="",
         subtitle="Says the page is missing, then offers the pages most people were looking for.",
         subtitle_bn="", demo=d_notfound, wide=True, height=1300),
    dict(slug="form-with-validation", group="Patterns", name="Form with validation", name_bn="",
         subtitle="A summary at the top, an error under each field, and nothing lost.",
         subtitle_bn="", demo=d_validation, wide=True, height=1700),
]

# --- Bangla, filled in from the verified string file ------------------------
# The card list above was written before 06_type/bangla-strings.json existed, so
# it carries empty strings wherever no approved Bangla was available at the time.
# Rather than edit 30 entries by hand and risk one of them drifting from the
# approved wording, the names and subtitles are filled in from that file here.
#
# It is the single source for approved Bangla: every string in it carries the
# rule number or dictionary page it rests on. Nothing is invented at this step —
# a card with no entry keeps its English, and says so in the gap list below.
_BN_STRINGS = ROOT / "06_type" / "bangla-strings.json"
if _BN_STRINGS.exists():
    _bn = json.loads(_BN_STRINGS.read_text(encoding="utf-8"))
    for _card in CARDS:
        for _field in ("name", "subtitle"):
            _entry = _bn.get(f"card.{_card['slug']}.{_field}")
            if _entry and _entry.get("bn"):
                _card[f"{_field}_bn"] = _entry["bn"]

    # The theme labels, for the same reason. THEMES above carried "" for the two
    # high-contrast labels, so 60 of the 120 theme buttons across the 30 cards were
    # monolingual next to 60 that were bilingual — and the gap was declared nowhere,
    # because _bangla_gaps covers card names and subtitles only. The register holds
    # both compounds with a cited basis: verified th-3 joined to verified th-1 or
    # th-2 with the same comma the English label uses.
    for _index, (_key, _label, _label_bn) in enumerate(THEMES):
        _entry = _bn.get(f"theme.{_key}")
        if _entry and _entry.get("bn"):
            if _entry.get("en") and _entry["en"] != _label:
                raise BuildError(
                    f"theme.{_key} in 06_type/bangla-strings.json is keyed to the "
                    f"English label {_entry['en']!r} and this file writes "
                    f"{_label!r}. The approved Bangla was joined to match that "
                    f"exact wording, so the two must not differ."
                )
            THEMES[_index] = (_key, _label, _entry["bn"])

GROUP_DIR = {"Foundations": "foundations", "Components": "components", "Patterns": "patterns"}


# =========================================================================
# Page assembly
# =========================================================================


def theme_switcher() -> str:
    buttons = ['<button type="button" class="as-doc-theme" data-set-theme="" aria-pressed="true">Follow the system</button>']
    for key, label, label_bn in THEMES:
        text = e(label) + ((" " + bn(label_bn)) if label_bn else "")
        buttons.append(
            f'<button type="button" class="as-doc-theme" data-set-theme="{key}" aria-pressed="false">{text}</button>'
        )
    return (
        '<div class="as-doc-themes" role="group" aria-label="Choose a theme for this page">'
        + "".join(buttons)
        + "</div>"
    )


SWITCHER_JS = """
(function () {
  var root = document.documentElement;
  var buttons = document.querySelectorAll('[data-set-theme]');
  function apply(value) {
    if (value === '') { root.removeAttribute('data-theme'); }
    else { root.setAttribute('data-theme', value); }
    for (var i = 0; i < buttons.length; i++) {
      var own = buttons[i].getAttribute('data-set-theme');
      buttons[i].setAttribute('aria-pressed', own === value ? 'true' : 'false');
    }
  }
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function (event) {
      apply(event.currentTarget.getAttribute('data-set-theme'));
    });
  }
  document.addEventListener('click', function (event) {
    var target = event.target;
    var anchor = target && target.closest ? target.closest('a[href="#"]') : null;
    if (anchor) { event.preventDefault(); }
  });
  document.addEventListener('submit', function (event) { event.preventDefault(); });

  // The copy button. It had no listener at all: a control whose name is a promise
  // and whose behaviour is nothing, announced identically to one that works, and
  // it matters most to the keyboard-only reader for whom it is the only offered
  // route to the code. Confirmed dead with a clipboard sentinel — the sentinel
  // survived the click.
  //
  // Both outcomes are announced through a live region, because a copy that
  // silently fails is the same defect one step along. navigator.clipboard is not
  // available on a file:// page in Chromium, so the execCommand path is the one
  // that actually runs for a reader who opened the card from disk; it is tried
  // second so a served page gets the modern API.
  var copies = document.querySelectorAll('.as-code__head .as-btn');
  for (var c = 0; c < copies.length; c++) {
    copies[c].addEventListener('click', function (event) {
      var head = event.currentTarget.parentNode;
      var block = head.parentNode;
      var pre = block.querySelector('.as-code__pre');
      var say = block.querySelector('.as-code__said');
      var code = pre ? pre.textContent : '';
      function said(message) { if (say) { say.textContent = message; } }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(
          function () { said('Copied.'); },
          function () { legacy(); }
        );
        return;
      }
      legacy();
      function legacy() {
        var area = document.createElement('textarea');
        area.value = code;
        area.setAttribute('readonly', 'readonly');
        area.style.position = 'fixed';
        area.style.opacity = '0';
        document.body.appendChild(area);
        area.select();
        var ok = false;
        try { ok = document.execCommand('copy'); } catch (error) { ok = false; }
        document.body.removeChild(area);
        said(ok ? 'Copied.' : 'Copying did not work. Select the code and copy it.');
      }
    });
  }

  // The other half of the ARIA tabs pattern. A roving tabindex takes every
  // unselected tab out of the tab sequence, so without this the tabs card shipped
  // ten visible buttons no key could reach. Click, arrow keys, Home and End all
  // move the selection, and the panels are shown and hidden to match.
  var lists = document.querySelectorAll('[role="tablist"]');
  for (var l = 0; l < lists.length; l++) {
    (function (list) {
      var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
      if (tabs.length < 2) { return; }
      function select(index, moveFocus) {
        for (var i = 0; i < tabs.length; i++) {
          var on = i === index;
          tabs[i].setAttribute('aria-selected', on ? 'true' : 'false');
          if (on) { tabs[i].removeAttribute('tabindex'); }
          else { tabs[i].setAttribute('tabindex', '-1'); }
          var panel = document.getElementById(tabs[i].getAttribute('aria-controls'));
          if (panel) {
            if (on) { panel.removeAttribute('hidden'); }
            else { panel.setAttribute('hidden', ''); }
          }
        }
        if (moveFocus) { tabs[index].focus(); }
      }
      for (var i = 0; i < tabs.length; i++) {
        (function (index) {
          tabs[index].addEventListener('click', function () { select(index, true); });
        })(i);
      }
      list.addEventListener('keydown', function (event) {
        var current = tabs.indexOf(document.activeElement);
        if (current < 0) { return; }
        var next = -1;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
          next = (current + 1) % tabs.length;
        } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
          next = (current - 1 + tabs.length) % tabs.length;
        } else if (event.key === 'Home') {
          next = 0;
        } else if (event.key === 'End') {
          next = tabs.length - 1;
        }
        if (next >= 0) { event.preventDefault(); select(next, true); }
      });
    })(lists[l]);
  }
})();
""".strip()


def build_page(card: dict, tokens_css: str, components_css: str, faces_css: str, T: dict) -> str:
    group = card["group"]
    demo = card["demo"]
    quad_class = "as-doc-quad as-doc-quad--wide" if card.get("wide") else "as-doc-quad"

    slug = card["slug"]
    panels = []
    for key, label, label_bn in THEMES:
        label_html = e(label) + ((" " + bn(label_bn)) if label_bn else "")
        body = demo(f"{slug}-{key}", key, T)
        # role="group" with aria-labelledby, so the panel has a NAME. Without it
        # every card put four or five copies of each control into one flat
        # accessibility tree with nothing to tell them apart: sign-in.html offered
        # five fields called "Email address", dialog.html five buttons called
        # "Delete the file". Reading the page linearly recovers which theme each
        # belongs to, because the label sits above it; tabbing does not, and the
        # label was in an unnamed div. The name is the label already on the page.
        panels.append(
            f'<div class="as-doc-panel" data-theme="{key}" role="group" '
            f'aria-labelledby="{slug}-{key}-label">'
            f'<p class="as-doc-panel__label" id="{slug}-{key}-label">'
            f'<span>{label_html}</span>'
            f'<code>data-theme="{key}"</code></p>'
            f"{body}</div>"
        )

    extra_html = ""
    for title, note, body in (card.get("extra", lambda _T: [])(T)):
        extra_html += (
            '<section class="as-doc-section">'
            f'<h2 class="as-doc-section__title">{e(title)}</h2>'
            f'<p class="as-doc-section__note">{e(note)}</p>'
            f"{body}</section>"
        )

    usage_html = ""
    if card.get("usage"):
        name, body = card["usage"]
        usage_html = (
            '<section class="as-doc-section">'
            '<h2 class="as-doc-section__title">How to write it</h2>'
            '<p class="as-doc-section__note">The classes carry the design decisions. '
            "The markup carries the meaning, and no class can supply that for you.</p>"
            f"{code_block(name, body)}</section>"
        )

    title_bn = f'<p class="as-doc-title-bn as-bn-large" lang="bn">{e(card["name_bn"])}</p>' if card["name_bn"] else ""
    sub_bn = f'<p class="as-doc-sub-bn" lang="bn">{e(card["subtitle_bn"])}</p>' if card["subtitle_bn"] else ""

    is_foundation = group == "Foundations"
    stage_heading = "The foundation" if is_foundation else ("The pattern" if group == "Patterns" else "The component")

    parts = [
        f'<!-- @dsCard group="{group}" -->',
        f"<!-- GENERATED FILE. Written by {GENERATOR} from 07_tokens/css/tokens.css and "
        "08_components/src/components.css. Do not hand-edit: the next build overwrites it, "
        "and build.py --check fails on any difference. -->",
        "<!doctype html>",
        '<html lang="en" class="as-root">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{e(card['name'])} — Aninda Studio</title>",
        f'<meta name="generator" content="{GENERATOR}">',
        "<style>",
        f"/* GENERATED FILE. Written by {GENERATOR}. Do not hand-edit — the next build overwrites it. */",
        "/* >>> begin 07_tokens/css/tokens.css (generated; the only place a literal colour is allowed) */",
        tokens_css.strip(),
        TOKENS_CSS_END,
        "/* >>> begin 08_components/src/components.css */",
        components_css.strip(),
        "/* <<< end 08_components/src/components.css */",
        faces_css,
        "</style>",
        "</head>",
        '<body class="as-doc-page">',
        '<header class="as-doc-head">',
        f'<p class="as-doc-eyebrow">{e(group)}</p>',
        f'<h1 class="as-doc-title">{e(card["name"])}</h1>',
        title_bn,
        f'<p class="as-doc-sub">{e(card["subtitle"])}</p>',
        sub_bn,
        theme_switcher(),
        "</header>",
        '<main class="as-stack as-stack--loose">',
        '<section class="as-doc-section">',
        f'<h2 class="as-doc-section__title">{e(stage_heading)}</h2>',
        '<p class="as-doc-section__note">Shown in whichever theme the buttons above have chosen. '
        "With none chosen, it follows the reader's system setting, including a request for more contrast.</p>",
        '<div class="as-doc-stage">',
        demo(f"{card['slug']}-stage", None, T),
        "</div>",
        "</section>",
        '<section class="as-doc-section">',
        '<h2 class="as-doc-section__title">All four themes at once</h2>',
        '<p class="as-doc-section__note">Each panel pins its own theme with a data-theme attribute. '
        "That is why a dark panel can sit inside a light page: the themes are scoped to an element, "
        "not to the document root.</p>",
        f'<div class="{quad_class}">',
        "".join(panels),
        "</div>",
        "</section>",
        extra_html,
        usage_html,
        "</main>",
        '<footer class="as-doc-foot">',
        f"<p>Generated by {e(GENERATOR)} from 07_tokens/css/tokens.css and "
        "08_components/src/components.css. Do not hand-edit this file. "
        "Fonts are subset and inlined; this card needs no network.</p>",
        "<p>Literata and Noto Serif Bengali are used under SIL OFL 1.1 under their own names. "
        "The monospace face is a subset of IBM Plex Mono, renamed to Aninda Mono because "
        "&ldquo;Plex&rdquo; is a Reserved Font Name — the single word, which is why the whole "
        "IBM Plex superfamily is covered — and subsetting is a modification under "
        "clause 3 of that licence. Each OFL.txt sits beside the subset in 08_components/fonts/.</p>",
        "</footer>",
        f"<script>{SWITCHER_JS}</script>",
        "</body>",
        "</html>",
        "",
    ]
    return "\n".join(parts)


# =========================================================================
# Build
# =========================================================================


def build() -> dict[str, bytes]:
    if not TOKENS_CSS.exists():
        raise BuildError(f"Token file not found: {TOKENS_CSS}")
    tokens_css = TOKENS_CSS.read_text("utf-8")
    components_css = COMPONENTS_CSS.read_text("utf-8")
    guard_stylesheet(components_css, "src/components.css")

    T = load_tokens()
    faces_css = font_face_css({})

    slugs = [c["slug"] for c in CARDS]
    if len(set(slugs)) != len(slugs):
        raise BuildError("Two cards share a slug.")

    pages: dict[str, str] = {}
    for card in CARDS:
        rel = f"cards/{GROUP_DIR[card['group']]}/{card['slug']}.html"
        pages[rel] = build_page(card, tokens_css, components_css, faces_css, T)

    # The character set is the union of everything the pages contain. Deterministic,
    # and it cannot miss a glyph the way a hand-written list can.
    charset = set()
    for text in pages.values():
        charset |= set(text)

    # Plus the Bangla the Claude Code plugin ships, because the plugin bundles
    # these same three subsets as assets/fonts/*.woff2 and renders its approved
    # strings with them. Subsetting to the cards alone left the plugin unable to
    # draw ঠ in কণ্ঠস্বর — one of its own approved strings — and ২ and ৫ in the
    # Bangla Academy edition years it cites as its authority, so those came out as
    # tofu boxes from the skill's own font. The union is the honest boundary: every
    # character any consumer of these files is told it may use.
    for extra in (PLUGIN_BANGLA_JSON, PLUGIN_BANGLA_MD):
        if not extra.exists():
            raise BuildError(
                f"{extra} is missing. The subset fonts are built to cover the "
                f"Bangla the Claude Code plugin ships, so that file has to be here."
            )
        charset |= set(extra.read_text(encoding="utf-8"))

    # Plus the shaping test set from the type research. 06_type/review_bangla.py
    # shows those conjuncts and words in the shipped face, so the shipped face has
    # to contain them — ঞ, in জ্ঞ, was absent, so the one row of the review sheet
    # whose job is to prove the conjuncts shape could not draw one of them.
    if not MEASUREMENTS_JSON.exists():
        raise BuildError(
            f"{MEASUREMENTS_JSON} is missing. The subsets cover the shaping test "
            f"set, and that is where it is recorded."
        )
    _shaping = json.loads(MEASUREMENTS_JSON.read_text(encoding="utf-8"))["shaping"]
    for _face in _shaping.values():
        charset |= set("".join(_face.get("conjuncts", {})))
        charset |= set("".join(w.get("text", "")
                               for w in _face.get("words", {}).values()))

    chars = "".join(sorted(charset))

    fonts: dict[str, bytes] = {}
    encoded: dict[str, str] = {}
    for key in ("latin", "bangla", "mono"):
        data = build_font(key, chars)
        fonts[key] = data
        encoded[key] = base64.b64encode(data).decode("ascii")

    out: dict[str, bytes] = {}
    for rel, text in pages.items():
        for key, blob in encoded.items():
            text = text.replace(PLACEHOLDER.format(key.upper()), blob)
        if PLACEHOLDER.split("{")[0] in text:
            raise BuildError(f"{rel}: a font placeholder was left unfilled.")

        lines = text.split("\n")
        group = next(c["group"] for c in CARDS if rel.endswith(f"/{c['slug']}.html"))
        expected = f'<!-- @dsCard group="{group}" -->'
        if lines[0] != expected:
            raise BuildError(f"{rel}: line 1 is {lines[0]!r}, not {expected!r}.")

        # partition returns ('whole', '', '') when the separator is absent, so a
        # cosmetic edit to this comment used to turn the markup guard into a
        # complete no-op with no error at all: `rest` became the empty string and
        # guard_markup inspected nothing. Round 1 of the convergence review proved
        # it by renaming the marker and shipping style="fill: #ff0000" past a
        # clean --check. The separator is now asserted before it is trusted.
        head, marker, rest = text.partition(TOKENS_CSS_END)
        if marker != TOKENS_CSS_END:
            raise BuildError(
                f"{rel}: the marker {TOKENS_CSS_END!r} is not in the page, so the markup "
                "guard would have nothing to inspect. It is emitted by build_page; if it "
                "was renamed there, rename it here too."
            )
        guard_markup(rest, rel)
        out[rel] = text.encode("utf-8")

    # WCAG 2.2 SC 3.1.2, over every card. Run on the whole page rather than on
    # `rest`, because the language of a run depends on the lang attributes of its
    # ancestors and <html lang="en"> is in the head.
    guard_language_of_parts({rel: data.decode("utf-8")
                             for rel, data in out.items() if rel.endswith(".html")})
    guard_field_descriptions({rel: data.decode("utf-8")
                             for rel, data in out.items() if rel.endswith(".html")})

    for key in ("latin", "bangla", "mono"):
        spec = FONT_SOURCES[key]
        out[f"fonts/{spec['out']}"] = fonts[key]
        out[f"fonts/{spec['ofl_out']}"] = spec["ofl"].read_bytes()
    out[f"fonts/{DESKTOP_FONT_OUT}"] = desktop_font()

    out["_cards.json"] = registry_bytes(fonts)
    return out


def desktop_font_row() -> list[dict]:
    """The desktop TTF, if it is on disk — the fourth OFL artefact this kit ships.

    The licence chapter said "Three faces ship with this system, each as a
    subset", and a fourth sat in the same directory: AnindaMono-Regular.ttf, the
    whole IBM Plex Mono renamed but NOT subset, and the largest single
    redistributed font in the tree. The OFL obligations were met — the licence
    file sits beside it and the rename is what clause 3 requires — but the file
    was named on no licence surface, and it is the one a reader is most likely to
    install or pass on. An inventory a reader is told is complete has to be.

    Generated rather than typed, so it appears the moment the file does and
    disappears if the desktop build is dropped.
    """
    path = FONTS_DIR / DESKTOP_FONT_OUT
    if not path.exists():
        return []
    return [{
        "file": f"fonts/{DESKTOP_FONT_OUT}",
        "family": "Aninda Mono (desktop)",
        "source": str(FONT_SOURCES["mono"]["path"].relative_to(ROOT)),
        "licence": "SIL OFL 1.1",
        "licence_file": f"fonts/{FONT_SOURCES['mono']['ofl_out']}",
        "bytes": path.stat().st_size,
        "renamed": True,
        "subset": False,
    }]


def registry_bytes(fonts: dict[str, bytes]) -> bytes:
    entries = []
    for card in CARDS:
        entries.append({
            "path": f"cards/{GROUP_DIR[card['group']]}/{card['slug']}.html",
            "name": card["name"],
            "name_bn": card["name_bn"],
            "group": card["group"],
            "subtitle": card["subtitle"],
            "subtitle_bn": card["subtitle_bn"],
            "width": 1280,
            "height": card["height"],
        })
    payload = {
        "_generator": GENERATOR,
        "_warning": "GENERATED FILE. Do not hand-edit — the next build overwrites it.",
        "_note": (
            "width and height are the declared design canvas for a card, not a measured "
            "render height. The cards are fluid; check.py measures them at 360, 768 and "
            "1280 CSS px."
        ),
        "_bangla_gaps": bangla_gaps(),
        "_fonts": [
            {
                "file": f"fonts/{FONT_SOURCES[k]['out']}",
                "family": FONT_SOURCES[k]["family"],
                "source": str(FONT_SOURCES[k]["path"].relative_to(ROOT)),
                "licence": "SIL OFL 1.1",
                "licence_file": f"fonts/{FONT_SOURCES[k]['ofl_out']}",
                "bytes": len(fonts[k]),
                "renamed": bool(FONT_SOURCES[k]["rename"]),
            }
            for k in ("latin", "bangla", "mono")
        ] + desktop_font_row(),
        "counts": {
            g: sum(1 for c in CARDS if c["group"] == g)
            for g in ("Foundations", "Components", "Patterns")
        },
        "cards": entries,
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    try:
        artefacts = build()
    except BuildError as exc:
        print(f"BUILD FAILED\n{exc}", file=sys.stderr)
        return 1

    if check_only:
        problems = []
        for rel, data in sorted(artefacts.items()):
            path = HERE / rel
            if not path.exists():
                problems.append(f"missing: {rel}")
            elif path.read_bytes() != data:
                problems.append(f"differs: {rel}")
        on_disk = set()
        for path in sorted(CARDS_DIR.rglob("*.html")):
            on_disk.add(str(path.relative_to(HERE)))
        extra = on_disk - set(artefacts)
        for rel in sorted(extra):
            problems.append(f"unexpected: {rel}")
        if problems:
            print("DRIFT\n  " + "\n  ".join(problems), file=sys.stderr)
            return 1
        print(f"No drift. {len(artefacts)} files match.")
        return 0

    for rel, data in sorted(artefacts.items()):
        path = HERE / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    known = set(artefacts)
    for path in sorted(CARDS_DIR.rglob("*.html")):
        rel = str(path.relative_to(HERE))
        if rel not in known:
            path.unlink()

    cards = [r for r in artefacts if r.startswith("cards/")]
    total = sum(len(v) for k, v in artefacts.items() if k.startswith("cards/"))
    print(f"Wrote {len(cards)} cards, {total / 1_000_000:.1f} MB total.")
    for key in ("latin", "bangla", "mono"):
        spec = FONT_SOURCES[key]
        size = len(artefacts[f"fonts/{spec['out']}"])
        print(f"  {spec['family']:<20} {size / 1024:6.1f} KB subset")
    gaps = bangla_gaps()
    print(f"Bangla left in English because neither 06_type/BANGLA-STANDARD.md nor "
          f"06_type/bangla-strings.json holds an approved string: "
          f"{len(gaps['name_bn'])} card names, {len(gaps['subtitle_bn'])} subtitles. "
          "The slugs are listed under _bangla_gaps in _cards.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
