# Aninda Studio — type measurements

**Date:** 14 August 2026
**Produced by:** `06_type/specimen.py` → `06_type/_data/measurements.json`
**Renderer:** headless Chromium via Playwright (`00_sandbox/browsers`), macOS,
`device_scale_factor` 1 for measurement and 2 for the specimen images.

Everything in this document is a **measurement**, not an estimate. Two sources:

- **[file]** — read out of the font file with `fontTools`.
- **[rendered]** — read off real rendered text in Chromium using the Canvas 2D
  text-metrics API (`actualBoundingBoxAscent` / `Descent` / `width`), which reports
  the **actual inked box** of a string rather than what the font declares about
  itself.

Where the two disagree, **[rendered]** is the truth for design purposes. They do
disagree, and it matters — see "Why declared metrics were not trusted" below.

---

## 1. Latin families at 16px

All values in CSS pixels at `font-size: 16px`, `font-weight: 400` **[rendered]**.
`Line box` is the height the browser gives one line at `line-height: normal`.

| Family | Cap height | x-height | Ascender (`d`) | Descender (`p`) | x/cap | Line box |
|---|---|---|---|---|---|---|
| Inter | 11.64 | **8.68** | 11.64 | 3.27 | 0.746 | 25.0 |
| Libre Franklin | **11.87** | 8.48 | 11.87 | 2.64 | 0.714 | 25.0 |
| Archivo | 10.98 | 8.42 | 11.57 | 2.77 | **0.767** | 25.0 |
| Public Sans | 11.57 | 8.27 | 11.89 | **2.58** | 0.715 | 25.0 |
| IBM Plex Sans | 11.17 | 8.26 | 11.84 | 3.20 | 0.739 | 25.0 |
| Roboto Flex | 11.38 | 8.17 | 11.97 | 3.26 | 0.718 | 25.0 |
| Instrument Sans | 11.52 | 8.16 | 11.52 | 3.28 | 0.708 | 25.0 |
| Literata | 11.23 | 8.12 | **12.26** | 3.46 | 0.723 | **26.0** |
| Work Sans | 10.56 | 8.00 | 11.68 | 3.36 | 0.758 | 25.0 |
| Source Sans 3 | 10.50 | 7.78 | 11.40 | 3.28 | 0.741 | 25.0 |
| Source Serif 4 | 10.72 | 7.78 | 11.79 | 3.76 | 0.725 | 25.0 |
| Newsreader | 10.82 | **7.05** | 11.44 | **3.99** | **0.651** | 25.0 |

**Spread:** x-height varies by 1.63px — 23% — between the largest (Inter) and
smallest (Newsreader) at the *same* nominal size. This is why "16px" is not a
statement about how big text looks.

**Line box:** eleven of the twelve give exactly 25.0px; Literata alone gives
26.0px. Any of these can share one vertical rhythm with a single exception.

---

## 2. Monospace families at 16px

| Family | Cap height | x-height | x/cap | Advance per character | Line box |
|---|---|---|---|---|---|
| Martian Mono | **12.80** | **9.60** | 0.750 | **0.700 em** | 25.0 |
| JetBrains Mono | 11.68 | 8.80 | 0.753 | 0.600 em | 25.0 |
| Noto Sans Mono | 11.42 | 8.58 | 0.751 | 0.600 em | 25.0 |
| Geist Mono | 11.36 | 8.48 | 0.746 | 0.600 em | 25.0 |
| Roboto Mono | 11.38 | 8.45 | 0.743 | 0.600 em | 25.0 |
| IBM Plex Mono | 11.17 | 8.26 | 0.739 | 0.600 em | 25.0 |
| Source Code Pro | 10.50 | 7.78 | 0.741 | 0.600 em | 25.0 |
| Inconsolata | **9.97** | **7.31** | 0.734 | **0.500 em** | 25.0 |

**Advance** was measured as the rendered width of the string `0123456789` divided
by ten, then by the font size **[rendered]**. Six of the eight sit at exactly
0.600 em. Martian Mono is 17% wider and Inconsolata 17% narrower, so swapping
either one into a layout built for the others will reflow every line of code.

**Note:** IBM Plex Mono's cap height, x-height and advance are *identical* to IBM
Plex Sans' — the two are one family. No other text/mono pair here matches exactly.

---

## 3. Bangla families at 16px

For Bangla, the height that governs apparent size is **baseline to মাত্রা**,
measured as the inked ascent of `ক` **[rendered]**. `Tall` is the inked ascent of
`ই`, which rises above the মাত্রা. `Descender` is the inked descent of the test
line `রুগ্ন হৃদয়ে কৃষ্ণচূড়া ফুটেছে`, which carries below-base conjuncts.

| Family | Baseline→মাত্রা | Tall (`ই`) | Descender | Line box | মাত্রা thickness |
|---|---|---|---|---|---|
| Galada | **10.74** | **15.76** | 5.95 | 26.0 | **0.1083 em** |
| Hind Siliguri | 10.27 | 13.25 | 4.50 | 26.0 | 0.0708 em |
| Mina | 10.18 | **12.35** | 5.23 | 25.0 | 0.0625 em |
| Anek Bangla | 10.02 | 14.07 | 5.45 | **30.0** | 0.0667 em |
| Atma | 9.98 | 13.04 | 4.94 | 26.0 | 0.0667 em |
| Noto Sans Bengali | 9.95 | 14.59 | 4.34 | **22.0** | **0.0750 em** |
| Noto Serif Bengali | 9.95 | 14.67 | 4.22 | 25.0 | **0.0542 em** |
| Noto Sans Bengali UI | 9.95 | 14.59 | 4.34 | 22.0 | 0.0750 em |
| Tiro Bangla | 9.92 | 14.34 | **4.08** | **21.0** | 0.0667 em |
| Baloo Da 2 | **9.90** | 14.38 | **5.97** | 27.0 | 0.0583 em |

**Spread is far narrower than Latin's:** baseline-to-মাত্রা varies by only 0.84px
(8%) across all ten, against 23% for Latin x-heights. Bangla faces agree with each
other about size much more closely than Latin faces do.

**Line box** is the outlier column. Tiro Bangla (21.0) and the two Noto Sans
Bengali variants (22.0) are *tighter* than every Latin candidate's 25.0. Anek
Bangla at 30.0 is 20% looser than any Latin face and will force a grid open.

### মাত্রা continuity — the disqualification test

Each face rendered `কলকাতা` at 240px — a word in which every letter carries a
মাত্রা, so the headline should run unbroken from the first letter to the last. Every
column of pixels across the word was then checked for ink in the upper band of the
letterform. Continuity is the longest unbroken run of such columns divided by the
word's total inked width **[rendered]**.

| Family | Columns carrying the মাত্রা | Continuity |
|---|---|---|
| Noto Sans Bengali | 866 / 866 | 1.000 |
| Noto Sans Bengali UI | 866 / 866 | 1.000 |
| Anek Bangla | 877 / 877 | 1.000 |
| Hind Siliguri | 828 / 828 | 1.000 |
| Baloo Da 2 | 840 / 840 | 1.000 |
| Noto Serif Bengali | 726 / 726 | 1.000 |
| Galada | 774 / 774 | 1.000 |
| Atma | 678 / 678 | 1.000 |
| Mina | 863 / 863 | 1.000 |
| Tiro Bangla | 784 / 787 | 0.996 |

**All ten keep the মাত্রা unbroken. No candidate is disqualified on this ground.**
Tiro Bangla's three missing columns out of 787 are at a tapered stroke terminal;
I checked the rendered crop by eye and the headline is visually continuous.

*Method note, recorded so the error is not repeated: two earlier versions of this
test gave wrong answers and were discarded. Scanning a single pixel row failed
every face whose মাত্রা is tapered or sloped — it scored Galada at 0.262 and Tiro
Bangla at 0.677, both of which are plainly continuous when you look at the crop.
Walking the topmost-ink edge failed every face with letter parts rising above the
মাত্রা, inverting the result. Only the band test is sound.*

### মাত্রা thickness in device pixels — what actually discriminates

Since nothing failed the pass/fail test, the useful measurement is how *thick* the
headline is, because a stroke below one device pixel greys out or drops away on an
ordinary 1× screen. Measured as the median vertical run of ink at the top edge,
across the word **[rendered]**:

| Family | em | at 16px | at 12px | at 11px |
|---|---|---|---|---|
| Galada | 0.1083 | 1.73px | 1.30px | 1.19px |
| Noto Sans Bengali / UI | 0.0750 | 1.20px | 0.90px | 0.83px |
| Hind Siliguri | 0.0708 | 1.13px | 0.85px | 0.78px |
| Anek Bangla | 0.0667 | 1.07px | 0.80px | 0.73px |
| Tiro Bangla | 0.0667 | 1.07px | 0.80px | 0.73px |
| Atma | 0.0667 | 1.07px | 0.80px | 0.73px |
| Mina | 0.0625 | 1.00px | 0.75px | 0.69px |
| Baloo Da 2 | 0.0583 | 0.93px | 0.70px | 0.64px |
| Noto Serif Bengali | 0.0542 | 0.87px | 0.65px | 0.60px |

**Only Galada holds a full device pixel below 16px, and Galada is a display face.**
Every text face's মাত্রা goes sub-pixel somewhere between 12px and 16px on a 1×
screen. On a 2× screen all of them are comfortable. The design rule that follows
is in §6.

---

## 4. The Latin : Bangla apparent-size ratio

**This is the headline number the design system needs.**

The comparison is like for like: Latin **x-height** against Bangla
**baseline-to-মাত্রা height**, both read from rendered ink at the same nominal size
**[rendered]**. The multiplier is `latin_x_height ÷ bangla_matra_height` — multiply
the Latin size by it to get the Bangla size that looks the same.

### Measured per pairing, per size

| Pairing | 11px | 12px | 16px | 28px | 56px | 100px |
|---|---|---|---|---|---|---|
| 01 Inter + Noto Sans Bengali | 0.878 | 0.878 | **0.872** | 0.840 | 0.829 | 0.829 |
| 02 IBM Plex Sans + Noto Sans Bengali | 0.830 | 0.830 | **0.830** | 0.830 | 0.830 | 0.830 |
| 03 Newsreader + Noto Serif Bengali | 0.766 | 0.754 | **0.708** | 0.710 | 0.782 | 0.824 |
| 04 Literata + Tiro Bangla | 0.822 | 0.818 | **0.818** | 0.820 | 0.825 | 0.828 |
| 05 Source Sans 3 + Hind Siliguri | 0.757 | 0.757 | **0.757** | 0.757 | 0.757 | 0.757 |
| 06 Public Sans + Noto Sans Bengali | 0.831 | 0.831 | **0.831** | 0.831 | 0.831 | 0.831 |
| 07 Archivo + Anek Bangla | 0.840 | 0.840 | **0.840** | 0.840 | 0.840 | 0.840 |
| 08 Literata + Noto Serif Bengali | 0.819 | 0.815 | **0.816** | 0.817 | 0.822 | 0.825 |

### Why some rows are flat and some are not

Pairings 02, 05, 06 and 07 are flat because their Latin face has no optical-size
axis, so its x-height is a fixed fraction of the em at every size.

Pairings 01, 03, 04 and 08 vary because their Latin face redraws itself as the size
changes. This was verified independently rather than assumed: I instanced each
variable font at specific `opsz` values with `fontTools.varLib.instancer` and
measured the outlines directly, then compared against what Chromium rendered. They
match exactly, which confirms **browsers apply optical sizing automatically**
(`font-optical-sizing: auto` is the default) **[file]** + **[rendered]**:

| Family | opsz 8 | opsz 12 | opsz 16 | opsz 28 | opsz 56 | opsz 72 |
|---|---|---|---|---|---|---|
| Inter (axis 14–32) | 0.5459 | 0.5459 | 0.5425 | 0.5224 | 0.5156 | 0.5156 |
| Newsreader (6–72) | 0.4977 | 0.4690 | 0.4403 | 0.4419 | 0.4865 | 0.5120 |
| Literata (7–72) | 0.5166 | 0.5070 | 0.5073 | 0.5083 | 0.5112 | 0.5130 |
| Source Serif 4 (8–60) | 0.5080 | 0.4970 | 0.4860 | 0.4704 | 0.4543 | 0.4520 |
| Roboto Flex (8–144) | 0.5317 | 0.5197 | 0.5107 | 0.4926 | 0.4678 | 0.4576 |

*x-height as a fraction of the em at each optical size.*

**Consequence for the design system:** for a pairing built on an optical-size
Latin, the per-script size token cannot be a single value. It must be a small
table, one entry per step of the type scale. For the other pairings one number
does the whole job.

### Underlying per-family values at 16px

| | Latin x-height (em) | | Bangla মাত্রা height (em) |
|---|---|---|---|
| Inter | 0.5425 | Noto Sans Bengali | 0.6220 |
| IBM Plex Sans | 0.5160 | Noto Serif Bengali | 0.6220 |
| Public Sans | 0.5170 | Hind Siliguri | 0.6420 |
| Archivo | 0.5260 | Anek Bangla | 0.6262 |
| Literata | 0.5073 | Tiro Bangla | 0.6200 |
| Source Sans 3 | 0.4861 | Baloo Da 2 | 0.6190 |
| Newsreader | 0.4403 | Galada | 0.6710 |

Bangla's reading height sits around 0.62 em; Latin's sits around 0.51 em. **The
gap is structural — no Latin face closes it entirely**, so some correction is
always needed. Inter at body size (0.5425 em) closes the most of it.

---

## 5. Line height — where the মাত্রা stops colliding

**Method.** A descender-heavy Bangla line (`রুগ্ন হৃদয়ে কৃষ্ণচূড়া ফুটেছে`, carrying
below-base conjuncts and vowel signs) was stacked directly above a headline-heavy
line (`কলকাতা বরিশাল ঢাকা চট্টগ্রাম`) at 40px. `line-height` was raised from 1.00 in
steps of 0.05, re-rendering each time, until the rendered ink separated into two
distinct horizontal bands with clear white between them. The first value that
achieves separation is the **collision floor** **[rendered]**.

The floor is where the ink merely *stops touching*. Running text needs air above
that, so the recommended token is the floor plus 0.35, rounded to a tidy step.

| Family | Collision floor | At 16px | Recommended token | At 16px |
|---|---|---|---|---|
| Hind Siliguri | 1.20 | 19.2px | **1.55** | 24.8px |
| Tiro Bangla | 1.20 | 19.2px | **1.55** | 24.8px |
| Atma | 1.20 | 19.2px | 1.55 | 24.8px |
| Noto Sans Bengali | 1.25 | 20.0px | **1.60** | 25.6px |
| Noto Serif Bengali | 1.25 | 20.0px | **1.60** | 25.6px |
| Noto Sans Bengali UI | 1.25 | 20.0px | 1.60 | 25.6px |
| Anek Bangla | 1.25 | 20.0px | **1.60** | 25.6px |
| Mina | 1.25 | 20.0px | 1.60 | 25.6px |
| Baloo Da 2 | 1.30 | 20.8px | 1.65 | 26.4px |
| Galada | 1.40 | 22.4px | 1.75 | 28.0px |

**Reading:** Bangla will not collide at any line-height at or above 1.30 for any
text face here — but "not colliding" is a low bar, and every one of these needs
roughly 1.55–1.65 to read comfortably, against 1.5–1.6 for the Latin. **Bangla
needs slightly more leading than Latin, but far less than is often assumed.**

**Caution — do not use the fonts' own declared line spacing.** The default line
box the browser computes from each font's declared metrics is wildly inconsistent
**[file]**: Anek Bangla declares 1.866 em, Baloo Da 2 1.684, Hind Siliguri 1.617,
Noto Sans Bengali 1.325, Tiro Bangla 1.330 (and Tiro is the only font in the whole
set with a non-zero line gap, 330 units). Setting `line-height: normal` would give
five different rhythms. Set the token explicitly.

---

## 6. Tokens this produces

Ready to hand to the design system. Values for the recommended pairing (01);
substitute from the tables above for the others.

```
/* per-script size correction — Inter + Noto Sans Bengali */
--type-bangla-scale-display   : 0.829;   /* 56px  -> 46.4px */
--type-bangla-scale-heading   : 0.840;   /* 28px  -> 23.5px */
--type-bangla-scale-body      : 0.872;   /* 16px  -> 14.0px */
--type-bangla-scale-caption   : 0.878;   /* 12px  -> 10.5px */

/* line height */
--type-line-latin-body        : 1.60;
--type-line-bangla-body       : 1.60;    /* floor measured at 1.25 */

/* the floor that protects the মাত্রা at small sizes */
--type-bangla-min-size        : 12px;
```

**The `--type-bangla-min-size` rule, and why it exists.** Applying the multiplier
strictly all the way down drives Bangla below the size at which its মাত্রা and
conjuncts survive. At an 11px Latin caption, pairing 01 gives 9.66px of Bangla with
a 0.72px মাত্রা, and pairing 03 gives 8.43px with a 0.46px মাত্রা **[rendered]**. **Do
not apply the full multiplier below 14px; clamp Bangla at 12px minimum.** Below
that, let the Bangla run slightly larger than strict parity would say. This is a
**[judgement]** built on the measurements, not itself a measurement — the trade is
between exact size parity and Bangla legibility, and legibility should win.

---

## 7. Why declared metrics were not trusted

Fonts declare their own cap height and x-height in the `OS/2` table. For Bangla
faces those declarations are misleading, and following them would have produced
wrong tokens.

**Noto Sans Bengali declares `sCapHeight` = 622** **[file]**. That is not the height
of its capital `H` — the rendered cap height is 0.714 em **[rendered]**. 0.622 em is
the **মাত্রা** height. The field has been repurposed. A design system that read
`sCapHeight` to align scripts would be aligning to the wrong thing entirely.

**Mina declares no cap height and no x-height at all** — both fields are absent
from its `OS/2` table **[file]**.

**Five families have `USE_TYPO_METRICS` switched off** — Roboto Mono, Noto Sans
Bengali UI, Galada, Atma and Mina **[file]** — which means browsers on different
platforms may compute their line height from different fields and disagree.

This is the reason every number in §1–§5 is rendered rather than declared.

---

## 8. What could not be measured

- **Any renderer other than Chromium on macOS.** All rendered values come from one
  engine on one platform. Windows (DirectWrite) and Android apply different
  hinting and stem darkening; the sub-pixel মাত্রা findings at 11–12px are the most
  likely to differ, and Hind Siliguri — the only explicitly hinted Bangla
  candidate **[file]** — may perform relatively better on Windows than these numbers
  suggest. Safari and Firefox were not tested.
- **Print.** Screen only. The device-pixel argument in §3 does not apply on paper.
- **Whether the conjuncts are well drawn.** HarfBuzz shaping was tested on 16
  conjuncts and all ten Bangla faces passed with no dotted circles, no missing
  glyphs and no stray hasantas — but that is a test for *failure*, not for
  *quality*. Whether a face's conjuncts look right to a Bangla reader cannot be
  measured and was not assessed.
- **Exhaustive conjunct coverage.** Sixteen conjuncts and five words were tested,
  not the full combinatorial set.
- **Real reading.** No reader, in either script, was asked whether the corrected
  sizes actually feel equal. The multipliers equalise a measured height; that is a
  strong proxy for apparent size, not a substitute for a person's judgement.
