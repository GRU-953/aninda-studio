// swift-tools-version: 5.9
// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
import PackageDescription

let package = Package(
    name: "AnindaTokens",
    platforms: [.iOS(.v17), .macOS(.v14), .watchOS(.v10), .tvOS(.v17), .visionOS(.v1)],
    products: [
        .library(name: "AnindaTokens", targets: ["AnindaTokens"]),
        .library(name: "AnindaTokensUI", targets: ["AnindaTokensUI"]),
        .library(name: "AnindaComponents", targets: ["AnindaComponents"]),
    ],
    targets: [
        // GENERATED, and framework-free on purpose. It imports nothing, so it
        // compiles anywhere Swift runs — which is what makes the gate on it real.
        .target(name: "AnindaTokens"),

        // AUTHORED from here down. These import SwiftUI, so they compile only
        // where Apple's SDKs are: on a Mac, and on the macos-15 runner. They are
        // kept in separate targets so the framework-free claim above stays true of
        // the target it is made about.
        .target(name: "AnindaTokensUI", dependencies: ["AnindaTokens"]),
        .target(name: "AnindaComponents",
                dependencies: ["AnindaTokens", "AnindaTokensUI"]),
        .target(name: "AnindaExamples",
                dependencies: ["AnindaTokens", "AnindaTokensUI",
                               "AnindaComponents"]),

        .testTarget(name: "AnindaTokensTests", dependencies: ["AnindaTokens"]),
    ]
)
