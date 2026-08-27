// Hand-authored. The framework-free token layer: no androidx import reaches it,
// which is what lets kotlinc compile it with no SDK at all. It is an Android
// library here only so the other two modules can depend on it in one graph.
plugins {
    id("com.android.library")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "studio.aninda.tokens"
    compileSdk = rootProject.extra["compileSdk"] as Int
    defaultConfig { minSdk = rootProject.extra["minSdk"] as Int }
    sourceSets["main"].kotlin.srcDirs("src/main/kotlin")
    sourceSets["main"].manifest.srcFile("src/main/AndroidManifest.xml")
}

kotlin { explicitApi() }
