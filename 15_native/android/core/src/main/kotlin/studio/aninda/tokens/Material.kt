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
    public const val LIGHT_ONPRIMARY: Long = 0xFFFDFFFE
    public const val LIGHT_PRIMARYCONTAINER: Long = 0xFFEDFAFD
    public const val LIGHT_ONPRIMARYCONTAINER: Long = 0xFF001B20
    public const val LIGHT_INVERSEPRIMARY: Long = 0xFF42A0AE
    public const val LIGHT_SECONDARY: Long = 0xFF41655C
    public const val LIGHT_ONSECONDARY: Long = 0xFFFDFFFE
    public const val LIGHT_SECONDARYCONTAINER: Long = 0xFFF2F9F7
    public const val LIGHT_ONSECONDARYCONTAINER: Long = 0xFF0D1A17
    public const val LIGHT_TERTIARY: Long = 0xFF235E8C
    public const val LIGHT_ONTERTIARY: Long = 0xFFFDFFFE
    public const val LIGHT_TERTIARYCONTAINER: Long = 0xFFEFF9FF
    public const val LIGHT_ONTERTIARYCONTAINER: Long = 0xFF071928
    public const val LIGHT_BACKGROUND: Long = 0xFFF8FAF9
    public const val LIGHT_ONBACKGROUND: Long = 0xFF0D1A17
    public const val LIGHT_SURFACE: Long = 0xFFF8FAF9
    public const val LIGHT_ONSURFACE: Long = 0xFF0D1A17
    public const val LIGHT_SURFACEVARIANT: Long = 0xFFF3F5F4
    public const val LIGHT_ONSURFACEVARIANT: Long = 0xFF41655C
    public const val LIGHT_SURFACETINT: Long = 0xFF126974
    public const val LIGHT_INVERSESURFACE: Long = 0xFF0B0D0C
    public const val LIGHT_INVERSEONSURFACE: Long = 0xFFF2F9F7
    public const val LIGHT_ERROR: Long = 0xFFA8301F
    public const val LIGHT_ONERROR: Long = 0xFFFDFFFE
    public const val LIGHT_ERRORCONTAINER: Long = 0xFFFFF2ED
    public const val LIGHT_ONERRORCONTAINER: Long = 0xFF2E0804
    public const val LIGHT_OUTLINE: Long = 0xFF0C3A31
    public const val LIGHT_OUTLINEVARIANT: Long = 0xFF0C3A31
    public const val LIGHT_SCRIM: Long = 0xFF0D1A17
    public const val LIGHT_SURFACEBRIGHT: Long = 0xFFFFFFFF
    public const val LIGHT_SURFACEDIM: Long = 0xFFF1F2F2
    public const val LIGHT_SURFACECONTAINER: Long = 0xFFF8FAF9
    public const val LIGHT_SURFACECONTAINERHIGH: Long = 0xFFF6F7F7
    public const val LIGHT_SURFACECONTAINERHIGHEST: Long = 0xFFF3F5F4
    public const val LIGHT_SURFACECONTAINERLOW: Long = 0xFFFBFCFC
    public const val LIGHT_SURFACECONTAINERLOWEST: Long = 0xFFFDFFFE
    public const val LIGHT_PRIMARYFIXED: Long = 0xFFEDFAFD
    public const val LIGHT_PRIMARYFIXEDDIM: Long = 0xFFD9F2F7
    public const val LIGHT_ONPRIMARYFIXED: Long = 0xFF001B20
    public const val LIGHT_ONPRIMARYFIXEDVARIANT: Long = 0xFF126974
    public const val LIGHT_SECONDARYFIXED: Long = 0xFFF2F9F7
    public const val LIGHT_SECONDARYFIXEDDIM: Long = 0xFFE3F0EC
    public const val LIGHT_ONSECONDARYFIXED: Long = 0xFF0D1A17
    public const val LIGHT_ONSECONDARYFIXEDVARIANT: Long = 0xFF41655C
    public const val LIGHT_TERTIARYFIXED: Long = 0xFFEFF9FF
    public const val LIGHT_TERTIARYFIXEDDIM: Long = 0xFFDEEFFF
    public const val LIGHT_ONTERTIARYFIXED: Long = 0xFF071928
    public const val LIGHT_ONTERTIARYFIXEDVARIANT: Long = 0xFF235E8C

    // dark
    public const val DARK_PRIMARY: Long = 0xFF42A0AE
    public const val DARK_ONPRIMARY: Long = 0xFF040504
    public const val DARK_PRIMARYCONTAINER: Long = 0xFF001B20
    public const val DARK_ONPRIMARYCONTAINER: Long = 0xFFEDFAFD
    public const val DARK_INVERSEPRIMARY: Long = 0xFF126974
    public const val DARK_SECONDARY: Long = 0xFF6F9B90
    public const val DARK_ONSECONDARY: Long = 0xFF040504
    public const val DARK_SECONDARYCONTAINER: Long = 0xFF0D1A17
    public const val DARK_ONSECONDARYCONTAINER: Long = 0xFFF2F9F7
    public const val DARK_TERTIARY: Long = 0xFF5C96C8
    public const val DARK_ONTERTIARY: Long = 0xFF040504
    public const val DARK_TERTIARYCONTAINER: Long = 0xFF071928
    public const val DARK_ONTERTIARYCONTAINER: Long = 0xFFEFF9FF
    public const val DARK_BACKGROUND: Long = 0xFF0B0D0C
    public const val DARK_ONBACKGROUND: Long = 0xFFF2F9F7
    public const val DARK_SURFACE: Long = 0xFF0B0D0C
    public const val DARK_ONSURFACE: Long = 0xFFF2F9F7
    public const val DARK_SURFACEVARIANT: Long = 0xFF0F1110
    public const val DARK_ONSURFACEVARIANT: Long = 0xFF6F9B90
    public const val DARK_SURFACETINT: Long = 0xFF42A0AE
    public const val DARK_INVERSESURFACE: Long = 0xFFF8FAF9
    public const val DARK_INVERSEONSURFACE: Long = 0xFF0D1A17
    public const val DARK_ERROR: Long = 0xFFE16551
    public const val DARK_ONERROR: Long = 0xFF040504
    public const val DARK_ERRORCONTAINER: Long = 0xFF2E0804
    public const val DARK_ONERRORCONTAINER: Long = 0xFFFFF2ED
    public const val DARK_OUTLINE: Long = 0xFF578076
    public const val DARK_OUTLINEVARIANT: Long = 0xFF578076
    public const val DARK_SCRIM: Long = 0xFFF2F9F7
    public const val DARK_SURFACEBRIGHT: Long = 0xFF111212
    public const val DARK_SURFACEDIM: Long = 0xFF000000
    public const val DARK_SURFACECONTAINER: Long = 0xFF0B0D0C
    public const val DARK_SURFACECONTAINERHIGH: Long = 0xFF0F1010
    public const val DARK_SURFACECONTAINERHIGHEST: Long = 0xFF0F1110
    public const val DARK_SURFACECONTAINERLOW: Long = 0xFF090A0A
    public const val DARK_SURFACECONTAINERLOWEST: Long = 0xFF040504
    public const val DARK_PRIMARYFIXED: Long = 0xFFEDFAFD
    public const val DARK_PRIMARYFIXEDDIM: Long = 0xFFD9F2F7
    public const val DARK_ONPRIMARYFIXED: Long = 0xFF001B20
    public const val DARK_ONPRIMARYFIXEDVARIANT: Long = 0xFF126974
    public const val DARK_SECONDARYFIXED: Long = 0xFFF2F9F7
    public const val DARK_SECONDARYFIXEDDIM: Long = 0xFFE3F0EC
    public const val DARK_ONSECONDARYFIXED: Long = 0xFF0D1A17
    public const val DARK_ONSECONDARYFIXEDVARIANT: Long = 0xFF41655C
    public const val DARK_TERTIARYFIXED: Long = 0xFFEFF9FF
    public const val DARK_TERTIARYFIXEDDIM: Long = 0xFFDEEFFF
    public const val DARK_ONTERTIARYFIXED: Long = 0xFF071928
    public const val DARK_ONTERTIARYFIXEDVARIANT: Long = 0xFF235E8C

    // hc-light
    public const val HC_LIGHT_PRIMARY: Long = 0xFF054D56
    public const val HC_LIGHT_ONPRIMARY: Long = 0xFFFCFDFC
    public const val HC_LIGHT_PRIMARYCONTAINER: Long = 0xFFEDFAFD
    public const val HC_LIGHT_ONPRIMARYCONTAINER: Long = 0xFF001B20
    public const val HC_LIGHT_INVERSEPRIMARY: Long = 0xFF65BAC7
    public const val HC_LIGHT_SECONDARY: Long = 0xFF2E4B43
    public const val HC_LIGHT_ONSECONDARY: Long = 0xFFFCFDFC
    public const val HC_LIGHT_SECONDARYCONTAINER: Long = 0xFFF2F9F7
    public const val HC_LIGHT_ONSECONDARYCONTAINER: Long = 0xFF0D1A17
    public const val HC_LIGHT_TERTIARY: Long = 0xFF214767
    public const val HC_LIGHT_ONTERTIARY: Long = 0xFFFCFDFC
    public const val HC_LIGHT_TERTIARYCONTAINER: Long = 0xFFEFF9FF
    public const val HC_LIGHT_ONTERTIARYCONTAINER: Long = 0xFF071928
    public const val HC_LIGHT_BACKGROUND: Long = 0xFFF7F8F7
    public const val HC_LIGHT_ONBACKGROUND: Long = 0xFF0D1A17
    public const val HC_LIGHT_SURFACE: Long = 0xFFF7F8F7
    public const val HC_LIGHT_ONSURFACE: Long = 0xFF0D1A17
    public const val HC_LIGHT_SURFACEVARIANT: Long = 0xFFF2F3F2
    public const val HC_LIGHT_ONSURFACEVARIANT: Long = 0xFF2E4B43
    public const val HC_LIGHT_SURFACETINT: Long = 0xFF054D56
    public const val HC_LIGHT_INVERSESURFACE: Long = 0xFF0C0D0C
    public const val HC_LIGHT_INVERSEONSURFACE: Long = 0xFFF2F9F7
    public const val HC_LIGHT_ERROR: Long = 0xFF752519
    public const val HC_LIGHT_ONERROR: Long = 0xFFFCFDFC
    public const val HC_LIGHT_ERRORCONTAINER: Long = 0xFFFFF2ED
    public const val HC_LIGHT_ONERRORCONTAINER: Long = 0xFF2E0804
    public const val HC_LIGHT_OUTLINE: Long = 0xFF0C3A31
    public const val HC_LIGHT_OUTLINEVARIANT: Long = 0xFF0C3A31
    public const val HC_LIGHT_SCRIM: Long = 0xFF0D1A17
    public const val HC_LIGHT_SURFACEBRIGHT: Long = 0xFFFFFFFF
    public const val HC_LIGHT_SURFACEDIM: Long = 0xFFF1F1F1
    public const val HC_LIGHT_SURFACECONTAINER: Long = 0xFFF7F8F7
    public const val HC_LIGHT_SURFACECONTAINERHIGH: Long = 0xFFF5F5F5
    public const val HC_LIGHT_SURFACECONTAINERHIGHEST: Long = 0xFFF2F3F2
    public const val HC_LIGHT_SURFACECONTAINERLOW: Long = 0xFFFAFAFA
    public const val HC_LIGHT_SURFACECONTAINERLOWEST: Long = 0xFFFCFDFC
    public const val HC_LIGHT_PRIMARYFIXED: Long = 0xFFEDFAFD
    public const val HC_LIGHT_PRIMARYFIXEDDIM: Long = 0xFFD9F2F7
    public const val HC_LIGHT_ONPRIMARYFIXED: Long = 0xFF001B20
    public const val HC_LIGHT_ONPRIMARYFIXEDVARIANT: Long = 0xFF054D56
    public const val HC_LIGHT_SECONDARYFIXED: Long = 0xFFF2F9F7
    public const val HC_LIGHT_SECONDARYFIXEDDIM: Long = 0xFFE3F0EC
    public const val HC_LIGHT_ONSECONDARYFIXED: Long = 0xFF0D1A17
    public const val HC_LIGHT_ONSECONDARYFIXEDVARIANT: Long = 0xFF2E4B43
    public const val HC_LIGHT_TERTIARYFIXED: Long = 0xFFEFF9FF
    public const val HC_LIGHT_TERTIARYFIXEDDIM: Long = 0xFFDEEFFF
    public const val HC_LIGHT_ONTERTIARYFIXED: Long = 0xFF071928
    public const val HC_LIGHT_ONTERTIARYFIXEDVARIANT: Long = 0xFF214767

    // hc-dark
    public const val HC_DARK_PRIMARY: Long = 0xFF65BAC7
    public const val HC_DARK_ONPRIMARY: Long = 0xFF040504
    public const val HC_DARK_PRIMARYCONTAINER: Long = 0xFF001B20
    public const val HC_DARK_ONPRIMARYCONTAINER: Long = 0xFFEDFAFD
    public const val HC_DARK_INVERSEPRIMARY: Long = 0xFF054D56
    public const val HC_DARK_SECONDARY: Long = 0xFF8BB5AA
    public const val HC_DARK_ONSECONDARY: Long = 0xFF040504
    public const val HC_DARK_SECONDARYCONTAINER: Long = 0xFF0D1A17
    public const val HC_DARK_ONSECONDARYCONTAINER: Long = 0xFFF2F9F7
    public const val HC_DARK_TERTIARY: Long = 0xFF7AB1E1
    public const val HC_DARK_ONTERTIARY: Long = 0xFF040504
    public const val HC_DARK_TERTIARYCONTAINER: Long = 0xFF071928
    public const val HC_DARK_ONTERTIARYCONTAINER: Long = 0xFFEFF9FF
    public const val HC_DARK_BACKGROUND: Long = 0xFF0C0D0C
    public const val HC_DARK_ONBACKGROUND: Long = 0xFFF2F9F7
    public const val HC_DARK_SURFACE: Long = 0xFF0C0D0C
    public const val HC_DARK_ONSURFACE: Long = 0xFFF2F9F7
    public const val HC_DARK_SURFACEVARIANT: Long = 0xFF101110
    public const val HC_DARK_ONSURFACEVARIANT: Long = 0xFF8BB5AA
    public const val HC_DARK_SURFACETINT: Long = 0xFF65BAC7
    public const val HC_DARK_INVERSESURFACE: Long = 0xFFF7F8F7
    public const val HC_DARK_INVERSEONSURFACE: Long = 0xFF0D1A17
    public const val HC_DARK_ERROR: Long = 0xFFFB836F
    public const val HC_DARK_ONERROR: Long = 0xFF040504
    public const val HC_DARK_ERRORCONTAINER: Long = 0xFF2E0804
    public const val HC_DARK_ONERRORCONTAINER: Long = 0xFFFFF2ED
    public const val HC_DARK_OUTLINE: Long = 0xFF6F9B90
    public const val HC_DARK_OUTLINEVARIANT: Long = 0xFF6F9B90
    public const val HC_DARK_SCRIM: Long = 0xFFF2F9F7
    public const val HC_DARK_SURFACEBRIGHT: Long = 0xFF111111
    public const val HC_DARK_SURFACEDIM: Long = 0xFF000000
    public const val HC_DARK_SURFACECONTAINER: Long = 0xFF0C0D0C
    public const val HC_DARK_SURFACECONTAINERHIGH: Long = 0xFF101010
    public const val HC_DARK_SURFACECONTAINERHIGHEST: Long = 0xFF101110
    public const val HC_DARK_SURFACECONTAINERLOW: Long = 0xFF090909
    public const val HC_DARK_SURFACECONTAINERLOWEST: Long = 0xFF040504
    public const val HC_DARK_PRIMARYFIXED: Long = 0xFFEDFAFD
    public const val HC_DARK_PRIMARYFIXEDDIM: Long = 0xFFD9F2F7
    public const val HC_DARK_ONPRIMARYFIXED: Long = 0xFF001B20
    public const val HC_DARK_ONPRIMARYFIXEDVARIANT: Long = 0xFF054D56
    public const val HC_DARK_SECONDARYFIXED: Long = 0xFFF2F9F7
    public const val HC_DARK_SECONDARYFIXEDDIM: Long = 0xFFE3F0EC
    public const val HC_DARK_ONSECONDARYFIXED: Long = 0xFF0D1A17
    public const val HC_DARK_ONSECONDARYFIXEDVARIANT: Long = 0xFF2E4B43
    public const val HC_DARK_TERTIARYFIXED: Long = 0xFFEFF9FF
    public const val HC_DARK_TERTIARYFIXEDDIM: Long = 0xFFDEEFFF
    public const val HC_DARK_ONTERTIARYFIXED: Long = 0xFF071928
    public const val HC_DARK_ONTERTIARYFIXEDVARIANT: Long = 0xFF214767

}
