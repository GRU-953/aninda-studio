<!-- GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it. -->

# What the native layer proves, and what it does not

Written by `15_native/build.py`. This page exists because the gate on this layer is
unusually strong, and a strong gate invites a reader to assume cover it does not
give.

## What was actually run

- no framework import reached the 4 files the framework-free claim is made about
- 20 authored source file(s) carry no literal colour and no literal size
- 16 SwiftUI components, one for each component card in 08_components/_cards.json, with nothing orphaned either way
- no deprecated Material role name is used as a token name in the 3 files that define tokens
- 160 emitted colour values re-derived and matched to their tokens
- 22 file Swift package builds and tests with Apple Swift version 6.3.3 (swiftlang-6.3.3.1.3 clang-2100.1.1.101) — Executed 3 tests, with 0 failures (0 unexpected)
- components build for macOS — NOT compiled for iOS, watchOS, tvOS, visionOS, whose SDKs are not installed on this machine. Those platforms are compiled by the macos-15 job in CI and by nothing here
- 2 framework-free Kotlin file(s) compile with kotlinc-jvm 2.4.10 (JRE 26.0.2); 2 authored Compose file(s) compile against the declared surface in compose/stubs, NOT against androidx

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
- **The Compose sources are compiled against a DECLARED SURFACE, not androidx.**
  The Android SDK is not installed. Compiling against `compose/stubs` proves the
  Kotlin parses, that every name and arity is consistent, that the token constants
  exist and are the right type, and — because the stubbed `ColorScheme` takes all
  48 parameters with no defaults — that not one Material role was forgotten. It
  does not prove the code compiles against androidx. A stub can differ from the
  library it imitates, and if it does, this gate passes and a real build fails.
- **No pattern is implemented.** `AnindaExamples` is a placeholder. The eight
  patterns are page compositions rather than components, and they are the part of
  the approved scope that is not done.
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
