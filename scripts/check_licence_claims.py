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

TWO OTHER CLAIMS RIDE ALONG, FOR THE SAME REASON
    * The PolyForm licence URL, whose trailing-slash form 404s.
    * The two package names. Both packages are `aninda-studio-tokens`, and the
      guidebook's "How to write it" table and the plugin's naming reference both
      gave them as `aninda-studio`, which is the repository's name — so a reader
      following either typed an install command for a package that does not
      exist under any state of publication. Those two surfaces are hand-written
      and cannot read package.json, so the sweep reads it for them.

    All three are whole-tree claims about a string held somewhere else in the
    tree. One sweep cannot disagree with itself the way three greps can.

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
# The repository has around 260 text files. A run that sees a small fraction of
# that has been filtered by accident, not by design.
MIN_FILES = 120

OFL = ROOT / "06_type" / "candidates" / "mono" / "ibmplexmono" / "OFL.txt"


def package_names() -> set[str]:
    """The two package names, read from the packages, never typed here."""
    names = set()
    npm = ROOT / "12_packages" / "npm" / "package.json"
    pyp = ROOT / "12_packages" / "python" / "pyproject.toml"
    for src, pat in ((npm, r'"name"\s*:\s*"([^"]+)"'),
                     (pyp, r'^name\s*=\s*"([^"]+)"')):
        if not src.exists():
            raise SystemExit(f"could not run: {src} is missing, so the real "
                             f"package name cannot be read from source")
        m = re.search(pat, src.read_text(encoding="utf-8"), re.M)
        if not m:
            raise SystemExit(f"could not run: no package name found in {src.name}")
        names.add(m.group(1))
    return names


def reserved_name() -> str:
    """The Reserved Font Name of the face this system actually ships."""
    if not OFL.exists():
        raise SystemExit(f"could not run: {OFL} is missing, so the correct "
                         f"Reserved Font Name cannot be read from source")
    first = OFL.read_text(encoding="utf-8", errors="replace").splitlines()[0]
    m = re.search(r'Reserved Font Name\s*"([^"]+)"', first)
    if not m:
        raise SystemExit(f"could not run: no Reserved Font Name on line 1 of {OFL.name}")
    return m.group(1)


def declared_names() -> set[str]:
    """Every Reserved Font Name declared by any licence in this repository.

    The widened claim pattern below now recognises the markdown-backtick form,
    which this repository's own prose uses. That prose also discusses the faces
    that were CONSIDERED and rejected, and some of them carry a Reserved Font
    Name of their own — 06_type/SHORTLIST.md correctly says Source Code Pro
    carries `Source`. Comparing every claim against the one shipped name would
    fail those true sentences, and a guard that cries wolf gets switched off.

    So the test is membership: a claim must name a Reserved Font Name that some
    licence in this tree actually declares. "IBM Plex" — the string this project
    got wrong three times — is declared by nothing, so it is still caught, and
    the check has become wider in both directions at once rather than trading
    one kind of blindness for another.
    """
    names: set[str] = set()
    for path in ROOT.rglob("*OFL*.txt"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts
               if part != "candidates"):
            continue
        try:
            first = path.read_text(encoding="utf-8", errors="replace").splitlines()[0]
        except (OSError, IndexError):
            continue
        for m in re.finditer(r"Reserved Font Name\s*[\"\'\u2018\u201c]?"
                             r"([A-Za-z0-9][A-Za-z0-9 \-]{0,23}?)"
                             r"[\"\'\u2019\u201d]?\s*(?:\.|$)", first):
            names.add(m.group(1).strip())
    return names


def main() -> int:
    expect_failure = "--expect-failure" in sys.argv
    correct = reserved_name()
    declared = {n.casefold() for n in declared_names()}
    if correct.casefold() not in declared:
        raise SystemExit(f"could not run: the shipped Reserved Font Name "
                         f"{correct!r} is not among the names any licence in this "
                         f"tree declares ({sorted(declared)}) — the two readers "
                         f"disagree, so neither can be trusted")

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
    # The quote may be a straight or curly double, a straight or curly single, a
    # markdown BACKTICK, or the HTML entity form. The backtick form was missing
    # and this repository's own prose uses it four times for this exact claim, so
    # the guard built to end a claim being right in one place and wrong in another
    # could not read four of the places. `RFN` is recognised too, because the
    # glossary defines the abbreviation and prose then uses it.
    Q1 = r"[\"'`\u2018\u201c]"
    Q2 = r"[\"'`\u2019\u201d]"
    RFN = r"(?:Reserved Font Name|RFN)"
    wrong = re.compile(
        rf"(?:{RFN}\s+(?:is\s+)?(?:the single word\s+)?{Q1}({NAME}){Q2})"
        rf"|(?:{RFN}\s+&ldquo;({NAME})&rdquo;)"
        rf"|(?:{Q1}({NAME}){Q2}\s+is a(?:n)? {RFN})"
        rf"|(?:&ldquo;({NAME})&rdquo;\s+is a(?:n)? {RFN})",
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

    # Two narrow shapes only, so this cannot cry wolf over prose that mentions the
    # repository, the plugin or the command — all three of which are correctly
    # named `aninda-studio` and appear far more often than the packages do.
    #   1. an install command:            npm install X   /   pip install X
    #   2. a table row that says which:   | npm package | … | `X` |
    # Anything else is left alone.
    packages = package_names()
    INSTALL = re.compile(r"\b(?:npm install|pip install)\s+(?:-e\s+)?"
                         r"([A-Za-z0-9@][A-Za-z0-9@/._-]*)")
    PKG_ROW = re.compile(r"^\|[^|]*\b(?:npm|PyPI|pypi)\s+package\b[^|]*\|.*?"
                         r"`([^`]+)`", re.IGNORECASE)

    offenders: list[tuple[str, int, str]] = []
    slashes: list[tuple[str, int]] = []
    misnamed: list[tuple[str, int, str]] = []
    scanned = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        # RELATIVE to the repository, not absolute. SKIP_DIRS holds repo-relative
        # directory names — `browsers` is 00_sandbox/browsers, and candidates,
        # specimens and _data exist only under 06_type. Matching them against the
        # absolute path meant any checkout whose own path contained one of those
        # words skipped EVERY file: in .claude/worktrees/<id>, which is exactly the
        # layout used to review this project, the sweep scanned 0 files and printed
        # an affirmative pass on all three licence claims.
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
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
            for m in (INSTALL.search(line), PKG_ROW.search(line)):
                if m and m.group(1) not in packages:
                    # A local path or a flag is not a registry name.
                    if m.group(1).startswith((".", "/", "-")):
                        continue
                    misnamed.append((str(path.relative_to(ROOT)), n,
                                     m.group(0).strip()))
            for m in wrong.finditer(line):
                named = next((g for g in m.groups() if g), "").strip()
                if named and named.casefold() not in declared:
                    offenders.append((str(path.relative_to(ROOT)), n, m.group(0).strip()))

    # A sweep that scanned nothing is not a sweep that found nothing. This is the
    # same silent-green-pass shape as the four CI steps that read
    # `test ! -f X || python X`: the check did not run, and said so in a line
    # nobody reads, while its exit code said everything was fine.
    if scanned < MIN_FILES:
        print(f"  scanned only {scanned} text files, expected at least {MIN_FILES}",
              file=sys.stderr)
        print("  This check did not really run, so its pass means nothing. Most likely "
              "the skip list matched a component of the checkout path itself.",
              file=sys.stderr)
        return 1
    print(f"  scanned {scanned} text files")
    print(f"  the Reserved Font Name, read from {OFL.name}: \"{correct}\"")

    if slashes:
        print(f"\n  {len(slashes)} PolyForm URL(s) with a trailing slash, which 404s:",
              file=sys.stderr)
        for f, n in slashes[:8]:
            print(f"    {f}:{n}", file=sys.stderr)
        return 0 if expect_failure else 1
    print(f"  no PolyForm URL carries a trailing slash")

    if misnamed:
        print(f"\n  {len(misnamed)} place(s) name a package that is not "
              f"{' or '.join(sorted(packages))}:", file=sys.stderr)
        for f, n, s in misnamed[:12]:
            print(f"    {f}:{n}  {s}", file=sys.stderr)
        print("\n  Both packages are named in 12_packages/npm/package.json and "
              "12_packages/python/pyproject.toml. An install command or a package "
              "row naming anything else sends a reader to a package that does not "
              "exist.", file=sys.stderr)
        return 0 if expect_failure else 1
    print(f"  every install command and package row names "
          f"{' or '.join(sorted(packages))}")

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
        print(f'\n  A Reserved Font Name claim must name one that a licence in '
              f'this tree actually declares: {sorted(declared_names())}. The face '
              f'this system ships reserves "{correct}" — the single word — and the '
              f'error this guard exists for is in the permissive direction: a '
              f'reader who trusts "IBM Plex" would think only the compound is '
              f'reserved and that "Plex Sans" is available.',
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
