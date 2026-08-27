<!-- GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it. -->

# What the native layer proves, and what it does not

Written by `15_native/build.py`. This page exists because the gate on this layer is
unusually strong, and a strong gate invites a reader to assume cover it does not
give.

## What the build asserted

- no framework import reached the 4 files the framework-free claim is made about
- 37 authored source file(s) carry no literal colour and no literal size
- 16 SwiftUI components, one for each component card in 08_components/_cards.json, with nothing orphaned either way
- 8 SwiftUI patterns and 8 Compose patterns, the same 8 names on both, matching the 8 pattern cards in 08_components/_cards.json
- 2 platform-limited API(s) are wrapped only in apple/Sources/AnindaTokensUI/Theme.swift, and every component calls the wrapper rather than the API
- no deprecated Material role name is used as a token name in the 3 files that define tokens
- 160 emitted colour values re-derived and matched to their tokens
- gradle: NOT ASKED FOR — this run did not require it, and no claim is made that the Compose sources build against androidx

The compile record — which compilers ran, at which versions, and which platforms
this machine could build for — is printed by the build and deliberately not
written here. It describes the machine rather than the layer, and it cannot be the
same on two machines: a runner with every Apple SDK installed compiles five
platforms where a development machine compiles one. Committing that figure would
mean this file could never be diffed, or could only be diffed on one computer.

## What a compile proves

The Swift side is built and tested, not merely parsed: `swift build` compiles and
links a real module from a temporary copy of the package, and `swift test` runs the
assertions in it. The Kotlin side is compiled by `kotlinc`. Between them they prove
that names resolve, that types agree, and that the package assembles.

They prove nothing about layout, nothing about whether a target measures 44 pt on a
screen, nothing about focus order, and nothing about what VoiceOver or TalkBack
announce. A compile is not a rendering.

Measured separately, and the only gate here that could catch a value being *wrong*
rather than merely well formed: every emitted colour is read back out of the
generated text and re-derived from the DTCG token it came from. A typo in a hex is
valid Swift and would pass every compiler.

## What is deliberately not here

- **The framework-free claim is about the TOKEN layer, and only that.**
  `AnindaTokens` and the Kotlin core import nothing, which is what lets a compiler
  run on them anywhere. `AnindaTokensUI`, `AnindaComponents` and the Compose theme
  all import a framework on purpose and are kept in separate targets so the claim
  stays true of the target it is made about.
- **The components are compiled for macOS here and for nothing else.** The package
  declares five Apple platforms; this machine has the macOS SDK alone. An API can
  be available on macOS and unavailable on watchOS — `onHover(perform:)` and
  `UIPasteboard` both are, and both reached this package before anything caught
  them. The macos-15 job in CI is the only place the other four are compiled, which
  makes it the one gate here that CI proves and a local run cannot.
- **The Compose sources are compiled against a DECLARED SURFACE, not androidx,
  and that surface got three times bigger on 27 August 2026.** The Android SDK is
  not installed. Compiling against `compose/stubs` proves the Kotlin parses, that
  every name and arity is consistent, that the token constants exist and are the
  right type, and — because the stubbed `ColorScheme` takes all 48 parameters with
  no defaults — that not one Material role was forgotten. It does not prove the
  code compiles against androidx. A stub can differ from the library it imitates,
  and if it does, this gate passes and a real build fails.

  That last sentence now carries more weight than it did. The surface was eight
  files when it declared little beyond `ColorScheme`, whose 48 parameters are READ
  from the derivation and therefore cannot drift. Carrying eight page compositions
  took it to twelve files, and the added declarations — `OutlinedTextField`,
  `Modifier`, the layout scopes — are hand-typed signatures whose fidelity rests on
  somebody having copied them correctly. Two of them were WRONG on the first
  attempt, and the compile caught both: `heading()` was declared as a member where
  androidx has an extension function, and `Arrangement.spacedBy` returned a
  horizontal-only type where androidx returns one that is both. A stub that refuses
  valid code is as much a fault as one that accepts invalid code.

  What bounds it: every stub file names the artifact and version its declarations
  were read from, so a divergence is attributable and dated; and a pattern may use
  only a Material composable corresponding to one of the sixteen component cards,
  which is why there is no icon set, no navigation library and no `LazyColumn`
  here.

  **It is no longer the only check on that code.** A Gradle job on `ubuntu-24.04`
  compiles the Compose theme and the eight patterns against REAL androidx —
  Material 3 from the stable channel, by way of `compose-bom`. The stub is what a
  developer machine without the Android SDK can run; the Gradle gate is what says
  whether the code actually builds. Where the two disagree, the Gradle gate is
  right, and CI is the only place it runs.
- **The Gradle gate touches the network, and this is the only thing here that
  does.** Every other build script in this repository reads the tree and nothing
  else. Resolution is pinned by VERSION and by channel, and the gate runs in CI
  alone — but NOT pinned by content: `gradle/verification-metadata.xml`, a sha256
  per artefact, does not exist yet, because producing it needs a JDK no machine
  this system is developed on has. An artefact republished under a pinned version
  would be taken. That is the same standing as `requirements.txt`, and it is
  written down rather than assumed away.
- **The patterns are compiled for five platforms and laid out for none.** Eight
  screens exist on both native platforms and every one of them compiles, but a
  compile is not a layout. Nothing here has measured a pattern on a screen, and
  watchOS and tvOS get the same composition as a desktop with no compact variant.
  The web card for Docs page is two columns where the Compose screen is one, because
  Compose has no `ViewThatFits` and branching on width needs a dependency this
  module does not carry.
- **The patterns' accessibility is written, not measured.** Headings are marked,
  the pricing cards carry content descriptions, and the validation summary merges
  its descendants so a count is announced as one thing. None of that is verified by
  anything: the thirty web cards are measured in a real browser, and the native
  equivalent does not exist. The SwiftUI validation summary is marked
  `.updatesFrequently`, which tells VoiceOver an element changes and does NOT
  announce the change — a real live region needs an announcement posted when the
  count moves, and that belongs to whatever owns the submit.
- **Type in Compose is Material's slots, and the mono face is missing.**
  `kotlin_tokens()` emits no `AnindaType`, so `Typography.kt` carries fifteen
  literal `sp` figures and a Compose caller cannot ask for the monospace family
  without writing a literal the token guard would refuse. The code sample on the
  Docs page screen is therefore set in the body face. The size guard was extended
  on 27 August 2026 to catch `padding(16.dp)`, which it had never seen — but
  deliberately not `.sp`, because that would fail a file for a gap in the emitter.
- **No rendered measurement.** Every contrast figure the native layer carries was
  computed from the same rounded 8-bit hexes the stylesheet uses, under the same
  worst-case sweep. No native pixel has been read. The browser harness measures
  thirty component cards; the native equivalent does not exist.
- **No Gradle project, and no `.xcodeproj`.** The Kotlin here compiles as plain
  JVM source. Assembling it into an Android library needs the SDK, and that is a
  toolchain this repository deliberately does not carry.

## Known divergences, recorded rather than reconciled

- **Apple's default body size is 17 pt; this system's is 16.** Changing the scale
  to suit one platform would change it for the web too, and the steps of a perfect
  fourth were chosen together. `AnindaType.rootPoints` is what a caller scales from.
- **macOS has no Dynamic Type.** Any Apple surface that needs scaling text has to
  use the iOS, iPadOS, tvOS, visionOS or watchOS route.
- **Android has no contrast qualifier.** `values/` and `values-night/` carry the
  two ordinary themes. The two high-contrast themes are available in the Kotlin
  constants and have no resource configuration to live in, so a View-based consumer
  gets the standard pair only.
- **Material's Bangla figure and this system's are not the same measurement.**
  Material calls Bangla a medium language-height script needing roughly 7 per cent
  taller line heights at the same nominal size. This system's Bangla leading is 1.6
  against Latin's 1.55, which is +3.2 per cent, and the Bangla is also set at
  x0.816 — so its absolute line box is smaller, not larger. Both are published and
  neither confirms the other.
