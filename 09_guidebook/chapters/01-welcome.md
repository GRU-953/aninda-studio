<!-- Hand-written chapter. build.py reads this file; it never writes it. -->

This is the whole of Aninda Studio in one file. The mark, the colour, the type,
the components, the words, the licences and the honest list of what is missing.
Nothing here points at a server. If you have this file, you have the brand.

I am Aninda Sundar Howlader. I work alone, from Barishal, in Bangladesh. The
studio serves two audiences in two scripts — Bangla and English — and most of
the decisions in this book exist because those two scripts do not behave the
same way.

## Two halves, and why they are separate

Apple and Google both publish a design system openly, and both keep their brand
book private. That is worth stating early, because it is the thing most often
missed by anyone reading the Human Interface Guidelines and assuming it is a
brand book. It is not. It is a platform design system. The brand rules — how the
mark is drawn, when it may be recoloured, who may use it — are the part nobody
published, and so they are the part that gets improvised.

This kit is deliberately two artefacts with two licences:

{{table: The two halves of the kit, and the licence each carries.}}
| Part | What is in it | Licence |
|---|---|---|
| The design system | Tokens, colour roles, type scale, space, shape, motion, components | Apache-2.0 |
| The identity | The name, the mark, the wordmark, the tile, the lockups | Not licensed at all |
| The writing | The chapters of this book | PolyForm Noncommercial 1.0.0 |

The design system has to be usable by someone who is not permitted to use the
mark. If removing the mark broke the token set, the boundary would have been
drawn in the wrong place. Chapter 13 sets out the terms in full.

## How to read this

Each chapter has an English section and a Bangla one. The button at the top of
the page shows one and hides the other. It is one book, not two, because two
files drift apart and this whole project is arranged against drift.

Every number in the generated chapters — colour, type, space and shape,
components, motion — was read out of the token files at build time. Not one of
them was typed by hand into this book. If a token changes and this book is not
rebuilt, the build's own check fails.

Where a technical term is the correct one, it stays, and it gets one plain
sentence of explanation the first time it appears.

## What was built, and in what order

{{table: Each stage of the work, and what it produced.}}
| Stage | What it produced |
|---|---|
| Research | A benchmark against Apple, Google, WCAG 2.2, DTCG and the font licences |
| Strategy | The English writing standard |
| Directions | Four brand directions, compared as rendered pages rather than as descriptions |
| The mark | One geometry, two weights, ten files |
| Colour | Six ramps computed in OKLCH, then measured against every surface |
| Type | Thirty families measured, one pairing chosen on the measurements |
| Tokens | DTCG 2025.10, four themes, every colour carrying its own proof |
| Components | Thirty cards, each a self-contained HTML file |
| This book | The whole thing, assembled from those sources |

## Dates

The system is version 1.0.0. Every figure in it was measured or verified on
14 August 2026. Anything dated after that supersedes this file.
