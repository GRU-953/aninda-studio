// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
//
// A DECLARED SURFACE, not androidx. See compose_stubs() in 15_native/build.py
// for what compiling against this does and does not prove.
@file:Suppress("unused", "UNUSED_PARAMETER")

package androidx.compose.material3

import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.foundation.shape.RoundedCornerShape

// Every parameter, and NO defaults. That is the completeness gate: a role left out
// is a compile error rather than Material's baseline purple shipped in silence.
// The list is read from material3.roles.json, which took it from ColorScheme.kt on
// androidx-main, so the stub cannot drift from the list the derivation used.
public class ColorScheme(
    public val primary: Color,
    public val onPrimary: Color,
    public val primaryContainer: Color,
    public val onPrimaryContainer: Color,
    public val inversePrimary: Color,
    public val secondary: Color,
    public val onSecondary: Color,
    public val secondaryContainer: Color,
    public val onSecondaryContainer: Color,
    public val tertiary: Color,
    public val onTertiary: Color,
    public val tertiaryContainer: Color,
    public val onTertiaryContainer: Color,
    public val background: Color,
    public val onBackground: Color,
    public val surface: Color,
    public val onSurface: Color,
    public val surfaceVariant: Color,
    public val onSurfaceVariant: Color,
    public val surfaceTint: Color,
    public val inverseSurface: Color,
    public val inverseOnSurface: Color,
    public val error: Color,
    public val onError: Color,
    public val errorContainer: Color,
    public val onErrorContainer: Color,
    public val outline: Color,
    public val outlineVariant: Color,
    public val scrim: Color,
    public val surfaceBright: Color,
    public val surfaceDim: Color,
    public val surfaceContainer: Color,
    public val surfaceContainerHigh: Color,
    public val surfaceContainerHighest: Color,
    public val surfaceContainerLow: Color,
    public val surfaceContainerLowest: Color,
    public val primaryFixed: Color,
    public val primaryFixedDim: Color,
    public val onPrimaryFixed: Color,
    public val onPrimaryFixedVariant: Color,
    public val secondaryFixed: Color,
    public val secondaryFixedDim: Color,
    public val onSecondaryFixed: Color,
    public val onSecondaryFixedVariant: Color,
    public val tertiaryFixed: Color,
    public val tertiaryFixedDim: Color,
    public val onTertiaryFixed: Color,
    public val onTertiaryFixedVariant: Color,
)

public class Shapes(
    public val extraSmall: RoundedCornerShape,
    public val small: RoundedCornerShape,
    public val medium: RoundedCornerShape,
    public val large: RoundedCornerShape,
    public val extraLarge: RoundedCornerShape,
)

public class Typography(
    public val displayLarge: TextStyle, public val displayMedium: TextStyle,
    public val displaySmall: TextStyle, public val headlineLarge: TextStyle,
    public val headlineMedium: TextStyle, public val headlineSmall: TextStyle,
    public val titleLarge: TextStyle, public val titleMedium: TextStyle,
    public val titleSmall: TextStyle, public val bodyLarge: TextStyle,
    public val bodyMedium: TextStyle, public val bodySmall: TextStyle,
    public val labelLarge: TextStyle, public val labelMedium: TextStyle,
    public val labelSmall: TextStyle,
)

@Composable
public fun MaterialTheme(
    colorScheme: ColorScheme,
    typography: Typography,
    shapes: Shapes,
    content: @Composable () -> Unit,
) { }
