#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
Because a licence claim was corrected twice and was still wrong both times.

IBM Plex Mono's Reserved Font Name is the single word "Plex". The exact string is
on the first line of the licence file this repository ships beside the font. That
single word is why the whole IBM Plex superfamily is covered by it.

This repository asserted "IBM Plex" instead. The first correction reached NOTICE,
the guidebook and the token descriptions. The second reached the docstrings. Both
times the fix was declared complete, and both times a review found more: the
second round found the wrong string still in 38 files — 30 shipped component
cards, both public site pages, the Figma plugin's variable description, and the
two NOTICE files a redistributor of the Claude Code plugin is REQUIRED to carry.
One generator held the fix and the error at once, thirty lines apart.

The error is in the permissive direction, which is what makes it matter. A reader
who trusts it would conclude that only the compound "IBM Plex" is reserved, and
that renaming a subset to "Plex Sans" or "Plex Mono Custom" is available. It is
not, and they would breach OFL 1.1 clause 3 believing they had complied.

Two hand-corrections were not enough because nothing checked. This does, over the
whole repository, so the claim cannot be wrong in one place while right in another.

RUN
---
    ./.venv/bin/python scripts/check_licence_claims.py
    ./.venv/bin/python scripts/check_licence_claims.py --expect-failure   # self-test
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".venv", "node_modules", "browsers", ".claude", "candidates",
             "specimens", "_data", "__pycache__"}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".html", ".json", ".css", ".ts", ".js",
                 ".mjs", ".yml", ".yaml", "", ".svg"}

# The exact string, read from the licence rather than typed here, so this checker
# cannot itself drift from the thing it is checking.
OFL = ROOT / "06_type" / "candidates" / "mono" / "ibmplexmono" / "OFL.txt"


def reserved_name() -> str:
    if not OFL.exists():
        raise SystemExit(f"could not run: {OFL} is missing, so the correct "
                         f"Reserved Font Name cannot be read from source")
    first = OFL.read_text(encoding="utf-8", errors="replace").splitlines()[0]
    m = re.search(r'Reserved Font Name\s*"([^"]+)"', first)
    if not m:
        raise SystemExit(f"could not run: no Reserved Font Name on line 1 of {OFL.name}")
    return m.group(1)


def main() -> int:
    expect_failure = "--expect-failure" in sys.argv
    correct = reserved_name()

    # Any claim that the reserved name is something other than the real string.
    # Matches the plain form, the HTML-entity form the cards use, and the
    # apostrophe form, in either order.
    # Only a NAMED claim counts. The first version matched the bare phrase
    # followed by any quote, so it flagged two table column headers reading
    # `"Reserved Font Name", "Subset"` and one sentence saying "IBM Plex carries a
    # Reserved Font Name" — which is true and says nothing about what the name is.
    # A guard that cries wolf gets switched off, and then it protects nothing.
    #
    # So the quoted part must look like a font name: letters, digits, spaces and
    # hyphens only, one to twenty-four characters, no punctuation.
    NAME = r"[A-Za-z0-9][A-Za-z0-9 \-]{0,23}"
    wrong = re.compile(
        rf"(?:Reserved Font Name\s+(?:is\s+)?[\"'“]({NAME})[\"'”])"
        rf"|(?:Reserved Font Name\s+&ldquo;({NAME})&rdquo;)"
        rf"|(?:[\"'“]({NAME})[\"'”]\s+is a Reserved Font Name)"
        rf"|(?:&ldquo;({NAME})&rdquo;\s+is a Reserved Font Name)",
        re.IGNORECASE,
    )

    # The PolyForm URL's trailing-slash form returns 404. This lived in CI as a
    # grep with --include='*.md' --include='*.json' --include='*.py', which could
    # see 10 of the 18 places the URL appears and missed the 8 that matter most:
    # all six NOTICE files, which have no extension and are what a redistributor
    # is obliged to carry, plus both guidebook builds. Proved by injecting the
    # trailing slash into 13_plugins/claude-code/NOTICE — the grep found nothing
    # and the step passed. It is folded in here because this script already walks
    # the whole tree with a suffix list that includes extensionless files, and one
    # sweep cannot disagree with itself the way two greps can.
    POLYFORM = re.compile(r"polyformproject\.org/licenses/noncommercial/1\.0\.0/")

    offenders: list[tuple[str, int, str]] = []
    slashes: list[tuple[str, int]] = []
    scanned = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        if path.name == Path(__file__).name:
            continue          # this file must be able to name the wrong string
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scanned += 1
        for n, line in enumerate(text.splitlines(), 1):
            if POLYFORM.search(line):
                slashes.append((str(path.relative_to(ROOT)), n))
            for m in wrong.finditer(line):
                named = next((g for g in m.groups() if g), "").strip()
                if named and named.casefold() != correct.casefold():
                    offenders.append((str(path.relative_to(ROOT)), n, m.group(0).strip()))

    print(f"  scanned {scanned} text files")
    print(f"  the Reserved Font Name, read from {OFL.name}: \"{correct}\"")

    if slashes:
        print(f"\n  {len(slashes)} PolyForm URL(s) with a trailing slash, which 404s:",
              file=sys.stderr)
        for f, n in slashes[:8]:
            print(f"    {f}:{n}", file=sys.stderr)
        return 0 if expect_failure else 1
    print(f"  no PolyForm URL carries a trailing slash")

    if offenders:
        by_file: dict[str, int] = {}
        for f, _, _ in offenders:
            by_file[f] = by_file.get(f, 0) + 1
        print(f"\n  {len(offenders)} wrong claim(s) in {len(by_file)} file(s):",
              file=sys.stderr)
        for f in sorted(by_file)[:12]:
            print(f"    {f} ({by_file[f]})", file=sys.stderr)
        if len(by_file) > 12:
            print(f"    … and {len(by_file) - 12} more", file=sys.stderr)
        print(f'\n  Every one must name exactly "{correct}". The error is in the '
              f'permissive direction: a reader who trusts it would think only the '
              f'compound is reserved and that "Plex Sans" is available.',
              file=sys.stderr)
        return 0 if expect_failure else 1

    if expect_failure:
        print("\n  --expect-failure: found nothing to fail on. Either the repository "
              "is clean or this checker no longer works.", file=sys.stderr)
        return 1
    print(f'\n  every licence claim names "{correct}" correctly.')
    return 0


if __name__ == "__main__":
    sys.exit(main())
