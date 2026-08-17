---
description: Check something that already exists against the Aninda Studio system and WCAG 2.2 AA — contrast, target size, focus, forced colours, tokens, English wording and Bangla.
argument-hint: "[path to a file or folder] [--aaa] [--json report.json]"
disable-model-invocation: true
---

<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->

Check something that already exists.

Use the `aninda-review` skill. It ships `scripts/check.py`, which reports both
what it checked and what it cannot see. Pass on the blind spots as well as the
failures: a check that hides its own limits is worse than no check.

What the user asked for: `$ARGUMENTS`

Do this:

1. Read `skills/aninda-review/SKILL.md` and follow it.
2. Run `scripts/check.py` over the path given. If no path was given, ask which
   one rather than guessing.
3. Report failures first, each with the measured number, the threshold it missed
   and the WCAG success criterion by number and name.
4. Then report the blind spots the script names, so the user knows what still
   needs a human eye.
5. Offer to fix what you found. Do not fix it without asking.

If the user wants something new made rather than checked, use the
`aninda-brand` skill. If they want a whole repository set up or upgraded, use
`aninda-repo`.
