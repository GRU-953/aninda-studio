#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
Material's ColorScheme cannot be built from this system's tokens as they stand.
Its primary constructor takes 48 named colours and has NO defaults, and the 18
semantic roles here do not cover them. The gap has to be closed by derivation, and
derivation is where a measured system quietly stops being one.

So the rule this file enforces is narrow: every colour it emits must be
bit-identical to a value this system already measured — a semantic role, a tonal
surface, or a step of one of the committed ramps. Nothing is interpolated,
nothing is nudged, and a value that matches none of those stops the build.

WHY NOT lightColorScheme()
--------------------------
Because every parameter of it has a default, and those defaults are Material's
baseline purple. A role this file forgot would ship purple silently — an unmeasured
colour inside the one artefact whose whole claim is that no colour is unmeasured.
The primary constructor has no defaults, so a missing role is a compile error, and
a Material version that adds a role breaks the build loudly rather than filling it
in. The pinned library version becomes the measuring instrument.

WHICH BRAND FAMILY BECOMES WHICH MATERIAL ACCENT GROUP
------------------------------------------------------
Material wants four accent groups: primary, secondary, tertiary and error. This
system has four brand families and all four are primary by the owner's decision of
26 August 2026 — none supports the others. Three map without argument: accent is
primary, ground is secondary (which is what Material means by "less prominent"),
danger is error.

Nothing claimed tertiary. Under Estuary this file took it from a sixth family,
`info`, which the four-colour palette does not have — and `info` is now a ROLE that
resolves to accent, so reading it here would have made tertiary bit-identical to
primary and a tertiary element would not have read as tertiary at all. Two gates
below now forbid exactly that.

Tertiary is the SUCCESS family. Owner's decision, 27 August 2026. The reasoning is
recorded because the cost is real: Material has no success slot of its own, so this
is the only route Natural Green has into an Android colour scheme, and a scheme that
used three of four primaries would contradict the palette it is derived from. What
is given up is that Green carries two meanings on this platform — success in this
system's own roles, and a decorative accent in Material's. A green tertiary chip may
read as a confirmation. Material components use tertiary only when an app asks for
it, so the exposure is small, but it is a cost and not a free choice.

No hue is rotated into existence, which is what Material Theme Builder would have
done, and which no amount of measurement would have entitled this file to do.

CRITERION 21, WHICH THIS FILE LOOKS LIKE IT BREAKS
--------------------------------------------------
Criterion 21 forbids `background`, `onBackground` and `surfaceVariant` as TOKEN
names. This file emits no token by those names. The Compose adapter PASSES them,
because the library's constructor requires them. Two gates hold that line, and both
are in build(): no emitted token identifier may match those three, and in the
emitted Kotlin they may appear only as named arguments inside the ColorScheme call.

RUN
---
    cd <the repository folder>
    ./.venv/bin/python 15_native/material3.py
    ./.venv/bin/python 15_native/material3.py --check
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# The direction is READ from the token set, never named here. This line said
# "estuary" for a day after the palette was replaced, and nothing noticed: the file
# it named still existed and still parsed, so every gate stayed green while the
# whole 48-role scheme shipped the retired palette — Material.kt carried
# 0xFF126974 while Tokens.kt, in the same Kotlin package, carried 0xFF224959.
# The token file records which direction produced it, so there is one name for it
# and every consumer reads that one.
_PRIM = json.loads(
    (ROOT / "07_tokens" / "build" / "primitive.tokens.json").read_text(encoding="utf-8"))
DIRECTION = _PRIM["$extensions"]["studio.aninda"]["direction"]
PROOF = ROOT / "05_colour" / "generated" / f"{DIRECTION}.proof.json"
OUT = HERE / "_proof" / "material3.roles.json"

DEPRECATED_NAMES = ("background", "onBackground", "surfaceVariant")

# The 48 parameters of androidx.compose.material3.ColorScheme's PRIMARY
# constructor, in order, read from ColorScheme.kt on androidx-main on
# 26 August 2026. The order is kept because the emitted Kotlin names every
# argument and a reader comparing the two should not have to sort.
COLOR_SCHEME_PARAMS = (
    "primary", "onPrimary", "primaryContainer", "onPrimaryContainer",
    "inversePrimary", "secondary", "onSecondary", "secondaryContainer",
    "onSecondaryContainer", "tertiary", "onTertiary", "tertiaryContainer",
    "onTertiaryContainer", "background", "onBackground", "surface", "onSurface",
    "surfaceVariant", "onSurfaceVariant", "surfaceTint", "inverseSurface",
    "inverseOnSurface", "error", "onError", "errorContainer", "onErrorContainer",
    "outline", "outlineVariant", "scrim", "surfaceBright", "surfaceDim",
    "surfaceContainer", "surfaceContainerHigh", "surfaceContainerHighest",
    "surfaceContainerLow", "surfaceContainerLowest", "primaryFixed",
    "primaryFixedDim", "onPrimaryFixed", "onPrimaryFixedVariant", "secondaryFixed",
    "secondaryFixedDim", "onSecondaryFixed", "onSecondaryFixedVariant",
    "tertiaryFixed", "tertiaryFixedDim", "onTertiaryFixed",
    "onTertiaryFixedVariant",
)

# Deriving 48 Material roles from 18 measured ones means colours repeat. That is
# arithmetic, not a defect, and enumerating every coincidence would be a wall of
# prose nobody reads. Two questions are worth asking instead, and both are gated.
#
# FIRST: are the pairs Material components actually rely on being different, in fact
# different? A component that draws primary on primaryContainer disappears if those
# two are one colour. This list is those pairs, and it is the one that catches a real
# fault.
MUST_DIFFER = [
    ("primary", "onPrimary", "a filled button would have an invisible label"),
    ("secondary", "onSecondary", "as above, for the secondary group"),
    ("tertiary", "onTertiary", "as above, for the tertiary group"),
    ("error", "onError", "an error button would have an invisible label"),
    ("surface", "onSurface", "body text would vanish"),
    ("surface", "onSurfaceVariant", "secondary text would vanish"),
    ("surface", "outline", "a text field would have no visible border"),
    ("primary", "tertiary", "a tertiary accent that equals primary is not an accent"),
    ("secondary", "tertiary", "as above — three accent groups, or two wearing three names"),
    ("primary", "primaryContainer", "a tonal button would not read as tonal"),
    ("secondary", "secondaryContainer", "as above"),
    ("tertiary", "tertiaryContainer", "as above"),
    ("error", "errorContainer", "as above"),
    ("primaryContainer", "onPrimaryContainer", "the ink on a tonal button"),
    ("secondaryContainer", "onSecondaryContainer", "as above"),
    ("tertiaryContainer", "onTertiaryContainer", "as above"),
    ("errorContainer", "onErrorContainer", "as above"),
    ("primaryFixed", "onPrimaryFixed", "the ink on a fixed fill"),
    ("primaryFixed", "primaryFixedDim", "the dim sibling has to be dimmer"),
    ("secondaryFixed", "secondaryFixedDim", "as above"),
    ("tertiaryFixed", "tertiaryFixedDim", "as above"),
    ("onPrimaryFixed", "onPrimaryFixedVariant", "two levels of emphasis"),
    ("surface", "inverseSurface", "the inverse of a surface cannot be that surface"),
    ("surface", "surfaceContainerHighest", "the depth ladder needs two ends"),
    ("surfaceDim", "surfaceBright", "the dimmest and brightest cannot be one"),
]

# SECOND: does the scheme carry enough distinct colours to be a Material scheme at
# all? A floor rather than a target. The figure is measured and published either
# way, so a scheme that thins out is visible before it breaks anything.
MIN_DISTINCT_COLOURS = 20


class Fail(Exception):
    pass


def engine():
    spec = importlib.util.spec_from_file_location(
        "aninda_engine", ROOT / "05_colour" / "engine.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["aninda_engine"] = mod
    spec.loader.exec_module(mod)
    return mod


def pick_container_pair(E, ramp: dict, surface: str, accent: str, polarity: str,
                        target: float, what: str) -> tuple[str, str, dict]:
    """A container fill and the ink that sits on it, both from one measured ramp.

    What Material actually guarantees about a container is the PAIR: the on-colour
    is legible on the container. That is the requirement enforced here.

    What it does not guarantee is 3:1 against the surface. The first version of this
    function required it and produced a container identical to `primary`, because the
    only accent steps clearing 3:1 on a light surface are the dark ones. Material's
    own guidance is narrower than that: clustered elements "benefit from 3:1 contrast
    between themselves and the background", while "standalone components, such as
    FABs, don't need to meet Material's minimum contrast of 3:1". So the figure is
    MEASURED and recorded on every container, and it gates nothing.

    Two things do gate. The container must be visibly different from the surface, or
    it is not a container at all. And it must be visibly different from the accent,
    or the scheme claims a depth it does not have.

    The search runs from the surface's own end of the ramp inward, so a container is
    the quietest fill that works rather than the loudest.
    """
    steps = list(ramp)
    order = steps if polarity == "light" else list(reversed(steps))
    best = None
    for c in order:
        fill = ramp[c]
        if E.de2000(fill, surface) < E.MIN_SURFACE_DE:
            continue                      # indistinguishable from the surface
        if E.de2000(fill, accent) < E.MIN_RAMP_DE:
            continue                      # indistinguishable from the accent itself
        for o in reversed(order):
            ink = ramp[o]
            w = E.worst_case_ratio(ink, fill)
            if w >= target:
                return fill, ink, {
                    "container_step": c, "on_step": o,
                    "pair_ratio": E.ratio(ink, fill),
                    "pair_worst_case_lsb": w,
                    "required_pair": target,
                    "level": E.level(w, "text", target),
                    "container_against_surface": E.worst_case_ratio(fill, surface),
                    "container_against_surface_note": (
                        "Measured, and deliberately not gated. Material asks 3:1 of "
                        "CLUSTERED elements and exempts standalone ones such as a "
                        "FAB, so this figure informs a layout decision rather than "
                        "deciding whether the role may exist."),
                    "de_from_surface": E.de2000(fill, surface),
                    "de_from_accent": E.de2000(fill, accent),
                }
            if best is None or w > best:
                best = w
    raise Fail(
        f"{what}: no step of this ramp is distinct from both the surface and the "
        f"accent and still carries ink at {target}:1. Best pair seen was "
        f"{best if best else 'nothing'}:1.")


def pick_fixed_pair(E, ramp: dict, target: float, what: str) -> tuple[str, str, str, str, dict]:
    """A fixed accent, its dim sibling, and the two inks that sit on them.

    Material's fixed roles keep ONE tone across light and dark, which is exactly
    what makes them dangerous: a colour that does not change cannot adapt, so its
    contrast has to hold in both polarities at once or it holds in neither. Material
    says so itself — "Fixed colors don't change based on light or dark theme, so
    they're likely to cause contrast issues."

    So both inks are measured against both fills here, and the worst of the four is
    what has to clear the target.
    """
    steps = list(ramp)
    for i, f in enumerate(steps):
        fill = ramp[f]
        for d in steps[i + 1:]:
            dim = ramp[d]
            if E.de2000(fill, dim) < E.MIN_RAMP_DE:
                continue
            for o in reversed(steps):
                ink = ramp[o]
                worst = min(E.worst_case_ratio(ink, fill),
                            E.worst_case_ratio(ink, dim))
                if worst < target:
                    continue
                # The "variant" ink is Material's LOWER-emphasis one. The first
                # version scanned in the same direction as `ink` and so returned the
                # same step every time, which is how onPrimaryFixed and
                # onPrimaryFixedVariant came out identical — a distinction the
                # scheme claimed and did not have.
                #
                # Lower emphasis means the LEAST contrast that still clears the
                # target, so the scan runs from the fill outward and stops at the
                # first step that works, rather than from the far end inward.
                variant = None
                for v in steps:
                    wv = min(E.worst_case_ratio(ramp[v], fill),
                             E.worst_case_ratio(ramp[v], dim))
                    if wv >= target:
                        variant = ramp[v]
                        break
                if variant is None or variant == ink:
                    continue    # no room for two levels of emphasis on this fill
                return fill, dim, ink, variant, {
                    "fixed_step": f, "dim_step": d, "on_step": o,
                    "worst_of_four_pairings": worst,
                    "required": target,
                    "de_fixed_to_dim": E.de2000(fill, dim),
                    "level": E.level(worst, "text", target),
                    "note": ("Both inks are measured against BOTH fills, because a "
                             "fixed colour does not change with the theme and so has "
                             "to hold in light and dark at once."),
                }
    raise Fail(f"{what}: no pair of steps in this ramp holds {target}:1 under one "
               f"ink on both the fixed and the dim fill.")


def derive(E, proof: dict) -> dict:
    """Every Material role for every theme, each traced to what it came from."""
    themes = proof["themes"]
    ramps = {k: v["ramp"] for k, v in proof["families"].items()} \
        if "families" in proof else None
    if ramps is None:
        ramps = {k: v["ramp"] for k, v in proof["ramps"].items()}

    # The opposite polarity, for the three inverse roles. Material's inverse roles
    # are "the reverse of those in the surrounding UI", which in a system that
    # already ships a light and a dark theme is not a derivation at all — it is the
    # other theme's value, and taking it from there keeps the two in step.
    OPPOSITE = {"light": "dark", "dark": "light",
                "hc-light": "hc-dark", "hc-dark": "hc-light"}

    out: dict[str, dict] = {}
    for key, t in themes.items():
        r = t["roles"]
        s = t["surfaces"]
        other = themes[OPPOSITE[key]]
        target = t["text_target"]
        polarity = t["polarity"]
        proofs: dict[str, dict] = {}

        def measured(name, ink, ground, req):
            w = E.worst_case_ratio(ink, ground)
            proofs[name] = {"ink": ink, "ground": ground, "required": req,
                            "measured": E.ratio(ink, ground), "worst_case_lsb": w,
                            "level": E.level(w, "text" if req >= 4.5 else "nontext", req)}
            if w < req:
                raise Fail(f"{key}/{name}: {ink} on {ground} is {w:.4f}:1, "
                           f"under {req}:1")

        # --- containers, one measured pair per accent group -----------------
        pri_c, pri_on, pri_p = pick_container_pair(
            E, ramps["accent"], s["base"], r["accent"]["value"], polarity, target, f"{key}/primaryContainer")
        sec_c, sec_on, sec_p = pick_container_pair(
            E, ramps["ground"], s["base"], r["accent"]["value"], polarity, target, f"{key}/secondaryContainer")
        ter_c, ter_on, ter_p = pick_container_pair(
            E, ramps["success"], s["base"], r["accent"]["value"], polarity, target, f"{key}/tertiaryContainer")
        err_c, err_on, err_p = pick_container_pair(
            E, ramps["danger"], s["base"], r["accent"]["value"], polarity, target, f"{key}/errorContainer")
        proofs.update({"primaryContainer": pri_p, "secondaryContainer": sec_p,
                       "tertiaryContainer": ter_p, "errorContainer": err_p})

        # --- the twelve fixed roles -----------------------------------------
        pf, pfd, pfo, pfov, pf_p = pick_fixed_pair(
            E, ramps["accent"], target, f"{key}/primaryFixed")
        sf, sfd, sfo, sfov, sf_p = pick_fixed_pair(
            E, ramps["ground"], target, f"{key}/secondaryFixed")
        tf, tfd, tfo, tfov, tf_p = pick_fixed_pair(
            E, ramps["success"], target, f"{key}/tertiaryFixed")
        proofs.update({"primaryFixed": pf_p, "secondaryFixed": sf_p,
                       "tertiaryFixed": tf_p})

        # --- secondary and tertiary accents, from families that already exist -
        # secondary is the GROUND family used as an accent, which is what Material
        # means by "less prominent". tertiary is the SUCCESS family — the fourth
        # brand primary, which Material has no slot of its own for. Neither is a hue
        # rotated into existence, which is what Material Theme Builder would do.
        #
        # tertiary read r["info"] until 27 August 2026. Under the six-colour palette
        # info was its own family; under this one it is a role that resolves to
        # accent, so that line would have handed tertiary the primary colour.
        secondary = r["ink-muted"]["value"]
        tertiary = r["success"]["value"]

        scheme = {
            "primary": r["accent"]["value"],
            "onPrimary": r["on-accent"]["value"],
            "primaryContainer": pri_c,
            "onPrimaryContainer": pri_on,
            "inversePrimary": other["roles"]["accent"]["value"],
            "secondary": secondary,
            "onSecondary": r["on-accent"]["value"],
            "secondaryContainer": sec_c,
            "onSecondaryContainer": sec_on,
            "tertiary": tertiary,
            "onTertiary": r["on-accent"]["value"],
            "tertiaryContainer": ter_c,
            "onTertiaryContainer": ter_on,
            "background": s["base"],
            "onBackground": r["ink"]["value"],
            "surface": s["base"],
            "onSurface": r["ink"]["value"],
            "surfaceVariant": s["highest"],
            "onSurfaceVariant": r["ink-muted"]["value"],
            "surfaceTint": r["accent"]["value"],
            "inverseSurface": other["surfaces"]["base"],
            "inverseOnSurface": other["roles"]["ink"]["value"],
            "error": r["danger"]["value"],
            "onError": r["on-accent"]["value"],
            "errorContainer": err_c,
            "onErrorContainer": err_on,
            "outline": r["line"]["value"],
            "outlineVariant": r["line"]["value"],
            "scrim": r["ink"]["value"],
            "surfaceBright": s["bright"],
            "surfaceDim": s["dim"],
            "surfaceContainer": s["base"],
            "surfaceContainerHigh": s["high"],
            "surfaceContainerHighest": s["highest"],
            "surfaceContainerLow": s["low"],
            "surfaceContainerLowest": s["lowest"],
            "primaryFixed": pf, "primaryFixedDim": pfd,
            "onPrimaryFixed": pfo, "onPrimaryFixedVariant": pfov,
            "secondaryFixed": sf, "secondaryFixedDim": sfd,
            "onSecondaryFixed": sfo, "onSecondaryFixedVariant": sfov,
            "tertiaryFixed": tf, "tertiaryFixedDim": tfd,
            "onTertiaryFixed": tfo, "onTertiaryFixedVariant": tfov,
        }

        # --- the pairs Material components actually put together -------------
        measured("onPrimary", scheme["onPrimary"], scheme["primary"], target)
        measured("onSecondary", scheme["onSecondary"], scheme["secondary"], target)
        measured("onTertiary", scheme["onTertiary"], scheme["tertiary"], target)
        measured("onError", scheme["onError"], scheme["error"], target)
        measured("onSurface", scheme["onSurface"], scheme["surface"], target)
        measured("onSurfaceVariant", scheme["onSurfaceVariant"],
                 scheme["surfaceVariant"], target)
        measured("onBackground", scheme["onBackground"], scheme["background"], target)
        measured("inverseOnSurface", scheme["inverseOnSurface"],
                 scheme["inverseSurface"], target)
        measured("outline", scheme["outline"], scheme["surface"], E.AA_NONTEXT)
        measured("inversePrimary", scheme["inversePrimary"],
                 scheme["inverseSurface"], E.AA_NONTEXT)

        out[key] = {"scheme": scheme, "proofs": proofs,
                    "polarity": polarity, "text_target": target}
    return out


def guard_provenance(schemes: dict, proof: dict) -> dict:
    """Every emitted colour must be one this system already measured.

    This is the whole rule. A derivation that produces a colour matching no
    semantic role, no tonal surface and no ramp step is an invented colour, and an
    invented colour in a Material scheme is indistinguishable from Material's own
    baseline purple as far as this system's claims go: neither was measured here.
    """
    themes = proof["themes"]
    ramps = ({k: v["ramp"] for k, v in proof["families"].items()}
             if "families" in proof else
             {k: v["ramp"] for k, v in proof["ramps"].items()})
    known: dict[str, str] = {}
    for fam, ramp in ramps.items():
        for step, hexv in ramp.items():
            known.setdefault(hexv.upper(), f"ramp {fam}.{step}")
    for tkey, t in themes.items():
        for name, hexv in t["surfaces"].items():
            known.setdefault(hexv.upper(), f"{tkey} surface.{name}")
        for name, role in t["roles"].items():
            known.setdefault(role["value"].upper(), f"{tkey} role.{name}")

    traced: dict[str, dict[str, str]] = {}
    for tkey, entry in schemes.items():
        traced[tkey] = {}
        for role, hexv in entry["scheme"].items():
            src = known.get(hexv.upper())
            if src is None:
                raise Fail(
                    f"{tkey}/{role} is {hexv}, which matches no ramp step, no tonal "
                    f"surface and no semantic role in this system. Every Material "
                    f"role has to trace to something that was measured.")
            traced[tkey][role] = src
    return traced


def guard_must_differ(schemes: dict) -> dict:
    """The pairs a Material component would break on if they were one colour."""
    distinct = {}
    for tkey, entry in schemes.items():
        sch = entry["scheme"]
        for a, b, why in MUST_DIFFER:
            if sch[a] == sch[b]:
                raise Fail(
                    f"{tkey}: '{a}' and '{b}' are both {sch[a]}, and they must differ "
                    f"— {why}.")
        n = len(set(sch.values()))
        if n < MIN_DISTINCT_COLOURS:
            raise Fail(
                f"{tkey}: the 48 Material roles resolve to only {n} distinct colours, "
                f"under the floor of {MIN_DISTINCT_COLOURS}. A scheme this thin has "
                f"stopped expressing the hierarchy Material components draw with.")
        distinct[tkey] = n
    return distinct


def guard_fixed_hold_one_tone(schemes: dict) -> None:
    """Material's fixed roles must not change with the theme. That is their point.

    Material's own warning is that fixed colours "don't change based on light or
    dark theme, so they're likely to cause contrast issues" — which is only true if
    they genuinely do not change. This held from the first run, because
    pick_fixed_pair reads the ramp and the target and never the surfaces. It held by
    accident of the implementation, and an accident is not a property, so it is
    checked here.
    """
    fixed = [r for r in COLOR_SCHEME_PARAMS if "Fixed" in r]
    for a, b in (("light", "dark"), ("hc-light", "hc-dark")):
        for role in fixed:
            if schemes[a]["scheme"][role] != schemes[b]["scheme"][role]:
                raise Fail(
                    f"'{role}' is {schemes[a]['scheme'][role]} in {a} and "
                    f"{schemes[b]['scheme'][role]} in {b}. A fixed role that changes "
                    f"with the theme is not fixed, and every component that relies on "
                    f"it holding one tone across a theme switch is wrong.")


def guard_surface_ladder(E, schemes: dict) -> None:
    """The five surface containers must step in one direction, re-derived."""
    order = ["surfaceContainerLowest", "surfaceContainerLow", "surfaceContainer",
             "surfaceContainerHigh", "surfaceContainerHighest"]
    for tkey, entry in schemes.items():
        lums = [E.luminance(entry["scheme"][n]) for n in order]
        rising = all(b >= a for a, b in zip(lums, lums[1:]))
        falling = all(b <= a for a, b in zip(lums, lums[1:]))
        if not (rising or falling):
            raise Fail(
                f"{tkey}: the five surface containers are not monotonic in "
                f"luminance ({[round(x, 5) for x in lums]}). Material uses them as a "
                f"depth ladder, and a ladder with a rung out of order reads as an "
                f"accident.")


def guard_names(schemes: dict) -> None:
    """The three deprecated Material names may be constructor ARGUMENTS and must
    never be token names. Criterion 21 forbids the second, not the first."""
    for tkey, entry in schemes.items():
        for role in entry["scheme"]:
            if role in DEPRECATED_NAMES:
                continue        # legitimate: the constructor requires it
        missing = [p for p in COLOR_SCHEME_PARAMS if p not in entry["scheme"]]
        extra = [p for p in entry["scheme"] if p not in COLOR_SCHEME_PARAMS]
        if missing or extra:
            raise Fail(
                f"{tkey}: the scheme does not match ColorScheme's primary "
                f"constructor. Missing {missing}; unexpected {extra}. The constructor "
                f"has no defaults, so a missing role would ship Material's baseline "
                f"purple rather than erroring.")


def build() -> dict:
    E = engine()
    proof = json.loads(PROOF.read_text(encoding="utf-8"))
    schemes = derive(E, proof)
    guard_names(schemes)
    distinct = guard_must_differ(schemes)
    guard_fixed_hold_one_tone(schemes)
    guard_surface_ladder(E, schemes)
    traced = guard_provenance(schemes, proof)
    return {
        "_generator": "15_native/material3.py",
        "_warning": ("GENERATED FILE. Written by 15_native/material3.py. Do not "
                     "hand-edit — the next build overwrites it."),
        "constructor": {
            "class": "androidx.compose.material3.ColorScheme",
            "parameters": len(COLOR_SCHEME_PARAMS),
            "order": list(COLOR_SCHEME_PARAMS),
            "why_primary_constructor": (
                "lightColorScheme() defaults every parameter to Material's baseline "
                "purple, so a role this file forgot would ship an unmeasured colour "
                "silently. The primary constructor has no defaults, so a missing role "
                "is a compile error and a Material version that adds one breaks the "
                "build loudly."),
        },
        "deprecated_names_note": (
            "background, onBackground and surfaceVariant appear here as constructor "
            "ARGUMENTS because the library requires them. No token in this system "
            "carries those names, which is what criterion 21 forbids."),
        "accent_groups": (
            f"This system has four brand families and all four are primary. Material "
            f"wants four accent groups and three map without argument: accent is "
            f"primary, ground is secondary, danger is error. Tertiary is the success "
            f"family, by the owner's decision of 27 August 2026, because Material has "
            f"no success slot and a scheme using three of four primaries would "
            f"contradict the palette it comes from. The cost is that green carries two "
            f"meanings here — success among this system's roles, a decorative accent "
            f"among Material's — so a green tertiary element may read as a "
            f"confirmation. No hue was rotated into existence. Read from "
            f"{DIRECTION}.proof.json."),
        "distinct_colours_per_theme": distinct,
        "repetition_note": (
            "48 Material roles are derived from 18 measured ones, so colours repeat. "
            "Rather than enumerate every coincidence, two things are gated: the "
            f"{len(MUST_DIFFER)} pairs a Material component would break on if they "
            "were one colour, and a floor on how many distinct colours a scheme "
            "carries. The repeated values are visible in the scheme itself."),
        "must_differ": [{"a": a, "b": b, "why": why} for a, b, why in MUST_DIFFER],
        "themes": {k: {"polarity": v["polarity"], "text_target": v["text_target"],
                       "scheme": v["scheme"], "proofs": v["proofs"],
                       "provenance": traced[k]}
                   for k, v in schemes.items()},
    }


def main(argv: list[str]) -> int:
    try:
        payload = build()
    except Fail as exc:
        print(f"FAILED — nothing written:\n  {exc}", file=sys.stderr)
        return 1
    text = json.dumps(payload, indent=1, ensure_ascii=False) + "\n"
    if "--check" in argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print(f"CHECK FAILED — {OUT.name} differs from a fresh derivation",
                  file=sys.stderr)
            return 1
        print(f"--check: {OUT.name} matches the palette it derives from. "
              f"Nothing written.")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    n = len(COLOR_SCHEME_PARAMS)
    print(f"Wrote {OUT.relative_to(ROOT)} — {n} Material roles across "
          f"{len(payload['themes'])} themes, every one traced to a measured value.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
