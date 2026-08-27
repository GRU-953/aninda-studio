// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/docs-page.html.

package studio.aninda.patterns

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import studio.aninda.tokens.AnindaSpace

/**
 * A documentation page: where you are, what is on this page, and the page.
 *
 * The breadcrumb's last item is plain text, not a button. A trail whose current
 * page is a control invites someone to activate the page they are already on, and
 * TalkBack announces it as somewhere to go.
 *
 * The contents list and the prose are stacked rather than placed side by side.
 * There is no `ViewThatFits` in Compose and no width to branch on without reading
 * the window size, which needs a dependency this module does not carry — so the
 * single-column arrangement is the one that is always correct, and the shortfall
 * against the web card's two-column layout is stated in LIMITS.md.
 */
@Composable
public fun AnindaDocsPageScreen(modifier: Modifier = Modifier) {
    val onThisPage = listOf(
        "Why the ring is offset",
        "What the ring must clear",
        "Where it comes from",
    )

    Column(
        modifier = modifier.padding(AnindaSpace.S4.dp),
        verticalArrangement = Arrangement.spacedBy(AnindaSpace.S3.dp),
    ) {
        Row(
            horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S1.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            TextButton(onClick = { }) { Text("Guidebook") }
            Text("/", color = MaterialTheme.colorScheme.onSurfaceVariant)
            TextButton(onClick = { }) { Text("Foundations") }
            Text("/", color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text("Focus", style = MaterialTheme.typography.bodyMedium)
        }

        Column(verticalArrangement = Arrangement.spacedBy(AnindaSpace.S0.dp)) {
            Text(
                text = "On this page",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            onThisPage.forEach { item ->
                TextButton(onClick = { }, modifier = Modifier.fillMaxWidth()) {
                    Text(item)
                }
            }
        }

        Text(
            text = "Focus",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.semantics { heading() },
        )

        Text(
            text = "The focus ring sits outside the control it belongs to, with a " +
                "gap between them. The gap is what makes the ring legible on a " +
                "control whose own edge is already a line.",
            style = MaterialTheme.typography.bodyLarge,
        )

        Text(
            text = "Why the ring is offset",
            style = MaterialTheme.typography.titleMedium,
            modifier = Modifier.semantics { heading() },
        )

        Text(
            text = "A ring drawn on the border replaces the border rather than " +
                "adding to it, so a focused control and an unfocused one differ by " +
                "colour alone. Offsetting it means focus adds a mark, and a mark " +
                "survives a forced-contrast setting where a colour does not.",
            style = MaterialTheme.typography.bodyLarge,
        )

        Surface(
            color = MaterialTheme.colorScheme.secondaryContainer,
            contentColor = MaterialTheme.colorScheme.onSecondaryContainer,
        ) {
            Column(modifier = Modifier.padding(AnindaSpace.S2.dp)) {
                Text("Where the figures come from",
                     style = MaterialTheme.typography.titleSmall)
                Text("The ring width and its offset are tokens, measured in a real " +
                     "browser and re-measured on every build.",
                     style = MaterialTheme.typography.bodySmall)
            }
        }

        // A code sample. The monospace face is not applied here: AnindaType is not
        // emitted to Kotlin, so a font family would have to be a literal, and the
        // token guard refuses that — correctly. Recorded as a follow-up in
        // LIMITS.md rather than worked around.
        Surface(
            color = MaterialTheme.colorScheme.surfaceContainerHighest,
            contentColor = MaterialTheme.colorScheme.onSurface,
        ) {
            Text(
                text = ".as-btn:focus-visible {\n" +
                    "  outline: var(--as-focus-ring-width) solid var(--as-focus-ring);\n" +
                    "  outline-offset: var(--as-focus-ring-offset);\n" +
                    "}",
                style = MaterialTheme.typography.bodySmall,
                modifier = Modifier.padding(AnindaSpace.S2.dp),
            )
        }
    }
}
