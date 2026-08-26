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
    public let warning: AnindaColour
}

public enum AnindaColours {
    /// The light theme.
    public static let light = AnindaPalette(
        accent: AnindaColour("#126974", 0.070588, 0.411765, 0.454902),
        accentEdge: AnindaColour("#278492", 0.152941, 0.517647, 0.572549),
        accentHover: AnindaColour("#054D56", 0.019608, 0.301961, 0.337255),
        accentOn: AnindaColour("#FDFFFE", 0.992157, 1.000000, 0.996078),
        danger: AnindaColour("#9B3728", 0.607843, 0.215686, 0.156863),
        focusRing: AnindaColour("#278492", 0.152941, 0.517647, 0.572549),
        info: AnindaColour("#316189", 0.192157, 0.380392, 0.537255),
        ink: AnindaColour("#0D1A17", 0.050980, 0.101961, 0.090196),
        inkMuted: AnindaColour("#41655C", 0.254902, 0.396078, 0.360784),
        line: AnindaColour("#578076", 0.341176, 0.501961, 0.462745),
        success: AnindaColour("#2D6C42", 0.176471, 0.423529, 0.258824),
        surfaceBase: AnindaColour("#F8FAF9", 0.972549, 0.980392, 0.976471),
        surfaceBright: AnindaColour("#FFFFFF", 1.000000, 1.000000, 1.000000),
        surfaceDim: AnindaColour("#F1F2F2", 0.945098, 0.949020, 0.949020),
        surfaceHigh: AnindaColour("#F6F7F7", 0.964706, 0.968627, 0.968627),
        surfaceHighest: AnindaColour("#F3F5F4", 0.952941, 0.960784, 0.956863),
        surfaceLow: AnindaColour("#FBFCFC", 0.984314, 0.988235, 0.988235),
        surfaceLowest: AnindaColour("#FDFFFE", 0.992157, 1.000000, 0.996078),
        warning: AnindaColour("#7C5414", 0.486275, 0.329412, 0.078431)
    )

    /// The dark theme.
    public static let dark = AnindaPalette(
        accent: AnindaColour("#42A0AE", 0.258824, 0.627451, 0.682353),
        accentEdge: AnindaColour("#278492", 0.152941, 0.517647, 0.572549),
        accentHover: AnindaColour("#65BAC7", 0.396078, 0.729412, 0.780392),
        accentOn: AnindaColour("#0B0C0B", 0.043137, 0.047059, 0.043137),
        danger: AnindaColour("#E16551", 0.882353, 0.396078, 0.317647),
        focusRing: AnindaColour("#278492", 0.152941, 0.517647, 0.572549),
        info: AnindaColour("#5C96C8", 0.360784, 0.588235, 0.784314),
        ink: AnindaColour("#F2F9F7", 0.949020, 0.976471, 0.968627),
        inkMuted: AnindaColour("#6F9B90", 0.435294, 0.607843, 0.564706),
        line: AnindaColour("#578076", 0.341176, 0.501961, 0.462745),
        success: AnindaColour("#59A46F", 0.349020, 0.643137, 0.435294),
        surfaceBase: AnindaColour("#111212", 0.066667, 0.070588, 0.070588),
        surfaceBright: AnindaColour("#121413", 0.070588, 0.078431, 0.074510),
        surfaceDim: AnindaColour("#060707", 0.023529, 0.027451, 0.027451),
        surfaceHigh: AnindaColour("#111312", 0.066667, 0.074510, 0.070588),
        surfaceHighest: AnindaColour("#121313", 0.070588, 0.074510, 0.074510),
        surfaceLow: AnindaColour("#0E100F", 0.054902, 0.062745, 0.058824),
        surfaceLowest: AnindaColour("#0B0C0B", 0.043137, 0.047059, 0.043137),
        warning: AnindaColour("#B8863E", 0.721569, 0.525490, 0.243137)
    )

    /// The hc-light theme.
    public static let highContrastLight = AnindaPalette(
        accent: AnindaColour("#054D56", 0.019608, 0.301961, 0.337255),
        accentEdge: AnindaColour("#126974", 0.070588, 0.411765, 0.454902),
        accentHover: AnindaColour("#013137", 0.003922, 0.192157, 0.215686),
        accentOn: AnindaColour("#FCFDFC", 0.988235, 0.992157, 0.988235),
        danger: AnindaColour("#752519", 0.458824, 0.145098, 0.098039),
        focusRing: AnindaColour("#126974", 0.070588, 0.411765, 0.454902),
        info: AnindaColour("#214767", 0.129412, 0.278431, 0.403922),
        ink: AnindaColour("#0D1A17", 0.050980, 0.101961, 0.090196),
        inkMuted: AnindaColour("#2E4B43", 0.180392, 0.294118, 0.262745),
        line: AnindaColour("#41655C", 0.254902, 0.396078, 0.360784),
        success: AnindaColour("#1D502E", 0.113725, 0.313725, 0.180392),
        surfaceBase: AnindaColour("#F7F8F7", 0.968627, 0.972549, 0.968627),
        surfaceBright: AnindaColour("#FFFFFF", 1.000000, 1.000000, 1.000000),
        surfaceDim: AnindaColour("#F1F1F1", 0.945098, 0.945098, 0.945098),
        surfaceHigh: AnindaColour("#F5F5F5", 0.960784, 0.960784, 0.960784),
        surfaceHighest: AnindaColour("#F2F3F2", 0.949020, 0.952941, 0.949020),
        surfaceLow: AnindaColour("#FAFAFA", 0.980392, 0.980392, 0.980392),
        surfaceLowest: AnindaColour("#FCFDFC", 0.988235, 0.992157, 0.988235),
        warning: AnindaColour("#5D3C07", 0.364706, 0.235294, 0.027451)
    )

    /// The hc-dark theme.
    public static let highContrastDark = AnindaPalette(
        accent: AnindaColour("#65BAC7", 0.396078, 0.729412, 0.780392),
        accentEdge: AnindaColour("#42A0AE", 0.258824, 0.627451, 0.682353),
        accentHover: AnindaColour("#8ED2DD", 0.556863, 0.823529, 0.866667),
        accentOn: AnindaColour("#070807", 0.027451, 0.031373, 0.027451),
        danger: AnindaColour("#FB836F", 0.984314, 0.513725, 0.435294),
        focusRing: AnindaColour("#42A0AE", 0.258824, 0.627451, 0.682353),
        info: AnindaColour("#7AB1E1", 0.478431, 0.694118, 0.882353),
        ink: AnindaColour("#F2F9F7", 0.949020, 0.976471, 0.968627),
        inkMuted: AnindaColour("#8BB5AA", 0.545098, 0.709804, 0.666667),
        line: AnindaColour("#6F9B90", 0.435294, 0.607843, 0.564706),
        success: AnindaColour("#77BE8B", 0.466667, 0.745098, 0.545098),
        surfaceBase: AnindaColour("#0E0F0E", 0.054902, 0.058824, 0.054902),
        surfaceBright: AnindaColour("#121212", 0.070588, 0.070588, 0.070588),
        surfaceDim: AnindaColour("#030303", 0.011765, 0.011765, 0.011765),
        surfaceHigh: AnindaColour("#111111", 0.066667, 0.066667, 0.066667),
        surfaceHighest: AnindaColour("#111211", 0.066667, 0.070588, 0.066667),
        surfaceLow: AnindaColour("#0C0C0C", 0.047059, 0.047059, 0.047059),
        surfaceLowest: AnindaColour("#070807", 0.027451, 0.031373, 0.027451),
        warning: AnindaColour("#D2A15F", 0.823529, 0.631373, 0.372549)
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
