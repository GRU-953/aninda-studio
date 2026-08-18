#!/usr/bin/env python3
"""Aninda Studio — anindastudio.com, generator.

This script is the ONLY writer of 11_site/. Nothing here is hand-written and
nothing here should be hand-edited: the next run overwrites it.

    Build:   ./.venv/bin/python 11_site/build.py
    Verify:  ./.venv/bin/python 11_site/build.py --check

`--check` regenerates every byte in memory and compares it against what is on
disk. It writes nothing and exits non-zero on the first difference. If a file has
been edited by hand, or the tokens have moved and the site has not been rebuilt,
--check fails.

What gets written
    index.html · 404.html · styles.css · site.webmanifest · robots.txt ·
    sitemap.xml · CNAME, plus the eight icon files the pages reference, copied
    byte for byte out of 10_assets/.

No framework, no bundler
    One stylesheet, one page, and about twenty lines of inline JavaScript for the
    theme control. The three fonts are inlined as base64 woff2, so the page needs
    no network at all.

Where the content comes from
    The component strip is read from 08_components/_cards.json, so the site
    cannot advertise a component that does not exist. The counts, the Bangla
    names and the font list all come from the same file. The Open Graph image
    dimensions come from 10_assets/MANIFEST.json.

Colour
    Not one colour is typed in this file or in the site layer of styles.css.
    tokens.css is inlined verbatim and is the only place a literal colour lives.
    The three places that cannot take a CSS variable — the two theme-color meta
    tags and the manifest's background and theme colours — have their values READ
    out of tokens.css at build time rather than typed here.

The one file that cannot carry a header
    CNAME. GitHub Pages parses the whole file as the hostname, so a comment line
    would break the custom domain. Every other file opens with its header.

Bangla
    Only strings from the final table of 06_type/BANGLA-STANDARD.md are used.
    Where the table has no entry, the text stays in English and the gap is
    printed by this build rather than filled with an invented translation.

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import base64
import html
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

TOKENS_CSS = ROOT / "07_tokens" / "css" / "tokens.css"
COMPONENTS_CSS = ROOT / "08_components" / "src" / "components.css"
CARDS_JSON = ROOT / "08_components" / "_cards.json"
FONTS_DIR = ROOT / "08_components" / "fonts"
MARK_DIR = ROOT / "04_mark" / "svg"
ASSETS_DIR = ROOT / "10_assets"
ASSETS_MANIFEST = ASSETS_DIR / "MANIFEST.json"
NPM_PACKAGE = ROOT / "12_packages" / "npm" / "package.json"
PY_PACKAGE = ROOT / "12_packages" / "python" / "pyproject.toml"

GENERATOR = "11_site/build.py"
BUILT_ON = "2026-08-14"

# The site's only Python usage example. It is a constant because it is EXECUTED
# against the built package before the page is written — see python_example_runs().
PYTHON_EXAMPLE = (
    "from aninda_studio_tokens import css, css_path, THEMES\n"
    "\n"
    "print(THEMES)              # ['light', 'dark', 'hc-light', 'hc-dark']\n"
    "print(css('dark')[:40])    # the dark theme's stylesheet text\n"
    "print(css_path())          # the path to the complete one\n"
)
DOMAIN = "anindastudio.com"
ORIGIN = f"https://{DOMAIN}"

DO_NOT_EDIT = (
    "GENERATED FILE. Written by " + GENERATOR + ". Do not hand-edit — the next "
    "build overwrites it, and --check fails on any difference."
)

# Copied byte for byte out of 10_assets/. The site references each one, so the
# build fails if any is missing rather than shipping a page with a broken icon.
ASSETS_TO_COPY = [
    "favicon.ico",
    "favicon-32.png",
    "icon.svg",
    "apple-touch-icon.png",
    "icon-192.png",
    "icon-512.png",
    "icon-maskable-512.png",
    "og-image.png",
]

FONT_FILES = [
    ("Literata", "literata-subset.woff2", "400 700"),
    ("Noto Serif Bengali", "notoserifbengali-subset.woff2", "400 700"),
    ("Aninda Mono", "anindamono-subset.woff2", "400"),
]


class BuildError(Exception):
    pass


# =========================================================================
# Verified Bangla. Every string below is quoted from the final table of
# 06_type/BANGLA-STANDARD.md, by its id. Nothing else may appear in Bangla.
# =========================================================================

BN = {
    "wm-1": "অনিন্দ্য স্টুডিও",
    "th-1": "আলো",
    "th-2": "অন্ধকার",
    "th-3": "বেশি কনট্রাস্ট",
    "gb-1": "স্বাগতম",
    "gb-3": "চিহ্ন",
    "gb-4": "রং",
    "gb-5": "হরফ",
    "gb-6": "ফাঁক ও আকার",
    "gb-7": "উপাদান",
    "gb-8": "গতি",
    "gb-10": "যা এই পদ্ধতি করে না",
    "vc-1": (
        "আমি ছোটো, যত্নে গড়া সফটওয়্যার বানাই। কোনো কিছুর সীমা থাকলে সেটা "
        "এখানেই লেখা থাকবে — লুকিয়ে রাখা হবে না।"
    ),
    "bt-5": "কোডটি কপি করুন",
}

# The ids above came from the first verified table. 06_type/bangla-strings.json
# was written afterwards and holds 94 approved strings under readable keys —
# `ui.copy`, `theme.hc-dark`, `card.button.name` and so on — each carrying the
# rule number or dictionary page it rests on.
#
# Merging it here rather than copying strings across is deliberate: two copies of
# a translation drift, and the one that drifts is always the one nobody is
# looking at. A key present in both keeps the value from the file, because the
# file is the maintained source.
_STRINGS_FILE = ROOT / "06_type" / "bangla-strings.json"
if _STRINGS_FILE.exists():
    for _key, _entry in json.loads(_STRINGS_FILE.read_text(encoding="utf-8")).items():
        if _entry.get("bn"):
            BN[_key] = _entry["bn"]

# What still has no Bangla, reported honestly at the end of every build.
#
# The card entries are COUNTED from _cards.json rather than described, because
# the first version of this list was written by hand and went stale the moment
# the verified strings arrived: it still claimed twenty-five card names were
# missing when every one of them had been filled in. A hand-written list of
# what is missing is a claim that rots silently, which is the exact failure this
# project is built to avoid. Anything that can be counted is counted.
def _bangla_gaps() -> list[str]:
    gaps = [
        "The 'follow the system' theme choice. The table has আলো, অন্ধকার and "
        "বেশি কনট্রাস্ট, but nothing for the option that follows the reader's own "
        "setting.",
        "The four section headings that do not match a guidebook chapter title: "
        "what the studio is, the work, installing the packages, and contact.",
        "Every sentence of body prose except the voice sample. Prose is written, "
        "not looked up, and writing it is a separate job from approving terms.",
    ]
    try:
        reg = json.loads(CARDS_JSON.read_text(encoding="utf-8"))
        cards = reg["cards"] if isinstance(reg, dict) and "cards" in reg else reg
        missing_names = [c["name"] for c in cards if not c.get("name_bn")]
        missing_subs = sum(1 for c in cards if not c.get("subtitle_bn"))
        if missing_names:
            gaps.append(f"{len(missing_names)} of {len(cards)} component names: "
                        f"{', '.join(missing_names[:5])}"
                        f"{'…' if len(missing_names) > 5 else ''}")
        if missing_subs:
            gaps.append(f"{missing_subs} of {len(cards)} component subtitles.")
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        gaps.append(f"The component list could not be read to count its gaps: {exc}")
    return gaps


BANGLA_GAPS = _bangla_gaps()


# =========================================================================
# Guards
# =========================================================================

_HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
# re.IGNORECASE: CSS colour functions are case-insensitive, so RGB(255 0 0)
# and OKLCH(...) are valid CSS. This guard was case-sensitive and let every
# uppercase form through while reporting a clean build — the same fault was
# fixed in 08_components/build.py first, and this second copy was missed.
_FUNC = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\s*\(",
                   re.IGNORECASE)

BANNED_WORDS = ["simply", "just", "easy", "obviously", "of course", "clearly"]
BANNED_LATIN = ["e.g.", "i.e.", "etc."]


def strip_css_comments(text: str) -> str:
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


def guard_site_css(text: str) -> None:
    """The site layer may not contain a literal colour. tokens.css may, and is
    checked separately by being taken verbatim from its own generator."""
    problems = []
    for lineno, line in enumerate(strip_css_comments(text).splitlines(), 1):
        if _HEX.search(line):
            problems.append(f"site layer:{lineno}: hex colour — {line.strip()}")
        if _FUNC.search(line):
            problems.append(f"site layer:{lineno}: colour function — {line.strip()}")
    if problems:
        raise BuildError("The no-literal-colour rule failed:\n  " + "\n  ".join(problems))


def guard_english(pages: dict[str, str]) -> None:
    """02_strategy/ENGLISH-STANDARD.md bans six words outright, bans exclamation
    marks, and bans Latin abbreviations. Those three are mechanical, so they are
    enforced rather than trusted."""
    problems = []
    for name, markup in pages.items():
        text = re.sub(r"<[^>]+>", " ", markup)
        text = html.unescape(text)
        low = text.lower()
        for word in BANNED_WORDS:
            for hit in re.finditer(r"\b" + re.escape(word) + r"\b", low):
                around = text[max(0, hit.start() - 40):hit.end() + 40].replace("\n", " ")
                problems.append(f"{name}: banned word '{word}' — …{around.strip()}…")
        for abbreviation in BANNED_LATIN:
            if abbreviation in low:
                problems.append(f"{name}: Latin abbreviation '{abbreviation}'")
        if "!" in text:
            hit = text.index("!")
            around = text[max(0, hit - 50):hit + 20].replace("\n", " ")
            problems.append(f"{name}: exclamation mark — …{around.strip()}…")
    if problems:
        raise BuildError("The English standard failed:\n  " + "\n  ".join(problems))


def guard_glyphs(pages: dict[str, str]) -> None:
    """Every character the page shows must exist in the subset that travels with
    it. A character outside the subset falls back to whatever face the reader's
    machine has, which is the one failure a self-contained page must not have."""
    from fontTools.ttLib import TTFont

    latin = set(TTFont(FONTS_DIR / "literata-subset.woff2").getBestCmap())
    bangla = set(TTFont(FONTS_DIR / "notoserifbengali-subset.woff2").getBestCmap())
    mono = set(TTFont(FONTS_DIR / "anindamono-subset.woff2").getBestCmap())

    problems = []
    for name, markup in pages.items():
        # Text inside <style>, <script> and <title> is never drawn in a page face.
        body = re.sub(r"<(style|script|title)\b[^>]*>.*?</\1>", " ", markup, flags=re.S)
        for run, chunk in text_runs(body):
            covered = {"bn": bangla, "mono": mono, "latin": latin}[run]
            missing = sorted({ch for ch in chunk if ord(ch) not in covered and ch not in "\n\t"})
            for ch in missing:
                problems.append(
                    f"{name}: {run} subset has no {ch!r} (U+{ord(ch):04X}) — "
                    f"in …{chunk.strip()[:60]}…"
                )
    if problems:
        raise BuildError(
            "A character on the page is not in the font that travels with it:\n  "
            + "\n  ".join(sorted(set(problems)))
        )


def text_runs(markup: str):
    """Split the markup into the text each face has to draw. Anything inside an
    element carrying lang="bn" is Bangla; anything inside .as-mono or
    .as-code__pre is the mono face; everything else is Latin."""
    runs: list[tuple[str, str]] = []
    depth_bn = 0
    depth_mono = 0
    stack: list[tuple[str, bool, bool]] = []
    for token in re.split(r"(<[^>]+>)", markup):
        if token.startswith("<"):
            if token.startswith("</"):
                if stack:
                    _, was_bn, was_mono = stack.pop()
                    depth_bn -= 1 if was_bn else 0
                    depth_mono -= 1 if was_mono else 0
                continue
            if token.endswith("/>") or re.match(r"<(meta|link|br|img|hr|input|source)\b", token):
                continue
            is_bn = 'lang="bn"' in token
            is_mono = "as-mono" in token or "as-code__pre" in token
            stack.append((token, is_bn, is_mono))
            depth_bn += 1 if is_bn else 0
            depth_mono += 1 if is_mono else 0
            continue
        chunk = html.unescape(token)
        if not chunk.strip():
            continue
        if depth_bn:
            runs.append(("bn", chunk))
        elif depth_mono:
            runs.append(("mono", chunk))
        else:
            runs.append(("latin", chunk))
    return runs


def guard_bangla(pages: dict[str, str]) -> None:
    """Two rules. Every Bangla character must sit inside an element that says
    lang="bn", and every Bangla string must be one of the verified ones."""
    allowed = set(BN.values())
    problems = []
    for name, markup in pages.items():
        for run, chunk in text_runs(markup):
            has_bangla = any("ঀ" <= ch <= "৿" for ch in chunk)
            if has_bangla and run != "bn":
                problems.append(f"{name}: Bangla outside lang=\"bn\" — {chunk.strip()[:50]}")
            if run == "bn" and chunk.strip() and chunk.strip() not in allowed:
                problems.append(
                    f"{name}: Bangla string not in the verified table — {chunk.strip()[:50]}"
                )
    if problems:
        raise BuildError("The Bangla standard failed:\n  " + "\n  ".join(problems))


# =========================================================================
# Reading the inputs
# =========================================================================


def token_value(css: str, selector: str, name: str) -> str:
    """Read one declared value straight out of tokens.css. This is how the two
    theme-color meta tags and the manifest colours get their values without a
    colour ever being typed into this file."""
    match = re.search(re.escape(selector) + r"\s*\{(.*?)\}", css, re.S)
    if not match:
        raise BuildError(f"tokens.css has no {selector} block.")
    found = re.search(re.escape(name) + r"\s*:\s*([^;]+);", match.group(1))
    if not found:
        raise BuildError(f"tokens.css has no {name} in {selector}.")
    return found.group(1).strip()


def read_json(path: Path) -> dict:
    if not path.exists():
        raise BuildError(f"Missing input: {path}")
    return json.loads(path.read_text("utf-8"))


def read_mark(name: str, size: str, title: str) -> str:
    from lxml import etree

    path = MARK_DIR / name
    if not path.exists():
        raise BuildError(f"Mark not found: {path}. Run 04_mark/build.py first.")
    node = etree.fromstring(path.read_bytes())
    node.set("width", size)
    node.set("height", size)
    node.set("aria-hidden", "true")
    node.set("focusable", "false")
    for child in list(node):
        if child.tag.endswith("}title") or child.tag == "title":
            node.remove(child)
    del node.attrib["role"]
    return etree.tostring(node, encoding="unicode")


def font_faces() -> str:
    blocks = []
    for family, filename, weight in FONT_FILES:
        path = FONTS_DIR / filename
        if not path.exists():
            raise BuildError(f"Font not found: {path}. Run 08_components/build.py first.")
        blob = base64.b64encode(path.read_bytes()).decode("ascii")
        blocks.append(
            "@font-face {\n"
            f"  font-family: \"{family}\";\n"
            "  font-style: normal;\n"
            f"  font-weight: {weight};\n"
            "  font-display: block;\n"
            f"  src: url(data:font/woff2;base64,{blob}) format(\"woff2\");\n"
            "}"
        )
    return "\n".join(blocks)


# =========================================================================
# Small HTML helpers
# =========================================================================


def e(text: str) -> str:
    return html.escape(str(text), quote=True)


def bn(key: str, large: bool = False) -> str:
    cls = ' class="as-bn-large"' if large else ""
    return f'<span lang="bn"{cls}>{e(BN[key])}</span>'


def bn_text(value: str, large: bool = False) -> str:
    cls = ' class="as-bn-large"' if large else ""
    return f'<span lang="bn"{cls}>{e(value)}</span>'


ICONS = {
    "check": '<path d="M3 8.6 6.4 12 13 4.6"/>',
    "cross": '<path d="M4 4 12 12M12 4 4 12"/>',
    "warn": '<path d="M8 2.2 15 13.8H1Z"/><path d="M8 6.4v3.1"/><path d="M8 11.9h.01"/>',
    "info": '<circle cx="8" cy="8" r="6.2"/><path d="M8 7.4v4"/><path d="M8 4.9h.01"/>',
    "dot": '<circle cx="8" cy="8" r="3.2" fill="currentColor" stroke="none"/>',
    "arrow": '<path d="M2.5 8h10.5"/><path d="M9.2 4.2 13 8l-3.8 3.8"/>',
}


def icon(name: str) -> str:
    return (
        '<svg class="as-icon" viewBox="0 0 16 16" width="16" height="16" '
        'aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
        f"{ICONS[name]}</svg>"
    )


def code(name: str, body: str) -> str:
    lines = "\n".join(e(line) for line in body.strip("\n").split("\n"))
    return (
        '<div class="as-code">'
        f'<div class="as-code__head"><span class="as-code__name">{e(name)}</span></div>'
        f'<pre class="as-code__pre"><code>{lines}</code></pre>'
        "</div>"
    )


# =========================================================================
# The site layer. Everything else is 08_components/src/components.css.
# =========================================================================

SITE_CSS = """
/* =========================================================================
   The site layer — the only CSS written for this page.
   Everything above is tokens.css and the component layer, both taken
   verbatim from their own generators. No literal colour appears below.
   ========================================================================= */

.site-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--as-space-3);
  padding-block-end: var(--as-space-3);
  border-block-end: 1px solid var(--as-line);
}

.site-brand { display: flex; align-items: center; gap: var(--as-space-2); min-width: 0; }
.site-brand__mark { flex: none; inline-size: var(--as-space-6); block-size: var(--as-space-6); }
.site-brand__mark svg { display: block; inline-size: 100%; block-size: 100%; }
.site-brand__text { min-width: 0; }
.site-brand__name { display: block; font-size: var(--as-text-lead); font-weight: 700; line-height: 1.2; }
.site-brand__bn { display: block; color: var(--as-ink-muted); }

.site-controls { display: flex; flex-wrap: wrap; align-items: center; gap: var(--as-space-2); }
.site-controls__label { font-size: var(--as-text-caption); font-weight: 700; color: var(--as-ink-muted); }

.site-hero { display: flex; flex-direction: column; gap: var(--as-space-3); }
.site-hero__bn { color: var(--as-ink-muted); }

.site-index {
  display: grid;
  gap: var(--as-space-2);
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
  min-width: 0;
}

.site-entry {
  display: flex;
  flex-direction: column;
  gap: var(--as-space-0);
  padding: var(--as-space-2);
  border: 1px solid var(--as-line);
  border-radius: var(--as-radius-control);
  background-color: var(--as-surface-bright);
  min-width: 0;
}

.site-entry__name { font-weight: 700; color: var(--as-ink); }
.site-entry__bn { color: var(--as-ink-muted); }
.site-entry__text { font-size: var(--as-text-caption); color: var(--as-ink-muted); }

.site-facts { max-inline-size: 46rem; }

/* The skip link is visible at all times rather than hidden until focus. A
   sighted keyboard user gets to see it, and it can be measured the same way as
   every other control instead of needing an exception in the check harness. */
.site-skip { flex: none; }

.site-foot__list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--as-space-2) var(--as-space-4);
  list-style: none;
  margin: 0;
  padding: 0;
}
"""


THEME_JS = """(function () {
  var root = document.documentElement, KEY = 'as-theme';
  var dark = window.matchMedia('(prefers-color-scheme: dark)');
  function stored() { try { return localStorage.getItem(KEY) || 'system'; } catch (e) { return 'system'; } }
  function apply(choice) {
    var value = choice === 'light' ? 'light' : choice === 'dark' ? 'dark'
      : choice === 'contrast' ? (dark.matches ? 'hc-dark' : 'hc-light') : '';
    if (value) { root.setAttribute('data-theme', value); } else { root.removeAttribute('data-theme'); }
    var buttons = document.querySelectorAll('[data-theme-choice]');
    for (var i = 0; i < buttons.length; i++) {
      var own = buttons[i].getAttribute('data-theme-choice');
      buttons[i].setAttribute('aria-pressed', own === choice ? 'true' : 'false');
    }
  }
  function choose(choice) { try { localStorage.setItem(KEY, choice); } catch (e) {} apply(choice); }
  apply(stored());
  dark.addEventListener('change', function () { apply(stored()); });
  document.addEventListener('DOMContentLoaded', function () {
    var buttons = document.querySelectorAll('[data-theme-choice]');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener('click', function (event) {
        choose(event.currentTarget.getAttribute('data-theme-choice'));
      });
    }
    apply(stored());
  });
})();"""


# =========================================================================
# The page
# =========================================================================


THEME_CHOICES = [
    ("system", "Follow the system", None),
    ("light", "Light", "th-1"),
    ("dark", "Dark", "th-2"),
    ("contrast", "More contrast", "th-3"),
]


def theme_control() -> str:
    buttons = []
    for value, label, key in THEME_CHOICES:
        pressed = "true" if value == "system" else "false"
        inner = e(label)
        if key:
            inner += " " + bn(key)
        buttons.append(
            f'<button type="button" class="as-doc-theme" data-theme-choice="{value}" '
            f'aria-pressed="{pressed}">{inner}</button>'
        )
    return (
        '<div class="site-controls">'
        '<span class="site-controls__label" id="theme-label">Theme</span>'
        '<div class="as-doc-themes" role="group" aria-labelledby="theme-label">'
        + "".join(buttons)
        + "</div></div>"
    )


def header(mark: str) -> str:
    return (
        '<header class="site-header">'
        '<div class="site-brand">'
        f'<span class="site-brand__mark">{mark}</span>'
        '<span class="site-brand__text">'
        '<span class="site-brand__name">Aninda Studio</span>'
        f'<span class="site-brand__bn">{bn("wm-1")}</span>'
        "</span></div>"
        '<a class="as-btn as-btn--quiet site-skip" href="#main">Skip to the content</a>'
        + theme_control()
        + "</header>"
    )


def hero() -> str:
    return (
        '<div class="site-hero">'
        '<h1 class="as-h1">Aninda Studio</h1>'
        f'<p class="site-hero__bn as-lead">{bn("wm-1", large=True)}</p>'
        '<p class="as-lead as-prose">I make small, careful software, and the design '
        "system it is built on. Where something has a limit, the limit is written "
        "down here rather than left for you to find.</p>"
        f'<p class="as-prose">{bn_text(BN["vc-1"])}</p>'
        "</div>"
    )


def section_studio() -> str:
    return (
        '<section class="as-doc-section" aria-labelledby="studio">'
        '<h2 class="as-h2" id="studio">What this studio is</h2>'
        '<div class="as-prose as-stack">'
        "<p>Aninda Studio is one person: Aninda Sundar Howlader. I design and build "
        "software, and I write in two languages, English and Bangla, because both "
        "are first languages for the people I build for.</p>"
        "<p>The rule I work to is that a claim gets measured before it is made. "
        "Contrast ratio — how far apart two colours are in brightness — was measured "
        "for every colour pairing in this system rather than judged by eye. Every "
        "page here was rendered in a real browser and then measured. Where a figure "
        "could not be checked against its own source, it is marked as unverified "
        "instead of being presented as fact.</p>"
        "<p>That applies to this page too. It was rendered at three widths in all "
        "four themes, and the contrast of every piece of text on it was measured "
        "against the background it actually sits on.</p>"
        "</div></section>"
    )


def section_work(cards: dict, tokens_css: str) -> str:
    """Every figure in this table is counted from a file, not typed. If the
    system changes and the site is rebuilt, the numbers change with it."""
    properties = len(set(re.findall(r"--as-[a-z0-9-]+(?=\s*:)", tokens_css)))
    themes = len(re.findall(r'\[data-theme="[a-z-]+"\]\s*\{', tokens_css))
    counts = cards["counts"]
    fonts = cards["_fonts"]

    rows = [
        ("Themes", themes,
         "Light, dark, and a high-contrast pair. Each one is a complete set of "
         "values, not a filter over another set."),
        ("Design tokens", properties,
         "Custom properties covering colour, type, space, shape and motion. "
         "The source is DTCG format."),
        ("Foundations", counts["Foundations"], "Colour, typography, space and shape, "
         "motion, the marks, and accessibility."),
        ("Components", counts["Components"], "Buttons, fields, badges, alerts, "
         "tables, tabs, navigation and the rest."),
        ("Patterns", counts["Patterns"], "Whole screens assembled from the "
         "components, including sign in, settings and a dashboard."),
        ("Fonts", len(fonts), "All three are SIL Open Font Licence 1.1, subset to "
         "what this page draws and carried inside the stylesheet."),
    ]
    body = "".join(
        f"<tr><th scope=\"row\">{e(name)}</th>"
        f"<td class=\"as-num\">{value}</td><td>{e(note)}</td></tr>"
        for name, value, note in rows
    )
    return (
        '<section class="as-doc-section" aria-labelledby="work">'
        '<h2 class="as-h2" id="work">The work</h2>'
        '<p class="as-doc-section__note">Every number below is counted from the '
        'files themselves when this page is built, so the page cannot claim '
        'something the system does not hold.</p>'
        '<div class="as-scroll-x site-facts"><table class="as-table as-table--numeric">'
        '<caption>What the system contains, counted on ' + BUILT_ON + '.</caption>'
        '<thead><tr><th scope="col">Part</th><th scope="col" class="as-num">Count</th>'
        '<th scope="col">What it is</th></tr></thead>'
        f"<tbody>{body}</tbody></table></div>"
        "</section>"
    )


def live_strip() -> str:
    badges = "".join(
        f'<span class="as-badge as-badge--{kind}">{icon(glyph)}'
        f'<span class="as-badge__label">{e(label)}</span></span>'
        for kind, glyph, label in [
            ("success", "check", "Measured"),
            ("info", "info", "Documented"),
            ("warning", "warn", "Unverified"),
            ("danger", "cross", "Failed"),
            ("accent", "dot", "In progress"),
        ]
    )
    return (
        '<div class="as-doc-stage as-stack as-stack--loose">'
        f'<div class="as-row">{badges}</div>'
        '<div class="as-alert as-alert--info">'
        f'<span class="as-alert__glyph">{icon("info")}</span>'
        '<div class="as-alert__body">'
        '<p class="as-alert__title">Every state carries a word and a glyph</p>'
        '<p class="as-alert__text">Colour is the third signal here and never the '
        'only one. A reader who cannot tell the five badges above apart by colour '
        'can still read which is which.</p></div></div>'
        '<div class="as-card">'
        '<p class="as-card__title">Card</p>'
        '<p class="as-card__meta">A surface one step brighter than the page</p>'
        '<p class="as-card__body">It carries a shadow in the light theme and none '
        'in the dark ones, because a shadow on a dark ground reads as dirt rather '
        'than as height.</p></div>'
        + code("styles.css", ".as-card {\n  background-color: var(--as-surface-bright);\n"
                             "  box-shadow: var(--as-shadow-float);\n}")
        + "</div>"
    )


def section_system(cards: dict) -> str:
    groups = ["Foundations", "Components", "Patterns"]
    blocks = []
    for group in groups:
        entries = []
        for card in cards["cards"]:
            if card["group"] != group:
                continue
            name_bn = ""
            if card["name_bn"]:
                name_bn = f'<span class="site-entry__bn">{bn_text(card["name_bn"])}</span>'
            entries.append(
                '<div class="site-entry">'
                f'<span class="site-entry__name">{card["name"]}</span>'
                + name_bn
                + f'<span class="site-entry__text">{card["subtitle"]}</span>'
                "</div>"
            )
        blocks.append(
            '<div class="as-stack">'
            f'<h3 class="as-h3">{e(group)} <span class="as-badge as-badge--accent">'
            f'<span class="as-badge__label">{len(entries)}</span></span></h3>'
            f'<div class="site-index">{"".join(entries)}</div>'
            "</div>"
        )

    return (
        '<section class="as-doc-section" aria-labelledby="system">'
        '<h2 class="as-h2" id="system">The design system '
        f'{bn("gb-7", large=True)}</h2>'
        '<p class="as-doc-section__note">These are live. The badges, the alert, the '
        'card and the code block below are the real components, styled by the same '
        'stylesheet the library uses, not pictures of them.</p>'
        + live_strip()
        + '<h3 class="as-h3">Everything in the library</h3>'
        '<p class="as-doc-section__note">Read from 08_components/_cards.json when '
        'this page is built. A component that is not in that file cannot appear here.</p>'
        + "".join(blocks)
        + "</section>"
    )


def section_install(npm: dict, py_name: str, pub: dict) -> str:
    # The publication record is read from 12_packages/PUBLICATION.json rather than
    # written here. This page was the ONLY place that told a reader the packages are
    # not published; the two READMEs and the guidebook all said "npm install" with
    # no caveat. One shared record is what stops the four disagreeing again.
    missing = [r for r in pub["registries"] if not r["published"]]
    where = " and ".join(e(r["registry"]) for r in missing)
    return (
        '<section class="as-doc-section" aria-labelledby="install">'
        '<h2 class="as-h2" id="install">Installing the token packages</h2>'
        + ('<div class="as-alert as-alert--warning">'
           f'<span class="as-alert__glyph">{icon("warn")}</span>'
           '<div class="as-alert__body">'
           '<p class="as-alert__title">Not published yet</p>'
           f'<p class="as-alert__text">On {e(pub["checked"])} I checked {where}, and '
           "neither holds these packages. They are built and they work from a local "
           "checkout. The two commands below are what will work once they are "
           "published, and I would rather show you that plainly than let you find "
           "out at the terminal.</p>"
           "</div></div>" if missing else "")
        + '<div class="as-grid as-grid--wide">'
        + "".join([
            '<div class="as-stack">'
            '<h3 class="as-h3">For a web project</h3>'
            + code("terminal", f"npm install {npm['name']}")
            + code("app.css", f'@import "{npm["name"]}/css";')
            + '<p class="as-caption as-muted">Version ' + e(npm["version"])
            + ", licensed Apache-2.0. The package also exports one stylesheet per "
              "theme, and the tokens as DTCG format data.</p>"
            "</div>",
            '<div class="as-stack">'
            '<h3 class="as-h3">For a Python project</h3>'
            + code("terminal", f"pip install {py_name}")
            # This block used to import `tokens_css`, a name the package has never
            # exported, so the site's only Python example raised ImportError
            # whether or not the package was published. It is now the real API, and
            # python_example_runs() below executes it against the built package
            # before this page may be written.
            + code("app.py", PYTHON_EXAMPLE)
            + '<p class="as-caption as-muted">The same values, the same four themes, '
              "read from the same source data.</p>"
            "</div>",
        ])
        + "</div>"
        '<div class="as-stack">'
        '<h3 class="as-h3">Using them without a package</h3>'
        '<p class="as-prose">The stylesheet is plain CSS custom properties. Copy '
        'tokens.css into your project, link it, and every value below is available '
        'to you.</p>'
        + code("index.html", '<link rel="stylesheet" href="tokens.css">')
        + code("anything.css", ".panel {\n  background-color: var(--as-surface-bright);\n"
                               "  color: var(--as-ink);\n  border-radius: var(--as-radius-card);\n}")
        + f'<p class="as-caption as-muted">{e(BN["bt-5"])}</p>'.replace(
            e(BN["bt-5"]), bn("bt-5"))
        + "</div></section>"
    )


def section_contact(email: str) -> str:
    return (
        '<section class="as-doc-section" aria-labelledby="contact">'
        '<h2 class="as-h2" id="contact">Contact</h2>'
        '<p class="as-prose">Write to me. If you send me what you are working on, '
        "I will tell you plainly whether I am the right person for it, and say so "
        "if I am not.</p>"
        '<div class="as-row">'
        f'<a class="as-btn as-btn--primary" href="mailto:{e(email)}">Write to me</a>'
        f'<span class="as-mono as-caption as-muted">{e(email)}</span>'
        "</div></section>"
    )


def footer(cards: dict) -> str:
    fonts = "".join(
        f'<li>{e(f["family"])} — {e(f["licence"])}'
        + (", subset and renamed" if f["renamed"] else ", subset")
        + "</li>"
        for f in cards["_fonts"]
    )
    return (
        '<footer class="as-doc-foot as-stack">'
        f"<p>Built on {BUILT_ON} by {GENERATOR}. This page is generated. Editing it "
        "by hand is undone by the next build.</p>"
        f'<ul class="as-doc-list">{fonts}</ul>'
        "<p>Literata and Noto Serif Bengali keep their own names. The monospace "
        "face is a subset of IBM Plex Mono renamed to Aninda Mono, because "
        "Plex is a Reserved Font Name and subsetting is a modification under "
        "clause 3 of the SIL Open Font Licence 1.1. Each licence file sits beside "
        "its font in 08_components/fonts/.</p>"
        "<p>The design tokens and this site are licensed Apache-2.0. "
        "Copyright 2026 Aninda Sundar Howlader.</p>"
        "<p>Bangla appears only where the verified table in "
        "06_type/BANGLA-STANDARD.md holds a string. Everywhere else the text stays "
        "in English rather than being translated by guesswork, and those places are "
        "listed in this build's output.</p>"
        "</footer>"
    )


def document(title: str, description: str, body: str, tokens_css: str,
             og_width: int, og_height: int, canonical: str, robots: str = "") -> str:
    light = token_value(tokens_css, ":root", "--as-surface-base")
    dark = token_value(tokens_css, '[data-theme="dark"]', "--as-surface-base")
    robots_tag = f'<meta name="robots" content="{robots}">\n' if robots else ""
    return (
        f"<!-- {DO_NOT_EDIT} -->\n"
        "<!doctype html>\n"
        '<html lang="en" class="as-root">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{e(title)}</title>\n"
        f'<meta name="description" content="{e(description)}">\n'
        f'<meta name="generator" content="{GENERATOR}">\n'
        + robots_tag
        + f'<link rel="canonical" href="{e(canonical)}">\n'
        f'<meta name="theme-color" media="(prefers-color-scheme: light)" content="{light}">\n'
        f'<meta name="theme-color" media="(prefers-color-scheme: dark)" content="{dark}">\n'
        '<link rel="icon" href="favicon.ico" sizes="32x32">\n'
        '<link rel="icon" href="icon.svg" type="image/svg+xml">\n'
        '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
        '<link rel="manifest" href="site.webmanifest">\n'
        '<link rel="stylesheet" href="styles.css">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:site_name" content="Aninda Studio">\n'
        f'<meta property="og:locale" content="en">\n'
        f'<meta property="og:title" content="{e(title)}">\n'
        f'<meta property="og:description" content="{e(description)}">\n'
        f'<meta property="og:url" content="{e(canonical)}">\n'
        f'<meta property="og:image" content="{ORIGIN}/og-image.png">\n'
        f'<meta property="og:image:width" content="{og_width}">\n'
        f'<meta property="og:image:height" content="{og_height}">\n'
        '<meta property="og:image:alt" content="The Aninda Studio mark, the name in '
        'English and Bangla, and the line: Small, careful software.">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        f"<script>{THEME_JS}</script>\n"
        "</head>\n"
        f"<body>{body}</body>\n"
        "</html>\n"
    )


def python_example_runs() -> None:
    """Run the site's Python example against the built package, or write nothing.

    The page carried `from aninda_studio_tokens import tokens_css`, a name the
    package has never exported, so the site's single Python example raised
    ImportError on a page whose own thesis is that every claim on it was measured.
    11_site/check.py drives a browser and measures contrast and layout; nothing
    executed a code sample. This does, in a subprocess, against
    12_packages/python/src so it is the shipped package that answers.
    """
    source = ROOT / "12_packages" / "python" / "src"
    if not source.is_dir():
        raise BuildError(f"{source} is missing. Run 12_packages/build.py first — the "
                         "site's Python example is executed against it.")
    proc = subprocess.run(
        [sys.executable, "-c", PYTHON_EXAMPLE],
        capture_output=True, text=True, cwd=source,
    )
    if proc.returncode != 0:
        raise BuildError(
            "the Python example on the site does not run. It was executed with "
            f"{source} on the path and exited {proc.returncode}:\n"
            + (proc.stderr.strip() or proc.stdout.strip())[:600]
        )


def index_page(tokens_css: str, cards: dict, npm: dict, py_name: str,
               email: str, og: tuple[int, int], pub: dict) -> str:
    mark = read_mark("icon-192.svg", "48", "Aninda Studio")
    body = (
        '<div class="as-doc-page">'
        + header(mark)
        + '<main id="main" class="as-stack as-stack--loose">'
        + hero()
        + section_studio()
        + section_work(cards, tokens_css)
        + section_system(cards)
        + section_install(npm, py_name, pub)
        + section_contact(email)
        + "</main>"
        + footer(cards)
        + "</div>"
    )
    return document(
        "Aninda Studio",
        "Small, careful software, and the design system it is built on. "
        "Design tokens, components and marks, measured rather than assumed.",
        body, tokens_css, og[0], og[1], ORIGIN + "/",
    )


def not_found_page(tokens_css: str, cards: dict, og: tuple[int, int]) -> str:
    mark = read_mark("icon-192.svg", "48", "Aninda Studio")
    body = (
        '<div class="as-doc-page">'
        + header(mark)
        + '<main id="main" class="as-stack as-stack--loose">'
        '<h1 class="as-h1">This page is not here</h1>'
        '<div class="as-empty">'
        f'<span class="as-empty__glyph">{icon("cross")}</span>'
        '<p class="as-empty__title">Nothing at this address</p>'
        '<p class="as-empty__text">The page you asked for is missing. It may have '
        'been renamed, or the link that brought you here may have a small mistake '
        'in it. Nothing you were doing has been lost.</p>'
        f'<a class="as-btn as-btn--primary" href="index.html">Go to the front page {icon("arrow")}</a>'
        "</div>"
        '<div class="as-stack">'
        '<h2 class="as-h2">What is on this site</h2>'
        '<ul class="as-doc-list">'
        '<li><a class="as-nav__link" href="index.html#studio">What this studio is</a></li>'
        '<li><a class="as-nav__link" href="index.html#work">The work</a></li>'
        '<li><a class="as-nav__link" href="index.html#system">The design system</a></li>'
        '<li><a class="as-nav__link" href="index.html#install">Installing the token packages</a></li>'
        '<li><a class="as-nav__link" href="index.html#contact">Contact</a></li>'
        "</ul></div>"
        "</main>"
        + footer(cards)
        + "</div>"
    )
    return document(
        "This page is not here — Aninda Studio",
        "The page you asked for is missing. Here is what is on the site instead.",
        body, tokens_css, og[0], og[1], ORIGIN + "/404.html",
        robots="noindex",
    )


# =========================================================================
# The other files
# =========================================================================


def stylesheet(tokens_css: str, components_css: str) -> str:
    guard_site_css(SITE_CSS)
    return (
        f"/* {DO_NOT_EDIT} */\n"
        "/* Three layers, in this order:\n"
        " *   1. 07_tokens/css/tokens.css   — verbatim, the only literal colours\n"
        " *   2. the three fonts            — subset woff2, inlined, no network\n"
        " *   3. 08_components/src/components.css — verbatim, the component layer\n"
        " *   4. the site layer             — written for this page, no literal colour\n"
        " */\n\n"
        "/* >>> begin 07_tokens/css/tokens.css */\n"
        + tokens_css
        + "\n/* <<< end 07_tokens/css/tokens.css */\n\n"
        "/* >>> begin fonts, inlined so the page needs no network */\n"
        + font_faces()
        + "\n/* <<< end fonts */\n\n"
        "/* >>> begin 08_components/src/components.css */\n"
        + components_css
        + "\n/* <<< end 08_components/src/components.css */\n"
        + SITE_CSS
    )


def webmanifest(tokens_css: str) -> str:
    background = token_value(tokens_css, ":root", "--as-surface-base")
    payload = {
        "_generator": GENERATOR,
        "_warning": DO_NOT_EDIT,
        "name": "Aninda Studio",
        "short_name": "Aninda",
        "description": "Small, careful software, and the design system it is built on.",
        "lang": "en",
        "dir": "ltr",
        "start_url": "/",
        "scope": "/",
        "id": "/",
        "display": "minimal-ui",
        "background_color": background,
        "theme_color": background,
        "icons": [
            {"src": "/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png",
             "purpose": "maskable"},
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def robots_txt() -> str:
    return (
        f"# {DO_NOT_EDIT}\n"
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {ORIGIN}/sitemap.xml\n"
    )


def sitemap_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"<!-- {DO_NOT_EDIT} -->\n"
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <url>\n"
        f"    <loc>{ORIGIN}/</loc>\n"
        f"    <lastmod>{BUILT_ON}</lastmod>\n"
        "  </url>\n"
        "</urlset>\n"
    )


def cname() -> str:
    # No header. GitHub Pages reads the whole file as the hostname, so a comment
    # line here would break the custom domain. This is the one exception, and the
    # build prints it so it is never a silent one.
    return DOMAIN + "\n"


# =========================================================================
# Build
# =========================================================================


def build() -> dict[str, bytes]:
    for path in (TOKENS_CSS, COMPONENTS_CSS, CARDS_JSON, NPM_PACKAGE, PY_PACKAGE):
        if not path.exists():
            raise BuildError(f"Missing input: {path}")
    if not ASSETS_MANIFEST.exists():
        raise BuildError(
            f"{ASSETS_MANIFEST} is missing. Run 10_assets/build.py first — the site "
            "references eight files from there and will not ship a broken icon."
        )

    tokens_css = TOKENS_CSS.read_text("utf-8")
    components_css = COMPONENTS_CSS.read_text("utf-8")
    cards = read_json(CARDS_JSON)
    npm = read_json(NPM_PACKAGE)
    assets = read_json(ASSETS_MANIFEST)

    py_text = PY_PACKAGE.read_text("utf-8")
    found = re.search(r'^name\s*=\s*"([^"]+)"', py_text, re.M)
    if not found:
        raise BuildError("Could not read the Python package name from pyproject.toml.")
    py_name = found.group(1)
    email = npm["author"]["email"]
    pub = read_json(ROOT / "12_packages" / "PUBLICATION.json")
    python_example_runs()

    og = next((f for f in assets["files"] if f["name"] == "og-image.png"), None)
    if og is None:
        raise BuildError("10_assets/MANIFEST.json has no og-image.png.")
    og_size = (og["width"], og["height"])

    pages = {
        "index.html": index_page(tokens_css, cards, npm, py_name, email, og_size, pub),
        "404.html": not_found_page(tokens_css, cards, og_size),
    }

    guard_english(pages)
    guard_bangla(pages)
    guard_glyphs(pages)

    out: dict[str, bytes] = {name: text.encode("utf-8") for name, text in pages.items()}
    out["styles.css"] = stylesheet(tokens_css, components_css).encode("utf-8")
    out["site.webmanifest"] = webmanifest(tokens_css).encode("utf-8")
    out["robots.txt"] = robots_txt().encode("utf-8")
    out["sitemap.xml"] = sitemap_xml().encode("utf-8")
    out["CNAME"] = cname().encode("utf-8")

    for name in ASSETS_TO_COPY:
        source = ASSETS_DIR / name
        if not source.exists():
            raise BuildError(f"{source} is missing. Run 10_assets/build.py first.")
        out[name] = source.read_bytes()

    # Nothing may be FETCHED over the network. An absolute address is fine where
    # it only names a location — the canonical link, og:url, og:image — but a
    # stylesheet, script, image or font must resolve inside the site.
    for name in ("index.html", "404.html", "styles.css"):
        text = out[name].decode("utf-8")
        fetched = [
            *re.findall(r'<script[^>]*\bsrc\s*=\s*"([^"]+)"', text),
            *re.findall(r'<img[^>]*\bsrc\s*=\s*"([^"]+)"', text),
            *re.findall(r"url\(\s*([^)\s]+)\s*\)", text),
        ]
        for tag in re.findall(r"<link\b[^>]*>", text):
            rel = re.search(r'rel\s*=\s*"([^"]+)"', tag)
            href = re.search(r'href\s*=\s*"([^"]+)"', tag)
            if href and rel and rel.group(1) != "canonical":
                fetched.append(href.group(1))
        for target in fetched:
            if target.startswith(("http://", "https://", "//")):
                raise BuildError(f"{name} fetches {target} from the network.")

    return out


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    try:
        artefacts = build()
    except BuildError as exc:
        print(f"BUILD FAILED\n{exc}", file=sys.stderr)
        return 1

    if check_only:
        problems = []
        for name, data in sorted(artefacts.items()):
            path = HERE / name
            if not path.exists():
                problems.append(f"missing: {name}")
            elif path.read_bytes() != data:
                problems.append(f"differs: {name}")
        for path in sorted(HERE.iterdir()):
            if path.name in ("build.py", "check.py", "__pycache__") or path.name.startswith("."):
                continue
            if path.is_file() and path.name not in artefacts:
                problems.append(f"unexpected: {path.name}")
        if problems:
            print("DRIFT\n  " + "\n  ".join(problems), file=sys.stderr)
            return 1
        print(f"No drift. {len(artefacts)} files match.")
        return 0

    for name, data in sorted(artefacts.items()):
        (HERE / name).write_bytes(data)
    for path in sorted(HERE.iterdir()):
        if path.name in ("build.py", "check.py", "__pycache__") or path.name.startswith("."):
            continue
        if path.is_file() and path.name not in artefacts:
            path.unlink()

    total = sum(len(v) for v in artefacts.values())
    print(f"Wrote {len(artefacts)} files, {total / 1_000_000:.2f} MB total, into 11_site/")
    for name in sorted(artefacts):
        print(f"  {name:<26} {len(artefacts[name]) / 1024:8.1f} KB")
    print("\nCNAME carries no header comment. GitHub Pages parses the whole file as "
          "the hostname, so a comment would break the custom domain. It is the only "
          "file here without one.")
    print(f"\nBangla left in English, because "
          f"06_type/BANGLA-STANDARD.md has no verified string ({len(BANGLA_GAPS)}):")
    for gap in BANGLA_GAPS:
        print(f"  · {gap}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
