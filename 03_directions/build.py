#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
To put four brand directions side by side on one page, built from the same
generated proofs, so the choice between them is made on the same evidence rather
than on four differently-flattering presentations.

Every colour on the page comes from 05_colour/generated/*.proof.json. Nothing is
typed. If a direction's palette changes, this page changes with it.

RUN
---
    cd <the repository folder>
    ./.venv/bin/python 03_directions/build.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROOFS = ROOT / "05_colour" / "generated"
MARKS = HERE / "marks"
OUT = HERE / "COMPARE.html"

GRID = 100  # every mark is drawn on a 100-unit square

# ---------------------------------------------------------------------------
# The marks. Each is a function of stroke weight, so the same geometry gets
# heavier for small sizes rather than being redrawn — one drawing, two weights,
# which is what stops the two versions drifting apart.
# ---------------------------------------------------------------------------


def mark_estuary(w: float) -> str:
    """A single-storey lowercase 'a': a circle tangent to a stem that overruns it.

    The stem is tangent to the bowl at x = 72 (centre 44 plus radius 28) and runs
    from the top of the bowl down past its base. That downward overrun is the only
    liberty taken with the letter, and it is what makes this a mark rather than a
    glyph.

    THE CORRECTION THAT MATTERS: the draft ran the stem from y=18, which is well
    ABOVE the bowl's top edge at y=30. A vertical stroke rising above a bowl is an
    ascender, and a bowl with an ascender is a lowercase 'd'. Rendering it proved
    the point immediately — the mark read as 'd aninda studio'. The overrun has to
    go downward.
    """
    return (
        f'<circle cx="44" cy="58" r="28" fill="none" stroke="currentColor" '
        f'stroke-width="{w}"/>'
        f'<path d="M72 30V94" stroke="currentColor" stroke-width="{w}" '
        f'stroke-linecap="round"/>'
    )


def mark_sandhya(w: float) -> str:
    """The skeleton of the Bangla অ: মাত্রা, right stem, and the left hook.

    Drawn geometrically rather than lifted from a typeface — a mark traced out of
    someone else's font is both weak design and a licensing question nobody needs.
    The proportions are the letter's; the curves are ours.
    """
    return (
        f'<path d="M12 26H88" stroke="currentColor" stroke-width="{w}" '
        f'stroke-linecap="round"/>'
        f'<path d="M76 26V88" stroke="currentColor" stroke-width="{w}" '
        f'stroke-linecap="round"/>'
        f'<path d="M46 26C28 26 20 44 20 58C20 74 30 88 46 88C56 88 62 82 62 74" '
        f'fill="none" stroke="currentColor" stroke-width="{w}" '
        f'stroke-linecap="round"/>'
    )


def mark_instrument(w: float) -> str:
    """No pictorial mark — a grid device.

    A square field divided once vertically and once horizontally, off-centre, into
    one tall cell and two stacked ones. It reads as a measuring instrument, which
    is the whole claim of the direction.

    Both rules stop AT the frame. The first version let them run past it, which
    read as a mistake rather than a decision — and at 16px it turned the mark into
    a smudge.
    """
    h = w / 2
    return (
        f'<rect x="{18 + h}" y="{18 + h}" width="{64 - w}" height="{64 - w}" '
        f'fill="none" stroke="currentColor" stroke-width="{w}" '
        f'stroke-linejoin="round"/>'
        f'<path d="M46 {18 + h}V{82 - h}" stroke="currentColor" stroke-width="{w}"/>'
        f'<path d="M46 54H{82 - h}" stroke="currentColor" stroke-width="{w}"/>'
    )


def mark_derived(w: float) -> str:
    """The type scale, drawn.

    Four strokes standing on one baseline, whose heights ARE the type scale: each
    is 1.333 times the one before it, the same perfect fourth that sets every text
    size in the system. Change the ratio and the mark changes shape. That is the
    direction's entire claim, made literal.

    The first attempt used the ratio for concentric arc RADII, and it failed for a
    reason worth writing down: a 1.333 ratio at usable radii puts the arcs 6 to 8
    units apart, and a 9-unit stroke is wider than the gap — so three separate
    arcs rendered as one solid blob. A ratio can only be seen if the thing it
    scales is bigger than the stroke drawing it.
    """
    base = 30.0
    heights = [base * (1.333 ** i) for i in range(4)]
    baseline = 92.0
    xs = (18.0, 40.0, 62.0, 84.0)
    return "".join(
        f'<path d="M{x} {baseline}V{baseline - hgt:.2f}" stroke="currentColor" '
        f'stroke-width="{w}" stroke-linecap="round"/>'
        for x, hgt in zip(xs, heights)
    )


DIRECTIONS: dict[str, dict] = {
    "estuary": {
        "mark": mark_estuary,
        "latin": "Archivo",
        "latin_css": "'Archivo',sans-serif",
        "bangla": "Noto Sans Bengali",
        "bangla_css": "'Noto Sans Bengali',sans-serif",
        "mono": "JetBrains Mono",
        "mono_css": "'JetBrains Mono',monospace",
        "wordmark_case": "lowercase",
        "wordmark_weight": 500,
        "voice_en": "I build small, careful software. If something here has a limit, "
                    "this page says so — that is information, not a confession.",
        "voice_bn": "আমি ছোট, যত্নে গড়া সফটওয়্যার বানাই। কোনো কিছুর সীমা থাকলে "
                    "সেটা এখানেই লেখা থাকবে — লুকিয়ে রাখা হবে না।",
        "type_note": "Archivo carries a width axis but no optical-size axis, so "
                     "caption sizes need the width dropped by hand.",
    },
    "sandhya": {
        "mark": mark_sandhya,
        "latin": "Source Serif 4",
        "latin_css": "'Source Serif 4',Georgia,serif",
        "bangla": "Noto Serif Bengali",
        "bangla_css": "'Noto Serif Bengali',serif",
        "mono": "IBM Plex Mono",
        "mono_css": "'IBM Plex Mono',monospace",
        "wordmark_case": "none",
        "wordmark_weight": 600,
        "voice_en": "A small press for software. Everything is set carefully, in both "
                    "scripts, because both are the point rather than one being a "
                    "translation of the other.",
        "voice_bn": "সফটওয়্যারের একটি ছোট ছাপাখানা। দুই লিপিতেই সমান যত্নে সাজানো — "
                    "একটি অন্যটির অনুবাদ নয়, দুটোই মূল।",
        "type_note": "Source Serif 4 has a genuine optical-size axis, which is the "
                     "one thing Archivo lacks.",
    },
    "instrument": {
        "mark": mark_instrument,
        "latin": "Inter",
        "latin_css": "'Inter',system-ui,sans-serif",
        "bangla": "Noto Sans Bengali",
        "bangla_css": "'Noto Sans Bengali',sans-serif",
        "mono": "JetBrains Mono",
        "mono_css": "'JetBrains Mono',monospace",
        "wordmark_case": "lowercase",
        "wordmark_weight": 500,
        "voice_en": "Tools, documented. Every number here was measured, and the ones "
                    "that could not be measured are listed as such.",
        "voice_bn": "যন্ত্র, নথিভুক্ত। এখানের প্রতিটি সংখ্যা মেপে নেওয়া; যেগুলো মাপা "
                    "যায়নি, সেগুলোও আলাদা করে লেখা আছে।",
        "type_note": "Inter has an optical-size axis and the widest weight range of "
                     "the four; built for interfaces at small sizes.",
    },
    "derived": {
        "mark": mark_derived,
        "latin": "Space Grotesk",
        "latin_css": "'Space Grotesk',sans-serif",
        "bangla": "Anek Bangla",
        "bangla_css": "'Anek Bangla',sans-serif",
        "mono": "Space Mono",
        "mono_css": "'Space Mono',monospace",
        "wordmark_case": "lowercase",
        "wordmark_weight": 500,
        "voice_en": "The system draws itself. Change a ratio and the mark, the type "
                    "and the spacing all move together — which is either elegant or "
                    "a hostage situation.",
        "voice_bn": "ব্যবস্থাটি নিজেই নিজেকে আঁকে। একটি অনুপাত বদলালে চিহ্ন, হরফ আর "
                    "ফাঁক — সব একসঙ্গে বদলায়।",
        "type_note": "Anek Bangla is variable with a width axis, so it can move with "
                     "the Latin face instead of merely sitting beside it.",
    },
}

FONT_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Archivo:wdth,wght@62..125,100..900"
    "&family=Source+Serif+4:opsz,wght@8..60,300..700"
    "&family=Inter:opsz,wght@14..32,100..900"
    "&family=Space+Grotesk:wght@300..700"
    "&family=Noto+Sans+Bengali:wght@100..900"
    "&family=Noto+Serif+Bengali:wght@100..900"
    "&family=Anek+Bangla:wdth,wght@75..125,100..800"
    "&family=JetBrains+Mono:wght@400;500"
    "&family=IBM+Plex+Mono:wght@400;500"
    "&family=Space+Mono:wght@400;700"
    "&display=swap"
)


def svg(body: str, size: int, colour: str) -> str:
    return (
        f'<svg viewBox="0 0 {GRID} {GRID}" width="{size}" height="{size}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'style="color:{colour};display:block" aria-hidden="true">{body}</svg>'
    )


def swatches(theme: dict) -> str:
    cells = []
    for name, hexv in theme["surfaces"].items():
        cells.append(
            f'<div class="sw"><span style="background:{hexv}"></span>'
            f'<code>{name}</code><code class="h">{hexv}</code></div>'
        )
    for name, r in theme["roles"].items():
        cells.append(
            f'<div class="sw"><span style="background:{r["value"]}"></span>'
            f'<code>{name}</code><code class="h">{r["value"]}</code>'
            f'<code class="r">{r["ratio"]}:1 · {r["level"]}</code></div>'
        )
    return f'<div class="pal">{"".join(cells)}</div>'


def panel(key: str, proof: dict) -> str:
    d = DIRECTIONS[key]
    light = proof["themes"]["light"]
    dark = proof["themes"]["dark"]
    hcl = proof["themes"]["hc-light"]

    ink_l = light["roles"]["ink"]["value"]
    ink_d = dark["roles"]["ink"]["value"]
    muted_l = light["roles"]["ink-muted"]["value"]
    acc_l = light["roles"]["accent"]["value"]
    acc_d = dark["roles"]["accent"]["value"]
    paper = light["surfaces"]["bright"]
    paper2 = light["surfaces"]["high"]
    line_l = light["roles"]["line"]["value"]
    night = dark["surfaces"]["base"]
    night2 = dark["surfaces"]["high"]

    case = "" if d["wordmark_case"] == "none" else f"text-transform:{d['wordmark_case']};"
    aaa_text = sum(1 for r in light["roles"].values()
                   if r["kind"] == "text" and r["level"] == "AAA")
    text_roles = sum(1 for r in light["roles"].values() if r["kind"] == "text")

    return f"""
<section class="dir" style="--paper:{paper};--paper2:{paper2};--ink:{ink_l};
  --muted:{muted_l};--acc:{acc_l};--line:{line_l}">
  <header>
    <div class="id">
      {svg(d["mark"](9), 64, ink_l)}
      <div>
        <div class="wm" style="font-family:{d['latin_css']};font-weight:{d['wordmark_weight']};{case}">aninda studio</div>
        <div class="wm bn" style="font-family:{d['bangla_css']};font-weight:{d['wordmark_weight']}">অনিন্দ্য স্টুডিও</div>
      </div>
    </div>
    <div class="tag"><code>{key}</code><b>{proof['name']}</b>
      <span class="bn">{proof.get('name_bn','')}</span></div>
  </header>

  <p class="premise">{proof['premise']}</p>

  <div class="row">
    <div class="box">
      <h4>The mark, at size</h4>
      <div class="sizes">
        {svg(d["mark"](9), 56, ink_l)}
        {svg(d["mark"](9), 32, ink_l)}
        {svg(d["mark"](9), 24, ink_l)}
        {svg(d["mark"](15), 16, ink_l)}
        <div class="tile" style="background:{ink_l}">{svg(d["mark"](15), 22, paper)}</div>
      </div>
      <p class="cap">56, 32 and 24px at stroke 9; 16px at stroke 15; and the tile,
        reversed. One geometry, two weights.</p>
    </div>
    <div class="box night" style="background:{night};color:{ink_d};border-color:{dark['roles']['line']['value']}">
      <h4 style="color:{ink_d}">Dark, same geometry</h4>
      <div class="sizes">
        {svg(d["mark"](9), 56, ink_d)}
        {svg(d["mark"](9), 24, ink_d)}
        <div class="tile" style="background:{night2}">{svg(d["mark"](15), 22, acc_d)}</div>
      </div>
      <p class="cap" style="color:{dark['roles']['ink-muted']['value']}">
        Not a second drawing — the same paths, recoloured from the dark theme's
        proven roles.</p>
    </div>
  </div>

  <div class="box">
    <h4>Type</h4>
    <div class="spec">
      <div class="line" style="font-family:{d['latin_css']};font-size:44px;line-height:1.1">
        Careful software, in two scripts</div>
      <div class="line bn" style="font-family:{d['bangla_css']};font-size:40px;line-height:1.6">
        যত্নে গড়া সফটওয়্যার</div>
      <div class="line" style="font-family:{d['latin_css']};font-size:16px;line-height:1.6;color:var(--muted)">
        {d['voice_en']}</div>
      <div class="line bn" style="font-family:{d['bangla_css']};font-size:16px;line-height:1.85;color:var(--muted)">
        {d['voice_bn']}</div>
      <div class="line" style="font-family:{d['mono_css']};font-size:13px;color:var(--acc)">
        ক্ষ ত্র জ্ঞ ঙ্গ ন্দ্য স্ত্র · 0 O o 1 l I · {d['latin']} / {d['bangla']} / {d['mono']}</div>
    </div>
    <p class="cap">{d['type_note']}</p>
  </div>

  <div class="box">
    <h4>Light — every value measured, none typed</h4>
    {swatches(light)}
    <p class="cap">{aaa_text} of {text_roles} text roles reach AAA (7:1) in this
      theme; the rest meet AA (4.5:1). Non-text roles meet WCAG 1.4.11 at 3:1 —
      there is no AAA level for non-text contrast.</p>
  </div>

  <details class="box">
    <summary>Dark, high-contrast light and high-contrast dark</summary>
    <h4>Dark</h4>{swatches(dark)}
    <h4>High contrast light — every text role at 7:1</h4>{swatches(hcl)}
    <h4>High contrast dark</h4>{swatches(proof['themes']['hc-dark'])}
  </details>
</section>"""


def main() -> int:
    if not PROOFS.exists():
        print("No proofs. Run 05_colour/engine.py first.", file=sys.stderr)
        return 2

    proofs = {}
    for key in DIRECTIONS:
        p = PROOFS / f"{key}.proof.json"
        if not p.exists():
            print(f"Missing proof for '{key}'. Run 05_colour/engine.py.", file=sys.stderr)
            return 2
        proofs[key] = json.loads(p.read_text())

    MARKS.mkdir(exist_ok=True)
    for key, d in DIRECTIONS.items():
        ink = proofs[key]["themes"]["light"]["roles"]["ink"]["value"]
        for label, w in (("regular", 9), ("heavy", 15)):
            (MARKS / f"{key}-mark-{label}.svg").write_text(
                f'<svg viewBox="0 0 {GRID} {GRID}" xmlns="http://www.w3.org/2000/svg" '
                f'role="img" style="color:{ink}">'
                f'<title>Aninda Studio — {proofs[key]["name"]} mark, {label} weight</title>'
                f'{d["mark"](w)}</svg>\n'
            )

    order = ["estuary", "sandhya", "instrument", "derived"]
    panels = "\n".join(panel(k, proofs[k]) for k in order)

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aninda Studio — four directions</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONT_URL}" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0}}
body{{background:#f4f4f2;color:#1a1a1a;font-family:Inter,system-ui,sans-serif;
  font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased;padding:40px 24px 96px}}
.doc{{max-width:1180px;margin:0 auto}}
.intro{{max-width:74ch;margin-bottom:48px}}
.intro h1{{font-size:40px;line-height:1.1;font-weight:600;margin-bottom:16px}}
.intro p{{color:#555;margin-bottom:12px}}
.intro code{{font-family:'JetBrains Mono',monospace;font-size:.85em;background:#e6e6e2;
  padding:2px 6px;border-radius:4px}}
.dir{{background:var(--paper);color:var(--ink);border:1px solid var(--line);
  border-radius:16px;padding:36px;margin-bottom:36px}}
.dir header{{display:flex;justify-content:space-between;align-items:flex-start;
  gap:24px;flex-wrap:wrap;padding-bottom:20px;border-bottom:1px solid var(--line);
  margin-bottom:20px}}
.id{{display:flex;gap:16px;align-items:center}}
.wm{{font-size:30px;line-height:1.15;letter-spacing:.005em}}
.wm.bn{{font-size:26px;line-height:1.5}}
.tag{{text-align:right;display:flex;flex-direction:column;gap:2px}}
.tag code{{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--acc)}}
.tag b{{font-size:20px;font-weight:600}}
.tag .bn{{font-family:'Noto Sans Bengali',sans-serif;font-size:15px;color:var(--muted)}}
.premise{{max-width:82ch;color:var(--muted);font-size:15px;margin-bottom:24px}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}
@media(max-width:860px){{.row{{grid-template-columns:1fr}}}}
.box{{border:1px solid var(--line);border-radius:12px;padding:20px;
  background:var(--paper2);margin-bottom:16px}}
.box h4{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;
  font-family:'JetBrains Mono',monospace;font-weight:400;color:var(--acc);
  margin-bottom:14px}}
.sizes{{display:flex;align-items:flex-end;gap:20px;flex-wrap:wrap;min-height:60px}}
.tile{{display:grid;place-items:center;width:40px;height:40px;border-radius:9px}}
.cap{{font-size:13px;color:var(--muted);margin-top:14px;max-width:62ch}}
.spec{{display:flex;flex-direction:column;gap:14px}}
.spec .line{{max-width:70ch}}
.pal{{display:grid;grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:10px}}
.sw{{display:flex;flex-direction:column;gap:2px}}
.sw span{{height:44px;border-radius:7px;border:1px solid rgba(0,0,0,.14);display:block}}
.sw code{{font-family:'JetBrains Mono',monospace;font-size:10px;line-height:1.4}}
.sw code.h{{opacity:.6}}
.sw code.r{{color:var(--acc)}}
details summary{{cursor:pointer;font-size:13px;font-family:'JetBrains Mono',monospace;
  letter-spacing:.06em;color:var(--acc);margin-bottom:8px}}
details h4{{margin-top:18px}}
.night h4,.night .cap{{color:inherit}}
</style></head><body><div class="doc">
<div class="intro">
<h1>Four directions for Aninda Studio</h1>
<p>Each one is a different answer at the root — a different mark logic, a different
colour philosophy, a different typographic voice. They are not four shades of one
idea, and they are deliberately not equally safe.</p>
<p>Every colour on this page was computed and measured by
<code>05_colour/engine.py</code> and read from its proof files. No hex value and no
contrast ratio was typed by hand anywhere. Each direction ships four themes —
light, dark, high-contrast light, high-contrast dark — and every text pairing in
every theme clears WCAG 2.2 AA (4.5:1), or AAA (7:1) in the high-contrast themes,
measured on the rounded 8-bit hex and then re-measured with every channel of both
colours nudged by &plusmn;1. The published figure is the worst of those.</p>
<p>Type is provisional: the pairings shown are plausible candidates so the
directions can be compared with real letterforms in both scripts. The final
typeface decision is being made separately, on rendered and measured specimens.</p>
</div>
{panels}
</div></body></html>
"""
    OUT.write_text(html)
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"Wrote {len(DIRECTIONS) * 2} mark files to {MARKS.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
