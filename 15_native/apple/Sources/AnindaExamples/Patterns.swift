// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// WHY THE PATTERNS LIVE HERE AND NOT IN AnindaComponents
// =====================================================
// The patterns are page compositions rather than components, kept OUTSIDE the
// component library on purpose: shipping opinionated screens inside a design
// system is a different product, and a caller who wants the button should not
// have to take the sign-in page with it.
//
// That paragraph is the placeholder's, moved here verbatim when the patterns were
// written on 27 August 2026. It is the reason this target exists, and it is worth
// more in a file that has code under it than in one that had none.
//
// SwiftPM enforces it: a caller depending on AnindaComponents never resolves this
// target. What a product adds is not coupling but REACH — xcodebuild generates
// schemes from products, so a target that is not one can only ever be compiled for
// the platform `swift build` happens to run on. Eight screens compiled for macOS
// alone would be the four platforms the components are mostly for going unchecked.
//
// WHAT A PATTERN MAY USE
// ======================
// Only the sixteen components, the tokens, and layout. No pattern reaches for a
// colour, a size, or a control the component library does not already carry — if a
// screen needs something new, the component library is where it goes, and the
// screen then uses it like any other caller. That is what keeps these eight
// examples rather than a second, quieter component library.

import SwiftUI
import AnindaTokens
import AnindaTokensUI
import AnindaComponents

/// The eight patterns, by name.
///
/// Here so that a caller who imports this module finds them without reading the
/// directory, and so the set is stated in one place rather than inferred from the
/// files. `scripts/check_patterns.py` holds the same eight and fails if the web,
/// Apple and Android sides ever disagree about which they are.
public enum AnindaPatterns {
    public static let names = [
        "Sign in", "Settings", "Dashboard", "Docs page",
        "Landing", "Pricing", "Not found", "Form with validation",
    ]
}

/// The page every pattern sits on.
///
/// Internal on purpose. It is a convenience for the eight screens below, not a
/// layout primitive this system is offering anyone — a caller who wants a page
/// surface has `AnindaStyle.page` and a `VStack`, which is all this is.
///
/// It states no width. The measure belongs to whatever is presenting the screen,
/// and a fixed point width would be wrong under Dynamic Type anyway: the reader's
/// own text size decides how much fits, and a number chosen here cannot know it.
struct PatternPage<Content: View>: View {
    private let content: () -> Content
    @Environment(\.anindaTheme) private var theme

    init(@ViewBuilder content: @escaping () -> Content) {
        self.content = content
    }

    var body: some View {
        let s = AnindaStyle(theme)
        return ScrollView {
            VStack(alignment: .leading, spacing: AnindaSpace.s4) {
                content()
            }
            .padding(AnindaSpace.s4)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .background(s.page)
    }
}

/// A heading that is announced as one.
///
/// `.accessibilityAddTraits(.isHeader)` is the whole point: a large font is a
/// visual heading and nothing more, and a screen reader moving by heading finds
/// nothing on a screen full of them. The 30 web cards are measured for this; these
/// screens are not measured for it by anything, so it is written by hand and said
/// out loud in LIMITS.md.
struct PatternHeading: View {
    private let text: String
    private let font: Font
    @Environment(\.anindaTheme) private var theme

    init(_ text: String, font: Font = AnindaFont.h2) {
        self.text = text
        self.font = font
    }

    var body: some View {
        Text(text)
            .font(font)
            .foregroundStyle(AnindaStyle(theme).ink)
            .accessibilityAddTraits(.isHeader)
    }
}
