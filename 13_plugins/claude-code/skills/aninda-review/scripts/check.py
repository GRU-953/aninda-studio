#!/usr/bin/env python3
"""Aninda Studio — check what already exists.

Measures what can be measured from the source, then says plainly what it cannot
see. The blind-spot list at the end of every run is not a disclaimer; it is part
of the result. A check that hides its own limits buys false confidence, which is
worse than no check.

  python check.py <path>              a file or a folder
  python check.py <path> --aaa        also report against AAA
  python check.py <path> --json out.json

Exit status: 0 nothing failed, 1 something failed, 3 not equipped to check this.

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
THEMES = ("light", "dark", "hc-light", "hc-dark")

CHECKABLE = {".css", ".html", ".htm", ".md", ".svg", ".js", ".ts", ".tsx", ".jsx", ".py", ".json"}
PROSE = {".md", ".html", ".htm"}
STYLE = {".css", ".html", ".htm", ".svg"}

BANNED_WORDS = ("simply", "just", "easy", "easily", "obviously", "of course", "clearly")
LATIN_ABBREVIATIONS = ("e.g.", "i.e.", "etc.")
AMERICAN_SPELLINGS = {
    "color": "colour",
    "colors": "colours",
    "behavior": "behaviour",
    "organize": "organise",
    "organized": "organised",
    "center": "centre",
    "centered": "centred",
    "license": "licence (as a noun)",
    "analyze": "analyse",
    "favorite": "favourite",
    "gray": "grey",
    "catalog": "catalogue",
    "defense": "defence",
}
# `color` is a CSS property, `colors` is part of forced-colors, and `license` is
# an SPDX field and a filename. The spelling check skips a line that is one of
# those rather than a piece of writing.
SPELLING_EXEMPT = re.compile(
    r"(color\s*:|--as-|background-color|currentColor|colorSpace|SPDX|License-Identifier"
    r"|\.color|colors\(|[\"']color[\"']|forced-color|forced colors|color-scheme"
    r"|LICENSE|\bLicense\b|license[\"']?\s*:|licenses/|openfontlicense)"
)

# Verbatim legal text. It must not be reworded to suit a house style, so the prose
# checks do not run over it at all.
VERBATIM = re.compile(r"^(LICENSE|LICENCE|NOTICE|COPYING)|OFL.*\.txt$|-OFL\.txt$", re.I)

# A document that states a rule has to name the word the rule is about. A word
# inside backticks or emphasis is a citation, and a line that states the ban is
# the rule itself. Neither is a use. This is kept narrow on purpose: plain prose
# use is still caught.
CITED = re.compile(r"`[^`]*`|\*\*[^*]*\*\*|\*[^*]*\*|\"[^\"]*\"|'[^']*'")
RULE_STATEMENT = re.compile(
    r"(banned|never |do not |don't |must not |may not |forbidden|no such|does not exist"
    r"|is always wrong|REFUSED|instead of|rather than|write '|write \*)",
    re.I,
)


# Two limits, so a very large file is reported rather than appearing to hang.
# Both are stated in the output every run, because a file that was not checked
# must never be counted as a file that passed.
#
# 1 MB per file. Measured on this project: a 331 KB card takes about 2 seconds and
#   a 586 KB one takes over 90, because the pattern work is superlinear in the
#   length of a single line.
# 4000 characters per line for the prose checks. A line longer than that is
#   minified or generated output, not writing, and the prose rules do not apply to
#   it in any useful way.
MAX_FILE_BYTES = 1_000_000
MAX_LINE_CHARS = 4000


def spans_of(pattern: re.Pattern[str], line: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in pattern.finditer(line)]


def inside(spans: list[tuple[int, int]], start: int, end: int) -> bool:
    return any(a <= start and end <= b for a, b in spans)


SENTENCE_WORD_LIMIT = 25
TARGET_FLOOR_PX = 24
SPACING_SCALE = (4, 8, 12, 16, 24, 32, 48, 64, 96, 128)
DURATIONS_MS = (120, 220)
BENGALI = re.compile(r"[ঀ-৿]")

# Bangla may appear in two kinds of file and nowhere else.
#
# RECORD — permanently. These do not ship Bangla; they are ABOUT it. The standard
# and the string register are the record of the decision. The type documents name
# Bengali faces and Bengali typographic features — মাত্রা is the headstroke, and a
# measurement of it cannot be written without naming it. 01_research narrates the
# work and its removal. Every one of these is still held to the English standard in
# every other respect, which is why they stay on the checked-path list rather than
# being exempted from it wholesale.
BANGLA_RECORD = (
    "06_type/BANGLA-STANDARD.md",
    "06_type/BANGLA-STRINGS.md",
    "06_type/MEASUREMENTS.md",
    "06_type/SHORTLIST.md",
    "06_type/RECOMMENDATION.md",
    "06_type/pairings.md",
    "01_research/",
)

# PENDING — temporarily, while the removal is in progress. Listed rather than
# exempted in silence, because a silent exemption is how a partial removal comes to
# look like a finished one.
#
# THIS TUPLE IS THE ACCEPTANCE TEST FOR THE WHOLE JOB. It must be empty before the
# removal can be called done, and when it is empty this gate proves that no Bangla
# ships anywhere outside the record. Do not add to it to make a build pass.
BANGLA_PENDING = (
    # 09_guidebook/chapters was here until 27 August 2026 and is not any more:
    # thirteen English chapters, no Bangla sections, no language toggle. The list
    # is empty because the removal reached it, which is the only way this list is
    # allowed to shrink.
)

# The studio's own name, which stays.
#
# A NAME IS NOT TEXT. It is not translated, it does not need a verified-string
# list, and dropping Bangla from what this system BUILDS does not rename the
# studio — "Aninda" is the romanised form of অনিন্দ্য and says so in
# references/naming.md, which is the one place a reader can find out why the
# English is not spelled "Anindya".
#
# Allowed as a STRING rather than by exempting files, because the alternative was a
# list naming TRADEMARKS.md, two NOTICE files, licence.md, naming.md and logo.md —
# six exemptions for one word, each of which would then also carry a licence to put
# any other Bangla in those files. This way the rule is what it sounds like.
STUDIO_NAME_BN = ("অনিন্দ্য স্টুডিও", "অনিন্দ্য")
# A run of Bengali script, allowing the spaces and punctuation that fall inside a
# Bangla phrase, but stopping at the first Latin character.
BENGALI_RUN = re.compile(r"[ঀ-৿](?:[ঀ-৿]|[  —\-,।](?=[ঀ-৿]))*")


class NotEquipped(Exception):
    pass


@dataclass
class Findings:
    failures: list[dict] = field(default_factory=list)
    notes: list[dict] = field(default_factory=list)
    checked: dict[str, int] = field(default_factory=dict)

    def fail(self, where: str, what: str, measured: str, criterion: str) -> None:
        self.failures.append(
            {"where": where, "what": what, "measured": measured, "criterion": criterion}
        )

    def note(self, where: str, what: str, detail: str = "") -> None:
        self.notes.append({"where": where, "what": what, "detail": detail})

    def did(self, name: str, count: int = 1) -> None:
        self.checked[name] = self.checked.get(name, 0) + count


BLIND_SPOTS = [
    "Whether anything here is actually usable. Contrast, target size and focus "
    "visibility are measurable; whether a person can finish a task is not.",
    "Anything that needs a browser. These are static-source checks, so a colour that "
    "comes from a computed value, an inherited value, a gradient, an image, or a style "
    "set by JavaScript is invisible here. To measure a rendered page, use "
    "08_components/check.py in the main project, which drives a real browser.",
    "Mid-transition states. A colour that dips below its floor for 60 ms on its way "
    "somewhere is not seen.",
    "Specificity and the cascade. This reads each CSS rule on its own, so a colour "
    "overridden later, or one inherited from a parent selector, is not resolved.",
    "Whether a heading structure makes sense, and whether an alt text describes the "
    "right thing. Both need a person.",
    "Whether the English is actually clear. Sentence length and a banned-word list are "
    "proxies; a short sentence can still be baffling.",
    "Whether a licence choice is legally sound. This checks that the files exist and "
    "that the identifiers and URLs are right. It is not legal advice.",
    "Text inside an image, a PDF, a font, or a compiled bundle.",
    f"Any file over {MAX_FILE_BYTES:,} bytes, and any single line over {MAX_LINE_CHARS:,} "
    "characters. Both are skipped, and both are named in the notes, so a file that was not "
    "checked is never counted as a file that passed.",
]


# ---------------------------------------------------------------------------
# The system's own numbers
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


def properties_from_css(text: str) -> dict[str, str]:
    """Every `--as-*` property tokens.css defines, mapped to its light-theme value.

    WHY THIS IS READ AND NOT DERIVED. This checker used to recommend a fix by
    substituting hyphens for the dots in a DTCG role name — `accent.default`
    became `--as-accent-default` inside a var(). 07_tokens/emit_css.py drops a trailing
    `default` segment and a leading `status` one, so `--as-accent-default` is not a
    property this system has; in a browser the undefined name resolves to nothing
    and the text falls back to inherited black. Seven of the seventeen roles this
    checker can name produced a property that does not exist, and it handed each
    one to a user as the recommended fix.

    Reading the names out of the stylesheet means the recommendation is measured
    against the artefact the user will actually link.
    """
    out: dict[str, str] = {}
    for name, value in re.findall(r"(--as-[a-z0-9-]+)\s*:\s*([^;}]+)", text):
        out.setdefault(name, value.strip())
    return out


def property_for_role(role: str, properties: dict[str, str]) -> str | None:
    """The CSS property for a DTCG role, by the rule emit_css.py uses.

    `color.` has already been stripped from `role` by the caller. The rule is
    emit_css.py's prop_for(): drop a leading `status` segment, drop a trailing
    `default` one. The result is then CHECKED against the properties the
    stylesheet defines, so a change to that rule cannot silently reappear here as
    advice to write a name that resolves to nothing.
    """
    parts = role.split(".")
    if parts and parts[0] == "status":
        parts = parts[1:]
    if len(parts) > 1 and parts[-1] == "default":
        parts = parts[:-1]
    name = "--as-" + "-".join(parts)
    return name if name in properties else None


def load_system() -> dict:
    """The role hexes, the token values and the CSS property names.

    Two layouts are supported. Installed as a plugin, the three skills sit side
    by side and this reads the brand skill's own assets, so there is one source
    of truth. Extracted from a standalone .skill bundle, it reads the data file
    the bundler wrote in. If neither is there, it says so rather than guessing.
    """
    tokens_dir = SKILL_ROOT.parent / "aninda-brand" / "assets" / "tokens"
    css_path = SKILL_ROOT.parent / "aninda-brand" / "assets" / "css" / "tokens.css"
    if tokens_dir.is_dir() and css_path.exists():
        primitives = _flatten(json.loads((tokens_dir / "primitive.tokens.json").read_text("utf-8")), "", {})

        def hex_of(value):
            if isinstance(value, str):
                return hex_of(primitives[value.strip().strip("{}")])
            return value["hex"]

        themes: dict[str, dict[str, str]] = {}
        targets: dict[str, dict[str, float]] = {}
        for theme in THEMES:
            raw = json.loads((tokens_dir / f"semantic.{theme}.tokens.json").read_text("utf-8"))
            flat = _flatten(raw, "", {})
            themes[theme] = {
                key[len("color.") :]: hex_of(value)
                for key, value in flat.items()
                if key.startswith("color.")
            }
            studio = raw.get("$extensions", {}).get("studio.aninda", {})
            targets[theme] = {
                "text": float(studio.get("textTarget", 4.5)),
                "nonText": float(studio.get("nonTextTarget", 3.0)),
            }
        return {
            "themes": themes,
            "targets": targets,
            "properties": properties_from_css(css_path.read_text("utf-8")),
            "source": "the aninda-brand skill's own token files",
        }

    bundled = SKILL_ROOT / "data" / "system.json"
    if bundled.exists():
        data = json.loads(bundled.read_text("utf-8"))
        data["source"] = "the data file bundled into this .skill"
        return data

    raise NotEquipped(
        "I cannot find the system's numbers. This skill reads them from the "
        "aninda-brand skill's assets/tokens folder and assets/css/tokens.css when "
        "both are installed together, or from data/system.json inside a standalone "
        ".skill bundle. Neither is here."
    )


# ---------------------------------------------------------------------------
# Contrast
# ---------------------------------------------------------------------------


def to_rgb(value: str) -> tuple[int, int, int] | None:
    text = value.strip().lstrip("#")
    if len(text) == 3:
        text = "".join(c * 2 for c in text)
    if len(text) == 8:
        text = text[:6]
    if len(text) != 6 or not re.fullmatch(r"[0-9A-Fa-f]{6}", text):
        return None
    return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)


def luminance(rgb) -> float:
    def channel(v: int) -> float:
        c = v / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2])


def ratio(a: str, b: str) -> float | None:
    ra, rb = to_rgb(a), to_rgb(b)
    if ra is None or rb is None:
        return None
    la, lb = luminance(ra), luminance(rb)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

RULE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
DECLARATION = re.compile(r"([-a-zA-Z]+)\s*:\s*([^;]+)")
VAR_REF = re.compile(r"var\(\s*(--as-[a-z0-9-]+)")
HEX = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
PX = re.compile(r"(-?\d+(?:\.\d+)?)px")
MS = re.compile(r"(\d+(?:\.\d+)?)(ms|s)\b")

INTERACTIVE = re.compile(
    r"(button|\[type=|input|select|textarea|\ba\b|\.btn|\.button|role=[\"']button|"
    r"summary|\[tabindex|\.tab\b|\.chip\b|\.link\b)",
    re.I,
)

# The role a CSS custom property stands for, so var() can be resolved.
def role_of(custom_property: str) -> str | None:
    name = custom_property[len("--as-") :]
    for prefix in ("surface-", "ink-", "line-", "accent-", "focus-", "status-"):
        if name.startswith(prefix):
            return name.replace("-", ".", 1) if name.count("-") >= 1 else None
    return None


def foreground_and_background(declarations: str) -> tuple[str | None, str | None]:
    fg = bg = None
    for prop, raw in DECLARATION.findall(declarations):
        prop = prop.strip().lower()
        value = raw.strip()
        if prop == "color":
            fg = value
        elif prop in ("background", "background-color"):
            bg = value
    return fg, bg


def literal_or_role(value: str) -> tuple[str | None, str | None]:
    """Return (literal hex, role name) for a CSS value."""
    match = VAR_REF.search(value)
    if match:
        return None, role_of(match.group(1))
    found = HEX.search(value)
    if found:
        return found.group(0), None
    return None, None


def check_css(text: str, where: str, system: dict, found: Findings, aaa: bool) -> None:
    seen_forced_colors = "forced-colors" in text
    seen_reduced_motion = "prefers-reduced-motion" in text
    seen_focus_visible = ":focus-visible" in text
    uses_motion = bool(re.search(r"\b(transition|animation)\s*:", text))

    for selector, declarations in RULE.findall(text):
        selector = " ".join(selector.split())
        if selector.startswith("@"):
            continue

        # --- contrast ------------------------------------------------------
        fg_value, bg_value = foreground_and_background(declarations)
        if fg_value and bg_value:
            fg_hex, fg_role = literal_or_role(fg_value)
            bg_hex, bg_role = literal_or_role(bg_value)
            for theme in THEMES:
                roles = system["themes"][theme]
                fg = fg_hex or (roles.get(fg_role) if fg_role else None)
                bg = bg_hex or (roles.get(bg_role) if bg_role else None)
                if not fg or not bg:
                    continue
                measured = ratio(fg, bg)
                if measured is None:
                    continue
                target = system["targets"][theme]["text"]
                found.did("contrast pairings measured")
                if measured + 1e-9 < target:
                    found.fail(
                        f"{where}  {selector}",
                        f"text {fg} on {bg} in the {theme} theme",
                        f"{measured:.2f}:1 against a target of {target:.1f}:1",
                        "WCAG 2.2 success criterion 1.4.3 Contrast (Minimum), level AA",
                    )
                elif aaa and measured + 1e-9 < 7.0:
                    found.note(
                        f"{where}  {selector}",
                        f"text {fg} on {bg} in the {theme} theme meets AA but not AAA",
                        f"{measured:.2f}:1, and AAA asks for 7:1 — WCAG 1.4.6",
                    )
                # Only the two literal-hex pairings are theme-independent.
                if fg_hex and bg_hex:
                    break

        # --- raw values ----------------------------------------------------
        for prop, raw in DECLARATION.findall(declarations):
            prop = prop.strip().lower()
            value = raw.strip()

            if prop.startswith("--") and not prop.startswith("--as-"):
                found.note(
                    f"{where}  {selector}",
                    f"the custom property {prop} does not begin with --as-",
                    "One prefix means one system. A second prefix means two.",
                )

            if prop in ("color", "background", "background-color", "border-color", "fill", "stroke"):
                literal = HEX.search(value)
                if literal:
                    hex_value = literal.group(0).upper()
                    properties = system.get("properties", {})
                    for theme in THEMES:
                        for role, role_hex in system["themes"][theme].items():
                            if role_hex.upper() != hex_value:
                                continue
                            css_property = property_for_role(role, properties)
                            if css_property:
                                advice = (f"That is {role} in the {theme} theme. "
                                          f"Use var({css_property}) so it follows "
                                          f"the theme.")
                            else:
                                # No invented name. Naming the role and admitting
                                # the property could not be found is worth more
                                # than a name that resolves to nothing.
                                advice = (
                                    f"That is {role} in the {theme} theme. I could "
                                    f"not find a custom property for it in the "
                                    f"tokens.css this skill carries, so read the "
                                    f"property name off that file rather than "
                                    f"taking one from me."
                                )
                            found.note(
                                f"{where}  {selector}",
                                f"{prop} is the raw hex {hex_value}, and a token exists for it",
                                advice,
                            )
                            break
                        else:
                            continue
                        break

            if prop in (
                "margin", "padding", "gap", "row-gap", "column-gap",
                "margin-top", "margin-right", "margin-bottom", "margin-left",
                "padding-top", "padding-right", "padding-bottom", "padding-left",
            ):
                # A hairline of 1 px, and the visually-hidden clip idiom, are both
                # legitimate and neither belongs on a spacing scale.
                hidden = re.search(r"visually-hidden|sr-only|screen-reader", selector, re.I)
                for number in PX.findall(value):
                    pixels = float(number)
                    if pixels == 0 or abs(pixels) == 1 or hidden:
                        continue
                    if abs(pixels) not in SPACING_SCALE:
                        found.note(
                            f"{where}  {selector}",
                            f"{prop} uses {number}px, which is not on the 4 px scale",
                            "The scale is " + ", ".join(str(s) for s in SPACING_SCALE) + " px.",
                        )

            if prop in ("transition", "transition-duration", "animation", "animation-duration"):
                for number, unit in MS.findall(value):
                    milliseconds = float(number) * (1000 if unit == "s" else 1)
                    if milliseconds not in DURATIONS_MS and milliseconds not in (0.0, 1.0):
                        found.note(
                            f"{where}  {selector}",
                            f"{prop} uses {number}{unit}, which is not one of the two durations",
                            "The system has 120 ms for a colour change and 220 ms for a move. "
                            "A third duration is a decision nobody wrote down.",
                        )

            if prop == "outline" and value.strip().lower() in ("none", "0", "0px"):
                if "focus" in selector.lower() and "box-shadow" not in declarations:
                    found.fail(
                        f"{where}  {selector}",
                        "outline is removed on a focus selector with nothing put back",
                        "outline: none, and no box-shadow or border in the same rule",
                        "WCAG 2.2 success criterion 2.4.7 Focus Visible, level AA",
                    )

            if prop in ("height", "min-height", "width", "min-width") and INTERACTIVE.search(selector):
                for number in PX.findall(value):
                    pixels = float(number)
                    if 0 < pixels < TARGET_FLOOR_PX:
                        found.fail(
                            f"{where}  {selector}",
                            f"an interactive element declares {prop}: {number}px",
                            f"{number}px against a floor of {TARGET_FLOOR_PX} CSS px",
                            "WCAG 2.2 success criterion 2.5.8 Target Size (Minimum), level AA",
                        )

        if "forced-color-adjust" in declarations and "none" in declarations:
            if "allow-list" not in text and "allowlist" not in text:
                found.fail(
                    f"{where}  {selector}",
                    "forced-color-adjust: none, with no allow-list note beside it",
                    "It is forbidden unless it is explicitly allow-listed with a stated reason",
                    "The system's own forced-colors rule, from forced-colors.map.json",
                )

    if uses_motion and not seen_reduced_motion:
        found.fail(
            where,
            "there are transitions or animations, and no prefers-reduced-motion block",
            "no @media (prefers-reduced-motion: reduce) anywhere in the file",
            "WCAG 2.2 success criterion 2.3.3 Animation from Interactions, level AAA, "
            "and the system's own motion rule, which is stricter",
        )
    # A reduce block that flattens EVERY transition on a wildcard selector. This
    # was only a PRESENCE check: a file could satisfy it and still delete the
    # cross-fade the rule explicitly allows, which is what the snippet in
    # references/motion.md did for months, directly under a sentence saying "a
    # colour change may stay".
    #
    # Removing a transition is not reducing motion. It replaces a smooth change
    # with a jump, which is a harsher change than the one being softened.
    # The inner rule keeps its own closing brace, or RULE below cannot match it.
    for block in re.findall(r"@media[^{]*prefers-reduced-motion[^{]*\{(.*?\})\s*\}",
                            text, re.S):
        for selector, declarations in RULE.findall(block):
            if " ".join(selector.split()) not in ("*", "*, *::before, *::after",
                                                  "*,*::before,*::after"):
                continue
            if re.search(r"(transition|animation)-duration\s*:\s*0?\.?0*(?:m?s)?\b"
                         r"|(transition|animation)-duration\s*:\s*1ms", declarations):
                found.fail(
                    where,
                    "a reduced-motion block flattens every transition on a wildcard",
                    f"{selector} {{ {' '.join(declarations.split())[:60]} }}",
                    "the motion rule allows a colour change to stay. A wildcard "
                    "takes the cross-fade with the movement, so a hover that was a "
                    "gentle tint becomes a snap. Collapse the movement duration and "
                    "leave the colour one alone.",
                )
    if not seen_forced_colors and RULE.search(text):
        found.note(
            where,
            "no forced-colors block",
            "Every brand colour must yield to the operating system's palette. A hex that "
            "survives forced-colors mode defeats the point of the mode.",
        )
    if not seen_focus_visible and INTERACTIVE.search(text):
        found.note(
            where,
            "no :focus-visible rule",
            "Focus must be visible in all four themes, with a 3 px ring and a 2 px offset.",
        )

    declared_themes = [t for t in THEMES if t in text]
    if declared_themes and len(declared_themes) < len(THEMES):
        found.note(
            where,
            f"only {len(declared_themes)} of the four themes appear",
            "Found " + ", ".join(declared_themes) + ". The system has all four: " + ", ".join(THEMES),
        )
    found.did("stylesheets read")


# ---------------------------------------------------------------------------
# Prose
# ---------------------------------------------------------------------------

TAG = re.compile(r"<(/?)([a-zA-Z][-a-zA-Z0-9]*)\b[^>]*>")
CODE_FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`]*`")

# Tags that keep words on the same line. Everything else ends the line, so text
# from two separate elements is never read as one very long sentence.
INLINE_TAGS = {
    "a", "span", "em", "strong", "b", "i", "u", "small", "abbr", "kbd",
    "samp", "var", "sup", "sub", "mark", "q", "cite", "time", "bdi", "bdo", "wbr",
}


def visible_prose(text: str, suffix: str) -> str:
    if suffix in (".html", ".htm"):
        # A code sample is not prose. Its contents go, not just its tags — an
        # HTML comment shown inside <code> would otherwise read as writing.
        text = re.sub(r"<(script|style|pre|code)\b.*?</\1>", "\n", text, flags=re.S | re.I)
        text = re.sub(r"<!--.*?-->", "\n", text, flags=re.S)
        text = re.sub(r"<![^>]*>", "\n", text)  # the doctype and any declaration
        text = TAG.sub(lambda m: " " if m.group(2).lower() in INLINE_TAGS else "\n", text)
    else:
        text = CODE_FENCE.sub("\n", text)
        # An HTML comment in Markdown is a note to whoever edits the file. It is
        # not prose a reader sees, so it is not checked as prose.
        text = re.sub(r"<!--.*?-->", "\n", text, flags=re.S)
        text = INLINE_CODE.sub(" ", text)
    return text


def check_prose(text: str, where: str, system: dict, found: Findings) -> None:
    prose = visible_prose(text, Path(where).suffix.lower())
    found.did("prose files read")

    over_long = 0
    for line_number, line in enumerate(prose.split("\n"), start=1):
        if len(line) > MAX_LINE_CHARS:
            over_long += 1
            continue
        lower = line.lower()
        cited = spans_of(CITED, line)
        stating_a_rule = bool(RULE_STATEMENT.search(line))

        for word in BANNED_WORDS:
            for match in re.finditer(r"\b" + re.escape(word) + r"\b", lower):
                if inside(cited, match.start(), match.end()) or stating_a_rule:
                    found.did("banned words cited rather than used")
                    continue
                found.fail(
                    f"{where}:{line_number}",
                    f"the banned word {word!r}",
                    line.strip()[max(0, match.start() - 30) : match.start() + 40].strip(),
                    "The English standard: every one of these tells a reader who is stuck "
                    "that the problem is them",
                )
        if "!" in line and not re.search(r"(!=|!important|<!--|!\[|\w!\w)", line):
            position = line.index("!")
            if not inside(cited, position, position + 1):
                found.fail(
                    f"{where}:{line_number}",
                    "an exclamation mark",
                    line.strip()[:80],
                    "The English standard: warmth comes from the words, not the punctuation",
                )
        for abbreviation in LATIN_ABBREVIATIONS:
            position = lower.find(abbreviation)
            if position == -1:
                continue
            if inside(cited, position, position + len(abbreviation)) or stating_a_rule:
                found.did("banned words cited rather than used")
                continue
            found.fail(
                f"{where}:{line_number}",
                f"the Latin abbreviation {abbreviation!r}",
                line.strip()[:80],
                "The English standard: write 'for example', 'that is', 'and so on'",
            )
        if not SPELLING_EXEMPT.search(line):
            for american, british in AMERICAN_SPELLINGS.items():
                match = re.search(r"\b" + american + r"\b", lower)
                if not match or inside(cited, match.start(), match.end()) or stating_a_rule:
                    continue
                found.note(
                    f"{where}:{line_number}",
                    f"the American spelling {american!r}",
                    f"British spelling is the standard here: {british}.",
                )
        match = re.search(r"\bwe\b", lower)
        if match and not inside(cited, match.start(), match.end()) and not stating_a_rule:
            found.note(
                f"{where}:{line_number}",
                "'we' used where the studio is one person",
                "First person singular. Using 'we' to sound larger is the first small "
                "dishonesty a studio tells about itself.",
            )

    if over_long:
        found.note(
            where,
            f"{over_long} line(s) longer than {MAX_LINE_CHARS} characters were not checked as prose",
            "A line that long is minified or generated output rather than writing, and the "
            "wording rules do not apply to it in any useful way.",
        )

    # Sentences are counted inside a line, never across two. Text from two
    # separate elements is two pieces of writing, not one long sentence.
    for line in prose.split("\n"):
        if len(line) > MAX_LINE_CHARS:
            continue
        for sentence in re.split(r"(?<=[.?।])\s+", line):
            words = [w for w in re.split(r"\s+", sentence.strip()) if w]
            if len(words) > SENTENCE_WORD_LIMIT:
                found.note(
                    where,
                    f"a sentence of {len(words)} words",
                    "The standard asks for 15 to 20 on average and says to break anything over "
                    f"{SENTENCE_WORD_LIMIT}. First words: " + " ".join(words[:12]) + " …",
                )

    # This system ships English. Bangla was removed on 27 August 2026, and two
    # documents were kept as the record of why — they are the only files it may
    # appear in.
    #
    # This is the INVERSE of the check that stood here, which asked whether a
    # Bangla string was on a verified list. Finding R7-1 recorded that that rule
    # was enforced where the words were SHOWN and not where they ENTERED, which is
    # how Bangla nobody had checked reached the palette. Inverting it closes both
    # doors, because there is no longer a door: the question is not "was this
    # checked?" but "why is this here?".
    #
    # It is a FAILURE and not a note, because nothing downstream applies the
    # Bangla rules any more. There is no :lang(bn) block, no Bengali face in the
    # subsets and no multiplier, so a Bangla run would fall back to whatever
    # Bengali font the reader's machine happens to have, at the Latin size, and
    # would fail WCAG 2.2 SC 3.1.2 with an English speech engine besides.
    for line_number, line in enumerate(prose.split("\n"), start=1):
        if len(line) > MAX_LINE_CHARS or not BENGALI.search(line):
            continue
        place = str(where).replace("\\", "/")
        if any(place.endswith(r) or f"/{r}" in place + "/" for r in BANGLA_RECORD):
            found.did("Bangla in a retained record, which is where it belongs")
            continue
        if any(f"/{r}" in place + "/" or place.startswith(r) for r in BANGLA_PENDING):
            found.note(
                f"{where}:{line_number}",
                "Bangla still here while the removal is in progress",
                "This path is in BANGLA_PENDING in this checker. That list is the "
                "acceptance test for the removal and has to reach empty.",
            )
            continue
        for match in BENGALI_RUN.finditer(line):
            candidate = " ".join(match.group(0).split()).strip(" —-,।")
            if not candidate:
                continue
            if any(candidate == name or candidate in name
                   for name in STUDIO_NAME_BN):
                found.did("the studio's own name, which is a name and not text")
                continue
            found.fail(
                f"{where}:{line_number}",
                "Bangla in a system that ships English",
                f"{candidate[:70]!r}",
                "Bangla was removed on 27 August 2026. Nothing applies the Bangla "
                "rules any more, so this would render in whatever Bengali font the "
                "reader happens to have, at the Latin size. The record of the "
                "decision lives in 06_type/BANGLA-STANDARD.md. If this run is a "
                "record rather than shipped prose, it belongs in BANGLA_RECORD in "
                "this checker, named and reasoned — not exempted quietly.",
            )


# ---------------------------------------------------------------------------
# Licences
# ---------------------------------------------------------------------------


REPOSITORY_MARKERS = (
    ".git", "package.json", "pyproject.toml", "requirements.txt", "LICENSE", "LICENSE.txt",
)


def looks_like_repository_root(path: Path) -> bool:
    return any((path / marker).exists() for marker in REPOSITORY_MARKERS)


def check_licences(root: Path, found: Findings) -> None:
    if not root.is_dir():
        return
    found.did("repositories checked for licences")
    for names, why in (
        (("LICENSE", "LICENSE.txt"), "the full Apache-2.0 text, for the system and the scripts"),
        (("NOTICE", "NOTICE.txt"), "all four licences, each with what it covers"),
    ):
        if not any((root / name).exists() for name in names):
            found.fail(
                str(root),
                f"{names[0]} is missing",
                why,
                "The licence split: system Apache-2.0, writing PolyForm Noncommercial 1.0.0, "
                "fonts SIL OFL 1.1, identity not licensed at all",
            )
    for name in ("LICENSE-DOCS.md", "LICENSE-DOCS.txt"):
        if (root / name).exists():
            break
    else:
        found.note(
            str(root),
            "no LICENSE-DOCS file",
            "The written documentation is PolyForm Noncommercial 1.0.0 and needs its own text.",
        )
    if not (root / "TRADEMARKS.md").exists():
        found.note(
            str(root),
            "no TRADEMARKS.md",
            "The name, mark, wordmark, tile and lockups are not licensed at all, and that is "
            "worth saying somewhere a reader will look.",
        )

    for font in list(root.rglob("*.woff2")) + list(root.rglob("*.ttf")) + list(root.rglob("*.otf")):
        siblings = list(font.parent.glob("*OFL*"))
        if not siblings:
            found.fail(
                str(font),
                "a font file with no OFL licence file beside it",
                "SIL OFL 1.1 asks for the licence to travel with the font",
                "SIL Open Font License 1.1, and there is no version 1.2",
            )


def check_licence_text(text: str, where: str, found: Findings) -> None:
    for match in re.finditer(r"polyformproject\.org/licenses/noncommercial/1\.0\.0/", text):
        found.fail(
            where,
            "the PolyForm URL has a trailing slash",
            text[max(0, match.start() - 20) : match.end() + 10].strip(),
            "The trailing-slash form returns 404. The canonical URL is "
            "https://polyformproject.org/licenses/noncommercial/1.0.0",
        )
    for match in re.finditer(r"\bOFL[\s-]*1\.2\b", text, re.I):
        # A window rather than a line, because a sentence that says this version
        # does not exist often wraps across two lines.
        window = text[max(0, match.start() - 160) : match.end() + 160]
        if RULE_STATEMENT.search(window) or "1.1" in window:
            found.did("wrong-version references cited rather than used")
            continue
        found.fail(
            where,
            "a reference to OFL 1.2",
            " ".join(window.split())[:100],
            "There is no SIL OFL version 1.2. Version 1.1 dates from 26 February 2007",
        )
    if "PolyForm" in text and "open source" in text.lower():
        window = text.lower()
        if "not open source" not in window and "not approved" not in window:
            found.note(
                where,
                "PolyForm is mentioned near 'open source' without the correction",
                "PolyForm Noncommercial is source-available, not open source. It is not "
                "OSI-approved, because the Open Source Definition does not allow a restriction "
                "on a field of use.",
            )


# ---------------------------------------------------------------------------
# Walking
# ---------------------------------------------------------------------------

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    ".mypy_cache", ".pytest_cache", "browsers",
}


def files_under(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    out = []
    for path in sorted(target.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in CHECKABLE:
            out.append(path)
    return out


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="check.py", description=__doc__.split("\n")[0])
    parser.add_argument("path", help="a file or a folder to check")
    parser.add_argument("--aaa", action="store_true", help="also report AAA, where AAA exists")
    parser.add_argument("--json", dest="json_out", default=None, help="write the full report here")
    args = parser.parse_args(argv)

    target = Path(args.path).expanduser().resolve()
    if not target.exists():
        sys.stderr.write(f"\nNOT EQUIPPED: there is nothing at {target}\n\n")
        return 3

    try:
        system = load_system()
    except NotEquipped as problem:
        sys.stderr.write(f"\nNOT EQUIPPED: {problem}\n\n")
        return 3

    found = Findings()
    paths = files_under(target)
    if not paths:
        sys.stderr.write(
            f"\nNOT EQUIPPED: nothing under {target} has a suffix I can read. "
            f"I read: {', '.join(sorted(CHECKABLE))}\n\n"
        )
        return 3

    for path in paths:
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            found.note(
                str(path),
                f"not checked: it is {size:,} bytes, over the {MAX_FILE_BYTES:,} byte limit",
                "The pattern work is superlinear in the length of a single line, so a file this "
                "big would appear to hang. Point the checker at the source this file was "
                "generated from instead, or at the folder holding its parts.",
            )
            found.did("files too big to check")
            continue
        try:
            text = path.read_text("utf-8")
        except (UnicodeDecodeError, OSError):
            found.note(str(path), "could not be read as UTF-8 text", "Skipped.")
            continue
        suffix = path.suffix.lower()
        where = str(path)
        verbatim = bool(VERBATIM.match(path.name))
        if verbatim:
            found.did("verbatim licence texts left alone")
        if suffix in STYLE and not verbatim:
            check_css(text, where, system, found, args.aaa)
        if suffix in PROSE and not verbatim:
            check_prose(text, where, system, found)
        check_licence_text(text, where, found)

    # The licence check is about a repository, so it only runs at a repository
    # root. Asking a subfolder for a NOTICE file beside it would be a failure the
    # reader can do nothing sensible about.
    if target.is_dir() and looks_like_repository_root(target):
        check_licences(target, found)
    else:
        found.note(
            str(target),
            "the licence check did not run",
            "It runs only at a repository root — a folder holding a .git, a package.json, a "
            "pyproject.toml, a requirements.txt, or a LICENSE. Point it at the root to check "
            "the four licences.",
        )

    report = {
        "checked": str(target),
        "files": len(paths),
        "system numbers from": system["source"],
        "aaa reported": bool(args.aaa),
        "counts": found.checked,
        "failures": found.failures,
        "notes": found.notes,
        "blind spots": BLIND_SPOTS,
    }
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", "utf-8")

    out: list[str] = ["", f"Checked {len(paths)} file(s) under {target}", ""]
    out.append(f"System numbers came from {system['source']}.")
    if found.checked:
        out.append("")
        for name in sorted(found.checked):
            out.append(f"  {found.checked[name]:>6}  {name}")

    out.append("")
    out.append(f"FAILURES ({len(found.failures)})")
    out.append("-" * 72)
    if not found.failures:
        out.append("  None.")
    for item in found.failures:
        out.append(f"  {item['where']}")
        out.append(f"    what      {item['what']}")
        out.append(f"    measured  {item['measured']}")
        out.append(f"    criterion {item['criterion']}")
        out.append("")

    out.append("")
    out.append(f"NOTES ({len(found.notes)})")
    out.append("-" * 72)
    if not found.notes:
        out.append("  None.")
    for item in found.notes[:200]:
        out.append(f"  {item['where']}")
        out.append(f"    {item['what']}")
        if item["detail"]:
            out.append(f"    {item['detail']}")
        out.append("")
    if len(found.notes) > 200:
        out.append(f"  … and {len(found.notes) - 200} more. Use --json to get them all.")

    out.append("")
    out.append("WHAT THIS CHECK CANNOT SEE")
    out.append("-" * 72)
    out.append("  Read these out. They are part of the result, not a disclaimer.")
    out.append("")
    for spot in BLIND_SPOTS:
        out.append(f"  - {spot}")
    out.append("")

    sys.stdout.write("\n".join(out) + "\n")
    return 1 if found.failures else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
