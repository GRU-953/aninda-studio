// Hand-authored. 15_native/build.py reads, gates and compiles this file; it never
// writes it. The values it uses all come from AnindaTokens, which IS generated.
//
// WHY THIS TARGET EXISTS
// ======================
// AnindaTokens imports nothing, which is what lets a compiler run on it anywhere.
// That also means it cannot mention SwiftUI, so it hands out an AnindaColour —
// a hex and three components — rather than a Color. This target is the one place
// that conversion happens.
//
// Keeping it separate is not tidiness. It is what stops a framework import
// reaching the layer whose gate depends on there being none.

import SwiftUI
import AnindaTokens

public extension Color {
    /// A measured colour, as SwiftUI sees it.
    ///
    /// `.sRGB` explicitly, because that is the space the values were measured in.
    /// Letting SwiftUI infer the space would mean the contrast figures this system
    /// publishes were taken in one space and rendered in another.
    init(_ c: AnindaColour) {
        self.init(.sRGB, red: c.red, green: c.green, blue: c.blue, opacity: 1)
    }
}

/// Which theme a view tree is drawn in.
///
/// This is an explicit environment value rather than a read of `colorScheme`,
/// because the system has FOUR themes and `colorScheme` knows two. A high-contrast
/// theme is not a dark theme, and asking the wrong question returns a plausible
/// wrong answer.
public struct AnindaThemeKey: EnvironmentKey {
    public static let defaultValue: AnindaTheme = .light
}

public extension EnvironmentValues {
    var anindaTheme: AnindaTheme {
        get { self[AnindaThemeKey.self] }
        set { self[AnindaThemeKey.self] = newValue }
    }
}

/// The palette for the current theme, resolved once per view.
public struct AnindaStyle {
    public let theme: AnindaTheme
    public let palette: AnindaPalette

    public init(_ theme: AnindaTheme) {
        self.theme = theme
        self.palette = AnindaColours.palette(for: theme)
    }

    public var page: Color { Color(palette.surfacePage) }
    public var surface: Color { Color(palette.surfaceLowest) }
    public var surfaceHigh: Color { Color(palette.surfaceHigh) }
    public var ink: Color { Color(palette.ink) }
    public var inkMuted: Color { Color(palette.inkMuted) }
    public var line: Color { Color(palette.line) }
    public var accent: Color { Color(palette.accent) }
    public var accentEdge: Color { Color(palette.accentEdge) }
    public var accentHover: Color { Color(palette.accentHover) }
    public var onAccent: Color { Color(palette.accentOn) }
    public var focusRing: Color { Color(palette.focusRing) }
    public var success: Color { Color(palette.success) }
    public var warning: Color { Color(palette.warning) }
    public var danger: Color { Color(palette.danger) }
    public var info: Color { Color(palette.info) }
}

public extension View {
    /// Draw this tree in one of the four themes.
    func anindaTheme(_ theme: AnindaTheme) -> some View {
        environment(\.anindaTheme, theme)
    }
}

/// The type scale, as SwiftUI fonts.
///
/// `relativeTo:` is what gives a custom face real Dynamic Type scaling. Without it
/// a custom font is a fixed size and stops responding to the reader's own setting,
/// which is the single most common way a design system breaks accessibility on
/// Apple platforms while looking correct in a screenshot.
public enum AnindaFont {
    public static let family = "Literata"

    public static func scaled(_ points: Double,
                              relativeTo style: Font.TextStyle) -> Font {
        .custom(family, size: points, relativeTo: style)
    }

    public static var body: Font { scaled(AnindaType.body * AnindaType.rootPoints,
                                          relativeTo: .body) }
    public static var caption: Font { scaled(AnindaType.caption * AnindaType.rootPoints,
                                             relativeTo: .caption) }
    public static var lead: Font { scaled(AnindaType.lead * AnindaType.rootPoints,
                                          relativeTo: .title3) }
    public static var h3: Font { scaled(AnindaType.h3 * AnindaType.rootPoints,
                                        relativeTo: .title2) }
    public static var h2: Font { scaled(AnindaType.h2 * AnindaType.rootPoints,
                                        relativeTo: .title) }
    public static var h1: Font { scaled(AnindaType.h1 * AnindaType.rootPoints,
                                        relativeTo: .largeTitle) }

    /// The largest step, for a page that has one thing to say.
    ///
    /// `relativeTo: .largeTitle` like `h1`, because that is the largest text style
    /// Apple defines and there is nothing above it to be relative to. The two
    /// therefore scale together under Dynamic Type, which is correct: they are two
    /// sizes of the same role, not two roles.
    public static var display: Font { scaled(AnindaType.display * AnindaType.rootPoints,
                                             relativeTo: .largeTitle) }
}

/// Motion, and what a reduced-motion preference does to it.
///
/// Under Reduce Motion the durations do NOT fall to zero. Removing a transition is
/// not the same as reducing motion: it replaces a smooth change with a jump, which
/// is a harsher change than the one it was meant to soften. They collapse to a
/// single frame's worth instead, so a colour still cross-fades and nothing moves.
public enum AnindaAnimation {
    public static func colour(reduceMotion: Bool) -> Animation {
        .easeInOut(duration: reduceMotion ? 0.001
                   : AnindaMotion.colourMilliseconds / 1000)
    }

    public static func move(reduceMotion: Bool) -> Animation {
        .easeInOut(duration: reduceMotion ? 0.001
                   : AnindaMotion.moveMilliseconds / 1000)
    }
}

public extension View {
    /// `onHover` where a pointer exists, and nothing where one does not.
    ///
    /// `onHover(perform:)` is unavailable — not deprecated, unavailable — on
    /// watchOS and tvOS, so calling it unguarded refuses to compile for two of the
    /// five platforms this package declares.
    ///
    /// It lives here rather than in each component because three components called
    /// it bare and two others had each written their own private copy of this
    /// guard under a different name. A rule that has to be remembered per file is a
    /// rule that will be forgotten in one.
    ///
    /// Hover is a pointer state. A platform without a pointer loses nothing by not
    /// having it, because no component in this system carries meaning in a hover
    /// fill alone — the state is always also a weight, a marker or a trait.
    @ViewBuilder
    func anindaHover(_ action: @escaping (Bool) -> Void) -> some View {
        #if os(watchOS) || os(tvOS)
        self
        #else
        onHover(perform: action)
        #endif
    }
}
