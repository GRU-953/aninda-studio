#!/usr/bin/env python3
"""Aninda Studio — the card check harness. It measures; it does not assert.

    export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
    ./.venv/bin/python 08_components/check.py [--only SLUG] [--widths 360,1280]

Every card is opened in a real Chromium at three widths and in all four themes,
and then MEASURED. The distinction matters. A static reading of the CSS can tell
you a rule exists; it cannot tell you whether the rule reached the pixel. So:

  * Contrast is read off the composited effective background, walking ancestors
    and blending partly-transparent layers. Reading an element's own
    background-color returns rgba(0, 0, 0, 0) for nearly every element in a real
    page and proves nothing at all.
  * Interaction states are driven by a real pointer — move, down, up — and the
    :active computed style is compared against the :hover one. Two identical
    readings are what a dead :active rule looks like from outside the browser.
  * The focus indicator is measured from pixels: the padded element is captured
    unfocused and focused, the two buffers are differenced, and the changed
    pixels are checked for a ring at least 2 CSS px thick at 3:1 contrast.
  * Forced colours run a liveness probe first. If the emulation is inert the run
    FAILS as not-equipped rather than passing silently, which is the failure mode
    that matters: a check that cannot fail is not a check.

Exit codes
    0  everything measured passed
    1  a real failure
    2  could not run — a tool or an emulation is missing

The harness prints what it could NOT check at the end. That list is part of the
result, not an apology.

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import argparse
import io as _io
import json
import sys
import time
from pathlib import Path

try:
    from PIL import Image, ImageChops
except ImportError:  # measured from pixels, so this is not optional
    Image = None
    ImageChops = None

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "_cards.json"

WIDTHS = [360, 768, 1280]
INTERACTION_WIDTH = 1280
THEMES = ["light", "dark", "hc-light", "hc-dark"]
HC_THEMES = {"hc-light", "hc-dark"}

TEXT_MIN = 4.5
TEXT_MIN_HC = 7.0
NON_TEXT_MIN = 3.0
TARGET_MIN = 24.0
RING_MIN_PX = 2

INTERACTIVE = (
    "a[href], button, input:not([type='hidden']), select, textarea, summary, "
    "[tabindex]:not([tabindex='-1']), [role='button'], [role='tab'], [role='link'], "
    "[role='checkbox'], [role='radio'], [role='switch']"
)

COMPARED_PROPS = [
    "background-color", "background-image", "color",
    "border-top-color", "border-right-color", "border-bottom-color", "border-left-color",
    "border-top-width", "border-right-width", "border-bottom-width", "border-left-width",
    "box-shadow", "outline-color", "outline-width", "outline-style",
    "opacity", "transform", "translate", "scale", "filter",
    "text-decoration-line", "text-decoration-color", "font-weight",
]

MEASURE_JS = r"""
window.__as = (function () {
  function parseColour(value) {
    if (!value) return null;
    var s = String(value).trim();
    if (s === 'transparent') return { r: 0, g: 0, b: 0, a: 0 };
    var m = s.match(/^rgba?\(([^)]+)\)$/);
    if (m) {
      var p = m[1].split(/[,\s\/]+/).filter(function (x) { return x.length; }).map(parseFloat);
      return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
    }
    m = s.match(/^color\(srgb\s+([^)]+)\)$/);
    if (m) {
      var q = m[1].split(/[\s\/]+/).filter(function (x) { return x.length; }).map(parseFloat);
      return { r: q[0] * 255, g: q[1] * 255, b: q[2] * 255, a: q.length > 3 ? q[3] : 1 };
    }
    return null;
  }

  function over(top, bottom) {
    var a = top.a;
    return {
      r: top.r * a + bottom.r * (1 - a),
      g: top.g * a + bottom.g * (1 - a),
      b: top.b * a + bottom.b * (1 - a),
      a: 1
    };
  }

  function channel(v) {
    var c = v / 255;
    return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  }

  function luminance(c) {
    return 0.2126 * channel(c.r) + 0.7152 * channel(c.g) + 0.0722 * channel(c.b);
  }

  function contrast(a, b) {
    var la = luminance(a), lb = luminance(b);
    var hi = Math.max(la, lb), lo = Math.min(la, lb);
    return (hi + 0.05) / (lo + 0.05);
  }

  /* The whole point. An element's own background-color is rgba(0,0,0,0) for
     nearly everything on a real page, so the background text actually sits on
     has to be composited from the ancestors that do paint. Element opacity is
     folded into the alpha, which is an approximation of what the compositor
     does with a group, and it is named as such in the report. */
  function effectiveBackground(el) {
    var layers = [];
    var node = el;
    var opacity = 1;
    while (node && node.nodeType === 1) {
      var cs = getComputedStyle(node);
      var own = parseFloat(cs.opacity);
      if (!isNaN(own)) opacity *= own;
      if (cs.backgroundImage && cs.backgroundImage !== 'none') {
        return { error: 'background-image on ' + describe(node) };
      }
      var colour = parseColour(cs.backgroundColor);
      if (!colour) return { error: 'unparsed background ' + cs.backgroundColor };
      var effective = { r: colour.r, g: colour.g, b: colour.b, a: colour.a * opacity };
      if (effective.a > 0) layers.push(effective);
      if (effective.a >= 0.999) break;
      node = node.parentElement;
    }
    if (!layers.length || layers[layers.length - 1].a < 0.999) {
      return { error: 'no opaque background anywhere up the tree' };
    }
    var result = layers[layers.length - 1];
    for (var i = layers.length - 2; i >= 0; i--) result = over(layers[i], result);
    return { colour: result };
  }

  function describe(el) {
    if (!el || el.nodeType !== 1) return '?';
    var out = el.tagName.toLowerCase();
    if (el.id) out += '#' + el.id;
    if (el.className && typeof el.className === 'string') {
      out += '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.');
    }
    return out;
  }

  function path(el) {
    var parts = [];
    var node = el;
    while (node && node.nodeType === 1 && parts.length < 5) {
      parts.unshift(describe(node));
      node = node.parentElement;
    }
    return parts.join(' > ');
  }

  function visible(el) {
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility !== 'visible') return false;
    if (parseFloat(cs.opacity) === 0) return false;
    var r = el.getBoundingClientRect();
    return r.width >= 1 && r.height >= 1;
  }

  function themeOf(el) {
    var holder = el.closest ? el.closest('[data-theme]') : null;
    return holder ? holder.getAttribute('data-theme') : '';
  }

  function measureText(hcThemes, floorNormal, floorHc) {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
    var skip = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEMPLATE: 1, TITLE: 1 };
    var failures = [];
    var problems = [];
    var counted = 0;
    var worst = { ratio: Infinity, where: '' };
    var node;
    while ((node = walker.nextNode())) {
      var text = node.nodeValue;
      if (!text || !text.trim()) continue;
      var el = node.parentElement;
      if (!el || skip[el.tagName]) continue;
      if (!visible(el)) continue;
      var cs = getComputedStyle(el);
      var fg = parseColour(cs.color);
      if (!fg) { problems.push('unparsed colour ' + cs.color + ' at ' + path(el)); continue; }
      var bg = effectiveBackground(el);
      if (bg.error) { problems.push(bg.error + ' at ' + path(el)); continue; }
      var composited = fg.a >= 0.999 ? fg : over(fg, bg.colour);
      var ratio = contrast(composited, bg.colour);
      counted++;
      var theme = themeOf(el);
      var need = hcThemes.indexOf(theme) >= 0 ? floorHc : floorNormal;
      if (ratio < worst.ratio) { worst = { ratio: ratio, where: path(el) }; }
      if (ratio + 0.0005 < need) {
        failures.push({
          ratio: Math.round(ratio * 100) / 100,
          need: need,
          theme: theme,
          text: text.trim().slice(0, 48),
          path: path(el),
          fontSize: cs.fontSize,
          fontWeight: cs.fontWeight
        });
      }
    }
    return { counted: counted, failures: failures, problems: problems, worst: worst };
  }

  function measureOverflow() {
    var de = document.documentElement;
    var clipped = [];
    var all = document.querySelectorAll('body *');
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      if (el.clientWidth < 2 || el.clientHeight < 2) continue;
      if (el.scrollWidth - el.clientWidth <= 1) continue;
      var own = getComputedStyle(el).overflowX;
      if (own === 'auto' || own === 'scroll') continue;
      if (own === 'hidden' || own === 'clip') {
        clipped.push({ path: path(el), by: 'itself', over: el.scrollWidth - el.clientWidth });
        continue;
      }
      var a = el.parentElement;
      while (a && a.nodeType === 1) {
        var o = getComputedStyle(a).overflowX;
        if (o !== 'visible') {
          if (o === 'hidden' || o === 'clip') {
            clipped.push({ path: path(el), by: path(a), over: el.scrollWidth - el.clientWidth });
          }
          break;
        }
        a = a.parentElement;
      }
    }
    return {
      page: de.scrollWidth - de.clientWidth,
      scrollWidth: de.scrollWidth,
      clientWidth: de.clientWidth,
      clipped: clipped
    };
  }

  function measureTargets(selector, minSize) {
    var small = [];
    var counted = 0;
    var nodes = document.querySelectorAll(selector);
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.disabled) continue;
      if (!visible(el)) continue;
      var r = el.getBoundingClientRect();
      counted++;
      if (r.width + 0.5 < minSize || r.height + 0.5 < minSize) {
        small.push({
          path: path(el),
          width: Math.round(r.width * 10) / 10,
          height: Math.round(r.height * 10) / 10,
          text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 40)
        });
      }
    }
    return { counted: counted, small: small };
  }

  function styleOf(el, props) {
    var cs = getComputedStyle(el);
    var out = {};
    for (var i = 0; i < props.length; i++) out[props[i]] = cs.getPropertyValue(props[i]);
    return out;
  }

  function hitTest(el, x, y) {
    var found = document.elementFromPoint(x, y);
    if (!found) return false;
    return found === el || el.contains(found) || found.contains(el);
  }

  function probeForcedColours() {
    var probe = document.createElement('div');
    probe.id = '__as_forced_probe';
    probe.textContent = 'probe';
    probe.style.color = 'rgb(255, 0, 255)';
    probe.style.backgroundColor = 'rgb(0, 255, 0)';
    probe.style.position = 'fixed';
    probe.style.left = '-9999px';
    document.body.appendChild(probe);
    var cs = getComputedStyle(probe);
    var out = { colour: cs.color, background: cs.backgroundColor };
    probe.remove();
    out.live = out.colour !== 'rgb(255, 0, 255)' || out.background !== 'rgb(0, 255, 0)';
    return out;
  }

  function tokenValues(names) {
    var cs = getComputedStyle(document.documentElement);
    var out = {};
    for (var i = 0; i < names.length; i++) out[names[i]] = cs.getPropertyValue(names[i]).trim();
    return out;
  }

  function setTheme(value) {
    if (value) document.documentElement.setAttribute('data-theme', value);
    else document.documentElement.removeAttribute('data-theme');
  }

  function freeze(on) {
    var id = '__as_freeze';
    var existing = document.getElementById(id);
    if (existing) existing.remove();
    if (!on) return;
    var style = document.createElement('style');
    style.id = id;
    style.textContent = '*, *::before, *::after { transition: none !important;' +
      ' caret-color: transparent !important; }';
    document.head.appendChild(style);
  }

  return {
    measureText: measureText,
    measureOverflow: measureOverflow,
    measureTargets: measureTargets,
    styleOf: styleOf,
    hitTest: hitTest,
    probeForcedColours: probeForcedColours,
    tokenValues: tokenValues,
    setTheme: setTheme,
    freeze: freeze,
    describe: describe,
    path: path,
    visible: visible
  };
})();
"""

CANNOT_CHECK = [
    "Whether a colour means the right thing. The harness proves a badge is "
    "readable; it cannot prove that 'Failed' is the honest word for what happened.",
    "Whether the markup carries a word and a glyph beside every colour. That is "
    "the third rule of the component layer and no measurement reaches it.",
    "Overlap. The background walk climbs ancestors, so text sitting over an "
    "absolutely positioned sibling is measured against the ancestor, not the "
    "sibling. Nothing in these cards does that, which is why the walk is enough here.",
    "Element opacity is folded into the layer alpha. That approximates what the "
    "compositor does with a group and is exact only when the group paints one layer.",
    "Screen readers. Roles, names and the order things are announced in are "
    "asserted in the markup and were not measured by any assistive technology.",
    "Keyboard order beyond the fact that focus can land. Tab order, focus "
    "trapping in a dialog and Escape handling are not exercised.",
    "Any browser other than the pinned Chromium, and any platform other than "
    "macOS. Safari, Firefox and Windows high contrast were not run.",
    "Real reading. Nobody in either script was asked whether these cards are "
    "actually comfortable to read.",
    "Print, and any resolution other than device_scale_factor 1.",
    "WCAG 2.2 SC 2.5.8 has exceptions — inline targets, targets whose spacing "
    "already gives them a 24 px circle, and ones the browser draws. The harness "
    "applies none of them: every interactive element is 24×24 or it fails. That "
    "is stricter than the criterion, which is the safe direction to be wrong in.",
    "The press test compares a fixed list of computed properties. A :active rule "
    "that changed only some property outside that list would read as dead here.",
    "Mid-transition states. Transitions are frozen for the whole run, so every "
    "reading is of a resting state. A colour that dips below its floor for 60 ms "
    "on its way somewhere would not be seen here.",
    "The four themes inside the quad panels are not driven by a pointer. "
    "Interaction and focus are measured on the primary stage, where every "
    "distinct control appears once, in all four page themes.",
]


class Findings:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.notes: list[str] = []

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


def srgb_luminance(rgb) -> float:
    def ch(v):
        c = v / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(rgb[0]) + 0.7152 * ch(rgb[1]) + 0.0722 * ch(rgb[2])


def ratio(a, b) -> float:
    la, lb = srgb_luminance(a), srgb_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def ring_from_diff(before, after):
    """Diff two buffers of the same padded element and describe the ring."""
    if before.size != after.size:
        return {"error": f"buffer sizes differ, {before.size} against {after.size}"}
    a = before.convert("RGB")
    b = after.convert("RGB")
    diff = ImageChops.difference(a, b)
    w, h = diff.size
    px = diff.load()
    changed = [[False] * w for _ in range(h)]
    minx, miny, maxx, maxy = w, h, -1, -1
    count = 0
    for y in range(h):
        row = changed[y]
        for x in range(w):
            r, g, bl = px[x, y]
            if r > 12 or g > 12 or bl > 12:
                row[x] = True
                count += 1
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    if count == 0:
        return {"error": "focusing the element changed no pixel at all"}

    midy = (miny + maxy) // 2
    midx = (minx + maxx) // 2

    def run(get, start, step, limit):
        n = 0
        i = start
        while 0 <= i < limit and get(i):
            n += 1
            i += step
        return n

    left = run(lambda x: changed[midy][x], minx, 1, w)
    right = run(lambda x: changed[midy][x], maxx, -1, w)
    top = run(lambda y: changed[y][midx], miny, 1, h)
    bottom = run(lambda y: changed[y][midx], maxy, -1, h)
    thickness = min(left, right, top, bottom)

    samples = []
    if left:
        samples.append((minx + left // 2, midy))
    if right:
        samples.append((maxx - right // 2, midy))
    if top:
        samples.append((midx, miny + top // 2))
    if bottom:
        samples.append((midx, maxy - bottom // 2))

    apx = a.load()
    bpx = b.load()
    contrasts = [ratio(apx[x, y], bpx[x, y]) for x, y in samples]
    return {
        "thickness": thickness,
        "sides": [left, right, top, bottom],
        "contrast": min(contrasts) if contrasts else 0.0,
        "changed": count,
        "box": [minx, miny, maxx, maxy],
    }


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--only", default="", help="Check one card by slug.")
    parser.add_argument("--widths", default=",".join(str(w) for w in WIDTHS))
    parser.add_argument("--skip-interaction", action="store_true")
    parser.add_argument("--json", default="", help="Write the full report here.")
    args = parser.parse_args(argv)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("NOT EQUIPPED: playwright is not importable.", file=sys.stderr)
        return 2
    if Image is None:
        print("NOT EQUIPPED: Pillow is not importable, so the focus ring cannot "
              "be measured from pixels.", file=sys.stderr)
        return 2

    if not REGISTRY.exists():
        print(f"NOT EQUIPPED: {REGISTRY} is missing. Run build.py first.", file=sys.stderr)
        return 2

    registry = json.loads(REGISTRY.read_text("utf-8"))
    cards = registry["cards"]
    if args.only:
        cards = [c for c in cards if c["path"].endswith(f"/{args.only}.html")]
        if not cards:
            print(f"NOT EQUIPPED: no card with slug {args.only!r}.", file=sys.stderr)
            return 2

    widths = [int(w) for w in args.widths.split(",") if w.strip()]
    found = Findings()
    report: dict = {"failures": [], "notes": []}
    started = time.time()

    try:
        pw = sync_playwright().start()
    except Exception as exc:
        print(f"NOT EQUIPPED: playwright would not start — {exc}", file=sys.stderr)
        return 2

    try:
        try:
            browser = pw.chromium.launch()
        except Exception as exc:
            print("NOT EQUIPPED: Chromium would not launch. Did you export "
                  f"PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers ?\n  {exc}", file=sys.stderr)
            return 2

        text_nodes_seen = 0
        targets_seen = 0
        elements_interacted = 0
        rings_measured = 0
        forced_pages = 0

        for width in widths:
            context = browser.new_context(
                viewport={"width": width, "height": 900},
                device_scale_factor=1,
                reduced_motion="no-preference",
            )
            context.add_init_script(MEASURE_JS)
            page = context.new_page()

            console: list[str] = []
            page.on("console", lambda m: console.append(f"{m.type}: {m.text}")
                    if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e: console.append(f"pageerror: {e}"))
            page.on("requestfailed", lambda r: console.append(
                f"requestfailed: {r.url} — {r.failure}"))

            for card in cards:
                slug = Path(card["path"]).stem
                url = (HERE / card["path"]).resolve().as_uri()
                console.clear()
                page.goto(url, wait_until="load")
                # Transitions are frozen for the whole run. Switching the theme
                # starts a 120 ms colour transition on every control, and reading
                # the computed style mid-flight measures a colour that is on its
                # way somewhere rather than the one the design specifies.
                page.evaluate("() => window.__as.freeze(true)")
                page.wait_for_timeout(60)

                # The @dsCard contract puts two comments in front of the doctype.
                # The parser is supposed to keep standards mode across those, and
                # "supposed to" is exactly the kind of claim worth measuring: in
                # quirks mode the box model changes and every width here is wrong.
                mode = page.evaluate("() => document.compatMode")
                if mode != "CSS1Compat":
                    found.fail(
                        f"{slug} @{width}: document.compatMode is {mode!r}, not "
                        "'CSS1Compat'. The comments before the doctype have dropped "
                        "the page into quirks mode."
                    )

                for theme in THEMES:
                    page.evaluate("t => window.__as.setTheme(t)", theme)
                    page.wait_for_timeout(30)
                    label = f"{slug} @{width} [{theme}]"

                    over = page.evaluate("() => window.__as.measureOverflow()")
                    if over["page"] > 1:
                        found.fail(
                            f"{label}: the page scrolls sideways by {over['page']} px "
                            f"({over['scrollWidth']} against {over['clientWidth']})."
                        )
                    for item in over["clipped"]:
                        found.fail(
                            f"{label}: {item['path']} overflows by {item['over']} px and is "
                            f"clipped by {item['by']}. A static read of the CSS cannot see this."
                        )

                    text = page.evaluate(
                        "a => window.__as.measureText(a[0], a[1], a[2])",
                        [list(HC_THEMES), TEXT_MIN, TEXT_MIN_HC],
                    )
                    text_nodes_seen += text["counted"]
                    for fail in text["failures"]:
                        found.fail(
                            f"{label}: contrast {fail['ratio']}:1 against a composited "
                            f"background, needs {fail['need']}:1 — {fail['path']} "
                            f"({fail['fontSize']}/{fail['fontWeight']}) \"{fail['text']}\""
                        )
                    for problem in text["problems"]:
                        found.fail(f"{label}: could not measure a background — {problem}")

                    targets = page.evaluate(
                        "a => window.__as.measureTargets(a[0], a[1])", [INTERACTIVE, TARGET_MIN]
                    )
                    targets_seen += targets["counted"]
                    for small in targets["small"]:
                        found.fail(
                            f"{label}: target {small['width']}×{small['height']} px is under "
                            f"{TARGET_MIN:.0f}×{TARGET_MIN:.0f} (WCAG 2.2 SC 2.5.8) — "
                            f"{small['path']} \"{small['text']}\""
                        )

                if width == INTERACTION_WIDTH and not args.skip_interaction:
                    for theme in THEMES:
                        page.evaluate("t => window.__as.setTheme(t)", theme)
                        page.wait_for_timeout(30)
                        label = f"{slug} @{width} [{theme}]"
                        did, rings = check_interaction(page, label, found)
                        elements_interacted += did
                        rings_measured += rings

                for line in console:
                    found.fail(f"{slug} @{width}: console — {line}")
                console.clear()

            page.close()
            context.close()

        # ---- forced colours -------------------------------------------------
        context = browser.new_context(
            viewport={"width": INTERACTION_WIDTH, "height": 900}, device_scale_factor=1
        )
        context.add_init_script(MEASURE_JS)
        page = context.new_page()
        try:
            page.emulate_media(forced_colors="active", color_scheme="light")
        except Exception as exc:
            print(f"NOT EQUIPPED: this Playwright cannot emulate forced colours — {exc}",
                  file=sys.stderr)
            return 2

        page.goto((HERE / cards[0]["path"]).resolve().as_uri(), wait_until="load")
        probe = page.evaluate("() => window.__as.probeForcedColours()")
        if not probe["live"]:
            print(
                "NOT EQUIPPED: the forced-colours emulation is inert. A probe set to "
                f"magenta on green came back as {probe['colour']} on {probe['background']}, "
                "unchanged. Passing this check would prove nothing, so it fails as "
                "not-equipped instead.",
                file=sys.stderr,
            )
            return 2

        for card in cards:
            slug = Path(card["path"]).stem
            page.goto((HERE / card["path"]).resolve().as_uri(), wait_until="load")
            page.evaluate("() => window.__as.freeze(true)")
            page.wait_for_timeout(40)
            forced_pages += 1
            for theme in THEMES:
                page.evaluate("t => window.__as.setTheme(t)", theme)
                page.wait_for_timeout(20)
                label = f"{slug} forced-colors [{theme}]"
                tokens = page.evaluate(
                    "n => window.__as.tokenValues(n)",
                    ["--as-surface-base", "--as-ink", "--as-focus-ring"],
                )
                if tokens["--as-surface-base"].lower() != "canvas":
                    found.fail(
                        f"{label}: --as-surface-base is {tokens['--as-surface-base']!r}, "
                        "not Canvas. A brand colour that survives forced colours defeats it."
                    )
                over = page.evaluate("() => window.__as.measureOverflow()")
                if over["page"] > 1:
                    found.fail(f"{label}: the page scrolls sideways by {over['page']} px.")
                text = page.evaluate(
                    "a => window.__as.measureText(a[0], a[1], a[2])",
                    [[], NON_TEXT_MIN, NON_TEXT_MIN],
                )
                for fail in text["failures"]:
                    found.fail(
                        f"{label}: contrast {fail['ratio']}:1 in the system palette — "
                        f"{fail['path']} \"{fail['text']}\""
                    )
        page.close()
        context.close()
        browser.close()
    finally:
        pw.stop()

    elapsed = time.time() - started
    report["failures"] = found.failures
    report["notes"] = found.notes
    report["measured"] = {
        "cards": len(cards),
        "widths": widths,
        "themes": THEMES,
        "text_nodes": text_nodes_seen,
        "targets": targets_seen,
        "elements_pointer_driven": elements_interacted,
        "focus_rings_measured": rings_measured,
        "forced_colours_pages": forced_pages,
        "seconds": round(elapsed, 1),
    }

    print("=" * 72)
    print("Aninda Studio — card check")
    print("=" * 72)
    print(f"Cards {len(cards)} · widths {widths} · themes {THEMES}")
    print(f"Measured: {text_nodes_seen} text nodes, {targets_seen} targets, "
          f"{elements_interacted} pointer-driven controls, "
          f"{rings_measured} focus rings, {forced_pages} forced-colour pages.")
    print(f"Took {elapsed:.0f} s.")
    print()

    if found.notes:
        print(f"Could not measure ({len(found.notes)}):")
        for note in found.notes:
            print(f"  · {note}")
        print()

    print("What this harness CANNOT check:")
    for line in CANNOT_CHECK:
        print(f"  · {line}")
    print()

    if found.failures:
        print(f"FAILURES ({len(found.failures)}):")
        for line in found.failures:
            print(f"  ✗ {line}")
        code = 1
    else:
        print("PASS — every measurement above met its floor.")
        code = 0

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2, ensure_ascii=False), "utf-8")

    return code


def place(page, handle, viewport, pad: int, tries: int = 3):
    """Scroll until the element and its padding are both inside the viewport, so
    a padded capture is possible and the pointer lands where it is aimed."""
    for _ in range(tries):
        box = handle.bounding_box()
        if not box or box["width"] < 1 or box["height"] < 1:
            return None
        top = box["y"] - pad
        bottom = box["y"] + box["height"] + pad
        if box["x"] - pad < 0 or box["x"] + box["width"] + pad > viewport["width"]:
            return None
        if box["height"] + pad * 2 > viewport["height"]:
            return None
        if top >= 0 and bottom <= viewport["height"]:
            return box
        delta = top - pad * 2 if top < 0 else bottom - viewport["height"] + pad * 2
        page.evaluate("d => window.scrollBy(0, d)", delta)
        page.wait_for_timeout(20)
    return None


def check_interaction(page, label: str, found: Findings) -> tuple[int, int]:
    """Drive a real pointer over every control on the stage, then measure the
    focus ring from pixels."""
    handles = page.query_selector_all(f".as-doc-stage :is({INTERACTIVE})")
    viewport = page.viewport_size
    pad = 8
    did = 0
    rings = 0

    for handle in handles:
        try:
            if handle.is_disabled():
                continue
        except Exception:
            pass
        if not handle.evaluate("el => window.__as.visible(el)"):
            continue
        described = handle.evaluate("el => window.__as.path(el)")
        tag = handle.evaluate("el => el.tagName.toLowerCase()")

        try:
            handle.scroll_into_view_if_needed(timeout=2000)
        except Exception:
            found.note(f"{label}: {described} would not scroll into view.")
            continue
        box = place(page, handle, viewport, pad)
        if not box:
            found.note(f"{label}: {described} would not sit far enough from the viewport "
                       f"edge for a {pad} px padded capture, so it was not measured.")
            continue

        cx = box["x"] + box["width"] / 2
        cy = box["y"] + box["height"] / 2
        if not (0 <= cx <= viewport["width"] and 0 <= cy <= viewport["height"]):
            found.note(f"{label}: {described} is outside the viewport, so the pointer "
                       "could not reach it.")
            continue
        if not handle.evaluate("(el, xy) => window.__as.hitTest(el, xy[0], xy[1])", [cx, cy]):
            found.note(f"{label}: {described} is not the topmost element at its own centre, "
                       "so a pointer press would land somewhere else.")
            continue

        # ---- :hover against :active, with a real pointer ----
        page.mouse.move(cx, cy)
        page.mouse.down()
        page.mouse.up()
        if tag == "select":
            page.keyboard.press("Escape")
        page.mouse.move(cx, cy)
        page.wait_for_timeout(25)
        hover = handle.evaluate("(el, p) => window.__as.styleOf(el, p)", COMPARED_PROPS)
        page.mouse.down()
        page.wait_for_timeout(25)
        active = handle.evaluate("(el, p) => window.__as.styleOf(el, p)", COMPARED_PROPS)
        page.mouse.up()
        if tag == "select":
            page.keyboard.press("Escape")
        page.mouse.move(0, 0)
        page.wait_for_timeout(15)
        did += 1

        if hover == active:
            found.fail(
                f"{label}: {described} looks identical while pressed and while hovered. "
                "That is what a dead :active rule looks like from outside the browser."
            )

        # ---- focus ring, measured from pixels ----
        page.evaluate("() => { if (document.activeElement) document.activeElement.blur(); }")
        page.wait_for_timeout(15)
        box = place(page, handle, viewport, pad)
        if not box:
            found.note(f"{label}: {described} would not sit far enough from the viewport "
                       f"edge for a {pad} px padded capture, so its focus ring was not measured.")
            continue
        clip = {
            "x": box["x"] - pad,
            "y": box["y"] - pad,
            "width": box["width"] + pad * 2,
            "height": box["height"] + pad * 2,
        }

        before = Image.open(_io.BytesIO(page.screenshot(clip=clip)))
        handle.evaluate("el => el.focus()")
        page.wait_for_timeout(25)
        after = Image.open(_io.BytesIO(page.screenshot(clip=clip)))
        page.evaluate("() => { if (document.activeElement) document.activeElement.blur(); }")
        page.wait_for_timeout(10)

        result = ring_from_diff(before, after)
        rings += 1
        if "error" in result:
            found.fail(f"{label}: {described} — {result['error']}. Focus must always be visible.")
            continue
        if result["thickness"] < RING_MIN_PX:
            found.fail(
                f"{label}: {described} focus ring measures {result['thickness']} px at its "
                f"thinnest (sides {result['sides']}), under the {RING_MIN_PX} px floor."
            )
        if result["contrast"] < NON_TEXT_MIN:
            found.fail(
                f"{label}: {described} focus ring contrasts {result['contrast']:.2f}:1 with "
                f"what it covers, under {NON_TEXT_MIN}:1."
            )

    return did, rings


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
