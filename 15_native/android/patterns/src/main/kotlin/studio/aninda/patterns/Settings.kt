// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/settings.html.

package studio.aninda.patterns

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.Checkbox
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import studio.aninda.tokens.AnindaSpace

/**
 * Settings: grouped choices, and one destructive action kept away from the rest.
 *
 * The four themes are radio buttons carrying `Role.RadioButton`, so TalkBack
 * announces each as one of a set with one selected. Five plain buttons would be
 * announced as five unrelated controls and the reader would have to infer which
 * is current.
 */
@Composable
public fun AnindaSettingsScreen(modifier: Modifier = Modifier) {
    val choices = listOf(
        "Follow the system", "Light", "Dark",
        "High contrast, light", "High contrast, dark",
    )
    var chosen by remember { mutableStateOf(choices[0]) }
    var keepDrafts by remember { mutableStateOf(true) }

    Column(
        modifier = modifier.padding(AnindaSpace.S4.dp),
        verticalArrangement = Arrangement.spacedBy(AnindaSpace.S4.dp),
    ) {
        Text(
            text = "Settings",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.semantics { heading() },
        )

        Card {
            Column(
                modifier = Modifier.padding(AnindaSpace.S3.dp),
                verticalArrangement = Arrangement.spacedBy(AnindaSpace.S2.dp),
            ) {
                Text(
                    text = "Appearance",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.semantics { heading() },
                )
                choices.forEach { label ->
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S1.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.semantics { role = Role.RadioButton },
                    ) {
                        RadioButton(
                            selected = chosen == label,
                            onClick = { chosen = label },
                        )
                        Text(label, style = MaterialTheme.typography.bodyMedium)
                    }
                }
            }
        }

        Card {
            Column(
                modifier = Modifier.padding(AnindaSpace.S3.dp),
                verticalArrangement = Arrangement.spacedBy(AnindaSpace.S2.dp),
            ) {
                Text(
                    text = "What I keep",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.semantics { heading() },
                )
                Row(
                    horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S1.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Checkbox(checked = keepDrafts, onCheckedChange = { keepDrafts = it })
                    Column {
                        Text("Keep unsent drafts",
                             style = MaterialTheme.typography.bodyMedium)
                        Text(
                            text = "Drafts stay on this device and are never sent anywhere.",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            }
        }

        HorizontalDivider()

        Card {
            Column(
                modifier = Modifier.padding(AnindaSpace.S3.dp),
                verticalArrangement = Arrangement.spacedBy(AnindaSpace.S2.dp),
            ) {
                Text(
                    text = "Deleting your account",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.semantics { heading() },
                )
                // The warning is a Surface tinted with the error container role,
                // not a red border. In a forced-contrast setting a border colour
                // can be replaced; the WORDS cannot.
                Surface(
                    color = MaterialTheme.colorScheme.errorContainer,
                    contentColor = MaterialTheme.colorScheme.onErrorContainer,
                ) {
                    Column(modifier = Modifier.padding(AnindaSpace.S2.dp)) {
                        Text("This cannot be undone",
                             style = MaterialTheme.typography.titleSmall)
                        Text("Your cards, tokens and licence records go with it.",
                             style = MaterialTheme.typography.bodySmall)
                    }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S2.dp)) {
                    Button(onClick = { }) { Text("Delete my account") }
                    TextButton(onClick = { }) { Text("Cancel the change") }
                }
            }
        }
    }
}
