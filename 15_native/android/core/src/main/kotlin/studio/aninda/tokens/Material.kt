// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.

package studio.aninda.tokens

/**
 * Material 3's 48 colour roles, derived from this system's measured
 * palette by 15_native/material3.py and proven there.
 *
 * Every value traces to a measured one: a semantic role, a tonal surface,
 * or a step of one of the six committed ramps. Nothing was interpolated.
 *
 * The names `background`, `onBackground` and `surfaceVariant` appear here
 * because androidx's ColorScheme constructor requires them. No TOKEN in
 * this system carries those names, which is what benchmark criterion 21
 * forbids.
 */
public object AnindaMaterial {
    // light
    public const val LIGHT_PRIMARY: Long = 0xFF126974
    public const val LIGHT_ON_PRIMARY: Long = 0xFFFDFFFE
    public const val LIGHT_PRIMARY_CONTAINER: Long = 0xFFEDFAFD
    public const val LIGHT_ON_PRIMARY_CONTAINER: Long = 0xFF001B20
    public const val LIGHT_INVERSE_PRIMARY: Long = 0xFF42A0AE
    public const val LIGHT_SECONDARY: Long = 0xFF41655C
    public const val LIGHT_ON_SECONDARY: Long = 0xFFFDFFFE
    public const val LIGHT_SECONDARY_CONTAINER: Long = 0xFFF2F9F7
    public const val LIGHT_ON_SECONDARY_CONTAINER: Long = 0xFF0D1A17
    public const val LIGHT_TERTIARY: Long = 0xFF235E8C
    public const val LIGHT_ON_TERTIARY: Long = 0xFFFDFFFE
    public const val LIGHT_TERTIARY_CONTAINER: Long = 0xFFEFF9FF
    public const val LIGHT_ON_TERTIARY_CONTAINER: Long = 0xFF071928
    public const val LIGHT_BACKGROUND: Long = 0xFFF8FAF9
    public const val LIGHT_ON_BACKGROUND: Long = 0xFF0D1A17
    public const val LIGHT_SURFACE: Long = 0xFFF8FAF9
    public const val LIGHT_ON_SURFACE: Long = 0xFF0D1A17
    public const val LIGHT_SURFACE_VARIANT: Long = 0xFFF3F5F4
    public const val LIGHT_ON_SURFACE_VARIANT: Long = 0xFF41655C
    public const val LIGHT_SURFACE_TINT: Long = 0xFF126974
    public const val LIGHT_INVERSE_SURFACE: Long = 0xFF0B0D0C
    public const val LIGHT_INVERSE_ON_SURFACE: Long = 0xFFF2F9F7
    public const val LIGHT_ERROR: Long = 0xFFA8301F
    public const val LIGHT_ON_ERROR: Long = 0xFFFDFFFE
    public const val LIGHT_ERROR_CONTAINER: Long = 0xFFFFF2ED
    public const val LIGHT_ON_ERROR_CONTAINER: Long = 0xFF2E0804
    public const val LIGHT_OUTLINE: Long = 0xFF0C3A31
    public const val LIGHT_OUTLINE_VARIANT: Long = 0xFF0C3A31
    public const val LIGHT_SCRIM: Long = 0xFF0D1A17
    public const val LIGHT_SURFACE_BRIGHT: Long = 0xFFFFFFFF
    public const val LIGHT_SURFACE_DIM: Long = 0xFFF1F2F2
    public const val LIGHT_SURFACE_CONTAINER: Long = 0xFFF8FAF9
    public const val LIGHT_SURFACE_CONTAINER_HIGH: Long = 0xFFF6F7F7
    public const val LIGHT_SURFACE_CONTAINER_HIGHEST: Long = 0xFFF3F5F4
    public const val LIGHT_SURFACE_CONTAINER_LOW: Long = 0xFFFBFCFC
    public const val LIGHT_SURFACE_CONTAINER_LOWEST: Long = 0xFFFDFFFE
    public const val LIGHT_PRIMARY_FIXED: Long = 0xFFEDFAFD
    public const val LIGHT_PRIMARY_FIXED_DIM: Long = 0xFFD9F2F7
    public const val LIGHT_ON_PRIMARY_FIXED: Long = 0xFF001B20
    public const val LIGHT_ON_PRIMARY_FIXED_VARIANT: Long = 0xFF126974
    public const val LIGHT_SECONDARY_FIXED: Long = 0xFFF2F9F7
    public const val LIGHT_SECONDARY_FIXED_DIM: Long = 0xFFE3F0EC
    public const val LIGHT_ON_SECONDARY_FIXED: Long = 0xFF0D1A17
    public const val LIGHT_ON_SECONDARY_FIXED_VARIANT: Long = 0xFF41655C
    public const val LIGHT_TERTIARY_FIXED: Long = 0xFFEFF9FF
    public const val LIGHT_TERTIARY_FIXED_DIM: Long = 0xFFDEEFFF
    public const val LIGHT_ON_TERTIARY_FIXED: Long = 0xFF071928
    public const val LIGHT_ON_TERTIARY_FIXED_VARIANT: Long = 0xFF235E8C

    // dark
    public const val DARK_PRIMARY: Long = 0xFF42A0AE
    public const val DARK_ON_PRIMARY: Long = 0xFF040504
    public const val DARK_PRIMARY_CONTAINER: Long = 0xFF001B20
    public const val DARK_ON_PRIMARY_CONTAINER: Long = 0xFFEDFAFD
    public const val DARK_INVERSE_PRIMARY: Long = 0xFF126974
    public const val DARK_SECONDARY: Long = 0xFF6F9B90
    public const val DARK_ON_SECONDARY: Long = 0xFF040504
    public const val DARK_SECONDARY_CONTAINER: Long = 0xFF0D1A17
    public const val DARK_ON_SECONDARY_CONTAINER: Long = 0xFFF2F9F7
    public const val DARK_TERTIARY: Long = 0xFF5C96C8
    public const val DARK_ON_TERTIARY: Long = 0xFF040504
    public const val DARK_TERTIARY_CONTAINER: Long = 0xFF071928
    public const val DARK_ON_TERTIARY_CONTAINER: Long = 0xFFEFF9FF
    public const val DARK_BACKGROUND: Long = 0xFF0B0D0C
    public const val DARK_ON_BACKGROUND: Long = 0xFFF2F9F7
    public const val DARK_SURFACE: Long = 0xFF0B0D0C
    public const val DARK_ON_SURFACE: Long = 0xFFF2F9F7
    public const val DARK_SURFACE_VARIANT: Long = 0xFF0F1110
    public const val DARK_ON_SURFACE_VARIANT: Long = 0xFF6F9B90
    public const val DARK_SURFACE_TINT: Long = 0xFF42A0AE
    public const val DARK_INVERSE_SURFACE: Long = 0xFFF8FAF9
    public const val DARK_INVERSE_ON_SURFACE: Long = 0xFF0D1A17
    public const val DARK_ERROR: Long = 0xFFE16551
    public const val DARK_ON_ERROR: Long = 0xFF040504
    public const val DARK_ERROR_CONTAINER: Long = 0xFF2E0804
    public const val DARK_ON_ERROR_CONTAINER: Long = 0xFFFFF2ED
    public const val DARK_OUTLINE: Long = 0xFF578076
    public const val DARK_OUTLINE_VARIANT: Long = 0xFF578076
    public const val DARK_SCRIM: Long = 0xFFF2F9F7
    public const val DARK_SURFACE_BRIGHT: Long = 0xFF111212
    public const val DARK_SURFACE_DIM: Long = 0xFF000000
    public const val DARK_SURFACE_CONTAINER: Long = 0xFF0B0D0C
    public const val DARK_SURFACE_CONTAINER_HIGH: Long = 0xFF0F1010
    public const val DARK_SURFACE_CONTAINER_HIGHEST: Long = 0xFF0F1110
    public const val DARK_SURFACE_CONTAINER_LOW: Long = 0xFF090A0A
    public const val DARK_SURFACE_CONTAINER_LOWEST: Long = 0xFF040504
    public const val DARK_PRIMARY_FIXED: Long = 0xFFEDFAFD
    public const val DARK_PRIMARY_FIXED_DIM: Long = 0xFFD9F2F7
    public const val DARK_ON_PRIMARY_FIXED: Long = 0xFF001B20
    public const val DARK_ON_PRIMARY_FIXED_VARIANT: Long = 0xFF126974
    public const val DARK_SECONDARY_FIXED: Long = 0xFFF2F9F7
    public const val DARK_SECONDARY_FIXED_DIM: Long = 0xFFE3F0EC
    public const val DARK_ON_SECONDARY_FIXED: Long = 0xFF0D1A17
    public const val DARK_ON_SECONDARY_FIXED_VARIANT: Long = 0xFF41655C
    public const val DARK_TERTIARY_FIXED: Long = 0xFFEFF9FF
    public const val DARK_TERTIARY_FIXED_DIM: Long = 0xFFDEEFFF
    public const val DARK_ON_TERTIARY_FIXED: Long = 0xFF071928
    public const val DARK_ON_TERTIARY_FIXED_VARIANT: Long = 0xFF235E8C

    // hc-light
    public const val HC_LIGHT_PRIMARY: Long = 0xFF054D56
    public const val HC_LIGHT_ON_PRIMARY: Long = 0xFFFCFDFC
    public const val HC_LIGHT_PRIMARY_CONTAINER: Long = 0xFFEDFAFD
    public const val HC_LIGHT_ON_PRIMARY_CONTAINER: Long = 0xFF001B20
    public const val HC_LIGHT_INVERSE_PRIMARY: Long = 0xFF65BAC7
    public const val HC_LIGHT_SECONDARY: Long = 0xFF2E4B43
    public const val HC_LIGHT_ON_SECONDARY: Long = 0xFFFCFDFC
    public const val HC_LIGHT_SECONDARY_CONTAINER: Long = 0xFFF2F9F7
    public const val HC_LIGHT_ON_SECONDARY_CONTAINER: Long = 0xFF0D1A17
    public const val HC_LIGHT_TERTIARY: Long = 0xFF214767
    public const val HC_LIGHT_ON_TERTIARY: Long = 0xFFFCFDFC
    public const val HC_LIGHT_TERTIARY_CONTAINER: Long = 0xFFEFF9FF
    public const val HC_LIGHT_ON_TERTIARY_CONTAINER: Long = 0xFF071928
    public const val HC_LIGHT_BACKGROUND: Long = 0xFFF7F8F7
    public const val HC_LIGHT_ON_BACKGROUND: Long = 0xFF0D1A17
    public const val HC_LIGHT_SURFACE: Long = 0xFFF7F8F7
    public const val HC_LIGHT_ON_SURFACE: Long = 0xFF0D1A17
    public const val HC_LIGHT_SURFACE_VARIANT: Long = 0xFFF2F3F2
    public const val HC_LIGHT_ON_SURFACE_VARIANT: Long = 0xFF2E4B43
    public const val HC_LIGHT_SURFACE_TINT: Long = 0xFF054D56
    public const val HC_LIGHT_INVERSE_SURFACE: Long = 0xFF0C0D0C
    public const val HC_LIGHT_INVERSE_ON_SURFACE: Long = 0xFFF2F9F7
    public const val HC_LIGHT_ERROR: Long = 0xFF752519
    public const val HC_LIGHT_ON_ERROR: Long = 0xFFFCFDFC
    public const val HC_LIGHT_ERROR_CONTAINER: Long = 0xFFFFF2ED
    public const val HC_LIGHT_ON_ERROR_CONTAINER: Long = 0xFF2E0804
    public const val HC_LIGHT_OUTLINE: Long = 0xFF0C3A31
    public const val HC_LIGHT_OUTLINE_VARIANT: Long = 0xFF0C3A31
    public const val HC_LIGHT_SCRIM: Long = 0xFF0D1A17
    public const val HC_LIGHT_SURFACE_BRIGHT: Long = 0xFFFFFFFF
    public const val HC_LIGHT_SURFACE_DIM: Long = 0xFFF1F1F1
    public const val HC_LIGHT_SURFACE_CONTAINER: Long = 0xFFF7F8F7
    public const val HC_LIGHT_SURFACE_CONTAINER_HIGH: Long = 0xFFF5F5F5
    public const val HC_LIGHT_SURFACE_CONTAINER_HIGHEST: Long = 0xFFF2F3F2
    public const val HC_LIGHT_SURFACE_CONTAINER_LOW: Long = 0xFFFAFAFA
    public const val HC_LIGHT_SURFACE_CONTAINER_LOWEST: Long = 0xFFFCFDFC
    public const val HC_LIGHT_PRIMARY_FIXED: Long = 0xFFEDFAFD
    public const val HC_LIGHT_PRIMARY_FIXED_DIM: Long = 0xFFD9F2F7
    public const val HC_LIGHT_ON_PRIMARY_FIXED: Long = 0xFF001B20
    public const val HC_LIGHT_ON_PRIMARY_FIXED_VARIANT: Long = 0xFF054D56
    public const val HC_LIGHT_SECONDARY_FIXED: Long = 0xFFF2F9F7
    public const val HC_LIGHT_SECONDARY_FIXED_DIM: Long = 0xFFE3F0EC
    public const val HC_LIGHT_ON_SECONDARY_FIXED: Long = 0xFF0D1A17
    public const val HC_LIGHT_ON_SECONDARY_FIXED_VARIANT: Long = 0xFF2E4B43
    public const val HC_LIGHT_TERTIARY_FIXED: Long = 0xFFEFF9FF
    public const val HC_LIGHT_TERTIARY_FIXED_DIM: Long = 0xFFDEEFFF
    public const val HC_LIGHT_ON_TERTIARY_FIXED: Long = 0xFF071928
    public const val HC_LIGHT_ON_TERTIARY_FIXED_VARIANT: Long = 0xFF214767

    // hc-dark
    public const val HC_DARK_PRIMARY: Long = 0xFF65BAC7
    public const val HC_DARK_ON_PRIMARY: Long = 0xFF040504
    public const val HC_DARK_PRIMARY_CONTAINER: Long = 0xFF001B20
    public const val HC_DARK_ON_PRIMARY_CONTAINER: Long = 0xFFEDFAFD
    public const val HC_DARK_INVERSE_PRIMARY: Long = 0xFF054D56
    public const val HC_DARK_SECONDARY: Long = 0xFF8BB5AA
    public const val HC_DARK_ON_SECONDARY: Long = 0xFF040504
    public const val HC_DARK_SECONDARY_CONTAINER: Long = 0xFF0D1A17
    public const val HC_DARK_ON_SECONDARY_CONTAINER: Long = 0xFFF2F9F7
    public const val HC_DARK_TERTIARY: Long = 0xFF7AB1E1
    public const val HC_DARK_ON_TERTIARY: Long = 0xFF040504
    public const val HC_DARK_TERTIARY_CONTAINER: Long = 0xFF071928
    public const val HC_DARK_ON_TERTIARY_CONTAINER: Long = 0xFFEFF9FF
    public const val HC_DARK_BACKGROUND: Long = 0xFF0C0D0C
    public const val HC_DARK_ON_BACKGROUND: Long = 0xFFF2F9F7
    public const val HC_DARK_SURFACE: Long = 0xFF0C0D0C
    public const val HC_DARK_ON_SURFACE: Long = 0xFFF2F9F7
    public const val HC_DARK_SURFACE_VARIANT: Long = 0xFF101110
    public const val HC_DARK_ON_SURFACE_VARIANT: Long = 0xFF8BB5AA
    public const val HC_DARK_SURFACE_TINT: Long = 0xFF65BAC7
    public const val HC_DARK_INVERSE_SURFACE: Long = 0xFFF7F8F7
    public const val HC_DARK_INVERSE_ON_SURFACE: Long = 0xFF0D1A17
    public const val HC_DARK_ERROR: Long = 0xFFFB836F
    public const val HC_DARK_ON_ERROR: Long = 0xFF040504
    public const val HC_DARK_ERROR_CONTAINER: Long = 0xFF2E0804
    public const val HC_DARK_ON_ERROR_CONTAINER: Long = 0xFFFFF2ED
    public const val HC_DARK_OUTLINE: Long = 0xFF6F9B90
    public const val HC_DARK_OUTLINE_VARIANT: Long = 0xFF6F9B90
    public const val HC_DARK_SCRIM: Long = 0xFFF2F9F7
    public const val HC_DARK_SURFACE_BRIGHT: Long = 0xFF111111
    public const val HC_DARK_SURFACE_DIM: Long = 0xFF000000
    public const val HC_DARK_SURFACE_CONTAINER: Long = 0xFF0C0D0C
    public const val HC_DARK_SURFACE_CONTAINER_HIGH: Long = 0xFF101010
    public const val HC_DARK_SURFACE_CONTAINER_HIGHEST: Long = 0xFF101110
    public const val HC_DARK_SURFACE_CONTAINER_LOW: Long = 0xFF090909
    public const val HC_DARK_SURFACE_CONTAINER_LOWEST: Long = 0xFF040504
    public const val HC_DARK_PRIMARY_FIXED: Long = 0xFFEDFAFD
    public const val HC_DARK_PRIMARY_FIXED_DIM: Long = 0xFFD9F2F7
    public const val HC_DARK_ON_PRIMARY_FIXED: Long = 0xFF001B20
    public const val HC_DARK_ON_PRIMARY_FIXED_VARIANT: Long = 0xFF054D56
    public const val HC_DARK_SECONDARY_FIXED: Long = 0xFFF2F9F7
    public const val HC_DARK_SECONDARY_FIXED_DIM: Long = 0xFFE3F0EC
    public const val HC_DARK_ON_SECONDARY_FIXED: Long = 0xFF0D1A17
    public const val HC_DARK_ON_SECONDARY_FIXED_VARIANT: Long = 0xFF2E4B43
    public const val HC_DARK_TERTIARY_FIXED: Long = 0xFFEFF9FF
    public const val HC_DARK_TERTIARY_FIXED_DIM: Long = 0xFFDEEFFF
    public const val HC_DARK_ON_TERTIARY_FIXED: Long = 0xFF071928
    public const val HC_DARK_ON_TERTIARY_FIXED_VARIANT: Long = 0xFF214767

}
