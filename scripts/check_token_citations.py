#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
PROSE THAT NAMES A CUSTOM PROPERTY NAMES ONE THAT EXISTS
========================================================
Every generated artefact in this repository is checked against the token files it
was built from. The PROSE about those artefacts was not. So when a token left, the
stylesheet lost the property, the components lost the rule, every `--check` passed
— and the guidebook went on telling readers to write:

    font-family: var(--as-font-bangla);

which resolves to nothing at all. A `var()` with no fallback and no definition is
not a build error and not a runtime error. It is an inherited value, silently.

That is what this gate is for, and it is deliberately narrow: it does NOT try to
judge whether a sentence about the system is true. It checks the one claim in
prose that has an exact mechanical answer — a property is defined or it is not.

WHY THE CODEPOINT GATE COULD NOT FIND THIS
------------------------------------------
The Bangla removal is enforced by 13_plugins/.../aninda-review/scripts/check.py,
which fails on Bengali script anywhere outside the retained record. Every string
this gate found is pure ASCII. `--as-font-bangla` contains no Bengali; neither
does "Each chapter has an English section and a Bangla one". A rule about SCRIPT
cannot see a claim about a script, and the two gates are not substitutes.

THE COUNTER-EXAMPLE LIST
------------------------
Some prose names a property in order to say it does NOT exist — the naming rules
teach that the CSS name drops a trailing `default`, and `--as-accent-default` is
the wrong half of that lesson. Those are declared below, with the reason, rather
than detected: a checker that tried to read the surrounding sentence would be
guessing, and a rule this small should not guess.

RUN
---
    cd <the repository folder>
    ./.venv/bin/python scripts/check_token_citations.py

Exit 0 if every custom property named in tracked prose is defined. Exit 1 naming
each file, each undefined property, and the line it sits on.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "07_tokens" / "css" / "tokens.css"

PROPERTY = re.compile(r"--as-[a-z0-9-]+")
DEFINITION = re.compile(r"(--as-[a-z0-9-]+)\s*:")

# Prose that names a property IN ORDER TO SAY IT DOES NOT EXIST. Each is declared
# with the lesson it serves, because an undeclared exemption here would hide the
# next real one.
# They hold IN PROSE ONLY. A document may name a property in order to say it is not
# there; a stylesheet or a card cannot, because there the name is not a sentence —
# it is a var() call that a browser will try to resolve. So the half of this gate
# that guards shipped artefacts has no exemptions at all.
COUNTER_EXAMPLES = {
    "--as-accent-default": (
        "the naming rules teach that a colour's CSS name drops a trailing "
        "`default`, and this is the wrong half of that lesson"),
    "--as-font-bangla": (
        "the findings register and the handover both quote it as the property a "
        "published stylesheet went on naming after it was removed — finding R8-3, "
        "which is the reason this gate exists"),
}

# Prose, stylesheets, and the pages a reader is handed. These are the three places
# a dead reference actually REACHES somebody: a document tells them to write it, a
# stylesheet ships it, a card shows it in a sample they are invited to copy. The
# npm package shipped `:lang(bn){font-family:var(--as-font-bangla)}` for a day and
# a half, and nothing else here would have found it.
#
# GENERATORS ARE NOT SCANNED, and that is a real hole rather than an oversight. A
# .py builds names by concatenation — f"--as-space-{step}" — so a scan of them
# reports `--as-space-` as undefined, which is noise, and suppressing the noise by
# ignoring fragments would also ignore a genuine typo. The generators are covered
# INDIRECTLY: what they write lands in the files below, which are scanned. A
# generator holding a dead name it never emits is the one case this misses.
#
# A file that DEFINES a property may also name it, which is what lets the token
# stylesheets themselves pass. That is stricter than an allow-list: a file gets to
# name only the properties it actually declares.
CHECKED = (".md", ".css", ".html")


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return [line for line in out.split("\n") if line]


def defined() -> set[str]:
    if not CSS.is_file():
        print(f"FAILED — {CSS.relative_to(ROOT)} is not there, so this gate "
              f"cannot run. A gate that cannot run is not a gate.", file=sys.stderr)
        raise SystemExit(2)
    return set(DEFINITION.findall(CSS.read_text(encoding="utf-8")))


def main() -> int:
    known = defined()
    problems: list[str] = []
    checked = cited = 0

    for rel in tracked():
        if not rel.endswith(CHECKED):
            continue
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "--as-" not in text:
            continue
        checked += 1
        local = set(DEFINITION.findall(text))
        for number, line in enumerate(text.split("\n"), start=1):
            for name in dict.fromkeys(PROPERTY.findall(line)):
                cited += 1
                if name in known or name in local:
                    continue
                if name in COUNTER_EXAMPLES and rel.endswith(".md"):
                    continue
                problems.append(
                    f"{rel}:{number}  {name} is not defined in "
                    f"{CSS.relative_to(ROOT)}")

    if problems:
        print("FAILED — prose names a custom property that does not exist:",
              file=sys.stderr)
        for x in problems:
            print(f"  {x}", file=sys.stderr)
        print("\n  A var() with no definition and no fallback inherits silently. "
              "Either\n  the property should be there, or the prose should say it "
              "is not — and if\n  it names one deliberately, declare it in "
              "COUNTER_EXAMPLES with the reason.", file=sys.stderr)
        return 1

    print(f"  ok    {cited} custom-property citations across {checked} documents, "
          f"stylesheets and cards, every one defined — among the {len(known)} in "
          f"{CSS.relative_to(ROOT)}, or by the file itself"
          + (f" ({len(COUNTER_EXAMPLES)} declared counter-examples, prose only)"
             if COUNTER_EXAMPLES else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
