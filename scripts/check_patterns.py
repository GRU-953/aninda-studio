#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
THE EIGHT PATTERNS EXIST ON THREE PLATFORMS, OR THE BUILD SAYS WHICH ONE IS SHORT
=================================================================================
A pattern is a page composition, and unlike a component it has no public API to
compare. So the only thing that can be checked mechanically is EXISTENCE — and
existence is exactly what goes wrong: a screen gets written for the platform
somebody was working on and forgotten on the other two, and nothing notices,
because each platform's own build is perfectly happy with what it has.

WHY THIS LIVES IN scripts/ AND NOT IN A BUILD
---------------------------------------------
It spans three folders and belongs to none of them. Putting it in
08_components/build.py would make the registry's PRODUCER assert facts about
15_native. Putting it only in 15_native/build.py would fail the native build over
a missing web card, which is not the native layer's business.

15_native/build.py does carry a narrower guard — guard_pattern_contract() — which
asserts that the two NATIVE platforms agree with each other and with the
registry's count. That one needs no name table, because set equality does not.
This file owns the name table, and therefore owns the web leg.

WHY THE TABLE IS STATED TWICE OVER
----------------------------------
_cards.json carries a card's prose NAME and its path, and nothing else. Two
different conventions have to be derived from that name — kebab-case for the web
file and UpperCamel for both native ones — and deriving either mechanically is
precisely the guess that 15_native/build.py's FILE_FOR refuses to make, "because a
guess would silently accept a rename". So both stems are stated, per pattern, and
a ninth card with no entry is a failure rather than a silent omission.

RUN
---
    cd <the repository folder>
    ./.venv/bin/python scripts/check_patterns.py

Exit 0 if every pattern exists on all three platforms. Exit 1 naming which
platform is short, for each pattern that is short on one.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "08_components" / "_cards.json"
WEB = ROOT / "08_components" / "cards" / "patterns"
APPLE = ROOT / "15_native" / "apple" / "Sources" / "AnindaExamples"
ANDROID = (ROOT / "15_native" / "android" / "patterns" / "src" / "main" / "kotlin"
           / "studio" / "aninda" / "patterns")

# A card's prose name, its web slug, and its native stem. Stated, not normalised.
PATTERN_FILE_FOR = {
    "Sign in":              ("sign-in",              "SignIn"),
    "Settings":             ("settings",             "Settings"),
    "Dashboard":            ("dashboard",            "Dashboard"),
    "Docs page":            ("docs-page",            "DocsPage"),
    "Landing":              ("landing",              "Landing"),
    "Pricing":              ("pricing",              "Pricing"),
    "Not found":            ("not-found",            "NotFound"),
    "Form with validation": ("form-with-validation", "FormWithValidation"),
}

# Not a pattern: the module's front door on both native platforms. Named rather
# than matched by prefix, so a file called PatternsHelper does not slip through.
NOT_A_PATTERN = {"Patterns"}


def main() -> int:
    if not CARDS.exists():
        print(f"FAILED: {CARDS.relative_to(ROOT)} is missing", file=sys.stderr)
        return 1
    reg = json.loads(CARDS.read_text(encoding="utf-8"))
    cards = reg["cards"] if isinstance(reg, dict) and "cards" in reg else reg
    declared = [c["name"] for c in cards if c["group"] == "Patterns"]

    problems: list[str] = []

    # A card this file has never heard of. Checked FIRST, because every assertion
    # below is keyed on the table and would otherwise skip the new card in silence.
    unmapped = [n for n in declared if n not in PATTERN_FILE_FOR]
    if unmapped:
        problems.append(
            "08_components/_cards.json declares pattern(s) this check has no entry "
            "for: " + ", ".join(unmapped)
            + " — add them to PATTERN_FILE_FOR with both stems")
    orphaned = [n for n in PATTERN_FILE_FOR if n not in declared]
    if orphaned:
        problems.append(
            "PATTERN_FILE_FOR names pattern(s) the registry does not: "
            + ", ".join(orphaned))

    counts = reg.get("counts", {}) if isinstance(reg, dict) else {}
    if counts.get("Patterns") != len(PATTERN_FILE_FOR):
        problems.append(
            f"the registry counts {counts.get('Patterns')} patterns and this check "
            f"holds {len(PATTERN_FILE_FOR)}")

    # The three legs. Each reports which PLATFORM is short, by name, because
    # "Pricing is missing" sends somebody to look in three places.
    for name in declared:
        if name not in PATTERN_FILE_FOR:
            continue
        slug, stem = PATTERN_FILE_FOR[name]
        where = {
            "the web": WEB / f"{slug}.html",
            "Apple": APPLE / f"{stem}.swift",
            "Android": ANDROID / f"{stem}.kt",
        }
        absent = [k for k, p in where.items() if not p.exists()]
        if absent:
            present = [k for k in where if k not in absent]
            problems.append(
                f"{name}: on {' and '.join(present) or 'no platform'} and not on "
                f"{' or '.join(absent)}")

    # And the other direction, per platform: a file with no card.
    stems = {stem for _, stem in PATTERN_FILE_FOR.values()}
    slugs = {slug for slug, _ in PATTERN_FILE_FOR.values()}
    for label, folder, suffix, known in (
        ("the web", WEB, ".html", slugs),
        ("Apple", APPLE, ".swift", stems | NOT_A_PATTERN),
        ("Android", ANDROID, ".kt", stems | NOT_A_PATTERN),
    ):
        if not folder.is_dir():
            problems.append(f"{label}: {folder.relative_to(ROOT)} does not exist")
            continue
        extra = sorted(p.stem for p in folder.glob(f"*{suffix}")
                       if p.stem not in known)
        if extra:
            problems.append(
                f"{label} carries file(s) no pattern card names: "
                + ", ".join(extra))

    if problems:
        print("FAILED — the eight patterns do not line up:", file=sys.stderr)
        for x in problems:
            print(f"  {x}", file=sys.stderr)
        return 1

    print(f"  ok    {len(declared)} patterns, each on the web, on Apple and on "
          f"Android, with nothing orphaned on any of the three")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
