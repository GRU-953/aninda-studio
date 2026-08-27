// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// EVERY VERSION IS PINNED WITH ITS CHANNEL, which 01_research/BENCHMARK.md
// criterion 23 asks of any Material dependency. Material 3 is taken from the
// STABLE channel: much of Material Expressive lives in 1.5.0-alpha, and an alpha
// is a pre-release channel whose interfaces may change without warning, so this
// system does not build against it.
plugins {
    // No org.jetbrains.kotlin.android. AGP 9.0 carries Kotlin support built in and
    // REFUSES the standalone plugin outright — "no longer required for Kotlin
    // support since AGP 9.0". Kotlin's own version comes from AGP; only the Compose
    // compiler plugin is still applied separately, and it is versioned with the
    // Kotlin AGP ships.
    id("com.android.library") version "9.0.0" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.4.10" apply false
}

// Read by the three module files, so a version is stated once.
extra["compileSdk"] = 36
extra["minSdk"] = 24
extra["composeBom"] = "2026.08.00"
