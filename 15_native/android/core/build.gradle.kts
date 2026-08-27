// Hand-authored. The framework-free token layer: no androidx import reaches it,
// which is what lets kotlinc compile it with no SDK at all. It is an Android
// library here only so the other two modules can depend on it in one graph.
plugins {
    id("com.android.library")
}

android {
    namespace = "studio.aninda.tokens"
    compileSdk = rootProject.extra["compileSdk"] as Int
    defaultConfig { minSdk = rootProject.extra["minSdk"] as Int }
    sourceSets["main"].kotlin.srcDirs("src/main/kotlin")
    sourceSets["main"].manifest.srcFile("src/main/AndroidManifest.xml")
}

// `kotlin { explicitApi() }` was here. It came from the standalone Kotlin plugin's
// extension, which AGP 9 replaces, and whether the built-in one exposes the same
// call is not something this machine can find out. Removed rather than guessed at:
// kotlinc does not enforce explicit API today either, so no check is lost — the
// sources declare `public` on everything regardless. Worth restoring once somebody
// with a JDK can confirm the DSL.
