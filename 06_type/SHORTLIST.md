# Aninda Studio — typeface shortlist

**Date of research:** 14 August 2026
**Scope:** 30 families downloaded and inspected — 12 Latin, 10 Bangla, 8 monospace.
**Files:** `06_type/candidates/<script>/<family>/`, each with its `OFL.txt` beside it.

---

## How to read this document

**Where the numbers come from.** Every number below is one of three kinds, and each
is labelled:

| Mark | Meaning |
|---|---|
| **[file]** | Read directly out of the font file with `fontTools` — the `name`, `fvar`, `OS/2`, `head` and `maxp` tables, or the glyph outlines themselves. Reproduce with `06_type/specimen.py`. |
| **[rendered]** | Measured from real rendered text in Chromium via Playwright, using the Canvas 2D text-metrics API, which reports the actual inked box of a string. |
| **[judgement]** | My opinion. Not measured. Treat as opinion. |

Nothing here comes from a foundry's marketing page or a specimen image.

**Terms, explained once.**

- **em** — the font's own design square. Dividing a measurement by it lets you
  compare fonts that were drawn at different internal scales.
- **x-height** — the height of a lowercase `x`. This, far more than the nominal
  point size, is what makes Latin text look big or small on a page.
- **cap height** — the height of a capital `H`.
- **variable font** — one file that slides continuously between weights, widths
  or other qualities, instead of one file per weight.
- **axis** — one thing a variable font can slide along: `wght` weight, `wdth`
  width, `opsz` optical size, `slnt` slant.
- **optical size (`opsz`)** — an axis that *redraws* the letters for the size
  they will be used at: sturdier and more open when small, finer and more
  tightly fitted when large. Most families do not have one, and it is a real
  advantage where they do.
- **Reserved Font Name (RFN)** — a name the licence forbids you to keep if you
  modify the font. Modify a font with an RFN and you must rename your version.
  Using it unmodified is unaffected.
- **মাত্রা (matra)** — the horizontal headline stroke running along the top of
  most Bangla letters, joining them into a word. If it breaks, the word looks
  wrong to a Bangla reader.
- **conjunct** — two or more Bangla consonants written as a single joined shape
  (`ক` + `ষ` → `ক্ষ`). Getting these right is the hard part of Bangla type.

---

## Licence position — all 30 candidates

**Every one of the 30 families is SIL Open Font License 1.1.** **[file]** Verified by
reading the full `OFL.txt` shipped in each family's folder, not by assumption.
No Apache-2.0 font ended up in the final set, and nothing with an unclear or
commercial licence was downloaded.

**Reserved Font Names found** **[file]** — extracted from the `with Reserved Font
Name …` declarations in each `OFL.txt`:

| Family | Reserved Font Name | Consequence |
|---|---|---|
| IBM Plex Sans, IBM Plex Mono | `Plex` | Modify → must rename |
| Source Sans 3, Source Code Pro | `Source` | Modify → must rename |
| Galada | `Lobster` | Inherited: Galada's Latin derives from Lobster |
| Mina | `Exo` | Inherited: Mina's Latin derives from Exo |

**The other 26 families carry no Reserved Font Name at all.** That matters more
than it looks. Subsetting a font — stripping out glyphs you never use to make
the file smaller and the site faster — counts as modification. With an RFN you
must rename the subset; without one you may subset freely and keep the name.
Since this brand will ship webfonts, an RFN is a genuine, if small, operational tax.

**Correction to a commonly-repeated fact.** Roboto Mono and Roboto Flex are
often described as Apache-2.0. They are not, as of this date. Both now sit under
`ofl/` in the Google Fonts repository with SIL OFL 1.1 licence files. **[file]** Only
Roboto Slab remains under `apache/`. I verified this by listing the `apache/`
tree directly.

*This is a reading of the licence text, not legal advice.*

---

## Latin candidates (12)

Ordered by how well suited they are to this brand, best first. **[judgement]**

Measurements are at 16px, the body size, and come from rendered ink **[rendered]**.
`x/cap` is the x-height as a proportion of the cap height — a high number means
a large-looking, contemporary face; a low number means a more traditional,
smaller-looking one.

### 1. Inter — Rasmus Andersson
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `opsz` 14–32, `wght` 100–900 **[file]**
- **Weights:** 9 named instances, Thin to Black; continuous in between **[file]**
- **Version:** 4.001 · 2,933 glyphs · 2048 units/em **[file]**
- **Proportions:** Cap 11.64px, x-height 8.68px, x/cap 0.746 at 16px **[rendered]** — a
  notably large x-height, and the largest of any Latin candidate at body size.
  Its optical-size axis is why: x-height is 0.5459em at 8–12px but 0.5156em at
  56px and above, so it deliberately grows to stay legible when small **[rendered]**.
- **Good at:** interface and body text at small sizes; it needs the least size
  correction of any Latin face here when set beside Bangla (see `pairings.md`).
- **Bad at:** it has no width axis, and at display sizes it is a plain, widely-used
  face that will not by itself make the brand distinctive. **[judgement]**

### 2. IBM Plex Sans — Mike Abbink, Paul van der Laan, Pieter van Rosmalen
- **Licence:** SIL OFL 1.1, **RFN `Plex`** **[file]**
- **Variable:** yes — `wght` 100–700, `wdth` 75–100 **[file]**
- **Weights:** 7 named instances, Thin to Bold **[file]**
- **Version:** 3.201 · 1,025 glyphs · 1000 units/em **[file]**
- **Proportions:** Cap 11.17px, x 8.26px, x/cap 0.739 **[rendered]** — moderate, even
  colour with slightly squared curves and a faint engineering accent.
- **Good at:** technical writing; it has a true monospace sibling drawn by the
  same hands, so prose and code match exactly.
- **Bad at:** the RFN blocks renaming-free subsetting; weight stops at 700, so
  there is no genuinely heavy display weight; no optical-size axis.

### 3. Public Sans — US Web Design System authors (after Libre Franklin)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `wght` 100–900 **[file]**
- **Weights:** 9 named instances **[file]**
- **Version:** 2.001 · 648 glyphs · 2000 units/em **[file]**
- **Proportions:** Cap 11.57px, x 8.27px, x/cap 0.715 **[rendered]** — tall caps, short
  descenders (2.58px, among the shallowest here), a compact and civic look.
- **Good at:** institutional, governmental and plainly-trustworthy registers;
  deliberately unfashionable in a way that ages well.
- **Bad at:** no width or optical-size axis; only 648 glyphs, so language
  coverage beyond Western European is thin.
- **Gotcha:** its variable default weight is **100 (Thin)**, not 400 **[file]**. Load it
  without specifying a weight and you get hairline text.

### 4. Literata — Veronika Burian & José Scaglione (TypeTogether)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `opsz` 7–72, `wght` 200–900 **[file]**
- **Weights:** 8 named instances **[file]**
- **Version:** 3.103 · 1,789 glyphs **[file]**
- **Proportions:** Cap 11.23px, x 8.12px, x/cap 0.723 **[rendered]** — a sturdy,
  large-bodied serif with low stroke contrast, drawn originally for e-readers.
- **Good at:** long-form reading on screen; the wide optical-size range means it
  works from footnote to poster from a single file.
- **Bad at:** it is a book face, so it carries a slightly literary air that may
  not suit a software studio. **[judgement]**

### 5. Archivo — Hector Gatti (Omnibus-Type)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `wght` 100–900, `wdth` 62–125 **[file]**
- **Weights:** 9 named instances **[file]**
- **Version:** 2.001 · 834 glyphs **[file]**
- **Proportions:** Cap 10.98px, x 8.42px, **x/cap 0.767 — the largest ratio of any
  Latin candidate** **[rendered]**; short descenders at 2.77px. Looks big and present
  at any size.
- **Good at:** headline and display work; the very wide `wdth` range (62–125) is
  the broadest here and allows genuinely compressed or extended settings.
- **Bad at:** the large x-height and tight descenders make long body text feel
  dense. No optical-size axis.
- **Gotcha:** variable default weight is **600**, not 400 **[file]**.

### 6. Newsreader — Hugues Gentile (Production Type)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `opsz` 6–72, `wght` 200–800 **[file]**
- **Weights:** 7 named instances **[file]**
- **Version:** 1.003 · 658 glyphs · 2000 units/em **[file]**
- **Proportions:** Cap 10.82px, x 7.05px, **x/cap 0.651 — the smallest of any
  candidate** **[rendered]**. Deep descenders at 3.99px. A small-bodied, distinctly
  editorial serif.
- **Good at:** editorial voice; the 6–72 optical range is the widest here, and
  the display cuts are genuinely elegant.
- **Bad at:** **its small x-height is a measured problem in this brand.** Paired
  with Bangla and matched properly by size, it forces the Bangla down to 11.33px
  when the Latin is at 16px **[rendered]** — too small to read Bangla conjuncts
  comfortably. See `pairings.md` §3 and the specimen.

### 7. Libre Franklin — Pablo Impallari, Rodrigo Fuenzalida, Nhung Nguyen
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `wght` 100–900 **[file]** · 9 instances · 1,007 glyphs
- **Proportions:** **Cap 11.87px — the tallest caps of any candidate** — x 8.48px,
  x/cap 0.714 **[rendered]**. An American gothic in the Franklin tradition.
- **Good at:** confident, slightly journalistic headlines.
- **Bad at:** no width or optical axis; the tall caps make all-caps settings shout.
- **Gotcha:** variable default weight is **100 (Thin)** **[file]**.

### 8. Work Sans — Wei Huang
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `wght` 100–900 **[file]** · 9 instances · 1,349 glyphs
- **Proportions:** Cap 10.56px, x 8.00px, x/cap 0.758 **[rendered]** — low caps, large
  x-height, slightly quirky and warm.
- **Good at:** friendly, approachable interface text; the middle weights were
  drawn for screen and hold up small.
- **Bad at:** the extreme weights are noticeably less refined than the middle;
  no width or optical axis. **[judgement]**

### 9. Source Sans 3 — Paul D. Hunt (Adobe)
- **Licence:** SIL OFL 1.1, **RFN `Source`** **[file]**
- **Variable:** yes — `wght` 200–900 **[file]** · 8 instances · 2,478 glyphs
- **Proportions:** Cap 10.50px, x 7.78px, x/cap 0.741 **[rendered]** — modest, quiet,
  humanist; deliberately recedes.
- **Good at:** stepping back so another element leads; excellent glyph coverage
  at 2,478 glyphs.
- **Bad at:** RFN; no width or optical axis; its very neutrality means it
  contributes little character. **[judgement]**
- **Gotcha:** variable default weight is **200** **[file]**.

### 10. Instrument Sans — Rodrigo Fuenzalida
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `wdth` 75–100, `wght` 400–700 **[file]**
- **Weights:** only 4 named instances, Regular to Bold **[file]** · 501 glyphs
- **Proportions:** Cap 11.52px, x 8.16px, x/cap 0.708 **[rendered]** — crisp,
  contemporary, slightly condensed by default.
- **Good at:** current-feeling interface work with a width axis.
- **Bad at:** **the weight axis starts at 400** — there is no light weight at all,
  which rules out several typographic moves. Only 501 glyphs, the thinnest
  coverage of any Latin candidate.

### 11. Source Serif 4 — Frank Grießhammer (Adobe)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]** (unlike its sans and mono siblings)
- **Variable:** yes — `wght` 200–900, `opsz` 8–60 **[file]** · 8 instances · 1,463 glyphs
- **Proportions:** Cap 10.72px, x 7.78px, x/cap 0.726 **[rendered]**. Its optical axis
  behaves classically: x-height falls from 0.508em at 8px to 0.452em at 60px **[rendered]**.
- **Good at:** a serif companion to Source Sans 3 with a proper optical axis and,
  usefully, no RFN of its own.
- **Bad at:** less distinctive than Newsreader or Literata; the small x-height
  raises the same Bangla-matching problem as Newsreader, though less severely.

### 12. Roboto Flex — David Berlow (Type Network), after Christian Robertson
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — **13 axes**: `opsz` 8–144, `wght` 100–1000, `wdth` 25–151,
  `slnt` −10–0, `GRAD`, `XOPQ`, `YOPQ`, `XTRA`, `YTUC`, `YTLC`, `YTAS`, `YTDE`,
  `YTFI` **[file]**. It is the only candidate carrying all four of the axes named in
  the brief — weight, width, optical size and slant.
- **Weights:** 20 named instances including italics **[file]** · 948 glyphs
- **Proportions:** Cap 11.38px, x 8.17px, x/cap 0.718 **[rendered]**. Its optical range
  is the widest of all: x-height 0.5317em at 8px down to 0.4490em at 100px **[rendered]**.
- **Good at:** a design system that wants to tune type precisely from one file.
- **Bad at:** **the flexibility is the problem.** Thirteen axes is a large surface
  for one person to maintain consistently, and Roboto's shapes are among the
  most familiar on earth, so it makes the brand generic. **[judgement]** Also the only
  Latin candidate that is unmistakably a Google system face.

---

## Bangla candidates (10)

The brief named nine faces to investigate. **All nine exist under SIL OFL 1.1**
and all were downloaded and tested. I added **Noto Sans Bengali UI** as a tenth,
because it is the variant actually built for constrained interface line heights.

### The disqualification tests, and what they found

The brief sets two grounds for disqualification: breaking the মাত্রা, and
rendering conjuncts poorly. Both were tested mechanically.

**Conjunct shaping — HarfBuzz, 16 conjuncts per face.** Each face was asked to
shape `ক্ষ ত্র জ্ঞ ঙ্গ ন্দ্য স্ত্র ক্ত ষ্ট হ্ম দ্ব ঞ্চ ণ্ড ক্ল শ্ব স্ক্র ত্ত`, plus `অনিন্দ্য স্টুডিও`, `কর্ম`,
`বিদ্যা`, `স্বাস্থ্য` and the Bangla digits. A failure shows up as one of three
things: a missing glyph, an inserted dotted circle (`◌`, the standard signal that
shaping has failed), or a visible hasanta (`্`) where a joined form should be.

**Result: all ten faces passed all sixteen conjuncts, with no dotted circles, no
missing glyphs and no stray hasantas.** **[file]** No face is disqualified on
shaping grounds. This is a *negative* test — it proves nothing is broken. It does
not prove the conjuncts are beautifully drawn, which only a Bangla reader can judge.

One real difference did emerge. Most faces draw each conjunct as a single
precomposed glyph — Hind Siliguri shapes `ন্দ্য` to `bnN_DA` + `bnYAc2`, two glyphs;
Tiro Bangla and Anek Bangla behave the same way. **Noto Sans Bengali instead
assembles some conjuncts from parts**, shaping `ন্দ্য` to four glyphs including a
separate `.headline` piece and a `.float` piece **[file]**. That is a deliberate
technique for keeping the মাত্রা continuous across assembled forms, not a fault —
and the pixel test below confirms it works.

**মাত্রা continuity — measured from pixels.** Each face rendered `কলকাতা` (a word
in which every letter carries a মাত্রা) at 240px. Every column of pixels across the
word was checked for ink in the upper band of the letterform; the মাত্রা is
continuous only if every column carries it.

**Result: all ten faces keep the মাত্রা unbroken.** **[rendered]** Nine score a perfect
1.000; Tiro Bangla scores 0.996, being three pixel columns short out of 787 at a
tapered stroke terminal — visually continuous, and I confirmed this by eye on the
rendered crop. No face is disqualified on মাত্রা grounds either.

*Two earlier versions of this test were wrong and were discarded — scanning a
single pixel row failed any face with a tapered মাত্রা, and walking the topmost-ink
edge failed any face with letter parts rising above the মাত্রা. Both are recorded
in the script's comments so the mistake is not repeated.*

**What did discriminate: মাত্রা thickness.** **[rendered]** Since nothing failed the
pass/fail tests, the useful measurement turned out to be how *thick* the headline
stroke is — because a stroke thinner than one device pixel greys out or drops
away on an ordinary screen.

| Face | মাত্রা thickness | at 16px | at 11px |
|---|---|---|---|
| Galada | 0.1083 em | 1.73px | 1.19px |
| **Noto Sans Bengali** / UI | **0.0750 em** | **1.20px** | **0.83px** |
| Hind Siliguri | 0.0708 em | 1.13px | 0.78px |
| Anek Bangla, Tiro Bangla, Atma | 0.0667 em | 1.07px | 0.73px |
| Mina | 0.0625 em | 1.00px | 0.69px |
| Baloo Da 2 | 0.0583 em | 0.93px | 0.64px |
| **Noto Serif Bengali** | **0.0542 em** | **0.87px** | **0.60px** |

Noto Sans Bengali has the sturdiest headline of any text face here. Noto Serif
Bengali has the finest, and at caption sizes its মাত্রা is well under one device
pixel — a real, practical caution for the editorial direction.

---

### Body-text grade

The brief asks which are genuinely good for **body text** rather than display.
My assessment **[judgement]**, supported by the measurements above:

| Face | Grade | Why |
|---|---|---|
| Noto Sans Bengali | **Body — first rank** | Sturdiest মাত্রা, widest coverage, variable weight *and* width |
| Noto Serif Bengali | **Body, with a size floor** | Excellent shapes; thin মাত্রা needs a minimum size |
| Hind Siliguri | **Body** | Familiar, robust, well-hinted; but static only |
| Tiro Bangla | **Body — scholarly** | The most authoritatively drawn; but one weight only |
| Anek Bangla | **Body / interface** | Contemporary, wght + wdth; slightly narrower coverage |
| Noto Sans Bengali UI | **Interface only** | Same design, tighter metrics, but almost no Latin |
| Mina | **Body, limited** | Usable but only two weights and incomplete `OS/2` data |
| Baloo Da 2 | **Display** | Heavy by design; weight axis starts at 400 |
| Atma | **Display** | High-contrast brush character |
| Galada | **Display only** | A joined script face; unsuitable for running text |

---

### 1. Noto Sans Bengali — Joana Ranito (Universal Thirst) with Jelle Bosma (Monotype)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `wght` 100–900, `wdth` 62.5–100 **[file]**
- **Weights:** 9 named instances, Thin to Black **[file]** · v3.011 · 730 glyphs
- **Coverage:** **96 of the 128 Bengali code points, the joint-widest here**, all 10
  Bengali digits, full Latin A–Z a–z **[file]**
- **Proportions:** baseline-to-মাত্রা 9.95px at 16px; tall letters (`ই`) reach
  14.59px; descenders 4.34px **[rendered]**. Its default line box is 22px at 16px —
  **the second-tightest of any Bangla face and tighter than every Latin candidate's
  25px** **[rendered]**, which makes it fit an existing grid with unusually little adjustment.
- **Good at:** everything asked of a workhorse — body, interface, captions;
  sturdiest মাত্রা of any text face; no RFN so it may be subsetted freely.
- **Bad at:** it is a system face and slightly anonymous; it will not give the
  brand a distinctive Bangla voice on its own. **[judgement]**
- **Note:** its `OS/2` `sCapHeight` is 622, which is not the Latin cap height but
  the মাত্রা height **[file]** — so trusting the font's declared cap height would
  mislead you. This is exactly why the numbers here are rendered, not declared.

### 2. Noto Serif Bengali — Juan Bruce, Universal Thirst, Indian Type Foundry, Monotype
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `wght` 100–900, `wdth` 62.5–100 **[file]** · 9 instances · 986 glyphs
- **Coverage:** 96/128 Bengali, 10/10 digits, full Latin **[file]**
- **Proportions:** identical baseline-to-মাত্রা (9.95px) and tall-letter height to
  its sans sibling **[rendered]** — the two are drawn to a shared brief and can be
  swapped without re-tuning sizes. Default line box 25px at 16px **[rendered]**.
- **Good at:** editorial Bangla with genuine warmth; the only serious open-licence
  Bangla serif with a full weight range.
- **Bad at:** **the thinnest মাত্রা measured, 0.0542em — 0.60px at 11px** **[rendered]**.
  Below roughly 14px it will need a heavier weight to hold the headline together.

### 3. Hind Siliguri — Jyotish Sonowal (Indian Type Foundry)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** **no** — 5 static files: Light, Regular, Medium, SemiBold, Bold **[file]**
- **Coverage:** 92/128 Bengali, 10/10 digits, full Latin **[file]** · 821 glyphs
- **Proportions:** the **largest baseline-to-মাত্রা of any text candidate at 10.27px**,
  with the shortest tall letters (13.25px) **[rendered]** — a low, wide, steady texture.
  Default line box 26px at 16px.
- **Good at:** this is the Bangla face Bangladeshi readers meet most often on
  screen, so it reads as unremarkable in the best sense; it is explicitly hinted
  (`ttfautohint` parameters are recorded in its version string **[file]**), which
  helps on low-resolution Windows screens.
- **Bad at:** static only — five files, no continuous weight, and no width axis at
  all, so it cannot move together with a variable Latin partner.

### 4. Tiro Bangla — Fiona Ross & John Hudson (Tiro Typeworks)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** **no** — Regular and Italic only, **one weight** **[file]**
- **Coverage:** 96/128 Bengali, 10/10 digits, full Latin **[file]** · 1,193 glyphs
- **Proportions:** baseline-to-মাত্রা 9.92px **[rendered]**; **the tightest default line
  box of any Bangla candidate at 21px** **[rendered]**. It is the only font in the whole
  set with a non-zero line gap (330 units) **[file]**, so its vertical spacing behaves
  differently from everything else here.
- **Good at:** Fiona Ross is the pre-eminent scholar of Bengali type, and this is
  the most carefully modelled Bengali on the list — the conjuncts and the
  relationship between letter and মাত্রা are drawn, not constructed.
- **Bad at:** **one weight.** For a design system that needs a bold for headings
  and emphasis, this is close to disqualifying on its own, and no amount of
  quality compensates. There is no synthetic bold worth having.

### 5. Anek Bangla — Sulekha Rajkumar, Bangla (Ek Type); Yesha Goshar, Latin
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `wght` 100–800, `wdth` 75–125 **[file]** · 8 instances · 838 glyphs
- **Coverage:** 90/128 Bengali, 10/10 digits, full Latin **[file]**
- **Proportions:** baseline-to-মাত্রা 10.02px at 16px **[rendered]**, a large, even
  texture. **Its default line box is 30px at 16px — by far the loosest of any
  candidate** (1.866em) **[rendered]**, because its declared ascender and descender are
  unusually generous.
- **Good at:** a contemporary Bangla with both weight and width, from a foundry
  with genuine Indic expertise; it can move together with a width-axis Latin.
- **Bad at:** the very large default line box will fight any tight vertical grid
  unless overridden. Narrowest Bengali coverage of the serious body candidates.
- **Gotcha:** variable default weight is **500**, not 400 **[file]**.

### 6. Noto Sans Bengali UI — Jelle Bosma (Monotype)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `wght` 100–900, `wdth` 62.5–100; **12 named instances**
  including SemiCondensed, Condensed and ExtraCondensed **[file]** · 695 glyphs
- **Coverage:** 96/128 Bengali, 10/10 digits — but **only 5 of 58 Latin letters** **[file]**.
- **Proportions:** identical Bangla metrics to Noto Sans Bengali, 22px line box **[rendered]**.
- **Good at:** interfaces with a fixed row height, where the standard face's
  vertical extent would overflow.
- **Bad at:** it has essentially **no Latin**, so it can never set a mixed-script
  line by itself — and this brand mixes scripts constantly. It also has
  `USE_TYPO_METRICS` switched off **[file]**, which means browsers on different
  platforms may compute its line height differently.

### 7. Mina — (designer not recorded in the font)
- **Licence:** SIL OFL 1.1, **RFN `Exo`** (inherited — the Latin derives from Exo) **[file]**
- **Variable:** **no** — Regular and Bold only **[file]** · 927 glyphs
- **Coverage:** 92/128 Bengali, 10/10 digits, full Latin **[file]**
- **Proportions:** baseline-to-মাত্রা 10.18px, but the **shortest tall letters of any
  candidate at 12.35px** **[rendered]** — a compressed vertical range that looks tidy
  but flattens the distinction between letter classes.
- **Good at:** compact settings where vertical space is scarce.
- **Bad at:** two weights only; **its `OS/2` table declares no cap height and no
  x-height at all** **[file]**, and `USE_TYPO_METRICS` is off — it is the least
  completely-engineered file in the set. The name field carries no designer.

### 8. Baloo Da 2 — Noopur Datye, Sulekha Rajkumar, Ek Type
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** yes — `wght` **400–800** **[file]** · 5 instances · 1,264 glyphs
- **Coverage:** **88/128 Bengali — the narrowest of all ten** **[file]**
- **Proportions:** baseline-to-মাত্রা 9.90px with **deep descenders at 5.97px, the
  deepest of any Bangla candidate** **[rendered]**; line box 27px, and the highest
  line-height floor of the text faces at 1.30 **[rendered]**.
- **Good at:** friendly, rounded display headlines; it has real personality.
- **Bad at:** **the weight axis begins at 400** — there is no light or regular-light
  cut, so it cannot set quiet body text. Thin মাত্রা (0.0583em) despite the
  heavy appearance.

### 9. Atma — Gregori Vincens, Jérémie Hornus, Riccardo Olocco, Yoann Minet (Black Foundry)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]**
- **Variable:** **no** — 5 static weights, Light to Bold **[file]** · 760 glyphs
- **Coverage:** 91/128 Bengali, 10/10 digits, full Latin **[file]**
- **Proportions:** baseline-to-মাত্রা 9.98px, tall letters only 13.04px **[rendered]** —
  a wide, low, high-contrast texture with a brush-drawn quality.
- **Good at:** display and packaging work where a warm, hand-influenced Bangla is
  wanted.
- **Bad at:** the stroke contrast that makes it attractive large makes it fragile
  small; `USE_TYPO_METRICS` is off **[file]**. Fewer OpenType Indic features than
  the leaders — no `cjct`, `blws`, `abvs` or `haln` **[file]** — though it still
  passed all 16 conjunct tests.

### 10. Galada — Bengali by Jérémie Hornus, Yoann Minet, Juan Bruce; Latin by Pablo Impallari
- **Licence:** SIL OFL 1.1, **RFN `Lobster`** (inherited — the Latin derives from Lobster) **[file]**
- **Variable:** **no** — a single weight **[file]** · 655 glyphs
- **Coverage:** 91/128 Bengali, 10/10 digits, full Latin **[file]**
- **Proportions:** the **largest baseline-to-মাত্রা of all at 10.74px** and the
  **thickest মাত্রা at 0.1083em** **[rendered]** — a joined, sloped, emphatic script face.
- **Good at:** a one-off logotype or a festival poster.
- **Bad at:** **display only, and not even general display.** It is a script face
  with a strongly sloped headline; it cannot set a sentence of body text, and its
  line-height floor of 1.40 is the highest measured **[rendered]**. Carries an RFN.
  Recorded here because the brief asked for it, not as a serious candidate. **[judgement]**

---

## Monospace candidates (8)

Character advance is the width of one character as a fraction of the em — it
decides how much code fits on a line. **[rendered]**

### 1. JetBrains Mono — Philipp Nurullin, Konstantin Bulenkov
- **Licence:** SIL OFL 1.1, **no RFN** **[file]** · variable `wght` 100–800 · 7 instances **[file]**
- **Advance:** 0.600 em/char **[rendered]** · v2.211 · 1,179 glyphs **[file]**
- **Proportions:** **the largest x-height of any mono candidate at 8.80px (x/cap
  0.753)** **[rendered]**, and the tallest caps at 11.68px — drawn deliberately tall so
  code stays legible at small sizes.
- **Good at:** code at 11–13px, which is where a studio actually reads it; `0` is
  dotted and `l`, `I`, `1` are unambiguous.
- **Bad at:** it has programming ligatures switched on by default, which turn
  `!==` into a single joined mark — pleasant in an editor, confusing in a brand
  specimen or a document a client reads. Turn them off with `font-variant-ligatures: none`.

### 2. IBM Plex Mono — Mike Abbink, Paul van der Laan, Pieter van Rosmalen
- **Licence:** SIL OFL 1.1, **RFN `Plex`** **[file]** · **static only** — 14 files **[file]**
- **Advance:** 0.600 em/char **[rendered]** · v2.3 · 1,033 glyphs
- **Proportions:** cap 11.17px, x 8.26px, x/cap 0.739 **[rendered]** — **identical to
  IBM Plex Sans**, because they are one family.
- **Good at:** pairing with IBM Plex Sans, where the match is exact rather than
  approximate; it is the only true text-and-mono sibling pair in this shortlist.
- **Bad at:** static only, so no continuous weight; and the RFN applies.

### 3. Noto Sans Mono — Monotype Design Team
- **Licence:** SIL OFL 1.1, **no RFN** **[file]** · variable `wght` 100–900, `wdth`
  62.5–100 **[file]** · 9 instances
- **Advance:** 0.600 em/char **[rendered]** · **3,920 glyphs — by far the largest
  coverage of any candidate in this whole shortlist** **[file]**
- **Proportions:** cap 11.42px, x 8.58px, x/cap 0.751 **[rendered]**.
- **Good at:** it is drawn to the same brief as Noto Sans Bengali, so a Noto
  pairing is metrically coherent by construction rather than by luck; it has both
  weight and width axes, unusual for a mono.
- **Bad at:** as with all Noto, it is deliberately neutral to the point of
  anonymity. **[judgement]**

### 4. Geist Mono — Basement.studio, Andrés Briganti, Mateo Zaragoza (Vercel)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]** · variable `wght` 100–900 · 9 instances **[file]**
- **Advance:** 0.600 em/char **[rendered]** · v1.701 · 1,159 glyphs
- **Proportions:** cap 11.36px, x 8.48px, x/cap 0.747; **the shallowest descenders
  of any mono at 2.40px** **[rendered]**, giving a very compact line.
- **Good at:** a current, sharply-drawn technical voice with a full variable
  weight range and no RFN.
- **Bad at:** it is strongly associated with one company's developer brand, which
  may read as borrowed rather than chosen. **[judgement]**

### 5. Source Code Pro — Paul D. Hunt, Teo Tuominen (Adobe)
- **Licence:** SIL OFL 1.1, **RFN `Source`** **[file]** · variable `wght` 200–900 · 8 instances **[file]**
- **Advance:** 0.600 em/char **[rendered]** · 1,568 glyphs
- **Proportions:** cap 10.50px, x 7.78px, x/cap 0.741 **[rendered]** — the smallest
  x-height of the mainstream monos here, so it sets a quieter, smaller-looking line.
- **Good at:** sitting beside Source Sans 3 or Source Serif 4 without competing.
- **Bad at:** RFN; small on the line, so it needs a size bump beside most sans faces.
- **Gotcha:** variable default weight is **200** **[file]**.

### 6. Roboto Mono — Google (Christian Robertson)
- **Licence:** SIL OFL 1.1 — **not Apache-2.0, see the licence note above** — **no RFN** **[file]**
- **Variable:** `wght` 100–700 · 7 instances **[file]** · advance 0.600 em/char **[rendered]**
- **Proportions:** cap 11.38px, x 8.45px, x/cap 0.743 **[rendered]**.
- **Good at:** utterly familiar and safe; excellent fallback behaviour because it
  is already present on most Android devices.
- **Bad at:** **it is the only font in the entire shortlist with `USE_TYPO_METRICS`
  switched off** **[file]**, which means its line height can compute differently
  across platforms — an avoidable inconsistency in a design system.

### 7. Martian Mono — Roman Shamin (Evil Martians)
- **Licence:** SIL OFL 1.1, **no RFN** **[file]** · variable `wght` 100–800, `wdth` 75–112.5 **[file]**
- **Advance:** **0.700 em/char — much the widest here** **[rendered]** · 567 glyphs
- **Proportions:** **cap 12.80px and x 9.60px, the largest of any candidate of any
  script in this shortlist** **[rendered]**. It is a very big, very wide face.
- **Good at:** deliberate, blocky, technical display — labels, version stamps,
  data tables that should look engineered.
- **Bad at:** at 0.700 em/char it is 17% wider than the 0.600 em faces, which fits
  about 14% fewer characters on a line, and its size means it will overpower any
  text face it sits beside unless set several points smaller.
- **Gotcha:** its `wdth` default is **112.5**, not 100 **[file]**.

### 8. Inconsolata — Raph Levien, Cyreal, Brenton Simpson
- **Licence:** SIL OFL 1.1, **no RFN** **[file]** · variable `wght` 200–900, `wdth`
  50–200 · **74 named instances**, the most of any candidate **[file]**
- **Advance:** **0.500 em/char — the narrowest here** **[rendered]** · 964 glyphs
- **Proportions:** cap 9.97px, x 7.31px **[rendered]** — much the smallest mono, so it
  reads a full step down from everything else at the same nominal size.
- **Good at:** dense tabular data where fitting more per line genuinely matters;
  the enormous width range (50–200) is unmatched.
- **Bad at:** it looks noticeably smaller and lighter than any text face beside it
  and needs a compensating size increase; at 0.500 em/char some readers find it
  cramped for code. **[judgement]**

---

## What was deliberately excluded

- **Fonts not on Google Fonts.** SolaimanLipi and Kalpurush are the most widely
  used Bangla fonts in Bangladesh, but neither is distributed under a clear SIL
  OFL or Apache licence from an authoritative source. **[judgement]** They were not
  downloaded and are not recommended, on licence grounds alone.
- **Baloo Da (version 1).** Superseded; only `balooda2` exists in the repository **[file]**.
- **Roboto Slab.** The one Roboto family still under `apache/` **[file]**, but a slab
  serif added nothing the shortlist lacked.

---

## Reproducing every number here

```bash
# from the repository root
export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
.venv/bin/python 06_type/specimen.py
```

Writes `06_type/_data/font_facts.json` (the **[file]** facts),
`06_type/_data/measurements.json` (the **[rendered]** facts) and the seven
specimens in `06_type/specimens/`.
