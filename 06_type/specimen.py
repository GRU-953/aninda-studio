#!/usr/bin/env python3
"""
Aninda Studio — typeface specimen renderer and measurement harness.

What this script does, in order:

  1. Reads every downloaded font file in 06_type/candidates/ with fontTools and
     records the facts that matter — licence and Reserved Font Name read from the
     OFL.txt beside each font, variable axes, declared metrics, glyph coverage.
     Output: 06_type/_data/font_facts.json
  2. Shapes a set of Bangla conjuncts and words with HarfBuzz and checks for the
     three ways shaping fails: a missing glyph, an inserted dotted circle, or a
     visible hasanta where a joined form was expected.
  3. Opens Chromium via Playwright and MEASURES each family's real rendered ink
     using the Canvas 2D text-metrics API, which reports the actual inked
     bounding box of a string rather than the numbers the font declares about
     itself.
  4. Measures matra continuity and matra thickness from real pixels with Pillow:
     does the headline stroke run unbroken across a word, and how thick is it.
  5. Finds, per Bangla face, the smallest line-height at which the matra of one
     line stops touching the descenders of the line above.
  6. Works out, per pairing and AT EVERY SIZE, the multiplier the Bangla face
     needs to look the same size as the Latin, then renders a specimen PNG per
     pairing into 06_type/specimens/

  Everything from steps 2-6 lands in 06_type/_data/measurements.json.

Every number quoted in SHORTLIST.md, pairings.md, MEASUREMENTS.md and
RECOMMENDATION.md is reproducible by running this one script.

Terms used below, explained once:
  - "em"        the font's own design square; dividing by it makes numbers from
                different fonts comparable.
  - "x-height"  the height of a lowercase 'x'. It, not the point size, is what
                makes Latin text look big or small.
  - "cap height" the height of a capital 'H'.
  - "মাত্রা / matra" the horizontal headline stroke that runs along the top of
                most Bangla letters and joins them into a word.
  - "variable font" one file that can slide continuously between weights,
                widths or optical sizes instead of shipping one file each.
  - "optical size (opsz)" an axis that redraws the letters for the size they
                will be used at: sturdier and more open when small, finer and
                tighter when large. Most families do not have one.

Run:
    cd <the repository folder>
    export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
    .venv/bin/python 06_type/specimen.py
"""

from __future__ import annotations

import json
import math
import os
import pathlib
import re
import sys

# ---------------------------------------------------------------------------
# Paths. Everything is project-local; nothing is installed or read from
# outside this project directory.
# ---------------------------------------------------------------------------
HERE = pathlib.Path(__file__).resolve().parent          # .../06_type
ROOT = HERE.parent                                      # the repository root


def rel(path) -> str:
    """A path as this repository sees it, never as this Mac sees it.

    The two data files this script writes carried 70 absolute paths into the
    repository — every font's `path` and `licence_file`, and every crop — which
    breaks the project's own rule that nothing generated may hold an absolute path,
    and makes the committed output different on anyone else's machine. Stored
    repo-relative and resolved through `absolute()` at the point of use.
    """
    return str(pathlib.Path(path).resolve().relative_to(ROOT))


def absolute(rel_path: str) -> pathlib.Path:
    """The inverse of rel(), for the places that must open the file."""
    return ROOT / rel_path
PROJECT = HERE.parent                                    # .../Aninda_Studio
CANDIDATES = HERE / "candidates"
SPECIMENS = HERE / "specimens"
DATA = HERE / "_data"
CROPS = DATA / "crops"

# Playwright will not find Chromium without this. Set defensively here as an
# absolute path so the script works from any working directory, but the
# documented invocation also exports it relative to the project root.
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(PROJECT / "00_sandbox" / "browsers"))

for d in (SPECIMENS, DATA, CROPS):
    d.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. The candidate registry.
#    key -> (script, relative path under candidates/, human family name)
# ---------------------------------------------------------------------------
REGISTRY: dict[str, tuple[str, str, str]] = {
    # --- Latin ---
    "inter":          ("latin", "latin/inter/Inter[opsz,wght].ttf", "Inter"),
    "newsreader":     ("latin", "latin/newsreader/Newsreader[opsz,wght].ttf", "Newsreader"),
    "literata":       ("latin", "latin/literata/Literata[opsz,wght].ttf", "Literata"),
    "sourceserif4":   ("latin", "latin/sourceserif4/SourceSerif4[opsz,wght].ttf", "Source Serif 4"),
    "ibmplexsans":    ("latin", "latin/ibmplexsans/IBMPlexSans[wdth,wght].ttf", "IBM Plex Sans"),
    "publicsans":     ("latin", "latin/publicsans/PublicSans[wght].ttf", "Public Sans"),
    "worksans":       ("latin", "latin/worksans/WorkSans[wght].ttf", "Work Sans"),
    "instrumentsans": ("latin", "latin/instrumentsans/InstrumentSans[wdth,wght].ttf", "Instrument Sans"),
    "archivo":        ("latin", "latin/archivo/Archivo[wdth,wght].ttf", "Archivo"),
    "sourcesans3":    ("latin", "latin/sourcesans3/SourceSans3[wght].ttf", "Source Sans 3"),
    "librefranklin":  ("latin", "latin/librefranklin/LibreFranklin[wght].ttf", "Libre Franklin"),
    "robotoflex":     ("latin", "latin/robotoflex/RobotoFlex[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,opsz,slnt,wdth,wght].ttf", "Roboto Flex"),

    # --- Bangla ---
    "notosansbengali":   ("bangla", "bangla/notosansbengali/NotoSansBengali[wdth,wght].ttf", "Noto Sans Bengali"),
    "notoserifbengali":  ("bangla", "bangla/notoserifbengali/NotoSerifBengali[wdth,wght].ttf", "Noto Serif Bengali"),
    "notosansbengaliui": ("bangla", "bangla/notosansbengaliui/NotoSansBengaliUI[wdth,wght].ttf", "Noto Sans Bengali UI"),
    "anekbangla":        ("bangla", "bangla/anekbangla/AnekBangla[wdth,wght].ttf", "Anek Bangla"),
    "hindsiliguri":      ("bangla", "bangla/hindsiliguri/HindSiliguri-Regular.ttf", "Hind Siliguri"),
    "balooda2":          ("bangla", "bangla/balooda2/BalooDa2[wght].ttf", "Baloo Da 2"),
    "tirobangla":        ("bangla", "bangla/tirobangla/TiroBangla-Regular.ttf", "Tiro Bangla"),
    "galada":            ("bangla", "bangla/galada/Galada-Regular.ttf", "Galada"),
    "atma":              ("bangla", "bangla/atma/Atma-Regular.ttf", "Atma"),
    "mina":              ("bangla", "bangla/mina/Mina-Regular.ttf", "Mina"),

    # --- Mono ---
    "jetbrainsmono": ("mono", "mono/jetbrainsmono/JetBrainsMono[wght].ttf", "JetBrains Mono"),
    "ibmplexmono":   ("mono", "mono/ibmplexmono/IBMPlexMono-Regular.ttf", "IBM Plex Mono"),
    "sourcecodepro": ("mono", "mono/sourcecodepro/SourceCodePro[wght].ttf", "Source Code Pro"),
    "robotomono":    ("mono", "mono/robotomono/RobotoMono[wght].ttf", "Roboto Mono"),
    "geistmono":     ("mono", "mono/geistmono/GeistMono[wght].ttf", "Geist Mono"),
    "martianmono":   ("mono", "mono/martianmono/MartianMono[wdth,wght].ttf", "Martian Mono"),
    "inconsolata":   ("mono", "mono/inconsolata/Inconsolata[wdth,wght].ttf", "Inconsolata"),
    "notosansmono":  ("mono", "mono/notosansmono/NotoSansMono[wdth,wght].ttf", "Noto Sans Mono"),
}

# ---------------------------------------------------------------------------
# 2. The pairings under test. Each is Latin + Bangla + mono.
# ---------------------------------------------------------------------------
PAIRINGS: dict[str, dict] = {
    "01-core-modern": {
        "title": "Core Modern",
        "latin": "inter", "bangla": "notosansbengali", "mono": "jetbrainsmono",
        "note": "Neutral software-native sans with an optical-size axis, paired with the most broadly engineered Bangla sans.",
    },
    "02-technical": {
        "title": "Technical",
        "latin": "ibmplexsans", "bangla": "notosansbengali", "mono": "ibmplexmono",
        "note": "Engineering register: text and mono drawn as one family, so code and prose sit together without a seam.",
    },
    "03-editorial": {
        "title": "Editorial",
        "latin": "newsreader", "bangla": "notoserifbengali", "mono": "sourcecodepro",
        "note": "Serif on both sides with a wide optical-size range on the Latin; reads as writing rather than interface.",
    },
    "04-rooted-scholarly": {
        "title": "Rooted / Scholarly",
        "latin": "literata", "bangla": "tirobangla", "mono": "ibmplexmono",
        "note": "Tiro Bangla is drawn from Bengali calligraphic sources by Fiona Ross and John Hudson; Literata brings an optical-size axis.",
    },
    "05-rooted-familiar": {
        "title": "Rooted / Familiar",
        "latin": "sourcesans3", "bangla": "hindsiliguri", "mono": "sourcecodepro",
        "note": "Hind Siliguri is the Bangla face Bangladeshi readers meet most often on screen; Source keeps the Latin quiet beside it.",
    },
    "06-civic-systemic": {
        "title": "Civic / Systemic",
        "latin": "publicsans", "bangla": "notosansbengali", "mono": "notosansmono",
        "note": "Institutional and plain. Noto Sans Bengali and Noto Sans Mono are built to a shared metric brief.",
    },
    "07-contemporary": {
        "title": "Contemporary",
        "latin": "archivo", "bangla": "anekbangla", "mono": "martianmono",
        "note": "Both text faces carry a width axis as well as weight, so the pair can compress together rather than separately.",
    },
    # Added after measurement. Pairing 03 is the natural editorial choice but
    # fails on size parity: Newsreader's small x-height forces the Bangla down
    # to 11.33px against 16px Latin. Swapping in Literata, whose x-height is a
    # full pixel taller at body size, and keeping Noto Serif Bengali for its
    # full weight range, fixes that without leaving the editorial register.
    "08-editorial-revised": {
        "title": "Editorial (revised)",
        "latin": "literata", "bangla": "notoserifbengali", "mono": "ibmplexmono",
        "note": "The editorial direction rebuilt around size parity: Literata's taller x-height "
                "lifts the Bangla multiplier from 0.708 to 0.816, and Noto Serif Bengali keeps a "
                "full weight range where Tiro Bangla has only one.",
    },
}

# ---------------------------------------------------------------------------
# 3. Specimen copy. The Bangla is written as Bangla, not translated from the
#    English; the two paragraphs say related things in their own idiom.
# ---------------------------------------------------------------------------
COPY = {
    "name_latin": "aninda studio",
    "name_bangla": "অনিন্দ্য স্টুডিও",

    "head_latin": "One person, two languages, one standard of work",
    "head_bangla": "একজন মানুষ, দুইটি ভাষা, কাজের একটিই মান",

    "body_latin": (
        "Aninda Studio is one person's work. Software is made here from a single "
        "room in Barishal — slowly, attentively, one thing at a time. There is no "
        "committee to satisfy, so decisions do not sit waiting; only what is "
        "actually needed gets built. Institutions inside the country and clients "
        "outside it are given the same attention and the same care. Every project "
        "begins with three questions: who will genuinely use this, how long must "
        "it keep working, and who repairs it on the day it breaks."
    ),
    "body_bangla": (
        "অনিন্দ্য স্টুডিও একজন মানুষের কাজ। বরিশালের একটি ঘর থেকেই সফটওয়্যার তৈরি হয় — "
        "ধীরে, মন দিয়ে, একটার পর একটা। বড় দলের ভিড় নেই, তাই সিদ্ধান্ত নিতে দেরিও হয় না; "
        "যতটুকু দরকার ঠিক ততটুকুই বানানো হয়। দেশের ভেতরের প্রতিষ্ঠান আর দেশের বাইরের "
        "ক্লায়েন্ট — দুই পক্ষের কাজেই সমান মনোযোগ দেওয়া হয়। প্রতিটি প্রকল্পে তিনটি প্রশ্ন "
        "আগে করা হয়: এটি আসলে কার কাজে লাগবে, কতদিন টিকবে, আর ভেঙে গেলে কে সারাবে।"
    ),
    "caption_latin": "Built in Barishal, Bangladesh · available worldwide · est. 2026",
    "caption_bangla": "বরিশাল, বাংলাদেশ থেকে তৈরি · সারা পৃথিবীতে পাওয়া যায় · ২০২৬ সাল থেকে",

    # Mono test line: digits, and the six characters that are most often
    # confused with one another in code.
    "mono_digits": "0123456789  ০১২৩৪৫৬৭৮৯",
    "mono_confusable": "0 O o 1 l I  ·  rn m  ·  {} [] () <>  ·  ; : , .",
    "mono_code": 'const মাত্রা = "matra";  if (x !== 0) return [1, l, I, O];',

    # Bangla shaping tests.
    "conjuncts": "ক্ষ  ত্র  জ্ঞ  ঙ্গ  ন্দ্য  স্ত্র",
    "conjuncts_more": "ক্ত  ষ্ট  হ্ম  দ্ব  ঞ্চ  ণ্ড  ক্ল  শ্ব  স্ক্র  ত্ত",
    "matra_word": "কলকাতা",           # every letter carries a matra: unbroken headline
    "matra_sentence": "বরিশাল শহরের কারিগরি কাজ",
    "descender_line": "রুগ্ন হৃদয়ে কৃষ্ণচূড়া ফুটেছে",   # below-base forms and descenders
    "matra_line": "কলকাতা বরিশাল ঢাকা চট্টগ্রাম",       # heavy headline on the following line
}


# ---------------------------------------------------------------------------
# Step 1 — read the facts out of the font files themselves.
# ---------------------------------------------------------------------------
def collect_font_facts() -> dict:
    from fontTools.ttLib import TTFont
    from fontTools.pens.boundsPen import BoundsPen

    def name(font, nid):
        t = font["name"]
        for pid, eid, lid in ((3, 1, 0x409), (1, 0, 0), (3, 10, 0x409)):
            r = t.getName(nid, pid, eid, lid)
            if r:
                try:
                    return str(r)
                except Exception:
                    pass
        return None

    facts = {}
    for key, (script, rel, human) in REGISTRY.items():
        path = CANDIDATES / rel
        if not path.exists():
            print(f"  !! missing font file: {path}", file=sys.stderr)
            continue
        f = TTFont(path, lazy=True)
        upem = f["head"].unitsPerEm
        os2, hhea = f["OS/2"], f["hhea"]
        cmap = f.getBestCmap()
        gs = f.getGlyphSet()

        def ink(ch):
            g = cmap.get(ord(ch))
            if not g:
                return None
            p = BoundsPen(gs)
            try:
                gs[g].draw(p)
            except Exception:
                return None
            return p.bounds

        def top(ch):
            b = ink(ch)
            return None if not b else round(b[3] / upem, 4)

        axes = []
        if "fvar" in f:
            axes = [{"tag": a.axisTag, "min": a.minValue, "def": a.defaultValue, "max": a.maxValue}
                    for a in f["fvar"].axes]
        instances = []
        if "fvar" in f:
            instances = [name(f, i.subfamilyNameID) for i in f["fvar"].instances]

        # Licence and Reserved Font Name, read from the OFL.txt sitting beside
        # the font, not from anything remembered or assumed.
        ofl = path.parent / "OFL.txt"
        txt = ofl.read_text(encoding="utf-8", errors="replace") if ofl.exists() else ""
        rfn = sorted({m.strip().strip('.,"‘’\'')
                      for m in re.findall(r"with Reserved Font Names?\s*[:\-]?\s*([^\n.]+)", txt)})
        if "SIL OPEN FONT LICENSE" in txt.upper():
            licence = "SIL OFL 1.1"
        elif "apache license" in txt.lower():
            licence = "Apache-2.0"
        else:
            licence = "UNKNOWN"

        cps = set(cmap.keys())
        facts[key] = {
            "key": key, "script": script, "human": human,
            "file": path.name, "path": rel(path),
            "family_name": name(f, 16) or name(f, 1),
            "version": name(f, 5), "designer": name(f, 9), "manufacturer": name(f, 8),
            "copyright": (name(f, 0) or "")[:400],
            "licence": licence, "licence_file": rel(ofl), "rfn": rfn,
            "upem": upem,
            "variable": bool(axes), "axes": axes, "named_instances": instances,
            "os2_capHeight": getattr(os2, "sCapHeight", None),
            "os2_xHeight": getattr(os2, "sxHeight", None),
            "os2_typoAscender": os2.sTypoAscender, "os2_typoDescender": os2.sTypoDescender,
            "os2_typoLineGap": os2.sTypoLineGap,
            "os2_winAscent": os2.usWinAscent, "os2_winDescent": os2.usWinDescent,
            "use_typo_metrics": bool(os2.fsSelection & (1 << 7)),
            "hhea_ascender": hhea.ascent, "hhea_descender": hhea.descent,
            "hhea_lineGap": hhea.lineGap,
            "default_line_box_em": round(
                (os2.sTypoAscender - os2.sTypoDescender + os2.sTypoLineGap) / upem, 4),
            "glyph_H_em": top("H"), "glyph_x_em": top("x"), "glyph_ka_em": top("ক"),
            "coverage_bengali": sum(1 for c in range(0x0980, 0x0A00) if c in cps),
            "coverage_bengali_digits": sum(1 for c in range(0x09E6, 0x09F0) if c in cps),
            "coverage_latin_letters": sum(1 for c in range(0x41, 0x7B) if c in cps),
            "num_glyphs": f["maxp"].numGlyphs,
        }
        f.close()

    (DATA / "font_facts.json").write_text(
        json.dumps(facts, indent=1, ensure_ascii=False), encoding="utf-8")
    return facts


# ---------------------------------------------------------------------------
# CSS helpers
# ---------------------------------------------------------------------------
def face_css(facts: dict, keys: list[str] | None = None) -> str:
    """
    One @font-face rule per candidate, pointing at the local .ttf.

    Pass `keys` to emit rules for only the families a given page needs; that
    keeps each page small and fast, which matters because the line-height
    search reloads a page for every step it tries.
    """
    out = []
    for key in (keys if keys is not None else list(facts)):
        fx = facts[key]
        uri = absolute(fx["path"]).as_uri()
        wght = next((a for a in fx["axes"] if a["tag"] == "wght"), None)
        wdth = next((a for a in fx["axes"] if a["tag"] == "wdth"), None)
        w = f"{int(wght['min'])} {int(wght['max'])}" if wght else "400"
        s = f"{wdth['min']}% {wdth['max']}%" if wdth else "100%"
        out.append(
            f'@font-face{{font-family:"{key}";src:url("{uri}") format("truetype");'
            f"font-weight:{w};font-stretch:{s};font-style:normal;font-display:block;}}"
        )
    return "\n".join(out)


def shape_bangla(facts: dict) -> dict:
    """
    Ask HarfBuzz — the same shaping engine browsers use — to lay out a set of
    Bangla conjuncts and words with each Bangla face, and check for the three
    ways shaping fails:

      - a missing glyph (.notdef, glyph id 0)
      - an inserted dotted circle (U+25CC), the standard signal that the shaper
        could not make sense of the sequence
      - a visible hasanta (U+09CD) left showing where a joined form was expected

    This is a test for FAILURE. Passing means nothing is broken; it does not
    mean the conjuncts are well drawn, which only a Bangla reader can judge.
    """
    import uharfbuzz as hb
    from fontTools.ttLib import TTFont

    conjuncts = ["ক্ষ", "ত্র", "জ্ঞ", "ঙ্গ", "ন্দ্য", "স্ত্র", "ক্ত", "ষ্ট",
                 "হ্ম", "দ্ব", "ঞ্চ", "ণ্ড", "ক্ল", "শ্ব", "স্ক্র", "ত্ত"]
    words = {
        "studio_name": COPY["name_bangla"],
        "reph": "কর্ম", "ya_phala": "বিদ্যা", "hard": "স্বাস্থ্য",
        "digits": "০১২৩৪৫৬৭৮৯",
    }
    DOTTED, VIRAMA = 0x25CC, 0x09CD

    out = {}
    for key, fx in facts.items():
        if fx["script"] != "bangla":
            continue
        tt = TTFont(str(absolute(fx["path"])), lazy=True)
        cmap, order = tt.getBestCmap(), tt.getGlyphOrder()
        dotted = order.index(cmap[DOTTED]) if DOTTED in cmap else None
        virama = order.index(cmap[VIRAMA]) if VIRAMA in cmap else None
        tt.close()

        face = hb.Face(absolute(fx["path"]).read_bytes())
        font = hb.Font(face)

        def run(text):
            buf = hb.Buffer()
            buf.add_str(text)
            buf.guess_segment_properties()
            hb.shape(font, buf)
            return [g.codepoint for g in buf.glyph_infos]

        rec = {"family": fx["human"], "conjuncts": {}, "words": {}, "failures": []}
        for cj in conjuncts:
            gids = run(cj)
            bad = {
                "notdef": 0 in gids,
                "dotted_circle": dotted is not None and dotted in gids,
                "visible_hasanta": virama is not None and virama in gids,
            }
            ok = not any(bad.values())
            rec["conjuncts"][cj] = {"in_chars": len(cj), "out_glyphs": len(gids),
                                    "formed": ok, **bad}
            if not ok:
                rec["failures"].append(cj)
        for name, w in words.items():
            gids = run(w)
            rec["words"][name] = {
                "text": w, "in_chars": len(w), "out_glyphs": len(gids),
                "notdef": 0 in gids,
                "dotted_circle": dotted is not None and dotted in gids,
            }
        rec["passed"] = f"{len(conjuncts) - len(rec['failures'])}/{len(conjuncts)}"
        out[key] = rec
    return out


def load_html(page, html: str, tag: str = "page") -> None:
    """
    Write the page to a real file and navigate to it over file://.

    Chromium refuses to fetch a file:// font from an about:blank document, which
    is what set_content() produces, so every page here is served from disk
    instead. Chromium is launched with --allow-file-access-from-files to permit
    the font requests.
    """
    tmp = DATA / f"_render_{tag}.html"
    tmp.write_text(html, encoding="utf-8")
    page.goto(tmp.as_uri(), wait_until="load")


def opsz_for(fx: dict, px: float) -> str:
    """
    If the family has an optical-size axis, return a font-variation-settings
    value pinning it to the size actually being used (clamped to the axis
    range). Families without the axis get an empty string.
    """
    a = next((a for a in fx["axes"] if a["tag"] == "opsz"), None)
    if not a:
        return ""
    v = max(a["min"], min(a["max"], px))
    return f'font-variation-settings:"opsz" {v:.1f};'


# ---------------------------------------------------------------------------
# Step 2 — measure real rendered ink in the browser.
# ---------------------------------------------------------------------------
MEASURE_JS = r"""
(payload) => {
  const {keys, probes, sizes} = payload;
  const cv = document.createElement('canvas');
  const ctx = cv.getContext('2d');
  const out = {};
  for (const k of keys) {
    out[k] = {};
    for (const size of sizes) {
      const rec = {};
      ctx.font = `400 ${size}px "${k}"`;
      for (const [pname, text] of Object.entries(probes)) {
        const m = ctx.measureText(text);
        rec[pname] = {
          // ink extents above and below the baseline, in CSS pixels
          ascent:  m.actualBoundingBoxAscent,
          descent: m.actualBoundingBoxDescent,
          width:   m.width,
          left:    m.actualBoundingBoxLeft,
          right:   m.actualBoundingBoxRight
        };
      }
      // font-declared metrics the browser will actually use
      const fm = ctx.measureText('Hxকy');
      rec._font = {
        fontAscent:  fm.fontBoundingBoxAscent,
        fontDescent: fm.fontBoundingBoxDescent
      };
      // the line box the browser gives this font at line-height:normal
      const el = document.createElement('div');
      el.style.cssText = `position:absolute;visibility:hidden;white-space:nowrap;`
        + `font:400 ${size}px "${k}";line-height:normal;`;
      el.textContent = 'Hxকy';
      document.body.appendChild(el);
      rec._lineBoxNormal = el.getBoundingClientRect().height;
      el.remove();
      out[k][size] = rec;
    }
  }
  return out;
}
"""

PROBES = {
    "cap_H": "H",
    "x_height": "x",
    "asc_d": "d",
    "desc_p": "p",
    "latin_word": "aninda studio",
    # Bangla: 'ক' runs from the baseline up to the matra, so its ink ascent is
    # the Bangla equivalent of an x-height — the height the eye actually reads.
    "bangla_ka": "ক",
    "bangla_tall": "ই",
    "bangla_word": "অনিন্দ্য স্টুডিও",
    "bangla_matra_word": COPY["matra_word"],
    "bangla_desc": COPY["descender_line"],
    "bangla_matraline": COPY["matra_line"],
    "conjuncts": COPY["conjuncts"],
    "digits": "0123456789",
}


# The sizes the design system actually uses, plus 100 as a high-precision
# reference. Optical-size families redraw themselves at each of these, so the
# Latin:Bangla ratio has to be measured at every one rather than measured once
# and scaled.
SIZES = (11, 12, 16, 28, 56, 100)


def measure(page, facts, sizes=SIZES):
    keys = list(facts.keys())
    page.evaluate("""async (keys) => {
        await Promise.all(keys.map(k => document.fonts.load(`400 16px "${k}"`)));
        await Promise.all(keys.map(k => document.fonts.load(`400 100px "${k}"`)));
        await document.fonts.ready;
    }""", keys)
    return page.evaluate(MEASURE_JS, {"keys": keys, "probes": PROBES, "sizes": list(sizes)})


# ---------------------------------------------------------------------------
# Step 3 — matra continuity, measured from pixels.
# ---------------------------------------------------------------------------
def matra_continuity(page, facts) -> dict:
    """
    Render one Bangla word in which every letter carries a matra, then read the
    rendered pixels to answer two separate questions.

    1. CONTINUITY. The matra joins the letters of a word into one connected
       stroke along the top. So the test is: does every single column of pixels
       across the word carry ink in the upper band of the letterform? Reported
       as the longest unbroken run of such columns divided by the word's inked
       width, so 1.00 means the headline runs right across the word as Bangla
       requires and anything less means it breaks somewhere.

       Two earlier versions of this test were wrong and were discarded. Scanning
       a single pixel row failed any face whose matra is tapered or sloped.
       Walking the topmost-ink edge failed any face that has letter parts rising
       ABOVE the matra, reading those as breaks. Only the band test is sound.

    2. THICKNESS. How thick the matra is, as a fraction of the em. This is the
       measurement that actually separates these faces, and it has a practical
       consequence: a matra thinner than about one device pixel at small sizes
       will grey out or drop away on an ordinary screen.
    """
    from PIL import Image

    results = {}
    bangla = [k for k, fx in facts.items() if fx["script"] == "bangla"]
    for k in bangla:
        load_html(page, f"""<!doctype html><meta charset="utf-8"><style>
          {face_css(facts, [k])}
          html,body{{margin:0;background:#fff;}}
          /* generous padding so no ink is clipped out of the element box,
             which would corrupt the pixel measurement */
          #w{{display:inline-block;font:400 240px "{k}";color:#000;
              line-height:1.9;padding:120px 60px;white-space:nowrap;}}
        </style><div id="w">{COPY['matra_word']}</div>""", "matra")
        page.evaluate("async () => { await document.fonts.ready; }")
        page.wait_for_timeout(120)
        out = CROPS / f"matra_{k}.png"
        page.locator("#w").screenshot(path=str(out))

        im = Image.open(out).convert("L")
        w, h = im.size
        px = im.load()
        ink = [[px[x, y] < 128 for x in range(w)] for y in range(h)]

        cols = [x for x in range(w) if any(ink[y][x] for y in range(h))]
        rows = [y for y in range(h) if any(ink[y][x] for x in range(w))]
        if not cols or not rows:
            results[k] = {"error": "no ink rendered"}
            continue
        x0, x1 = min(cols), max(cols)
        y0, y1 = min(rows), max(rows)
        ink_w = x1 - x0 + 1
        ink_h = y1 - y0 + 1

        # A column carries the headline if it has ink anywhere in the upper
        # band of the letterform. The band is generous so that a tapered or
        # slightly sloped matra still counts.
        band_lo, band_hi = y0, y0 + max(1, int(ink_h * 0.55))
        carries = [any(ink[y][x] for y in range(band_lo, band_hi + 1))
                   for x in range(x0, x1 + 1)]
        best_run = cur = 0
        for c in carries:
            cur = cur + 1 if c else 0
            best_run = max(best_run, cur)

        # Matra thickness: at each column take the topmost ink and count how
        # many rows of ink continue unbroken below it. The median across the
        # word is the headline's thickness.
        thicks = []
        for x in range(x0, x1 + 1):
            t = next((y for y in range(y0, y1 + 1) if ink[y][x]), None)
            if t is None:
                continue
            n = 0
            y = t
            while y <= y1 and ink[y][x]:
                n += 1
                y += 1
            thicks.append(n)
        thicks.sort()
        med = thicks[len(thicks) // 2] if thicks else 0
        thick_em = med / 240.0

        results[k] = {
            "word": COPY["matra_word"],
            "render_px": 240,
            "ink_width_px": ink_w,
            "ink_height_px": ink_h,
            "band_rows_searched": [0, band_hi - y0],
            "columns_carrying_headline": sum(carries),
            "columns_total": len(carries),
            "longest_unbroken_run_px": best_run,
            "continuity_ratio": round(best_run / ink_w, 4),
            "matra_thickness_px_at_240": med,
            "matra_thickness_em": round(thick_em, 5),
            "matra_thickness_px_at_16": round(thick_em * 16, 3),
            "matra_thickness_px_at_11": round(thick_em * 11, 3),
            "crop": rel(out),
        }
    return results


# ---------------------------------------------------------------------------
# Step 4 — smallest line-height at which two Bangla lines stop touching.
# ---------------------------------------------------------------------------
def line_height_floor(page, facts, size_px=40, lo=1.00, hi=2.60, step=0.05) -> dict:
    """
    Stack a descender-heavy Bangla line above a matra-heavy one and increase
    line-height until the two lines' ink separates into two distinct
    horizontal bands with clear white between them. Reports the first
    line-height that achieves separation.
    """
    from PIL import Image

    results = {}
    bangla = [k for k, fx in facts.items() if fx["script"] == "bangla"]
    for k in bangla:
        found = None
        lh = lo
        while lh <= hi + 1e-9:
            load_html(page, f"""<!doctype html><meta charset="utf-8"><style>
              {face_css(facts, [k])}
              html,body{{margin:0;background:#fff;}}
              /* vertical padding so ink overflowing a tight line box is still
                 inside the screenshot and therefore still measured */
              #b{{display:inline-block;font:400 {size_px}px "{k}";color:#000;
                  line-height:{lh:.2f};white-space:nowrap;padding:100px 12px;}}
            </style><div id="b">{COPY['descender_line']}<br>{COPY['matra_line']}</div>""", "lh")
            page.evaluate("async () => { await document.fonts.ready; }")
            page.wait_for_timeout(30)
            out = CROPS / f"lh_{k}.png"
            page.locator("#b").screenshot(path=str(out))
            im = Image.open(out).convert("L")
            w, h = im.size
            px = im.load()
            inked_rows = [any(px[x, y] < 128 for x in range(w)) for y in range(h)]
            # count contiguous bands of inked rows
            bands, prev = 0, False
            for r in inked_rows:
                if r and not prev:
                    bands += 1
                prev = r
            if bands >= 2:
                found = round(lh, 2)
                break
            lh += step
        results[k] = {
            "font_size_px": size_px,
            "min_line_height_unitless": found,
            "min_line_height_px_at_16": None if found is None else round(found * 16, 2),
            "method": "two stacked Bangla lines; first line-height at which rendered ink "
                      "separates into two distinct horizontal bands",
            "line_1": COPY["descender_line"],
            "line_2": COPY["matra_line"],
        }
    return results


# ---------------------------------------------------------------------------
# Step 5 — render one specimen page per pairing.
# ---------------------------------------------------------------------------
def specimen_html(pair_key, pair, facts, scales: dict) -> str:
    """
    `scales` maps each size used on the page to the Bangla multiplier measured
    at that size. Optical-size Latin families change x-height as they grow, so
    a single multiplier would be wrong at three of the four steps.
    """
    L, B, M = pair["latin"], pair["bangla"], pair["mono"]
    fl, fb, fm = facts[L], facts[B], facts[M]
    bangla_scale = scales[16]

    def sc(px):
        """The multiplier measured at this size (nearest measured size)."""
        return scales.get(px) or scales[min(scales, key=lambda s: abs(s - px))]

    def bsize(px):
        """Bangla px value corrected so it reads the same size as the Latin."""
        return round(px * sc(px), 2)

    css = f"""
    {face_css(facts, [L, B, M])}
    :root {{ --rule:#d9d6d0; --ink:#141414; --mute:#6b6660; --bg:#fbfaf8;
             --accent:#8a3a2a; }}
    *{{box-sizing:border-box;}}
    html,body{{margin:0;background:var(--bg);color:var(--ink);
      -webkit-font-smoothing:antialiased;}}
    body{{width:1400px;padding:56px 64px 64px;}}
    .lat{{font-family:"{L}";}}
    .ban{{font-family:"{B}";}}
    .mon{{font-family:"{M}";}}

    header{{display:flex;justify-content:space-between;align-items:baseline;
      border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:34px;}}
    header .t{{font-family:"{M}";font-size:13px;letter-spacing:.14em;
      text-transform:uppercase;}}
    header .n{{font-family:"{M}";font-size:12px;color:var(--mute);}}

    .grid{{display:grid;grid-template-columns:1fr 1fr;gap:0 56px;}}
    .col{{min-width:0;}}
    .col + .col{{border-left:1px solid var(--rule);padding-left:56px;}}
    .lbl{{font-family:"{M}";font-size:11px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--mute);margin:0 0 10px;}}
    .sec{{margin-bottom:30px;}}
    .meta{{font-family:"{M}";font-size:11px;color:var(--mute);margin-top:6px;}}
    hr.r{{border:0;border-top:1px solid var(--rule);margin:30px 0;}}

    .disp-l{{font-size:56px;line-height:1.06;margin:0;font-weight:600;
      letter-spacing:-.02em;{opsz_for(fl,56)}}}
    .disp-b{{font-size:{bsize(56)}px;line-height:1.42;margin:0;font-weight:600;
      {opsz_for(fb,56)}}}
    .head-l{{font-size:28px;line-height:1.2;margin:0;font-weight:600;
      {opsz_for(fl,28)}}}
    .head-b{{font-size:{bsize(28)}px;line-height:1.55;margin:0;font-weight:600;
      {opsz_for(fb,28)}}}
    .body-l{{font-size:16px;line-height:1.62;margin:0;{opsz_for(fl,16)}}}
    .body-b{{font-size:{bsize(16)}px;line-height:{LH_TOKEN[B]};margin:0;
      {opsz_for(fb,16)}}}
    .cap-l{{font-size:12px;line-height:1.5;color:var(--mute);margin:0;
      {opsz_for(fl,12)}}}
    .cap-b{{font-size:{bsize(12)}px;line-height:1.6;color:var(--mute);margin:0;
      {opsz_for(fb,12)}}}

    .same{{font-size:16px;line-height:1.9;margin:0;}}
    .conj{{font-size:34px;line-height:1.75;margin:0;letter-spacing:.02em;}}
    .matra{{font-size:44px;line-height:1.5;margin:0;}}
    .monoblk{{font-size:15px;line-height:1.75;margin:0;white-space:pre-wrap;}}
    .small11{{font-size:11px;line-height:1.6;}}
    .swatch{{display:flex;gap:26px;align-items:baseline;flex-wrap:wrap;}}
    .foot{{margin-top:34px;border-top:2px solid var(--ink);padding-top:12px;
      font-family:"{M}";font-size:11px;color:var(--mute);line-height:1.7;}}
    .tag{{color:var(--accent);}}
    """

    def axes_str(fx):
        return ", ".join(f"{a['tag']} {a['min']:g}–{a['max']:g}" for a in fx["axes"]) or "static"

    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>

<header>
  <div class="t">Aninda Studio · Type Pairing {pair_key.split('-')[0]} · {pair['title']}</div>
  <div class="n">{fl['human']} + {fb['human']} + {fm['human']}</div>
</header>

<!-- 1. The studio name, both scripts, display size -->
<div class="grid sec">
  <div class="col">
    <p class="lbl">Display · 56px · Latin</p>
    <p class="disp-l lat">{COPY['name_latin']}</p>
    <p class="meta">{fl['human']} · {axes_str(fl)}</p>
  </div>
  <div class="col">
    <p class="lbl">Display · {bsize(56)}px · Bangla <span class="tag">(×{sc(56)})</span></p>
    <p class="disp-b ban">{COPY['name_bangla']}</p>
    <p class="meta">{fb['human']} · {axes_str(fb)}</p>
  </div>
</div>

<hr class="r">

<!-- 2. Heading -->
<div class="grid sec">
  <div class="col">
    <p class="lbl">Heading · 28px</p>
    <p class="head-l lat">{COPY['head_latin']}</p>
  </div>
  <div class="col">
    <p class="lbl">Heading · {bsize(28)}px</p>
    <p class="head-b ban">{COPY['head_bangla']}</p>
  </div>
</div>

<!-- 3. Running body text at the same measure -->
<div class="grid sec">
  <div class="col">
    <p class="lbl">Body · 16px</p>
    <p class="body-l lat">{COPY['body_latin']}</p>
  </div>
  <div class="col">
    <p class="lbl">Body · {bsize(16)}px · line-height {LH_TOKEN[B]}</p>
    <p class="body-b ban">{COPY['body_bangla']}</p>
  </div>
</div>

<!-- 4. Caption -->
<div class="grid sec">
  <div class="col">
    <p class="lbl">Caption · 12px</p>
    <p class="cap-l lat">{COPY['caption_latin']}</p>
  </div>
  <div class="col">
    <p class="lbl">Caption · {bsize(12)}px</p>
    <p class="cap-b ban">{COPY['caption_bangla']}</p>
  </div>
</div>

<hr class="r">

<!-- 5. Control: both scripts at the SAME nominal 16px, uncorrected -->
<div class="grid sec">
  <div class="col">
    <p class="lbl">Control · both at a flat 16px, no correction</p>
    <p class="same lat">aninda studio — Barishal</p>
  </div>
  <div class="col">
    <p class="lbl">&nbsp;</p>
    <p class="same ban">অনিন্দ্য স্টুডিও — বরিশাল</p>
  </div>
</div>

<hr class="r">

<!-- 6. Bangla shaping: conjuncts and matra -->
<div class="sec">
  <p class="lbl">Bangla conjuncts · {fb['human']}</p>
  <p class="conj ban">{COPY['conjuncts']}</p>
  <p class="conj ban">{COPY['conjuncts_more']}</p>
</div>
<div class="sec">
  <p class="lbl">মাত্রা running across whole words — the headline must not break</p>
  <p class="matra ban">{COPY['matra_word']} · {COPY['matra_sentence']}</p>
  <p class="matra ban">{COPY['name_bangla']}</p>
</div>
<div class="sec">
  <p class="lbl">Descenders and below-base forms against the following line</p>
  <p class="ban" style="font-size:26px;line-height:{LH_TOKEN[B]};margin:0;">
    {COPY['descender_line']}<br>{COPY['matra_line']}</p>
</div>

<hr class="r">

<!-- 7. Mono -->
<div class="sec">
  <p class="lbl">Monospace · {fm['human']} · {axes_str(fm)}</p>
  <p class="monoblk mon">{COPY['mono_digits']}</p>
  <p class="monoblk mon">{COPY['mono_confusable']}</p>
  <p class="monoblk mon">{COPY['mono_code']}</p>
  <p class="monoblk mon small11">11px · {COPY['mono_confusable']}</p>
</div>

<!-- 8. Small-size stress test at 11px, both scripts -->
<div class="grid sec">
  <div class="col">
    <p class="lbl">Stress · 11px Latin</p>
    <p class="lat" style="font-size:11px;line-height:1.55;margin:0;{opsz_for(fl,11)}">
      {COPY['body_latin'][:230]}</p>
  </div>
  <div class="col">
    <p class="lbl">Stress · {bsize(11)}px Bangla</p>
    <p class="ban" style="font-size:{bsize(11)}px;line-height:{LH_TOKEN[B]};margin:0;{opsz_for(fb,11)}">
      {COPY['body_bangla'][:230]}</p>
  </div>
</div>

<div class="foot">
  {pair['note']}<br>
  Latin {fl['human']} — {fl['licence']}{' · RFN: ' + ', '.join(fl['rfn']) if fl['rfn'] else ' · no Reserved Font Name'} · axes: {axes_str(fl)}<br>
  Bangla {fb['human']} — {fb['licence']}{' · RFN: ' + ', '.join(fb['rfn']) if fb['rfn'] else ' · no Reserved Font Name'} · axes: {axes_str(fb)}<br>
  Mono {fm['human']} — {fm['licence']}{' · RFN: ' + ', '.join(fm['rfn']) if fm['rfn'] else ' · no Reserved Font Name'} · axes: {axes_str(fm)}<br>
  Bangla size multiplier by step — 56px ×{sc(56)} · 28px ×{sc(28)} · 16px ×{sc(16)} · 12px ×{sc(12)} · 11px ×{sc(11)} —
  each derived from measured rendered ink at that size, not estimated.
  Bangla line-height floor measured at {LH_FLOOR.get(B)}; token set to {LH_TOKEN[B]}.
</div>

</body></html>"""


# populated at run time from measurement, used by specimen_html
LH_TOKEN: dict[str, float] = {}   # recommended line-height token per Bangla face
LH_FLOOR: dict[str, float] = {}   # measured collision floor per Bangla face


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    from playwright.sync_api import sync_playwright

    print("1/6  reading font files …")
    facts = collect_font_facts()
    print(f"     {len(facts)} families")

    print("2/6  shaping Bangla conjuncts with HarfBuzz …")
    shaping = shape_bangla(facts)
    bad = {k: v["failures"] for k, v in shaping.items() if v["failures"]}
    print(f"     {len(shaping)} Bangla faces tested, "
          f"{len(bad)} with shaping failures{': ' + str(bad) if bad else ''}")

    results = {"shaping": shaping}
    with sync_playwright() as p:
        # --allow-file-access-from-files lets a page served from file:// fetch
        # the font files sitting next to it on disk.
        browser = p.chromium.launch(args=["--allow-file-access-from-files"])

        # -- measurement pass -------------------------------------------------
        page = browser.new_page(viewport={"width": 1400, "height": 900},
                                device_scale_factor=1)
        load_html(page, f'<!doctype html><meta charset="utf-8">'
                        f"<style>{face_css(facts)}</style><body></body>", "measure")
        print("3/6  measuring rendered ink in Chromium …")
        ink = measure(page, facts)
        results["ink"] = ink

        print("4/6  measuring মাত্রা continuity from pixels …")
        results["matra"] = matra_continuity(page, facts)

        print("5/6  finding the line-height floor for each Bangla face …")
        results["line_height"] = line_height_floor(page, facts)
        page.close()

        # -- derive the Latin:Bangla size ratio, at every size ----------------
        # Compare like with like: the Latin x-height (what the eye reads as the
        # size of Latin text) against the Bangla baseline-to-matra height (what
        # the eye reads as the size of Bangla text). Both are read straight off
        # the rendered ink. Because optical-size families redraw themselves as
        # the size changes, this is computed separately at each size rather
        # than measured once and reused.
        def at(key, size, probe):
            return ink[key][str(size)][probe]["ascent"]

        ratios = {}
        for pk, pair in PAIRINGS.items():
            L, B = pair["latin"], pair["bangla"]
            per_size = {}
            for s in SIZES:
                lx, bk = at(L, s, "x_height"), at(B, s, "bangla_ka")
                per_size[s] = {
                    "latin_x_height_px": round(lx, 3),
                    "latin_x_height_em": round(lx / s, 4),
                    "bangla_matra_height_px": round(bk, 3),
                    "bangla_matra_height_em": round(bk / s, 4),
                    "bangla_appears_larger_by": round(bk / lx, 4),
                    "bangla_size_multiplier": round(lx / bk, 3),
                }
            ratios[pk] = {
                "latin": L, "bangla": B, "mono": pair["mono"],
                "per_size": per_size,
                # headline number: the multiplier at body size
                "bangla_size_multiplier_at_16": per_size[16]["bangla_size_multiplier"],
                "varies_with_size": len({v["bangla_size_multiplier"] for v in per_size.values()}) > 1,
            }
        results["ratios"] = ratios

        # Line-height token per Bangla face. The measured floor is where the
        # ink merely stops touching; running text needs air above that, so the
        # token is the floor plus a margin, rounded to a tidy 0.05 step.
        for k, v in results["line_height"].items():
            f = v["min_line_height_unitless"]
            LH_FLOOR[k] = f
            LH_TOKEN[k] = 1.9 if f is None else round(min(2.4, f + 0.35) * 20) / 20

        # -- render specimens -------------------------------------------------
        print("6/6  rendering specimens …")
        page = browser.new_page(viewport={"width": 1400, "height": 1200},
                                device_scale_factor=2)
        for pk, pair in PAIRINGS.items():
            scales = {s: ratios[pk]["per_size"][s]["bangla_size_multiplier"] for s in SIZES}
            html = specimen_html(pk, pair, facts, scales)
            load_html(page, html, f"spec_{pk}")
            page.evaluate("async () => { await document.fonts.ready; }")
            page.wait_for_timeout(300)
            out = SPECIMENS / f"{pk}.png"
            page.screenshot(path=str(out), full_page=True)
            print(f"     {out.name}  Bangla ×{scales[16]} @16px "
                  f"(×{scales[56]} @56px), line-height {LH_TOKEN[pair['bangla']]}")
        page.close()
        browser.close()

    results["line_height_tokens"] = LH_TOKEN
    results["pairings"] = PAIRINGS
    (DATA / "measurements.json").write_text(
        json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")

    # Remove the scratch HTML pages used to serve fonts over file://; they are
    # regenerated on every run and only clutter the folder.
    for tmp in DATA.glob("_render_*.html"):
        tmp.unlink()

    print(f"\nwrote {DATA/'measurements.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
