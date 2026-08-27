---
description: Set up or upgrade a whole repository to the Aninda Studio standard — the four licences, NOTICE, the README, the token files and a CI brand check.
argument-hint: "[path to the repository, default the current folder] [--upgrade]"
disable-model-invocation: true
---

<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->

Set up a new repository, or upgrade an existing one, to the Aninda Studio
standard.

Use the `aninda-repo` skill. It owns the whole-repository job: the licence
split, the NOTICE file, the README, the token files, and the
continuous-integration check that keeps them from drifting.

What the user asked for: `$ARGUMENTS`

Do this:

1. Read `skills/aninda-repo/SKILL.md` and follow it.
2. Before writing anything, list what you are about to add or change and ask the
   user to confirm. This skill writes several files at the root of a repository,
   and that is not something to do unannounced.
3. Never overwrite an existing `LICENSE`, `NOTICE` or `README.md` without saying
   what is in it now and what would replace it.
4. Finish by running the `aninda-review` skill's checker over the result, and
   report what it found.

If the user wants one asset made, use `aninda-brand`. If they want an existing
page or component checked rather than a whole repository set up, use
`aninda-review`.
