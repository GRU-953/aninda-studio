// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.

/// Every colour this system measured, for all four themes.
///
/// This file imports nothing. That is deliberate: it means `swiftc
/// -typecheck` compiles it, so the values are proven to build rather than
/// asserted to. The SwiftUI bridge sits in AnindaTokensUI, where no such
/// proof is possible on a machine without Apple's SDKs.
///
/// Components are 0...1 sRGB, derived from the hex rather than typed
/// beside it, so the two cannot disagree.

public struct AnindaColour: Sendable, Equatable {
    public let hex: String
    public let red: Double
    public let green: Double
    public let blue: Double

    public init(_ hex: String, _ r: Double, _ g: Double, _ b: Double) {
        self.hex = hex; self.red = r; self.green = g; self.blue = b
    }
}

public enum AnindaTheme: String, Sendable, CaseIterable {
    case light = "light"
    case dark = "dark"
    case highContrastLight = "hc-light"
    case highContrastDark = "hc-dark"
}

public struct AnindaPalette: Sendable {
    public let accent: AnindaColour
    public let accentEdge: AnindaColour
    public let accentHover: AnindaColour
    public let accentOn: AnindaColour
    public let danger: AnindaColour
    public let focusRing: AnindaColour
    public let info: AnindaColour
    public let ink: AnindaColour
    public let inkMuted: AnindaColour
    public let line: AnindaColour
    public let success: AnindaColour
    public let surfaceBase: AnindaColour
    public let surfaceBright: AnindaColour
    public let surfaceDim: AnindaColour
    public let surfaceHigh: AnindaColour
    public let surfaceHighest: AnindaColour
    public let surfaceLow: AnindaColour
    public let surfaceLowest: AnindaColour
    public let surfacePage: AnindaColour
    public let warning: AnindaColour
}

public enum AnindaColours {
    /// The light theme.
    public static let light = AnindaPalette(
        accent: AnindaColour("#224959", 0.133333, 0.286275, 0.349020),
        accentEdge: AnindaColour("#577D8D", 0.341176, 0.490196, 0.552941),
        accentHover: AnindaColour("#1B2D35", 0.105882, 0.176471, 0.207843),
        accentOn: AnindaColour("#FCFBFB", 0.988235, 0.984314, 0.984314),
        danger: AnindaColour("#A14F39", 0.631373, 0.309804, 0.223529),
        focusRing: AnindaColour("#577D8D", 0.341176, 0.490196, 0.552941),
        info: AnindaColour("#224959", 0.133333, 0.286275, 0.349020),
        ink: AnindaColour("#000000", 0.000000, 0.000000, 0.000000),
        inkMuted: AnindaColour("#605C59", 0.376471, 0.360784, 0.349020),
        line: AnindaColour("#84807C", 0.517647, 0.501961, 0.486275),
        success: AnindaColour("#2C5A3A", 0.172549, 0.352941, 0.227451),
        surfaceBase: AnindaColour("#F8F7F7", 0.972549, 0.968627, 0.968627),
        surfaceBright: AnindaColour("#FFFFFF", 1.000000, 1.000000, 1.000000),
        surfaceDim: AnindaColour("#F1F1F0", 0.945098, 0.945098, 0.941176),
        surfaceHigh: AnindaColour("#F5F5F4", 0.960784, 0.960784, 0.956863),
        surfaceHighest: AnindaColour("#F4F3F3", 0.956863, 0.952941, 0.952941),
        surfaceLow: AnindaColour("#F9F9F8", 0.976471, 0.976471, 0.972549),
        surfaceLowest: AnindaColour("#FCFBFB", 0.988235, 0.984314, 0.984314),
        surfacePage: AnindaColour("#FFFFFF", 1.000000, 1.000000, 1.000000),
        warning: AnindaColour("#464341", 0.274510, 0.262745, 0.254902)
    )

    /// The dark theme.
    public static let dark = AnindaPalette(
        accent: AnindaColour("#6F98AA", 0.435294, 0.596078, 0.666667),
        accentEdge: AnindaColour("#577D8D", 0.341176, 0.490196, 0.552941),
        accentHover: AnindaColour("#8BB2C3", 0.545098, 0.698039, 0.764706),
        accentOn: AnindaColour("#060505", 0.023529, 0.019608, 0.019608),
        danger: AnindaColour("#CC765E", 0.800000, 0.462745, 0.368627),
        focusRing: AnindaColour("#577D8D", 0.341176, 0.490196, 0.552941),
        info: AnindaColour("#6F98AA", 0.435294, 0.596078, 0.666667),
        ink: AnindaColour("#FFFFFF", 1.000000, 1.000000, 1.000000),
        inkMuted: AnindaColour("#84807C", 0.517647, 0.501961, 0.486275),
        line: AnindaColour("#84807C", 0.517647, 0.501961, 0.486275),
        success: AnindaColour("#6E9E7A", 0.431373, 0.619608, 0.478431),
        surfaceBase: AnindaColour("#0E0D0D", 0.054902, 0.050980, 0.050980),
        surfaceBright: AnindaColour("#111110", 0.066667, 0.066667, 0.062745),
        surfaceDim: AnindaColour("#000000", 0.000000, 0.000000, 0.000000),
        surfaceHigh: AnindaColour("#10100F", 0.062745, 0.062745, 0.058824),
        surfaceHighest: AnindaColour("#111010", 0.066667, 0.062745, 0.062745),
        surfaceLow: AnindaColour("#0A0A09", 0.039216, 0.039216, 0.035294),
        surfaceLowest: AnindaColour("#060505", 0.023529, 0.019608, 0.019608),
        surfacePage: AnindaColour("#000000", 0.000000, 0.000000, 0.000000),
        warning: AnindaColour("#94908C", 0.580392, 0.564706, 0.549020)
    )

    /// The hc-light theme.
    public static let highContrastLight = AnindaPalette(
        accent: AnindaColour("#224959", 0.133333, 0.286275, 0.349020),
        accentEdge: AnindaColour("#426271", 0.258824, 0.384314, 0.443137),
        accentHover: AnindaColour("#1B2D35", 0.105882, 0.176471, 0.207843),
        accentOn: AnindaColour("#FCFBFB", 0.988235, 0.984314, 0.984314),
        danger: AnindaColour("#693223", 0.411765, 0.196078, 0.137255),
        focusRing: AnindaColour("#426271", 0.258824, 0.384314, 0.443137),
        info: AnindaColour("#224959", 0.133333, 0.286275, 0.349020),
        ink: AnindaColour("#000000", 0.000000, 0.000000, 0.000000),
        inkMuted: AnindaColour("#464341", 0.274510, 0.262745, 0.254902),
        line: AnindaColour("#605C59", 0.376471, 0.360784, 0.349020),
        success: AnindaColour("#1B3020", 0.105882, 0.188235, 0.125490),
        surfaceBase: AnindaColour("#F4F3F3", 0.956863, 0.952941, 0.952941),
        surfaceBright: AnindaColour("#FFFFFF", 1.000000, 1.000000, 1.000000),
        surfaceDim: AnindaColour("#E7E7E7", 0.905882, 0.905882, 0.905882),
        surfaceHigh: AnindaColour("#EFEFEF", 0.937255, 0.937255, 0.937255),
        surfaceHighest: AnindaColour("#ECEBEB", 0.925490, 0.921569, 0.921569),
        surfaceLow: AnindaColour("#F7F7F7", 0.968627, 0.968627, 0.968627),
        surfaceLowest: AnindaColour("#FCFBFB", 0.988235, 0.984314, 0.984314),
        surfacePage: AnindaColour("#FFFFFF", 1.000000, 1.000000, 1.000000),
        warning: AnindaColour("#2C2A28", 0.172549, 0.164706, 0.156863)
    )

    /// The hc-dark theme.
    public static let highContrastDark = AnindaPalette(
        accent: AnindaColour("#8BB2C3", 0.545098, 0.698039, 0.764706),
        accentEdge: AnindaColour("#6F98AA", 0.435294, 0.596078, 0.666667),
        accentHover: AnindaColour("#AACBD9", 0.666667, 0.796078, 0.850980),
        accentOn: AnindaColour("#060505", 0.023529, 0.019608, 0.019608),
        danger: AnindaColour("#E6927B", 0.901961, 0.572549, 0.482353),
        focusRing: AnindaColour("#6F98AA", 0.435294, 0.596078, 0.666667),
        info: AnindaColour("#8BB2C3", 0.545098, 0.698039, 0.764706),
        ink: AnindaColour("#FFFFFF", 1.000000, 1.000000, 1.000000),
        inkMuted: AnindaColour("#AEAAA6", 0.682353, 0.666667, 0.650980),
        line: AnindaColour("#84807C", 0.517647, 0.501961, 0.486275),
        success: AnindaColour("#8AB895", 0.541176, 0.721569, 0.584314),
        surfaceBase: AnindaColour("#0F0E0E", 0.058824, 0.054902, 0.054902),
        surfaceBright: AnindaColour("#151515", 0.082353, 0.082353, 0.082353),
        surfaceDim: AnindaColour("#000000", 0.000000, 0.000000, 0.000000),
        surfaceHigh: AnindaColour("#10100F", 0.062745, 0.062745, 0.058824),
        surfaceHighest: AnindaColour("#131212", 0.074510, 0.070588, 0.070588),
        surfaceLow: AnindaColour("#0A0A09", 0.039216, 0.039216, 0.035294),
        surfaceLowest: AnindaColour("#060505", 0.023529, 0.019608, 0.019608),
        surfacePage: AnindaColour("#000000", 0.000000, 0.000000, 0.000000),
        warning: AnindaColour("#C7C4C1", 0.780392, 0.768627, 0.756863)
    )

    public static func palette(for theme: AnindaTheme) -> AnindaPalette {
        switch theme {
        case .light: return light
        case .dark: return dark
        case .highContrastLight: return highContrastLight
        case .highContrastDark: return highContrastDark
        }
    }
}
