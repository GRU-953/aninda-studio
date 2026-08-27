<!-- Hand-written chapter. build.py reads this file; it never writes it. -->

This chapter is not a disclaimer. Every item below is a real gap that changes
how much weight you should put on something earlier in the book.

## No screen-reader testing by a person who depends on one

Contrast is computed. Target sizes are measured. Focus rings are read off
differenced pixel buffers. Roles and labels are in the markup and were reviewed.

**None of that is the same claim as "this works with a screen reader".** Nobody
who uses a screen reader every day has tried this system. Lived accessibility is
a different claim, and this book does not make it. If you depend on one and
something here fails you, write to me and I will fix it.

## No user research

Not a small study. None.

Google's Material 3 Expressive is described on Google's own site as backed by
46 studies and more than 18,000 participants. That figure is reported here as
**Google's stated research**: there is no published methodology, no
preregistration, no peer review, and the page carrying the claim has no publish
date.

This kit has no equivalent, and no amount of rigour elsewhere substitutes for
it. Every judgement in this book about how something *feels* — whether the
type looks right at 220 ms, whether the mark reads as a river — is one
person's judgement.

## The Bangla record was never read by a second Bangla reader

The Bangla stopped shipping on 27 August 2026 and the record of it was kept.
This is a limitation of that record, and it transfers to anyone who picks it up.

The Bangla was checked rule by rule against the Bangla Academy's 2012 spelling
rules and its own dictionary, with page numbers recorded for every ruling. That
is a careful reading of primary sources by one person. It was never a review by
a second Bangla reader, and it cannot substitute for one.

The type work has the same shape. HarfBuzz shaping produced no dotted circles,
no missing glyphs and no stray hasantas across sixteen conjuncts in all ten
Bangla faces, and pixel analysis confirmed the matra was continuous. **That
proved nothing was broken. It never proved the Bangla was good.** Whether Noto
Serif Bengali's conjuncts read as well-drawn Bangla to someone in Barishal is a
judgement no measurement can make.

So the record is sound about the rules it cites and silent about whether the
result reads well. Anyone rebuilding a Bangla layer from it inherits both halves.

## Chromium only

Every rendered measurement in this system — the type metrics, the matra
continuity, the line-height collision floors, the contrast readings, the focus
ring — comes from **headless Chromium**, at a device scale factor of 1 for
measurement and 2 for the specimen images. It runs on macOS here and on Ubuntu in
CI, from a clean checkout, so the readings are not particular to one machine.

Windows uses DirectWrite. Android has its own stack. Hinting and stem darkening
differ between them. Safari and Firefox were not tested at all.

Nothing was tested in print, either. Every size floor in this system is argued
from device pixels, and that argument does not apply on paper, so print can go
smaller than this system says.

## The icon decision's untested dynamic cost

One rounded icon is used on every surface, Apple included. One part of the
static cost is measured: under the circle watchOS and visionOS mask to, the
rounded icon and the square master are the same image in every pixel, so there
the penalty is nil. The other part is a judgement, not a measurement — under
Apple's rounded-rectangle mask the difference looks slight to me in a static
render, and it cannot be measured, because Apple publishes no corner radius and
so there is no mask to composite against without substituting this kit's own
radius for Apple's and measuring the substitution. Chapter 04 separates the two
at length, and `04_mark/manifest.json` records the same split.

**The dynamic cost was not measured and is not known.** Liquid Glass specular
highlights are generated at run time by Apple's own renderer from the layer
edges, and there is no way to reproduce that outside it. The rounded artwork may
produce a highlight that follows the wrong geometry on a moving device. It might
be invisible. Saying which would be a guess, and this book will not guess.

## Smaller things, named rather than buried

- **Conjunct coverage is a sample.** Sixteen conjuncts and five words were
  tested, not the full combinatorial set of Bengali conjuncts.
- **No fallback or email testing.** How these type stacks degrade when the
  webfonts fail to load was not tested, and email clients cannot use webfonts at
  all.
- **Licence reading is not legal advice.** Every `OFL.txt` was read in full and
  the Reserved Font Name declarations were extracted mechanically. I am
  confident in the reading. It is still a reading.
- **Guidance moves.** Apple's icon guidance changed materially twice in two
  years. Two benchmark systems were archived in the ten weeks before this kit's
  research pass, and a Figma deprecation landed three days after it.
- **The PDF has no bookmark tree.** The print pipeline is Playwright only, with
  no post-processing tool, and there is no way to add PDF bookmarks afterwards.
  A generated table of contents with internal links stands in for it.
- **This system has one user.** It has never been handed to a second designer to
  build with. Everything about how learnable it is is untested.

## The half of this system that was removed

This book was bilingual. Every chapter carried an English section and a Bangla
one, a language toggle switched between them, and no Bangla was ever written for
it — only strings checked against the Bangla Academy's own dictionary, page by
page, with the ruling recorded beside each one. Where no approved string existed,
the book said so rather than inventing one.

It was removed on 27 August 2026, by the owner's decision, and this system now
ships English.

What was measured before it went is worth keeping, because it is the strongest
piece of measurement in the book and none of it was guesswork:

{{data:bangla-removed}}

The record itself is `06_type/BANGLA-STANDARD.md`, with the string register in
`06_type/BANGLA-STRINGS.md` and the face measurements in
`06_type/MEASUREMENTS.md`. All three are kept, and all three are still held to
the English standard.

## What would close these

In the order I would do them, given the chance:

1. A person who uses a screen reader daily, going through the components.
2. Rendering checks on Windows and on Android, at 1× and 2×.
3. Five people who are not me, building something small with the kit.
4. A Bangla reader who is not me, going through the retained record — needed
   only by whoever rebuilds a Bangla layer from it, which is why it is last
   here and was first while the Bangla shipped.

Until those happen, the honest description of this system is: carefully
measured, thoroughly documented, and checked by one person — on two operating
systems, but in one browser engine, and by nobody who depends on a screen reader.

## Where every outside claim comes from

This book leans on outside authorities in a few dozen places — Apple's minimum text
sizes, Android's touch target, WCAG's contrast floors, the Bangla Academy's spelling
rules, the DTCG format. Until 19 August 2026 it carried exactly two URLs, both of
them licence texts, and none of those claims cited anything.

That was the worst omission in the book, because it is the one that asks a reader to
take a number on trust while the rest of the system is built on refusing to do that.
The table below is the whole apparatus, generated from the same record the benchmark
uses, and the benchmark itself now travels inside this file.

{{data:sources}}
