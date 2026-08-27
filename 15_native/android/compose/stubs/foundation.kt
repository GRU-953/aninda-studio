// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
//
// A DECLARED SURFACE, not androidx. See compose_stubs() in 15_native/build.py
// for what compiling against this does and does not prove.
//
// Declarations read from: compose-bom 1.4.0 (stable, 12 August 2026) — androidx.compose.material3 1.4.0, androidx.compose.foundation 1.4.0, androidx.compose.ui 1.4.0. Read 27 August 2026.
@file:Suppress("unused", "UNUSED_PARAMETER")

package androidx.compose.foundation

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.Dp

@Composable
public fun isSystemInDarkTheme(): Boolean = false

public class ScrollState(public val initial: Int)

@Composable
public fun rememberScrollState(initial: Int = 0): ScrollState = ScrollState(initial)

public fun Modifier.verticalScroll(state: ScrollState): Modifier = this
public fun Modifier.background(color: Color): Modifier = this
public fun Modifier.background(color: Color, shape: RoundedCornerShape): Modifier = this
public fun Modifier.border(width: Dp, color: Color): Modifier = this
public fun Modifier.border(width: Dp, color: Color, shape: RoundedCornerShape): Modifier = this
public fun Modifier.clip(shape: RoundedCornerShape): Modifier = this
