#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
06_type/MEASUREMENTS.md opens by saying every number in it is a measurement, and
06_type/specimen.py promises every one is reproducible by running one script. The
document is written by hand, and nothing compared it to the data.

Round 3 found three x/cap cells disagreeing with 06_type/_data/measurements.json,
and they erred in OPPOSITE directions, so it was not a rounding convention — it
was three cells computed three different ways. Source Serif 4 and Inconsolata were
divided from the ROUNDED cap and x-height printed beside them; Geist Mono was
0.74648 written as 0.747, which is not what that rounds to either way.

The x/cap column is the one this checks, because it is derived rather than
observed: cap height and x-height are readings, and x/cap is arithmetic on them,
so it is the column that can be wrong without anyone touching a font.

RUN
---
    ./.venv/bin/python scripts/check_measurements.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "06_type" / "_data" / "measurements.json"
DOC = ROOT / "06_type" / "MEASUREMENTS.md"

# The size the two x/cap tables are quoted at.
SIZE = "16"

# Display name in the document -> key in measurements.json. Written out because
# the two vocabularies genuinely differ ("Source Serif 4" / "sourceserif4"), and
# a silent failure to match a row would be this checker not running.
FAMILIES = {
    "Inter": "inter", "Libre Franklin": "librefranklin", "Archivo": "archivo",
    "Public Sans": "publicsans", "IBM Plex Sans": "ibmplexsans",
    "Roboto Flex": "robotoflex", "Instrument Sans": "instrumentsans",
    "Literata": "literata", "Work Sans": "worksans",
    "Source Sans 3": "sourcesans3", "Source Serif 4": "sourceserif4",
    "Newsreader": "newsreader", "Martian Mono": "martianmono",
    "JetBrains Mono": "jetbrainsmono", "Noto Sans Mono": "notosansmono",
    "Geist Mono": "geistmono", "Roboto Mono": "robotomono",
    "IBM Plex Mono": "ibmplexmono", "Source Code Pro": "sourcecodepro",
    "Inconsolata": "inconsolata",
}

ROW = re.compile(r"^\|\s*([A-Za-z0-9 ]+?)\s*\|(.+)\|\s*$")
CELL = re.compile(r"\*{0,2}([0-9]*\.?[0-9]+)\*{0,2}")


def main() -> int:
    for path in (DATA, DOC):
        if not path.exists():
            print(f"could not run: {path} is missing", file=sys.stderr)
            return 2

    ink = json.loads(DATA.read_text())["ink"]
    problems: list[str] = []
    checked = 0

    # Table-aware. The document holds several tables whose rows start with a
    # family name — optical-size axes, line-height floors, Bangla metrics — and
    # some of those carry numbers between 0.5 and 1.0 too. Only the tables whose
    # HEADER declares an x/cap column are read, and the column index comes from
    # that header rather than from guessing which cell looks like a ratio.
    column: int | None = None
    for line in DOC.read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            headers = [c.strip().lower() for c in line.strip("|").split("|")]
            if "x/cap" in headers:
                column = headers.index("x/cap") - 1   # minus the family column
                continue
        elif line.strip() and not line.startswith("|"):
            column = None            # a table ended
        if column is None:
            continue
        match = ROW.match(line)
        if not match:
            continue
        name = match.group(1).strip()
        key = FAMILIES.get(name)
        if key is None or key not in ink or SIZE not in ink[key]:
            continue
        cells = [c.strip() for c in match.group(2).split("|")]
        if column >= len(cells) or not CELL.fullmatch(cells[column]):
            problems.append(f"{name}: no x/cap value in column {column + 2}")
            continue
        stated = float(CELL.fullmatch(cells[column]).group(1))
        metrics = ink[key][SIZE]
        real = round(metrics["x_height"]["ascent"] / metrics["cap_H"]["ascent"], 3)
        checked += 1
        if stated != real:
            problems.append(
                f"{name}: MEASUREMENTS.md says x/cap {stated}, and "
                f"{metrics['x_height']['ascent']:.4f} / {metrics['cap_H']['ascent']:.4f} "
                f"at {SIZE}px is {real}"
            )

    # A run that matched no rows would print a clean pass having checked nothing.
    if checked < 18:
        print(f"could not run: matched only {checked} family rows in {DOC.name}, "
              f"and there are 20 families to find. The table shape changed, so this "
              f"check did not really run.", file=sys.stderr)
        return 1

    if problems:
        print(f"{len(problems)} x/cap figure(s) disagree with the measurements:",
              file=sys.stderr)
        for item in problems:
            print(f"  {item}", file=sys.stderr)
        print("\n  Every one is arithmetic on the two readings printed beside it. "
              "Divide the raw values, not the rounded ones.", file=sys.stderr)
        return 1

    print(f"  {checked} x/cap figures in MEASUREMENTS.md match "
          f"{DATA.relative_to(ROOT)} at {SIZE}px.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
