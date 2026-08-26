<!-- Hand-written chapter. build.py reads this file; it never writes it. -->

{{figure:icons}}

## The decision

**Each platform's own icon geometry is followed.** Apple and Android are given
square, unmasked artwork and apply their own masks. The web keeps the rounded
tile, because a browser will not round a favicon for you. That is the owner's
decision, taken on 26 August 2026.

It reverses the opposite decision, taken on 14 August 2026, which was to use one
rounded icon on every surface, Apple included. Both are recorded, because a
reversed decision that vanishes teaches nobody anything.

{{data:icon-files}}

## Why it was reversed

This kit now ships to two developer accounts, and both platforms ask for the same
thing in different words.

Apple asks for square, unmasked artwork. The system applies the mask itself, and
it derives the Liquid Glass specular highlights — the moving glints along the
edge of an icon — from the edges of the layers you supply. A pre-rounded edge
sits inside the mask the system draws, so the highlight follows the wrong
geometry. Apple's own wording is that pre-masked artwork "negatively impacts
specular highlight effects" and makes edges "look jagged".

Google asks for the same, and is more specific about it. The Play Store icon is a
full square. Play applies a corner radius **equivalent to 30% of the icon size**
and adds the drop shadow itself, and the specification says not to bake either
one in.

That contrast is worth noticing. **Google publishes a number here and Apple does
not.** It is the same rule on both platforms, and only one of them can be quoted.

## What the old decision accepted, and what has changed about it

The 14 August decision was recorded with three claims, each labelled as a
measurement, a judgement, or neither. That structure still holds, and two of the
three have moved.

**Measured, and still true: on watchOS and visionOS the rounding cost nothing.**
Both mask to a **circle**, and the corner material a radius removes lies outside
a circle inscribed in the same square. `04_mark/build.py` renders the rounded web
icon and the square Apple master under that circle and differences the two images
pixel by pixel.

{{data:icon-mask-measurement}}

**Judged, not measured: the static difference under the rounded-rectangle mask
looked slight.** That was a reading of a static render. It could not be a
measurement, because Apple publishes no corner radius, so there is no mask to
composite against without substituting this kit's own radius for Apple's and then
measuring the substitution.

**Neither, and this is the one that decided it: the dynamic cost.** Liquid Glass
highlights are generated at run time by Apple's renderer, from the layer edges,
as the device moves. There is no way to reproduce that outside that renderer, so
the difference in the moving highlight was never measured and was never known.

The old decision accepted that unknown in exchange for one icon instead of
several. The new one removes it instead, by giving each platform the geometry it
asks for. Nothing was measured that had not been measured before. What changed is
that an unknown no longer has to be carried.

## What differs between the platforms, and what does not

The corner shape now differs. The size of the mark does not, and that is measured
rather than hoped for.

The two canvases invite a mistake here. Apple's mark sits inside 100 units,
all of which are shown. Android's sits inside 108 units, of which only the middle
72 are ever displayed. Comparing the two scales directly would say they are very
different and would mean nothing. What matters is the fraction of the **visible**
area the mark fills.

{{data:icon-visual-parity}}

The build fails if that difference ever exceeds two percentage points.

## The Android layers

Android's adaptive icon is three layers on a 108 dp canvas: a background, a
foreground, and a monochrome silhouette the system tints to match the wallpaper.
The outer 18 dp on each side is reserved for masking and for motion effects, and
the middle **66 dp** is the zone no launcher mask may clip. Both figures are
Google's.

The monochrome layer matters more than its size suggests. From Android 13 a
person can ask for themed icons, and from Android 16 QPR 2 the system generates a
monochrome layer for any app that does not supply one. Supplying the shape by
hand is better than having it inferred.

One shortfall is recorded rather than designed away. Google asks for a logo of at
least 48 dp. At the scale that keeps every inked pixel inside the safe circle,
this mark measures **43.89 × 49.29 dp** — so it meets 48 dp on its long axis and
not on its short one. Fitting the 66 dp square instead would meet both, and would
put ink outside the circle a round launcher mask leaves. The circle wins, because
a clipped mark is a worse fault than a narrow one.

## The corner radius is this kit's own number

The web tile rounds by 24% of its width. The build reads that numeral from this
system's own `radius-hero` token, so it is not typed anywhere.

Be precise about what that means. `radius-hero` is **24 px**; the tile rounds by
24 units per 100 on its grid, which is 245.8 px at 1024 px. The number is reused
on purpose, so the tile's corner belongs to the same family as every other
rounded corner in the kit — an echo, not a unit conversion.

**Apple publishes no corner radius, no percentage, and does not use the word
"squircle" anywhere in current guidance.** The widely circulated community figure
of 22.37% with roughly 60% corner smoothing describes a superellipse — a rounded
shape whose curvature varies continuously — which a single radius value cannot
describe at all. Any radius quoted in this kit is this kit's, and is not claimed
to be Apple's.

## The safe field

On the 100-unit grid the mark sits inside a 90-unit field, centred. That is this
kit's own rule. **Apple publishes no numeric safe zone** for iOS, iPadOS or
macOS; the guidance is qualitative. Stating a percentage and attributing it to
Apple would be a fabrication.

On the 108-unit Android grid the field is Google's 66 dp, not this kit's 90. The
same placement rule serves both: fit the mark's diagonal inside the inscribed
circle, because a circle is the tightest mask any platform applies.
