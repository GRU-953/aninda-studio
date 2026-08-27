# Aninda Studio — type recommendation

**Date:** 14 August 2026
**Evidence:** `SHORTLIST.md` (30 families), `pairings.md` (8 pairings),
`MEASUREMENTS.md` (all numbers), `specimens/` (8 rendered pages).

---

## This recommendation was not the one that shipped

**Superseded. Read this section before the rest of the document.**

This page recommended **Inter + Noto Sans Bengali + JetBrains Mono** on 14 August
2026, and the system shipped **Literata + Noto Serif Bengali + Aninda Mono** — this
document's own *"More editorial"* row, at a multiplier of ×0.816 rather than the
recommended ×0.872. The reversal was visible only in `07_tokens/build.py` and
nowhere in prose, so a reader following this page was sent to the wrong stack for
two weeks. That was gap **G-REC-1**.

Why the editorial pairing won: Literata carries an optical-size axis from 7 to 72,
so its letterforms are redrawn for the size rather than scaled, and its x-height is
nearly flat across that range — which is what held the Bangla multiplier almost
constant across the whole scale. The recommendation below preferred Inter partly to
avoid a Reserved Font Name rename, and that cost was paid anyway: the monospace
face is a subset of IBM Plex Mono, `Plex` is a Reserved Font Name, and subsetting
is a modification under OFL 1.1 clause 3, so it ships as **Aninda Mono**.

And since 27 August 2026 there is no Bengali face at all. The system ships English,
so the stack is **Literata + Aninda Mono** — two faces, not three. Every Bangla
figure in this document is a record of measurements taken while the system was
bilingual, and they are kept because they are the evidence for choosing Literata.

The rest of this page is left exactly as it was written. A recommendation that was
not taken is worth more intact than tidied.

---

## The recommendation as written on 14 August 2026

# Inter + Noto Sans Bengali + JetBrains Mono

*Specimen: `specimens/01-core-modern.png`*

| | Family | Licence | Axes | RFN |
|---|---|---|---|---|
| Latin | **Inter** 4.001 — Rasmus Andersson | SIL OFL 1.1 | `opsz` 14–32, `wght` 100–900 | none |
| Bangla | **Noto Sans Bengali** 3.011 — Joana Ranito (Universal Thirst) with Jelle Bosma (Monotype) | SIL OFL 1.1 | `wght` 100–900, `wdth` 62.5–100 | none |
| Mono | **JetBrains Mono** 2.211 — Philipp Nurullin, Konstantin Bulenkov | SIL OFL 1.1 | `wght` 100–800 | none |

### Why

**1. It needs the least correction between the two scripts — and that is the whole
problem this brand has to solve.**

Bangla and Latin do not look the same size at the same size. Bangla's reading
height sits around 0.62 em; Latin's around 0.51 em. Every pairing therefore needs a
per-script size multiplier, and a multiplier nearer 1.000 is better because it
means less correction, fewer places to get it wrong, and — the point that decides
it — **a line mixing both scripts inline needs no adjustment at all**. This brand
will write Bangla sentences containing English product names constantly. Measured:

| Pairing | Multiplier at 16px |
|---|---|
| **01 Inter + Noto Sans Bengali** | **0.872 — best of eight** |
| 07 Archivo + Anek Bangla | 0.840 |
| 06 Public Sans + Noto Sans Bengali | 0.831 |
| 02 IBM Plex Sans + Noto Sans Bengali | 0.830 |
| 08 Literata + Noto Serif Bengali | 0.816 |
| 05 Source Sans 3 + Hind Siliguri | 0.757 |
| 03 Newsreader + Noto Serif Bengali | 0.708 — worst |

**2. Inter's optical-size axis works in exactly the right direction.**

This is the non-obvious finding, and it is the strongest single argument here.
Because Bangla's problem is that it is *taller* than Latin, what you want is a
Latin face that grows when small. Inter does precisely that: its x-height rises
from 0.5156 em at display sizes to 0.5459 em at caption sizes **[rendered]**. It
actively closes the gap where the gap hurts most. I verified this independently by
instancing the font at each optical size with `fontTools` and comparing against
what Chromium rendered — they match exactly, confirming browsers apply optical
sizing automatically. Inter's worst multiplier anywhere on the scale (0.829 at
56px) is still better than four other pairings' best.

**3. Noto Sans Bengali is the strongest Bangla face for a system that must work
small.**

- **Sturdiest মাত্রা of any text face measured** — 0.0750 em, against 0.0542 em for
  Noto Serif Bengali. At caption sizes this is the difference between a headline
  stroke that holds and one that greys out **[rendered]**.
- **Joint-widest Bengali coverage** — 96 of 128 code points, plus all ten Bengali
  digits and a full Latin **[file]**.
- **Tightest line box of any workhorse face here** — 22px at 16px, tighter than
  every Latin candidate's 25px **[rendered]**, so it drops into a Latin-derived
  vertical grid instead of forcing it open.
- **Variable in both weight and width**, so it can follow a weight token and
  compress independently if a layout demands it **[file]**.
- **মাত্রা measured continuous** across every one of 866 pixel columns, and all
  sixteen tested conjuncts shape correctly under HarfBuzz with no dotted circles,
  no missing glyphs and no stray hasantas **[file]** + **[rendered]**.

**4. No Reserved Font Name on any of the three.**

All three are SIL OFL 1.1 with no RFN **[file]**. Subsetting a webfont — stripping
unused glyphs to cut file size — counts as modification, and a Reserved Font Name
would force a rename on every build. Four of the shortlisted families carry one
(`Plex`, `Source`, `Lobster`, `Exo`); this pairing avoids the problem entirely. For
a one-person studio that has to maintain its own build pipeline, this is a small
permanent saving.

**5. JetBrains Mono is drawn for the size code is actually read at.**

Largest x-height of any mono candidate at 8.80px, tallest caps at 11.68px
**[rendered]**, which keeps code legible at 11–13px. Its `0 O o 1 l I` are
unambiguous, and it has a continuous weight axis where IBM Plex Mono is static.
One thing to configure: **switch its programming ligatures off**
(`font-variant-ligatures: none`) outside a code editor, or `!==` renders as a
single joined mark in documents clients read.

### What is weak about it, stated plainly

- **Inter has no width axis**, so the Latin cannot compress with the Bangla. If
  the brand later needs condensed settings, only Bangla and mono can follow.
- **Both faces are extremely widely used and deliberately neutral.** This pairing
  is correct rather than characterful, and it will not make the studio look
  distinctive by itself **[judgement]**. Distinctiveness will have to come from the
  mark, colour and layout, not the type.
- Even here, the মাত্রা falls below one device pixel at caption sizes on a 1×
  screen (0.72px at an 11px Latin caption) **[rendered]**. That is a property of
  Bangla at small sizes rather than a fault, and the mitigation is the size floor
  below.

### Non-negotiable rule that comes with this recommendation

Do **not** apply the multiplier strictly all the way down. Below 14px it drives
Bangla under the size at which its মাত্রা and conjuncts survive.

```
--type-bangla-scale-display : 0.829   /* 56px -> 46.4px */
--type-bangla-scale-heading : 0.840   /* 28px -> 23.5px */
--type-bangla-scale-body    : 0.872   /* 16px -> 14.0px */
--type-bangla-scale-caption : 0.878   /* 12px -> 10.5px, then clamped */
--type-bangla-min-size      : 12px    /* hard floor */
--type-line-bangla-body     : 1.60    /* collision floor measured at 1.25 */
```

The floor is a **[judgement]** built on the measurements, not a measurement: the
trade is between exact size parity and Bangla legibility, and legibility wins.

---

## Second choice

# IBM Plex Sans + Noto Sans Bengali + IBM Plex Mono

*Specimen: `specimens/02-technical.png`*

Take this if the studio would rather have **perfect text-and-code unity** than
best-in-class size parity.

IBM Plex Sans and IBM Plex Mono are one family drawn by the same three designers,
and the measurements confirm it exactly rather than approximately: identical cap
height (11.17px), identical x-height (8.26px), identical 0.600 em advance
**[rendered]**. No other pairing in this shortlist has that. For a studio whose work
*is* software, prose and code sitting together without a visible seam is a real
asset. The multiplier is a flat ×0.830 at every size, so the size token is a single
number with no scale-dependent table — genuinely simpler to maintain than the
recommendation's four-value table. Plex Sans and Noto Sans Bengali both carry
weight *and* width axes, so the two text faces can compress together.

**Why it is second and not first:** both Plex faces carry the Reserved Font Name
`Plex` **[file]**, so every subsetted webfont build needs a rename. IBM Plex Mono is
static, so it cannot follow a weight token. Plex Sans stops at weight 700, leaving
no genuinely heavy display cut. And at ×0.830 it needs measurably more correction
than Inter for mixed-script lines.

---

## The four brand directions

Four directions will be built and they need not all use the same type. Here is
what I would use for each, with the reasoning.

### More *editorial*

# Literata + Noto Serif Bengali + IBM Plex Mono
*Specimen: `specimens/08-editorial-revised.png`*

**Not Newsreader.** The obvious editorial pairing — Newsreader + Noto Serif Bengali
(`specimens/03-editorial.png`) — is the most beautiful page in the set and the
measurements reject it. Newsreader has the smallest x-height of any candidate
(0.4403 em at body size), so matching the Bangla honestly means shrinking it to
×0.708, or 11.33px of Bangla against 16px of Latin. Look at the specimen: the
Bangla column is visibly smaller, lighter and less present than the English. For a
brand whose two audiences are explicitly equal, that is the one failure that is not
acceptable, and it gets worse at caption sizes where Noto Serif Bengali's মাত্রা
falls to 0.46 device pixels.

Swapping Literata in fixes it without leaving the editorial register: same wide
optical-size axis (7–72), but an x-height a full pixel taller, which lifts the
multiplier to **×0.816** and holds it nearly flat across the whole scale
**[rendered]**. Noto Serif Bengali is kept over Tiro Bangla because it has a full
weight axis where Tiro has one weight, and because it shares metrics with Noto Sans
Bengali, so the system can move between serif and sans without re-tuning sizes.

**One rule attached:** Noto Serif Bengali's মাত্রা is the thinnest measured. Set
Bangla captions at **weight 500 rather than 400** — that thickens the headline
without touching the size relationship.

### More *technical*

# IBM Plex Sans + Noto Sans Bengali + IBM Plex Mono
*Specimen: `specimens/02-technical.png`*

The same pairing as the second choice, and for the same reason: it is the only one
where the text face and the code face are genuinely the same family rather than two
faces chosen to look similar. Plex was drawn for a technology company and reads
that way without costume. Accept the `Plex` Reserved Font Name as the price.

*If the technical direction wants to look sharper and more current rather than
corporate, substitute **Geist Mono** for IBM Plex Mono — same 0.600 em advance, a
full variable weight range, and no RFN **[file]** — at the cost of losing the exact
family match.*

### More *rooted / local*

This one splits, because "rooted" can mean two different things, and the right
answer differs.

**If rooted means *familiar to a Bangladeshi reader* — the everyday, unremarkable,
gets-read-not-noticed quality:**

# Source Sans 3 + Hind Siliguri + Source Code Pro
*Specimen: `specimens/05-rooted-familiar.png`*

Hind Siliguri is the Bangla face Bangladeshi readers actually meet every day on
screen. It is also the most practical choice for poor conditions: the only Bangla
candidate with explicit `ttfautohint` hinting recorded in its version string
**[file]**, which helps on the low-resolution Windows machines still common in
Bangladesh, and it has the largest baseline-to-মাত্রা height of any text candidate
(10.27px) with a sturdy 0.0708 em headline **[rendered]**. Source Sans 3 is chosen
precisely because it recedes and lets the Bangla lead.
**Costs, stated plainly:** Hind Siliguri is **static — five files, no variable axis
at all** **[file]**, so it cannot follow a weight token; the multiplier is ×0.757,
second-worst of the eight; and both Source faces carry the `Source` RFN.

**If rooted means *authentically drawn Bengali* — historical depth rather than
everyday familiarity:**

# Literata + Tiro Bangla + IBM Plex Mono
*Specimen: `specimens/04-rooted-scholarly.png`*

Tiro Bangla is the best-drawn Bengali on this list and it is not close. Fiona Ross
is the pre-eminent scholar of Bengali type; the relationship between letter and
মাত্রা here is drawn rather than constructed, and it shows in running text. It also
gives the most vertically compact setting available — the tightest line box of any
Bangla candidate at 21px **[rendered]**.
**But it has exactly one weight** **[file]**. No bold for headings, no light for
captions, no emphasis inside a paragraph. **Use this for a single considered
artefact — an essay, a printed piece, a colophon — never as a system default.**

### More *contemporary / distinctive* (a fourth direction, since four are planned)

# Archivo + Anek Bangla + Martian Mono
*Specimen: `specimens/07-contemporary.png`*

The only pairing where **all three families carry both a weight and a width axis**
**[file]** — one token can compress or expand the whole system across both scripts
and the code face at once, and Archivo's width range (62–125) is the broadest of
any Latin candidate. It is the most distinctive-looking pairing here and the one
most likely to read as a considered brand rather than a default **[judgement]**.
**Watch two things:** Anek Bangla's default line box is 30px at 16px, by far the
loosest measured, so override it explicitly; and Martian Mono is the largest face
in the entire shortlist at 0.700 em per character, so set it several points down or
it will overpower everything beside it.

---

## Summary

| Purpose | Latin | Bangla | Mono | Multiplier @16px |
|---|---|---|---|---|
| **Recommended default** | Inter | Noto Sans Bengali | JetBrains Mono | 0.872 |
| **Second choice** | IBM Plex Sans | Noto Sans Bengali | IBM Plex Mono | 0.830 |
| Editorial | Literata | Noto Serif Bengali | IBM Plex Mono | 0.816 |
| Technical | IBM Plex Sans | Noto Sans Bengali | IBM Plex Mono | 0.830 |
| Rooted — familiar | Source Sans 3 | Hind Siliguri | Source Code Pro | 0.757 |
| Rooted — scholarly | Literata | Tiro Bangla | IBM Plex Mono | 0.818 |
| Contemporary | Archivo | Anek Bangla | Martian Mono | 0.840 |

**Noto Sans Bengali appears in three of the seven rows, and Noto Serif Bengali in
one more.** That is deliberate and useful: the two share metrics, so a direction
can move between them without any size token changing.

---

## What I could not test — read this before locking anything

These are real gaps, not disclaimers.

1. **No Bangla reader has looked at this.** Every Bangla judgement here is
   mechanical: HarfBuzz shaping produced no dotted circles, no missing glyphs and
   no stray hasantas across sixteen conjuncts, and pixel analysis confirmed the
   মাত্রা is continuous in all ten faces. **That proves nothing is broken. It does
   not prove the Bangla is good.** Whether Noto Sans Bengali's conjuncts read as
   well-drawn Bangla to someone in Barishal is a judgement no measurement can
   make. **This is the single most important thing to check before committing**,
   and it needs a person, not a script.

2. **One renderer, one platform.** Every rendered number comes from headless
   Chromium on macOS. Windows uses DirectWrite and Android its own stack; hinting
   and stem darkening differ. The findings most likely to move are the sub-pixel
   মাত্রা results at 11–12px — and note that Hind Siliguri, the only explicitly
   hinted Bangla candidate, may perform relatively better on Windows than these
   numbers suggest. Safari and Firefox were not tested.

3. **Screen only.** Nothing was tested in print. The device-pixel argument that
   drives the 12px Bangla floor does not apply on paper, so print can go smaller.

4. **Conjunct coverage is a sample, not a sweep.** Sixteen conjuncts and five
   words were tested, not the full combinatorial set of Bengali conjuncts.

5. **No reader was asked whether the corrected sizes feel equal.** The multipliers
   equalise a measured height, which is a strong proxy for apparent size but not a
   substitute for someone's eye.

6. **Fallback and email were not tested** — how these stacks degrade when webfonts
   fail to load, and what happens in email clients, which cannot use webfonts.

7. **Licence reading is not legal advice.** I read each `OFL.txt` in full and
   extracted the Reserved Font Name declarations mechanically **[file]**. All 30
   families are SIL OFL 1.1. I am confident in the reading; it is still a reading.

8. **One thing worth re-checking periodically:** Roboto Mono and Roboto Flex are
   widely described as Apache-2.0 and are not — both now sit under `ofl/` with SIL
   OFL licence files, with only Roboto Slab left under `apache/` **[file]**. Google
   moves families between licences occasionally, so verify from the repository
   rather than from memory if either is ever adopted.

---

## Reproducing all of this

```bash
# from the repository root
export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
.venv/bin/python 06_type/specimen.py
```

Reads the fonts in `06_type/candidates/`, writes `06_type/_data/font_facts.json`
and `06_type/_data/measurements.json`, and renders all eight specimens.
