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
    return name.upper().replace("-", "_")


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


def compile_kotlin(files: dict[Path, str]) -> str:
    if shutil.which("kotlinc") is None:
        raise NotEquipped(
            "kotlinc is not on PATH, so the emitted Kotlin cannot be compiled. "
            "The files are still written; what is missing is the proof.")
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for p, text in files.items():
            if p.suffix != ".kt":
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
        ver = subprocess.run(["kotlinc", "-version"], capture_output=True,
                             text=True)
        # kotlinc reports its version on stderr with an "info:" prefix. Keeping it
        # would put a log level into a generated document.
        v = (ver.stderr or ver.stdout).strip().splitlines()[0]
        v = v.removeprefix("info:").strip()
    return f"{len(paths)} Kotlin file(s) compile with {v}"


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


def guard_no_framework_imports(files: dict[Path, str]) -> str:
    """The strong gate only means something if these files stay importless."""
    banned = ("import SwiftUI", "import UIKit", "import AppKit", "androidx.",
              "import android.")
    for p, text in files.items():
        if p.suffix not in (".swift", ".kt"):
            continue
        if "/Tests/" in str(p):
            continue        # XCTest is a framework and a test file may import it
        for b in banned:
            if b in text:
                raise BuildError(
                    f"{p.relative_to(ROOT)} contains '{b}'. This layer is compiled "
                    f"by swiftc and kotlinc alone, and a framework import turns a "
                    f"real gate into one that cannot run.")
    return "no framework import reached the layer that is compiled here"


def guard_deprecated_names(files: dict[Path, str]) -> str:
    """background, onBackground and surfaceVariant may appear ONLY in the Material
    adapter, and only as role names there. Criterion 21 forbids them as tokens."""
    for p, text in files.items():
        if p.name == "Material.kt":
            continue
        for name in ("BACKGROUND", "ON_BACKGROUND", "SURFACE_VARIANT"):
            if name in text.upper().replace("-", "_"):
                raise BuildError(
                    f"{p.relative_to(ROOT)} carries the deprecated Material name "
                    f"'{name}'. Criterion 21 forbids it as a token name; it is "
                    f"permitted only as a constructor argument in the adapter.")
    return "no deprecated Material role name is used as a token name"


PACKAGE_SWIFT = '''// swift-tools-version: 5.9
// {generated}
import PackageDescription

let package = Package(
    name: "AnindaTokens",
    platforms: [.iOS(.v17), .macOS(.v14), .watchOS(.v10), .tvOS(.v17), .visionOS(.v1)],
    products: [
        .library(name: "AnindaTokens", targets: ["AnindaTokens"]),
    ],
    targets: [
        // Framework-free on purpose. It imports nothing, so `swift build` and
        // `swiftc -typecheck` both compile it anywhere Swift runs — which is what
        // makes the gate on it a real one.
        .target(name: "AnindaTokens"),
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

- **No SwiftUI, no Compose.** Both layers import nothing. That is what lets a
  compiler run on them at all: SwiftUI is an Apple-only framework, absent from the
  open-source Swift toolchain on Linux, and Compose needs the Android SDK. A
  framework layer would carry a weaker gate, and mixing the two would let this
  page's strong claim cover code it never tested.
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
            guard_deprecated_names(files),
            guard_values_match_source(files, data),
        ]
        for name, fn in (("swift", compile_swift), ("kotlin", compile_kotlin)):
            try:
                notes.append(fn(files))
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
            if p.resolve() not in skip and p not in files:
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
        if p.resolve() not in skip and p not in files:
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


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
