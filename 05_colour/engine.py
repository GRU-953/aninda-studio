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
    cd <the repository folder>
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
    # The dark ranges START AT ZERO so their dimmest rung is pure black, which is
    # what makes the Natural direction's two anchors literal on both sides: pure
    # white is the light theme's brightest surface and pure black is the dark
    # theme's dimmest. The range was 0.128 to 0.345 when the ground was a tinted
    # green and there was no reason to reach the floor.
    "light": (0.855, 1.000),
    "dark": (0.000, 0.345),
    # High contrast widens the ladder rather than compressing it. Compressing was
    # the obvious first instinct — squeeze every surface toward the extreme so
    # 7:1 is easy — but it makes the surfaces themselves indistinguishable, and
    # someone who has turned high contrast on is the last person who should be
    # asked to tell two near-identical greys apart.
    "hc-light": (0.840, 1.000),
    "hc-dark": (0.000, 0.330),
}

# Rungs from darkest to lightest, per theme polarity. In a light theme the
# container ladder runs lightest-to-darkest as it does in Material, so ascending
# lightness reads dim, highest, high, base, low, lowest, bright.
LADDER_ORDER: dict[str, tuple[str, ...]] = {
    "light": ("dim", "highest", "high", "base", "low", "lowest", "bright"),
    "dark": ("dim", "lowest", "low", "base", "high", "highest", "bright"),
}

SURFACE_ORDER = ("lowest", "low", "base", "high", "highest", "dim", "bright",
                 "page")

# `page` is the eighth, and it is DERIVED rather than swept. The other seven come
# out of the lightness sweep and hold their relative brightness across themes, which
# is what makes `bright` the brightest surface in BOTH the light and the dark theme.
# That is Material's own bright/dim semantics and it is deliberate.
#
# It also means no swept surface inverts to the theme's own extreme, and the Natural
# direction needs exactly that: a page that is pure white in the light theme and pure
# black in the dark one. `page` is that surface. It aliases the polarity's extreme —
# `bright` in a light theme, `dim` in a dark one — so it is never a new colour, only
# a name for which end of the ladder the reader is looking at.
PAGE_ALIAS = {"light": "bright", "dark": "dim"}

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

        # Snap the anchor onto the ramp: the nearest step BECOMES the brand colour,
        # so ramp and brand can never drift apart.
        #
        # That sentence was here from the start and the code did not do it. The
        # anchor set the ramp's HUE and its chroma ceiling, but every step's
        # lightness comes from the fixed LIGHTNESS table above, so the anchor almost
        # never landed on a step. Measured on the Natural direction, whose four
        # colours were supplied by name and by Pantone reference: the nearest step
        # to Natural Green #2C5A3A was #2D4C36, deltaE 5.67 — a visibly different
        # green. The brand colour was not in the palette that claimed to be built
        # from it.
        #
        # The nearest step is now literally overwritten with the anchor. check()
        # re-runs monotonic luminance and the minimum spacing afterwards, so a
        # substitution that breaks the ramp fails the build rather than bending it.
        anchor_hex = to_hex(a)
        self.anchor_step = min(
            STEPS, key=lambda s: Color(self.ramp[s]).distance(Color(anchor_hex), space="oklab")
        )
        self.ramp[self.anchor_step] = anchor_hex

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
    # Over the SWEPT rungs only. `page` is added after this and is an alias of one
    # of them by construction, so including it here would fail every build.
    if len(set(surfaces.values())) != len(order):
        raise Fail(f"{theme.key}: the sweep produced duplicate surfaces")
    lums = [luminance(surfaces[r]) for r in order]
    if lums != sorted(lums):
        raise Fail(f"{theme.key}: swept surfaces are not monotonic in luminance")

    surfaces["page"] = surfaces[PAGE_ALIAS[theme.polarity]]
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

    `prefer="anchor"` returns the family's ANCHOR STEP — the brand colour itself —
    whenever it clears the target on every ground, and falls back to "gentle" when
    it does not. This exists because the gentle scan stops at the first step that
    clears, which on a light theme is usually one step lighter than the anchor: the
    Natural direction's accent came out #426271 while its brand colour, Natural
    Blue, is #224959 and clears 9.70:1 on white with room to spare. A palette that
    names four colours and then ships neighbours of them is not shipping them.

    The fallback is the honest half. On a dark theme a dark brand colour cannot
    carry text on a dark surface, so the role takes a lighter step of the SAME
    family and the proof says which step it took.

    The published ratio is the worst measured across all grounds, under ±1 LSB
    perturbation of both colours — never the flattering one.
    """
    if prefer == "anchor" and fam.anchor_step is not None:
        cand = fam.ramp[fam.anchor_step]
        worst = min(worst_case_ratio(cand, g) for g in grounds.values())
        if worst >= target:
            m = {n: ratio(cand, g) for n, g in grounds.items()}
            hardest = min(m, key=m.get)
            return {
                "value": cand, "family": fam.key, "step": fam.anchor_step,
                "target": target, "measured": m, "hardest_ground": hardest,
                "ratio": m[hardest], "worst_case_lsb": worst, "kind": kind,
                "level": level(worst, kind, target),
                "criterion": ("WCAG 2.2 1.4.11" if kind == "nontext"
                              else "WCAG 2.2 1.4.6" if target == AAA_TEXT
                              else "WCAG 2.2 1.4.3"),
                "rationale": (f"the {fam.key} family's anchor step "
                              f"{fam.anchor_step} — the brand colour itself, which "
                              f"clears {target}:1 on every ground it can land on"),
                "is_brand_anchor": True,
            }
        prefer = "gentle"
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


def pick_on_fill(label: str, grounds: dict[str, str], target: float,
                 what: str) -> dict:
    """The colour that sits ON a fill, named at last, and proven on every fill.

    This role already existed and had no name. components.css paints
    .as-btn--primary and .as-btn--danger with `color: var(--as-surface-lowest)`,
    and 08_components/check.py measures those composited pairs in a real browser —
    so the relationship was proven while nothing in the token set expressed it.

    Two things went wrong for want of a name. The Figma plugin draws OUTLINED
    rather than filled buttons, and its own receipt records the reason: "no 'on
    accent' text colour is defined". And Material 3 cannot construct a ColorScheme
    at all without onPrimary — its primary constructor has no defaults, so a
    missing role silently ships Material's baseline purple.

    No new colour is invented here. The value IS surface.lowest. What is new is
    that it is measured against EVERY fill that carries it rather than one, and
    the published figure is the worst of those.
    """
    measured = {name: ratio(label, g) for name, g in grounds.items()}
    worst_name = min(measured, key=measured.get)
    worst = min(worst_case_ratio(label, g) for g in grounds.values())
    if worst < target:
        raise Fail(
            f"{what}: {label} measures {worst:.4f}:1 on '{worst_name}' against a "
            f"target of {target}:1. This is the colour every filled control puts on "
            f"top of itself, so a fill it cannot clear is a fill that must not carry "
            f"a label."
        )
    return {
        "value": label,
        "family": "surface",
        "step": "lowest",
        "target": target,
        "measured": measured,
        "hardest_ground": worst_name,
        "ratio": measured[worst_name],
        "worst_case_lsb": worst,
        # "on-fill", not "text". A text role is measured against the seven
        # surfaces; this one is measured against the fills it lands on, and calling
        # it text would put it in a matrix whose seven columns it does not have.
        # The contrast standard applied to it is still the text one — it is ink.
        "kind": "on-fill",
        "level": level(worst, "text", target),
        "criterion": "WCAG 2.2 1.4.6" if target == AAA_TEXT else "WCAG 2.2 1.4.3",
        "carries": ", ".join(sorted(grounds)),
        "rationale": (
            f"surface.lowest, measured as ink against every fill that carries it "
            f"({', '.join(sorted(grounds))}); the published figure is the worst of "
            f"them, which is '{worst_name}'"
        ),
    }


def build_theme(theme: Theme, fams: dict[str, Family],
                fixed: dict | None = None,
                role_sources: dict | None = None,
                declared_duplicates: list | None = None) -> dict:
    ground = fams["ground"]
    surfaces = build_surfaces(theme, ground)

    roles: dict[str, dict] = {}

    def add(name: str, fam_key: str, target: float, kind: str = "text",
            prefer: str = "gentle") -> None:
        roles[name] = pick(fams[fam_key], surfaces, target, theme.polarity,
                           f"{theme.key}/{name}", kind, prefer)

    # Primary text. A direction may FIX it rather than take it from the ground
    # ramp, and the Natural direction does: pure black on a white page and pure
    # white on a black one. That is 21:1, which no ramp step can beat, and it is
    # the reason those two colours are named in the palette at all.
    #
    # A fixed ink is still measured against all seven surfaces, like every other
    # role. Being chosen by hand does not exempt it from the proof.
    fixed_ink = None
    if fixed:
        fixed_ink = fixed.get("ink_light" if theme.polarity == "light" else "ink_dark")
    if fixed_ink:
        measured = {n: ratio(fixed_ink, g) for n, g in surfaces.items()}
        hardest = min(measured, key=measured.get)
        worst = min(worst_case_ratio(fixed_ink, g) for g in surfaces.values())
        if worst < theme.text_target:
            raise Fail(
                f"{theme.key}/ink: the fixed ink {fixed_ink} measures {worst:.4f}:1 "
                f"on surface {hardest!r}, under the {theme.text_target}:1 target. A "
                f"direction that fixes its ink still has to prove it.")
        roles["ink"] = {
            "value": fixed_ink, "family": "fixed", "step": "ink",
            "target": theme.text_target, "measured": measured,
            "hardest_ground": hardest, "ratio": measured[hardest],
            "worst_case_lsb": worst, "kind": "text",
            "level": level(worst, "text", theme.text_target),
            "criterion": ("WCAG 2.2 1.4.6" if theme.text_target == AAA_TEXT
                          else "WCAG 2.2 1.4.3"),
            "rationale": ("a fixed anchor of this direction rather than a ramp step, "
                          "measured against every surface it can land on"),
        }
    else:
        # There is no reason for body copy to be gentle, and taking the strongest
        # is what leaves room for a genuinely quieter secondary role beneath it.
        add("ink", "ground", theme.text_target, prefer="strong")
    add("ink-muted", "ground", theme.text_target)
    add("line", "ground", theme.nontext_target, kind="nontext", prefer="anchor")
    add("accent", "accent", theme.text_target, prefer="anchor")
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
            add(sem, sem, theme.text_target, prefer="anchor")

    # A direction with fewer families than roles has to say where the missing ones
    # come from, and it says so in ITS OWN SPEC rather than here.
    #
    # Two modes, and the difference between them is the point.
    #
    #   "beyond"   the first step past a named sibling that still clears the target
    #              and is visibly apart from it. NOT the extreme. The first version
    #              of this used prefer="strong" and produced a light-theme warning
    #              of #181716 — the grey ramp's darkest step, which reads as black.
    #              A warning colour that looks like body text is not a warning.
    #
    #   "same-as"  deliberately the same colour as another role, with a reason
    #              recorded. Information IS the accent in the Natural direction:
    #              Natural Blue carries links, focus, the primary action and
    #              information. Saying that plainly is honest; deriving a
    #              near-identical second blue to avoid saying it is not.
    for role_name, spec_row in (role_sources or {}).items():
        if role_name in roles:
            continue
        mode = spec_row.get("mode")
        if mode == "same-as":
            sibling = roles[spec_row["same_as"]]
            roles[role_name] = dict(sibling)
            roles[role_name]["rationale"] = (
                f"the same colour as {spec_row['same_as']!r} by declaration — "
                f"{spec_row.get('why', 'no reason given')}")
            roles[role_name]["declared_same_as"] = spec_row["same_as"]
        elif mode == "beyond":
            fam = fams[spec_row["family"]]
            sib = roles[spec_row["beyond"]]
            order = STEPS if theme.polarity == "light" else tuple(reversed(STEPS))
            started, chosen = False, None
            for st in order:
                if st == sib["step"]:
                    started = True
                    continue
                if not started:
                    continue
                cand = fam.ramp[st]
                w = min(worst_case_ratio(cand, g) for g in surfaces.values())
                if w >= theme.text_target and de2000(cand, sib["value"]) >= MIN_RAMP_DE:
                    chosen = st
                    break
            if chosen is None:
                raise Fail(
                    f"{theme.key}/{role_name}: no step of {spec_row['family']!r} "
                    f"beyond {spec_row['beyond']!r} clears {theme.text_target}:1 on "
                    f"every surface and stays visibly apart from it. A doubled role "
                    f"that cannot be told from its sibling must not ship.")
            m = {n: ratio(fam.ramp[chosen], g) for n, g in surfaces.items()}
            hardest = min(m, key=m.get)
            worst = min(worst_case_ratio(fam.ramp[chosen], g)
                        for g in surfaces.values())
            roles[role_name] = {
                "value": fam.ramp[chosen], "family": fam.key, "step": chosen,
                "target": theme.text_target, "measured": m,
                "hardest_ground": hardest, "ratio": m[hardest],
                "worst_case_lsb": worst, "kind": "text",
                "level": level(worst, "text", theme.text_target),
                "criterion": ("WCAG 2.2 1.4.6" if theme.text_target == AAA_TEXT
                              else "WCAG 2.2 1.4.3"),
                "rationale": (f"the first {fam.key} step beyond "
                              f"{spec_row['beyond']!r} that clears "
                              f"{theme.text_target}:1 on every surface and stays at "
                              f"least deltaE {MIN_RAMP_DE} from it"),
                "declared_beyond": spec_row["beyond"],
            }
        else:
            raise Fail(f"{theme.key}/{role_name}: role source mode {mode!r} is not "
                       f"one this engine knows.")

    # The colour every filled control puts on top of itself. It is measured against
    # each fill that actually carries it, read from components.css: the primary
    # button uses accent and its hover uses accent-hover, and the danger button uses
    # danger. Adding a fill without adding it here would leave that fill's label
    # unproven, which is the defect pick_fill was written to repair.
    roles["on-accent"] = pick_on_fill(
        surfaces["lowest"],
        {"accent": roles["accent"]["value"],
         "accent-hover": roles["accent-hover"]["value"],
         "danger": roles["danger"]["value"]},
        theme.text_target, f"{theme.key}/on-accent")

    # Two names for one colour is a lie about the system's depth. If the theme's
    # target leaves no room for a quieter text role, say so rather than ship it.
    # Roles drawn from one family must not resolve to one colour. Two names for
    # one colour is a lie about the system's depth, and a four-hue palette invites
    # exactly that.
    for a, b, why in (
        ("warning", "ink-muted",
         "warning is the ground family's strong step and ink-muted its gentle one; "
         "landing together would leave the palette unable to say caution in a "
         "colour distinct from quiet text"),
        ("warning", "ink", "warning must not be the body text colour"),
    ):
        # A DECLARED duplicate is allowed; an accidental one is not. That is the
        # whole distinction: the direction spec has to name the role it is copying
        # and say why, and then the pair is recorded rather than refused.
        if a in roles and b in roles and roles[a]["value"] == roles[b]["value"] \
                and roles[a].get("declared_same_as") != b:
            raise Fail(f"{theme.key}: {a!r} and {b!r} both resolve to "
                       f"{roles[a]['value']} — {why}.")

    # Any two roles resolving to one colour must be DECLARED in the direction spec.
    #
    # A four-hue palette makes collisions inevitable rather than exceptional, and
    # the choice is between engineering them away — which means deriving colours
    # nobody chose — and naming them. The Natural direction names them. What is
    # refused is a collision nobody noticed.
    # Structural duplicates: pairs this ENGINE makes identical by construction, in
    # every direction. They are declared here rather than in each direction spec,
    # because they are a property of the code and not of a palette.
    STRUCTURAL = {
        frozenset(("accent-edge", "focus")):
            "The focus ring is drawn in the accent's edge colour. Both are the "
            "accent family measured at the non-text target, with the same "
            "preference, so they are one colour by definition rather than by "
            "coincidence. Every direction in this repository has shipped them "
            "identical since the first build; nothing said so until 26 August 2026.",
    }
    declared = dict(STRUCTURAL)
    declared.update({frozenset(pair["roles"]): pair.get("why", "")
                     for pair in (declared_duplicates or [])})
    seen: dict[str, str] = {}
    for name, r in roles.items():
        v = r["value"]
        if v in seen:
            pair = frozenset((seen[v], name))
            if r.get("declared_same_as") == seen[v] or \
                    roles[seen[v]].get("declared_same_as") == name:
                continue
            if pair not in declared:
                raise Fail(
                    f"{theme.key}: {sorted(pair)} both resolve to {v}, and that pair "
                    f"is not declared in the direction spec. Two names for one "
                    f"colour is a claim about the palette's depth and has to be made "
                    f"on purpose, with a reason.")
        else:
            seen[v] = name

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

    themes = [build_theme(t, fams, spec.get("fixed"), spec.get("role_sources"),
                          spec.get("declared_duplicates"))
              for t in THEMES]

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
        "fixed": spec.get("fixed", {}),
        "role_sources": spec.get("role_sources", {}),
        "declared_duplicates": spec.get("declared_duplicates", []),
        "supersedes": spec.get("supersedes", {}),
        "pantone": spec.get("pantone", {}),
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
