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
REPO_ROOT = PLUGIN_ROOT.parent.parent
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"

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


# Every file the skill bundles that also exists in the repository, and where it
# comes from. The skill is meant to work standalone once installed, so it carries
# copies — but while both live in one tree the copy must be the source, byte for
# byte.
BUNDLED_FROM_REPO = {
    "aninda-brand/assets/css/tokens.css": "07_tokens/css/tokens.css",
    "aninda-brand/assets/marks/manifest.json": "04_mark/manifest.json",
}


def check_bundled_copies(problems: Problems) -> None:
    """Nothing copied into the skill may have drifted from the file it came from.

    Nothing syncs these, and two of them have now gone stale in ways that mattered.

    First: the bundled primitive.tokens.json still recorded IBM Plex Mono's
    Reserved Font Name as "IBM Plex" after the source had been corrected to the
    exact string "Plex", so the plugin shipped a licence-relevant statement that the
    repository had already fixed. The token documents and the marks were switched to
    pattern matching then, "so a new one cannot be missed" — and the FONTS were left
    as one hand-typed entry for anindamono-subset.woff2. Two of the three were
    therefore outside every check in the repository.

    Second, and that is what it cost: the bundled Noto Serif Bengali subset drifted
    to 450 glyphs against the source's 515, losing ten codepoints including ঠ and ২.
    ঠ is in কণ্ঠস্বর, one of the approved strings in this skill's own
    bangla-verified.json, and ২ is in the Bangla Academy edition year the same file
    cites as its authority. Both rendered as tofu boxes from the skill's own font,
    on green CI, because the guard for exactly this hand-listed one file of three.

    So the fonts are now matched by pattern too. Any file in the skill's fonts
    folder that also exists in 08_components/fonts is compared, and — because a
    pattern that only looks at what the copy holds could be satisfied by deleting
    the copy — every subset the repository ships must also be present.
    """
    pairs = dict(BUNDLED_FROM_REPO)
    for source in sorted((REPO_ROOT / "07_tokens" / "build").glob("*.json")):
        pairs[f"aninda-brand/assets/tokens/{source.name}"] = f"07_tokens/build/{source.name}"
    for source in sorted((REPO_ROOT / "04_mark" / "svg").glob("*.svg")):
        copy = SKILLS / "aninda-brand" / "assets" / "marks" / source.name
        if copy.exists():
            pairs[f"aninda-brand/assets/marks/{source.name}"] = f"04_mark/svg/{source.name}"
    # Every subset font, from the source side, so a MISSING copy is a failure and
    # not merely an absence. This is the direction the hand-typed entry got wrong.
    for source in sorted((REPO_ROOT / "08_components" / "fonts").glob("*.woff2")):
        pairs[f"aninda-brand/assets/fonts/{source.name}"] = \
            f"08_components/fonts/{source.name}"

    stale = []
    for relative, origin in sorted(pairs.items()):
        copy, source = SKILLS / relative, REPO_ROOT / origin
        if not source.exists():
            problems.wrong(f"{origin} is missing, so skills/{relative} cannot be checked")
            continue
        if not copy.exists():
            problems.wrong(f"skills/{relative} is missing, and {origin} is there to copy")
            continue
        if copy.read_bytes() != source.read_bytes():
            stale.append(f"skills/{relative} has drifted from {origin}")
    for item in stale:
        problems.wrong(item)
    if not stale:
        problems.ok(f"{len(pairs)} bundled files are byte-identical to their sources "
                    "in the repository")


def check_bangla_font_coverage(problems: Problems) -> None:
    """The bundled Bangla font must be able to draw the Bangla this skill ships.

    A byte-for-byte drift check is not enough on its own. The subsets are built
    from the union of what the 30 component cards contain, so a Bangla character
    that appears only in the plugin's own data was never in the font — and the
    plugin is the surface that carries this system's Bangla to other people. When
    this guard was written it found ৫, the Bengali five in the Bangla Academy
    reprint year the skill cites as its authority, and ঝ in the reference tables.
    08_components/build.py now folds these two files into the charset, so the fix
    is at the subsetter and this is the check that says it held.

    Measured from the font's cmap, not asserted.
    """
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        problems.wrong("fontTools is not importable, so the bundled Bangla font "
                       "cannot be checked against the Bangla this skill ships")
        return
    font_path = (SKILLS / "aninda-brand" / "assets" / "fonts"
                 / "notoserifbengali-subset.woff2")
    if not font_path.exists():
        problems.wrong(f"{font_path.relative_to(SKILLS)} is missing")
        return
    covered = set(TTFont(str(font_path)).getBestCmap())
    sources = [SKILLS / "aninda-brand" / "assets" / "bangla-verified.json",
               SKILLS / "aninda-brand" / "references" / "bangla.md"]
    missing: dict[str, set[str]] = {}
    for source in sources:
        if not source.exists():
            problems.wrong(f"{source.relative_to(SKILLS)} is missing")
            continue
        text = source.read_text(encoding="utf-8")
        gap = {ch for ch in text if "\u0980" <= ch <= "\u09ff" and ord(ch) not in covered}
        if gap:
            missing[source.relative_to(SKILLS).as_posix()] = gap
    if missing:
        for name, gap in sorted(missing.items()):
            problems.wrong(
                f"{name} holds Bangla the bundled subset cannot draw: "
                f"{''.join(sorted(gap))} — those render as tofu boxes. Add these "
                f"files to the charset union in 08_components/build.py and rebuild."
            )
        return
    problems.ok(f"the bundled Bangla subset covers every Bangla character in "
                f"{len(sources)} shipped data file(s), {len(covered)} codepoints")


SPELLED = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
           8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


def check_rule_count(problems: Problems) -> None:
    """SKILL.md's heading must count the rules under it.

    The heading and the intro line both spell the number out — "The seven rules",
    "These seven cover most of what goes wrong" — and the list under them is the
    plugin's whole set of hard rules. Adding one meant three places to change and
    only two of them were obvious, so this counts the list and compares.

    It exists because a rule was missing from that list: nothing in the plugin told
    an agent to write `lang="bn"`, without which the entire Bangla half of the
    stylesheet never matches.
    """
    path = SKILLS / "aninda-brand" / "SKILL.md"
    if not path.exists():
        problems.wrong("aninda-brand/SKILL.md is missing")
        return
    text = path.read_text("utf-8")
    section = re.search(r"^## The (\w+) rules\s*\n(.*?)(?=^## |\Z)",
                        text, re.M | re.S)
    if not section:
        problems.wrong("aninda-brand/SKILL.md has no '## The <number> rules' section")
        return
    claimed, body = section.group(1).lower(), section.group(2)
    counted = len(re.findall(r"^\d+\. \*\*", body, re.M))
    want = SPELLED.get(counted)
    if want is None:
        problems.wrong(f"aninda-brand/SKILL.md lists {counted} rules and this check "
                       f"has no word for that number")
        return
    intro = re.search(r"^These (\w+) cover", body, re.M)
    if claimed != want:
        problems.wrong(f"aninda-brand/SKILL.md's heading says '{claimed}' rules and "
                       f"{counted} are listed under it")
    elif not intro or intro.group(1).lower() != want:
        problems.wrong(f"aninda-brand/SKILL.md lists {counted} rules but the line "
                       f"under the heading says "
                       f"'{intro.group(1) if intro else 'nothing'}'")
    else:
        problems.ok(f"SKILL.md's heading and intro both say {want}, and {counted} "
                    f"rules are listed")


def check_marketplace(problems: Problems) -> None:
    """A plugin nobody can install is not shipped.

    Claude Code installs a plugin from a marketplace, which is a
    `.claude-plugin/marketplace.json` at the root of a git repository. Until
    18 August 2026 this repository had none, and no document anywhere said how to
    get the plugin into Claude Code by any other route — while the plugin's own
    README told the reader to type `/aninda-studio:` and pick a command. Everything
    else about it was finished and machine-checked, so the one missing piece was the
    only thing between all that work and anybody running it.
    """
    if not MARKETPLACE.exists():
        problems.wrong(
            f"{MARKETPLACE.relative_to(REPO_ROOT)} is missing, so there is no way to "
            "install this plugin. Claude Code installs from a marketplace file at the "
            "root of a git repository."
        )
        return
    listing = json.loads(MARKETPLACE.read_text("utf-8"))
    manifest = json.loads(MANIFEST.read_text("utf-8")) if MANIFEST.exists() else {}
    entries = listing.get("plugins")
    if not isinstance(entries, list) or not entries:
        problems.wrong("marketplace.json lists no plugins")
        return
    mine = [entry for entry in entries if entry.get("name") == manifest.get("name")]
    if not mine:
        problems.wrong(
            f"marketplace.json lists {[entry.get('name') for entry in entries]} and none "
            f"of them is {manifest.get('name')!r}, the name in plugin.json. The install "
            "command names the plugin, so the two have to agree."
        )
        return
    entry = mine[0]
    source = (MARKETPLACE.parent.parent / entry.get("source", "")).resolve()
    if source != PLUGIN_ROOT:
        problems.wrong(
            f"marketplace.json points {entry['name']} at {entry.get('source')!r}, which "
            f"resolves to {source}, not {PLUGIN_ROOT}"
        )
        return
    if entry.get("version") != manifest.get("version"):
        problems.wrong(
            f"marketplace.json says version {entry.get('version')!r} and plugin.json "
            f"says {manifest.get('version')!r}"
        )
        return
    # The README has to say how to install it. A marketplace file nobody is told
    # about is the same failure one step further along.
    readme = (PLUGIN_ROOT / "README.md").read_text("utf-8")
    for needed in ("/plugin marketplace add", "/plugin install"):
        if needed not in readme:
            problems.wrong(f"13_plugins/claude-code/README.md never shows `{needed}`, so "
                           "a reader is not told how to install the plugin")
            return
    problems.ok(
        f"marketplace.json lists {entry['name']} v{entry['version']} at "
        f"{entry['source']}, and the README shows both install commands"
    )


def check_token_names(problems: Problems) -> None:
    """Every `var(--as-...)` the plugin prints must be a property tokens.css defines.

    Round 1 of the convergence review found `var(--as-accent-default)` in the first
    of SKILL.md's numbered rules and again in references/colour.md. It is not a
    property:
    07_tokens/emit_css.py drops a trailing `default` segment, so the property is
    `--as-accent`. In Chromium the undefined name resolved to the empty string and
    the text fell back to inherited black, which looks plausible and is wrong. The
    DTCG role name does keep `.default`, which is how the two forms got confused.
    Nothing measured the instructions against the stylesheet, so this does.

    IT USED TO READ ONLY `*.md`. That was the whole defect the second time round.
    The prose was corrected and the guard was scoped to markdown, so it saw 2 of
    the 8 occurrences in the skills and printed "all name one of the 63 properties"
    as though it had swept everything — while
    aninda-review/scripts/check.py built `var(--as-accent-default)` at runtime and
    handed it to a user as the recommended fix. The executable that gives the
    advice was outside the check that existed for that advice.

    So the sweep now reads every text file in the skills: markdown, Python, JSON,
    CSS, HTML. A `var(--as-...)` assembled from parts at runtime still escapes a
    static sweep — check.py's own recommendation is now measured against tokens.css
    by check.py itself, which is where that has to be caught.
    """
    stylesheet = SKILLS / "aninda-brand" / "assets" / "css" / "tokens.css"
    if not stylesheet.exists():
        problems.wrong(f"{stylesheet} is missing, so no token name can be checked")
        return
    defined = set(re.findall(r"(--as-[a-z0-9-]+)\s*:", stylesheet.read_text("utf-8")))
    if not defined:
        problems.wrong(f"{stylesheet} defines no custom properties")
        return
    used = 0
    scanned = 0
    undefined: list[str] = []
    suffixes = {".md", ".py", ".json", ".css", ".html", ".txt", ".ts", ".js", ".yml"}
    for path in sorted(SKILLS.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if "__pycache__" in path.parts:
            continue
        # tokens.css is the definition, not a use of one.
        if path == stylesheet:
            continue
        text = path.read_text("utf-8", errors="replace")
        scanned += 1
        for match in re.finditer(r"var\(\s*(--as-[a-z0-9-]+)", text):
            used += 1
            if match.group(1) not in defined:
                line = text.count("\n", 0, match.start()) + 1
                undefined.append(f"{path.relative_to(PLUGIN_ROOT)}:{line} names {match.group(1)}")
    for item in undefined:
        problems.wrong(f"a token that does not exist: {item}")
    if not undefined:
        problems.ok(
            f"{used} var(--as-...) references across {scanned} text files in the "
            f"skills all name one of the {len(defined)} properties tokens.css defines"
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
    check_marketplace(problems)
    check_bundled_copies(problems)
    check_bangla_font_coverage(problems)
    check_rule_count(problems)
    check_token_names(problems)
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
