// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-toast`, its glyph, body,
// title, text and dismiss parts, and the three tone modifiers. Every value here
// comes from AnindaTokens, and the gate refuses this file if it carries a literal
// colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// The tones the stylesheet gives a toast.
///
/// The bare `.as-toast` — a muted glyph, no status — is the `.neutral` case, and
/// unlike the alert it IS exposed here, because a toast that reports "Copied" has
/// no status to report and the stylesheet keeps that shape for it.
public enum AnindaToastTone: Sendable {
    case neutral
    case success
    case danger
    case info
}

/// A short, transient message about something that has finished.
///
/// This is a `View` rather than a style or a modifier, and that is the same
/// exception the alert makes. SwiftUI has no toast control to wrap — the nearest
/// thing, `.alert`, is a modal sheet that takes the keyboard and demands an answer,
/// which is the opposite of what a toast is for. Where SwiftUI DOES own the control
/// this library styles the real one, and the dismiss control below is a real
/// `Button` with a `ButtonStyle` for exactly that reason: a redrawn button with an
/// `.onTapGesture` looks the same and loses the button trait, keyboard activation,
/// Full Keyboard Access, Voice Control and Switch Control.
///
/// The tone is never carried by colour alone. Each tone has its own symbol shape,
/// and that symbol carries a spoken word, so the status survives a monochrome
/// display and a reader who never sees the toast.
///
/// What this does NOT handle, deliberately:
///   - Presentation, stacking and timing. A toast that shows itself, queues behind
///     another and retires after a few seconds is a presentation concern, and
///     putting a timer in here would give every caller the same one. The caller
///     owns when this appears and when it goes.
///   - The announcement. There is no live-region equivalent in SwiftUI on macOS 14
///     and iOS 17, so a toast that appears silently stays silent for VoiceOver
///     unless the caller posts an announcement at the moment it presents it. This
///     is the one thing a caller must remember to do.
///   - `inline-size: min(100%, 380px)`. I wanted the 380 pt cap and there is no
///     token for it; the nearest constant that exists is `AnindaSpace.s9` at 128 pt,
///     which is not a usable stand-in for a text width, so the toast fills the width
///     it is given and the caller frames it. Adding a token is a change to the
///     generator, not to a component.
public struct AnindaToast: View {
    private let tone: AnindaToastTone
    private let title: String
    private let message: String?
    private let onDismiss: (() -> Void)?
    @Environment(\.anindaTheme) private var theme

    public init(_ tone: AnindaToastTone = .neutral,
                title: String,
                message: String? = nil,
                onDismiss: (() -> Void)? = nil) {
        self.tone = tone
        self.title = title
        self.message = message
        self.onDismiss = onDismiss
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        return HStack(alignment: .top, spacing: AnindaSpace.s2) {
            // The glyph and the two lines are one announcement, so they are one
            // element. The grouping is this inner row rather than the whole toast,
            // because combining the whole would swallow the dismiss button and
            // leave a reader no way to close it. The row repeats the outer row's
            // spacing, so the three parts sit exactly where they did before.
            HStack(alignment: .top, spacing: AnindaSpace.s2) {
                Image(systemName: symbolName)
                    .font(AnindaFont.lead)
                    .foregroundStyle(glyph(s))
                    // The symbol IS the status for a sighted reader, so it has to
                    // be the status for a listening one too.
                    .accessibilityLabel(Text(spokenTone))
                VStack(alignment: .leading, spacing: AnindaSpace.s0) {
                    Text(title)
                        .font(AnindaFont.body.weight(.bold))
                        .foregroundStyle(s.ink)
                    if let message {
                        Text(message)
                            .font(AnindaFont.caption)
                            .foregroundStyle(s.inkMuted)
                    }
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                // Long prose in a narrow toast has to wrap rather than push it
                // wider; this is the `min-width: 0` of the CSS body element.
                .fixedSize(horizontal: false, vertical: true)
            }
            .accessibilityElement(children: .combine)
            if let onDismiss {
                Button(action: onDismiss) {
                    Image(systemName: "xmark")
                        .font(AnindaFont.body)
                }
                .buttonStyle(AnindaToastDismissStyle())
                .accessibilityLabel(Text("Dismiss"))
            }
        }
        .padding(.vertical, AnindaSpace.s2)
        .padding(.horizontal, AnindaSpace.s3)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(RoundedRectangle(cornerRadius: AnindaRadius.control).fill(s.surface))
        .overlay(
            RoundedRectangle(cornerRadius: AnindaRadius.control)
                .strokeBorder(s.line, lineWidth: 1)
        )
        // The border is drawn in every theme, and it is what gives the toast its
        // edge where the shadow is switched off. A toast that floats above the page
        // by shadow alone would merge into the page in high contrast.
        .modifier(AnindaToastShadow(theme: theme))
    }

    /// `.as-toast--success/--danger/--info` tint only the glyph; the fill and the
    /// border stay neutral. Copying that keeps the toast quiet, which is the point
    /// of a toast, and leaves the shape and the spoken word to carry the status.
    private func glyph(_ s: AnindaStyle) -> Color {
        switch tone {
        case .neutral: return s.inkMuted
        case .success: return s.success
        case .danger: return s.danger
        case .info: return s.info
        }
    }

    /// Four distinct silhouettes, not four tints of one. A reader who cannot
    /// separate red from green still separates an octagon from a circle.
    private var symbolName: String {
        switch tone {
        case .neutral: return "bell.fill"
        case .success: return "checkmark.circle.fill"
        case .danger: return "xmark.octagon.fill"
        case .info: return "info.circle.fill"
        }
    }

    /// English only, and knowingly so. This library has no string catalogue yet,
    /// and inventing one here would put the translations of four words in a
    /// component file rather than where the rest of the copy will live.
    private var spokenTone: String {
        switch tone {
        case .neutral: return "Notice"
        case .success: return "Success"
        case .danger: return "Error"
        case .info: return "Information"
        }
    }
}

/// `.as-toast__dismiss` — transparent until touched, then a fill and a border.
///
/// A `ButtonStyle` on a real `Button`, so the whole of the platform's button
/// behaviour is inherited rather than rebuilt.
private struct AnindaToastDismissStyle: ButtonStyle {
    @Environment(\.anindaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    func makeBody(configuration: Configuration) -> some View {
        let s = AnindaStyle(theme)
        let pressed = configuration.isPressed
        return configuration.label
            .foregroundStyle(s.ink)
            // The CSS asks for `--as-target-min`, 24 pt. I have used 44 instead:
            // the house rule is that an interactive target is at least
            // `AnindaTarget.comfortable` in both dimensions, and a finger has no
            // hover state to find a 24 pt cross with. The GLYPH stays small, which
            // is the design decision; the TARGET does not, which is the
            // accessibility one.
            .frame(minWidth: AnindaTarget.comfortable,
                   minHeight: AnindaTarget.comfortable)
            .background(
                RoundedRectangle(cornerRadius: AnindaRadius.badge)
                    // `:active` in the CSS fills with `--as-surface-dim`, turns the
                    // border to ink, and adds an inset ink ring on top of that.
                    // `AnindaStyle` publishes no dim surface, so the pressed fill
                    // is `surfaceHigh`, the nearest tinted surface it does publish,
                    // and the ink border is kept. What is dropped is the inset
                    // ring: at one point wide and the same ink, it draws the edge
                    // the border already draws.
                    .fill(pressed ? s.surfaceHigh : .clear)
            )
            .overlay(
                RoundedRectangle(cornerRadius: AnindaRadius.badge)
                    .strokeBorder(pressed ? s.ink : .clear, lineWidth: 1)
            )
            .contentShape(RoundedRectangle(cornerRadius: AnindaRadius.badge))
            .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                       value: pressed)
    }
}

/// The float shadow, drawn only in the theme that publishes one.
///
/// `--as-shadow-float` is `none` in the dark theme and in both high-contrast
/// themes. Reading the theme rather than always drawing keeps the four themes
/// matching the stylesheet. This repeats the card's shadow rather than sharing it,
/// because the card's copy is `private` to its own file and promoting it to public
/// API is a decision about the library's surface, not about this component.
///
/// There is no shadow token in AnindaTokens — that file is generated, so adding one
/// is a change to the generator. I wanted the CSS pair `0 1px 2px rgb(0 0 0 / 0.06)`
/// and `0 8px 24px rgb(0 0 0 / 0.08)`. The blur radii map to half their CSS values,
/// because SwiftUI's radius is a standard deviation where CSS's is a blur diameter:
/// 2 becomes 1, and 24 becomes `AnindaSpace.s2`. The colour is `s.ink` at those
/// opacities rather than pure black, which the gate refuses — in the light theme
/// ink is a near-black and the difference is below what 6 and 8 per cent can show.
private struct AnindaToastShadow: ViewModifier {
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
