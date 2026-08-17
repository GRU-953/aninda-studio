---
name: aninda-repo
description: >-
  Set up or upgrade a WHOLE REPOSITORY to the Aninda Studio standard. Writes the
  four-licence split (Apache-2.0 for the system and scripts, PolyForm
  Noncommercial 1.0.0 for the writing, SIL OFL 1.1 for the fonts, and no licence
  at all for the name and the marks), the NOTICE file that states all four, a
  TRADEMARKS file, a bilingual English and Bangla README pair, the DTCG token
  files, an SPDX header on every source file, a .gitignore, and a
  continuous-integration workflow that regenerates every generated file and fails
  on a diff. Use when asked to set up, scaffold, bootstrap, initialise, start,
  create, upgrade, migrate, standardise or bring a repository or project up to
  standard, and when asked "add a licence", "which licence", "licence headers",
  "SPDX headers", "add a NOTICE", "add a bilingual README", "README.bn.md", "set
  up CI", "add a brand check to CI", "GitHub Actions for the brand", "new repo",
  "new project", or "make this repo compliant". This skill WRITES SEVERAL FILES
  AT A REPOSITORY ROOT, so it lists what it will do and asks before it does it.
  For making ONE asset or designing one thing, use the aninda-brand skill
  instead. For checking something that already exists, use the aninda-review
  skill instead.
---

<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->

# Aninda Studio — set up or upgrade a repository

This skill works at the scale of a repository. If the job is one file, one asset
or one page, it is the wrong skill.

**Licence:** the scripts and templates are Apache-2.0. This document is PolyForm
Noncommercial 1.0.0. See `NOTICE`.

---

## Ask first. Always.

This skill writes at the root of somebody's repository, including files that may
already exist and may already say something different. So:

1. Read what is there now. `LICENSE`, `NOTICE`, `README.md`, `.gitignore`,
   `.github/workflows/`.
2. Write the user a short list: what will be **added**, what will be
   **replaced**, and what will be **left alone**.
3. For anything being replaced, say what it says now and what would replace it.
4. Wait for a clear yes.
5. Then write.

Never overwrite `LICENSE`, `NOTICE` or `README.md` without step 3. A licence file
someone chose on purpose is not a thing to quietly swap.

---

## What a repository gets

| File | What goes in it | Licence of the file |
| --- | --- | --- |
| `LICENSE` | The full Apache License 2.0 text. | — |
| `LICENSE-DOCS.md` | The full PolyForm Noncommercial 1.0.0 text, with the "source-available, not open source" note above it. | — |
| `NOTICE` | All four licences, each with what it covers and where its text lives. | — |
| `TRADEMARKS.md` | What is not licensed at all, and how to ask. | PolyForm |
| `README.md` | English. | PolyForm |
| `README.bn.md` | Bangla, written as Bangla — not translated from the English. | PolyForm |
| `.gitignore` | The usual, plus anything generated that is not committed. | — |
| `.github/workflows/brand.yml` | The brand check. | Apache-2.0 |
| `fonts/*-OFL.txt` | One beside each font file, never one shared copy. | — |

`references/licence-matrix.md` has the exact wording for each. Do not paraphrase
a licence identifier or URL from memory.

---

## The four licences, in one table

| Part | Licence | SPDX | Open source? |
| --- | --- | --- | --- |
| The system, the tokens, every script | Apache License 2.0 | `Apache-2.0` | Yes, OSI-approved |
| The written documentation | PolyForm Noncommercial 1.0.0 | `PolyForm-Noncommercial-1.0.0` | **No.** Source-available |
| The typefaces | SIL Open Font License 1.1 | `OFL-1.1` | Yes |
| The name, mark, wordmark, tile, lockups | **None at all** | — | No licence granted |

For a package holding both code and documentation, the combined expression is
`Apache-2.0 AND PolyForm-Noncommercial-1.0.0`.

Three things to get right, because each is commonly got wrong:

- The PolyForm URL is `https://polyformproject.org/licenses/noncommercial/1.0.0`
  with **no trailing slash**. The trailing-slash form returns 404.
- PolyForm Noncommercial is **source-available, not open source**. It is not
  OSI-approved. Say so wherever the licence is named.
- **There is no SIL OFL version 1.2.** Version 1.1 dates from 26 February 2007
  and its home is now `openfontlicense.org`.

---

## SPDX headers

Every source file gets one, matching which of the four it belongs to.

```
SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
```

```
SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader
```

A generated file also says it is generated, and names the script that makes it,
on the first line. `references/ci.md` explains why that line is load-bearing.

---

## The bilingual README

Two files, not one file with two halves.

- `README.md` — English, written to `aninda-brand/references/voice.md`.
- `README.bn.md` — Bangla, written **as Bangla**. Same meaning, same steps,
  different sentences.

**Use only a verified Bangla string.** The list is in
`aninda-brand/references/bangla.md` and `aninda-brand/assets/bangla-verified.json`.
If a heading or a sentence you need is not on it, keep that part in English and
tell the user which string is missing. Do not write new Bangla.

Each README links to the other in its first few lines, so a reader lands in the
right one.

`templates/README.md` and `templates/README.bn.md` are the starting points.

---

## The CI check

`templates/brand.yml` is a GitHub Actions workflow. Its jobs are ordered so the
**cheapest failure surfaces first**: a typo fails in fifteen seconds, and the
slow job never starts.

The job that matters most regenerates every generated file and then runs
`git diff --exit-code`. A non-empty diff means one of two things: a generator
changed without its output being regenerated, or somebody hand-edited an output
file instead of its input. Both are silent failures in every other kind of check.

**That check only works if generation is deterministic**, which is why nothing
generated may contain a timestamp. Build time belongs in the CI log, never in a
file that gets diffed. `references/ci.md` covers this in full.

---

## Order of work

1. Read what is already there.
2. List what will change. Ask. Wait.
3. Write the licence files, then `NOTICE`, then `TRADEMARKS.md`.
4. Add SPDX headers, matching each file to the right one of the four.
5. Write `README.md`, then `README.bn.md` with verified Bangla only.
6. Copy the token files in, if the repository uses them.
7. Put one `-OFL.txt` beside each font file.
8. Add `.gitignore` and the CI workflow.
9. Run the `aninda-review` skill's checker over the result and report what it
   found, blind spots included.

---

## If the job is smaller than a repository

Use `aninda-brand` to make one asset or design one thing. Use `aninda-review` to
check something that already exists.
