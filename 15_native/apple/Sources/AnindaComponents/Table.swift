// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-table`. Every value here
// comes from AnindaTokens, and the gate refuses this file if it contains a literal
// colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// How one column reads.
public enum AnindaTableColumnKind: Sendable {
    /// Text, aligned to the start of the line.
    case text
    /// A figure, aligned to the end of the line and set with tabular digits so
    /// the columns of digits line up down the table.
    case numeric
}

/// One column heading.
public struct AnindaTableColumn: Sendable {
    public let title: String
    public let kind: AnindaTableColumnKind

    public init(_ title: String, kind: AnindaTableColumnKind = .text) {
        self.title = title
        self.kind = kind
    }
}

/// One row of already-formatted cells.
///
/// The cells are strings, not values, because formatting a number is a decision
/// about locale and precision that belongs to the caller. A table that formatted
/// on the caller's behalf would quietly impose one answer on every app using it.
public struct AnindaTableRow: Identifiable, Sendable {
    public let id: String
    public let cells: [String]

    /// - Parameter id: stable across reloads. Row position is NOT identity: using
    ///   the index would re-use a row's animation and accessibility focus for
    ///   whatever data slid into that slot after a sort.
    public init(id: String, cells: [String]) {
        self.id = id
        self.cells = cells
    }
}

/// A static table of text, styled to this system.
///
/// WHY THIS IS A VIEW AND NOT A WRAPPED `SwiftUI.Table`
/// ---------------------------------------------------
/// The house rule is to wrap the platform control rather than redraw it, and I
/// have followed that rule everywhere it earns its keep — a redrawn Toggle or
/// Button throws away the accessibility trait, keyboard activation, Voice Control
/// and Switch Control that the real one carries. `SwiftUI.Table` is the exception,
/// and here is the trade-off I made.
///
/// `SwiftUI.Table` is a selectable, sortable, column-resizable data control. On
/// macOS that is a lot of behaviour worth inheriting; on iOS 17 it degrades to its
/// first column in compact widths, which silently deletes data from the reader's
/// screen. The CSS reference is not that control: `.as-table` has no selection, no
/// sort and no resizing, so none of the behaviour I would be inheriting exists to
/// be lost. What is left is a grid of text, and `Grid` renders that identically on
/// both platforms.
///
/// The cost is real and I am stating it: this view carries no table trait, so
/// VoiceOver does not offer row-and-column navigation over it. I pay that back per
/// cell — each cell announces its own column heading — which reads correctly in a
/// linear swipe but is not the same affordance. If you need selection, sorting or
/// true table semantics on macOS, use `SwiftUI.Table` directly; this view is for
/// presenting figures, not for operating on them.
public struct AnindaTable: View {
    private let caption: String?
    private let columns: [AnindaTableColumn]
    private let rows: [AnindaTableRow]
    @Environment(\.anindaTheme) private var theme

    /// - Parameter caption: describes the table for a reader who arrives at it out
    ///   of context. Optional, but a table without one is a table nobody can cite.
    public init(caption: String? = nil,
                columns: [AnindaTableColumn],
                rows: [AnindaTableRow]) {
        self.caption = caption
        self.columns = columns
        self.rows = rows
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        return VStack(alignment: .leading, spacing: 0) {
            if let caption {
                Text(caption)
                    .font(AnindaFont.caption)
                    .foregroundStyle(s.inkMuted)
                    .padding(.bottom, AnindaSpace.s1)
            }
            // Spacing is 0 in both axes because the rules are drawn as hairlines
            // between rows, exactly as `border-collapse: collapse` does. A grid gap
            // would put a stripe of page colour where the CSS puts a line.
            Grid(alignment: .topLeading, horizontalSpacing: 0, verticalSpacing: 0) {
                GridRow {
                    ForEach(Array(columns.enumerated()), id: \.offset) { _, column in
                        cell(column.title, column: column, s: s, heading: true)
                    }
                }
                rule(s)
                ForEach(Array(rows.enumerated()), id: \.element.id) { index, row in
                    GridRow {
                        ForEach(Array(columns.enumerated()), id: \.offset) { i, column in
                            // Read once and used twice. A row shorter than the
                            // header is padded rather than dropped, and working
                            // that out separately for the visible text and for the
                            // spoken one is how the two drift apart.
                            let value = i < row.cells.count ? row.cells[i] : ""
                            cell(value, column: column, s: s, heading: false)
                                // The heading is spoken with the value because the
                                // grid gives VoiceOver no column context of its own.
                                // Not `Text(...)`: an interpolated `Text` is a
                                // localisation key, and cell data is not a key.
                                .accessibilityLabel(column.title + ", " + value)
                        }
                    }
                    // `tbody tr:last-child` drops its rule in the CSS: the last line
                    // would read as a border round a table that has no border.
                    if index < rows.count - 1 { rule(s) }
                }
            }
        }
    }

    @ViewBuilder
    private func cell(_ text: String,
                      column: AnindaTableColumn,
                      s: AnindaStyle,
                      heading: Bool) -> some View {
        // A heading is bold AND sits on a raised surface. Either alone would do the
        // job for most readers; the pair is what keeps the header row findable for
        // someone who cannot separate the two surface tones by colour.
        //
        // The CSS sets `white-space: nowrap` on headings and on numeric cells and
        // this does not, deliberately. On the web a nowrap cell widens the table;
        // here it would either truncate the figure or push the row off the screen
        // once the reader raises their Dynamic Type size, and a figure the reader
        // cannot see is worse than a figure that wraps.
        Text(text)
            .font(numericFont(column, heading: heading))
            .foregroundStyle(s.ink)
            // `th` is a heading on the web and the rotor is the equivalent here:
            // without the trait a VoiceOver reader has no way to reach the header
            // row except by swiping through every cell above it.
            .accessibilityAddTraits(heading ? [.isHeader] : [])
            .multilineTextAlignment(column.kind == .numeric ? .trailing : .leading)
            .padding(.vertical, AnindaSpace.s1)
            .padding(.horizontal, AnindaSpace.s2)
            .frame(maxWidth: .infinity,
                   alignment: column.kind == .numeric ? .topTrailing : .topLeading)
            .background(heading ? s.surfaceHigh : Color.clear)
    }

    private func numericFont(_ column: AnindaTableColumn, heading: Bool) -> Font {
        let base = heading ? AnindaFont.body.weight(.bold) : AnindaFont.body
        // The CSS sets `--as-font-mono` on numeric cells. There is no mono family in
        // AnindaTokens, and I have not added one: a font family is a design decision
        // for the whole system, not something a single component should introduce.
        // `monospacedDigit()` delivers the part that matters here — tabular figures,
        // so the columns of digits align — in the system's own face.
        return column.kind == .numeric ? base.monospacedDigit() : base
    }

    @ViewBuilder
    private func rule(_ s: AnindaStyle) -> some View {
        // Not `Divider()`: its colour comes from the platform separator, which would
        // ignore the theme this table is drawn in. 1 is a hairline, not a size.
        Rectangle()
            .fill(s.line)
            .frame(height: 1)
            .gridCellUnsizedAxes(.horizontal)
            .gridCellColumns(max(columns.count, 1))
    }
}
