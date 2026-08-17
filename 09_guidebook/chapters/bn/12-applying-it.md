<!-- Hand-written Bangla chapter. Only strings verified in 06_type/BANGLA-STANDARD.md
     appear here. No Bangla is written for this book. -->

{{gap-notice}}

Everything in the English section is code, file names, package names and command
lines. None of it changes between languages, and none of it should: rule 3 of
the house guidance on Latin words inside Bangla says to keep Latin for anything
copied literally.

## The one rule that is about Bangla

Mark Bangla with `lang="bn"` and the token file does the rest.

```css
:lang(bn), [lang="bn"] {
  font-family: var(--as-font-bangla);
  line-height: var(--as-bangla-line-height);
  font-size: clamp(var(--as-text-bangla-min),
                   calc(1em * var(--as-bangla-scale-body)), 100em);
}
```

The `clamp()` applies the measured multiplier and refuses to go below the 12 px
floor. Add `.as-bn-large` to anything at lead size or larger to exempt it from
the small-size weight bump.

{{data:output-files}}
