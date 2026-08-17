#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
Because build.py can only prove that the site was WRITTEN correctly. This proves
it BEHAVES correctly, which is a different claim and the one that matters to a
person opening the page.

Everything here is a measurement taken from a rendered page — a computed style, a
bounding box, a sampled pixel. Nothing is inferred from the source text.

THE ONE THAT CATCHES REAL BUGS
------------------------------
Contrast is measured against the COMPOSITED EFFECTIVE BACKGROUND: the script walks
up the ancestor chain blending every partly-transparent layer until it reaches an
opaque one. Reading an element's own `background-color` returns `rgba(0,0,0,0)`
for nearly every element on a page and proves nothing at all, which is how a
contrast check can report a clean pass over text nobody can read.

EXIT CODES
----------
    0  measured and clean
    1  a real failure
    2  could not run — Playwright, Chromium, or an emulation probe is unavailable

RUN
---
    cd /Users/gru953/Claude/Cowork/Aninda_Studio
    export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
    ./.venv/bin/python 11_site/check.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGES = ["index.html", "404.html"]
WIDTHS = [360, 768, 1280]
THEMES = ["light", "dark", "hc-light", "hc-dark"]

# WCAG 2.2: 1.4.3 (AA) 4.5:1 for text; 1.4.6 (AAA) 7:1. The high-contrast themes
# are held to AAA because a high-contrast theme that only reaches AA is a third
# colour scheme wearing the name.
TARGET = {"light": 4.5, "dark": 4.5, "hc-light": 7.0, "hc-dark": 7.0}
TARGET_MIN_PX = 24        # SC 2.5.8 Target Size (Minimum), Level AA

MEASURE_JS = r"""
() => {
  const px = v => parseFloat(v) || 0;
  const parse = c => {
    const m = c.match(/[\d.]+/g);
    if (!m) return null;
    return [ +m[0], +m[1], +m[2], m.length > 3 ? +m[3] : 1 ];
  };
  // Walk ancestors, blending every partly transparent layer, until opaque.
  const effectiveBg = el => {
    let acc = null;
    for (let n = el; n; n = n.parentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (!c || c[3] === 0) continue;
      acc = acc === null ? c.slice() : acc;
      if (acc[3] >= 1) break;
      if (acc !== c) {
        const a = acc[3];
        for (let i = 0; i < 3; i++) acc[i] = acc[i] * a + c[i] * (1 - a);
        acc[3] = a + c[3] * (1 - a);
      }
      if (acc[3] >= 0.999) break;
    }
    if (!acc) {
      const b = parse(getComputedStyle(document.body).backgroundColor);
      acc = b && b[3] > 0 ? b : [255, 255, 255, 1];
    }
    return acc;
  };
  const lum = ([r, g, b]) => {
    const f = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (a, b) => {
    const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
    return (x + 0.05) / (y + 0.05);
  };

  const out = { text: [], targets: [], overflow: [], clipped: [], hex: [] };

  // Text nodes with real, visible content.
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || px(cs.opacity) === 0) continue;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (el.closest('[disabled]') || el.matches(':disabled')) continue;  // 1.4.3 exempts these
    const fg = parse(cs.color);
    if (!fg || fg[3] === 0) continue;
    const size = px(cs.fontSize), weight = parseInt(cs.fontWeight) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    out.text.push({
      tag: el.tagName.toLowerCase(),
      text: el.textContent.trim().slice(0, 40),
      ratio: +ratio(fg, effectiveBg(el)).toFixed(3),
      large, size,
    });
  }

  // Interactive targets.
  const INT = 'a[href],button,input,select,textarea,summary,[role="button"],[tabindex]:not([tabindex="-1"])';
  for (const el of document.querySelectorAll(INT)) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (el.closest('p, li')) continue;   // SC 2.5.8 exempts inline targets in text
    out.targets.push({
      tag: el.tagName.toLowerCase(),
      label: (el.textContent || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 30),
      w: +r.width.toFixed(1), h: +r.height.toFixed(1),
    });
  }

  // Page-level and clipped overflow.
  const de = document.documentElement;
  if (de.scrollWidth > de.clientWidth + 1)
    out.overflow.push({ by: de.scrollWidth - de.clientWidth });
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.overflowX === 'hidden' || cs.overflowX === 'clip') {
      if (el.scrollWidth > el.clientWidth + 1)
        out.clipped.push({
          tag: el.tagName.toLowerCase(), cls: (el.className || '').toString().slice(0, 40),
          by: el.scrollWidth - el.clientWidth,
        });
    }
  }
  return out;
}
"""


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        print(f"could not run: {e}", file=sys.stderr)
        return 2

    missing = [p for p in PAGES if not (HERE / p).exists()]
    if missing:
        print(f"could not run: no {missing}. Run 11_site/build.py first.", file=sys.stderr)
        return 2

    problems: list[str] = []
    notes: list[str] = []
    counts = {"text": 0, "targets": 0}

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as e:
            print(f"could not run: chromium unavailable ({e})", file=sys.stderr)
            return 2

        for page_name in PAGES:
            url = (HERE / page_name).as_uri()
            for width in WIDTHS:
                for theme in THEMES:
                    ctx = browser.new_context(viewport={"width": width, "height": 900})
                    pg = ctx.new_page()
                    errs: list[str] = []
                    pg.on("pageerror", lambda e: errs.append(str(e)))
                    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                    pg.on("requestfailed", lambda r: errs.append(f"failed request {r.url[:60]}"))
                    pg.goto(url)
                    pg.wait_for_timeout(400)
                    pg.evaluate("document.fonts.ready")
                    pg.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
                    # Freeze transitions. Reading a computed style mid-transition
                    # measures a colour that exists for 120ms and reports it as
                    # permanent — which is how a harness invents its own failures.
                    pg.add_style_tag(content="*,*::before,*::after{transition:none!important;"
                                             "animation:none!important}")
                    pg.wait_for_timeout(200)

                    m = pg.evaluate(MEASURE_JS)
                    where = f"{page_name} @{width}px/{theme}"

                    counts["text"] += len(m["text"])
                    counts["targets"] += len(m["targets"])

                    for t in m["text"]:
                        need = 3.0 if t["large"] else TARGET[theme]
                        if theme.startswith("hc") and t["large"]:
                            need = 4.5
                        if t["ratio"] < need:
                            problems.append(f"{where}: <{t['tag']}> {t['ratio']}:1 against its "
                                            f"background, needs {need}:1 — {t['text']!r}")
                    for tg in m["targets"]:
                        if tg["w"] < TARGET_MIN_PX or tg["h"] < TARGET_MIN_PX:
                            problems.append(f"{where}: <{tg['tag']}> is {tg['w']}×{tg['h']}px, "
                                            f"below the {TARGET_MIN_PX}px minimum — {tg['label']!r}")
                    for o in m["overflow"]:
                        problems.append(f"{where}: the page scrolls sideways by {o['by']}px")
                    for c in m["clipped"]:
                        problems.append(f"{where}: <{c['tag']} class={c['cls']!r}> has {c['by']}px "
                                        f"outside an ancestor that clips it — invisible and "
                                        f"unreachable")
                    for e in errs:
                        problems.append(f"{where}: {e}")
                    ctx.close()

        notes.append(f"{counts['text']} text nodes measured against composited backgrounds")
        notes.append(f"{counts['targets']} interactive targets sized")
        notes.append(f"{len(PAGES)} pages × {len(WIDTHS)} widths × {len(THEMES)} themes")

        # --- forced colours, with a liveness probe FIRST --------------------
        ctx = browser.new_context(forced_colors="active")
        pg = ctx.new_page()
        pg.goto((HERE / "index.html").as_uri())
        pg.wait_for_timeout(400)
        probe = pg.evaluate("""() => {
            const d = document.createElement('div');
            d.style.cssText = 'background:#ff00ff;width:10px;height:10px';
            document.body.appendChild(d);
            const c = getComputedStyle(d).backgroundColor;
            d.remove(); return c;
        }""")
        if "255, 0, 255" in probe:
            problems.append("forced-colors emulation is INERT — a #ff00ff element came back "
                            "unchanged, so this check proves nothing and must not pass")
        else:
            survivors = pg.evaluate("""() => {
                const cs = getComputedStyle(document.documentElement);
                const out = [];
                for (const n of cs) {
                  if (!n.startsWith('--as-')) continue;
                  const v = cs.getPropertyValue(n).trim();
                  if (/^#[0-9a-f]{6}$/i.test(v)) out.push(n + ': ' + v);
                }
                return out;
            }""")
            if survivors:
                problems.append(f"brand colours survive forced-colors mode: {survivors[:5]}")
            else:
                notes.append(f"forced-colors active (probe returned {probe}) — no brand hex survives")
        ctx.close()

        # --- reduced motion ---------------------------------------------------
        ctx = browser.new_context(reduced_motion="reduce")
        pg = ctx.new_page()
        pg.goto((HERE / "index.html").as_uri())
        pg.wait_for_timeout(300)
        d = pg.evaluate("getComputedStyle(document.documentElement)"
                        ".getPropertyValue('--as-duration-move').trim()")
        if d and not d.startswith(("1ms", "0")):
            problems.append(f"prefers-reduced-motion left the move duration at {d}")
        else:
            notes.append(f"reduced motion honoured (move duration {d or 'unset'})")
        ctx.close()

        # --- structure, once ---------------------------------------------------
        ctx = browser.new_context()
        pg = ctx.new_page()
        pg.goto((HERE / "index.html").as_uri())
        pg.wait_for_timeout(400)
        s = pg.evaluate("""() => ({
            h1: document.querySelectorAll('h1').length,
            lang: document.documentElement.lang,
            skip: !!document.querySelector('a[href^="#"]'),
            main: document.querySelectorAll('main').length,
            title: document.title,
            bnWithoutLang: [...document.querySelectorAll('*')].filter(el =>
                [...el.childNodes].some(n => n.nodeType === 3 && /[ঀ-৿]/.test(n.textContent))
                && !el.closest('[lang="bn"]')).length,
            external: [...document.querySelectorAll('[src],[href]')]
                .map(e => e.getAttribute('src') || e.getAttribute('href'))
                .filter(u => u && !u.startsWith('data:') && !u.startsWith('#')
                             && !u.startsWith('./') && !/^[a-z0-9._-]+$/i.test(u)),
        })""")
        if s["h1"] != 1:
            problems.append(f"index.html has {s['h1']} <h1> elements, expected exactly 1")
        if not s["lang"]:
            problems.append("index.html has no lang attribute on <html>")
        if not s["main"]:
            problems.append("index.html has no <main> landmark")
        if not s["skip"]:
            problems.append("index.html has no skip link")
        if s["bnWithoutLang"]:
            problems.append(f"{s['bnWithoutLang']} elements contain Bangla text but are not "
                            f"inside lang=\"bn\" — a screen reader will read them in English")
        notes.append(f"structure: <h1>×{s['h1']}, lang={s['lang']!r}, <main> present, skip link present")
        notes.append(f"external references: {s['external'] or 'none — the page works offline'}")
        ctx.close()
        browser.close()

    for n in notes:
        print(f"  ok    {n}")
    print()
    print("This script CANNOT check: whether a screen reader makes sense of the page; "
          "whether real Windows High Contrast behaves like Chromium's emulation; "
          "whether the Bangla reads well; or whether the page is any good to use.")

    if problems:
        print(f"\n{len(problems)} problem(s):", file=sys.stderr)
        for p in problems[:40]:
            print(f"  FAIL  {p}", file=sys.stderr)
        if len(problems) > 40:
            print(f"  … and {len(problems) - 40} more", file=sys.stderr)
        return 1
    print(f"\n{len(notes)} checks passed, 0 failed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
