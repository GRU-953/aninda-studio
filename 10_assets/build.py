#!/usr/bin/env python3
"""Aninda Studio — the raster asset set, generator.

This script is the ONLY writer of 10_assets/. Nothing here is hand-drawn and
nothing here should be hand-edited: the next run overwrites it.

    export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
    ./.venv/bin/python 10_assets/build.py

How the pixels are made
    Every raster comes out of the same Chromium that a reader will view the site
    in, driven by Playwright. The source is always an SVG from 04_mark/svg/ — no
    artwork is redrawn here. Pillow packs the multi-size .ico and then MEASURES
    each PNG back off disk.

The one geometry fact that governs everything
    The everyday icon is ROUNDED and its corners are transparent. Anything that
    must be opaque therefore needs a ground drawn behind it. Assuming a square
    would leave four transparent corners on the Apple touch icon, which renders
    as black on some surfaces and white on others. Each asset below declares
    `opaque` explicitly and the check refuses to write a file whose alpha does
    not match what it declared.

Icon policy
    04_mark/manifest.json records the owner's decision of 26 August 2026, which
    reversed the decision of 14 August: each platform's own icon geometry is
    followed. This folder holds the WEB set only — the rounded tile and the
    favicons — because a browser will not round a favicon for you. The Apple and
    Android masters are square and unmasked by design and are delivered by the
    store packages, not rendered here.

Colour
    Not one colour is typed in this file. Grounds are var(--as-…) resolved from
    07_tokens/css/tokens.css, which is inlined into every render page. The mark
    SVGs carry their own values, and those were written by 04_mark/build.py.

Sizes
    Two classes, and the difference is recorded per file in MANIFEST.json:
      * long-stable  — favicon, PWA, Apple touch, Open Graph, GitHub preview.
      * verified     — checked against the platform's own help page on the date
                       in MANIFEST.json, with the URL and the quote it came from.
    Anything that could not be verified is marked unverified rather than guessed.

Exit codes
    0  written and measured
    1  a guard failed — nothing is written
    2  could not run — a tool is missing

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import base64
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

TOKENS_CSS = ROOT / "07_tokens" / "css" / "tokens.css"
MARK_DIR = ROOT / "04_mark" / "svg"
MARK_MANIFEST = ROOT / "04_mark" / "manifest.json"
FONTS_DIR = ROOT / "08_components" / "fonts"

GENERATOR = "10_assets/build.py"
BUILT_ON = "2026-08-14"
DO_NOT_EDIT = (
    "GENERATED FILE. Written by " + GENERATOR + ". Do not hand-edit — the next "
    "build overwrites it."
)

# Playwright looks in a shared cache outside this folder unless it is told
# otherwise, and then reports the browser as missing. Setting it here as well as
# in the shell means the failure cannot happen quietly.
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(ROOT / "00_sandbox" / "browsers"))

try:
    from PIL import Image
except ImportError:  # every guard below reads pixels, so this is not optional
    Image = None


class BuildError(Exception):
    pass


# =========================================================================
# The verified figures
# -------------------------------------------------------------------------
# Checked on 14 August 2026 against each platform's OWN help documentation.
# No third-party "image size" article was used for any number here. The quote
# is short and attributed so the figure can be traced without trusting me.
# =========================================================================

VERIFIED = {
    "x-header": {
        "spec": "X header photo, 1500 x 500 px",
        "url": "https://help.x.com/en/managing-your-account/how-to-customize-your-profile",
        "quote": "recommended dimensions are 1500x500 pixels",
        "note": (
            "X states that about 60 px at the top and 60 px at the bottom can be "
            "cropped, depending on the monitor and the browser. Everything in this "
            "image is kept clear of both bands."
        ),
    },
    "x-profile-photo": {
        "spec": "X profile photo, 400 x 400 px, under 2 MB",
        "url": "https://help.x.com/en/managing-your-account/how-to-customize-your-profile",
        "quote": "recommended dimensions are 400x400 pixels",
        "note": "X crops the profile photo to a circle, so the ground is drawn full bleed.",
    },
    "linkedin-personal-banner": {
        "spec": "LinkedIn profile cover image, 1584 x 396 px, under 8 MB",
        "url": "https://www.linkedin.com/help/linkedin/answer/a566232",
        "quote": "1584 (w) x 396 (h) pixels (recommended)",
        "note": (
            "LinkedIn has renamed this slot: the current help article calls it the "
            "cover image, not the background photo. The figure is unchanged."
        ),
    },
    "linkedin-company-cover": {
        "spec": "LinkedIn Page cover image, 4200 x 700 px, under 3 MB",
        "url": (
            "https://www.linkedin.com/help/linkedin/answer/a563309/"
            "image-specifications-for-your-linkedin-pages-and-career-pages"
        ),
        "quote": "4200 (w) x 700 (h) pixels",
        "note": (
            "LinkedIn gives the same figure as both the minimum and the recommended "
            "size. It also asks for key details to be kept away from the edges and "
            "especially the lower-right corner, so the content sits left of centre."
        ),
    },
    "linkedin-company-logo": {
        "spec": "LinkedIn Page logo, 400 x 400 px recommended (268 x 268 minimum), under 3 MB",
        "url": (
            "https://www.linkedin.com/help/linkedin/answer/a563309/"
            "image-specifications-for-your-linkedin-pages-and-career-pages"
        ),
        "quote": "268 (w) x 268 (h) pixels | 400 (w) x 400 (h) pixels",
        "note": "400 x 400 is the recommended figure and is what is written here.",
    },
}

STABLE_NOTE = (
    "Long-stable size. It has been the same for years across browsers and "
    "platforms and is not tied to one company's current help page."
)


# =========================================================================
# SVG handling — lxml, so the source artwork is never edited by string search
# =========================================================================


def load_svg(name: str):
    from lxml import etree

    path = MARK_DIR / name
    if not path.exists():
        raise BuildError(f"Mark not found: {path}. Run 04_mark/build.py first.")
    return etree.fromstring(path.read_bytes())


def svg_to_text(node) -> str:
    from lxml import etree

    return etree.tostring(node, encoding="unicode")


def fill_box(node):
    """Make the SVG fill whatever box CSS gives it. viewBox stays, so the
    drawing scales rather than being cropped."""
    node.set("width", "100%")
    node.set("height", "100%")
    return node


def free_height(node):
    """Drop the fixed width and height so CSS can set one and the browser works
    the other out from the viewBox. Also drop the inline `color`, so the drawing
    inherits the theme colour from its parent instead of carrying its own."""
    for attribute in ("width", "height"):
        if attribute in node.attrib:
            del node.attrib[attribute]
    if "style" in node.attrib:
        del node.attrib["style"]
    return node


def drop_ground(node):
    """Remove the rounded background rectangle. Used for the maskable icon,
    where the platform supplies the shape and the ground must be full bleed."""
    for child in list(node):
        if child.tag.endswith("}rect") or child.tag == "rect":
            node.remove(child)
    return node


def scale_about_centre(node, factor: float, grid: float = 100.0):
    """Wrap everything but the title in one more transform, scaled about the
    centre of the grid. This is how the maskable icon gets its safe zone."""
    from lxml import etree

    mid = grid / 2.0
    group = etree.Element("g")
    group.set(
        "transform",
        f"translate({mid},{mid}) scale({factor:.6f}) translate({-mid},{-mid})",
    )
    for child in list(node):
        if child.tag.endswith("}title") or child.tag == "title":
            continue
        node.remove(child)
        group.append(child)
    node.append(group)
    return node


# =========================================================================
# Fonts — the tagline is real text, so the face has to travel with the page
# =========================================================================


def font_face_block() -> str:
    """Literata only. The names are drawn from the wordmark SVGs, which are real
    outlines, so no Bangla face is needed to render an image here."""
    path = FONTS_DIR / "literata-subset.woff2"
    if not path.exists():
        raise BuildError(f"Font not found: {path}. Run 08_components/build.py first.")
    blob = base64.b64encode(path.read_bytes()).decode("ascii")
    return (
        "@font-face{font-family:\"Literata\";font-style:normal;font-weight:400 700;"
        "font-display:block;src:url(data:font/woff2;base64," + blob + ") format(\"woff2\");}"
    )


def guard_glyphs(strings: list[str]) -> None:
    """The subset in 08_components/fonts/ carries only what the card library
    asked for. A character outside it would fall back to whatever face the
    machine happens to have, and the image would differ between machines. So
    check, and fail closed rather than render something unrepeatable."""
    from fontTools.ttLib import TTFont

    covered = set(TTFont(FONTS_DIR / "literata-subset.woff2").getBestCmap())
    missing = sorted({ch for text in strings for ch in text if ord(ch) not in covered})
    if missing:
        raise BuildError(
            "Literata's subset does not carry: "
            + " ".join(f"{ch!r} (U+{ord(ch):04X})" for ch in missing)
            + ". Either change the wording or re-subset in 08_components/build.py."
        )


# =========================================================================
# The pages that get screenshotted
# =========================================================================


def page_shell(theme: str, body: str, extra_css: str = "", with_font: bool = False) -> str:
    tokens = TOKENS_CSS.read_text("utf-8")
    face = font_face_block() if with_font else ""
    return (
        "<!doctype html>\n"
        f"<!-- {DO_NOT_EDIT} This page is rendered, never saved. -->\n"
        f'<html lang="en" data-theme="{theme}"><head><meta charset="utf-8">'
        "<style>\n" + tokens + "\n" + face + "\n"
        "html,body{margin:0;padding:0;height:100%;width:100%;background-color:transparent;}\n"
        "*{box-sizing:border-box;}\n"
        ".ground{position:absolute;inset:0;overflow:hidden;}\n"
        ".fill{position:absolute;inset:0;display:block;}\n"
        + extra_css
        + "\n</style></head><body>" + body + "</body></html>"
    )


def icon_page(source: str, opaque: bool, maskable: bool = False, safe: float = 0.80) -> str:
    """One rounded icon, filling the frame. When `opaque` is set the ground is
    drawn behind it, because the corners of this artwork are transparent."""
    node = fill_box(load_svg(source))
    if maskable:
        node = drop_ground(node)
        # 04_mark/manifest.json records the mark's worst corner at 45.0 of the
        # 100-unit grid's centre, that is a radius of 45. The maskable safe zone
        # is a circle of 80% of the icon, a radius of 40. 40/45 is the exact
        # factor that brings the worst corner onto the safe circle.
        node = scale_about_centre(node, (safe * 100.0 / 2.0) / 45.0)
    ground = '<div class="ground" style="background-color:var(--as-ink)"></div>' if opaque else ""
    return page_shell(
        "light",
        ground + '<div class="fill">' + svg_to_text(node) + "</div>",
        ".fill svg{display:block;width:100%;height:100%;}",
    )


TAGLINE = "Small, careful software."
SITE_URL = "anindastudio.com"
STRAPLINE = "Design tokens, components and marks. Measured, not assumed."


def banner_page(layout: dict) -> str:
    """A wide image: the icon, both wordmarks, one line of English and the
    address. Everything sits on an opaque ground taken from the theme."""
    icon = fill_box(load_svg("icon-512.svg"))
    latin = free_height(load_svg("wordmark-latin.svg"))
    bangla = free_height(load_svg("wordmark-bangla.svg"))

    lines = [
        f'<p class="tagline">{TAGLINE}</p>',
        f'<p class="strap">{STRAPLINE}</p>' if layout.get("strapline") else "",
        f'<p class="url">{SITE_URL}</p>' if layout.get("url") else "",
    ]
    body = (
        '<div class="ground" style="background-color:var(--as-surface-lowest)">'
        '<div class="frame">'
        '<div class="icon">' + svg_to_text(icon) + "</div>"
        '<div class="words">'
        '<div class="mark-latin">' + svg_to_text(latin) + "</div>"
        '<div class="mark-bangla" lang="bn">' + svg_to_text(bangla) + "</div>"
        + "".join(lines) +
        "</div></div></div>"
    )
    css = f"""
.frame{{position:absolute;inset:0;display:flex;align-items:center;
  justify-content:{layout['justify']};gap:{layout['gap']}px;
  padding:{layout['pad_block']}px {layout['pad_inline_end']}px {layout['pad_block']}px {layout['pad_inline']}px;}}
.icon{{flex:none;width:{layout['icon']}px;height:{layout['icon']}px;}}
.icon svg{{display:block;width:100%;height:100%;}}
.words{{display:flex;flex-direction:column;gap:{layout['stack']}px;min-width:0;color:var(--as-ink);}}
.mark-latin svg{{display:block;height:{layout['latin']}px;width:auto;color:var(--as-ink);}}
.mark-bangla svg{{display:block;height:{layout['bangla']}px;width:auto;color:var(--as-ink-muted);}}
p{{margin:0;font-family:Literata,serif;color:var(--as-ink);}}
.tagline{{font-size:{layout['tagline']}px;line-height:1.3;font-weight:600;}}
.strap{{font-size:{layout['strap']}px;line-height:1.4;font-weight:400;color:var(--as-ink-muted);}}
.url{{font-size:{layout['url']}px;line-height:1.3;font-weight:400;color:var(--as-ink-muted);}}
"""
    return page_shell(layout["theme"], body, css, with_font=True)


# =========================================================================
# The asset list
# =========================================================================


def banner(theme: str, icon: int, latin: int, bangla: int, tagline: int,
           strap: int = 0, url: int = 0, pad_block: int = 0, pad_inline: int = 0,
           pad_inline_end: int = 0, gap: int = 0, stack: int = 0,
           justify: str = "center") -> dict:
    return {
        "theme": theme, "icon": icon, "latin": latin, "bangla": bangla,
        "tagline": tagline, "strap": strap, "url": url,
        "strapline": strap > 0, "url_line": url > 0,
        "pad_block": pad_block, "pad_inline": pad_inline,
        "pad_inline_end": pad_inline_end or pad_inline,
        "gap": gap, "stack": stack, "justify": justify,
    }


def stroke_rule() -> dict:
    """The mark's stroke rule, read from 04_mark/manifest.json rather than typed.

    The manifest carries `switch_px` and a per-file stroke measured off the
    artwork, so this file can ask which artefact carries which weight instead of
    naming one and hoping.
    """
    if not MARK_MANIFEST.exists():
        raise BuildError(f"{MARK_MANIFEST} is missing. Run 04_mark/build.py first.")
    strokes = json.loads(MARK_MANIFEST.read_text("utf-8"))["strokes"]
    for key in ("regular", "heavy", "switch_px", "stroke_by_file"):
        if key not in strokes:
            raise BuildError(
                f"04_mark/manifest.json's strokes block has no {key!r}. This build "
                f"reads the stroke rule from there so it cannot be retyped here."
            )
    return strokes


def icon_source(size: int, above: str) -> str:
    """Which mark artefact a raster of this size must be rendered from.

    THE ONE PLACE THE HEAVY WEIGHT IS ACTUALLY NEEDED WAS THE ONE PLACE IT WAS NOT
    USED. Every favicon here was rendered from icon-192.svg, which carries the
    regular stroke of 9 units. At 16 px that is 9/100 x 0.9208 x 16 = 1.33 px, and
    measured in the shipped file only one of its three pixels reached near full
    value. The manifest, chapter 03 of the guidebook and asset.py all state that
    the regular weight may not be used below 24 px — asset.py refuses to make it,
    with exit 2 — and 10_assets shipped it anyway, in favicon-16.png and in the
    16 px plane of favicon.ico.

    tile-web.svg is the same construction at the heavy weight: same rounded
    rectangle, same rx, the mark scaled a little smaller to give the thicker
    stroke its clearance. The plugin's icons.md has named it "the web tile and
    favicon source" all along, while nothing in 10_assets referenced it.
    """
    strokes = stroke_rule()
    if size >= strokes["switch_px"]:
        return above
    heavy = [name for name, width in strokes["stroke_by_file"].items()
             if width == strokes["heavy"] and name.startswith(("tile", "icon"))]
    if not heavy:
        raise BuildError(
            f"nothing in 04_mark/svg carries the heavy stroke "
            f"({strokes['heavy']:g}) as a rounded icon, so a {size} px favicon "
            f"cannot be rendered without breaking the stroke rule."
        )
    return sorted(heavy)[0]


def guard_stroke_rule(items: list[dict]) -> None:
    """Prove the stroke rule on every icon raster, from the artwork it came from.

    guard_mark_size in asset.py applies the rule to the standalone mark only, so
    make_icon and make_tile scaled the same artwork to any size above the 16 px
    floor with no stroke check at all. This is the missing half: it reads the
    stroke width out of the source SVG for every raster about to be rendered and
    compares it against the size that raster is declared at.
    """
    strokes = stroke_rule()
    problems = []
    for item in items:
        if item["render"][0] != "icon":
            continue
        source = item["render"][1]
        actual = strokes["stroke_by_file"].get(source)
        if actual is None:
            problems.append(f"{item['name']}: 04_mark/manifest.json records no "
                            f"stroke for {source}")
            continue
        wanted = (strokes["regular"] if min(item["w"], item["h"]) >= strokes["switch_px"]
                  else strokes["heavy"])
        if actual != wanted:
            problems.append(
                f"{item['name']} is {item['w']}x{item['h']} px and is rendered from "
                f"{source}, whose stroke is {actual:g}. The rule is "
                f"\"{strokes['rule']}\", so it needs {wanted:g}."
            )
    if problems:
        raise BuildError("The stroke rule failed:\n  " + "\n  ".join(problems))


def asset_list() -> list[dict]:
    ico_pngs = [16, 32, 48]
    items: list[dict] = []

    for size in (16, 32, 48, 96):
        source = icon_source(size, "icon-192.svg")
        items.append({
            "name": f"favicon-{size}.png", "w": size, "h": size, "opaque": False,
            "render": ("icon", source, False, False),
            "purpose": f"Browser tab and bookmark icon at {size} px.",
            "spec": "PNG favicon, 16/32/48/96 px",
            "verified": "stable", "note": STABLE_NOTE,
            "in_ico": size in ico_pngs,
        })

    items += [
        {
            "name": "apple-touch-icon.png", "w": 180, "h": 180, "opaque": True,
            "render": ("icon", "icon-192.svg", True, False),
            "purpose": "Home-screen icon on iOS and iPadOS. Opaque, because iOS "
                       "composites no ground of its own behind it.",
            "spec": "apple-touch-icon, 180 x 180 px, opaque",
            "verified": "stable", "note": STABLE_NOTE,
        },
        {
            "name": "icon-192.png", "w": 192, "h": 192, "opaque": False,
            "render": ("icon", "icon-192.svg", False, False),
            "purpose": "Installed web app icon, purpose \"any\".",
            "spec": "Web app manifest icon, 192 x 192 px",
            "verified": "stable", "note": STABLE_NOTE,
        },
        {
            "name": "icon-512.png", "w": 512, "h": 512, "opaque": False,
            "render": ("icon", "icon-512.svg", False, False),
            "purpose": "Installed web app icon and splash artwork, purpose \"any\".",
            "spec": "Web app manifest icon, 512 x 512 px",
            "verified": "stable", "note": STABLE_NOTE,
        },
        {
            "name": "icon-maskable-512.png", "w": 512, "h": 512, "opaque": True,
            "render": ("icon", "icon-512.svg", True, True),
            "purpose": "Installed web app icon, purpose \"maskable\". The ground is "
                       "full bleed and every drawn pixel sits inside the central "
                       "80%, so any shape the platform masks to keeps the mark whole.",
            "spec": "Maskable icon, 512 x 512 px, content within the central 80%",
            "verified": "stable", "note": STABLE_NOTE,
        },
        {
            "name": "avatar-512.png", "w": 512, "h": 512, "opaque": True,
            "render": ("icon", "icon-512.svg", True, False),
            "purpose": "General profile picture. Opaque, because most services "
                       "flatten an avatar onto their own background.",
            "spec": "Square avatar, 512 x 512 px",
            "verified": "stable", "note": STABLE_NOTE,
        },
        {
            "name": "x-profile-photo.png", "w": 400, "h": 400, "opaque": True,
            "render": ("icon", "icon-512.svg", True, False),
            "purpose": "Profile photo on X.",
            "spec": VERIFIED["x-profile-photo"]["spec"],
            "verified": "verified", "source": VERIFIED["x-profile-photo"],
        },
        {
            "name": "linkedin-company-logo.png", "w": 400, "h": 400, "opaque": True,
            "render": ("icon", "icon-512.svg", True, False),
            "purpose": "Logo on a LinkedIn Page.",
            "spec": VERIFIED["linkedin-company-logo"]["spec"],
            "verified": "verified", "source": VERIFIED["linkedin-company-logo"],
        },
        {
            "name": "og-image.png", "w": 1200, "h": 630, "opaque": True,
            "render": ("banner", banner(
                "dark", icon=132, latin=76, bangla=54, tagline=34, url=25,
                pad_block=72, pad_inline=88, gap=56, stack=18)),
            "purpose": "Open Graph image, and the X large summary card. One image "
                       "serves both; they take the same shape.",
            "spec": "Open Graph / X summary_large_image, 1200 x 630 px",
            "verified": "stable", "note": STABLE_NOTE,
        },
        {
            "name": "github-social-preview.png", "w": 1280, "h": 640, "opaque": True,
            "render": ("banner", banner(
                "dark", icon=136, latin=78, bangla=56, tagline=35, url=26,
                pad_block=76, pad_inline=92, gap=58, stack=18)),
            "purpose": "Repository social preview on GitHub.",
            "spec": "GitHub repository social preview, 1280 x 640 px",
            "verified": "stable", "note": STABLE_NOTE,
        },
        {
            "name": "x-header.png", "w": 1500, "h": 500, "opaque": True,
            "render": ("banner", banner(
                "dark", icon=104, latin=58, bangla=42, tagline=26, url=20,
                pad_block=96, pad_inline=96, gap=48, stack=12)),
            "purpose": "Header image on an X profile. Everything is kept 96 px "
                       "clear of the top and bottom, past the 60 px X says it may crop.",
            "spec": VERIFIED["x-header"]["spec"],
            "verified": "verified", "source": VERIFIED["x-header"],
        },
        {
            "name": "linkedin-personal-banner.png", "w": 1584, "h": 396, "opaque": True,
            "render": ("banner", banner(
                "dark", icon=96, latin=54, bangla=38, tagline=24, url=18,
                pad_block=56, pad_inline=96, gap=44, stack=10)),
            "purpose": "Cover image on a personal LinkedIn profile.",
            "spec": VERIFIED["linkedin-personal-banner"]["spec"],
            "verified": "verified", "source": VERIFIED["linkedin-personal-banner"],
        },
        {
            "name": "linkedin-company-cover.png", "w": 4200, "h": 700, "opaque": True,
            "render": ("banner", banner(
                "dark", icon=168, latin=96, bangla=68, tagline=44, url=32,
                pad_block=120, pad_inline=260, pad_inline_end=1700, gap=76, stack=20,
                justify="flex-start")),
            "purpose": "Cover image on a LinkedIn Page. The content is held to the "
                       "left half, because LinkedIn asks for key details to be kept "
                       "away from the edges and the lower-right corner in particular.",
            "spec": VERIFIED["linkedin-company-cover"]["spec"],
            "verified": "verified", "source": VERIFIED["linkedin-company-cover"],
        },
        {
            "name": "README-header-light.png", "w": 1280, "h": 320, "opaque": True,
            "render": ("banner", banner(
                "light", icon=124, latin=62, bangla=44, tagline=28, strap=20,
                pad_block=52, pad_inline=72, gap=48, stack=12)),
            "purpose": "Header image for a README, shown to readers using the light theme.",
            "spec": "No platform publishes a size for this. 1280 x 320 was chosen "
                    "because GitHub renders README content at about 880 CSS px wide, "
                    "so this is close to two device pixels per CSS pixel.",
            "verified": "unverified",
            "note": "UNVERIFIED: this size is a house decision, not a published spec.",
        },
        {
            "name": "README-header-dark.png", "w": 1280, "h": 320, "opaque": True,
            "render": ("banner", banner(
                "dark", icon=124, latin=62, bangla=44, tagline=28, strap=20,
                pad_block=52, pad_inline=72, gap=48, stack=12)),
            "purpose": "Header image for a README, shown to readers using the dark theme.",
            "spec": "No platform publishes a size for this. 1280 x 320 was chosen "
                    "because GitHub renders README content at about 880 CSS px wide, "
                    "so this is close to two device pixels per CSS pixel.",
            "verified": "unverified",
            "note": "UNVERIFIED: this size is a house decision, not a published spec.",
        },
    ]
    return items


# =========================================================================
# Rendering and measuring
# =========================================================================


def stamp(png: bytes, name: str) -> bytes:
    """A PNG cannot open with a comment the way a text file can, so the header
    goes into tEXt chunks instead. `Software` and `Comment` are both standard
    keywords and every image tool shows them."""
    import io

    from PIL import PngImagePlugin

    image = Image.open(io.BytesIO(png))
    info = PngImagePlugin.PngInfo()
    info.add_text("Software", GENERATOR)
    info.add_text("Comment", DO_NOT_EDIT)
    info.add_text("Title", f"Aninda Studio — {name}")
    # The sRGB chunk, added 26 August 2026. Benchmark criterion 7 asks that icon
    # masters be authored in sRGB, and its 19 August verdict was "no P3 asset exists
    # anywhere, so none is offered for visionOS — but none of the exported rasters
    # carries an embedded profile, so sRGB is implicit rather than declared".
    #
    # This declares it. Be precise about what that means: it states which colour
    # space these numbers are in. It does not claim the renderer produced sRGB
    # values, and no Display P3 asset exists here, so no P3 claim is made for any
    # platform. 0 is the perceptual rendering intent.
    info.add(b"sRGB", b"\x00")
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True, pnginfo=info)
    return out.getvalue()


def measure(png: bytes, item: dict) -> None:
    """Read the file back and check it against what it said it would be. A
    render that silently came out square, or opaque when it should be clear, is
    exactly the failure this catches."""
    import io

    image = Image.open(io.BytesIO(png)).convert("RGBA")
    if image.size != (item["w"], item["h"]):
        raise BuildError(
            f"{item['name']}: rendered {image.size[0]}x{image.size[1]}, "
            f"declared {item['w']}x{item['h']}."
        )
    alpha = image.getchannel("A")
    low, high = alpha.getextrema()

    if item["opaque"]:
        if low < 255:
            raise BuildError(
                f"{item['name']}: declared opaque but the least opaque pixel is "
                f"alpha {low}. The rounded icon's corners are transparent, so a "
                "ground has to be drawn behind it."
            )
    else:
        if high < 255:
            raise BuildError(f"{item['name']}: nothing in it is opaque at all.")
        corner = image.getpixel((0, 0))
        if corner[3] != 0:
            raise BuildError(
                f"{item['name']}: declared transparent-cornered but pixel (0, 0) "
                f"has alpha {corner[3]}."
            )

    if "maskable" in item["name"]:
        check_maskable(image, item)


def check_maskable(image, item: dict) -> None:
    """Measure, do not assume. Find every pixel that differs from the ground and
    check the furthest one is inside the safe circle — a radius of 40% of the
    icon, centred."""
    ground = image.getpixel((0, 0))
    width, height = image.size
    centre_x, centre_y = (width - 1) / 2.0, (height - 1) / 2.0
    limit = 0.40 * width
    pixels = image.load()
    worst = 0.0
    worst_at = (0, 0)
    for y in range(height):
        for x in range(width):
            p = pixels[x, y]
            if abs(p[0] - ground[0]) + abs(p[1] - ground[1]) + abs(p[2] - ground[2]) < 24:
                continue
            distance = ((x - centre_x) ** 2 + (y - centre_y) ** 2) ** 0.5
            if distance > worst:
                worst, worst_at = distance, (x, y)
    if worst == 0.0:
        raise BuildError(f"{item['name']}: nothing is drawn on the ground at all.")
    if worst > limit:
        raise BuildError(
            f"{item['name']}: a drawn pixel sits {worst:.1f} px from the centre at "
            f"{worst_at}, outside the {limit:.0f} px safe radius (the central 80%)."
        )
    item["measured_safe_radius"] = round(worst, 1)
    item["safe_radius_limit"] = round(limit, 1)


def pack_ico(pngs: dict[int, bytes]) -> bytes:
    """One .ico holding 16, 32 and 48, each rendered at its own size rather than
    resampled down from one big one."""
    import io

    sizes = sorted(pngs)
    # The base image has to be the LARGEST: Pillow skips any requested size
    # bigger than the image it was handed. The other two are passed alongside and
    # matched by exact size, so each entry is the render made at that size rather
    # than a resample of the 48.
    images = [Image.open(io.BytesIO(pngs[s])).convert("RGBA") for s in reversed(sizes)]
    out = io.BytesIO()
    images[0].save(
        out, format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:],
    )
    data = out.getvalue()

    # Read it back. Pillow will happily write one entry if append_images is not
    # honoured, and a favicon that lost two of its three sizes still opens.
    check = Image.open(io.BytesIO(data))
    got = sorted(check.ico.sizes()) if hasattr(check, "ico") else []
    want = sorted((s, s) for s in sizes)
    if got != want:
        raise BuildError(f"favicon.ico holds {got}, not {want}.")
    return data


def build_svg_icon() -> bytes:
    """icon.svg — the scalable favicon, with its fixed width and height removed so
    it scales to whatever the browser asks for.

    It is rendered from the HEAVY artwork, for the same reason the 16 px PNG is.
    This file is declared as `rel="icon"` with no `sizes`, and the surfaces a
    browser draws that on — the tab strip, the bookmark bar, the history list —
    are 16 to 20 px. Every size above the switch already has its own declared
    file: favicon.ico at 32, apple-touch-icon at 180, the manifest icons at 192
    and 512. So the size this one is actually drawn at is below the switch, and
    the asymmetry decides it: the heavy weight at 48 px is a slightly bolder mark,
    while the regular weight at 16 px thins away, which is the failure the rule
    was written for.
    """
    node = load_svg(icon_source(16, "icon-1024.svg"))
    for attribute in ("width", "height"):
        if attribute in node.attrib:
            del node.attrib[attribute]
    for child in node:
        if child.tag.endswith("}title") or child.tag == "title":
            child.text = "Aninda Studio"
    text = (
        f"<!-- {DO_NOT_EDIT} -->\n"
        f"<!-- Source: 04_mark/svg/{icon_source(16, 'icon-1024.svg')}, "
        f"written by 04_mark/build.py. -->\n"
        + svg_to_text(node)
        + "\n"
    )
    return text.encode("utf-8")


def _ink_geometry(data: bytes) -> tuple:
    """Ink coverage and bounding box, measured at FULL resolution in C.

    The first version sampled on a stride of about a two-hundredth of each axis, and
    that stride was the whole problem: on a 1280 px image it steps 5 px, so a
    one-pixel antialiasing shift changes WHICH pixels get looked at, and the box moved
    by a hundredth between macOS and Ubuntu. CI caught it on README-header-dark.png.

    Now every pixel is compared, using PIL's own C paths, so the only remaining
    difference is genuine edge antialiasing — which moves a box edge by at most a
    pixel, or 0.002 of a 512 px frame, comfortably inside two decimal places.
    """
    from PIL import Image, ImageChops
    import io as _io
    im = Image.open(_io.BytesIO(data)).convert("RGBA")
    w, h = im.size
    corner = im.getpixel((0, 0))
    flat = Image.new("RGBA", im.size, corner)
    # Per-channel absolute difference, flattened to one band, then thresholded.
    diff = ImageChops.difference(im, flat).convert("L")
    mask = diff.point(lambda v: 255 if v > 24 else 0)
    counts = mask.histogram()
    inked = counts[255]
    coverage = round(inked / float(w * h), 3)
    box = mask.getbbox()
    if not box:
        return (w, h, 0.0, None)
    frame = (round(box[0] / w, 2), round(box[1] / h, 2),
             round(box[2] / w, 2), round(box[3] / h, 2))
    return (w, h, coverage, frame)


def _ico_planes(raw: bytes):
    """Every plane inside an .ico, measured the way the PNGs are measured.

    Returns {(w, h): _ink_geometry(...)} or None when the bytes are not an icon at
    all. Pillow reads an .ico as a multi-size container; each plane is extracted and
    put through the same ink-geometry comparison, because an .ico is a raster and
    two rasterisers do not agree byte for byte.
    """
    import io as _io
    if Image is None:
        return None
    try:
        with Image.open(_io.BytesIO(raw)) as ico:
            sizes = list(ico.ico.sizes()) if hasattr(ico, "ico") else [ico.size]
            planes = {}
            for size in sizes:
                frame = ico.ico.getimage(size) if hasattr(ico, "ico") else ico
                buf = _io.BytesIO()
                frame.convert("RGBA").save(buf, format="PNG")
                planes[tuple(size)] = _ink_geometry(buf.getvalue())
            return planes
    except Exception:
        return None


def _structural_check(out: dict) -> list[str]:
    import json as _json
    problems: list[str] = []
    known = set(out)
    for path in sorted(HERE.iterdir()):
        if path.name in ("build.py", "__pycache__") or path.name.startswith("."):
            continue
        if path.is_file() and path.name not in known:
            problems.append(f"not generated by this build: {path.name}")

    for name, data in sorted(out.items()):
        path = HERE / name
        if not path.exists():
            problems.append(f"missing: {name}")
            continue
        on_disk = path.read_bytes()
        if name.endswith(".svg"):
            if on_disk != data:
                problems.append(f"differs (text, so this is real): {name}")
        elif name == "MANIFEST.json":
            def strip(raw):
                doc = _json.loads(raw)
                for entry in doc.get("files", []):
                    entry.pop("bytes", None)
                return doc
            if strip(on_disk) != strip(data):
                problems.append("differs (ignoring the per-file byte sizes, which a "
                                "rasteriser changes): MANIFEST.json")
        elif name.endswith(".ico"):
            # The .ico fell through every branch above, so the only thing checked
            # about it was that a file existed. Replacing it with 26 bytes of text
            # left this reporting "21 asset files match the source". It is a
            # container of PNG planes, so it gets the same rasteriser-tolerant
            # comparison the PNGs get, plane by plane, plus its size list.
            want_planes, got_planes = _ico_planes(data), _ico_planes(on_disk)
            if want_planes is None or got_planes is None:
                problems.append(f"{name}: could not be read as an icon container")
            elif sorted(want_planes) != sorted(got_planes):
                problems.append(f"{name}: holds sizes {sorted(got_planes)} on disk, "
                                f"{sorted(want_planes)} from the marks")
            else:
                for size in sorted(want_planes):
                    want, got = want_planes[size], got_planes[size]
                    if (abs(want[2] - got[2]) > 0.01
                            or want[3] is None or got[3] is None
                            or max(abs(a - b) for a, b in zip(want[3], got[3])) > 0.02):
                        problems.append(
                            f"{name} at {size[0]}x{size[1]}: the artwork has moved — "
                            f"ink coverage {got[2]} and box {got[3]} on disk against "
                            f"{want[2]} and {want[3]} from the marks")
        elif name.endswith(".png"):
            want, got = _ink_geometry(data), _ink_geometry(on_disk)
            if want[:2] != got[:2]:
                problems.append(f"{name}: {got[0]}x{got[1]} on disk, "
                                f"{want[0]}x{want[1]} from the marks")
            elif (abs(want[2] - got[2]) > 0.01
                  or want[3] is None or got[3] is None
                  or max(abs(a - b) for a, b in zip(want[3], got[3])) > 0.02):
                problems.append(
                    f"{name}: the artwork has moved — ink coverage {got[2]} and box "
                    f"{got[3]} on disk against {want[2]} and {want[3]} from the marks")
    return problems


def run(check_only: bool = False) -> int:
    if Image is None:
        print("NOT EQUIPPED: Pillow is not importable.", file=sys.stderr)
        return 2
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("NOT EQUIPPED: playwright is not importable.", file=sys.stderr)
        return 2
    if not TOKENS_CSS.exists():
        print(f"NOT EQUIPPED: {TOKENS_CSS} is missing.", file=sys.stderr)
        return 2

    guard_glyphs([TAGLINE, SITE_URL, STRAPLINE])
    items = asset_list()
    guard_stroke_rule(items)

    out: dict[str, bytes] = {}
    try:
        pw = sync_playwright().start()
    except Exception as exc:
        print(f"NOT EQUIPPED: playwright would not start — {exc}", file=sys.stderr)
        return 2
    try:
        try:
            browser = pw.chromium.launch()
        except Exception as exc:
            print(
                "NOT EQUIPPED: Chromium would not launch. Did you export "
                f"PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers ?\n  {exc}",
                file=sys.stderr,
            )
            return 2

        for item in items:
            kind = item["render"][0]
            if kind == "icon":
                _, source, opaque, maskable = item["render"]
                html = icon_page(source, opaque, maskable)
            else:
                html = banner_page(item["render"][1])

            context = browser.new_context(
                viewport={"width": item["w"], "height": item["h"]},
                device_scale_factor=1,
            )
            page = context.new_page()
            failures: list[str] = []
            page.on("pageerror", lambda e: failures.append(str(e)))
            page.on("requestfailed", lambda r: failures.append(f"{r.url} — {r.failure}"))
            page.set_content(html, wait_until="load")
            page.wait_for_timeout(60)
            png = page.screenshot(omit_background=not item["opaque"])
            context.close()
            if failures:
                raise BuildError(f"{item['name']}: the render page reported {failures}")

            png = stamp(png, item["name"])
            measure(png, item)
            out[item["name"]] = png
            item["bytes"] = len(png)

        browser.close()
    finally:
        pw.stop()

    ico_sources = {
        int(i["name"].split("-")[1].split(".")[0]): out[i["name"]]
        for i in items if i.get("in_ico")
    }
    if sorted(ico_sources) != [16, 32, 48]:
        raise BuildError(f"favicon.ico wants 16, 32 and 48; it was offered {sorted(ico_sources)}.")
    out["favicon.ico"] = pack_ico(ico_sources)
    out["icon.svg"] = build_svg_icon()

    manifest = build_manifest(items, out)
    out["MANIFEST.json"] = manifest

    # --check compares and writes nothing. Twenty rasters, an .ico and a manifest
    # were regenerated and diffed nowhere: this build had no --check mode at all, so
    # nothing in CI or in scripts/verify-all.sh could notice a hand-edited asset or
    # a mark change that never reached the icons.
    if check_only:
        # STRUCTURAL, not byte for byte, and the reason is measured. These rasters are
        # rendered by a browser, and a browser does not rasterise identically across
        # platforms: the committed files are made on macOS, and on Ubuntu in CI all
        # twenty differ, along with MANIFEST.json, whose per-file `bytes` field records
        # the PNG sizes. On one machine the render IS deterministic — built twice, the
        # same sha256 both times — so a byte gate is meaningful locally and impossible
        # in CI. That is the same wall 09_guidebook/scripts/pdf.py hit.
        #
        # So this compares what a rasteriser cannot change and a mark change cannot
        # hide: the declared file set, each image's dimensions and opacity, and the
        # GEOMETRY of its ink — coverage to three decimal places and the bounding box
        # of every non-background pixel. Antialiasing moves neither. Redrawing the mark
        # moves both. The SVG and the manifest are still compared byte for byte with
        # the manifest's `bytes` field excluded, because both are text.
        problems = _structural_check(out)
        if problems:
            raise BuildError("dist has drifted from the marks and tokens:\n  "
                             + "\n  ".join(problems))
        print(f"--check: {len(out)} asset files match the source. Nothing written.")
        return 0

    HERE.mkdir(parents=True, exist_ok=True)
    for name, data in sorted(out.items()):
        (HERE / name).write_bytes(data)

    known = set(out)
    for path in sorted(HERE.iterdir()):
        if path.name in ("build.py", "__pycache__") or path.name.startswith("."):
            continue
        if path.is_file() and path.name not in known:
            path.unlink()

    total = sum(len(v) for v in out.values())
    print(f"Wrote {len(out)} files, {total / 1_000_000:.2f} MB total, into 10_assets/")
    for name in sorted(out):
        print(f"  {name:<34} {len(out[name]) / 1024:8.1f} KB")
    verified = [i["name"] for i in items if i["verified"] == "verified"]
    unverified = [i["name"] for i in items if i["verified"] == "unverified"]
    print(f"\nVerified against the platform's own help page on {BUILT_ON}: {len(verified)}")
    for name in verified:
        print(f"  · {name}")
    print(f"Could NOT be verified against any published spec: {len(unverified)}")
    for name in unverified:
        print(f"  · {name}")
    print("\nThe Apple and Android masters are not rendered here. This folder is "
          "the web set; those are store assets — see 04_mark/manifest.json.")
    print("favicon.ico carries no text header: the ICO container has no field for "
          "one. Its provenance is in MANIFEST.json.")
    return 0


def build_manifest(items: list[dict], out: dict[str, bytes]) -> bytes:
    files = []
    for item in items:
        entry = {
            "name": item["name"],
            "size": f"{item['w']}x{item['h']}",
            "width": item["w"],
            "height": item["h"],
            "bytes": item["bytes"],
            "opaque": item["opaque"],
            "purpose": item["purpose"],
            "spec": item["spec"],
            "verification": item["verified"],
        }
        # Which artwork this raster came from, and at what stroke. Recorded because
        # every favicon here was rendered from the regular-weight icon-192.svg
        # while three documents said the regular weight may not be used below
        # 24 px, and nothing in the shipped output said which file it came from.
        if item["render"][0] == "icon":
            entry["rendered_from"] = item["render"][1]
            entry["stroke"] = stroke_rule()["stroke_by_file"].get(item["render"][1])
        if item["verified"] == "verified":
            source = item["source"]
            entry["verified_on"] = BUILT_ON
            entry["verified_against"] = source["url"]
            entry["verified_quote"] = source["quote"]
            entry["note"] = source["note"]
        else:
            entry["verified_on"] = None
            entry["note"] = item.get("note", "")
        if "measured_safe_radius" in item:
            entry["measured_safe_radius_px"] = item["measured_safe_radius"]
            entry["safe_radius_limit_px"] = item["safe_radius_limit"]
        files.append(entry)

    files.append({
        "name": "favicon.ico",
        "size": "16x16, 32x32, 48x48",
        "width": None, "height": None,
        "bytes": len(out["favicon.ico"]),
        "opaque": False,
        "purpose": "The classic favicon, for browsers and tools that ask for "
                   "/favicon.ico. Each of the three sizes is rendered at its own "
                   "size rather than resampled from one large image.",
        "spec": "Multi-size ICO, 16 + 32 + 48",
        "verification": "stable",
        "verified_on": None,
        "note": "The ICO container has no text field, so this file carries no "
                "generator header. Its provenance is this manifest. " + STABLE_NOTE,
    })
    files.append({
        "name": "icon.svg",
        "size": "scalable",
        "width": None, "height": None,
        "bytes": len(out["icon.svg"]),
        "opaque": False,
        "purpose": "The scalable favicon, linked as rel=\"icon\" type=\"image/svg+xml\". "
                   "Browsers that support it use this at any size.",
        "spec": "SVG favicon, scalable",
        "verification": "stable",
        "verified_on": None,
        "note": STABLE_NOTE,
    })

    mark_policy = json.loads(MARK_MANIFEST.read_text("utf-8"))["icon_policy"]
    payload = {
        "_generator": GENERATOR,
        "_warning": DO_NOT_EDIT,
        "built_on": BUILT_ON,
        "source_artwork": "04_mark/svg/, written by 04_mark/build.py",
        "renderer": "Chromium via Playwright, device_scale_factor 1",
        "colour": "No colour is typed in the generator. Every ground is a "
                  "var(--as-…) resolved from 07_tokens/css/tokens.css.",
        "icon_policy": {
            "decision": mark_policy["decision"],
            "reason": mark_policy["reason"],
            "surfaces": mark_policy["surfaces"],
            "used_here": ("The web set only. The Apple and Android masters are "
                          "delivered by the store packages rather than rendered "
                          "into this folder, because they are not web assets."),
        },
        "transparency": "The web icon is rounded and its corners are "
                        "transparent. Every file marked opaque has a ground drawn "
                        "behind it, and the build measures the alpha channel to "
                        "prove it rather than trusting the CSS.",
        "verification_key": {
            "verified": "Checked against the platform's own help page on the date "
                        "given, with the URL and the sentence it came from.",
            "stable": STABLE_NOTE,
            "unverified": "No platform publishes a size for this. The figure is a "
                          "house decision and is named as one.",
        },
        "files": sorted(files, key=lambda f: f["name"]),
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main(argv: list[str]) -> int:
    try:
        return run(check_only="--check" in argv)
    except BuildError as exc:
        print(f"BUILD FAILED\n{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
