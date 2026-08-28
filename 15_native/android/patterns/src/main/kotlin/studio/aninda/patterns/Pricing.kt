// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/pricing.html.

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
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import studio.aninda.tokens.AnindaSpace

/**
 * Three plans, one recommended.
 *
 * The recommended plan carries a badge AND says so in the card's own content
 * description. A tint, a ring or a raised card marks it for a sighted reader and
 * for nobody else: TalkBack moving between three cards has no way to hear which
 * one the page is pushing.
 */
@Composable
public fun AnindaPricingScreen(modifier: Modifier = Modifier) {
    data class Plan(
        val name: String,
        val price: String,
        val note: String,
        val includes: List<String>,
        val recommended: Boolean,
    )

    val plans = listOf(
        Plan("Reader", "Free", "For reading and for learning from.",
             listOf("The guidebook", "Every token", "The component cards"), false),
        Plan("Studio", "Per project", "For building something with it.",
             listOf("Everything in Reader", "The native libraries",
                    "Both store asset packages", "The Figma library"), true),
        Plan("Atelier", "Talk to me", "For a system of your own.",
             listOf("Everything in Studio", "A palette derived for your brand",
                    "The measurement harness, set up on your repository"), false),
    )

    Column(
        modifier = modifier.padding(AnindaSpace.S4.dp),
        verticalArrangement = Arrangement.spacedBy(AnindaSpace.S3.dp),
    ) {
        Text(
            text = "Plans",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.semantics { heading() },
        )

        plans.forEach { plan ->
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .semantics {
                        contentDescription = if (plan.recommended) {
                            "${plan.name}, the recommended plan"
                        } else {
                            plan.name
                        }
                    },
            ) {
                Column(
                    modifier = Modifier.padding(AnindaSpace.S3.dp),
                    verticalArrangement = Arrangement.spacedBy(AnindaSpace.S1.dp),
                ) {
                    if (plan.recommended) {
                        // A pill drawn from the primary role. Material's own Badge
                        // is for navigation counts, not for labelling a card, so a
                        // tinted Surface is the honest component for this.
                        Surface(
                            color = MaterialTheme.colorScheme.primary,
                            contentColor = MaterialTheme.colorScheme.onPrimary,
                            shape = MaterialTheme.shapes.small,
                        ) {
                            Text(
                                text = "Recommended",
                                style = MaterialTheme.typography.labelMedium,
                                modifier = Modifier.padding(
                                    AnindaSpace.S1.dp, AnindaSpace.S0.dp),
                            )
                        }
                    }
                    Text(
                        text = plan.name,
                        style = MaterialTheme.typography.titleLarge,
                        modifier = Modifier.semantics { heading() },
                    )
                    Text(plan.price, style = MaterialTheme.typography.headlineSmall)
                    Text(
                        text = plan.note,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    plan.includes.forEach { line ->
                        Row(
                            horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S1.dp),
                            verticalAlignment = Alignment.Top,
                        ) {
                            Text("•", color = MaterialTheme.colorScheme.primary)
                            Text(line, style = MaterialTheme.typography.bodyMedium)
                        }
                    }
                    if (plan.recommended) {
                        Button(onClick = { }) { Text("Choose ${plan.name}") }
                    } else {
                        OutlinedButton(onClick = { }) { Text("Choose ${plan.name}") }
                    }
                }
            }
        }
    }
}
