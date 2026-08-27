// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-choice`. Every value
// here comes from AnindaTokens, and the gate refuses this file if it contains a
// literal colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// A checkbox styled to this system.
///
/// The whole of `makeBody` is a wrapper around the platform's own checkbox. It
/// does not draw a box, a tick, a hover shadow or a focus ring, and that is the
/// point: a hand-drawn indicator loses the toggle accessibility trait, the
/// space-bar activation, Full Keyboard Access, Voice Control and Switch Control
/// that the real control carries, and it gains nothing but a shape I could have
/// tinted instead. The inner `Toggle` names its own style, so there is no
/// recursion back into this one.
///
/// WHAT THIS DOES NOT HANDLE. Four rules in the CSS have no SwiftUI expression
/// on a control I refuse to redraw:
///   - `.as-choice__control:hover` (a 1px ink-muted shadow) and `:active` (an ink
///     shadow at the ring offset). AppKit and UIKit own the pressed and hovered
///     appearance of a real checkbox, and there is no API to restyle it.
///   - the focus ring at AnindaFocus.ringWidth in the focus-ring colour. The
///     platform draws its own ring on the real control. A ring of mine would sit
///     beside the platform's rather than replace it, so I left the platform's.
///   - `gap: var(--as-space-1)` between the control and its text. A `Toggle` owns
///     the distance between its indicator and its label and exposes no way to set
///     it, so the platform's own figure stands.
/// The one thing the platform does honour is the tint, which is what
/// `accent-color: var(--as-accent)` asks for in the stylesheet.
public struct AnindaCheckboxStyle: ToggleStyle {
    @Environment(\.anindaTheme) private var theme

    public init() {}

    public func makeBody(configuration: Configuration) -> some View {
        let s = AnindaStyle(theme)
        #if os(macOS)
        // macOS has a real checkbox, so the checkbox is what the caller gets.
        return Toggle(isOn: configuration.$isOn) { configuration.label }
            .toggleStyle(.checkbox)
            .tint(s.accent)
            .frame(minHeight: AnindaTarget.comfortable, alignment: .leading)
        #elseif os(tvOS)
        // tvOS has neither a checkbox nor a switch: `.switch` was not added there
        // until tvOS 18, and this package declares tvOS 17. `.automatic` is the
        // platform's own binary control, and naming it — rather than leaving the
        // toggle style unset — is what stops the lookup finding this style again
        // and recursing.
        return Toggle(isOn: configuration.$isOn) { configuration.label }
            .toggleStyle(.automatic)
            .tint(s.accent)
            .frame(minHeight: AnindaTarget.comfortable, alignment: .leading)
        #else
        // iOS, watchOS and visionOS have no checkbox. The switch is the platform's
        // binary control there, and borrowing it keeps every assistive-technology
        // behaviour intact. The trade-off is honest: an iOS reader sees a switch,
        // not a tick box.
        return Toggle(isOn: configuration.$isOn) { configuration.label }
            .toggleStyle(.switch)
            .tint(s.accent)
            .frame(minHeight: AnindaTarget.comfortable, alignment: .leading)
        #endif
    }
}

public extension ToggleStyle where Self == AnindaCheckboxStyle {
    static var anindaCheckbox: AnindaCheckboxStyle { AnindaCheckboxStyle() }
}

/// A labelled checkbox with an optional hint beneath it.
///
/// This exists for the hint alone. `.as-choice__label` and `.as-choice__hint`
/// are two pieces of text with different weights and colours inside one label,
/// and a `ToggleStyle` cannot supply text the caller did not write. The control
/// underneath is still a real `Toggle` wearing `AnindaCheckboxStyle`.
///
/// The state is carried by shape and position, never by colour alone. On macOS an
/// on checkbox is a filled box with a tick in it; elsewhere the switch moves its
/// knob from one end of the track to the other. Both read with the tint removed,
/// and both report the on/off value to VoiceOver as well.
public struct AnindaCheckbox: View {
    private let title: String
    private let hint: String?
    @Binding private var isOn: Bool
    @Environment(\.anindaTheme) private var theme

    public init(_ title: String, hint: String? = nil, isOn: Binding<Bool>) {
        self.title = title
        self.hint = hint
        self._isOn = isOn
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        return Toggle(isOn: $isOn) {
            // The stylesheet gives the two lines no gap of their own; the line
            // height does the separating. 0 is a literal the gate allows.
            VStack(alignment: .leading, spacing: 0) {
                Text(title)
                    .font(AnindaFont.body.weight(.semibold))
                    .foregroundStyle(s.ink)
                if let hint {
                    Text(hint)
                        .font(AnindaFont.caption)
                        .foregroundStyle(s.inkMuted)
                }
            }
            .multilineTextAlignment(.leading)
        }
        .toggleStyle(.anindaCheckbox)
        // `padding-block: var(--as-space-0)` in the stylesheet. The row's own
        // minimum height comes from the style, and it is AnindaTarget.comfortable
        // rather than the CSS `--as-target-min`: a 24 pt row is fine on a mouse
        // and short of Apple's guidance under a thumb. A smaller LABEL would be a
        // design choice; a smaller TARGET is an accessibility one.
        .padding(.vertical, AnindaSpace.s0)
    }
}
