# Benchmark — Aninda Studio against published industry guidance

**Status:** source document for a guidebook chapter. Not the chapter itself.
**All facts below checked:** 14 August 2026.
**Language:** UK English.

---

## 1. What this document is, and what it is not

This is a comparison between the Aninda Studio brand system and the **published**
design and brand guidance of the companies whose work is most often held up as the standard —
principally Apple and Google, then a wider field of public design systems.

Three things it is, stated plainly.

1. **It compares against published guidance, not against practice.** What Apple writes on its
   Human Interface Guidelines pages is a document. Whether Apple's own applications follow that
   document is a separate question, and this benchmark does not attempt to answer it. The same
   applies to Google, IBM, GOV.UK and everyone else here.
2. **Every claim carries a date.** Guidance moves quickly, and in ways that invalidate work
   built on it. Apple's app-icon guidance changed materially in June 2025 and again in June 2026.
   Google's current design direction is still partly in pre-release code as of August 2026. A
   benchmark without dates is a benchmark that quietly rots. Every row below therefore names the
   page or file it came from and the date on it.
3. **It was a measuring stick before it was a scorecard.** Section 7 lists the criteria this
   kit is held to. It recorded no verdicts while the kit did not exist; the verdicts were run
   against the finished system on 19 August 2026 and are in the table there, each with the
   evidence that decided it.

Three things it is not.

1. **It is not a claim of parity.** Apple and Google run design systems with research budgets,
   dedicated teams and platform control. This is a small studio's identity system. The point of
   the comparison is to inherit good practice and to be honest about the gap, not to close it.
2. **It is not exhaustive.** Several well-known systems were checked and found unusable as
   benchmarks, for reasons recorded in section 5.
3. **It is not a substitute for testing.** Contrast can be measured by a script. Whether a
   screen reader — software that reads an interface aloud for blind and partially sighted users —
   makes sense of the result is a different claim, and section 8 says exactly which claims this
   document declines to make.

A note on vocabulary, because two words are used loosely everywhere and precisely here.

- A **design system** is the working kit a product is built from: colour roles, type scale,
  spacing, components, and the code or files that carry them.
- A **brand book** is the rulebook for the identity itself: the mark, the name, who may use it,
  how it is written, and what is forbidden.
- A **design token** is a single named design decision stored as data — for example, a colour
  recorded as `colour.surface.default` rather than as a hex value pasted into a file — so that one
  edit can propagate everywhere.
- **Machine-readable** means a computer can read and validate the file without a human
  interpreting it; a JSON token file is machine-readable, a PDF of swatches is not.

---

## 2. The most important structural finding

**Apple and Google both publish a design system openly, and both keep their brand book private.**

This is the single most useful thing in the entire benchmark, and it is almost always missed.

What is public from Apple:

- The Human Interface Guidelines — comprehensive, free, no login.
- Apple Design Resources — template files for Figma, Sketch and Photoshop.
- The App Store Marketing Guidelines, which govern how *other people* may display Apple's badges
  and product images.
- The Apple Trademark List and the Guidelines for Using Apple Trademarks — again, rules for
  other people.
- The Apple Style Guide, a public writing and terminology manual.

What is **not** public from Apple: **there is no Apple brand kit.** No logo files, no brand
palette, no identity manual for Apple's own mark. The nearest public equivalent to a
verbal-identity guide is the Apple Style Guide, and the nearest thing to a visual identity manual
is a legacy PDF for channel affiliates whose content dates to around 2013.

Google is the same shape, more bluntly. Material 3 is fully public. The brand guidance is not:
`google.com/permissions` now redirects to `about.google/brand-resource-center`, which redirects
onward to a partner marketing hub requiring a login, and `brand.google` redirects to a Google
sign-in page. Google Sans, the corporate typeface, is not on Google Fonts.

Meta is the clearest case of all: a public Brand Resource Center that is entirely permission-based
— every use requires approval, and only files downloaded from the centre may be used — with no
public design system and no public tokens.

### Why conflating the two is the commonest error in benchmarked brand work

A small studio reads the Human Interface Guidelines, sees a rigorous public document, and
concludes that this is what a brand system looks like. It is not. It is what a *platform design
system* looks like. The brand rules — how the mark is drawn, when it may be recoloured, who may
use it — are the part nobody published, and so they are the part that gets improvised.

The result is a predictable failure: a "brand book" that is really a component library with a logo
page bolted on the front, strong on button radii and silent on the questions a brand book exists
to answer.

Apple itself made this distinction explicitly in June 2026. WWDC26 session 251, *Communicate your
brand identity on iOS* (8 June 2026), argues that brand belongs in the **content layer** — the part
of the screen that is yours — while the functional layer of controls and navigation should look
like the platform. That is a brand-versus-system boundary drawn by the platform vendor.

### What Aninda Studio will do about it

*(This is a decision recorded here, not a sourced external fact.)*

**Ship the two artefacts separately, with separate licences and separate front doors.**

1. **The brand book** — the mark, its construction and clear space, the name and how it is
   written, the voice, the permission rules — as a standalone document, under a licence that keeps
   the identity controlled. Identity assets are proposed under **PolyForm Noncommercial 1.0.0**,
   which is source-available rather than open source (see section 6).
2. **The design system** — tokens, type scale, colour roles, components — as a separate,
   openly licensed, machine-readable artefact under **Apache-2.0**, so it can be used, forked and
   built on without touching the identity.
3. **No cross-contamination.** The design system must be usable by someone who is not permitted
   to use the mark. If removing the logo breaks the token set, the boundary was drawn wrongly.
4. **State the boundary in the guidebook,** in the same terms used above, so a reader who has
   only ever seen the Human Interface Guidelines understands why this kit has two halves.

This mirrors what Apple and Google actually do, rather than what a casual reading of their public
pages suggests they do.

---

## 3. Apple — Human Interface Guidelines

Checked 14 August 2026. Current operating system generation: iOS 27, iPadOS 27, macOS 27.
"Liquid Glass" is Apple's name for the material system introduced at WWDC25 on 9 June 2025 (the
iOS 26 generation) and refined at WWDC26 on 8 June 2026.

Throughout: **pt** is a point, Apple's device-independent unit of size; **px** is a pixel;
**masking** means the system clipping artwork to a shape; a **layer** is one separable piece of
artwork stacked with others.

### 3.1 App icons

Source page change log: 8 June 2026 ("Refined guidance for Liquid Glass"), previously 9 June 2025
and 10 June 2024.

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| Master size and shape | 1024×1024 px square for iOS, iPadOS and macOS, which the system then masks to a rounded rectangle. tvOS is 800×480 landscape. visionOS is 1024×1024 masked to a **circle**. watchOS is **1088×1088** masked to a circle. *(App Icons page, change log 8 Jun 2026)* | Produce five masters, not one. The watchOS master is a different pixel size from the phone master, and two platforms mask to a circle rather than a rounded square — a mark that only works inside a square will fail on two of the five. |
| Colour space | sRGB, Gray Gamma 2.2 or Display P3. Display P3 is **not** supported on visionOS. *(App Icons page, 8 Jun 2026)* | Author masters in sRGB, the common colour space of the web and most screens. Any Display P3 variant — a wider range of colours available on newer displays — is an addition, and must not be the only master. |
| Masking | The system applies the mask. Apple asks for "appropriately shaped, unmasked layers"; pre-masked artwork "negatively impacts specular highlight effects" and makes edges "look jagged". Xcode's own documentation says not to export the canvas mask. The *Adopting Liquid Glass* guidance says to let the system apply masking. *(all 8 Jun 2026 or later)* | Never bake the rounded corner into the exported artwork. Export the full square, unmasked. This is the opposite of the long-standing habit of shipping a pre-rounded tile. |
| Corner radius | **Apple publishes no corner radius, no percentage, and does not use the word "squircle" anywhere in current guidance.** The icon grid is described as concentric with the hardware, and SwiftUI provides `ConcentricRectangle` precisely so that values are not hard-coded. Apple also notes that effects "can appear differently between system versions". *(App Icons page, 8 Jun 2026)* | Do not publish a corner-radius percentage and attribute it to Apple. The widely circulated community figure — 22.37% with roughly 60% corner smoothing — describes a **superellipse**, a rounded shape whose curvature varies continuously and which a single radius value cannot describe. If this kit needs a radius for its own non-Apple surfaces, it must be declared as this kit's own number. |
| Appearance variants | Three different counts appear in Apple's material, and all three are correct in their own context. The specification table lists **six** (default, dark, clear light, clear dark, tinted light, tinted dark). The surrounding prose says **four**. Icon Composer, Apple's authoring tool, has you author **three** (Default, Dark and **Mono**) and previews the clear and tinted appearances from Mono. The system generates any variant you do not supply. watchOS has no variants. *(App Icons page and Icon Composer documentation, 8 Jun 2026)* | Author three, expect six, describe the discrepancy rather than picking one number and looking wrong to a reader holding a different page. The practical deliverable is Default, Dark and Mono. A mark that does not survive being reduced to a single-colour Mono layer is not finished. |
| Layers | iOS, iPadOS, macOS and watchOS take a background plus one or more foreground layers. tvOS takes 2–5. visionOS takes a background plus 1–2. Icon Composer allows a **maximum of four groups**. SVG is preferred and text must be converted to outlines. *(8 Jun 2026)* | Design the mark as separable background and foreground from the start, in vector form, within four groups. Convert any lettering to outlines so it does not depend on a font being present. |
| What to strip before export | Blurs, shadows, specular highlights, opacity and translucency, and background colours or gradients are all applied by the system and should be removed from the source. Apple asks for "clearly defined edges". *(8 Jun 2026)* | The exported icon source is flatter and plainer than the finished icon looks on a device. Any depth effect drawn by hand competes with the system's own and loses. |
| Safe zone | **No numeric safe zone is published** for iOS, iPadOS or macOS. The guidance is qualitative — keep primary content centred. tvOS is the only platform with an explicit safe-zone instruction, and Apple notes it can vary. *(8 Jun 2026)* | Any margin figure this kit uses is this kit's own rule and must be labelled as such. Stating a percentage and attributing it to Apple would be a fabrication. |
| Grid | No numeric grid is published. Apple points to the App Icon Template on Apple Design Resources, refreshed 23 June 2026 for iOS 27, iPadOS 27 and macOS 27. *(Apple Design Resources, 23 Jun 2026)* | Construct against the template file, not against a reconstructed grid. Record the template version used. |
| Tooling | Icon Composer's own page requires macOS Tahoe 26.4 or later; Apple Design Resources says macOS Sequoia or later. **Apple's own pages conflict.** Icon Composer 2 beta was released 8 June 2026 at WWDC26. It covers iPhone, iPad, Mac and Apple Watch only. *(both checked 14 Aug 2026)* | Record which version of the tool was used and on which macOS. Do not rely on either stated minimum, since they disagree. tvOS and visionOS icons fall outside the tool and need another route. |

### 3.2 Materials

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| Two material systems | Liquid Glass is the **functional layer** — controls and navigation. Standard materials serve the **content layer**. Apple's instruction is not to use Liquid Glass in the content layer. *(Materials page, current 14 Aug 2026)* | If this kit ever specifies a translucent surface, it must say which layer it belongs to. A brand surface is content-layer, and therefore uses standard materials, not Liquid Glass. |
| Two Liquid Glass variants | Regular and clear. Regular is the general-purpose variant and is the one to use where there is a significant amount of text. *(Materials page)* | Any text-bearing surface in this kit that sits on a translucent background uses the regular equivalent, never the clear one. |
| Contrast over materials | **Apple states no contrast ratio for text over materials.** Legibility is delivered by system *vibrancy* — an automatic adjustment that pushes foreground colours away from whatever is behind them — rather than by a fixed ratio. Apple does warn against quaternary vibrancy on the thinnest materials because "the contrast is too low". *(Materials page)* | This kit cannot inherit a number here, because there is not one. It must set its own measurable rule: no text over any translucent surface unless the measured contrast against the *worst-case* backdrop still passes. That is stricter than Apple's guidance, and defensible precisely because Apple's is qualitative. |
| The one published number | With **clear** Liquid Glass over bright content, Apple suggests considering a dark dimming layer at **35% opacity**. *(Materials page)* | This is the only numeric material value in the guidance. If this kit reproduces it, it must be reproduced in context — clear variant, bright content — not generalised into a house rule. |

### 3.3 Typography

Typography page change log: 16 December 2025.

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| Minimum text sizes | iOS and iPadOS: 17 pt default, **11 pt minimum**. macOS: 13 / **10**. tvOS: 29 / **23**. visionOS: 17 / **12**. watchOS: 16 / **12**. These apply to custom fonts as well as system fonts. *(Typography page, 16 Dec 2025)* | The type scale must have a documented floor per platform, and every specimen must be checkable against it. A single "smallest size" for the whole kit is not enough, because the floor differs by a factor of more than two across platforms. |
| Weights to avoid | Avoid Ultralight, Thin and Light. *(Typography page)* | These weights should not appear in any specified role. If the chosen typeface has a variable weight axis, the usable range must be documented with a lower bound. |
| Optical sizing | Apple's system fonts now have **dynamic optical sizes** — the letterforms adjust continuously with size, merging what used to be separate Text and Display designs. The system also adjusts tracking (letter spacing) at every point size. *(Typography page, 16 Dec 2025)* | The familiar rule of swapping typeface family at around 20 pt is a **design-tool workaround, not a platform rule**, and should be described that way. If this kit's typeface has no optical-size axis, the compensating rules — tracking and width adjustments at small sizes — are this kit's own and must be written as manual instructions with the sizes at which they apply. |
| Dynamic Type | **macOS does not support Dynamic Type** — Apple's system-wide user setting for larger or smaller text. This is commonly got wrong. *(Typography page)* | Any statement in this kit about honouring Dynamic Type must exclude macOS explicitly. Claiming support on macOS would be inaccurate. |
| Number of typefaces | Apple's instruction is to minimise the number of typefaces used. The Branding page notes that a custom font for headlines with a **system font for body copy and captions** can work well. *(Branding page, current 14 Aug 2026)* | The kit should state its typeface count and justify it. Apple's own suggested pattern — brand face for headlines, system face for body — is a legitimate option and should be considered rather than assumed away. |

### 3.4 Accessibility

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| Standards position | **Apple states no WCAG version and makes no conformance claim.** It names WCAG and APCA as two popular standards of measure, says to strive to meet minimum colour-contrast standards, and attributes the actual figures to a tool: the Accessibility Inspector uses WCAG Level AA values as guidance. *(Accessibility page, current 14 Aug 2026)* | This kit cannot say "Apple requires 4.5:1". It can say Apple's inspection tool uses WCAG AA values, and that this kit holds itself to WCAG 2.2 AA directly — which, unlike Apple's position, is a conformance claim with a version number attached. |
| Contrast values | Via that tool: text at 17 pt or below, all weights, **4.5:1**; at 18 pt, **3:1**; bold, **3:1**. *(Accessibility page)* | Adopt as the floor and measure every pair, rather than sampling. |
| Colour alone | Colour alone is insufficient to convey meaning; Apple asks for distinct shapes or icons alongside. *(Accessibility page)* | Every status or semantic colour in this kit needs a non-colour partner — a shape, an icon or a word — and a greyscale test that proves it. |
| Target sizes | iOS and iPadOS: **44×44 pt** default, **28×28 pt** minimum. macOS: 28 / 20. tvOS: 66 / 56. visionOS: 60 / 28. watchOS: 44 / 28. *(Accessibility page)* | Interactive components must carry a documented hit area per platform. Note these are Apple's figures and differ from both Android's and WCAG's — section 6 sets out which one binds. |
| Spacing | Apple treats spacing between controls as as important as size, suggesting roughly 12 pt of padding around bezelled elements and roughly 24 pt around unbezelled ones. *(Accessibility page)* | Spacing tokens must exist alongside size tokens, and the component specifications must state the gap between adjacent controls, not only their dimensions. |
| Focus indicators | Focus guidance lives on a separate page whose change log reads **24 October 2023** — predating Liquid Glass entirely. Focus is "not supported in iOS or watchOS". **No numeric focus-indicator specification is published.** *(Focus and selection page, 24 Oct 2023)* | There is nothing here to inherit. This kit must specify its own focus indicator numerically, and should meet WCAG's figures instead (section 6). The staleness of this page is itself worth noting in the guidebook: even a first-rate design system has corners that have not been touched in nearly three years. |

### 3.5 Motion

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| Durations and easing | **Apple publishes no durations, no easing curves and no timing tokens.** The guidance is principled rather than numeric: add motion purposefully, make motion optional, favour realism, keep it brief, show restraint on frequent interactions, and let people cancel it. *(Motion page, current 14 Aug 2026)* | Every duration and curve in this kit is this kit's own invention and must be labelled as such. Presenting a timing scale as "Apple-aligned" would be false. |
| The only numbers anywhere | Games should run at 30–60 fps. On visionOS, avoid sustained oscillation at around 0.2 Hz. *(Motion page)* | Neither is applicable to a studio identity system. Recording that the search found only these two figures is more useful than inventing a scale and attributing it. |
| Reduced motion | Apple's Reduce Motion techniques: tighten springs, track gestures, avoid depth (z-axis) animation, replace movement transitions with **fades**, and avoid animating into and out of blurs. *(Accessibility page)* | This is inheritable and specific. The kit's reduced-motion rule should be: substitute a fade, never a spatial move or a blur, and prove it by toggling the setting. |

### 3.6 Apple's public brand artefacts

| Artefact | What it is, and its date | What it means for this kit |
|---|---|---|
| Human Interface Guidelines — Branding page | Public guidance on expressing an identity within Apple's platforms. *(current 14 Aug 2026)* | The nearest thing Apple publishes to advice on brand-in-product. Worth reading as a model of scope: it tells you where brand goes, not what your brand should be. |
| App Store Marketing Guidelines | Rules for third parties displaying Apple's badges and product images: badge minimum **10 mm in print / 40 px on screen**; clear space **one quarter of the badge height**; Apple product images minimum **25 mm / 200 px**. *(checked 14 Aug 2026)* | A working model for how to write minimum-size and clear-space rules: an absolute floor in both print and screen units, and clear space expressed as a proportion of the mark rather than a fixed measure. This kit should do the same for its own mark. |
| Apple Trademark List | Self-described as including updates as of **14 July 2026**, and as non-exhaustive. Its core rule: trademarks are adjectives — never verbs, plurals or possessives. *(checked 14 Aug 2026)* | The adjective rule is a borrowable convention for the studio name. Note also that neither "Liquid Glass" nor "Icon Composer" appears on the list as of 14 July 2026 — though as the list says it is not exhaustive, absence is not evidence of anything. |
| Guidelines for Using Apple Trademarks | Public rules for third-party use. *(checked 14 Aug 2026)* | A model for the permissions section of this kit's brand book. |
| Apple Identity Guidelines for Channel Affiliates | A PDF whose content dates to roughly 2013; legacy. *(checked 14 Aug 2026)* | Evidence for the section 2 finding: Apple's only public identity manual is more than a decade old and aimed at resellers. |
| Apple Style Guide | Re-published as a PDF on **25 June 2026**. Apple's closest public equivalent to a verbal-identity guide. | The best available public model for the voice and terminology half of a brand book. |
| Apple Design Resources | Template files for Figma, Sketch and Photoshop; App Icon Template refreshed **23 June 2026**. | The source of truth for icon construction, in place of a published grid. |
| WWDC26 session 251 | *Communicate your brand identity on iOS*, **8 June 2026**. Thesis: the content layer is where brand belongs. | The strongest single statement of the brand-versus-system boundary this kit is built around. |
| A brand kit | **Does not exist publicly.** | See section 2. |

---

## 4. Google — Material 3 Expressive

Material 3 Expressive was announced on **13 May 2025** at The Android Show, tied to Android 16 and
Wear OS 6. It is an **expansion of** Material 3, not a replacement for it.

### 4.1 The stability caveat, first

This matters more than any individual value, so it comes before the tables.

Material 3 Expressive is Google's current published direction, but **much of it is not yet in
stable code**. As of 14 August 2026:

- The stable Compose Material library, `androidx.compose.material3`, is at **1.4.0 (12 August 2026)**.
- Much of Expressive lives in **1.5.0-alpha** — an alpha is a pre-release channel where interfaces
  may still change without warning. The latest is alpha26, also 12 August 2026.
- The `MotionScheme` interface lost its experimental marking in 1.5.0-alpha15 (25 February 2026),
  but the library version carrying it is still an alpha.
- `materialExpressiveTheme` and `expressiveLightColorScheme` were promoted in alpha19
  (6 May 2026).
- Shape morphing shipped on `FilterChip`, `ElevatedFilterChip` and `InputChip` in alpha18
  (22 April 2026).

Two adjacent libraries are in **maintenance mode** — receiving fixes but not new work:
Material Components for Android, the older Views and XML implementation; and Material Web
Components, which Google describes as awaiting new maintainers.

**What this means for this kit:** anything borrowed from Expressive must record the library
version and its channel. Describing an alpha-stage interface as though it were settled would
mislead anyone who tried to build on it.

### 4.2 Colour

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| Number of roles | **48 roles** in the Compose `ColorScheme`. Material Web's `_md-sys-color.scss` lists 49 tokens. *(checked 14 Aug 2026)* | A studio identity does not need 48 roles, but the kit should state its own count and say which of Material's roles it does not implement, so an Android developer can see the gap immediately. |
| Tonal surfaces — the precise count | There are exactly **five** tonal surface *container* roles: `surfaceContainerLowest`, `surfaceContainerLow`, `surfaceContainer`, `surfaceContainerHigh`, `surfaceContainerHighest`. Adding `surfaceDim` and `surfaceBright` gives **seven tonal surfaces in total, of which five are containers**. *(Compose `ColorScheme`, 14 Aug 2026)* | Stating "seven containers" is wrong; so is stating "five tonal surfaces". The kit must use whichever number it means and name the roles. This is the sort of small error that a reader who works in Material spots instantly. |
| Fixed roles | A further **12** "fixed" roles exist — colours that stay constant between light and dark. | If this kit has colours that must not invert between light and dark, Material already has a vocabulary for them and the kit should borrow the naming rather than invent one. |
| Deprecations | `background`, `onBackground` and `surfaceVariant` are **deprecated** in the specification, with `surface`, `onSurface` and `surfaceContainerHighest` as replacements. Flutter enforces this. Compose still contains them and does **not** annotate them as deprecated. *(checked 14 Aug 2026)* | Do not use these three names for this kit's own roles. And say **deprecated**, never **removed** — they are still present in Compose, and a reader who checks will find them. |

### 4.3 Shape

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| Shape scale | In dp — density-independent pixels, Android's device-independent unit: None 0, ExtraSmall 4, Small 8, Medium 12, Large 16, **LargeIncreased 20**, ExtraLarge **28**, **ExtraLargeIncreased 32**, **ExtraExtraLarge 48**, plus Full. *(`ShapeTokens.kt`, 14 Aug 2026)* | If this kit maps its own radii onto Material, map onto these ten steps and record the mapping. |
| A conflict in Google's own material | Compose's *guide page* states extraLarge as 24 dp; `ShapeTokens.kt` states 28. **The token file is authoritative.** *(both checked 14 Aug 2026)* | Cite the token file, not the guide page, and note the discrepancy rather than silently picking one. |
| Shape library and morphing | **35 shapes** in `MaterialShapes.kt`. The morphing engine is `androidx.graphics:graphics-shapes`. | Shape morphing is a genuine capability this kit will not have. That should be stated as a deliberate omission with a reason, not left as a silent absence. |

### 4.4 Motion

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| Spring-based motion | `MotionScheme.standard()` and `MotionScheme.expressive()`, each providing six specifications on a 2×3 grid: `defaultSpatialSpec`, `fastSpatialSpec`, `slowSpatialSpec`, `defaultEffectsSpec`, `fastEffectsSpec`, `slowEffectsSpec`. *(checked 14 Aug 2026)* | The 2×3 structure — three speeds across two kinds of motion — is worth borrowing even if the values are not. |
| The expressive values | Spatial: default damping 0.8 / stiffness 380; fast 0.6 / 800; slow 0.8 / 200. Effects: default 1.0 / 1600; fast 1.0 / 3800; slow 1.0 / 800. *(checked 14 Aug 2026)* | Damping controls whether a spring overshoots its target before settling; stiffness controls how fast it gets there. |
| The damping split | **Every effects damping is exactly 1.0** — critically damped, meaning it never overshoots. **Every spatial damping is below 1.0** — underdamped, meaning it overshoots and settles. *(derived directly from the values above)* | This is the actual design rule underneath the numbers, and it transfers even to a kit that uses simple easing curves: things that *move* may overshoot; things that *fade, tint or resize in place* must not. Worth stating in the guidebook as the principle, with the values as evidence. |
| The older tokens still exist | The duration and easing tokens were **not** replaced by springs. **16 durations** (50–1000 ms) and **10 easing curves** remain published, including `EasingEmphasized` at (0.2, 0, 0, 1). *(checked 14 Aug 2026)* | A kit built on durations and cubic-Bézier curves — the four numbers that describe an acceleration curve — is not out of date relative to Material. It is using the other half of a system that publishes both. |

### 4.5 Typography

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| Role count | 15 base roles — Display, Headline, Title, Body and Label, each in Large, Medium and Small — **plus 15 "Emphasized" styles, giving 30 in total**. Emphasized is a parallel set at every size, not a handful of extra headings. *(checked 14 Aug 2026)* | If the kit offers an emphasis mechanism, it should be systematic across the whole scale rather than applied to selected sizes. And the kit's own role count should be stated honestly against 30. |

### 4.6 Dynamic colour

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| It is opt-in | Dynamic colour — an Android feature that derives an app palette from the user's wallpaper — is **opt-in per app**. A developer must call `applyToActivitiesIfAvailable()`. *(checked 14 Aug 2026)* | Nothing forces a brand palette to give way to the wallpaper. This is a choice, and this kit must state which choice it makes. |
| The two routes | Either hold brand colours static, or **harmonise** them towards the user's palette using `HarmonizedColors`. *(checked 14 Aug 2026)* | Naming the mechanism matters. "We keep our brand colours" is a position; "we keep our brand colours and do not use `HarmonizedColors`" is a specification. |
| The engine | `material-color-utilities`, built on HCT — hue, chroma and tone, a colour model derived from CAM16 and CIE L\* — and actively maintained (last pushed 10 August 2026). | Usable as a dependency. |
| The tool that is not | **Material Theme Builder's GitHub repository was archived in July 2026**, although the hosted tool still runs. *(checked 14 Aug 2026)* | Do not build any pipeline step on it. An archived repository receives no fixes. This is one of the traps a benchmark exists to catch. |

### 4.7 Accessibility

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| Touch targets | Android's minimum touch target is **48 dp × 48 dp**. *(checked 14 Aug 2026)* | Different from Apple's 44 pt and from WCAG's 24 CSS px. A kit that targets more than one platform must carry all three figures and say which applies where. |
| Contrast | 4.5:1 for text under 18 sp, or bold text under 14 sp; 3:1 for other text. *(sp is Android's scalable text unit.)* | Consistent with WCAG AA. Adopt as the floor. |
| Contrast variants | Material generates standard, medium and high contrast variants as a **first-class system input**, not an override applied afterwards. *(checked 14 Aug 2026)* | The strongest idea to borrow in this whole section: high contrast should be a mode the palette is generated *for*, not a patch applied to a palette designed without it. |
| Standards position | **Google does not name WCAG on the Android accessibility page.** The numbers are verified; the "AA" label is an inference. *(checked 14 Aug 2026)* | Mark it that way in the guidebook. The figures match WCAG AA; Google does not say so on that page. |

### 4.8 Research base

| Criterion | Their published standard | What it means for this kit |
|---|---|---|
| The claims | **46 studies, more than 18,000 participants**, described on Google's own site as the most researched update to its design system ever. Also: 87% preference among 18–24 year olds, and elements spotted up to 4× faster. *(design.google, checked 14 Aug 2026 — the page carries no publish date)* | Cite as **Google's stated research**, not as independent evidence. There is no published methodology, no preregistration and no peer review. The absence of a publish date on the page is itself worth recording. |
| What this kit has | Nothing comparable. | State it plainly. A one-person kit has no user research, and no amount of rigour elsewhere substitutes for that. Saying so is more credible than not mentioning it. |

### 4.9 Google's public brand artefacts

| Artefact | Status, checked 14 August 2026 | What it means for this kit |
|---|---|---|
| Brand guidelines | **Not public.** `google.com/permissions` returns a 301 redirect to `about.google/brand-resource-center`, which leads on to a partner marketing hub requiring a login; `brand.google` redirects to a Google sign-in. | Section 2's finding, confirmed on Google's side. |
| Google Sans | Not available on Google Fonts. | The corporate typeface is withheld while the design system is given away — the clearest single illustration of the brand/system split. |
| Google Fonts licensing | Most fonts are under SIL OFL 1.1; some under Apache-2.0; the Ubuntu fonts under the UFL. **The top-level directory encodes the licence** (`ofl/`, `apache/`, `ufl/`). Some fonts carry a **Reserved Font Name**, meaning a modified fork may legally require renaming. | If this kit bundles or recommends any Google font, the licence must be read from the directory it sits in, and any Reserved Font Name must be checked before any modified version is distributed. |

---

## 5. The wider field

All rows checked 14 August 2026. "Machine-readable tokens" means design tokens published as data a
build tool can consume, not a PDF or an image.

| System | Brand guidance public? | Design system public? | Machine-readable tokens? | Licence | Note |
|---|---|---|---|---|---|
| **Apple** | No brand kit; trademark, marketing and style guidance only | Yes — Human Interface Guidelines | No public token file | Guidance is documentation, not licensed code | See section 3 |
| **Google / Material 3** | No — partner login required | Yes — Material 3 and Material 3 Expressive | Yes, in code (Compose token files, Material Web SCSS) | Apache-2.0 for the libraries | Much of Expressive still alpha — section 4.1 |
| **IBM Carbon** | Not assessed here | Yes | **Yes — the only flagship system verified shipping conformant DTCG tokens**: `@carbon/themes` 11.79.0 (12 Aug 2026) has a `/src/dtcg/` directory with `$schema: https://tr.designtokens.org/format/` and `org.carbon` `$extensions` | Apache-2.0 | The reference implementation to follow for token format |
| **GitHub Primer** | Not assessed here | Yes | Yes — DTCG-style tokens | MIT | Solid, widely used |
| **Atlassian** | Not assessed here | Yes | Yes — `@atlaskit/tokens` 16.7.0, but in the **legacy Style Dictionary v3 shape**, not DTCG | Apache-2.0 | Useful as a counter-example: a current, maintained system that has not moved to the new format |
| **Adobe Spectrum** | Not assessed here | Yes | Yes, but a **bespoke schema** (`value`, `uuid`, `sets`) — **not DTCG**. The repository has been renamed to `adobe/spectrum-design-data` | Apache-2.0 | Any guide citing the old repository name is out of date |
| **Microsoft Fluent** | Not assessed here | Yes | Yes, but `@fluentui/tokens` is still at **1.0.0-alpha.24** — pre-release | MIT | Not a stable target |
| **Shopify Polaris** | Not assessed here | Yes | Yes | — | **Polaris React was archived and deprecated on 11 August 2026**, replaced by Polaris Web Components (released 1 October 2025) |
| **Salesforce Lightning** | Not assessed here | Yes | Yes | BSD-3-Clause | **The `salesforce-ux/design-system` repository is archived** (last push 2 June 2026), though npm still publishes 2.264.0 (22 July 2026) |
| **GOV.UK** | **Yes — a separate brand site** at `brand.design-system.service.gov.uk` | Yes | Yes | Code MIT; page content OGL v3.0; **the asset repository is "All rights reserved"** and the Crown logo is excluded from the OGL | The clearest public example of the section 2 split done deliberately and in the open — worth studying as the model |
| **Uber Base** | Not assessed here | Yes | Yes | MIT | — |
| **Meta** | Yes — Brand Resource Center at `meta.com/brand/resources/`: logo in four colour variations, monochrome only for low-reproduction contexts, **all usage requires approval**, and only files downloaded from the centre may be used | **No public design system** | **No public tokens** | Permission-based | Pure brand control, no system. The mirror image of Apple and Google |
| **Mailchimp** | Content style guide still public | No | No | **No LICENSE file; repository last pushed May 2022** | Frequently cited as a voice-and-tone model. Still readable, but unmaintained and unlicensed — do not copy from it |
| **Airbnb** | Cereal, the corporate typeface, is proprietary | No | No | Proprietary | `airbnb/lunar` is a different project and is not the Airbnb design system |
| **Spotify Encore** | No | **No public documentation** | No | — | Not a usable benchmark, despite being widely referenced |
| **Stripe** | **No Stripe-owned brand or design-system page was reachable** | Not reachable | Not reachable | — | **Treat every circulating claim about Stripe's brand system as unverified.** It is one of the most cited examples in brand writing and one of the least verifiable |

### The two archived benchmarks that stale guides still cite

Two systems on this list were archived in the last ten weeks, and both are still routinely
recommended:

1. **Shopify Polaris React** — archived and deprecated **11 August 2026**, three days before this
   check. Its replacement, Polaris Web Components, has existed since 1 October 2025.
2. **Salesforce `salesforce-ux/design-system`** — repository archived, last push **2 June 2026**,
   even though the npm package continued to publish (2.264.0, 22 July 2026). A live package on top
   of an archived repository is a specific hazard: the usual "is it still maintained?" check gives
   the wrong answer.

To which should be added **Material Theme Builder** (section 4.6), archived July 2026 while its
hosted tool keeps running — the same trap in a different shape.

---

## 6. Standards this kit is actually held to

Everything above is guidance from a company. This section is the part with external authority.

### 6.1 WCAG 2.2 — the accessibility standard

The Web Content Accessibility Guidelines version 2.2 are a **W3C Recommendation dated 12 December
2024**. A W3C Recommendation is the World Wide Web Consortium's final, ratified status — the
strongest standing a web standard has.

Success criteria are graded A, AA and AAA. This kit is held to **AA**, and adopts two AAA criteria
by choice where the AA equivalent is too weak to be useful.

**Level AA — the conformance target:**

| Criterion | Requirement |
|---|---|
| 1.4.3 Contrast (Minimum) | **4.5:1** for normal text; **3:1** for large text |
| 1.4.11 Non-text Contrast | **3:1** for user-interface components and meaningful graphics |
| 2.5.8 Target Size (Minimum) | **24×24 CSS pixels**, with five listed exceptions |
| 2.4.11 Focus Not Obscured (Minimum) | The focused item must not be **entirely** hidden by author-created content |

A **CSS pixel** is the web's device-independent unit of length, and is not the same as a physical
screen pixel, an Apple point or an Android dp — which is why sections 3.4 and 4.7 give three
different target-size figures.

**Level AAA — adopted selectively, by choice:**

| Criterion | Requirement | Why it is adopted here |
|---|---|---|
| 1.4.6 Contrast (Enhanced) | **7:1** for text | Adopted as an aspiration for body text, not a blanket requirement |
| 2.4.13 Focus Appearance | The focus indicator must cover at least the area of a **2 CSS pixel thick perimeter** of the component, at **3:1** contrast | Adopted outright, because there is nothing to inherit: Apple publishes no focus-indicator numbers at all (section 3.4) |
| 2.5.5 Target Size (Enhanced) | A larger minimum than 2.5.8 | Noted; the exact figure was not recorded in this research pass and must be read from the specification before it is quoted |

**Two things not to do:**

- **Do not cite WCAG 3.0.** It is a **Working Draft dated 3 March 2026** and states within itself
  that it is inappropriate to cite as anything other than work in progress.
- **Do not present APCA as a standard.** APCA — the Accessible Perceptual Contrast Algorithm, an
  alternative way of measuring contrast — **is not mentioned anywhere in the WCAG 3.0 draft and is
  not normative**. Apple names it as one of two popular measures (section 3.4); that is the whole
  of its published standing. It may be reported alongside WCAG figures, never instead of them.

### 6.2 DTCG 2025.10 — the token format

The **Design Tokens Format Module 2025.10** is a **Final Community Group Report dated 28 October
2025**, published under the W3C Community Final Specification Agreement.

**It is explicitly not a W3C Standard and is not on the W3C Standards Track.** This is a real
distinction and the guidebook should not blur it: WCAG 2.2 is a ratified standard; DTCG is a
community group's finished report. A living draft dated 30 July 2026 also exists.

What conformance requires:

- The 13 permitted `$type` values: `color`, `dimension`, `fontFamily`, `fontWeight`, `duration`,
  `cubicBezier`, `number`, `strokeStyle`, `border`, `transition`, `shadow`, `gradient`,
  `typography`.
- Aliasing — one token referring to another — via `{group.token}` syntax and `$ref` JSON Pointer.
- **Colour `$value` is now a structured object**, not a hex string:
  `{"colorSpace": "srgb", "components": […], "hex": "#…"}`.
- Dimension and duration are likewise objects carrying **mandatory units, even at zero**.

Tooling reality, checked 14 August 2026:

- **IBM Carbon `@carbon/themes` 11.79.0** (12 August 2026, Apache-2.0) is the only flagship system
  verified shipping conformant DTCG.
- **Style Dictionary 5.5.1** (7 August 2026, Apache-2.0) has had DTCG support since v4, but its own
  documentation says **2025.10 support is incomplete**, and it does not rewrite type names into
  DTCG vocabulary.
- **Tokens Studio for Figma** (MIT) supports a W3C DTCG format and a legacy format, switchable;
  DTCG coverage is not complete.

**Figma constraints, which shape what a token pipeline can actually do:**

- The `.fig` file is a **proprietary, undocumented binary format** (Kiwi codec). It cannot be
  authored in any supported way.
- The REST API — the interface for reading Figma data over the web — has **no node-creating
  endpoint**.
- The **Variables REST API requires an Enterprise plan for reading as well as writing.**
- The **Plugin API** — code running inside Figma itself — *can* create nodes and variables. This is
  the only supported authoring route.
- **Code Connect framework-specific parsers lose support on 17 August 2026** — three days after
  this check. Template files become the only maintained approach. Code Connect also requires an
  Organisation or Enterprise plan.

### 6.3 SIL OFL 1.1 — fonts

The SIL Open Font Licence is at version **1.1, dated 26 February 2007**. **There is no version
1.2.** The canonical home is now `openfontlicense.org`, moved from `scripts.sil.org`. The FAQ is at
revision 1.1-update7 (November 2023).

The operative constraint for this kit: a font may carry a **Reserved Font Name**, which means a
modified copy may legally require renaming before distribution. Any bundled or forked font must be
checked for one.

### 6.4 Apache-2.0 — code and tokens

The proposed licence for this kit's design-system half. It is an OSI-approved permissive
open-source licence, and is the licence used by IBM Carbon's themes, Style Dictionary, Atlassian's
tokens and Adobe's Spectrum design data — all verified 14 August 2026.

*(A summary of its specific terms — attribution, NOTICE file, patent grant — was not
re-verified against the licence text in this research pass, and should be read from
`apache.org/licenses/LICENSE-2.0` before being restated in the guidebook.)*

### 6.5 PolyForm Noncommercial 1.0.0 — identity assets

- SPDX identifier: `PolyForm-Noncommercial-1.0.0`. (SPDX is the standard machine-readable
  vocabulary for naming licences.)
- Released **9 July 2019**.
- Canonical URL: `https://polyformproject.org/licenses/noncommercial/1.0.0` — **with no trailing
  slash. The trailing-slash form returns a 404.** Any link in this kit must be written without it.
- **Not OSI-approved and not FSF Free/Libre.** The correct description is **source-available, not
  open source**. Calling it open source would be inaccurate.
- Licence scanners and corporate allowlists often flag it. Anyone choosing it should expect that,
  and the guidebook should warn them rather than let them discover it in a compliance review.

---

## 7. The criteria this kit must meet

Twenty-six testable criteria. **No verdicts are recorded**, because the kit does not exist yet.
Each row names the test that decides it, so the verdict can be filled in by inspection rather than
by opinion.

| # | Criterion | The test that decides it | Verdict |
|---|---|---|---|
| 1 | Icon masters are exported **unmasked**, at 1024×1024 px for iOS, iPadOS and macOS, and 1088×1088 px for watchOS | Open each exported file: check pixel dimensions, and check the four corners are opaque artwork rather than transparent rounded-off area | — |
| 2 | The mark survives a **circular** mask, not only a rounded square | Apply a circular mask to the master and confirm no essential part of the mark is clipped | — |
| 3 | **No corner-radius figure anywhere in the kit is attributed to Apple** | Search all tokens and prose for "22.37", "22.46", "squircle" and "corner radius"; every surviving figure must be labelled as this kit's own | — |
| 4 | Icon source is layered as background plus foreground, within a maximum of **four groups**, with text converted to outlines | Open the SVG: count top-level groups; confirm no `<text>` element remains | — |
| 5 | Icon source contains **no baked blur, shadow, specular highlight, opacity or background gradient** | Search the SVG for `filter`, `feGaussianBlur`, `opacity` and gradient definitions; each hit must be justified or removed | — |
| 6 | A **Mono** (single-colour) variant exists and is legible at both full size and the smallest specified size | Render the Mono layer at both sizes and confirm the mark reads | — |
| 7 | Icon masters are authored in **sRGB**; any Display P3 variant is additional, and no P3 asset is offered for visionOS | Read the embedded colour profile of every exported asset | — |
| 8 | The safe field and any margin figure are declared as **this kit's own rule**, never attributed to Apple | Read the guidebook text: the attribution must be explicit | — |
| 9 | The type scale has a documented **floor per platform**: 11 pt iOS/iPadOS, 10 pt macOS, 23 pt tvOS, 12 pt visionOS, 12 pt watchOS | Compute the smallest specified size for each surface and compare against the list | — |
| 10 | **No Ultralight, Thin or Light weight** appears in any specified role | Search the type tokens for those weight names and for any variable-font weight value below the documented lower bound | — |
| 11 | Documentation does **not** claim Dynamic Type support on macOS | Search the guidebook for "Dynamic Type" and check every macOS context | — |
| 12 | The typeface count is stated, with a reason, and any small-size compensation rules (tracking, width) are written as manual instructions with the sizes at which they apply | Count families in the type tokens; confirm each rule names a size threshold | — |
| 13 | **Every** foreground/background pair is measured and the measured figure recorded — 4.5:1 for text at 17 pt or below at any weight, 3:1 at 18 pt or bold | Run the contrast measurement over the full pair matrix and publish the resulting table, not a sample | — |
| 14 | Non-text contrast reaches **3:1** for interface components and meaningful graphics (WCAG 1.4.11 AA) | Measure borders, icons, focus rings and chart strokes against their adjacent colours | — |
| 15 | **Nothing is conveyed by colour alone** | Render every status and semantic state in greyscale; each must remain distinguishable by shape, icon or text | — |
| 16 | Interactive targets meet **24×24 CSS px** (WCAG 2.2 AA), and additionally **44×44 pt** where an Apple platform is specified and **48×48 dp** where Android is | Measure rendered hit areas per platform specification, not drawn box sizes | — |
| 17 | Spacing between adjacent controls is specified, not only their sizes — approximately 12 pt around bezelled and 24 pt around unbezelled elements where Apple platforms are targeted | Read the component specifications: each must state an inter-control gap | — |
| 18 | The **focus indicator is specified numerically by this kit**, meeting WCAG 2.4.13 geometry (area at least that of a 2 CSS px perimeter) at 3:1 contrast, and is never entirely obscured (2.4.11) | Measure the rendered indicator; attempt to overlap it with sticky page furniture and confirm part remains visible | — |
| 19 | Every motion duration and easing curve is labelled as **this kit's own**, with no attribution to Apple | Read the motion documentation for attribution claims | — |
| 20 | Reduced motion substitutes a **fade**, never a spatial move, depth transition or blur | Enable the reduced-motion setting and observe every animation in the kit | — |
| 21 | **No deprecated Material colour role name** (`background`, `onBackground`, `surfaceVariant`) is used as a token name, and any Material mapping counts tonal surfaces correctly — five containers, seven tonal surfaces | Search the token file for the three names; count surface tokens and compare against the written claim | — |
| 22 | The dynamic-colour position is stated explicitly, naming the mechanism — static brand colours, or harmonised via `HarmonizedColors` | Read the guidebook: the decision and the mechanism must both appear | — |
| 23 | Any dependency on Material Expressive records the **library version and its channel** (stable 1.4.0 versus 1.5.0-alpha) | Read the dependency manifest: version and channel must both be present | — |
| 24 | Tokens validate as **DTCG 2025.10**: only the 13 permitted `$type` values; colour values as structured objects with `colorSpace` and `components`; dimension and duration carrying units even at zero; every alias resolvable | Run schema validation against the format, then resolve every alias and confirm none dangles | — |
| 25 | **No pipeline step depends on an archived or expiring dependency** — Material Theme Builder's repository, Figma Code Connect framework-specific parsers after 17 August 2026, the Enterprise-only Figma Variables REST API, or authoring `.fig` files | Read every build script and list each external dependency with its maintenance status and licence | — |
| 26 | Licences are declared per artefact and are machine-readable — Apache-2.0 for code and tokens, the font's own licence for any bundled font (with Reserved Font Name checked before any fork is renamed), PolyForm Noncommercial 1.0.0 for identity assets using the **no-trailing-slash** canonical URL | Confirm a licence file in each artefact directory, a licence manifest listing SPDX identifiers, and a link check that every licence URL resolves | — |

Two further criteria that govern the document rather than the artefacts:

| # | Criterion | The test that decides it | Verdict |
|---|---|---|---|
| 27 | The **brand book and the design system ship as separate artefacts**, with separate licences and separate front doors, and the design system remains usable by someone not permitted to use the mark | Remove the identity assets and confirm the token set still builds and the component documentation still makes sense | — |
| 28 | **Every factual claim in the guidebook carries a source and a date checked**, and no number appears that cannot be traced to one | Read every claim: each must have a citation with a URL and a date; count the untraceable numbers, which must be zero | — |

---

## 8. What this benchmark cannot claim

- **It makes no claim of parity.** Apple and Google run design systems with research budgets,
  dedicated teams and control of the platforms themselves. This is one person's kit. The
  comparison exists to inherit good practice and to locate the gaps precisely, not to suggest the
  gaps are small.
- **It compares against published guidance only** — not against how faithfully those companies
  follow their own guidance, which was not examined and would require a different method.
- **The Meta material is structural observation.** No published Meta design specification was
  consulted, because none is public. Only the stated rules of the Brand Resource Center are
  sourced; anything said about Meta's brand architecture is observation of a visible public
  structure, and is marked as such.
- **Nothing here has been tested with a screen reader by a person who uses one.** Contrast is
  computed and target sizes are measured. Lived accessibility is a different claim and this
  document does not make it.
- **There is no user research behind this kit.** Google's figures — 46 studies, more than 18,000
  participants — are Google's own, published without methodology, preregistration or peer review,
  on a page carrying no publish date. They are reported as Google's stated research. This kit has
  no equivalent and does not pretend otherwise.
- **Several widely cited systems could not be verified.** No Stripe-owned brand or design-system
  page was reachable, so every circulating claim about Stripe's brand should be treated as
  unverified. Spotify Encore has no public documentation. Mailchimp's style guide is readable but
  its repository has no licence file and was last touched in May 2022.
- **Some rows are marked "not assessed here".** Where a system's design system was checked but its
  brand guidance was not, the table says so rather than implying an absence.
- **Guidance moves, sometimes within weeks.** Apple's icon guidance changed materially twice in
  two years. Two benchmark systems were archived in the ten weeks before this check, and a Figma
  deprecation lands three days after it. **Anything dated after 14 August 2026 supersedes this
  file.**

---

## 9. Sources

All checked **14 August 2026**. Where a deep link was not recorded in the research pass, the
canonical entry point is given and the specific page named.

### Apple

| Source | URL | Date on the source |
|---|---|---|
| Human Interface Guidelines — App Icons | `developer.apple.com/design/human-interface-guidelines/app-icons` | Change log 8 Jun 2026 (prev. 9 Jun 2025, 10 Jun 2024) |
| Human Interface Guidelines — Materials | `developer.apple.com/design/human-interface-guidelines/foundations/materials/` | Current at check |
| Human Interface Guidelines — Typography | `developer.apple.com/design/human-interface-guidelines/typography` | Change log 16 Dec 2025 |
| Human Interface Guidelines — Accessibility | `developer.apple.com/design/human-interface-guidelines/accessibility` | Current at check |
| Human Interface Guidelines — Motion | `developer.apple.com/design/human-interface-guidelines/motion` | Current at check |
| Human Interface Guidelines — Focus and selection | `developer.apple.com/design/human-interface-guidelines/focus-and-selection` | Change log 24 Oct 2023 |
| Human Interface Guidelines — Branding | `developer.apple.com/design/human-interface-guidelines/foundations/branding/` | Current at check |
| Adopting Liquid Glass | `developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass` | Current at check |
| Creating your app icon using Icon Composer (Xcode documentation) | `developer.apple.com/documentation/xcode` — Icon Composer article | Current at check |
| Apple Design Resources (App Icon Template) | `developer.apple.com/design/resources/` | Refreshed 23 Jun 2026 |
| App Store Marketing Guidelines | `developer.apple.com/app-store/marketing/guidelines/` | Current at check |
| Apple Trademark List | `apple.com/legal/intellectual-property/trademark/appletmlist.html` | States updates as of 14 Jul 2026 |
| Guidelines for Using Apple Trademarks and Copyrights | `apple.com/legal/intellectual-property/guidelinesfor3rdparties.html` | Current at check |
| Apple Identity Guidelines for Channel Affiliates (PDF) | `apple.com/legal/sales-support/certification/docs/logo_guidelines.pdf` | Content c. 2013 |
| Apple Style Guide (PDF) | `help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf` | Re-published 25 Jun 2026 |
| WWDC26 session 251 — *Communicate your brand identity on iOS* | `developer.apple.com/videos/play/wwdc2026/251/` | 8 Jun 2026 |

### Google

| Source | URL | Date on the source |
|---|---|---|
| Material 3 Expressive launch announcement | `blog.google/products-and-platforms/platforms/android/material-3-expressive-android-wearos-launch/` | 13 May 2025 |
| Material 3 specification | `m3.material.io` | Current at check |
| Compose Material 3 release notes (versions, alphas, promotions) | `developer.android.com/jetpack/androidx/releases/compose-material3` | 1.4.0 and 1.5.0-alpha26, both 12 Aug 2026 |
| Compose `ColorScheme`, `ShapeTokens.kt`, `MaterialShapes.kt`, `MotionScheme` | AndroidX source, via `developer.android.com` and the AndroidX repository | Checked 14 Aug 2026 |
| Material Components for Android (maintenance mode) | `github.com/material-components/material-components-android` | Checked 14 Aug 2026 |
| Material Web Components (maintenance mode) | `github.com/material-components/material-web` | Checked 14 Aug 2026 |
| `material-color-utilities` | `github.com/material-foundation/material-color-utilities` | Last push 10 Aug 2026 |
| Material Theme Builder (repository archived) | `github.com/material-foundation/material-theme-builder` | Archived Jul 2026 |
| Android accessibility guidance (touch targets, contrast) | `developer.android.com` — accessibility pages | Checked 14 Aug 2026 |
| Expressive design research | `design.google/library/expressive-material-design-google-research` | **No publish date on the page** |
| Google brand resources (redirect chain) | `google.com/permissions` → `about.google/brand-resource-center` → `partnermarketinghub.withgoogle.com`; `brand.google` → sign-in | Checked 14 Aug 2026 |
| Google Fonts licensing structure | `fonts.google.com` and `github.com/google/fonts` (`ofl/`, `apache/`, `ufl/`) | Checked 14 Aug 2026 |

### Standards and formats

| Source | URL | Date on the source |
|---|---|---|
| WCAG 2.2 | `w3.org/TR/WCAG22/` | W3C Recommendation, 12 Dec 2024 |
| WCAG 3.0 | `w3.org/TR/wcag-3.0/` | Working Draft, 3 Mar 2026 |
| Design Tokens Format Module 2025.10 | `designtokens.org/tr/2025.10/format/` | Final Community Group Report, 28 Oct 2025 |
| DTCG schema identifier used by implementers | `tr.designtokens.org/format/` | Checked 14 Aug 2026 |
| SIL Open Font Licence 1.1 | `openfontlicense.org` | Licence 26 Feb 2007; FAQ 1.1-update7, Nov 2023 |
| Apache License 2.0 | `apache.org/licenses/LICENSE-2.0` | Checked 14 Aug 2026 |
| PolyForm Noncommercial 1.0.0 | `polyformproject.org/licenses/noncommercial/1.0.0` (**no trailing slash**) | Released 9 Jul 2019 |
| SPDX licence list | `spdx.org/licenses/` | Checked 14 Aug 2026 |

### Tooling and other design systems

| Source | URL | Date on the source |
|---|---|---|
| IBM Carbon `@carbon/themes` (DTCG tokens) | `github.com/carbon-design-system/carbon` | 11.79.0, 12 Aug 2026, Apache-2.0 |
| Style Dictionary | `styledictionary.com` | 5.5.1, 7 Aug 2026, Apache-2.0 |
| Tokens Studio for Figma | Tokens Studio documentation | Checked 14 Aug 2026, MIT |
| Figma REST and Plugin APIs; Variables API plan requirements | `developers.figma.com/docs/` | Checked 14 Aug 2026 |
| Figma Code Connect — parser deprecation | `developers.figma.com/docs/code-connect/` and `github.com/figma/code-connect` | Framework-specific parsers unsupported from 17 Aug 2026 |
| GitHub Primer | `primer.style` | Checked 14 Aug 2026, MIT |
| Atlassian `@atlaskit/tokens` | `atlassian.design` | 16.7.0, Apache-2.0 |
| Adobe Spectrum design data (repository renamed) | `github.com/adobe/spectrum-design-data` | Checked 14 Aug 2026, Apache-2.0 |
| Microsoft Fluent `@fluentui/tokens` | `github.com/microsoft/fluentui` | 1.0.0-alpha.24 |
| Shopify Polaris | `polaris.shopify.com` | Polaris React archived and deprecated 11 Aug 2026; Polaris Web Components released 1 Oct 2025 |
| Salesforce Lightning Design System | `github.com/salesforce-ux/design-system` | Repository archived, last push 2 Jun 2026; npm 2.264.0, 22 Jul 2026, BSD-3-Clause |
| GOV.UK Design System and brand site | `design-system.service.gov.uk` and `brand.design-system.service.gov.uk` | Code MIT; content OGL v3.0; assets "All rights reserved" |
| Uber Base | `base.uber.com` | Checked 14 Aug 2026, MIT |
| Meta Brand Resource Center | `meta.com/brand/resources/` | Checked 14 Aug 2026 |
| Mailchimp content style guide | `styleguide.mailchimp.com` | Repository last pushed May 2022; no LICENSE file |
| Stripe | No Stripe-owned brand or design-system page reachable | Checked 14 Aug 2026 |
| Spotify Encore | No public documentation found | Checked 14 Aug 2026 |

---

*End of source document. Checked 14 August 2026. The date is part of the claim.*
