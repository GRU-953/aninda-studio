// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/form-with-validation.html.

import SwiftUI
import AnindaTokens
import AnindaTokensUI
import AnindaComponents

/// A form that has been submitted and refused.
///
/// This is the screen in the set with the most accessibility in it, and the reason
/// is that a validation failure is the moment a form is most likely to be
/// announced badly.
///
/// Three rules it follows. The summary is a live region, so the count is announced
/// when it changes rather than only when someone happens to move focus onto it.
/// Every invalid field carries its message as its OWN accessibility value, not
/// only as text beside it, because a reader landing on the field would otherwise
/// hear the label and nothing about why it was refused. And nothing is marked
/// invalid by colour alone — `AnindaInput` draws a message and the field takes an
/// error skin, which both survive forced-colours mode.
public struct AnindaFormWithValidationScreen: View {
    private enum Group: String, CaseIterable, Identifiable {
        case foundations = "Foundations"
        case components = "Components"
        case patterns = "Patterns"
        var id: String { rawValue }
    }

    @State private var name = ""
    @State private var attachment = ""
    @State private var group: Group = .foundations
    @State private var submitted = true
    @Environment(\.anindaTheme) private var theme

    public init() {}

    /// The two faults, derived rather than listed, so the count and the messages
    /// cannot disagree with each other.
    private var faults: [String] {
        var out: [String] = []
        if name.trimmingCharacters(in: .whitespaces).isEmpty {
            out.append("The card needs a name.")
        }
        if attachment.isEmpty {
            out.append("Choose a file to attach, or clear the field.")
        }
        return out
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        let showing = submitted && !faults.isEmpty
        return PatternPage {
            PatternHeading("New card")

            if showing {
                AnindaAlert(.danger,
                            title: faults.count == 1
                                ? "One thing needs fixing before this can be saved"
                                : "\(faults.count) things need fixing before this can be saved",
                            message: faults.joined(separator: " "))
                    .accessibilityAddTraits(.isSummaryElement)
                    // `.updatesFrequently` is as close as SwiftUI comes to the
                    // web's aria-live. It is NOT the same thing: it tells
                    // VoiceOver the element changes, it does not announce the
                    // change. A real live region needs
                    // AccessibilityNotification.Announcement posted when the
                    // count moves, which belongs to whatever owns the submit — an
                    // example screen posting announcements would fire them in a
                    // preview. The shortfall is recorded in 15_native/LIMITS.md
                    // rather than papered over here.
                    .accessibilityAddTraits(.updatesFrequently)
            }

            AnindaCard {
                VStack(alignment: .leading, spacing: AnindaSpace.s3) {
                    AnindaInput("Card name",
                                hint: "The name shown on the card index.",
                                error: showing && name.trimmingCharacters(in: .whitespaces).isEmpty
                                       ? "The card needs a name." : nil) {
                        TextField("", text: $name)
                            .modifier(AnindaInputSkin(
                                invalid: showing && name.trimmingCharacters(in: .whitespaces).isEmpty))
                    }

                    AnindaInput("Attachment",
                                optionalText: "optional",
                                error: showing && attachment.isEmpty
                                       ? "Choose a file to attach, or clear the field." : nil) {
                        TextField("", text: $attachment)
                            .modifier(AnindaInputSkin(invalid: showing && attachment.isEmpty))
                    }

                    AnindaInput("Group") {
                        Picker("Group", selection: $group) {
                            ForEach(Group.allCases) { g in Text(g.rawValue).tag(g) }
                        }
                        .modifier(AnindaSelect())
                    }

                    HStack(spacing: AnindaSpace.s2) {
                        Button("Save the entry") { submitted = true }
                            .buttonStyle(AnindaButtonStyle(.primary))
                        Button("Cancel the change") { submitted = false }
                            .buttonStyle(AnindaButtonStyle(.quiet))
                    }
                }
            }
            .foregroundStyle(s.ink)
        }
    }
}
