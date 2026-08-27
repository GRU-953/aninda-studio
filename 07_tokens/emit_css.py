#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
To turn the DTCG token set into stylesheets, and then to PROVE the stylesheets
say the same thing as the tokens. Producing an output is not evidence about the
output, so `--check` re-parses the emitted CSS, pulls every custom property back
out of it, and compares value by value against the source. It also asserts set
equality in both directions: no property in the CSS that is not a token, and no
token missing from the CSS.

THEME SCOPING, AND THE ONE RULE THAT MAKES IT WORK
--------------------------------------------------
`[data-theme]` is scoped to the attribute, never to `:root`. That single decision
is what lets a dark panel sit inside a light page — which is a real requirement
the moment a page has a code block, a hero, or an embedded preview.

The cascade is ordered deliberately, and the order is the whole trick:

  1. `:root`                                  light values, the default
  2. `@media (prefers-color-scheme: dark)`
     `:root:not([data-theme])`                follow the reader's system setting,
                                              but ONLY if nobody chose explicitly
  3. `@media (prefers-contrast: more)`        the same, for high contrast
  4. `[data-theme="light"]` … `["hc-dark"]`   an explicit choice, anywhere in the
                                              tree, and it wins because it comes last
  5. `@media (forced-colors: active)`         the operating system wins over all

Put the explicit blocks BEFORE the media queries and a reader whose system is set
to dark can never choose light. The order is not cosmetic.

RUN
---
    cd <the repository folder>
    ./.venv/bin/python 07_tokens/emit_css.py
    ./.venv/bin/python 07_tokens/emit_css.py --check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = HERE / "build"
OUT = HERE / "css"
NS = "studio.aninda"
P = "--as-"

THEMES = ("light", "dark", "hc-light", "hc-dark")

HEADER = """/* Aninda Studio — {what}
 *
 * GENERATED FILE. Do not hand-edit.
 *   Regenerate:  ./.venv/bin/python 07_tokens/emit_css.py
 *   Source:      07_tokens/build/*.tokens.json  (DTCG 2025.10)
 *
 * Not one colour in this file was typed by a person. Every value was computed by
 * 05_colour/engine.py and measured against every surface it can land on.
 *
 * SPDX-License-Identifier: Apache-2.0
 * Copyright 2026 Aninda Sundar Howlader
 */
"""


def load() -> tuple[dict, dict[str, dict], dict]:
    prim = json.loads((SRC / "primitive.tokens.json").read_text())
    sem = {t: json.loads((SRC / f"semantic.{t}.tokens.json").read_text()) for t in THEMES}
    forced = json.loads((SRC / "forced-colors.map.json").read_text())
    return prim, sem, forced


def resolve(value, prim: dict):
    """Resolve an alias to its primitive value. Cycles are impossible here because
    aliases only ever point from semantic files into the primitive file."""
    if isinstance(value, str) and value.startswith("{"):
        node = prim
        for part in value.strip("{}").split("."):
            node = node[part]
        return node["$value"]
    return value


def fmt(v) -> str:
    if isinstance(v, dict) and "hex" in v:
        return v["hex"]
    if isinstance(v, dict) and "unit" in v:
        n = v["value"]
        n = int(n) if isinstance(n, float) and n.is_integer() else n
        return f"{n}{v['unit']}"
    if isinstance(v, list) and all(isinstance(x, (int, float)) for x in v):
        return "cubic-bezier(" + ", ".join(str(x) for x in v) + ")"
    if isinstance(v, list):
        return ", ".join(f'"{x}"' if " " in x else x for x in v)
    return str(v)


def prop_for(path: str) -> str:
    """The one place a DTCG token path becomes a CSS custom property name.

    It exists because the first version derived the name twice — once in the
    theme emitter and once in the forced-colors emitter — with two slightly
    different string manipulations. `color.status.success` became `--as-success`
    in one and `--as-status-success` in the other, so the forced-colors block
    overrode a property nothing used and the four status colours kept their brand
    hex right through forced-colors mode.

    The static verifier did not catch it, because it derived the name with the
    *same* wrong transformation and so confirmed its own mistake. Only rendering
    the page in a browser found it. One function, used everywhere, is the fix.
    """
    parts = path.split(".")
    if parts[0] == "color":
        parts = parts[1:]
    if parts[0] == "status":          # color.status.danger -> --as-danger
        parts = parts[1:]
    if len(parts) > 1 and parts[-1] == "default":   # color.ink.default -> --as-ink
        parts = parts[:-1]
    return P + "-".join(parts)


def theme_vars(doc: dict, prim: dict) -> dict[str, str]:
    c = doc["color"]
    out: dict[str, str] = {}
    for name, tok in c["surface"].items():
        out[prop_for(f"color.surface.{name}")] = fmt(resolve(tok["$value"], prim))
    # Walked, not listed. This used to be a hand-typed tuple of (group, keys),
    # and adding color.accent.hover to the token source emitted the forced-colors
    # override for it — that block iterates the map — while the four theme blocks
    # emitted nothing, because `hover` was not in the tuple. A property overridden
    # in forced-colors mode and defined in no theme is the same defect prop_for was
    # written to end, one level up: two derivations of the same list disagreeing.
    # The token document is now the only list.
    for group in ("ink", "line", "accent", "focus", "status"):
        for k, tok in c.get(group, {}).items():
            if k.startswith("$"):
                continue
            out[prop_for(f"color.{group}.{k}")] = fmt(resolve(tok["$value"], prim))
    # A shadow on a dark ground reads as dirt, so in the dark and high-contrast
    # themes the elevation shadow resolves to none and a lighter surface carries
    # the lift instead. Stated here rather than left for a component to discover.
    dark = doc["$extensions"][NS]["polarity"] == "dark"
    hc = doc["$extensions"][NS]["highContrast"]
    out[f"{P}shadow-float"] = (
        "none" if (dark or hc)
        else "0 1px 2px rgb(0 0 0 / 0.06), 0 8px 24px rgb(0 0 0 / 0.08)"
    )
    out[f"{P}color-scheme"] = "dark" if dark else "light"
    return out


def static_vars(prim: dict) -> dict[str, str]:
    d = prim["dimension"]
    out: dict[str, str] = {}
    for i, tok in d["space"].items():
        out[f"{P}space-{i}"] = fmt(tok["$value"])
    for k, tok in d["radius"].items():
        out[f"{P}radius-{k}"] = fmt(tok["$value"])
    for k, tok in d["target"].items():
        out[f"{P}target-{k}"] = fmt(tok["$value"])
    for k, tok in d["focus"].items():
        out[f"{P}focus-{k}"] = fmt(tok["$value"])
    for k, tok in d["type"].items():
        out[f"{P}text-{k}"] = fmt(tok["$value"])
    for k, tok in prim["fontFamily"].items():
        if not k.startswith("$"):
            out[f"{P}font-{k}"] = fmt(tok["$value"])
    for k, tok in prim["duration"]["motion"].items():
        out[f"{P}duration-{k}"] = fmt(tok["$value"])
    for k, tok in prim["cubicBezier"]["motion"].items():
        out[f"{P}ease-{k}"] = fmt(tok["$value"])
    out[f"{P}scale-ratio"] = fmt(prim["number"]["scale"]["ratio"]["$value"])
    return out


def block(sel: str, vars_: dict[str, str], indent: str = "  ") -> str:
    body = "\n".join(f"{indent}{k}: {v};" for k, v in vars_.items())
    return f"{sel} {{\n{body}\n}}\n"


def build(prim: dict, sem: dict[str, dict], forced: dict) -> str:
    tv = {t: theme_vars(sem[t], prim) for t in THEMES}
    parts = [HEADER.format(what="design tokens")]

    parts.append("/* 1. The default. Light values, unscoped. */\n")
    parts.append(block(":root", {**static_vars(prim), **tv["light"]}))
    parts.append("  :root { color-scheme: light dark; }\n".replace("  ", ""))

    parts.append("\n/* 2. Follow the reader's system setting — but only where nobody\n"
                 "   has chosen explicitly. `:not([data-theme])` is what makes an\n"
                 "   explicit choice further down the tree possible at all. */\n")
    parts.append("@media (prefers-color-scheme: dark) {\n"
                 + block(":root:not([data-theme])", tv["dark"], "    ").replace("\n", "\n  ")[:-2]
                 + "}\n")

    parts.append("\n/* 3. The same, for high contrast. */\n")
    parts.append("@media (prefers-contrast: more) {\n"
                 + block(":root:not([data-theme])", tv["hc-light"], "    ").replace("\n", "\n  ")[:-2]
                 + "}\n")
    parts.append("@media (prefers-contrast: more) and (prefers-color-scheme: dark) {\n"
                 + block(":root:not([data-theme])", tv["hc-dark"], "    ").replace("\n", "\n  ")[:-2]
                 + "}\n")

    parts.append("\n/* 4. An explicit choice, on ANY element — which is what lets a dark\n"
                 "   panel sit inside a light page. These come last so they win. */\n")
    for t in THEMES:
        parts.append(block(f'[data-theme="{t}"]', tv[t]))

    parts.append("\n/* 5. Forced colours. The operating system supplies the palette, so every\n"
                 "   brand value must give way. A hex that survives this mode defeats it.\n"
                 "   Both `:root` and `[data-theme]` are targeted, or a themed island keeps\n"
                 "   its own colours while the rest of the page gives them up. */\n")
    fmap = {prop_for(k): v for k, v in forced["map"].items()}
    fmap[f"{P}shadow-float"] = "none"
    parts.append("@media (forced-colors: active) {\n"
                 + block(":root, [data-theme]", fmap, "    ").replace("\n", "\n  ")[:-2]
                 + "}\n")

    # A MOVEMENT IS REMOVED. A CROSS-FADE IS NOT.
    #
    # Both durations used to collapse to 1 ms here, and that is not what either
    # platform asks for. Apple lists REPLACING transitions among the practices for
    # Reduce Motion, not deleting them; Material expresses the same split
    # numerically, with every effects damping at exactly 1.0 — critically damped,
    # never overshooting — while spatial damping sits below it. The reduced case is
    # the effects half surviving and the spatial half going.
    #
    # This system already argued exactly that in print, in the guidebook's motion
    # chapter: "things that move may overshoot; things that only change colour never
    # do. That is why --as-duration-colour and --as-duration-move are two tokens and
    # not one." The stylesheet had simply not been doing what the book said.
    #
    # The colour duration is INTERPOLATED from the primitive, never typed, so it
    # cannot drift from the value the rest of the sheet uses. It is stated rather
    # than left to inherit for three reasons: it records the decision where a reader
    # looks for it, it survives a later override further down the tree, and it gives
    # the gates a property to READ under reduce rather than an absence to interpret.
    colour_ms = prim["duration"]["motion"]["colour"]["$value"]["value"]
    parts.append("\n/* 6. Reduced motion. A movement is removed; the cross-fade is not. */\n"
                 "@media (prefers-reduced-motion: reduce) {\n"
                 "  :root {\n"
                 f"    {P}duration-move: 1ms;\n"
                 f"    {P}duration-colour: {colour_ms:g}ms;\n"
                 "  }\n}\n")

    # SECTION 7 WAS THE BANGLA BLOCK, and it was the best-argued rule in this
    # file: one `clamp()` carrying the measured multiplier AND its floor, so nobody
    # had to remember the exception, plus text-transform, letter-spacing and both
    # font-synthesis properties held down because all four destroy either the
    # matra or the conjuncts. It left with the Bangla on 27 August 2026.
    #
    # Nothing replaced it, and nothing should: the rule existed because two scripts
    # at one nominal size do not look the same size. One script has no such problem.
    return "".join(parts)


def extract(css: str) -> dict[str, list[str]]:
    """Pull every custom property back out of the emitted CSS."""
    found: dict[str, list[str]] = {}
    for m in re.finditer(r"(--as-[a-z0-9-]+)\s*:\s*([^;]+);", css):
        found.setdefault(m.group(1), []).append(m.group(2).strip())
    return found


def verify(css: str, prim: dict, sem: dict[str, dict], forced: dict) -> list[str]:
    problems: list[str] = []
    found = extract(css)

    expected: dict[str, set[str]] = {}
    for k, v in static_vars(prim).items():
        expected.setdefault(k, set()).add(v)
    for t in THEMES:
        for k, v in theme_vars(sem[t], prim).items():
            expected.setdefault(k, set()).add(v)

    for k in sorted(set(expected) - set(found)):
        problems.append(f"token '{k}' is in the source but not in the CSS")
    unexpected = set(found) - set(expected) - {f"{P}color-scheme"}
    for k in sorted(unexpected):
        # forced-colors keywords are legitimately not token values
        if all(v[0].isupper() for v in found[k]) or found[k] == ["none"]:
            continue
        problems.append(f"CSS defines '{k}', which is not a token")

    for k, want in expected.items():
        got = set(found.get(k, []))
        missing = want - got
        if missing:
            problems.append(f"'{k}': source values {sorted(missing)} never appear in the CSS")

    # Cascade order, proved by position rather than by hoping.
    i_media = css.find("@media (prefers-color-scheme: dark)")
    i_expl = css.find('[data-theme="light"]')
    i_forced = css.find("@media (forced-colors: active)")
    if not (0 < i_media < i_expl < i_forced):
        problems.append("cascade order is wrong: the explicit [data-theme] blocks must "
                        "come after the media queries and before forced-colors")

    # No brand colour may survive forced-colors mode.
    fblock = css[i_forced:]
    # 3, 4, 6 and 8 digits are all valid CSS hex, and so are the colour
    # functions. Matching only six digits meant a brand colour written #f00
    # or #0C3A31FF survived forced-colors mode with the guard reporting clean.
    if re.search(r"#[0-9a-f]{3,8}\b"
                 r"|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\s*\(",
                 fblock, re.IGNORECASE):
        problems.append("a hex colour survives the forced-colors block")
    # Every colour property the themes define must be overridden here — derived
    # from what the CSS actually emits, NOT from the forced-colors map, so the
    # check cannot agree with the emitter about a name they both got wrong.
    colour_props = {k for k in theme_vars(sem["light"], prim)
                    if k not in (f"{P}shadow-float", f"{P}color-scheme")}
    for prop in sorted(colour_props):
        if not re.search(rf"{re.escape(prop)}\s*:", fblock):
            problems.append(f"forced-colors block does not override '{prop}' — its brand "
                            f"value would survive into forced-colors mode")
    # And the converse, which is not the same check. A property overridden here
    # and defined in no theme is an override of nothing: the name is dead, any
    # component using it falls back to the initial value, and the check above
    # reads clean because it only walks the other direction. This happened while
    # color.accent.hover was being added — the forced-colors emitter iterates the
    # map and picked it up, while theme_vars was iterating a hand-typed list of
    # group keys and did not. The `unexpected` loop above cannot see it either,
    # because it deliberately excuses any property whose values are all system
    # keywords, which is exactly what a dead forced-colors override looks like.
    for prop in sorted(set(re.findall(r"(--as-[a-z0-9-]+)\s*:", fblock))):
        if prop not in theme_vars(sem["light"], prim) and prop not in static_vars(prim):
            problems.append(f"forced-colors block overrides '{prop}', which no theme "
                            f"defines — the override applies to nothing")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not (SRC / "primitive.tokens.json").exists():
        print("No token build. Run 07_tokens/build.py first.", file=sys.stderr)
        return 2

    prim, sem, forced = load()
    css = build(prim, sem, forced)
    problems = verify(css, prim, sem, forced)

    if problems:
        print("FAILED — nothing written:\n", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    n_props = len(extract(css))
    print(f"tokens.css  {len(css):>6} bytes  {n_props} custom properties  "
          f"{len(THEMES)} themes  forced-colors + reduced-motion")

    if args.check:
        print("--check: CSS re-parsed and matched against source. Nothing written.")
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tokens.css").write_text(css)
    print(f"Wrote {(OUT / 'tokens.css').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
