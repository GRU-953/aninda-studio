#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
There are two lists of the checks this project runs: `.github/workflows/ci.yml` and
`scripts/verify-all.sh`. The whole point of the second is that a local pass means
the same thing as a green run — and it only means that if the two lists agree.

They did not. Three pushes went out red, each on a different gate the script was
missing: the Figma bundle drift check, then the .skill bundle drift check, then the
README rebuild chain. Each was found by pushing, one at a time. A fourth diff, done
properly instead of by discovery, found SEVEN more absent at once — the marks drift
guard among them, which is the gate that proves the identity artwork still matches
its generator.

So this compares the two mechanically. Every command CI runs must appear in
verify-all.sh. It is a substring test on the artefact each command names, not a
literal string match, because the script legitimately calls things differently:
CI runs `python 04_mark/build.py` and then a `git diff`, while the script does both
inside one gate and prints one line.

WHAT IT DELIBERATELY IGNORES
----------------------------
Setup commands. `npm ci`, `pip install`, `playwright install` and the `cd` lines
are how a runner gets ready, not checks. They are listed in SETUP below so that
adding one does not fail this guard, and so that a reader can see the distinction
was made on purpose.

RUN
---
    cd /Users/gru953/Claude/Cowork/Aninda_Studio
    ./.venv/bin/python scripts/check_gates.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CI = ROOT / ".github" / "workflows" / "ci.yml"
SCRIPT = ROOT / "scripts" / "verify-all.sh"

# Commands that prepare a runner rather than check anything.
SETUP = (
    "npm ci", "pip install", "playwright install", "cd ", "tsc --noEmit",
)

# The artefact each CI command names, and the text that must appear somewhere in
# verify-all.sh for that gate to be covered. Only needed where the two phrase the
# same check differently.
ALIAS = {
    "python 04_mark/build.py": "04_mark/build.py",
    "git diff --exit-code 04_mark/svg": "04_mark/svg",
    "python 05_colour/engine.py": "05_colour/engine.py",
    "python 07_tokens/build.py": "07_tokens/build.py",
    "python 07_tokens/emit_css.py": "07_tokens/emit_css.py",
    "git diff --exit-code 05_colour/generated": "05_colour/engine.py --check",
    "git diff --exit-code 13_plugins/figma/dist": "13_plugins/figma/dist",
    "git diff --exit-code 13_plugins/claude-code/dist": "13_plugins/claude-code/dist",
    # The script checks TRACKED files for both of these, because CI only ever sees
    # a checkout; sweeping the working tree made them fail on gitignored files.
    "find . -name '*.json'": "every tracked JSON parses",
    "if find . -name '.DS_Store'": ".DS_Store",
    "for f in 07_tokens/css/tokens.css": "generated files say they are generated",
    "fail=0": "english standard",
    "node build.mjs --code-only": "node build.mjs",
    "python 13_plugins/claude-code/scripts/build_skills.py --prove":
        "build_skills.py --prove",
}


def ci_commands() -> list[tuple[str, str]]:
    text = CI.read_text(encoding="utf-8")
    out: list[tuple[str, str]] = []
    for block in re.finditer(
            r"^\s+- name: (?P<name>.+)\n(?:\s+#.*\n)*\s+run: (?:\|\s*\n)?(?P<body>.*)$",
            text, re.M):
        out.append((block.group("name").strip(), block.group("body").strip()))
    # `run:` steps with no name (there are a few) still count as gates.
    for block in re.finditer(r"^\s+- run: (?P<body>.*)$", text, re.M):
        out.append(("(unnamed)", block.group("body").strip()))
    return out


def main() -> int:
    for path in (CI, SCRIPT):
        if not path.exists():
            print(f"could not run: {path} is missing", file=sys.stderr)
            return 2
    script = SCRIPT.read_text(encoding="utf-8").lower()

    missing: list[tuple[str, str]] = []
    checked = 0
    for name, body in ci_commands():
        if any(body.startswith(s) or body == s.strip() for s in SETUP):
            continue
        if any(s in body for s in ("npm ci", "pip install", "playwright install")):
            continue
        needle = None
        for prefix, alias in ALIAS.items():
            if body.startswith(prefix):
                needle = alias
                break
        if needle is None:
            # Default: the first path-looking token in the command.
            token = re.search(r"[\w./-]+\.(?:py|mjs|sh)", body)
            needle = token.group(0) if token else body[:40]
        checked += 1
        if needle.lower() not in script:
            missing.append((name, needle))

    if checked < 20:
        print(f"could not run: only {checked} CI gates were parsed out of ci.yml, "
              f"and there are more than that. The workflow's shape changed, so this "
              f"comparison did not really run.", file=sys.stderr)
        return 1

    if missing:
        print(f"{len(missing)} of {checked} CI gates are not in "
              f"scripts/verify-all.sh:", file=sys.stderr)
        for name, needle in missing:
            print(f"  {name}\n      expected to find {needle!r} in the script",
                  file=sys.stderr)
        print("\n  A local pass has to mean what a green run means. Add each gate to "
              "the script, or add an alias to ALIAS in this file if the script "
              "already covers it under another name.", file=sys.stderr)
        return 1

    print(f"  all {checked} CI gates appear in scripts/verify-all.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
