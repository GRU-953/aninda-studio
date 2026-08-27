// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
package studio.aninda.compose

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import studio.aninda.tokens.AnindaBangla

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
    script: AnindaScript = AnindaScript.LATIN,
): Typography {
    val m = script.multiplier
    fun style(sp: Float, weight: FontWeight = FontWeight.Normal) = TextStyle(
        fontFamily = family,
        fontWeight = weight,
        fontSize = (sp * m).sp,
        // Bangla needs more room between lines than Latin at the same size,
        // because its matra sits above the letters and its descenders below.
        lineHeight = (sp * m * script.lineHeight).sp,
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

/**
 * Which script a tree is set in, and what that does to its size.
 *
 * The multipliers were measured on rendered specimens rather than estimated:
 * Bangla's reading height sits near 0.62 em against Latin's 0.51, so equal nominal
 * sizes do not look equal.
 *
 * Material classifies Bangla as a MEDIUM language-height script needing roughly
 * 7 per cent taller line heights at the same nominal size. These figures are not
 * that measurement and are not offered as agreeing with it: this system's Bangla
 * leading is 1.6 against Latin's 1.55, which is +3.2 per cent, and the Bangla is
 * also set smaller — so its absolute line box is smaller, not larger. Both numbers
 * are published; neither confirms the other.
 */
public enum class AnindaScript(
    public val multiplier: Float,
    public val lineHeight: Float,
) {
    LATIN(1.0f, 1.55f),
    BANGLA(AnindaBangla.BODY, 1.6f),
}
