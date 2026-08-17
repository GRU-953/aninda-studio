<!-- Hand-written chapter. build.py reads this file; it never writes it. -->

The mark is a circle tangent to a stem. The stem overruns the circle
**downward**.

{{figure:marks}}

That is the whole idea. A river meeting the sea is a circle of still water with
a channel running out of it, and Barishal sits in a delta. The mark is not a
letter and is not asked to be one.

## The mistake that shaped it, recorded so it is not repeated

An earlier draft ran the stem **upward** past the top of the circle. Drawn that
way, a circle with a vertical stroke rising on its right side is a lowercase
**d**. Not something like a *d* — it is a *d*. The studio's Latin name begins
with an *a*, so the mark was quietly spelling the wrong letter.

Nothing in the specification caught this. The numbers were fine, the tangency
was exact, the proportions were the ones I had chosen. It was found by rendering
the thing and looking at it. That is the argument for building the artefact
early rather than describing it well, and it is why every stage of this project
ends in a rendered file rather than a document.

Turning the overrun downward fixed it. The circle and the stem are otherwise
unchanged.

## Construction

The mark is drawn on a 100-unit grid. These figures are read from
`04_mark/manifest.json` at build time.

{{data:mark-geometry}}

The stem sits at the exact x of the circle's right edge, so the two are tangent
rather than overlapping. The stem starts level with the top of the circle and
runs past the bottom of it.

## Two weights, one geometry

{{data:mark-strokes}}

There is one geometry and two stroke widths. Nothing else changes: the circle
does not move, the stem does not move, and the two weights are the same drawing
with a heavier pen. A thin stroke disappears at small sizes, so below 24 px the
heavy weight takes over. Choose by the size the mark will be seen at, not by
taste.

Both files are drawn in `currentColor`, so the mark takes the colour of whatever
text it sits in, in any of the four themes and in forced colours.

## Clear space

**Clear space is half the mark's own height, on all four sides.**

It is written as a proportion rather than a fixed measure so that it holds at
every size without a table. At the regular weight the drawn mark is 73 units
tall on the 100-unit grid, so the clear space is 36.5 units. At the heavy weight
the mark is 79 units tall and the clear space is 39.5.

Nothing enters that space. Not a caption, not a rule, not the edge of a
photograph, not another logo.

## Minimum size

The stroke rule is the minimum-size rule. Below 24 px use the heavy weight.
Below 16 px, use the icon rather than the bare mark: the icon has a solid ground
behind it and survives where a hairline on a busy background does not.

## What not to do

- Do not run the stem upward. That is the *d*, and it is the one mistake this
  mark has already made.
- Do not add a second colour. The mark is one colour and takes it from its
  context.
- Do not outline it, add a shadow, or set it on a gradient.
- Do not stretch it. Scale both axes together.
- Do not rotate it.
- Do not redraw it at a stroke width between 9 and 15. There are two weights,
  and a third one drawn by hand will not match either.
- Do not put the mark and the wordmark at arbitrary distances from each other.
  Use the lockups, or leave clear space and set them on a shared baseline.

## The files

{{data:mark-files}}
