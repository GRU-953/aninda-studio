<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# The licence matrix — exact wording

Copy from here. Do not paraphrase a licence identifier or a URL from memory:
three of the four have a form that is commonly written wrong.

**Licence of this document:** PolyForm Noncommercial 1.0.0.

---

## Which file gets which

| Pattern | Licence | Header |
| --- | --- | --- |
| `*.py`, `*.js`, `*.ts`, `*.mjs`, `*.sh` | Apache-2.0 | `SPDX-License-Identifier: Apache-2.0` |
| `*.css`, `*.json` tokens, `*.svg` in a system folder | Apache-2.0 | same |
| `.github/workflows/*.yml` | Apache-2.0 | same |
| `README.md`, `README.bn.md`, any guide, any reference document | PolyForm-Noncommercial-1.0.0 | `SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0` |
| `*.woff2`, `*.ttf`, `*.otf` | OFL-1.1 | the `-OFL.txt` beside it, not a header |
| The mark, wordmark, tile and icon files | **none** | no header; named in `NOTICE` and `TRADEMARKS.md` |

A file that is both — a script whose docstring is the documentation — takes
`Apache-2.0`. The code is the thing being licensed.

---

## The three things commonly written wrong

**1. The PolyForm URL.** This is the whole of it, and it ends at the last zero:

```
https://polyformproject.org/licenses/noncommercial/1.0.0
```

**Adding a trailing slash to that URL returns 404.** The wrong form is not
written out here on purpose: a repository that greps for the literal string would
match this file and fail on a warning about the mistake rather than on the
mistake. Check for it with a pattern instead — `references/ci.md` has one.

**2. "Open source".** PolyForm Noncommercial is **source-available, not open
source**. It is not approved by the Open Source Initiative, because the Open
Source Definition does not permit a restriction on a field of use, and
noncommercial-only is exactly that. Licence scanners and company allowlists
often flag it. Write that plainly wherever the licence is named, so a reader
learns it before they depend on it rather than after.

**3. The OFL version.** There is **no SIL OFL 1.2**. Version 1.1 dates from
26 February 2007. The canonical home moved to `https://openfontlicense.org/`.

---

## SPDX expressions

| Situation | Expression |
| --- | --- |
| A package of scripts only | `Apache-2.0` |
| A package of documentation only | `PolyForm-Noncommercial-1.0.0` |
| A package holding both | `Apache-2.0 AND PolyForm-Noncommercial-1.0.0` |
| A package that also ships fonts | `Apache-2.0 AND PolyForm-Noncommercial-1.0.0 AND OFL-1.1` |

`AND` means both apply to their own parts. It does not mean the reader chooses.
`OR` would be a dual licence, and this is not one.

---

## Reserved Font Names

A Reserved Font Name may not appear in the name of a **modified** version of the
font, and **subsetting counts as modifying** under OFL 1.1 clause 3.

| Family | Reserved name | If you subset it |
| --- | --- | --- |
| IBM Plex Mono | `IBM Plex` | Rename it. This system's subset is `Aninda Mono`. |
| Literata | none | Keep the name. |
| Noto Serif Bengali | none | Keep the name. |

When a font is renamed, keep the unmodified family as the next fallback in the
stack, so anyone who already has the original gets the original:

```css
--as-font-mono: "Aninda Mono", "IBM Plex Mono", ui-monospace, monospace;
```

---

## What NOTICE must say

All four, each with three things: what it covers, what it means, and where its
full text lives. Plus the "not open source" note on PolyForm, and the reason the
identity is unlicensed:

> The system is meant to be reused. The identity is not. Fork the system and put
> your own name and mark on it — that is the intended use, and it costs you
> nothing.

That last sentence matters. A repository that says "the marks are not licensed"
and stops there reads as a threat. Saying what someone *may* do turns it into an
invitation.

---

## Contact

`aninda.sh15@gmail.com` for questions and permissions.

*Not legal advice. Written by the author of this kit, who is not a lawyer.*
