// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-empty`. Every value here
// comes from AnindaTokens, and the gate refuses this file if it contains a literal
// colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// The state a list, a search or an inbox is in when it holds nothing.
///
/// This is a `View` rather than a style or a modifier, and that is the exception
/// to the rule I hold everywhere else in this library: where SwiftUI already owns
/// the control I wrap it and return it, because a redrawn control throws away the
/// accessibility trait, the keyboard activation, Voice Control and Switch Control
/// that the real one carries for nothing. SwiftUI has no empty-state control on
/// macOS 14 / iOS 17 that I could style — `ContentUnavailableView` arrives in the
/// same releases but takes its type and metrics from the platform, not from this
/// system's tokens, so styling it to the CSS is not possible. There is nothing to
/// wrap here, so drawing it is the honest choice rather than a lazy one.
///
/// What this does NOT handle: it is a static panel. It does not know why the list
/// is empty, so the caller supplies the wording, and a "no results" message and a
/// "nothing here yet" message are different messages the caller must choose
/// between.
public struct AnindaEmptyState<Action: View>: View {
    private let glyph: String?
    private let title: String
    private let message: String?
    private let action: Action

    @Environment(\.anindaTheme) private var theme

    public init(glyph: String? = nil,
                title: String,
                message: String? = nil,
                @ViewBuilder action: () -> Action) {
        self.glyph = glyph
        self.title = title
        self.message = message
        self.action = action()
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        return VStack(spacing: AnindaSpace.s2) {
            VStack(spacing: AnindaSpace.s2) {
                if let glyph {
                    Text(glyph)
                        .font(AnindaFont.h3)
                        .foregroundStyle(s.inkMuted)
                        // The glyph repeats what the title already says, so a
                        // screen reader that read both would read the state twice.
                        // Hiding it is safe precisely BECAUSE the title carries
                        // the meaning in words: nothing here is signalled by the
                        // mark alone.
                        .accessibilityHidden(true)
                }
                Text(title)
                    .font(AnindaFont.lead.weight(.bold))
                    .foregroundStyle(s.ink)
                if let message {
                    Text(message)
                        .font(AnindaFont.body)
                        .foregroundStyle(s.inkMuted)
                        // The CSS caps this line at 46ch, roughly 368 pt at body
                        // size. There is no token for that width and I did not
                        // invent one: a measure is a typographic decision about
                        // the running text of a page, not a spacing step, and
                        // adding it to AnindaSpace would put a value in the scale
                        // that no other component could use. The panel therefore
                        // takes the width its parent gives it, and a caller
                        // placing this in a wide window should constrain it there.
                        // That is the one place this diverges from the web.
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
            // Read as one announcement, the way AnindaAlert reads. Left split,
            // VoiceOver makes the reader swipe through a heading and a sentence to
            // learn one fact. The action is deliberately OUTSIDE this stack:
            // combining it in would fold a control into a block of text and cost
            // it the button trait and its own focus stop.
            .accessibilityElement(children: .combine)

            action
        }
        .multilineTextAlignment(.center)
        .padding(.vertical, AnindaSpace.s5)
        .padding(.horizontal, AnindaSpace.s3)
        .frame(maxWidth: .infinity)
        .background(
            RoundedRectangle(cornerRadius: AnindaRadius.card)
                .fill(s.surface)
        )
        .overlay(
            RoundedRectangle(cornerRadius: AnindaRadius.card)
                // Dashed, as the CSS has it, and the dash is doing work rather than
                // decorating: a solid border reads as a card that holds content, a
                // dashed one reads as a space waiting for it. The dash length is a
                // spacing step because a border pattern is a measurement like any
                // other and should not be a loose number.
                .strokeBorder(s.line,
                              style: StrokeStyle(lineWidth: 1,
                                                 dash: [AnindaSpace.s0]))
        )
        // `.contain` and not `.combine`: it makes the panel a container the reader
        // can navigate into, and leaves the two elements inside it — the combined
        // text above, and the action — reachable in their own right. `.combine`
        // here would swallow the action's button trait; the merge that IS wanted
        // happens one level down, on the text alone.
        .accessibilityElement(children: .contain)
    }
}

public extension AnindaEmptyState where Action == EmptyView {
    /// The common case: a panel that states the situation and offers no control.
    init(glyph: String? = nil, title: String, message: String? = nil) {
        self.init(glyph: glyph, title: title, message: message) { EmptyView() }
    }
}
