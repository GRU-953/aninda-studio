<!-- GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it. -->

# What the native layer proves, and what it does not

Written by `15_native/build.py`. This page exists because the gate on this layer is
unusually strong, and a strong gate invites a reader to assume cover it does not
give.

## What was actually run

- no framework import reached the layer that is compiled here
- no deprecated Material role name is used as a token name
- 152 emitted colour values re-derived and matched to their tokens
- 4 file Swift package builds and tests with Apple Swift version 6.3.3 (swiftlang-6.3.3.1.3 clang-2100.1.1.101) — Executed 3 tests, with 0 failures (0 unexpected)
- 2 Kotlin file(s) compile with kotlinc-jvm 2.4.10 (JRE 26.0.2)

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

- **No SwiftUI, no Compose.** Both layers import nothing. That is what lets a
  compiler run on them at all: SwiftUI is an Apple-only framework, absent from the
  open-source Swift toolchain on Linux, and Compose needs the Android SDK. A
  framework layer would carry a weaker gate, and mixing the two would let this
  page's strong claim cover code it never tested.
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
