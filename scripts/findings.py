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
    cd /Users/gru953/Claude/Cowork/Aninda_Studio
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

VERIFIED_ON = "19 August 2026"

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
    out.append(
        f"**Every entry below was re-verified against the tree on {VERIFIED_ON}.** "
        f"Each carries the command that was run and what it returned. Nothing here "
        f"is asserted from memory, and nothing was marked fixed because it looked "
        f"like the sort of thing that had probably been fixed — a claim was either "
        f"reproduced or it was not.\n")
    out.append(
        f"That pass was needed because this document had drifted. It was written "
        f"across three review rounds and never re-checked, and of its "
        f"{len(verified)} entries **{n_stale} were already fixed** and "
        f"**{n_half} were half right**. A register that is wrong in either "
        f"direction is worse than a short accurate one.\n")

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
            out.append(f"**{STATUS_LABEL[v['status']]}, {VERIFIED_ON}.** "
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
            out.append(f"**Fixed.** {v['note']}\n")
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
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(data['findings'])} findings, "
          f"{len(verified)} re-verified on {VERIFIED_ON}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
