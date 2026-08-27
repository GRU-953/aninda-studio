// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/dashboard.html.

package studio.aninda.patterns

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import studio.aninda.tokens.AnindaSpace

/**
 * A build report: summary figures, then the rows behind them.
 *
 * The table is a `Column` of `Row`s with weighted cells, not a LazyColumn and not
 * a grid component. Four rows is a fixed-length example, and `weight` inside
 * `RowScope` is what keeps the columns aligned down the table — which is the only
 * thing a table layout actually has to do.
 *
 * Every figure is stated as an example on the page. A dashboard full of plausible
 * numbers is the easiest screen in this set to mistake for a live reading.
 */
@Composable
public fun AnindaDashboardScreen(modifier: Modifier = Modifier) {
    val ranges = listOf("This week", "This month", "This quarter")
    var range by remember { mutableStateOf(0) }

    val rows = listOf(
        Triple("Lint", "11", "Passed"),
        Triple("Tokens", "4", "Passed"),
        Triple("Marks", "5", "Passed"),
        Triple("Rendered and measured", "3", "Passed"),
    )

    Column(
        modifier = modifier.padding(AnindaSpace.S4.dp),
        verticalArrangement = Arrangement.spacedBy(AnindaSpace.S3.dp),
    ) {
        Row(
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text(
                text = "Build report",
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier.semantics { heading() },
            )
            Button(onClick = { }) { Text("Run the check") }
        }

        Surface(
            color = MaterialTheme.colorScheme.secondaryContainer,
            contentColor = MaterialTheme.colorScheme.onSecondaryContainer,
        ) {
            Column(modifier = Modifier.padding(AnindaSpace.S2.dp)) {
                Text("Example figures, not a live reading",
                     style = MaterialTheme.typography.titleSmall)
                Text("This screen is a layout in a design system. Nothing here queried anything.",
                     style = MaterialTheme.typography.bodySmall)
            }
        }

        TabRow(selectedTabIndex = range) {
            ranges.forEachIndexed { i, label ->
                Tab(
                    selected = range == i,
                    onClick = { range = i },
                    text = { Text(label) },
                )
            }
        }

        Row(horizontalArrangement = Arrangement.spacedBy(AnindaSpace.S2.dp)) {
            summary("Gates", "40")
            summary("Passing", "40")
            summary("Open gaps", "6")
        }

        Card {
            Column(modifier = Modifier.padding(AnindaSpace.S2.dp)) {
                headerRow()
                HorizontalDivider()
                rows.forEach { (check, gates, outcome) ->
                    Row(modifier = Modifier.padding(AnindaSpace.S0.dp, AnindaSpace.S1.dp)) {
                        cell(check, WIDE)
                        cell(gates, NARROW)
                        cell(outcome, NARROW)
                    }
                }
                Text(
                    text = "Every gate group in the last run.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(AnindaSpace.S1.dp),
                )
            }
        }
    }
}

// Column weights. Named rather than repeated as bare numbers, because a weight is
// a RATIO and not a size — the size guard allows it, and a reader still deserves to
// be told which column is the wide one.
private const val WIDE = 2f
private const val NARROW = 1f

@Composable
private fun headerRow() {
    Row(modifier = Modifier.padding(AnindaSpace.S0.dp, AnindaSpace.S1.dp)) {
        headerCell("Check", WIDE)
        headerCell("Gates", NARROW)
        headerCell("Outcome", NARROW)
    }
}

@Composable
private fun summary(label: String, value: String) {
    Card {
        Column(modifier = Modifier.padding(AnindaSpace.S2.dp)) {
            Text(label, style = MaterialTheme.typography.labelMedium,
                 color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(value, style = MaterialTheme.typography.headlineSmall)
        }
    }
}

// `weight` is declared INSIDE RowScope, in the stub and in androidx alike, so a
// cell helper has to be an extension on that scope. It cannot be a plain function
// taking a Modifier: the weight would have nowhere to come from. That constraint
// is the reason a table works at all here.
@Composable
private fun RowScope.cell(text: String, weight: Float) {
    Text(
        text = text,
        style = MaterialTheme.typography.bodyMedium,
        modifier = Modifier.weight(weight),
    )
}

@Composable
private fun RowScope.headerCell(text: String, weight: Float) {
    Text(
        text = text,
        style = MaterialTheme.typography.labelLarge,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        modifier = Modifier.weight(weight),
    )
}
