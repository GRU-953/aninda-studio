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
corrected Bangla size looks equal to the Latin beside it, whether 220 ms feels
right, whether the mark reads as a river — is one person's judgement.

## The Bangla has not been reviewed by a second Bangla reader

This is the single most important gap in the book.

The Bangla was checked rule by rule against the Bangla Academy's 2012 spelling
rules and its own dictionary, with page numbers recorded for every ruling. That
is a careful reading of primary sources by one person. It is not a review by a
second Bangla reader, and it cannot substitute for one.

The type work has the same shape. HarfBuzz shaping produced no dotted circles,
no missing glyphs and no stray hasantas across sixteen conjuncts in all ten
Bangla faces, and pixel analysis confirmed the মাত্রা is continuous. **That proves
nothing is broken. It does not prove the Bangla is good.** Whether Noto Serif
Bengali's conjuncts read as well-drawn Bangla to someone in Barishal is a
judgement no measurement can make.

Where no verified string existed, the English was left in place and the gap was
named rather than filled. Those gaps are listed with the chapter they fall in,
below.

## Chromium only

Every rendered measurement in this system — the type metrics, the মাত্রা
continuity, the line-height collision floors, the contrast readings, the focus
ring — comes from **headless Chromium on macOS**, at a device scale factor of 1
for measurement and 2 for the specimen images.

Windows uses DirectWrite. Android has its own stack. Hinting and stem darkening
differ between them. The findings most likely to move are the sub-pixel মাত্রা
results at 11 px and 12 px. Safari and Firefox were not tested at all.

Nothing was tested in print, either. The device-pixel argument that sets the
12 px Bangla floor does not apply on paper, so print can go smaller than this
system says.

## The icon decision's untested dynamic cost

One rounded icon is used on every surface, Apple included. The static penalty
was measured and is small. On watchOS and visionOS it is nil, because the
circular mask cuts inside the rounding.

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

## The Bangla gaps in this book, by chapter

{{data:bangla-gaps}}

## What would close these

In the order I would do them, given the chance:

1. A Bangla reader who is not me, going through every string and every specimen.
2. A person who uses a screen reader daily, going through the components.
3. Rendering checks on Windows and on Android, at 1× and 2×.
4. Five people who are not me, building something small with the kit.

Until those happen, the honest description of this system is: carefully
measured, thoroughly documented, and tested by one person on one machine.
