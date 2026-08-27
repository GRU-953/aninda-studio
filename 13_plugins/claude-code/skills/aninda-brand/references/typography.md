<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# Typography

Two faces and one scale. There were three: a Bengali face and a measured
multiplier that made Bangla and Latin look the same size beside each other left
with the Bangla on 27 August 2026. `06_type/BANGLA-STANDARD.md` is the record.

**Licence:** PolyForm Noncommercial 1.0.0. The fonts are SIL OFL 1.1 and carry
their own licence files.

---

## The two faces

| Role | Family | CSS token | Licence |
| --- | --- | --- | --- |
| Latin | Literata | `--as-font-latin` | SIL OFL 1.1 |
| Monospaced | Aninda Mono | `--as-font-mono` | SIL OFL 1.1 |

**Aninda Mono is a renamed subset of IBM Plex Mono.** `IBM Plex` is a Reserved
Font Name, subsetting counts as modifying under OFL 1.1 clause 3, and a modified
version may not use the reserved name. The unmodified family stays as the next
fallback in the stack, so anyone who already has IBM Plex Mono gets the original.

Literata was chosen over Inter, which measured slightly better on the
cross-script multiplier. Inter is the default of half the web, and this is a
studio identity: distinctiveness was traded for 0.056 of a multiplier, knowingly.

---

## The scale

A perfect fourth, ratio 1.333.

| Step | rem | px at a 16 px root | CSS token |
| --- | --- | --- | --- |
| caption | 0.7502 | 12.00 | `--as-text-caption` |
| body | 1.0 | 16.00 | `--as-text-body` |
| lead | 1.333 | 21.33 | `--as-text-lead` |
| h3 | 1.7769 | 28.43 | `--as-text-h3` |
| h2 | 2.3686 | 37.90 | `--as-text-h2` |
| h1 | 3.1573 | 50.52 | `--as-text-h1` |
| display | 4.2087 | 67.34 | `--as-text-display` |

There is **no line-height token at all**. There was one, for Bangla, and it
went with the Bangla. Do not invent one; use the platform's own default.

---

## Sentence case, everywhere

Headings, buttons, labels — sentence case. Not Title Case, not ALL CAPS.
Capitals are harder to read: the word shapes that a reader recognises without
spelling out are made by ascenders and descenders, and capitals flatten them
into one rectangle. The second half of this rule used to be "and in Bangla they
do not exist at all", which was true and is no longer this system's argument to
make.

---

## Verified against

- Apple's system fonts now use dynamic optical sizes, so the old "swap the
  family at 20 pt" rule is a design-tool workaround, not a platform rule.
- macOS does **not** support Dynamic Type. iOS and iPadOS do.
- Checked 14 August 2026.
