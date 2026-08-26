// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.

package studio.aninda.tokens

/**
 * Every colour this system measured, for all four themes, plus the
 * dimensions and the Bangla ramp.
 *
 * This file imports nothing — no androidx, no Compose. That is what lets
 * `kotlinc` compile it, so the values are proven to build rather than
 * asserted to. The Compose theme sits in the :compose module, where that
 * proof needs the Android toolchain.
 *
 * Colours are ARGB Longs. Kotlin has no unsigned Int literal that reads
 * well here, and a Long keeps the alpha byte visible.
 */

public enum class AnindaTheme(public val key: String) {
    LIGHT("light"),
    DARK("dark"),
    HC_LIGHT("hc-light"),
    HC_DARK("hc-dark"),
}

public object AnindaColours {
    // The light theme.
    public const val LIGHT_ACCENT: Long = 0xFF126974
    public const val LIGHT_ACCENT_EDGE: Long = 0xFF278492
    public const val LIGHT_ACCENT_HOVER: Long = 0xFF054D56
    public const val LIGHT_ACCENT_ON: Long = 0xFFFDFFFE
    public const val LIGHT_DANGER: Long = 0xFF9B3728
    public const val LIGHT_FOCUS_RING: Long = 0xFF278492
    public const val LIGHT_INFO: Long = 0xFF316189
    public const val LIGHT_INK: Long = 0xFF0D1A17
    public const val LIGHT_INK_MUTED: Long = 0xFF41655C
    public const val LIGHT_LINE: Long = 0xFF578076
    public const val LIGHT_SUCCESS: Long = 0xFF2D6C42
    public const val LIGHT_SURFACE_BASE: Long = 0xFFF8FAF9
    public const val LIGHT_SURFACE_BRIGHT: Long = 0xFFFFFFFF
    public const val LIGHT_SURFACE_DIM: Long = 0xFFF1F2F2
    public const val LIGHT_SURFACE_HIGH: Long = 0xFFF6F7F7
    public const val LIGHT_SURFACE_HIGHEST: Long = 0xFFF3F5F4
    public const val LIGHT_SURFACE_LOW: Long = 0xFFFBFCFC
    public const val LIGHT_SURFACE_LOWEST: Long = 0xFFFDFFFE
    public const val LIGHT_WARNING: Long = 0xFF7C5414

    // The dark theme.
    public const val DARK_ACCENT: Long = 0xFF42A0AE
    public const val DARK_ACCENT_EDGE: Long = 0xFF278492
    public const val DARK_ACCENT_HOVER: Long = 0xFF65BAC7
    public const val DARK_ACCENT_ON: Long = 0xFF0B0C0B
    public const val DARK_DANGER: Long = 0xFFE16551
    public const val DARK_FOCUS_RING: Long = 0xFF278492
    public const val DARK_INFO: Long = 0xFF5C96C8
    public const val DARK_INK: Long = 0xFFF2F9F7
    public const val DARK_INK_MUTED: Long = 0xFF6F9B90
    public const val DARK_LINE: Long = 0xFF578076
    public const val DARK_SUCCESS: Long = 0xFF59A46F
    public const val DARK_SURFACE_BASE: Long = 0xFF111212
    public const val DARK_SURFACE_BRIGHT: Long = 0xFF121413
    public const val DARK_SURFACE_DIM: Long = 0xFF060707
    public const val DARK_SURFACE_HIGH: Long = 0xFF111312
    public const val DARK_SURFACE_HIGHEST: Long = 0xFF121313
    public const val DARK_SURFACE_LOW: Long = 0xFF0E100F
    public const val DARK_SURFACE_LOWEST: Long = 0xFF0B0C0B
    public const val DARK_WARNING: Long = 0xFFB8863E

    // The hc-light theme.
    public const val HC_LIGHT_ACCENT: Long = 0xFF054D56
    public const val HC_LIGHT_ACCENT_EDGE: Long = 0xFF126974
    public const val HC_LIGHT_ACCENT_HOVER: Long = 0xFF013137
    public const val HC_LIGHT_ACCENT_ON: Long = 0xFFFCFDFC
    public const val HC_LIGHT_DANGER: Long = 0xFF752519
    public const val HC_LIGHT_FOCUS_RING: Long = 0xFF126974
    public const val HC_LIGHT_INFO: Long = 0xFF214767
    public const val HC_LIGHT_INK: Long = 0xFF0D1A17
    public const val HC_LIGHT_INK_MUTED: Long = 0xFF2E4B43
    public const val HC_LIGHT_LINE: Long = 0xFF41655C
    public const val HC_LIGHT_SUCCESS: Long = 0xFF1D502E
    public const val HC_LIGHT_SURFACE_BASE: Long = 0xFFF7F8F7
    public const val HC_LIGHT_SURFACE_BRIGHT: Long = 0xFFFFFFFF
    public const val HC_LIGHT_SURFACE_DIM: Long = 0xFFF1F1F1
    public const val HC_LIGHT_SURFACE_HIGH: Long = 0xFFF5F5F5
    public const val HC_LIGHT_SURFACE_HIGHEST: Long = 0xFFF2F3F2
    public const val HC_LIGHT_SURFACE_LOW: Long = 0xFFFAFAFA
    public const val HC_LIGHT_SURFACE_LOWEST: Long = 0xFFFCFDFC
    public const val HC_LIGHT_WARNING: Long = 0xFF5D3C07

    // The hc-dark theme.
    public const val HC_DARK_ACCENT: Long = 0xFF65BAC7
    public const val HC_DARK_ACCENT_EDGE: Long = 0xFF42A0AE
    public const val HC_DARK_ACCENT_HOVER: Long = 0xFF8ED2DD
    public const val HC_DARK_ACCENT_ON: Long = 0xFF070807
    public const val HC_DARK_DANGER: Long = 0xFFFB836F
    public const val HC_DARK_FOCUS_RING: Long = 0xFF42A0AE
    public const val HC_DARK_INFO: Long = 0xFF7AB1E1
    public const val HC_DARK_INK: Long = 0xFFF2F9F7
    public const val HC_DARK_INK_MUTED: Long = 0xFF8BB5AA
    public const val HC_DARK_LINE: Long = 0xFF6F9B90
    public const val HC_DARK_SUCCESS: Long = 0xFF77BE8B
    public const val HC_DARK_SURFACE_BASE: Long = 0xFF0E0F0E
    public const val HC_DARK_SURFACE_BRIGHT: Long = 0xFF121212
    public const val HC_DARK_SURFACE_DIM: Long = 0xFF030303
    public const val HC_DARK_SURFACE_HIGH: Long = 0xFF111111
    public const val HC_DARK_SURFACE_HIGHEST: Long = 0xFF111211
    public const val HC_DARK_SURFACE_LOW: Long = 0xFF0C0C0C
    public const val HC_DARK_SURFACE_LOWEST: Long = 0xFF070807
    public const val HC_DARK_WARNING: Long = 0xFFD2A15F

}

public object AnindaSpace {
    /** 4 dp */
    public const val S0: Int = 4
    /** 8 dp */
    public const val S1: Int = 8
    /** 12 dp */
    public const val S2: Int = 12
    /** 16 dp */
    public const val S3: Int = 16
    /** 24 dp */
    public const val S4: Int = 24
    /** 32 dp */
    public const val S5: Int = 32
    /** 48 dp */
    public const val S6: Int = 48
    /** 64 dp */
    public const val S7: Int = 64
    /** 96 dp */
    public const val S8: Int = 96
    /** 128 dp */
    public const val S9: Int = 128
}

public object AnindaRadius {
    public const val BADGE: Int = 4
    public const val CONTROL: Int = 8
    public const val CARD: Int = 14
    public const val HERO: Int = 24
}

public object AnindaTarget {
    public const val MIN: Int = 24
    public const val APPLE_MIN: Int = 28
    public const val COMFORTABLE: Int = 44
    public const val ANDROID_MIN: Int = 48
}

/**
 * Bangla is set smaller than Latin so the two look the same size, and the
 * multipliers were measured on rendered specimens rather than estimated.
 *
 * Material classifies Bangla as a MEDIUM language-height script, needing
 * roughly 7 per cent taller line heights at the same nominal size. These
 * figures are not that measurement and are not offered as agreeing with
 * it: this system's Bangla leading is 1.6 against Latin's 1.55, which is
 * +3.2 per cent, and the Bangla is also set at x0.816 — so its absolute
 * line box is smaller, not larger. Both numbers are published; neither
 * confirms the other.
 */
public object AnindaBangla {
    public const val CAPTION: Float = 0.815f
    public const val BODY: Float = 0.816f
    public const val HEADING: Float = 0.817f
    public const val TITLE: Float = 0.822f
    public const val DISPLAY: Float = 0.825f
    public const val MINIMUM_SP: Int = 12
    public const val WEIGHT_BUMP_BELOW_SP: Int = 14
}

public object AnindaMotion {
    public const val COLOUR_MS: Int = 120
    public const val MOVE_MS: Int = 220
}
