// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/dashboard.html.

import SwiftUI
import AnindaTokens
import AnindaTokensUI
import AnindaComponents

/// A build report: summary figures, then the rows behind them.
///
/// The table is `AnindaTable`, never SwiftUI's `Table`. Table.swift's own doc
/// comment argues that case: it is a macOS-shaped control that degrades to its
/// first column in compact iOS widths, "which silently deletes data from the
/// reader's screen". A dashboard is exactly where that would happen.
///
/// The figures are stated as an example, on the card, because a dashboard full of
/// plausible numbers is the easiest screen in this set to mistake for a real
/// reading.
public struct AnindaDashboardScreen: View {
    private enum Range: String, CaseIterable, Identifiable {
        case week, month, quarter
        var id: String { rawValue }
        var label: String {
            switch self {
            case .week: return "This week"
            case .month: return "This month"
            case .quarter: return "This quarter"
            }
        }
    }

    @State private var range: Range = .week
    @Environment(\.anindaTheme) private var theme

    private let columns = [
        AnindaTableColumn("Check"),
        AnindaTableColumn("Gates", kind: .numeric),
        AnindaTableColumn("Outcome"),
    ]

    private let rows = [
        AnindaTableRow(id: "lint", cells: ["Lint", "11", "Passed"]),
        AnindaTableRow(id: "tokens", cells: ["Tokens", "4", "Passed"]),
        AnindaTableRow(id: "marks", cells: ["Marks", "5", "Passed"]),
        AnindaTableRow(id: "render", cells: ["Rendered and measured", "3", "Passed"]),
    ]

    public init() {}

    public var body: some View {
        let s = AnindaStyle(theme)
        return PatternPage {
            HStack(alignment: .firstTextBaseline, spacing: AnindaSpace.s2) {
                PatternHeading("Build report")
                Spacer(minLength: AnindaSpace.s1)
                Button("Run the check") {}
                    .buttonStyle(AnindaButtonStyle(.primary, small: true))
            }

            AnindaAlert(.info,
                        title: "Example figures, not a live reading",
                        message: "This screen is a layout in a design system. Nothing here queried anything.")

            Picker("Filter the rows", selection: $range) {
                ForEach(Range.allCases) { r in Text(r.label).tag(r) }
            }
            .modifier(AnindaSelect())

            LazyVGrid(columns: [GridItem(.adaptive(minimum: AnindaSpace.s9),
                                         spacing: AnindaSpace.s3)],
                      spacing: AnindaSpace.s3) {
                summary(s, "Gates", "40", .accent)
                summary(s, "Passing", "40", .success)
                summary(s, "Open gaps", "6", .warning)
                summary(s, "Blockers", "1", .danger)
            }

            AnindaTable(caption: "Every gate group in the last run.",
                        columns: columns, rows: rows)
        }
    }

    /// One figure, its label, and a badge that carries the same meaning in a word.
    ///
    /// The badge is why this is not colour alone: in forced-colours mode every
    /// status colour resolves to one system colour, so a green tile and a red tile
    /// become the same tile. The word survives that.
    private func summary(_ s: AnindaStyle, _ label: String, _ value: String,
                         _ tone: AnindaBadgeTone) -> some View {
        AnindaCard(padding: .tight, elevation: .flat) {
            VStack(alignment: .leading, spacing: AnindaSpace.s1) {
                Text(label)
                    .font(AnindaFont.caption)
                    .foregroundStyle(s.inkMuted)
                Text(value)
                    .font(AnindaFont.h2)
                    .foregroundStyle(s.ink)
                AnindaBadge(label, tone: tone)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
    }
}
