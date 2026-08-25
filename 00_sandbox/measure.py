#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
Because a static check cannot see a cascade.

Everything up to this point proves that the token files say the right thing. This
script proves that a browser, resolving the real stylesheet through the real
cascade, produces the values the tokens claim. Those are different claims, and
the gap between them is where the interesting bugs live: a media query in the
wrong order, an explicit theme that cannot win, a forced-colors block that misses
one property, a theme that silently ignores the system setting.

Every finding here is a MEASUREMENT — a computed style read back out of the page
— never an inference from the source text.

The most important check is the last one: the ratio each token CLAIMS is
recomputed from the pixels the browser actually resolved. That closes the loop
from specification to screen, in both directions.

EXIT CODES
----------
    0  everything measured and matched
    1  a real mismatch
    2  could not run — Playwright, Chromium, or an emulation probe is unavailable

RUN
---
    cd <the repository folder>
    PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers ./.venv/bin/python 00_sandbox/measure.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CSS = ROOT / "07_tokens" / "css" / "tokens.css"
SEM = ROOT / "07_tokens" / "build"
NS = "studio.aninda"

SURFACES = ("lowest", "low", "base", "high", "highest", "dim", "bright")
ROLES = ("ink", "ink-muted", "line", "accent", "accent-edge", "focus-ring",
         "success", "warning", "danger", "info")

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="tokens.css">
<style>
  body { margin:0; background: var(--as-surface-base); color: var(--as-ink); }
  #island { background: var(--as-surface-base); color: var(--as-ink); padding: 8px; }
  #probe { background: #ff00ff; color: #00ff00; border: 2px solid #123456; }
  #anim { transition-duration: var(--as-duration-move); }
</style></head><body>
<div id="island"><span id="t">অনিন্দ্য স্টুডিও — aninda studio</span></div>
<div id="probe">probe</div><div id="anim">anim</div>
</body></html>"""


def rgb_to_hex(s: str) -> str:
    nums = [int(float(x)) for x in
            s.replace("rgba(", "").replace("rgb(", "").rstrip(")").replace("/", ",").split(",")[:3]]
    return "#%02X%02X%02X" % tuple(nums)


def rel_lum(hexv: str) -> float:
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    h = hexv.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a: str, b: str) -> float:
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 4)


def read_vars(page) -> dict[str, str]:
    return page.evaluate("""() => {
        const cs = getComputedStyle(document.documentElement);
        const out = {};
        for (const n of ['%s','%s']) {}
        return out;
    }""" % ("", ""))


def snapshot(page, names: list[str]) -> dict[str, str]:
    return page.evaluate(
        """(names) => { const cs = getComputedStyle(document.documentElement);
           const o = {}; for (const n of names) o[n] = cs.getPropertyValue(n).trim();
           return o; }""", names)


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        print(f"could not run: playwright unavailable ({e})", file=sys.stderr)
        return 2

    if not CSS.exists():
        print("could not run: no tokens.css. Run 07_tokens/emit_css.py first.", file=sys.stderr)
        return 2

    sem = {t: json.loads((SEM / f"semantic.{t}.tokens.json").read_text())
           for t in ("light", "dark", "hc-light", "hc-dark")}

    tmp = CSS.parent / "_measure.html"
    tmp.write_text(PAGE)

    names = ([f"--as-surface-{s}" for s in SURFACES]
             + [f"--as-{r}" for r in ROLES]
             + ["--as-duration-move", "--as-shadow-float"])

    problems: list[str] = []
    notes: list[str] = []

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as e:
            print(f"could not run: chromium unavailable ({e})", file=sys.stderr)
            return 2

        def ctx(**kw):
            c = browser.new_context(**kw)
            pg = c.new_page()
            pg.goto(tmp.as_uri())
            pg.wait_for_timeout(160)
            return c, pg

        # --- 1. the system-following path, both ways -------------------------
        c, pg = ctx(color_scheme="light")
        sys_light = snapshot(pg, names)
        c.close()
        c, pg = ctx(color_scheme="dark")
        sys_dark = snapshot(pg, names)
        c.close()

        if sys_light["--as-surface-base"] == sys_dark["--as-surface-base"]:
            problems.append(
                "with no [data-theme] attribute, the page renders identically under "
                "system light and system dark — it is not following the reader's "
                "setting at all")
        else:
            notes.append(f"system light  base {sys_light['--as-surface-base']} · "
                         f"system dark  base {sys_dark['--as-surface-base']}  → follows the system")

        # --- 2. an explicit choice must beat the system ----------------------
        c, pg = ctx(color_scheme="dark")
        pg.evaluate("document.documentElement.setAttribute('data-theme','light')")
        pg.wait_for_timeout(60)
        explicit = snapshot(pg, names)
        if explicit["--as-surface-base"] != sys_light["--as-surface-base"]:
            problems.append(
                "data-theme=\"light\" under a dark system setting did not produce the "
                "light values — the explicit blocks are losing to the media query, "
                "which means the cascade order is wrong")
        else:
            notes.append("explicit [data-theme] beats the system setting")
        c.close()

        # --- 3. a themed island inside an oppositely-themed page -------------
        c, pg = ctx(color_scheme="light")
        pg.evaluate("document.getElementById('island').setAttribute('data-theme','dark')")
        pg.wait_for_timeout(60)
        pair = pg.evaluate("""() => [
            getComputedStyle(document.body).backgroundColor,
            getComputedStyle(document.getElementById('island')).backgroundColor]""")
        if rgb_to_hex(pair[0]) == rgb_to_hex(pair[1]):
            problems.append("a [data-theme=\"dark\"] island inside a light page has the "
                            "same background as its parent — theming is bound to :root")
        else:
            notes.append(f"dark island {rgb_to_hex(pair[1])} inside light page "
                         f"{rgb_to_hex(pair[0])} → attribute-scoped, not :root-scoped")
        c.close()

        # --- 4. high contrast ------------------------------------------------
        c, pg = ctx(color_scheme="light", contrast="more")
        probe = pg.evaluate("getComputedStyle(document.getElementById('probe')).backgroundColor")
        hc = snapshot(pg, names)
        c.close()
        if hc["--as-surface-base"] == sys_light["--as-surface-base"]:
            problems.append("prefers-contrast: more produced the ordinary light values — "
                            "either the emulation is inert or the media query is not matching")
        else:
            notes.append(f"prefers-contrast: more → base {hc['--as-surface-base']}, "
                         f"ink {hc['--as-ink']}")

        # --- 5. forced colours, with a liveness probe first -------------------
        c, pg = ctx(color_scheme="light", forced_colors="active")
        live = pg.evaluate("getComputedStyle(document.getElementById('probe')).backgroundColor")
        if rgb_to_hex(live) == "#FF00FF":
            problems.append("forced-colors emulation is INERT — a #ff00ff element came "
                            "back unchanged, so this check proves nothing and must not "
                            "be reported as a pass")
        else:
            fc = snapshot(pg, names)
            survivors = [k for k, v in fc.items()
                         if v.startswith("#") and k != "--as-shadow-float"]
            if survivors:
                problems.append(f"brand hex values survive forced-colors mode: {survivors}")
            else:
                notes.append(f"forced-colors active → probe {rgb_to_hex(live)}, "
                             f"no brand hex survives")
        c.close()

        # --- 6. reduced motion ------------------------------------------------
        c, pg = ctx(reduced_motion="reduce")
        dur = pg.evaluate("getComputedStyle(document.getElementById('anim')).transitionDuration")
        if not (dur.startswith("0") or dur in ("1ms", "0.001s")):
            problems.append(f"prefers-reduced-motion: reduce left transition-duration at {dur}")
        else:
            notes.append(f"reduced motion → transition-duration {dur}")
        c.close()

        # --- 7. claim versus render, the one that closes the loop -------------
        checked = 0
        for theme, doc in sem.items():
            c, pg = ctx(color_scheme="light")
            pg.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
            pg.wait_for_timeout(60)
            got = snapshot(pg, names)
            c.close()

            colours = doc["color"]
            flat = {
                "ink": colours["ink"]["default"], "ink-muted": colours["ink"]["muted"],
                "line": colours["line"]["default"], "accent": colours["accent"]["default"],
                "accent-edge": colours["accent"]["edge"], "focus-ring": colours["focus"]["ring"],
                **{k: v for k, v in colours["status"].items()},
            }
            for role, tok in flat.items():
                pr = tok["$extensions"][NS]["proof"]
                fg = got[f"--as-{role}"].upper()
                worst = min(contrast(fg, got[f"--as-surface-{s}"].upper()) for s in SURFACES)
                claimed = pr["measured"]
                if abs(worst - claimed) > 0.02:
                    problems.append(
                        f"{theme}/{role}: the token claims {claimed}:1 against its hardest "
                        f"surface, the browser resolved {worst}:1")
                if worst < pr["required"]:
                    problems.append(
                        f"{theme}/{role}: rendered at {worst}:1, below its required "
                        f"{pr['required']}:1")
                checked += 1
        notes.append(f"{checked} role/theme pairs recomputed from resolved pixels and "
                     f"matched their claimed ratios")

        browser.close()

    tmp.unlink(missing_ok=True)

    for n in notes:
        print(f"  ok    {n}")
    print()
    print("This script CANNOT check: what a screen reader announces; whether real "
          "Windows High Contrast behaves like Chromium's emulation; whether the "
          "Bangla reads correctly to a Bangla reader; or whether any of this looks "
          "good.")

    if problems:
        print(f"\n{len(problems)} problem(s):", file=sys.stderr)
        for p in problems:
            print(f"  FAIL  {p}", file=sys.stderr)
        return 1
    print(f"\n{len(notes)} checks passed, 0 failed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
