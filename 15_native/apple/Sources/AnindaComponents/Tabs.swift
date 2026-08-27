// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-tabs`, `.as-tab` and
// `.as-tabpanel`. Every value here comes from AnindaTokens, and the gate refuses
// this file if it contains a literal colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// One tab in a strip.
public struct AnindaTabItem<Value: Hashable>: Identifiable {
    public let id: Value
    public let title: String
    public init(_ id: Value, _ title: String) {
        self.id = id
        self.title = title
    }
}

/// A strip of tabs bound to a selection.
///
/// WHY THIS IS A VIEW AND NOT A STYLE
/// ==================================
/// The house rule is to wrap the platform control rather than redraw it, and I
/// have followed it as far as the platform allows. SwiftUI's `TabView` is not
/// the same control: it owns the panels, the paging and the animation, and it
/// cannot be repainted into this strip without redrawing it anyway.
/// `Picker(.segmented)` is a different affordance with a different meaning. So
/// there is no platform tab strip to wrap, and this is a small View instead.
///
/// What I did NOT redraw is each tab: every one is a real `Button`, so the
/// accessibility trait, keyboard activation, Full Keyboard Access, Voice
/// Control and Switch Control all arrive for nothing. A row of shapes carrying
/// `.onTapGesture` would look the same and have none of them.
///
/// WHAT THIS DOES NOT HANDLE
/// - Roving arrow-key movement between tabs. Tab-key focus works because these
///   are real buttons; left and right arrow do not move the selection.
/// - The CSS strip wraps onto a second line when it runs out of room. This one
///   scrolls horizontally instead, because a wrapped row on a phone hides the
///   fact that there is more to see, and a scroll view at least offers a
///   scroller and a flick.
public struct AnindaTabs<Value: Hashable>: View {
    private let items: [AnindaTabItem<Value>]
    @Binding private var selection: Value
    @Environment(\.anindaTheme) private var theme

    public init(selection: Binding<Value>, items: [AnindaTabItem<Value>]) {
        self._selection = selection
        self.items = items
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        return ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: AnindaSpace.s0) {
                ForEach(items) { item in
                    Button(item.title) { selection = item.id }
                        .buttonStyle(AnindaTabButtonStyle(selected: selection == item.id))
                        // The trait is what makes a screen reader say "selected".
                        // The underline, the weight and the ink colour are the
                        // three signals a sighted reader gets, and only one of
                        // them is a colour — a tab is never marked by hue alone.
                        .accessibilityAddTraits(selection == item.id ? [.isSelected] : [])
                }
            }
        }
        // The hairline the whole strip sits on. 1 is a hairline, not a size the
        // system chose, which is why the gate allows it.
        //
        // BEHIND the row rather than over it. In the CSS the strip's
        // border-block-end and the selected tab's own border-block-end are two
        // separate edges, and nothing paints over the tab's 4 pt accent. As an
        // overlay this hairline drew the line colour across the bottom quarter of
        // that marker on whichever tab was selected. As a background it shows
        // through every unselected tab — their fill is transparent — and the
        // selected tab's marker covers it, which is what the CSS does.
        .background(alignment: .bottom) {
            Rectangle().fill(s.line).frame(height: 1)
        }
    }
}

/// The look of a single tab.
public struct AnindaTabButtonStyle: ButtonStyle {
    private let selected: Bool
    public init(selected: Bool) { self.selected = selected }

    public func makeBody(configuration: Configuration) -> some View {
        TabBody(selected: selected, configuration: configuration)
    }

    /// A nested view because hover is state, and a `ButtonStyle` cannot hold any.
    private struct TabBody: View {
        let selected: Bool
        let configuration: Configuration
        @Environment(\.anindaTheme) private var theme
        @Environment(\.accessibilityReduceMotion) private var reduceMotion
        @State private var hovered = false

        var body: some View {
            let s = AnindaStyle(theme)
            let pressed = configuration.isPressed
            return configuration.label
                .font(AnindaFont.body.weight(selected ? .bold : .regular))
                .foregroundStyle(selected || hovered || pressed ? s.ink : s.inkMuted)
                .padding(.horizontal, AnindaSpace.s3)
                .padding(.vertical, AnindaSpace.s1)
                // Both dimensions, on every tab. A tab's label is short and the
                // temptation is to let the target shrink with it; a smaller
                // LABEL is a design choice and a smaller TARGET is an
                // accessibility one, and they are not the same decision.
                .frame(minWidth: AnindaTarget.comfortable,
                       minHeight: AnindaTarget.comfortable)
                .background(
                    // Only the top corners are rounded, because the tab meets
                    // the strip's hairline along its bottom edge.
                    UnevenRoundedRectangle(
                        topLeadingRadius: AnindaRadius.control,
                        bottomLeadingRadius: 0,
                        bottomTrailingRadius: 0,
                        topTrailingRadius: AnindaRadius.control
                    )
                    .fill(fill(s, pressed: pressed))
                )
                // The pressed inset outline the CSS draws with box-shadow. An
                // overlay border is the nearest honest equivalent; SwiftUI has
                // no inner shadow.
                .overlay(
                    UnevenRoundedRectangle(
                        topLeadingRadius: AnindaRadius.control,
                        bottomLeadingRadius: 0,
                        bottomTrailingRadius: 0,
                        topTrailingRadius: AnindaRadius.control
                    )
                    .strokeBorder(pressed ? s.ink : .clear, lineWidth: 1)
                )
                // The selected marker. The CSS underline is --as-space-0 thick,
                // so AnindaSpace.s0 is the same 4 pt and not an approximation.
                // I wanted the high-contrast bump the CSS makes to
                // --as-focus-ring-width as well, but that value is THINNER than
                // s0 here, so applying it would weaken the marker rather than
                // strengthen it; the strong theme keeps the 4 pt line instead.
                .overlay(alignment: .bottom) {
                    Rectangle()
                        .fill(selected ? s.accent : .clear)
                        .frame(height: AnindaSpace.s0)
                }
                .contentShape(Rectangle())
                .anindaHover { hovered = $0 }
                .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                           value: pressed)
                .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                           value: hovered)
        }

        // The CSS reaches for --as-surface-highest on hover and --as-surface-dim
        // on press. BOTH EXIST in AnindaTokens — AnindaPalette carries
        // surfaceHighest and surfaceDim, measured like every other role. What
        // does not exist is an accessor for either on AnindaStyle, which
        // publishes one raised surface, `surfaceHigh`, so both land on it.
        // Widening that surface is a change to AnindaTokensUI rather than to a
        // component, which is why it is not made from here; CodeBlock and Nav
        // resolve the same gap the same way. The cost is that hover and press
        // are indistinguishable to a pointer. Neither carries information on its
        // own, so the cost is affordable.
        private func fill(_ s: AnindaStyle, pressed: Bool) -> Color {
            if pressed || hovered { return s.surfaceHigh }
            return .clear
        }
    }
}


public extension View {
    /// The panel a tab reveals: `.as-tabpanel`, which is spacing and nothing else.
    func anindaTabPanel() -> some View {
        padding(.top, AnindaSpace.s3)
    }
}
