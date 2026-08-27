// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
//
// A DECLARED SURFACE, not androidx. See compose_stubs() in 15_native/build.py
// for what compiling against this does and does not prove.
//
// Declarations read from: compose-bom 1.4.0 (stable, 12 August 2026) — androidx.compose.material3 1.4.0, androidx.compose.foundation 1.4.0, androidx.compose.ui 1.4.0. Read 27 August 2026.
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

// State. `by remember { mutableStateOf(x) }` is how every one of the eight
// patterns holds its own field values, so the delegation operators have to be
// here or the `by` refuses to compile.
public interface State<out T> { public val value: T }
public interface MutableState<T> : State<T> { public override var value: T }

public fun <T> mutableStateOf(value: T): MutableState<T> = object : MutableState<T> {
    override var value: T = value
}

@Composable
public fun <T> remember(calculation: () -> T): T = calculation()

@Composable
public fun <T> remember(key1: Any?, calculation: () -> T): T = calculation()

public operator fun <T> State<T>.getValue(thisObj: Any?, property: Any?): T = value
public operator fun <T> MutableState<T>.setValue(
    thisObj: Any?, property: Any?, value: T,
) { this.value = value }
