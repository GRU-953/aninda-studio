// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-alert` and its four
// variants. Every value here comes from AnindaTokens, and the gate refuses this
// file if it contains a literal colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// The four alert variants the CSS defines.
///
/// The bare `.as-alert` — neutral line, muted glyph — is not exposed as a case.
/// An alert with no status is a paragraph in a box, and the CSS keeps that shape
/// only as the base the four variants inherit from.
public enum AnindaAlertTone: Sendable {
    case success
    case warning
    case danger
    case info
}

/// A banner that reports the outcome of something.
///
/// This is a `View` rather than a style or a modifier, and that is the exception
/// to the rule elsewhere in this library rather than a departure from it. SwiftUI
/// has no in-flow banner control to wrap: `.alert` is a modal sheet, which
/// interrupts the reader and cannot sit inside a form. There is nothing here to
/// inherit behaviour from, so drawing it loses nothing. Where SwiftUI does own the
/// control — a button, a toggle, a field — this library styles the real one.
///
/// The tone is never carried by colour alone. Each variant has its own symbol
/// shape, and that symbol carries a spoken word for VoiceOver, so the status
/// survives both a monochrome display and a reader who never sees the banner.
public struct AnindaAlert: View {
    private let tone: AnindaAlertTone
    private let title: String
    private let message: String?
    @Environment(\.anindaTheme) private var theme

    public init(_ tone: AnindaAlertTone, title: String, message: String? = nil) {
        self.tone = tone
        self.title = title
        self.message = message
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        let edge = accent(s)
        return HStack(alignment: .top, spacing: AnindaSpace.s2) {
            Image(systemName: symbolName)
                .font(AnindaFont.lead)
                .foregroundStyle(edge)
                // The symbol IS the status for a sighted reader, so it has to be
                // the status for a listening one too. An empty label here would
                // hand VoiceOver the title with no indication of what went wrong.
                .accessibilityLabel(Text(spokenTone))
            VStack(alignment: .leading, spacing: AnindaSpace.s0) {
                Text(title)
                    .font(AnindaFont.body.weight(.bold))
                    .foregroundStyle(s.ink)
                if let message {
                    Text(message)
                        .font(AnindaFont.body)
                        .foregroundStyle(s.ink)
                }
            }
            // Long prose in a narrow column has to wrap rather than push the
            // banner wider; this is the `min-width: 0` of the CSS body element.
            .frame(maxWidth: .infinity, alignment: .leading)
            .fixedSize(horizontal: false, vertical: true)
        }
        .padding(AnindaSpace.s3)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(RoundedRectangle(cornerRadius: AnindaRadius.control).fill(s.surfaceHigh))
        // `border-inline-start-width: var(--as-space-0)` in the CSS. `.leading`
        // rather than `.left`, so a right-to-left layout moves the bar with the
        // text instead of stranding it on the wrong side.
        .overlay(alignment: .leading) {
            Rectangle()
                .fill(edge)
                .frame(width: AnindaSpace.s0)
        }
        .clipShape(RoundedRectangle(cornerRadius: AnindaRadius.control))
        .overlay(
            RoundedRectangle(cornerRadius: AnindaRadius.control)
                .strokeBorder(edge, lineWidth: 1)
        )
        // Read as one announcement. Split across three elements, VoiceOver makes
        // the reader swipe through a symbol, a heading and a sentence to learn
        // one fact.
        .accessibilityElement(children: .combine)
        // There is no minimum height here on purpose. An alert is not a target —
        // nothing in it is tappable — and padding a static banner out to 44pt
        // would be the accessibility rule applied where it does not hold. A
        // dismiss control or an inline action added later WOULD need it, and
        // this component does not yet offer either.
    }

    private func accent(_ s: AnindaStyle) -> Color {
        switch tone {
        case .success: return s.success
        case .warning: return s.warning
        case .danger: return s.danger
        case .info: return s.info
        }
    }

    /// Four distinct silhouettes, not four tints of one. A reader who cannot
    /// separate red from green still separates an octagon from a circle.
    private var symbolName: String {
        switch tone {
        case .success: return "checkmark.circle.fill"
        case .warning: return "exclamationmark.triangle.fill"
        case .danger: return "xmark.octagon.fill"
        case .info: return "info.circle.fill"
        }
    }

    /// English only, and knowingly so. This library has no string catalogue yet,
    /// and inventing one here would place the translations of four words in a
    /// component file rather than where the rest of the copy will live.
    private var spokenTone: String {
        switch tone {
        case .success: return "Success"
        case .warning: return "Warning"
        case .danger: return "Error"
        case .info: return "Information"
        }
    }
}
