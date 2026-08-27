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
    public const val LIGHT_PRIMARY: Long = 0xFF224959
    public const val LIGHT_ON_PRIMARY: Long = 0xFFFCFBFB
    public const val LIGHT_PRIMARY_CONTAINER: Long = 0xFFF2F9FC
    public const val LIGHT_ON_PRIMARY_CONTAINER: Long = 0xFF0D191F
    public const val LIGHT_INVERSE_PRIMARY: Long = 0xFF6F98AA
    public const val LIGHT_SECONDARY: Long = 0xFF605C59
    public const val LIGHT_ON_SECONDARY: Long = 0xFFFCFBFB
    public const val LIGHT_SECONDARY_CONTAINER: Long = 0xFFEEECEB
    public const val LIGHT_ON_SECONDARY_CONTAINER: Long = 0xFF181716
    public const val LIGHT_TERTIARY: Long = 0xFF2C5A3A
    public const val LIGHT_ON_TERTIARY: Long = 0xFFFCFBFB
    public const val LIGHT_TERTIARY_CONTAINER: Long = 0xFFF2FAF4
    public const val LIGHT_ON_TERTIARY_CONTAINER: Long = 0xFF0C1B10
    public const val LIGHT_BACKGROUND: Long = 0xFFF8F7F7
    public const val LIGHT_ON_BACKGROUND: Long = 0xFF000000
    public const val LIGHT_SURFACE: Long = 0xFFF8F7F7
    public const val LIGHT_ON_SURFACE: Long = 0xFF000000
    public const val LIGHT_SURFACE_VARIANT: Long = 0xFFF4F3F3
    public const val LIGHT_ON_SURFACE_VARIANT: Long = 0xFF605C59
    public const val LIGHT_SURFACE_TINT: Long = 0xFF224959
    public const val LIGHT_INVERSE_SURFACE: Long = 0xFF0E0D0D
    public const val LIGHT_INVERSE_ON_SURFACE: Long = 0xFFFFFFFF
    public const val LIGHT_ERROR: Long = 0xFFA14F39
    public const val LIGHT_ON_ERROR: Long = 0xFFFCFBFB
    public const val LIGHT_ERROR_CONTAINER: Long = 0xFFFFF3EF
    public const val LIGHT_ON_ERROR_CONTAINER: Long = 0xFF280E08
    public const val LIGHT_OUTLINE: Long = 0xFF84807C
    public const val LIGHT_OUTLINE_VARIANT: Long = 0xFF84807C
    public const val LIGHT_SCRIM: Long = 0xFF000000
    public const val LIGHT_SURFACE_BRIGHT: Long = 0xFFFFFFFF
    public const val LIGHT_SURFACE_DIM: Long = 0xFFF1F1F0
    public const val LIGHT_SURFACE_CONTAINER: Long = 0xFFF8F7F7
    public const val LIGHT_SURFACE_CONTAINER_HIGH: Long = 0xFFF5F5F4
    public const val LIGHT_SURFACE_CONTAINER_HIGHEST: Long = 0xFFF4F3F3
    public const val LIGHT_SURFACE_CONTAINER_LOW: Long = 0xFFF9F9F8
    public const val LIGHT_SURFACE_CONTAINER_LOWEST: Long = 0xFFFCFBFB
    public const val LIGHT_PRIMARY_FIXED: Long = 0xFFF2F9FC
    public const val LIGHT_PRIMARY_FIXED_DIM: Long = 0xFFE3EFF5
    public const val LIGHT_ON_PRIMARY_FIXED: Long = 0xFF0D191F
    public const val LIGHT_ON_PRIMARY_FIXED_VARIANT: Long = 0xFF426271
    public const val LIGHT_SECONDARY_FIXED: Long = 0xFFF8F7F6
    public const val LIGHT_SECONDARY_FIXED_DIM: Long = 0xFFEEECEB
    public const val LIGHT_ON_SECONDARY_FIXED: Long = 0xFF181716
    public const val LIGHT_ON_SECONDARY_FIXED_VARIANT: Long = 0xFF605C59
    public const val LIGHT_TERTIARY_FIXED: Long = 0xFFF2FAF4
    public const val LIGHT_TERTIARY_FIXED_DIM: Long = 0xFFE3F1E6
    public const val LIGHT_ON_TERTIARY_FIXED: Long = 0xFF0C1B10
    public const val LIGHT_ON_TERTIARY_FIXED_VARIANT: Long = 0xFF41674B

    // dark
    public const val DARK_PRIMARY: Long = 0xFF6F98AA
    public const val DARK_ON_PRIMARY: Long = 0xFF060505
    public const val DARK_PRIMARY_CONTAINER: Long = 0xFF0D191F
    public const val DARK_ON_PRIMARY_CONTAINER: Long = 0xFFF2F9FC
    public const val DARK_INVERSE_PRIMARY: Long = 0xFF224959
    public const val DARK_SECONDARY: Long = 0xFF84807C
    public const val DARK_ON_SECONDARY: Long = 0xFF060505
    public const val DARK_SECONDARY_CONTAINER: Long = 0xFF181716
    public const val DARK_ON_SECONDARY_CONTAINER: Long = 0xFFF8F7F6
    public const val DARK_TERTIARY: Long = 0xFF6E9E7A
    public const val DARK_ON_TERTIARY: Long = 0xFF060505
    public const val DARK_TERTIARY_CONTAINER: Long = 0xFF0C1B10
    public const val DARK_ON_TERTIARY_CONTAINER: Long = 0xFFF2FAF4
    public const val DARK_BACKGROUND: Long = 0xFF0E0D0D
    public const val DARK_ON_BACKGROUND: Long = 0xFFFFFFFF
    public const val DARK_SURFACE: Long = 0xFF0E0D0D
    public const val DARK_ON_SURFACE: Long = 0xFFFFFFFF
    public const val DARK_SURFACE_VARIANT: Long = 0xFF111010
    public const val DARK_ON_SURFACE_VARIANT: Long = 0xFF84807C
    public const val DARK_SURFACE_TINT: Long = 0xFF6F98AA
    public const val DARK_INVERSE_SURFACE: Long = 0xFFF8F7F7
    public const val DARK_INVERSE_ON_SURFACE: Long = 0xFF000000
    public const val DARK_ERROR: Long = 0xFFCC765E
    public const val DARK_ON_ERROR: Long = 0xFF060505
    public const val DARK_ERROR_CONTAINER: Long = 0xFF280E08
    public const val DARK_ON_ERROR_CONTAINER: Long = 0xFFFFF3EF
    public const val DARK_OUTLINE: Long = 0xFF84807C
    public const val DARK_OUTLINE_VARIANT: Long = 0xFF84807C
    public const val DARK_SCRIM: Long = 0xFFFFFFFF
    public const val DARK_SURFACE_BRIGHT: Long = 0xFF111110
    public const val DARK_SURFACE_DIM: Long = 0xFF000000
    public const val DARK_SURFACE_CONTAINER: Long = 0xFF0E0D0D
    public const val DARK_SURFACE_CONTAINER_HIGH: Long = 0xFF10100F
    public const val DARK_SURFACE_CONTAINER_HIGHEST: Long = 0xFF111010
    public const val DARK_SURFACE_CONTAINER_LOW: Long = 0xFF0A0A09
    public const val DARK_SURFACE_CONTAINER_LOWEST: Long = 0xFF060505
    public const val DARK_PRIMARY_FIXED: Long = 0xFFF2F9FC
    public const val DARK_PRIMARY_FIXED_DIM: Long = 0xFFE3EFF5
    public const val DARK_ON_PRIMARY_FIXED: Long = 0xFF0D191F
    public const val DARK_ON_PRIMARY_FIXED_VARIANT: Long = 0xFF426271
    public const val DARK_SECONDARY_FIXED: Long = 0xFFF8F7F6
    public const val DARK_SECONDARY_FIXED_DIM: Long = 0xFFEEECEB
    public const val DARK_ON_SECONDARY_FIXED: Long = 0xFF181716
    public const val DARK_ON_SECONDARY_FIXED_VARIANT: Long = 0xFF605C59
    public const val DARK_TERTIARY_FIXED: Long = 0xFFF2FAF4
    public const val DARK_TERTIARY_FIXED_DIM: Long = 0xFFE3F1E6
    public const val DARK_ON_TERTIARY_FIXED: Long = 0xFF0C1B10
    public const val DARK_ON_TERTIARY_FIXED_VARIANT: Long = 0xFF41674B

    // hc-light
    public const val HC_LIGHT_PRIMARY: Long = 0xFF224959
    public const val HC_LIGHT_ON_PRIMARY: Long = 0xFFFCFBFB
    public const val HC_LIGHT_PRIMARY_CONTAINER: Long = 0xFFF2F9FC
    public const val HC_LIGHT_ON_PRIMARY_CONTAINER: Long = 0xFF0D191F
    public const val HC_LIGHT_INVERSE_PRIMARY: Long = 0xFF8BB2C3
    public const val HC_LIGHT_SECONDARY: Long = 0xFF464341
    public const val HC_LIGHT_ON_SECONDARY: Long = 0xFFFCFBFB
    public const val HC_LIGHT_SECONDARY_CONTAINER: Long = 0xFFF8F7F6
    public const val HC_LIGHT_ON_SECONDARY_CONTAINER: Long = 0xFF181716
    public const val HC_LIGHT_TERTIARY: Long = 0xFF1B3020
    public const val HC_LIGHT_ON_TERTIARY: Long = 0xFFFCFBFB
    public const val HC_LIGHT_TERTIARY_CONTAINER: Long = 0xFFF2FAF4
    public const val HC_LIGHT_ON_TERTIARY_CONTAINER: Long = 0xFF0C1B10
    public const val HC_LIGHT_BACKGROUND: Long = 0xFFF4F3F3
    public const val HC_LIGHT_ON_BACKGROUND: Long = 0xFF000000
    public const val HC_LIGHT_SURFACE: Long = 0xFFF4F3F3
    public const val HC_LIGHT_ON_SURFACE: Long = 0xFF000000
    public const val HC_LIGHT_SURFACE_VARIANT: Long = 0xFFECEBEB
    public const val HC_LIGHT_ON_SURFACE_VARIANT: Long = 0xFF464341
    public const val HC_LIGHT_SURFACE_TINT: Long = 0xFF224959
    public const val HC_LIGHT_INVERSE_SURFACE: Long = 0xFF0F0E0E
    public const val HC_LIGHT_INVERSE_ON_SURFACE: Long = 0xFFFFFFFF
    public const val HC_LIGHT_ERROR: Long = 0xFF693223
    public const val HC_LIGHT_ON_ERROR: Long = 0xFFFCFBFB
    public const val HC_LIGHT_ERROR_CONTAINER: Long = 0xFFFFF3EF
    public const val HC_LIGHT_ON_ERROR_CONTAINER: Long = 0xFF280E08
    public const val HC_LIGHT_OUTLINE: Long = 0xFF605C59
    public const val HC_LIGHT_OUTLINE_VARIANT: Long = 0xFF605C59
    public const val HC_LIGHT_SCRIM: Long = 0xFF000000
    public const val HC_LIGHT_SURFACE_BRIGHT: Long = 0xFFFFFFFF
    public const val HC_LIGHT_SURFACE_DIM: Long = 0xFFE7E7E7
    public const val HC_LIGHT_SURFACE_CONTAINER: Long = 0xFFF4F3F3
    public const val HC_LIGHT_SURFACE_CONTAINER_HIGH: Long = 0xFFEFEFEF
    public const val HC_LIGHT_SURFACE_CONTAINER_HIGHEST: Long = 0xFFECEBEB
    public const val HC_LIGHT_SURFACE_CONTAINER_LOW: Long = 0xFFF7F7F7
    public const val HC_LIGHT_SURFACE_CONTAINER_LOWEST: Long = 0xFFFCFBFB
    public const val HC_LIGHT_PRIMARY_FIXED: Long = 0xFFF2F9FC
    public const val HC_LIGHT_PRIMARY_FIXED_DIM: Long = 0xFFE3EFF5
    public const val HC_LIGHT_ON_PRIMARY_FIXED: Long = 0xFF0D191F
    public const val HC_LIGHT_ON_PRIMARY_FIXED_VARIANT: Long = 0xFF224959
    public const val HC_LIGHT_SECONDARY_FIXED: Long = 0xFFF8F7F6
    public const val HC_LIGHT_SECONDARY_FIXED_DIM: Long = 0xFFEEECEB
    public const val HC_LIGHT_ON_SECONDARY_FIXED: Long = 0xFF181716
    public const val HC_LIGHT_ON_SECONDARY_FIXED_VARIANT: Long = 0xFF464341
    public const val HC_LIGHT_TERTIARY_FIXED: Long = 0xFFF2FAF4
    public const val HC_LIGHT_TERTIARY_FIXED_DIM: Long = 0xFFE3F1E6
    public const val HC_LIGHT_ON_TERTIARY_FIXED: Long = 0xFF0C1B10
    public const val HC_LIGHT_ON_TERTIARY_FIXED_VARIANT: Long = 0xFF1B3020

    // hc-dark
    public const val HC_DARK_PRIMARY: Long = 0xFF8BB2C3
    public const val HC_DARK_ON_PRIMARY: Long = 0xFF060505
    public const val HC_DARK_PRIMARY_CONTAINER: Long = 0xFF0D191F
    public const val HC_DARK_ON_PRIMARY_CONTAINER: Long = 0xFFF2F9FC
    public const val HC_DARK_INVERSE_PRIMARY: Long = 0xFF224959
    public const val HC_DARK_SECONDARY: Long = 0xFFAEAAA6
    public const val HC_DARK_ON_SECONDARY: Long = 0xFF060505
    public const val HC_DARK_SECONDARY_CONTAINER: Long = 0xFF181716
    public const val HC_DARK_ON_SECONDARY_CONTAINER: Long = 0xFFF8F7F6
    public const val HC_DARK_TERTIARY: Long = 0xFF8AB895
    public const val HC_DARK_ON_TERTIARY: Long = 0xFF060505
    public const val HC_DARK_TERTIARY_CONTAINER: Long = 0xFF0C1B10
    public const val HC_DARK_ON_TERTIARY_CONTAINER: Long = 0xFFF2FAF4
    public const val HC_DARK_BACKGROUND: Long = 0xFF0F0E0E
    public const val HC_DARK_ON_BACKGROUND: Long = 0xFFFFFFFF
    public const val HC_DARK_SURFACE: Long = 0xFF0F0E0E
    public const val HC_DARK_ON_SURFACE: Long = 0xFFFFFFFF
    public const val HC_DARK_SURFACE_VARIANT: Long = 0xFF131212
    public const val HC_DARK_ON_SURFACE_VARIANT: Long = 0xFFAEAAA6
    public const val HC_DARK_SURFACE_TINT: Long = 0xFF8BB2C3
    public const val HC_DARK_INVERSE_SURFACE: Long = 0xFFF4F3F3
    public const val HC_DARK_INVERSE_ON_SURFACE: Long = 0xFF000000
    public const val HC_DARK_ERROR: Long = 0xFFE6927B
    public const val HC_DARK_ON_ERROR: Long = 0xFF060505
    public const val HC_DARK_ERROR_CONTAINER: Long = 0xFF280E08
    public const val HC_DARK_ON_ERROR_CONTAINER: Long = 0xFFFFF3EF
    public const val HC_DARK_OUTLINE: Long = 0xFF84807C
    public const val HC_DARK_OUTLINE_VARIANT: Long = 0xFF84807C
    public const val HC_DARK_SCRIM: Long = 0xFFFFFFFF
    public const val HC_DARK_SURFACE_BRIGHT: Long = 0xFF151515
    public const val HC_DARK_SURFACE_DIM: Long = 0xFF000000
    public const val HC_DARK_SURFACE_CONTAINER: Long = 0xFF0F0E0E
    public const val HC_DARK_SURFACE_CONTAINER_HIGH: Long = 0xFF10100F
    public const val HC_DARK_SURFACE_CONTAINER_HIGHEST: Long = 0xFF131212
    public const val HC_DARK_SURFACE_CONTAINER_LOW: Long = 0xFF0A0A09
    public const val HC_DARK_SURFACE_CONTAINER_LOWEST: Long = 0xFF060505
    public const val HC_DARK_PRIMARY_FIXED: Long = 0xFFF2F9FC
    public const val HC_DARK_PRIMARY_FIXED_DIM: Long = 0xFFE3EFF5
    public const val HC_DARK_ON_PRIMARY_FIXED: Long = 0xFF0D191F
    public const val HC_DARK_ON_PRIMARY_FIXED_VARIANT: Long = 0xFF224959
    public const val HC_DARK_SECONDARY_FIXED: Long = 0xFFF8F7F6
    public const val HC_DARK_SECONDARY_FIXED_DIM: Long = 0xFFEEECEB
    public const val HC_DARK_ON_SECONDARY_FIXED: Long = 0xFF181716
    public const val HC_DARK_ON_SECONDARY_FIXED_VARIANT: Long = 0xFF464341
    public const val HC_DARK_TERTIARY_FIXED: Long = 0xFFF2FAF4
    public const val HC_DARK_TERTIARY_FIXED_DIM: Long = 0xFFE3F1E6
    public const val HC_DARK_ON_TERTIARY_FIXED: Long = 0xFF0C1B10
    public const val HC_DARK_ON_TERTIARY_FIXED_VARIANT: Long = 0xFF1B3020

}
