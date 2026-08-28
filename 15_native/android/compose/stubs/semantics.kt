// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
//
// A DECLARED SURFACE, not androidx. See compose_stubs() in 15_native/build.py
// for what compiling against this does and does not prove.
//
// Declarations read from: compose-bom 1.4.0 (stable, 12 August 2026) — androidx.compose.material3 1.4.0, androidx.compose.foundation 1.4.0, androidx.compose.ui 1.4.0. Read 27 August 2026.
@file:Suppress("unused", "UNUSED_PARAMETER")

package androidx.compose.ui.semantics

import androidx.compose.ui.Modifier

// The receiver carries NOTHING. Every semantics property androidx defines is an
// EXTENSION at package level, so each one is imported separately — and a screen
// that forgets an import does not compile.
//
// contentDescription, stateDescription and role were MEMBERS of this class until
// 28 August 2026, which meant they needed no import and the receiver resolved them
// for free. The note under heading() already said, twelve lines below, exactly why
// that is wrong; it was written for heading() and not applied upward.
//
// The real library refused all three: GitHub Actions run 33118789482, job
// native-android, four errors and no others —
//
//   e: patterns/.../FormWithValidation.kt:86:25 Unresolved reference 'stateDescription'.
//   e: patterns/.../FormWithValidation.kt:159:57 Unresolved reference 'role'.
//   e: patterns/.../Pricing.kt:70:25 Unresolved reference 'contentDescription'.
//   e: patterns/.../Settings.kt:75:57 Unresolved reference 'role'.
//
// Correcting them here moves that failure OFF a remote branch gate and onto the
// local kotlinc compile, which is the whole point: a surface that accepts what the
// library refuses is worse than no surface, because it reports success.
public class SemanticsPropertyReceiver

// A heading announced as one. The web cards are MEASURED for this; these screens
// are not measured for it by anything, which is stated in LIMITS.md rather than
// implied by the declaration existing.
//
// An extension at package level, which is how androidx declares it — so it is
// IMPORTED rather than reached through the receiver. Declaring it as a member
// compiled here and would have failed against the real library.
public fun SemanticsPropertyReceiver.heading() { }

// The three that were members. An extension property can carry no backing field,
// so each states a getter and a setter that do nothing; this surface exists to be
// compiled against and never to run.
public var SemanticsPropertyReceiver.contentDescription: String
    get() = ""
    set(value) { }

public var SemanticsPropertyReceiver.stateDescription: String
    get() = ""
    set(value) { }

public var SemanticsPropertyReceiver.role: Role
    get() = Role.Button
    set(value) { }

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
