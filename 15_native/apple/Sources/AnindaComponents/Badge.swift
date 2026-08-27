// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-badge`. Every value here
// comes from AnindaTokens, and the gate refuses this file if it contains a literal
// colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// Which of the five meanings a badge carries, plus the neutral default.
///
/// The CSS has one unmodified `.as-badge` and five modifiers. `neutral` is the
/// unmodified one rather than a sixth colour, so the two files stay countable
/// against each other.
public enum AnindaBadgeTone: Sendable {
    case neutral
    case success
    case warning
    case danger
    case info
    case accent
}

/// A small status marker: a word, a shape, and a colour.
///
/// This one is a `View` and not a style, and that is the exception to the rule
/// the button follows rather than a departure from it. SwiftUI's own `.badge()`
/// is not a general-purpose control — it attaches a count to a `List` row, a tab
/// or a toolbar item, takes no colour, no glyph and no shape, and cannot be
/// placed inline in a sentence. There is no platform control here to wrap, so
/// there is nothing to lose by drawing one.
///
/// The label is not optional, and that is rule 3 of the CSS header made
/// structural. A stylesheet cannot stop somebody colouring an empty span red;
/// an initialiser that demands a `String` can. The glyph is a second, redundant
/// signal for the same reason — it survives greyscale, it survives a reader who
/// does not distinguish the amber from the red, and it is spoken, so it survives
/// a reader who hears the badge rather than seeing it.
///
/// What this does NOT handle: it is decorative, not interactive. Rule 6's 44 pt
/// minimum is a rule about targets, and a badge is not a target — it sits at the
/// CSS's own 24 pt minimum height. Anybody who puts one inside a `Button` owes
/// that button the comfortable target, and this view will not supply it.
public struct AnindaBadge: View {
    private let label: String
    private let tone: AnindaBadgeTone
    private let glyph: String
    private let solid: Bool

    @Environment(\.anindaTheme) private var theme

    /// - Parameters:
    ///   - label: the word. Required, deliberately — see the type's own note.
    ///   - tone: which meaning this carries.
    ///   - glyph: overrides the tone's default mark. Pass an empty string to drop
    ///     it, which is worth doing only where the surrounding text already
    ///     repeats the state in words.
    ///   - solid: the `.as-badge--solid` modifier — a filled badge rather than an
    ///     outlined one. Louder, so reserve it for the one badge in a row that
    ///     matters most.
    public init(_ label: String,
                tone: AnindaBadgeTone = .neutral,
                glyph: String? = nil,
                solid: Bool = false) {
        self.label = label
        self.tone = tone
        self.glyph = glyph ?? Self.defaultGlyph(for: tone)
        self.solid = solid
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        return HStack(spacing: AnindaSpace.s0) {
            if !glyph.isEmpty {
                Text(glyph)
                    // The glyph IS the status for a sighted reader, so it has to
                    // be the status for a listening one too — the same rule
                    // AnindaAlert and AnindaToast follow with their symbols.
                    // Hiding it was the earlier answer, on the argument that the
                    // label repeats the state in words. The label often does not:
                    // "Beta", "3" and "Draft" all carry their state in the colour
                    // and the mark alone, and hiding the mark leaves a VoiceOver
                    // reader with the colour alone, which is the one thing this
                    // system refuses. The cost is a repeated word on the badges
                    // whose label does name the state.
                    .accessibilityLabel(Text(spokenTone))
            }
            Text(label)
        }
        .font(AnindaFont.caption.weight(.semibold))
        .foregroundStyle(foreground(s))
        .lineLimit(1)
        // `white-space: nowrap` in the CSS. On Apple platforms a one-line limit
        // alone would truncate to an ellipsis at large Dynamic Type sizes, and a
        // status word with its end cut off is worse than one that overruns. The
        // trade-off is that a badge can push past a narrow container instead of
        // shrinking; a truncated "Failed" is a defect, an overhanging one is a
        // layout to fix.
        .fixedSize(horizontal: true, vertical: false)
        .padding(.horizontal, AnindaSpace.s1)
        // No vertical padding, matching `padding: 0 var(--as-space-1)`. The height
        // comes from the minimum below, which grows with the text when the reader
        // has scaled it up.
        .frame(minHeight: AnindaSpace.s4)
        .background(
            RoundedRectangle(cornerRadius: AnindaRadius.badge)
                .fill(background(s))
        )
        .overlay(
            RoundedRectangle(cornerRadius: AnindaRadius.badge)
                .strokeBorder(border(s), lineWidth: 1)
        )
        // One element, one announcement — "Failed", not "✕" then "Failed".
        .accessibilityElement(children: .combine)
    }

    /// The default mark per tone.
    ///
    /// These are text, not SF Symbols, because the CSS `.as-badge__glyph` is text
    /// and the two platforms should show the same mark. A symbol would render
    /// better on Apple and match nothing.
    private static func defaultGlyph(for tone: AnindaBadgeTone) -> String {
        switch tone {
        case .neutral: return ""
        case .success: return "\u{2713}"   // ✓
        case .warning: return "\u{26A0}"   // ⚠
        case .danger:  return "\u{2715}"   // ✕
        case .info:    return "\u{2139}"   // ℹ
        case .accent:  return "\u{2605}"   // ★
        }
    }

    /// What the glyph says out loud.
    ///
    /// English only, and knowingly so — the same limit AnindaAlert and AnindaToast
    /// record. This library has no string catalogue yet, and inventing one here
    /// would put the translations of five words in a component file rather than
    /// where the rest of the copy will live.
    ///
    /// `neutral` has no glyph, so it has nothing to speak; the empty string is the
    /// case never reached rather than a word chosen for it.
    private var spokenTone: String {
        switch tone {
        case .neutral: return ""
        case .success: return "Success"
        case .warning: return "Warning"
        case .danger:  return "Error"
        case .info:    return "Information"
        case .accent:  return "Highlighted"
        }
    }

    /// The tone's own colour. Outlined badges wear it as ink and as border, which
    /// is what `border: 1px solid currentColor` does in the CSS.
    private func toneColour(_ s: AnindaStyle) -> Color {
        switch tone {
        case .neutral: return s.inkMuted
        case .success: return s.success
        case .warning: return s.warning
        case .danger:  return s.danger
        case .info:    return s.info
        case .accent:  return s.accent
        }
    }

    private func foreground(_ s: AnindaStyle) -> Color {
        // Solid badges put the surface colour on top of the tone. `s.surface` and
        // not `s.onAccent`: the CSS names `--as-surface-lowest` here, and
        // `accentOn` is a different measured pair that happens to look similar in
        // the light theme and diverges in the other three.
        solid ? s.surface : toneColour(s)
    }

    private func background(_ s: AnindaStyle) -> Color {
        solid ? toneColour(s) : s.surface
    }

    private func border(_ s: AnindaStyle) -> Color {
        toneColour(s)
    }
}
