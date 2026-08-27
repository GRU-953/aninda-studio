// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/landing.html.

import SwiftUI
import AnindaTokens
import AnindaTokensUI
import AnindaComponents

/// A landing page: what this is, why, and the two things to do next.
///
/// The headline is the studio's tagline rather than the web card's, which is a
/// deliberate difference and not a drift. The card read "Software made carefully,
/// for two languages" when this screen was written — true of a bilingual system
/// and not of this one — so the screen was written to where the brand was rather
/// than to where the card sat. The card was corrected on 28 August 2026 and now
/// reads "Software made carefully, and measured before it is claimed"; the tagline
/// here is shorter on purpose, because a phone headline has less room than a page.
public struct AnindaLandingScreen: View {
    @Environment(\.anindaTheme) private var theme

    private let sections = ["Cards", "Tokens", "Licence"]

    public init() {}

    public var body: some View {
        let s = AnindaStyle(theme)
        return PatternPage {
            AnindaNav(axis: .horizontal) {
                ForEach(sections, id: \.self) { item in
                    Button(item) {}
                        .buttonStyle(AnindaNavItemStyle(axis: .horizontal,
                                                        isCurrent: item == sections[0]))
                }
            }

            VStack(alignment: .leading, spacing: AnindaSpace.s3) {
                Text("Simple apps for real life")
                    .font(AnindaFont.display)
                    .foregroundStyle(s.ink)
                    .accessibilityAddTraits(.isHeader)

                Text("""
                     An openly licensed design system where nothing is asserted: \
                     every colour, size and contrast figure is measured or \
                     generated, and the build refuses itself when one is not.
                     """)
                    .font(AnindaFont.lead)
                    .foregroundStyle(s.inkMuted)

                HStack(spacing: AnindaSpace.s2) {
                    Button("Read the guidebook") {}
                        .buttonStyle(AnindaButtonStyle(.primary))
                    Button("See the tokens") {}
                        .buttonStyle(AnindaButtonStyle())
                }
            }

            LazyVGrid(columns: [GridItem(.adaptive(minimum: AnindaSpace.s9),
                                         spacing: AnindaSpace.s3)],
                      spacing: AnindaSpace.s3) {
                feature(s, "Measured",
                        "Every contrast ratio is read back out of a real browser, at the worst case a rounding error can produce.")
                feature(s, "Four themes",
                        "Light, dark, and a high-contrast pair. Plus forced-colours mode, where every brand colour yields to the system.")
                feature(s, "Two platforms",
                        "The same tokens reach SwiftUI and Jetpack Compose, and both compilers say so rather than the documentation saying so.")
            }
        }
    }

    private func feature(_ s: AnindaStyle, _ title: String,
                         _ body: String) -> some View {
        AnindaCard {
            VStack(alignment: .leading, spacing: AnindaSpace.s1) {
                Text(title)
                    .font(AnindaFont.h3)
                    .foregroundStyle(s.ink)
                    .accessibilityAddTraits(.isHeader)
                Text(body)
                    .font(AnindaFont.body)
                    .foregroundStyle(s.inkMuted)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
    }
}
