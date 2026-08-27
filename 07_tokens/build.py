#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
This is the single writer of the Aninda Studio design tokens. Everything that
carries a colour, a size, a duration or a typeface downstream — the stylesheets,
the Figma library, the component cards, the guidebook, the npm and PyPI packages
— is generated from what this script emits. Nothing hand-edits its output.

The colour values are not decided here. They are read from
05_colour/generated/estuary.proof.json, which measured them. This script's job is
to express them in a standard other tools can read, and to carry the proof along
with them so a downstream reader can check the claim rather than trust it.

THE STANDARD, STATED PRECISELY
------------------------------
Design Tokens Format Module **2025.10**, a Final Community Group Report of the
W3C Design Tokens Community Group, dated 28 October 2025. It is published under
the W3C Community Final Specification Agreement and is **not a W3C Standard and
not on the W3C Standards Track**. Calling it "a W3C standard" is wrong and this
system does not.

Three things about 2025.10 that catch people out, all handled here:
  * a colour `$value` is an OBJECT — {colorSpace, components, hex} — not a string;
  * `dimension` and `duration` are objects with a mandatory unit, even at zero;
  * there is no theming or mode concept in the specification at all.

HOW THEMES ARE MODELLED, AND WHY
--------------------------------
One file per theme, with identical token paths in each.

The tempting alternative is a single file carrying all four themes inside
`$extensions`. It is rejected because the specification permits any tool to
IGNORE `$extensions` — and a tool that ignores it does not error, it silently
renders one theme's values for all four. Silent wrong output is the exact failure
class this whole system exists to prevent. One file per theme is also what IBM
Carbon does, and Carbon is the only flagship system verified shipping conformant
DTCG.

WHAT CANNOT BE MODELLED IN DTCG AT ALL
--------------------------------------
`forced-colors` mode. Its values are CSS system colour keywords — Canvas,
CanvasText, ButtonFace — which are not colours in the DTCG sense: they have no
colour space, no components and no hex, because the operating system supplies
them. DTCG's thirteen types include nothing that fits. So the forced-colors map
lives in its own file, outside the DTCG tree, explicitly marked as not DTCG,
rather than being bent into a shape the specification does not have.

RUN
---
    cd <the repository folder>
    ./.venv/bin/python 07_tokens/build.py
    ./.venv/bin/python 07_tokens/build.py --check    # verify, write nothing
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "build"

# The chosen direction, named ONCE. PROOF is derived from it rather than written
# out beside it: the two were separate constants, and switching the direction to
# "natural" left PROOF still reading estuary.proof.json — so the build reported a
# new direction and emitted the old palette, silently and with no gate able to see
# it. One name, one source.
DIRECTION = "natural"
PROOF = ROOT / "05_colour" / "generated" / f"{DIRECTION}.proof.json"
SCHEMA = "https://tr.designtokens.org/format/"
NS = "studio.aninda"

# The thirteen types DTCG 2025.10 defines, and the units each measured type
# permits. Written out rather than inferred, because a typed vocabulary is the
# only thing that lets check() tell a dimension from a number and so notice a
# missing unit. The docstring above has claimed "thirteen types" since the file
# was written; this is the list, so the claim is now checkable.
DTCG_TYPES = frozenset({
    "color", "dimension", "fontFamily", "fontWeight", "duration", "cubicBezier",
    "number", "strokeStyle", "border", "transition", "shadow", "gradient",
    "typography",
})
DTCG_UNITS = {"dimension": frozenset({"px", "rem"}), "duration": frozenset({"ms", "s"})}

THEMES = ("light", "dark", "hc-light", "hc-dark")

# --- Specified constants. A person chose these. Everything else is measured. ---

SCALE_RATIO = 1.333            # a perfect fourth
BASE_PX = 16                   # the anchor, and the floor for running prose
SPACE_PX = (4, 8, 12, 16, 24, 32, 48, 64, 96, 128)
RADIUS_PX = {"badge": 4, "control": 8, "card": 14, "hero": 24}

# The three platform floors are different numbers and the system states all
# three rather than picking one and implying it is universal.
# Each description carries the source and the date it was read. These four figures
# were the clearest example of the fault acceptance criterion 28 found: a number
# attributed to an outside body with neither a URL nor a date, in a token document
# that a stranger consumes. A figure like that cannot be re-checked, which is the
# whole reason to cite one.
TARGET_PX = {
    "min": (24, "WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA — "
                "w3.org/TR/WCAG22/#target-size-minimum, Recommendation "
                "12 December 2024, read 14 August 2026"),
    "apple-min": (28, "Apple HIG minimum control size, iOS and iPadOS — "
                      "developer.apple.com/design/human-interface-guidelines/"
                      "accessibility, read 14 August 2026"),
    "comfortable": (44, "Apple HIG default control size, iOS and iPadOS — "
                        "developer.apple.com/design/human-interface-guidelines/"
                        "accessibility, read 14 August 2026"),
    "android-min": (48, "Android accessibility guidance minimum touch target, in dp "
                        "— developer.android.com accessibility pages, "
                        "read 14 August 2026"),
}

# WCAG 2.4.13 Focus Appearance is Level AAA, not AA. AA requires only 2.4.11,
# that focus is not ENTIRELY obscured. This system adopts the AAA geometry by
# choice and labels it honestly.
FOCUS_PX = {"ring-width": 3, "ring-offset": 2}

TYPE_STEPS = (
    ("caption", -1), ("body", 0), ("lead", 1), ("h3", 2),
    ("h2", 3), ("h1", 4), ("display", 5),
)

# 120ms for a colour changing in place, 220ms for something arriving or leaving.
# Nothing over 300ms. Deliberately simpler than Material's spring system, and the
# reason is a choice rather than an omission: springs are excellent on a platform
# that owns its frame budget, and this system targets low-end Android where a
# 220ms ease-out costs nothing.
DURATION_MS = {"colour": 120, "move": 220}
EASING = {
    "standard": [0.2, 0.0, 0.0, 1.0],
    "enter": [0.05, 0.7, 0.1, 1.0],
    "exit": [0.3, 0.0, 0.8, 0.15],
}

# Material's own split, adopted as a principle even though its spring system is
# not: things that MOVE may overshoot; things that merely change colour or
# opacity never do.
MOTION_NOTE = ("Things that move may overshoot; things that only change colour "
               "or opacity never do.")

FONTS = {
    "latin": {"family": ["Literata", "Georgia", "serif"],
              "licence": "SIL OFL 1.1", "rfn": None,
              "note": "Literata, by Veronika Burian and José Scaglione (TypeTogether). "
                      "An optical-size axis from 7 to 72, so the letterforms are "
                      "redrawn for the size rather than merely scaled. Its x-height "
                      "is almost flat across that range (0.5166 to 0.5130 em)."},
    "mono": {"family": ["Aninda Mono", "IBM Plex Mono", "ui-monospace", "monospace"],
             "licence": "SIL OFL 1.1", "rfn": "Plex",  # the exact string in its own OFL, NOT "IBM Plex"
             "note": "IBM Plex Mono, by Mike Abbink and Bold Monday. It carries the "
                     "Reserved Font Name 'Plex', and subsetting a font counts as "
                     "modifying it under OFL 1.1 clause 3 — so the subset shipped "
                     "here is renamed 'Aninda Mono'. The unmodified family name is "
                     "kept as the next fallback, so anyone who already has IBM Plex "
                     "Mono installed gets the real thing."},
}

# THE THREE BANGLA CONSTANTS THAT WERE HERE
#
# A per-size multiplier (0.815 to 0.825), a 12 px floor and a weight step below
# 14 px. They were the only size-dependent compensation rules this system had, and
# they left with the script they were measured for on 27 August 2026.
#
# The derivation is NOT deleted. It was the strongest measurement in this
# repository — the luminance the মাত্রা actually rendered at, read at
# device_scale_factor 1, where 12 px at weight 400 came out at 123 on white and
# read as grey rather than ink — and it now sits in the guidebook's chapter on what
# this system does not do, reading 06_type/_data/measurements.json rather than
# these constants. A record that depended on the tokens would have died with them.


def colour(hexv: str) -> dict:
    """A DTCG 2025.10 colour value.

    The components are derived FROM the hex rather than alongside it, so the two
    representations cannot disagree — a verifier can re-derive the bytes and
    assert equality.
    """
    h = hexv.lstrip("#")
    comps = [round(int(h[i:i + 2], 16) / 255, 6) for i in (0, 2, 4)]
    return {"colorSpace": "srgb", "components": comps, "hex": f"#{h.upper()}"}


def dim(value: float, unit: str = "px") -> dict:
    """A DTCG dimension. The unit is mandatory even when the value is zero."""
    return {"value": value, "unit": unit}


def ms(value: int) -> dict:
    return {"value": value, "unit": "ms"}


def primitives(proof: dict) -> dict:
    ramps: dict = {}
    for key, fam in proof["families"].items():
        steps = {
            step: {
                "$value": colour(hexv),
                "$extensions": {NS: {
                    "step": int(step),
                    "luminance": fam["ramp_luminance"][step],
                    "isAnchor": int(step) == fam["anchor_step"],
                }},
            }
            for step, hexv in fam["ramp"].items()
        }
        steps["$description"] = f"{fam['label']} — {fam['note'] or fam['kind']}"
        steps["$extensions"] = {NS: {
            "hueOklch": fam["hue_oklch"],
            "chromaCeiling": fam["chroma_ceiling"],
            "anchor": fam["anchor"],
            "anchorStep": fam["anchor_step"],
        }}
        ramps[key] = steps

    return {
        "$schema": SCHEMA,
        "$description": (
            "Aninda Studio primitive tokens. Generated — do not hand-edit. "
            "Colour ramps are computed in OKLCH and gamut-mapped into sRGB; every "
            "value is the rounded 8-bit hex a browser will actually produce."
        ),
        "$extensions": {NS: {
            "direction": DIRECTION,
            "generatedBy": "07_tokens/build.py",
            "spec": "DTCG 2025.10 (Final Community Group Report, 28 October 2025) "
                    "— a W3C Community Group specification, NOT a W3C Standard",
        }},
        "color": {"$type": "color", "ramp": ramps},
        "dimension": {
            "$type": "dimension",
            "space": {
                str(i): {"$value": dim(px),
                         "$description": f"Step {i} of the 4px spacing scale"}
                for i, px in enumerate(SPACE_PX)
            },
            "radius": {
                k: {"$value": dim(px), "$description": f"Corner radius for a {k}"}
                for k, px in RADIUS_PX.items()
            },
            "target": {
                k: {"$value": dim(px), "$description": src,
                    "$extensions": {NS: {"source": src}}}
                for k, (px, src) in TARGET_PX.items()
            },
            "focus": {
                k: {"$value": dim(px),
                    "$description": "Focus indicator geometry. WCAG 2.2 SC 2.4.13 "
                                    "Focus Appearance is Level AAA, adopted here by "
                                    "choice; Level AA requires only SC 2.4.11."}
                for k, px in FOCUS_PX.items()
            },
            "type": {
                **{
                    name: {
                        "$value": dim(round(SCALE_RATIO ** n, 4), "rem"),
                        "$description": f"{round(BASE_PX * SCALE_RATIO ** n, 2)}px at a "
                                        f"16px root — step {n:+d} of a {SCALE_RATIO} scale",
                    }
                    for name, n in TYPE_STEPS
                },
            },
        },
        "number": {
            "$type": "number",
            "scale": {
                "ratio": {
                    "$value": SCALE_RATIO,
                    "$description": "A perfect fourth. The jumps are large on purpose: "
                                    "hierarchy is unmistakable and fewer levels are "
                                    "needed to express it.",
                },
            },
        },
        "fontFamily": {
            "$type": "fontFamily",
            **{k: {"$value": v["family"], "$description": v["note"],
                   "$extensions": {NS: {"licence": v["licence"]}}}
               for k, v in FONTS.items()},
        },
        "duration": {
            "$type": "duration",
            "motion": {k: {"$value": ms(v)} for k, v in DURATION_MS.items()},
        },
        "cubicBezier": {
            "$type": "cubicBezier",
            "motion": {k: {"$value": v, "$description": MOTION_NOTE}
                       for k, v in EASING.items()},
        },
    }


def semantic(proof: dict, theme_key: str) -> dict:
    t = proof["themes"][theme_key]
    fams = proof["families"]

    def step_of(hexv: str, fam_key: str) -> str | None:
        # A role whose family is not one of the six ramps has no primitive to alias.
        # `on-accent` is the case: its value is a tonal SURFACE, which is computed
        # per theme rather than taken from a ramp. Returning None here is the right
        # answer and not a fallback — it makes the token a literal carrying its
        # derivation, which is exactly what the aliasing rule asks for. Without this
        # the lookup raised KeyError: 'surface'.
        if fam_key not in fams:
            return None
        for step, h in fams[fam_key]["ramp"].items():
            if h == hexv:
                return step
        return None

    surfaces = {}
    for name, hexv in t["surfaces"].items():
        surfaces[name] = {
            "$value": colour(hexv),
            "$description": f"Tonal surface '{name}' for the {t['label']} theme",
            "$extensions": {NS: {
                "luminance": t["surface_luminance"][name],
                "derivation": "swept along the lightness axis until each rung was at "
                              "least ΔE2000 0.9 from the one before it",
            }},
        }

    def role(name: str) -> dict:
        r = t["roles"][name]
        s = step_of(r["value"], r["family"])
        node: dict = {
            "$description": r["rationale"],
            "$extensions": {NS: {
                "family": r["family"],
                "step": r["step"],
                "kind": r["kind"],
                "proof": {
                    "required": r["target"],
                    "measured": r["ratio"],
                    "worstCaseLsb": r["worst_case_lsb"],
                    "hardestGround": r["hardest_ground"],
                    "level": r["level"],
                    "criterion": r["criterion"],
                    "againstEverySurface": r["measured"],
                },
            }},
        }
        # A semantic token is an alias if and only if its value is bit-identical
        # to a primitive. Anything else is a literal carrying its derivation, so
        # the graph never lies about where a value came from.
        if s is not None:
            node["$value"] = f"{{color.ramp.{r['family']}.{s}}}"
        else:
            node["$value"] = colour(r["value"])
        return node

    return {
        "$schema": SCHEMA,
        "$description": (
            f"Aninda Studio semantic tokens — {t['label']} theme. Generated; do not "
            f"hand-edit. Every text pairing in this file was measured against every "
            f"surface it can land on, at a target of {t['text_target']}:1, on the "
            f"rounded 8-bit hex and again with every channel of both colours nudged "
            f"by ±1. The published figure is the worst of those."
        ),
        "$extensions": {NS: {
            "direction": DIRECTION,
            "theme": theme_key,
            "polarity": t["polarity"],
            "highContrast": t["high_contrast"],
            "textTarget": t["text_target"],
            "nonTextTarget": t["nontext_target"],
            "generatedBy": "07_tokens/build.py",
            "note": ("DTCG 2025.10 has no theming concept. Themes are separate files "
                     "with identical token paths, because a tool is permitted to "
                     "ignore $extensions and would then render one theme's values "
                     "for all four without erroring."),
        }},
        "color": {
            "$type": "color",
            "surface": surfaces,
            "ink": {"default": role("ink"), "muted": role("ink-muted")},
            "line": {"default": role("line")},
            # `on` is the colour a filled control puts on top of itself. Its value
            # is surface.lowest, and it is a LITERAL rather than an alias because
            # what makes it a token is the proof attached to it: it is measured
            # against every fill that carries it, and the published figure is the
            # worst of those. In the dark themes the hardest ground is `danger`
            # rather than `accent`, so a role proven only against the accent would
            # publish a figure that is not the worst one.
            "accent": {"default": role("accent"), "edge": role("accent-edge"),
                       "hover": role("accent-hover"), "on": role("on-accent")},
            "focus": {"ring": role("focus")},
            "status": {k: role(k) for k in ("success", "warning", "danger", "info")
                       if k in t["roles"]},
        },
    }


FORCED_COLORS = {
    "format": "non-dtcg",
    "$description": (
        "Forced-colors mode cannot be expressed in DTCG. Its values are CSS system "
        "colour keywords supplied by the operating system — they have no colour "
        "space, no components and no hex, and DTCG's thirteen types include nothing "
        "that fits. Bending them into a colour token would be a lie about what they "
        "are, so this file sits deliberately outside the DTCG tree."
    ),
    "generatedBy": "07_tokens/build.py",
    "map": {
        "color.surface.base": "Canvas",
        "color.surface.lowest": "Canvas",
        "color.surface.low": "Canvas",
        "color.surface.high": "Canvas",
        "color.surface.highest": "Canvas",
        "color.surface.dim": "Canvas",
        "color.surface.bright": "Canvas",
        # The page, added with the Natural direction. It aliases the polarity's own
        # extreme — pure white in a light theme, pure black in a dark one — and in
        # forced-colors mode the operating system supplies the page, so it takes
        # Canvas like every other surface.
        "color.surface.page": "Canvas",
        "color.ink.default": "CanvasText",
        # CanvasText, not GrayText. CSS Color 4 defines GrayText normatively as
        # DISABLED text, and this role paints toast bodies, empty-state messages,
        # page subtitles, card meta lines and a badge background — live
        # content, in 33 places in the component layer. In high contrast a reader
        # has learned that colour means "inactive". It also put the measured 5.64:1
        # floor outside this system's control, because WCAG exempts inactive
        # components from contrast requirements, so the guarantee would have been
        # given away for a role that never needed to.
        "color.ink.muted": "CanvasText",
        "color.line.default": "CanvasText",
        "color.accent.default": "LinkText",
        "color.accent.edge": "CanvasText",
        # A button fill, so it takes the system's own button colour rather than a
        # generic one. ButtonFace is paired with ButtonText by the OS, which is
        # what makes the hovered label readable without this file choosing a
        # contrast for it.
        "color.accent.hover": "ButtonFace",
        # Canvas, and NOT ButtonText, which is what this was first mapped to.
        #
        # The reasoning that produced ButtonText was about the wrong pair. This role
        # is the label on a FILL, and the fill it sits on is `accent.default`, three
        # lines above, which maps to LinkText. ButtonText is guaranteed to contrast
        # with ButtonFace, not with LinkText, and 08_components/check.py measured the
        # result in a real browser at 1.5:1 against a 4.5 floor, in both
        # high-contrast themes:
        #
        #   form-with-validation forced-colors [hc-light]: contrast 1.5:1 in the
        #   system palette, needs 4.5:1 — button.as-btn.as-btn--primary
        #
        # Canvas is the ground LinkText is defined to be legible against, and
        # contrast is symmetric, so a Canvas label on a LinkText fill is the same
        # measured pair the operating system already guarantees. It is also what
        # surface.lowest mapped to before this role had a name, which is why nothing
        # regressed until the name arrived.
        "color.accent.on": "Canvas",
        "color.focus.ring": "Highlight",
        "color.status.success": "CanvasText",
        "color.status.warning": "CanvasText",
        "color.status.danger": "CanvasText",
        "color.status.info": "CanvasText",
    },
    "rules": [
        "Every brand colour must be overridden. A hex that survives forced-colors "
        "mode defeats the whole point of it.",
        "forced-color-adjust: none is forbidden except where explicitly allow-listed "
        "with a stated reason.",
        "Because status colours all resolve to CanvasText, nothing may rely on colour "
        "alone — every state carries a glyph and a word regardless.",
        "GrayText is reserved for roles that are genuinely disabled, and this map "
        "assigns it to none. CSS Color 4 defines it normatively as disabled text, so "
        "using it for a live role teaches a high-contrast reader that live content is "
        "inactive — and WCAG exempts inactive components from contrast requirements, "
        "which would hand away a measured guarantee for nothing. color.ink.muted was "
        "mapped to it and paints subtitles, toast bodies and empty-state messages.",
    ],
}


def emit(proof: dict) -> dict[str, dict]:
    files = {"primitive.tokens.json": primitives(proof)}
    for th in THEMES:
        files[f"semantic.{th}.tokens.json"] = semantic(proof, th)
    files["forced-colors.map.json"] = FORCED_COLORS
    return files


def check(files: dict[str, dict], proof: dict) -> list[str]:
    """Re-read what was built and prove it, rather than trusting that it was built."""
    problems: list[str] = []
    prim = files["primitive.tokens.json"]

    def walk(node, path="", inherited=None):
        """Yield (path, token, resolved $type) for every token in the document.

        The third element carries the type down from the nearest ancestor group,
        which is how DTCG inheritance works. It exists because the type gates
        below cannot ask "is this a dimension?" without it.
        """
        if isinstance(node, dict):
            declared = node.get("$type", inherited)
            if "$value" in node:
                yield path, node, declared
            for k, v in node.items():
                if not k.startswith("$"):
                    yield from walk(v, f"{path}.{k}" if path else k, declared)

    for name, doc in files.items():
        if name == "forced-colors.map.json":
            continue
        if doc.get("$schema") != SCHEMA:
            problems.append(f"{name}: wrong or missing $schema")
        for path, tok, type_ in walk(doc):
            v = tok["$value"]

            # A COLOUR IS AN OBJECT, and this is the gate that says so.
            #
            # The earlier form of this gate read `if isinstance(v, dict) and
            # "colorSpace" in v:` — so it ran only on values that had already
            # passed the thing it was checking, which is the same shape of defect
            # round 1 found and fixed in the dimension gate. Proved by making
            # colour() return `f"#{h.upper()}"`, the pre-2025.10 string form:
            # --check reported "6 files verified, 0 problems", exit 0, and wrote
            # the files, while an independent validator found 94 errors over 178
            # tokens. That single change — object, not string — is the most-cited
            # difference between 2025.10 and what came before, and it is the first
            # bullet of this file's own docstring.
            #
            # It is keyed on the resolved $type rather than on the value's shape,
            # because the shape is exactly what is in question. An alias is
            # allowed: a `{…}` reference resolves to the target token's $value.
            if type_ == "color" and not (isinstance(v, str) and v.startswith("{")):
                if not isinstance(v, dict):
                    problems.append(
                        f"{name}:{path}: color $value is {type(v).__name__} "
                        f"{v!r}; DTCG 2025.10 requires an object with colorSpace "
                        f"and components, or an alias")
                else:
                    missing = [k for k in ("colorSpace", "components") if k not in v]
                    if missing:
                        problems.append(f"{name}:{path}: color object has no "
                                        f"{' and no '.join(missing)}")
                    elif "hex" not in v:
                        # `hex` is this system's own srgb fallback, not required by
                        # the format — but every colour here carries one, and the
                        # re-derivation below indexed v["hex"] unconditionally, so
                        # a colour without it raised KeyError instead of reporting
                        # a problem. A gate that crashes reports nothing.
                        problems.append(f"{name}:{path}: color object has no hex, so "
                                        f"the components cannot be re-derived from it")
                    else:
                        h = v["hex"].lstrip("#")
                        want = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
                        got = [round(c * 255) for c in v["components"]]
                        if want != got:
                            problems.append(
                                f"{name}:{path}: components {got} do not re-derive "
                                f"the hex bytes {want}")

            # Every token must resolve a $type, from itself or from an ancestor
            # group, and it must be one of the thirteen the format defines.
            # Nothing checked this before, so a typo in a group's $type or a
            # token added outside any typed group would have shipped.
            if type_ is None:
                problems.append(f"{name}:{path}: no $type on the token or any ancestor group")
            elif type_ not in DTCG_TYPES:
                problems.append(f"{name}:{path}: $type {type_!r} is not one of the "
                                f"{len(DTCG_TYPES)} types DTCG 2025.10 defines")

            # A dimension or a duration is an object carrying BOTH a value and a
            # unit, and the unit is mandatory even at zero. The earlier form of
            # this gate read `if "unit" in v and not v["unit"]`, which could only
            # fire when a unit key was present and empty — that is, never for the
            # failure the specification actually forbids. Round 1 of the
            # convergence review proved it by making dim() drop the unit key:
            # --check reported 0 problems and `--as-space-3: {'value': 16};`
            # reached the shipped stylesheet as a Python dict repr.
            if type_ in ("dimension", "duration"):
                if not isinstance(v, dict):
                    problems.append(f"{name}:{path}: a {type_} $value must be an object "
                                    f"carrying value and unit, not {type(v).__name__}")
                else:
                    missing = [key for key in ("value", "unit") if key not in v]
                    if missing:
                        problems.append(f"{name}:{path}: {type_} has no "
                                        f"{' and no '.join(missing)} — the unit is required "
                                        f"even when the value is zero")
                    elif not v["unit"]:
                        problems.append(f"{name}:{path}: {type_} carries an empty unit")
                    elif v["unit"] not in DTCG_UNITS[type_]:
                        problems.append(f"{name}:{path}: {type_} unit {v['unit']!r} is not one of "
                                        f"{sorted(DTCG_UNITS[type_])}")
            if isinstance(v, str) and v.startswith("{"):
                target = v.strip("{}").split(".")
                node = prim
                for part in target:
                    node = node.get(part) if isinstance(node, dict) else None
                    if node is None:
                        problems.append(f"{name}:{path}: alias {v} does not resolve")
                        break
                else:
                    # The walk above only proves the PATH exists. A `{…}` reference
                    # resolves to the target token's $value, and a group has none,
                    # so an alias pointing at a group is unresolvable under the
                    # format. This gate reported such an alias as clean; proved by
                    # changing a ramp alias from {color.ramp.ground.50} to
                    # {color.ramp.ground} — --check said 0 problems and exit 0,
                    # and emit_css.py then died with KeyError: '$value'. The
                    # downstream crash was the only signal.
                    if not (isinstance(node, dict) and "$value" in node):
                        problems.append(
                            f"{name}:{path}: alias {v} points at a group, not a "
                            f"token. A reference resolves to the target's $value "
                            f"and a group has none")

    # Theme parity: identical token paths in every theme file, or a consumer that
    # switches theme loses tokens without being told.
    sets = {th: {p for p, _, _ in walk(files[f"semantic.{th}.tokens.json"])} for th in THEMES}
    base = sets["light"]
    for th, s in sets.items():
        if s != base:
            problems.append(f"semantic.{th}: token paths differ from light "
                            f"(missing {sorted(base - s)}, extra {sorted(s - base)})")

    # Every role in the forced-colors map must exist, or the two drift apart.
    for role_path in FORCED_COLORS["map"]:
        if role_path not in base:
            problems.append(f"forced-colors.map.json: '{role_path}' is not a real token")

    # Every claimed ratio must still hold against the proof it came from.
    for th in THEMES:
        doc = files[f"semantic.{th}.tokens.json"]
        for path, tok, _ in walk(doc):
            pr = tok.get("$extensions", {}).get(NS, {}).get("proof")
            if not pr:
                continue
            if pr["worstCaseLsb"] < pr["required"]:
                problems.append(f"semantic.{th}:{path}: worst case {pr['worstCaseLsb']} "
                                f"is below its required {pr['required']}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit the Aninda Studio DTCG token set.")
    ap.add_argument("--check", action="store_true", help="verify without writing")
    args = ap.parse_args()

    if not PROOF.exists():
        print(f"Missing {PROOF}. Run 05_colour/engine.py first.", file=sys.stderr)
        return 2

    proof = json.loads(PROOF.read_text())
    files = emit(proof)
    problems = check(files, proof)

    if problems:
        print("FAILED — nothing written:\n", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    counts = []
    for name, doc in files.items():
        blob = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
        counts.append((name, len(blob), hashlib.sha256(blob.encode()).hexdigest()[:12]))

    for name, size, sha in counts:
        print(f"  {name:<34} {size:>7} bytes  sha256:{sha}")

    if args.check:
        print(f"\n--check: {len(files)} files verified, {len(problems)} problems. "
              f"Nothing written.")
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    for name, doc in files.items():
        (OUT / name).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(files)} files to {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
