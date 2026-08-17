<!-- Hand-written chapter. build.py reads this file; it never writes it. -->

Three licences and one thing that has no licence at all.

| Part | Terms | SPDX identifier |
|---|---|---|
| The design system — tokens, stylesheets, build scripts, component cards | Apache License 2.0 | `Apache-2.0` |
| The writing — the chapters of this book | PolyForm Noncommercial 1.0.0 | `PolyForm-Noncommercial-1.0.0` |
| The typefaces | SIL Open Font Licence 1.1 | `OFL-1.1` |
| **The name, the mark, the wordmark, the tile and every lockup of them** | **Not licensed** | — |

## The system: Apache-2.0

The tokens, the stylesheets, the build scripts and the thirty component cards
are under the Apache License, Version 2.0. It is an OSI-approved permissive
open-source licence. Use it, fork it, build a product on it, sell that product.

Keep the copyright notice and the `NOTICE` file with any redistribution. The
full text is at `https://www.apache.org/licenses/LICENSE-2.0`.

## The writing: PolyForm Noncommercial 1.0.0

The chapters of this book are under PolyForm Noncommercial 1.0.0.

- SPDX identifier: `PolyForm-Noncommercial-1.0.0`
- Released 9 July 2019
- Canonical URL: `https://polyformproject.org/licenses/noncommercial/1.0.0`

**Write that URL with no trailing slash.** The trailing-slash form returns a 404.
It is an ordinary mistake to make and the link then looks broken to whoever you
sent it to.

Two things to be straight about:

**It is source-available, not open source.** PolyForm Noncommercial is **not
OSI-approved and not FSF Free/Libre**. Calling it open source would be
inaccurate, and this book will not do that.

**Licence scanners and corporate allowlists often flag it.** If you work
somewhere with an automated compliance check, expect this licence to be
questioned. I would rather tell you here than let you find it in a review.

The practical effect: you may read this book, quote it, learn from it and use it
inside a non-commercial project. You may not sell it or fold it into something
you sell. The design system next to it has no such restriction, which is the
whole point of splitting them.

## The typefaces: SIL OFL 1.1

Three faces ship with this system, each as a subset — a copy with the unused
glyphs stripped out to cut the file size.

{{data:font-licences}}

The Open Font Licence is at version **1.1, dated 26 February 2007. There is no
version 1.2.** The canonical home is now `openfontlicense.org`, moved from
`scripts.sil.org`.

### The Reserved Font Name, and why one face was renamed

A font under the OFL may carry a **Reserved Font Name** — a name that a modified
copy is not allowed to keep. Subsetting a font counts as modification under
clause 3 of the licence, so a subset of a font with a Reserved Font Name has to
be renamed before it is distributed.

**IBM Plex Mono carries the Reserved Font Name "IBM Plex".** The subset used in
this system is therefore renamed **Aninda Mono** in its `name` table, and the
build refuses to finish if any Reserved Font Name survives the rename.

**Literata and Noto Serif Bengali carry no Reserved Font Name**, so their
subsets keep their real names. Renaming those would make the system harder to
trace rather than safer, which is the opposite of what the rule is for.

Each subset ships with the full `OFL.txt` of the font it came from.

## The identity: not licensed at all

**The name "Aninda Studio", the Bangla name, the mark, the wordmark, the tile
and any lockup of them are not licensed.** No permission to use them is granted
by this book, by the Apache licence on the system, or by the PolyForm licence on
the writing.

They are not included in the npm or Python packages, and no licence to them is
granted by those packages either.

**Fork the system and put your own identity on it.** That is the intended path
and it is a supported one: the design system was built so that it works with the
mark removed. If deleting the identity broke the tokens, the boundary would have
been drawn in the wrong place.

### What you may do without asking

- Use the design system, in full, in anything.
- Reproduce the mark to refer to Aninda Studio — in a piece of writing about the
  studio, in a list of tools you use, in a credit line.
- Link to the studio.

### What needs a written yes from me

- Putting the mark on a product, a package, a site or a document that is not
  Aninda Studio's.
- Any use that suggests I made, endorsed or checked something I did not.
- Modifying the mark in any way, including recolouring it outside the rules in
  chapter 3.

Write to **aninda.sh15@gmail.com**. I answer.

### The name is an adjective

Never a verb, never a plural, never a possessive. *An Aninda Studio component* —
yes. *Anindas* — no. That convention is borrowed from Apple's own trademark
guidance, and it is the ordinary way a name stays a name.

## Contact

**aninda.sh15@gmail.com**

## Not legal advice.
