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
    cd <the repository folder>
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
#
# `cd ` is deliberately NOT in this list, and that is the whole point of the note.
# It used to be, and combined with a parser that read only the first line of a
# `run: |` block it silently exempted three real gates — the npm resolve check and
# both manifest gates, the two newest and the ones added to close exactly the class
# of bug this file exists to catch. Deleting any of them from verify-all.sh still
# printed "all 32 CI gates appear". A step is setup only when EVERY line in it is
# setup, which is what is tested below.
SETUP = (
    "npm ci", "pip install", "playwright install",
    "python -m playwright install", "tsc --noEmit",
)

# Lines that are neither setup nor a check: they move around, name a thing, or
# report. A block made only of these plus SETUP is not a gate.
NOISE_PREFIXES = ("cd ", "export ", "set ", "echo ", "#", "fi", "else", "done", "}")


def is_setup(body: str) -> bool:
    """True when nothing in this block actually checks anything.

    Judged line by line. A block that changes directory and THEN runs a gate is a
    gate; a block that only changes directory is setup. Reading the first line
    alone cannot tell those apart, and for three steps it got it wrong.
    """
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    if not lines:
        return True
    for line in lines:
        if any(line.startswith(s) or line == s.strip() for s in SETUP):
            continue
        if any(line.startswith(n) for n in NOISE_PREFIXES) or line in ("|", "\\"):
            continue
        return False
    return True

# The artefact each CI command names, and the text that must appear somewhere in
# verify-all.sh for that gate to be covered. Only needed where the two phrase the
# same check differently.
# Keyed by the STEP'S NAME, and checked before ALIAS. Needed where the command
# names an artefact that several gates name — three steps all run `build.mjs`, so
# a substring test on "build.mjs" passes even when the specific gate has been
# deleted from the script. The value is the distinctive label verify-all.sh prints
# for that gate, which is unique by construction because it is what a reader sees.
NAME_ALIAS = {
    "The full build completes and the manifest is adopted":
        "the full figma build completes",
    "A placeholder manifest must stop the build":
        "a placeholder manifest stops the figma build",
    "The npm package must actually resolve":
        "npm entry points import and agree",
    "Nothing built may differ from what was committed":
        "figma plugin build is current",
    "Nothing bundled may differ from what was committed":
        "claude-code skill bundles are current",
    "Rebuild the Figma plugin": "figma plugin build is current",
    "The Figma plugin must typecheck": "figma plugin typechecks",
}

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
    """Every `run:` in the workflow, with its WHOLE body.

    The body used to be `(?P<body>.*)$` under re.M, and `.` does not cross a
    newline — so a `run: |` block collapsed to its first line. Three gates opened
    with `cd`, were read as a bare directory change, and were dropped. The block is
    now taken in full: every line indented deeper than the `run:` key belongs to it.
    """
    text = CI.read_text(encoding="utf-8")
    out: list[tuple[str, str]] = []
    lines = text.splitlines()
    name = "(unnamed)"
    i = 0
    while i < len(lines):
        line = lines[i]
        m_name = re.match(r"^\s+- name: (?P<n>.+)$", line)
        if m_name:
            name = m_name.group("n").strip()
            i += 1
            continue
        m_run = re.match(r"^(?P<indent>\s+)-? ?run: (?P<rest>.*)$", line)
        if m_run:
            indent = len(m_run.group("indent"))
            rest = m_run.group("rest").strip()
            body_lines: list[str] = []
            if rest and rest != "|":
                body_lines.append(rest)
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if not nxt.strip():
                    body_lines.append("")
                    i += 1
                    continue
                depth = len(nxt) - len(nxt.lstrip())
                if depth <= indent:
                    break
                body_lines.append(nxt.strip())
                i += 1
            out.append((name, "\n".join(body_lines).strip()))
            name = "(unnamed)"
            continue
        i += 1
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
        if is_setup(body):
            continue
        # Match an alias against ANY line of the block, not just the first. With
        # whole blocks now in hand, a gate's identifying command is often on line
        # two or three, after a cd or an export.
        needle = NAME_ALIAS.get(name)
        block_lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        for prefix, alias in ALIAS.items() if needle is None else ():
            if any(ln.startswith(prefix) for ln in block_lines):
                needle = alias
                break
        if needle is None:
            # Default: the first path-looking token in the first line that is not
            # setup or noise — the command the step is actually about.
            meat = [ln for ln in block_lines
                    if not any(ln.startswith(n) for n in NOISE_PREFIXES)
                    and not any(ln.startswith(s) for s in SETUP)]
            token = re.search(r"[\w./-]+\.(?:py|mjs|sh)", "\n".join(meat))
            needle = token.group(0) if token else (meat[0][:40] if meat else body[:40])
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
