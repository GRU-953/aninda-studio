// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
//
// A DECLARED SURFACE, not androidx. See compose_stubs() in 15_native/build.py
// for what compiling against this does and does not prove.
//
// Declarations read from: compose-bom 1.4.0 (stable, 12 August 2026) — androidx.compose.material3 1.4.0, androidx.compose.foundation 1.4.0, androidx.compose.ui 1.4.0. Read 27 August 2026.
@file:Suppress("unused", "UNUSED_PARAMETER")

package androidx.compose.ui

public interface Modifier {
    public companion object : Modifier
}

// Alignment's nested types are separate on purpose: Row takes a Vertical and
// Column takes a Horizontal, and mixing them up is a compile error in androidx
// too. A single flat Alignment type would accept both and prove less.
public class Alignment {
    public class Vertical
    public class Horizontal
    public companion object {
        public val Top: Vertical = Vertical()
        public val CenterVertically: Vertical = Vertical()
        public val Bottom: Vertical = Vertical()
        public val Start: Horizontal = Horizontal()
        public val CenterHorizontally: Horizontal = Horizontal()
        public val End: Horizontal = Horizontal()
    }
}
