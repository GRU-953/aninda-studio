#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
Because a contrast figure that a person types is a contrast figure that is wrong.

Every colour in the Aninda Studio system is *computed* here and every pairing is
*measured* here. Nothing downstream may hand-write a hex value or a ratio.

Four specific failures this design prevents:

1. A ratio measured on floating-point colour, then shipped as an 8-bit hex.
   Rounding moves the colour, and the ratio moves with it. This engine rounds to
   hex FIRST and measures the rounded value, so the published number is the one a
   browser will actually produce. On top of that, every proven pair is re-measured
   with each channel of both colours nudged by ±1 — the worst of those 64 results
   is what gets published. That replaces a guessed safety margin with a measured
   one.

2. Surfaces taken from the main 11-step ramp. In a light theme all seven surfaces
   live between OKLCH L 0.93 and 1.00, where an 11-step ramp has one or two
   members — so several surfaces come out identical and the depth vocabulary is
   fictional. The surface ladder is therefore swept separately, at fine
   resolution, and checked for real perceptual separation.

3. A role proven against one background and then used on another. Text is proven
   here against EVERY surface it can legally land on, and the published ratio is
   the worst of them, not the flattering one.

4. A ramp that is monotonic in OKLCH lightness but not in relative luminance.
   Contrast depends on luminance, so lightness monotonicity alone proves nothing.
   Both are checked.

FAIL-CLOSED
-----------
If any check fails, this script writes nothing at all — not even for the
directions that passed. A consumer holding three proven themes and one missing
one will ship the gap without knowing it.

EXIT CODES
----------
    0  every direction built and proved
    1  a real failure — a palette cannot support a role
    2  could not run — a spec is missing or malformed

RUN
---
    cd /Users/gru953/Claude/Cowork/Aninda_Studio
    ./.venv/bin/python 05_colour/engine.py
    ./.venv/bin/python 05_colour/engine.py --only estuary
    ./.venv/bin/python 05_colour/engine.py --check     # verify, write nothing
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from coloraide import Color

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SPEC_DIR = HERE / "directions"
OUT_DIR = HERE / "generated"

# ---------------------------------------------------------------------------
# Specified constants. These are the ONLY numbers a person chose.
# Every other number in this system is measured.
# ---------------------------------------------------------------------------

# WCAG 2.2, W3C Recommendation of 12 December 2024.
AA_TEXT = 4.5      # 1.4.3 Contrast (Minimum) — normal text
AA_LARGE = 3.0     # 1.4.3 — large text (18pt, or 14pt bold)
AA_NONTEXT = 3.0   # 1.4.11 Non-text Contrast — UI components, graphical objects
AAA_TEXT = 7.0     # 1.4.6 Contrast (Enhanced)
# Note: WCAG defines no AAA level for non-text contrast. The high-contrast themes
# below hold non-text to 4.5, which is a POLICY choice sitting above 1.4.11's
# normative 3.0 — not a standard. It is recorded as such in the proof.
HC_NONTEXT = 4.5

STEPS: tuple[int, ...] = (50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950)

LIGHTNESS: dict[int, float] = {
    50: 0.977, 100: 0.945, 200: 0.888, 300: 0.822, 400: 0.740,
    500: 0.655, 600: 0.567, 700: 0.478, 800: 0.386, 900: 0.286, 950: 0.205,
}

# Near-white and near-black cannot hold much chroma without leaving sRGB, and
# forcing them to try produces muddy clipped colour. The peak sits slightly light
# of centre, where a hue reads as most itself.
CHROMA_ARC: dict[int, float] = {
    50: 0.16, 100: 0.30, 200: 0.55, 300: 0.78, 400: 0.94,
    500: 1.00, 600: 0.96, 700: 0.86, 800: 0.72, 900: 0.54, 950: 0.40,
}

# The seven tonal surfaces, swept at fine resolution rather than taken from the
# ramp. Five are the "container" ladder; dim and bright sit outside it. Keeping
# the same count as Material makes the system mappable onto it without adopting
# its vocabulary — these names say what a surface is FOR, not where it sits in
# someone else's hierarchy.
# The surface ladder is SWEPT, not tabulated. Hand-written lightness values were
# the first attempt and they were wrong in a way worth recording: CIEDE2000
# compresses hard near white and near black, so an evenly-spaced lightness ladder
# produces wildly uneven perceptual spacing. Near black it is worse still,
# because below about L 0.10 the sRGB 8-bit grid is coarser than the eye and two
# surfaces specified 0.03 apart round to nearly the same byte.
#
# So instead of choosing seven numbers, the engine declares where the ladder may
# live and how far apart the rungs must be, then walks the lightness axis at
# 1/2000 resolution taking a rung whenever it is far enough from the last one.
# The values are an outcome, which is the same rule every other number here obeys.
SURFACE_RANGE: dict[str, tuple[float, float]] = {
    "light": (0.855, 1.000),
    "dark": (0.128, 0.345),
    # High contrast widens the ladder rather than compressing it. Compressing was
    # the obvious first instinct — squeeze every surface toward the extreme so
    # 7:1 is easy — but it makes the surfaces themselves indistinguishable, and
    # someone who has turned high contrast on is the last person who should be
    # asked to tell two near-identical greys apart.
    "hc-light": (0.840, 1.000),
    "hc-dark": (0.100, 0.330),
}

# Rungs from darkest to lightest, per theme polarity. In a light theme the
# container ladder runs lightest-to-darkest as it does in Material, so ascending
# lightness reads dim, highest, high, base, low, lowest, bright.
LADDER_ORDER: dict[str, tuple[str, ...]] = {
    "light": ("dim", "highest", "high", "base", "low", "lowest", "bright"),
    "dark": ("dim", "lowest", "low", "base", "high", "highest", "bright"),
}

SURFACE_ORDER = ("lowest", "low", "base", "high", "highest", "dim", "bright")

# How much of the ground family's chroma a surface carries. A surface is a tinted
# neutral, not a pale version of the brand colour.
SURFACE_TINT = {"light": 0.030, "dark": 0.038, "hc-light": 0.014, "hc-dark": 0.020}

# Minimum perceptual separation between adjacent surfaces. A surface nobody can
# see is not a surface. Expressed in CIEDE2000 units.
MIN_SURFACE_DE = 0.9
MIN_RAMP_DE = 1.5


class Fail(Exception):
    """A real failure. Nothing is written."""


class NotEquipped(Exception):
    """Could not run — a spec is missing or malformed. Distinct from a failure."""


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------

def to_hex(c: Color) -> str:
    """Gamut-map into sRGB and round to eight bits per channel.

    `oklch-chroma` preserves hue and reduces chroma rather than clipping
    channels, so a colour that leaves sRGB desaturates instead of shifting hue.
    """
    return c.convert("srgb").fit(method="oklch-chroma").to_string(hex=True, upper=True)


def ratio(fg: str, bg: str) -> float:
    return round(Color(fg).contrast(Color(bg), method="wcag21"), 4)


def luminance(h: str) -> float:
    return round(Color(h).convert("srgb").luminance(), 6)


def de2000(a: str, b: str) -> float:
    return round(Color(a).delta_e(Color(b), method="2000"), 3)


def _neighbours(h: str) -> list[str]:
    """The hex plus every ±1 perturbation of its three channels: 27 values."""
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    out = []
    for dr, dg, db in itertools.product((-1, 0, 1), repeat=3):
        out.append("#%02X%02X%02X" % (
            min(255, max(0, r + dr)), min(255, max(0, g + dg)), min(255, max(0, b + db))
        ))
    return out


def worst_case_ratio(fg: str, bg: str) -> float:
    """The lowest contrast this pair can produce if either colour is re-quantised.

    Defends against a tool round-tripping through Display P3, a browser resolving
    an oklch() slightly differently, or an OS colour-managing the display. The
    pessimistic figure is the one this system publishes.
    """
    return round(min(ratio(f, b) for f in _neighbours(fg) for b in _neighbours(bg)), 4)


def level(r: float, kind: str, target: float) -> str:
    """Which conformance statement a measured ratio actually supports.

    The AA/AAA ladder belongs to TEXT contrast (1.4.3 and 1.4.6). WCAG defines no
    AAA level for non-text contrast at all, so a border measuring 3.9:1 has fully
    met 1.4.11 — judging it against the 4.5 text threshold and calling it a
    failure is a category error, and it was the first thing this function got
    wrong.
    """
    if kind == "nontext":
        if r < target:
            return "fail"
        return "meets 1.4.11" if target == AA_NONTEXT else "meets policy"
    if r >= AAA_TEXT:
        return "AAA"
    return "AA" if r >= AA_TEXT else "fail"


# ---------------------------------------------------------------------------
# Families
# ---------------------------------------------------------------------------

@dataclass
class Family:
    key: str
    label: str
    label_bn: str
    kind: str
    anchor: str
    note: str = ""
    max_chroma: float | None = None

    ramp: dict[int, str] = field(default_factory=dict)
    anchor_step: int | None = None
    hue: float = 0.0
    chroma_ceiling: float = 0.0

    def build(self) -> None:
        a = Color(self.anchor).convert("oklch")
        self.hue = round(float(a["hue"]) if a["hue"] is not None else 0.0, 3)
        self.chroma_ceiling = self.max_chroma if self.max_chroma is not None else float(a["chroma"])

        for s in STEPS:
            self.ramp[s] = to_hex(
                Color("oklch", [LIGHTNESS[s], self.chroma_ceiling * CHROMA_ARC[s], self.hue])
            )

        # Snap the anchor onto the ramp: the nearest step BECOMES the brand
        # colour, so ramp and brand can never drift apart. The anchor's own
        # chroma set the ceiling above, so the ramp moved to meet the anchor
        # rather than the anchor being nudged onto a ramp it does not belong to.
        anchor_hex = to_hex(a)
        self.anchor_step = min(
            STEPS, key=lambda s: Color(self.ramp[s]).distance(Color(anchor_hex), space="oklab")
        )

    def check(self) -> None:
        ls = [float(Color(self.ramp[s]).convert("oklch")["lightness"]) for s in STEPS]
        for i in range(1, len(ls)):
            if ls[i] >= ls[i - 1] - 1e-6:
                raise Fail(f"{self.key}: OKLCH lightness not monotonic at step {STEPS[i]}")

        # Contrast depends on relative luminance, not on OKLCH lightness. A ramp
        # can be monotonic in one and not the other, and only this one matters.
        lum = [luminance(self.ramp[s]) for s in STEPS]
        for i in range(1, len(lum)):
            if lum[i] >= lum[i - 1]:
                raise Fail(
                    f"{self.key}: relative luminance not monotonic at step {STEPS[i]} "
                    f"({lum[i]} is not below {lum[i-1]} at {STEPS[i-1]})"
                )

        for i in range(1, len(STEPS)):
            d = de2000(self.ramp[STEPS[i - 1]], self.ramp[STEPS[i]])
            if d < MIN_RAMP_DE:
                raise Fail(
                    f"{self.key}: steps {STEPS[i-1]} and {STEPS[i]} are only ΔE {d} apart "
                    f"(minimum {MIN_RAMP_DE}) — they will read as the same colour"
                )


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

@dataclass
class Theme:
    key: str
    label: str
    label_bn: str
    polarity: str          # light | dark
    text_target: float
    nontext_target: float
    high_contrast: bool = False


# The English labels carry the comma, because that is the wording the approved
# Bangla was joined to match — see 06_type/bangla-strings.json, theme.hc-light.
# The two high-contrast labels used to read "High contrast light" here, "High
# contrast, light" on the 30 cards and "High contrast light" again in the
# guidebook: three spellings of two names, in a system whose naming rule is one
# name for one thing.
#
# label_bn is READ from 06_type/bangla-strings.json rather than typed. It used to
# carry "উচ্চ বৈসাদৃশ্য — আলো", which is the draft the Bangla review REJECTED:
# বৈসাদৃশ্য means dissimilarity, not display contrast, and th-3 was changed to
# বেশি কনট্রাস্ট because of it. The rejected wording went on being written into
# estuary.proof.json, which is the file every downstream generator reads.
def _theme_bn(key: str, fallback: str) -> str:
    register = ROOT / "06_type" / "bangla-strings.json"
    if not register.exists():
        return fallback
    entry = json.loads(register.read_text(encoding="utf-8")).get(f"theme.{key}", {})
    return entry.get("bn") or fallback


THEMES = (
    Theme("light", "Light", _theme_bn("light", "আলো"), "light", AA_TEXT, AA_NONTEXT),
    Theme("dark", "Dark", _theme_bn("dark", "অন্ধকার"), "dark", AA_TEXT, AA_NONTEXT),
    Theme("hc-light", "High contrast, light", _theme_bn("hc-light", ""),
          "light", AAA_TEXT, HC_NONTEXT, True),
    Theme("hc-dark", "High contrast, dark", _theme_bn("hc-dark", ""),
          "dark", AAA_TEXT, HC_NONTEXT, True),
)


def build_surfaces(theme: Theme, ground: Family) -> dict[str, str]:
    """Sweep the lightness axis for seven visibly distinct surfaces.

    Walks from the dark end of the theme's permitted range upward, taking a rung
    whenever it is at least MIN_SURFACE_DE from the rung before it. If seven
    rungs cannot be found inside the range, the theme is unbuildable and says so
    — which is a real answer, not an error to work around.
    """
    tint = SURFACE_TINT[theme.key] * (ground.chroma_ceiling or 0.1)
    lo, hi = SURFACE_RANGE[theme.key]
    order = LADDER_ORDER[theme.polarity]

    # The sweep is ANCHORED at the theme's own extreme and walks inward: a light
    # theme starts at paper white and gets dimmer, a dark theme starts near black
    # and gets brighter. Walking the other way packs all seven rungs into the far
    # end of the range and produces a "light" theme whose lightest surface is
    # mid-grey — which is what the first version of this function did.
    n = len(order)
    rungs: list[str] = []
    prev: str | None = None
    total = int((hi - lo) * 2000) + 1
    for i in range(total):
        l = (hi - i / 2000.0) if theme.polarity == "light" else (lo + i / 2000.0)
        h = to_hex(Color("oklch", [l, tint, ground.hue]))
        if prev is None or de2000(prev, h) >= MIN_SURFACE_DE:
            rungs.append(h)
            prev = h
            if len(rungs) == n:
                break

    if len(rungs) < n:
        raise Fail(
            f"{theme.key}: only {len(rungs)} visibly distinct surfaces fit between "
            f"L {lo} and L {hi} at ΔE {MIN_SURFACE_DE}. This theme cannot carry a "
            f"seven-surface depth vocabulary — widen the range in SURFACE_RANGE or "
            f"accept fewer surfaces, but do not pretend."
        )

    # `order` is darkest-first; the light sweep produced lightest-first.
    if theme.polarity == "light":
        rungs.reverse()
    surfaces = dict(zip(order, rungs))

    # Distinct hexes and monotonic luminance are now guaranteed by construction,
    # so these are cheap re-derivations rather than hopes. They stay because a
    # future change to the sweep should break here, loudly.
    if len(set(surfaces.values())) != len(order):
        raise Fail(f"{theme.key}: the sweep produced duplicate surfaces")
    lums = [luminance(surfaces[r]) for r in order]
    if lums != sorted(lums):
        raise Fail(f"{theme.key}: swept surfaces are not monotonic in luminance")

    return {role: surfaces[role] for role in SURFACE_ORDER}


def pick(fam: Family, grounds: dict[str, str], target: float, polarity: str,
         what: str, kind: str = "text", prefer: str = "gentle") -> dict:
    """A ramp step that clears `target` against EVERY ground it can land on.

    `prefer="gentle"` scans from the pale end on light themes (deep end on dark)
    and returns the least-heavy colour that is still provably legible. This is
    right for almost everything: an accent picked from the safe end comes back
    near-black and the brand colour is thrown away.

    `prefer="strong"` scans from the other end and returns the most contrasting
    step. This is right for primary body text, where there is no reason to be
    gentle, and it is what leaves room for a genuinely quieter secondary text
    role beneath it.

    The published ratio is the worst measured across all grounds, under ±1 LSB
    perturbation of both colours — never the flattering one.
    """
    # On a light ground the text must be dark, so the *gentlest* legible choice is
    # the LIGHTEST step that still clears — scan 50 upward. On a dark ground the
    # text must be light, so the gentlest is the DARKEST that clears — scan 950
    # downward. Getting this the wrong way round returns step 950 for every role
    # on a light theme, which clears every target easily and throws the entire
    # palette away in exchange for near-black.
    order = STEPS if polarity == "light" else tuple(reversed(STEPS))
    if prefer == "strong":
        order = tuple(reversed(order))

    best_step, best_worst = None, -1.0
    for s in order:
        w = min(worst_case_ratio(fam.ramp[s], g) for g in grounds.values())
        if w > best_worst:
            best_step, best_worst = s, w
        if w >= target:
            measured = {name: ratio(fam.ramp[s], g) for name, g in grounds.items()}
            hardest = min(measured, key=measured.get)
            return {
                "value": fam.ramp[s],
                "family": fam.key,
                "step": s,
                "target": target,
                "measured": measured,
                "hardest_ground": hardest,
                "ratio": measured[hardest],
                "worst_case_lsb": w,
                "kind": kind,
                "level": level(w, kind, target),
                "criterion": (
                    ("WCAG 2.2 1.4.11" if target == AA_NONTEXT
                     else "policy, above WCAG 2.2 1.4.11 — WCAG defines no AAA "
                          "level for non-text contrast")
                    if kind == "nontext" else
                    ("WCAG 2.2 1.4.6" if target == AAA_TEXT else "WCAG 2.2 1.4.3")
                ),
                "rationale": (
                    f"{'lightest' if polarity == 'light' else 'darkest'} {fam.key} step "
                    f"clearing {target}:1 against all {len(grounds)} surfaces, "
                    f"hardest being {hardest}"
                ),
            }

    raise Fail(
        f"{what}: no step of '{fam.key}' reaches {target}:1 against all "
        f"{len(grounds)} surfaces. Best was step {best_step} at {best_worst}:1. "
        f"This direction's palette cannot support this role — change the anchor "
        f"in the direction spec, not this script."
    )


def pick_fill(fam: Family, label: str, target: float, polarity: str,
              what: str, rest_step: int) -> dict:
    """A ramp step to paint BEHIND text, measured against that text.

    `pick` answers a different question: which step of this family is legible
    when it is the ink sitting ON the seven surfaces. A button fill inverts the
    relationship — the role is the ground and one specific colour is the ink —
    so the seven surfaces are irrelevant to it and `surface.lowest`, the label,
    is the only thing it must clear.

    Round 3 of the review found the consequence of not having this function.
    `.as-btn--primary:hover` was painted with `accent-edge`, a role proven at
    3:1 as a LINE, and the white label on it measured 4.3549:1 in light and
    4.4808:1 in dark. Both harnesses read resting states only, so nothing saw
    it. The role was legitimately proven; it was proven for the wrong job.

    The step is taken one rung FURTHER FROM THE LABEL than the resting fill, so
    hovering always deepens the contrast rather than eroding it — the specific
    error being fixed was a hover that moved the fill towards the label's own
    lightness. It must also stay visibly different from the resting fill, or the
    state change is invisible; ΔE2000 against `rest_step` is checked, not assumed.
    """
    # Away from the label. `surface.lowest` is near-white on a light theme, so
    # further means darker: scan up the steps. On a dark theme it is near-black,
    # so further means lighter: scan down. Getting this backwards is exactly the
    # fault under repair, so it is derived from the label's own luminance rather
    # than from `polarity` — one fewer thing that can be passed in wrongly.
    away = STEPS if luminance(label) > 0.5 else tuple(reversed(STEPS))
    if polarity != ("light" if luminance(label) > 0.5 else "dark"):
        raise Fail(
            f"{what}: the label colour {label} is not the polarity's extreme. "
            f"A fill role is measured against the label it carries, and this "
            f"label does not look like one this theme would use."
        )

    rest = fam.ramp[rest_step]
    started = False
    best_step, best_worst, best_de = None, -1.0, 0.0
    for s in away:
        if s == rest_step:
            started = True
            continue
        if not started:
            continue
        w = worst_case_ratio(label, fam.ramp[s])
        d = de2000(fam.ramp[s], rest)
        if w > best_worst:
            best_step, best_worst, best_de = s, w, d
        if w >= target and d >= MIN_RAMP_DE:
            return {
                "value": fam.ramp[s],
                "family": fam.key,
                "step": s,
                "target": target,
                "measured": {"label (surface.lowest)": ratio(label, fam.ramp[s])},
                "hardest_ground": "label (surface.lowest)",
                "ratio": ratio(label, fam.ramp[s]),
                "worst_case_lsb": w,
                "kind": "fill",
                "level": level(w, "text", target),
                "criterion": (
                    "WCAG 2.2 1.4.6" if target == AAA_TEXT else "WCAG 2.2 1.4.3"
                ),
                "carries": "surface.lowest",
                "rest_step": rest_step,
                "de_from_rest": d,
                "rationale": (
                    f"nearest {fam.key} step beyond {rest_step}, away from the "
                    f"label {label}, clearing {target}:1 as a ground under that "
                    f"label and staying ΔE {d:.2f} from the resting fill"
                ),
            }

    raise Fail(
        f"{what}: no step of '{fam.key}' beyond {rest_step} both clears "
        f"{target}:1 under the label {label} and stays ΔE {MIN_RAMP_DE} from "
        f"the resting fill. Best was step {best_step} at {best_worst}:1, "
        f"ΔE {best_de:.2f}. A hovered fill that fails this must not ship: the "
        f"label on it becomes unreadable in the one state a pointer user sees "
        f"most. Widen the accent ramp or drop the hover fill change."
    )


def build_theme(theme: Theme, fams: dict[str, Family]) -> dict:
    ground = fams["ground"]
    surfaces = build_surfaces(theme, ground)

    roles: dict[str, dict] = {}

    def add(name: str, fam_key: str, target: float, kind: str = "text",
            prefer: str = "gentle") -> None:
        roles[name] = pick(fams[fam_key], surfaces, target, theme.polarity,
                           f"{theme.key}/{name}", kind, prefer)

    # Primary text takes the strongest step available — there is no reason for
    # body copy to be gentle, and taking the strongest is what leaves room for a
    # genuinely quieter secondary role beneath it.
    add("ink", "ground", theme.text_target, prefer="strong")
    add("ink-muted", "ground", theme.text_target)
    add("line", "ground", theme.nontext_target, kind="nontext")
    add("accent", "accent", theme.text_target)
    add("accent-edge", "accent", theme.nontext_target, kind="nontext")
    add("focus", "accent", theme.nontext_target, kind="nontext")

    # A ground that carries text, so it is measured against the text and not
    # against the surfaces. See pick_fill for why this is a separate function
    # and which shipped defect it repairs.
    roles["accent-hover"] = pick_fill(
        fams["accent"], surfaces["lowest"], theme.text_target, theme.polarity,
        f"{theme.key}/accent-hover", roles["accent"]["step"],
    )
    for sem in ("success", "warning", "danger", "info"):
        if sem in fams:
            add(sem, sem, theme.text_target)

    # Two names for one colour is a lie about the system's depth. If the theme's
    # target leaves no room for a quieter text role, say so rather than ship it.
    if roles["ink-muted"]["value"] == roles["ink"]["value"]:
        raise Fail(
            f"{theme.key}: ink and ink-muted resolve to the same colour "
            f"({roles['ink']['value']}, step {roles['ink']['step']}) at "
            f"{theme.text_target}:1. Every step gentler than the strongest one fails "
            f"the target, so this theme has no room for a secondary text role."
        )

    return {
        "key": theme.key,
        "label": theme.label,
        "label_bn": theme.label_bn,
        "polarity": theme.polarity,
        "high_contrast": theme.high_contrast,
        "text_target": theme.text_target,
        "nontext_target": theme.nontext_target,
        "surfaces": surfaces,
        "surface_luminance": {k: luminance(v) for k, v in surfaces.items()},
        "roles": roles,
    }


# ---------------------------------------------------------------------------
# Driving one direction
# ---------------------------------------------------------------------------

def run(spec_path: Path) -> dict:
    try:
        spec = json.loads(spec_path.read_text())
    except json.JSONDecodeError as e:
        raise NotEquipped(f"{spec_path.name} is not valid JSON: {e}") from e

    for req in ("key", "name", "premise", "families"):
        if req not in spec:
            raise NotEquipped(f"{spec_path.name} is missing '{req}'")

    fams: dict[str, Family] = {}
    for key, f in spec["families"].items():
        fam = Family(key=key, label=f["label"], label_bn=f.get("label_bn", ""),
                     kind=f["kind"], anchor=f["anchor"], note=f.get("note", ""),
                     max_chroma=f.get("max_chroma"))
        fam.build()
        fam.check()
        fams[key] = fam

    for required in ("ground", "accent"):
        if required not in fams:
            raise NotEquipped(f"{spec['key']}: a direction must define a '{required}' family")

    themes = [build_theme(t, fams) for t in THEMES]

    return {
        "key": spec["key"],
        "name": spec["name"],
        "name_bn": spec.get("name_bn", ""),
        "premise": spec["premise"],
        "generated_by": "05_colour/engine.py",
        "warning": "Generated file. Do not hand-edit — change the direction spec and re-run.",
        "measurement": {
            "library": "coloraide", "contrast_method": "wcag21",
            "delta_e_method": "2000", "ramp_space": "oklch",
            "gamut_map": "oklch-chroma",
            "note": ("Every ratio is measured on the rounded 8-bit hex, then re-measured "
                     "with each channel of both colours nudged by ±1. The published "
                     "worst_case_lsb is the lowest of those results."),
        },
        "steps": list(STEPS),
        "families": {
            k: {"label": f.label, "label_bn": f.label_bn, "kind": f.kind, "note": f.note,
                "hue_oklch": f.hue, "chroma_ceiling": round(f.chroma_ceiling, 5),
                "anchor": to_hex(Color(f.anchor)), "anchor_step": f.anchor_step,
                "ramp": {str(s): f.ramp[s] for s in STEPS},
                "ramp_luminance": {str(s): luminance(f.ramp[s]) for s in STEPS}}
            for k, f in fams.items()
        },
        "themes": {t["key"]: t for t in themes},
    }


def summarise(r: dict) -> str:
    out = [f"{r['name']}  ({r['key']})"]
    for tk, t in r["themes"].items():
        txt = [v for v in t["roles"].values() if v["kind"] == "text"]
        non = [v for v in t["roles"].values() if v["kind"] == "nontext"]
        out.append(
            f"    {tk:<9}  text {t['text_target']}:1 -> worst "
            f"{min(v['worst_case_lsb'] for v in txt):>7}:1 "
            f"({'/'.join(sorted({v['level'] for v in txt}))})   "
            f"non-text {t['nontext_target']}:1 -> worst "
            f"{min(v['worst_case_lsb'] for v in non):>6}:1"
        )
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate and prove every Aninda Studio palette.")
    ap.add_argument("--only", help="one direction key")
    ap.add_argument("--check", action="store_true", help="verify without writing")
    args = ap.parse_args()

    specs = sorted(SPEC_DIR.glob("*.json"))
    if args.only:
        specs = [p for p in specs if p.stem == args.only]
    if not specs:
        print(f"No direction specs in {SPEC_DIR}", file=sys.stderr)
        return 2

    results, failures, not_equipped = {}, [], []
    for p in specs:
        try:
            results[p.stem] = run(p)
        except NotEquipped as e:
            not_equipped.append(str(e))
        except Fail as e:
            failures.append(f"{p.stem}: {e}")

    if not_equipped:
        print("COULD NOT RUN — nothing written:\n", file=sys.stderr)
        for n in not_equipped:
            print(f"  - {n}", file=sys.stderr)
        return 2

    if failures:
        print("FAILED — nothing written, for any direction:\n", file=sys.stderr)
        for f in failures:
            print(f"  - {f}\n", file=sys.stderr)
        return 1

    for r in results.values():
        print(summarise(r))

    if args.check:
        print(f"\n--check: {len(results)} direction(s) verified. Nothing written.")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for key, r in results.items():
        (OUT_DIR / f"{key}.proof.json").write_text(json.dumps(r, indent=2, sort_keys=False) + "\n")
    print(f"\nWrote {len(results)} proof file(s) to {OUT_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
