<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# The continuous-integration check

Two ideas do most of the work here. Everything else follows from them.

**Licence:** PolyForm Noncommercial 1.0.0. The workflow template is Apache-2.0.

---

## Idea one: the cheapest failure surfaces first

Order the jobs by how long they take, shortest first, each one depending on the
last. A typo fails in fifteen seconds and the slow job never starts.

| Order | Job | Takes | Catches |
| --- | --- | --- | --- |
| 1 | `lint` | seconds | JSON that does not parse, a committed `.DS_Store`, a generated file that lost its header, a PolyForm URL with a trailing slash |
| 2 | `tokens` | under a minute | **drift** — see idea two |
| 3 | `build` | a minute or two | anything with a `--check` mode |
| 4 | `render` | several minutes | what only a real browser can measure |

The point is not speed for its own sake. It is that a person waiting on a slow
job to learn about a typo stops reading CI output, and CI nobody reads is worse
than no CI.

---

## Idea two: regenerate, then diff

The most valuable job in the file is four lines long:

```yaml
- name: Regenerate everything
  run: python build.py
- name: Nothing generated may differ from what was committed
  run: git diff --exit-code
```

A non-empty diff means one of exactly two things:

1. A generator changed and its output was not regenerated.
2. Somebody hand-edited an output file instead of its input.

Both are silent failures under every other kind of check. Tests pass, the build
passes, and the repository quietly contains a file that no longer matches the
code that claims to produce it.

---

## What makes idea two work: no timestamps

**Nothing generated may contain a date, a time, a random value, or an absolute
path.** Every generated artefact must be a pure function of its inputs, so that
regenerating something unchanged produces a byte-identical file.

Put build time in the CI log, never in a file that gets diffed. If a file needs
to say which version of its input it came from, use a content hash — it changes
only when the content does. That is a stronger statement than a date anyway: a
date tells you when someone ran a script, and a hash tells you what it read.

The same rule makes a reproducible archive possible. A zip that stores the
filesystem modification time is different every build even when its contents are
identical, so every entry gets a fixed timestamp instead.

---

## What the brand job checks

```yaml
- name: The brand check
  run: python path/to/aninda-review/scripts/check.py .
```

It exits `1` on a failure, `0` on none, and `3` when it is not equipped for what
it was given. Treat `3` as a failure in CI: it means the check did not actually
run, and a check that did not run must never read as a pass.

---

## Two more small guards worth having

**The PolyForm trailing slash.** It takes one keystroke to add and returns 404,
and nobody notices for months:

```yaml
- run: |
    if grep -rnE "noncommercial/1\.0\.0/" --include='*.md' . ; then
      echo "::error::The PolyForm URL must not have a trailing slash"; exit 1
    fi
```

The pattern is a regular expression with the dots escaped, rather than the plain
string. That is not fussiness: a plain-string check would match this very file
and fail the build on a warning about the mistake instead of on the mistake.

**A generated file that lost its header.** A generated file with no "GENERATED"
line invites someone to edit it:

```yaml
- run: grep -q "GENERATED" path/to/output.css || exit 1
```

---

## Permissions

Start at `contents: read` and add only what a job proves it needs. A workflow
with write access it does not use is a standing risk for no benefit.

```yaml
permissions:
  contents: read
```

---

## Cancel superseded runs

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Pushing twice in a minute should not run the slow job twice.
