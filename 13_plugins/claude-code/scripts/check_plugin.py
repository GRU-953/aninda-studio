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
    # The version is READ from VERSION, not typed here. It used to be the literal
    # "1.0.0", so this guard obstructed the release it exists to protect: bumping
    # VERSION and both manifests to 1.1.0 failed with "plugin.json version is
    # '1.1.0', and should be '1.0.0'". Everything else in the system — guidebook,
    # packages, site, both READMEs — already follows VERSION; only the plugin did
    # not, and the one check that could have noticed was the one asserting the
    # wrong thing.
    version_file = REPO_ROOT / "VERSION"
    if not version_file.exists():
        problems.wrong("VERSION is missing, so the plugin's version has nothing "
                       "to be checked against")
        return
    version = version_file.read_text(encoding="utf-8").strip()
    required = {
        "name": "aninda-studio",
        "version": version,
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
    """The table a person reads and the JSON a script reads must say the same thing —
    and BOTH must match the document they cite as their source.

    Comparing only the plugin's two copies to each other left four copies of these
    31 pairs with one comparison between two of them. ms-2's English gloss read
    "That file is too big. The limit is 10 MB." while 06_type/review_bangla.py,
    which BANGLA-STANDARD.md quotes, says "That file is too large. The limit is
    10 MB." The Bangla was identical in all four; only the gloss diverged — and the
    gloss is the only way an agent finds the right string, with the plugin's rule
    being to use a listed string or leave the English alone.
    """
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
    # The source: the review sheet's STRINGS table, which BANGLA-STANDARD.md
    # quotes string by string. Read by parsing rather than importing, so this
    # check does not depend on that script running.
    source_path = REPO_ROOT / "06_type" / "review_bangla.py"
    source: dict[str, tuple[str, str]] = {}
    if source_path.exists():
        text = source_path.read_text("utf-8")
        for match in re.finditer(
                r'\(\s*"([a-z]+-\d+)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*,\s*\n?\s*"((?:[^"\\]|\\.)*)"',
                text):
            source[match.group(1)] = (match.group(2), match.group(3))
    else:
        problems.wrong("06_type/review_bangla.py is missing, so the plugin's verified "
                       "strings cannot be checked against the document they cite")

    glosses = {entry["id"]: entry["english"]
               for entry in json.loads(json_path.read_text("utf-8"))["strings"]}

    # The gb-* namespace is EXCLUDED, and this is a real defect rather than a
    # convenience: the review sheet uses gb-1 for a display row carrying three
    # chapter titles at once ("Welcome · The name · The mark"), and the plugin uses
    # gb-1 for the single title "Welcome". Two documents, one id namespace, two
    # meanings. The guidebook now keys its chapters to chapter.<slug> in the
    # register; the plugin still uses gb-*, and until it does the same these ids
    # cannot be compared. Recorded in 01_research/OPEN-FINDINGS.md.
    GROUPED = {key for key in source if key.startswith("gb-")}

    drifted = []
    for key, (english, bangla) in sorted(source.items()):
        if key in GROUPED:
            continue
        if key in from_json and from_json[key] != bangla:
            drifted.append(f"{key} Bangla: the plugin has {from_json[key]!r}, "
                           f"06_type/review_bangla.py has {bangla!r}")
    for item in drifted:
        problems.wrong(item)

    # The two files ask different questions of the same string, and for two ids
    # the right answers differ. The review sheet's English column is "the string
    # this row is about", shown to a reviewer beside its Bangla; the plugin's
    # gloss is "what this Bangla means", used by an agent to find the right
    # string. For the wordmark those are not the same thing:
    #
    #   wm-1  the wordmark is DRAWN lowercase, so the sheet shows "aninda studio";
    #         the name it means is "Aninda Studio", which is the useful gloss.
    #   wm-2  the sheet labels the row "Aninda Studio (short form)" to say which
    #         wordmark is under review; অনিন্দ্য on its own means "Aninda".
    #
    # Both are right, so both stay, and the reconciliation is written here rather
    # than left as an unexplained divergence a future reader would try to "fix".
    # Settled by the owner on 19 August 2026.
    #
    # The other two in this group were real and are gone: ms-2 read "too big"
    # against a source saying "too large", and th-3 was "High contrast" here and
    # "More contrast" in the sheet and on the website's own theme button — one
    # English for one string, and BANGLA-STANDARD.md reviews it as "High contrast".
    RECONCILED = {"wm-1", "wm-2"}

    gloss_drift = [
        f"{key}: plugin gloss {glosses[key]!r}, 06_type/review_bangla.py {english!r}"
        for key, (english, _) in sorted(source.items())
        if key not in GROUPED and key not in RECONCILED
        and key in glosses and glosses[key] != english
    ]
    for item in gloss_drift:
        problems.wrong(item)
    if not gloss_drift:
        problems.ok(f"every English gloss matches 06_type/review_bangla.py, except "
                    f"{len(RECONCILED)} recorded as deliberately different and why")

    if from_json == from_markdown and not drifted and not gloss_drift:
        problems.ok(
            f"the {len(from_json)} verified Bangla strings agree between bangla.md, "
            f"bangla-verified.json and the {len(source)} in 06_type/review_bangla.py, "
            f"in Bangla and in English"
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
    # The two licence texts the aninda-repo skill tells an agent to copy. They were
    # absent entirely until 19 August 2026: the skill's file table promised the full
    # PolyForm and OFL texts and shipped neither, so an agent following it had to
    # reproduce a licence from memory or fetch one. Byte-compared here, because a
    # licence that has drifted from its source is worse than one that is missing —
    # it looks authoritative.
    "aninda-repo/LICENSE.txt": "LICENSE",
    "aninda-repo/templates/LICENSE-DOCS.md": "LICENSE-DOCS.md",
}


def bundled_pairs() -> dict[str, str]:
    """The single list of (copy in the skill, source in the repository).

    Split out of check_bundled_copies so `--sync` copies exactly what the check
    compares. Before this existed the check reported drift and a person fixed it
    by hand, which is how the bundled Bangla subset lost ten codepoints: the
    report was right, and the hand that acted on it missed a file.
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
    return pairs


def sync_bundled_copies() -> int:
    """Copy every source over its bundled copy. Prints what it changed."""
    changed = []
    for relative, origin in sorted(bundled_pairs().items()):
        copy, source = SKILLS / relative, REPO_ROOT / origin
        if not source.exists():
            print(f"  ! {origin} is missing — cannot sync skills/{relative}",
                  file=sys.stderr)
            return 1
        data = source.read_bytes()
        if not copy.exists() or copy.read_bytes() != data:
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_bytes(data)
            changed.append(f"skills/{relative}  <-  {origin}")
    if changed:
        print(f"Synced {len(changed)} bundled file(s):")
        for line in changed:
            print(f"  {line}")
    else:
        print("Every bundled file already matched its source. Nothing copied.")
    return 0


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
    pairs = bundled_pairs()

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


def check_ofl_template(problems: Problems) -> None:
    """The OFL template's licence body must match the OFL this repository ships.

    It cannot be a byte copy: the shipped file's first line names IBM Corp and the
    Plex Reserved Font Name, which would be wrong to hand a stranger as a template.
    So the header is SIL's placeholder form and everything from the rule onwards is
    compared byte for byte.
    """
    template = SKILLS / "aninda-repo" / "templates" / "OFL.txt"
    shipped = REPO_ROOT / "08_components" / "fonts" / "anindamono-OFL.txt"
    if not template.exists() or not shipped.exists():
        problems.wrong("the OFL template or the shipped OFL is missing, so the "
                       "template cannot be checked against a real licence text")
        return
    marker = "-" * 59
    a = template.read_text(encoding="utf-8")
    b = shipped.read_text(encoding="utf-8")
    if marker not in a or marker not in b:
        problems.wrong("could not find the OFL rule line in the template or the "
                       "shipped licence, so the comparison did not really run")
        return
    if a[a.index(marker):] != b[b.index(marker):]:
        problems.wrong("aninda-repo/templates/OFL.txt's licence body differs from "
                       "08_components/fonts/anindamono-OFL.txt")
        return
    if "<Reserved Font Name>" not in a:
        problems.wrong("the OFL template has no placeholder header — it would hand a "
                       "stranger somebody else's copyright line")
        return
    problems.ok("aninda-repo/templates/OFL.txt carries SIL's placeholder header and "
                "a licence body byte-identical to the OFL this repository ships")


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
    # Three versions, all compared: the plugin entry, plugin.json, and
    # marketplace.json's own metadata.version — which was compared to nothing and
    # could drift on its own with every check green.
    root_version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    versions = {
        "VERSION": root_version,
        "plugin.json": manifest.get("version"),
        "marketplace.json plugins[].version": entry.get("version"),
        "marketplace.json metadata.version": listing.get("metadata", {}).get("version"),
    }
    if len(set(versions.values())) != 1:
        problems.wrong("the version is not the same in every place that states it: "
                       + ", ".join(f"{k} says {v!r}" for k, v in versions.items()))
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
        f"{entry['source']}, the README shows both install commands, and all "
        f"{len(versions)} places that state a version agree with VERSION"
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


def check_colour_reference(problems: Problems) -> None:
    """references/colour.md's hex table must match the token documents.

    It is hand-maintained markdown, and nothing compared it to anything. It was
    headed "The seventeen roles" over eighteen rows of which seven are surfaces,
    it was missing color.accent.hover entirely, and this is the document the
    skill routes every colour question to. A reference table nobody checks is a
    second source of truth, which is the failure mode the whole token pipeline
    exists to prevent.

    Every value is compared in both directions: no row may disagree with the
    tokens, and no token may be absent from the table.
    """
    doc = SKILLS / "aninda-brand" / "references" / "colour.md"
    if not doc.exists():
        problems.wrong(f"{doc.name} is missing")
        return
    themes = ["light", "dark", "hc-light", "hc-dark"]
    prim_path = REPO_ROOT / "07_tokens" / "build" / "primitive.tokens.json"
    if not prim_path.exists():
        problems.wrong("07_tokens/build is missing, so colour.md cannot be checked")
        return
    prim = json.loads(prim_path.read_text())

    def resolve(value):
        if isinstance(value, str) and value.startswith("{"):
            node = prim
            for part in value.strip("{}").split("."):
                node = node[part]
            return node["$value"]["hex"]
        return value["hex"]

    expected: dict[str, dict[str, str]] = {}
    for theme in themes:
        colour = json.loads(
            (REPO_ROOT / "07_tokens" / "build" / f"semantic.{theme}.tokens.json").read_text()
        )["color"]
        for group in ("surface", "ink", "line", "accent", "focus", "status"):
            for key, token in colour.get(group, {}).items():
                if key.startswith("$"):
                    continue
                expected.setdefault(f"color.{group}.{key}", {})[theme] = resolve(token["$value"])

    found: dict[str, list[str]] = {}
    for line in doc.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\|\s*`(color\.[a-z.]+)`\s*\|(.+)\|\s*$", line)
        if match:
            found[match.group(1)] = [cell.strip() for cell in match.group(2).split("|")]

    bad = []
    for role in sorted(set(expected) | set(found)):
        if role not in found:
            bad.append(f"colour.md has no row for {role}")
            continue
        if role not in expected:
            bad.append(f"colour.md has a row for {role}, which the tokens do not define")
            continue
        want = [expected[role][t] for t in themes]
        if [c.upper() for c in found[role]] != [w.upper() for w in want]:
            bad.append(f"colour.md {role} reads {found[role]}, tokens say {want}")
    for item in bad:
        problems.wrong(item)
    if not bad:
        problems.ok(f"references/colour.md's table matches the tokens for all "
                    f"{len(expected)} colour values across {len(themes)} themes")


def check_bangla_document(problems: Problems) -> None:
    """06_type/BANGLA-STRINGS.md must agree with 06_type/bangla-strings.json.

    The document is a hand-written table of the same 94 approved strings the
    register holds, and nothing compared them. Two rows had already drifted —
    both of them rows whose English was corrected for a false claim, where the
    document kept the wrong version, which is the worst direction for a drift to
    run in a file a reviewer reads to approve wording.

    Basis notes are compared too. The basis is the citation behind each string,
    and a citation that no longer matches its string is worse than none.
    """
    doc = REPO_ROOT / "06_type" / "BANGLA-STRINGS.md"
    reg = REPO_ROOT / "06_type" / "bangla-strings.json"
    if not doc.exists() or not reg.exists():
        problems.wrong(f"{doc.name} or {reg.name} is missing, so the register "
                       f"cannot be checked against the document that publishes it")
        return
    register = json.loads(reg.read_text(encoding="utf-8"))
    rows = {}
    for line in doc.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*`([a-z0-9.\-]+)`\s*\|(.*?)\|(.*?)\|(.*)\|\s*$", line)
        if match:
            rows[match.group(1)] = tuple(g.strip() for g in match.groups()[1:])

    bad = []
    for key in sorted(set(register) | set(rows)):
        if key not in rows:
            bad.append(f"BANGLA-STRINGS.md has no row for {key}")
        elif key not in register:
            bad.append(f"BANGLA-STRINGS.md has a row for {key}, which is not in the register")
        else:
            entry = register[key]
            want = (entry["en"], entry["bn"], entry["basis"])
            for field, got, expected in zip(("English", "Bangla", "basis"), rows[key], want):
                if got != expected:
                    # Show the text AROUND the first difference, not the first 48
                    # characters of each. A basis note runs to several hundred
                    # characters and these two strings agreed for the first 200 of
                    # them, so the report printed two identical-looking excerpts
                    # and named no difference at all.
                    at = next((i for i, (a, b) in enumerate(zip(got, expected)) if a != b),
                              min(len(got), len(expected)))
                    bad.append(f"{key} {field}: differs at character {at} — "
                               f"document has ...{got[at:at + 44]!r}, "
                               f"register has ...{expected[at:at + 44]!r}")
    for item in bad:
        problems.wrong(item)
    if not bad:
        problems.ok(f"BANGLA-STRINGS.md matches the register for all "
                    f"{len(register)} approved strings, English, Bangla and basis")


def main() -> int:
    if "--sync" in sys.argv[1:]:
        return sync_bundled_copies()

    problems = Problems()
    check_manifest(problems)
    check_commands(problems)
    check_skills(problems)
    check_bangla_agreement(problems)
    check_marketplace(problems)
    check_bundled_copies(problems)
    check_bangla_font_coverage(problems)
    check_ofl_template(problems)
    check_rule_count(problems)
    check_token_names(problems)
    check_colour_reference(problems)
    check_bangla_document(problems)
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
