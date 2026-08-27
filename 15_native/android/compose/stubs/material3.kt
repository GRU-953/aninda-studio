// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
//
// A DECLARED SURFACE, not androidx. See compose_stubs() in 15_native/build.py
// for what compiling against this does and does not prove.
//
// Declarations read from: compose-bom 1.4.0 (stable, 12 August 2026) — androidx.compose.material3 1.4.0, androidx.compose.foundation 1.4.0, androidx.compose.ui 1.4.0. Read 27 August 2026.
@file:Suppress("unused", "UNUSED_PARAMETER")

package androidx.compose.material3

import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp

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

// A function and an object may share a name in Kotlin, which is exactly how
// androidx declares this: MaterialTheme(...) wraps a tree, MaterialTheme.colorScheme
// reads out of it. The object is the ONLY way a Compose pattern takes a type size
// or a colour without writing a literal, so without it the authored screens could
// not satisfy guard_authored_uses_tokens() at all.
//
// The getters throw. A declared surface has no values in it — these resolve types,
// and the compile never runs them. Returning a constructed ColorScheme would mean
// typing 48 placeholder colours, which reads like data and is not.
public object MaterialTheme {
    private const val SURFACE = "declared surface: types only, no values"
    public val colorScheme: ColorScheme @Composable get() = error(SURFACE)
    public val typography: Typography @Composable get() = error(SURFACE)
    public val shapes: Shapes @Composable get() = error(SURFACE)
}

// ---------------------------------------------------------------------------
// The composables the eight patterns use.
//
// One per component card, and no more. There is no LazyColumn (the screens are
// fixed-length examples, so a Column and a forEach is enough and halves this
// file), no Icons (a separate artifact, and stubbing an icon set proves nothing),
// and no navigation. A pattern that needs something else needs a COMPONENT, and
// the component library is where that goes.
// ---------------------------------------------------------------------------

@Composable
public fun Text(
    text: String,
    modifier: Modifier = Modifier,
    color: Color? = null,
    style: TextStyle? = null,
    textAlign: TextAlign? = null,
    maxLines: Int = Int.MAX_VALUE,
) { }

@Composable
public fun Button(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    content: @Composable RowScope.() -> Unit,
) { }

@Composable
public fun OutlinedButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    content: @Composable RowScope.() -> Unit,
) { }

@Composable
public fun TextButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    content: @Composable RowScope.() -> Unit,
) { }

@Composable
public fun OutlinedTextField(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    label: (@Composable () -> Unit)? = null,
    supportingText: (@Composable () -> Unit)? = null,
    isError: Boolean = false,
    singleLine: Boolean = false,
    minLines: Int = 1,
    readOnly: Boolean = false,
) { }

@Composable
public fun Checkbox(
    checked: Boolean,
    onCheckedChange: ((Boolean) -> Unit)?,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
) { }

@Composable
public fun RadioButton(
    selected: Boolean,
    onClick: (() -> Unit)?,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
) { }

@Composable
public fun Card(
    modifier: Modifier = Modifier,
    shape: RoundedCornerShape? = null,
    content: @Composable ColumnScope.() -> Unit,
) { }

@Composable
public fun Surface(
    modifier: Modifier = Modifier,
    shape: RoundedCornerShape? = null,
    color: Color? = null,
    contentColor: Color? = null,
    border: Dp? = null,
    content: @Composable () -> Unit,
) { }

@Composable
public fun HorizontalDivider(
    modifier: Modifier = Modifier,
    thickness: Dp? = null,
    color: Color? = null,
) { }

@Composable
public fun TabRow(
    selectedTabIndex: Int,
    modifier: Modifier = Modifier,
    containerColor: Color? = null,
    contentColor: Color? = null,
    tabs: @Composable () -> Unit,
) { }

@Composable
public fun Tab(
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    text: (@Composable () -> Unit)? = null,
) { }
