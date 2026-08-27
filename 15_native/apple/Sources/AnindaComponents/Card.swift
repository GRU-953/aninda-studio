// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-card`, `.as-card--flat`
// and `.as-card--tight`. Every value here comes from AnindaTokens, and the gate
// refuses this file if it carries a literal colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// How much room a card gives its content.
public enum AnindaCardPadding: Sendable {
    /// `.as-card` — 24 pt on every side.
    case regular
    /// `.as-card--tight` — 16 pt, for a card in a dense list or a sidebar.
    case tight
}

/// Whether a card lifts off the page.
public enum AnindaCardElevation: Sendable {
    /// `.as-card` — the float shadow, in the themes that publish one.
    case floating
    /// `.as-card--flat` — border and fill alone.
    case flat
}

/// A bordered container that groups one thought.
///
/// SwiftUI has no card control to wrap, so this is a small `View` rather than a
/// style or a modifier — the rule is to wrap the platform control wherever one
/// exists, and here none does. Nothing in it is interactive and nothing in it
/// steals a gesture, so a card that should be tappable is built by putting a real
/// `Button` inside it, or by wrapping the card in one and applying
/// `AnindaButtonStyle`. That keeps the button trait, keyboard activation, Voice
/// Control and Switch Control that a `.onTapGesture` on a container throws away.
///
/// What this does not handle: the CSS `min-width: 0` has no analogue here, because
/// it exists to stop a flex child refusing to shrink and SwiftUI's layout has no
/// equivalent failure. The CSS `.as-card__foot` is an ordinary `HStack` with
/// `AnindaSpace.s1` spacing and `AnindaSpace.s1` of top padding — the stylesheet's
/// `gap` and `margin-block-start` — and is left to the caller rather than wrapped,
/// since a one-line stack is not worth a type. Its `flex-wrap: wrap` has no
/// one-modifier equivalent, so a foot with more actions than fit needs a layout
/// that wraps rather than an `HStack`.
public struct AnindaCard<Content: View>: View {
    private let padding: AnindaCardPadding
    private let elevation: AnindaCardElevation
    private let content: Content
    @Environment(\.anindaTheme) private var theme

    public init(padding: AnindaCardPadding = .regular,
                elevation: AnindaCardElevation = .floating,
                @ViewBuilder content: () -> Content) {
        self.padding = padding
        self.elevation = elevation
        self.content = content()
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        // The CSS card is a column flex box with a 12 pt gap; a VStack with that
        // spacing is the same arrangement.
        return VStack(alignment: .leading, spacing: AnindaSpace.s2) {
            content
        }
        .foregroundStyle(s.ink)
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(padding == .tight ? AnindaSpace.s3 : AnindaSpace.s4)
        .background(
            RoundedRectangle(cornerRadius: AnindaRadius.card).fill(s.surface)
        )
        .overlay(
            RoundedRectangle(cornerRadius: AnindaRadius.card)
                .strokeBorder(s.line, lineWidth: 1)
        )
        // The border is drawn in every theme, and that is what carries the card's
        // edge where the shadow is switched off. An elevation told by shadow alone
        // would vanish for a reader in high contrast.
        .modifier(AnindaCardShadow(theme: theme, elevation: elevation))
    }
}

/// The float shadow, applied only where the theme publishes one.
///
/// `--as-shadow-float` is `none` in the dark theme and in both high-contrast
/// themes, and only the light theme carries it. Reading the theme rather than
/// always drawing it keeps the four themes matching the stylesheet.
///
/// There is no shadow token in AnindaTokens — the file is generated, and adding
/// one is a change to the generator rather than to a component, so I have not made
/// it here. I wanted the CSS pair `0 1px 2px rgb(0 0 0 / 0.06)` and
/// `0 8px 24px rgb(0 0 0 / 0.08)`. The blur radii map to half their CSS values,
/// because SwiftUI's shadow radius is a standard deviation and CSS's is a blur
/// diameter: 2 becomes 1, and 24 becomes `AnindaSpace.s2`. The colour is `s.ink`
/// at the same opacities rather than pure black, since a literal colour is
/// refused by the gate — in the light theme ink is a near-black and the difference
/// is below what a shadow at 6 and 8 per cent can show.
private struct AnindaCardShadow: ViewModifier {
    let theme: AnindaTheme
    let elevation: AnindaCardElevation

    func body(content: Content) -> some View {
        let s = AnindaStyle(theme)
        let lifted = elevation == .floating && theme == .light
        return content
            .shadow(color: lifted ? s.ink.opacity(0.06) : .clear,
                    radius: lifted ? 1 : 0, x: 0, y: lifted ? 1 : 0)
            .shadow(color: lifted ? s.ink.opacity(0.08) : .clear,
                    radius: lifted ? AnindaSpace.s2 : 0,
                    x: 0, y: lifted ? AnindaSpace.s1 : 0)
    }
}

public extension View {
    /// `.as-card__title` — the lead size at bold.
    ///
    /// The CSS sets `line-height: 1.3` and that is not carried over: SwiftUI's
    /// `lineSpacing` adds points between lines rather than multiplying the line
    /// box, so the two cannot be made to agree by copying the number. The font's
    /// own leading is used instead.
    func anindaCardTitle() -> some View {
        font(AnindaFont.lead.weight(.bold))
    }

    /// `.as-card__meta` — the caption size in muted ink.
    ///
    /// Muted ink is the quietest colour the palette proves against the card fill,
    /// so meta text must still say what it is in words. Colour alone never carries
    /// a meaning here.
    func anindaCardMeta() -> some View {
        modifier(AnindaCardMetaStyle())
    }
}

/// Muted ink at the caption size, resolved for the theme the view is drawn in.
///
/// A `ViewModifier` rather than a plain `foregroundStyle` call, because a `View`
/// extension has no environment of its own and so cannot read the theme; a
/// modifier does.
private struct AnindaCardMetaStyle: ViewModifier {
    @Environment(\.anindaTheme) private var theme

    func body(content: Content) -> some View {
        content
            .font(AnindaFont.caption)
            .foregroundStyle(AnindaStyle(theme).inkMuted)
    }
}
