#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
This project's rule is that nothing generated may carry an absolute path: it is
drift a diff cannot catch, and it makes committed output different on every
machine. The rule was written down and never enforced, so on 25 August 2026 the
tree held 86 of them — 70 in two generated data files, 5 telling readers to `cd`
into one person's home directory, and 16 in run-instructions inside generators.
One more had already been found by hand in the guidebook a few hours earlier.

A rule nobody measures is a wish. This measures it.

WHAT IS EXEMPT, AND WHY
-----------------------
The evidence records in 01_research are quotations: they say what command someone
ran and what it printed. Rewriting a quoted command to look tidier would falsify
the record, which is worse than the untidiness. They are exempt BY NAME below, so
the exemption is visible rather than a hole.

RUN
---
    ./.venv/bin/python scripts/check_no_absolute_paths.py

Exit 0 clean · 1 a real hit · 2 could not run.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Quotations of commands as they were actually run. Changing these would falsify a
# record. Everything else in the tree is held to the rule.
EXEMPT = {
    "01_research/_data/findings.json",
    "01_research/_data/benchmark-verdicts.json",
    "01_research/OPEN-FINDINGS.md",
}

# Any /Users/<name>/ or /home/<name>/ path. Not just this Mac's — a gate that only
# knows one machine's home directory passes on everyone else's.
ABSOLUTE = re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/")

# Binary and vendored things a text sweep should not read.
SKIP_SUFFIX = {".png", ".ico", ".pdf", ".woff2", ".ttf", ".otf", ".skill", ".zip"}
SKIP_PREFIX = ("06_type/candidates/", "00_sandbox/node_modules/")


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                         capture_output=True, text=True)
    if out.returncode != 0:
        return []
    return [f for f in out.stdout.split("\0") if f]


def main() -> int:
    files = tracked()
    if not files:
        print("could not run: git ls-files returned nothing, so this check did not "
              "really run.", file=sys.stderr)
        return 2

    looked_at = 0
    hits: list[tuple[str, int, str]] = []
    for name in files:
        if name in EXEMPT or name.startswith(SKIP_PREFIX):
            continue
        if Path(name).suffix.lower() in SKIP_SUFFIX:
            continue
        path = ROOT / name
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        looked_at += 1
        for n, line in enumerate(text.splitlines(), 1):
            found = ABSOLUTE.search(line)
            if found:
                hits.append((name, n, line.strip()[:110]))

    # A floor. A sweep that read nothing must not read as a pass — the failure mode
    # this project keeps finding in its own guards.
    if looked_at < 100:
        print(f"could not run: only {looked_at} files were read and this repository "
              f"holds far more, so the sweep did not really run.", file=sys.stderr)
        return 2

    if hits:
        print(f"{len(hits)} absolute home-directory path(s) in tracked files:",
              file=sys.stderr)
        for name, n, line in hits:
            print(f"  {name}:{n}\n      {line}", file=sys.stderr)
        print("\n  Nothing generated may carry an absolute path, and nothing a reader "
              "follows should name one machine. Use a repository-relative path, or "
              "add the file to EXEMPT in this script with the reason.", file=sys.stderr)
        return 1

    print(f"no absolute home-directory paths in {looked_at} tracked text files "
          f"({len(EXEMPT)} evidence records exempt by name).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
