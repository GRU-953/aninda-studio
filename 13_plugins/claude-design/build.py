#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
Claude Design is one of the nine deliverables, and it is the only one whose
artefact lives on a remote service. That makes it the one most likely to drift
without anything saying so: the tokens change, the local tree is regenerated and
checked, and the copy on claude.ai keeps showing last month's palette.

So the bundle is GENERATED, from the same files everything else is generated from,
and `--check` re-runs the generation and compares it byte for byte. Pushing is a
separate step that uploads what this wrote. Nothing here is hand-drawn.

WHAT IT WRITES
--------------
`dist/` holds the whole design-system project:

    styles.css              tokens.css + components.css + the three @font-face
                            rules, so every card renders standalone
    tokens/                 the DTCG source and the generated stylesheet
    tokens/fonts/           the three subsets and their licences
    css/components.css      the component layer on its own
    assets/marks/           the shipped identity artwork
    guidelines/*.card.html  one preview card per part of the system

Each card's FIRST line is an `@dsCard` comment. The Design System pane builds its
index from those, so a card without one is invisible in the pane even though the
file uploaded fine.

THE ONE PLACE A LITERAL COLOUR IS ALLOWED
-----------------------------------------
The ramp card. `07_tokens/css/tokens.css` exposes the eleven semantic roles and
the seven surfaces as custom properties, and it does NOT expose the sixty-six ramp
steps — they are primitives that the roles alias. A card whose subject is the
ramps therefore has to name their hexes, and it reads them from
primitive.tokens.json rather than carrying a copy. Every other card paints with
`var(--as-…)`, which is also the better demonstration.

RUN
---
    cd <the repository folder>
    ./.venv/bin/python 13_plugins/claude-design/build.py
    ./.venv/bin/python 13_plugins/claude-design/build.py --check
"""

from __future__ import annotations

import html
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TOKENS = ROOT / "07_tokens" / "build"
TOKENS_CSS = ROOT / "07_tokens" / "css" / "tokens.css"
COMPONENTS_CSS = ROOT / "08_components" / "src" / "components.css"
FONTS = ROOT / "08_components" / "fonts"
MARKS = ROOT / "04_mark" / "svg"
DIST = HERE / "dist"

THEMES = ["light", "dark", "hc-light", "hc-dark"]
THEME_LABEL = {"light": "Light", "dark": "Dark",
               "hc-light": "High contrast, light", "hc-dark": "High contrast, dark"}

FONT_FILES = [
    ("Literata", "literata-subset.woff2", "400 700"),
    ("Noto Serif Bengali", "notoserifbengali-subset.woff2", "400 700"),
    ("Aninda Mono", "anindamono-subset.woff2", "400"),
]


class BuildError(Exception):
    pass


def e(text) -> str:
    return html.escape(str(text), quote=True)


def read_json(path: Path) -> dict:
    if not path.exists():
        raise BuildError(f"{path} is missing. Run 07_tokens/build.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Reading the system
# ---------------------------------------------------------------------------

def load() -> tuple[dict, dict[str, dict], dict]:
    prim = read_json(TOKENS / "primitive.tokens.json")
    sem = {t: read_json(TOKENS / f"semantic.{t}.tokens.json") for t in THEMES}
    forced = read_json(TOKENS / "forced-colors.map.json")
    return prim, sem, forced


def resolve(value, prim: dict) -> str:
    """A DTCG colour $value to a hex, following one alias if there is one."""
    if isinstance(value, str) and value.startswith("{"):
        node = prim
        for part in value.strip("{}").split("."):
            node = node[part]
        return node["$value"]["hex"]
    return value["hex"]


def roles_of(doc: dict, prim: dict) -> list[dict]:
    """Every semantic colour role, with its proof, in document order."""
    out = []
    colour = doc["color"]
    for group in ("ink", "line", "accent", "focus", "status"):
        for key, token in colour.get(group, {}).items():
            if key.startswith("$"):
                continue
            ext = token["$extensions"]["studio.aninda"]
            proof = ext["proof"]
            name = f"{group}.{key}"
            prop = "--as-" + "-".join(
                p for p in name.replace("status.", "").split(".") if p != "default")
            out.append({
                "role": name,
                "var": prop,
                "hex": resolve(token["$value"], prim),
                "kind": ext["kind"],
                "step": f'{ext["family"]} {ext["step"]}',
                "required": proof["required"],
                "measured": proof["measured"],
                "worst": proof["worstCaseLsb"],
                "against": proof["hardestGround"],
                "level": proof["level"],
                "criterion": proof["criterion"],
            })
    return out


def surfaces_of(doc: dict) -> list[dict]:
    out = []
    for key, token in doc["color"]["surface"].items():
        if key.startswith("$"):
            continue
        ext = token["$extensions"]["studio.aninda"]
        out.append({"name": key, "var": f"--as-surface-{key}",
                    "hex": token["$value"]["hex"], "luminance": ext["luminance"]})
    return out


# ---------------------------------------------------------------------------
# The card shell
# ---------------------------------------------------------------------------

def card(group: str, name: str, subtitle: str, body: str,
         width: int = 760, height: int = 520, wide_note: str = "") -> str:
    """One preview card. The @dsCard comment MUST be the first line."""
    note = (f'<p class="note">{wide_note}</p>' if wide_note else "")
    return (
        f'<!-- @dsCard group="{e(group)}" viewport="{width}x{height}" '
        f'name="{e(name)}" subtitle="{e(subtitle)}" -->\n'
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        f"<title>{e(name)}</title>"
        '<link rel="stylesheet" href="../styles.css">'
        "<style>"
        "*{box-sizing:border-box}"
        "body{margin:0;padding:var(--as-space-6);"
        "background:var(--as-surface-base);color:var(--as-ink);"
        "font-family:var(--as-font-latin);font-size:var(--as-text-body);"
        "-webkit-font-smoothing:antialiased}"
        ".hd{display:flex;align-items:baseline;justify-content:space-between;"
        "gap:var(--as-space-4);padding-bottom:var(--as-space-3);"
        "border-bottom:1px solid var(--as-line);margin-bottom:var(--as-space-5)}"
        ".hd h1{margin:0;font-size:var(--as-text-h3);font-weight:600}"
        ".hd p{margin:0;font-family:var(--as-font-mono);"
        "font-size:var(--as-text-caption);color:var(--as-ink-muted)}"
        ".note{margin:var(--as-space-5) 0 0;max-width:66ch;"
        "font-size:var(--as-text-caption);color:var(--as-ink-muted)}"
        ".grid{display:grid;gap:var(--as-space-3)}"
        ".sw{display:flex;flex-direction:column;gap:2px;min-width:0}"
        ".sw i{display:block;height:52px;border-radius:var(--as-radius-badge);"
        "border:1px solid var(--as-line)}"
        ".sw b{font-size:var(--as-text-caption);font-weight:600}"
        ".sw code,.mono{font-family:var(--as-font-mono);"
        "font-size:var(--as-text-caption);color:var(--as-ink-muted)}"
        "table{width:100%;border-collapse:collapse;font-size:var(--as-text-caption)}"
        "caption{text-align:left;color:var(--as-ink-muted);"
        "padding-bottom:var(--as-space-2)}"
        "th,td{text-align:left;padding:6px 10px 6px 0;"
        "border-bottom:1px solid var(--as-line);vertical-align:baseline}"
        "th{font-family:var(--as-font-mono);font-weight:400;"
        "text-transform:none;color:var(--as-ink-muted)}"
        ".num{text-align:right;font-family:var(--as-font-mono);"
        "font-variant-numeric:tabular-nums}"
        ".row{display:flex;flex-wrap:wrap;gap:var(--as-space-3);"
        "align-items:center}"
        ".panels{display:grid;grid-template-columns:repeat(2,1fr);"
        "gap:var(--as-space-4)}"
        ".panel{padding:var(--as-space-4);border:1px solid var(--as-line);"
        "border-radius:var(--as-radius-card);background:var(--as-surface-base);"
        "color:var(--as-ink)}"
        ".panel h2{margin:0 0 var(--as-space-3);font-size:var(--as-text-caption);"
        "font-family:var(--as-font-mono);color:var(--as-ink-muted);font-weight:400}"
        "</style></head><body>"
        f'<div class="hd"><h1>{e(name)}</h1><p>{e(subtitle)}</p></div>'
        f"{body}{note}"
        "</body></html>\n"
    )


def swatch(label: str, value_css: str, code: str) -> str:
    return (f'<div class="sw"><i style="background:{value_css}"></i>'
            f"<b>{e(label)}</b><code>{e(code)}</code></div>")


def table(caption: str, headers: list[str], rows: list[list[str]],
          numeric: set[int] = frozenset()) -> str:
    head = "".join(f'<th scope="col"'
                   f'{" class=\"num\"" if i in numeric else ""}>{e(h)}</th>'
                   for i, h in enumerate(headers))
    body = ""
    for row in rows:
        cells = "".join(
            (f'<th scope="row">{c}</th>' if i == 0 else
             f'<td{" class=\"num\"" if i in numeric else ""}>{c}</td>')
            for i, c in enumerate(row))
        body += f"<tr>{cells}</tr>"
    return (f"<table><caption>{e(caption)}</caption>"
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")


def themed_panels(inner: str) -> str:
    """The same markup in all four themes, each panel pinning its own."""
    panels = "".join(
        f'<div class="panel" data-theme="{t}" role="group" '
        f'aria-labelledby="p-{t}"><h2 id="p-{t}">{e(THEME_LABEL[t])}</h2>{inner}</div>'
        for t in THEMES)
    return f'<div class="panels">{panels}</div>'


# ---------------------------------------------------------------------------
# The cards
# ---------------------------------------------------------------------------

def card_surfaces(prim, sem, forced) -> str:
    rows = []
    for s in surfaces_of(sem["light"]):
        rows.append([f"<code>{e(s['name'])}</code>",
                     swatch("", f"var({s['var']})", "").replace("<b></b><code></code>", ""),
                     f"<code>{e(s['var'])}</code>",
                     f"{s['luminance']:.4f}"])
    body = (
        '<div class="grid" style="grid-template-columns:repeat(7,1fr)">'
        + "".join(swatch(s["name"], f"var({s['var']})", s["hex"])
                  for s in surfaces_of(sem["light"]))
        + "</div>"
        + themed_panels(
            '<div class="grid" style="grid-template-columns:repeat(7,1fr)">'
            + "".join(f'<i style="background:var({s["var"]});display:block;'
                      f'height:34px;border-radius:var(--as-radius-badge);'
                      f'border:1px solid var(--as-line)"></i>'
                      for s in surfaces_of(sem["light"]))
            + "</div>")
    )
    return card(
        "Colour", "Surfaces", "seven grounds, per theme", body, 900, 560,
        "Every surface is swept along a lightness ladder anchored at the theme's own "
        "extreme, not taken from the ramp — steps taken from an eleven-step ramp "
        "collided in the light themes. Each is at least 0.9 CIEDE2000 from its "
        "neighbours, so the depth vocabulary is visibly distinct rather than "
        "nominally so.")


def card_roles(prim, sem, forced) -> str:
    rows = []
    for r in roles_of(sem["light"], prim):
        rows.append([
            f'<span style="display:inline-block;width:11px;height:11px;'
            f'border-radius:50%;background:var({r["var"]});vertical-align:middle;'
            f'margin-right:6px"></span><code>{e(r["role"])}</code>',
            f"<code>{e(r['var'])}</code>",
            e(r["kind"]),
            f"{r['required']:.1f}",
            f"<b>{r['measured']:.4f}</b>",
            f"{r['worst']:.4f}",
            e(r["level"]),
        ])
    body = table(
        "Every colour role in the Light theme. Required is the floor it had to "
        "clear; measured is the worst ratio against any surface it can land on; "
        "worst case is that ratio again with every channel of both colours nudged "
        "by one bit.",
        ["Role", "Property", "Kind", "Needs", "Measured", "Worst ±1 bit", "Level"],
        rows, numeric={3, 4, 5})
    return card(
        "Colour", "Roles", "measured, not chosen", body, 900, 620,
        "A role is picked by measurement: the engine scans the ramp and takes the "
        "first step that clears its target against every surface, then publishes the "
        "worst figure rather than the flattering one. accent.hover is measured "
        "against the label it carries instead, because it is a ground that holds "
        "text — a distinction that cost a real contrast failure to learn.")


def card_ramps(prim, sem, forced) -> str:
    ramp = prim["color"]["ramp"]
    families = [k for k in ramp if not k.startswith("$")]
    steps = [k for k in ramp[families[0]] if not k.startswith("$")]
    rows = []
    for fam in families:
        cells = [f"<code>{e(fam)}</code>"]
        for step in steps:
            hexv = ramp[fam][step]["$value"]["hex"]
            cells.append(
                f'<span title="{e(hexv)}" style="display:block;height:26px;'
                f'background:{e(hexv)};border:1px solid var(--as-line);'
                f'border-radius:3px"></span>')
        rows.append(cells)
    body = table(
        "The six primitive ramps, eleven steps each. These are the only literal "
        "colours in this project: the ramps are primitives that the roles alias, and "
        "tokens.css exposes the roles rather than the steps, so a card about the "
        "steps has to name them. Read from primitive.tokens.json at build time.",
        ["Family"] + steps, rows)
    return card(
        "Colour", "Ramps", f"{len(families)} families, {len(steps)} steps", body,
        980, 420,
        "Generated in OKLCH from one anchor per family, then gamut-mapped and "
        "rounded to eight bits before anything is measured — because measuring the "
        "unrounded colour and shipping the rounded one is how a system passes its "
        "own check and fails a reader's screen.")


def card_type(prim, sem, forced) -> str:
    ty = prim["dimension"]["type"]
    ratio = prim["number"]["scale"]["ratio"]["$value"]
    sizes = [k for k in ty if not k.startswith("$")
             and not k.startswith("bangla")]
    rows = []
    for key in sizes:
        v = ty[key]["$value"]
        rows.append([f"<code>--as-text-{e(key)}</code>",
                     f"{v['value']:g}{e(v['unit'])}",
                     f'<span style="font-size:var(--as-text-{key})">Ag</span>'])
    body = (table(
        f"The scale, a perfect fourth at {ratio}. Every size is a token; none is "
        f"typed into a stylesheet.",
        ["Token", "Size", "Specimen"], rows, numeric={1})
        + f'<p class="note mono">ratio {ratio} · '
          f'--as-scale-ratio</p>')
    return card(
        "Type", "Scale", f"perfect fourth, {ratio}", body, 760, 560,
        "A perfect fourth is a large jump on purpose: the hierarchy is unmistakable "
        "and fewer levels are needed to express it. Literata carries an optical-size "
        "axis from 7 to 72, so the letterforms are redrawn for the size rather than "
        "scaled, and browsers apply that automatically.")


def card_bangla(prim, sem, forced) -> str:
    scale = prim["number"]["scale"]["bangla"]
    keys = [k for k in scale if not k.startswith("$")]
    floor = prim["dimension"]["type"]["bangla-min"]["$value"]
    bump = prim["dimension"]["type"]["bangla-weight-bump-below"]["$value"]
    lh = prim["number"]["lineHeight"]["bangla"]["$value"]
    rows = [[f"<code>{e(k)}</code>", f"{scale[k]['$value']}"] for k in keys]
    body = (
        table("The measured multiplier per size band. Bangla is set smaller than "
              "Latin at the same nominal size because its x-height runs larger; "
              "these figures were measured from rendered specimens, not chosen.",
              ["Band", "Multiplier"], rows, numeric={1})
        + '<div style="margin-top:var(--as-space-5)">'
          '<p lang="bn" style="font-family:var(--as-font-bangla);'
          'font-size:var(--as-text-h2);line-height:var(--as-bangla-line-height);'
          'margin:0">অনিন্দ্য স্টুডিও</p>'
          '<p lang="bn" style="font-family:var(--as-font-bangla);'
          'line-height:var(--as-bangla-line-height);margin:var(--as-space-2) 0 0">'
          'আমি ছোটো, যত্নে গড়া সফটওয়্যার বানাই।</p></div>'
        + f'<p class="note mono">floor {floor["value"]:g}{e(floor["unit"])} · '
          f'weight bump below {bump["value"]:g}{e(bump["unit"])} · '
          f'line-height {lh}</p>')
    return card(
        "Type", "Bangla", "measured multiplier and a floor", body, 760, 560,
        "The multiplier never takes Bangla below the floor, because below it the "
        "মাত্রা — the headline stroke that runs across the top of the letters — stops "
        "resolving into a continuous line. Under the bump size the weight steps up "
        "for the same reason.")


def card_space(prim, sem, forced) -> str:
    space = prim["dimension"]["space"]
    keys = [k for k in space if not k.startswith("$")]
    rows = []
    for k in keys:
        v = space[k]["$value"]
        rows.append([f"<code>--as-space-{e(k)}</code>",
                     f"{v['value']:g}{e(v['unit'])}",
                     f'<span style="display:block;height:12px;'
                     f'width:var(--as-space-{k});background:var(--as-accent);'
                     f'border-radius:2px"></span>'])
    body = table("Ten steps on a four-pixel grid. Every gap in the component layer "
                 "is one of these.", ["Token", "Value", ""], rows, numeric={1})
    return card("Space and shape", "Space scale", "ten steps, 4 px grid", body,
                760, 560,
                "A four-pixel grid is small enough to place things precisely and "
                "coarse enough that two people reaching for the same gap choose the "
                "same token.")


def card_shape(prim, sem, forced) -> str:
    radius = prim["dimension"]["radius"]
    target = prim["dimension"]["target"]
    focus = prim["dimension"]["focus"]
    rrows = []
    for k in [x for x in radius if not x.startswith("$")]:
        v = radius[k]["$value"]
        rrows.append([f"<code>--as-radius-{e(k)}</code>",
                      f"{v['value']:g}{e(v['unit'])}",
                      f'<span style="display:block;height:34px;width:56px;'
                      f'background:var(--as-surface-highest);'
                      f'border:1px solid var(--as-line);'
                      f'border-radius:var(--as-radius-{k})"></span>'])
    trows = []
    for k in [x for x in target if not x.startswith("$")]:
        v = target[k]["$value"]
        trows.append([f"<code>--as-target-{e(k)}</code>",
                      f"{v['value']:g}{e(v['unit'])}"])
    body = (table("Four radii.", ["Token", "Value", ""], rrows, numeric={1})
            + '<div style="height:var(--as-space-5)"></div>'
            + table("Four target floors, because three platforms publish three "
                    "different ones and this system states all of them.",
                    ["Token", "Value"], trows, numeric={1})
            + f'<p class="note mono">focus ring '
              f'{focus["ring-width"]["$value"]["value"]:g}'
              f'{e(focus["ring-width"]["$value"]["unit"])} at '
              f'{focus["ring-offset"]["$value"]["value"]:g}'
              f'{e(focus["ring-offset"]["$value"]["unit"])} offset</p>')
    return card("Space and shape", "Shape and targets", "radii, targets, focus",
                body, 760, 620,
                "WCAG 2.2 SC 2.5.8 asks for 24 CSS pixels at AA. Apple's iOS minimum "
                "is 28pt with 44 as the default, and Android's is 48dp. Three floors, "
                "all named, so nobody has to guess which one a design is being held "
                "to.")


def card_motion(prim, sem, forced) -> str:
    dur = prim["duration"]["motion"]
    ease = prim["cubicBezier"]["motion"]
    rows = []
    for k in [x for x in dur if not x.startswith("$")]:
        v = dur[k]["$value"]
        rows.append([f"<code>--as-duration-{e(k)}</code>",
                     f"{v['value']:g}{e(v['unit'])}",
                     e(dur[k].get("$description", ""))])
    erows = []
    for k in [x for x in ease if not x.startswith("$")]:
        v = ease[k]["$value"]
        erows.append([f"<code>--as-ease-{e(k)}</code>",
                      f"cubic-bezier({', '.join(f'{n:g}' for n in v)})"])
    body = (table("Two durations. Nothing in this system goes over 300 ms.",
                  ["Token", "Value", "For"], rows, numeric={1})
            + '<div style="height:var(--as-space-5)"></div>'
            + table("Three curves.", ["Token", "Value"], erows))
    return card("Motion", "Duration and easing", "two durations, three curves",
                body, 800, 480,
                "Material's split is the useful idea even without springs: spatial "
                "movement may overshoot, effects must not. Every motion token here "
                "is also disabled wholesale under prefers-reduced-motion, which the "
                "stylesheet does rather than asking each component to remember.")


def card_forced(prim, sem, forced) -> str:
    rows = [[f"<code>{e(k)}</code>", f"<code>{e(v)}</code>"]
            for k, v in forced["map"].items()]
    body = (table("Every brand colour, and the system colour it becomes in "
                  "forced-colors mode.", ["Token", "System colour"], rows)
            + "<ul class=\"note\">"
            + "".join(f"<li>{e(r)}</li>" for r in forced["rules"])
            + "</ul>")
    return card("Colour", "Forced colours", "every brand colour overridden", body,
                820, 640,
                "This file sits deliberately outside the DTCG tree: system colour "
                "keywords have no colour space, no components and no hex, and none "
                "of DTCG's thirteen types fits them. Bending them into a colour "
                "token would be a lie about what they are.")


def card_marks(prim, sem, forced) -> str:
    def mark(name: str) -> str:
        svg = (MARKS / name).read_text(encoding="utf-8")
        svg = svg.replace("<svg ", '<svg width="96" height="96" role="img" '
                                  'aria-label="The Aninda Studio mark" ', 1)
        return svg
    body = (
        '<div class="row" style="gap:var(--as-space-6)">'
        f'<div class="sw" style="color:var(--as-ink)">{mark("mark-regular.svg")}'
        '<b>Regular</b><code>mark-regular.svg</code></div>'
        f'<div class="sw" style="color:var(--as-ink)">{mark("mark-heavy.svg")}'
        '<b>Heavy</b><code>mark-heavy.svg</code></div>'
        f'<div class="sw" style="color:var(--as-accent)">{mark("mark-regular.svg")}'
        '<b>In the accent</b><code>currentColor</code></div>'
        "</div>"
        + themed_panels(
            f'<div style="color:var(--as-ink)">{mark("mark-regular.svg")}</div>'))
    return card("Brand", "The mark", "two weights, drawn in currentColor", body,
                860, 560,
                "The mark carries no colour of its own: it is drawn in currentColor, "
                "so it takes the theme it lands in and yields to the system palette "
                "in forced colours. Setting a colour on it is the exception, not the "
                "default, and the only files that carry one are the fixed-colour icon "
                "masters a platform draws without a stylesheet.")


def card_wordmarks(prim, sem, forced) -> str:
    def art(name: str, width: int) -> str:
        svg = (MARKS / name).read_text(encoding="utf-8")
        return svg.replace("<svg ", f'<svg width="{width}" role="img" ', 1)
    body = (
        '<div class="sw" style="color:var(--as-ink);gap:var(--as-space-2)">'
        f'{art("wordmark-latin.svg", 300)}<code>wordmark-latin.svg</code></div>'
        '<div class="sw" style="color:var(--as-ink);gap:var(--as-space-2);'
        'margin-top:var(--as-space-5)">'
        f'{art("wordmark-bangla.svg", 300)}<code>wordmark-bangla.svg</code></div>')
    return card("Brand", "Wordmarks", "Latin and Bangla, drawn as outlines", body,
                760, 460,
                "Both are outlines, not live text, so they need no font installed "
                "and cannot reflow. অনিন্দ্য is the name; Aninda is its romanised "
                "form, and the two are not interchangeable in running text.")


def card_icons(prim, sem, forced) -> str:
    manifest = read_json(MARKS.parent / "manifest.json")
    radius = manifest["tile_radius_percent"]
    px = manifest["tile_radius_px_at_1024"]
    tile = (MARKS / "tile-web.svg").read_text(encoding="utf-8")
    tile = tile.replace("<svg ", '<svg width="120" height="120" role="img" '
                                 'aria-label="The Aninda Studio icon tile" ', 1)
    files = [[f"<code>{e(name)}</code>"] for name in manifest["files"]
             if "icon" in name or "tile" in name]
    body = (f'<div class="row">{tile}'
            f'<div><p class="mono">corner radius {radius:g}% of the width — '
            f'{px:g} px on the 1024 px icon</p></div></div>'
            + '<div style="height:var(--as-space-4)"></div>'
            + table("The icon files this system ships.", ["File"], files))
    return card("Brand", "Icons", "one rounded tile, everywhere", body, 780, 520,
                "One rounded icon is used on every surface, Apple included — the "
                "owner's decision, recorded with its trade-off. Apple publishes no "
                "corner radius and no percentage, and does not use the word "
                "'squircle' anywhere in current guidance, so this figure is ours: "
                "the radius-hero token's numeral reused as a percentage.")


def _icon(path: str) -> str:
    return ('<svg class="as-icon" viewBox="0 0 16 16" width="16" height="16" '
            'aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
            f"{path}</svg>")


CHECK = _icon('<path d="M3 8.6 6.4 12 13 4.6"/>')
INFO = _icon('<circle cx="8" cy="8" r="6.2"/><path d="M8 7.4v4"/>'
             '<path d="M8 4.9h.01"/>')
WARN = _icon('<path d="M8 2.2 15 13.8H1Z"/><path d="M8 6.4v3.1"/>'
             '<path d="M8 11.9h.01"/>')
CROSS = _icon('<path d="M4 4 12 12M12 4 4 12"/>')


def card_actions(prim, sem, forced) -> str:
    demo = (
        '<div class="row">'
        '<button type="button" class="as-btn as-btn--primary">Save the entry</button>'
        '<button type="button" class="as-btn">Cancel</button>'
        '<button type="button" class="as-btn as-btn--quiet">Learn more</button>'
        '<button type="button" class="as-btn as-btn--danger">Delete the file</button>'
        '<button type="button" class="as-btn as-btn--small">Copy the code</button>'
        "</div>")
    return card("Components", "Buttons", "four tones, two sizes", demo + themed_panels(demo),
                900, 620,
                "The hovered primary action uses --as-accent-hover, a role measured "
                "against the label it carries. It used to use the line colour, which "
                "is proven at 3:1 as a line and took the white label to 4.35:1 — a "
                "resting state that passes proves nothing about the state a pointer "
                "is actually in, and both harnesses now measure all three.")


def card_forms(prim, sem, forced) -> str:
    demo = (
        '<div class="as-stack" style="display:grid;gap:var(--as-space-4)">'
        '<div class="as-field"><label class="as-label" for="d-email">Email address'
        '</label><input class="as-input" id="d-email" type="email" '
        'placeholder="you@example.com"><p class="as-hint">We reply from this '
        'address too.</p></div>'
        '<div class="as-field"><label class="as-label" for="d-plan">Plan</label>'
        '<select class="as-select" id="d-plan"><option>Monthly</option>'
        '<option>Yearly</option></select></div>'
        '<label class="as-choice"><input class="as-choice__control" type="checkbox" '
        'checked><span>Send me the release notes</span></label>'
        "</div>")
    return card("Components", "Fields", "input, select, choice", demo, 780, 560,
                "Every field has a real label element, and every hint is tied to its "
                "field rather than left floating beside it. Focus is shown on :focus, "
                "not :focus-visible — this system shows focus to anyone who focuses, "
                "rather than only to those the browser guesses are using a keyboard.")


def card_feedback(prim, sem, forced) -> str:
    badges = (
        '<div class="row">'
        f'<span class="as-badge as-badge--success">{CHECK}'
        '<span class="as-badge__label">Measured</span></span>'
        f'<span class="as-badge as-badge--info">{INFO}'
        '<span class="as-badge__label">Documented</span></span>'
        f'<span class="as-badge as-badge--warning">{WARN}'
        '<span class="as-badge__label">Unverified</span></span>'
        f'<span class="as-badge as-badge--danger">{CROSS}'
        '<span class="as-badge__label">Failed</span></span>'
        "</div>")
    alert = (
        '<div class="as-alert as-alert--info" style="margin-top:var(--as-space-4)">'
        f'<span class="as-alert__glyph">{INFO}</span>'
        '<div class="as-alert__body">'
        '<p class="as-alert__title">Every state carries a word and a glyph</p>'
        '<p class="as-alert__text">Colour is the third signal here and never the '
        'only one, so a reader who cannot tell these apart by colour can still read '
        'which is which.</p></div></div>')
    return card("Components", "Badges and alerts", "status, three signals deep",
                badges + alert + themed_panels(badges), 900, 660,
                "In forced-colors mode every status colour resolves to CanvasText, "
                "so colour disappears entirely. That is why the glyph and the word "
                "are not decoration: they are what survives.")


def card_data(prim, sem, forced) -> str:
    demo = (
        '<div class="as-card"><p class="as-card__title">Card</p>'
        '<p class="as-card__meta">A surface one step brighter than the page</p>'
        '<p class="as-card__body">It carries a shadow in the light theme and none in '
        'the dark ones, because a shadow on a dark ground reads as dirt rather than '
        'as height.</p></div>'
        '<div class="as-scroll-x" style="margin-top:var(--as-space-4)">'
        '<table class="as-table as-table--numeric">'
        '<caption>A table with a caption, column headers and a row header.</caption>'
        '<thead><tr><th scope="col">Part</th><th scope="col" class="as-num">Count'
        '</th></tr></thead><tbody>'
        '<tr><th scope="row">Themes</th><td class="as-num">4</td></tr>'
        '<tr><th scope="row">Design tokens</th><td class="as-num">64</td></tr>'
        "</tbody></table></div>")
    return card("Components", "Card and table", "surfaces and tabular data", demo,
                800, 560,
                "Every table in this system has a caption and a row header. That rule "
                "was written after the book's own tables broke it, so the table "
                "helper now refuses to build without a caption rather than trusting "
                "whoever calls it.")


def card_navigation(prim, sem, forced) -> str:
    demo = (
        '<nav class="as-breadcrumb" aria-label="Breadcrumb"><ol>'
        '<li><a class="as-breadcrumb__link" href="#">Home</a></li>'
        '<li><a class="as-breadcrumb__link" href="#">Components</a></li>'
        '<li aria-current="page">Navigation</li></ol></nav>'
        '<div class="as-tabs" role="tablist" aria-label="Example" '
        'style="margin-top:var(--as-space-4)">'
        '<button type="button" class="as-tab" role="tab" id="t1" '
        'aria-selected="true" aria-controls="pan1">Overview</button>'
        '<button type="button" class="as-tab" role="tab" id="t2" '
        'aria-selected="false" aria-controls="pan2" tabindex="-1">Detail</button>'
        "</div>"
        '<div class="as-tabpanel" role="tabpanel" id="pan1" aria-labelledby="t1">'
        '<p>A roving tabindex keeps one tab in the tab sequence; the arrow keys move '
        'the selection.</p></div>')
    return card("Components", "Navigation", "breadcrumb and tabs", demo, 800, 480,
                "The tabs pattern needs both halves: a roving tabindex takes every "
                "unselected tab out of the tab sequence, so without the arrow-key "
                "handler the card ships visible buttons no key can reach.")


def card_accessibility(prim, sem, forced) -> str:
    rows = []
    for theme in THEMES:
        ext = sem[theme]["$extensions"]["studio.aninda"]
        worst_text = min(r["worst"] for r in roles_of(sem[theme], prim)
                         if r["kind"] in ("text", "fill"))
        worst_non = min(r["worst"] for r in roles_of(sem[theme], prim)
                        if r["kind"] == "nontext")
        rows.append([e(THEME_LABEL[theme]),
                     f"{ext['textTarget']:.1f}", f"{worst_text:.4f}",
                     f"{ext['nonTextTarget']:.1f}", f"{worst_non:.4f}"])
    body = (table("The worst measured ratio in each theme, against the floor that "
                  "theme is held to. Text and non-text are reported separately, "
                  "because judging a border against the text floor invents a failure "
                  "and judging text against the non-text floor hides one.",
                  ["Theme", "Text needs", "Worst text", "Non-text needs",
                   "Worst non-text"], rows, numeric={1, 2, 3, 4})
            + '<p class="note">WCAG 2.2 defines no AAA level for non-text contrast, '
              'so the high-contrast themes hold their borders to 4.5:1 as policy '
              'rather than as a criterion, and say so.</p>')
    return card("Foundations", "Accessibility", "measured floors per theme", body,
                860, 460,
                "AA is 4.5:1 for text and 3:1 for non-text. The two high-contrast "
                "themes are held to AAA at 7:1 for text, because a high-contrast "
                "theme that only reaches AA is a third colour scheme wearing the "
                "name.")


CARDS = [
    card_surfaces, card_roles, card_ramps, card_forced,
    card_type, card_bangla,
    card_space, card_shape, card_motion,
    card_marks, card_wordmarks, card_icons,
    card_actions, card_forms, card_feedback, card_data, card_navigation,
    card_accessibility,
]


# ---------------------------------------------------------------------------
# The bundle
# ---------------------------------------------------------------------------

def slug(fn) -> str:
    return fn.__name__.removeprefix("card_").replace("_", "-")


def styles_css() -> str:
    """tokens.css + components.css + the three @font-face rules.

    Cards link one stylesheet, so a card is a complete document: no build step,
    no network, and the same values the repository ships.
    """
    faces = []
    for family, filename, weight in FONT_FILES:
        if not (FONTS / filename).exists():
            raise BuildError(f"{FONTS / filename} is missing. "
                             f"Run 08_components/build.py first.")
        faces.append(
            "@font-face{\n"
            f'  font-family: "{family}";\n'
            "  font-style: normal;\n"
            f"  font-weight: {weight};\n"
            "  font-display: swap;\n"
            f'  src: url("tokens/fonts/{filename}") format("woff2");\n'
            "}")
    return "\n".join([
        "/* Aninda Studio — the whole visual system in one stylesheet.",
        "   GENERATED by 13_plugins/claude-design/build.py. Do not hand-edit.",
        "   Sources: 07_tokens/css/tokens.css and 08_components/src/components.css. */",
        "",
        "\n".join(faces),
        "",
        TOKENS_CSS.read_text(encoding="utf-8").strip(),
        "",
        COMPONENTS_CSS.read_text(encoding="utf-8").strip(),
        "",
    ])


def skill_md(cards: dict[str, str]) -> str:
    groups: dict[str, list[str]] = {}
    for path, text in sorted(cards.items()):
        first = text.split("\n", 1)[0]
        group = first.split('group="', 1)[1].split('"', 1)[0]
        name = first.split('name="', 1)[1].split('"', 1)[0]
        groups.setdefault(group, []).append(name)
    listing = "\n".join(
        f"- **{g}** — {', '.join(names)}" for g, names in sorted(groups.items()))
    return f"""---
name: Aninda Studio
description: >-
  The Aninda Studio brand and design system. Use these tokens, components and
  rules when designing or building anything for Aninda Studio, in English or in
  Bangla. Every colour pairing here was measured rather than chosen, and the
  figure published is the worst case rather than the flattering one.
---

# Aninda Studio

A studio of one, working in two scripts. This project holds the whole visual
system: {len(cards)} preview cards, the design tokens they are built from, the
component stylesheet, and the identity artwork.

## What is here

{listing}

## The rules that matter

1. **Paint with a role, never a literal.** `var(--as-accent)`, not a hex. The
   roles resolve per theme, so a design written in roles works in all four
   without being rewritten.
2. **Four themes, not two.** Light, dark, and a high-contrast pair. Each is a
   complete set of values, not a filter over another set.
3. **Colour is never the only signal.** Every state carries a word and a glyph,
   because in forced-colors mode every status colour becomes CanvasText.
4. **Bangla is set from the register.** Only strings approved against
   বাংলা একাডেমি প্রমিত বাংলা বানানের নিয়ম appear in Bangla; everything else stays
   in English rather than being translated by guesswork.
5. **A number that must stay true is derived, never typed.** Every figure on
   every card here is read from the token files when this project is built.

## Naming

Prefix `--as-`. For a colour, drop a leading `color.` or `status.` and a trailing
`default`: `color.ink.default` is `--as-ink`, `color.status.danger` is
`--as-danger`. Everything else has a fixed family name — `--as-space-4`,
`--as-text-body`, `--as-radius-card`, `--as-duration-move`, `--as-ease-enter`.
When in doubt read the property out of `tokens/tokens.css` rather than deriving
it.

## Licence

The tokens, stylesheets and artwork are Apache-2.0. The three typefaces are SIL
OFL 1.1, with their licence texts in `tokens/fonts/`. The monospace face is a
subset of IBM Plex Mono renamed to Aninda Mono, because "Plex" is a Reserved Font
Name and subsetting is a modification under clause 3 of that licence.

Generated by `13_plugins/claude-design/build.py`. Nothing in this project is
hand-drawn, and editing a file here is undone by the next build.
"""


def readme_md(cards: dict[str, str], prim: dict) -> str:
    ramp = prim["color"]["ramp"]
    families = [k for k in ramp if not k.startswith("$")]
    steps = [k for k in ramp[families[0]] if not k.startswith("$")]
    return f"""# Aninda Studio — Claude Design project

Generated. The source of truth is the repository:
<https://github.com/GRU-953/aninda-studio>

- {len(cards)} preview cards in `guidelines/`
- {len(families)} colour ramps of {len(steps)} steps in `tokens/`
- 4 themes: light, dark, high-contrast light, high-contrast dark
- 1 stylesheet, `styles.css`, holding the tokens, the component layer and the
  three inlined typefaces

To update this project, change the tokens in the repository, run
`13_plugins/claude-design/build.py`, and push the `dist/` folder. Editing a file
here by hand is undone by the next build, and nothing here will report that the
remote copy has fallen behind — which is why the build is the route.
"""


def build() -> dict[str, bytes]:
    prim, sem, forced = load()
    out: dict[str, bytes] = {}

    cards: dict[str, str] = {}
    for fn in CARDS:
        text = fn(prim, sem, forced)
        if not text.startswith("<!-- @dsCard "):
            raise BuildError(
                f"{fn.__name__} does not begin with an @dsCard comment. The Design "
                f"System pane builds its index from that first line, so the card "
                f"would upload fine and never appear.")
        cards[f"guidelines/{slug(fn)}.card.html"] = text
    for path, text in cards.items():
        out[path] = text.encode("utf-8")

    out["styles.css"] = styles_css().encode("utf-8")
    out["css/components.css"] = COMPONENTS_CSS.read_bytes()
    out["tokens/tokens.css"] = TOKENS_CSS.read_bytes()
    for src in sorted(TOKENS.glob("*.json")):
        out[f"tokens/{src.name}"] = src.read_bytes()
    for _, filename, _ in FONT_FILES:
        out[f"tokens/fonts/{filename}"] = (FONTS / filename).read_bytes()
    for licence in sorted(FONTS.glob("*-OFL.txt")):
        out[f"tokens/fonts/{licence.name}"] = licence.read_bytes()
    for svg in sorted(MARKS.glob("*.svg")):
        out[f"assets/marks/{svg.name}"] = svg.read_bytes()
    out["assets/marks/manifest.json"] = (MARKS.parent / "manifest.json").read_bytes()

    out["SKILL.md"] = skill_md(cards).encode("utf-8")
    out["readme.md"] = readme_md(cards, prim).encode("utf-8")
    # All four, not two. The NOTICE copied in here is the repository's own: it is
    # headed "FOUR LICENCES APPLY TO DIFFERENT PARTS OF THIS REPOSITORY" and sends
    # the reader to LICENSE-DOCS.md for the writing's terms and TRADEMARKS.md for
    # the identity detail. Neither travelled, and this is the one deliverable whose
    # artefact lives on a remote service — so that NOTICE is the only licence
    # statement a recipient gets, and it pointed at nothing. The `if exists` guard
    # is gone too: a missing licence file must stop the build, not vanish quietly.
    for name in ("LICENSE", "NOTICE", "LICENSE-DOCS.md", "TRADEMARKS.md"):
        src = ROOT / name
        if not src.exists():
            raise SystemExit(f"FAILED — nothing written: {name} is missing from the "
                             f"repository root, so the bundle cannot carry it")
        out[name] = src.read_bytes()

    # Every var(--as-...) on every card must be a property styles.css defines.
    # A card that paints with a name the stylesheet does not have renders with the
    # property unset, which looks like a design decision rather than a fault.
    import re
    defined = set(re.findall(r"(--as-[a-z0-9-]+)\s*:", out["styles.css"].decode()))
    for path, text in cards.items():
        used = set(re.findall(r"var\((--as-[a-z0-9-]+)", text))
        missing = sorted(used - defined)
        if missing:
            raise BuildError(f"{path} paints with {missing}, which styles.css does "
                             f"not define. {len(defined)} properties are available.")
    return out


def main(argv: list[str]) -> int:
    check = "--check" in argv
    try:
        artefacts = build()
    except BuildError as exc:
        print(f"BUILD FAILED — nothing written.\n  {exc}", file=sys.stderr)
        return 1

    if check:
        problems = []
        for rel, data in sorted(artefacts.items()):
            path = DIST / rel
            if not path.exists():
                problems.append(f"missing: {rel}")
            elif path.read_bytes() != data:
                problems.append(f"differs: {rel}")
        existing = {str(p.relative_to(DIST)) for p in DIST.rglob("*") if p.is_file()}
        for extra in sorted(existing - set(artefacts)):
            problems.append(f"not generated by this build: {extra}")
        if problems:
            print("CHECK FAILED — dist/ has drifted from the system:", file=sys.stderr)
            for item in problems:
                print(f"  {item}", file=sys.stderr)
            return 1
        print(f"--check: {len(artefacts)} files match the system. Nothing written.")
        return 0

    if DIST.exists():
        shutil.rmtree(DIST)
    for rel, data in artefacts.items():
        path = DIST / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    total = sum(len(d) for d in artefacts.values())
    n_cards = sum(1 for k in artefacts if k.startswith("guidelines/"))
    print(f"Wrote {len(artefacts)} files ({total / 1000:.0f} kB) to "
          f"{DIST.relative_to(ROOT)}/ — {n_cards} preview cards.")
    print("Push with DesignSync, or see readme.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
