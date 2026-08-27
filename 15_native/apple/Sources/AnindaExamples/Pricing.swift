// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/pricing.html.

import SwiftUI
import AnindaTokens
import AnindaTokensUI
import AnindaComponents

/// Three plans, one recommended.
///
/// The recommended plan is marked with a solid badge AND named in the card's
/// accessibility label. A ring, a tint or a raised card marks it for a sighted
/// reader and for nobody else; a screen reader moving between three cards has no
/// way to hear which one the page is pushing.
public struct AnindaPricingScreen: View {
    private struct Plan: Identifiable {
        let id: String
        let price: String
        let note: String
        let includes: [String]
        let recommended: Bool
    }

    @Environment(\.anindaTheme) private var theme

    private let plans = [
        Plan(id: "Reader", price: "Free", note: "For reading and for learning from.",
             includes: ["The guidebook", "Every token", "The component cards"],
             recommended: false),
        Plan(id: "Studio", price: "Per project", note: "For building something with it.",
             includes: ["Everything in Reader", "The native libraries",
                        "Both store asset packages", "The Figma library"],
             recommended: true),
        Plan(id: "Atelier", price: "Talk to me", note: "For a system of your own.",
             includes: ["Everything in Studio", "A palette derived for your brand",
                        "The measurement harness, set up on your repository"],
             recommended: false),
    ]

    public init() {}

    public var body: some View {
        PatternPage {
            PatternHeading("Plans")

            LazyVGrid(columns: [GridItem(.adaptive(minimum: AnindaSpace.s9),
                                         spacing: AnindaSpace.s3)],
                      alignment: .leading, spacing: AnindaSpace.s3) {
                ForEach(plans) { plan in
                    card(plan)
                }
            }
        }
    }

    private func card(_ plan: Plan) -> some View {
        let s = AnindaStyle(theme)
        return AnindaCard {
            VStack(alignment: .leading, spacing: AnindaSpace.s2) {
                if plan.recommended {
                    AnindaBadge("Recommended", tone: .accent, solid: true)
                }
                Text(plan.id)
                    .font(AnindaFont.h3)
                    .foregroundStyle(s.ink)
                    .accessibilityAddTraits(.isHeader)
                Text(plan.price)
                    .font(AnindaFont.h2)
                    .foregroundStyle(s.ink)
                Text(plan.note)
                    .font(AnindaFont.caption)
                    .foregroundStyle(s.inkMuted)

                VStack(alignment: .leading, spacing: AnindaSpace.s1) {
                    ForEach(plan.includes, id: \.self) { line in
                        HStack(alignment: .firstTextBaseline, spacing: AnindaSpace.s1) {
                            // A bullet, marked as decoration so it is not read out
                            // before every line.
                            Text("•")
                                .foregroundStyle(s.accent)
                                .accessibilityHidden(true)
                            Text(line)
                                .font(AnindaFont.body)
                                .foregroundStyle(s.ink)
                        }
                    }
                }

                Button("Choose \(plan.id)") {}
                    .buttonStyle(AnindaButtonStyle(plan.recommended ? .primary : .ordinary))
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .accessibilityElement(children: .contain)
        .accessibilityLabel(plan.recommended
                            ? "\(plan.id), the recommended plan"
                            : plan.id)
    }
}
