---
name: aninda-review
description: >-
  CHECK something that already exists against the Aninda Studio system and WCAG
  2.2 AA. Use when asked to review, audit, check, verify, validate, inspect,
  test, critique or assess an existing page, component, stylesheet, template,
  document, README, repository or design, and when asked "is this accessible",
  "is this on-brand", "does this pass WCAG", "check the contrast", "check the
  colour contrast", "is the contrast enough", "accessibility review", "a11y
  check", "WCAG 2.2 AA", "AAA", "target size", "focus visible", "focus
  obscured", "reduced motion", "forced colors", "high contrast mode", "does this
  use the tokens", "any hard-coded hex", "raw pixel values", "did I use banned
  words", "plain English check", "why is there Bangla here", "are the licences
  right", or "what did I miss". Ships scripts/check.py, which measures what it
  can from the source and then names its own blind spots rather than passing them
  silently. For MAKING something new — an asset, a page, a component, a piece of
  copy — use the aninda-brand skill instead. For setting up or upgrading a whole
  REPOSITORY, use the aninda-repo skill instead.
---

<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->

# Aninda Studio — check what already exists

This skill measures. It does not make anything and it does not fix anything
without being asked.

**Licence:** the checker is Apache-2.0. This document is PolyForm Noncommercial
1.0.0. See `NOTICE`.

---

## Run the checker first, then read it

```
python scripts/check.py <path>              a file or a folder
python scripts/check.py <path> --aaa         also report against AAA
python scripts/check.py <path> --json out.json
```

It exits `0` when it found no failure, `1` when it did, and `3` when it is not
equipped to check what it was given.

`references/wcag-2.2-aa.md` lists every criterion the checker touches, with its
number, its level and its threshold, plus four things that are commonly got wrong
— including the fact that **WCAG defines no AAA level for non-text contrast**.
Read it before reporting a criterion by number.

It reports three things, in this order, and all three matter:

1. **Failures.** Each one with the measured number, the threshold it missed, and
   the WCAG success criterion by number and name.
2. **Notes.** Things worth a look that are not failures.
3. **Blind spots.** What this checker cannot see at all. Read these out to the
   user. A check that hides its own limits is worse than no check, because it
   buys false confidence.

---

## What it checks

**Colour**
- Every `#rrggbb` in the source, paired against every background colour declared
  in the same rule, measured with the WCAG relative-luminance formula.
- Every use of a semantic role against every ground it appears on, in all four
  themes, from the token files.
- Whether all four themes are present at all.
- Whether a `forced-colors` block exists, and whether `forced-color-adjust: none`
  appears without an allow-list comment beside it.

**Tokens**
- Raw hex values where a token exists for that exact colour.
- Raw pixel values that are not on the 4 px spacing scale.
- Raw durations that are neither 120 ms nor 220 ms.
- Custom properties beginning with anything other than `--as-`.

**Size and focus**
- Declared heights and widths on interactive elements against the 24 CSS px
  floor of WCAG 2.2 success criterion 2.5.8.
- Whether a `:focus-visible` rule exists at all, and whether any rule sets
  `outline: none` without replacing it.

**Motion**
- Whether a `prefers-reduced-motion` block exists wherever a transition or an
  animation is declared.

**English**
- The banned words: *simply*, *just*, *easy*, *obviously*, *of course*,
  *clearly*.
- Exclamation marks.
- Latin abbreviations: *e.g.*, *i.e.*, *etc.*
- American spellings where the British form is the standard.
- Sentences over 25 words.
- *we* used for one person.

**Bangla**

This studio shipped Bangla until 27 August 2026 and now ships English. The check
was **inverted** rather than deleted, and the difference matters when you read a
report: the old question was "is this string on the verified list?", the new one
is "why is there Bangla here at all?".

- **Any Bengali-script run is a FAILURE**, not a note. Nothing applies the Bangla
  rules any more — no `:lang(bn)` block, no Bengali face in the subsets — so the
  run would render in whatever font the reader's machine happens to have, at the
  Latin size.
- **Two exceptions, both named in the checker.** The studio's own name
  (**অনিন্দ্য**, **অনিন্দ্য স্টুডিও**) passes, because a name is not text. And a
  short list of retained record documents passes — the Bangla standard, the string
  register and the type measurements, which are *about* Bangla rather than written
  in it. They stay on the checked-path list in every other respect.
- **Do not exempt a file quietly.** If a run really is record, it belongs in
  `BANGLA_RECORD` in the checker, named with its reason. An exemption for one word
  would also license every other Bangla run in that file, which is the failure the
  old rule had.

**Licences**
- Whether `LICENSE`, `LICENSE-DOCS.md`, `NOTICE` and `TRADEMARKS.md` exist.
- Whether the PolyForm URL carries a trailing slash. The trailing-slash form
  returns 404.
- Any reference to "OFL 1.2", which does not exist.
- Whether each font file has an `-OFL.txt` beside it.

---

## What it cannot check, and never claims to

The checker prints these itself, every run. They are here so you know them
before you run it.

- **Whether anything is actually usable.** Contrast, target size and focus
  visibility are measurable. Whether a person can complete a task is not.
- **Anything that needs a browser.** These are static-source checks. A colour
  that comes from a computed value, an inherited value, a gradient, an image or a
  JavaScript-set style is invisible here. To measure a rendered page, use
  `08_components/check.py` in the main project, which drives a real browser.
- **Mid-transition states.** A colour that dips below its floor for 60 ms on its
  way somewhere is not seen.
- **Whether a heading structure makes sense**, or whether an `alt` text describes
  the right thing. Both need a person.
- **Whether the English is *actually* clear.** Sentence length and a banned-word
  list are proxies. A short sentence can still be baffling.
- **Whether the Bangla in a retained record is *right*.** It reports where
  Bangla is allowed to be, not whether the words there are correct. That needs
  the Bangla Academy dictionary and a reader.
- **Whether a licence choice is legally sound.** It checks that the files exist
  and that the identifiers and URLs are right. It is not legal advice.

---

## How to report what you find

1. Failures first, each with its number and its criterion. Never soften a
   failure.
2. Then the notes.
3. Then the blind spots, in full.
4. Then offer to fix. Do not fix without asking — a contrast failure sometimes
   wants a design decision, not a nudged hex.

---

## If you need to make something rather than check it

Use the `aninda-brand` skill. If you need a whole repository set up or upgraded,
use `aninda-repo`.
