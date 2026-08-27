// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// WHY THIS EXISTS
// ===============
// The Compose sources next to this file were compiled against a DECLARED SURFACE —
// twelve files of hand-typed androidx signatures under compose/stubs — because the
// Android SDK is not installed on the machine this system is developed on. That
// surface proved the Kotlin parsed, that names and arities were self-consistent,
// and that no Material role had been forgotten. It did not prove the code compiles
// against androidx.
//
// It also turned out to be error-prone in a measurable way: of roughly thirteen
// declarations added on 27 August 2026 to carry the eight patterns, TWO were wrong,
// and one of them REJECTED valid code — `Arrangement.spacedBy` returned a
// horizontal-only type where androidx returns one implementing both. A stub that
// refuses correct code is as much a fault as one that accepts incorrect code.
//
// ubuntu-24.04 carries the Android SDK and Gradle preinstalled, so the real compile
// is available in CI and nowhere else. This project is what makes it possible.
//
// WHAT IT COSTS, STATED HERE RATHER THAN DISCOVERED
// ================================================
// A Gradle resolve TOUCHES THE NETWORK. Every other build script in this
// repository is hermetic, and 01_research/BENCHMARK.md criterion 25 says so in
// those words. That property changes with this file, and the change is bounded
// three ways: every version below is pinned with its channel, gradle/
// verification-metadata.xml carries a sha256 per artefact so a substituted jar
// fails the build closed, and the gate runs in CI only — a local run reports the
// refusal and the install command rather than printing ok.

pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    // FAIL_ON_PROJECT_REPOS: a module declaring its own repository would be a
    // second place for an artefact to come from, and the verification metadata
    // would not cover it.
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "aninda-android"

include(":core")
include(":compose")
include(":patterns")
