// swift-tools-version: 5.9
// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
import PackageDescription

let package = Package(
    name: "AnindaTokens",
    platforms: [.iOS(.v17), .macOS(.v14), .watchOS(.v10), .tvOS(.v17), .visionOS(.v1)],
    products: [
        .library(name: "AnindaTokens", targets: ["AnindaTokens"]),
    ],
    targets: [
        // Framework-free on purpose. It imports nothing, so `swift build` and
        // `swiftc -typecheck` both compile it anywhere Swift runs — which is what
        // makes the gate on it a real one.
        .target(name: "AnindaTokens"),
        .testTarget(name: "AnindaTokensTests", dependencies: ["AnindaTokens"]),
    ]
)
