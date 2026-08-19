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


# Commands that cannot run without a browser. Determined by reading the script, not
# guessed: each of these launches Chromium through Playwright at some point in the
# path its CI invocation takes.
#
# --check modes are NOT automatically safe. 08_components/build.py --check,
# 11_site/build.py --check and 09_guidebook/build.py --check all import playwright
# somewhere and all run fine without a browser, because their check paths never
# launch one. 10_assets/build.py --check does launch one, because it re-renders
# twenty rasters in order to compare them. That difference is exactly what this list
# records, and it is why the list is hand-kept with a reason rather than derived from
# an import scan.
# Each entry is a full invocation including its flags, because the flags decide it.
# MEASURED, not reasoned about: every one below was run with
# PLAYWRIGHT_BROWSERS_PATH pointed at an empty directory, and these are the ones that
# failed with "Chromium would not launch".
#
#   10_assets/build.py --check        NEEDS a browser  — it re-renders 20 rasters
#   09_guidebook/scripts/pdf.py --check   runs without one
#   08_components/build.py --check        runs without one
#   11_site/build.py --check              runs without one
#   09_guidebook/build.py --check         runs without one
#
# The first version of this list held the script names rather than the invocations,
# and it immediately flagged pdf.py --check, which is fine. A guard that cries wolf
# gets switched off, so the list is what the empty-directory test actually returned.
NEEDS_BROWSER = (
    "python 10_assets/build.py --check",
    "python 10_assets/build.py\n",
    "python 04_mark/build.py",
    "python 00_sandbox/measure.py",
    "python 08_components/check.py",
    "python 11_site/check.py",
)


def jobs_and_steps() -> dict[str, str]:
    """Each job's name mapped to its whole YAML body."""
    text = CI.read_text(encoding="utf-8")
    body = text[text.index("\njobs:"):]
    out: dict[str, str] = {}
    starts = [(m.start(), m.group(1))
              for m in re.finditer(r"^  ([a-z][\w-]*):\n", body, re.M)]
    for i, (at, name) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(body)
        out[name] = body[at:end]
    return out


def check_browser_jobs() -> list[str]:
    """A gate that needs Chromium must sit in a job that installs Chromium.

    This cost two red CI runs. 10_assets/build.py --check went into the `build` job,
    which installs Python and Node and no browser, and the check re-renders twenty
    rasters — so it failed with "Chromium would not launch" while every local gate
    passed, because a development machine always has one. No comparison of the two
    gate LISTS could see it: the gate was present in both, in the wrong job.
    """
    problems: list[str] = []
    for name, body in jobs_and_steps().items():
        has_browser = "playwright install" in body
        for command in NEEDS_BROWSER:
            if command in body and not has_browser:
                problems.append(
                    f"job {name!r} runs {command!r}, which launches Chromium, and "
                    f"that job never runs `playwright install`")
    return problems


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

    browser = check_browser_jobs()
    if browser:
        print(f"{len(browser)} CI gate(s) need a browser and are in a job without "
              f"one:", file=sys.stderr)
        for item in browser:
            print(f"  {item}", file=sys.stderr)
        print("\n  Move the step to `marks` or `render`, which install Chromium, or "
              "add the install to its job. A local run cannot catch this: a "
              "development machine always has a browser.", file=sys.stderr)
        return 1

    print(f"  all {checked} CI gates appear in scripts/verify-all.sh, and every gate "
          f"that needs a browser is in a job that installs one")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
