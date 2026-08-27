// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
//
// A DECLARED SURFACE, not androidx. See compose_stubs() in 15_native/build.py
// for what compiling against this does and does not prove.
//
// Declarations read from: compose-bom 1.4.0 (stable, 12 August 2026) — androidx.compose.material3 1.4.0, androidx.compose.foundation 1.4.0, androidx.compose.ui 1.4.0. Read 27 August 2026.
@file:Suppress("unused", "UNUSED_PARAMETER")

package androidx.compose.foundation.layout

import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.Dp

public class PaddingValues(public val all: Dp)

// Horizontal and Vertical are INTERFACES and spacedBy returns a type implementing
// both, which is androidx's own shape. Declaring them as classes made
// `Column(verticalArrangement = Arrangement.spacedBy(...))` a type error here while
// being perfectly correct against the real library — a stub failing valid code is
// as much a fault as one accepting invalid code.
public class Arrangement {
    public interface Horizontal
    public interface Vertical
    public interface HorizontalOrVertical : Horizontal, Vertical
    public companion object {
        public val Start: Horizontal = object : Horizontal {}
        public val End: Horizontal = object : Horizontal {}
        public val Center: HorizontalOrVertical = object : HorizontalOrVertical {}
        public val SpaceBetween: HorizontalOrVertical = object : HorizontalOrVertical {}
        public val Top: Vertical = object : Vertical {}
        public val Bottom: Vertical = object : Vertical {}
        public fun spacedBy(space: Dp): HorizontalOrVertical =
            object : HorizontalOrVertical {}
    }
}

public fun Modifier.padding(all: Dp): Modifier = this
public fun Modifier.padding(horizontal: Dp, vertical: Dp): Modifier = this
public fun Modifier.fillMaxWidth(fraction: Float = 1f): Modifier = this
public fun Modifier.fillMaxSize(fraction: Float = 1f): Modifier = this
public fun Modifier.width(width: Dp): Modifier = this
public fun Modifier.height(height: Dp): Modifier = this
public fun Modifier.heightIn(min: Dp): Modifier = this
public fun Modifier.widthIn(min: Dp): Modifier = this
public fun Modifier.defaultMinSize(minWidth: Dp, minHeight: Dp): Modifier = this
public fun Modifier.size(size: Dp): Modifier = this

// weight lives INSIDE the scopes, exactly as it does in androidx. That is what
// makes a weighted cell a compile error outside a Row or a Column, and it is the
// whole reason a table of Rows works at all.
public interface ColumnScope { public fun Modifier.weight(weight: Float): Modifier }
public interface RowScope { public fun Modifier.weight(weight: Float): Modifier }

@Composable
public fun Column(
    modifier: Modifier = Modifier,
    verticalArrangement: Arrangement.Vertical = Arrangement.Top,
    horizontalAlignment: Alignment.Horizontal = Alignment.Start,
    content: @Composable ColumnScope.() -> Unit,
) { }

@Composable
public fun Row(
    modifier: Modifier = Modifier,
    horizontalArrangement: Arrangement.Horizontal = Arrangement.Start,
    verticalAlignment: Alignment.Vertical = Alignment.Top,
    content: @Composable RowScope.() -> Unit,
) { }

@Composable
public fun Box(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit,
) { }

@Composable
public fun Spacer(modifier: Modifier = Modifier) { }
