// GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — the next build overwrites it.
import XCTest
@testable import AnindaTokens

/// These assert the SHAPE of the emitted surface, not the values.
///
/// Checking a value here would mean writing it down a second time, and a second
/// copy of a number is the thing this whole system is built to avoid. The values
/// are checked against the DTCG tokens by 15_native/build.py, which reads the
/// emitted file back and re-derives every component from the hex.
final class AnindaTokensTests: XCTestCase {
    func testEveryThemeHasAPalette() {
        for theme in AnindaTheme.allCases {
            let p = AnindaColours.palette(for: theme)
            XCTAssertTrue(p.accent.hex.hasPrefix("#"))
            XCTAssertEqual(p.accent.hex.count, 7)
        }
    }

    func testComponentsAgreeWithTheirOwnHex() {
        for theme in AnindaTheme.allCases {
            let c = AnindaColours.palette(for: theme).accent
            let r = Int(c.hex.dropFirst(1).prefix(2), radix: 16)!
            XCTAssertEqual(c.red, Double(r) / 255.0, accuracy: 1e-6)
        }
    }

    func testBanglaFloorIsBelowItsSmallestStep() {
        XCTAssertLessThanOrEqual(AnindaBangla.minimumPoints,
                                 AnindaType.caption * AnindaType.rootPoints)
    }
}
