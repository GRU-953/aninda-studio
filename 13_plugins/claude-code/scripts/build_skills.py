#!/usr/bin/env python3
"""Aninda Studio — build the three .skill bundles, reproducibly, and prove it.

A .skill bundle is a plain zip with SKILL.md at the archive root.

Reproducible means: the same input always gives the same bytes, so a SHA-256 is a
statement about content rather than about when somebody ran a script. Three things
make that true here, and every one of them matters:

  1. The file list comes from sorted(), so the walk order never depends on the
     filesystem.
  2. Every entry is written through zipfile.ZipInfo with a fixed date_time and an
     explicit external_attr. zf.write(path) is never used, because it copies the
     filesystem modification time into the archive and that changes every build.
  3. .DS_Store, __pycache__ and *.pyc are excluded, because macOS writes the first
     one by looking at a folder and Python writes the other two by importing.

  python build_skills.py            build into dist/
  python build_skills.py --prove    build twice into two temporary folders,
                                    compare the SHA-256s, then build into dist/

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PLUGIN_ROOT / "skills"
DIST = PLUGIN_ROOT / "dist"
PROJECT_ROOT = PLUGIN_ROOT.parent.parent
TOKENS_DIR = SKILLS_DIR / "aninda-brand" / "assets" / "tokens"
TOKENS_CSS = SKILLS_DIR / "aninda-brand" / "assets" / "css" / "tokens.css"

# A fixed point in time for every entry in every archive. Not "now", and not the
# file's own mtime: either would make the same content hash differently on a
# second build, and the reproducibility proof below would be meaningless.
FIXED_DATE = (2026, 1, 1, 0, 0, 0)

# 0o644 for a plain file, 0o755 for one meant to be run, shifted into the high
# 16 bits where a zip stores Unix permissions.
FILE_MODE = 0o644 << 16
EXECUTABLE_MODE = 0o755 << 16

EXCLUDE_NAMES = {".DS_Store"}
EXCLUDE_DIRS = {"__pycache__", ".git", ".mypy_cache", ".pytest_cache"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}

THEMES = ("light", "dark", "hc-light", "hc-dark")


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def included(path: Path, root: Path) -> bool:
    if path.name in EXCLUDE_NAMES:
        return False
    if path.suffix in EXCLUDE_SUFFIXES:
        return False
    return not any(part in EXCLUDE_DIRS for part in path.relative_to(root).parts)


def is_executable(relative: Path) -> bool:
    return relative.suffix == ".py" and relative.parts[0] == "scripts"


# ---------------------------------------------------------------------------
# The data the review skill needs when it travels on its own
# ---------------------------------------------------------------------------


def _flatten(node, prefix: str, out: dict) -> dict:
    for key, value in node.items():
        if key.startswith("$"):
            continue
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict) and "$value" in value:
            out[path] = value["$value"]
        elif isinstance(value, dict):
            _flatten(value, path, out)
    return out


def review_system_data() -> str:
    """Derive the numbers the review skill needs from the brand skill's own files.

    Installed as a plugin, the review skill reads the brand skill's tokens
    directly, so there is one source of truth. Extracted from a standalone bundle
    there is no sibling to read, so this goes in — derived here at bundle time
    rather than committed, which means it cannot drift.
    """
    primitives = _flatten(json.loads((TOKENS_DIR / "primitive.tokens.json").read_text("utf-8")), "", {})

    def hex_of(value):
        if isinstance(value, str):
            return hex_of(primitives[value.strip().strip("{}")])
        return value["hex"]

    themes: dict[str, dict[str, str]] = {}
    targets: dict[str, dict[str, float]] = {}
    for theme in THEMES:
        raw = json.loads((TOKENS_DIR / f"semantic.{theme}.tokens.json").read_text("utf-8"))
        flat = _flatten(raw, "", {})
        themes[theme] = {
            key[len("color.") :]: hex_of(value)
            for key, value in flat.items()
            if key.startswith("color.")
        }
        studio = raw.get("$extensions", {}).get("studio.aninda", {})
        targets[theme] = {
            "text": float(studio.get("textTarget", 4.5)),
            "nonText": float(studio.get("nonTextTarget", 3.0)),
        }

    # The CSS property names, read out of the stylesheet the brand skill bundles.
    # The checker used to derive a property from a role name by swapping dots for
    # hyphens, which produced --as-accent-default and six other names that do not
    # exist. A standalone bundle has no sibling skill to read, so the names travel
    # with it.
    properties: dict[str, str] = {}
    for _name, _value in re.findall(r"(--as-[a-z0-9-]+)\s*:\s*([^;}]+)",
                                    TOKENS_CSS.read_text("utf-8")):
        properties.setdefault(_name, _value.strip())

    data = {
        "$comment": (
            "GENERATED at bundle time by 13_plugins/claude-code/scripts/build_skills.py from the "
            "aninda-brand skill's own token files. It exists so this skill can measure on its own "
            "when it travels as a single .skill file. Installed alongside aninda-brand, the "
            "checker reads that skill's tokens directly instead and ignores this. There is no date "
            "in here on purpose: the bundle has to hash the same on every build."
        ),
        "themes": themes,
        "targets": targets,
        "properties": properties,
    }
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


EXTRA_FILES = {"aninda-review": {"data/system.json": review_system_data}}


# ---------------------------------------------------------------------------
# The bundler
# ---------------------------------------------------------------------------


def build_one(skill_dir: Path, out_dir: Path) -> Path:
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise SystemExit(f"{skill_dir} has no SKILL.md, so it is not a skill")

    entries: list[tuple[str, bytes, bool]] = []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or not included(path, skill_dir):
            continue
        relative = path.relative_to(skill_dir)
        entries.append((relative.as_posix(), path.read_bytes(), is_executable(relative)))

    for archive_name, produce in EXTRA_FILES.get(name, {}).items():
        entries.append((archive_name, produce().encode("utf-8"), False))

    # Sorted again, because the extra files were appended after the walk.
    entries.sort(key=lambda item: item[0])
    if entries[0][0] != "SKILL.md" and not any(item[0] == "SKILL.md" for item in entries):
        raise SystemExit(f"{name}: SKILL.md must sit at the archive root")

    out_dir.mkdir(parents=True, exist_ok=True)
    bundle = out_dir / f"{name}.skill"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for archive_name, payload, executable in entries:
            info = zipfile.ZipInfo(archive_name, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = EXECUTABLE_MODE if executable else FILE_MODE
            info.create_system = 3  # Unix, so the permission bits above are read
            archive.writestr(info, payload)
    return bundle


def build_all(out_dir: Path) -> dict[str, str]:
    skills = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skills:
        raise SystemExit(f"there are no skills under {SKILLS_DIR}")
    return {skill.name: sha256_of(build_one(skill, out_dir)) for skill in skills}


def prove() -> dict[str, str]:
    """Build twice into two different folders and assert identical SHA-256s."""
    first_dir = Path(tempfile.mkdtemp(prefix="aninda-skill-a-"))
    second_dir = Path(tempfile.mkdtemp(prefix="aninda-skill-b-"))
    try:
        first = build_all(first_dir)
        second = build_all(second_dir)
    finally:
        pass

    lines = ["", "REPRODUCIBILITY PROOF", "-" * 72]
    lines.append(f"  build A in {first_dir}")
    lines.append(f"  build B in {second_dir}")
    lines.append("")
    failed = []
    for name in sorted(first):
        same = first[name] == second[name]
        lines.append(f"  {'same' if same else 'DIFFERENT'}  {name}.skill")
        lines.append(f"          A  {first[name]}")
        lines.append(f"          B  {second[name]}")
        if not same:
            failed.append(name)
    lines.append("")
    sys.stdout.write("\n".join(lines) + "\n")

    shutil.rmtree(first_dir, ignore_errors=True)
    shutil.rmtree(second_dir, ignore_errors=True)

    if failed:
        raise SystemExit(
            "The bundles are not reproducible: " + ", ".join(failed) + ". Something in the "
            "build is reading the clock, the filesystem's modification times, or an unsorted "
            "directory listing."
        )
    return first


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="build_skills.py", description=__doc__.split("\n")[0])
    parser.add_argument(
        "--prove",
        action="store_true",
        help="build twice into two temporary folders and assert identical SHA-256s",
    )
    args = parser.parse_args(argv)

    expected: dict[str, str] | None = None
    if args.prove:
        expected = prove()

    final = build_all(DIST)
    lines = ["", f"Wrote {len(final)} bundle(s) to {DIST}", ""]
    for name in sorted(final):
        bundle = DIST / f"{name}.skill"
        with zipfile.ZipFile(bundle) as archive:
            count = len(archive.namelist())
        lines.append(f"  {name}.skill   {bundle.stat().st_size:>7} bytes   {count:>3} entries")
        lines.append(f"    sha256  {final[name]}")
    if expected is not None:
        matched = all(expected[name] == final[name] for name in final)
        lines.append("")
        lines.append(
            "  dist/ matches the proven build."
            if matched
            else "  dist/ DIFFERS from the proven build, which should be impossible."
        )
        if not matched:
            lines.append("")
            sys.stdout.write("\n".join(lines) + "\n")
            return 1
    lines.append("")
    sys.stdout.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
