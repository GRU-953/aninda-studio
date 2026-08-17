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

## What was measured, and what could not be

This is the part that decides whether the trade is acceptable, so it is stated
in full.

**Measured here: the static penalty is small.** In a static render the
difference between the rounded artwork inside the system mask and a square
master is slight. The rounding radius is 24% of the icon's width, and the
system's own rounded-rectangle mask cuts close to it.

**Measured here: the penalty is nil on watchOS and visionOS.** Both mask to a
**circle**, and a circle inscribed in a square cuts well inside the corner
rounding. The rounded corners are removed by the mask before they can be seen.
The build records the mark's worst corner at 45.00 of 45 units from the centre —
inside both the 90-unit safe field and the circle those two platforms mask to.

**Not measured: the dynamic cost.** Liquid Glass highlights are generated at
run time by Apple's renderer, from the layer edges, as the device moves. There
is no way to reproduce that outside Apple's own renderer, so the difference in
the moving highlight was **not measured and is not known**. It might be
invisible. It might be a visible seam on a device in the hand. Saying which
would be a guess.

That is the honest shape of this decision: a small known static cost, a nil cost
on two platforms, and one unmeasured unknown accepted deliberately in exchange
for one icon instead of five.

## If you ever submit to the App Store

Use `icon-appstore-square-1024.svg`, not the rounded icon. Icon Composer expects
unmasked layers, and the rounded file is the wrong input for it. The square file
is square, fully opaque and carries no baked mask.

## The corner radius is this kit's own number

The rounding is 24% of the icon width. That comes from this system's own
`radius-hero` token and from nowhere else.

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
