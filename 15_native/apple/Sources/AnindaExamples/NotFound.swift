// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/not-found.html.

import SwiftUI
import AnindaTokens
import AnindaTokensUI
import AnindaComponents

/// A page that is not there, and two ways out of it.
///
/// Every route out is a real destination. An empty state whose only action is "go
/// back" leaves someone who arrived from a stale link with nowhere to go, which is
/// the one case this screen exists for.
public struct AnindaNotFoundScreen: View {
    private let sections = ["Cards", "Tokens", "Licence"]

    public init() {}

    public var body: some View {
        PatternPage {
            AnindaNav(axis: .horizontal) {
                ForEach(sections, id: \.self) { item in
                    Button(item) {}
                        .buttonStyle(AnindaNavItemStyle(axis: .horizontal))
                }
            }

            AnindaEmptyState(
                title: "That page is not here",
                message: "The link may be old, or the page may have been renamed. Both of these go somewhere that exists."
            ) {
                HStack(spacing: AnindaSpace.s2) {
                    Button("Go to the card index") {}
                        .buttonStyle(AnindaButtonStyle(.primary))
                    Button("Search the guidebook") {}
                        .buttonStyle(AnindaButtonStyle())
                }
            }
        }
    }
}
