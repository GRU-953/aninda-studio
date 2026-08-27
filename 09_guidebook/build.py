#!/usr/bin/env python3
"""Aninda Studio — the brand guidebook, generator.

This script is the ONLY writer of 09_guidebook/Aninda-Studio-Guidebook.html and
09_guidebook/Aninda-Studio-Guidebook-print.html. Neither file is hand-written and
neither should ever be hand-edited: the next run overwrites it.

    Build:   ./.venv/bin/python 09_guidebook/build.py
    Verify:  ./.venv/bin/python 09_guidebook/build.py --check

`--check` regenerates every byte of both files in memory and compares them
against what is on disk. It writes nothing and exits non-zero on the first
difference. That is the drift guard: if a token moves and this book is not
rebuilt, --check fails.

WHAT IS HAND-WRITTEN AND WHAT IS NOT
    Hand-written, read from chapters/ and chapters/bn/:
        Welcome, The name, The mark, Icons, Voice, Writing in Bangla,
        Applying it, Licence and trademarks, What this system does not do.
    Generated here, from the sources named at the top of each builder function:
        Colour, Type, Space and shape, Components, Motion.
    Not one colour, size, duration or ratio in this book was typed by a person.
    The colour chapter in particular is read out of 07_tokens/build/*.tokens.json
    and its embedded proofs, never transcribed.

WHY THERE ARE TWO OUTPUT FILES, AND WHY IT MATTERS
    Aninda-Studio-Guidebook.html carries the whole kit inline: every file a user
    of the system needs is a download link whose href is its own base64 data URI.
    That is 67 files, about 9.8 MB on disk and about 13.1 MB once base64-encoded,
    in one document. The print build STRIPS those download data URIs and keeps
    their labels as plain text.

    The reason is the same in both directions: a paper page cannot be clicked. The
    download payloads buy a printed reader nothing at all, and they cost the whole
    document. Measured with `scripts/pdf.py --probe-interactive`:

      * printing the print build gives a PDF of about 1.8 MB — the exact size is
        read from the file and never typed, by _pdf_sizes();
      * printing the interactive build gave a 14.2 MB PDF when measured once,
        while deciding this split, because Chromium
        carries every data URI into the PDF as a link target — ten times the size,
        for links nobody on paper can follow;
      * and the interactive build has no A4 page geometry and no page-break
        rules, so its layout breaks in the wrong places throughout.

    ONE HONEST CORRECTION. The failure this split is usually justified by —
    Chromium's PDF pipeline emitting blank pages once the inlined base64 gets
    large, at somewhere around 24 MB — was NOT reproduced here. At 13.6 MB the
    interactive build printed, with no blank page. So the split rests on the two
    costs measured above and on the fact that the payloads are dead weight on
    paper, and NOT on a blank-page failure this build has actually seen. Anyone
    growing the kit past roughly twice its present size should re-run the probe
    before assuming it still prints.

    Fonts and images are kept in BOTH builds. Without the embedded fonts the
    Bangla prints in a fallback face, which is the one thing this book must not do.

FAIL CLOSED
    Every guard runs against both documents held in memory. If any guard fails,
    the script writes nothing and exits 1:
      * banned English words (the ENGLISH-STANDARD blocklist) — including in the
        generated chapters, which is where they would otherwise creep in;
      * any Bangla run that does not appear verbatim in a verified source file.
        No Bangla is written for this book. Where a verified string does not
        exist the English stays and the gap is named;
      * any unresolved {{placeholder}};
      * any literal colour in this script's own stylesheet;
      * any external reference — http, https or protocol-relative — in a src,
        href to an asset, or url() in CSS.

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import base64
import html as html_mod
import json
import mimetypes
import os
import re
import sys
from pathlib import Path

try:
    import markdown as markdown_mod
except ImportError:  # pragma: no cover - environment guard
    print("markdown is not installed in the project venv.", file=sys.stderr)
    raise SystemExit(2)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

GENERATOR = "09_guidebook/build.py"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

# Every figure in this kit was measured or verified on this date. It is a
# constant rather than today's date so that two builds of the same sources are
# byte-identical and --check means something.
SOURCE_DATE = "14 August 2026"

OUT_INTERACTIVE = HERE / "Aninda-Studio-Guidebook.html"
OUT_PRINT = HERE / "Aninda-Studio-Guidebook-print.html"

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

TOKENS_DIR = ROOT / "07_tokens" / "build"
TOKENS_CSS = ROOT / "07_tokens" / "css" / "tokens.css"
COMPONENTS_CSS = ROOT / "08_components" / "src" / "components.css"
CARDS_JSON = ROOT / "08_components" / "_cards.json"
CARDS_DIR = ROOT / "08_components" / "cards"
FONTS_DIR = ROOT / "08_components" / "fonts"
MARK_DIR = ROOT / "04_mark"
SVG_DIR = MARK_DIR / "svg"
# The chosen direction is READ from the token set rather than named here.
#
# It was hard-coded as "estuary". When the palette was replaced on 26 August 2026
# the token build switched to "natural" and this line did not, so the book asked
# the new four-family token set for a ramp called "warning" that the old six-family
# proof still listed — KeyError: 'warning'. The token file records which direction
# it came from, so there is one name for it and every consumer reads that one.
_PRIM = json.loads(
    (ROOT / "07_tokens" / "build" / "primitive.tokens.json").read_text())
DIRECTION = _PRIM["$extensions"]["studio.aninda"]["direction"]
PROOF_JSON = ROOT / "05_colour" / "generated" / f"{DIRECTION}.proof.json"
MEASUREMENTS_JSON = ROOT / "06_type" / "_data" / "measurements.json"
FONT_FACTS_JSON = ROOT / "06_type" / "_data" / "font_facts.json"
# The external authorities this book cites, with a URL and a date on each. The
# book carried two URLs before this file existed, both licence texts, and 72
# sentences that named an outside body and a number without citing either.
EXTERNAL_JSON = ROOT / "01_research" / "_data" / "external-sources.json"
NPM_DIST = ROOT / "12_packages" / "npm" / "dist"
BANGLA_STANDARD = ROOT / "06_type" / "BANGLA-STANDARD.md"

THEMES = ["light", "dark", "hc-light", "hc-dark"]

VERIFIED_BN_SOURCES = [
    BANGLA_STANDARD,
    ROOT / "06_type" / "RECOMMENDATION.md",
    ROOT / "06_type" / "MEASUREMENTS.md",
    CARDS_JSON,
    COMPONENTS_CSS,
    PROOF_JSON,
    MARK_DIR / "manifest.json",
    MEASUREMENTS_JSON,
    TOKENS_DIR / "primitive.tokens.json",
]

# ---------------------------------------------------------------------------
CHAPTERS = [
    # (number, slug, English title, Bangla title id or None, source)
    # All fourteen keyed to chapter.* in 06_type/bangla-strings.json. Ten used to
    # be served from the hand-typed BN table instead, and the register holds those
    # same ten under chapter.* — so ten of the ninety-four approved keys were dead,
    # and a correction made in the register, the file carrying the dictionary
    # citation behind each string, would have changed nothing in the book. The
    # comment at the head of the BN table names this exact consequence: "two copies
    # of a translation drift, and the one that drifts is the one nobody is looking
    # at." Verified all ten agreed at the moment of the change.
    # Thirteen chapters, and the numbers RUN CONSECUTIVELY. "Writing in Bangla"
    # was chapter 11 and went with the Bangla on 27 August 2026; 12, 13 and 14
    # moved up rather than leaving a hole. A gap would show on the cover, in the
    # contents and in every #ch-NN anchor, in a book whose whole claim is that its
    # numbers are measured — and renaming three files is cheaper than explaining it.
    #
    # The fourth field was a verified-Bangla key for the chapter's own title. Every
    # chapter had one, and each was checked against the string register before it
    # could be printed.
    ("01", "welcome", "Welcome", "file"),
    ("02", "the-name", "The name", "file"),
    ("03", "the-mark", "The mark", "file"),
    ("04", "icons", "Icons", "file"),
    ("05", "colour", "Colour", "generated"),
    ("06", "type", "Type", "generated"),
    ("07", "space-and-shape", "Space and shape", "generated"),
    ("08", "components", "Components", "generated"),
    ("09", "motion", "Motion", "generated"),
    ("10", "voice", "Voice", "file"),
    ("11", "applying-it", "Applying it", "file"),
    ("12", "licence-and-trademarks", "Licence and trademarks", "file"),
    ("13", "what-this-system-does-not-do", "What this system does not do", "file"),
]

CHAPTER_STANDFIRST = {
    "01": "What this is, who wrote it, and why the brand and the design system are two artefacts rather than one.",
    "02": "A Bangla name written in Latin script, and the one thing about it that looks like a mistake and is not.",
    "03": "A circle tangent to a stem that overruns downward. One geometry, two weights, and the mistake that produced it.",
    "04": "Each platform gets the icon geometry it asks for — and exactly what that trades away.",
    "05": "Every ramp, every role and every measured ratio in four themes, read out of the token files.",
    "06": "Two faces, one scale, and the measurements that chose them over twenty-eight others.",
    "07": "A 4 px scale in ten steps, four radii, four target sizes and one focus ring.",
    "08": "Thirty cards in three groups, and the three rules the component layer is built to keep.",
    "09": "Two durations, three curves, and why Material's spring system was read and not adopted.",
    "10": "Plain international English, British spelling, and the six words that are banned outright.",
    "11": "How to install it, theme it, check it, and rebuild this book.",
    "12": "Three licences, one thing with no licence at all, and where the boundary falls.",
    "13": "The honest list. Not a disclaimer — every item changes how much weight to put on something earlier.",
}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def e(text) -> str:
    return html_mod.escape(str(text), quote=True)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_ratio(value: float) -> str:
    return f"{value:.2f}:1"


def fmt_bytes(n: int) -> str:
    """SI, not binary. MB is 10^6 bytes and kB is 10^3 — that is what the prefixes
    mean, it is what macOS and every browser report, and it is what
    scripts/readme.py has always used.

    This divided by 1024 and wrote "MB", so the book called the shipped PDF
    1.7 MB while the generated README called the same file 1.8 MB. Two documents
    in one repository disagreeing about the size of a file both describe is the
    kind of small wrongness that makes a reader doubt the large claims.
    """
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f} MB"
    if n >= 1_000:
        return f"{n / 1_000:.0f} kB"
    return f"{n} bytes"


def table(headers: list[str], rows: list[list[str]], cls: str = "gb-table",
          caption: str = "", row_header: bool = True) -> str:
    """A data table with a caption, column headers and a row header on every row.

    THE BOOK PRINTS THIS RULE AND ITS OWN TABLES BROKE IT. The Table component's
    card says "Row headers, a caption saying what the numbers are, and a sideways
    scroll when the table is wider than the space", and both other surfaces that
    ship that component obey it. In this book none of the 68 tables had a row
    header and 54 had no caption, because this function emitted every body cell as
    a <td> and ignored the caption argument on 29 of its 39 call sites.

    What that costs is WCAG 2.2 SC 1.3.1 Info and Relationships, Level A. In table
    mode a screen reader announces a cell with its headers, so on the ten-column
    colour tables it could say "Worst case ±1 bit, 15.61:1" and never which role
    that belonged to — the role name was a presentational <b> inside a <td>. Ten
    and eight columns is exactly where reading order cannot recover the
    relationship.

    The caption is now REQUIRED. A table of numbers with no statement of what they
    are is the failure this book exists to argue against, and an optional argument
    that 29 call sites skipped is how it stayed that way.

    row_header is there for the rare table whose first column is not the row's
    identity. Nothing passes False today; the argument exists so that a table which
    genuinely has no row identity does not force a wrong <th> on it.
    """
    if not caption.strip():
        raise BuildError(
            f"a table with headers {headers} was built with no caption. Every table "
            f"in this book states what its rows are, because a table of figures "
            f"with no statement of what they are is the thing this book argues "
            f"against. Pass caption=."
        )
    head = "".join(f"<th scope=\"col\">{h}</th>" for h in headers)
    body = []
    for row in rows:
        if row_header and row:
            first = f'<th scope="row">{row[0]}</th>'
            cells = first + "".join(f"<td>{c}</td>" for c in row[1:])
        else:
            cells = "".join(f"<td>{c}</td>" for c in row)
        body.append(f"<tr>{cells}</tr>")
    cap = f"<caption>{caption}</caption>"
    return (
        f'<div class="gb-scroll-x"><table class="{cls}">{cap}'
        f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"
    )


def details(summary: str, body: str) -> str:
    return f"<details class=\"gb-details\"><summary>{summary}</summary>{body}</details>"


def note(body: str, kind: str = "note") -> str:
    return f'<aside class="gb-note gb-note--{kind}">{body}</aside>'


# ---------------------------------------------------------------------------
# Token access
# ---------------------------------------------------------------------------


class Tokens:
    """Reads the DTCG files and resolves aliases. Nothing here invents a value."""

    def __init__(self) -> None:
        self.primitive = read_json(TOKENS_DIR / "primitive.tokens.json")
        self.semantic = {t: read_json(TOKENS_DIR / f"semantic.{t}.tokens.json")
                         for t in THEMES}
        self.forced = read_json(TOKENS_DIR / "forced-colors.map.json")
        self.proof = read_json(PROOF_JSON)

    def prim(self, dotted: str):
        node = self.primitive
        for part in dotted.split("."):
            node = node[part]
        return node

    def resolve_colour(self, value):
        """A semantic $value is either an inline colour object or {alias}."""
        if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            return self.prim(value[1:-1])["$value"]
        return value

    def ramp(self, family: str) -> dict:
        return self.prim(f"color.ramp.{family}")

    def surfaces(self, theme: str) -> dict:
        return self.semantic[theme]["color"]["surface"]

    def roles(self, theme: str) -> list[tuple[str, dict]]:
        """Flatten the semantic colour tree to (role-name, node) in file order,
        skipping the surfaces, which are presented separately."""
        out: list[tuple[str, dict]] = []
        colour = self.semantic[theme]["color"]
        for group, node in colour.items():
            if group.startswith("$") or group == "surface":
                continue
            for name, leaf in node.items():
                if name.startswith("$"):
                    continue
                label = group if name == "default" else f"{group}-{name}"
                out.append((label, leaf))
        return out

    @staticmethod
    def proof_of(leaf: dict) -> dict:
        return leaf["$extensions"]["studio.aninda"]["proof"]

    @staticmethod
    def ext(leaf: dict) -> dict:
        return leaf["$extensions"]["studio.aninda"]


# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------


def load_fonts() -> dict[str, str]:
    cards = read_json(CARDS_JSON)
    out = {}
    # Subsets only. The inventory now also lists the desktop TTF, which is a
    # deliverable rather than a webfont: inlining 136 kB of unsubset TrueType as
    # an @font-face would add weight to every page and draw nothing.
    for spec in cards["_fonts"]:
        if not spec.get("subset", True):
            continue
        path = ROOT / "08_components" / spec["file"]
        out[spec["family"]] = base64.b64encode(path.read_bytes()).decode("ascii")
    return out


def font_face_css(encoded: dict[str, str]) -> str:
    weights = {"Literata": "400 700", "Noto Serif Bengali": "400 700", "Aninda Mono": "400"}
    blocks = []
    for family, data in encoded.items():
        blocks.append(
            "@font-face {\n"
            f'  font-family: "{family}";\n'
            "  font-style: normal;\n"
            f"  font-weight: {weights[family]};\n"
            "  font-display: block;\n"
            f'  src: url(data:font/woff2;base64,{data}) format("woff2");\n'
            "}"
        )
    return "\n".join(blocks)


def inline_svg(name: str, cls: str, title: str, theme_aware: bool = False) -> str:
    """Take a mark file and make it safe to drop inside a page: force a class,
    replace the file's own <title>, and drop the export dimensions so the page
    sizes it.

    `theme_aware` removes the `style="color:…"` the export sets on the root
    element. The artwork is drawn in `currentColor`, so with that inline colour
    gone the mark inherits the theme — which is the point of drawing it that way,
    and without this the mark is invisible in the dark themes. It is applied to
    the bare mark and the wordmarks, and NOT to the icons, whose ground and
    foreground colours are deliberate parts of the artwork.
    """
    raw = (SVG_DIR / name).read_text(encoding="utf-8").strip()
    raw = re.sub(r"<title>.*?</title>", f"<title>{e(title)}</title>", raw, count=1,
                 flags=re.S)
    if theme_aware:
        raw = re.sub(r'(<svg[^>]*?)\s+style="color:#[0-9A-Fa-f]{3,8}"', r"\1", raw,
                     count=1)
    raw = raw.replace("<svg ", f'<svg class="{cls}" ', 1)
    # width and height on the source files are export sizes; the page sizes them.
    raw = re.sub(r'\swidth="[\d.]+"\s*height="[\d.]+"', "", raw, count=1)
    return raw


# ---------------------------------------------------------------------------
# The kit — every file a download link points at
# ---------------------------------------------------------------------------


class BuildError(Exception):
    """A check did not pass. Nothing is written."""


def kit_files() -> list[tuple[str, Path, str]]:
    """(display path, real path, what it is). Order is stable, so --check works."""
    items: list[tuple[str, Path, str]] = []

    for name in ("primitive", "semantic.light", "semantic.dark",
                 "semantic.hc-light", "semantic.hc-dark"):
        items.append((f"07_tokens/build/{name}.tokens.json",
                      TOKENS_DIR / f"{name}.tokens.json",
                      "Design tokens, DTCG 2025.10"))
    items.append(("07_tokens/build/forced-colors.map.json",
                  TOKENS_DIR / "forced-colors.map.json",
                  "Which system colour each role gives way to in forced colours"))
    items.append(("07_tokens/css/tokens.css", TOKENS_CSS,
                  "Every token as a CSS custom property, in five layers"))
    items.append(("01_research/BENCHMARK.md", ROOT / "01_research" / "BENCHMARK.md",
                  "The benchmark this book cites: every external source with its URL "
                  "and date, and the 28 acceptance criteria with their verdicts"))
    items.append(("08_components/src/components.css", COMPONENTS_CSS,
                  "The component layer. No literal colour in it"))

    seen_licences = set()
    for spec in read_json(CARDS_JSON)["_fonts"]:
        form = "subset" if spec.get("subset", True) else "whole face, not subset"
        items.append((f"08_components/{spec['file']}",
                      ROOT / "08_components" / spec["file"],
                      f"{spec['family']} {form}, {spec['licence']}"))
        # The desktop face shares its licence file with the subset it came from,
        # and the same path twice would be two rows for one artefact.
        if spec["licence_file"] not in seen_licences:
            seen_licences.add(spec["licence_file"])
            items.append((f"08_components/{spec['licence_file']}",
                          ROOT / "08_components" / spec["licence_file"],
                          f"The full licence text for {spec['family']}"))

    manifest = read_json(MARK_DIR / "manifest.json")
    for name in manifest["files"]:
        items.append((f"04_mark/svg/{name}", SVG_DIR / name, "Identity artwork"))
    items.append(("04_mark/manifest.json", MARK_DIR / "manifest.json",
                  "The mark's construction, with every check it passed"))
    items.append((f"05_colour/generated/{DIRECTION}.proof.json", PROOF_JSON,
                  "Every colour, every ramp, every measured ratio"))

    for path in sorted(NPM_DIST.iterdir()):
        if path.is_file():
            items.append((f"12_packages/npm/dist/{path.name}", path,
                          "Published package build output"))

    for card in read_json(CARDS_JSON)["cards"]:
        items.append((f"08_components/{card['path']}",
                      ROOT / "08_components" / card["path"],
                      f"{card['group']} card — {card['name']}"))

    return items


def data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    if path.suffix == ".woff2":
        mime = "font/woff2"
    elif path.suffix in (".mjs", ".cjs"):
        mime = "text/javascript"
    elif path.suffix == ".ts":
        mime = "text/plain"
    mime = mime or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


# ---------------------------------------------------------------------------
# Blocks the hand-written chapters ask for by name
# ---------------------------------------------------------------------------


def block_figure_marks() -> str:
    manifest = read_json(MARK_DIR / "manifest.json")
    strokes = manifest["strokes"]
    reg = inline_svg("mark-regular.svg", "gb-mark", "The mark, regular weight",
                     theme_aware=True)
    heavy = inline_svg("mark-heavy.svg", "gb-mark", "The mark, heavy weight",
                       theme_aware=True)
    return (
        '<figure class="gb-figure gb-figure--marks">'
        f'<div class="gb-markbox"><div class="gb-markbox__art">{reg}</div>'
        f'<figcaption class="gb-caption">Regular — stroke {strokes["regular"]:g}</figcaption></div>'
        f'<div class="gb-markbox"><div class="gb-markbox__art">{heavy}</div>'
        f'<figcaption class="gb-caption">Heavy — stroke {strokes["heavy"]:g}</figcaption></div>'
        "</figure>"
    )


def block_figure_construction() -> str:
    m = read_json(MARK_DIR / "manifest.json")
    g = m["geometry"]
    c, sx, st, sb = g["circle"], g["stem_x"], g["stem_top"], g["stem_bottom"]
    grid = "".join(
        f'<line x1="0" y1="{v}" x2="100" y2="{v}"/><line x1="{v}" y1="0" x2="{v}" y2="100"/>'
        for v in range(10, 100, 10)
    )
    return (
        '<figure class="gb-figure">'
        '<svg class="gb-construction" viewBox="-6 -6 112 112" role="img" '
        'aria-label="The mark on its 100-unit construction grid">'
        f'<g class="gb-c-grid">{grid}</g>'
        '<rect class="gb-c-frame" x="0" y="0" width="100" height="100"/>'
        f'<circle class="gb-c-guide" cx="{c["cx"]:g}" cy="{c["cy"]:g}" r="{c["r"]:g}"/>'
        f'<line class="gb-c-guide" x1="{sx:g}" y1="-4" x2="{sx:g}" y2="104"/>'
        f'<circle class="gb-c-art" cx="{c["cx"]:g}" cy="{c["cy"]:g}" r="{c["r"]:g}"/>'
        f'<path class="gb-c-art" d="M{sx:g} {st:g}V{sb:g}"/>'
        f'<circle class="gb-c-dot" cx="{sx:g}" cy="{c["cy"]:g}" r="2.4"/>'
        "</svg>"
        '<figcaption class="gb-caption">The circle, the tangent stem, and the '
        "downward overrun. Read from <code>04_mark/manifest.json</code>."
        "</figcaption></figure>"
    )


def block_figure_icons() -> str:
    order = [
        ("icon-1024.svg", "icon-1024", "The web icon, rounded"),
        ("icon-512.svg", "icon-512", "Avatars and progressive web apps"),
        ("icon-192.svg", "icon-192", "Progressive web apps"),
        ("tile-web.svg", "tile-web", "Web tile, heavy weight"),
        ("icon-apple-1024.svg", "icon-apple", "Apple, Default — square, unmasked"),
        ("icon-apple-1024-dark.svg", "icon-apple-dark", "Apple, Dark"),
        ("icon-apple-1024-mono.svg", "icon-apple-mono", "Apple, Mono — no ground"),
        ("icon-apple-1088-watch.svg", "icon-apple-watch", "Apple, watchOS at 1088"),
        ("icon-android-background-108.svg", "icon-android-bg",
         "Android, background layer"),
        ("icon-android-foreground-108.svg", "icon-android-fg",
         "Android, foreground layer"),
        ("icon-android-monochrome-108.svg", "icon-android-mono",
         "Android, monochrome — the system tints this"),
    ]
    cells = []
    for name, ident, caption in order:
        art = inline_svg(name, "gb-icon", caption)
        cells.append(
            f'<div class="gb-iconbox"><div class="gb-iconbox__art">{art}</div>'
            f'<p class="gb-caption"><code>{e(name)}</code><br>{e(caption)}</p></div>'
        )
    return f'<figure class="gb-figure gb-figure--icons">{"".join(cells)}</figure>'


def block_figure_wordmarks() -> str:
    """One wordmark. There were two, in two scripts, side by side.

    The Bangla wordmark went with the Bangla on 27 August 2026. Its cell carried a
    note worth keeping the substance of: the image's accessible name was written in
    English on purpose, because an SVG <title> is the whole accessible name and SVG
    offers no way to mark the language of PART of one — so Bangla embedded there was
    pronounced by an English speech engine. That constraint still applies to any
    future artwork whose name is not English.
    """
    latin = inline_svg("wordmark-latin.svg", "gb-wordmark",
                       "The wordmark — aninda studio", theme_aware=True)
    return (
        '<figure class="gb-figure gb-figure--wordmarks">'
        f'<div class="gb-wordbox">{latin}'
        '<figcaption class="gb-caption">aninda studio</figcaption></div>'
        "</figure>"
    )


def block_mark_geometry() -> str:
    m = read_json(MARK_DIR / "manifest.json")
    g = m["geometry"]
    c = g["circle"]
    rows = [
        ["Grid", f"{m['grid']:g} × {m['grid']:g} units"],
        ["Circle centre", f"x {c['cx']:g}, y {c['cy']:g}"],
        ["Circle radius", f"{c['r']:g} units"],
        ["Stem x", f"{g['stem_x']:g} — the circle's right edge, so the two are tangent"],
        ["Stem top", f"y {g['stem_top']:g} — level with the top of the circle"],
        ["Stem bottom", f"y {g['stem_bottom']:g} — "
                        f"{g['stem_bottom'] - (c['cy'] + c['r']):g} units below the circle"],
        ["Clear space", e(m["clear_space"])],
        ["Safe field inside an icon", f"{m['safe_field']:g} of {m['grid']:g} units"],
    ]
    return (block_figure_construction()
            + table(["Measure", "Value"], rows,
                    caption="Read from 04_mark/manifest.json at build time."))


def block_mark_strokes() -> str:
    m = read_json(MARK_DIR / "manifest.json")
    s = m["strokes"]
    rows = [
        ["Regular", f"{s['regular']:g}", "24 px and above", "65 × 73 units", "36.5 units"],
        ["Heavy", f"{s['heavy']:g}", "below 24 px", "71 × 79 units", "39.5 units"],
    ]
    return table(
        ["Weight", "Stroke", "Use at", "Drawn extent", "Clear space"],
        rows,
        caption=f"The rule, in the manifest's own words: {e(s['rule'])}.",
    )


def block_mark_files() -> str:
    m = read_json(MARK_DIR / "manifest.json")
    rows = []
    for name in m["files"]:
        path = SVG_DIR / name
        rows.append([f"<code>{e(name)}</code>", fmt_bytes(path.stat().st_size)])
    checks = "".join(f"<li>{e(c)}</li>" for c in m["checks"])
    return (
        table(["File", "Size"], rows,
                caption="Every mark file this build wrote, with its size read off the file.")
        + details("Every check the mark build ran, and passed",
                  f'<ul class="gb-list">{checks}</ul>')
    )


def block_icon_files() -> str:
    m = read_json(MARK_DIR / "manifest.json")
    pol = m["icon_policy"]
    where = {
        "web": "The web. Rounded, because a browser will not round a favicon for you",
        "apple": "Apple. Square and unmasked — the system applies its own mask",
        "android": "Android. A layer the launcher composites",
    }
    rows = []
    for surface, names in pol["surfaces"].items():
        for name in names:
            rows.append([f"<code>{e(name)}</code>", e(where[surface])])
    sup = pol["superseded"][0]
    return (
        table(["File", "Which platform it is for"], rows,
                caption="Every icon artefact, and the platform each one is for.")
        + note(f"<p><strong>The decision.</strong> {e(pol['decision'])} "
               f"{e(pol['reason'])} Verified against the "
               f"{e(pol['verified_against'])}.</p>")
        + note(f"<p><strong>What this reversed.</strong> On {e(sup['taken'])} the "
               f"decision here was the opposite: {e(sup['decision'])} It was reversed "
               f"on {e(sup['reversed'])}. {e(sup['why_reversed'])} "
               f"{e(sup['what_of_it_still_holds'])}</p>")
    )


def block_publication() -> str:
    """Whether the registries hold these packages, read from one shared record.

    Three of the four places that told a reader to install these packages omitted
    that they are not published; only the website said so. All four now read
    12_packages/PUBLICATION.json, so they cannot disagree about it.
    """
    pub = read_json(ROOT / "12_packages" / "PUBLICATION.json")
    missing = [r for r in pub["registries"] if not r["published"]]
    if not missing:
        return note("<p><strong>Published.</strong> Both packages are on their "
                    f"registries, checked {e(pub['checked'])}.</p>")
    where = " and ".join(e(r["registry"]) for r in missing)
    # Both registries carry the same package name, so the list is deduplicated
    # while keeping its order — otherwise the sentence reads "neither holds X, X".
    names = ", ".join(f"<code>{e(name)}</code>"
                      for name in dict.fromkeys(r["package"] for r in missing))
    return note(
        f"<p><strong>Not published yet.</strong> On {e(pub['checked'])} I checked "
        f"{where}, and neither holds {names}. The two commands below are what will "
        f"work once they are published. Until then, use the checkout: the packages "
        f"are built, and the files they carry are in <code>12_packages/</code>.</p>",
        kind="gap",
    )


def block_icon_mask_measurement() -> str:
    """The circular-mask difference, read out of the mark manifest.

    This chapter used to assert "Measured here: the penalty is nil on watchOS and
    visionOS" and offer the placement check's "worst corner 45.00 of 45" as the
    evidence — a different quantity, and one that equals 45.00 by construction.
    04_mark/build.py now renders the rounded icon and the square master under the
    same inscribed circle and differences them, and this block prints what it
    measured rather than restating a claim.
    """
    m = read_json(MARK_DIR / "manifest.json")
    measured = [line for line in m["checks"] if line.startswith("under a circle")]
    if len(measured) != 1:
        raise BuildError(
            "04_mark/manifest.json holds "
            f"{len(measured)} circular-mask measurements, expected exactly one. The "
            "chapter states this as measured, so it must not be assembled without it."
        )
    return note(f"<p><strong>Measured.</strong> {e(measured[0][0].upper() + measured[0][1:])}.</p>")


def block_icon_visual_parity() -> str:
    """The Apple-against-Android size comparison, read out of the mark manifest.

    Following each platform's own geometry changes the corner SHAPE on purpose. The
    thing it must not change is how large the mark reads, and that is the claim a
    reader will most want evidence for, because it is the one that decides whether
    two different-shaped icons still look like one brand. 04_mark/build.py measures
    it and this block prints what it measured.
    """
    m = read_json(MARK_DIR / "manifest.json")
    measured = [line for line in m["checks"] if line.startswith("visual parity")]
    if len(measured) != 1:
        raise BuildError(
            f"04_mark/manifest.json holds {len(measured)} visual-parity measurements, "
            "expected exactly one. The chapter states this as measured, so it must "
            "not be assembled without it."
        )
    text = measured[0]
    text = text[0].upper() + text[1:]
    return note(f"<p><strong>Measured.</strong> {e(text)}.</p>")


def block_bangla_removed() -> str:
    """The measured half of the Bangla work, kept after the Bangla went.

    This was four sections of the type chapter until 27 August 2026 — the
    multiplier's derivation, the size floor, the weight bump and the shaping
    proof. It is the strongest measurement in this book: two rendered ink heights
    read out of Chromium at six nominal sizes, and a luminance reading that decided
    a weight step. Deleting it would have deleted the evidence for a decision, so
    it moved here instead, into the chapter about what this system does not do.

    It reads 06_type/_data/measurements.json and NOT the token set. That is the
    point of putting it here: the tokens it used to quote have been removed, and a
    record that depended on them would have died with them. The measurements file
    is retained, so this passage still cites what was actually read.
    """
    meas = read_json(MEASUREMENTS_JSON)
    ratio = meas["ratios"]["08-editorial-revised"]
    out: list[str] = []

    out.append(
        "<p>Bangla and Latin do not look the same size at the same size. Bangla's "
        "reading height — baseline to the matra — the headline stroke along the top of "
        "the letters — sat at about 0.62 em against Latin's x-height of about "
        "0.51 em. Setting both at 16 px made the Bangla look a fifth larger, so it "
        "was multiplied down until the two measured heights matched.</p>")

    rows = []
    for size in ("11", "12", "16", "28", "56", "100"):
        s = ratio["per_size"][size]
        rows.append([
            f"{size} px",
            f"{s['latin_x_height_px']:.3f} px ({s['latin_x_height_em']:.4f} em)",
            f"{s['bangla_matra_height_px']:.3f} px "
            f"({s['bangla_matra_height_em']:.4f} em)",
            f"×{s['bangla_appears_larger_by']:.4f}",
            f"<b>×{s['bangla_size_multiplier']:.3f}</b>",
        ])
    out.append(table(["Nominal size", "Literata x-height",
                      "Noto Serif Bengali baseline to the matra",
                      "Bangla appeared larger by", "Multiplier"], rows,
                     caption="Where the Bangla multiplier came from: two measured "
                             "heights at each nominal size, read off rendered ink."))

    out.append(
        f"<p>The headline figure was <strong>×"
        f"{ratio['bangla_size_multiplier_at_16']}</strong> at body size, and it "
        "barely moved across the scale because Literata's x-height is nearly flat "
        "along its optical-size axis. Every figure above was read off real rendered "
        "ink in Chromium through the Canvas text-metrics interface, never from what "
        "a font declares about itself.</p>")

    out.append(note(
        "<p><strong>Why declared metrics were not trusted.</strong> Noto Sans "
        "Bengali declares a cap height of 622 units, and that is not the height of "
        "its capital H — it is the matra height. The field had been repurposed. A "
        "design system that read it to align two scripts would have been aligning "
        "to the wrong thing entirely. That warning outlives the Bangla: a declared "
        "metric is a claim, and this system measures claims.</p>"))

    out.append(
        "<p>Two rules followed from it. Bangla never went below <strong>12 px</strong> "
        "whatever the multiplier said, because below that the matra and the "
        "conjuncts stopped surviving. And <strong>below 14 px it gained one weight "
        "step</strong>: measured at a device scale factor of 1, the matra at 12 px "
        "and weight 400 rendered at luminance 123 on white, which reads as grey "
        "rather than black, and at weight 500 it held at 108. Those were the only "
        "size-dependent compensation rules this system had, and they left with the "
        "script they were measured for.</p>")

    shaping = meas["shaping"]["notoserifbengali"]
    out.append(
        f"<p>Shaping was proved, not assumed: {shaping['passed']} conjuncts and the "
        "five test words shaped through HarfBuzz with no dotted circles, no missing "
        "glyphs and no stray hasantas. The studio name shaped 16 code points into "
        "11 glyphs, and a negative control confirmed that was real — mapping each "
        "code point straight through the cmap gave 16. That negative control is the "
        "one piece of this that did not leave. It is now an English ligature test, "
        "and <code>04_mark/manifest.json</code> records both what it proves and what "
        "it no longer does.</p>")

    out.append(note(
        "<p><strong>What none of this measured.</strong> Whether the Bangla read "
        "well to a Bangla reader. Every ruling was sourced to the Bangla Academy's "
        "own dictionary, and sourced is not the same as read well — no second Bangla "
        "reader was ever asked, and that gap closed by removal rather than by being "
        "filled.</p>"))

    return "".join(out)


def block_font_licences() -> str:
    cards = read_json(CARDS_JSON)
    rows = []
    for spec in cards["_fonts"]:
        rows.append([
            e(spec["family"]),
            e(spec["licence"]),
            "Yes — renamed" if spec["renamed"] else "No",
            "Subset" if spec.get("subset", True) else "Whole face",
            fmt_bytes(spec["bytes"]),
            f"<code>{e(spec['licence_file'])}</code>",
        ])
    subsets = sum(1 for f in cards["_fonts"] if f.get("subset", True))
    whole = len(cards["_fonts"]) - subsets
    return table(["Family", "Licence", "Reserved Font Name", "Form", "Size on disk",
                  "Licence text"], rows,
                 caption=(f"Every font artefact this kit redistributes: {subsets} "
                          f"subsets and {whole} whole face, each with its licence "
                          f"and its size as written to disk. The whole face is the "
                          f"desktop file, listed here because a reader is more "
                          f"likely to install or pass on that one than any subset."))


def _pdf_sizes() -> str:
    """The two PDF sizes, read from disk where a file exists.

    These were the typed figures "about 1.4 MB" and "about 14.2 MB" in the
    paragraph that justifies shipping two HTML builds. The shipped PDF is 1.8 MB
    and README.md — which is generated — said so, so the book and its own README
    disagreed about a file both of them describe.

    The print PDF is read at build time. The interactive one is not shipped and
    never has been: 14.2 MB was a single measurement taken while deciding the
    split, so it is now labelled as that rather than stated as a property of a
    file. On a clean tree the print PDF does not exist yet either — the PDF is
    printed FROM this HTML — and in that case the sentence says the measurement
    has not been taken rather than quoting a number for a file that is not there.
    """
    # THE PRINT PDF'S OWN SIZE IS NOT QUOTED, and that is a fix rather than an
    # omission. This sentence used to read it off the file, which is a loop: the
    # PDF is printed FROM this HTML, so the book cited a figure its own text
    # changed. It converged only while the size was stable. Removing the Bangla
    # took the PDF from 1.9 MB to 1.2 MB and the build stopped being idempotent —
    # same byte LENGTH both runs, because the two figures are the same width, and
    # different content. --check reported "differs — on disk 543177 bytes,
    # regenerated 543177 bytes", which is a strange sentence and an accurate one.
    #
    # The two figures that remain are inputs rather than outputs: the kit's own
    # size on disk, and one recorded measurement of an interactive PDF that is not
    # shipped. Neither moves when this paragraph does.
    return ("Printing the interactive build gave a PDF of about 14.2 MB when that "
            "was measured, once, while deciding this split; the print build's is a "
            "small fraction of it. That figure is not quoted here, because this "
            "book is what the PDF is printed from and a document that cites the "
            "size of its own output cannot settle. That PDF is "
            "not shipped, ")


def block_output_files(print_mode: bool) -> str:
    items = kit_files()
    on_disk = sum(p.stat().st_size for _, p, _ in items)
    encoded = on_disk * 4 / 3
    rows = [
        ["<code>Aninda-Studio-Guidebook.html</code>",
         "The whole kit inline. Every file in the kit is a download link whose "
         "href is its own data URI. Opens from a file path with no network."],
        ["<code>Aninda-Studio-Guidebook-print.html</code>",
         "The same book with the download data URIs stripped and their labels "
         "kept as text. Adds A4 page geometry and page-break rules."],
        ["<code>Aninda-Studio-Guidebook.pdf</code>",
         "A4, printed from the second file by Playwright. No other tool is "
         "involved: no ghostscript, no qpdf."],
    ]
    reason = (
        "<p><strong>Why two HTML files, and what was measured.</strong> The "
        f"interactive file carries {len(items)} kit files — about "
        f"{fmt_bytes(on_disk)} on disk, about {fmt_bytes(int(encoded))} once "
        "base64-encoded. A paper page cannot be clicked, so those payloads buy a "
        "printed reader nothing.</p>"
        "<p>They also cost a great deal. " + _pdf_sizes() +
        "because Chromium carries every data URI into the PDF as a link target — "
        "for links nobody on paper can follow. The "
        "interactive build also has no A4 page geometry and no page-break rules, "
        "so its layout breaks in the wrong places throughout.</p>"
        "<p><strong>One correction, since this split is usually justified with a "
        "stronger claim.</strong> Chromium's PDF pipeline is known to emit blank "
        "pages once the inlined base64 gets large, at somewhere around 24 MB. "
        "<em>That was not reproduced here.</em> At the present size the "
        "interactive build printed, with no blank page. The split rests on the "
        "two costs above, not on a failure this build has seen. Run "
        "<code>scripts/pdf.py --probe-interactive</code> to re-measure it after "
        "the kit grows.</p>"
        "<p>Fonts and images stay in both builds. Without the embedded fonts the "
        "type prints in a fallback face, which is the one thing this book must "
        "not do.</p>"
    )
    return table(["File", "What it is"], rows,
                 caption="What this build writes, and what each file is for.") + note(reason)


def block_kit_index() -> str:
    items = kit_files()
    total = sum(p.stat().st_size for _, p, _ in items)
    rows = [
        ["Files in the kit", str(len(items))],
        ["Total size on disk", fmt_bytes(total)],
        ["Themes", "4 — light, dark, high contrast light, high contrast dark"],
        ["Component cards", "30 — 6 foundations, 16 components, 8 patterns"],
        ["Identity files", "10"],
        ["Typefaces", "3, each SIL OFL 1.1"],
    ]
    return table(["Measure", "Value"], rows,
                 caption="What the kit contains, counted from the repository "
                         "each time this book is built.") + (
        '<p>The full list, with a download link for each, is at the end of this '
        "book.</p>"
    )


def block_banned_words() -> str:
    """The one place the blocklist itself is printed. It is marked
    `data-verbatim` so the English guard skips it — a list of banned words is the
    single case where naming them is the point rather than the failure."""
    return ('<p class="gb-verbatim" data-verbatim><b>'
            + " · ".join(BANNED_WORDS[:4] + ["of course"] + BANNED_WORDS[4:])
            + "</b></p>")


def block_banned_latin() -> str:
    return ('<p class="gb-verbatim" data-verbatim>Banned: <b>'
            + "</b>, <b>".join(p for p in BANNED_PHRASES if p.endswith("."))
            + "</b>. Write <i>for example</i>, <i>that is</i>, <i>and so on</i>.</p>")


# ---------------------------------------------------------------------------
# Generated chapter — Colour
#
# Sources: 07_tokens/build/primitive.tokens.json,
#          07_tokens/build/semantic.{light,dark,hc-light,hc-dark}.tokens.json,
#          07_tokens/build/forced-colors.map.json,
#          05_colour/generated/<direction>.proof.json (names and premise only).
# Every ratio below is read from the proof carried inside the token file. None
# of them is transcribed.
# ---------------------------------------------------------------------------


def chapter_colour_en(tok: Tokens) -> str:
    out: list[str] = []
    proof = tok.proof

    out.append("<h2>Three terms, first</h2>")
    out.append(
        "<dl class=\"gb-defs\">"
        "<dt>Contrast ratio</dt><dd>How far apart two colours are in brightness, "
        "written as a ratio. Black on white is 21:1; two colours you cannot tell "
        "apart are 1:1.</dd>"
        "<dt>WCAG AA</dt><dd>The middle of the three conformance levels in the "
        "Web Content Accessibility Guidelines: 4.5:1 for normal text and 3:1 for "
        "borders, icons and controls. This system is held to it.</dd>"
        "<dt>WCAG AAA</dt><dd>The strictest level: 7:1 for normal text. This "
        "system reaches it in places, and the high contrast themes are generated "
        "against it rather than patched towards it.</dd>"
        "</dl>"
    )
    out.append(note(
        "<p><strong>WCAG defines no AAA level for non-text contrast.</strong> "
        "Criterion 1.4.11 has a single requirement of 3:1 and no enhanced tier "
        "above it. So a border measured at 3.9:1 has <em>fully met</em> 1.4.11. "
        "It is not an AA-only compromise waiting to be improved, and nothing in "
        "this book will describe it as one.</p>"))

    out.append("<h2>The direction</h2>")
    # The direction's own Bangla name, and NOTHING if it has none.
    #
    # This printed bn_span("col-1"), a fixed key that resolved to মোহনা — the
    # previous palette's name for its ground family, meaning "estuary". When the
    # palette was replaced on 26 August 2026 the label stayed, so the book showed
    # "Natural Gray — মোহনা": a new colour under an old colour's name, in a language
    # the reader is being asked to trust.
    out.append(f'<p class="gb-lead">{e(proof["name"])}</p>')
    if not proof.get("name_bn"):
        out.append(note(
            "<p><strong>This palette has no Bangla names yet.</strong> The English "
            "names were supplied by the owner; the Bangla ones have not been. No "
            "Bangla is written for this book — only strings checked against the "
            "Bangla Academy standard appear — so the names are absent rather than "
            "translated. The previous palette's names belong to colours that no "
            "longer exist and are not reused here.</p>"))
    out.append(f"<p>{e(proof['premise'])}</p>")

    out.append(f"<h2>The ramps</h2>")
    out.append(
        "<p>Each ramp is computed in OKLCH — a colour space where a fixed change "
        "in lightness looks like the same change to the eye at every hue — then "
        "mapped into sRGB. Each rung is at least 0.9 ΔE2000 from the one before "
        "it, which is the smallest difference a person reliably sees. The 11 "
        "steps run 50 to 950.</p>"
    )
    steps = proof["steps"]
    for family, fam in proof["families"].items():
        ramp = tok.ramp(family)
        ext = ramp["$extensions"]["studio.aninda"]
        swatches = []
        for step in steps:
            leaf = ramp[str(step)]
            hexv = leaf["$value"]["hex"]
            swatches.append(
                f'<div class="gb-swatch"><div class="gb-swatch__chip" '
                f'style="background:{e(hexv)}"></div>'
                f'<div class="gb-swatch__meta"><b>{step}</b>'
                f'<code>{e(hexv)}</code></div></div>'
            )
        # row_header=False: this is a single row of five different measures, so
        # the first cell is a hue rather than the row's identity. The row's
        # identity is the family, and that is in the caption and the heading above.
        meta = table(
            ["Hue (OKLCH)", "Chroma ceiling", "Anchor", "Anchor step", "Kind"],
            [[f"{ext['hueOklch']}°", f"{ext['chromaCeiling']}",
              f"<code>{e(ext['anchor'])}</code>", str(ext["anchorStep"]),
              e(fam["kind"])]],
            caption=f"How the {e(fam['label'])} ramp is generated.",
            row_header=False,
        )
        note_text = fam["note"] or ramp["$description"]
        out.append(
            f'<section class="gb-ramp"><h3>{e(fam["label"])} '
            f'<span class="gb-muted">/ {e(family)}</span></h3>'
            f"<p>{e(note_text)}</p>"
            f'<div class="gb-swatches">{"".join(swatches)}</div>'
            f"{meta}</section>"
        )

    out.append("<h2>The four themes</h2>")
    out.append(
        "<p>Not four skins over one palette. Each theme was generated against its "
        "own contrast target, which is why the high contrast pair is a different "
        "set of colours rather than the same colours pushed further apart.</p>"
    )
    for theme in THEMES:
        out.append(theme_section(tok, theme))

    out.append("<h2>Forced colours</h2>")
    out.append(
        "<p>Forced colours is the mode where the operating system replaces every "
        "colour on the page with its own. Every brand value gives way. A hex that "
        "survives this mode has defeated it, which is why the token file maps "
        "each role to a system colour keyword instead.</p>"
    )
    forced = tok.forced
    rows = [[f"<code>{e(k)}</code>", f"<code>{e(v)}</code>"]
            for k, v in forced["map"].items()]
    out.append(table(["Token", "System colour it becomes"], rows,
                     caption="Forced-colors mode: which system keyword each "
                             "token yields to, from forced-colors.map.json."))
    out.append(
        '<ul class="gb-list">'
        + "".join(f"<li>{e(r)}</li>" for r in forced["rules"])
        + "</ul>")
    out.append(note(f"<p>{e(forced['$description'])}</p>"))

    out.append("<h2>How every figure above was produced</h2>")
    m = proof["measurement"]
    out.append(table(
        ["Step", "How"],
        caption="How every colour figure in this chapter was produced.",
        rows=
        [["Library", e(m["library"])],
         ["Contrast method", e(m["contrast_method"])],
         ["Perceptual difference", f"ΔE{e(m['delta_e_method'])}"],
         ["Ramp space", e(m["ramp_space"])],
         ["Gamut mapping", e(m["gamut_map"])]],
    ))
    out.append(f"<p>{e(m['note'])}</p>")
    out.append(note(
        "<p><strong>What the worst-case column means.</strong> A colour written "
        "as a hex is rounded to 8 bits per channel. Nudging every channel of both "
        "colours by one bit, in the direction that hurts, gives the worst ratio "
        "the pair can actually produce on a screen. That figure is published "
        "beside the measured one. Where the two differ, trust the worst case.</p>"))
    out.append(block_dynamic_colour())

    return "".join(out)


def fmt_list(names: list[str]) -> str:
    """`a`, `b` and `c` — the Oxford-comma-free form the English standard uses."""
    codes = [f"<code>{e(n)}</code>" for n in names]
    if len(codes) == 1:
        return codes[0]
    return ", ".join(codes[:-1]) + " and " + codes[-1]


def theme_section(tok: Tokens, theme: str) -> str:
    proof_theme = tok.proof["themes"][theme]
    ext = tok.semantic[theme]["$extensions"]["studio.aninda"]
    label = proof_theme["label"]

    surfaces = tok.surfaces(theme)
    chips = []
    for name, leaf in surfaces.items():
        if name.startswith("$"):
            continue
        hexv = leaf["$value"]["hex"]
        lum = leaf["$extensions"]["studio.aninda"]["luminance"]
        chips.append(
            f'<div class="gb-swatch"><div class="gb-swatch__chip gb-swatch__chip--bordered" '
            f'style="background:{e(hexv)}"></div>'
            f'<div class="gb-swatch__meta"><b>{e(name)}</b><code>{e(hexv)}</code>'
            f'<span class="gb-muted">luminance {lum:.4f}</span></div></div>'
        )

    rows = []
    matrix_rows = []
    fills: list[str] = []
    surface_names = [n for n in surfaces if not n.startswith("$")]
    for role, leaf in tok.roles(theme):
        p = tok.proof_of(leaf)
        x = tok.ext(leaf)
        hexv = tok.resolve_colour(leaf["$value"])["hex"]
        rows.append([
            f'<span class="gb-dot" style="background:{e(hexv)}"></span> <b>{e(role)}</b>',
            f"<code>{e(hexv)}</code>",
            f"{e(x['family'])} {x['step']}",
            e(x["kind"]),
            fmt_ratio(p["required"]),
            f"<b>{fmt_ratio(p['measured'])}</b>",
            fmt_ratio(p["worstCaseLsb"]),
            e(p["hardestGround"]),
            e(p["level"]),
            e(p["criterion"]),
        ])
        # Two kinds are measured against a named partner rather than against the
        # seven surfaces, and both are legitimately absent from this matrix for the
        # same reason: putting them in it would mean inventing seven ratios that
        # were never taken.
        #   "fill"    — a GROUND that carries text, measured against the label.
        #   "on-fill" — the INK on such a ground, measured against every fill that
        #               carries it. Added 26 August 2026 with color/accent/on.
        # Any other role missing a surface is a real fault and must stop the build
        # rather than be quietly dropped from the table.
        if x["kind"] in ("fill", "on-fill"):
            fills.append(role)
            continue
        missing = [n for n in surface_names if n not in p["againstEverySurface"]]
        if missing:
            raise BuildError(
                f"{theme}/{role} is kind '{x['kind']}' but was not measured against "
                f"{missing}. Only a 'fill' role is legitimately absent from the "
                f"against-every-surface matrix."
            )
        matrix_rows.append(
            [f"<b>{e(role)}</b>"]
            + [fmt_ratio(p["againstEverySurface"][s]) for s in surface_names]
        )

    return (
        f'<section class="gb-theme" data-theme="{e(theme)}">'
        f"<h3>{e(label)}</h3>"
        + table(["Setting", "Value"],
                caption=f"What the {e(label)} theme is measured against.",
                rows=[["Polarity", e(ext["polarity"])],
                 ["High contrast", "yes" if ext["highContrast"] else "no"],
                 ["Text target", fmt_ratio(ext["textTarget"])],
                 ["Non-text target", fmt_ratio(ext["nonTextTarget"])]])
        + "<h4>Surfaces</h4>"
        + f'<div class="gb-swatches gb-swatches--surfaces">{"".join(chips)}</div>'
        + "<h4>Roles</h4>"
        + table(["Role", "Value", "Ramp step", "Kind", "Required", "Measured",
                 "Worst case ±1 bit", "Hardest surface", "Level", "Criterion"], rows,
                caption=f"Every role in the {e(label)} theme, with the contrast "
                        f"ratio it was measured at and the criterion it was "
                        f"measured against.")
        + details(
            "Every ink and line role against every one of the seven surfaces",
            table(["Role"] + surface_names, matrix_rows,
                  caption=(
                      f"Every role that sits ON a surface, against every surface in "
                      f"the {e(label)} theme. Each cell is a measured contrast ratio. "
                      + (f"{fmt_list(fills)} " + ("is" if len(fills) == 1 else "are")
                         + " absent because "
                         + ("it is a ground that carries text, so it is measured "
                            "against the label on it — see the Hardest surface "
                            "column above." if len(fills) == 1 else
                            "they are grounds that carry text, so they are measured "
                            "against the labels on them — see the Hardest surface "
                            "column above.")
                         if fills else ""))))
        + "</section>"
    )


def cite(entry: dict) -> str:
    """One citation: the authority, the page, its URL and the date it carried."""
    return (f'<span class="gb-cite">{e(entry["title"])} — '
            f'<code>{e(entry["url"])}</code>, {e(entry["date_on_source"])}</span>')


def _external() -> dict:
    return read_json(EXTERNAL_JSON)


def block_platform_floors() -> str:
    """The smallest type size each Apple platform allows, and this kit's own floor.

    The kit documented ONE floor — 12 px — for everything, and acceptance criterion 9
    in 01_research/BENCHMARK.md had already written down why that is not enough: the
    minimum differs by more than a factor of two across Apple's five platforms, so a
    single smallest size cannot be checked against any of them. tvOS appeared nowhere
    in this book at all.
    """
    ext = _external()
    ty = ext["platforms"]["type"]
    caption_rem = tok_caption = None
    prim = read_json(TOKENS_DIR / "primitive.tokens.json")
    px = prim["dimension"]["type"]["caption"]["$value"]["value"] * 16
    rows = []
    for row in ty["rows"]:
        clears = px >= row["minimum_pt"]
        rows.append([
            e(row["platform"]),
            f'{row["default_pt"]} pt',
            f'<b>{row["minimum_pt"]} pt</b>',
            ("clears it" if clears else
             f'<b>below it</b> — this kit is not specified for {e(row["platform"])}'),
        ])
    return (
        table(["Platform", "Default", "Minimum", "This kit's smallest step, "
               f"{px:g} px"], rows,
              caption=("The smallest text size each Apple platform allows, against "
                       "the smallest step in this scale. Two of these are floors this "
                       "kit clears with nothing to spare."))
        + f'<p class="gb-note">Source: {cite({"title": ty["source"], "url": "developer.apple.com/design/human-interface-guidelines/typography", "date_on_source": ty["source_date"]})}. '
          f'{e(ty["note"])}</p>'
        + f'<p>This kit is built for the web, where the unit is the CSS pixel and '
          f'there is no platform minimum to clear — so its own floor is the one it '
          f'sets: <b>{px:g} px</b> for the smallest step. Ported to an Apple '
          f'platform, that floor clears iOS, iPadOS, macOS, visionOS and watchOS, and '
          f'does <b>not</b> clear tvOS, whose minimum is '
          f'{[r["minimum_pt"] for r in ty["rows"] if r["platform"] == "tvOS"][0]} pt. '
          f'This kit is not specified for tvOS and does not claim to be.</p>'
    )


def block_control_spacing() -> str:
    """The gap between adjacent controls, which the kit set in code and never stated."""
    ext = _external()
    sp = ext["platforms"]["spacing"]
    prim = read_json(TOKENS_DIR / "primitive.tokens.json")
    space = {k: v["$value"]["value"]
             for k, v in prim["dimension"]["space"].items() if not k.startswith("$")}
    bez = next((k for k, v in space.items() if v == sp["bezelled_pt"]), None)
    unbez = next((k for k, v in space.items() if v == sp["unbezelled_pt"]), None)
    return (
        f'<p><b>Adjacent controls are separated by at least '
        f'<code>--as-space-{e(bez)}</code>, which is {sp["bezelled_pt"]} px.</b> '
        f'Where controls have no visible edge of their own — a row of quiet buttons, '
        f'an icon-only toolbar — the gap goes to '
        f'<code>--as-space-{e(unbez)}</code>, {sp["unbezelled_pt"]} px. That is the '
        f'rule; the component layer already obeys it, and now says so.</p>'
        f'<p class="gb-note">{e(sp["claim"])} Source: '
        f'{cite({"title": sp["source"], "url": "developer.apple.com/design/human-interface-guidelines/accessibility", "date_on_source": sp["source_date"]})}. '
        f'The two figures coincide with two steps this scale already had, which is why '
        f'no token was added for them. A size without a gap is half a specification: '
        f'two 24 px targets touching are harder to hit accurately than one, however '
        f'well each measures.</p>'
    )


def block_dynamic_colour() -> str:
    """This kit's position on Android dynamic colour, and the mechanism it names."""
    ext = _external()
    dc = ext["platforms"]["dynamic_colour"]
    return (
        '<h3>Dynamic colour: this kit holds its own</h3>'
        f'<p>{e(dc["opt_in"])} There are two routes: '
        f'{e(dc["routes"][0])}, or {e(dc["routes"][1])}.</p>'
        '<p><b>This kit takes the first. Brand colours stay static, and '
        '<code>HarmonizedColors</code> is not used.</b> The reason is the whole point '
        'of the colour engine: every pair in this system was measured, and the figure '
        'published is the worst case under a one-bit perturbation. A palette shifted '
        'towards a wallpaper at run time has not been measured against anything, so '
        'every ratio in this book would become an estimate.</p>'
        '<p>That is a trade, and it is worth naming what it costs: on Android a '
        'reader who has set a wallpaper palette will see this system ignore it.</p>'
        f'<p class="gb-note">Source: {cite({"title": dc["source"], "url": "m3.material.io and developer.android.com/jetpack/androidx/releases/compose-material3", "date_on_source": dc["source_date"]})}. '
        f'The engine behind the other route is {e(dc["engine"])}</p>'
    )


def block_sources() -> str:
    """Every external authority this book relies on, with a URL and a date."""
    ext = _external()
    # The four rows this refuses were in the data for weeks and the book printed
    # them: `| Source | URL | Date on the source |` is the HEADER of each of
    # BENCHMARK.md's four tables, and the extractor took them as sources. So the
    # book said "57 sources" over 53 real ones, and rendered four rows whose URL
    # was the word URL. Fail closed rather than filter quietly — a header row in
    # here means the extractor is wrong, and that is worth knowing.
    for src in ext["sources"]:
        if src["url"] in ("URL", "") or src["title"] == "Source":
            raise SystemExit(
                f"FAILED — nothing written: {EXTERNAL_JSON.name} holds a Markdown "
                f"table header as if it were a source ({src['authority']}: "
                f"{src['title']!r} / {src['url']!r}). Re-extract it from "
                f"01_research/BENCHMARK.md without the header lines.")
    by: dict[str, list] = {}
    for src in ext["sources"]:
        by.setdefault(src["authority"], []).append(src)
    out = [
        f'<p>Every claim in this book about an outside body rests on one of the '
        f'{len(ext["sources"])} sources below. Each carries the URL it was read at '
        f'and the date the source itself showed, which is not the same as the date it '
        f'was read: a page with no change log is marked as current at the check '
        f'rather than given a false date.</p>',
        f'<p class="gb-note">All checked {e(ext["platforms"]["checked"])}. The full '
        f'benchmark that produced them, with what each source was read for, is '
        f'<code>01_research/BENCHMARK.md</code>, which travels inside this file.</p>',
    ]
    for authority in sorted(by):
        rows = [[e(x["title"]), f'<code>{e(x["url"])}</code>',
                 e(x["date_on_source"])] for x in by[authority]]
        out.append(f"<h3>{e(authority)}</h3>")
        out.append(table(["Source", "URL", "Date on the source"], rows,
                         caption=f"{len(rows)} sources from {e(authority)}."))
    return "".join(out)


def chapter_type_en(tok: Tokens) -> str:
    out: list[str] = []
    cards = read_json(CARDS_JSON)
    meas = read_json(MEASUREMENTS_JSON)
    facts = read_json(FONT_FACTS_JSON)
    pairing = meas["ratios"]["08-editorial-revised"]

    out.append("<h2>Three families</h2>")
    rows = []
    # The three FAMILIES, so the desktop file is not a fourth row here — it is
    # the same face as the mono subset, in a different form, and the licence
    # chapter is where the artefacts are inventoried. This loop reads the same
    # list, so it has to say which entries it means rather than assume the list
    # only ever holds three.
    for spec in cards["_fonts"]:
        if not spec.get("subset", True):
            continue
        key = {"Literata": "literata", "Noto Serif Bengali": "notoserifbengali",
               "Aninda Mono": "ibmplexmono"}[spec["family"]]
        f = facts[key]
        axes = ", ".join(f"{a['tag']} {a['min']:g}–{a['max']:g}" for a in f["axes"]) or "none"
        rows.append([
            e(spec["family"]),
            e(f["version"]),
            e(spec["licence"]),
            axes,
            "yes" if f["rfn"] else "no",
            fmt_bytes(spec["bytes"]),
        ])
    out.append(table(["Family", "Version", "Licence", "Variable axes",
                      "Reserved Font Name", "Subset"], rows,
                     caption="The three families, read from the font files "
                             "themselves."))
    out.append(
        "<p>The mono face is IBM Plex Mono, subset and <strong>renamed</strong>. "
        "IBM Plex carries a Reserved Font Name, and subsetting counts as "
        "modification under clause 3 of the Open Font Licence, so the subset "
        "cannot keep the name. Chapter 13 sets out why the other two keep "
        "theirs.</p>")

    out.append("<h2>The scale</h2>")
    ratio = tok.prim("number.scale.ratio")["$value"]
    out.append(
        f"<p>One ratio of {ratio} — a perfect fourth — from caption to display. "
        "Sizes are in rem, so they follow the reader's own text-size setting. The "
        "pixel column assumes the browser default of 16 px.</p>")
    scale_names = ["caption", "body", "lead", "h3", "h2", "h1", "display"]
    bn_scale_for = {"caption": "caption", "body": "body", "lead": "body",
                    "h3": "heading", "h2": "heading", "h1": "title",
                    "display": "display"}
    rows = []
    bn_min = tok.prim("dimension.type.bangla-min")["$value"]["value"]
    for name in scale_names:
        rem = tok.prim(f"dimension.type.{name}")["$value"]["value"]
        px = rem * 16
        mult_key = bn_scale_for[name]
        mult = tok.prim(f"number.scale.bangla.{mult_key}")["$value"]
        bn_px = px * mult
        clamped = bn_px < bn_min
        bn_cell = f"{max(bn_px, bn_min):.1f} px"
        if clamped:
            bn_cell += f' <span class="gb-muted">(clamped up from {bn_px:.1f})</span>'
        rows.append([
            f"<code>--as-text-{e(name)}</code>",
            f"{rem:g} rem",
            f"{px:.1f} px",
            f"×{mult}",
            bn_cell,
        ])
    out.append(table(["Token", "Size", "At 16 px root", "Bangla multiplier",
                      "Bangla size"], rows,
                     caption="The type scale in rem and at a 16 px root, with the "
                             "measured Bangla multiplier for each step."))

    out.append("<h2>The families this one was chosen over</h2>")
    rows = []
    for key, p in meas["ratios"].items():
        info = meas["pairings"][key]
        chosen = key == "08-editorial-revised"
        name = (f"<b>{e(info['title'])}</b>" if chosen else e(info["title"]))
        rows.append([
            name,
            e(info["latin"]),
            e(info["bangla"]),
            f"×{p['bangla_size_multiplier_at_16']}",
            "yes" if p["varies_with_size"] else "no",
        ])
    out.append(table(["Pairing", "Latin", "Bangla", "Multiplier at 16 px",
                      "Varies with size"], rows,
                     caption="Eight pairings measured out of thirty families."))
    out.append(
        "<p>The obvious editorial pairing was Newsreader with Noto Serif Bengali, "
        "and the measurements rejected it: at ×0.708 the Bangla column is visibly "
        "smaller and lighter than the English beside it. For a brand whose two "
        "audiences are equal, that is the one failure that is not acceptable. "
        "Literata has an x-height a full pixel taller, which lifts the multiplier "
        "to ×0.816 and holds it nearly flat across the whole scale.</p>")

    return "".join(out)


def chapter_space_en(tok: Tokens) -> str:
    out: list[str] = []
    out.append("<h2>The space scale</h2>")
    out.append(
        "<p>Ten steps built on 4 px. Everything in the system sits on one of "
        "them: no padding, gap or margin anywhere in the component layer is a "
        "number typed by hand.</p>")
    space = tok.prim("dimension.space")
    rows = []
    bars = []
    for key in sorted((k for k in space if not k.startswith("$")), key=int):
        v = space[key]["$value"]["value"]
        rows.append([f"<code>--as-space-{key}</code>", f"{v:g} px",
                     f"{v / 16:g} rem"])
        bars.append(
            f'<div class="gb-bar"><div class="gb-bar__fill" style="width:{v}px"></div>'
            f'<span class="gb-bar__label"><code>{key}</code> {v:g} px</span></div>')
    out.append(f'<div class="gb-bars">{"".join(bars)}</div>')
    out.append(table(["Token", "Value", "At 16 px root"], rows,
                     caption="The ten steps of the space scale."))

    out.append("<h2>Four radii</h2>")
    radius = tok.prim("dimension.radius")
    chips = []
    rows = []
    for key in ("badge", "control", "card", "hero"):
        v = radius[key]["$value"]["value"]
        rows.append([f"<code>--as-radius-{key}</code>", f"{v:g} px",
                     {"badge": "Badges and small pills",
                      "control": "Buttons, inputs, selects",
                      "card": "Cards, dialogs, panels",
                      "hero": "The icon tile, and large surfaces"}[key]])
        chips.append(
            f'<div class="gb-radius"><div class="gb-radius__box" '
            f'style="border-radius:{v}px"></div>'
            f'<span class="gb-caption"><code>{key}</code><br>{v:g} px</span></div>')
    out.append(f'<div class="gb-radii">{"".join(chips)}</div>')
    out.append(table(["Token", "Value", "Where"], rows,
                     caption="The four radii, and what each is used on."))
    manifest = read_json(MARK_DIR / "manifest.json")
    out.append(note(
        f"<p>The hero radius is also the icon's corner rounding, at "
        f"{manifest['tile_radius_percent']:g}% of the icon width. The manifest "
        f"records where that number comes from: {e(manifest['tile_radius_source'])} "
        "Apple publishes no corner radius and does not use the word squircle "
        "anywhere in current guidance.</p>"))

    out.append("<h2>Target sizes</h2>")
    out.append(
        "<p>A target is the area a finger or a pointer can hit. Three "
        "authorities give three different minimums, and they are not "
        "interchangeable. All four figures are tokens, so the platform decides "
        "rather than habit.</p>")
    target = tok.prim("dimension.target")
    sources = {
        "min": "WCAG 2.2 criterion 2.5.8, in CSS pixels. The floor this system is held to.",
        "apple-min": "Apple's published minimum, in points, for iOS and iPadOS.",
        "comfortable": "Apple's published default, in points. The size to use unless there is a reason not to.",
        "android-min": "Android's minimum touch target, in density-independent pixels.",
    }
    rows = []
    for key in ("min", "apple-min", "comfortable", "android-min"):
        v = target[key]["$value"]["value"]
        rows.append([f"<code>--as-target-{key}</code>", f"{v:g}", sources[key]])
    out.append(table(["Token", "Size", "Where the figure comes from"], rows,
                     caption="The four target sizes, each with the guidance it "
                             "comes from."))
    out.append(note(
        "<p>A CSS pixel is the web's device-independent unit of length. It is "
        "not the same as a physical screen pixel, an Apple point or an Android "
        "density-independent pixel, which is why the three figures above cannot "
        "be compared directly or collapsed into one number.</p>"))

    out.append("<h2>The focus ring</h2>")
    fw = tok.prim("dimension.focus.ring-width")["$value"]["value"]
    fo = tok.prim("dimension.focus.ring-offset")["$value"]["value"]
    out.append(table(
        ["Token", "Value", "Why"],
        caption="The focus ring, and the criterion behind each figure.",
        rows=
        [[f"<code>--as-focus-ring-width</code>", f"{fw:g} px",
          "WCAG 2.2 criterion 2.4.13 asks for a perimeter at least 2 CSS pixels "
          "thick. 3 px clears it with room for a rounded corner."],
         [f"<code>--as-focus-ring-offset</code>", f"{fo:g} px",
          "Separates the ring from the control's own border so the two do not "
          "read as one thick edge."]]))
    out.append(
        "<p>The ring is drawn on <code>:focus</code>, not "
        "<code>:focus-visible</code>. <code>:focus-visible</code> is a browser "
        "heuristic, and a heuristic can decide not to draw the ring. Showing it "
        "once too often is a smaller failure than losing it once.</p>")
    out.append(note(
        "<p>Apple publishes <strong>no numeric focus-indicator specification at "
        "all</strong>, and its focus guidance page predates its current material "
        "system entirely. There was nothing to inherit here, so this system "
        "specifies its own numbers and meets WCAG's instead.</p>"))
    out.append("<h2>The gap between two controls</h2>")
    out.append(block_control_spacing())

    return "".join(out)


def chapter_components_en(tok: Tokens) -> str:
    cards = read_json(CARDS_JSON)
    out: list[str] = []
    counts = cards["counts"]
    total = sum(counts.values())
    out.append(
        f"<p class=\"gb-lead\">{total} cards — "
        + ", ".join(f"{v} {k.lower()}" for k, v in counts.items())
        + ". Each is a single self-contained HTML file with the tokens, the "
          "component layer and the three fonts inlined. A card opens from a file "
          "path with no network at all.</p>")

    out.append("<h2>The three rules the layer enforces</h2>")
    out.append(
        "<ol class=\"gb-list gb-list--numbered\">"
        "<li><b>No literal colour.</b> Every colour in the component layer is a "
        "<code>var(--as-…)</code> from the token file. The build scans for hex, "
        "<code>rgb()</code>, <code>hsl()</code>, <code>lab()</code>, "
        "<code>oklch()</code> and the CSS named colours, and refuses to build if "
        "it finds one. Two keywords are allowed and nothing else: "
        "<code>currentColor</code>, which is a reference rather than a value, and "
        "<code>transparent</code>, which is the only way CSS lets you express "
        "the absence of a colour.</li>"
        "<li><b>Focus is always visible.</b> Every focusable control gets a ring "
        "from <code>:focus</code>. No rule in the layer sets "
        "<code>outline: none</code>.</li>"
        "<li><b>Nothing relies on colour alone.</b> Every state carries a word "
        "and a glyph as well as a colour — a danger badge says Failed and shows a "
        "cross, a selected tab is bold and underlined, the current navigation "
        "item has a bar.</li>"
        "</ol>")
    out.append(note(
        "<p><strong>CSS cannot enforce rule 3, and this book will say so.</strong> "
        "A stylesheet has no way to know whether the markup it is styling carries "
        "a word next to the colour. A danger modifier will happily colour an "
        "empty element red. Rules 1 and 2 are machine-checked. Rule 3 lives in "
        "the markup and in review, and it is a promise rather than a "
        "guarantee.</p>"))

    out.append("<h2>Glyphs are drawn, not typed</h2>")
    out.append(
        "<p>Every glyph in the system is an inline SVG in "
        "<code>currentColor</code>. Literata has no tick, no cross and no warning "
        "triangle, so a glyph typed as a character would fall back silently to "
        "whatever font the reader's machine happens to have. Drawing them keeps "
        "the shape, the weight and the colour under the system's control, and "
        "<code>currentColor</code> means each glyph inherits both the theme and "
        "the forced-colours palette.</p>")

    for group in ("Foundations", "Components", "Patterns"):
        rows = []
        for card in cards["cards"]:
            if card["group"] != group:
                continue
            rows.append([
                f"<b>{e(card['name'])}</b>",
                card["subtitle"],
                f"{card['width']} × {card['height']}",
            ])
        out.append(f"<h2>{group} — {counts[group]}</h2>")
        out.append(table(["Card", "What it shows", "Design canvas"], rows,
                         caption=f"The {group.lower()} cards, read from 08_components/_cards.json."))

    out.append("<h2>The fonts each card carries</h2>")
    out.append(block_font_licences())

    out.append("<h2>How the cards are checked</h2>")
    out.append(
        "<p>Every card is opened in a real Chromium at 360, 768 and 1280 CSS "
        "pixels and in all four themes, and then measured. A static reading of "
        "the CSS can tell you a rule exists; it cannot tell you whether the rule "
        "reached the pixel.</p>"
        "<ul class=\"gb-list\">"
        "<li>Contrast is read off the composited effective background, walking "
        "ancestors and blending partly transparent layers. Reading an element's "
        "own background colour returns a fully transparent value for nearly every "
        "element in a real page and proves nothing.</li>"
        "<li>Interaction states are driven by a real pointer — move, down, up — "
        "and the pressed style is compared against the hovered one. Two identical "
        "readings are what a dead rule looks like from outside the browser.</li>"
        "<li>The focus indicator is measured from pixels: the element is captured "
        "unfocused and focused, the two buffers are differenced, and the changed "
        "pixels are checked for a ring at least 2 CSS pixels thick at 3:1.</li>"
        "<li>Forced colours runs a liveness probe first. If the emulation is "
        "inert the run fails as not-equipped rather than passing silently. A "
        "check that cannot fail is not a check.</li>"
        "</ul>")
    return "".join(out)


def chapter_motion_en(tok: Tokens) -> str:
    out: list[str] = []
    colour_ms = tok.prim("duration.motion.colour")["$value"]["value"]
    move_ms = tok.prim("duration.motion.move")["$value"]["value"]

    out.append(
        f'<p class="gb-lead">{colour_ms:g} ms for a colour change. {move_ms:g} ms '
        "for something arriving or leaving. Nothing in this system goes over "
        "300 ms.</p>")
    out.append(table(
        ["Token", "Value", "What it is for"],
        caption="The two durations, and what each is for.",
        rows=
        [[f"<code>--as-duration-colour</code>", f"{colour_ms:g} ms",
          "Anything that changes in place: a hover tint, a border, a background, "
          "a text colour."],
         [f"<code>--as-duration-move</code>", f"{move_ms:g} ms",
          "Anything that arrives or leaves: a dialog, a toast, a panel, a menu."]]))

    out.append("<h2>Three curves</h2>")
    out.append(
        "<p>A cubic Bézier curve is four numbers describing how a change "
        "accelerates and slows. These three are the whole set.</p>")
    rows = []
    curves = {
        "standard": "Anything that stays on screen throughout — a colour, a size, a position.",
        "enter": "Something arriving. Fast at the start, settling at the end.",
        "exit": "Something leaving. Slow to commit, then quick to go.",
    }
    for key, why in curves.items():
        v = tok.prim(f"cubicBezier.motion.{key}")["$value"]
        nums = ", ".join(f"{n:g}" for n in v)
        rows.append([
            f"<code>--as-ease-{key}</code>",
            f"<code>cubic-bezier({nums})</code>",
            f'<svg class="gb-curve" viewBox="-8 -18 116 136" aria-hidden="true">'
            f'<rect class="gb-curve__frame" x="0" y="0" width="100" height="100"/>'
            f'<path class="gb-curve__line" d="M0 100C{v[0]*100:.1f} {100-v[1]*100:.1f} '
            f'{v[2]*100:.1f} {100-v[3]*100:.1f} 100 0"/></svg>',
            why,
        ])
    out.append(table(["Token", "Curve", "Shape", "Where"], rows,
                     caption="The three easing curves, drawn from their own control points."))

    out.append("<h2>Material's spring system was read, and not adopted</h2>")
    out.append(
        "<p>Material 3 publishes a spring-based motion system: two schemes, each "
        "with six specifications on a grid of three speeds by two kinds of "
        "motion. The expressive scheme's spatial values are damping 0.8 with "
        "stiffness 380 at default, 0.6 with 800 fast, and 0.8 with 200 slow; its "
        "effects values are damping 1.0 with stiffness 1600, 3800 and 800. Those "
        "figures were checked on 14 August 2026.</p>")
    out.append(
        "<p><strong>This system does not adopt them, for three reasons.</strong> "
        "A spring needs a physics integrator at run time, and this kit is a "
        "stylesheet — it has no run time of its own. A spring's duration is an "
        "outcome rather than a setting, which makes it far harder to hold to a "
        "stated ceiling. And Material did not replace its own duration and easing "
        "tokens when it added springs: 16 durations and 10 easing curves remain "
        "published. A kit built on durations and cubic Bézier curves is not out "
        "of date relative to Material. It is using the other half of a system "
        "that publishes both halves.</p>")
    out.append(note(
        "<p><strong>The principle underneath their numbers does transfer, and "
        "this system takes it.</strong> Every effects damping in Material's "
        "scheme is exactly 1.0 — critically damped, meaning it never overshoots. "
        "Every spatial damping is below 1.0 — underdamped, meaning it overshoots "
        "and settles. So: <b>things that move may overshoot; things that only "
        "change colour never do.</b> That is why "
        "<code>--as-duration-colour</code> and <code>--as-duration-move</code> "
        "are two tokens and not one, and why the enter and exit curves are only "
        "ever applied to things that arrive or leave.</p>"))

    out.append("<h2>Apple publishes no durations at all</h2>")
    out.append(
        "<p>Apple's motion guidance is principled rather than numeric: add motion "
        "purposefully, keep it brief, show restraint on frequent interactions, "
        "let people cancel it. The only two figures anywhere in it are that games "
        "should run at 30 to 60 frames per second, and that visionOS should avoid "
        "sustained oscillation at around 0.2 Hz. Neither applies to a studio "
        "identity system. <strong>Every duration and curve in this kit is this "
        "kit's own, and presenting any of them as Apple-aligned would be "
        "false.</strong></p>")

    out.append("<h2>Reduced motion</h2>")
    out.append(
        "<p>When the reader has asked their system for reduced motion, both "
        "durations collapse to 1 ms at the root. Nothing is left half-animated "
        "and nothing needs a second rule further down the tree.</p>")
    out.append(
        "<pre class=\"gb-code\"><code>@media (prefers-reduced-motion: reduce) {\n"
        "  :root {\n"
        "    --as-duration-colour: 1ms;\n"
        "    --as-duration-move: 1ms;\n"
        "  }\n}</code></pre>")
    out.append(
        "<p>The substitution rule, inherited from Apple's own reduced-motion "
        "techniques, is to replace a movement with a <strong>fade</strong> — "
        "never a spatial move and never a blur, and never an animation into or "
        "out of a blur.</p>")
    return "".join(out)


def render_markdown(path: Path, print_mode: bool) -> str:
    text = path.read_text(encoding="utf-8")

    # Block placeholders become a marker paragraph, replaced after conversion.
    markers: dict[str, str] = {}
    counter = [0]

    def stash(html_fragment: str) -> str:
        counter[0] += 1
        key = f"GBBLOCK{counter[0]}ZZ"
        markers[key] = html_fragment
        return key

    def block_sub(match):
        kind = match.group(1)
        name = match.group(2) if match.re.groups > 1 else ""
        if kind == "figure":
            return stash({
                "marks": block_figure_marks,
                "icons": block_figure_icons,
                "wordmarks": block_figure_wordmarks,
                "construction": block_figure_construction,
            }[name]())
        if kind == "data":
            builders = {
                "mark-geometry": block_mark_geometry,
                "mark-strokes": block_mark_strokes,
                "mark-files": block_mark_files,
                "icon-files": block_icon_files,
                "icon-mask-measurement": block_icon_mask_measurement,
                "icon-visual-parity": block_icon_visual_parity,
                "publication": block_publication,
                "bangla-removed": block_bangla_removed,
                "font-licences": block_font_licences,
                "kit-index": block_kit_index,
                "banned-words": block_banned_words,
                "banned-latin": block_banned_latin,
                "sources": block_sources,
            }
            if name == "output-files":
                return stash(block_output_files(print_mode))
            return stash(builders[name]())
        raise BuildError(f"{path.name}: unknown placeholder {{{{{kind}:{name}}}}}")

    text = re.sub(r"\{\{(figure|data):([a-z0-9\-]+)\}\}", block_sub, text)

    # Pulled out before Markdown runs, in document order, so each caption stays
    # with the table it was written above.
    captions = [c.strip() for c in re.findall(r"^\{\{table:\s*(.+?)\}\}\s*$",
                                              text, re.M)]
    text = re.sub(r"^\{\{table:\s*.+?\}\}\s*$\n?", "", text, flags=re.M)

    md = markdown_mod.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    body = md.convert(text)
    body = fix_markdown_tables(body, path.name, captions)

    for key, fragment in markers.items():
        body = body.replace(f"<p>{key}</p>", fragment)
        body = body.replace(key, fragment)
    return body


def fix_markdown_tables(body: str, source: str, captions: list[str]) -> str:
    """Give a markdown table the headers and caption the generator's tables have.

    Python-Markdown's tables extension emits a bare <th> with no scope, a <tbody>
    whose first cell is a <td>, and no caption at all — so seventeen of the book's
    column headers declared no scope and seven of its tables had no row header even
    after table() above was fixed. A screen reader in table mode needs both.

    Three changes, all mechanical:
      * scope="col" on every <th> in the <thead>;
      * the first cell of every body row becomes <th scope="row">;
      * a <caption>, taken from the `{{table:…}}` marker the chapter puts
        immediately above the table. The caption is AUTHORED, not lifted from the
        nearest sentence: the first version of this took the preceding paragraph
        and captioned the name table "Both forms are correct", which is true of
        the paragraph and says nothing about the rows. A guessed caption is worse
        than none, because it looks deliberate. A table with no marker fails the
        build.

    Every markdown table in this book has a first column that is the row's
    identity — Part, Stage, Situation, Use, "Use this" — which is why the promotion
    is unconditional here. A table whose first column is a measure belongs in
    table(row_header=False) in this file, not in chapter markdown.
    """
    out: list[str] = []
    position = 0
    pending = list(captions)
    for match in re.finditer(r"<table>(.*?)</table>", body, re.S):
        inner = match.group(1)
        before = body[position:match.start()]
        if not pending:
            raise BuildError(
                f"{source}: a table has no caption. Put a line reading "
                f"{{{{table: what these rows are}}}} immediately above it. Every "
                f"table in this book states what its rows are."
            )
        sentence = pending.pop(0)

        head, sep, rest = inner.partition("</thead>")
        if not sep:
            raise BuildError(f"{source}: a markdown table has no <thead>")
        head = head.replace("<th>", '<th scope="col">')
        rest = re.sub(r"<tr>\s*<td>", '<tr>\n<th scope="row">', rest)
        rest = re.sub(r'(<th scope="row">(?:(?!</td>).)*?)</td>', r"\1</th>", rest,
                      flags=re.S)
        out.append(before)
        out.append(f"<table><caption>{e(sentence)}</caption>{head}</thead>{rest}</table>")
        position = match.end()
    out.append(body[position:])
    if pending:
        raise BuildError(
            f"{source}: {len(pending)} {{{{table:…}}}} caption(s) with no table "
            f"under them — {pending}. A caption that captions nothing is a caption "
            f"that has drifted off its table."
        )
    return "".join(out)


# ---------------------------------------------------------------------------
# Stylesheet
#
# Every colour here is a var(--as-…) from the token file. The build refuses to
# finish if a literal colour reaches this string. `transparent` and
# `currentColor` are the two allowed keywords, for the same reason the component
# layer allows them: one is the absence of a colour, the other is a reference.
# ---------------------------------------------------------------------------

GUIDEBOOK_CSS = """
.gb-page {
  background-color: var(--as-surface-low);
  color: var(--as-ink);
  font-family: var(--as-font-latin);
  font-size: var(--as-text-body);
  line-height: 1.6;
  margin: 0;
  overflow-wrap: break-word;
}
.gb-shell { max-width: 62rem; margin: 0 auto; padding: var(--as-space-4); }
.gb-prose { max-width: 42rem; }

.gb-bar-top {
  position: sticky; top: 0; z-index: 20;
  display: flex; flex-wrap: wrap; align-items: center; gap: var(--as-space-2);
  padding: var(--as-space-2) var(--as-space-4);
  background-color: var(--as-surface-bright);
  border-block-end: 1px solid var(--as-line);
}
.gb-bar-top__name { font-weight: 700; margin-inline-end: auto; }
.gb-bar-top__name svg { inline-size: 1.4em; block-size: 1.4em; vertical-align: -0.3em; }
.gb-langbtn {
  font: inherit; font-size: var(--as-text-caption);
  padding: var(--as-space-0) var(--as-space-2);
  min-block-size: var(--as-target-min);
  border: 1px solid var(--as-line);
  border-radius: var(--as-radius-control);
  background-color: var(--as-surface-lowest);
  color: var(--as-ink);
  cursor: pointer;
  transition: background-color var(--as-duration-colour) var(--as-ease-standard),
              color var(--as-duration-colour) var(--as-ease-standard);
}
.gb-langbtn[aria-pressed="true"] {
  background-color: var(--as-accent); color: var(--as-surface-lowest);
  border-color: var(--as-accent);
}
.gb-page :is(a, button, summary, [tabindex]):focus {
  outline: var(--as-focus-ring-width) solid var(--as-focus-ring);
  outline-offset: var(--as-focus-ring-offset);
}

.gb-cover { padding-block: var(--as-space-8) var(--as-space-7); }
.gb-cover__mark svg { inline-size: 7rem; block-size: 7rem; color: var(--as-ink); }
.gb-cover h1 { font-size: var(--as-text-display); line-height: 1.05; margin: var(--as-space-4) 0 0; }
.gb-cover__bn { font-size: var(--as-text-h2); color: var(--as-ink-muted); margin: var(--as-space-1) 0 0; }
.gb-cover__lede { font-size: var(--as-text-lead); max-width: 34rem; margin-block-start: var(--as-space-4); }
.gb-cover__meta { margin-block-start: var(--as-space-5); font-size: var(--as-text-caption); color: var(--as-ink-muted); }

.gb-toc ol { list-style: none; padding: 0; margin: 0; }
.gb-toc li { border-block-start: 1px solid var(--as-line); }
.gb-toc a { display: flex; gap: var(--as-space-3); padding: var(--as-space-2) 0; color: var(--as-ink); text-decoration: none; align-items: baseline; }
.gb-toc a:hover { color: var(--as-accent); }
.gb-toc__num { font-family: var(--as-font-mono); font-variant-ligatures: none; color: var(--as-ink-muted); font-size: var(--as-text-caption); }
.gb-toc__title { font-weight: 600; }
.gb-toc__bn { color: var(--as-ink-muted); }
.gb-toc__stand { display: block; font-size: var(--as-text-caption); color: var(--as-ink-muted); font-weight: 400; }

.gb-chapter { padding-block-start: var(--as-space-7); }
.gb-chapter__head { border-block-start: 2px solid var(--as-accent); padding-block-start: var(--as-space-3); }
.gb-chapter__num { font-family: var(--as-font-mono); font-variant-ligatures: none; color: var(--as-accent); font-size: var(--as-text-caption); }
.gb-chapter h2.gb-chapter__title { font-size: var(--as-text-h1); line-height: 1.1; margin: var(--as-space-1) 0 0; }
.gb-chapter__stand { font-size: var(--as-text-lead); color: var(--as-ink-muted); max-width: 38rem; margin-block-start: var(--as-space-2); }
.gb-section { margin-block-start: var(--as-space-5); }
.gb-section__label {
  display: inline-block; font-size: var(--as-text-caption);
  font-family: var(--as-font-mono); font-variant-ligatures: none;
  border: 1px solid var(--as-line); border-radius: var(--as-radius-badge);
  padding: 0 var(--as-space-0); color: var(--as-ink-muted);
  margin-block-end: var(--as-space-2);
}
.gb-section h2 { font-size: var(--as-text-h2); line-height: 1.15; margin-block: var(--as-space-6) var(--as-space-2); }
.gb-section h3 { font-size: var(--as-text-h3); line-height: 1.2; margin-block: var(--as-space-5) var(--as-space-2); }
.gb-section h4 { font-size: var(--as-text-lead); margin-block: var(--as-space-4) var(--as-space-1); }
.gb-section p, .gb-section ul, .gb-section ol, .gb-section dl { max-width: 42rem; }
/* components.css zeroes every block margin, which is right for a component and
   wrong for running prose. Paragraph rhythm is restored here and nowhere else. */
.gb-section > p, .gb-section > ul, .gb-section > ol, .gb-section > dl,
.gb-section > blockquote, .gb-section > pre, .gb-ramp > p, .gb-theme > p {
  margin-block: 0 var(--as-space-3);
}
.gb-note p + p { margin-block-start: var(--as-space-2); }
.gb-lead { font-size: var(--as-text-lead); }
.gb-muted { color: var(--as-ink-muted); }

.gb-scroll-x { overflow-x: auto; margin-block: var(--as-space-3); }
.gb-table { border-collapse: collapse; inline-size: 100%; font-size: var(--as-text-caption); }
.gb-table caption { text-align: start; color: var(--as-ink-muted); padding-block-end: var(--as-space-1); }
.gb-table th, .gb-table td { text-align: start; vertical-align: top; padding: var(--as-space-1) var(--as-space-2); border-block-end: 1px solid var(--as-line); }
.gb-table thead th { border-block-end: 2px solid var(--as-line); white-space: nowrap; }
.gb-table code { font-family: var(--as-font-mono); font-variant-ligatures: none; }

.gb-note {
  border-inline-start: 3px solid var(--as-accent-edge);
  background-color: var(--as-surface-high);
  padding: var(--as-space-3);
  border-radius: var(--as-radius-control);
  margin-block: var(--as-space-3);
  max-width: 42rem;
}
.gb-note--gap { border-inline-start-color: var(--as-warning); }
.gb-note p { margin: 0 0 var(--as-space-1); }
.gb-note p:last-child { margin-block-end: 0; }

.gb-quote {
  margin: var(--as-space-3) 0; padding: var(--as-space-3);
  border-inline-start: 3px solid var(--as-accent);
  background-color: var(--as-surface-high);
  border-radius: var(--as-radius-control);
  font-size: var(--as-text-lead);
}
.gb-defs dt { font-weight: 700; margin-block-start: var(--as-space-2); }
.gb-defs dd { margin: 0 0 0 var(--as-space-3); }
.gb-list { padding-inline-start: var(--as-space-4); }
.gb-list li { margin-block-end: var(--as-space-1); }
.gb-code, pre {
  font-family: var(--as-font-mono); font-variant-ligatures: none;
  font-size: var(--as-text-caption);
  background-color: var(--as-surface-highest);
  border: 1px solid var(--as-line);
  border-radius: var(--as-radius-control);
  padding: var(--as-space-2); overflow-x: auto;
}
code { font-family: var(--as-font-mono); font-variant-ligatures: none; }

.gb-figure { display: flex; flex-wrap: wrap; gap: var(--as-space-4); margin: var(--as-space-4) 0; padding: 0; }
.gb-caption { font-size: var(--as-text-caption); color: var(--as-ink-muted); margin: var(--as-space-1) 0 0; }
.gb-markbox__art, .gb-iconbox__art {
  background-color: var(--as-surface-bright);
  border: 1px solid var(--as-line);
  border-radius: var(--as-radius-card);
  padding: var(--as-space-4);
  display: grid; place-items: center;
}
.gb-mark { inline-size: 7rem; block-size: 7rem; color: var(--as-ink); }
.gb-icon { inline-size: 5rem; block-size: 5rem; }
.gb-iconbox { inline-size: 9rem; }
.gb-wordbox { flex: 1 1 18rem; background-color: var(--as-surface-bright); border: 1px solid var(--as-line); border-radius: var(--as-radius-card); padding: var(--as-space-4); }
.gb-wordmark { inline-size: 100%; block-size: auto; color: var(--as-ink); }
.gb-construction { inline-size: 16rem; block-size: 16rem; }
.gb-c-grid { stroke: var(--as-line); stroke-width: 0.25; opacity: 0.45; }
.gb-c-frame { fill: none; stroke: var(--as-line); stroke-width: 0.5; }
.gb-c-guide { fill: none; stroke: var(--as-accent-edge); stroke-width: 0.5; stroke-dasharray: 2 2; }
.gb-c-art { fill: none; stroke: var(--as-ink); stroke-width: 9; stroke-linecap: round; }
.gb-c-dot { fill: var(--as-danger); stroke: none; }

.gb-swatches { display: flex; flex-wrap: wrap; gap: var(--as-space-1); margin-block: var(--as-space-2); }
.gb-swatch { inline-size: 5.5rem; }
.gb-swatch__chip { block-size: 3rem; border-radius: var(--as-radius-badge); }
.gb-swatch__chip--bordered { border: 1px solid var(--as-line); }
.gb-swatch__meta { font-size: var(--as-text-caption); display: flex; flex-direction: column; }
.gb-swatch__meta code { font-size: 0.85em; }
.gb-dot { display: inline-block; inline-size: 0.8em; block-size: 0.8em; border-radius: var(--as-radius-badge); border: 1px solid var(--as-line); vertical-align: -0.05em; }
.gb-ramp { margin-block-start: var(--as-space-5); }
.gb-theme { margin-block-start: var(--as-space-6); }

.gb-bars { margin-block: var(--as-space-3); }
.gb-bar { display: flex; align-items: center; gap: var(--as-space-2); margin-block-end: var(--as-space-0); }
.gb-bar__fill { block-size: 0.75rem; background-color: var(--as-accent-edge); border-radius: var(--as-radius-badge); flex: none; }
.gb-bar__label { font-size: var(--as-text-caption); color: var(--as-ink-muted); }
.gb-radii { display: flex; flex-wrap: wrap; gap: var(--as-space-3); margin-block: var(--as-space-3); }
.gb-radius { text-align: center; }
.gb-radius__box { inline-size: 4rem; block-size: 4rem; background-color: var(--as-surface-highest); border: 1px solid var(--as-line); }
.gb-curve { inline-size: 4rem; block-size: 4rem; }
.gb-curve__frame { fill: none; stroke: var(--as-line); stroke-width: 1.5; }
.gb-curve__line { fill: none; stroke: var(--as-accent); stroke-width: 4; }

.gb-details { border: 1px solid var(--as-line); border-radius: var(--as-radius-control); padding: var(--as-space-2); margin-block: var(--as-space-3); }
.gb-details summary { cursor: pointer; font-weight: 600; }

.gb-kit li { margin-block-end: var(--as-space-1); }
.gb-kit__label { font-family: var(--as-font-mono); font-variant-ligatures: none; font-size: var(--as-text-caption); }
.gb-kit__what { color: var(--as-ink-muted); font-size: var(--as-text-caption); }

.gb-colophon { margin-block-start: var(--as-space-8); border-block-start: 1px solid var(--as-line); padding-block-start: var(--as-space-4); font-size: var(--as-text-caption); color: var(--as-ink-muted); }

@media (max-width: 40rem) {
  .gb-shell { padding: var(--as-space-3); }
  .gb-cover h1 { font-size: var(--as-text-h1); }
}
"""

PRINT_CSS = """
@page { size: A4; margin: 14mm; }
.gb-bar-top { display: none; }
.gb-page { background-color: var(--as-surface-bright); font-size: 10.5pt; }
.gb-shell { max-width: none; padding: 0; }
.gb-cover { padding-block: 0 var(--as-space-6); break-after: page; }
.gb-toc { break-after: page; }
.gb-toc li, .gb-toc a { break-inside: avoid; }
/* Fifteen entries have to fit one A4 page, or the break-after rule leaves a
   near-empty page 3 carrying one line. */
.gb-toc h2 { font-size: 16pt; margin-block: 0 6pt; }
.gb-toc a { padding: 3.2pt 0; }
.gb-toc__stand { font-size: 7.6pt; }
.gb-chapter { break-before: page; padding-block-start: 0; }
.gb-chapter__head, .gb-section h2, .gb-section h3, .gb-section h4 { break-after: avoid; }
.gb-table, .gb-figure, .gb-note, .gb-quote, .gb-swatch, .gb-radius,
.gb-markbox, .gb-iconbox, .gb-wordbox, .gb-ramp, .gb-bar, pre { break-inside: avoid; }
.gb-theme { break-before: page; }
.gb-scroll-x { overflow-x: visible; }
.gb-details { border: none; padding: 0; }
.gb-details summary { list-style: none; }
.gb-details summary::-webkit-details-marker { display: none; }
.gb-table { font-size: 8pt; }
.gb-table th, .gb-table td { padding: 2pt 4pt; }
.gb-cover h1 { font-size: 32pt; }
.gb-section h2 { font-size: 18pt; }
.gb-chapter h2.gb-chapter__title { font-size: 24pt; }
a { color: var(--as-ink); text-decoration: none; }
"""

TOGGLE_JS = """
(function () {
  var buttons = document.querySelectorAll('[data-set-lang]');
  function apply(lang) {
    document.querySelectorAll('[data-lang]').forEach(function (node) {
      node.hidden = node.getAttribute('data-lang') !== lang;
    });
    buttons.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-set-lang') === lang));
    });
  }
  buttons.forEach(function (b) {
    b.addEventListener('click', function () { apply(b.getAttribute('data-set-lang')); });
  });
  apply('en');
})();
"""


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def build_document(print_mode: bool) -> str:
    tok = Tokens()
    fonts = load_fonts()
    tokens_css = TOKENS_CSS.read_text(encoding="utf-8")
    components_css = COMPONENTS_CSS.read_text(encoding="utf-8")

    generated_en = {
        "05": chapter_colour_en, "06": chapter_type_en, "07": chapter_space_en,
        "08": chapter_components_en, "09": chapter_motion_en,
    }
    # --- chapters ---------------------------------------------------------
    chapter_html: list[str] = []
    toc_items: list[str] = []
    for num, slug, title, source in CHAPTERS:
        if source == "file":
            en_body = render_markdown(HERE / "chapters" / f"{num}-{slug}.md",
                                      print_mode)
        else:
            en_body = generated_en[num](tok)

        chapter_html.append(
            f'<article class="gb-chapter" id="ch-{num}">'
            f'<header class="gb-chapter__head">'
            f'<p class="gb-chapter__num">Chapter {num}</p>'
            f'<h2 class="gb-chapter__title">{e(title)}</h2>'
            f'<p class="gb-chapter__stand">{e(CHAPTER_STANDFIRST[num])}</p>'
            f"</header>"
            # The section keeps data-lang and lang, and both are still
            # load-bearing: lang="en" is what a screen reader picks a voice from,
            # and it has to be stated rather than inherited. The Bangla sibling
            # that sat beside this one carried lang="bn" for the same reason —
            # without it a screen reader pronounced Bengali with an English engine
            # (WCAG 2.2 SC 3.1.2, Level AA) and none of the Bangla typography
            # applied. That section, and the toggle that switched to it, went with
            # the Bangla on 27 August 2026.
            f'<section class="gb-section" data-lang="en" lang="en" id="ch-{num}-en">'
            f'<p class="gb-section__label">English</p>{en_body}</section>'
            f"</article>"
        )
        toc_items.append(
            f'<li><a href="#ch-{num}"><span class="gb-toc__num">{num}</span>'
            f'<span class="gb-toc__title">{e(title)} '
            f'<span class="gb-toc__stand">{e(CHAPTER_STANDFIRST[num])}</span>'
            f"</span></a></li>"
        )

    # --- the kit ----------------------------------------------------------
    items = kit_files()
    kit_rows = []
    for display, path, what in items:
        size = fmt_bytes(path.stat().st_size)
        if print_mode:
            link = f'<span class="gb-kit__label">{e(display)}</span>'
        else:
            uri = data_uri(path)
            link = (f'<a class="gb-kit__label" href="{uri}" '
                    f'download="{e(Path(display).name)}">{e(display)}</a>')
        kit_rows.append(
            f'<li>{link} <span class="gb-kit__what">— {e(what)} · {size}</span></li>')
    kit_note = (
        "<p>Each name below is a download link, and the link's target is the "
        "file itself, carried inside this document. Nothing is fetched.</p>"
        if not print_mode else
        "<p><strong>The download links are stripped in the print build.</strong> "
        "Their names are kept. A paper page cannot be clicked, so the payloads "
        "buy a printed reader nothing while making the PDF about ten times "
        "larger. Chapter 12 gives the measured figures. Open "
        "<code>Aninda-Studio-Guidebook.html</code> for the files themselves.</p>")

    kit_section = (
        '<article class="gb-chapter" id="kit">'
        '<header class="gb-chapter__head">'
        '<p class="gb-chapter__num">The kit</p>'
        '<h2 class="gb-chapter__title">Every file, in this file</h2>'
        f'<p class="gb-chapter__stand">{len(items)} files, '
        f'{fmt_bytes(sum(p.stat().st_size for _, p, _ in items))} on disk.</p>'
        "</header>"
        f'<section class="gb-section">{kit_note}'
        f'<ul class="gb-list gb-kit">{"".join(kit_rows)}</ul></section></article>'
    )

    # --- head and frame ---------------------------------------------------
    cover_mark = inline_svg("mark-regular.svg", "gb-cover-mark",
                            "The Aninda Studio mark", theme_aware=True)
    bar_mark = inline_svg("mark-regular.svg", "gb-bar-mark", "Aninda Studio",
                          theme_aware=True)

    style = "\n".join([
        font_face_css(fonts),
        tokens_css,
        components_css,
        GUIDEBOOK_CSS,
        PRINT_CSS if print_mode else "",
    ])

    header_comment = (
        "<!--\n"
        f"  Aninda Studio — the brand guidebook. Version {VERSION}.\n"
        f"  GENERATED FILE, written by {GENERATOR}. Do not hand-edit:\n"
        "  change the chapter markdown or the token sources and re-run.\n"
        f"      Build:  ./.venv/bin/python {GENERATOR}\n"
        f"      Verify: ./.venv/bin/python {GENERATOR} --check\n"
        f"  Sources verified {SOURCE_DATE}.\n"
        + ("  This is the PRINT build: the download data URIs are stripped and\n"
           "  their labels kept as text, and A4 page geometry is applied.\n"
           if print_mode else
           "  This is the INTERACTIVE build: every file in the kit is inlined as\n"
           "  its own base64 data URI. Use the print build for the PDF.\n")
        + "  The design system is Apache-2.0. The writing is\n"
          "  PolyForm-Noncommercial-1.0.0. The identity is not licensed.\n"
          "  Copyright 2026 Aninda Sundar Howlader.\n"
        "-->\n"
    )

    toggle = "" if print_mode else (
        # The bar was a language switch, with two buttons and a group role. One
        # language needs neither, so what is left is the name — a group of one
        # control is not a group, and announcing it as one is worse than not.
        '<div class="gb-bar-top">'
        f'<span class="gb-bar-top__name">{bar_mark} Aninda Studio</span>'
        "</div>"
    )
    script = "" if print_mode else f"<script>{TOGGLE_JS}</script>"

    cover = (
        '<header class="gb-cover">'
        f'<div class="gb-cover__mark">{cover_mark}</div>'
        "<h1>The Aninda Studio guidebook</h1>"
        '<p class="gb-cover__lede">The mark, the colour, the type, the '
        "components, the words, the licences, and the honest list of what is "
        "missing. One file, no network.</p>"
        f'<p class="gb-cover__meta">Version {e(VERSION)} · sources verified '
        f"{e(SOURCE_DATE)} · Aninda Sundar Howlader, Barishal, Bangladesh · "
        "aninda.sh15@gmail.com<br>"
        f"Generated by <code>{e(GENERATOR)}</code>. This file is not "
        "hand-edited.</p>"
        "</header>"
    )

    toc = (
        '<nav class="gb-toc" aria-labelledby="toc-h">'
        '<h2 id="toc-h">Contents</h2>'
        f'<ol>{"".join(toc_items)}'
        '<li><a href="#kit"><span class="gb-toc__num">—</span>'
        '<span class="gb-toc__title">Every file, in this file'
        '<span class="gb-toc__stand">The whole kit, with a download link for '
        "each file.</span></span></a></li>"
        "</ol></nav>"
    )

    colophon = (
        '<footer class="gb-colophon">'
        f"<p>Generated by <code>{e(GENERATOR)}</code> from the sources in this "
        "repository. Do not hand-edit this file — change the sources and re-run. "
        f"<code>build.py --check</code> proves it has not drifted.</p>"
        f"<p>Version {e(VERSION)} · sources verified {e(SOURCE_DATE)} · "
        "design system Apache-2.0 · writing PolyForm-Noncommercial-1.0.0 · "
        "typefaces SIL OFL 1.1 · the name, mark, wordmark, tile and lockups are "
        "not licensed. Copyright 2026 Aninda Sundar Howlader. Not legal advice.</p>"
        "</footer>"
    )

    return (
        "<!DOCTYPE html>\n"
        + header_comment
        + '<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>The Aninda Studio guidebook</title>\n"
        '<meta name="author" content="Aninda Sundar Howlader">\n'
        '<meta name="generator" content="' + e(GENERATOR) + '">\n'
        f"<style>{style}</style>\n"
        "</head>\n"
        '<body class="as-root gb-page">\n'
        + toggle
        + '<main class="gb-shell">'
        + cover + toc + "".join(chapter_html) + kit_section + colophon
        + "</main>\n"
        + script
        + "\n</body>\n</html>\n"
    )


# ---------------------------------------------------------------------------
# Guards — all of them run before anything is written
# ---------------------------------------------------------------------------

BANNED_WORDS = ["simply", "just", "easy", "obviously", "clearly"]
BANNED_PHRASES = ["of course", "e.g.", "i.e.", "etc."]

BENGALI_RUN = re.compile(r"[ঀ-৿‌‍]+")
LITERAL_COLOUR = re.compile(
    r"#[0-9a-f]{3,8}\b|\b(?:rgb|rgba|hsl|hsla|hwb|lab|lch|oklch|oklab|color)\s*\(",
    re.IGNORECASE,   # third copy of the same guard; hwb() was also missing
)


def strip_tags(html_text: str) -> str:
    """Reduce a document to the words a reader sees.

    Script, style and comments go, because none of them is prose. So does any
    element marked `data-verbatim`: that attribute marks the one place in the
    book where a banned word is printed on purpose, which is the chapter that
    bans it. The exemption is narrow, it is named here, and it is the only one.
    """
    text = re.sub(r"<script\b.*?</script>", " ", html_text, flags=re.S | re.I)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<p\b[^>]*\bdata-verbatim\b[^>]*>.*?</p>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return html_mod.unescape(text)


_BANGLA_RUN = re.compile(r"[\u0980-\u09FF][\u0980-\u09FF\s\u200c\u200d।,;:!?()\u2014-]*[\u0980-\u09FF]|[\u0980-\u09FF]")
_ENGLISH_RUN = re.compile(
    r"[A-Za-z][A-Za-z0-9\s.,;:!?()\u2019'\u2014/&%-]*[A-Za-z0-9.)]|[A-Za-z]{2,}"
)
# An HTML character reference is ONE character to a reader and a unit the parser
# will not let a tag divide. _ENGLISH_RUN's character class contains both & and ;,
# so a run could start inside `&quot;` and end inside the next one — which is what
# happened. The Bangla chapter's copy of the one CSS rule the Bangla half depends
# on shipped as `:lang(bn), [lang=&quot;bn";] {` and Chromium parsed it to ZERO
# rules: a selector list is unforgiving, so the valid `:lang(bn)` half went with
# it. A reader who copied the sample got nothing.
#
# Masking these out before tagging makes the split structurally impossible rather
# than merely unlikely, and it keeps & and ; usable inside a run — a literal
# ampersand in prose and a semicolon inside a CSS declaration both still tag as
# one piece. guard_split_entities re-checks the output; the pattern is general and
# the next Bangla chapter that quotes markup would break the same way.
_ENTITY = re.compile(r"&(?:[a-zA-Z][a-zA-Z0-9]{1,31}|#[0-9]{1,7}|#[xX][0-9a-fA-F]{1,6});")

_SKIP_ELEMENTS = ("script", "style", "title", "textarea")


def _sub_outside_entities(pattern: re.Pattern, repl, text: str) -> str:
    """Apply `pattern.sub` to every part of `text` that is not a character
    reference, leaving the references themselves untouched and intact."""
    out, last = [], 0
    for m in _ENTITY.finditer(text):
        out.append(pattern.sub(repl, text[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(pattern.sub(repl, text[last:]))
    return "".join(out)


def walk_scopes(doc: str, markers: tuple[str, ...] = ()):
    """Yield (text, nearest_declared_lang, markers_in_scope) for every text run.

    The one element stack in this project. `markers` are substrings — normally
    class names — whose enclosing scope the caller also needs; each yielded run
    reports the set of them that are open around it.

    The generalisation exists because 11_site/build.py had a FOURTH stack of its
    own, `text_runs`, deciding which font must cover each run. It was the weaker
    design this consolidation replaced: it popped on any closing tag without
    matching the name, its void-element list was missing area, base, col, embed,
    param, track and wbr, and it pushed comments and the doctype as openers, so
    its stack ran permanently four frames out of balance. It happened to agree
    with this walker on both site pages, which is the only reason nothing wrong
    shipped. Rather than add a fifth rule, the site now asks this one for the two
    class scopes it cares about.
    """
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
            "meta", "param", "source", "track", "wbr"}
    stack: list[tuple[str, str | None, frozenset[str]]] = []

    for token in re.split(r"(<[^>]+>)", doc):
        if token.startswith("<"):
            m = re.match(r"</?\s*([a-zA-Z0-9-]+)", token)
            tag = m.group(1).lower() if m else ""
            # A comment or a doctype is not an element and must never be pushed.
            if token.startswith(("<!--", "<!")):
                yield token, None, frozenset()
                continue
            if token.startswith("</"):
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i][0] == tag:
                        del stack[i:]
                        break
            elif not token.rstrip().endswith("/>") and tag not in VOID:
                lm = re.search(r'\blang="([a-zA-Z-]+)"', token)
                here = frozenset(k for k in markers if k in token)
                stack.append((tag, lm.group(1).lower() if lm else None, here))
            yield token, None, frozenset()          # tags pass through unchanged
            continue

        if any(t in _SKIP_ELEMENTS for t, _, _ in stack):
            yield token, "skip", frozenset()
            continue

        lang = None
        for _, declared, _ in reversed(stack):
            if declared:
                lang = declared
                break
        open_marks = frozenset().union(*(m for _, _, m in stack)) if stack else frozenset()
        yield token, lang, open_marks


def walk_language_scopes(doc: str):
    """Yield (text, nearest_declared_lang) for every text run in the document.

    The single source of truth for "what language is this run in". The tagger and
    the guard both use it, because the previous version had each carry its own
    scope tracking and they drifted the moment one was improved: the tagger got a
    proper element stack, the guard kept a bare counter that closed a scope on the
    first closing tag of any kind, and the guard then reported 76 faults in a
    document that was correct.

    Two implementations of the same rule is one implementation and one liability.
    """
    for token, lang, _ in walk_scopes(doc):
        yield token, lang


def guard_english(documents: dict[str, str]) -> None:
    for label, doc in documents.items():
        text = strip_tags(doc)
        # Quoted matter and code identifiers are not this book's own prose, but
        # nothing in this book quotes a banned word, so the check is unqualified.
        for word in BANNED_WORDS:
            hit = re.search(rf"\b{word}\b", text, flags=re.I)
            if hit:
                context = text[max(0, hit.start() - 70):hit.end() + 70]
                raise BuildError(
                    f"{label}: the ENGLISH-STANDARD blocklist word '{word}' "
                    f"reached the book. Context: …{context.strip()}…")
        for phrase in BANNED_PHRASES:
            if re.search(re.escape(phrase), text, flags=re.I):
                raise BuildError(
                    f"{label}: the banned phrase '{phrase}' reached the book.")
        if "!" in text:
            hit = text.index("!")
            raise BuildError(
                f"{label}: an exclamation mark reached the book. Context: "
                f"…{text[max(0, hit - 70):hit + 70].strip()}…")


def guard_placeholders(documents: dict[str, str]) -> None:
    for label, doc in documents.items():
        hit = re.search(r"\{\{[^}]{0,60}\}\}", doc)
        if hit:
            raise BuildError(f"{label}: unresolved placeholder {hit.group(0)}")
        hit = re.search(r"GBBLOCK\d+ZZ", doc)
        if hit:
            raise BuildError(f"{label}: a block marker survived: {hit.group(0)}")


def guard_own_css() -> None:
    for name, sheet in (("GUIDEBOOK_CSS", GUIDEBOOK_CSS), ("PRINT_CSS", PRINT_CSS)):
        hit = LITERAL_COLOUR.search(sheet)
        if hit:
            raise BuildError(
                f"{name}: literal colour '{hit.group(0)}' — every colour in this "
                "book's own stylesheet must be a var(--as-…) from the tokens.")


def guard_no_external(documents: dict[str, str]) -> None:
    pattern = re.compile(
        r"""(?:src|href)\s*=\s*["'](?:https?:)?//""", re.I)
    for label, doc in documents.items():
        # Links in prose are allowed; asset references are not. Scan attributes
        # that cause a fetch, plus every url() in CSS.
        for match in re.finditer(r"""<(?:img|script|link|source|iframe|object|embed)\b[^>]*>""",
                                 doc, flags=re.I):
            if pattern.search(match.group(0)):
                raise BuildError(f"{label}: external asset reference {match.group(0)[:120]}")
        for match in re.finditer(r"url\(\s*['\"]?([^)'\"]+)", doc):
            target = match.group(1).strip()
            if target.startswith(("http:", "https:", "//")):
                raise BuildError(f"{label}: external url() in CSS — {target[:80]}")


def guard_kit(documents: dict[str, str]) -> None:
    items = kit_files()
    for _, path, _ in items:
        if not path.is_file():
            raise BuildError(f"kit file missing: {path}")
    interactive = documents["Aninda-Studio-Guidebook.html"]
    if interactive.count('download="') != len(items):
        raise BuildError(
            f"interactive build has {interactive.count('download=')} download "
            f"links for {len(items)} kit files.")
    printed = documents["Aninda-Studio-Guidebook-print.html"]
    if 'download="' in printed:
        raise BuildError("the print build still carries download links.")
    if "data:application/json;base64" in printed or "data:text/css;base64" in printed:
        raise BuildError("the print build still carries kit data URIs.")
    if "data:font/woff2;base64" not in printed:
        raise BuildError(
            "the print build has no embedded fonts. Without them the Bangla "
            "prints in a fallback face.")

    # A download link that points at the wrong bytes is worse than no link, so
    # one payload is decoded and compared against the file it claims to be. The
    # smallest file is chosen because the check costs nothing then and the
    # encoder is the same for all 67.
    display, path, _ = min(items, key=lambda row: row[1].stat().st_size)
    name = Path(display).name
    hit = re.search(
        r'href="data:[^"]+;base64,([A-Za-z0-9+/=]+)"\s+download="'
        + re.escape(name) + '"', interactive)
    if not hit:
        raise BuildError(f"no data URI found for the kit file {display}")
    if base64.b64decode(hit.group(1)) != path.read_bytes():
        raise BuildError(
            f"the inlined payload for {display} does not match the file on disk.")


def guard_tables(documents: dict[str, str]) -> None:
    """Every table: a caption, scope on every header, and a row header per row.

    WCAG 2.2 SC 1.3.1 Info and Relationships, Level A. In table mode a screen
    reader announces a cell together with its headers, so a data cell with only a
    column header cannot be tied back to the row it belongs to. On the ten-column
    colour tables that means "Worst case ±1 bit, 15.61:1" with no way to know which
    role it is about.

    This book PRINTS the rule — the Table component's card says "Row headers, a
    caption saying what the numbers are, and a sideways scroll when the table is
    wider than the space" — and none of its 68 tables had a row header, 54 had no
    caption, and 17 header cells had no scope at all. Both other surfaces that ship
    that component get it right, so the book contradicted a rule on its own pages.

    A SINGLE-ROW TABLE IS EXEMPT from the row-header rule, and that is not a
    loophole. Six tables here are one row of five different measures each — a hue,
    a chroma ceiling, an anchor — where the first cell is a measure, not the row's
    identity. There is no second row to tell it apart from, and forcing a <th>
    there would assert a relationship that is not the one the table has. The
    identity of those rows is in the caption and the heading above.

    Measured with lxml over the documents that ship, not asserted about the
    generator.
    """
    try:
        from lxml import etree
    except ImportError:
        raise BuildError("lxml is not importable, so the tables cannot be checked")

    problems: list[str] = []
    for name, doc in documents.items():
        tree = etree.fromstring(doc.encode("utf-8"), etree.HTMLParser())
        tables = tree.xpath("//table")
        for index, table in enumerate(tables):
            where = f"{name}: table {index}"
            caption = table.xpath("./caption")
            # The text content, not .text. The language tagger runs before this and
            # wraps every run in a <span lang="…">, so .text is empty on a caption
            # that reads perfectly well.
            caption_text = (etree.tostring(caption[0], method="text",
                                           encoding="unicode").strip()
                            if caption else "")
            if not caption_text:
                problems.append(f"{where} has no caption")
            body_rows = table.xpath("./tbody/tr")
            if len(body_rows) > 1:
                for row_index, row in enumerate(body_rows):
                    cells = row.xpath("./*")
                    if not cells:
                        continue
                    if cells[0].tag != "th" or cells[0].get("scope") != "row":
                        problems.append(
                            f'{where} row {row_index} starts with a '
                            f'<{cells[0].tag}>, not <th scope="row">')
                        break
        for header in tree.xpath("//th"):
            if header.get("scope") not in ("col", "row"):
                text = etree.tostring(header, method="text",
                                      encoding="unicode").strip()[:30]
                problems.append(f'{name}: a <th> has scope={header.get("scope")!r} '
                                f'— "{text}"')
    if problems:
        raise BuildError(
            f"WCAG 2.2 SC 1.3.1, tables, failed in {len(problems)} place(s):\n  "
            + "\n  ".join(problems[:10]) + ("\n  …" if len(problems) > 10 else "")
        )


def guard_platform_claims(documents: dict[str, str]) -> None:
    """The book may not claim the measurements come from one machine.

    README.md's limits block is generated and CI-enforced, and says the rendering
    checks "run on macOS locally and on Ubuntu in CI, from a clean checkout, so the
    results are not particular to one machine". Chapter 14 said the opposite twice —
    "headless Chromium on macOS" and "tested by one person on one machine" — and it
    is the calibration the whole book is read against. The correct claim was the
    generated one; the wrong ones were hand-written and unguarded, which is why they
    drifted.
    """
    for name, doc in documents.items():
        text = strip_tags(doc)
        for phrase in ("one person on one machine", "on one machine"):
            if phrase in text:
                raise SystemExit(
                    f"{name}: still says {phrase!r}. The rendering checks run on "
                    f"macOS locally and on Ubuntu in CI, which README.md states and "
                    f"CI enforces. Say what is true of both, or say nothing."
                )
        # Where the book says the measurements come from Chromium, it must not
        # pin that to a single operating system.
        if "headless Chromium on macOS" in text:
            raise SystemExit(
                f"{name}: says the measurements come from 'headless Chromium on "
                f"macOS'. They come from macOS and from Ubuntu in CI."
            )


def guard_split_entities(documents: dict[str, str]) -> None:
    """No inserted tag may sit inside an HTML character reference.

    This is the structural form of the fault, not the instance of it. The
    instance was `[lang=&quot;bn&quot;]` in the Bangla chapter arriving as
    `[lang=&<span lang="en">quot;bn&quot</span>;]`, which a browser renders as
    `[lang=&quot;bn";]` and parses to zero CSS rules — dropping the valid
    `:lang(bn)` half of the selector list with it. build.py --check reported
    "byte for byte" throughout, because it compared the build against a re-run
    of the same corrupting build.

    Checked on the shipped document, so it covers any future pass that inserts
    markup, not only the tagger that caused it.
    """
    broken = re.compile(r"&(?:[a-zA-Z][a-zA-Z0-9]{0,31}|#[0-9xX]{1,8})?<|>(?:[a-zA-Z][a-zA-Z0-9]{1,31}|#[0-9]{1,7});")
    for name, doc in documents.items():
        hits = [m.group(0) for m in broken.finditer(doc)]
        if hits:
            raise SystemExit(
                f"{name}: {len(hits)} HTML character reference(s) divided by an "
                f"inserted tag, e.g. {hits[:3]}. The browser renders the pieces "
                f"as literal text, which silently corrupts whatever the reference "
                f"was part of — a CSS selector list, an attribute, a code sample."
            )


def build_all() -> dict[str, str]:
    docs = {
        OUT_INTERACTIVE.name: build_document(print_mode=False),
        OUT_PRINT.name: build_document(print_mode=True),
    }

    # A pass here used to tag every inline Bangla run with lang="bn" before the
    # guards ran, so guard_inline_bangla checked the document that actually shipped
    # rather than the one before tagging. Chapter prose mentioned Bangla words
    # inside English sentences and those runs arrived untagged.
    #
    # With one language there is nothing to tag: the whole document is English and
    # says so once, on <html>. The three Bangla guards went with it —
    # guard_bangla checked every run against a verified source, guard_bn_sections
    # counted one Bangla section per chapter, and guard_inline_bangla enforced
    # WCAG 2.2 SC 3.1.2 in both directions. The rule they enforced now lives in
    # the English-standard checker, inverted: Bangla anywhere outside the record is
    # a failure there, which is one rule instead of four.
    guard_split_entities(docs)
    guard_platform_claims(docs)

    guard_own_css()
    guard_placeholders(docs)
    guard_english(docs)
    guard_no_external(docs)
    guard_tables(docs)
    guard_kit(docs)
    return docs


def main(argv: list[str]) -> int:
    check = "--check" in argv
    only_print = os.environ.get("PRINT_MODE") == "1"

    try:
        docs = build_all()
    except BuildError as exc:
        print(f"BUILD FAILED — nothing written.\n  {exc}", file=sys.stderr)
        return 1
    except KeyError as exc:
        print(f"BUILD FAILED — nothing written.\n  missing key {exc}", file=sys.stderr)
        return 1

    targets = {OUT_INTERACTIVE.name: OUT_INTERACTIVE, OUT_PRINT.name: OUT_PRINT}
    if only_print and not check:
        targets = {OUT_PRINT.name: OUT_PRINT}

    if check:
        drift = []
        for name, path in targets.items():
            if not path.exists():
                drift.append(f"{name}: not on disk")
                continue
            on_disk = path.read_text(encoding="utf-8")
            if on_disk != docs[name]:
                drift.append(
                    f"{name}: differs — on disk {len(on_disk)} bytes, "
                    f"regenerated {len(docs[name])} bytes")
        if drift:
            print("CHECK FAILED — the outputs have drifted from their sources.",
                  file=sys.stderr)
            for line in drift:
                print(f"  {line}", file=sys.stderr)
            return 1
        for name in targets:
            print(f"  {name}: identical")
        print("CHECK PASSED — both files match their sources byte for byte.")
        return 0

    for name, path in targets.items():
        path.write_text(docs[name], encoding="utf-8")
        print(f"  wrote {path.relative_to(ROOT)} — {fmt_bytes(path.stat().st_size)}")
    print(f"  chapters: {len(CHAPTERS)} · kit files: {len(kit_files())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
