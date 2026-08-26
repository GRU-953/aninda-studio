#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
01_research/BENCHMARK.md records what Apple and Google publish. It does not record
what this kit does about it. Those are different documents and conflating them is
how a benchmark turns into a wish list: a row that says "Apple asks for unmasked
layers" reads as though the matter is settled, when the tree was in fact shipping
pre-rounded artwork on the day it was written.

So the distance between the two is measured here, once, and generated. Each gap
names four things and is refused without them: the requirement, the source it comes
from with the date it was read, what was measured in this tree, and the fix. A gap
with no source is one this system sets for itself, and the register says so rather
than borrowing authority it does not have.

WHY IT IS SEPARATE FROM OPEN-FINDINGS.md
----------------------------------------
OPEN-FINDINGS.md records defects against this system's own rules. This records
distance from someone else's published rules, which can change without anything
here changing. Keeping them apart means a platform revision does not look like a
regression, and a regression does not hide among platform revisions.

RUN
---
    cd <the repository folder>
    ./.venv/bin/python scripts/gaps.py
    ./.venv/bin/python scripts/gaps.py --check
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "01_research" / "_data" / "platform-gaps.json"
OUT = ROOT / "01_research" / "PLATFORM-GAPS.md"

SEVERITY_ORDER = ["blocker", "major", "minor"]
SEVERITY_LABEL = {
    "blocker": "Blocker",
    "major": "Major",
    "minor": "Minor",
}
STATUS_LABEL = {
    "open": "open",
    "deferred": "deferred, with the reason recorded",
    "closed": "closed",
}
PLATFORM_LABEL = {
    "apple": "Apple",
    "google": "Google",
    "both": "Both",
    "none": "This kit's own record",
}
AREA_ORDER = ["icon", "store", "colour", "native", "motion", "accessibility", "record"]
AREA_LABEL = {
    "icon": "The icon",
    "store": "Store assets",
    "colour": "Colour",
    "native": "Reaching a native app",
    "motion": "Motion",
    "accessibility": "Accessibility",
    "record": "The record itself",
}


def load() -> dict:
    with DATA.open(encoding="utf-8") as fh:
        return json.load(fh)


def guard(data: dict) -> list[str]:
    """Fail closed. A register that is missing the parts that make a gap checkable
    is worse than no register, because it reads as though the work were done."""
    problems: list[str] = []
    seen: set[str] = set()
    for g in data["gaps"]:
        gid = g.get("id", "<no id>")
        if gid in seen:
            problems.append(f"{gid}: duplicate id")
        seen.add(gid)
        for field in ("id", "area", "platform", "severity", "title",
                      "requirement", "measured", "fix", "status"):
            if not g.get(field):
                problems.append(f"{gid}: no {field!r}")
        if g.get("severity") not in SEVERITY_ORDER:
            problems.append(f"{gid}: severity {g.get('severity')!r} is not one of {SEVERITY_ORDER}")
        if g.get("status") not in STATUS_LABEL:
            problems.append(f"{gid}: status {g.get('status')!r} is not one of {sorted(STATUS_LABEL)}")
        if g.get("area") not in AREA_ORDER:
            problems.append(f"{gid}: area {g.get('area')!r} is not one of {AREA_ORDER}")
        if g.get("platform") not in PLATFORM_LABEL:
            problems.append(f"{gid}: platform {g.get('platform')!r} is not known")
        # A gap against a published requirement must cite it. A gap this kit sets
        # for itself must NOT, so that borrowed authority is visible as borrowed.
        for src in g.get("sources", []):
            if not src.get("url") or not src.get("date"):
                problems.append(f"{gid}: a source has no url or no date")
        if g.get("platform") in ("apple", "google", "both") and not g.get("sources"):
            problems.append(f"{gid}: names a platform but cites no source for the requirement")
    return problems


def render(data: dict) -> str:
    gaps = data["gaps"]
    counts = {s: sum(1 for g in gaps if g["severity"] == s) for s in SEVERITY_ORDER}
    open_n = sum(1 for g in gaps if g["status"] == "open")
    deferred_n = sum(1 for g in gaps if g["status"] == "deferred")
    sourced = sum(1 for g in gaps if g.get("sources"))
    urls = {s["url"] for g in gaps for s in g.get("sources", [])}

    L: list[str] = []
    add = L.append
    add("# Where this kit stands against Apple and Google")
    add("")
    add("GENERATED FILE. Written by `scripts/gaps.py` from "
        "`01_research/_data/platform-gaps.json`. Do not hand-edit — the next build "
        "overwrites it. Change the data and re-run.")
    add("")
    add(f"**Assessed:** {data['assessed_on']}.")
    add("")
    add(data["against"])
    add("")
    add(f"{len(gaps)} gaps: **{counts['blocker']} blockers**, {counts['major']} major, "
        f"{counts['minor']} minor. {open_n} open, {deferred_n} deferred with the reason "
        f"recorded. {sourced} of {len(gaps)} cite a published requirement, across "
        f"{len(urls)} distinct sources; the rest are rules this kit sets for itself "
        f"and are marked as such.")
    add("")
    add("A **blocker** means a store would refuse the listing, or a platform's own "
        "component set cannot be built. It does not mean the work is poor. Every one "
        "of them is a thing this kit never claimed to do, being claimed now.")
    add("")
    add("---")
    add("")

    add("## The short answer")
    add("")
    add("| # | Gap | Platform | Severity |")
    add("|---|---|---|---|")
    for s in SEVERITY_ORDER:
        for g in gaps:
            if g["severity"] != s:
                continue
            add(f"| `{g['id']}` | {g['title']} | {PLATFORM_LABEL[g['platform']]} "
                f"| {SEVERITY_LABEL[s]} |")
    add("")
    add("---")
    add("")

    for area in AREA_ORDER:
        here = [g for g in gaps if g["area"] == area]
        if not here:
            continue
        add(f"## {AREA_LABEL[area]}")
        add("")
        here.sort(key=lambda g: (SEVERITY_ORDER.index(g["severity"]), g["id"]))
        for g in here:
            add(f"### `{g['id']}` — {g['title']}")
            add("")
            add(f"**{SEVERITY_LABEL[g['severity']]}** · {PLATFORM_LABEL[g['platform']]} "
                f"· {STATUS_LABEL[g['status']]}")
            add("")
            add(f"**What is required.** {g['requirement']}")
            add("")
            add(f"**What is here.** {g['measured']}")
            add("")
            add(f"**The fix.** {g['fix']}")
            add("")
            if g.get("sources"):
                add("**Sources.**")
                add("")
                for src in g["sources"]:
                    add(f"- `{src['url']}` — {src['date']}")
                add("")
            else:
                add("**Sources.** None. This is a rule this kit sets for itself, "
                    "and no platform is cited for it.")
                add("")
        add("---")
        add("")

    add("## What this register cannot tell you")
    add("")
    add("- **It does not prove a store would accept anything.** Every figure is "
        "measured against a published specification, not against a console's own "
        "validator. A console may refuse a file for a reason no published page states.")
    add("- **It is current only on the date at the top.** Store specifications change "
        "without notice and without a change log. Two of the gaps here exist because "
        "a page moved and this kit did not notice for twelve days.")
    add("- **It measures distance, not quality.** A kit can close every gap here and "
        "still be unpleasant to use. Contrast, target size and safe-zone occupancy are "
        "measurable; whether a person can finish a task is not.")
    add("- **Some requirements have no number to meet.** Apple publishes no app-icon "
        "corner radius, no numeric safe zone outside tvOS, and no pixel dimensions for "
        "its new creative slots. Where that is so, this register says so rather than "
        "supplying a figure and attributing it.")
    add("")
    return "\n".join(L) + "\n"


def main(argv: list[str]) -> int:
    data = load()
    problems = guard(data)
    if problems:
        print("REFUSED — the gap data is not complete enough to publish:",
              file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    text = render(data)
    if "--check" in argv:
        if not OUT.exists():
            print(f"CHECK FAILED — {OUT.name} is missing", file=sys.stderr)
            return 1
        if OUT.read_text(encoding="utf-8") != text:
            print(f"CHECK FAILED — {OUT.name} has drifted from its data",
                  file=sys.stderr)
            return 1
        print(f"--check: {OUT.name} matches its data. Nothing written.")
        return 0

    OUT.write_text(text, encoding="utf-8")
    gaps = data["gaps"]
    blockers = sum(1 for g in gaps if g["severity"] == "blocker")
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(gaps)} gaps, {blockers} of them "
          f"blockers, assessed {data['assessed_on']}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
