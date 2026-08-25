# Aninda Studio — sandbox and toolchain

**Set up:** 14 August 2026 · Sandbox root: the repository folder itself

Everything here is **project-local**. Nothing was installed on the Mac outside this folder, no
Homebrew package was added, and no system setting was changed. Deleting this folder removes the
entire build environment.

Every tool below was **smoke-tested** — a small real job was run through it to prove it works,
not merely that it installed.

---

## Where things live

| Path | What it is |
|---|---|
| `.venv/` | The Python environment. Run things as `./.venv/bin/python …` |
| `00_sandbox/node_modules/` | The Node tools |
| `00_sandbox/browsers/` | Chromium (554 MB), pinned here by `PLAYWRIGHT_BROWSERS_PATH` |

Nothing in `.venv/`, `node_modules/` or `browsers/` is ever committed or shipped.

---

## Python packages

Run with `./.venv/bin/python`. Versions are pinned exactly, because an unpinned colour library
would silently change measured contrast figures between runs.

| Package | Version | Licence | What it does, in plain English |
|---|---|---|---|
| `coloraide` | 8.11.1 | MIT | Converts between colour systems and **measures** contrast, so the palette is provably readable rather than assumed to be |
| `fonttools` | 4.63.0 | MIT | Reads font files, pulls out letter outlines, subsets fonts down to only the characters used, and writes web font files |
| `uharfbuzz` | 0.56.0 | Apache-2.0 | Real text shaping — the thing that makes Bangla come out right. See below |
| `brotli` | 1.2.0 | MIT | Compression used to make `.woff2` web fonts |
| `playwright` | 1.62.0 | Apache-2.0 | Drives a real browser: renders pages, **measures** what actually appeared, exports PNG and PDF |
| `Pillow` | 12.1.0 | MIT-CMU | Image work — PNG exports, and writing the multi-size `.ico` favicon |
| `Markdown` | 3.10 | BSD-3-Clause | Turns the hand-written guidebook chapters into HTML |
| `lxml` | 6.0.2 | BSD-3-Clause | Reads and edits SVG safely |

## Node packages

| Package | Version | Licence | What it does |
|---|---|---|---|
| `esbuild` | 0.25.12 | MIT | Bundles the Figma plugin into a single file, which is what Figma requires |
| `typescript` | 5.9.3 | Apache-2.0 | Type-checks the Figma plugin before it is bundled |
| `@figma/plugin-typings` | 1.133.0 | MIT | Figma's own type definitions. 1.133.0 was the current release on 6 August 2026 |

---

## The one dependency this build deliberately does NOT have: Inkscape

The sibling GRU953 kit treated Inkscape as a hard requirement. It used it for one job: converting
Bangla text to real, correctly-shaped outlines. Bangla needs genuine text shaping — consonants
join into conjuncts, and some vowel signs are **written before** the consonant they actually
follow. Pulling glyphs out of a font by code point produces nonsense.

Inkscape is a ~1 GB application that must be installed system-wide. **This build replaces it with
`uharfbuzz` + `fontTools`**, both pip packages inside `.venv/`, which do the same job through the
same underlying library (HarfBuzz) with no system install.

### The proof it works

Shaping the Bangla wordmark **অনিন্দ্য** through `uharfbuzz`:

```
codepoints:     8   অ ন ি ন ্ দ ্ য
shaped glyphs:  5
script: Beng · direction: ltr
glyph → cluster: [(121, 0), (168, 1), (152, 1), (467, 3), (218, 7)]
```

Two things are visible in that output, and both are the things naive code gets wrong:

1. **The conjunct formed.** Clusters 3–7 (`ন ্ দ ্ য`) collapsed into a single glyph, 467. Eight
   code points became five glyphs. Without shaping you would get eight separate letters and a
   word no Bangla reader would accept.
2. **The vowel sign reordered.** Cluster 1 is `ন` followed by `ি`, but two glyphs come out of it
   and the pre-base form is placed first — the vowel is drawn to the **left** of the consonant it
   belongs to, which is how Bangla is actually written.

Outlines then come out of `fontTools` as SVG path data (`SVGPathPen`), giving the same result
Inkscape's export produced.

**Fail-closed rule:** the mark and lockup generators check that shaping is available and that the
intended font family loaded, and **refuse to draw at all** if either check fails. They never
silently substitute a different typeface — that failure is invisible in the output and was worth
designing against explicitly.

---

## Other substitutions made to stay project-local

| Normally needs a system install | Used instead | Why it is fine |
|---|---|---|
| Inkscape | `uharfbuzz` + `fontTools` | Same shaping engine (HarfBuzz), proven above |
| `rsvg-convert` / `cairosvg` (SVG → PNG) | Chromium via Playwright | Chromium's SVG renderer is the one the artwork will actually be viewed in, so it is the more honest target |
| `ghostscript` / `qpdf` (PDF) | Chromium's own PDF export | One renderer for both the HTML guidebook and its A4 print edition, so they cannot drift apart |
| `woff2_compress` | `fontTools` + `brotli` | Same output format, pure pip |
| `optipng` | Pillow's own PNG optimisation | Slightly larger files; not worth a system install |
| ImageMagick | Pillow | Everything needed here is resize, convert and `.ico` packing |
| `fontforge` | `fontTools` | Only needed if letterforms are edited; deferred until a direction requires it |

**Nothing failed to install.** Every package above resolved to a pre-built wheel for
Python 3.13 on Apple Silicon, so nothing had to be compiled.

---

## Host tools already present (not installed by this build)

Node 26.7.0 · npm 11.19.0 · Python 3.13.15 · git 2.55.0 · gh 2.97.0 (signed in as `GRU-953`,
scopes `gist, read:org, repo, workflow`) · brotli.

---

## Running things

```
# from the repository root
export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
./.venv/bin/python <script>
```

The `PLAYWRIGHT_BROWSERS_PATH` line matters — without it Playwright looks in a shared cache
outside this folder and will report the browser as missing.
