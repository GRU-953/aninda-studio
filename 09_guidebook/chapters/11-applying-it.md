<!-- Hand-written chapter. build.py reads this file; it never writes it. -->

Everything in this chapter is about the design system half — the part under
Apache-2.0, which you may use without asking. The identity half is covered in
chapter 13.

## The shortest possible start

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components.css">
```

`tokens.css` defines every custom property. `components.css` is the component
layer, and it contains no literal colour at all — every colour in it is a
`var(--as-…)` from the token file. That is machine-checked at build time, so a
hard-coded colour cannot reach it.

Then write markup with the `.as-` classes, inside an element carrying `.as-root`.

## Or install it

{{data:publication}}

```bash
npm install aninda-studio-tokens
```

```bash
pip install aninda-studio-tokens
```

Both packages carry the same token data: the DTCG JSON, the combined CSS, and a
separate stylesheet per theme.

## Themes

There are four: light, dark, high contrast light, high contrast dark. They are
not four skins over one palette. Each was generated against its own contrast
target, which is why the high contrast pair is a different set of colours rather
than the same colours pushed further apart.

The token file arranges them in five layers, and the order matters:

1. **The default.** Light values on `:root`, unscoped.
2. **The reader's system setting**, under `prefers-color-scheme` and
   `prefers-contrast`, applied only where nobody has chosen explicitly. The
   `:not([data-theme])` in those rules is what makes an explicit choice further
   down the tree possible at all.
3. **An explicit choice**, `[data-theme="…"]` on any element. These come last so
   they win, and because they can sit on any element, a dark panel can live
   inside a light page.
4. **Forced colours.** The operating system supplies the palette and every brand
   value gives way. A hex that survives this mode has defeated it.
5. **Reduced motion**, honoured at the root.

```html
<html data-theme="dark">
<div data-theme="hc-light"> … a high-contrast island … </div>
```

Leave `data-theme` off entirely to follow the reader's own system setting. That
is the right default for most pages.

## A second script

There is no rule for one, and that is a deliberate absence rather than an
oversight. A `:lang(bn)` block sat in the stylesheet until 27 August 2026,
carrying a measured size multiplier and a 12 px floor in a single `clamp()`.
It went with the Bangla, along with the four custom properties it read.

If you set a second script with this kit, do not reach for the shape of that
rule from memory. Measure the face you actually intend to ship: the multiplier
that made the two look equal was a property of Literata and Noto Serif Bengali
together, not a general fact about either script. `06_type/BANGLA-STANDARD.md`
records how it was measured, which is the transferable part.

## Accessibility, in the order it usually goes wrong

- **Focus.** The component layer draws the ring on `:focus`, not
  `:focus-visible`. `:focus-visible` is a browser heuristic, and a heuristic can
  decide not to draw the ring. Showing the ring once too often is a smaller
  failure than losing it once. No rule in the layer sets `outline: none`.
- **Colour alone is never the signal.** Every state carries a word and a glyph
  as well as a colour. CSS cannot enforce this — a stylesheet has no way to know
  whether the markup it is styling carries a word next to the colour — so it
  lives in the markup and in review, and it is named here as a promise rather
  than as a guarantee.
- **Targets.** Three different minimums exist and they are not the same number:
  WCAG 2.2 says 24 CSS px, Apple says 28 pt minimum with 44 pt comfortable, and
  Android says 48 dp. All four figures are tokens. Pick by platform, not by
  habit.
- **Glyphs are drawn, not typed.** Literata has no tick, no cross and no warning
  triangle, so a glyph typed as a character would fall back silently to whatever
  font the reader's machine happens to have. Every glyph in the system is an
  inline SVG in `currentColor`, which means it inherits both the theme and the
  forced-colours palette.

## Checking your work

The component library ships a harness that measures rather than asserts. It
opens every card in a real Chromium at three widths and in all four themes, and
then reads the pixels.

```bash
export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
./.venv/bin/python 08_components/check.py
```

It reads contrast off the composited effective background, walking ancestors and
blending partly transparent layers, because reading an element's own
`background-color` returns a transparent value for nearly every element in a
real page and proves nothing. It drives interaction states with a real pointer.
It measures the focus ring from differenced pixel buffers. It runs a liveness
probe on the forced-colours emulation first, and fails as not-equipped rather
than passing silently if the emulation is inert — a check that cannot fail is
not a check.

It prints what it could not check at the end. That list is part of the result.

## Rebuilding this book

From the repository root, as with every command in this book:

```bash
export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
./.venv/bin/python 09_guidebook/build.py
./.venv/bin/python 09_guidebook/scripts/pdf.py
```

`build.py --check` regenerates every byte in memory and compares it against what
is on disk, writes nothing, and exits non-zero on the first difference. That is
the drift guard. If a token moves and this book is not rebuilt, the check fails.

## The two files this book ships as

{{data:output-files}}

## What is in the kit

{{data:kit-index}}
