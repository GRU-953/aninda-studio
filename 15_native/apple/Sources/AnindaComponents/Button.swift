// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-btn`. Every value here
// comes from AnindaTokens, and the gate refuses this file if it contains a literal
// colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

public enum AnindaButtonTone: Sendable {
    case ordinary
    case primary
    case danger
    /// Borderless. Used where a button would otherwise crowd the thing it acts on.
    case quiet
}

/// A button styled to this system.
///
/// It is a `ButtonStyle` rather than a wrapper view, and that is deliberate: a
/// style leaves the caller with a real `Button`, so every behaviour the platform
/// gives one for nothing — the accessibility trait, the keyboard activation, Full
/// Keyboard Access, Voice Control, the press semantics — is inherited rather than
/// re-implemented. A custom view that draws a button and adds `.onTapGesture`
/// looks identical and has none of them.
public struct AnindaButtonStyle: ButtonStyle {
    private let tone: AnindaButtonTone
    private let small: Bool
    @Environment(\.anindaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    public init(_ tone: AnindaButtonTone = .ordinary, small: Bool = false) {
        self.tone = tone
        self.small = small
    }

    public func makeBody(configuration: Configuration) -> some View {
        let s = AnindaStyle(theme)
        let pressed = configuration.isPressed
        return configuration.label
            .font(AnindaFont.body.weight(.semibold))
            .foregroundStyle(foreground(s))
            .padding(.horizontal, small ? AnindaSpace.s2 : AnindaSpace.s3)
            .padding(.vertical, AnindaSpace.s1)
            // The minimum is Apple's own default control size, not a number chosen
            // here. Small buttons keep it too: a smaller LABEL is a design choice,
            // a smaller TARGET is an accessibility one, and they are not the same
            // decision.
            .frame(minWidth: AnindaTarget.comfortable,
                   minHeight: AnindaTarget.comfortable)
            .background(
                RoundedRectangle(cornerRadius: AnindaRadius.control)
                    .fill(background(s, pressed: pressed))
            )
            .overlay(
                RoundedRectangle(cornerRadius: AnindaRadius.control)
                    .strokeBorder(border(s, pressed: pressed), lineWidth: 1)
            )
            .contentShape(RoundedRectangle(cornerRadius: AnindaRadius.control))
            .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                       value: pressed)
    }

    private func foreground(_ s: AnindaStyle) -> Color {
        switch tone {
        case .ordinary, .quiet: return s.ink
        case .primary, .danger: return s.onAccent
        }
    }

    private func background(_ s: AnindaStyle, pressed: Bool) -> Color {
        switch tone {
        case .ordinary: return pressed ? s.surfaceHigh : s.surface
        case .quiet: return pressed ? s.surfaceHigh : .clear
        // accentHover, not accentEdge. accentEdge is proven at 3:1 as a LINE, and
        // behind this label it measured 4.35:1 — it moves the fill towards the
        // label's own lightness. accentHover is proven against the label itself.
        case .primary: return pressed ? s.accentHover : s.accent
        case .danger: return pressed ? s.accentHover : s.danger
        }
    }

    private func border(_ s: AnindaStyle, pressed: Bool) -> Color {
        switch tone {
        case .quiet: return .clear
        case .ordinary: return pressed ? s.ink : s.line
        case .primary: return pressed ? s.ink : s.accent
        case .danger: return pressed ? s.ink : s.danger
        }
    }
}

public extension ButtonStyle where Self == AnindaButtonStyle {
    static var aninda: AnindaButtonStyle { AnindaButtonStyle() }
    static func aninda(_ tone: AnindaButtonTone,
                       small: Bool = false) -> AnindaButtonStyle {
        AnindaButtonStyle(tone, small: small)
    }
}
