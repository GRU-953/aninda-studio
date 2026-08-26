// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.

/// Spacing, radii, target sizes and the type scale.
///
/// The target sizes are the interesting ones, and each carries the source
/// it came from in its own documentation comment. They are figures Apple
/// and Google publish, not figures this system chose.

public enum AnindaSpace {
    /// 4 pt
    public static let s0: Double = 4
    /// 8 pt
    public static let s1: Double = 8
    /// 12 pt
    public static let s2: Double = 12
    /// 16 pt
    public static let s3: Double = 16
    /// 24 pt
    public static let s4: Double = 24
    /// 32 pt
    public static let s5: Double = 32
    /// 48 pt
    public static let s6: Double = 48
    /// 64 pt
    public static let s7: Double = 64
    /// 96 pt
    public static let s8: Double = 96
    /// 128 pt
    public static let s9: Double = 128
}

public enum AnindaRadius {
    public static let badge: Double = 4
    public static let control: Double = 8
    public static let card: Double = 14
    public static let hero: Double = 24
}

public enum AnindaTarget {
    /// WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA — w3.org/TR/WCAG22/#target-size-minimum, Recommendation 12 December 2024, read 14 August 2026
    public static let min: Double = 24
    /// Apple HIG minimum control size, iOS and iPadOS — developer.apple.com/design/human-interface-guidelines/accessibility, read 14 August 2026
    public static let appleMin: Double = 28
    /// Apple HIG default control size, iOS and iPadOS — developer.apple.com/design/human-interface-guidelines/accessibility, read 14 August 2026
    public static let comfortable: Double = 44
    /// Android accessibility guidance minimum touch target, in dp — developer.android.com accessibility pages, read 14 August 2026
    public static let androidMin: Double = 48
}

public enum AnindaFocus {
    public static let ringWidth: Double = 3
    public static let ringOffset: Double = 2
}

/// The type scale, in rem against a 16 pt root.
///
/// Apple's default body size is 17 pt and this system's is 16. The
/// divergence is recorded rather than reconciled: changing the scale to
/// suit one platform would change it for the web too, and the scale is a
/// perfect fourth whose steps were chosen together. `bodyPoints` below is
/// what a caller should scale from.
public enum AnindaType {
    /// The root this scale is expressed against.
    public static let rootPoints: Double = 16.0
    /// 12.00 pt at a 16 pt root
    public static let caption: Double = 0.7502
    /// 16.00 pt at a 16 pt root
    public static let body: Double = 1
    /// 21.33 pt at a 16 pt root
    public static let lead: Double = 1.333
    /// 28.43 pt at a 16 pt root
    public static let h3: Double = 1.7769
    /// 37.90 pt at a 16 pt root
    public static let h2: Double = 2.3686
    /// 50.52 pt at a 16 pt root
    public static let h1: Double = 3.1573
    /// 67.34 pt at a 16 pt root
    public static let display: Double = 4.2087
}

/// Bangla is set smaller than Latin so the two look the same size, and
/// the multipliers were measured on rendered specimens rather than
/// estimated. Below `weightBumpBelowPoints` the weight steps up, because
/// the matra thins out on the pixel grid before the glyph does — the two
/// rules only work together.
public enum AnindaBangla {
    public static let caption: Double = 0.815
    public static let body: Double = 0.816
    public static let heading: Double = 0.817
    public static let title: Double = 0.822
    public static let display: Double = 0.825
    public static let minimumPoints: Double = 12
    public static let weightBumpBelowPoints: Double = 14
    public static let banglaLineHeight: Double = 1.6
}

public enum AnindaMotion {
    public static let colourMilliseconds: Double = 120
    public static let moveMilliseconds: Double = 220
}
