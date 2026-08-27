// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/not-found.html.

package studio.aninda.patterns

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
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
 * A page that is not there, and two ways out of it.
 *
 * Every route out is a real destination. An empty state whose only action is "go
 * back" leaves someone who arrived from a stale link with nowhere to go, which is
 * the one case this screen exists for.
 */
@Composable
public fun AnindaNotFoundScreen(modifier: Modifier = Modifier) {
    val sections = listOf("Cards", "Tokens", "Licence")

    Column(
        modifier = modifier.padding(AnindaSpace.S4.dp),
        verticalArrangement = Arrangement.spacedBy(AnindaSpace.S4.dp),
        horizontalAlignment = Alignment.Start,
    ) {
        Row(horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S1.dp)) {
            sections.forEach { item ->
                TextButton(onClick = { }) { Text(item) }
            }
        }

        Column(verticalArrangement = Arrangement.spacedBy(AnindaSpace.S2.dp)) {
            Text(
                text = "That page is not here",
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier.semantics { heading() },
            )
            Text(
                text = "The link may be old, or the page may have been renamed. " +
                    "Both of these go somewhere that exists.",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S2.dp)) {
                Button(onClick = { }) { Text("Go to the card index") }
                OutlinedButton(onClick = { }) { Text("Search the guidebook") }
            }
        }
    }
}
