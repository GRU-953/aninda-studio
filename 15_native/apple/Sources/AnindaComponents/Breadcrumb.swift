// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/src/components.css `.as-breadcrumb`. Every value
// here comes from AnindaTokens, and the gate refuses this file if it contains a
// literal colour or a literal size.

import SwiftUI
import AnindaTokens
import AnindaTokensUI

/// One ancestor step in a trail: the words on it, and what happens when it is
/// chosen.
///
/// There is no `isCurrent` flag. The current page is a separate argument to
/// `AnindaBreadcrumb`, so a trail cannot be built with two current pages or with
/// none — the CSS can only ask for `aria-current="page"` on the last item and
/// hope, whereas a type can refuse the other shapes outright.
public struct AnindaBreadcrumbItem: Identifiable, Sendable {
    public let id: UUID
    public let label: String
    public let action: @MainActor @Sendable () -> Void

    public init(_ label: String,
                action: @escaping @MainActor @Sendable () -> Void) {
        self.id = UUID()
        self.label = label
        self.action = action
    }
}

/// The trail of ancestors above the page a reader is on.
///
/// This is a `View` and not a style, for the same reason the badge is: SwiftUI
/// has no breadcrumb control to wrap, so there is no platform behaviour to lose
/// by drawing one. The parts that ARE platform controls stay platform controls —
/// each ancestor is a real `Button`, so the accessibility trait, keyboard
/// activation, Full Keyboard Access, Voice Control and Switch Control all come
/// for nothing. A `Text` with `.onTapGesture` would look identical and reach
/// none of those readers.
///
/// Colour is never the only signal, per rule 7: an ancestor is underlined as
/// well as accent-coloured, and the current page is bold as well as ink. Turn
/// the whole thing greyscale and the trail still reads correctly.
///
/// What this does NOT handle: the labels are not shortened. A single step longer
/// than the container overruns it rather than truncating, because a path segment
/// with its end cut off is a worse failure than one that overhangs — the same
/// trade-off the badge makes. Trails of unbounded depth are the caller's problem
/// to elide before they arrive here.
public struct AnindaBreadcrumb: View {
    private let trail: [AnindaBreadcrumbItem]
    private let current: String

    @Environment(\.anindaTheme) private var theme

    /// - Parameters:
    ///   - trail: the ancestors, outermost first. May be empty, which leaves the
    ///     current page standing alone.
    ///   - current: the page the reader is on. Required, so the trail always ends
    ///     somewhere.
    public init(trail: [AnindaBreadcrumbItem], current: String) {
        self.trail = trail
        self.current = current
    }

    public var body: some View {
        let s = AnindaStyle(theme)
        return AnindaBreadcrumbRow(gap: AnindaSpace.s0) {
            ForEach(trail) { item in
                // The link and the separator after it are ONE child of the
                // wrapping row, matching `.as-breadcrumb__item` in the CSS, which
                // holds both inside a single flex child. Handed to the row
                // separately they wrap separately, and a line can then open with a
                // stranded stroke above the label it belongs to.
                HStack(spacing: CGFloat(AnindaSpace.s0)) {
                    Button(action: item.action) { Text(item.label) }
                        .buttonStyle(AnindaBreadcrumbLinkStyle())
                    Text(verbatim: "/")
                        .font(AnindaFont.caption)
                        .foregroundStyle(s.inkMuted)
                        // The separator is punctuation, not content. A screen
                        // reader that voices it reads "Home slash Work slash
                        // Notes", which is noise on top of an announcement that is
                        // already ordered.
                        .accessibilityHidden(true)
                }
            }
            Text(current)
                .font(AnindaFont.caption.weight(.bold))
                .foregroundStyle(s.ink)
                .padding(.horizontal, AnindaSpace.s0)
                // Matching `min-height: var(--as-target-min)` in the CSS. The
                // current page is not a target — it does nothing when tapped — so
                // rule 6's 44 pt does not apply to it, and forcing it there would
                // make the row taller for no one's benefit.
                .frame(minHeight: AnindaTarget.min)
                // `aria-current="page"` has no SwiftUI counterpart. Saying it in
                // the label is the closest honest equivalent; the bold weight
                // already carries it for a reader who can see the row. This
                // string is English only — the system has no localisation
                // surface yet, and inventing one here would put it in the wrong
                // place.
                .accessibilityLabel(Text("\(current), current page"))
        }
        // One container, announced as a group, so a reader hears where they are
        // rather than meeting six loose buttons.
        .accessibilityElement(children: .contain)
        .accessibilityLabel(Text("Breadcrumb"))
    }
}

/// The ancestor link.
///
/// A `ButtonStyle` rather than a wrapper view, so the caller keeps the real
/// `Button` underneath.
private struct AnindaBreadcrumbLinkStyle: ButtonStyle {
    @Environment(\.anindaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    func makeBody(configuration: Configuration) -> some View {
        // Hover needs state, and a `ButtonStyle` has none. The nested view is what
        // gives `@State` somewhere to live; `:hover` in the CSS is a macOS and
        // iPadOS-pointer state only, and it stays absent on touch, which is
        // correct rather than missing.
        LinkBody(configuration: configuration,
                 theme: theme,
                 reduceMotion: reduceMotion)
    }

    private struct LinkBody: View {
        let configuration: ButtonStyleConfiguration
        let theme: AnindaTheme
        let reduceMotion: Bool

        @State private var hovering = false

        var body: some View {
            let s = AnindaStyle(theme)
            let pressed = configuration.isPressed
            return configuration.label
                .font(AnindaFont.caption)
                // `text-decoration: underline`, and it is load-bearing: it is the
                // second signal that marks an ancestor as reachable when the
                // accent colour is not available to the reader.
                .underline()
                .foregroundStyle(pressed || hovering ? s.ink : s.accent)
                .padding(.horizontal, AnindaSpace.s0)
                // The CSS asks for `--as-target-min`, 24 pt, which clears WCAG 2.2
                // SC 2.5.8. Rule 6 asks for 44 pt in both dimensions, which is
                // Apple's own default control size, and on a hand-held device the
                // stricter figure is the one that matters. The cost is a taller
                // row than the web shows for the same trail; a small LABEL is a
                // design choice and a small TARGET is an accessibility one, so the
                // caption type stays and the target grows.
                .frame(minWidth: AnindaTarget.comfortable,
                       minHeight: AnindaTarget.comfortable)
                .background(
                    // A plain rectangle, because the CSS gives this no radius.
                    // Rounding it would look more at home on Apple and would put
                    // the two platforms out of step over a hover highlight, which
                    // is not a trade worth making.
                    Rectangle()
                        .fill(pressed || hovering ? s.surfaceHigh : Color.clear)
                )
                .overlay(
                    // `box-shadow: inset 0 0 0 1px var(--as-ink)` on `:active`.
                    Rectangle()
                        .strokeBorder(pressed ? s.ink : Color.clear, lineWidth: 1)
                )
                .contentShape(Rectangle())
                .anindaHover { hovering = $0 }
                .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                           value: pressed)
                .animation(AnindaAnimation.colour(reduceMotion: reduceMotion),
                           value: hovering)
        }
    }
}


/// A row that wraps onto a second line when it runs out of width.
///
/// `flex-wrap: wrap` has no modifier equivalent, so it is a `Layout`. The
/// alternative was a single `HStack` that overflows or scrolls, and a trail that
/// silently pushes its last step off the edge is the one failure a breadcrumb
/// cannot afford — the last step is the one saying where the reader is.
///
/// What this does NOT handle: items are aligned to the top of their line rather
/// than centred within it. Every child here is one line of caption text at the
/// same height, so the difference does not arise; it would if somebody put a
/// taller view in.
private struct AnindaBreadcrumbRow: Layout {
    /// Named `gap` rather than `spacing`, matching the CSS property it comes from.
    var gap: Double

    func sizeThatFits(proposal: ProposedViewSize,
                      subviews: Subviews,
                      cache: inout ()) -> CGSize {
        arrange(subviews: subviews, maxWidth: proposal.width ?? .infinity).size
    }

    func placeSubviews(in bounds: CGRect,
                       proposal: ProposedViewSize,
                       subviews: Subviews,
                       cache: inout ()) {
        let placed = arrange(subviews: subviews, maxWidth: bounds.width)
        for (index, subview) in subviews.enumerated() {
            let origin = placed.origins[index]
            subview.place(at: CGPoint(x: bounds.minX + origin.x,
                                      y: bounds.minY + origin.y),
                          anchor: .topLeading,
                          proposal: .unspecified)
        }
    }

    /// Walks the children once, breaking to a new line when the next one would
    /// cross the right edge. Measured at `.unspecified` because each child is a
    /// word or a stroke that should be asked for its natural width, not squeezed.
    private func arrange(subviews: Subviews,
                         maxWidth: CGFloat) -> (size: CGSize, origins: [CGPoint]) {
        let step = CGFloat(gap)
        var origins: [CGPoint] = []
        var x: CGFloat = 0
        var y: CGFloat = 0
        var lineHeight: CGFloat = 0
        var widest: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            // `x > 0` keeps the first item on its line even when it alone is wider
            // than the container. Wrapping it would move it nowhere and leave an
            // empty line above it.
            if x > 0, x + size.width > maxWidth {
                x = 0
                y += lineHeight + step
                lineHeight = 0
            }
            origins.append(CGPoint(x: x, y: y))
            x += size.width + step
            widest = max(widest, x - step)
            lineHeight = max(lineHeight, size.height)
        }

        return (CGSize(width: widest, height: y + lineHeight), origins)
    }
}
