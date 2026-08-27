// Hand-authored. The eight page compositions, compiled against REAL androidx.
plugins {
    id("com.android.library")
    id("org.jetbrains.kotlin.android")
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

kotlin { explicitApi() }

dependencies {
    implementation(project(":core"))
    implementation(project(":compose"))
    val bom = platform("androidx.compose:compose-bom:${rootProject.extra["composeBom"]}")
    implementation(bom)
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.foundation:foundation")
}
