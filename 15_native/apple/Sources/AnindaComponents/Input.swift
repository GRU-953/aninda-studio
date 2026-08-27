// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css — `.as-field`, `.as-label`,
// `.as-input`, `.as-hint` and `.as-error`. Every value here comes from
// AnindaTokens, and the gate refuses this file if it contains a literal colour or
// a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

// MARK: - The control's own skin

/// The skin of `.as-input`, applied to a real `TextField` or `SecureField`.
///
/// This is a `ViewModifier` and not a replacement view, and that is the whole
/// point. SwiftUI already has the control, so I style it and hand it back. A
/// redrawn field — a `RoundedRectangle` with a tap gesture and a cursor of my own
/// — would lose the text-field accessibility trait, the keyboard focus chain,
/// dictation, Voice Control, Switch Control, autofill, the text-editing context
/// menu and the input accessory bar, and would gain nothing at all in return.
///
/// What it does not handle: the CSS `:active` state. A pointer press on a text
/// field is not a state SwiftUI exposes, and the moment of the press is
/// immediately followed by focus, which this DOES draw. `.as-select` and
/// `.as-textarea` share the CSS rule but not this modifier — a picker and a
/// multi-line editor have different platform controls, and wrapping them belongs
/// in their own files rather than in a flag here.
public struct AnindaInputSkin: ViewModifier {
    private let invalid: Bool
    @Environment(\.anindaTheme) private var theme
    @Environment(\.isEnabled) private var isEnabled
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @FocusState private var focused: Bool
    @State private var hovering = false

    public init(invalid: Bool = false) { self.invalid = invalid }

    public func body(content: Content) -> some View {
        let s = AnindaStyle(theme)
        return content
            // `.plain` strips Apple's own bezel. Without it the platform border
            // and this system's border are both drawn, one inside the other.
            .textFieldStyle(.plain)
            .font(AnindaFont.body)
            .foregroundStyle(isEnabled ? s.ink : s.inkMuted)
            .padding(.vertical, AnindaSpace.s1)
            .padding(.horizontal, AnindaSpace.s2)
            // The comfortable target, not the height the text needs. A field
            // sized to its glyphs is a smaller tap target than Apple's own
            // default, and a smaller TARGET is an accessibility decision rather
            // than a visual one.
            .frame(maxWidth: .infinity, minHeight: AnindaTarget.comfortable)
            .background(
                RoundedRectangle(cornerRadius: AnindaRadius.control)
                    .fill(isEnabled ? s.surface : s.surfaceHigh)
            )
            .overlay(
                RoundedRectangle(cornerRadius: AnindaRadius.control)
                    .strokeBorder(border(s), lineWidth: invalid ? 2 : 1)
            )
            // The ring sits OUTSIDE the border, as `outline-offset` puts it in
            // CSS, so a danger border and the ring stay separately readable. The
            // negative padding is what pushes it out; the radius grows by the
            // same offset so the two curves stay concentric.
            .overlay(
                RoundedRectangle(
                    cornerRadius: AnindaRadius.control + AnindaFocus.ringOffset
                )
                .strokeBorder(focused ? s.focusRing : .clear,
                              lineWidth: AnindaFocus.ringWidth)
                .padding(-AnindaFocus.ringOffset)
            )
            // Without this the field answers a tap only where its glyphs are. The
            // frame above makes the BOX 44 pt tall; a plain text field's own hit
            // region is the text line inside it, so the padding around the text
            // was dead to touch and the real target was shorter than the drawn
            // one. This hands the whole rounded box to the control.
            .contentShape(RoundedRectangle(cornerRadius: AnindaRadius.control))
            .focused($focused)
            .anindaHover { hovering = $0 }
            .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                       value: focused)
            .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                       value: hovering)
    }

    /// Invalid first, then disabled, then hover. That order is the CSS cascade's:
    /// the `[disabled]` rule sets a background and a text colour and leaves
    /// `border-color` alone, so a field that is both invalid and disabled keeps its
    /// danger border. With the two the other way round the border kept the 2 pt
    /// width of the invalid state while wearing the resting colour, which reads as
    /// a rendering fault rather than as a state.
    private func border(_ s: AnindaStyle) -> Color {
        if invalid { return s.danger }
        if !isEnabled { return s.line }
        return hovering ? s.inkMuted : s.line
    }
}

public extension View {
    /// Style a real `TextField` or `SecureField` as `.as-input`.
    ///
    /// Reach for `AnindaInput` instead when the field has a label, a hint or an
    /// error to show — that view applies this skin itself and wires the three to
    /// the control for VoiceOver, which a bare modifier cannot do.
    func anindaInput(invalid: Bool = false) -> some View {
        modifier(AnindaInputSkin(invalid: invalid))
    }
}

// MARK: - The field around it

/// A labelled field: `.as-field` — label, control, and then a hint or an error.
///
/// The control is the caller's own, passed in and never rebuilt. This view puts a
/// label above it, the skin on it, and one line of guidance below it.
///
/// An error replaces the hint rather than joining it. Two lines of small text
/// under one field compete, and the one that matters at that moment is the error;
/// showing both is how a hint ends up read out after a failure message.
public struct AnindaInput<Control: View>: View {
    private let label: String
    private let optionalText: String?
    private let hint: String?
    private let error: String?
    private let control: Control

    @Environment(\.anindaTheme) private var theme

    /// - Parameters:
    ///   - label: The visible label. It is also the accessibility label.
    ///   - optionalText: A quieter suffix, as `.as-label__optional`. I mark what
    ///     is optional rather than what is required, so the common case carries
    ///     no ornament.
    ///   - hint: Guidance shown while the field is valid.
    ///   - error: A whole sentence. Non-nil is what makes the field invalid, so
    ///     the message and the state cannot disagree.
    ///   - control: The real `TextField` or `SecureField`.
    public init(_ label: String,
                optionalText: String? = nil,
                hint: String? = nil,
                error: String? = nil,
                @ViewBuilder control: () -> Control) {
        self.label = label
        self.optionalText = optionalText
        self.hint = hint
        self.error = error
        self.control = control()
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        return VStack(alignment: .leading, spacing: AnindaSpace.s0) {
            labelText(s)
            control
                .anindaInput(invalid: error != nil)
                .accessibilityLabel(Text(label))
                // SwiftUI has no "invalid" accessibility trait to set, so the
                // error travels as the hint instead. That is weaker than the
                // web's aria-invalid: a screen reader announces it as guidance
                // rather than as a fault, and it is read after the value.
                .accessibilityHint(Text(error ?? hint ?? ""))
            if let error {
                // Never colour alone, and the same symbol `AnindaTextarea` uses so
                // the two fields fail alike. It was a bare multiplication-sign
                // character here before, which had neither property that matters:
                // it is drawn in Literata, which has no glyph at that code point,
                // and VoiceOver reads it aloud as a multiplication sign. A symbol
                // carries the state for a reader who cannot separate danger from
                // ink; its spoken label carries it for one who sees no field at
                // all; the sentence carries it for everyone else.
                HStack(alignment: .firstTextBaseline, spacing: AnindaSpace.s0) {
                    Image(systemName: "exclamationmark.triangle.fill")
                        // English only, as in `AnindaAlert`, and for the same
                        // reason: this library has no string catalogue yet.
                        .accessibilityLabel(Text(verbatim: "Error"))
                    Text(error)
                }
                .font(AnindaFont.caption.weight(.semibold))
                .foregroundStyle(s.danger)
                .accessibilityElement(children: .combine)
            } else if let hint {
                Text(hint)
                    .font(AnindaFont.caption)
                    .foregroundStyle(s.inkMuted)
            }
        }
    }

    private func labelText(_ s: AnindaStyle) -> some View {
        // One Text, built from two, so the label wraps as a single sentence
        // instead of breaking into two stacked pieces at a narrow width.
        var composed = Text(label).font(AnindaFont.body.weight(.semibold))
            .foregroundStyle(s.ink)
        if let optionalText {
            composed = composed
                + Text(verbatim: " ")
                + Text(optionalText).font(AnindaFont.body.weight(.regular))
                    .foregroundStyle(s.inkMuted)
        }
        return composed.fixedSize(horizontal: false, vertical: true)
    }
}
