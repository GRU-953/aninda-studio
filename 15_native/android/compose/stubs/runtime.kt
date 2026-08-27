// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
//
// A DECLARED SURFACE, not androidx. See compose_stubs() in 15_native/build.py
// for what compiling against this does and does not prove.
@file:Suppress("unused", "UNUSED_PARAMETER")

package androidx.compose.runtime

// TYPE and TYPE_PARAMETER are what let @Composable sit on a function TYPE, which
// is how every content lambda in Compose is declared. Without them kotlinc refuses
// `content: @Composable () -> Unit` — the shape of essentially every composable
// that takes children.
@Target(
    AnnotationTarget.CLASS,
    AnnotationTarget.FUNCTION,
    AnnotationTarget.PROPERTY_GETTER,
    AnnotationTarget.PROPERTY_SETTER,
    AnnotationTarget.TYPE,
    AnnotationTarget.TYPE_PARAMETER,
    AnnotationTarget.PROPERTY,
)
@Retention(AnnotationRetention.BINARY)
public annotation class Composable

public interface CompositionLocal<T> { public val current: T }

public class ProvidableCompositionLocal<T>(private val v: T) : CompositionLocal<T> {
    override val current: T get() = v
    public infix fun provides(value: T): Pair<ProvidableCompositionLocal<T>, T> =
        this to value
}

public fun <T> staticCompositionLocalOf(default: () -> T):
    ProvidableCompositionLocal<T> = ProvidableCompositionLocal(default())

@Composable
public fun CompositionLocalProvider(
    vararg values: Pair<ProvidableCompositionLocal<*>, Any?>,
    content: @Composable () -> Unit,
) { }
