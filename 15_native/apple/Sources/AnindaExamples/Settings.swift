// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/settings.html.

import SwiftUI
import AnindaTokens
import AnindaTokensUI
import AnindaComponents

/// Settings: grouped choices, and one destructive action kept away from the rest.
///
/// The four themes are a `Picker` rather than four buttons, because a picker is
/// announced as one control with a selected value — four buttons are announced as
/// four controls and the reader has to infer which is current.
///
/// Reduce Motion is shown as a row that reports the SYSTEM's setting rather than
/// as a switch this screen owns. An app-level toggle that could disagree with the
/// operating system is a second source of truth for an accessibility preference,
/// which is worse than having none.
public struct AnindaSettingsScreen: View {
    /// The four themes this system ships, in the order the guidebook lists them.
    private enum Choice: String, CaseIterable, Identifiable {
        case system, light, dark, hcLight, hcDark
        var id: String { rawValue }
        var label: String {
            switch self {
            case .system: return "Follow the system"
            case .light: return "Light"
            case .dark: return "Dark"
            case .hcLight: return "High contrast, light"
            case .hcDark: return "High contrast, dark"
            }
        }
    }

    @State private var choice: Choice = .system
    @State private var keepDrafts = true
    @State private var confirming = false
    @Environment(\.anindaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    public init() {}

    public var body: some View {
        let s = AnindaStyle(theme)
        return PatternPage {
            PatternHeading("Settings")

            AnindaCard {
                VStack(alignment: .leading, spacing: AnindaSpace.s3) {
                    PatternHeading("Appearance", font: AnindaFont.h3)

                    Picker("Theme", selection: $choice) {
                        ForEach(Choice.allCases) { c in
                            Text(c.label).tag(c)
                        }
                    }
                    .modifier(AnindaSelect())

                    HStack(alignment: .firstTextBaseline, spacing: AnindaSpace.s2) {
                        Text("Reduce motion")
                            .font(AnindaFont.body)
                            .foregroundStyle(s.ink)
                        Spacer(minLength: AnindaSpace.s1)
                        AnindaBadge(reduceMotion ? "On" : "Off",
                                    tone: reduceMotion ? .info : .neutral)
                    }
                    Text(reduceMotion
                         ? "Already on, because your system asks for it."
                         : "This follows your system setting.")
                        .font(AnindaFont.caption)
                        .foregroundStyle(s.inkMuted)
                }
            }

            AnindaCard {
                VStack(alignment: .leading, spacing: AnindaSpace.s3) {
                    PatternHeading("What I keep", font: AnindaFont.h3)
                    AnindaCheckbox("Keep unsent drafts",
                                   hint: "Drafts stay on this machine and are never sent anywhere.",
                                   isOn: $keepDrafts)
                }
            }

            AnindaCard {
                VStack(alignment: .leading, spacing: AnindaSpace.s3) {
                    PatternHeading("Deleting your account", font: AnindaFont.h3)
                    AnindaAlert(.danger,
                                title: "This cannot be undone",
                                message: "Your cards, tokens and licence records go with it.")
                    HStack(spacing: AnindaSpace.s2) {
                        Button("Delete my account") { confirming = true }
                            .buttonStyle(AnindaButtonStyle(.danger))
                        Button("Cancel the change") { confirming = false }
                            .buttonStyle(AnindaButtonStyle())
                    }
                }
            }
        }
    }
}
