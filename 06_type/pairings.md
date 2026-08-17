# Aninda Studio — candidate type pairings

**Date:** 14 August 2026
**Specimens:** `06_type/specimens/01-*.png` … `07-*.png` — one rendered page per
pairing, both scripts side by side at the same measure.
**Raw data:** `06_type/_data/measurements.json`

Seven pairings, each Latin + Bangla + monospace. Every pairing was rendered and
measured; none of the judgements below rest on looking at a specimen image alone.

---

## The one thing that decides these pairings

Bangla and Latin do not look the same size at the same size.

In Latin, what the eye reads as "how big is this text" is the **x-height** — the
height of a lowercase `x` — not the nominal point size. In Bangla, the equivalent
is the height from the baseline up to the **মাত্রা**, the headline stroke, because
that is where most of the letter mass sits.

Measured at 16px **[rendered]**, Latin x-heights across the twelve candidates run
from 7.05px (Newsreader) to 8.68px (Inter). Bangla baseline-to-মাত্রা heights run
from 9.90px (Baloo Da 2) to 10.74px (Galada). **Bangla is consistently the taller
of the two.** Set both at a flat 16px and the Bangla will look bigger and heavier
than the Latin beside it — which you can see for yourself in the "control" row on
every specimen, where the correction is deliberately switched off.

So each pairing needs a **per-script size multiplier**: the number you multiply
the Latin size by to get the Bangla size that *looks* the same. That multiplier
is the single most important token this exercise produces, and it is different
for every pairing.

**One complication, and it is a real one.** Four of the Latin candidates have an
optical-size axis, which redraws the letters as the size changes — and that
changes the x-height. So for those families the multiplier is **not one number**;
it has to be measured at every size in the type scale. Inter's x-height is
0.5459em at 12px but 0.5156em at 56px **[rendered]**, so its multiplier moves from
0.878 to 0.829 across the scale. Pairings built on a Latin without an optical
axis have a single flat multiplier at every size.

---

## Summary — all seven measured

Bangla size multiplier, measured at each step of the scale **[rendered]**:

| # | Pairing | 11px | 12px | 16px | 28px | 56px | Flat? |
|---|---|---|---|---|---|---|---|
| 01 | Inter + Noto Sans Bengali + JetBrains Mono | 0.878 | 0.878 | **0.872** | 0.840 | 0.829 | no — `opsz` |
| 02 | IBM Plex Sans + Noto Sans Bengali + IBM Plex Mono | 0.830 | 0.830 | **0.830** | 0.830 | 0.830 | yes |
| 03 | Newsreader + Noto Serif Bengali + Source Code Pro | 0.766 | 0.754 | **0.708** | 0.710 | 0.782 | no — `opsz` |
| 04 | Literata + Tiro Bangla + IBM Plex Mono | 0.822 | 0.818 | **0.818** | 0.820 | 0.825 | nearly |
| 05 | Source Sans 3 + Hind Siliguri + Source Code Pro | 0.757 | 0.757 | **0.757** | 0.757 | 0.757 | yes |
| 06 | Public Sans + Noto Sans Bengali + Noto Sans Mono | 0.831 | 0.831 | **0.831** | 0.831 | 0.831 | yes |
| 07 | Archivo + Anek Bangla + Martian Mono | 0.840 | 0.840 | **0.840** | 0.840 | 0.840 | yes |
| 08 | Literata + Noto Serif Bengali + IBM Plex Mono | 0.819 | 0.815 | **0.816** | 0.817 | 0.822 | nearly |

**A multiplier closer to 1.000 is better.** It means the two scripts already agree
about size, so less correction is needed, and — critically for this brand — a line
that mixes both scripts inline (a Bangla sentence containing an English product
name, which will happen constantly) needs no per-run adjustment at all to look
right. On that measure **pairing 01 wins outright** and pairing 03 is worst.

### Does it survive 11px?

The brief asks whether each pair works at 11px as well as at 60px. The 11px case
is decided by whether the মাত্রা survives, because a stroke thinner than one device
pixel greys out or disappears on an ordinary screen. Combining the multiplier with
each face's measured মাত্রা thickness **[rendered]**:

| # | Bangla size when Latin is 11px | মাত্রা in device pixels | Verdict |
|---|---|---|---|
| 01 | 9.66px | **0.72px** | Best available; still sub-pixel |
| 02 | 9.13px | 0.68px | Acceptable |
| 06 | 9.14px | 0.69px | Acceptable |
| 07 | 9.24px | 0.62px | Marginal |
| 04 | 9.04px | 0.60px | Marginal |
| 05 | 8.33px | 0.59px | Marginal |
| 08 | 9.01px | 0.49px | Poor — needs a heavier weight below 14px |
| 03 | 8.43px | **0.46px** | **Fails** |

**No pairing keeps the মাত্রা above one whole device pixel at 11px on a standard
1× screen.** That is a property of Bangla type at caption sizes, not a fault in any
of these faces, and on a 2× screen every one of them is fine. The practical
conclusion is a rule rather than a font choice: **set a floor of 12px for Bangla
and do not apply the full multiplier below 14px.** Pairing 03 fails this test
badly enough to matter.

At 60px every pairing is comfortable; large sizes are not where these choices are
decided.

### Can the families move together?

A design system is far easier to run when the faces share axes, so a single token
change moves all three at once **[file]**:

| # | Shared `wght` | Shared `wdth` | Notes |
|---|---|---|---|
| 07 | **all three** | **all three** | The only pairing where every family has both axes |
| 02 | Latin + Bangla | Latin + Bangla | Mono is static |
| 06 | all three | Bangla + mono | Latin has no width axis |
| 01 | all three | Bangla only | |
| 03 | all three | Bangla only | |
| 08 | Latin + Bangla | Bangla only | Mono is static |
| 05 | Latin + mono | none | **Bangla is static** — five separate files |
| 04 | Latin only | none | **Bangla and mono both static** |

---

## 01 · Core Modern — Inter + Noto Sans Bengali + JetBrains Mono

This is the pairing the measurements keep pointing at. Inter has the largest
Latin x-height at body size of any candidate (8.68px at 16px), and it gets there
deliberately: its optical-size axis grows the x-height as the text gets smaller,
from 0.5156em at display sizes to 0.5459em at caption sizes **[rendered]**. Because
Bangla's problem is that it is *taller* than Latin, a Latin face that grows when
small is exactly what closes the gap — so this pairing needs the least size
correction of all seven, ×0.872 at body size, and its worst case across the whole
scale (×0.829 at 56px) is still better than four of the other pairings' best. On
the other side, Noto Sans Bengali has the sturdiest মাত্রা of any text face measured
(0.0750em, 1.20px at 16px), the joint-widest Bengali coverage at 96 of 128 code
points, and a default line box of 22px at 16px — tighter than every Latin candidate's
25px, so it drops into a Latin-derived grid without forcing it open **[rendered]**.
Stroke contrast is low on both sides and the apparent weights match without
adjustment. All three carry a continuous weight axis, and none of the three has a
Reserved Font Name, so all may be subsetted for the web without renaming. Against
it: Inter has no width axis, so the pair cannot compress together; and both Inter
and Noto Sans Bengali are widely-used, deliberately neutral faces, so this pairing
is correct rather than characterful **[judgement]**. JetBrains Mono brings the largest
x-height of any mono here (8.80px), which keeps code legible at 11–13px, but its
programming ligatures need switching off for anything a client reads.

## 02 · Technical — IBM Plex Sans + Noto Sans Bengali + IBM Plex Mono

The argument here is unity: IBM Plex Sans and IBM Plex Mono are one family drawn
by the same hands, and the measurements confirm it — identical cap height
(11.17px), identical x-height (8.26px), identical 0.600 em character advance
**[rendered]**. No other pairing in this shortlist has a text-and-mono match that is
exact rather than approximate, and in a studio whose work is software, prose and
code sit next to each other constantly. The multiplier is a flat ×0.830 at every
size, which makes the design token trivially simple — one number, no scale-dependent
table — and Plex Sans and Noto Sans Bengali both carry weight *and* width axes,
so the two text faces can compress together. The engineering register is genuine
rather than borrowed: Plex was drawn for a technology company and reads that way.
Against it: **both Plex faces carry the Reserved Font Name `Plex`** **[file]**, so any
subsetting for the web requires renaming the file — a small but permanent
operational tax on every build. IBM Plex Mono is static only, so it cannot follow
a weight token; and Plex Sans stops at weight 700, leaving no genuinely heavy
display cut. The pair is a step further from parity than pairing 01, so mixed-script
inline text needs slightly more correction.

## 03 · Editorial — Newsreader + Noto Serif Bengali + Source Code Pro

This is the most beautiful pairing on the page and the one the measurements
reject. Newsreader's optical-size axis spans 6–72, the widest of any candidate,
and its display cuts are genuinely elegant; Noto Serif Bengali is the only serious
open-licence Bangla serif with a full weight range, and it is drawn to the same
metric brief as its sans sibling. The problem is arithmetic. Newsreader has the
smallest x-height of any Latin candidate — 7.05px at 16px, x/cap 0.651 **[rendered]** —
so matching Bangla to it honestly means shrinking the Bangla to ×0.708, or 11.33px
of Bangla against 16px of Latin. You can see the result in
`specimens/03-editorial.png`: the Bangla column is visibly smaller, lighter and
less present than the English beside it, which is precisely the failure this brand
cannot have, since the two audiences are equal. It gets worse at caption sizes,
where Noto Serif Bengali's মাত্রা — already the thinnest measured at 0.0542em — falls
to 0.46 device pixels **[rendered]** and begins to break up. The fix is not to abandon
the editorial direction but to stop equalising strictly: hold the Bangla at ×0.85
or above and accept that the Latin will look slightly the smaller of the two, or
swap Newsreader for Literata, whose x-height is a full pixel taller at body size.
Both options are covered in `RECOMMENDATION.md`.

## 04 · Rooted / Scholarly — Literata + Tiro Bangla + IBM Plex Mono

Tiro Bangla is the best-drawn Bengali on this list and it is not close. Fiona Ross
is the pre-eminent scholar of Bengali type and the relationship between letter and
মাত্রা here is drawn rather than constructed, which shows in running text. Literata
is a good partner: an optical-size axis spanning 7–72, low stroke contrast to match
Tiro's, and an x-height (8.12px) tall enough that the multiplier stays a steady
×0.818 and barely moves across the scale **[rendered]**. Tiro Bangla also has the
tightest default line box of any Bangla candidate — 21px at 16px **[rendered]** — so
this is the most vertically compact pairing available, which suits dense editorial
layout. And then it falls over: **Tiro Bangla has exactly one weight** **[file]**. No
bold for headings, no light for captions, no emphasis inside a paragraph, and no
synthetic bold worth shipping. For a design system that has to serve a whole brand
across four directions, that is close to disqualifying regardless of how well the
face is drawn **[judgement]**. It also has a 330-unit line gap, the only non-zero one
in the entire set **[file]**, so its vertical rhythm behaves unlike everything else
and needs its own token. Use this pairing for a single considered artefact — an
essay, a printed piece, a colophon — not as the system default.

## 05 · Rooted / Familiar — Source Sans 3 + Hind Siliguri + Source Code Pro

The case for this pairing is not typographic, it is social. Hind Siliguri is the
Bangla face that Bangladeshi readers actually encounter every day on screen, and
familiarity is a real asset when half your audience is local: text that looks
ordinary is text that gets read rather than noticed. It is also the most
practically-engineered choice for poor conditions — it is the only Bangla candidate
carrying explicit `ttfautohint` hinting parameters in its version string **[file]**,
which helps on the low-resolution Windows machines still common in Bangladesh, and
it has the largest baseline-to-মাত্রা height of any text candidate at 10.27px with a
sturdy 0.0708em headline **[rendered]**. Source Sans 3 is chosen precisely because it
recedes, letting the Bangla lead. The costs are real, though. **Hind Siliguri is
static — five separate files with no variable axis at all** **[file]** — so it cannot
move with a weight token and cannot compress at all, which breaks the "move
together" property every other serious pairing has. Its small x-height combined
with Source Sans 3's gives a multiplier of ×0.757, the second-worst here, meaning
noticeably more correction for mixed-script lines. And Source Sans 3 and Source
Code Pro both carry the Reserved Font Name `Source` **[file]**.

## 06 · Civic / Systemic — Public Sans + Noto Sans Bengali + Noto Sans Mono

The quiet argument for this pairing is coherence by construction rather than by
luck: Noto Sans Bengali and Noto Sans Mono were drawn to a shared brief by the
same design programme, and it shows in the numbers — both carry `wght` 100–900 and
`wdth` 62.5–100, and Noto Sans Mono's 3,920 glyphs are the widest coverage of
anything in this shortlist **[file]**. Public Sans is the deliberately plain civic
partner, drawn for the US Web Design System, with tall caps (11.57px) and unusually
shallow descenders (2.58px) **[rendered]** that give a compact, official texture. The
multiplier is a flat ×0.831 with no scale-dependence, all three families share a
weight axis, and none of the three carries a Reserved Font Name — so this is the
most administratively frictionless pairing of the seven. It reads as
institutional, trustworthy and unexciting, which is exactly right for a government
tender or a university contract and exactly wrong for anything that needs to feel
like a person made it **[judgement]**. Watch the variable default: Public Sans defaults
to weight **100**, so loading it without specifying a weight gives hairline text **[file]**.

## 07 · Contemporary — Archivo + Anek Bangla + Martian Mono

This is the only pairing in which **all three families carry both a weight and a
width axis** **[file]**, which makes it uniquely controllable: one token can compress
or expand the whole system across both scripts and the code face at once, and
Archivo's `wdth` range of 62–125 is the broadest of any Latin candidate. Archivo
also has the largest x-height-to-cap ratio measured (0.767) and Anek Bangla is a
contemporary Bangla from Ek Type with genuine Indic expertise behind it, so the two
share a large, even, modern texture; the multiplier is a flat ×0.840, third-best of
the seven **[rendered]**. It is the most distinctive-looking pairing here and the one
most likely to be mistaken for a considered brand rather than a default
**[judgement]**. The costs: Anek Bangla's default line box is 30px at 16px, by far the
loosest of any candidate (1.866em) **[rendered]**, so it will fight a tight vertical
grid unless explicitly overridden; its Bengali coverage is the narrowest of the
serious body faces at 90 of 128 **[file]**; and Martian Mono is enormous — cap 12.80px
and x 9.60px, the largest of anything in this shortlist, at 0.700 em per character
**[rendered]** — so it is 17% wider per character than the other monos, fitting about
14% fewer characters on a line, and must be set several points down or it will
overpower the text faces beside it. Both
Archivo and Anek Bangla have non-standard variable defaults (600 and 500) **[file]**.

## 08 · Editorial, revised — Literata + Noto Serif Bengali + IBM Plex Mono

This pairing exists because the measurements rejected pairing 03, and an
editorial direction is still needed. The diagnosis there was specific: Newsreader's
x-height is simply too small (0.4403 em at body size) to carry Bangla beside it
without shrinking the Bangla to an unreadable 11.33px. Literata is the fix —
same editorial register, same wide optical-size axis (7–72), but an x-height of
0.5073 em at 16px **[rendered]**, a full pixel taller. That single substitution lifts
the multiplier from ×0.708 to **×0.816**, and because Literata's optical axis
changes its x-height only slightly across the scale, the multiplier stays almost
flat from 0.815 to 0.825 — one number does the job at every step **[rendered]**. Noto
Serif Bengali is kept rather than Tiro Bangla because it carries a full weight axis
(100–900) where Tiro has exactly one weight **[file]**, and the two Noto Bengali
faces share metrics, so the system can swap between serif and sans without
re-tuning any size token. You can see the difference in the specimens: set
`03-editorial.png` beside `08-editorial-revised.png` and the Bangla column moves
from visibly subordinate to an equal partner. The remaining weakness is inherited
and real — Noto Serif Bengali has the thinnest মাত্রা measured (0.0542 em), so at an
11px caption the headline falls to 0.49 device pixels **[rendered]**. The fix is a
weight bump rather than a different font: set Bangla captions at weight 500 rather
than 400, which thickens the মাত্রা without changing the size relationship.

---

## What these pairings were judged on, and what was not tested

**Judged, by measurement:** apparent size match between scripts at five sizes;
মাত্রা thickness in device pixels at caption size; default line box; line-height
collision floor; shared axes; character advance; licence and Reserved Font Name;
Bengali code-point coverage; conjunct shaping under HarfBuzz.

**Judged, by opinion, and marked as such:** register and character — whether a
pairing reads as editorial, technical, civic or rooted.

**Not tested at all:**

- **Rendering outside Chromium on macOS.** Every rendered number here comes from
  headless Chromium. Windows uses DirectWrite and Android uses its own stack;
  hinting and stem darkening differ, and the 11px conclusions in particular could
  move. Hind Siliguri is the only Bangla candidate with explicit hinting, which
  may matter more on Windows than these measurements can show.
- **Print.** Screen only. The device-pixel argument about মাত্রা thickness does not
  apply on paper.
- **A Bangla reader's judgement.** The conjunct and মাত্রা tests are mechanical.
  Whether Anek Bangla or Noto Sans Bengali reads as *good* Bangla typography to a
  Bangladeshi reader is not something measurement can settle, and it should be
  checked with a native reader before anything is locked.
- **Fallback behaviour** when webfonts fail to load, and behaviour in email
  clients, which cannot use webfonts at all.
