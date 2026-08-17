#!/usr/bin/env python3
"""Aninda Studio — put the right SPDX header on every file, or check that it is there.

Four licences apply to different parts of a repository, so a header is not one
string repeated everywhere. This maps each file to the licence that actually
covers it, and refuses to guess: a suffix it has no rule for is reported, never
stamped with a default.

  python spdx.py --check <path>    report what is missing or wrong; changes nothing
  python spdx.py --write <path>    add a missing header; never replaces a different one

Exit status: 0 nothing to do, 1 something is missing or wrong, 2 bad arguments.

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

APACHE = "Apache-2.0"
POLYFORM = "PolyForm-Noncommercial-1.0.0"

# Which licence covers which kind of file. A suffix that is not here is reported
# rather than given a default, because a wrong licence header is worse than none.
BY_SUFFIX = {
    ".py": APACHE,
    ".mjs": APACHE,
    ".js": APACHE,
    ".ts": APACHE,
    ".tsx": APACHE,
    ".jsx": APACHE,
    ".sh": APACHE,
    ".css": APACHE,
    ".yml": APACHE,
    ".yaml": APACHE,
    ".md": POLYFORM,
    # In this system an HTML file is either a plugin window or a generated card,
    # and both are code. A hand-written HTML documentation page needs PolyForm
    # chosen by hand rather than taken from this table.
    ".html": APACHE,
    ".htm": APACHE,
}

# Files that carry no header at all, and why.
NO_HEADER = {
    # Verbatim legal text. Stamping a header onto a licence changes a licence.
    re.compile(r"^(LICENSE|LICENCE|NOTICE|COPYING)"): "verbatim licence text",
    re.compile(r"-OFL\.txt$"): "verbatim licence text",
    # JSON has no comment syntax, so a header cannot go in one without breaking it.
    re.compile(r"\.json$"): "JSON has no comments; state the licence in NOTICE instead",
    # The identity is not licensed, so it gets no licence header.
    re.compile(r"^(mark|wordmark|tile|icon)-"): "part of the identity, which is not licensed",
    re.compile(r"\.(woff2|ttf|otf|png|jpg|jpeg|pdf|fig|zip|skill)$"): "a binary file",
}

# A file with no suffix, matched by name instead.
BY_NAME = {
    "gitignore": APACHE,
    ".gitignore": APACHE,
    "gitattributes": APACHE,
    ".gitattributes": APACHE,
    "Makefile": APACHE,
    "Dockerfile": APACHE,
}
HASH_COMMENT_NAMES = set(BY_NAME)

COMMENT = {
    ".py": ("# ", ""),
    ".sh": ("# ", ""),
    ".yml": ("# ", ""),
    ".yaml": ("# ", ""),
    ".mjs": ("// ", ""),
    ".js": ("// ", ""),
    ".ts": ("// ", ""),
    ".tsx": ("// ", ""),
    ".jsx": ("// ", ""),
    ".css": ("/* ", " */"),
    ".md": ("<!-- ", " -->"),
}

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "browsers",
    ".mypy_cache", ".pytest_cache", "dist",
}

SPDX_LINE = re.compile(r"SPDX-License-Identifier:\s*([A-Za-z0-9.\-+ ]+)")
COPYRIGHT = "Copyright 2026 Aninda Sundar Howlader"
FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.S)

# How far into a file a real header can be. A header often sits inside a docstring
# or an opening comment block, which can run a good few lines. Beyond this an SPDX
# line is a code sample or a quotation, and a reference document about licensing is
# full of both.
HEADER_LINES = 40


def no_header_reason(path: Path) -> str | None:
    for pattern, why in NO_HEADER.items():
        if pattern.search(path.name):
            return why
    return None


def comment_style(path: Path) -> tuple[str, str]:
    if path.name in HASH_COMMENT_NAMES:
        return "# ", ""
    return COMMENT[path.suffix.lower()]


def licence_for(path: Path) -> str | None:
    if path.name in BY_NAME:
        return BY_NAME[path.name]
    return BY_SUFFIX.get(path.suffix.lower())


def header_for(path: Path, licence: str) -> str:
    opener, closer = comment_style(path)
    if closer:
        return f"{opener}SPDX-License-Identifier: {licence}\n{COPYRIGHT}{closer}\n"
    return f"{opener}SPDX-License-Identifier: {licence}\n{opener}{COPYRIGHT}\n"


def declared_licence(text: str) -> str | None:
    """Read a header, and only a header.

    The search starts after any YAML front matter and stops after a few lines, so
    an SPDX line quoted in a code sample further down is not mistaken for the
    file's own.
    """
    body = text
    match = FRONT_MATTER.match(text)
    if match:
        body = text[match.end() :]
    window = "\n".join(body.split("\n")[:HEADER_LINES])
    found = SPDX_LINE.search(window)
    return found.group(1).strip() if found else None


def walk(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return [
        p
        for p in sorted(target.rglob("*"))
        if p.is_file() and not any(part in SKIP_DIRS for part in p.parts)
    ]


def insert_header(text: str, header: str) -> str:
    """Put the header where it belongs, which is not always the first line.

    A shebang has to stay on line one or the file stops being runnable. YAML front
    matter has to start on line one or the tool reading it stops seeing it. In both
    cases the header goes immediately after.
    """
    if text.startswith("#!"):
        first, _, rest = text.partition("\n")
        return f"{first}\n{header}{rest}"
    match = FRONT_MATTER.match(text)
    if match:
        return text[: match.end()] + "\n" + header + text[match.end() :]
    return header + text


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="spdx.py", description=__doc__.split("\n")[0])
    parser.add_argument("path")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    target = Path(args.path).expanduser().resolve()
    if not target.exists():
        sys.stderr.write(f"\nThere is nothing at {target}\n\n")
        return 2

    missing: list[str] = []
    wrong: list[str] = []
    unknown: list[str] = []
    exempt = 0
    already = 0
    written: list[str] = []

    for path in walk(target):
        why = no_header_reason(path)
        if why:
            exempt += 1
            continue
        suffix = path.suffix.lower()
        licence = licence_for(path)
        if licence is None:
            unknown.append(f"{path}  (no rule for {suffix or 'a file with no suffix'})")
            continue
        try:
            text = path.read_text("utf-8")
        except (UnicodeDecodeError, OSError):
            unknown.append(f"{path}  (could not be read as UTF-8 text)")
            continue

        declared = declared_licence(text)
        if declared is not None:
            if declared == licence:
                already += 1
            else:
                wrong.append(
                    f"{path}  says {declared}, and the rule for {suffix or path.name} is {licence}"
                )
            continue

        missing.append(f"{path}  needs {licence}")
        if args.write:
            path.write_text(insert_header(text, header_for(path, licence)), "utf-8")
            written.append(str(path))

    out = ["", f"{'Wrote' if args.write else 'Checked'} headers under {target}", ""]
    out.append(f"  {already:>5}  already correct")
    out.append(f"  {exempt:>5}  exempt, by the rules in this script")
    out.append(f"  {len(written) if args.write else len(missing):>5}  {'written' if args.write else 'missing'}")
    out.append(f"  {len(wrong):>5}  declaring a different licence")
    out.append(f"  {len(unknown):>5}  no rule, so left alone")

    for title, items in (
        ("MISSING" if not args.write else "WRITTEN", written if args.write else missing),
        ("DECLARING A DIFFERENT LICENCE — decide by hand, this script will not change one", wrong),
        ("NO RULE — add one to BY_SUFFIX or NO_HEADER rather than guessing", unknown),
    ):
        if not items:
            continue
        out.append("")
        out.append(title)
        out.append("-" * 72)
        for item in items:
            out.append(f"  {item}")

    out.append("")
    sys.stdout.write("\n".join(out) + "\n")
    return 1 if (missing and not args.write) or wrong or unknown else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
