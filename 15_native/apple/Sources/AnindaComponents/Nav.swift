// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-nav`. Every value here
// comes from AnindaTokens, and the gate refuses this file if it contains a
// literal colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// Which way the list of destinations runs.
///
/// The CSS carries this as a `.as-nav--horizontal` modifier rather than as two
/// components, because the two share every colour and differ only in which edge
/// the current-item bar sits on. That is kept here.
public enum AnindaNavAxis: Sendable {
    /// A sidebar. The current item is marked on its leading edge.
    case vertical
    /// A bar. The current item is marked on its bottom edge.
    case horizontal
}

/// A destination in a nav, styled to this system.
///
/// It is a `ButtonStyle`, so the caller keeps a real `Button` or
/// `NavigationLink`. WRAP THE PLATFORM CONTROL, NEVER REDRAW IT: a redrawn row
/// with `.onTapGesture` looks identical and silently drops the button
/// accessibility trait, keyboard activation, Full Keyboard Access, Voice Control
/// and Switch Control that the real control has for nothing.
///
/// What it does not handle: the CSS underlines a link on hover, and SwiftUI has
/// no view-level underline to apply to an opaque `configuration.label`, so hover
/// is carried by the background change alone. Hover is a pointer state, so no
/// information lives only there.
public struct AnindaNavItemStyle: ButtonStyle {
    private let axis: AnindaNavAxis
    private let isCurrent: Bool

    public init(axis: AnindaNavAxis = .vertical, isCurrent: Bool = false) {
        self.axis = axis
        self.isCurrent = isCurrent
    }

    public func makeBody(configuration: Configuration) -> some View {
        Row(configuration: configuration, axis: axis, isCurrent: isCurrent)
    }

    // A nested view, because hover has to be held in `@State` and a `ButtonStyle`
    // is not itself a view — state declared on the style would not drive a redraw.
    // The name is `Row` rather than `Body`: `Body` is the protocol's own
    // associated type, and a private nested type of that name collides with it.
    private struct Row: View {
        let configuration: Configuration
        let axis: AnindaNavAxis
        let isCurrent: Bool

        @Environment(\.anindaTheme) private var theme
        @Environment(\.accessibilityReduceMotion) private var reduceMotion
        @State private var hovering = false

        var body: some View {
            let s = AnindaStyle(theme)
            let pressed = configuration.isPressed
            let shape = Self.shape(axis)

            return configuration.label
                // Weight, not colour. The current item says "current" three ways —
                // a bar, a heavier weight and the selected trait below — so a
                // reader who cannot separate the tint from the surface still has it.
                .font(AnindaFont.body.weight(isCurrent ? .bold : .regular))
                .foregroundStyle(s.ink)
                .padding(.horizontal, AnindaSpace.s2)
                .padding(.vertical, AnindaSpace.s0)
                // The bar's width is reserved on every item, current or not, so
                // that becoming current does not shift the label sideways.
                .padding(axis == .vertical ? .leading : .bottom, AnindaSpace.s0)
                // A smaller LABEL would be a design choice; a smaller TARGET is an
                // accessibility one, and they are different decisions. Both
                // dimensions are held at Apple's own default control size, where
                // the CSS constrains only the height.
                //
                // The width is greedy on the vertical axis and not on the
                // horizontal one, and that asymmetry is the CSS's own. The list is
                // a flex container at its default `align-items: stretch`, so in a
                // column every link is as wide as the sidebar and in a row every
                // link is as wide as its text. A SwiftUI `VStack` does not stretch
                // its children, so without this the tint and the current-item row
                // would be text-width and ragged down the sidebar — the highlight
                // stopping mid-row is the usual sign of a nav built this way.
                .frame(minWidth: AnindaTarget.comfortable,
                       maxWidth: axis == .vertical ? .infinity : nil,
                       minHeight: AnindaTarget.comfortable,
                       alignment: .leading)
                .background(shape.fill(background(s, pressed: pressed)))
                .overlay(alignment: axis == .vertical ? .leading : .bottom) {
                    marker(s)
                }
                // The pressed inset rule from the CSS. A hairline, so the literal 1
                // is the value itself rather than a size that wanted a token.
                .overlay(shape.strokeBorder(pressed ? s.ink : .clear, lineWidth: 1))
                .contentShape(shape)
                // The nearest thing Apple platforms have to aria-current="page".
                .accessibilityAddTraits(isCurrent ? [.isSelected] : [])
                .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                           value: pressed)
                .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                           value: hovering)
                .anindaHover { hovering = $0 }
        }

        /// The current-item bar.
        ///
        /// Transparent rather than absent when the item is not current, matching
        /// the CSS `border-inline-start: ... solid transparent`.
        ///
        /// The CSS bumps this bar to `--as-focus-ring-width` under a high-contrast
        /// theme. That figure is 3 pt and `AnindaSpace.s0` is 4, so honouring the
        /// bump would make the marker THINNER in the theme it was meant to
        /// strengthen. The 4 pt bar is kept in all four themes instead. This is the
        /// same call Tabs.swift makes about the same rule.
        @ViewBuilder
        private func marker(_ s: AnindaStyle) -> some View {
            let bar = Rectangle().fill(isCurrent ? s.accent : .clear)
            switch axis {
            case .vertical: bar.frame(width: AnindaSpace.s0)
            case .horizontal: bar.frame(height: AnindaSpace.s0)
            }
        }

        private func background(_ s: AnindaStyle, pressed: Bool) -> Color {
            // The CSS distinguishes three raised surfaces here: --as-surface-high
            // for current, --as-surface-highest for hover and --as-surface-dim for
            // pressed. AnindaStyle publishes one raised surface, `surfaceHigh`, so
            // all three land on it. I did not add surfaceHighest or surfaceDim,
            // because AnindaTokens is generated and a hand-added colour would be an
            // unmeasured one — the contrast figures this system publishes are
            // measured, and inventing a value here would quietly break that.
            // The cost is that hovering the current item is no longer visible; the
            // bar and the weight still are, which is why the cost is affordable.
            if pressed || isCurrent || hovering { return s.surfaceHigh }
            return .clear
        }

        /// Vertical items are square on the leading edge, where the bar runs, and
        /// rounded away from it. Horizontal items are rounded all round.
        private static func shape(_ axis: AnindaNavAxis) -> UnevenRoundedRectangle {
            switch axis {
            case .vertical:
                return UnevenRoundedRectangle(topLeadingRadius: 0,
                                              bottomLeadingRadius: 0,
                                              bottomTrailingRadius: AnindaRadius.control,
                                              topTrailingRadius: AnindaRadius.control)
            case .horizontal:
                return UnevenRoundedRectangle(topLeadingRadius: AnindaRadius.control,
                                              bottomLeadingRadius: AnindaRadius.control,
                                              bottomTrailingRadius: AnindaRadius.control,
                                              topTrailingRadius: AnindaRadius.control)
            }
        }
    }
}

public extension ButtonStyle where Self == AnindaNavItemStyle {
    static func anindaNavItem(axis: AnindaNavAxis = .vertical,
                              isCurrent: Bool = false) -> AnindaNavItemStyle {
        AnindaNavItemStyle(axis: axis, isCurrent: isCurrent)
    }
}

/// The list a set of nav destinations sits in.
///
/// This is a small view rather than a style because SwiftUI has no control that
/// corresponds to `<nav><ul>` — a `List` is a scrolling collection with its own
/// chrome and its own selection model, which is a different thing. All this does
/// is the gap, the axis and the landmark grouping; the destinations inside stay
/// real buttons.
///
/// What it does not handle: the CSS lets a horizontal nav wrap onto a second
/// line, and `HStack` does not wrap. A horizontal nav wider than its container
/// will be compressed rather than wrapped, so the vertical axis is the safer one
/// for a long list.
public struct AnindaNav<Content: View>: View {
    private let axis: AnindaNavAxis
    private let label: Text?
    private let content: Content

    public init(axis: AnindaNavAxis = .vertical,
                label: Text? = nil,
                @ViewBuilder content: () -> Content) {
        self.axis = axis
        self.label = label
        self.content = content()
    }

    public var body: some View {
        Group {
            switch axis {
            case .vertical:
                VStack(alignment: .leading, spacing: AnindaSpace.s0) { content }
            case .horizontal:
                HStack(alignment: .center, spacing: AnindaSpace.s0) { content }
            }
        }
        // `.contain` keeps each destination its own element. Flattening the nav
        // into one element would read the whole list as a single button, which is
        // the usual way a hand-built nav becomes unusable with VoiceOver.
        .accessibilityElement(children: .contain)
        .modifier(AnindaNavLabel(label: label))
    }
}

/// Applies an accessibility label when the caller gave one, and nothing when they
/// did not. An empty label would be worse than none: it names the group as
/// nothing, rather than leaving the reader to the destinations inside it.
private struct AnindaNavLabel: ViewModifier {
    let label: Text?

    func body(content: Content) -> some View {
        if let label {
            content.accessibilityLabel(label)
        } else {
            content
        }
    }
}
