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
    public const val LIGHT_ACCENT: Long = 0xFF224959
    public const val LIGHT_ACCENT_EDGE: Long = 0xFF577D8D
    public const val LIGHT_ACCENT_HOVER: Long = 0xFF1B2D35
    public const val LIGHT_ACCENT_ON: Long = 0xFFFCFBFB
    public const val LIGHT_DANGER: Long = 0xFFA14F39
    public const val LIGHT_FOCUS_RING: Long = 0xFF577D8D
    public const val LIGHT_INFO: Long = 0xFF224959
    public const val LIGHT_INK: Long = 0xFF000000
    public const val LIGHT_INK_MUTED: Long = 0xFF605C59
    public const val LIGHT_LINE: Long = 0xFF84807C
    public const val LIGHT_SUCCESS: Long = 0xFF2C5A3A
    public const val LIGHT_SURFACE_BASE: Long = 0xFFF8F7F7
    public const val LIGHT_SURFACE_BRIGHT: Long = 0xFFFFFFFF
    public const val LIGHT_SURFACE_DIM: Long = 0xFFF1F1F0
    public const val LIGHT_SURFACE_HIGH: Long = 0xFFF5F5F4
    public const val LIGHT_SURFACE_HIGHEST: Long = 0xFFF4F3F3
    public const val LIGHT_SURFACE_LOW: Long = 0xFFF9F9F8
    public const val LIGHT_SURFACE_LOWEST: Long = 0xFFFCFBFB
    public const val LIGHT_SURFACE_PAGE: Long = 0xFFFFFFFF
    public const val LIGHT_WARNING: Long = 0xFF464341

    // The dark theme.
    public const val DARK_ACCENT: Long = 0xFF6F98AA
    public const val DARK_ACCENT_EDGE: Long = 0xFF577D8D
    public const val DARK_ACCENT_HOVER: Long = 0xFF8BB2C3
    public const val DARK_ACCENT_ON: Long = 0xFF060505
    public const val DARK_DANGER: Long = 0xFFCC765E
    public const val DARK_FOCUS_RING: Long = 0xFF577D8D
    public const val DARK_INFO: Long = 0xFF6F98AA
    public const val DARK_INK: Long = 0xFFFFFFFF
    public const val DARK_INK_MUTED: Long = 0xFF84807C
    public const val DARK_LINE: Long = 0xFF84807C
    public const val DARK_SUCCESS: Long = 0xFF6E9E7A
    public const val DARK_SURFACE_BASE: Long = 0xFF0E0D0D
    public const val DARK_SURFACE_BRIGHT: Long = 0xFF111110
    public const val DARK_SURFACE_DIM: Long = 0xFF000000
    public const val DARK_SURFACE_HIGH: Long = 0xFF10100F
    public const val DARK_SURFACE_HIGHEST: Long = 0xFF111010
    public const val DARK_SURFACE_LOW: Long = 0xFF0A0A09
    public const val DARK_SURFACE_LOWEST: Long = 0xFF060505
    public const val DARK_SURFACE_PAGE: Long = 0xFF000000
    public const val DARK_WARNING: Long = 0xFF94908C

    // The hc-light theme.
    public const val HC_LIGHT_ACCENT: Long = 0xFF224959
    public const val HC_LIGHT_ACCENT_EDGE: Long = 0xFF426271
    public const val HC_LIGHT_ACCENT_HOVER: Long = 0xFF1B2D35
    public const val HC_LIGHT_ACCENT_ON: Long = 0xFFFCFBFB
    public const val HC_LIGHT_DANGER: Long = 0xFF693223
    public const val HC_LIGHT_FOCUS_RING: Long = 0xFF426271
    public const val HC_LIGHT_INFO: Long = 0xFF224959
    public const val HC_LIGHT_INK: Long = 0xFF000000
    public const val HC_LIGHT_INK_MUTED: Long = 0xFF464341
    public const val HC_LIGHT_LINE: Long = 0xFF605C59
    public const val HC_LIGHT_SUCCESS: Long = 0xFF1B3020
    public const val HC_LIGHT_SURFACE_BASE: Long = 0xFFF4F3F3
    public const val HC_LIGHT_SURFACE_BRIGHT: Long = 0xFFFFFFFF
    public const val HC_LIGHT_SURFACE_DIM: Long = 0xFFE7E7E7
    public const val HC_LIGHT_SURFACE_HIGH: Long = 0xFFEFEFEF
    public const val HC_LIGHT_SURFACE_HIGHEST: Long = 0xFFECEBEB
    public const val HC_LIGHT_SURFACE_LOW: Long = 0xFFF7F7F7
    public const val HC_LIGHT_SURFACE_LOWEST: Long = 0xFFFCFBFB
    public const val HC_LIGHT_SURFACE_PAGE: Long = 0xFFFFFFFF
    public const val HC_LIGHT_WARNING: Long = 0xFF2C2A28

    // The hc-dark theme.
    public const val HC_DARK_ACCENT: Long = 0xFF8BB2C3
    public const val HC_DARK_ACCENT_EDGE: Long = 0xFF6F98AA
    public const val HC_DARK_ACCENT_HOVER: Long = 0xFFAACBD9
    public const val HC_DARK_ACCENT_ON: Long = 0xFF060505
    public const val HC_DARK_DANGER: Long = 0xFFE6927B
    public const val HC_DARK_FOCUS_RING: Long = 0xFF6F98AA
    public const val HC_DARK_INFO: Long = 0xFF8BB2C3
    public const val HC_DARK_INK: Long = 0xFFFFFFFF
    public const val HC_DARK_INK_MUTED: Long = 0xFFAEAAA6
    public const val HC_DARK_LINE: Long = 0xFF84807C
    public const val HC_DARK_SUCCESS: Long = 0xFF8AB895
    public const val HC_DARK_SURFACE_BASE: Long = 0xFF0F0E0E
    public const val HC_DARK_SURFACE_BRIGHT: Long = 0xFF151515
    public const val HC_DARK_SURFACE_DIM: Long = 0xFF000000
    public const val HC_DARK_SURFACE_HIGH: Long = 0xFF10100F
    public const val HC_DARK_SURFACE_HIGHEST: Long = 0xFF131212
    public const val HC_DARK_SURFACE_LOW: Long = 0xFF0A0A09
    public const val HC_DARK_SURFACE_LOWEST: Long = 0xFF060505
    public const val HC_DARK_SURFACE_PAGE: Long = 0xFF000000
    public const val HC_DARK_WARNING: Long = 0xFFC7C4C1

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
