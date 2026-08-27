# Where this kit stands against Apple and Google

GENERATED FILE. Written by `scripts/gaps.py` from `01_research/_data/platform-gaps.json`. Do not hand-edit — the next build overwrites it. Change the data and re-run.

**Assessed:** 26 August 2026.

Apple Human Interface Guidelines and App Store Connect, and Google Material 3, Android developer documentation and Google Play Console, all read on 26 August 2026.

23 gaps found: **8 blockers**, 8 major, 7 minor.

**15 are now closed**, 6 are open and 2 are deferred with the reason recorded. Of the 8 blockers, **1 remain open**.

20 of 23 cite a published requirement, across 14 distinct sources; the rest are rules this kit sets for itself and are marked as such. A closed gap keeps its entry, because the record of what was wrong is the useful part.

A **blocker** means a store would refuse the listing, or a platform's own component set cannot be built. It does not mean the work is poor. Every one of them is a thing this kit never claimed to do, being claimed now.

---

## The short answer

| # | Gap | Platform | Severity | Status |
|---|---|---|---|---|
| `G-STORE-2` | No store screenshots, and none can honestly be made yet | Both | Blocker | open |
| `G-COLOUR-1` | No token is named for the colour that sits on the accent | Google | Blocker | **closed** |
| `G-ICON-1` | The app icon is pre-rounded, and both platforms ask for it not to be | Both | Blocker | **closed** |
| `G-ICON-2` | No 1024 px raster exists, only a vector that is never rendered | Apple | Blocker | **closed** |
| `G-ICON-3` | The watchOS master is pre-rounded and no unmasked 1088 exists | Apple | Blocker | **closed** |
| `G-ICON-4` | No adaptive icon exists at all | Google | Blocker | **closed** |
| `G-ICON-6` | No Play Store icon | Google | Blocker | **closed** |
| `G-STORE-1` | No feature graphic | Google | Blocker | **closed** |
| `G-REC-1` | The type recommendation names a stack that did not ship | This kit's own record | Major | open |
| `G-REC-4` | The benchmark missed an announcement nine days older than its own check date | This kit's own record | Major | open |
| `G-COLOUR-2` | No Material 3 role mapping exists | Google | Major | **closed** |
| `G-COLOUR-3` | Material needs secondary and tertiary groups; the brand premise forbids a second expressive colour | Google | Major | **closed** |
| `G-ICON-5` | No monochrome layer, so themed icons fall back or are machine-generated | Google | Major | **closed** |
| `G-ICON-7` | No artefact is designated the Mono appearance layer | Apple | Major | **closed** |
| `G-NATIVE-1` | Tokens reach no Apple or Android surface | Both | Major | **closed** |
| `G-NATIVE-2` | No component maps to either platform | Both | Major | **closed** |
| `G-A11Y-1` | Contrast is measured by WCAG relative luminance only; Apple now names APCA as well | Apple | Minor | open |
| `G-MOTION-1` | Reduced motion removes transitions rather than substituting a fade | Both | Minor | open |
| `G-REC-3` | The mark's minimum size is not in the mark's own manifest | This kit's own record | Minor | open |
| `G-A11Y-2` | Accessibility Nutrition Labels are unaddressed | Apple | Minor | deferred |
| `G-REC-2` | A third, stale type answer survives in the directions build | This kit's own record | Minor | **closed** |
| `G-STORE-3` | No raster declares its colour space | Both | Minor | **closed** |
| `G-STORE-4` | No notification icon | Google | Minor | deferred |

---

## The icon

### `G-ICON-1` — The app icon is pre-rounded, and both platforms ask for it not to be

**Blocker** · Both · closed

**What is required.** Apple: "Produce appropriately shaped, unmasked layers. The system masks all layer edges… Providing layers with pre-defined masking negatively impacts specular highlight effects and makes edges look jagged." Google: the Play icon is a full square and Play applies a corner mask equivalent to 30 % of the icon size, plus the drop shadow.

**What is here.** Every shipped icon carries rx=24 ry=24 on the 100-unit grid and measures 4.7 % background showing. 04_mark/manifest.json records the decision behind it: "One rounded icon is used on every surface, Apple included. Owner's decision, 14 August 2026."

**The fix.** Closed 26 August 2026. The owner reversed the policy and 04_mark/build.py now writes square unmasked masters for Apple and three 108 dp layers for Android, with the rounded tile kept for the web. Measured: the Apple masters and the Android background show 0.0 per cent background, and the mark reads at the same size on both platforms to within 1.24 percentage points.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/app-icons` — change log 8 Jun 2026; read 26 Aug 2026
- `developer.android.com/distribute/google-play/resources/icon-design-specifications` — page updated 15 Jun 2026; read 26 Aug 2026

### `G-ICON-2` — No 1024 px raster exists, only a vector that is never rendered

**Blocker** · Apple · closed

**What is required.** App icon layout size is 1024×1024 px for iOS, iPadOS and macOS.

**What is here.** 04_mark/svg/icon-appstore-square-1024.svg exists and is square, fully opaque, 0.0 % background showing. 10_assets/MANIFEST.json states plainly that it "is not rendered by this build". The largest raster in the tree is 512×512.

**The fix.** Closed 26 August 2026. 14_delivery/build.py renders icon-1024.png, -dark, -mono and the 1088 watchOS master, each measured for opaque corners and each declaring sRGB.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/app-icons` — change log 8 Jun 2026; read 26 Aug 2026

### `G-ICON-3` — The watchOS master is pre-rounded and no unmasked 1088 exists

**Blocker** · Apple · closed

**What is required.** watchOS app icon layout size is 1088×1088 px, unmasked; the system masks it to a circle.

**What is here.** icon-1088-watch.svg is the correct 1088×1088 but carries rx=24 ry=24 and all four corners read (0,0,0,0). Benchmark criterion 1 already records this as part met.

**The fix.** Closed 26 August 2026. icon-apple-1088-watch.svg is square and unmasked, and its rendered master measures 0.0 per cent background showing.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/app-icons` — change log 8 Jun 2026; read 26 Aug 2026

### `G-ICON-4` — No adaptive icon exists at all

**Blocker** · Google · closed

**What is required.** Each layer is 108×108 dp; the safe zone never clipped by any mask is 66×66 dp centred; the outer 18 dp per side is reserved for masking and motion effects.

**What is here.** No ic_launcher, no mipmap directory, no foreground or background layer anywhere in the repository. The string "adaptive icon" does not appear in any file.

**The fix.** Closed 26 August 2026. Background, foreground and monochrome layers exist on the 108 dp canvas, rendered at all five densities, with ic_launcher.xml. Every foreground pixel is measured against the 66 dp safe circle, in both directions, so a mark that shrank would fail as loudly as one that overflowed.

**Sources.**

- `developer.android.com/develop/ui/views/launch/icon_design_adaptive` — page updated 13 Aug 2026; read 26 Aug 2026

### `G-ICON-5` — No monochrome layer, so themed icons fall back or are machine-generated

**Major** · Google · closed

**What is required.** A single monochrome layer supports user theming from Android 13 (API 33). From Android 16 QPR 2 the system themes icons automatically for apps that supply none.

**What is here.** 11_site/site.webmanifest declares only "any" and "maskable". No monochrome purpose and no monochrome drawable exists.

**The fix.** Closed 26 August 2026. The monochrome layer is byte-identical to the foreground apart from its title, is measured for a single grey value, and is declared unconditionally in ic_launcher.xml.

**Sources.**

- `developer.android.com/develop/ui/views/launch/icon_design_adaptive` — page updated 13 Aug 2026; read 26 Aug 2026

### `G-ICON-7` — No artefact is designated the Mono appearance layer

**Major** · Apple · closed

**What is required.** Apple's specification table lists six appearances for iOS, iPadOS and macOS; the prose says four; Icon Composer has you author three, of which Mono is one, and previews clear and tinted from it.

**What is here.** Benchmark criterion 6, part met: single-colour recolourable marks render legibly at 1024 px and at the documented 16 px floor, counter open in both, but no artefact is designated a Mono appearance layer.

**The fix.** Closed 26 August 2026. icon-apple-1024-mono.svg is designated the Mono appearance, carries no ground, and is refused by check_transparent_layer if one is ever baked in.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/app-icons` — change log 8 Jun 2026; read 26 Aug 2026

---

## Store assets

### `G-ICON-6` — No Play Store icon

**Blocker** · Google · closed

**What is required.** 512×512 px, 32-bit PNG, sRGB, maximum 1024 KB, full square. Mandatory to publish a listing.

**What is here.** Nothing of that size or purpose exists.

**The fix.** Closed 26 August 2026. 512 x 512, 32-bit PNG with a fully opaque alpha band, sRGB declared, 13,037 bytes against Google's 1,024,000 limit, and every pixel outside Play's 30 per cent corner arc is measured as ground.

**Sources.**

- `developer.android.com/distribute/google-play/resources/icon-design-specifications` — page updated 15 Jun 2026; read 26 Aug 2026
- `support.google.com/googleplay/android-developer/answer/9866151` — no date published; read 26 Aug 2026

### `G-STORE-1` — No feature graphic

**Blocker** · Google · closed

**What is required.** 1024×500 px, JPEG or 24-bit PNG, no alpha. "You must provide a feature graphic to publish your store listing." It must not contain device images, screenshots, or small text illegible when scaled down, and must not resemble an advertisement.

**What is here.** No file of that dimension exists and the term appears nowhere in the repository.

**The fix.** Closed 26 August 2026. 1024 x 500, 24-bit, no alpha band, sRGB declared. It carries the mark, the name and one line — no device image, no screenshot, and no small text, per Play_Feature_Graphic.

**Sources.**

- `support.google.com/googleplay/android-developer/answer/9866151` — no date published; read 26 Aug 2026
- `developer.android.com/docs/quality-guidelines/core-app-quality` — page updated 21 Aug 2026; read 26 Aug 2026

### `G-STORE-2` — No store screenshots, and none can honestly be made yet

**Blocker** · Both · open

**What is required.** Google: at least two across device types, mandatory to publish. Apple: iPhone 6.9 inch and iPad 13 inch, 1 to 10 per device type, no alpha channels. Apple additionally forbids screenshots that show only title art, a login page or a splash screen.

**What is here.** No screenshot assets exist. No Aninda Studio app exists either, so there is nothing truthful to photograph.

**The fix.** Part met 26 August 2026. Correctly sized frames exist for iPhone 6.9 inch, iPad 13 inch and Android phone, drawn with a 45-degree hatch and labelled so they could not be mistaken for a capture, and each names the file that should replace it. A read-only --check-captures mode measures the owner's own screenshots. What cannot be closed without an app is the screenshots themselves.

**Sources.**

- `developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications` — read 26 Aug 2026
- `developer.apple.com/app-store/review/guidelines/` — App Review Guideline 2.3.3; read 26 Aug 2026
- `support.google.com/googleplay/android-developer/answer/9866151` — no date published; read 26 Aug 2026

### `G-STORE-3` — No raster declares its colour space

**Minor** · Both · closed

**What is required.** Play requires sRGB for the store icon. Apple supports sRGB, Gray Gamma 2.2 and Display P3.

**What is here.** Benchmark criterion 7, scored 19 August 2026: no P3 asset exists anywhere, but none of the 19 exported rasters carries an embedded profile, so sRGB is implicit rather than declared.

**The fix.** Closed 26 August 2026 for the store packages: every raster written by 14_delivery/build.py carries an sRGB chunk, read back off the file by guard_srgb_declared. The 20 rasters in 10_assets still carry none, so criterion 7 is closed for the store assets and open for the web set.

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

**Blocker** · Google · closed

**What is required.** Material 3 cannot construct a ColorScheme without onPrimary, and every on-role and on-container role has the same requirement. The Compose primary constructor takes 48 named parameters and has no defaults.

**What is here.** 08_components/src/components.css:225 paints .as-btn--primary with background-color: var(--as-accent) and color: var(--as-surface-lowest), and 08_components/check.py already measures that composited pair in a real browser at rest, hover and active. So the pair is proven. What is missing is the name: no token carries it, so nothing downstream can reference it. The Figma plugin's own receipt records the consequence — it draws outlined rather than filled buttons "because no 'on accent' text colour is defined".

**The fix.** Closed 26 August 2026. color.accent.on is emitted as --as-accent-on in all four themes. No colour was invented: the value is surface.lowest, which components.css was already using. What is new is the name and the proof — it is measured as ink against EVERY fill that carries it (accent, accent-hover and danger) and the published figure is the worst of those. In the dark themes the hardest ground turned out to be danger rather than accent, so a role proven only against the accent would have published 6.2931 instead of the true worst of 5.6640. The Figma library now draws filled buttons, which is what it recorded the missing role as the reason for not doing.

**Sources.**

- `m3.material.io/styles/color/roles` — read 26 Aug 2026 through a browser

### `G-COLOUR-2` — No Material 3 role mapping exists

**Major** · Google · closed

**What is required.** 26 documented colour roles in six groups, plus add-on roles; 48 parameters on the Compose constructor.

**What is here.** 18 semantic colours per theme: 7 surfaces plus ink, ink-muted, line, accent, accent-edge, accent-hover, focus-ring, success, warning, danger and info.

**The fix.** Closed 26 August 2026. 15_native/material3.py derives all 48 parameters of androidx.compose.material3.ColorScheme's PRIMARY constructor for each of the four themes, and every emitted value is proven to be bit-identical to a semantic role, a tonal surface, or a step of one of the six committed ramps — a value matching none of those stops the build. The primary constructor is used rather than lightColorScheme() precisely because the latter defaults every parameter to Material's baseline purple, so a forgotten role would ship an unmeasured colour in silence. 23 pairs a Material component would break on if they were one colour are gated, along with a floor on distinct colours per theme; the four schemes carry 25 to 27.

**Sources.**

- `m3.material.io/styles/color/roles` — read 26 Aug 2026 through a browser

### `G-COLOUR-3` — Material needs secondary and tertiary groups; the brand premise forbids a second expressive colour

**Major** · Google · closed

**What is required.** Material components reference secondary and tertiary roles, so those roles must exist.

**What is here.** 05_colour/directions/estuary.json states the premise: "the warmth coming from the paper rather than from a second expressive colour." Two brand families exist, ground and accent, and no third hue.

**The fix.** Closed 26 August 2026. Secondary is filled from the ground family and tertiary from the info family. Every Material role exists and no new hue entered the brand, so the premise in estuary.json holds as written. Material Theme Builder would have derived a tertiary by rotating the hue about 60 degrees; that is a brand decision and no measurement makes it one a generator may take. The consequence — an Aninda scheme carries less hue variety than a stock Material one — is recorded in material3.roles.json rather than hidden.

**Sources.**

- `m3.material.io/styles/color/roles` — read 26 Aug 2026 through a browser

---

## Reaching a native app

### `G-NATIVE-1` — Tokens reach no Apple or Android surface

**Major** · Both · closed

**What is required.** Apple: "When you need a custom color, add a Color Set asset to your app's asset catalog in Xcode, and specify the bright and dim variants… Avoid using hard-coded color values or colors that don't adapt." Android core app quality requires app content to support both light and dark themes (Theme_Support). Neither is reachable from a stylesheet.

**What is here.** Tokens emit CSS, DTCG JSON, TypeScript and Python. There is no Swift, Kotlin, Xcode or Gradle file in the repository; benchmark criterion 23 records this in writing. The three platform target tokens, 28, 44 and 48 px, are cited figures rather than outputs.

**The fix.** Closed 26 August 2026. 15_native/ emits a Swift package and a Kotlin token layer, both framework-free by design, which is what lets a compiler run on them: the Swift package builds and its tests pass under Swift 6.3.3, and the Kotlin compiles under kotlinc 2.4.10. Stronger than either compile, because a wrong hex is valid Swift: all 152 emitted colour values are read back out of the generated text and re-derived from the DTCG token they came from, each RGB component included. The Bangla ramp ships as values-bn/dimens.xml, applied by Android's own locale mechanism, with the caption size clamped to the measured 12 sp floor.

**Sources.**

- `developer.apple.com/design/human-interface-guidelines/dark-mode` — change log 6 Aug 2024; read 26 Aug 2026
- `developer.android.com/docs/quality-guidelines/core-app-quality` — page updated 21 Aug 2026; read 26 Aug 2026

### `G-NATIVE-2` — No component maps to either platform

**Major** · Both · closed

**What is required.** Apple gives default and minimum control sizes per platform — 44×44 pt default and 28×28 pt minimum on iOS and iPadOS — and asks for roughly 12 pt of padding around bezelled elements and 24 pt around unbezelled ones. Android core app quality requires touch targets of at least 48 dp (Touch_Target_Size), 3:1 contrast for large text and graphics and 4.5:1 for small text (Visual_Contrast), and a content description on every element that is not a TextView (Content_Description). A stylesheet can satisfy none of these on either platform.

**What is here.** 30 cards, HTML and CSS only: 1,109 lines and 87 class blocks in 08_components/src/components.css. No SwiftUI, no Compose, no Material role names, no Cupertino equivalents.

**The fix.** Closed 27 August 2026 for the component layer. 16 SwiftUI components are authored against the CSS reference and compile: the package builds and its tests pass under Swift 6.3.3, and a gate refuses any authored file carrying a literal colour or a literal size — the native analogue of the stylesheet guard, proven in both directions by planting a literal and watching it fail. Android takes the idiomatic route instead of a parallel set: Material's own components read colour, type and shape from the theme, so AnindaTheme supplies a ColorScheme built with the PRIMARY constructor and every Material component is themed at once. Reimplementing Compose's Button would discard the ripple, the state layers, the touch-target expansion and the accessibility it already has. Two things remain: the eight patterns are not implemented, and the components are compiled for macOS here and for the other four Apple platforms only by CI, because this machine has one SDK.

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

**Minor** · This kit's own record · closed

**What is required.** One name for one thing.

**What is here.** 03_directions/build.py names Estuary's type as Archivo, Noto Sans Bengali and JetBrains Mono. The file is flagged as one-off exploration and sits outside the build chain, but it still generates COMPARE.html and COMPARE.pdf.

**The fix.** Closed 27 August 2026 by removing the exploration entirely. The folder held a fourth answer to the typeface question — Archivo, Noto Sans Bengali and JetBrains Mono for Estuary — plus every rejected direction's colours and hand-typed Bangla, and it was outside the rebuild chain, so nothing regenerated it and no gate compared it to anything. Owner's decision: moved to Trash rather than corrected, because a record that contradicts what shipped is worse than no record, and the reason the palette was chosen over three alternatives is written down in 05_colour/directions/natural.json's own premise and supersedes block. Its NOT_IN_CHAIN entry in scripts/readme.py went in the same commit, because that guard raises on an entry naming a file that is not there.

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

