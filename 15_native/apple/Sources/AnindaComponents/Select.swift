// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-select`, together with
// the `.as-input, .as-select, .as-textarea` block it shares. Every value here
// comes from AnindaTokens, and the gate refuses this file if it carries a literal
// colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// The field chrome of this system, applied to a real `Picker`.
///
/// I wrap the platform control rather than redrawing it. SwiftUI already has the
/// menu picker, and a hand-drawn substitute would lose the pop-up-button
/// accessibility trait, keyboard activation, Full Keyboard Access, Voice Control
/// and Switch Control that the real one carries for nothing — in exchange for a
/// border I can draw around the real one anyway. So this is a `ViewModifier`: the
/// caller keeps their `Picker`, its selection binding and its tags, and receives
/// the surface, line, radius and states the CSS specifies.
///
/// What it does not handle. The focus ring is left to the platform. The CSS draws
/// its own outline at `AnindaFocus.ringWidth` and `AnindaFocus.ringOffset`, but a
/// modifier cannot see the focus state of a control it does not own, and a ring
/// that guesses is worse than the one the system draws while actually tracking
/// focus. `.as-select`'s `padding-inline-end: var(--as-space-6)` and its
/// `.as-select-wrap__arrow` are also dropped: that reserve exists because the CSS
/// sets `appearance: none` and then draws its own arrow, whereas the native
/// control brings an indicator with its own metrics. Adding a second chevron would
/// put two arrows on one control.
public struct AnindaSelect: ViewModifier {
    private let invalid: Bool
    @Environment(\.anindaTheme) private var theme
    @Environment(\.isEnabled) private var isEnabled
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var hovering = false

    /// - Parameter invalid: matches `[aria-invalid="true"]`. The border turns to
    ///   danger AND thickens, because a colour on its own is not a signal. The
    ///   sentence that says what is wrong belongs beside the field, in the
    ///   caller's own error text — this modifier styles a control, not a form row.
    public init(invalid: Bool = false) {
        self.invalid = invalid
    }

    public func body(content: Content) -> some View {
        let s = AnindaStyle(theme)
        return presented(content)
            .labelsHidden()
            .font(AnindaFont.body)
            .foregroundStyle(isEnabled ? s.ink : s.inkMuted)
            // The menu's own tint, so the indicator matches the label rather than
            // falling back to the platform accent this system did not measure.
            .tint(isEnabled ? s.ink : s.inkMuted)
            .padding(.horizontal, AnindaSpace.s2)
            .padding(.vertical, AnindaSpace.s1)
            // A field is dragged onto and tapped like any other target, so the
            // minimum applies in both directions. A shorter LABEL would be a
            // design choice; a shorter TARGET is an accessibility one.
            .frame(minWidth: AnindaTarget.comfortable,
                   minHeight: AnindaTarget.comfortable)
            .background(
                RoundedRectangle(cornerRadius: AnindaRadius.control).fill(fill(s))
            )
            .overlay(
                RoundedRectangle(cornerRadius: AnindaRadius.control)
                    .strokeBorder(border(s), lineWidth: invalid ? 2 : 1)
            )
            .contentShape(RoundedRectangle(cornerRadius: AnindaRadius.control))
            // Hover is a pointer state. It is inert on a touch-only device, which
            // is why it changes the border rather than being the only way to tell
            // the control apart from the page.
            .anindaHover { hovering = $0 }
            .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                       value: hovering)
            .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                       value: invalid)
    }

    /// The picker as the platform presents it, before this system's chrome.
    ///
    /// The menu picker is the control the CSS `<select>` maps onto, and plain
    /// button styling is what stops the platform's own bezel sitting inside the
    /// border drawn below — a control wearing two frames.
    ///
    /// watchOS has no menu picker: `.menu` is unavailable there, and the package
    /// declares watchOS 10, so naming it would refuse to compile for a platform
    /// this package claims. The wrist gets its own picker presentation — a
    /// full-screen list reached from the field — and the chrome below still
    /// applies to the field itself. Substituting a hand-drawn menu is the trade
    /// the type of this file exists to refuse.
    @ViewBuilder
    private func presented(_ content: Content) -> some View {
        #if os(watchOS)
        content
        #else
        content
            .pickerStyle(.menu)
            .buttonStyle(.plain)
        #endif
    }

    private func fill(_ s: AnindaStyle) -> Color {
        // `[disabled]` in the CSS fills with surface-high and mutes the ink. There
        // is no `cursor: not-allowed` here: the platform decides its own pointer.
        isEnabled ? s.surface : s.surfaceHigh
    }

    private func border(_ s: AnindaStyle) -> Color {
        if invalid { return s.danger }
        if !isEnabled { return s.line }
        return hovering ? s.inkMuted : s.line
    }
}

public extension View {
    /// Give a `Picker` the field chrome of this system.
    ///
    /// The CSS `:active` state — ink border, surface-high fill and an inset
    /// hairline — is not reproduced. A menu picker's press opens the menu, and
    /// SwiftUI does not expose that press to a modifier the way `ButtonStyle`
    /// exposes `isPressed`. I would rather leave the state out than fake it with a
    /// gesture recogniser that competes with the control's own.
    func anindaSelect(invalid: Bool = false) -> some View {
        modifier(AnindaSelect(invalid: invalid))
    }
}
