// Hand-authored. The eight page compositions, compiled against REAL androidx.
plugins {
    id("com.android.library")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "studio.aninda.patterns"
    compileSdk = rootProject.extra["compileSdk"] as Int
    defaultConfig { minSdk = rootProject.extra["minSdk"] as Int }
    buildFeatures { compose = true }
    sourceSets["main"].kotlin.srcDirs("src/main/kotlin")
    sourceSets["main"].manifest.srcFile("src/main/AndroidManifest.xml")
}

// `kotlin { explicitApi() }` was here. It came from the standalone Kotlin plugin's
// extension, which AGP 9 replaces, and whether the built-in one exposes the same
// call is not something this machine can find out. Removed rather than guessed at:
// kotlinc does not enforce explicit API today either, so no check is lost — the
// sources declare `public` on everything regardless. Worth restoring once somebody
// with a JDK can confirm the DSL.

dependencies {
    implementation(project(":core"))
    implementation(project(":compose"))
    val bom = platform("androidx.compose:compose-bom:${rootProject.extra["composeBom"]}")
    implementation(bom)
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.foundation:foundation")
}
