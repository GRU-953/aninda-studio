// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-textarea`, together with
// the `.as-input, .as-select, .as-textarea` block it inherits from and the
// `.as-error` sentence that sits under an invalid field. Every value here comes
// from AnindaTokens, and the gate refuses this file if it contains a literal
// colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// The house dress for a multi-line text control.
///
/// It is a `ViewModifier` applied to a real `TextEditor` (or to a
/// `TextField(axis: .vertical)`), not a view that draws its own editable box.
/// That is the whole point: the platform control already carries the text
/// accessibility trait, VoiceOver's text-input rotor, caret and selection
/// handling, dictation, Voice Control, Switch Control, undo, spelling and the
/// system context menu. A redrawn box loses all of it and looks identical in a
/// screenshot, which is how the loss goes unnoticed until somebody who needs
/// those things tries to type.
///
/// I did not write a `TextEditorStyle` conformance instead. On the oldest target
/// this system supports — macOS 14 and iOS 17 — that protocol's configuration
/// gives no useful surface to style against, so a modifier is the honest choice.
///
/// What this does NOT handle: the CSS `resize: vertical` grab handle has no Apple
/// equivalent, so the box grows only as far as the caller's own layout allows;
/// and `::placeholder` is not offered, because `TextEditor` has no placeholder and
/// faking one over the top puts unfocusable text where VoiceOver expects content.
/// A visible label and a hint do that job in this system anyway.
public struct AnindaTextareaModifier: ViewModifier {
    /// Non-nil marks the field invalid AND supplies the sentence shown beneath it.
    /// The two are one parameter deliberately: the CSS pairs a red border with a
    /// glyph and a sentence, and a caller who could set the border alone would be
    /// signalling an error by colour alone the first time they were in a hurry.
    private let error: String?

    @Environment(\.anindaTheme) private var theme
    @Environment(\.isEnabled) private var isEnabled
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @FocusState private var focused: Bool
    @State private var hovering = false

    public init(error: String? = nil) {
        self.error = error
    }

    public func body(content: Content) -> some View {
        let s = AnindaStyle(theme)
        let invalid = error != nil
        return VStack(alignment: .leading, spacing: AnindaSpace.s0) {
            content
                .font(AnindaFont.body)
                .foregroundStyle(isEnabled ? s.ink : s.inkMuted)
                // Without this the editor paints its own opaque backing over the
                // token fill, and the field reads as the wrong colour in the dark
                // and high-contrast themes only. Through the bridge, because the
                // modifier is unavailable on tvOS — see anindaHideScrollBackground.
                .anindaHideScrollBackground()
                // The CSS asks for line-height 1.5 — a 24 pt line box on 16 pt
                // text, so 8 pt of added leading. There is no token for the
                // remainder after the font's own leading is counted, and I did not
                // add one for a single call site: s0 is the nearest that exists and
                // lands close on Literata at body size.
                .lineSpacing(AnindaSpace.s0)
                .focused($focused)
                // The CSS puts `aria-invalid="true"` on the control itself, so a
                // screen reader hears the fault ON the field. SwiftUI has no
                // invalid trait to set, so the sentence travels as the hint
                // instead — the same compromise `AnindaInput` makes, and weaker
                // in the same way: it is announced as guidance rather than as a
                // fault, and after the value. Without it the only carrier of the
                // state is a red border and a sibling sentence, which is the
                // colour-alone failure this file says it avoids.
                //
                // It is applied unconditionally, with an empty string when the
                // field is valid, because branching here would change the view's
                // identity the moment an error appeared and take the caret and
                // the selection with it.
                .accessibilityHint(Text(error ?? ""))
                .padding(.horizontal, AnindaSpace.s2)
                .padding(.vertical, AnindaSpace.s1)
                // 96 pt, from the CSS `min-height: var(--as-space-8)`. It clears
                // the 44 pt comfortable target on its own, so the target rule is
                // satisfied by the design size rather than in spite of it.
                .frame(maxWidth: .infinity, minHeight: AnindaSpace.s8,
                       alignment: .topLeading)
                .background(
                    RoundedRectangle(cornerRadius: AnindaRadius.control)
                        .fill(isEnabled ? s.surface : s.surfaceHigh)
                )
                .overlay(
                    RoundedRectangle(cornerRadius: AnindaRadius.control)
                        .strokeBorder(border(s, invalid: invalid),
                                      lineWidth: invalid ? 2 : 1)
                )
                .overlay(focusRing(s))
                .contentShape(RoundedRectangle(cornerRadius: AnindaRadius.control))
                .anindaHover { hovering = $0 }
                .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                           value: hovering)
                .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                           value: focused)

            if let error {
                // A shape and a word, never the colour on its own — the border
                // turning red is invisible to a reader who cannot see red, and
                // inaudible to one who cannot see the field at all.
                HStack(alignment: .firstTextBaseline, spacing: AnindaSpace.s0) {
                    Image(systemName: "exclamationmark.triangle.fill")
                    Text(error)
                }
                .font(AnindaFont.caption.weight(.semibold))
                .foregroundStyle(s.danger)
                .accessibilityElement(children: .combine)
            }
        }
    }

    /// Rest, hover and invalid. The CSS `:active` state has no counterpart here:
    /// AppKit and UIKit do not expose the press moment of a text view, and a
    /// tap-gesture stand-in would swallow the tap that places the caret. I chose
    /// the caret over the flicker of feedback.
    private func border(_ s: AnindaStyle, invalid: Bool) -> Color {
        if invalid { return s.danger }
        if !isEnabled { return s.line }
        return hovering ? s.inkMuted : s.line
    }

    private func focusRing(_ s: AnindaStyle) -> some View {
        // Negative padding puts the ring outside the border, as `outline-offset`
        // does in CSS, and the radius grows by the same offset so the two curves
        // stay concentric. Insetting the rounded rectangle by a negative amount
        // instead would move the edge and leave the corner radius where it was,
        // giving a ring whose corners are tighter than the border it surrounds.
        //
        // The ring is always in the tree and merely goes clear, rather than being
        // inserted when focus arrives. An overlay that appears fades in; one that
        // changes colour cross-fades, which is what the `.animation` on `focused`
        // below was written to do.
        //
        // It is drawn without reserving space for itself, so a parent that clips
        // tightly will crop it; that was the trade — the field stays on the layout
        // grid, and callers give it room.
        RoundedRectangle(
            cornerRadius: AnindaRadius.control + AnindaFocus.ringOffset
        )
        .strokeBorder(focused ? s.focusRing : .clear,
                      lineWidth: AnindaFocus.ringWidth)
        .padding(-AnindaFocus.ringOffset)
    }
}

public extension View {
    /// Dress a `TextEditor` — or any multi-line text control — as this system's
    /// textarea. Pass `error` to mark it invalid and show the sentence beneath.
    func anindaTextarea(error: String? = nil) -> some View {
        modifier(AnindaTextareaModifier(error: error))
    }
}
