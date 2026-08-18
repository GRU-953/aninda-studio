<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# Typography

Three faces, one scale, and one measured multiplier that makes Bangla and Latin
look the same size next to each other.

**Licence:** PolyForm Noncommercial 1.0.0. The fonts are SIL OFL 1.1 and carry
their own licence files.

---

## The three faces

| Role | Family | CSS token | Licence |
| --- | --- | --- | --- |
| Latin | Literata | `--as-font-latin` | SIL OFL 1.1 |
| Bangla | Noto Serif Bengali | `--as-font-bangla` | SIL OFL 1.1 |
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

There is **no Latin line-height token**. The system defines a line height for
Bangla only. Do not invent one; use the platform's own default.

---

## Bangla sizing — the rule that matters most

**Write `lang="bn"` and every figure in this section applies itself.** The
`:lang(bn), [lang="bn"]` block in `assets/css/tokens.css` sets the family, the
multiplier, the floor and the weight step in one declaration. The numbers below
are here so you can check what a rendered page is doing and explain it — they are
not a list of things to type. Applying them by hand to text that is tagged applies
them twice; applying them by hand instead of tagging leaves the text announced as
English, which fails WCAG 2.2 SC 3.1.2 (Level AA). Rule 5 in `SKILL.md` is the
short version.

Bangla's reading height is about 0.62 em against Latin's 0.72, so Bangla set at
the same nominal size looks smaller. The multipliers below were measured on
rendered specimens, not estimated.

| Step | Multiplier | CSS token |
| --- | --- | --- |
| caption | 0.815 | `--as-bangla-scale-caption` |
| body | 0.816 | `--as-bangla-scale-body` |
| heading | 0.817 | `--as-bangla-scale-heading` |
| title | 0.822 | `--as-bangla-scale-title` |
| display | 0.825 | `--as-bangla-scale-display` |

Two hard limits sit on top of the multiplier:

1. **Floor: 12 px** (`--as-text-bangla-min`). Never smaller, whatever the
   multiplier works out to. Body at 16 px × 0.816 gives 13.06 px, which is fine.
   Caption at 12 px × 0.815 gives 9.78 px, which is not, so caption Bangla is
   held at 12 px.
2. **One weight heavier below 14 px** (`--as-text-bangla-weight-bump-below`).
   Measured at true 1×: 12 px at weight 400 renders the মাত্রা — the horizontal
   headline above the letters — at luminance 123, which reads as grey. At weight
   500 it renders at 108, which reads as ink.

**Bangla line height is 1.6** (`--as-bangla-line-height`). Bangla needs more
leading than Latin because of the মাত্রা above and the vowel signs below.

---

## Writing Bangla text

Do not write new Bangla. Use only a string listed as verified in
`references/bangla.md`. If none fits, leave the English in place and say which
string is missing. This is not caution about quality; it is that the verified
list was checked against the Bangla Academy's own dictionary page by page, and
anything outside it has not been.

---

## Sentence case, everywhere

Headings, buttons, labels — sentence case. Not Title Case, not ALL CAPS.
Capitals are harder to read, and in Bangla they do not exist at all.

---

## Verified against

- Apple's system fonts now use dynamic optical sizes, so the old "swap the
  family at 20 pt" rule is a design-tool workaround, not a platform rule.
- macOS does **not** support Dynamic Type. iOS and iPadOS do.
- W3C, *Bengali Layout Requirements*, for the layout of the মাত্রা and the
  vowel signs.
- Checked 14 August 2026.
