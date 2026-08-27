// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-dialog`. Every value here
// comes from AnindaTokens, and the gate refuses this file if it contains a literal
// colour or a literal size.
//
// WHY THIS IS A VIEW AND NOT A STYLE OF SOMETHING PLATFORM-GIVEN
// ==============================================================
// The house rule is to wrap the platform control and never redraw it, and I have
// kept it as far as the platform allows. SwiftUI's `.alert` and
// `.confirmationDialog` are drawn by the operating system and expose no surface
// for a palette, a radius or a border, so there is no style protocol to conform
// to and nothing to hand back. What SwiftUI does give is the PRESENTATION, and
// that is the part worth keeping: `.sheet` supplies the modal focus containment,
// the drag dismissal on iOS and the modal announcement to VoiceOver. So the
// presentation stays the platform's and only the card inside it is drawn here.
//
// One thing `.sheet` does NOT supply, and an earlier draft of this comment claimed
// it did: Escape does not dismiss a sheet on macOS on its own. AppKit routes the
// key to whichever control carries the cancel key equivalent, and a sheet with no
// such control has nothing to route it to. The caller has to give one action
// `.keyboardShortcut(.cancelAction)`, and `anindaDialog` says so where a caller
// will read it.
//
// Where the platform alert is enough — a destructive confirmation with no custom
// content — prefer `.alert`. It will look like the operating system rather than
// like this system, and on that trade I would rather lose the styling than the
// behaviour.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// The dialog card: a titled surface with content and a trailing row of actions.
///
/// This draws the card only. Present it with `View.anindaDialog(isPresented:…)`
/// below, or place it inside a presentation of your own.
public struct AnindaDialog<Content: View, Actions: View>: View {
    private let title: String
    private let content: Content
    private let actions: Actions
    @Environment(\.anindaTheme) private var theme

    public init(title: String,
                @ViewBuilder content: () -> Content,
                @ViewBuilder actions: () -> Actions) {
        self.title = title
        self.content = content()
        self.actions = actions()
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        return VStack(alignment: .leading, spacing: AnindaSpace.s2) {
            Text(title)
                .font(AnindaFont.lead.weight(.bold))
                .foregroundStyle(s.ink)
                // A dialog title is a heading to a screen reader even though the
                // card carries no heading level. Without this the rotor has
                // nothing to land on and the title reads as ordinary text.
                .accessibilityAddTraits(.isHeader)
            content
                .font(AnindaFont.body)
                .foregroundStyle(s.ink)
            footer
                // The CSS sets margin-block-start on the footer as well as the
                // column gap, so the actions sit further from the text than the
                // text does from the title. That extra step is this one.
                .padding(.top, AnindaSpace.s1)
        }
        // The CSS caps the card at `min(100%, 420px)`. There is no 420 in
        // AnindaTokens and I did not add one: the spacing scale is a rhythm, not a
        // measure, and a one-off width would be the first value in it that no
        // other component uses. The card takes the width its presentation gives
        // it instead, which on a sheet is already bounded. On a wide macOS window
        // that reads a little broader than the web dialog does.
        .padding(AnindaSpace.s4)
        .background(
            RoundedRectangle(cornerRadius: AnindaRadius.card).fill(s.surface)
        )
        .overlay(
            RoundedRectangle(cornerRadius: AnindaRadius.card)
                .strokeBorder(s.line, lineWidth: 1)
        )
        // The border is drawn in every theme, and it is what carries the card's
        // edge in the three themes where the shadow is switched off. A card told
        // apart from its backdrop by shadow alone would merge into it for a reader
        // in high contrast.
        .modifier(AnindaDialogShadow(theme: theme))
        // `.contain` rather than `.combine`: the actions inside must stay
        // separately focusable, and combining would flatten them into the label.
        .accessibilityElement(children: .contain)
        .accessibilityAddTraits(.isModal)
        .accessibilityLabel(Text(title))
    }

    /// The action row.
    ///
    /// The CSS footer wraps. SwiftUI has no flex-wrap, and `ViewThatFits` is the
    /// nearest honest equivalent: it lays the buttons out in a row, and drops to a
    /// stacked column when the row no longer fits. That covers the case the wrap
    /// exists for — a narrow card, or long labels at a large Dynamic Type
    /// setting — but it moves ALL the buttons at once rather than wrapping the
    /// last one, so a three-button footer degrades a step earlier than the web
    /// version does. I took that over letting the labels squash.
    ///
    /// Nothing here sets a target size. The actions are the caller's own
    /// `Button`s, and `AnindaButtonStyle` already holds them at
    /// `AnindaTarget.comfortable` in both dimensions.
    private var footer: some View {
        ViewThatFits(in: .horizontal) {
            HStack(spacing: AnindaSpace.s1) { actions }
            VStack(alignment: .trailing, spacing: AnindaSpace.s1) { actions }
        }
        .frame(maxWidth: .infinity, alignment: .trailing)
    }
}

/// The float shadow, drawn only in the theme that publishes one.
///
/// `.as-dialog` carries `box-shadow: var(--as-shadow-float)` and this file had no
/// answer to it, which left the dialog the only one of the three floating surfaces
/// in the stylesheet — card, dialog, toast — without its lift. `--as-shadow-float`
/// is `none` in the dark theme and in both high-contrast themes, so reading the
/// theme rather than always drawing keeps the four matching the stylesheet.
///
/// This repeats the card's shadow rather than sharing it, for the reason the toast
/// gives: the card's copy is `private` to its own file, and promoting it to public
/// API is a decision about the library's surface rather than about this component.
///
/// There is no shadow token in AnindaTokens — that file is generated, so adding one
/// is a change to the generator. I wanted the CSS pair `0 1px 2px rgb(0 0 0 / 0.06)`
/// and `0 8px 24px rgb(0 0 0 / 0.08)`. The blur radii map to half their CSS values,
/// because SwiftUI's radius is a standard deviation where CSS's is a blur diameter:
/// 2 becomes 1, and 24 becomes `AnindaSpace.s2`. The colour is `s.ink` at those
/// opacities rather than pure black, which the gate refuses — in the light theme
/// ink is a near-black and the difference is below what 6 and 8 per cent can show.
private struct AnindaDialogShadow: ViewModifier {
    let theme: AnindaTheme

    func body(content: Content) -> some View {
        let s = AnindaStyle(theme)
        let lifted = theme == .light
        return content
            .shadow(color: lifted ? s.ink.opacity(0.06) : .clear,
                    radius: lifted ? 1 : 0, x: 0, y: lifted ? 1 : 0)
            .shadow(color: lifted ? s.ink.opacity(0.08) : .clear,
                    radius: lifted ? AnindaSpace.s2 : 0,
                    x: 0, y: lifted ? AnindaSpace.s1 : 0)
    }
}

/// Presents an `AnindaDialog` over the modified view.
struct AnindaDialogPresentation<DialogContent: View, Actions: View>: ViewModifier {
    @Binding var isPresented: Bool
    let title: String
    let dialogContent: () -> DialogContent
    let actions: () -> Actions
    @Environment(\.anindaTheme) private var theme

    func body(content: Content) -> some View {
        content.sheet(isPresented: $isPresented) {
            AnindaDialog(title: title, content: dialogContent, actions: actions)
                .padding(AnindaSpace.s4)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                // A sheet is a separate presentation and custom environment values
                // have not always crossed into one reliably. Re-stating the theme
                // costs nothing and removes the question; without it a dialog can
                // come back in the default light palette over a dark app.
                .anindaTheme(theme)
                // The scrim in the CSS is `--as-ink` at 45%, which is a token plus
                // an alpha and so cannot itself be a token. Clearing the sheet's
                // own background lets the card read as a card, and what stands in
                // for the scrim is whatever the presentation dims by itself: it
                // matches every other modal on the device and it respects the
                // reduce-transparency setting a hand-drawn rectangle would ignore.
                // That is a dimmed backdrop on iOS and iPadOS. On macOS a sheet
                // does not dim its parent window at all, so the dialog is told
                // from the window behind it by its border and its shadow rather
                // than by a scrim. Both are the platform's own convention, which
                // is the trade this whole file is making.
                .presentationBackground(Color.clear)
        }
    }
}

public extension View {
    /// Present a dialog styled to this system, using the platform's own sheet.
    ///
    /// Give each action a word, never a colour alone: a destructive button is
    /// recognised by reading "Delete", not by being red.
    ///
    /// Give one action `.keyboardShortcut(.cancelAction)` as well. On macOS that
    /// is what makes Escape close the dialog — a sheet with no cancel action has
    /// nothing for the key to reach, and a keyboard-only reader is then held in a
    /// dialog they cannot leave. On iOS and iPadOS the drag dismissal covers the
    /// same ground, and the shortcut costs nothing there.
    func anindaDialog<DialogContent: View, Actions: View>(
        isPresented: Binding<Bool>,
        title: String,
        @ViewBuilder content: @escaping () -> DialogContent,
        @ViewBuilder actions: @escaping () -> Actions
    ) -> some View {
        modifier(AnindaDialogPresentation(isPresented: isPresented,
                                          title: title,
                                          dialogContent: content,
                                          actions: actions))
    }
}
