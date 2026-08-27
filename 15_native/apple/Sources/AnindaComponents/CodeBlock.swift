// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-code`, `.as-code__head`,
// `.as-code__name`, `.as-code__pre` and `.as-code__comment`, together with the copy
// button and the `.as-code__said` live region the component card puts in the head.
// Every value here comes from AnindaTokens, and the gate refuses this file if it
// carries a literal colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

// WHICH PLATFORMS HAVE A PASTEBOARD
// =================================
// `UIPasteboard` is declared `API_UNAVAILABLE(tvos)` and `API_UNAVAILABLE(watchos)`
// in the UIKit headers, and neither of those two ships a replacement. The package
// declares tvOS 17 and watchOS 10, so the condition has to name both: `canImport
// (UIKit)` is TRUE on tvOS, and reaching for the pasteboard behind it is a build
// failure on a platform this library says it supports.
//
// The same condition gates the copy button itself further down, and that is the
// point rather than a tidy-up. A button that says "Copy the code", says "Copied"
// and posts an announcement while nothing reached a pasteboard is a control that
// reports a success it did not have — worse for somebody reading the screen than
// no button at all, because the announcement is the only evidence they get.
#if canImport(UIKit) && !os(watchOS) && !os(tvOS)
import UIKit
#elseif canImport(AppKit)
import AppKit
#endif

/// A fenced block of code with a filename and a copy button.
///
/// This is a small `View` rather than a style or a modifier, and that follows the
/// rule rather than bending it: the rule is to wrap the platform control wherever
/// one exists, and SwiftUI ships nothing that is a code block. The one real control
/// inside it — the copy button — IS a genuine `Button` wearing `AnindaButtonStyle`,
/// not a tappable rectangle. That is what keeps the button accessibility trait,
/// keyboard activation, Full Keyboard Access, Voice Control and Switch Control,
/// none of which an `.onTapGesture` on a drawn shape has.
///
/// What this does NOT handle:
///
/// - `.as-code__comment`. The stylesheet mutes comment spans inside the code, and
///   that needs either a lexer or a marked-up string. Taking an `AttributedString`
///   would push the colouring decision onto every caller and still leave them
///   reaching into the palette themselves, and writing a lexer is a far larger
///   thing than the block it would serve. Code arrives here as plain text and is
///   drawn in `ink` throughout.
/// - `tab-size: 2`. SwiftUI's `Text` has no tab-stop control, so a tab lands on the
///   font's own stop. Indent the string with spaces where the width matters.
/// - `line-height: 1.6`. SwiftUI's `lineSpacing` adds points BETWEEN lines while
///   CSS multiplies the whole line box, so copying the number across would not
///   reproduce the same rhythm. The font's own leading is used instead, which is
///   the decision `Card.swift` records for `.as-card__title` as well.
/// - `min-width: 0`. That declaration exists to stop a flex child refusing to
///   shrink, and SwiftUI's layout has no matching failure to guard against.
/// - `flex-wrap: wrap` on the head. An `HStack` has no one-modifier equivalent, so
///   a very long filename truncates in the middle rather than dropping the button
///   onto a second row. Truncation is why `.truncationMode(.middle)` is there.
/// - The copy button, on tvOS and watchOS. Neither platform has a pasteboard —
///   `UIPasteboard` is marked unavailable on both — so the head carries the
///   filename alone there. The initialiser still takes both labels on every
///   platform, so a caller writes the same call everywhere.
/// - `user-select` on the code, on tvOS and watchOS. `textSelection` is marked
///   unavailable on both, and with no pointer and no selection menu on either
///   there is nothing for it to drive.
public struct AnindaCodeBlock: View {
    private let name: String
    private let code: String
    private let copyLabel: String
    private let copiedLabel: String

    @Environment(\.anindaTheme) private var theme
    @State private var copied = false

    /// - Parameters:
    ///   - name: the filename shown in the head, matching `.as-code__name`. Pass an
    ///     empty string for a block with no name; the copy button stays where it is.
    ///   - code: the code itself, as plain text.
    ///   - copyLabel: the copy button's words. It says what it copies rather than
    ///     carrying a bare icon, because an icon alone gives a screen reader nothing
    ///     to read out and gives Voice Control no name to speak.
    ///   - copiedLabel: what the button says once the copy has happened. This is the
    ///     sighted half of the confirmation; the spoken half is posted as an
    ///     accessibility announcement, which is what `.as-code__said` does on the web
    ///     with a polite live region.
    public init(name: String,
                code: String,
                copyLabel: String = "Copy the code",
                copiedLabel: String = "Copied") {
        self.name = name
        self.code = code
        self.copyLabel = copyLabel
        self.copiedLabel = copiedLabel
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        return VStack(alignment: .leading, spacing: 0) {
            head(s)
            pre(s)
        }
        // `--as-surface-highest` is what the stylesheet fills this with, and
        // AnindaStyle publishes no `surfaceHighest`. `surfaceHigh` is the nearest
        // role it does publish, and the two sit one step apart — #F4F3F3 against
        // #F5F5F4 in the light theme. I have not added the missing role here,
        // because AnindaTokensUI's palette surface is a deliberate subset and
        // widening it is a change to the token layer rather than to a component.
        .background(
            RoundedRectangle(cornerRadius: AnindaRadius.control).fill(s.surfaceHigh)
        )
        .overlay(
            RoundedRectangle(cornerRadius: AnindaRadius.control)
                .strokeBorder(s.line, lineWidth: 1)
        )
    }

    /// `.as-code__head` — the filename on one side, the copy button on the other.
    @ViewBuilder
    private func head(_ s: AnindaStyle) -> some View {
        HStack(spacing: AnindaSpace.s1) {
            Text(name)
                // Aninda Mono is not registered with the system on Apple platforms,
                // so asking for it by name would land on a silent fallback that
                // nobody would catch in a screenshot. Asking the scale's own face
                // for a fixed-width variant is honest about that: the SIZE stays on
                // the scale, and the width behaviour is whatever the platform can
                // actually supply.
                .font(AnindaFont.caption.monospaced())
                .foregroundStyle(s.inkMuted)
                .lineLimit(1)
                .truncationMode(.middle)

            Spacer(minLength: 0)

            // Only where something can actually be copied. See the note on the
            // imports at the top of the file.
            #if (canImport(UIKit) && !os(watchOS) && !os(tvOS)) || canImport(AppKit)
            Button(copied ? copiedLabel : copyLabel) { copy() }
                .buttonStyle(AnindaButtonStyle(.ordinary, small: true))
            #endif
        }
        .padding(.horizontal, AnindaSpace.s2)
        // The CSS pads this row by 4 pt and lets the small button settle the height.
        // The button here claims the comfortable 44 pt target from its own style, so
        // the head ends up taller than the stylesheet's. That is the trade I want: a
        // smaller LABEL is a design choice and a smaller TARGET is an accessibility
        // one, and the head's height is much the cheaper of the two to give up.
        .padding(.vertical, AnindaSpace.s0)
        .overlay(alignment: .bottom) {
            // `border-block-end`. A hairline, so the literal 1 the gate allows.
            Rectangle().fill(s.line).frame(height: 1)
        }
    }

    /// `.as-code__pre` — the code, scrolling sideways rather than wrapping.
    private func pre(_ s: AnindaStyle) -> some View {
        ScrollView(.horizontal) {
            Text(code)
                .font(AnindaFont.caption.monospaced())
                .foregroundStyle(s.ink)
                // A wrapped line of code stops being the line you would copy, so the
                // block scrolls instead. `fixedSize` is what stops SwiftUI folding
                // the text into the available width.
                .fixedSize(horizontal: true, vertical: false)
                .multilineTextAlignment(.leading)
                // A `<pre>` is selectable for nothing; a SwiftUI `Text` is not until
                // it is asked. Somebody who wants three lines out of twenty should
                // not have to take all twenty through the button.
                .anindaSelectableCode()
                .padding(AnindaSpace.s2)
        }
        // Clipping the scroller alone, rather than the whole block, leaves the system
        // focus ring around the copy button outside the clip. A ring cut in half is
        // worse than no ring at all for somebody navigating by keyboard.
        .clipShape(RoundedRectangle(cornerRadius: AnindaRadius.control))
    }

    /// Put the code on the pasteboard, then confirm it twice over.
    ///
    /// The button's own words change AND an announcement is posted. Neither signal
    /// is a colour: a confirmation that only recoloured something would be invisible
    /// to a reader who does not separate the two colours, and silent for one who
    /// reads the screen rather than looks at it.
    ///
    /// Compiled only where a pasteboard exists, alongside the button that calls it.
    #if (canImport(UIKit) && !os(watchOS) && !os(tvOS)) || canImport(AppKit)
    @MainActor
    private func copy() {
        #if canImport(UIKit) && !os(watchOS) && !os(tvOS)
        UIPasteboard.general.string = code
        #elseif canImport(AppKit)
        let board = NSPasteboard.general
        board.clearContents()
        board.setString(code, forType: .string)
        #endif

        copied = true
        AccessibilityNotification.Announcement(copiedLabel).post()

        // The label reverts after a moment so the button reads as an instruction
        // again rather than as a stale status. What this does not handle: a second
        // press inside those two seconds restarts nothing, so the label can revert
        // while the reader still thinks of it as fresh. The announcement fires on
        // every press regardless, and that is the signal that carries the meaning.
        Task {
            try? await Task.sleep(nanoseconds: 2_000_000_000)
            copied = false
        }
    }
    #endif
}

private extension View {
    /// `user-select` on the code, where the platform has a selection to make.
    ///
    /// `textSelection` is marked unavailable on tvOS and on watchOS, so naming it
    /// there is a build failure rather than a modifier that does nothing. Nothing
    /// is lost on either: there is no pointer to drag with and no menu to lift a
    /// selection into.
    @ViewBuilder
    func anindaSelectableCode() -> some View {
        #if os(watchOS) || os(tvOS)
        self
        #else
        self.textSelection(.enabled)
        #endif
    }
}
