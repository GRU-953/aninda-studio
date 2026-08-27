<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# Handover

**Written 28 August 2026.** Hand-written, not generated — this is a note between
people, and it goes stale on purpose rather than being kept true by a build.

Read `00_README.md` first for what this repository is. This page is only about what
is unfinished and what you need to know before touching it.

---

## The one rule that explains the rest

**Nothing is asserted; everything is measured or generated.** About twenty Python
generators write nearly every artefact here. Every one of them is fail-closed: a
check that does not pass writes nothing at all. Every one has a `--check` mode, and
CI diffs the whole tree against a fresh run.

Two consequences you will meet within an hour:

- **Do not hand-edit anything a generator writes.** Change the generator and re-run
  it. Generated files say so in their first line.
- **A number in prose is a claim.** If you write one, something has to check it.
  This is not stylistic: the registers here are full of figures that were true when
  typed and false a week later.

Run everything with the project's own interpreter, `./.venv/bin/python`, and set
`PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers` — several gates render in a real
Chromium and refuse rather than skip when they cannot find one.

```bash
cd "/Volumes/Aninda Studio/Aninda_Studio" && git add -A && sh scripts/verify-all.sh
```

That is the whole suite, 42 gates, and it takes several minutes. **Stage first** —
`scripts/readme.py` discovers generators with `git ls-files`, so an untracked new
generator is invisible to the gate meant to catch it.

---

## State on 28 August 2026

`main` is green: all 42 gates locally, all eight CI jobs. Benchmark **24 met, 4
part met**. Platform gaps **19 of 23 closed**. Version **2.0.0**.

One branch exists, `compose-against-androidx` at `c780c3a`, pushed and **not**
merged. Its Gradle gate is failing on purpose — see below. No commit hash is given
for `main` here: this page is committed to `main`, so any hash it named would be
the one before itself. `git log --oneline -1` is the answer.

---

## What is left, in the order I would do it

### 1. The Compose patterns do not compile against androidx — finding R8-2

**This is the only piece of unfinished work with a failing check behind it.**

The eight Compose screens were written against `15_native/android/compose/stubs`,
twelve files of hand-typed androidx signatures, because no machine this system is
developed on has the Android SDK. A Gradle gate on the branch compiles them against
the real library instead. As of the last run:

- `:compose:compileReleaseKotlin` **passes** — the theme is fine
- `:patterns:compileReleaseKotlin` **fails** — the eight screens are not

That is the gate working, not a fault in it. Two of roughly thirteen declarations
added to that stub on 27 August were already known to be wrong, one of them
*rejecting* valid code; this is the other direction, the stub accepting code the
library refuses.

**What to do.** Push the branch, read `native-android` in the CI run, and fix the
screens. The gate re-runs once with `--info` on the failure path specifically to
recover Kotlin's `e: file://…` lines, so the next run names them. You cannot run
this locally without a JDK and Gradle — `brew install gradle` pulls one, and that
is a change to the owner's machine, so it was offered rather than made.

**Do not merge the branch until it is green.** `main`'s current claim — that the
Compose code is checked against a declared surface only — is the honest one while
the gate is failing.

Also on that branch and worth restoring once someone has a JDK: `kotlin {
explicitApi() }` was removed from the three module files because it came from the
standalone Kotlin plugin's extension, which AGP 9 replaces, and whether the
built-in one exposes the same call could not be found out from here.

### 2. Artefact hashes for the Gradle gate

`15_native/android/gradle/verification-metadata.xml` does not exist. It pins a
sha256 per artefact so a substituted jar fails the build closed, and it is the
third of three bounds on the only gate here that touches the network. Gradle
produces it by resolving the graph:

```bash
cd 15_native/android && gradle --write-verification-metadata sha256 :compose:compileReleaseKotlin :patterns:compileReleaseKotlin
```

Until it exists, resolution is pinned by **version** and not by **content** — the
same standing as `requirements.txt`. `compile_gradle()` in `15_native/build.py`
says so in its own docstring, and reports it in its note rather than claiming
verification it does not have.

### 3. The two gaps that remain open

- **G-STORE-2, the only open blocker.** No store screenshots, and none can honestly
  be made: there is no Aninda Studio app to photograph. Correctly sized frames
  exist, drawn with a 45-degree hatch so they could not be mistaken for captures,
  each naming the file that should replace it. `14_delivery/build.py
  --check-captures` measures the owner's own screenshots when there are some. This
  closes when an app exists and not before.
- **G-A11Y-1, minor.** Contrast is measured by WCAG 2.1 relative luminance only;
  Apple's accessibility page now names APCA as well. Additive — publishing an APCA
  figure beside the WCAG one would say more about small text than a ratio can, and
  it changes no existing verdict.

Two more are **deferred with the reason recorded**: G-STORE-4 (no notification
icon — not required to publish either listing, and no app to notify) and G-A11Y-2
(Accessibility Nutrition Labels — voluntary, and claiming one needs an app because
the threshold is about completing tasks).

### 4. Smaller things, none of them blocking

- **Compose type sizes are literals.** `Typography.kt` carries fifteen literal `sp`
  figures because `kotlin_tokens()` emits no `AnindaType`. The size guard was
  extended on 27 August to catch `padding(16.dp)`, which it had never seen, but
  deliberately **not** `.sp` — that would fail a file for a gap in the emitter
  rather than a fault in the file. Emit `AnindaType`, then extend the guard.
- **The patterns' accessibility is written, not measured.** The thirty web cards are
  measured in a browser; the native equivalent does not exist. The SwiftUI
  validation summary is marked `.updatesFrequently`, which tells VoiceOver an
  element changes and does **not** announce the change.
- **The patterns are compiled for five platforms and laid out for none.** watchOS
  and tvOS get a desktop composition with no compact variant.

---

## Things that will bite you

These all cost real time here. None is obvious from reading the code.

**The repository path has a space in it.** `/Volumes/Aninda Studio/…`. Quote it
everywhere. A `.split()` on command output once shattered it and the resulting gate
matched nothing — green in CI forever, because GitHub checks out to a path without
a space. That is finding R6-1.

**A gate on the FORM of something does not gate CLAIMS about it.** The Bangla
removal is enforced by a rule that fails on Bengali codepoints. It reached empty,
and 42 gates still passed over a published npm stylesheet shipping
`var(--as-font-bangla)`, a component card teaching readers to write that rule, and
about thirty English sentences saying the system is bilingual — none of which
contains a single Bengali character. `scripts/check_token_citations.py` now closes
the mechanical half: a custom property named in prose, in a stylesheet or on a card
is defined or it is not. The prose half is not gated and cannot easily be — "the
system is bilingual" has no mechanical answer. Finding R8-3 has the full list. When
you remove something from this system, grep for what the prose *says about* it, not
only for the thing.

**A committed generated file must not record the machine that wrote it.** This has
been learned four times: PNG bytes, then a per-file byte count in the store
packages, then compiler versions in `LIMITS.md`, then the guidebook citing the size
of the PDF printed from the guidebook. Browsers do not rasterise identically across
platforms; runners do not have the same toolchain; a document that cites its own
output cannot settle. **Nothing enforces this rule.** A gate that regenerated every
committed artefact twice on one machine and diffed the two would catch the whole
class, and it does not exist.

**Two gates are proved by CI and cannot be run locally**, which is the reverse of
everything else here:
- the Apple platform sweep — this machine has the macOS SDK alone, and iOS,
  watchOS, tvOS and visionOS are compiled by the `macos-15` job and by nothing here
- the Gradle gate, which needs a JDK and Gradle

`scripts/verify-all.sh` prints a refusal for these rather than `ok`, so a green
local run never implies cover it cannot give.

**`check_gates.py` asserts CI and `verify-all.sh` run the same list.** Add a gate to
one and you must add it to the other. It also now compares both copies of the
22-path English-standard list, which are written out longhand in two files and
were compared by nothing until 27 August.

**A step that cannot fail is not a gate.** `continue-on-error` in CI was refused for
exactly this reason. The repository already states the rule as "a gate that cannot
run is not a gate".

**Removing a function with a regex will eat its neighbours.** This swallowed
`BuildError`, `SPELLED`, `BUNDLED_FROM_REPO` and an entire `anindaTypography`
during this session. Compare the set of top-level definitions before and after:

```bash
./.venv/bin/python -c "import ast,subprocess; a=lambda s:{n.name for n in ast.parse(s).body if hasattr(n,'name')}; print(sorted(a(subprocess.run(['git','show','HEAD:FILE'],capture_output=True,text=True).stdout) - a(open('FILE').read())))"
```

**Trash, never delete.** The owner's standing instruction. Use `/usr/bin/trash`.
Five generators sweep their own output directories with `unlink()`, so the order is
**trash the file first, then run the generator** — its sweep then finds nothing to
destroy.

**Do not push without being asked.** Also standing.

---

## Bangla

This system was bilingual until 27 August 2026 and now ships English. The removal
touched 237 of 592 tracked files.

**What is kept, and must not be tidied away:** `06_type/BANGLA-STANDARD.md`,
`BANGLA-STRINGS.md` and `bangla-strings.json` are the record — seven orthography
questions with Bangla Academy citations and a 31-string review. The type research
names Bengali faces and features because it is the evidence for choosing Literata.
The seventeen Bengali font candidates are research *inputs*, excluded from every
counted figure, still read through `measurements.json` and swept by
`check_licence_claims.py` as its Reserved Font Name set.

**The studio's name stays.** A name is not text. "Aninda" is the romanised form of
অনিন্দ্য, and `references/naming.md` is the only place a reader learns why it is not
spelled "Anindya". The English-standard checker allows it as a *string* rather than
by exempting the six files that mention it.

**The rule is enforced by inversion.** The old question was "is this Bangla string
on the verified list?"; the new one is "why is there Bangla here?". Finding R7-1
recorded that the old rule was enforced where words were *shown* and not where they
*entered*; an inverted rule has no entry door to leave unguarded.

---

## Where to read next

| For | Read |
|---|---|
| What the system is | `00_README.md` |
| What it does not do | `15_native/LIMITS.md`, and the guidebook's last chapter |
| What is wrong with it | `01_research/OPEN-FINDINGS.md` — 108 entries, 106 re-verified |
| How it measures against Apple and Google | `01_research/BENCHMARK.md` |
| What is missing for the two stores | `01_research/PLATFORM-GAPS.md` |
| Why the English reads as it does | `02_strategy/ENGLISH-STANDARD.md` |
| What the last pass found and fixed | findings R8-1, R8-2, R8-3 |

The findings register is the most useful of these. It is generated from
`_data/findings.json`, every entry carries the command that proves it, and a
finding that gets fixed keeps its entry with the status changed — because the
record of what was wrong is the useful part.
