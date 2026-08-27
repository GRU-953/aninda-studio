// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
//
// A DECLARED SURFACE, not androidx. See compose_stubs() in 15_native/build.py
// for what compiling against this does and does not prove.
//
// Declarations read from: compose-bom 1.4.0 (stable, 12 August 2026) — androidx.compose.material3 1.4.0, androidx.compose.foundation 1.4.0, androidx.compose.ui 1.4.0. Read 27 August 2026.
@file:Suppress("unused", "UNUSED_PARAMETER")

package androidx.compose.ui.semantics

import androidx.compose.ui.Modifier

// A heading announced as one. The web cards are MEASURED for this; these screens
// are not measured for it by anything, which is stated in LIMITS.md rather than
// implied by the declaration existing.
public class SemanticsPropertyReceiver {
    public var contentDescription: String = ""
    public var stateDescription: String = ""
    public var role: Role? = null
}

// An extension function at package level, which is how androidx declares it — so
// it is IMPORTED rather than reached through the receiver. Declaring it as a
// member compiled here and would have failed against the real library.
public fun SemanticsPropertyReceiver.heading() { }

public class Role {
    public companion object {
        public val Button: Role = Role()
        public val Checkbox: Role = Role()
        public val RadioButton: Role = Role()
        public val Tab: Role = Role()
    }
}

public fun Modifier.semantics(
    mergeDescendants: Boolean = false,
    properties: SemanticsPropertyReceiver.() -> Unit,
): Modifier = this

public fun Modifier.clearAndSetSemantics(
    properties: SemanticsPropertyReceiver.() -> Unit,
): Modifier = this
