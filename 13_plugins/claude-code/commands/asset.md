---
description: Make one Aninda Studio asset — a mark, an icon, a wordmark, a tile or a colour swatch — with the rules enforced rather than described.
argument-hint: "[mark|icon|wordmark|tile|swatch] [--size 64] [--on surface-base] [--theme light] [--out path.svg]"
disable-model-invocation: true
---

<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->

Make exactly one asset from the Aninda Studio system.

Use the `aninda-brand` skill. It holds every rule and it ships
`scripts/asset.py`, which refuses an impermissible combination instead of
warning about it. A refusal is the answer, not a failure: pass on the refusal
message word for word, because it names the rule and the number it broke.

What the user asked for: `$ARGUMENTS`

Do this:

1. Read `skills/aninda-brand/SKILL.md` and follow it.
2. If the request is missing something the script needs, ask one question with
   the options laid out, rather than guessing.
3. Run `scripts/asset.py` with the arguments the request implies.
4. If it refuses, show the user the refusal in full and offer the nearest
   permitted alternative it named. Do not work around a refusal.
5. If it succeeds, say where the file is, what was checked, and the measured
   number behind each check.

If the user wants a whole repository set up rather than one asset, use the
`aninda-repo` skill instead. If they want something that already exists
checked, use `aninda-review`.
