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
        // The patterns are a product for a MECHANICAL reason, not a change of
        // heart about coupling. xcodebuild generates schemes from products, so a
        // target that is not one can only ever be compiled for whatever platform
        // `swift build` happens to run on — and eight page compositions are
        // exactly the code that breaks on availability. Without this line the
        // patterns would be checked for macOS and for nothing else.
        //
        // A product does not couple anything: a caller depending on
        // AnindaComponents never resolves AnindaExamples. The opt-in the target
        // boundary expresses is unchanged.
        .library(name: "AnindaExamples", targets: ["AnindaExamples"]),
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
