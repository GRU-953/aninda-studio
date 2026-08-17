#!/usr/bin/env python3
"""Aninda Studio — check that the Claude Code plugin is well formed.

Everything here is a thing that would otherwise fail quietly: a command that
never appears, a skill that competes with another for the same request, a
reference the SKILL.md points at that is not there, or a verified Bangla table
that has drifted from the JSON the scripts read.

  python check_plugin.py

Exit status: 0 all well, 1 something is wrong.

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
COMMANDS = PLUGIN_ROOT / "commands"
SKILLS = PLUGIN_ROOT / "skills"
DIST = PLUGIN_ROOT / "dist"

EXPECTED_SKILLS = ("aninda-brand", "aninda-repo", "aninda-review")
EXPECTED_COMMANDS = ("asset", "design", "check", "init")
BRAND_REFERENCES = (
    "colour", "typography", "layout", "logo", "icons",
    "motion", "voice", "bangla", "licence", "naming",
)
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


class Problems:
    def __init__(self) -> None:
        self.items: list[str] = []
        self.passed: list[str] = []

    def wrong(self, message: str) -> None:
        self.items.append(message)

    def ok(self, message: str) -> None:
        self.passed.append(message)


def front_matter(path: Path) -> dict[str, str]:
    """A small YAML reader for `key: value` and `key: >-` folded blocks."""
    match = FRONT_MATTER.match(path.read_text("utf-8"))
    if not match:
        return {}
    out: dict[str, str] = {}
    key = None
    buffer: list[str] = []
    for line in match.group(1).split("\n"):
        header = re.match(r"^([a-zA-Z-]+):\s*(.*)$", line)
        if header and not line.startswith(" "):
            if key:
                out[key] = " ".join(buffer).strip()
            key = header.group(1)
            value = header.group(2).strip()
            buffer = [] if value in (">-", ">", "|", "|-", "") else [value]
        elif key:
            buffer.append(line.strip())
    if key:
        out[key] = " ".join(buffer).strip()
    return out


def check_manifest(problems: Problems) -> None:
    if not MANIFEST.exists():
        problems.wrong(f"{MANIFEST} is missing")
        return
    manifest = json.loads(MANIFEST.read_text("utf-8"))
    required = {
        "name": "aninda-studio",
        "version": "1.0.0",
        "license": "Apache-2.0 AND PolyForm-Noncommercial-1.0.0",
    }
    for key, value in required.items():
        if manifest.get(key) != value:
            problems.wrong(f"plugin.json {key} is {manifest.get(key)!r}, and should be {value!r}")
        else:
            problems.ok(f"plugin.json {key} is {value!r}")
    for key in ("displayName", "description", "author", "homepage", "repository", "keywords"):
        if not manifest.get(key):
            problems.wrong(f"plugin.json has no {key}")
    if not isinstance(manifest.get("keywords"), list) or len(manifest["keywords"]) < 5:
        problems.wrong("plugin.json needs a keywords list, so the plugin can be found")
    else:
        problems.ok(f"plugin.json has {len(manifest['keywords'])} keywords")


def check_commands(problems: Problems) -> None:
    for name in EXPECTED_COMMANDS:
        path = COMMANDS / f"{name}.md"
        if not path.exists():
            problems.wrong(f"commands/{name}.md is missing, so /aninda-studio:{name} will not exist")
            continue
        fields = front_matter(path)
        if not fields.get("description"):
            problems.wrong(f"commands/{name}.md has no description")
        if not fields.get("argument-hint"):
            problems.wrong(f"commands/{name}.md has no argument-hint")
        if fields.get("disable-model-invocation") != "true":
            problems.wrong(
                f"commands/{name}.md must set disable-model-invocation: true, so the command runs "
                "only when a person asks for it"
            )
        else:
            problems.ok(f"/aninda-studio:{name} is defined and is person-invoked only")

    extra = {p.stem for p in COMMANDS.glob("*.md")} - set(EXPECTED_COMMANDS)
    if extra:
        problems.wrong(f"commands/ holds files nobody expects: {', '.join(sorted(extra))}")


def check_skills(problems: Problems) -> None:
    for name in EXPECTED_SKILLS:
        skill_dir = SKILLS / name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            problems.wrong(f"skills/{name}/SKILL.md is missing")
            continue
        fields = front_matter(skill_md)
        if fields.get("name") != name:
            problems.wrong(f"skills/{name}/SKILL.md declares name {fields.get('name')!r}")
        description = fields.get("description", "")
        if len(description) < 200:
            problems.wrong(
                f"skills/{name}: the description is {len(description)} characters. It has to be "
                "dense with the phrases a person would actually type, or the skill will not be "
                "chosen"
            )
        else:
            problems.ok(f"skills/{name}: description is {len(description)} characters")

        # Each skill must send the other two jobs elsewhere, or all three compete.
        others = [other for other in EXPECTED_SKILLS if other != name]
        for other in others:
            if other not in description:
                problems.wrong(
                    f"skills/{name}: the description never names {other}, so nothing routes a "
                    f"{other}-shaped request away from it"
                )
        if all(other in description for other in others):
            problems.ok(f"skills/{name}: routes both other jobs away explicitly")

        for required in ("LICENSE.txt", "NOTICE"):
            if not (skill_dir / required).exists():
                problems.wrong(f"skills/{name}/{required} is missing")
        if (skill_dir / "LICENSE.txt").exists() and (skill_dir / "NOTICE").exists():
            problems.ok(f"skills/{name}: ships its own LICENSE.txt and NOTICE")

        # Anything the SKILL.md points at has to be there.
        body = skill_md.read_text("utf-8")
        for reference in sorted(set(re.findall(r"`((?:references|scripts|assets)/[^`\s]+)`", body))):
            # A wildcard or a brace expansion names a set, not one file.
            if any(character in reference for character in "*{}"):
                continue
            if not (skill_dir / reference).exists():
                problems.wrong(f"skills/{name}/SKILL.md points at {reference}, which is not there")

    for name in BRAND_REFERENCES:
        path = SKILLS / "aninda-brand" / "references" / f"{name}.md"
        if not path.exists():
            problems.wrong(f"skills/aninda-brand/references/{name}.md is missing")
    if all((SKILLS / "aninda-brand" / "references" / f"{n}.md").exists() for n in BRAND_REFERENCES):
        problems.ok(f"aninda-brand carries all {len(BRAND_REFERENCES)} reference files")

    extra = {p.name for p in SKILLS.iterdir() if p.is_dir()} - set(EXPECTED_SKILLS)
    if extra:
        problems.wrong(f"skills/ holds folders nobody expects: {', '.join(sorted(extra))}")


def check_bangla_agreement(problems: Problems) -> None:
    """The table a person reads and the JSON a script reads must say the same thing."""
    json_path = SKILLS / "aninda-brand" / "assets" / "bangla-verified.json"
    markdown_path = SKILLS / "aninda-brand" / "references" / "bangla.md"
    if not json_path.exists() or not markdown_path.exists():
        problems.wrong("the verified Bangla data or its reference document is missing")
        return
    from_json = {entry["id"]: entry["bangla"] for entry in json.loads(json_path.read_text("utf-8"))["strings"]}
    from_markdown = {}
    for line in markdown_path.read_text("utf-8").split("\n"):
        row = re.match(r"^\|\s*([a-z]+-\d+)\s*\|\s*([^|]+?)\s*\|", line)
        if row:
            from_markdown[row.group(1)] = row.group(2).strip()
    if from_json == from_markdown:
        problems.ok(
            f"the {len(from_json)} verified Bangla strings agree between bangla.md and "
            "bangla-verified.json"
        )
        return
    for key in sorted(set(from_json) | set(from_markdown)):
        if from_json.get(key) != from_markdown.get(key):
            problems.wrong(
                f"verified Bangla {key} differs: bangla-verified.json has "
                f"{from_json.get(key)!r} and bangla.md has {from_markdown.get(key)!r}"
            )


def check_bundles(problems: Problems) -> None:
    import zipfile

    for name in EXPECTED_SKILLS:
        bundle = DIST / f"{name}.skill"
        if not bundle.exists():
            problems.wrong(f"dist/{name}.skill is missing. Run scripts/build_skills.py")
            continue
        with zipfile.ZipFile(bundle) as archive:
            names = archive.namelist()
            if "SKILL.md" not in names:
                problems.wrong(f"dist/{name}.skill has no SKILL.md at the archive root")
                continue
            stamps = {info.date_time for info in archive.infolist()}
            if stamps != {(2026, 1, 1, 0, 0, 0)}:
                problems.wrong(
                    f"dist/{name}.skill has entries with more than one timestamp: {sorted(stamps)}. "
                    "That makes the archive unreproducible"
                )
                continue
            bad = [n for n in names if ".DS_Store" in n or "__pycache__" in n or n.endswith(".pyc")]
            if bad:
                problems.wrong(f"dist/{name}.skill carries files that should be excluded: {bad}")
                continue
            problems.ok(f"dist/{name}.skill: SKILL.md at the root, {len(names)} entries, one timestamp")


def main() -> int:
    problems = Problems()
    check_manifest(problems)
    check_commands(problems)
    check_skills(problems)
    check_bangla_agreement(problems)
    check_bundles(problems)

    lines = ["", f"PASSED ({len(problems.passed)})", "-" * 72]
    for item in problems.passed:
        lines.append(f"  {item}")
    lines.append("")
    lines.append(f"WRONG ({len(problems.items)})")
    lines.append("-" * 72)
    if not problems.items:
        lines.append("  Nothing.")
    for item in problems.items:
        lines.append(f"  {item}")
    lines.append("")
    sys.stdout.write("\n".join(lines) + "\n")
    return 1 if problems.items else 0


if __name__ == "__main__":
    sys.exit(main())
