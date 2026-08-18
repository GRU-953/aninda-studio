<!-- Hand-written chapter. build.py reads this file; it never writes it. -->

{{figure:icons}}

## The decision

**One rounded icon is used everywhere, Apple included.** That is the owner's
decision, taken on 14 August 2026, and it is recorded here with what it costs.

The everyday icon is a rounded square with the mark inside it, in white on the
ground colour. The same artwork ships at every size. A single square, unmasked
file exists as well, and it is for one purpose only.

{{data:icon-files}}

## What the decision trades away, in Apple's own terms

Apple's current guidance asks for **square, unmasked artwork**. The system
applies the mask itself, and it derives the Liquid Glass specular highlights —
the moving glints along the edge of an icon — from the edges of the layers you
supply. A pre-rounded edge therefore sits inside the mask the system draws, and
the highlight follows the wrong geometry.

Apple's own wording is that pre-masked artwork "negatively impacts specular
highlight effects" and makes edges "look jagged". Xcode's documentation says not
to export the canvas mask, and the *Adopting Liquid Glass* guidance says to let
the system apply the masking. All of that was checked against the Human
Interface Guidelines on 14 August 2026.

## What was measured, what was judged, and what could not be either

This is the part that decides whether the trade is acceptable, so it is stated
in full — and each of the three claims is labelled with which of the three it is.
An earlier version of this chapter presented the first two both as measurements.
Only one of them is.

**Measured: on watchOS and visionOS the rounding costs nothing.** Both mask to a
**circle**, and the corner material a radius removes lies outside a circle
inscribed in the same square. `04_mark/build.py` renders the rounded icon and the
square master under that circle and differences the two images pixel by pixel.

{{data:icon-mask-measurement}}

**Judged, not measured: the static difference under the rounded-rectangle mask
looks slight.** This is my reading of a static render, and it is a judgement. It
cannot be a measurement, because Apple publishes no corner radius, so there is no
mask to composite against without substituting this kit's own radius for Apple's
and then measuring the substitution.

**Neither: the dynamic cost.** Liquid Glass highlights are generated at run time
by Apple's renderer, from the layer edges, as the device moves. There is no way to
reproduce that outside Apple's own renderer, so the difference in the moving
highlight was **not measured and is not known**. It might be invisible. It might
be a visible seam on a device in the hand. Saying which would be a guess.

That is the honest shape of this decision: one measured nil cost on two platforms,
one judged small cost on the rest, and one unknown accepted deliberately in
exchange for one icon instead of five.

## If you ever submit to the App Store

Use `icon-appstore-square-1024.svg`, not the rounded icon. Icon Composer expects
unmasked layers, and the rounded file is the wrong input for it. The square file
is square, fully opaque and carries no baked mask.

## The corner radius is this kit's own number

The rounding is 24% of the icon width. The build reads that numeral from this
system's own `radius-hero` token, so it is not typed anywhere.

Be precise about what that means. `radius-hero` is **24 px**; the icon rounds by
24 units per 100 on its grid, which is 245.8 px on the 1024 px icon. The number
is reused on purpose, so the icon's corner belongs to the same family as every
other rounded corner in the kit — an echo, not a unit conversion. This page used
to say the radius "comes from" the token "and from nowhere else", which claimed a
derivation the build could not perform.

**Apple publishes no corner radius, no percentage, and does not use the word
"squircle" anywhere in current guidance.** The widely circulated community
figure of 22.37% with roughly 60% corner smoothing describes a superellipse — a
rounded shape whose curvature varies continuously — which a single radius value
cannot describe at all. Any radius quoted in this kit is this kit's, and is not
claimed to be Apple's.

## The safe field

The mark sits inside a 90-unit field on the 100-unit grid, centred. That is this
kit's own rule too. **Apple publishes no numeric safe zone** for iOS, iPadOS or
macOS; the guidance is qualitative. Stating a percentage and attributing it to
Apple would be a fabrication.
