// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// WHY THE PATTERNS LIVE IN THEIR OWN SOURCE ROOT
// ==============================================
// The patterns are page compositions rather than components, kept OUTSIDE the
// component layer on purpose: shipping opinionated screens inside a design system
// is a different product, and a caller who wants the theme should not have to take
// the sign-in page with it.
//
// On Apple that separation is ENFORCED — SwiftPM has targets and products, so a
// caller depending on AnindaComponents never resolves AnindaExamples. Here it is
// not. There is no Gradle project and no AAR, so Android has no product boundary
// at all, and the only thing expressing the separation is this directory sitting
// beside `compose/` rather than inside it.
//
// That is STRUCTURAL INTENT, NOT AN ENFORCED BOUNDARY, and 15_native/LIMITS.md
// says so in those words. The layout is chosen so that the day a Gradle module
// exists, this root lifts into it unchanged.
//
// WHAT A PATTERN MAY USE
// ======================
// A Material composable corresponding to one of the sixteen component cards, plus
// layout, text, state and semantics. Nothing else — no icon set, no navigation
// library, no LazyColumn. The declared surface in compose/stubs contains exactly
// that and no more, so a screen reaching past it does not compile.
//
// Type comes from MaterialTheme.typography and colour from
// MaterialTheme.colorScheme, never from a literal. That is not a style preference:
// guard_authored_uses_tokens() in 15_native/build.py refuses this file if it
// carries a literal colour or a literal size.
//
// THESE SCREENS ANIMATE NOTHING. Not one of the eight declares a transition, so
// there is no reduced-motion behaviour here to get wrong. AnindaMotion carries the
// two durations and a consumer applies them; an example that animated would be
// making a decision on the consumer's behalf.

package studio.aninda.patterns

/**
 * The eight patterns, by name.
 *
 * Here so the set is stated in one place rather than inferred from the directory.
 * `scripts/check_patterns.py` holds the same eight and fails if the web, Apple and
 * Android sides ever disagree about which they are.
 */
public object AnindaPatterns {
    public val names: List<String> = listOf(
        "Sign in", "Settings", "Dashboard", "Docs page",
        "Landing", "Pricing", "Not found", "Form with validation",
    )
}
