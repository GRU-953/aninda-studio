<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# The Aninda Studio Claude Code plugin

Three skills, four commands, and one rule behind all of it: a script that refuses
teaches the rule, and a document that warns does not.

**Written documentation licence:** PolyForm Noncommercial 1.0.0.
**Code, tokens and scripts licence:** Apache-2.0.
Combined SPDX expression: `Apache-2.0 AND PolyForm-Noncommercial-1.0.0`.
See `NOTICE` for the full split, including the fonts and the identity.

---

## The three skills, split by unit of work

They are split this way so that choosing between them is reliable. Each one names
the other two and sends their work to them, rather than competing for it.

| Skill | Unit of work | Reach for it when |
| --- | --- | --- |
| `aninda-brand` | **one thing** | Making a mark, an icon, a page, a component, a piece of copy. It holds every rule; the other two point back at it. |
| `aninda-repo` | **a whole repository** | Setting up or upgrading licences, `NOTICE`, a bilingual README pair, SPDX headers, a CI brand check. |
| `aninda-review` | **something that already exists** | Checking a page, a stylesheet or a repository against the system and WCAG 2.2 AA. |

`aninda-brand` carries ten reference files — colour, typography, layout, logo,
icons, motion, voice, Bangla, licence, naming — plus the token files, the
stylesheet, the marks and the fonts. Its `SKILL.md` says which to read for which
job, so a small question does not cost ten files of context.

---

## The four commands

Every one has `disable-model-invocation: true`, so it runs when a person asks and
not otherwise.

| Command | What it does |
| --- | --- |
| `/aninda-studio:asset` | Make one asset. Refuses an impermissible combination. |
| `/aninda-studio:design` | Design or build something new to the system. |
| `/aninda-studio:check` | Check something that already exists. |
| `/aninda-studio:init` | Set up or upgrade a whole repository. |

---

## The two scripts that do the real work

### `aninda-brand/scripts/asset.py` — it refuses

```
python skills/aninda-brand/scripts/asset.py list
python skills/aninda-brand/scripts/asset.py mark --weight heavy --size 20 --on surface-base --theme dark
python skills/aninda-brand/scripts/asset.py icon --appstore
python skills/aninda-brand/scripts/asset.py contrast --fg accent-default --bg surface-dim --theme light
```

It exits `2` and writes nothing when the combination breaks a rule. Every refusal
names the rule, the measured number, and the nearest thing that would have been
allowed. Seven refusals are implemented:

1. The mark below its 16 px floor.
2. The regular weight below 24 px, where its stroke thins away.
3. The mark in a colour that is not one of the five it may take.
4. The mark with a shadow.
5. The mark at a non-square aspect ratio.
6. A colour on a ground it was never measured against, or on something that is
   not a ground at all.
7. The App Store master with a radius, or at any size other than 1024 px.

**One honest note.** Against the token files shipped here, every one of the
17 × 7 × 4 role-and-ground pairings passes, so refusal 6 cannot fire on a bad
measurement today. That is the proof the token set is sound, not proof the check
works. It fires today on a ground that is not a surface, and it will fire on a
measurement if the skill is pointed at a different token set.

### `aninda-review/scripts/check.py` — it names its own blind spots

```
python skills/aninda-review/scripts/check.py <path>
python skills/aninda-review/scripts/check.py <path> --aaa --json report.json
```

Exit `0` nothing failed, `1` something failed, `3` not equipped to check what it
was given. **Treat `3` as a failure in continuous integration**: it means the
check did not run, and a check that did not run must never read as a pass.

It ends every run with what it cannot see — nine items, from "anything that needs
a browser" to "whether the English is actually clear". Those are part of the
result. Read them out.

---

## Building the `.skill` bundles

```
python scripts/build_skills.py --prove
```

A `.skill` bundle is a plain zip with `SKILL.md` at the archive root. `--prove`
builds every bundle twice into two different temporary folders and asserts the
SHA-256s are identical, then writes the proven build into `dist/`.

Three things make that hold, and each one is a bug waiting to happen if it is
dropped:

1. The file list comes from `sorted()`, so the walk order never depends on the
   filesystem.
2. Every entry goes in through `zipfile.ZipInfo(name, date_time=(2026,1,1,0,0,0))`
   with an explicit `external_attr`. `zf.write(path)` is never used, because it
   copies the file's modification time into the archive and that changes on every
   build.
3. `.DS_Store`, `__pycache__` and `*.pyc` are excluded, because macOS writes the
   first by looking at a folder and Python writes the others by importing.

The `aninda-review` bundle also gets a generated `data/system.json`, derived at
bundle time from the `aninda-brand` skill's own token files. Installed as a
plugin, the checker reads those tokens directly and ignores the copy, so there is
one source of truth and the copy cannot drift.

---

## Checking the plugin itself

```
python scripts/check_plugin.py
```

It checks the things that would otherwise fail quietly: a command with no
`argument-hint`, a skill whose description is too thin to be chosen, a skill that
does not route the other two jobs away, a `SKILL.md` pointing at a file that is
not there, a bundle with more than one timestamp in it, and the verified Bangla
table disagreeing with the JSON the scripts read.

---

## For a non-technical reader: how to use this

1. Open your terminal.
2. Type `cd` followed by a space, then drag this folder onto the window, then
   press Return.
3. Type `../../.venv/bin/python skills/aninda-brand/scripts/asset.py list` and
   press Return. That prints everything the asset script can make, and nothing is
   changed.
4. To make something, copy one of the example lines it printed and change the
   numbers.
5. If it answers with `REFUSED`, read the three lines under it. The last one,
   `Instead`, tells you exactly what to change.

Inside Claude Code, you do not need any of that. Type `/aninda-studio:` and pick
one of the four commands.

---

## What needs the owner

Two things in the system's own files disagree, and a script cannot settle a
disagreement between two sources of truth:

- **Clear space around the mark.** `04_mark/manifest.json` says half the mark's
  own height on all four sides. The marks card in `08_components` says one stroke
  width. `asset.py` follows the manifest and says so in its output every time,
  but the losing statement still needs correcting at its source.
- **Bangla beyond the verified list.** The 30 component cards contain Bangla
  prose that is not among the 31 verified strings. `check.py` reports each one as
  a note rather than a failure, because it cannot tell you whether the Bangla is
  wrong — only that it has not been checked against the Bangla Academy
  dictionary.

---

## Contact

`aninda.sh15@gmail.com`
Source: `https://github.com/GRU-953/aninda-studio`
Site: `https://anindastudio.com`
