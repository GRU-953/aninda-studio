// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/docs-page.html.

import SwiftUI
import AnindaTokens
import AnindaTokensUI
import AnindaComponents

/// A documentation page: where you are, what is on this page, and the page.
///
/// The two-column layout is `ViewThatFits` rather than `NavigationSplitView`. A
/// split view is unavailable on watchOS and meaningless on tvOS, so using it would
/// make this screen's claim to five platforms conditional. `ViewThatFits` takes the
/// two-column arrangement when there is room and the stacked one when there is not,
/// which is the same decision a media query makes on the web card.
public struct AnindaDocsPageScreen: View {
    @Environment(\.anindaTheme) private var theme

    private let trail = [
        AnindaBreadcrumbItem("Guidebook", action: {}),
        AnindaBreadcrumbItem("Foundations", action: {}),
    ]

    private let onThisPage = [
        "Why the ring is offset",
        "What the ring must clear",
        "Where it comes from",
    ]

    public init() {}

    public var body: some View {
        PatternPage {
            AnindaBreadcrumb(trail: trail, current: "Focus")

            ViewThatFits(in: .horizontal) {
                HStack(alignment: .top, spacing: AnindaSpace.s5) {
                    contents
                        .frame(maxWidth: .infinity, alignment: .leading)
                    prose
                        .frame(maxWidth: .infinity, alignment: .leading)
                }
                VStack(alignment: .leading, spacing: AnindaSpace.s4) {
                    contents
                    prose
                }
            }
        }
    }

    private var contents: some View {
        AnindaNav(axis: .vertical, label: Text("On this page")) {
            ForEach(onThisPage, id: \.self) { item in
                Button(item) {}
                    .buttonStyle(AnindaNavItemStyle(axis: .vertical,
                                                    isCurrent: item == onThisPage[0]))
            }
        }
    }

    private var prose: some View {
        let s = AnindaStyle(theme)
        return VStack(alignment: .leading, spacing: AnindaSpace.s3) {
            PatternHeading("Focus")

            Text("""
                 The focus ring sits outside the control it belongs to, with a gap \
                 between them. The gap is what makes the ring legible on a control \
                 whose own edge is already a line.
                 """)
                .font(AnindaFont.body)
                .foregroundStyle(s.ink)

            PatternHeading("Why the ring is offset", font: AnindaFont.h3)

            Text("""
                 A ring drawn on the border replaces the border rather than adding \
                 to it, so a focused control and an unfocused one differ by colour \
                 alone. Offsetting it means focus adds a mark, and a mark survives \
                 forced-colours mode where a colour does not.
                 """)
                .font(AnindaFont.body)
                .foregroundStyle(s.ink)

            AnindaAlert(.info,
                        title: "Where the figures come from",
                        message: "The ring width and its offset are tokens, measured in a real browser and re-measured on every build.")

            AnindaCodeBlock(name: "focus.css", code: """
                .as-btn:focus-visible {
                  outline: var(--as-focus-ring-width) solid var(--as-focus-ring);
                  outline-offset: var(--as-focus-ring-offset);
                }
                """)
        }
    }
}
