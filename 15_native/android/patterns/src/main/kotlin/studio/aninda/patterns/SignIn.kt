// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/sign-in.html.

package studio.aninda.patterns

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.Checkbox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import studio.aninda.tokens.AnindaSpace

/**
 * Signing in: two fields, one primary action, and a way out that is not a dead end.
 *
 * The sign-in-link route is a `TextButton` rather than a link, because on a form
 * the alternative is an ACTION. TalkBack announces a button as a button, and a
 * caller hearing "link" would expect to leave the page.
 */
@Composable
public fun AnindaSignInScreen(modifier: Modifier = Modifier) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var stayed by remember { mutableStateOf(false) }

    Card(modifier = modifier.padding(AnindaSpace.S3.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(AnindaSpace.S3.dp)) {
            Text(
                text = "Sign in",
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier.semantics { heading() },
            )

            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email address") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
            )

            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
            )

            Row(
                horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S1.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Checkbox(checked = stayed, onCheckedChange = { stayed = it })
                Column {
                    Text("Keep me signed in", style = MaterialTheme.typography.bodyMedium)
                    Text(
                        text = "Only on a machine you trust.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }

            Button(onClick = { }, modifier = Modifier.fillMaxWidth()) {
                Text("Sign in")
            }

            TextButton(onClick = { }) {
                Text("Send me a sign-in link instead")
            }
        }
    }
}
