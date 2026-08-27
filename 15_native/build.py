#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
Until now this design system stopped at the browser. Tokens emitted CSS, DTCG JSON,
TypeScript and Python, and 01_research/BENCHMARK.md criterion 23 recorded in writing
that no Gradle or Kotlin file existed anywhere. A system that claims to produce
polished apps cannot reach one from a stylesheet.

This writes the token layer for both platforms, and it writes it FRAMEWORK-FREE on
purpose. No `import SwiftUI`, no `androidx`. That is not a limitation dressed up as
a choice — it is what makes the gate real:

    swiftc -typecheck   compiles the Swift here
    kotlinc             compiles the Kotlin here

Both run on this machine, so the emitted code is proven to compile rather than
asserted to. Framework code cannot make that claim: SwiftUI is an Apple-only
framework absent from the open-source Linux toolchain, and Compose needs the Android
SDK. Those layers come later, with a weaker gate, and LIMITS.md will say so plainly
rather than letting the strong gate here imply cover it does not give.

EVERY NUMBER IS RE-DERIVED
--------------------------
Nothing here holds a second copy of a value. Colours come from the DTCG token files,
the Material scheme from 15_native/_proof/material3.roles.json, and both are
compared against their sources before anything is written. An emitter that keeps its
own copy of a number is a second source of truth waiting to drift.

RUN
---
    cd <the repository folder>
    ./.venv/bin/python 15_native/build.py
    ./.venv/bin/python 15_native/build.py --check
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOKENS = ROOT / "07_tokens" / "build"
M3 = HERE / "_proof" / "material3.roles.json"
APPLE = HERE / "apple"
ANDROID = HERE / "android"

GENERATED = ("GENERATED FILE. Written by 15_native/build.py. Do not hand-edit — "
             "the next build overwrites it.")

# Two kinds of file live under 15_native, and confusing them would delete work.
#
# GENERATED — the token layers. Written by this script, swept if this script stops
# writing them, and never edited by hand.
#
# AUTHORED — the SwiftUI bridge, the Compose theme, and the components. These are
# CODE, not values. 08_components/src/components.css is the precedent: a
# hand-written source that a generator reads, guards and bundles rather than
# writes. Deriving a button's layout from a token file would mean inventing a
# component language, and this system has enough of those.
#
# The sweep is scoped to the generated trees ONLY. Everything under an authored
# root is read and gated, never removed.
AUTHORED_ROOTS = (
    "apple/Sources/AnindaTokensUI",
    "apple/Sources/AnindaComponents",
    "apple/Sources/AnindaExamples",
    "android/compose/src/main/kotlin",
)
# NOT the stubs. compose/stubs is GENERATED — it is in `files`, so the sweep keeps
# it — and listing it as authored made the second Kotlin pass collect it twice,
# once from `files` and once off disk. kotlinc then reported "overload resolution
# ambiguity between candidates" with the same signature printed twice, which is a
# confusing way to be told a file was compiled twice.


def is_authored(p: Path) -> bool:
    rel = p.relative_to(HERE).as_posix()
    return any(rel.startswith(root + "/") for root in AUTHORED_ROOTS)
THEMES = ("light", "dark", "hc-light", "hc-dark")
SWIFT_NAME = {"light": "light", "dark": "dark",
              "hc-light": "highContrastLight", "hc-dark": "highContrastDark"}


class BuildError(Exception):
    pass


class NotEquipped(Exception):
    pass


def load() -> dict:
    prim = json.loads((TOKENS / "primitive.tokens.json").read_text())
    sem = {t: json.loads((TOKENS / f"semantic.{t}.tokens.json").read_text())
           for t in THEMES}
    if not M3.exists():
        raise NotEquipped(f"{M3.relative_to(ROOT)} is missing. Run "
                          f"15_native/material3.py first.")
    return {"primitive": prim, "semantic": sem,
            "material3": json.loads(M3.read_text())}


def resolve(node: dict, prim: dict) -> str:
    v = node["$value"]
    if isinstance(v, str) and v.startswith("{"):
        cur = prim
        for part in v.strip("{}").split("."):
            cur = cur[part]
        return cur["$value"]["hex"]
    return v["hex"]


def semantic_colours(data: dict, theme: str) -> dict[str, str]:
    """Flatten one theme's colour tokens to name -> hex, exactly as tokens.css does."""
    out: dict[str, str] = {}
    prim = data["primitive"]
    colour = data["semantic"][theme]["color"]
    for group, node in colour.items():
        if group.startswith("$"):
            continue
        for leaf, spec in node.items():
            if leaf.startswith("$"):
                continue
            name = group if leaf == "default" else f"{group}-{leaf}"
            if group == "status":
                name = leaf
            out[name] = resolve(spec, prim)
    return out


def dimensions(data: dict) -> dict[str, dict[str, float]]:
    prim = data["primitive"]
    out: dict[str, dict[str, float]] = {}
    for group in ("space", "radius", "target", "focus"):
        node = prim.get("dimension", {}).get(group, {})
        out[group] = {k: v["$value"]["value"] for k, v in node.items()
                      if not k.startswith("$")}
    out["type"] = {k: v["$value"]["value"]
                   for k, v in prim.get("dimension", {}).get("type", {}).items()
                   if not k.startswith("$")}
    # `number` nests one level deeper than the dimension groups: scale.ratio is a
    # value, scale.bangla is a group of five, and lineHeight is its own group. Walk
    # it rather than assuming a shape.
    def walk(node, prefix=""):
        found = {}
        for k, v in node.items():
            if k.startswith("$"):
                continue
            if isinstance(v, dict) and "$value" in v:
                found[f"{prefix}{k}"] = v["$value"]
            elif isinstance(v, dict):
                found.update(walk(v, f"{prefix}{k}-"))
        return found

    out["number"] = walk(prim.get("number", {}))
    out["duration"] = {k: v["value"] for k, v in
                       walk(prim.get("duration", {})).items()}
    return out


# =========================================================================
# Apple — framework-free Swift
# =========================================================================

def swift_ident(name: str) -> str:
    head, *rest = name.split("-")
    return head + "".join(p.capitalize() for p in rest)


def swift_colours(data: dict) -> str:
    L = [f"// {GENERATED}", "",
         "/// Every colour this system measured, for all four themes.",
         "///",
         "/// This file imports nothing. That is deliberate: it means `swiftc",
         "/// -typecheck` compiles it, so the values are proven to build rather than",
         "/// asserted to. The SwiftUI bridge sits in AnindaTokensUI, where no such",
         "/// proof is possible on a machine without Apple's SDKs.",
         "///",
         "/// Components are 0...1 sRGB, derived from the hex rather than typed",
         "/// beside it, so the two cannot disagree.", "",
         "public struct AnindaColour: Sendable, Equatable {",
         "    public let hex: String",
         "    public let red: Double",
         "    public let green: Double",
         "    public let blue: Double",
         "",
         "    public init(_ hex: String, _ r: Double, _ g: Double, _ b: Double) {",
         "        self.hex = hex; self.red = r; self.green = g; self.blue = b",
         "    }",
         "}", "",
         "public enum AnindaTheme: String, Sendable, CaseIterable {"]
    for t in THEMES:
        L.append(f'    case {SWIFT_NAME[t]} = "{t}"')
    L += ["}", "",
          "public struct AnindaPalette: Sendable {"]
    names = sorted(semantic_colours(data, "light"))
    for n in names:
        L.append(f"    public let {swift_ident(n)}: AnindaColour")
    L += ["}", "", "public enum AnindaColours {"]
    for t in THEMES:
        cols = semantic_colours(data, t)
        L.append(f"    /// The {t} theme.")
        L.append(f"    public static let {SWIFT_NAME[t]} = AnindaPalette(")
        rows = []
        for n in names:
            h = cols[n]
            r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
            rows.append(f'        {swift_ident(n)}: AnindaColour("{h}", '
                        f"{r:.6f}, {g:.6f}, {b:.6f})")
        L.append(",\n".join(rows))
        L.append("    )")
        L.append("")
    L += ["    public static func palette(for theme: AnindaTheme) -> AnindaPalette {",
          "        switch theme {"]
    for t in THEMES:
        L.append(f"        case .{SWIFT_NAME[t]}: return {SWIFT_NAME[t]}")
    L += ["        }", "    }", "}", ""]
    return "\n".join(L)


def swift_dimensions(data: dict) -> str:
    d = dimensions(data)
    prim = data["primitive"]

    def described(group: str, key: str) -> str:
        node = prim.get("dimension", {}).get(group, {}).get(key, {})
        return node.get("$description", "")

    L = [f"// {GENERATED}", "",
         "/// Spacing, radii, target sizes and the type scale.",
         "///",
         "/// The target sizes are the interesting ones, and each carries the source",
         "/// it came from in its own documentation comment. They are figures Apple",
         "/// and Google publish, not figures this system chose.", "",
         "public enum AnindaSpace {"]
    for k, v in sorted(d["space"].items(), key=lambda kv: int(kv[0])):
        L.append(f"    /// {v:g} pt")
        L.append(f"    public static let s{k}: Double = {v:g}")
    L += ["}", "", "public enum AnindaRadius {"]
    for k, v in d["radius"].items():
        L.append(f"    public static let {swift_ident(k)}: Double = {v:g}")
    L += ["}", "", "public enum AnindaTarget {"]
    for k, v in d["target"].items():
        doc = described("target", k)
        if doc:
            L.append(f"    /// {doc}")
        L.append(f"    public static let {swift_ident(k)}: Double = {v:g}")
    L += ["}", "", "public enum AnindaFocus {"]
    for k, v in d["focus"].items():
        L.append(f"    public static let {swift_ident(k)}: Double = {v:g}")
    L += ["}", "",
          "/// The type scale, in rem against a 16 pt root.",
          "///",
          "/// Apple's default body size is 17 pt and this system's is 16. The",
          "/// divergence is recorded rather than reconciled: changing the scale to",
          "/// suit one platform would change it for the web too, and the scale is a",
          "/// perfect fourth whose steps were chosen together. `bodyPoints` below is",
          "/// what a caller should scale from.",
          "public enum AnindaType {",
          "    /// The root this scale is expressed against.",
          "    public static let rootPoints: Double = 16.0"]
    for k, v in d["type"].items():
        if k in ("bangla-min", "bangla-weight-bump-below"):
            continue
        L.append(f"    /// {v * 16:.2f} pt at a 16 pt root")
        L.append(f"    public static let {swift_ident(k)}: Double = {v:g}")
    L += ["}", "",
          "/// Bangla is set smaller than Latin so the two look the same size, and",
          "/// the multipliers were measured on rendered specimens rather than",
          "/// estimated. Below `weightBumpBelowPoints` the weight steps up, because",
          "/// the matra thins out on the pixel grid before the glyph does — the two",
          "/// rules only work together.",
          "public enum AnindaBangla {"]
    for k, v in d["number"].items():
        if k.startswith("scale-bangla-"):
            L.append(f"    public static let {swift_ident(k[13:])}: Double = {v:g}")
    L.append(f"    public static let minimumPoints: Double = "
             f"{d['type'].get('bangla-min', 12):g}")
    L.append(f"    public static let weightBumpBelowPoints: Double = "
             f"{d['type'].get('bangla-weight-bump-below', 14):g}")
    for k, v in d["number"].items():
        if k.startswith("lineHeight-"):
            L.append(f"    public static let {swift_ident(k[11:])}LineHeight: "
                     f"Double = {v:g}")
    L += ["}", "", "public enum AnindaMotion {"]
    for k, v in d["duration"].items():
        L.append(f"    public static let {swift_ident(k[7:])}Milliseconds: "
                 f"Double = {v:g}")
    L += ["}", ""]
    return "\n".join(L)


# =========================================================================
# Android — framework-free Kotlin, plus resource XML
# =========================================================================

def kt_const(name: str) -> str:
    """SCREAMING_SNAKE, including from camelCase.

    A plain .upper() turns Material's `onSecondaryContainer` into
    ONSECONDARYCONTAINER, which is not a name anybody can read and is not what the
    Kotlin that consumes it expects. The boundary between a lower-case letter and
    an upper-case one is a word boundary, so it becomes an underscore.
    """
    import re as _re
    spaced = _re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return spaced.upper().replace("-", "_")


def kotlin_tokens(data: dict) -> str:
    d = dimensions(data)
    L = [f"// {GENERATED}", "", "package studio.aninda.tokens", "",
         "/**", " * Every colour this system measured, for all four themes, plus the",
         " * dimensions and the Bangla ramp.",
         " *",
         " * This file imports nothing — no androidx, no Compose. That is what lets",
         " * `kotlinc` compile it, so the values are proven to build rather than",
         " * asserted to. The Compose theme sits in the :compose module, where that",
         " * proof needs the Android toolchain.",
         " *",
         " * Colours are ARGB Longs. Kotlin has no unsigned Int literal that reads",
         " * well here, and a Long keeps the alpha byte visible.",
         " */", "",
         "public enum class AnindaTheme(public val key: String) {"]
    L += [f'    {kt_const(t).replace("-", "_")}("{t}"),' for t in THEMES]
    L += ["}", "", "public object AnindaColours {"]
    names = sorted(semantic_colours(data, "light"))
    for t in THEMES:
        cols = semantic_colours(data, t)
        L.append(f"    // The {t} theme.")
        for n in names:
            h = cols[n]
            L.append(f"    public const val {kt_const(t)}_{kt_const(n)}: Long = "
                     f"0xFF{h[1:].upper()}")
        L.append("")
    L += ["}", "", "public object AnindaSpace {"]
    for k, v in sorted(d["space"].items(), key=lambda kv: int(kv[0])):
        L.append(f"    /** {v:g} dp */")
        L.append(f"    public const val S{k}: Int = {int(v)}")
    L += ["}", "", "public object AnindaRadius {"]
    for k, v in d["radius"].items():
        L.append(f"    public const val {kt_const(k)}: Int = {int(v)}")
    L += ["}", "", "public object AnindaTarget {"]
    for k, v in d["target"].items():
        L.append(f"    public const val {kt_const(k)}: Int = {int(v)}")
    L += ["}", "",
          "/**",
          " * Bangla is set smaller than Latin so the two look the same size, and the",
          " * multipliers were measured on rendered specimens rather than estimated.",
          " *",
          " * Material classifies Bangla as a MEDIUM language-height script, needing",
          " * roughly 7 per cent taller line heights at the same nominal size. These",
          " * figures are not that measurement and are not offered as agreeing with",
          " * it: this system's Bangla leading is 1.6 against Latin's 1.55, which is",
          " * +3.2 per cent, and the Bangla is also set at x0.816 — so its absolute",
          " * line box is smaller, not larger. Both numbers are published; neither",
          " * confirms the other.",
          " */",
          "public object AnindaBangla {"]
    for k, v in d["number"].items():
        if k.startswith("scale-bangla-"):
            L.append(f"    public const val {kt_const(k[13:])}: Float = {v:g}f")
    L.append(f"    public const val MINIMUM_SP: Int = "
             f"{int(d['type'].get('bangla-min', 12))}")
    L.append(f"    public const val WEIGHT_BUMP_BELOW_SP: Int = "
             f"{int(d['type'].get('bangla-weight-bump-below', 14))}")
    L += ["}", "", "public object AnindaMotion {"]
    for k, v in d["duration"].items():
        L.append(f"    public const val {kt_const(k[7:])}_MS: Int = {int(v)}")
    L += ["}", ""]
    return "\n".join(L)


def kotlin_material(data: dict) -> str:
    """The Material scheme, still framework-free.

    The ColorScheme itself cannot be built without androidx, so this emits the 48
    values as constants and the :compose module assembles them. Splitting it this
    way is what keeps the numbers under a gate that actually runs: kotlinc compiles
    this file today, and the assembly above it compiles only where the Android SDK
    is installed.
    """
    m3 = data["material3"]
    params = m3["constructor"]["order"]
    L = [f"// {GENERATED}", "", "package studio.aninda.tokens", "",
         "/**", " * Material 3's 48 colour roles, derived from this system's measured",
         " * palette by 15_native/material3.py and proven there.",
         " *",
         " * Every value traces to a measured one: a semantic role, a tonal surface,",
         " * or a step of one of the six committed ramps. Nothing was interpolated.",
         " *",
         " * The names `background`, `onBackground` and `surfaceVariant` appear here",
         " * because androidx's ColorScheme constructor requires them. No TOKEN in",
         " * this system carries those names, which is what benchmark criterion 21",
         " * forbids.",
         " */",
         "public object AnindaMaterial {"]
    for t in THEMES:
        sch = m3["themes"][t]["scheme"]
        L.append(f"    // {t}")
        for p in params:
            L.append(f"    public const val {kt_const(t)}_{kt_const(p)}: Long = "
                     f"0xFF{sch[p][1:].upper()}")
        L.append("")
    L += ["}", ""]
    return "\n".join(L)


def android_colors_xml(data: dict, theme: str) -> str:
    cols = semantic_colours(data, theme)
    L = ['<?xml version="1.0" encoding="utf-8"?>',
         f"<!-- {GENERATED} -->", "<resources>"]
    for n in sorted(cols):
        L.append(f'    <color name="aninda_{n.replace("-", "_")}">'
                 f'#{cols[n][1:].upper()}</color>')
    L.append("</resources>")
    return "\n".join(L) + "\n"


def android_dimens_xml(data: dict) -> str:
    d = dimensions(data)
    L = ['<?xml version="1.0" encoding="utf-8"?>',
         f"<!-- {GENERATED} -->", "<resources>"]
    for k, v in sorted(d["space"].items(), key=lambda kv: int(kv[0])):
        L.append(f'    <dimen name="aninda_space_{k}">{int(v)}dp</dimen>')
    for k, v in d["radius"].items():
        L.append(f'    <dimen name="aninda_radius_{k}">{int(v)}dp</dimen>')
    for k, v in d["target"].items():
        L.append(f'    <dimen name="aninda_target_{k.replace("-", "_")}">'
                 f"{int(v)}dp</dimen>")
    for k, v in d["focus"].items():
        L.append(f'    <dimen name="aninda_focus_{k.replace("-", "_")}">'
                 f"{int(v)}dp</dimen>")
    for k, v in d["type"].items():
        if k.startswith("bangla"):
            continue
        L.append(f'    <dimen name="aninda_text_{k}">{v * 16:.2f}sp</dimen>')
    L.append("</resources>")
    return "\n".join(L) + "\n"


def android_dimens_bn_xml(data: dict) -> str:
    """values-bn. Android's own locale mechanism carries the Bangla ramp, so a
    Bangla layout gets the measured sizes without any code asking which script it
    is rendering."""
    d = dimensions(data)
    mult = {k[13:]: v for k, v in d["number"].items()
            if k.startswith("scale-bangla-")}
    band = {"caption": "caption", "body": "body", "lead": "heading",
            "h3": "heading", "h2": "title", "h1": "title", "display": "display"}
    floor = d["type"].get("bangla-min", 12)
    L = ['<?xml version="1.0" encoding="utf-8"?>',
         f"<!-- {GENERATED}",
         "     Bangla sizes, applied by Android's own locale mechanism. Each is the",
         "     Latin size times the measured multiplier for its band, and none falls",
         f"     below the {floor:g} sp floor. -->",
         "<resources>"]
    for k, v in d["type"].items():
        if k.startswith("bangla"):
            continue
        m = mult.get(band.get(k, "body"), 0.816)
        size = max(v * 16 * m, floor)
        L.append(f'    <dimen name="aninda_text_{k}">{size:.2f}sp</dimen>')
    L.append("</resources>")
    return "\n".join(L) + "\n"


# =========================================================================
# The gates that actually compile
# =========================================================================

def compile_swift(files: dict[Path, str]) -> str:
    """Build AND test the emitted package, in a temporary copy of it.

    `swiftc -typecheck` was the first gate here and it is the weaker one: it proves
    the grammar and that names resolve, and stops there. Laying the package out in
    a temporary directory instead means `swift build` compiles and links a real
    module and `swift test` runs the assertions in it — so what is proven is that
    the emitted code builds as a package, not merely that it parses.

    It runs on a COPY. Building in place would put a .build directory inside the
    generated tree, which the drift gate would then report as a file the build did
    not write.
    """
    if shutil.which("swift") is None:
        raise NotEquipped(
            "swift is not on PATH, so the emitted package cannot be built. On macOS "
            "it comes with Xcode or the command line tools. The files are still "
            "written; what is missing is the proof that they build.")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "pkg"
        n = 0
        for p, text in files.items():
            if not str(p).startswith(str(APPLE)):
                continue
            q = root / p.relative_to(APPLE)
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_text(text, encoding="utf-8")
            n += 1
        # The AUTHORED sources too, read off disk. The package is the generated
        # token layer PLUS the SwiftUI bridge and the components, and compiling
        # only half of it would prove only half of it — while reporting that the
        # package builds.
        for p in sorted(APPLE.rglob("*.swift")):
            if not is_authored(p):
                continue
            q = root / p.relative_to(APPLE)
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
            n += 1
        res = subprocess.run(["swift", "build", "--package-path", str(root)],
                             capture_output=True, text=True)
        if res.returncode != 0:
            raise BuildError("the emitted Swift package does not build:\n"
                             + (res.stderr or res.stdout)[:2000])
        test = subprocess.run(["swift", "test", "--package-path", str(root)],
                              capture_output=True, text=True)
        if test.returncode != 0:
            raise BuildError("the emitted Swift package builds but its tests fail:\n"
                             + (test.stderr or test.stdout)[:2000])
        # The count, WITHOUT the timing. `swift test` reports "Executed 3 tests,
        # with 0 failures (0 unexpected) in 0.001 (0.008) seconds", and those
        # seconds change on every run. LIMITS.md embeds this line, so leaving the
        # timing in made a generated file differ from itself between two builds —
        # the drift gate caught it, which is what it is for. No generated file in
        # this repository may carry a timestamp, and a duration is one.
        import re as _re
        passed = [_re.sub(r"\s+in\s+[\d.]+\s*\([\d.]+\)\s*seconds\.?$", "", ln.strip())
                  for ln in (test.stderr + test.stdout).splitlines()
                  if "Executed" in ln]
        ver = subprocess.run(["swift", "--version"], capture_output=True,
                             text=True).stdout.splitlines()[0].strip()
    detail = passed[-1].strip() if passed else "tests ran"
    return (f"{n} file Swift package builds and tests with {ver} — {detail}")


DESTINATIONS = (("macOS", "generic/platform=macOS"),
                ("iOS", "generic/platform=iOS"),
                ("watchOS", "generic/platform=watchOS"),
                ("tvOS", "generic/platform=tvOS"),
                ("visionOS", "generic/platform=visionOS"))


def compile_swift_platforms(root: Path) -> str:
    """Build for every platform the package declares, and NAME the ones it could not.

    `swift build` compiles for the host and nothing else. The package declares five
    platforms, and an API can be perfectly available on macOS and unavailable on
    watchOS — `onHover(perform:)` and `UIPasteboard` both are. A macOS-only build
    reports success over code that cannot compile for the platform the components
    are mostly FOR.

    A destination whose SDK is not installed is REPORTED, never skipped in silence.
    This machine has macOS alone; the macos-15 runner has all five. So a local pass
    means less than a CI pass here, which is the opposite of the arrangement
    everywhere else in this repository, and saying so is the only honest way to
    have it.
    """
    if shutil.which("xcodebuild") is None:
        return "xcodebuild is absent, so only the host platform was compiled"
    built, missing = [], []
    # Derived data goes OUTSIDE the tree. Building into it left a .dd directory
    # inside 15_native/apple that the sweep then deleted file by file, which is a
    # lot of churn to announce for a build product.
    dd = tempfile.mkdtemp(prefix="aninda-dd-")
    for name, dest in DESTINATIONS:
        res = subprocess.run(
            ["xcodebuild", "-scheme", "AnindaComponents", "-destination", dest,
             "-derivedDataPath", dd, "build"],
            cwd=root, capture_output=True, text=True)
        out = res.stdout + res.stderr
        if "BUILD SUCCEEDED" in out:
            built.append(name)
        elif "is not installed" in out or "Unable to find a destination" in out:
            missing.append(name)
        else:
            errs = [l.strip() for l in out.splitlines() if ": error:" in l][:6]
            raise BuildError(
                f"the components do not build for {name}:\n  "
                + "\n  ".join(errs or [out[-1200:]]))
    shutil.rmtree(dd, ignore_errors=True)
    note = f"components build for {', '.join(built)}"
    if missing:
        note += (f" — NOT compiled for {', '.join(missing)}, whose SDKs are not "
                 f"installed on this machine. Those platforms are compiled by the "
                 f"macos-15 job in CI and by nothing here")
    return note


def compile_kotlin(files: dict[Path, str]) -> str:
    """Two compiles, and they prove different things.

    FIRST the framework-free core, on its own. That one is the real claim: this
    Kotlin needs nothing but a Kotlin compiler, and it is what the token layer's
    strong gate is made about.

    SECOND the authored Compose sources, against the declared surface in
    compose/stubs. That proves the theme parses, that every name and arity is
    consistent, that the token constants exist and are the right type, and — since
    the stubbed ColorScheme takes all 48 parameters with no defaults — that not one
    Material role was forgotten. It does not prove they compile against androidx.
    """
    if shutil.which("kotlinc") is None:
        raise NotEquipped(
            "kotlinc is not on PATH, so the emitted Kotlin cannot be compiled. "
            "The files are still written; what is missing is the proof.")
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for p, text in files.items():
            # The framework-free core only. The stubs are a declared surface, not
            # part of the claim this pass makes, and counting them here would
            # inflate the figure the gate reports.
            if p.suffix != ".kt" or "compose/stubs" in str(p):
                continue
            q = Path(tmp) / p.name
            q.write_text(text, encoding="utf-8")
            paths.append(str(q))
        res = subprocess.run(
            ["kotlinc", *sorted(paths), "-d", str(Path(tmp) / "out"),
             "-nowarn"], capture_output=True, text=True)
        if res.returncode != 0:
            raise BuildError("the emitted Kotlin does not compile:\n"
                             + (res.stderr or res.stdout)[:2000])

        # Second compile: the authored Compose sources, plus the generated token
        # layer they import, plus the declared surface.
        stub_paths, compose_paths = [], []
        for p, text in files.items():
            if "compose/stubs" in str(p):
                q = Path(tmp) / "stub" / p.name
                q.parent.mkdir(parents=True, exist_ok=True)
                q.write_text(text, encoding="utf-8")
                stub_paths.append(str(q))
        for p in sorted(ANDROID.rglob("*.kt")):
            if is_authored(p):
                q = Path(tmp) / "authored" / p.name
                q.parent.mkdir(parents=True, exist_ok=True)
                q.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
                compose_paths.append(str(q))
        n_compose = 0
        if compose_paths:
            res2 = subprocess.run(
                ["kotlinc", *sorted(stub_paths), *sorted(paths),
                 *sorted(compose_paths), "-d", str(Path(tmp) / "out2"), "-nowarn"],
                capture_output=True, text=True)
            if res2.returncode != 0:
                raise BuildError(
                    "the authored Compose sources do not compile against the "
                    "declared surface:\n" + (res2.stderr or res2.stdout)[:2500])
            n_compose = len(compose_paths)
        ver = subprocess.run(["kotlinc", "-version"], capture_output=True,
                             text=True)
        # kotlinc reports its version on stderr with an "info:" prefix. Keeping it
        # would put a log level into a generated document.
        v = (ver.stderr or ver.stdout).strip().splitlines()[0]
        v = v.removeprefix("info:").strip()
    core = f"{len(paths)} framework-free Kotlin file(s) compile with {v}"
    if n_compose:
        core += (f"; {n_compose} authored Compose file(s) compile against the "
                 f"declared surface in compose/stubs, NOT against androidx")
    return core


def guard_values_match_source(files: dict[Path, str], data: dict) -> str:
    """Re-derive every colour from the emitted text and compare it to the tokens.

    The emitters could hold a typo and every compile gate would still pass, because
    a wrong hex is valid Swift. So the emitted files are read back and each colour
    is checked against the DTCG source it came from. This is the only gate here
    that would catch a value being wrong rather than merely being well formed.
    """
    import re
    checked = 0
    for t in THEMES:
        cols = semantic_colours(data, t)
        swift = files[APPLE / "Sources" / "AnindaTokens" / "Colours.swift"]
        # the palette literal for this theme
        block = swift.split(f"public static let {SWIFT_NAME[t]} = AnindaPalette(")[1]
        block = block.split("    )")[0]
        for name, hexv in cols.items():
            ident = swift_ident(name)
            m = re.search(rf'{ident}: AnindaColour\("([^"]+)", ([\d.]+), ([\d.]+), ([\d.]+)\)',
                          block)
            if not m:
                raise BuildError(f"Colours.swift has no entry for {t}/{name}")
            if m.group(1).upper() != hexv.upper():
                raise BuildError(f"Colours.swift {t}/{name} is {m.group(1)}, "
                                 f"the token says {hexv}")
            for i, comp in enumerate((1, 3, 5)):
                want = int(hexv[comp:comp + 2], 16) / 255
                got = float(m.group(i + 2))
                if abs(want - got) > 1e-6:
                    raise BuildError(
                        f"Colours.swift {t}/{name} component {i} is {got}, "
                        f"derived from the hex it should be {want:.6f}")
            checked += 1
        kt = files[ANDROID / "core/src/main/kotlin/studio/aninda/tokens/Tokens.kt"]
        for name, hexv in cols.items():
            want = f"{kt_const(t)}_{kt_const(name)}: Long = 0xFF{hexv[1:].upper()}"
            if want not in kt:
                raise BuildError(f"Tokens.kt is missing or wrong for {t}/{name} "
                                 f"(expected {want})")
            checked += 1
    return f"{checked} emitted colour values re-derived and matched to their tokens"


# The two trees the framework-free claim is actually about. Everything else in
# 15_native either imports a framework on purpose (the SwiftUI bridge, the
# components) or is not source at all (Package.swift).
FRAMEWORK_FREE = ("apple/Sources/AnindaTokens/",
                  "android/core/src/main/kotlin/")


def guard_no_framework_imports(files: dict[Path, str]) -> str:
    """The strong gate only means something if THOSE files stay importless.

    Scoped, and it has to be. The first version swept every file and tripped on
    Package.swift for the words "import SwiftUI" inside a COMMENT explaining which
    targets do import it. A guard that cannot tell a comment from an import, on a
    file that is not even in the target it protects, fails the build for being
    right about something it was not asked.
    """
    banned = ("import SwiftUI", "import UIKit", "import AppKit", "androidx.",
              "import android.")
    checked = 0
    for p, text in files.items():
        rel = p.relative_to(HERE).as_posix()
        if not any(rel.startswith(t) for t in FRAMEWORK_FREE):
            continue
        checked += 1
        for b in banned:
            if b in text:
                raise BuildError(
                    f"{p.relative_to(ROOT)} contains '{b}'. This is the layer "
                    f"compiled by swiftc and kotlinc alone, and a framework import "
                    f"turns a real gate into one that cannot run.")
    return (f"no framework import reached the {checked} files the framework-free "
            f"claim is made about")


def guard_authored_uses_tokens() -> str:
    """No authored component may carry a literal colour or a literal size.

    This is the native analogue of 08_components/build.py's guard_stylesheet, which
    refuses a hex in the hand-written CSS. The reason is the same and it is not
    style: a literal is a value nobody measured, sitting in a system whose entire
    claim is that every value was. One `Color(red: 0.13, ...)` in a button and the
    contrast figures this repository publishes stop describing what ships.

    What it looks for, and what it deliberately does not. A hex string, an RGB
    initialiser and a bare number used as a size all fail. A number used as a
    COUNT, a fraction, a line-height multiplier or an opacity does not — those are
    not sizes, and refusing them would push authors into inventing tokens for
    things that are not design decisions. The line between the two is drawn by the
    property being set, not by the number.
    """
    import re
    HEX = re.compile(r'#[0-9A-Fa-f]{3,8}\b')
    # A colour built from NUMBERS. Not from a token's own components — the whole
    # point of AnindaTokensUI is to be the one place that conversion happens, and
    # `Color(.sRGB, red: c.red, ...)` reading a measured value is the conversion
    # rather than a violation of it. The first version matched the construct and
    # failed the bridge for existing.
    RGB = re.compile(r'(?:\.(?:sRGB|displayP3)\s*,\s*)?red:\s*[\d.]+|'
                     r'Color\s*\(\s*0x|Color\s*\(\s*"#')
    # A number given to a property that positions or sizes something.
    SIZED = re.compile(
        r'\.(padding|frame|cornerRadius|lineWidth|offset|spacing|size|'
        r'strokeBorder|inset)\s*\([^)]*?(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])')
    ALLOW = {"0", "1", "0.0", "1.0", "2"}   # hairlines, zero, and a 2px focus ring
    problems: list[str] = []
    n = 0
    for root, exts in ((APPLE, (".swift",)), (ANDROID, (".kt",))):
        if not root.is_dir():
            continue
        for p in sorted(root.rglob("*")):
            if p.suffix not in exts or not is_authored(p):
                continue
            n += 1
            for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                code = line.split("//")[0]
                if HEX.search(code):
                    problems.append(f"{p.relative_to(ROOT)}:{i}: a literal colour")
                if RGB.search(code):
                    problems.append(f"{p.relative_to(ROOT)}:{i}: a colour built "
                                    f"from components rather than from a token")
                for m in SIZED.finditer(code):
                    if m.group(2) not in ALLOW:
                        problems.append(
                            f"{p.relative_to(ROOT)}:{i}: the literal size "
                            f"{m.group(2)} on .{m.group(1)} — use a token")
    if problems:
        raise BuildError(
            "authored source carries values nobody measured:\n  "
            + "\n  ".join(problems[:25])
            + (f"\n  ... and {len(problems) - 25} more" if len(problems) > 25 else ""))
    return f"{n} authored source file(s) carry no literal colour and no literal size"


def guard_component_contract() -> str:
    """One SwiftUI component per component card, and no orphans either way.

    08_components/_cards.json is the registry the whole system counts from: the
    README, the site and the Figma plan all read it. If the native library drifts
    from it — a card with no component, or a component with no card — then the
    README's "16 SwiftUI components" is a number that happens to be right rather
    than one that is kept right.

    Both directions, because the interesting failure is the quiet one: adding a
    card and forgetting the component leaves a documented thing that does not
    exist, and that is worse than the reverse.
    """
    reg = json.loads((ROOT / "08_components" / "_cards.json").read_text())
    cards = reg["cards"] if isinstance(reg, dict) and "cards" in reg else reg
    names = {c["name"] for c in cards if c["group"] == "Components"}

    # The registry's names are prose ("Checkbox and radio", "Empty state"); the
    # files are identifiers. One mapping, stated here rather than guessed by
    # normalising, because a guess would silently accept a rename.
    FILE_FOR = {
        "Button": "Button", "Input": "Input", "Select": "Select",
        "Checkbox and radio": "Checkbox", "Textarea": "Textarea",
        "Badge": "Badge", "Card": "Card", "Alert": "Alert", "Dialog": "Dialog",
        "Table": "Table", "Tabs": "Tabs", "Nav": "Nav",
        "Breadcrumb": "Breadcrumb", "Toast": "Toast",
        "Empty state": "EmptyState", "Code block": "CodeBlock",
    }
    unmapped = sorted(names - set(FILE_FOR))
    if unmapped:
        raise BuildError(
            f"these component cards have no entry in FILE_FOR: {unmapped}. A card "
            f"added to the registry needs a component or an explicit reason not to "
            f"have one.")

    src = APPLE / "Sources" / "AnindaComponents"
    on_disk = {p.stem for p in src.glob("*.swift")} if src.is_dir() else set()
    expected = {FILE_FOR[n] for n in names}
    missing = sorted(expected - on_disk)
    extra = sorted(on_disk - expected)
    if missing:
        raise BuildError(f"the registry lists components with no SwiftUI file: "
                         f"{missing}")
    if extra:
        raise BuildError(f"these SwiftUI files match no component card: {extra}. "
                         f"A component nothing documents is a component nobody "
                         f"finds.")
    return (f"{len(expected)} SwiftUI components, one for each component card in "
            f"08_components/_cards.json, with nothing orphaned either way")


def guard_deprecated_names(files: dict[Path, str]) -> str:
    """background, onBackground and surfaceVariant may appear ONLY in the Material
    adapter, and only as role names there. Criterion 21 forbids them as tokens."""
    # Scoped to the files that define TOKENS, which is what criterion 21 is about.
    #
    # The three names are REQUIRED wherever Material's constructor is spoken to:
    # the adapter that fills it, the declared surface that stubs it, and the theme
    # that calls it. Sweeping every file failed the build on the stub's own
    # parameter list — the guard catching the library for being the library.
    ADAPTERS = ("Material.kt", "material3.kt", "Theme.kt")
    checked = 0
    for p, text in files.items():
        rel = p.relative_to(HERE).as_posix()
        if p.name in ADAPTERS:
            continue
        if not any(rel.startswith(t) for t in FRAMEWORK_FREE):
            continue
        checked += 1
        for name in ("BACKGROUND", "ON_BACKGROUND", "SURFACE_VARIANT"):
            if name in text.upper().replace("-", "_"):
                raise BuildError(
                    f"{p.relative_to(ROOT)} carries the deprecated Material name "
                    f"'{name}'. Criterion 21 forbids it as a token name; it is "
                    f"permitted only where Material's constructor is spoken to.")
    return (f"no deprecated Material role name is used as a token name "
            f"in the {checked} files that define tokens")


PACKAGE_SWIFT = '''// swift-tools-version: 5.9
// {generated}
import PackageDescription

let package = Package(
    name: "AnindaTokens",
    platforms: [.iOS(.v17), .macOS(.v14), .watchOS(.v10), .tvOS(.v17), .visionOS(.v1)],
    products: [
        .library(name: "AnindaTokens", targets: ["AnindaTokens"]),
        .library(name: "AnindaTokensUI", targets: ["AnindaTokensUI"]),
        .library(name: "AnindaComponents", targets: ["AnindaComponents"]),
    ],
    targets: [
        // GENERATED, and framework-free on purpose. It imports nothing, so it
        // compiles anywhere Swift runs — which is what makes the gate on it real.
        .target(name: "AnindaTokens"),

        // AUTHORED from here down. These import SwiftUI, so they compile only
        // where Apple's SDKs are: on a Mac, and on the macos-15 runner. They are
        // kept in separate targets so the framework-free claim above stays true of
        // the target it is made about.
        .target(name: "AnindaTokensUI", dependencies: ["AnindaTokens"]),
        .target(name: "AnindaComponents",
                dependencies: ["AnindaTokens", "AnindaTokensUI"]),
        .target(name: "AnindaExamples",
                dependencies: ["AnindaTokens", "AnindaTokensUI",
                               "AnindaComponents"]),

        .testTarget(name: "AnindaTokensTests", dependencies: ["AnindaTokens"]),
    ]
)
'''

TESTS_SWIFT = '''// {generated}
import XCTest
@testable import AnindaTokens

/// These assert the SHAPE of the emitted surface, not the values.
///
/// Checking a value here would mean writing it down a second time, and a second
/// copy of a number is the thing this whole system is built to avoid. The values
/// are checked against the DTCG tokens by 15_native/build.py, which reads the
/// emitted file back and re-derives every component from the hex.
final class AnindaTokensTests: XCTestCase {{
    func testEveryThemeHasAPalette() {{
        for theme in AnindaTheme.allCases {{
            let p = AnindaColours.palette(for: theme)
            XCTAssertTrue(p.accent.hex.hasPrefix("#"))
            XCTAssertEqual(p.accent.hex.count, 7)
        }}
    }}

    func testComponentsAgreeWithTheirOwnHex() {{
        for theme in AnindaTheme.allCases {{
            let c = AnindaColours.palette(for: theme).accent
            let r = Int(c.hex.dropFirst(1).prefix(2), radix: 16)!
            XCTAssertEqual(c.red, Double(r) / 255.0, accuracy: 1e-6)
        }}
    }}

    func testBanglaFloorIsBelowItsSmallestStep() {{
        XCTAssertLessThanOrEqual(AnindaBangla.minimumPoints,
                                 AnindaType.caption * AnindaType.rootPoints)
    }}
}}
'''


def build_files(data: dict) -> dict[Path, str]:
    f: dict[Path, str] = {}
    f[APPLE / "Package.swift"] = PACKAGE_SWIFT.format(generated=GENERATED)
    f[APPLE / "Sources/AnindaTokens/Colours.swift"] = swift_colours(data)
    f[APPLE / "Sources/AnindaTokens/Dimensions.swift"] = swift_dimensions(data)
    f[APPLE / "Tests/AnindaTokensTests/AnindaTokensTests.swift"] = \
        TESTS_SWIFT.format(generated=GENERATED)

    kt = "core/src/main/kotlin/studio/aninda/tokens"
    f[ANDROID / kt / "Tokens.kt"] = kotlin_tokens(data)
    f[ANDROID / kt / "Material.kt"] = kotlin_material(data)
    f[ANDROID / "tokens/src/main/res/values/colors.xml"] = \
        android_colors_xml(data, "light")
    f[ANDROID / "tokens/src/main/res/values-night/colors.xml"] = \
        android_colors_xml(data, "dark")
    f[ANDROID / "tokens/src/main/res/values/dimens.xml"] = android_dimens_xml(data)
    f[ANDROID / "tokens/src/main/res/values-bn/dimens.xml"] = \
        android_dimens_bn_xml(data)
    for name, text in compose_stubs(data).items():
        f[ANDROID / "compose/stubs" / name] = text
    return f


def limits(notes: list[str]) -> str:
    return f"""<!-- {GENERATED} -->

# What the native layer proves, and what it does not

Written by `15_native/build.py`. This page exists because the gate on this layer is
unusually strong, and a strong gate invites a reader to assume cover it does not
give.

## What was actually run

{chr(10).join(f'- {n}' for n in notes)}

## What a compile proves

The Swift side is built and tested, not merely parsed: `swift build` compiles and
links a real module from a temporary copy of the package, and `swift test` runs the
assertions in it. The Kotlin side is compiled by `kotlinc`. Between them they prove
that names resolve, that types agree, and that the package assembles.

They prove nothing about layout, nothing about whether a target measures 44 pt on a
screen, nothing about focus order, and nothing about what VoiceOver or TalkBack
announce. A compile is not a rendering.

Measured separately, and the only gate here that could catch a value being *wrong*
rather than merely well formed: every emitted colour is read back out of the
generated text and re-derived from the DTCG token it came from. A typo in a hex is
valid Swift and would pass every compiler.

## What is deliberately not here

- **The framework-free claim is about the TOKEN layer, and only that.**
  `AnindaTokens` and the Kotlin core import nothing, which is what lets a compiler
  run on them anywhere. `AnindaTokensUI`, `AnindaComponents` and the Compose theme
  all import a framework on purpose and are kept in separate targets so the claim
  stays true of the target it is made about.
- **The components are compiled for macOS here and for nothing else.** The package
  declares five Apple platforms; this machine has the macOS SDK alone. An API can
  be available on macOS and unavailable on watchOS — `onHover(perform:)` and
  `UIPasteboard` both are, and both reached this package before anything caught
  them. The macos-15 job in CI is the only place the other four are compiled, which
  makes it the one gate here that CI proves and a local run cannot.
- **The Compose sources are compiled against a DECLARED SURFACE, not androidx.**
  The Android SDK is not installed. Compiling against `compose/stubs` proves the
  Kotlin parses, that every name and arity is consistent, that the token constants
  exist and are the right type, and — because the stubbed `ColorScheme` takes all
  48 parameters with no defaults — that not one Material role was forgotten. It
  does not prove the code compiles against androidx. A stub can differ from the
  library it imitates, and if it does, this gate passes and a real build fails.
- **No pattern is implemented.** `AnindaExamples` is a placeholder. The eight
  patterns are page compositions rather than components, and they are the part of
  the approved scope that is not done.
- **No rendered measurement.** Every contrast figure the native layer carries was
  computed from the same rounded 8-bit hexes the stylesheet uses, under the same
  worst-case sweep. No native pixel has been read. The browser harness measures
  thirty component cards; the native equivalent does not exist.
- **No Gradle project, and no `.xcodeproj`.** The Kotlin here compiles as plain
  JVM source. Assembling it into an Android library needs the SDK, and that is a
  toolchain this repository deliberately does not carry.

## Known divergences, recorded rather than reconciled

- **Apple's default body size is 17 pt; this system's is 16.** Changing the scale
  to suit one platform would change it for the web too, and the steps of a perfect
  fourth were chosen together. `AnindaType.rootPoints` is what a caller scales from.
- **macOS has no Dynamic Type.** Any Apple surface that needs scaling text has to
  use the iOS, iPadOS, tvOS, visionOS or watchOS route.
- **Android has no contrast qualifier.** `values/` and `values-night/` carry the
  two ordinary themes. The two high-contrast themes are available in the Kotlin
  constants and have no resource configuration to live in, so a View-based consumer
  gets the standard pair only.
- **Material's Bangla figure and this system's are not the same measurement.**
  Material calls Bangla a medium language-height script needing roughly 7 per cent
  taller line heights at the same nominal size. This system's Bangla leading is 1.6
  against Latin's 1.55, which is +3.2 per cent, and the Bangla is also set at
  x0.816 — so its absolute line box is smaller, not larger. Both are published and
  neither confirms the other.
"""


def ignored(paths: list[Path]) -> set[Path]:
    if not paths:
        return set()
    res = subprocess.run(["git", "check-ignore", "--stdin"], cwd=ROOT, text=True,
                         input="\n".join(str(p) for p in paths),
                         capture_output=True)
    # splitlines(), not split() — this repository's path contains a space, and
    # 12_packages/build.py shipped that exact bug.
    return {Path(line).resolve() for line in res.stdout.splitlines()}


def main(argv: list[str]) -> int:
    # --require names which compilers MUST run. It exists because the two live on
    # different machines: Swift ships on the macOS runners and Kotlin on the Ubuntu
    # ones, so neither CI job can prove both. Each job names what it is responsible
    # for and fails if that compiler is missing, rather than skipping quietly — a
    # gate that reports success because it could not run is worse than no gate.
    #
    # This machine has both, so scripts/verify-all.sh asks for both and a local
    # pass is therefore stronger than either CI job on its own.
    required = {"swift", "kotlin"}
    for i, a in enumerate(argv):
        if a == "--require" and i + 1 < len(argv):
            required = {x.strip() for x in argv[i + 1].split(",") if x.strip()}
    try:
        data = load()
        files = build_files(data)
        notes = [
            guard_no_framework_imports(files),
            guard_authored_uses_tokens(),
            guard_component_contract(),
            guard_deprecated_names(files),
            guard_values_match_source(files, data),
        ]
        for name, fn in (("swift", compile_swift), ("kotlin", compile_kotlin)):
            try:
                notes.append(fn(files))
                if name == "swift":
                    # Only after the package is known to build for the host. There
                    # is no sense asking about watchOS while macOS is broken.
                    notes.append(compile_swift_platforms(APPLE))
            except NotEquipped:
                if name in required:
                    raise
                notes.append(f"{name}: NOT COMPILED HERE — this run did not require "
                             f"it, and no claim is made that it builds")
    except NotEquipped as exc:
        print(f"NOT EQUIPPED: {exc}", file=sys.stderr)
        return 2
    except BuildError as exc:
        print(f"FAILED — nothing written:\n  {exc}", file=sys.stderr)
        return 1

    files[HERE / "LIMITS.md"] = limits(notes)

    if "--check" in argv:
        problems = []
        for p, text in sorted(files.items()):
            if not p.exists():
                problems.append(f"{p.relative_to(ROOT)} is missing")
            elif p.read_text(encoding="utf-8") != text:
                problems.append(f"{p.relative_to(ROOT)} differs from the build")
        on_disk = [p for root in (APPLE, ANDROID) if root.is_dir()
                   for p in root.rglob("*") if p.is_file()]
        skip = ignored(on_disk)
        for p in sorted(on_disk):
            if p.resolve() in skip or is_authored(p) or p in files:
                continue
            problems.append(f"{p.relative_to(ROOT)} is in the tree and is not "
                            f"generated by this build")
        if problems:
            print("--check: the native layer differs from the build:", file=sys.stderr)
            for x in problems:
                print(f"  {x}", file=sys.stderr)
            return 1
        for n in notes:
            print(f"  ok    {n}")
        print(f"\n--check: {len(files)} files match the build. Nothing written.")
        return 0

    on_disk = [p for root in (APPLE, ANDROID) if root.is_dir()
               for p in root.rglob("*") if p.is_file()]
    skip = ignored(on_disk)
    removed = []
    for p in sorted(on_disk):
        if p.resolve() in skip or is_authored(p) or p in files:
            continue
        p.unlink()
        removed.append(p.relative_to(ROOT))
    for p, text in sorted(files.items()):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    for n in notes:
        print(f"  ok    {n}")
    print()
    for r in removed:
        print(f"  removed {r}")
    print(f"  wrote 15_native/apple    "
          f"{sum(1 for p in files if str(p).startswith(str(APPLE)))} files")
    print(f"  wrote 15_native/android  "
          f"{sum(1 for p in files if str(p).startswith(str(ANDROID)))} files")
    print(f"  wrote 15_native/LIMITS.md")
    print("\nThis layer imports no framework, which is what lets a compiler run on "
          "it. What that compile does NOT prove is in LIMITS.md.")
    return 0


# =========================================================================
# The declared Compose surface, and the stub compiled against it
# =========================================================================

def compose_stubs(data: dict) -> dict[str, str]:
    """Enough of Compose, declared, for kotlinc to compile the authored theme.

    WHY THIS EXISTS, AND WHAT IT IS NOT
    ===================================
    The Android SDK is not installed here and installing it is a change to
    somebody's machine. Without it, `kotlinc` cannot resolve `androidx`, so the
    Compose sources would ship with NO compiler having looked at them — weaker than
    the Swift side by a long way, and a weakness that would sit inside a document
    claiming everything is measured.

    Compiling against a declared surface is the strongest thing available short of
    the real SDK. It proves the Kotlin parses, that every name and arity the
    authored code uses is consistent, that the token constants it references exist
    and are the right type, and — because ColorScheme's stub takes all 48
    parameters with no defaults — that not one Material role has been forgotten.

    It does NOT prove the code compiles against androidx. A stub can differ from
    the library it imitates, and if it does, this gate passes and the real build
    fails. 15_native/LIMITS.md says that in those words rather than these.

    The ColorScheme parameter list is not typed here: it is read from
    15_native/_proof/material3.roles.json, which took it from ColorScheme.kt on
    androidx-main. So the stub cannot drift from the list the derivation used, and
    a Material release that adds a role changes both together or neither.
    """
    params = data["material3"]["constructor"]["order"]
    args = ",\n".join(f"    public val {p}: Color" for p in params)
    banner = (f"// {GENERATED}\n//\n// A DECLARED SURFACE, not androidx. See "
              f"compose_stubs() in 15_native/build.py\n// for what compiling "
              f"against this does and does not prove.\n"
              f'@file:Suppress("unused", "UNUSED_PARAMETER")\n\n')

    files: dict[str, str] = {}

    files["runtime.kt"] = banner + """package androidx.compose.runtime

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
"""

    files["graphics.kt"] = banner + """package androidx.compose.ui.graphics

public class Color(public val value: Long) {
    public companion object { public val Transparent: Color = Color(0L) }
}
"""

    files["unit.kt"] = banner + """package androidx.compose.ui.unit

public class Dp(public val value: Float)
public val Int.dp: Dp get() = Dp(this.toFloat())
public val Float.dp: Dp get() = Dp(this)

public class TextUnit(public val value: Float)
public val Float.sp: TextUnit get() = TextUnit(this)
public val Int.sp: TextUnit get() = TextUnit(this.toFloat())
"""

    files["font.kt"] = banner + """package androidx.compose.ui.text.font

public class FontFamily {
    public companion object { public val Default: FontFamily = FontFamily() }
}

public class FontWeight(public val weight: Int) {
    public companion object {
        public val Normal: FontWeight = FontWeight(400)
        public val Medium: FontWeight = FontWeight(500)
        public val SemiBold: FontWeight = FontWeight(600)
        public val Bold: FontWeight = FontWeight(700)
    }
}
"""

    files["text.kt"] = banner + """package androidx.compose.ui.text

import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.TextUnit

public class TextStyle(
    public val fontFamily: FontFamily? = null,
    public val fontWeight: FontWeight? = null,
    public val fontSize: TextUnit? = null,
    public val lineHeight: TextUnit? = null,
)
"""

    files["shape.kt"] = banner + """package androidx.compose.foundation.shape

import androidx.compose.ui.unit.Dp

public class RoundedCornerShape(public val radius: Dp)
"""

    files["foundation.kt"] = banner + """package androidx.compose.foundation

import androidx.compose.runtime.Composable

@Composable
public fun isSystemInDarkTheme(): Boolean = false
"""

    files["material3.kt"] = banner + """package androidx.compose.material3

import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.foundation.shape.RoundedCornerShape

// Every parameter, and NO defaults. That is the completeness gate: a role left out
// is a compile error rather than Material's baseline purple shipped in silence.
// The list is read from material3.roles.json, which took it from ColorScheme.kt on
// androidx-main, so the stub cannot drift from the list the derivation used.
public class ColorScheme(
""" + args + """,
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
"""
    return files

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
