// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/landing.html.

package studio.aninda.patterns

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import studio.aninda.tokens.AnindaSpace

/**
 * A landing page: what this is, why, and the two things to do next.
 *
 * The headline is the studio's tagline. The web card still reads "Software made
 * carefully, for two languages", which was true of a bilingual system and is not
 * true of this one; that card changes when Bangla leaves the component library,
 * and this screen is written to where the brand now is rather than to where the
 * card currently sits.
 */
@Composable
public fun AnindaLandingScreen(modifier: Modifier = Modifier) {
    val sections = listOf("Cards", "Tokens", "Licence")

    val features = listOf(
        "Measured" to
            "Every contrast ratio is read back out of a real browser, at the worst " +
            "case a rounding error can produce.",
        "Four themes" to
            "Light, dark, and a high-contrast pair. Plus a forced-contrast setting, " +
            "where every brand colour yields to the system.",
        "Two platforms" to
            "The same tokens reach SwiftUI and Jetpack Compose, and both compilers " +
            "say so rather than the documentation saying so.",
    )

    Column(
        modifier = modifier.padding(AnindaSpace.S4.dp),
        verticalArrangement = Arrangement.spacedBy(AnindaSpace.S4.dp),
    ) {
        Row(horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S1.dp)) {
            sections.forEach { item ->
                TextButton(onClick = { }) { Text(item) }
            }
        }

        Column(verticalArrangement = Arrangement.spacedBy(AnindaSpace.S2.dp)) {
            Text(
                text = "Simple apps for real life",
                style = MaterialTheme.typography.displaySmall,
                modifier = Modifier.semantics { heading() },
            )
            Text(
                text = "An openly licensed design system where nothing is asserted: " +
                    "every colour, size and contrast figure is measured or generated, " +
                    "and the build refuses itself when one is not.",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S2.dp)) {
                Button(onClick = { }) { Text("Read the guidebook") }
                OutlinedButton(onClick = { }) { Text("See the tokens") }
            }
        }

        features.forEach { (title, body) ->
            Card(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(AnindaSpace.S3.dp),
                    verticalArrangement = Arrangement.spacedBy(AnindaSpace.S0.dp),
                ) {
                    Text(
                        text = title,
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.semantics { heading() },
                    )
                    Text(
                        text = body,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}
