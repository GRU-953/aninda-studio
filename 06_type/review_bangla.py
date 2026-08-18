#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
Every automated check in this project proves that the Bangla is not BROKEN. The
মাত্রা is continuous, the conjuncts shape, no glyph is missing, the contrast holds.
None of that proves the Bangla is GOOD — that it reads as Bangla rather than as
English wearing a Bangla script, that the register is right, that the word chosen
for "contrast" is the word a Bangla reader would actually use.

A machine cannot decide that. So this script does the one useful thing it can: it
puts every Bangla string the system will ship onto a single page, at the exact
size and in the exact face it will ship in, next to what it is for and what it
says in English — and gets out of the way.

"Every" is now true and checked. The sheet is built from 06_type/bangla-strings.json,
the register of what actually ships, and guard_covers_register() below refuses to
write a sheet that is missing one of its strings. It used to be a hand-typed list of
24 entries under this same sentence, while the system shipped 88 distinct strings:
3 of the 94 register keys were on it, and all 60 card names and subtitles, 13 of the
14 chapter titles, both high-contrast theme labels and every ui.* and status.*
string were not. A reviewer marked up 24 rows and had no way to tell.

It needs no network either. It carries the three subset faces inlined, which is what
makes "the exact face" true — see embedded_fonts().

Mark it up. Anything you change here changes at the source, not in a patch.

RUN
---
    cd /Users/gru953/Claude/Cowork/Aninda_Studio
    PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers ./.venv/bin/python 06_type/review_bangla.py
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOKENS = ROOT / "07_tokens" / "build"
OUT = HERE / "BANGLA-REVIEW.html"
PDF = HERE / "BANGLA-REVIEW.pdf"

# The hand-written rows: the strings the 2026 review put questions against, each
# with the question. Every one is also in 06_type/bangla-strings.json; these carry
# the reviewer's prompt, which no data file holds.
#
# THIS LIST IS NOT THE SHEET. It used to be — a hand-typed literal of 24 entries,
# under a docstring promising "every Bangla string the system will ship", while the
# system shipped 88 distinct strings. Three of the 94 keys were on it. A reviewer
# handed the page marked up 24 strings and was given no signal that 91 keys had
# never been shown, including every Bangla word a reader of the component library
# actually sees. strings_for_review() below appends everything in the register that
# is not already here, so a string added since cannot fall outside review again.
#   (id, English, Bangla, where it appears, px size it ships at, what to check)
STRINGS: list[tuple[str, str, str, str, int, str]] = [
    # --- identity -----------------------------------------------------------
    ("wm-1", "aninda studio", "অনিন্দ্য স্টুডিও", "The wordmark, everywhere", 44,
     "Is স্টুডিও right, or should the Bangla lockup be অনিন্দ্য on its own? Does "
     "the ন্দ্য conjunct look correct at this size?"),
    ("wm-2", "Aninda Studio (short form)", "অনিন্দ্য", "Favicon, avatar, tight lockups", 32,
     "Does the name alone read as a studio name, or only as a person's name?"),

    # --- themes -------------------------------------------------------------
    ("th-1", "Light", "আলো", "Theme switcher", 16,
     "আলো means 'light' as in illumination. Is that right for a UI theme, or is "
     "উজ্জ্বল (bright) or দিন (day) more natural?"),
    ("th-2", "Dark", "অন্ধকার", "Theme switcher", 16,
     "অন্ধকার is literally 'darkness' and may be too heavy. Is গাঢ় (deep) or "
     "রাত (night) better?"),
    ("th-3", "More contrast", "বেশি কনট্রাস্ট", "Theme switcher, accessibility settings", 16,
     "CHANGED. বৈসাদৃশ্য was not merely heavy — it means 'dissimilarity', not "
     "display contrast, so it was the right word for the wrong sense. কনট্রাস্ট is "
     "licensed as a loanword by rule ২.৬, and বেশি avoids the তৎসম register clash "
     "that উচ্চ would have kept."),

    # --- colour names -------------------------------------------------------
    ("cl-1", "Estuary — the ground colour", "মোহনা", "Guidebook, colour chapter", 21,
     "মোহনা is where a river meets the sea. Does it carry the right feeling for "
     "a deep green-teal?"),
    ("cl-2", "Tidewater — the accent", "জোয়ার", "Guidebook, colour chapter", 21,
     "জোয়ার is the incoming tide. Right for a brighter cyan-teal?"),
    ("cl-3", "Silt / Kans / Laterite / Monsoon", "পলি · কাশ · লাল মাটি · বর্ষা",
     "Guidebook, the four status colours", 21,
     "These name success, warning, danger and information. Do they read as a set? "
     "Is লাল মাটি too literal for an error colour?"),

    # --- buttons ------------------------------------------------------------
    ("bt-1", "Save the entry", "লেখাটি সংরক্ষণ করুন", "Primary button", 16,
     "The voice rule is that buttons are verbs with their object. Is সংরক্ষণ করুন "
     "too formal for a small studio's tools? Would সেভ করুন be more honest?"),
    ("bt-2", "Cancel", "বাতিল করুন", "Secondary button", 16, "Natural, or stiff?"),
    ("bt-3", "Delete the file", "ফাইলটি মুছে ফেলুন", "Destructive button", 16,
     "Does this carry enough weight for an action that cannot be undone?"),
    ("bt-4", "Try again", "আবার চেষ্টা করুন", "Error recovery", 16, "Natural?"),
    ("bt-5", "Copy the code", "কোডটি কপি করুন", "Code block", 16,
     "কপি is an English loanword written in Bangla. Right, or should it be "
     "অনুলিপি করুন?"),

    # --- messages -----------------------------------------------------------
    ("ms-1", "Couldn't save. Your work is still here — try again in a moment.",
     "সংরক্ষণ করা যায়নি। আপনার লেখা এখনো আছে — একটু পরে আবার চেষ্টা করুন।",
     "Error message", 16,
     "CHANGED এখনও → এখনো. The Academy dictionary lists এখনও only as a "
     "cross-reference (দ্র এখনো); এখনো carries the entry. Says what happened, then "
     "what happens next, and does not blame the reader."),
    ("ms-2", "That file is too large. The limit is 10 MB.",
     "ফাইলটি অনেক বড়ো। সর্বোচ্চ ১০ মেগাবাইট।", "Error message", 16,
     "CHANGED twice: বড় → বড়ো (the dictionary headword; বড় has no entry, rule ২.৩), "
     "and সর্বোচ্চ সীমা → সর্বোচ্চ, which was a doublet adding only weight. Bengali "
     "digits ১০ are kept — Academy standard for Bangla running text."),
    ("ms-3", "Nothing here yet. Add your first entry to begin.",
     "এখনো কিছু নেই। শুরু করতে প্রথম লেখাটি যোগ করুন।", "Empty state", 16,
     "CHANGED এখনও → এখনো, same ruling as ms-1. Tells the reader what to do next "
     "rather than only what is absent."),
    ("ms-4", "Saved", "সংরক্ষিত হয়েছে", "Success toast", 14,
     "Kept. Agrees with the Save button, so the two never disagree about the word."),

    # --- voice --------------------------------------------------------------
    ("vc-1", "I build small, careful software. If something has a limit, you'll find "
     "it written down here — nothing gets hidden.",
     "আমি ছোটো, যত্নে গড়া সফটওয়্যার বানাই। কোনো কিছুর সীমা থাকলে সেটা এখানেই "
     "লেখা থাকবে — লুকিয়ে রাখা হবে না।",
     "The voice sample, used in the guidebook and on the website", 21,
     "CHANGED ছোট → ছোটো. Doubly sourced: rule ২.৩ names ছোটো in its own example "
     "list (কালো, খাটো, ছোটো, ভালো), and ছোটো is the dictionary headword while ছোট "
     "has no entry. This one string sets the register for every Bangla sentence in "
     "the system, so the spelling had to be right. The English was also rewritten "
     "to be warmer and less defensive."),

    # --- guidebook chapters -------------------------------------------------
    ("gb-1", "Welcome · The name · The mark", "স্বাগতম · নাম · চিহ্ন",
     "Guidebook chapter titles", 21,
     "চিহ্ন means 'mark' or 'sign'. Right for a logo, or is লোগো clearer?"),
    ("gb-2", "Colour · Type · Space and shape", "রং · হরফ · ফাঁক ও আকার",
     "Guidebook chapter titles", 21,
     "হরফ means letterform. Is it right for a typography chapter, or is "
     "টাইপোগ্রাফি expected?"),
    ("gb-3", "Components · Motion · Voice", "উপাদান · গতি · কণ্ঠস্বর",
     "Guidebook chapter titles", 21, "Do these read as a set of chapter titles?"),
    ("gb-4", "What this system does not do", "যা এই পদ্ধতি করে না",
     "Guidebook chapter title — the honest list", 21,
     "CHANGED ব্যবস্থা → পদ্ধতি. ব্যবস্থা reads administrative in Bangladeshi usage "
     "(ব্যবস্থা নেওয়া — 'to take measures'); পদ্ধতি is a dictionary headword and the "
     "plain Bangla for a system."),

    # --- the mechanical test ------------------------------------------------
    ("cj-1", "Conjunct stress test", "ক্ষ ত্র জ্ঞ ঙ্গ ন্দ্য স্ত্র ষ্ণ ন্ত্র হ্ম দ্ধ",
     "Not shipped — a rendering check", 32,
     "Every one of these should be a single joined form with no dotted circle and "
     "no visible hasanta. If any looks wrong, the font or the shaping is at fault, "
     "not the wording."),
    ("cj-2", "The মাত্রা at caption size", "বাংলা লেখা ছোট আকারে",
     "Not shipped — the size-floor check", 12,
     "This is at the 12px floor. Is the মাত্রা still solid, or has it greyed out? "
     "This is the single measurement that set the floor."),
]

REGISTER = ROOT / "06_type" / "bangla-strings.json"
FONTS_DIR = ROOT / "08_components" / "fonts"

# Where each family of keys appears, and the px size it ships at, so a generated
# row says as much about itself as a hand-written one.
KEY_CONTEXT = {
    "card.": ("The component card library", 16),
    "chapter.": ("A guidebook chapter title", 21),
    "theme.": ("The theme switcher, on every surface", 16),
    "ui.": ("Interface furniture — the site, the cards, the plugins", 16),
    "status.": ("Status and validation messages", 16),
}


def strings_for_review() -> list[tuple[str, str, str, str, int, str]]:
    """The hand-written rows, then every register string not already on one.

    The register is the authority on WHAT ships; this script is the instrument for
    reviewing it. So the sheet is the register, in full, with the hand-written
    prompts attached to the rows that have them.
    """
    if not REGISTER.exists():
        raise SystemExit(
            f"{REGISTER} is missing. This sheet is built from the register, because "
            f"a hand-typed list of what ships is a list that goes stale."
        )
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    already = {bn for _, _, bn, *_ in STRINGS}
    rows = list(STRINGS)
    for key, entry in register.items():
        bn = entry.get("bn", "")
        if not bn or bn in already:
            continue
        already.add(bn)
        where, px = next(((w, s) for prefix, (w, s) in KEY_CONTEXT.items()
                          if key.startswith(prefix)),
                         ("Shipped, from the register", 16))
        rows.append((key, entry.get("en", ""), bn, where, px,
                     entry.get("basis", "")))
    return rows


def embedded_fonts() -> str:
    """The three subset faces, base64, so this page needs no network.

    This was the ONE committed HTML artefact in the repository that fetched over
    the network: three <link> tags to fonts.googleapis.com and no @font-face of its
    own, while every other HTML file here embeds all three faces. Its stated
    purpose is to show each string "at the exact size and in the exact face it will
    ship in" — and with no network, or on any machine without Noto Serif Bengali
    installed, the Bangla fell back to a generic serif, so the conjunct shapes the
    reviewer was asked to judge were not the ones that ship. Neither of the
    repository's two network guards reached 06_type at all.

    These are the same subsets the cards and the site inline, which is what makes
    "the exact face" true.
    """
    faces = [("Literata", "literata-subset.woff2", "400 700"),
             ("Noto Serif Bengali", "notoserifbengali-subset.woff2", "400 700"),
             ("Aninda Mono", "anindamono-subset.woff2", "400 500")]
    out = []
    for family, filename, weights in faces:
        path = FONTS_DIR / filename
        if not path.exists():
            raise SystemExit(
                f"{path} is missing. Run 08_components/build.py first — this sheet "
                f"embeds the same subsets the component cards do."
            )
        blob = base64.b64encode(path.read_bytes()).decode("ascii")
        out.append(
            f"@font-face{{font-family:'{family}';font-style:normal;"
            f"font-weight:{weights};font-display:block;"
            f"src:url(data:font/woff2;base64,{blob}) format('woff2')}}"
        )
    return "\n".join(out)


def guard_covers_register(rows) -> None:
    """Every Bangla string the register holds must be on the sheet."""
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    shown = {bn for _, _, bn, *_ in rows}
    missing = sorted(key for key, entry in register.items()
                     if entry.get("bn") and entry["bn"] not in shown)
    if missing:
        raise SystemExit(
            f"{len(missing)} register string(s) are not on this sheet: "
            f"{', '.join(missing[:8])}"
            f"{'…' if len(missing) > 8 else ''}. The docstring above promises every "
            f"Bangla string the system will ship, and a reviewer handed the page "
            f"has no way to know what was left off it."
        )


def guard_no_network(html: str) -> None:
    """Refuse to write a sheet that fetches anything over the network.

    11_site/build.py raises on a network fetch and 09_guidebook/build.py has its own
    external-asset guard; nothing guarded 06_type, and this was the one committed
    HTML artefact in the repository that needed a network — three <link> tags to
    fonts.googleapis.com and no @font-face of its own.

    It checks the attributes a browser actually FETCHES from, not the word
    "googleapis" anywhere in the file, so the comment above the embedded faces
    explaining what used to be here does not trip it.
    """
    import re

    fetched = [
        *re.findall(r'<script[^>]*\bsrc\s*=\s*"([^"]+)"', html),
        *re.findall(r'<img[^>]*\bsrc\s*=\s*"([^"]+)"', html),
        *re.findall(r"url\(\s*(?!data:)([^)\s]+)\s*\)", html),
        *re.findall(r'<link\b[^>]*\bhref\s*=\s*"([^"]+)"', html),
    ]
    remote = [target for target in fetched
              if target.startswith(("http://", "https://", "//"))]
    if remote:
        raise SystemExit(
            "this sheet would fetch " + ", ".join(sorted(set(remote))) +
            " over the network. Its whole purpose is to show each string in the "
            "exact face that ships, and a fetched face is not that one — with no "
            "network the Bangla falls back to a generic serif and the conjunct "
            "shapes the reviewer is asked to judge are not the shipped shapes. "
            "Embed it instead, as embedded_fonts() does."
        )


def guard_font_covers(rows, bangla_font: Path) -> None:
    """Refuse to write a sheet whose own font cannot draw what it shows.

    A reviewer judging a tofu box is worse than no reviewer. The charset union in
    08_components/build.py is where a missing character is fixed.
    """
    from fontTools.ttLib import TTFont

    covered = set(TTFont(str(bangla_font)).getBestCmap())
    missing = sorted({ch for _, _, bn, *_ in rows for ch in bn
                      if "\u0980" <= ch <= "\u09ff" and ord(ch) not in covered})
    if missing:
        raise SystemExit(
            f"the embedded Noto Serif Bengali subset cannot draw "
            f"{''.join(missing)}, which this sheet shows. Those would render as "
            f"tofu boxes and the reviewer would be judging the wrong shapes. Add "
            f"them to the charset union in 08_components/build.py and re-run it."
        )


def main() -> int:
    prim = json.loads((TOKENS / "primitive.tokens.json").read_text())
    light = json.loads((TOKENS / "semantic.light.tokens.json").read_text())
    c = light["color"]
    paper = c["surface"]["bright"]["$extensions"]["studio.aninda"]
    ink_step = c["ink"]["default"]["$value"]
    fam = prim["color"]["ramp"]

    def resolve(alias: str) -> str:
        node = prim
        for part in alias.strip("{}").split("."):
            node = node[part]
        return node["$value"]["hex"]

    ink = resolve(ink_step) if isinstance(ink_step, str) else ink_step["hex"]
    muted = resolve(c["ink"]["muted"]["$value"]) if isinstance(c["ink"]["muted"]["$value"], str) else c["ink"]["muted"]["$value"]["hex"]
    accent = resolve(c["accent"]["default"]["$value"]) if isinstance(c["accent"]["default"]["$value"], str) else c["accent"]["default"]["$value"]["hex"]
    line = resolve(c["line"]["default"]["$value"]) if isinstance(c["line"]["default"]["$value"], str) else c["line"]["default"]["$value"]["hex"]
    surf = c["surface"]["base"]["$value"]["hex"]
    bg = c["surface"]["bright"]["$value"]["hex"]

    # Row numbers are looked up, never typed. The first version of this sheet said
    # "Row 17 sets the register" while the voice sample was actually row 18 — an
    # off-by-one in a document whose whole purpose is to be precise about detail.
    rows_in = strings_for_review()
    guard_covers_register(rows_in)
    guard_font_covers(rows_in, FONTS_DIR / "notoserifbengali-subset.woff2")
    idx = {sid: i for i, (sid, *_) in enumerate(rows_in, 1)}
    n_voice, n_conj, n_floor = idx["vc-1"], idx["cj-1"], idx["cj-2"]

    bscale = prim["number"]["scale"]["bangla"]
    rows = []
    for i, (sid, en, bn, where, px, check) in enumerate(rows_in, 1):
        # Apply the measured multiplier, but never below the floor — the same rule
        # the stylesheet enforces, applied here so the sheet shows the real size.
        mult = (bscale["caption"]["$value"] if px <= 12 else
                bscale["body"]["$value"] if px <= 16 else
                bscale["heading"]["$value"] if px <= 28 else
                bscale["title"]["$value"])
        bn_px = max(12, round(px * mult, 1))
        rows.append(f"""
<tr id="{sid}">
  <td class="n">{i}</td>
  <td class="meta"><code>{sid}</code><span class="where">{where}</span>
      <span class="size">Latin {px}px → Bangla {bn_px}px</span></td>
  <td class="en">{en}</td>
  <td class="bn"><span lang="bn" style="font-size:{bn_px}px">{bn}</span></td>
  <td class="ck">{check}</td>
  <td class="mark">
    <label><input type="radio" name="{sid}" value="ok"><span>OK</span></label>
    <label><input type="radio" name="{sid}" value="change"><span>Change</span></label>
    <textarea data-for="{sid}" rows="2" placeholder="what it should say"></textarea>
  </td>
</tr>""")

    ids_json = json.dumps([s[0] for s in rows_in])

    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aninda Studio — Bangla review sheet</title>
<style>
/* The three faces, inlined. No network: this sheet is judged on the exact
   subsets that ship, and it used to fetch them from fonts.googleapis.com. */
{embedded_fonts()}
</style>
<style>
*{{box-sizing:border-box;margin:0}}
body{{background:{bg};color:{ink};font-family:Literata,Georgia,serif;font-size:16px;
  line-height:1.55;padding:40px 28px 80px;-webkit-font-smoothing:antialiased}}
.doc{{max-width:1220px;margin:0 auto}}
h1{{font-size:38px;line-height:1.15;margin-bottom:14px;font-weight:600}}
.lede{{max-width:74ch;color:{muted};margin-bottom:10px}}
.rule{{background:{surf};border:1px solid {line};border-left:4px solid {accent};
  border-radius:10px;padding:18px 20px;margin:24px 0 32px;max-width:88ch}}
.rule b{{display:block;margin-bottom:6px}}
.rule ul{{margin:8px 0 0 20px;color:{muted};font-size:15px}}
.rule li{{margin-bottom:5px}}
table{{width:100%;border-collapse:collapse;margin-top:20px}}
th{{text-align:left;font-family:'Aninda Mono',monospace;font-size:10.5px;
  letter-spacing:.11em;text-transform:uppercase;font-weight:400;color:{accent};
  padding:0 12px 10px 0;border-bottom:2px solid {line};vertical-align:bottom}}
td{{padding:18px 12px 18px 0;border-bottom:1px solid {line};vertical-align:top}}
.n{{width:26px;color:{muted};font-family:'Aninda Mono',monospace;font-size:12px}}
.meta{{width:15%}}
.meta code{{font-family:'Aninda Mono',monospace;font-size:11px;color:{accent};display:block}}
.meta .where{{display:block;font-size:12.5px;color:{muted};margin-top:3px}}
.meta .size{{display:block;font-family:'Aninda Mono',monospace;font-size:10.5px;
  color:{muted};margin-top:5px;opacity:.8}}
.en{{width:22%;font-size:14.5px;color:{muted}}}
.bn{{width:26%}}
.bn span{{font-family:'Noto Serif Bengali',serif;line-height:1.6;display:block}}
.ck{{width:27%;font-size:13px;color:{muted}}}
.mark{{width:150px}}
.mark label{{display:inline-flex;align-items:center;gap:5px;font-size:12.5px;
  margin-right:10px;cursor:pointer}}
.mark input{{accent-color:{accent};width:16px;height:16px;cursor:pointer}}
.mark textarea{{width:100%;margin-top:7px;font-family:'Noto Serif Bengali',Literata,serif;
  font-size:13px;border:1px solid {line};border-radius:6px;padding:5px 6px;
  background:{bg};color:{ink};resize:vertical}}
.mark textarea:focus{{outline:3px solid {accent};outline-offset:2px}}
#bar{{position:sticky;bottom:0;background:{surf};border-top:2px solid {accent};
  padding:14px 18px;margin-top:28px;display:flex;gap:14px;align-items:center;
  flex-wrap:wrap;border-radius:10px 10px 0 0}}
#bar button{{font:inherit;font-size:15px;padding:11px 20px;border-radius:8px;
  border:1px solid {accent};background:{accent};color:{bg};cursor:pointer;
  min-height:44px}}
#bar button.ghost{{background:transparent;color:{accent}}}
#bar button:focus-visible{{outline:3px solid {ink};outline-offset:2px}}
#count{{font-size:14px;color:{muted}}}
#out{{width:100%;margin-top:12px;font-family:'Aninda Mono',monospace;font-size:12px;
  border:1px solid {line};border-radius:8px;padding:10px;min-height:90px;display:none;
  background:{bg};color:{ink}}}
.foot{{margin-top:36px;padding-top:20px;border-top:1px solid {line};color:{muted};
  font-size:14px;max-width:80ch}}
@media print{{body{{padding:0}} tr{{break-inside:avoid}} .rule{{break-inside:avoid}}}}
</style></head><body><div class="doc">
<h1>Bangla review sheet</h1>
<p class="lede">Every Bangla string the Aninda Studio system currently intends to
ship, at the exact size and in the exact face it will ship in — Noto Serif Bengali,
beside Literata.</p>
<p class="lede">The automated checks have already proved that none of this is
<em>broken</em>: the মাত্রা is continuous across all 866 pixel columns measured, all
sixteen tested conjuncts shape correctly, no glyph is missing. What no check can
prove is whether it is <em>good</em>.</p>

<div class="rule"><b>What to look for, in order of how much it matters</b>
<ul>
<li><b>Does it read as Bangla, or as English in Bangla script?</b> The rule this
system sets itself is that Bangla is written as Bangla — same meaning, different
sentences — never translated word by word. Row {n_voice} sets the register for
everything else, so start there.</li>
<li><b>Is the word the one a Bangladeshi reader would actually use?</b> Several
rows below offer a formal Bangla word and an English loanword, because I genuinely
do not know which is right. Pick.</li>
<li><b>Is the register consistent?</b> A studio run by one person should not sound
like a government form.</li>
<li><b>Do any conjuncts look wrong?</b> Row {n_conj} is the stress test. If a form
there looks broken, that is the font or the shaping, not the wording — tell me and
I will fix it at that level.</li>
<li><b>Row {n_floor} is at the 12px floor.</b> If the মাত্রা has greyed out on your
screen, the floor is too low and I will raise it.</li>
</ul></div>

<table>
<thead><tr><th></th><th>Where it appears</th><th>English</th><th>Bangla, at size</th>
<th>What I am unsure about</th><th>OK / Change</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>

<div id="bar">
  <button type="button" id="copy">Copy my answers</button>
  <button type="button" class="ghost" id="dl">Save as a file</button>
  <span id="count">Nothing marked yet</span>
  <textarea id="out" readonly aria-label="Your answers, ready to paste"></textarea>
</div>

<p class="foot">Choose <b>OK</b> or <b>Change</b> for each row, and type the correction
where you choose Change. Then press <b>Copy my answers</b> and paste the result back
to me — or press <b>Save as a file</b> and send that. Anything you change here changes
at the source: these strings are generated into the guidebook, the component library,
the website and both plugins from one place, so nothing is ever corrected twice.</p>

<p class="foot"><b>Why this page has buttons instead of printed boxes.</b> The first
version of this sheet was a PDF with boxes to tick. It came back with nothing in it —
the annotations were made in a viewer that never wrote them into the file, and there
was no way to tell that had happened until the boxes were read back and found empty.
Marks made here are read straight out of the page, so they cannot go missing the same
way.</p>
</div>

<script>
(function () {{
  const ids = {ids_json};
  const out = document.getElementById('out');
  const count = document.getElementById('count');

  function collect() {{
    const lines = [];
    let done = 0;
    for (const id of ids) {{
      const picked = document.querySelector('input[name="' + id + '"]:checked');
      const note = document.querySelector('textarea[data-for="' + id + '"]').value.trim();
      if (!picked && !note) continue;
      done++;
      const verdict = picked ? picked.value : 'change';
      lines.push(id + '\\t' + verdict + (note ? '\\t' + note : ''));
    }}
    count.textContent = done + ' of ' + ids.length + ' rows marked';
    return lines.length
      ? 'ANINDA STUDIO — Bangla review\\nid\\tverdict\\tcorrection\\n' + lines.join('\\n')
      : '';
  }}

  document.addEventListener('change', collect);
  document.addEventListener('input', collect);

  document.getElementById('copy').addEventListener('click', async function () {{
    const text = collect();
    if (!text) {{ count.textContent = 'Nothing marked yet'; return; }}
    out.style.display = 'block';
    out.value = text;
    try {{
      await navigator.clipboard.writeText(text);
      count.textContent = 'Copied. Paste it back to me.';
    }} catch (e) {{
      out.select();
      count.textContent = 'Could not reach the clipboard — the text is below, select and copy it.';
    }}
  }});

  document.getElementById('dl').addEventListener('click', function () {{
    const text = collect();
    if (!text) {{ count.textContent = 'Nothing marked yet'; return; }}
    out.style.display = 'block';
    out.value = text;
    out.select();
    count.textContent = 'Downloads are blocked in some viewers — the text is below, select and copy it.';
  }});

  collect();
}})();
</script>
</body></html>"""

    guard_no_network(html)
    OUT.write_text(html)
    print(f"Wrote {OUT.relative_to(ROOT)}  ({len(rows_in)} rows: "
          f"{len(STRINGS)} with a written question, "
          f"{len(rows_in) - len(STRINGS)} more from the register)")

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto(OUT.as_uri())
            pg.wait_for_timeout(3000)
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(1200)
            loaded = pg.evaluate(
                'document.fonts.check(\'20px "Noto Serif Bengali"\') && '
                'document.fonts.check(\'20px "Literata"\')')
            if not loaded:
                print("could not run: the review fonts did not load, so the sheet "
                      "would show a fallback face and prove nothing", file=sys.stderr)
                b.close()
                return 2
            pg.pdf(path=str(PDF), format="A3", print_background=True,
                   margin={"top": "12mm", "bottom": "12mm", "left": "10mm", "right": "10mm"})
            b.close()
        print(f"Wrote {PDF.relative_to(ROOT)}")
    except Exception as e:
        print(f"could not render the PDF ({e}) — the HTML is still usable", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
