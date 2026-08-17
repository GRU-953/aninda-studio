<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# The licence split

Most projects have one licence. This one has four, because the parts genuinely
differ. Getting the split wrong in either direction causes real harm: too
permissive gives away an identity that is not being given away, too restrictive
stops someone reusing work that was meant to be reused.

**Licence of this document:** PolyForm Noncommercial 1.0.0.

---

## The four, at a glance

| Part | Licence | SPDX | Open source? |
| --- | --- | --- | --- |
| The system, the tokens, every script | Apache License 2.0 | `Apache-2.0` | Yes, OSI-approved |
| The written documentation | PolyForm Noncommercial 1.0.0 | `PolyForm-Noncommercial-1.0.0` | **No.** Source-available |
| The typefaces | SIL Open Font License 1.1 | `OFL-1.1` | Yes |
| The name, mark, wordmark, tile, lockups | **None at all** | — | No licence granted |

The combined expression for a package that holds both code and documentation is:

```
Apache-2.0 AND PolyForm-Noncommercial-1.0.0
```

---

## 1. The system — Apache-2.0

**Covers** the design tokens, the stylesheets, the component code, every build
and verification script, and both plugins.

**Means** anyone may use, change and redistribute it, including commercially,
with attribution and a note of what they changed.

**File header:**

```
SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
```

---

## 2. The writing — PolyForm Noncommercial 1.0.0

**Covers** the guidebook, the reference documents, the research and benchmark
documents, and the templates.

**Means** free to read, copy, adapt and share for any noncommercial purpose,
including personal study, research, hobby projects, and use by charities,
educational institutions, public research bodies, public safety and health
organisations, and government bodies. Not for resale.

**Canonical URL:** `https://polyformproject.org/licenses/noncommercial/1.0.0`

**The URL has no trailing slash. The trailing-slash form returns 404.** A
trailing slash takes one keystroke to add and a long time to notice, so it is
worth checking whenever the URL is written.

**Released** 9 July 2019 by the PolyForm Project.

**Say this plainly, every time:** PolyForm Noncommercial is **source-available,
not open source**. It is not approved by the Open Source Initiative, because the
Open Source Definition does not permit a restriction on a field of use. Licence
scanners and company allowlists often flag it. Anyone deciding whether to depend
on it should know that before they do, not after.

**File header:**

```
SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader
```

---

## 3. The typefaces — SIL Open Font License 1.1

**Covers** Literata, Noto Serif Bengali, and the IBM Plex Mono subset.

**There is no OFL version 1.2.** Version 1.1 dates from 26 February 2007 and the
canonical home is now `https://openfontlicense.org/`. A reference to "OFL 1.2" is
always wrong.

**One `-OFL.txt` travels beside each font file.** Not one shared copy at the
root — one per font, next to the font.

**Reserved Font Names.** IBM Plex Mono carries the Reserved Font Name `IBM Plex`.
Subsetting a font counts as modifying it under OFL 1.1 clause 3, and a modified
version may not use a reserved name. The subset here is therefore renamed
**Aninda Mono**, with the unmodified family kept as the next fallback in the
stack. Literata and Noto Serif Bengali carry no reserved name and keep theirs.

---

## 4. The identity — not licensed at all

**Covers** the name "Aninda Studio", the Bangla name "অনিন্দ্য", the mark, the
wordmark, the tile, the icons, and any lockup of them.

**Means** no licence is granted to any of it, by any file in the system. It is
not open source, not source-available, and not free to use.

**Why** the system is meant to be reused; the identity is not. Fork the system and
put your own name and mark on it. That is the intended use, and it costs nothing.

---

## What a repository needs

| File | Holds |
| --- | --- |
| `LICENSE` | The full Apache-2.0 text. |
| `LICENSE-DOCS.md` | The full PolyForm Noncommercial 1.0.0 text, with the "not open source" note above it. |
| `NOTICE` | All four, each with what it covers and where its text lives. |
| `TRADEMARKS.md` | What is not licensed, and how to ask. |
| `fonts/*-OFL.txt` | One per font file, beside the font. |

The `aninda-repo` skill writes all of these.

---

## Contact

Questions and permissions: `aninda.sh15@gmail.com`
Source: `https://github.com/GRU-953/aninda-studio`
Site: `https://anindastudio.com`

*Not legal advice. Written by the author of this kit, who is not a lawyer.*
