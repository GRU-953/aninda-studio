// Hand-authored. The theme and typography, compiled against REAL androidx.
//
// compose/stubs is deliberately NOT in this source set. Those twelve files are the
// declared surface kotlinc uses when the SDK is absent; compiling both would define
// every symbol twice and prove nothing about either.
plugins {
    id("com.android.library")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "studio.aninda.compose"
    compileSdk = rootProject.extra["compileSdk"] as Int
    defaultConfig { minSdk = rootProject.extra["minSdk"] as Int }
    buildFeatures { compose = true }
    sourceSets["main"].kotlin.srcDirs("src/main/kotlin")
    sourceSets["main"].manifest.srcFile("src/main/AndroidManifest.xml")
}

kotlin { explicitApi() }

dependencies {
    implementation(project(":core"))
    val bom = platform("androidx.compose:compose-bom:${rootProject.extra["composeBom"]}")
    implementation(bom)
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.foundation:foundation")
}
