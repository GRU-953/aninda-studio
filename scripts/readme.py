#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
Because a README is the one file everybody reads and nobody maintains.

Every number in the two READMEs this writes is COUNTED from the repository at
build time — cards, themes, tokens, chapters, pages. None is typed.

That is not tidiness. Twice already in this project a hand-written statement of
fact went stale and started lying: the site's list of missing Bangla still claimed
twenty-five card names were absent after every one had been filled in, and a
comment asserted a Chromium failure that turned out never to have been tested. A
sentence a human wrote once and nobody re-reads is the least reliable thing in a
repository, and a README is made almost entirely of those.

So the prose is written here and the facts are looked up here, together, and CI
regenerates the files and fails on any difference.

RUN
---
    cd /Users/gru953/Claude/Cowork/Aninda_Studio
    ./.venv/bin/python scripts/readme.py
    ./.venv/bin/python scripts/readme.py --check
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

EMAIL = "aninda.sh15@gmail.com"
REPO = "https://github.com/GRU-953/aninda-studio"
SITE = "https://anindastudio.com"
PKG = "aninda-studio-tokens"

# The one command in the README chosen to teach the system's governing idea:
# refuse, do not warn. It is run below rather than quoted, because the README used
# to print `asset.py --mark --size 12`, which argparse rejects as an invalid choice
# and exits 2 — the same exit code as the refusal, so a reader checking only the
# status concluded the demonstration had worked. It never reached the size floor.
REFUSAL_SCRIPT = "13_plugins/claude-code/skills/aninda-brand/scripts/asset.py"
REFUSAL_ARGS = ["mark", "--size", "12"]
REFUSAL_EXIT = 2

# The rebuild order, in dependency order, and the one place it is written down.
#
# WHY THIS IS A LIST AND NOT A SENTENCE. The README used to print a six-script
# chain under the heading "Rebuild everything". It rebuilt six of the sixteen
# generators, so a reader who edited one token and followed it was left with a
# stale website, stale npm and PyPI packages, a stale Figma bundle, stale platform
# assets and a stale PDF — and the first thing that told them was CI failing on
# `12_packages/build.py --check`, a step the README never named. The chain is now
# data, and `check_rebuild_chain()` below refuses to write a README when a
# generator exists in the tree that is neither in this list nor in NOT_IN_CHAIN.
#
# Ordering constraints, each taken from the generator's own error message:
#   10_assets  needs 04_mark (marks) and 08_components (subset fonts)
#   12_packages needs 07_tokens/build.py and emit_css.py
#   11_site    needs 12_packages, 10_assets, 04_mark and 08_components
#   pdf.py     needs the guidebook print build
#   readme.py  runs last, because it counts what the others produced
REBUILD_CHAIN = [
    "05_colour/engine.py",
    "07_tokens/build.py",
    "07_tokens/emit_css.py",
    "04_mark/build.py",
    "08_components/build.py",
    "10_assets/build.py",
    "12_packages/build.py",
    "11_site/build.py",
    "09_guidebook/build.py",
    "09_guidebook/scripts/pdf.py",
    "13_plugins/claude-code/scripts/build_skills.py",
    # After the tokens, the marks and the component stylesheet, because it bundles
    # all three, and before readme.py, which counts what it wrote.
    "13_plugins/claude-design/build.py",
    # The findings register is generated from its own data, so it belongs in the
    # chain — but AFTER readme.py would be wrong too, because readme.py counts the
    # tree and the register is part of it. It reads only 01_research/_data, so it
    # can run anywhere; here, next to the other document generators.
    "scripts/findings.py",
    "scripts/readme.py",
]

# benchmark.py runs BEFORE the guidebook, not after it. The guidebook embeds
# 01_research/BENCHMARK.md among its kit files, so writing the acceptance verdicts
# after the book was built left the book carrying a stale copy — and the two differed
# at IDENTICAL byte length, because a verdict cell was swapped for one the same
# size, which is the confusing shape this ordering bug takes. Inserted rather than
# listed in place so the reason travels with the line.
REBUILD_CHAIN.insert(REBUILD_CHAIN.index("09_guidebook/build.py"),
                     "scripts/benchmark.py")

# The Figma bundle is Node, not Python, so it is named separately in the prose.
REBUILD_NODE = "13_plugins/figma/build.mjs"

# Generators deliberately outside the chain, each with the reason. A script here
# is a script whose output is not a shipped deliverable that drifts with a token.
NOT_IN_CHAIN = {
    "03_directions/build.py":
        "one-off exploration: it writes the three rejected colour directions, "
        "which are a record of a decision already taken and do not move again",
    "06_type/specimen.py":
        "one-off: the type specimen pages that fed the typeface decision",
    "06_type/review_bangla.py":
        "a review instrument, run when a Bangla reader is available, not part of "
        "the build",
}


class BuildError(Exception):
    pass


def publication() -> dict:
    """The registry record, read once and used by both READMEs."""
    return json.loads((ROOT / "12_packages" / "PUBLICATION.json").read_text())


def refusal() -> dict:
    """Run the README's demonstration command and read the refusal off it.

    A README that states WHY a command fails, without running it, is a sentence
    nobody re-reads. This runs it and refuses to write a README that describes a
    refusal the script does not actually give.
    """
    proc = subprocess.run(
        [sys.executable, str(ROOT / REFUSAL_SCRIPT), *REFUSAL_ARGS],
        capture_output=True, text=True, cwd=ROOT,
    )
    output = (proc.stdout + proc.stderr).strip()
    if proc.returncode != REFUSAL_EXIT or not output.startswith("REFUSED"):
        raise BuildError(
            f"the README's demonstration command did not refuse. Ran\n"
            f"  {REFUSAL_SCRIPT} {' '.join(REFUSAL_ARGS)}\n"
            f"and got exit {proc.returncode} with:\n{output[:400]}\n"
            f"The README says this command refuses because 12 px is below the mark's "
            f"size floor. Either the command form is wrong or the floor has moved."
        )
    rule = next((line.split("Rule", 1)[1].strip()
                 for line in output.splitlines() if line.strip().startswith("Rule")), "")
    if not rule:
        raise BuildError(f"the refusal printed no Rule line:\n{output[:400]}")
    return {"command": f"./.venv/bin/python {REFUSAL_SCRIPT} {' '.join(REFUSAL_ARGS)}",
            "exit": proc.returncode, "rule": rule}


def check_rebuild_chain() -> dict:
    """Find every generator in the tree and refuse if one is unaccounted for.

    A generator whose output is committed and diffed by CI must appear either in
    REBUILD_CHAIN or in NOT_IN_CHAIN with a reason. Nothing enforced this before,
    which is how "Rebuild everything" came to name six of sixteen.

    The sweep looks for the file names the repository actually uses for its
    writers. A new generator under a new name would slip past it, so the names are
    listed here rather than guessed from content, and this docstring is the place
    to add one.
    """
    names = ("build.py", "build.mjs", "emit_css.py", "engine.py", "readme.py",
             "pdf.py", "specimen.py", "review_bangla.py", "build_skills.py",
             "findings.py", "benchmark.py")
    # `git ls-files` rather than rglob, because rglob also walks ignored trees —
    # a stray git worktree under .claude/ made the first version of this guard
    # report eleven generators that are not part of the repository at all.
    proc = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise BuildError(
            "could not list the tracked files with `git ls-files`, so the rebuild "
            f"chain cannot be checked:\n{proc.stderr.strip()[:300]}"
        )
    found = {rel for rel in proc.stdout.split("\0")
             if rel and rel.rsplit("/", 1)[-1] in names
             and "dist/" not in rel}

    accounted = set(REBUILD_CHAIN) | {REBUILD_NODE} | set(NOT_IN_CHAIN)
    missing = sorted(found - accounted)
    if missing:
        raise BuildError(
            "these generators are in the tree but in neither REBUILD_CHAIN nor "
            "NOT_IN_CHAIN:\n  " + "\n  ".join(missing) +
            "\nAdd each to the chain in dependency order, or to NOT_IN_CHAIN with "
            "the reason it is not a shipped deliverable. The README's "
            '"Rebuild everything" heading has to be true of the whole tree.'
        )
    stale = sorted(accounted - found)
    if stale:
        raise BuildError(
            "these are named in the rebuild chain but are not in the tree:\n  " +
            "\n  ".join(stale) + "\nThe README would tell a reader to run a script "
            "that does not exist."
        )
    return {
        "chain_count": len(REBUILD_CHAIN) + 1,
        "chain": " && \\\n  ".join(f"./.venv/bin/python {s}" for s in REBUILD_CHAIN),
        "chain_excluded": "Three generators are deliberately not in that chain: " +
                          "; ".join(f"`{k}` — {v}" for k, v in NOT_IN_CHAIN.items()) +
                          ".",
    }


def count() -> dict:
    """Every figure in the README, read from the thing it describes."""
    f: dict = {}
    f.update(check_rebuild_chain())

    reg = json.loads((ROOT / "08_components" / "_cards.json").read_text())
    cards = reg["cards"] if isinstance(reg, dict) and "cards" in reg else reg
    f["cards"] = len(cards)
    for g in ("Foundations", "Components", "Patterns"):
        f[g.lower()] = sum(1 for c in cards if c["group"] == g)
    f["cards_bn"] = sum(1 for c in cards if c.get("name_bn"))

    css = (ROOT / "07_tokens" / "css" / "tokens.css").read_text()
    f["tokens"] = len(set(re.findall(r"--as-[a-z0-9-]+", css)))
    f["themes"] = len(re.findall(r'\[data-theme="[a-z-]+"\] \{', css))

    proof = json.loads((ROOT / "05_colour" / "generated" / "estuary.proof.json").read_text())
    roles = [r for t in proof["themes"].values() for r in t["roles"].values()]
    f["pairs"] = len(roles)

    # Text and non-text are counted SEPARATELY, and this is not fussiness.
    # Reporting one minimum across both produced a README that said "the lowest
    # anywhere is 3.81:1, against a floor of 4.5:1" — which reads as the system
    # failing its own standard. That 3.81 is a border, and WCAG 1.4.11 asks 3:1 of
    # a border and defines no AAA level for it at all. Comparing a non-text role
    # to the text floor is a category error, and it is the same one the colour
    # engine had to be corrected for. Prose can make it just as easily as code.
    f["worst_text"] = min(r["worst_case_lsb"] for r in roles if r["kind"] == "text")
    f["worst_nontext"] = min(r["worst_case_lsb"] for r in roles if r["kind"] == "nontext")
    f["n_text"] = sum(1 for r in roles if r["kind"] == "text")
    f["n_nontext"] = sum(1 for r in roles if r["kind"] == "nontext")

    gb = ROOT / "09_guidebook" / "Aninda-Studio-Guidebook.html"
    f["guidebook_mb"] = round(gb.stat().st_size / 1_000_000, 1) if gb.exists() else 0
    pdf = ROOT / "09_guidebook" / "Aninda-Studio-Guidebook.pdf"
    f["pdf_mb"] = round(pdf.stat().st_size / 1_000_000, 1) if pdf.exists() else 0
    build = (ROOT / "09_guidebook" / "build.py").read_text()
    f["chapters"] = len(re.findall(r'^\s*\("\d\d", "', build, re.M))

    f["assets"] = len(list((ROOT / "10_assets").glob("*.png"))) + \
                  len(list((ROOT / "10_assets").glob("*.ico"))) + \
                  len(list((ROOT / "10_assets").glob("*.svg")))
    f["marks"] = len(list((ROOT / "04_mark" / "svg").glob("*.svg")))
    f["files"] = sum(1 for p in ROOT.rglob("*") if p.is_file()
                     and not any(x in p.parts for x in
                                 (".venv", "node_modules", "browsers", ".git", "candidates")))

    pub = publication()
    unpublished = [r for r in pub["registries"] if not r["published"]]
    f["pub_checked"] = pub["checked"]
    f["pub_registries"] = " and ".join(r["registry"] for r in unpublished)
    f["pub_unpublished"] = len(unpublished)

    ref = refusal()
    f["refusal_command"] = ref["command"]
    f["refusal_exit"] = ref["exit"]
    f["refusal_rule"] = ref["rule"]
    return f


def english(f: dict) -> str:
    return f"""<!-- GENERATED by scripts/readme.py — do not hand-edit.
     Every number below is counted from the repository, not typed.
     Regenerate: ./.venv/bin/python scripts/readme.py -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="10_assets/README-header-dark.png">
    <img src="10_assets/README-header-light.png" alt="Aninda Studio" width="640">
  </picture>
</p>

# Aninda Studio

**A brand and a design system, built by one person and measured rather than
asserted.**

*অনিন্দ্য স্টুডিও · [বাংলায় পড়ুন](README.bn.md)*

[![System: Apache-2.0](https://img.shields.io/badge/system-Apache--2.0-0D1A17)](LICENSE)
[![Writing: PolyForm NC](https://img.shields.io/badge/writing-PolyForm%20NC%201.0.0-115E68)](LICENSE-DOCS.md)
[![Fonts: OFL 1.1](https://img.shields.io/badge/fonts-OFL%201.1-115E68)](NOTICE)

I make small, careful software. This is the design system it is built on, and the
brand that sits on top of it. Where something here has a limit, the limit is
written down rather than left for you to find.

## The one thing to understand

**Every colour pairing in this system was measured, not chosen.**

There are **{f['pairs']} colour role and theme pairings** across
**{f['themes']} themes** — light, dark, and a high-contrast pair. Each one was
measured against every surface it can land on, on the rounded 8-bit hex a browser
actually produces, and then measured again with every channel of both colours
nudged by one bit. The published figure is the worst of those results.

- **{f['n_text']} text pairings.** The lowest is **{f['worst_text']}:1**, against a
  floor of 4.5:1 (WCAG 2.2 SC 1.4.3) in the ordinary themes and 7:1 (SC 1.4.6) in
  the high-contrast ones.
- **{f['n_nontext']} non-text pairings** — borders and focus rings. The lowest is
  **{f['worst_nontext']}:1**, against a floor of 3:1 (SC 1.4.11).

Those two are counted separately on purpose. **WCAG defines no AAA level for
non-text contrast**, so a border at 3.9:1 has fully met its criterion; judging it
against the 4.5:1 text threshold would call a pass a failure.

That is why every contrast figure this system publishes about itself is read from
the token files or measured in a browser, never typed. A number a person types is a
number that can be wrong and stay wrong.

The one exception is labelled as one: the Table and Dashboard cards carry five
illustrative rows each, so those components have something to render. Their caption
and their alert both say the figures are examples rather than readings.

## What is in here

| Folder | What it holds |
|---|---|
| `09_guidebook/` | **The guidebook.** {f['chapters']} chapters in English and Bangla, one self-contained HTML file ({f['guidebook_mb']} MB) that needs no network, plus a {f['pdf_mb']} MB PDF |
| `07_tokens/` | The design tokens: DTCG source, and {f['tokens']} CSS custom properties generated from it |
| `08_components/` | {f['cards']} component and pattern cards — {f['foundations']} foundations, {f['components']} components, {f['patterns']} patterns |
| `04_mark/` | {f['marks']} mark, wordmark and icon files |
| `10_assets/` | {f['assets']} ready-made images at exact platform sizes |
| `11_site/` | The website, generated from the tokens |
| `12_packages/` | The tokens as an npm package and a Python package |
| `13_plugins/` | A Figma plugin, a Claude Code plugin, and the Claude Design bundle |
| `01_research/` | What was checked, when, and against which source — including what could not be verified |

## Try it in one minute

Start from a local checkout. **The two token packages are built but not
published.** On {f['pub_checked']} I checked {f['pub_registries']}, and neither
holds `{PKG}`, so `npm install` and `pip install` will not work yet. Everything
below works from a checkout.

```bash
./.venv/bin/python 00_sandbox/measure.py
```

That command opens a real browser and re-measures every colour pairing against the
pixels it actually produced. It takes a few seconds and it either agrees with the
token files or tells you exactly where it does not.

```bash
{f['refusal_command']}
```

**That one fails on purpose**, with exit {f['refusal_exit']}. It asks for the mark
at 12 px, and the rule it meets is this: {f['refusal_rule']} The script refuses
rather than producing something unreadable. A system that warns teaches nothing;
one that refuses teaches the rule.

That command is run by `scripts/readme.py` every time this file is generated, and
the rule quoted above is the script's own words. If it stopped refusing, this
README could not be written.

## Rebuild everything

{f['chain_count']} generators, in dependency order. Each step reads the output of
the ones above it, so the order is not interchangeable.

```bash
{f['chain']}
```

Then the Figma plugin bundle, which is Node rather than Python:

```bash
cd 13_plugins/figma && node build.mjs --code-only
```

{f['chain_excluded']}

Every generator is fail-closed: if a check does not pass, it writes nothing at
all. A half-written token set that looks plausible is worse than none.

## What this does not do

Stated here rather than discovered later:

- **Nothing has been tested with a screen reader by somebody who depends on one.**
  Contrast is computed and proved. Lived accessibility is a different claim and
  this kit does not make it.
- **No user research.** One person's judgement, and it says so.
- **The npm and PyPI packages are built but not published.** Checked
  {f['pub_checked']}: {f['pub_registries']} hold nothing under `{PKG}`. The
  packages work from this checkout; the registry commands do not work yet.
- **The Bangla has not been reviewed by a second Bangla reader.** Spelling follows
  the Bangla Academy standard and every ruling is sourced, but sourced is not the
  same as read well. {f['cards_bn']} of {f['cards']} cards carry Bangla names.
- **Rendering checks are Chromium only.** They run on macOS locally and on Ubuntu
  in CI, from a clean checkout, so the results are not particular to one machine.
  Safari, Firefox and real Windows High Contrast were not run.
- **The icons are rounded everywhere, Apple included.** That is a deliberate
  choice against Apple's current guidance, and what it trades away is recorded in
  `04_mark/manifest.json`.
- **The website is not deployed, and its domain is not registered.**
  `11_site/` names `anindastudio.com` in its CNAME, its canonical URLs, its sitemap
  and its social image, because that is the address it is built for. The `.com`
  registry held no record of it on 19 August 2026, so nothing is served there yet.

## Licence

Four licences, because the parts genuinely differ. `NOTICE` explains each one.

- **The system** — tokens, stylesheets, components, scripts: **Apache-2.0**. Use
  it commercially, change it, ship it.
- **The writing** — the guidebook and the documents: **PolyForm Noncommercial
  1.0.0**. Free to read, copy and adapt; not to resell. This is
  source-available, **not open source**, and licence scanners will flag it.
- **The typefaces** — Literata, Noto Serif Bengali, IBM Plex Mono: **SIL OFL 1.1**,
  each licence beside its file.
- **The name and the marks** — **not licensed at all**. Take the system, leave the
  identity. See `TRADEMARKS.md`.

Questions and permissions: **{EMAIL}**

*Not legal advice — written by the author, who is not a lawyer.*
"""


def bangla(f: dict) -> str:
    """Written as Bangla, not translated from the English.

    Same facts, same steps, its own sentences. Only vocabulary approved in
    06_type/BANGLA-STANDARD.md and bangla-strings.json is used; where no approved
    term exists, the English word stands, which is honest rather than invented.
    """
    return f"""<!-- GENERATED by scripts/readme.py — do not hand-edit. -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="10_assets/README-header-dark.png">
    <img src="10_assets/README-header-light.png" alt="অনিন্দ্য স্টুডিও" width="640">
  </picture>
</p>

# অনিন্দ্য স্টুডিও

**এক জনের গড়া একটি ব্র্যান্ড ও ডিজাইন পদ্ধতি — যেখানে প্রতিটি দাবি মেপে দেখা
হয়েছে, শুধু বলা হয়নি।**

*Aninda Studio · [Read in English](README.md)*

আমি ছোটো, যত্নে গড়া সফটওয়্যার বানাই। কোনো কিছুর সীমা থাকলে সেটা এখানেই লেখা
থাকবে — লুকিয়ে রাখা হবে না।

## মূল কথাটা

**এখানের প্রতিটি রঙের জোড়া মেপে নেওয়া, বেছে নেওয়া নয়।**

{f['themes']}টি থিমে মোট **{f['pairs']}টি জোড়া** আছে — আলো, অন্ধকার, আর বেশি
কনট্রাস্টের দুটি। প্রতিটি জোড়া যে যে পৃষ্ঠের উপর বসতে পারে, সবগুলোর সঙ্গে মেপে
দেখা হয়েছে। মাপা হয়েছে সেই ৮-বিট হেক্স মানে, ব্রাউজার আসলে যেটা দেখায় — তারপর
দুই রঙের প্রতিটি চ্যানেল এক বিট সরিয়ে আবার মাপা হয়েছে। যেটা প্রকাশ করা হয়েছে,
সেটা এই সবের মধ্যে সবচেয়ে খারাপ ফলাফল।

- **লেখার জন্য {f['n_text']}টি জোড়া।** সবচেয়ে কম **{f['worst_text']}:1** —
  সাধারণ থিমে সীমা ৪.৫:১, বেশি কনট্রাস্টে ৭:১।
- **লেখা ছাড়া {f['n_nontext']}টি জোড়া** — সীমারেখা আর ফোকাস রিং। সবচেয়ে কম
  **{f['worst_nontext']}:1** — সীমা ৩:১।

দুটি আলাদা করে গোনা হয়েছে, কারণ **লেখা ছাড়া কনট্রাস্টের জন্য WCAG-এ AAA স্তর
নেই**। তাই ৩.৯:১ মানের একটি সীমারেখা তার নিয়ম পুরোপুরি মেনেছে; ৪.৫:১ দিয়ে বিচার
করলে উত্তীর্ণকে ব্যর্থ বলা হবে।

তাই এখানে হাতে লেখা কোনো কনট্রাস্টের সংখ্যা নেই। মানুষের হাতে লেখা সংখ্যা ভুল
হতে পারে, আর ভুল থেকেই যেতে পারে।

## এখানে কী আছে

| ফোল্ডার | কী আছে |
|---|---|
| `09_guidebook/` | **নির্দেশিকা।** বাংলা ও ইংরেজিতে {f['chapters']}টি অধ্যায়, একটি ফাইলেই ({f['guidebook_mb']} মেগাবাইট), ইন্টারনেট ছাড়াই চলে। সঙ্গে {f['pdf_mb']} মেগাবাইটের PDF |
| `07_tokens/` | ডিজাইন টোকেন — DTCG সূত্র, আর তা থেকে বানানো {f['tokens']}টি CSS প্রপার্টি |
| `08_components/` | {f['cards']}টি উপাদান ও নকশার কার্ড |
| `04_mark/` | চিহ্ন, নামলিপি আর আইকনের {f['marks']}টি ফাইল |
| `10_assets/` | নানা মাপে তৈরি {f['assets']}টি ছবি |
| `11_site/` | ওয়েবসাইট, টোকেন থেকে বানানো |
| `12_packages/` | টোকেনগুলো npm ও Python প্যাকেজ হিসেবে |
| `13_plugins/` | Figma প্লাগইন, Claude Code প্লাগইন আর Claude Design বান্ডিল |

## শুরু করতে

> **Not published yet.** *This paragraph is in English because no reviewed Bangla
> exists for it, and the rule in this project is to leave the English rather than
> invent the Bangla.* On {f['pub_checked']} I checked {f['pub_registries']}, and
> neither holds `{PKG}`. So `npm install` and `pip install` will not work yet.
> The command below works from a local checkout.

```bash
./.venv/bin/python 00_sandbox/measure.py
```

এই কমান্ডটি সত্যিকারের একটি ব্রাউজার খুলে প্রতিটি রঙের জোড়া আবার মেপে
দেখে। কয়েক সেকেন্ড লাগে। হয় সে টোকেন ফাইলের সঙ্গে একমত হবে, নয়তো ঠিক কোথায় মেলে না
তা বলে দেবে।

## যা এই পদ্ধতি করে না

- **কোনো স্ক্রিন রিডার ব্যবহারকারী এটি পরীক্ষা করেননি।** কনট্রাস্ট মাপা হয়েছে ও
  প্রমাণ করা হয়েছে। কিন্তু বাস্তবে ব্যবহারের সুবিধা আলাদা দাবি, আর সেই দাবি এখানে
  করা হয়নি।
- **কোনো ব্যবহারকারী গবেষণা হয়নি।** এক জনের বিচার, এবং সেটা স্পষ্ট করেই বলা।
- **দ্বিতীয় কোনো বাংলা পাঠক এই বাংলা দেখেননি।** বানান বাংলা একাডেমির প্রমিত
  নিয়ম মেনে, প্রতিটি সিদ্ধান্তের সূত্র দেওয়া — তবু সূত্র থাকা আর ভালো পড়া এক
  জিনিস নয়।
- **পরীক্ষা শুধু Chromium-এ।** নিজের ম্যাকে আর CI-তে উবুন্টুতে, দুই জায়গাতেই চলে —
  তাই ফলাফল কোনো একটি যন্ত্রের উপর নির্ভর করে না। Safari, Firefox আর উইন্ডোজের হাই
  কনট্রাস্ট পরীক্ষা করা হয়নি।
- **সব জায়গায় আইকনের কোণ গোল, Apple-সহ।** এটি Apple-এর বর্তমান নির্দেশনার
  বিপরীতে নেওয়া একটি সিদ্ধান্ত। এর বিনিময়ে কী ছাড়া হলো, তা
  `04_mark/manifest.json`-এ লেখা আছে।
- **ওয়েবসাইটটি এখনো প্রকাশ করা হয়নি, ডোমেইনটিও নিবন্ধন করা হয়নি।** `11_site/`
  ফোল্ডারে `anindastudio.com` লেখা আছে, কারণ সাইটটি ওই ঠিকানার জন্যই তৈরি।
  ১৯ অগস্ট ২০২৬ পর্যন্ত `.com` নিবন্ধকের কাছে ওই নামের কোনো রেকর্ড নেই, তাই
  ওখানে এখনো কিছুই দেখা যাবে না।

## লাইসেন্স

চারটি আলাদা লাইসেন্স, কারণ অংশগুলো সত্যিই আলাদা। বিস্তারিত `NOTICE` ফাইলে।

- **পদ্ধতি** — টোকেন, স্টাইলশিট, উপাদান, স্ক্রিপ্ট: **Apache-2.0**। বাণিজ্যিক
  কাজেও ব্যবহার করা যায়।
- **লেখা** — নির্দেশিকা ও নথিপত্র: **PolyForm Noncommercial 1.0.0**। পড়া, নকল
  করা, বদলানো যায়; বিক্রি করা যায় না। এটি উৎস-উন্মুক্ত, **ওপেন সোর্স নয়**।
- **হরফ** — Literata, Noto Serif Bengali, IBM Plex Mono: **SIL OFL 1.1**।
- **নাম ও চিহ্ন** — **কোনো লাইসেন্স নেই**। পদ্ধতি নিন, পরিচয়টি রেখে দিন।

প্রশ্ন বা অনুমতির জন্য: **{EMAIL}**

*এটি আইনি পরামর্শ নয় — লেখক আইনজীবী নন।*
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    try:
        f = count()
    except BuildError as exc:
        print(f"FAILED — nothing written:\n  {exc}", file=sys.stderr)
        return 1
    if f["pub_unpublished"] != 2:
        # Both READMEs are written for the state recorded today: neither package is
        # published. When that changes, the prose has to change with it rather than
        # being quietly wrong in the other direction.
        print("FAILED — nothing written:\n  12_packages/PUBLICATION.json now records "
              f"{2 - f['pub_unpublished']} of 2 packages as published. The install "
              "sections in both READMEs are written for neither being published; "
              "rewrite them in scripts/readme.py before regenerating.", file=sys.stderr)
        return 1
    files = {ROOT / "README.md": english(f), ROOT / "README.bn.md": bangla(f)}

    for k, v in f.items():
        print(f"  counted  {k:<14} {v}")

    if args.check:
        for path, content in files.items():
            if not path.exists():
                print(f"\n--check: {path.name} is missing", file=sys.stderr)
                return 1
            if path.read_text() != content:
                print(f"\n--check: {path.name} differs from a fresh build — the counts "
                      f"in it have gone stale. Run scripts/readme.py.", file=sys.stderr)
                return 1
        print("\n--check: both READMEs match the repository they describe.")
        return 0

    for path, content in files.items():
        path.write_text(content)
    print(f"\nWrote README.md and README.bn.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
