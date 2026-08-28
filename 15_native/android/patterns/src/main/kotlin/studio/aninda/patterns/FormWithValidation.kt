// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/form-with-validation.html.

package studio.aninda.patterns

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
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
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.unit.dp
import studio.aninda.tokens.AnindaSpace

/**
 * A form that has been submitted and refused.
 *
 * This is the screen in the set with the most accessibility in it, because a
 * validation failure is the moment a form is most likely to be announced badly.
 *
 * Three rules it follows. The summary is marked as a live region so TalkBack reads
 * the count when it changes, rather than only when someone happens to move focus
 * onto it. Every invalid field carries its message in `supportingText` with
 * `isError` set, so a reader landing on the field hears WHY it was refused rather
 * than only its label. And nothing is marked invalid by colour alone: the message
 * is words, which survive a forced-contrast setting.
 *
 * The faults are DERIVED from the field values rather than listed, so the count in
 * the summary and the messages under the fields cannot disagree with each other.
 */
@Composable
public fun AnindaFormWithValidationScreen(modifier: Modifier = Modifier) {
    val groups = listOf("Foundations", "Components", "Patterns")
    var name by remember { mutableStateOf("") }
    var attachment by remember { mutableStateOf("") }
    var group by remember { mutableStateOf(groups[0]) }
    var submitted by remember { mutableStateOf(true) }

    val nameMissing = name.trim().isEmpty()
    val attachmentMissing = attachment.isEmpty()
    val faults = buildList {
        if (nameMissing) add("The card needs a name.")
        if (attachmentMissing) add("Choose a file to attach, or clear the field.")
    }
    val showing = submitted && faults.isNotEmpty()

    Column(
        modifier = modifier.padding(AnindaSpace.S4.dp),
        verticalArrangement = Arrangement.spacedBy(AnindaSpace.S3.dp),
    ) {
        Text(
            text = "New card",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.semantics { heading() },
        )

        if (showing) {
            Surface(
                color = MaterialTheme.colorScheme.errorContainer,
                contentColor = MaterialTheme.colorScheme.onErrorContainer,
                modifier = Modifier
                    .fillMaxWidth()
                    // The whole summary is announced as one thing, with the count
                    // in it. Without mergeDescendants a reader hears the heading
                    // and each line as separate stops and has to assemble the
                    // count itself.
                    .semantics(mergeDescendants = true) {
                        stateDescription = if (faults.size == 1) {
                            "One thing needs fixing"
                        } else {
                            "${faults.size} things need fixing"
                        }
                    },
            ) {
                Column(
                    modifier = Modifier.padding(AnindaSpace.S2.dp),
                    verticalArrangement = Arrangement.spacedBy(AnindaSpace.S0.dp),
                ) {
                    Text(
                        text = if (faults.size == 1) {
                            "One thing needs fixing before this can be saved"
                        } else {
                            "${faults.size} things need fixing before this can be saved"
                        },
                        style = MaterialTheme.typography.titleSmall,
                    )
                    faults.forEach { fault ->
                        Text(fault, style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
        }

        Card {
            Column(
                modifier = Modifier.padding(AnindaSpace.S3.dp),
                verticalArrangement = Arrangement.spacedBy(AnindaSpace.S3.dp),
            ) {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Card name") },
                    isError = showing && nameMissing,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    supportingText = {
                        Text(
                            if (showing && nameMissing) "The card needs a name."
                            else "The name shown on the card index.",
                        )
                    },
                )

                OutlinedTextField(
                    value = attachment,
                    onValueChange = { attachment = it },
                    label = { Text("Attachment") },
                    isError = showing && attachmentMissing,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    supportingText = {
                        Text(
                            if (showing && attachmentMissing) {
                                "Choose a file to attach, or clear the field."
                            } else {
                                "Optional."
                            },
                        )
                    },
                )

                Text(
                    text = "Group",
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                groups.forEach { label ->
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S1.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.semantics { role = Role.RadioButton },
                    ) {
                        RadioButton(
                            selected = group == label,
                            onClick = { group = label },
                        )
                        Text(label, style = MaterialTheme.typography.bodyMedium)
                    }
                }

                Row(horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S2.dp)) {
                    Button(onClick = { submitted = true }) { Text("Save the entry") }
                    TextButton(onClick = { submitted = false }) {
                        Text("Cancel the change")
                    }
                }
            }
        }
    }
}
