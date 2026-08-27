// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
package studio.aninda.compose

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

/** The line height this scale is set at. */
private const val LINE_HEIGHT = 1.55f

/**
 * Material's type slots, filled with THIS system's scale rather than Material's.
 *
 * Material's own scale runs on a Major Second, 1.125, from a 14 sp base. This one
 * is a perfect fourth, 1.333, from 16. Adopting Material's numbers would discard a
 * scale whose steps were chosen together, so the slot NAMES are Material's and the
 * sizes are not — which is the supported way to customise it.
 *
 * The mapping is stated rather than implied: Material has fifteen slots and this
 * system has seven sizes, so several slots share one.
 */
public fun anindaTypography(
    family: FontFamily = FontFamily.Default,
): Typography {
    fun style(sp: Float, weight: FontWeight = FontWeight.Normal) = TextStyle(
        fontFamily = family,
        fontWeight = weight,
        fontSize = sp.sp,
        lineHeight = (sp * LINE_HEIGHT).sp,
    )
    return Typography(
        displayLarge = style(67.34f), displayMedium = style(50.52f),
        displaySmall = style(37.90f),
        headlineLarge = style(37.90f), headlineMedium = style(28.43f),
        headlineSmall = style(21.33f),
        titleLarge = style(21.33f, FontWeight.Medium),
        titleMedium = style(16f, FontWeight.Medium),
        titleSmall = style(16f, FontWeight.Medium),
        bodyLarge = style(16f), bodyMedium = style(16f), bodySmall = style(12f),
        labelLarge = style(16f, FontWeight.Medium),
        labelMedium = style(12f, FontWeight.Medium),
        labelSmall = style(12f, FontWeight.Medium),
    )
}

// A `script` PARAMETER AND AN `AnindaScript` ENUM WERE HERE, and removing them is
// a source-breaking change to a published API rather than an internal tidy — which
// is why the package version goes to 2.0.0 in the same body of work.
//
// The enum carried two cases, LATIN and BANGLA, and Bangla's multiplier and
// leading with them. What it recorded is worth keeping: Material classifies Bangla
// as a MEDIUM language-height script needing roughly 7 per cent taller line
// heights at the same nominal size, and this system's own measurement did NOT
// agree with that figure — its Bangla leading was 1.6 against Latin's 1.55, +3.2
// per cent, and the Bangla was also set smaller, so its absolute line box was
// smaller rather than larger. Both numbers were published and neither was offered
// as confirming the other. 06_type/MEASUREMENTS.md keeps the measurement.
