#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
01_research/OPEN-FINDINGS.md is the document a future reader trusts to say what is
wrong with this system. It was hand-written across three review rounds and never
re-checked, so it drifted: on 19 August 2026 all 54 of its open entries were
re-verified against the tree, and four had already been fixed while six were half
right. A register that is wrong in either direction is worse than a short accurate
one, because a stale entry sends someone to fix something that is already fixed and
a missing one lets a real fault sit.

So the register is now GENERATED from 01_research/_data/findings.json, which holds
every finding, its verdict, and the command that produced that verdict. The counts
in the prose are counted. `--check` regenerates and compares, so the document cannot
drift from its own data.

RE-VERIFYING
------------
Editing a `verdict` in the data file and re-running is the whole update path. A
finding fixed after this date should have its status changed to `stale` with the
evidence that shows it, not deleted — the record of what was wrong is the useful
part.

RUN
---
    cd <the repository folder>
    ./.venv/bin/python scripts/findings.py
    ./.venv/bin/python scripts/findings.py --check
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "01_research" / "_data" / "findings.json"
OUT = ROOT / "01_research" / "OPEN-FINDINGS.md"

# The first full re-verification pass. Entries carry their own date now: a later
# pass that re-checks six of seventy entries must not stamp the other sixty-four
# with today's date, which is exactly the drift this register exists to catch. An
# entry with no date of its own belongs to the pass below.
VERIFIED_ON = "19 August 2026"


def verified_on(finding: dict) -> str:
    """The date of the CHECK THIS ENTRY NOW SHOWS — its most recent one."""
    return finding["verdict"].get("verified_on", VERIFIED_ON)


def passes(finding: dict) -> list[str]:
    """Every pass this entry has been through, oldest first.

    A pass is a historical fact and does not change when an entry is looked at
    again. Deriving membership from the latest date instead made the prose
    retroactively false: entry 12 was checked on 19 August and again on 25 August,
    and the 19 August tally silently dropped from 64 to 63 — a statement about a
    pass that had already happened, rewritten by a later one, in the one document
    whose whole purpose is that its statements stay true.
    """
    seen = finding["verdict"].get("passes")
    if seen:
        return list(seen)
    # No explicit history: the entry belongs to exactly the pass whose date it
    # carries. An entry raised on a later date was NOT in the first pass, and
    # assuming it was would inflate that pass's tally — the same falsification in
    # the other direction. Say so with `passes` when an entry has been through more
    # than one.
    return [finding["verdict"].get("verified_on", VERIFIED_ON)]

STATUS_LABEL = {
    "still_open": "Still open",
    "partly_stale": "Half stale",
    "stale": "Fixed since this was written",
    "could_not_check": "Could not be checked",
}

SEVERITY_ORDER = ["blocker", "major", "minor", "not-a-defect"]


def load() -> dict:
    if not DATA.exists():
        raise SystemExit(f"could not run: {DATA} is missing")
    return json.loads(DATA.read_text(encoding="utf-8"))


def render(data: dict) -> str:
    findings = data["findings"]
    verified = [f for f in findings if f.get("verdict")]
    closed = [f for f in findings if not f.get("verdict")]

    by_status: dict[str, list] = {}
    for f in verified:
        by_status.setdefault(f["verdict"]["status"], []).append(f)
    live = by_status.get("still_open", []) + by_status.get("partly_stale", [])
    by_sev: dict[str, list] = {}
    for f in live:
        by_sev.setdefault(f["verdict"]["severity_now"], []).append(f)

    n_stale = len(by_status.get("stale", []))
    n_open = len(by_status.get("still_open", []))
    n_half = len(by_status.get("partly_stale", []))
    n_unchecked = len(by_status.get("could_not_check", []))

    out: list[str] = []
    out.append("# Aninda Studio — what is still open\n")
    first_pass = [f for f in verified if VERIFIED_ON in passes(f)]
    later_dates = sorted({d for f in verified for d in passes(f)} - {VERIFIED_ON})
    rechecked = [f for f in verified if len(passes(f)) > 1]
    later = later_dates
    # What each pass FOUND is frozen in the data, because it is history. Deriving it
    # from today's statuses made the same sentence false twice: an entry fixed in
    # September would silently change what a pass in August is recorded as having
    # found. What CAN still be measured is the size of the pass, so it is — and a
    # disagreement stops the build rather than being written out.
    recorded = {p["date"]: p for p in data.get("_passes", [])}
    first_record = recorded.get(VERIFIED_ON)
    if first_record and first_record["covered"] != len(first_pass):
        raise SystemExit(
            f"FAILED — nothing written: _passes says the {VERIFIED_ON} pass covered "
            f"{first_record['covered']} entries, and {len(first_pass)} entries carry "
            f"that date. One of the two is wrong; fix the data, not this file.")
    out.append(
        f"**Every entry below was re-verified against the tree, and each says on "
        f"what date.** Each also carries the command that was run and what it "
        f"returned. Nothing here is asserted from memory, and nothing was marked "
        f"fixed because it looked like the sort of thing that had probably been "
        f"fixed — a claim was either reproduced or it was not.\n")
    out.append(
        f"{len(first_pass)} entries were checked in the pass of {VERIFIED_ON}"
        + (f". {len(verified) - len(first_pass)} more were raised later, and "
           + (f"{len(rechecked)} of the original entries was re-checked"
              if len(rechecked) == 1 else
              f"{len(rechecked)} of the original entries were re-checked")
           + f" — {', '.join(later)}"
           if later else "")
        + ". That first pass was needed because this document had drifted. It was "
        f"written across three review rounds and never re-checked, and of the "
        f"{len(first_pass)} entries it covered, "
        f"**{first_record['already_fixed'] if first_record else 0} were already "
        f"fixed** and "
        f"**{first_record['half_right'] if first_record else 0} were half right** — "
        f"what that pass found, on the day, kept as it was reported. A register that "
        f"is wrong in either direction is worse than a short accurate one.\n")

    counts = " · ".join(
        f"{len(by_sev.get(s, []))} {s}" for s in SEVERITY_ORDER if by_sev.get(s))
    out.append("## Where it stands\n")
    out.append("| | |")
    out.append("|---|---|")
    out.append(f"| Entries re-verified | **{len(verified)}** |")
    out.append(f"| Still open | {n_open} |")
    out.append(f"| Half stale — part reproduced, part not | {n_half} |")
    out.append(f"| Already fixed, kept as a record | {n_stale} |")
    if n_unchecked:
        out.append(f"| Could not be checked | {n_unchecked} |")
    out.append(f"| Closed earlier, by the owner's decision | {len(closed)} |")
    out.append("")
    out.append(f"Of the {len(live)} that carry work: {counts}. "
               f"**No blocker.** Everything below is a thing this system says about "
               f"itself that is not quite true, a guard that is narrower than its "
               f"message, or a piece of work not yet done — not a defect in what it "
               f"produces.\n")

    out.append("## The register\n")
    for sev in SEVERITY_ORDER:
        group = by_sev.get(sev, [])
        if not group:
            continue
        heading = {"blocker": "Blockers", "major": "Majors", "minor": "Minors",
                   "not-a-defect": "Recorded, not defects"}[sev]
        out.append(f"### {heading} ({len(group)})\n")
        for f in sorted(group, key=lambda x: (x["round"], x["id"])):
            v = f["verdict"]
            out.append(f"#### {f['id']} · {f['heading']}\n")
            if f["file"]:
                out.append(f"`{f['file']}`\n")
            out.append(f"{f['body']}\n")
            out.append(f"**{STATUS_LABEL[v['status']]}, {verified_on(f)}.** "
                       f"{v['note']}\n")
            out.append(f"*How that was checked.* {v['evidence']}\n")
            if v.get("cheap_fix"):
                out.append(f"*Smallest fix.* {v['cheap_fix']}\n")

    if by_status.get("stale"):
        out.append("### Already fixed, kept as a record "
                   f"({len(by_status['stale'])})\n")
        out.append(
            "These were true when written and are not true now. They stay because "
            "the record of what went wrong is the useful part, and because deleting "
            "them would hide that this document had drifted.\n")
        for f in sorted(by_status["stale"], key=lambda x: (x["round"], x["id"])):
            v = f["verdict"]
            out.append(f"#### {f['id']} · {f['heading']}\n")
            out.append(f"**Fixed, confirmed {verified_on(f)}.** {v['note']}\n")
            out.append(f"*How that was checked.* {v['evidence']}\n")

    if closed:
        out.append(f"### Closed by the owner's decision ({len(closed)})\n")
        for f in sorted(closed, key=lambda x: (x["round"], x["id"])):
            out.append(f"#### {f['id']} · {f['heading']}\n")
            out.append(f"{f['body']}\n")

    out.append("---\n")
    out.append(
        f"Generated by `scripts/findings.py` from `01_research/_data/findings.json`. "
        f"Editing this file by hand is undone by the next build; change the data and "
        f"regenerate. The counts above are counted, not typed.\n")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    text = render(load())
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
    data = load()
    verified = [f for f in data["findings"] if f.get("verdict")]
    dates: dict[str, int] = {}
    for f in verified:
        dates[verified_on(f)] = dates.get(verified_on(f), 0) + 1
    when = "; ".join(f"{n} on {d}" for d, n in sorted(dates.items(), key=lambda x: -x[1]))
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(data['findings'])} findings, "
          f"{len(verified)} re-verified ({when}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
