# Where this kit stands against Apple and Google

GENERATED FILE. Written by `scripts/gaps.py` from `01_research/_data/platform-gaps.json`. Do not hand-edit — the next build overwrites it. Change the data and re-run.

**Assessed:** 26 August 2026.

Apple Human Interface Guidelines and App Store Connect, and Google Material 3, Android developer documentation and Google Play Console, all read on 26 August 2026.

23 gaps: **8 blockers**, 8 major, 7 minor. 21 open, 2 deferred with the reason recorded. 20 of 23 cite a published requirement, across 14 distinct sources; the rest are rules this kit sets for itself and are marked as such.

A **blocker** means a store would refuse the listing, or a platform's own component set cannot be built. It does not mean the work is poor. Every one of them is a thing this kit never claimed to do, being claimed now.

---

## The short answer

| # | Gap | Platform | Severity |
|---|---|---|---|
| `G-ICON-1` | The app icon is pre-rounded, and both platforms ask for it not to be | Both | Blocker |
| `G-ICON-2` | No 1024 px raster exists, only a vector that is never rendered | Apple | Blocker |
| `G-ICON-3` | The watchOS master is pre-rounded and no unmasked 1088 exists | Apple | Blocker |
| `G-ICON-4` | No adaptive icon exists at all | Google | Blocker |
| `G-ICON-6` | No Play Store icon | Google | Blocker |
| `G-STORE-1` | No feature graphic | Google | Blocker |
| `G-STORE-2` | No store screenshots, and none can honestly be made yet | Both | Blocker |
| `G-COLOUR-1` | No token is named for the colour that sits on the accent | Google | Blocker |
| `G-ICON-5` | No monochrome layer, so themed icons fall back or are machine-generated | Google | Major |
| `G-COLOUR-2` | No Material 3 role mapping exists | Google | Major |
| `G-COLOUR-3` | Material needs secondary and tertiary groups; the brand premise forbids a second expressive colour | Google | Major |
| `G-NATIVE-1` | Tokens reach no Apple or Android surface | Both | Major |
| `G-NATIVE-2` | No component maps to either platform | Both | Major |
| `G-ICON-7` | No artefact is designated the Mono appearance layer | Apple | Major |
| `G-REC-1` | The type recommendation names a stack that did not ship | This kit's own record | Major |
| `G-REC-4` | The benchmark missed an announcement nine days older than its own check date | This kit's own record | Major |
| `G-STORE-3` | No raster declares its colour space | Both | Minor |
| `G-STORE-4` | No notification icon | Google | Minor |
| `G-MOTION-1` | Reduced motion removes transitions rather than substituting a fade | Both | Minor |
| `G-A11Y-1` | Contrast is measured by WCAG relative luminance only; Apple now names APCA as well | Apple | Minor |
| `G-A11Y-2` | Accessibility Nutrition Labels are unaddressed | Apple | Minor |
| `G-REC-2` | A third, stale type answer survives in the directions build | This kit's own record | Minor |
| `G-REC-3` | The mark's minimum size is not in the mark's own manifest | This kit's own record | Minor |

---

## The icon

### `G-ICON-1` — The app icon is pre-rounded, and both platforms ask for it not to be

**Blocker** · Both · open

**What is required.** Apple: "Produce appropriately shaped, unmasked layers. The system masks all layer edges… Providing layers with pre-defined masking negatively impacts specular highlight effects and makes edges look jagged." Google: the Play icon is a full square and Play applies a corner mask equivalent to 30 % of the icon size, plus the drop shadow.

**What is here.** Every shipped icon carries rx=24 ry=24 on the 100-unit grid and measures 4.7 % background showing. 04_mark/manifest.json records the decision behind it: "One rounded icon is used on every surface, Apple included. Owner's decision, 14 August 2026."

**The fix.** Reversed by the owner on 26 August 2026: follow each platform's own geometry. Square unmasked masters for Apple, a full square for Play, layered adaptive icons for Android, and the rounded tile kept for the web, because a browser will not round a favicon for you.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/app-icons` — change log 8 Jun 2026; read 26 Aug 2026
- `developer.android.com/distribute/google-play/resources/icon-design-specifications` — page updated 15 Jun 2026; read 26 Aug 2026

### `G-ICON-2` — No 1024 px raster exists, only a vector that is never rendered

**Blocker** · Apple · open

**What is required.** App icon layout size is 1024×1024 px for iOS, iPadOS and macOS.

**What is here.** 04_mark/svg/icon-appstore-square-1024.svg exists and is square, fully opaque, 0.0 % background showing. 10_assets/MANIFEST.json states plainly that it "is not rendered by this build". The largest raster in the tree is 512×512.

**The fix.** Render it, and its watchOS sibling, through the existing Chromium harness with the existing measured guards.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/app-icons` — change log 8 Jun 2026; read 26 Aug 2026

### `G-ICON-3` — The watchOS master is pre-rounded and no unmasked 1088 exists

**Blocker** · Apple · open

**What is required.** watchOS app icon layout size is 1088×1088 px, unmasked; the system masks it to a circle.

**What is here.** icon-1088-watch.svg is the correct 1088×1088 but carries rx=24 ry=24 and all four corners read (0,0,0,0). Benchmark criterion 1 already records this as part met.

**The fix.** Replace with a square unmasked 1088 whose body is provably the same artwork as the 1024.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/app-icons` — change log 8 Jun 2026; read 26 Aug 2026

### `G-ICON-4` — No adaptive icon exists at all

**Blocker** · Google · open

**What is required.** Each layer is 108×108 dp; the safe zone never clipped by any mask is 66×66 dp centred; the outer 18 dp per side is reserved for masking and motion effects.

**What is here.** No ic_launcher, no mipmap directory, no foreground or background layer anywhere in the repository. The string "adaptive icon" does not appear in any file.

**The fix.** Draw background, foreground and monochrome layers on a 108-unit grid. The placement rule already in 04_mark/build.py generalises: scale is safe_radius / mark_half_diagonal, so 33 / 48.87228 = 0.675229 at stroke 9.

**Sources.**

- `developer.android.com/develop/ui/views/launch/icon_design_adaptive` — page updated 13 Aug 2026; read 26 Aug 2026

### `G-ICON-5` — No monochrome layer, so themed icons fall back or are machine-generated

**Major** · Google · open

**What is required.** A single monochrome layer supports user theming from Android 13 (API 33). From Android 16 QPR 2 the system themes icons automatically for apps that supply none.

**What is here.** 11_site/site.webmanifest declares only "any" and "maskable". No monochrome purpose and no monochrome drawable exists.

**The fix.** Emit a monochrome layer with geometry provably identical to the foreground, and gate that identity by comparing rendered alpha channels.

**Sources.**

- `developer.android.com/develop/ui/views/launch/icon_design_adaptive` — page updated 13 Aug 2026; read 26 Aug 2026

### `G-ICON-7` — No artefact is designated the Mono appearance layer

**Major** · Apple · open

**What is required.** Apple's specification table lists six appearances for iOS, iPadOS and macOS; the prose says four; Icon Composer has you author three, of which Mono is one, and previews clear and tinted from it.

**What is here.** Benchmark criterion 6, part met: single-colour recolourable marks render legibly at 1024 px and at the documented 16 px floor, counter open in both, but no artefact is designated a Mono appearance layer.

**The fix.** Author Default, Dark and Mono, and record that the other four appearances are generated by Apple's renderer and cannot be shown by this build.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/app-icons` — change log 8 Jun 2026; read 26 Aug 2026

---

## Store assets

### `G-ICON-6` — No Play Store icon

**Blocker** · Google · open

**What is required.** 512×512 px, 32-bit PNG, sRGB, maximum 1024 KB, full square. Mandatory to publish a listing.

**What is here.** Nothing of that size or purpose exists.

**The fix.** Render from the square Apple master, which already clears Play's mask: the furthest inked pixel sits 221.7 px from centre against a nearest mask boundary of 256 px, 34.3 px of clearance.

**Sources.**

- `developer.android.com/distribute/google-play/resources/icon-design-specifications` — page updated 15 Jun 2026; read 26 Aug 2026
- `support.google.com/googleplay/android-developer/answer/9866151` — no date published; read 26 Aug 2026

### `G-STORE-1` — No feature graphic

**Blocker** · Google · open

**What is required.** 1024×500 px, JPEG or 24-bit PNG, no alpha. "You must provide a feature graphic to publish your store listing." It must not contain device images, screenshots, or small text illegible when scaled down, and must not resemble an advertisement.

**What is here.** No file of that dimension exists and the term appears nowhere in the repository.

**The fix.** Draw it from the existing banner harness, which already produces seven social banners from tokens, and gate it for the absent alpha band.

**Sources.**

- `support.google.com/googleplay/android-developer/answer/9866151` — no date published; read 26 Aug 2026
- `developer.android.com/docs/quality-guidelines/core-app-quality` — page updated 21 Aug 2026; read 26 Aug 2026

### `G-STORE-2` — No store screenshots, and none can honestly be made yet

**Blocker** · Both · open

**What is required.** Google: at least two across device types, mandatory to publish. Apple: iPhone 6.9 inch and iPad 13 inch, 1 to 10 per device type, no alpha channels. Apple additionally forbids screenshots that show only title art, a login page or a splash screen.

**What is here.** No screenshot assets exist. No Aninda Studio app exists either, so there is nothing truthful to photograph.

**The fix.** Ship correctly sized frames that could not be mistaken for real captures, plus a step-by-step guide for replacing them. Owner's decision, 26 August 2026. The frames carry no mark, because a frame carrying only the logo is precisely what guideline 2.3.3 rejects.

**Sources.**

- `developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications` — read 26 Aug 2026
- `developer.apple.com/app-store/review/guidelines/` — App Review Guideline 2.3.3; read 26 Aug 2026
- `support.google.com/googleplay/android-developer/answer/9866151` — no date published; read 26 Aug 2026

### `G-STORE-3` — No raster declares its colour space

**Minor** · Both · open

**What is required.** Play requires sRGB for the store icon. Apple supports sRGB, Gray Gamma 2.2 and Display P3.

**What is here.** Benchmark criterion 7, scored 19 August 2026: no P3 asset exists anywhere, but none of the 19 exported rasters carries an embedded profile, so sRGB is implicit rather than declared.

**The fix.** Write an sRGB chunk in the PNG stamping step and gate it by reading the chunk back. This declares which space the numbers are in; it does not claim the renderer produced them.

**Sources.**

- `developer.android.com/distribute/google-play/resources/icon-design-specifications` — page updated 15 Jun 2026; read 26 Aug 2026

### `G-STORE-4` — No notification icon

**Minor** · Google · deferred, with the reason recorded

**What is required.** A small icon is the only user-visible content a notification requires. It renders monochrome in the status bar and the system tints it from Android 12.

**What is here.** None exists. The answer is computable from the mark's own floor: at 24 dp the regular stroke renders at 9 × 0.920767 × 0.24 = 1.99 px, below the 2.4 px the 16 px mark floor is written against, while the heavy stroke gives 3.05 px.

**The fix.** Not required to publish either listing, and no app exists to notify. The measurement is recorded so the next person does not re-derive it: if one is ever needed, it is the heavy artwork.

**Sources.**

- `developer.android.com/develop/ui/views/notifications/build-notification` — page updated 14 Aug 2026; read 26 Aug 2026

---

## Colour

### `G-COLOUR-1` — No token is named for the colour that sits on the accent

**Blocker** · Google · open

**What is required.** Material 3 cannot construct a ColorScheme without onPrimary, and every on-role and on-container role has the same requirement. The Compose primary constructor takes 48 named parameters and has no defaults.

**What is here.** 08_components/src/components.css:225 paints .as-btn--primary with background-color: var(--as-accent) and color: var(--as-surface-lowest), and 08_components/check.py already measures that composited pair in a real browser at rest, hover and active. So the pair is proven. What is missing is the name: no token carries it, so nothing downstream can reference it. The Figma plugin's own receipt records the consequence — it draws outlined rather than filled buttons "because no 'on accent' text colour is defined".

**The fix.** Promote the existing, already-measured relationship to a named token. This invents no colour.

**Sources.**

- `m3.material.io/styles/color/roles` — read 26 Aug 2026 through a browser

### `G-COLOUR-2` — No Material 3 role mapping exists

**Major** · Google · open

**What is required.** 26 documented colour roles in six groups, plus add-on roles; 48 parameters on the Compose constructor.

**What is here.** 18 semantic colours per theme: 7 surfaces plus ink, ink-muted, line, accent, accent-edge, accent-hover, focus-ring, success, warning, danger and info.

**The fix.** Derive every missing role from a step of an existing measured ramp and prove each pair, rather than inventing values. The surfaces map one to one, because 05_colour/engine.py already orders seven tonal surfaces of which five are containers.

**Sources.**

- `m3.material.io/styles/color/roles` — read 26 Aug 2026 through a browser

### `G-COLOUR-3` — Material needs secondary and tertiary groups; the brand premise forbids a second expressive colour

**Major** · Google · open

**What is required.** Material components reference secondary and tertiary roles, so those roles must exist.

**What is here.** 05_colour/directions/estuary.json states the premise: "the warmth coming from the paper rather than from a second expressive colour." Two brand families exist, ground and accent, and no third hue.

**The fix.** Fill secondary from the ground family and tertiary from the accent family at another tonal position. Every role then exists and no new hue enters the brand. Material Theme Builder would rotate the hue about 60 degrees to invent a tertiary; that is a brand decision no measurement can make, so it is refused. The consequence, that an Aninda scheme carries less hue variety than a stock one, is recorded rather than hidden.

**Sources.**

- `m3.material.io/styles/color/roles` — read 26 Aug 2026 through a browser

---

## Reaching a native app

### `G-NATIVE-1` — Tokens reach no Apple or Android surface

**Major** · Both · open

**What is required.** Apple: "When you need a custom color, add a Color Set asset to your app's asset catalog in Xcode, and specify the bright and dim variants… Avoid using hard-coded color values or colors that don't adapt." Android core app quality requires app content to support both light and dark themes (Theme_Support). Neither is reachable from a stylesheet.

**What is here.** Tokens emit CSS, DTCG JSON, TypeScript and Python. There is no Swift, Kotlin, Xcode or Gradle file in the repository; benchmark criterion 23 records this in writing. The three platform target tokens, 28, 44 and 48 px, are cited figures rather than outputs.

**The fix.** Emit a framework-free token layer for each platform, then the framework layers above it.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/dark-mode` — change log 6 Aug 2024; read 26 Aug 2026
- `developer.android.com/docs/quality-guidelines/core-app-quality` — page updated 21 Aug 2026; read 26 Aug 2026

### `G-NATIVE-2` — No component maps to either platform

**Major** · Both · open

**What is required.** Apple gives default and minimum control sizes per platform — 44×44 pt default and 28×28 pt minimum on iOS and iPadOS — and asks for roughly 12 pt of padding around bezelled elements and 24 pt around unbezelled ones. Android core app quality requires touch targets of at least 48 dp (Touch_Target_Size), 3:1 contrast for large text and graphics and 4.5:1 for small text (Visual_Contrast), and a content description on every element that is not a TextView (Content_Description). A stylesheet can satisfy none of these on either platform.

**What is here.** 30 cards, HTML and CSS only: 1,109 lines and 87 class blocks in 08_components/src/components.css. No SwiftUI, no Compose, no Material role names, no Cupertino equivalents.

**The fix.** Implement the 16 components as thin token-styled wrappers over platform controls wherever a platform control exists, so the accessibility the platform provides is inherited rather than re-implemented. The 8 patterns become example targets outside the public API; the 6 foundations are documentation and have nothing to implement.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/accessibility` — change log 9 Jun 2025; read 26 Aug 2026
- `developer.android.com/docs/quality-guidelines/core-app-quality` — page updated 21 Aug 2026; read 26 Aug 2026

---

## Motion

### `G-MOTION-1` — Reduced motion removes transitions rather than substituting a fade

**Minor** · Both · open

**What is required.** Apple: "When this setting is active, ensure your app or game responds by reducing automatic and repetitive animations, including zooming, scaling, and peripheral motion," and lists replacing transitions among the practices for doing so. Material expresses the same split in its motion scheme: every effects damping is 1.0 and never overshoots, while spatial motion does — so the reduced case is the effects half, not the absence of both.

**What is here.** Benchmark criterion 20, part met: nothing moves, blurs or changes depth either way, but under prefers-reduced-motion both duration tokens fall to 1 ms and the colour transitions are removed rather than cross-faded.

**The fix.** Substitute a fade rather than collapsing the duration.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/accessibility` — change log 9 Jun 2025; read 26 Aug 2026
- `github.com/androidx/androidx` — StandardMotionTokens.kt and ExpressiveMotionTokens.kt, VERSION v0_14_0; read 26 Aug 2026

---

## Accessibility

### `G-A11Y-1` — Contrast is measured by WCAG relative luminance only; Apple now names APCA as well

**Minor** · Apple · open

**What is required.** Apple's Accessibility page names both the Web Content Accessibility Guidelines and the Accessible Perceptual Contrast Algorithm as standards of measure.

**What is here.** 05_colour/engine.py measures WCAG 2.1 relative-luminance ratios with coloraide, method wcag21. There is no APCA anywhere in the repository.

**The fix.** Additive, not a defect. Publishing an APCA figure beside the WCAG one would say more about small text than a ratio can. It changes no existing verdict.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/accessibility` — change log 9 Jun 2025; read 26 Aug 2026

### `G-A11Y-2` — Accessibility Nutrition Labels are unaddressed

**Minor** · Apple · deferred, with the reason recorded

**What is required.** Voluntary today, with nine declarable features. The threshold to claim one is strict: a person must be able to complete all common tasks of the app using that feature.

**What is here.** Apple's own wording is "voluntary to start", and the Upcoming Requirements page carries no entry for them as at 26 August 2026.

**The fix.** Record which of the nine this system can already substantiate from measurements it holds, and which it cannot. Claiming one needs an app, because the threshold is about completing tasks.

**Sources.**

- `developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels` — read 26 Aug 2026

---

## The record itself

### `G-REC-1` — The type recommendation names a stack that did not ship

**Major** · This kit's own record · open

**What is required.** One name for one thing.

**What is here.** 06_type/RECOMMENDATION.md recommends Inter, Noto Sans Bengali and JetBrains Mono. 07_tokens/build.py ships Literata, Noto Serif Bengali and Aninda Mono. No document records the reversal; it is visible only in the generator.

**The fix.** Record the reversal and its reason where the recommendation is, so a reader is not sent to the wrong stack.

**Sources.** None. This is a rule this kit sets for itself, and no platform is cited for it.

### `G-REC-4` — The benchmark missed an announcement nine days older than its own check date

**Major** · This kit's own record · open

**What is required.** A benchmark that claims a check date must actually cover what was published before it.

**What is here.** Apple announced new App Store creative asset slots on 5 August 2026. The benchmark was checked on 14 August 2026 and does not mention them. The Play icon design specification, updated 15 June 2026, was missed the same way.

**The fix.** The fault is structural rather than careless: the check read guideline pages and not the developer news feed or the distribution pages. Both are now sources, and the omission is recorded as a method finding rather than quietly patched.

**Sources.**

- `developer.apple.com/app-store/asset-best-practices/` — announced 5 Aug 2026; read 26 Aug 2026

### `G-REC-2` — A third, stale type answer survives in the directions build

**Minor** · This kit's own record · open

**What is required.** One name for one thing.

**What is here.** 03_directions/build.py names Estuary's type as Archivo, Noto Sans Bengali and JetBrains Mono. The file is flagged as one-off exploration and sits outside the build chain, but it still generates COMPARE.html and COMPARE.pdf.

**The fix.** Mark the stale answer where it is generated, rather than leaving a reader to discover the contradiction.

**Sources.** None. This is a rule this kit sets for itself, and no platform is cited for it.

### `G-REC-3` — The mark's minimum size is not in the mark's own manifest

**Minor** · This kit's own record · open

**What is required.** A consumer reading the manifest should find every rule the manifest is about.

**What is here.** 04_mark/manifest.json states the stroke rule and the safe field but no minimum size. The 16 px floor lives in a plugin script, and its own reference document acknowledges the split.

**The fix.** Carry the floor in the manifest, computed rather than typed.

**Sources.** None. This is a rule this kit sets for itself, and no platform is cited for it.

---

## What this register cannot tell you

- **It does not prove a store would accept anything.** Every figure is measured against a published specification, not against a console's own validator. A console may refuse a file for a reason no published page states.
- **It is current only on the date at the top.** Store specifications change without notice and without a change log. Two of the gaps here exist because a page moved and this kit did not notice for twelve days.
- **It measures distance, not quality.** A kit can close every gap here and still be unpleasant to use. Contrast, target size and safe-zone occupancy are measurable; whether a person can finish a task is not.
- **Some requirements have no number to meet.** Apple publishes no app-icon corner radius, no numeric safe zone outside tvOS, and no pixel dimensions for its new creative slots. Where that is so, this register says so rather than supplying a figure and attributing it.

