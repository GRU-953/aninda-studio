// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
//
// A DECLARED SURFACE, not androidx. See compose_stubs() in 15_native/build.py
// for what compiling against this does and does not prove.
//
// Declarations read from: compose-bom 1.4.0 (stable, 12 August 2026) — androidx.compose.material3 1.4.0, androidx.compose.foundation 1.4.0, androidx.compose.ui 1.4.0. Read 27 August 2026.
@file:Suppress("unused", "UNUSED_PARAMETER")

package androidx.compose.ui.unit

public class Dp(public val value: Float)
public val Int.dp: Dp get() = Dp(this.toFloat())
public val Float.dp: Dp get() = Dp(this)

public class TextUnit(public val value: Float)
public val Float.sp: TextUnit get() = TextUnit(this)
public val Int.sp: TextUnit get() = TextUnit(this.toFloat())
