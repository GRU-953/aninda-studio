# Aninda Studio — what is still open

**Every entry below was re-verified against the tree, and each says on what date.** Each also carries the command that was run and what it returned. Nothing here is asserted from memory, and nothing was marked fixed because it looked like the sort of thing that had probably been fixed — a claim was either reproduced or it was not.

64 entries were checked in the pass of 19 August 2026. 43 more were raised later, and 6 of the original entries were re-checked — 25 August 2026, 26 August 2026, 27 August 2026, 28 August 2026. That first pass was needed because this document had drifted. It was written across three review rounds and never re-checked, and of the 64 entries it covered, **18 were already fixed** and **12 were half right** — what that pass found, on the day, kept as it was reported. A register that is wrong in either direction is worse than a short accurate one.

## Where it stands

| | |
|---|---|
| Entries re-verified | **107** |
| Still open | 30 |
| Half stale — part reproduced, part not | 12 |
| Already fixed, kept as a record | 63 |
| Closed earlier, by the owner's decision | 2 |

Of the 42 that carry work: 41 minor · 1 not-a-defect. **No blocker.** Everything below is a thing this system says about itself that is not quite true, a guard that is narrower than its message, or a piece of work not yet done — not a defect in what it produces.

## The register

### Minors (41)

#### 11 · README.bn.md silently drops a whole section and the asset.py demonstration, with no note that it is abridged

`README.bn.md`

Everywhere else the project declares its Bangla gaps at the point of the gap — 11_site/index.html closes with "Bangla appears only where the verified table in 06_type/BANGLA-STANDARD.md holds a string ... those places are listed in this build's output", and the Bangla guidebook chapters carry a {{gap-notice}}. The README pair is the one place that omits without declaring, so a Bangla reader has no way to know a section exists that they were not shown — including the commands for rebuilding the system, which need no translation.

**Still open, 19 August 2026.** Still true, both halves. The Bangla README omits the whole "Rebuild everything" section — the 13-generator chain, the Figma bundle command and the three deliberately excluded generators — and the asset.py refusal demonstration, with no declaration of the gap, in a project whose stated practice is to name a Bangla gap at the point of the gap. The omitted commands are shell lines needing no translation.

*How that was checked.* `grep -n '^#' README.md` → `27 ## The one thing to understand`, `50 ## What is in here`, `64 ## Try it in one minute`, `92 ## Rebuild everything`, `123 ## What this does not do`, `144 ## Licence`. `grep -n '^#' README.bn.md` → `20 ## মূল কথাটা`, `42 ## এখানে কী আছে`, `55 ## শুরু করতে`, `71 ## যা এই পদ্ধতি করে না`, `84 ## লাইসেন্স` — no counterpart to "Rebuild everything". `grep -n asset.py README.md README.bn.md` → only `README.md:80`. Code fences: README.md has four (lines 71, 79, 97, 114), README.bn.md has one (line 63). Reading README.bn.md lines 1-95 in full, its only English notice is the "Not published yet" registry paragraph; there is no note that the file is abridged.

*Smallest fix.* In scripts/readme.py, emit the same rebuild code block in the Bangla README under a one-line Bangla heading, or add a short Bangla note at the omission point saying the section exists in the English README.

#### 12 · Outstanding, not a defect: the Claude Design push has not been done; the local side is ready and only the push remains

`08_components/cards`

This is the one requested artefact with no local work left. What remains is the push itself: pick or create a design-system project, finalize a plan covering 08_components/cards/**/*.html, upload the 30 files, and let the pane build its card index from the @dsCard markers (the three groups are already Foundations 6, Components 16, Patterns 8). Worth recording so it is not mistaken for a build gap — and worth doing before the 30 cards move again, since nothing will tell you the remote copy has fallen behind.

**Half stale, 25 August 2026.** Two of its three claims are now false and one still reproduces. The push happened and the remote copy is current — measured today, not taken from the commit message. The README pair now names the bundle. What still reproduces is narrower than it was: the two surfaces a non-developer actually reads, the site and the guidebook, still do not mention that this deliverable exists.

*How that was checked.* Push half, now closed. `DesignSync list_projects` returns **Aninda Studio Design System**, owned, updated 2026-08-19T07:47:14Z. `DesignSync list_files` on it returned 48 paths; `find dist -type f` returns 48; sorted and compared with `comm`, neither side holds a path the other lacks. `DesignSync get_file readme.md` against `dist/readme.md` under `cmp`: identical byte for byte, sha256 4809caa13c81633088265745bb208a53cf40623a38f103d522a2835ca222c3dc on both sides. That is now written down in 13_plugins/claude-design/PUSH-RECORD.md, which also states the limit — one file was compared, not 48. Naming half, half closed. `grep -n '13_plugins' README.md README.bn.md` → `README.md:66 | \u006013_plugins/\u0060 | A Figma plugin, a Claude Code plugin, and the Claude Design bundle |` and its Bangla twin at README.bn.md:53; the wording changed in commit 66fc0f7, one commit before this register was last regenerated, and the register kept the stale claim anyway. Still true: `grep -c -i 'claude design' 11_site/index.html 09_guidebook/Aninda-Studio-Guidebook.html` → `0` and `0`. Re-pushed on 25 August 2026 after the bundle grew to 50 files; the path sets match again, verified with list_files against find.

*Smallest fix.* Name the Claude Design bundle where the guidebook and the site list what ships, or decide it is a developer surface that neither should carry and record that decision. Either closes this; leaving it undecided is what keeps it open.

#### 14 · pypdfium2 is a pinned dependency imported by the PDF verifier but is missing from TOOLCHAIN.md's package table

`00_sandbox/TOOLCHAIN.md`

The one dependency omitted from the toolchain document is the one that backs a verification claim ("no page is blank — every page is rendered with pypdfium2 and its pixels sampled"). A reader auditing the build from TOOLCHAIN.md alone gets an incomplete dependency and licence list, and the file's closing assurance about "every package above" silently excludes it.

**Still open, 19 August 2026.** Still true, and worse than the record states. pypdfium2 is not merely undocumented: it is the single omission from a ten-package list, it is the dependency that backs the guidebook's blank-page verification claim, and it is the only dependency in the build whose licence is a bundle (BSD-3-Clause plus Apache-2.0 plus CC-BY-4.0 plus vendored PDFium/abseil notices) rather than one line. Anyone auditing the licence surface from TOOLCHAIN.md alone misses precisely the entry that needed the most care.

*How that was checked.* Pinned: `cat requirements.txt` → line 9 "pypdfium2==5.13.0". Imported: `grep -rn -i pypdfium ...` → "09_guidebook/scripts/pdf.py:154: import pypdfium2 as pdfium", and the docstring at pdf.py:43 leans on it — "4. no page is blank — every page is rendered with pypdfium2 and its pixels".

Absent from the table: the TOOLCHAIN.md grep returned no TOOLCHAIN.md line for pypdfium. Confirmed by differencing every requirement against the document:
`while read -r line; do pkg="${line%%==*}"; grep -qi "\`$pkg\`" 00_sandbox/TOOLCHAIN.md || echo "MISSING from TOOLCHAIN.md: $line"; done < requirements.txt` → "MISSING from TOOLCHAIN.md: pypdfium2==5.13.0" and nothing else. It is the only one of the ten requirements omitted.

Sharper than recorded — it is also the licence-heaviest entry. `grep -iE "^License|Classifier: License" .venv/lib/python3.13/site-packages/pypdfium2*.dist-info/METADATA` → "License: BSD-3-Clause, Apache-2.0, dependency licenses", plus "License-File: LICENSES/CC-BY-4.0.txt" and bundled third-party files such as "License-File: data/darwin_arm64/BUILD_LICENSES/abseil.txt". Every listed package in TOOLCHAIN.md carries a single simple licence; the one omitted is the multi-licence bundle.

TOOLCHAIN.md still closes the section with "**Nothing failed to install.** Every package above resolved to a pre-built wheel" — an assurance whose scope silently excludes it.

*Smallest fix.* Add a `pypdfium2` / 5.13.0 row to the Python table in TOOLCHAIN.md, giving its licence as the bundle it actually is and its job as rendering each PDF page to pixels so the blank-page check is a measurement.

#### 15 · pdf.py records a probe measurement of 55 pages; re-running the documented probe today gives 58

`09_guidebook/scripts/pdf.py`

The docstring's whole point is that "the reason for the two-file split stays a measurement rather than a memory", and it has become a memory — the recorded page count no longer matches what the script reports. The MB/MiB mislabelling means the repository states two different sizes for the same PDF and the same HTML file in its two most-read technical documents, with no way for a reader to tell which convention is meant.

**Still open, 19 August 2026.** Still true. I could not re-measure the 55 itself without writing a PDF, which is out of bounds here — but I did not need to: two of the three numbers in the same recorded sentence are reproducibly wrong (13.6 MB input is now 14.3 MB, the 1.4 MB print PDF is now 1.7 MB by the script's own formatter), which proves the whole measurement block describes a superseded state of the document. The comment's own escape clause, "Re-run the probe after the kit grows", has been triggered and not acted on: pdf.py has not been touched since the 1.0.0 commit. This is an internal source comment, not reader-facing, which is the only reason it is not worse.

*How that was checked.* The comment is unchanged. `sed -n '46,50p' 09_guidebook/scripts/pdf.py` → "memory. As at 15 August 2026, at 13.6 MB, it printed: 55 pages, none blank, a / 14.2 MB PDF against the print build's 1.4 MB, with the page breaks in the wrong places. ... Re-run the probe after the kit grows."

Unchanged since the initial release: `git log --oneline -- 09_guidebook/scripts/pdf.py` → one commit only, "e418bcc Aninda Studio 1.0.0 …"; `git diff --stat HEAD -- 09_guidebook/scripts/pdf.py` → empty.

I could not re-run the probe read-only — `probe_interactive()` calls `render_pdf(INTERACTIVE_HTML, PROBE_PDF, …)`, which writes 09_guidebook/_probe-interactive.pdf (absent: "ls: 09_guidebook/_probe-interactive.pdf: No such file or directory"), and OUT_PDF is rewritten before the probe is reached. So I reasoned from source and measured the inputs instead.

Two of the three figures in that one sentence reproduce as WRONG, using the script's own `fmt_bytes` (pdf.py:82-87, `f"{n / (1024*1024):.1f} MB"`):
 · the probe's input, "at 13.6 MB": `stat -f %z 09_guidebook/Aninda-Studio-Guidebook.html` → 15024974 bytes = 14.3 MB.
 · "the print build's 1.4 MB": `stat -f %z 09_guidebook/Aninda-Studio-Guidebook.pdf` → 1791468 bytes = 1.7 MB.
For scale, the current print PDF is far larger than the recorded era: `pypdfium2.PdfDocument(...)` → "print-build PDF pages = 76".

*Smallest fix.* Re-run `pdf.py --probe-interactive` and replace all three figures, or drop the numbers and keep only the instruction to re-run the probe.

#### 19 · 07_tokens/build.py's proof check ignores its own `proof` argument and compares two numbers the generator guarantees agree

`07_tokens/build.py`

The docstring promises two things the code does not do — re-reading, and comparison against the proof — and the ratio assertion is structurally incapable of failing on any output this generator produces. It reads as independent verification and is not. Either re-derive the ratio from the two hexes with the same formula the engine uses, or delete the claim; the component and site harnesses are the only places contrast is actually re-measured.

**Still open, 19 August 2026.** 07_tokens/build.py:510 `check(files, proof)` never touches `proof`, so the one thing that argument could uniquely verify — that emitted token values still equal the measured proof they claim to come from — is not verified; an emitter that fabricated a hex would be reported clean.

*How that was checked.* AST scan of the current file: `python -c` over `ast.parse(open('07_tokens/build.py'))` printed "def check at line 510 args: ['files', 'proof']" and "param 'proof' referenced in body: False" — the Name list for the whole function body contains no `proof`. Consequence proved in an isolated scratchpad copy (repo untouched) by monkeypatching the emitter in memory so it disagreed with the proof: "proof says ground.50 = #F2F9F7 / emitted ground.50 = #FF00FF / check(files, proof) problems: []". The only in-file use of the word is the string key `tok["$extensions"][NS]["proof"]` at line 656, which reads the token's own copy, not the argument.

*Smallest fix.* In `check()`, walk the primitive ramps and semantic roles and compare each emitted `$value["hex"]` against `proof["families"][fam]["ramp"][step]` and `proof["themes"][t]["roles"][name]["value"]`, appending a problem on mismatch (or delete the unused parameter if no cross-check is wanted).

#### 2 · Semantic theme files are not resolvable as standalone DTCG documents, and nothing shipped says so

`07_tokens/build/semantic.light.tokens.json`

The kit describes each of these files as DTCG 2025.10 in its own right, and the plugin hands them to a consumer individually. A spec-conformant single-document tool loading semantic.dark.tokens.json gets ten unresolvable references and no instruction telling it what to load alongside. The fix is documentation, not restructuring — one sentence in SKILL.md and the guidebook token chapter saying the semantic files resolve only when merged with primitive.tokens.json — but as shipped a reader has to infer it from the failure.

**Half stale, 19 August 2026.** Half stale: "every colour value is an alias" is now false — 7 of the 18 tokens per theme file carry literal sRGB objects. The other half reproduces exactly: 11 of 18 are `{color.ramp.*}` references whose target group exists only in primitive.tokens.json, so a tool handed one semantic file alone still cannot resolve those 11, and no field in the file tells it which companion file to load.

*How that was checked.* Resolved each semantic file against itself only, in Python: `UNRESOLVABLE within this file alone: 11 of 18 tokens`, listing `.color.ink.default -> {color.ramp.ground.950}`, `.color.accent.default -> {color.ramp.accent.700}`, `.color.status.info -> {color.ramp.info.700}` and eight more. The other 7 are now literal objects: `.color.surface.lowest -> OBJ:#FDFFFE` … `.color.surface.bright -> OBJ:#FFFFFF`. Counted across all four: each of semantic.light/dark/hc-light/hc-dark reports `tokens: 18 | string values: 11 | aliases: 11 | object values: 7`. The alias root really is absent from the semantic files — `[k for k in d['color']]` gives `['surface','ink','line','accent','focus','status']` with no `ramp`, while primitive.tokens.json's colour group is `['ramp']`. 07_tokens/build.py:398 states the rule deliberately: "A semantic token is an alias if and only if its value is bit-identical to a primitive. Anything else is a literal carrying its derivation", and the validation gate at build.py:621 resolves aliases against `prim`, that is, only ever with both files loaded. The same 11 dangling aliases ship in 12_packages/npm/dist/tokens/ and 13_plugins/claude-code/skills/aninda-brand/assets/tokens/ (`tokens 18 aliases 11` each). Nothing in each file's $description or $extensions names primitive.tokens.json as a required companion.

*Smallest fix.* Add one line to each semantic file's `$extensions.studio.aninda` — for example `"requires": "primitive.tokens.json"` — in the generator, so a single-file consumer is told what the 11 aliases need.

#### 20 · engine.py and emit_css.py --check never compare against the committed output, so a hand-edited generated file passes

`05_colour/engine.py`

Five of the seven --check modes in this repository compare against the committed bytes; these two do not, and emit_css.py's message ("CSS re-parsed and matched against source") reads as if it had. Anyone using --check locally as the drift gate — which is what the phrase invites — gets a false pass, and the only thing actually holding the line is one git-diff step in CI. Either compare against disk or reword to "re-verified the freshly generated set".

**Still open, 19 August 2026.** Both --check modes still verify only their in-memory rebuild, so a hand-edited committed artefact passes them (and 07_tokens/build.py has the same hole); CI's regenerate-and-diff job closes the gap, but scripts/verify-all.sh omits that step, so its own claim that a local pass means the same as a green CI run is false for exactly this gate. Separately and outside this finding: `./.venv/bin/python scripts/readme.py --check` currently FAILS on the real tree — "these generators are in the tree but in neither REBUILD_CHAIN nor NOT_IN_CHAIN: 13_plugins/claude-design/build.py".

*How that was checked.* In a scratchpad copy of the tree: after hand-editing the committed 05_colour/generated/estuary.proof.json (ground ramp 50 → "#FF00FF", name → "Estuary TAMPERED"), `engine.py --check` printed "--check: 4 direction(s) verified. Nothing written." exit=0. After hand-editing the committed 07_tokens/css/tokens.css (comment inserted, `--as-space-0` corrupted to #FF00FF; file 9019 → 9072 bytes), `emit_css.py --check` printed "tokens.css 9019 bytes 64 custom properties" then "--check: CSS re-parsed and matched against source. Nothing written." exit=0, and the edit was still on disk. Same hole in 07_tokens/build.py: "--check: 6 files verified, 0 problems" exit=0 while an in-process comparison gave "fresh == committed: False". Source confirms it: neither main() ever reads its OUT path. BUT .github/workflows/ci.yml:104 regenerates and runs `git diff --exit-code 05_colour/generated 07_tokens/build 07_tokens/css`, which does catch it; scripts/verify-all.sh has no equivalent step (its only git-diff guards are for 13_plugins/figma and 13_plugins/claude-code/dist).

*Smallest fix.* Add the CI regenerate-and-diff step (or, better, a disk comparison inside each --check as 12_packages/build.py already does at main()) covering 05_colour/generated, 07_tokens/build and 07_tokens/css to scripts/verify-all.sh.

#### 21 · A malformed direction spec escapes 05_colour/engine.py as a traceback with exit 1, not the documented exit 2

`05_colour/engine.py`

The two exit codes exist so a caller can tell "this palette cannot support the role you asked for" from "I could not read your input" — the distinction the file spends a paragraph justifying. A malformed spec reports the first while meaning the second, and does it as an unhandled traceback. Wrap the family construction in the same NotEquipped conversion the JSON parse already gets.

**Half stale, 19 August 2026.** The guard added since the record covers only the four top-level keys (run() line 604), so those now fail closed with a message; the per-family dict is still indexed raw at engine.py:609, so a family missing label, kind or anchor still escapes as a bare KeyError traceback. Nothing is written and the exit code is non-zero, so CI still goes red — only the diagnostic is wrong.

*How that was checked.* Scratchpad copy of 05_colour with three malformed specs. Top level, spec missing "premise": "COULD NOT RUN — nothing written:\n\n - notop.json is missing 'premise'" exit=2 — fail-closed, as promised. Family level, ground missing "kind": "File .../engine.py, line 609, in run\n kind=f[\"kind\"], anchor=f[\"anchor\"], note=f.get(\"note\", \"\"),\nKeyError: 'kind'" exit=1. Accent missing "anchor": "KeyError: 'anchor'" at the same line. `grep -n "except KeyError"` over engine.py returns nothing.

*Smallest fix.* Inside the `for key, f in spec["families"].items()` loop, check for ("label", "kind", "anchor") and `raise NotEquipped(f"{spec_path.name}: family '{key}' is missing '{req}'")` before constructing Family.

#### 22 · 12_packages/build.py --check writes VERSION to disk while printing "Nothing written"

`12_packages/build.py`

A verify-only mode that mutates the tree is the one thing --check must never do, and CI runs this mode. It also means a missing VERSION is silently resurrected as 1.0.0 rather than reported: if the real version were 2.3.0, the packages would be regenerated against a fabricated version rather than the run failing. Split the read from the create, and have --check report a missing VERSION instead of writing one.

**Still open, 19 August 2026.** The write is still on the --check path: with VERSION absent, a verify-only run creates VERSION at the repo root while printing "Nothing written." Only reachable when VERSION is missing, which the committed tree never is, so it is a broken promise rather than a live corruption.

*How that was checked.* Scratchpad copy: `rm VERSION`, confirmed absent ("No such file or directory"), then `12_packages/build.py --check` printed " ok npm 'aninda-studio-tokens' — 20 files … \n--check: both packages match the source. Nothing written." exit=0 — and afterwards "-rw-r--r-- 1 gru953 staff 6 … /VERSION" containing "1.0.0". Source path: read_version() at line 288 does `VERSION_FILE.write_text("1.0.0\n")`, and build() calls it at line 318, that is, before the --check branch at line 892 can return.

*Smallest fix.* Make read_version() side-effect free — return "1.0.0" (or raise SystemExit naming the missing file) and do the `write_text` only in main()'s write phase, alongside the other writes.

#### 23 · 08_components/check.py drops measureText's "could not measure" list in the forced-colours pass

`08_components/check.py`

The docstring says "The harness prints what it could NOT check at the end. That list is part of the result, not an apology." In forced-colours mode it silently is not: an element whose background cannot be composited is skipped, unmeasured and unreported, so the forced-colours contrast pass can report clean over text it never looked at. One extra loop, matching the main pass.

**Still open, 19 August 2026.** The code defect is unchanged — the forced-colours pass still throws away the problems array, so a text node whose background it cannot composite in that mode is skipped and never reported — but on today's 30 cards that array is empty, so it is currently masking nothing. Latent hole in exactly the pass where compositing is most likely to fail.

*How that was checked.* `grep -c 'text["problems"]' 08_components/check.py` → "1" (line 773, the per-width/per-theme pass). The forced-colours pass at lines 876-884 calls the same `window.__as.measureText(...)` and then consumes only `text["failures"]` — no loop over `text["problems"]` (nor `shouted`, nor `counted`). In the JS a problems entry is pushed with `continue`, so that text node's contrast is never measured. A read-only Playwright probe mirroring the harness's own forced-colours setup over all 30 cards × 4 themes reported: "text nodes measured: 15460 / problems returned but DISCARDED by the forced pass: 0".

*Smallest fix.* In the forced-colours pass, add `for problem in text["problems"]: found.fail(f"{label}: could not measure a background — {problem}")`, mirroring line 773.

#### 24 · 11_site/check.py's external-reference finding is only ever an ok note, never a problem

`11_site/check.py`

"the page works offline" is a stated property of this site, and 11_site/build.py enforces it at build time (lines 1085-1097, `raise BuildError(f"{name} fetches {target} from the network.")`). The browser check, which is the only thing that sees the rendered page, records a violation as a pass and phrases it as reassurance. Make it a problem, or drop the collection so the note cannot be mistaken for enforcement.

**Still open, 19 August 2026.** The external-reference check is still note-only, so it cannot fail a run; an external asset is caught only incidentally, and only when its request fails, which means a reachable CDN font or script would ship with the harness reporting "ok". Nothing external ships on the real page today (only an anindastudio.com link and a mailto), so no reader is affected yet.

*How that was checked.* 11_site/check.py:444 is still `notes.append(f"external references: {s['external'] or 'none — the page works offline'}")` with no matching problems.append. Proved end to end on a scratchpad copy with two external references injected into index.html: the run printed " ok external references: ['https://anindastudio.com/', 'https://cdn.example.com/tracker.js', 'https://fonts.googleapis.com/css2?family=Inter', 'mailto:aninda.sh15@gmail.com']". The 24 FAILs it did report all name cdn.example.com ("failed request https://cdn.example.com/tracker.js", "net::ERR_NAME_NOT_RESOLVED") and come from the unrelated requestfailed/console listeners at lines 262-264; `grep -n googleapis` over the output hit only the ok line, so the Google Fonts stylesheet — an external asset that did not fail to load — produced no problem at all.

*Smallest fix.* After the note, append a problem for any entry in s['external'] whose scheme is http/https and which is a loaded asset (src, rel=stylesheet, rel=preload), while still allowing plain anchor hrefs and mailto:.

#### 25 · 09_guidebook's external-asset guard inspects <source> but its regex cannot see srcset

`09_guidebook/build.py`

A 14 MB self-contained book whose whole promise is that it opens with no network. The guard lists the one element whose entire purpose is the attribute it cannot read, which reads as coverage it does not have. Add `srcset` and `poster` to the attribute alternation.

**Still open, 19 August 2026.** The guard is unchanged and still partial: it inspects seven element names and two attributes, so `<video src>`, `<audio src>`, `srcset`, `poster`, `object data`, `<input type=image src>`, `<track src>`, SVG `use`/`image` `href`, `xlink:href` and CSS `@import` all pass. Nothing in the tree currently exploits the gap, so the "one file, no network" claim happens to be true today — it is merely not proven by this guard, and the interactive build has no behavioural backstop the way the print build does.

*How that was checked.* Read the guard: `09_guidebook/build.py:2933-2946` matches only `(?:src|href)\s*=\s*["'](?:https?:)?//` inside `<(?:img|script|link|source|iframe|object|embed)\b[^>]*>`, plus `url(...)` in CSS. I loaded the real module and fed it synthetic documents (no file written): `./.venv/bin/python` importing `09_guidebook/build.py` and calling `m.guard_no_external({...})` returned:
 NOT CAUGHT: video src / audio src / video poster / img srcset / input image / track src / svg use href / svg image href / xlink:href / css @import / object data
 caught : img src (control)
Note `object data=` escapes even though `<object>` IS in the element list, because `data` is not in the attribute pattern. The compensating behavioural check is print-only: `09_guidebook/scripts/pdf.py:212` calls `render_pdf(PRINT_HTML, OUT_PDF, strict=True)` (fails on any request), but line 185 renders the interactive build with `strict=False` and discards the observation — so the 15 MB file readers download is covered by the regex alone. No live violation: `grep -o -E '<(video|audio|track|input|use|image)\b|srcset=|poster=|xlink:href=|@import'` over both built HTML files returned nothing.

*Smallest fix.* Add video|audio|track|input|use|image to the element list and srcset|poster|data|xlink:href to the attribute pattern plus an `@import` check — or, better, run the interactive build through pdf.py's request observer with strict=True so the claim is measured rather than pattern-matched.

#### 26 · ring_from_diff's `thickness` is not ring thickness, so the 2px focus-ring floor cannot fail for a whole-box change

`08_components/check.py`

A background inversion is a legitimate focus indicator under SC 2.4.13, so the pass is defensible — but the number reported is the control's own size dressed as a ring measurement, which means RING_MIN_PX is dead for any element whose focused appearance differs across its whole box. A focus style that changed the fill and put a border on one side only would report sides [60, 60, 44, 44] and clear the floor with three sides bare. Measure the ring as changed pixels OUTSIDE the element's own box, or rename the figure to what it is.

**Still open, 19 August 2026.** The quantity is a run-length of changed pixels, not a ring thickness, so the docstring line "the changed pixels are checked for a ring at least 2 CSS px thick" is not what the code tests — proven by case C, where no ring at all scores 24. The other half does not reproduce: on every real card the number is exactly 3 and equals the outline width, because the one `:focus` rule in components.css is a 3px outline at 2px offset and nothing else changes. So the defect is latent, not a wrong published number.

*How that was checked.* `08_components/check.py:609` computes `thickness = min(left, right, top, bottom)` where each side is `run(...)` — the count of contiguous changed pixels inward from the diff bounding box along a midline. `git log -L :ring_from_diff:08_components/check.py` shows one commit only, e418bcc (initial), so nothing was changed after the review. I called the harness's own function on synthetic before/after buffers:
 A clean 3px ring, 2px offset -> {'thickness': 3, 'sides': [3,3,3,3]}
 B 1px ring + fill change (contiguous) -> {'thickness': 24, 'sides': [40,40,24,24]}
 C no ring, fill change only -> {'thickness': 24, 'sides': [40,40,24,24]}
 D 3px ring + one stray pixel -> {'thickness': 0, 'sides': [0,3,0,3]}
Case C is the important one: an element with NO focus ring that merely repaints its background reports 24 px and clears the `RING_MIN_PX = 2` floor. I also drove real Chromium (PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers) over `08_components/cards/components/button.html` with the harness's pad of 8 and its own `ring_from_diff`: every button returned `thickness 3, sides [3,3,3,3]`, matching `--as-focus-ring-width: 3px`. The full harness run `check.py --only button --widths 1280` printed "40 focus rings" and "PASS".

*Smallest fix.* Before trusting the runs, assert the changed pixels form a hollow band (interior unchanged) and fail with "no ring — only a fill change" otherwise; and start each run from the extreme pixel ON the midline rather than from the bounding box, so one stray changed pixel cannot zero the reading.

#### 27 · engine.py's header states the perturbation sweep is 64 measurements; it is 729

`05_colour/engine.py`

This paragraph is the file's own account of its central method, quoted onward into 07_tokens/build.py's generated $description text ("nudged by ±1. The published figure is the worst of those"). The measurement is stronger than the number claimed, so the error is in the safe direction, but it is the kind of unverified stated fact this repository otherwise refuses to ship.

**Still open, 19 August 2026.** Still 729 and still documented as 64. Contained to the engine's own header comment — no reader-facing copy carries the number — but it is a factual error in the file whose stated purpose is that nothing is asserted without measurement.

*How that was checked.* `sed -n 18,18p 05_colour/engine.py` returns: "with each channel of both colours nudged by ±1 — the worst of those 64 results". Importing the module and counting: `len(_neighbours('#278492')) = 27, unique = 27`, and `worst_case_ratio` is `min(ratio(f, b) for f in _neighbours(fg) for b in _neighbours(bg))`, so `pairs compared = 27*27 = 729`. The helper's own docstring at line 184 is correct ("27 values"); only the header is wrong. `grep -rn "those 64"` over the tree matches exactly one line, 05_colour/engine.py:18, so the wrong figure is not repeated in any README, the site or the guidebook.

*Smallest fix.* Change "those 64 results" to "those 729 results (27 neighbours of each colour)" on 05_colour/engine.py:18.

#### 28 · scripts/readme.py walks the entire repository to compute a figure neither README uses, and prints it as a counted fact

`scripts/readme.py`

Every line of the --check output reads as "this number in the README was verified against the thing it describes". One of the eighteen is asserted nowhere, is derived from the working tree rather than the repository, and costs a full recursive walk. It invites the reader to trust a figure that is not under any guard.


---

## From round 2

Same judgement as above: real, reproducible, not affecting the correctness of the
system's output. Recorded rather than dropped.

**Still open, 19 August 2026.** All three parts hold: the fact is computed, is never asserted in either README, and is derived from the working tree — it counts 35 untracked files including .DS_Store while excluding tracked `candidates/` paths, giving 428 against git's 461. The cost claim is the weak part: the walk takes 0.08 s, so "costs a full recursive walk" is true but negligible. Separately and more urgently, readme.py --check is failing outright on the new claude-design generator.

*How that was checked.* `grep -n files scripts/readme.py` shows `f["files"]` assigned once, at line 238, and read nowhere: the only other hits are `git ls-files` comments, the unrelated `{f['marks']} … files` table cell, and the local `files = {ROOT / "README.md": …}` dict. There is no `**f` or `format(**f)` — both templates are plain f-strings — so an unread key cannot reach either README. The basis is the working tree, not the repository: I ran the exact expression from line 238 and compared it with git — "rglob count = 428 in 0.08s / git ls-files count = 461 / counted but NOT tracked = 35 / examples: ['.DS_Store', '04_mark/.DS_Store', '09_guidebook/.DS_Store', …]". The same file explains at line 155 why this is wrong: "`git ls-files` rather than rglob, because rglob also walks ignored trees". The figure is not entirely invisible — line 536 prints every fact as `counted {k} {v}` to the operator's console. Incidental blocker found while running it: `./.venv/bin/python scripts/readme.py --check` exits 1 with "these generators are in the tree but in neither REBUILD_CHAIN nor NOT_IN_CHAIN: 13_plugins/claude-design/build.py", so neither README can currently be regenerated or verified.

*Smallest fix.* Delete line 238; if the figure is wanted, count it from the `git ls-files` output that check_rebuild_chain already fetches and actually print it in the READMEs. Then add 13_plugins/claude-design/build.py to REBUILD_CHAIN or NOT_IN_CHAIN so --check can run at all.

#### 3 · Reserved-Font-Name family count is wrong in two research documents that label the figure as mechanically extracted

`06_type/SHORTLIST.md`

Both documents mark this figure **[file]**, the repository's own convention for "read directly out of the font file, reproduce with 06_type/specimen.py", which invites the reader to trust it without rechecking. The count is the one that decides whether a family can be subsetted without renaming, so a reader picking a substitute face from the shortlist could take a Plex or Source family as RFN-free. It contradicts the table printed three lines above it.

**Still open, 19 August 2026.** Still open in both documents, and both are now contradicted by the repo's own machine-extracted 06_type/_data/font_facts.json, which says 6 families. SHORTLIST.md's "other 26" should be 24; RECOMMENDATION.md's "Four of the shortlisted families" conflates four reserved names with six families.

*How that was checked.* Ground truth from the licences shipped in the tree: `grep -rl "with Reserved Font Name" 06_type/candidates/` returns exactly 6 files — bangla/galada, bangla/mina, latin/ibmplexsans, latin/sourcesans3, mono/ibmplexmono, mono/sourcecodepro — while `ls -d 06_type/candidates/*/*/ | wc -l` is 30 and `ls 06_type/candidates/*/*/OFL.txt | wc -l` is 30. The repo's own generated data agrees: reading 06_type/_data/font_facts.json gives `families in font_facts: 30` and `carrying an RFN: 6 ['ibmplexsans', 'sourcesans3', 'galada', 'mina', 'ibmplexmono', 'sourcecodepro']`. Both documents still contradict that. 06_type/SHORTLIST.md:65: "**The other 26 families carry no Reserved Font Name at all.**" — 30 − 6 = 24, not 26. 06_type/RECOMMENDATION.md:76: "Four of the shortlisted families carry one (`Plex`, `Source`, `Lobster`, `Exo`)" — four is the number of distinct reserved names, not of families; six families carry them. SHORTLIST.md contradicts itself in place: the table immediately above line 65 lists six family names across its four rows. No guard covers it — scripts/check_licence_claims.py checks only the "Plex" string, the PolyForm URL and the two package names, and scripts/check_measurements.py mentions families only at line 111 ("there are 20 families to find").

*Smallest fix.* Change SHORTLIST.md:65 to "other 24" and RECOMMENDATION.md:76 to "Six of the shortlisted families carry one of four reserved names" — or better, have the generator derive both figures from the `rfn` field in 06_type/_data/font_facts.json.

#### 4 · The $schema every token file declares resolves to the DTCG living draft, not the 2025.10 report the same file pins

`07_tokens/build/primitive.tokens.json`

The files go to unusual lengths to distinguish the frozen 2025.10 report from the moving draft — it is the point of the `spec` extension string and of BENCHMARK section 6.2 — and then the machine-readable field points at the moving one. Anything that dereferences `$schema` to decide which rules to apply lands on the 30 July 2026 draft, whose requirements can diverge from the version the file claims. Pinning `https://www.designtokens.org/TR/2025.10/format/` would make the two agree; leaving it as is means the version claim survives only in prose a tool is permitted to ignore.

**Still open, 19 August 2026.** Still open: the declared $schema is the DTCG prose specification (a ReSpec HTML page), not a JSON Schema document, so no validator can dereference it, and it ships on 25 JSON files plus the Figma bundle — including the copies inside the npm, Python and plugin packages a consumer would feed to a validator.

*How that was checked.* `grep -rho '"\$schema": "[^"]*"' --include="*.json"` over the tree returns a single distinct value, 25 times: `"$schema": "https://tr.designtokens.org/format/"` (set at 07_tokens/build.py:72, `SCHEMA = "https://tr.designtokens.org/format/"`), and it is also baked into 13_plugins/figma/dist/code.js and 13_plugins/figma/src/tokens.generated.ts. Dereferenced the URL: `curl -sS -L -o /dev/null -w "status=%{http_code} type=%{content_type} url=%{url_effective}"` returned `status=200 type=text/html; charset=UTF-8 url=https://www.designtokens.org/tr/drafts/format/`, and the body begins `<!DOCTYPE html><html lang="en"><head>… <meta name="generator" content="ReSpec 37.1.0">` with `<title>Design Tokens Format Module 2025.10</title>`. Requesting it with `Accept: application/schema+json, application/json` returns the same HTML. Checked 19 August 2026. No comment near build.py:72 qualifies the claim.

*Smallest fix.* Either drop the `$schema` key from the generator, or point it at a real JSON Schema file shipped in 07_tokens/ and say in the file's $description that the DTCG URL is the prose spec, not a schema.

#### 5 · README.bn.md mixes Bengali and Western numerals inside single sentences, against house rule 9 of the Bangla standard

`README.bn.md`

The Bangla README is one of two front doors to the project and the main demonstration that the Bangla is written as Bangla rather than translated. Two numeral systems inside one sentence is the most visible possible signal that the Bangla was assembled rather than written, and it lands in the paragraph whose whole point is that the numbers are trustworthy. It also breaks a rule the project itself researched, sourced and wrote down.

**Still open, 19 August 2026.** Still open. Every number read from the tree is interpolated as Western digits directly next to the hand-typed Bengali ones — the same sentence carries `5.3348:1` and `৪.৫:১`. README.bn.md is generated, so hand-editing it would be overwritten; the fix belongs in scripts/readme.py.

*How that was checked.* House rule quoted from 06_type/BANGLA-STANDARD.md:421: "9. **Bengali numerals** in prose and measurements; Western digits only where a string must be copied literally." README.bn.md breaks it inside single sentences. Line 24: "4টি থিমে মোট **44টি জোড়া** আছে" — Western 4 and 44 — two lines above "মাপা হয়েছে সেই ৮-বিট হেক্স মানে" (Bengali ৮). Lines 30-31, in one sentence pair: "লেখার জন্য 28টি জোড়া। সবচেয়ে কম **5.3348:1** — সাধারণ থিমে সীমা ৪.৫:১, বেশি কনট্রাস্টে ৭:১।" — Western `28` and `5.3348:1` beside Bengali `৪.৫:১` and `৭:১`. Lines 32-33 repeat it: "লেখা ছাড়া 12টি জোড়া … **3.8134:1** — সীমা ৩:১।" Also line 46 ("14টি অধ্যায়", "15.0 মেগাবাইট", "1.8 মেগাবাইটের PDF") and lines 47-50 (64টি, 30টি, 10টি, 20টি). Cause is in the generator, not the file: scripts/readme.py:444-447 reads `- **লেখার জন্য {f['n_text']}টি জোড়া।** সবচেয়ে কম **{f['worst_text']}:1** — সাধারণ থিমে সীমা ৪.৫:১, বেশি কনট্রাস্টে ৭:১।`, and `grep -n "numeral" scripts/readme.py` returns nothing — there is no digit-conversion step anywhere in `bangla()`.

*Smallest fix.* Add a one-line `bn_digits()` translation helper in scripts/readme.py and wrap every `{f[...]}` interpolation inside `bangla()` (including the `:1` of each ratio) with it.

#### 6 · The plugin reference file that documents the mark is named logo.md, the one word the plugin's own naming rule forbids for it

`13_plugins/claude-code/skills/aninda-brand/references/naming.md`

This is the exact failure the naming rule was written to prevent, in the artefact whose job is to teach the rule. An agent or a person reading SKILL.md is told to open references/logo.md to learn that the thing is never called a logo, and SKILL.md's own description offers 'a logo' and 'mark' as two different things you might ask for. Because check_plugin.py hard-requires the filename, the wrong name is now pinned in place by CI.

**Still open, 19 August 2026.** Still open, unchanged, and now shipped inside dist/aninda-brand.skill: the file teaching that the thing is never called a logo is itself called logo.md, and check_plugin.py holds the wrong name in place — a rename without touching line 35 would fail CI.

*How that was checked.* `ls 13_plugins/claude-code/skills/aninda-brand/references/` still shows `logo.md` (3999 bytes, 18 Aug), whose own H1 is `# The mark and the wordmark`. The rule it breaks is in the sibling file, naming.md:5-6: "One name for one thing, everywhere. If it is the *mark*, it is never also the *logo* in a different paragraph", and its table row reads `| **mark** | The `a` glyph on its own | logo, icon, symbol, logomark |`. naming.md's single stated exception does not cover it: "**One exception, and it is deliberate: platform-facing FILENAMES follow the platform's word**", naming favicon.ico, avatar-512.png and linkedin-company-logo.png — a skill reference document has no platform asking for the word. The name is pinned by CI: 13_plugins/claude-code/scripts/check_plugin.py:35 hard-lists it in `BRAND_REFERENCES = ("colour", "typography", "layout", "logo", "icons", …)`. Two files point readers at it — SKILL.md:51 `| The mark, the wordmark, clear space | `references/logo.md` |` and icons.md:8 "see `references/logo.md`" — and it ships in the built bundle: reading 13_plugins/claude-code/dist/aninda-brand.skill lists `references/logo.md` alongside `references/naming.md`. SKILL.md's description also still offers "a logo, mark, icon" as separate things and both `"the mark"` and `"the logo"` as triggers.

*Smallest fix.* Rename references/logo.md to references/mark.md and update the three places that name it: check_plugin.py:35, SKILL.md:51 and icons.md:8, then rebuild the .skill bundle.

#### 7 · The wordmark ships set in lowercase while the chapter that presents it says "Sentence case, always", with nothing reconciling the two

`09_guidebook/chapters/02-the-name.md`

The chapter's own second section is titled "The one thing that looks like an inconsistency, and is not", and it spends five sentences explaining the অনিন্দ্য/aninda transliteration gap so that nobody has to wonder. The casing gap gets none of that treatment: a reader sees lowercase artwork at the top of the page and an unqualified "Sentence case, always" twenty-six lines below, with no row in the table and no note. Anyone setting the name in a lockup has to guess which of the two governs, and the earlier draft shows the distinction was understood and then lost.

**Still open, 19 August 2026.** Still true today and unchanged in substance: the artwork is drawn from the literal string "aninda studio", the chapter prints "Aninda Studio" and states "Sentence case, always" twenty-six lines below the lowercase figure, and no sentence in the book, the mark folder or the plugin references says the artwork's casing is a drawn letterform rather than a breach of the rule.

*How that was checked.* `grep -n 'WORD_LATIN' 04_mark/build.py` → `92:WORD_LATIN = "aninda studio"`, and the shipped artwork's own title is `<title>Aninda Studio — wordmark, aninda studio</title>` (04_mark/svg/wordmark-latin.svg). The chapter that presents it writes the name capitalised and gives an unqualified rule: 09_guidebook/chapters/02-the-name.md line 3 `The studio is called **Aninda Studio** in English`, the table row `| Full name, English | Aninda Studio |`, and line 33 `Sentence case, always. Not ANINDA STUDIO, not Aninda STUDIO.` Nothing reconciles the two: `grep -c lowercase 09_guidebook/Aninda-Studio-Guidebook.html` → `1`, and that one hit is line 1861, chapter 03 describing the mark as `a lowercase` 'd' — not the wordmark. `grep -rn -i 'lowercase|lower case' 09_guidebook/chapters 04_mark README.md README.bn.md` returns only that line plus a comment in 04_mark/build.py. The chapter's table has no wordmark row, and 13_plugins/claude-code/skills/aninda-brand/references/naming.md mentions lowercase only for repo, package and plugin names.

*Smallest fix.* Add one row to the chapter's "How to write it" table — the wordmark artwork is drawn lowercase, the rule governs text rather than the drawing — or one sentence to that effect under the figure.

#### R2-11 · The site header's brand lockup loses its tile in both dark themes: the icon's baked-in ground measures 1.05:1 against the page it sits on

`11_site/index.html`

The primary lockup on the studio's front door reads as two different marks depending on theme — a rounded dark tile with a knocked-out 'a' in the two light themes, a bare floating 'a' in the two dark ones — on a site whose own theme switcher makes all four first-class. The mark stays legible, which is why this is minor, and the icon is fixed artwork by policy, but nothing shipped says the header deliberately keeps a fixed ground, so a reader comparing the header against the marks card's stated rule finds them disagreeing. The site's contrast harness cannot catch it: the icon is aria-hidden and the site's claim is scoped to "the contrast of every piece of text".

**Still open, 19 August 2026.** Reproduced. The tile ground sits at 1.07:1 (dark) and 1.10:1 (dark high contrast) against the page it is drawn on, which is imperceptible, so in two of the four themes the header shows a bare white ring-and-bar instead of an app-icon tile. The literal-colour guard at 11_site/build.py:303 explicitly whitelists these three literals as a declared exception and never measures the tile against the page, so no guard covers this.

*How that was checked.* 11_site/index.html line 57 ships the header lockup as <span class="site-brand__mark"><svg …><rect width="100" height="100" rx="24" ry="24" fill="#0D1A17"/>…, produced by read_mark("icon-192.svg", …) at 11_site/build.py:1115 and :1139 (so index.html and 404.html both). The page ground is .as-root { background-color: var(--as-surface-low) } at 11_site/styles.css:392. Computing WCAG contrast of the tile against that token in each theme (07_tokens/css/tokens.css): light #FBFCFC → 17.356:1; dark #0E100F → 1.071:1; hc-light #FAFAFA → 17.090:1; hc-dark #0C0C0C → 1.097:1. Against every dark surface token the range is 1.037–1.156:1, and #111212 gives exactly 1.052:1, which is the 1.05 figure recorded. grep for "rect|site-brand__mark" in styles.css shows only sizing rules (lines 1465–1466) — nothing recolours or hides the rect per theme. The white glyph on the tile is 17.84:1, so the mark is visible; the tile is not.

*Smallest fix.* Draw the header lockup from the recolourable mark (currentColor, no baked rect) instead of the fixed-colour icon-192.svg master, or give .site-brand__mark a token-driven tile background and drop the baked rect.

#### R2-12 · The token files name a ramp "family", the one word the naming reference forbids for it

`07_tokens/build/semantic.light.tokens.json`

One thing carries two names inside the same shipped file — `ramp` in the token path and `family` in the extension on the leaf beside it — and the second is the word the project's own naming authority names as wrong. A consumer reading $extensions.studio.aninda to group roles by ramp has to learn that `family` means `ramp`, which is the exact cost the naming rule exists to avoid. It is minor because the key is machine-readable rather than prose, and because nothing breaks; it is worth recording because naming.md is enforced nowhere and this is the one place its vocabulary table is contradicted by generated output rather than by prose.

**Still open, 19 August 2026.** Reproduced, and wider than recorded: the key now ships in the npm package, the Python package, the plugin skill assets and the colour proofs as well as 07_tokens/build. The extension names a ramp 'family' — the exact word the kit's own naming reference forbids for it — while the sibling key 'step' does follow the reference. (The unrelated 'family' keys for fontFamily at build.py:134–146 are correct; a font family really is a family.)

*How that was checked.* 13_plugins/claude-code/skills/aninda-brand/references/naming.md:32 reads: | **ramp** | A primitive scale of eleven steps | palette, family | — the third column is the never-use list. Walking 07_tokens/build/semantic.light.tokens.json for 'family' keys returns 11 hits, all under $extensions/studio.aninda, for example /color/ink/default/$extensions/studio.aninda -> "ground", and sed -n 145,160p shows "family": "ground", "step": 950 side by side. primitive.tokens.json confirms 'ground' is a ramp: list(d['color']['ramp'].keys()) → ['ground', 'accent', 'success', 'warning', 'danger', 'info']. The emitter is 07_tokens/build.py:384, "family": r["family"]. A tree grep for '"family"' finds it shipped in all four semantic token files, all four 05_colour/generated/*.proof.json, 12_packages/npm/dist/tokens/*, 12_packages/python/src/aninda_studio_tokens/data/tokens/* and 13_plugins/claude-code/skills/aninda-brand/assets/tokens/*.

*Smallest fix.* Rename the extension key from "family" to "ramp" in 07_tokens/build.py:384 and 05_colour/engine.py:422/:504, then regenerate the tokens, proofs and the two packages.

#### R2-13 · 07_tokens/build.py's $schema check compares the emitted document against the constant that wrote it, so it is structurally incapable of failing

`07_tokens/build.py`

It reads as a conformance check on the one machine-readable field that tells a consuming tool which rules to apply, and it can never report anything. This is the same shape as the already-recorded finding 19 about the proof-ratio assertion, but a different check that OPEN-FINDINGS.md does not cover, and the two together mean two of check()'s gates are tautologies inside a function whose docstring is "Re-read what was built and prove it, rather than trusting that it was built." The only thing standing between a wrong $schema and a release is the CI git-diff, which reports that bytes changed without knowing why.

**Still open, 19 August 2026.** Reproduced exactly as recorded. Both sides of the comparison are the same module-level constant, so the branch cannot be taken by any input; the check's docstring claim to "re-read what was built" is not what the code does. Practical exposure is limited — a hand-edit to the committed JSON would still be caught by CI's `git diff --exit-code 07_tokens/build` step — but the check itself measures nothing.

*How that was checked.* 07_tokens/build.py:72 defines SCHEMA = "https://tr.designtokens.org/format/". The only two document constructors set it from that constant: line 237 (primitives) and line 408 (semantic), each `"$schema": SCHEMA,`. main() at line 674–676 does `proof = json.loads(PROOF.read_text())` / `files = emit(proof)` / `problems = check(files, proof)` — check() is handed the in-memory dicts emit() merely built, never the files on disk. check() then asserts at line 533–534: `if doc.get("$schema") != SCHEMA: problems.append(f"{name}: wrong or missing $schema")`. emit() (line 501) produces only those two constructors' output plus forced-colors.map.json, which line 531 skips by name.

*Smallest fix.* Have check() load the committed files from OUT with json.loads and compare their $schema against the literal DTCG URL, or drop the tautological branch and say plainly that the drift guard covers it.

#### R2-14 · 11_site/check.py's reduced-motion check reports "reduced motion honoured" and exits 0 when the property it measures does not exist at all

`11_site/check.py`

This harness exists because "build.py can only prove that the site was WRITTEN correctly. This proves it BEHAVES correctly." Reporting a measurement as honoured when the measured value is absent is the same shape as the already-fixed bug where the site's stylesheet never loaded and no check noticed: a note that reads as reassurance about something the script never saw. The nearby forced-colours check gets this right — it probes for liveness first and refuses to pass if the emulation is inert — so the pattern for handling "I could not see it" already exists in the same file, eleven lines above.

**Still open, 19 August 2026.** Reproduced as a logic defect: an absent property yields '', which is falsy, so control falls to the success branch, and the note's own `{d or 'unset'}` prints the word 'unset' while still calling it honoured. The token does exist today, so the check is not currently masking a real regression — but rename or drop --as-duration-move and the harness reports a green pass on motion it never measured.

*How that was checked.* 11_site/check.py:404–410 reads: d = pg.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--as-duration-move').trim()") / `if d and not d.startswith(("1ms", "0")): problems.append(...)` / `else: notes.append(f"reduced motion honoured (move duration {d or 'unset'})")`. I drove the identical expression with the pinned Chromium against a page that does not define the property: returned value = '' , truthiness = False, BRANCH -> note appended: "reduced motion honoured (move duration unset)". A real run today prints "ok reduced motion honoured (move duration 1ms)" and "8 checks passed, 0 failed", because 11_site/styles.css:57 and :292 do currently define --as-duration-move (220ms, and 1ms under @media (prefers-reduced-motion: reduce)). grep -rn "as-duration-move" over 11_site/*.py and 07_tokens/*.py returns only check.py:406 — nothing anywhere asserts the property exists.

*Smallest fix.* Fail when d is empty: treat a missing --as-duration-move as a problem in its own right, for example `if not d: problems.append("--as-duration-move is not defined; the reduced-motion check measured nothing")` before the value test.

#### R2-15 · 05_colour/engine.py's documented exit-1 failure — a palette that cannot support a role — is unreachable, and its remedy names an input that provably cannot change the outcome

`05_colour/engine.py`

The file spends a paragraph justifying the 1-versus-2 exit-code split, and the meaning it gives to 1 is "a real failure — a palette cannot support a role". That is the branch a reader is told to expect when a direction is unbuildable, and it is the one branch that no direction spec can produce. Worse, the message instructs the reader to change the anchor, which alters only hue and chroma while the outcome depends entirely on lightness — so a reader who somehow reached it would be sent to the wrong file. Either derive the ramp's lightness from the anchor as well, or state plainly that a direction spec cannot fail a contrast target and that this branch guards against a future change to LIGHTNESS.

**Still open, 19 August 2026.** Still open, and sharper than recorded: pick()'s Fail — the one the exit-1 line describes — cannot fire for any spec, because the lightness ladder is a module constant and the anchor supplies only hue and chroma. The extreme ramp step clears at least 10.08:1 against the worst surface the engine may build, versus a 7.0 maximum target.

*How that was checked.* Docstring at 05_colour/engine.py:43-46 still promises: "EXIT CODES ... 1 a real failure — a palette cannot support a role". main() (lines 679-693) returns 1 only when a Fail propagates out of run(). Fail and NotEquipped are independent Exception subclasses (lines 150-156), so the routing is correct — but no direction spec can raise Fail. Family.build() (lines 240-257) takes ONLY hue and chroma from the anchor: `self.hue = ...a['hue']`, `self.chroma_ceiling = self.max_chroma if ... else float(a['chroma'])`, then `self.ramp[s] = to_hex(Color('oklch', [LIGHTNESS[s], self.chroma_ceiling * CHROMA_ARC[s], self.hue]))`. LIGHTNESS is a hard-coded constant dict (lines 89-92); the anchor's own lightness is discarded. Ran run() directly on five pathological specs written to the scratchpad (repo untouched): 'accent near-white zero chroma -> no exception (exit 0)', 'accent max chroma 0.4 yellow -> no exception (exit 0)', 'ground pure white -> no exception (exit 0)', 'ground max chroma 0.5 -> no exception (exit 0)', 'everything grey zero chroma -> no exception (exit 0)'. Structural bound over 36 hues x 4 chroma multipliers, extreme ramp step vs the least favourable legally-permitted surface in each polarity: 'light: 10.9054', 'dark: 10.0799', 'hc-lite: 10.3762', 'hc-dark: 10.7006' — against 'targets: AA 4.5 AAA 7.0 HC nontext 4.5'.

*Smallest fix.* Change the EXIT CODES block to say what is true — anchors supply hue and chroma only, the lightness ladder is fixed, so exit 1 is a safety net no direction spec can currently trigger — or make the ladder spec-derived if role failure is meant to be a real possibility.

#### R2-17 · 08_components/build.py's no-literal-colour guard does not treat CSS system colour keywords as literals, so hard-coded ButtonFace, ButtonText and AccentColor pass

`08_components/build.py`

A system colour keyword outside a forced-colors block paints one fixed operating-system colour in all four themes and ignores every token, which is exactly the class of value the guard exists to keep out of the hand-authored layer — 07_tokens/build.py puts them in a separate non-DTCG file precisely because they are colours the system supplies. Nothing downstream would catch it either: it would not change with data-theme, and no check verifies that a painted colour differs between themes. It is minor because reaching it takes a deliberate edit to components.css and the keywords are arguably outside the guard's intended vocabulary — but the guard's stated rule is unqualified, and the same omission lets `color-mix()` through when both its operands are keywords.

**Still open, 19 August 2026.** Still open. Every CSS system colour keyword — ButtonFace, ButtonText, AccentColor, Canvas, CanvasText, LinkText — passes both the stylesheet guard and the markup guard, so a hand-authored one would ship reported as a clean run. Nothing in 08_components currently uses them, so the gap is latent rather than live.

*How that was checked.* Imported 08_components/build.py and called its own guard functions. colour_literal_in returns None for every CSS system colour: "colour_literal_in('ButtonFace') -> None", "colour_literal_in('ButtonText') -> None", "colour_literal_in('AccentColor') -> None", "colour_literal_in('Canvas') -> None", "colour_literal_in('CanvasText') -> None", "colour_literal_in('LinkText') -> None", while "colour_literal_in('#ff0000') -> '#ff0000'" and "colour_literal_in('red') -> 'red'". Both guards then pass: "guard_markup: PASSED (no error) for <div style=\"background: ButtonFace; color: ButtonText; outline-color: AccentColor\">x</div><svg><rect fill=\"Canvas\"/></svg>" and "guard_stylesheet: PASSED (no error) for a { background: ButtonFace; color: ButtonText; accent-color: AccentColor; }". Cause: NAMED_COLOURS (lines 152-181) holds only the CSS named colours; no system colour keyword is in it, and the membership test at lines 233 and 275 is the only name-based branch.

*Smallest fix.* Add the CSS Color 4 system colour keywords to NAMED_COLOURS in 08_components/build.py (they are colour values by definition), keeping ALLOWED_COLOUR_KEYWORDS for currentcolor and transparent.

#### R2-18 · The Bangla review sheet's checkboxes are 16 px, below SC 2.5.8, and no harness measures the page

`06_type/BANGLA-REVIEW.html`

The kit's central accessibility claim is WCAG 2.2 AA proven, and its own checker fails a committed interactive page against SC 2.5.8. The buttons on the same page were given `min-height:44px` deliberately, so the floor was understood and the 24 controls a reviewer actually clicks were missed. It is also the page a second Bangla reader is asked to work through, which is the audience least well served by a 16 px target.

**Half stale, 19 August 2026.** Half reproduces, half does not. The 16px measurement and the absent harness are exactly as recorded, but the SC 2.5.8 conclusion does not hold: the Spacing exception is met with zero violations at five viewport widths, so the page conforms. It does fail this project's own stricter internal floor — 08_components/check.py:493 states the harness 'applies none of them: every interactive element is 24x24 or it fails' — which the review sheet's 19.38px labels would not survive if anything opened it.

*How that was checked.* Measured in the pinned Chromium via Playwright against 06_type/BANGLA-REVIEW.html (read-only, PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers): 'inputs found: 218 / min input WxH: [16, 16] / min wrapping-label WxH: [39.94, 19.38]'. Source: 06_type/review_bangla.py:434 '.mark input{{accent-color:{accent};width:16px;height:16px;cursor:pointer}}'. But the SC 2.5.8 Spacing exception is satisfied — a 24px-diameter circle centred on each of the 436 undersized targets intersects nothing, at every width tested: '375 {"total": 547, "undersized": 436, "violations": 0}' and '1400 {... "violations": 0}'; minimum centre-to-centre distance 28.01px at 375/768/1280/1400/1920. Harness half reproduces: `grep -rn BANGLA-REVIEW` finds only '06_type/review_bangla.py:47:OUT = HERE / "BANGLA-REVIEW.html"' and the findings record; the only rendered gates in scripts/verify-all.sh are '11_site/check.py' (PAGES = ["index.html", "404.html"], line 41) and '08_components/check.py' (opens only card HTML under 08_components); `grep -rn 06_type` in both returns nothing.

*Smallest fix.* In 06_type/review_bangla.py raise '.mark input' to 24x24 and add min-height:24px to '.mark label' so the page meets the project's own no-exceptions floor, and add the generated sheet to one rendered harness so the number is measured rather than asserted.

#### R2-19 · 12_packages --check reports "6 DTCG documents" while one of the six is declared not DTCG

`12_packages/build.py`

This line is the one confirmation a reader gets that the DTCG documents in the package are conformant, and it counts a file the kit insists three times over is not one — so the number that certifies conformance is the number that includes the exception. The file's own comment names this string as a past false claim and then re-emits it, which is exactly the drift the repository built its guards to stop.

**Still open, 19 August 2026.** Still open. Five DTCG documents plus one that declares itself non-DTCG are reported as '6 DTCG documents shipped verbatim' — the same wrong count the comment above verify() (lines 779-783) cites as a past packaging bug. Console output only; nothing shipped carries the number.

*How that was checked.* `./.venv/bin/python 12_packages/build.py --check` prints ' ok 6 DTCG documents shipped verbatim'. The count is `f"{len(docs)} DTCG documents shipped verbatim"` (line 769) over `docs = {p.name: ... for p in sorted(TOKENS.glob('*.json'))}` (line 325), and that glob is exactly six files: forced-colors.map.json, primitive.tokens.json, semantic.{dark,hc-dark,hc-light,light}.tokens.json. The same build file declares one of them non-DTCG at line 248: 'The forced-colours map. Deliberately **not** DTCG'. The document says so of itself too — its JSON contains 'non-dtcg' and "Forced-colors mode cannot be expressed in DTCG. Its values are CSS system colour keywords supplied by the operating system — they have no colour space, no components and no hex".

*Smallest fix.* Split the note in 12_packages/build.py:769 — count only the five DTCG documents and name the forced-colours map separately, for example '5 DTCG documents and the forced-colours map shipped verbatim'.

#### R2-3 · CI enforces a seventh banned word that appears in no published blocklist, so a writer who follows the English standard exactly can be failed by it

`02_strategy/ENGLISH-STANDARD.md`

The rule as published is the rule a writer reads, and it is a strict subset of the rule CI applies. A contributor who obeys the standard word for word can still be failed on a step that names this document as its authority, and neither of the two places the project publishes the blocklist — the standard itself and the guidebook chapter whose whole purpose is to state it — lists the seventh word. The standard's assurance about what CI covers is written as an exact account ("stated exactly, because the previous version of this section overstated it") and is still not exact.

**Still open, 19 August 2026.** Reproduced exactly: CI fails on `easily`, a word the published standard never lists. Sharper today — the mismatch also runs the other way: the standard's sentence 'Every banned word and idiom above is in the checker's blocklist' is false about the idioms, because `grep -n "ballpark|touch base|out of the box|whilst|amongst|IDIOMS" check.py` returns nothing, so no idiom is enforced at all.

*How that was checked.* Line 105 of 02_strategy/ENGLISH-STANDARD.md publishes six words: `- **Banned outright: **, *merely*, *straightforward*, **, **, **.**`. `grep -n "easily" 02_strategy/ENGLISH-STANDARD.md` returns nothing (exit 1); `grep -n -i "inflect|variant|its forms|and their forms|easi"` on the same file returns `EXIT=1`. Line 35 of 13_plugins/claude-code/skills/aninda-review/scripts/check.py reads `BANNED_WORDS = ("", "merely", "straightforward", "easily", "", "", "")` — seven. Importing the module and calling its own `check_prose` in memory: `'The tokens can easily be rebuilt from the checkout.' -> [("the banned word 'easily'", 'demo.md:1')]` while the same sentence without the word returns `[]`. The CI step `The English standard's blocklist is enforced` in .github/workflows/ci.yml runs this checker over `01_research`, `02_strategy`, both READMEs, the guidebook chapters and more, with `|| { echo "::error::$path fails the English standard"; fail=1; }`.

*Smallest fix.* Add *easily* to the banned list on line 105 of 02_strategy/ENGLISH-STANDARD.md, and soften the 'every banned word and idiom' sentence to say the words are enforced and the idioms are not.

#### R2-7 · The tabs card's panels are unreachable by keyboard and the markup it teaches omits the tabindex that would fix it

`08_components/cards/components/tabs.html`

The WAI-ARIA Authoring Practices tabs pattern requires tabindex="0" on a tabpanel that holds no focusable element, so that after choosing a tab the reader can put focus into the panel and page through it. Without it a keyboard-only user activates a tab and focus jumps past the content they only revealed, with nothing focused inside the region they were reading. The card is the system's teaching artefact for this pattern and says so in its own panel text — 'Arrow keys move between the tabs and Home and End jump to the ends, which is what the roving tabindex on this pattern requires' — so the omission is copied by anyone following it. This is guidance rather than a WCAG success criterion, and the panels here are two short paragraphs, which is why it is minor rather than more.

**Half stale, 19 August 2026.** The roving-tabindex/arrow-key half is genuinely fixed and the harness proves it by pressing keys. The half the recorded body actually argues is untouched: no tabpanel carries tabindex="0", in the live card or in the markup it teaches, so after choosing a tab a keyboard-only reader has nothing focused inside the region they revealed. The card also teaches markup only — `grep -o 'as-code__name">[^<]*'` returns a single `markup` block and no JS — so a copier gets the roving tabindex and must supply the handler from the comment.

*How that was checked.* STALE HALF — the arrow-key handler now exists. tabs.html lines 1584–1628 contain a real roving-tabindex handler ('The other half of the ARIA tabs pattern ... Click, arrow keys, Home and End all move the selection') with `ArrowRight/ArrowDown/ArrowLeft/ArrowUp/Home/End` and `select(next, true)`. 08_components/check.py line 944 `check_tablists` presses real keys (`page.keyboard.press("ArrowRight")`) and fails on any tab not reached. `PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers ./.venv/bin/python 08_components/check.py --only tabs` printed 'Measured: ... 15 tabs reached by keyboard.' and 'PASS — every measurement above met its floor.' The taught markup now also carries `tabindex="-1"` on the unselected tab (line 1505) plus the comment 'tabindex="-1" without them takes the tab off the keyboard entirely' (line 1510). OPEN HALF — the record's own body is about `tabindex="0"` on the tabpanel, not the arrow keys: 'The WAI-ARIA Authoring Practices tabs pattern requires tabindex="0" on a tabpanel that holds no focusable element'. `grep -o 'role="tabpanel"[^>]*' tabs.html` returns all 15 panels with only `id` and `aria-labelledby` (plus `hidden`) — no tabindex. `grep -c 'tabindex="0"' tabs.html` → `0` and `grep -c 'tabindex=&quot;0&quot;' tabs.html` → `0`, so the taught markup omits it too. Every panel holds only `<p>` text, which is the case the APG guidance covers.

*Smallest fix.* Add tabindex="0" to each tabpanel in the tabs card generator in 08_components/build.py and to the taught markup sample, then regenerate and re-run 08_components/check.py --only tabs.

#### R2-8 · The site harness's structure and Bangla-language probe runs on index.html only, and its Bangla expression has no script/style skip list

`11_site/check.py`

Round 1 removed four CI steps that could pass without running. This is the same shape one level down: a harness that measures two pages reports a structure result derived from one, and prints it as an unqualified pass, so a regression on 404.html — a missing skip link, a lost <main>, an untagged Bangla string — is green. The skip-list omission is the reason the check cannot be pointed at the component cards as it stands: it would fire on every card's own stylesheet comment and the real defects would be indistinguishable from the noise. Both are cheap to close, and closing them is what would let one guard cover all thirty-two shipped pages instead of one.

**Still open, 19 August 2026.** Still open as written. The gap is latent rather than live: 404.html satisfies all four structure checks and has no untagged Bangla today, so nothing ships wrong — but the harness reports a one-page result as an unqualified pass directly beneath a '2 pages' line, and the missing script/style skip list still blocks pointing the guard at the 30 cards.

*How that was checked.* Both halves reproduce by reading 11_site/check.py. Scope: line 41 is `PAGES = ["index.html", "404.html"]`, but the block at lines 413–444 is headed `# --- structure, once ---` and hardcodes `pg.goto((HERE / "index.html").as_uri())` (line 416); every message is hardcoded too — 'index.html has no <main> landmark', 'index.html has no skip link'. Running it: `PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers ./.venv/bin/python 11_site/check.py` prints 'ok 2 pages × 3 widths × 4 themes' and then, unqualified, 'ok structure: <h1>×1, lang=''en'', <main> present, skip link present', ending '8 checks passed, 0 failed.' Bangla probe: line 425 is `[...el.childNodes].some(n => n.nodeType === 3 && /[ঀ-৿]/.test(n.textContent)) && !el.closest('[lang="bn"]')` — the only filter is the lang ancestor; there is no script/style exclusion, and a <style> or <script> element's contents are node type 3. I re-ran that exact probe against both pages in Chromium: `index.html {'h1': 1, 'lang': 'en', 'skip': True, 'main': 1, 'bnWithoutLang': 0}` and `404.html {'h1': 1, 'lang': 'en', 'skip': True, 'main': 1, 'bnWithoutLang': 0}`. 404.html does hold 6 Bangla runs that are never probed. The skip-list consequence is concrete: 08_components/cards/components/tabs.html has Bangla inside its <style> block — 'style bangla in block: [''মাত্রা'', ''মাত্রা'']' — so pointing this probe at the cards fires two false positives on that card alone.

*Smallest fix.* Loop the structure block over PAGES with the page name in each message, and add `&& !el.closest('script, style, pre, code')` to the Bangla filter.

#### R2-9 · The accessibility card's subtitle double-escapes an em dash, so the entity is read out as literal text on the one card whose subject is accessibility

`08_components/build.py`

A screen reader reads the visible characters, so the card's one-line summary is announced as 'forced colours ampersand m dash semicolon the mode where…' — six syllables of markup in the middle of a sentence, on the card a reader most likely reaches with a screen reader precisely because it is the accessibility card. It is also a visible defect for everyone. The site and the guidebook prove the string itself is right and only the card's escaping is wrong, so three surfaces built from one entry in 08_components/_cards.json now disagree about what that entry says, and the card generator is the only one that cannot pass an entity through.

**Still open, 19 August 2026.** Still true and unchanged. The one card whose subject is accessibility renders the seven characters &mdash; as literal text where an em dash belongs. Sharper than recorded: the same source string is passed through UNescaped by the other two consumers — 11_site/index.html and 09_guidebook/Aninda-Studio-Guidebook.html both contain the raw "&mdash;", which renders correctly there — so one source string renders as a dash on the site and the guidebook and as visible markup on the card.

*How that was checked.* grep -n "&mdash;" 08_components/build.py → line 1955: subtitle="…what happens in forced colours &mdash; the mode where the operating system replaces every colour with its own.". The subtitle is emitted at line 2317 as f'<p class="as-doc-sub">{e(card["subtitle"])}</p>', and e() is defined at line 498 as `return html.escape(str(text), quote=True)`. Reading the shipped output: grep -n "as-doc-sub" 08_components/cards/foundations/accessibility.html → line 1451: '<p class="as-doc-sub">Target sizes … in forced colours &amp;mdash; the mode …</p>'. A tree-wide grep for "&amp;mdash" over *.html/*.json/*.md/*.css returns exactly one file: 08_components/cards/foundations/accessibility.html. 08_components/check.py contains no match for "amp;|escape|mdash|&#", and a full run finished PASS (exit 0), so nothing catches it.

*Smallest fix.* In 08_components/build.py line 1955 replace the entity &mdash; with the literal em dash character —, as every other subtitle in the CARDS list already uses, then regenerate the cards.

#### B7-1 · Acceptance criterion 1 is met only in part: Icon masters are exported unmasked, at 1024×1024 px for iOS, iPadOS and macOS, and 1088×1088 px for watchOS

`01_research/BENCHMARK.md`

This kit's own acceptance criterion, written in section 7 of the benchmark before anything was built and scored for the first time on 19 August 2026.

The test it names: Open each exported file: check pixel dimensions, and check the four corners are opaque artwork rather than transparent rounded-off area.

**Half stale, 19 August 2026.** An unmasked 1024 master exists with opaque corners, but the 1088 watchOS file is pre-rounded with transparent corners and no unmasked 1088 exists.

*How that was checked.* Rendered each candidate master with Playwright at its own declared size and read the alpha of all four corner pixels (/tmp/acc/corners.py). 04_mark/svg/icon-appstore-square-1024.svg: declared 1024x1024, rendered 1024x1024, all four corners (13,26,23,255) fully opaque, no rx/ry in the source — this half of the criterion is met for iOS, iPadOS and macOS. 04_mark/svg/icon-1024.svg: 1024x1024 but carries rx=24 ry=24, all four corners (0,0,0,0), transparent rounded-off area. 04_mark/svg/icon-1088-watch.svg: correct 1088x1088 but also rx=24 ry=24, all four corners (0,0,0,0). No unmasked 1088 file exists anywhere in the repository, so the watchOS master fails the corner-opacity half of the test. Raster exports were also checked: the largest PNG in 10_assets is 512x512, so no 1024 or 1088 bitmap master exists. The rounding is a documented owner's decision (04_mark/manifest.json icon_policy, 14 August 2026): one rounded icon everywhere, square only for App Store submission.

#### B7-20 · Acceptance criterion 20 is met only in part: Reduced motion substitutes a fade, never a spatial move, depth transition or blur

`01_research/BENCHMARK.md`

This kit's own acceptance criterion, written in section 7 of the benchmark before anything was built and scored for the first time on 19 August 2026.

The test it names: Enable the reduced-motion setting and observe every animation in the kit.

**Half stale, 19 August 2026.** Nothing moves, blurs or changes depth, reduced or not. But no fade is substituted either: under reduce the two duration tokens fall to 1 ms and the colour transitions are removed rather than cross-faded.

*How that was checked.* I ran the named test: /tmp/as_reduced.py opened all 30 cards, 11_site/index.html and 09_guidebook/Aninda-Studio-Guidebook.html in Chromium contexts with reduced_motion set to reduce and then to no-preference, and read the computed animationName, animationDuration, transitionProperty and transitionDuration of every element on every page. With reduce off, the entire kit has exactly three transitioned properties — background-color at 0.12s on 415 elements, border-color at 0.12s on 309, color at 0.12s on 246 — and zero running keyframe animations, zero spatial transitions (transform, translate, scale, rotate, inset, margin, width, height, perspective or all), zero depth or blur transitions (box-shadow, filter, backdrop-filter, perspective) and zero opacity transitions. `grep -rnoE '@keyframes [a-zA-Z0-9_-]+'` across every css, html, py, js and ts file in the repository returns nothing at all. With reduce on, --as-duration-colour and --as-duration-move both read 1ms at the root (07_tokens/css/tokens.css:279-285) and the same three colour transitions run at 0.001s. So the prohibition half of the criterion holds absolutely and on every page: nothing moves, nothing changes depth, nothing blurs, reduced or not. The half that is not met is the positive one. Reduced motion substitutes nothing — it collapses both durations to 1 ms, which is removal, not a cross-fade; opacity is never transitioned anywhere in the kit, so no fade exists to be the substitute. The fade rule is written down (09_guidebook/build.py:2063-2068, "replace a movement with a fade — never a spatial move and never a blur") but no animation in the kit exercises it, because there is no movement to replace. I interpreted the test strictly: I observed every animation with the setting enabled rather than accepting the documented rule as evidence, and I am not scoring the fade requirement as vacuously satisfied.

#### B7-26 · Acceptance criterion 26 is met only in part: Licences are declared per artefact and are machine-readable — Apache-2.0 for code and tokens, the font's own licence for any bundled font (with Reserved Font Name checked before any fork is renamed), PolyForm Noncommercial 1.0.0 for identity assets using the no-trailing-slash canonical URL

`01_research/BENCHMARK.md`

This kit's own acceptance criterion, written in section 7 of the benchmark before anything was built and scored for the first time on 19 August 2026.

The test it names: Confirm a licence file in each artefact directory, a licence manifest listing SPDX identifiers, and a link check that every licence URL resolves.

**Half stale, 19 August 2026.** All 5 licence URLs return 200 and every font ships its OFL. But six artefact directories hold no licence file, spdx.py --check exits 1 on 47 files, and identity is unlicensed rather than PolyForm.

*How that was checked.* TEST PART 3 (link check) PASSES. Collected every licence URL in the tree, then curl -sL -o /dev/null -w '%{http_code}': 200 http://www.apache.org/licenses/LICENSE-2.0, 200 https://www.apache.org/licenses/LICENSE-2.0, 200 https://openfontlicense.org/, 200 http://scripts.sil.org/OFL, 200 https://polyformproject.org/licenses/noncommercial/1.0.0, 200 the polyform raw markdown. The trailing-slash form returns 404 and appears nowhere: ./.venv/bin/python scripts/check_licence_claims.py exits 0 over 326 text files with 'no PolyForm URL carries a trailing slash'. FONT CLAUSE PASSES. Every shipped face has its licence beside it in 08_components/fonts (literata-OFL.txt, notoserifbengali-OFL.txt, anindamono-OFL.txt). Reserved Font Name read from source: head -1 06_type/candidates/mono/ibmplexmono/OFL.txt gives 'Copyright (c) 2017 IBM Corp. with Reserved Font Name "Plex"'; the subset is renamed 'Aninda Mono' and its shipped OFL preserves that first line, so the name was checked before the fork was renamed. TEST PART 1 (licence file per artefact dir) PARTIAL. Present: 12_packages/npm (LICENSE, NOTICE), 12_packages/python (LICENSE, NOTICE), 13_plugins/claude-code (LICENSE.txt, LICENSE-DOCS.md, NOTICE), 13_plugins/figma (same three), 13_plugins/claude-design/dist (LICENSE, NOTICE). Absent: 04_mark, 10_assets, 07_tokens, 08_components, 09_guidebook, 11_site hold no LICENSE, NOTICE or COPYING at all. TEST PART 2 (SPDX manifest) PARTIAL. Machine-readable SPDX exists per package only: 12_packages/npm/package.json '"license": "Apache-2.0"', 12_packages/python/pyproject.toml 'license = "Apache-2.0"', 13_plugins/claude-code/.claude-plugin/plugin.json and .claude-plugin/marketplace.json both 'Apache-2.0 AND PolyForm-Noncommercial-1.0.0'. There is no repository-wide licence manifest; the SPDX tables live in prose (NOTICE, guidebook chapter 13, licence-matrix.md), and grep -in 'licen|spdx' over 07_tokens/build/*.json, 04_mark/manifest.json and 10_assets/MANIFEST.json returns nothing, so the DTCG token documents and the identity manifests carry no SPDX field. The kit's own enforcer disagrees with its published matrix: ./.venv/bin/python 13_plugins/claude-code/skills/aninda-repo/scripts/spdx.py --check . exits 1 with '99 already correct / 206 exempt / 47 missing / 0 declaring a different licence', the 47 including both READMEs, TRADEMARKS.md, .github/workflows/ci.yml, all 18 guidebook chapter sources, 11_site/index.html and four packaged stylesheets. IDENTITY CLAUSE NOT MET AS WRITTEN. NOTICE section 4 declares 'THE IDENTITY - not licensed at all ... No licence is granted to any of it'; PolyForm-Noncommercial-1.0.0 covers the writing instead. This is a deliberate, consistently documented deviation (13_plugins/claude-design/dist/NOTICE says the same), not an oversight, but the criterion's assignment of PolyForm to identity assets does not hold. ONE STALE CLAIM FOUND. 13_plugins/claude-code/skills/aninda-repo/references/licence-matrix.md line 73 reads '| IBM Plex Mono | `IBM Plex` | Rename it.' - the wrong reserved name the repository's guard exists to catch. It escapes because the guard's pattern requires the phrase 'Reserved Font Name' or 'RFN' and that table's column header reads 'Reserved name'.

#### B7-27 · Acceptance criterion 27 is met only in part: The brand book and the design system ship as separate artefacts, with separate licences and separate front doors, and the design system remains usable by someone not permitted to use the mark

`01_research/BENCHMARK.md`

This kit's own acceptance criterion, written in section 7 of the benchmark before anything was built and scored for the first time on 19 August 2026.

The test it names: Remove the identity assets and confirm the token set still builds and the component documentation still makes sense.

**Half stale, 19 August 2026.** Tokens and both packages still verify with 04_mark and 10_assets deleted, and packages ship no identity file. But 08_components and 11_site builds fail-close on the missing mark manifests.

*How that was checked.* Ran the named test in a throwaway copy, never in the repository: rsync -a (excluding .venv, .git, browsers, node_modules, font candidates) to /tmp/as_c27, baseline verified there first (07_tokens/build.py --check exit 0, emit_css.py --check exit 0), then rm -rf 04_mark 10_assets and re-ran. TOKEN SET STILL BUILDS: 07_tokens/build.py --check exit 0, '--check: 6 files verified, 0 problems. Nothing written.'; 07_tokens/emit_css.py --check exit 0, 'CSS re-parsed and matched against source'; 12_packages/build.py --check exit 0, 'both packages match the source', 'ok npm aninda-studio-tokens - 20 files', 'ok PyPI aninda-studio-tokens - 17 files'. The packages are genuinely clean of the identity: find 12_packages -type f piped to grep -iE 'mark|wordmark|icon|logo|tile|svg|png' returns nothing. COMPONENT DOCUMENTATION STILL READS: of the 30 built cards, grep -rl finds only 08_components/cards/foundations/the-marks.html mentioning the identity, and that card IS the identity card; the other 29 never name it. All three cards I parsed (button, colour, dashboard) have zero external src or href, so they render intact with 04_mark and 10_assets gone. WHAT DOES NOT SURVIVE: 08_components/build.py --check exits 1 with FileNotFoundError '/private/tmp/as_c27/04_mark/manifest.json', and 11_site/build.py --check exits 1 with 'BUILD FAILED - 10_assets/MANIFEST.json is missing. Run 10_assets/build.py first'. So the shipped documentation reads, but someone not permitted to use the mark cannot regenerate the card set or the site, including the 29 cards that have nothing to do with the identity. 09_guidebook/build.py --check exits 1 on 04_mark/svg/wordmark-latin.svg, which is expected of a brand book. SEPARATE LICENCES: yes, and verified per artefact (Apache-2.0 on tokens and code, PolyForm-Noncommercial-1.0.0 on the writing, identity unlicensed; 09_guidebook/chapters/01-welcome.md carries the three-row table stating it). SEPARATE ARTEFACTS AND FRONT DOORS: not as written. The brand-book chapters (01-04, 10, 11, 13) and the design-system chapters (05-09, 12) are one 15 MB guidebook file under the single writing licence, and README.md plus 11_site/index.html are one shared front door for both halves; the only genuinely separate front doors are the two package READMEs. 01_research/BENCHMARK.md states the original intent as 'Ship the two artefacts separately, with separate licences and separate front doors', so the shortfall is against the kit's own plan.

#### B7-28 · Acceptance criterion 28 is not met: Every factual claim in the guidebook carries a source and a date checked, and no number appears that cannot be traced to one

`01_research/BENCHMARK.md`

This kit's own acceptance criterion, written in section 7 of the benchmark before anything was built and scored for the first time on 19 August 2026.

The test it names: Read every claim: each must have a citation with a URL and a date; count the untraceable numbers, which must be zero.

**Half stale, 19 August 2026.** The apparatus now exists and is reachable: 38 distinct real URLs against 2 before, a generated 57-source appendix, and BENCHMARK.md embedded in the book. Per-sentence citation is not met — 68 of 76 external-authority sentences still carry no URL of their own.

*How that was checked.* Re-ran the audit on the rebuilt book. Distinct real URLs went from 2, both licence texts, to 38. A Sources appendix generated from 01_research/_data/external-sources.json lists all 57 sources across Apple, Google, standards and formats, and tooling, each with its URL and the date the source itself carried rather than the date it was read. BENCHMARK.md is now file 69 in the embedded kit, so a reader of the book alone can reach the record it cites — that was the specific defect, that the apparatus existed and was unreachable. The four target tokens now carry a URL and a read date in their own $description, so the figures a stranger consumes can be re-checked. What is NOT met is the literal reading: of 76 sentences naming an external authority and a number, 68 still carry no URL in the same sentence. Grading this a pass would be the kind of rounding-up this system exists to refuse.

#### B7-6 · Acceptance criterion 6 is met only in part: A Mono (single-colour) variant exists and is legible at both full size and the smallest specified size

`01_research/BENCHMARK.md`

This kit's own acceptance criterion, written in section 7 of the benchmark before anything was built and scored for the first time on 19 August 2026.

The test it names: Render the Mono layer at both sizes and confirm the mark reads.

**Half stale, 19 August 2026.** Single-colour recolourable marks render legibly at 1024 px and at the documented 16 px floor, counter open in both. No artefact is designated a Mono icon appearance layer.

*How that was checked.* Rendered with Playwright Chromium at device_scale_factor 1 on white, then flood-filled the background to test whether the ring's counter stays open. /Users/gru953/Claude/Cowork/Aninda_Studio/04_mark/svg/mark-regular.svg and mark-heavy.svg are the kit's single-colour files ('Recolourable: drawn in currentColor, with no colour on the root'). Results: mark-heavy at 1024 px, ink 31.56 per cent, 1 enclosed counter of 138380 px measuring 419x420; mark-heavy at 16 px, ink 32.42 per cent, 1 enclosed counter of 34 px measuring 6x6; mark-regular at 1024 px, counter 481x481; mark-regular at 24 px, counter 11x11. An ASCII dump of the 16 px render shows the ring, an open counter and the stem tail below it, so the mark reads at both extremes. 16 px is the correct smallest specified size: MARK_FLOOR_PX = 16 in 13_plugins/claude-code/skills/aninda-brand/scripts/asset.py, and 09_guidebook/chapters/03-the-mark.md says 'Below 16 px, use the icon rather than the bare mark'. What does not exist: no file, layer or manifest entry anywhere is designated Mono. `find . -iname "*mono*" -o -iname "*.icon"` returns only the Aninda Mono typeface files. 04_mark/manifest.json lists 10 artefacts, none of them a Mono or Dark appearance layer, and 13_plugins/claude-code/skills/aninda-brand/references/icons.md names Mono only as one of Apple's three Icon Composer appearances without shipping one.

#### B7-7 · Acceptance criterion 7 is met only in part: Icon masters are authored in sRGB; any Display P3 variant is additional, and no P3 asset is offered for visionOS

`01_research/BENCHMARK.md`

This kit's own acceptance criterion, written in section 7 of the benchmark before anything was built and scored for the first time on 19 August 2026.

The test it names: Read the embedded colour profile of every exported asset.

**Half stale, 19 August 2026.** No P3 asset exists anywhere, so none is offered for visionOS. But none of the 19 exported rasters carries an embedded profile, so sRGB is implicit rather than declared.

*How that was checked.* Parsed the PNG chunk stream of every exported raster and checked PIL's icc_profile for each. All 18 PNGs in /Users/gru953/Claude/Cowork/Aninda_Studio/10_assets/ plus favicon.ico carry no iCCP, no sRGB chunk, no cHRM and no gAMA; icc_profile is False on every file, and the only text chunks present are Software, Comment and Title. The same holds for all 30 other PNGs in the repository. 10_assets/MANIFEST.json records the renderer as 'Chromium via Playwright, device_scale_factor 1' and says nothing about colour space, only 'No colour is typed in the generator.' The vector masters in 04_mark/svg/ carry no colour-profile attribute either; their literals are plain hex, #0D1A17 and #FFFFFF, which are sRGB by the CSS and SVG specifications, and 07_tokens/build/primitive.tokens.json emits every colour as {\"colorSpace\": \"srgb\", ...}. On the P3 half of the criterion the result is unambiguous: `grep -rl "display-p3"` across all JSON, CSS, PY, SVG, HTML and MD files returns nothing, so no Display P3 asset exists for any platform and none is offered for visionOS.

#### R3-1 · About forty tracked files carry no SPDX header, against the licence matrix this system publishes

`13_plugins/claude-code/skills/aninda-repo/scripts/spdx.py`

Both READMEs, `TRADEMARKS.md`, `ci.yml`, the guidebook chapter sources, nine
reference documents and several stylesheets. The checker ships here and no CI
step runs it.

Left deliberately, on the reviewer's own recommendation and on the evidence. No
file is ambiguously licensed: `NOTICE`, both READMEs and guidebook chapter 13 all
state the four-licence split and what each covers, so no reader is misled. Seven
of the flagged files are the enforcer over-reaching its own published matrix,
demanding headers for `.html` and `.gitignore`, which the matrix does not cover.
And the remedy is not "turn the checker on": most of the flagged files are
generated, so `spdx.py --write README.md` immediately fails `scripts/readme.py
--check`. Closing this means either a generator change per artefact or scoping
the matrix down to hand-written files. It is a decision about the matrix, not a
sweep, and it is the owner's to make.

The window was widened from 40 lines to 120 in this pass, which is a separate
fault: the checker was calling seven files missing a header they carry, because
the house docstring style puts the essay above the identifier. The deepest real
identifier in the tree sits at line 69.

**Still open, 19 August 2026.** Reproduced precisely, and the count has grown to 47. The mitigation still stands: the published matrix in aninda-brand/references/licence.md lines 16-21 states the four-licence split by part, and NOTICE plus both READMEs carry it, so no file is ambiguously licensed. This remains a decision about the scope of the matrix, not a sweep.

*How that was checked.* `./.venv/bin/python 13_plugins/claude-code/skills/aninda-repo/scripts/spdx.py --check .` → "97 already correct / 204 exempt, by the rules in this script / 47 missing / 0 declaring a different licence / 65 no rule, so left alone". I then tested each of the 47 with `git ls-files --error-unmatch`: tracked=47, untracked=none — so "about forty tracked files" is if anything an understatement. The named categories all appear in the MISSING list: README.md, README.bn.md, TRADEMARKS.md, .github/workflows/ci.yml, the guidebook chapter sources (18 files under 09_guidebook/chapters/ and chapters/bn/), the reference documents (00_sandbox/TOOLCHAIN.md, 01_research/BENCHMARK.md, 01_research/OPEN-FINDINGS.md, 02_strategy/ENGLISH-STANDARD.md, 06_type/BANGLA-STANDARD.md, BANGLA-STRINGS.md, MEASUREMENTS.md, RECOMMENDATION.md, SHORTLIST.md, pairings.md) and four stylesheets (12_packages/python/src/aninda_studio_tokens/data/tokens.{light,dark,hc-light,hc-dark}.css). No CI step runs it: `grep -rn "spdx" .github/workflows/ci.yml scripts/*.sh scripts/*.py` returns nothing. The recorded over-reach sub-claim also holds exactly: the flagged non-matrix files are six .html (03_directions/COMPARE.html, shots/_m2.html, shots/_marks.html, 06_type/BANGLA-REVIEW.html, 11_site/404.html, 11_site/index.html) plus .gitignore — seven, as stated.

*Smallest fix.* Scope BY_SUFFIX in spdx.py down to hand-written files (drop .html and add a name-based exemption for generated output), then run --write over what remains and add the check to verify-all.sh — but only after deciding the matrix question, since --write on a generated file breaks scripts/readme.py --check.

#### R3-2 · The plugin and the review sheet use the same `gb-*` ids for different things

`06_type/review_bangla.py`

`13_plugins/claude-code/skills/aninda-brand/assets/bangla-verified.json`,

`gb-1` is a single chapter title, "Welcome", in the plugin. In the review sheet it
is a display row carrying three at once, "Welcome · The name · The mark". One id
namespace, two meanings, so the guard that now compares the plugin's verified
strings against the document they cite has to exclude the whole `gb-*` range.

The guidebook was moved onto `chapter.<slug>` keys from the register in this
pass, which is the shape the plugin should follow. Until it does, those ids are
outside the comparison. Nothing wrong ships: the Bangla itself agrees everywhere.

**Still open, 19 August 2026.** Still open, and sharper than recorded: the guard's own pass line claims all 31 strings agree with the review sheet when 10 of them — the entire gb-* range — were never compared to it, and 4 of the sheet's 23 rows were skipped. The exclusion hides no live error today (BANGLA-STANDARD.md:398 confirms gb-1 স্বাগতম and :407 confirms gb-10's change to পদ্ধতি, both matching the plugin), so the defect is the unmeasured claim in the printed output, not a wrong string.

*How that was checked.* The collision is intact and the exclusion is exactly as described. Review sheet, 06_type/review_bangla.py:160: `("gb-1", "Welcome · The name · The mark", "স্বাগতম · নাম · চিহ্ন",` — one id, three chapter titles. Plugin, references/bangla.md:79: `| gb-1 | স্বাগতম | Welcome |`, and assets/bangla-verified.json:112 `"id": "gb-1"` — one id, one title. 09_guidebook/build.py:187 agrees with the plugin (`"gb-1": "স্বাগতম",`). The guard, 13_plugins/claude-code/scripts/check_plugin.py, drops the whole namespace: `GROUPED = {key for key in source if key.startswith("gb-")}`, with both the Bangla loop and the gloss loop guarded by `if key in GROUPED: continue` / `if key not in GROUPED`. Counts: 10 gb-* ids in bangla-verified.json, 10 rows in bangla.md, 4 rows in the review sheet. Running `./.venv/bin/python 13_plugins/claude-code/scripts/check_plugin.py` prints "the 31 verified Bangla strings agree between bangla.md, bangla-verified.json and the 23 in 06_type/review_bangla.py, in Bangla and in English".

*Smallest fix.* Re-key the plugin's ten chapter ids to the `chapter.<slug>` register the guidebook already uses, or at minimum change the pass line to name the number actually compared (21 of 31) instead of implying all 31 were.

### Recorded, not defects (1)

#### R3-5 · The interactive guidebook's PDF size is a recorded one-off, not a measurement

`09_guidebook/build.py`

The print build's PDF size is now read from the file. The interactive build's is
not: that PDF is not shipped, and 14.2 MB was measured once while deciding to
ship two HTML builds. It is labelled as exactly that. Producing it on every build
to keep the figure current would cost more than the sentence is worth.

**Still open, 19 August 2026.** Reproduced as a statement of fact, but it is no longer a defect in effect: the shipped prose says in as many words that the number was measured once, while deciding the split, and that the PDF is not shipped, so nothing false reaches a reader and the figure is a historical claim that cannot drift into being wrong. Worth noting the machinery to close it already exists — 09_guidebook/scripts/pdf.py has `probe_interactive()` behind `--probe-interactive`, which prints the interactive build to PROBE_PDF and reports `fmt_bytes(PROBE_PDF.stat().st_size)`.

*How that was checked.* 09_guidebook/build.py:1004 `_pdf_sizes()` reads the print PDF from disk — `if pdf.exists(): printed = (f"Printing the print build gives a PDF of " f"{fmt_bytes(pdf.stat().st_size)}, read from the file in this " f"repository. ")` — and then returns a hardcoded literal for the other: line 1027, `return (printed + "Printing the interactive build gave one of about 14.2 MB " "when that was measured, once, while deciding this split; that PDF is " "not shipped, ")`. The sentence ships in both builds: grep against 09_guidebook/Aninda-Studio-Guidebook.html and -print.html returns "Printing the print build gives a PDF of 1.8 MB, read from the file in this repository. Printing the interactive build gave one of about 14.2 MB when that was measured, once, while deciding this split". The print figure checks out — Aninda-Studio-Guidebook.pdf is 1,791,468 bytes, 1.8 MB at the file's own SI convention (fmt_bytes, line 354, `n / 1_000_000`). No probe output exists to read: `ls 09_guidebook/_probe-interactive.pdf` → "No such file or directory".

*Smallest fix.* Run pdf.py --probe-interactive once and have _pdf_sizes() read PROBE_PDF's size when the file is present, mirroring what it already does for the print PDF; otherwise leave it, since the prose is already honest about what the number is.

### Already fixed, kept as a record (63)

These were true when written and are not true now. They stay because the record of what went wrong is the useful part, and because deleting them would hide that this document had drifted.

#### 1 · Overflowing horizontal scroll containers on every card and on the site are real tab stops that the design system's focus rule and check.py's INTERACTIVE selector both exclude

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. Both builds now set tabindex="0", role="region" and an aria-label from the table's caption, but only while the container overflows — the rule readme.md states.

*How that was checked.* Measured in Chromium: at 360 px all five containers on the table card are tabbable, named and matched by the harness INTERACTIVE selector, with the system ring at 3px solid rgb(39,132,146) offset 2px; at 1280 px, where none overflows, zero tab stops. The card harness now measures 7,592 targets where it measured 7,464 and the site 148 where it measured 144.

#### 10 · Two superseded pre-decision drafts ship in the published repository, unlabelled, arguing against the decisions the system actually made

**Fixed, confirmed 19 August 2026.** Fixed. Both pre-decision drafts were deleted in commit 70c7f45, are absent from HEAD and from the working tree, and `_reference/` is now gitignored with a comment recording why, so a re-copy cannot be committed again.

*How that was checked.* `ls -la _reference` → `ls: _reference: No such file or directory`. `git ls-files | grep -i -E '_reference|DRAFT'` → no output. `find . -name 'DRAFT*'` → no output. `git log --diff-filter=D --format='%h %s' -- _reference` → `70c7f45 Convergence round 1: fix four blockers and the Reserved Font Name`, whose deletion list includes `_reference/DRAFT-benchmark.html` and `_reference/DRAFT-reference-sheet.html`. `git ls-tree -r HEAD --name-only | grep -c _reference` → `0`. .gitignore now carries a `_reference/` entry under "The superseded Aninda drafts" ending "They are gone; this stops them returning."

#### 13 · TOOLCHAIN.md documents Jinja2 as the templating engine for the guidebook and the component cards; nothing in the repository imports it

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026, together with its Node twin. Jinja2 is no longer pinned, and TOOLCHAIN.md no longer gives it a job. The same sweep found `svgo` pinned in 00_sandbox/package.json with a documented job and no caller anywhere, so both were removed rather than one.

*How that was checked.* `grep -rn -iE 'import jinja|from jinja|jinja2' --include='*.py' --include='*.mjs'` → no output, before and after. `grep -c -i 'jinja\|svgo' 00_sandbox/TOOLCHAIN.md` → `0`. requirements.txt went from 10 pinned packages to 9. 00_sandbox/package.json lost `svgo` and the lockfile was regenerated offline with `npm install --package-lock-only --offline`; `grep -c '"svgo"' 00_sandbox/package-lock.json` → `0`, and `npm ci --offline` on a copy still installs, 4 packages. `tsc` and the Figma build both still run.

#### 16 · BENCHMARK.md still says the kit does not exist yet, and all 28 promised verdicts are unfilled

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. All 28 acceptance criteria were run against the finished kit and the verdicts published with their evidence.

*How that was checked.* Six read-only agents each ran the test its criterion names. First pass: 17 met, 6 part met, 4 not met, 1 not applicable. The four unmet were then fixed and re-scored, giving 20 met, 7 part met, 1 not applicable and none unmet. The verdicts live in 01_research/_data/benchmark-verdicts.json and scripts/benchmark.py writes section 7 from them, so the counts are counted. The three stale sentences and the wrong 'Twenty-six' over 28 rows are also corrected.

#### 17 · The guidebook and the card harness state that measurement happened on macOS only and on one machine, which CI contradicts on every run

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. All three surfaces now say the same true thing, and the harness line is derived rather than asserted.

*How that was checked.* check.py's blind-spot entry is now built from platform.system(), so it names the platform the run actually measured on instead of claiming macOS on every Ubuntu run. Chapter 14 says the checks run on macOS here and on Ubuntu in CI. guard_platform_claims fails the guidebook build if the book says 'one machine' again — proved by putting the phrase back.

#### 18 · NOTICE publishes a studio website address that does not resolve

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. Every surface that presented the unregistered domain as a live site now points at the repository or says it is not registered.

*How that was checked.* The Site: line is gone from all six NOTICE files and the plugin README; plugin.json's homepage and author.url and 12_packages/build.py's HOME point at github.com/GRU-953/aninda-studio, which propagates to npm's homepage and PyPI's Homepage. The site keeps the domain in its CNAME, canonical URLs, sitemap and og:image, because that is the address it is built for, and both READMEs now disclose in English and Bangla that it is unregistered and nothing is served there. Chapter 02's naming table says so too.

#### 8 · The guidebook PDF and three other committed generated trees have no drift guard anywhere

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. The PDF is regenerated, and pdf.py --check now gates it on content because a byte gate is impossible here.

*How that was checked.* Two consecutive renders of identical input gave sha256 5b747e9b… and dd69c896…, because Chromium stamps a creation date, and an mtime gate is useless in CI where a checkout shares one timestamp. So --check compares the PDF's extracted text against every Latin segment of every heading in the print build. Proved by adding a heading and leaving the PDF alone: CHECK FAILED, naming it. 10_assets/build.py also gained the --check it never had. Both are in CI and in verify-all.sh.

#### 9 · The 18 August coverage correction was applied to the two READMEs only; the wording it set out to remove survives in the guidebook and in the harness that prints it while running on Ubuntu

**Fixed, confirmed 25 August 2026.** Fixed, and it was already fixed when the 19 August pass recorded it as open — the same correction is recorded under entry 17. Both halves are gone: the chapter names both operating systems, and the harness derives its blind-spot line from the platform it is running on.

*How that was checked.* `grep -rln -i ubuntu 09_guidebook/chapters/` → `09_guidebook/chapters/14-what-this-system-does-not-do.md`, where the evidence said it returned nothing. `grep -c 'headless Chromium on macOS' 09_guidebook/Aninda-Studio-Guidebook.html 09_guidebook/Aninda-Studio-Guidebook-print.html` → `0` and `0`, where the evidence said `1` and `1`. `grep -n 'any platform other than' 08_components/check.py` → one hit, line 489, inside a comment recording that the string was removed; the live line is derived from `platform.system()`.

#### R2-1 · Both published site pages date themselves 2026-08-14 and claim their counts were taken that day, while the same page reports checking registries on 2026-08-18 and the file was regenerated on 18 August

**Fixed, confirmed 19 August 2026.** Fixed properly, not cosmetically: the constant was removed rather than updated, the sitemap now ships no <lastmod> at all, and guard_dates() (wired at build.py:1339) demonstrably rejects any ISO date that no committed record supplies. One residual limit worth knowing: the guard only recognises ISO-format dates, so a typed "14 August 2026" would slip through — no built page contains one today.

*How that was checked.* The typed constant is gone and its absence is documented: `11_site/build.py:80-95` — "There is deliberately no BUILT_ON constant here any more, and no call to date.today() either." Scanning the built output, `grep -o -E '[0-9]{4}-[0-9]{2}-[0-9]{2}'` returns `2026-08-18` for index.html and NOTHING for 404.html, sitemap.xml, robots.txt, site.webmanifest and styles.css. `grep -rn lastmod 11_site/sitemap.xml` returns nothing (build.py:1246 replaces it with a comment explaining why). `grep -i 'counted on'` over index.html and 404.html returns nothing. The one surviving date is sourced, not typed: `12_packages/PUBLICATION.json:4` holds `"checked": "2026-08-18"`, and it appears as "On 2026-08-18 I checked the npm registry and the Python Package Index". I also confirmed the new guard would actually fire, by calling it directly: `guard_dates({"index.html": b"<p>Counted on 2026-08-14.</p>"}, {"checked": "2026-08-18"})` raised "The typed-date rule failed", while the PUBLICATION.json date passed.

#### R2-10 · A banned word is used in shipped prose in a lint-covered path, and the CI blocklist guard cannot see it because the same paragraph contains a rule-statement phrase

**Fixed, confirmed 19 August 2026.** Fixed by commit 30d3688; the four words were removed from OPEN-FINDINGS.md and nothing has replaced them. Worth recording that the exemption mechanism the finding named is unchanged and still line-scoped: RULE_STATEMENT matches "rather than", "instead of", "never ", "do not" and "does not exist", any of which appear in ordinary prose, so a future banned word sharing a line with one of them would still pass silently. Today no such line exists in any lint-covered path.

*How that was checked.* grep -niE "\\b(|merely|straightforward|easily|||)\\b" 01_research/OPEN-FINDINGS.md → no output. Running the guard the CI job runs: .venv/bin/python 13_plugins/claude-code/skills/aninda-review/scripts/check.py 01_research → "Checked 2 file(s)", "1 banned words cited rather than used", "FAILURES (0) … None." I then re-implemented the guard's own loop (BANNED_WORDS, CITED, RULE_STATEMENT, inside(), MAX_LINE_CHARS imported from check.py) and ran it over all 18 lint-covered paths from .github/workflows/ci.yml: "files scanned: 94 / total exempted-by-rule-statement, not quoted: 0". The only banned word anywhere in 01_research is BENCHMARK.md:148, inside quotation marks — Apple asks for " defined edges" — which CITED exempts as a genuine citation. git show 30d3688 -- 01_research/OPEN-FINDINGS.md confirms the four uses (three "", one "merely") were deleted in "Remove four banned words from the findings record".

#### R2-16 · tag_inline_bangla's docstring claims Bangla inside attributes is counted by the guard and named in a chapter; neither the counter nor the chapter text exists

**Fixed, confirmed 19 August 2026.** Stale. Commit 1677ee3 deleted the four docstring lines that made the claim; the text appears nowhere in the file now, so there is no promise left to be unmet.

*How that was checked.* `sed -n '2820,2839p' 09_guidebook/build.py` prints the whole current tag_inline_bangla docstring; it ends 'Returns (bangla_runs, english_runs, document).' with no attribute claim. `grep -rn "counted separately\|named in the chapter" 09_guidebook/build.py` returns only unrelated hits (line 19 and line 294, both the chapter-title list); `grep -rn "ALT attribute\|alt attribute\|inside an attribute\|part of an attribute" 09_guidebook/build.py` -> 'grep-exit=1' (no matches). `git log --oneline -S "Those are counted separately by the guard" -- 09_guidebook/build.py` -> '1677ee3 / 70c7f45'; `git show 1677ee3 -- 09_guidebook/build.py` shows the removal: '- Note the honest limit: a Bangla word inside an ALT attribute cannot be marked / - up at all ... / - Those are counted separately by the guard and named in the chapter on what this / - system does not do.' replaced by '+ Two implementations of the same rule is one implementation and one liability.'

#### R2-2 · The table and dashboard cards ship hand-typed contrast figures under a caption saying they were measured and an alert titled "These figures come from check.py", against README's claim that no hand-written contrast figures exist in the repository

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. Both cards now say the figures are examples, and the README's claim names its one exception.

*How that was checked.* The table card's caption reads 'Example rows: a contrast report as this table would render it. The figures are illustrative, not measurements'. The dashboard alert title is 'Example figures, not a live reading', replacing a title that claimed check.py as the source while its own body denied it. Feeding the cards check.py's real report was rejected for a stated reason: the figures would change every run and the card build is diffed byte for byte.

#### R2-20 · The aninda-repo skill promises two full licence texts and ships neither a template nor the text

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. All three licence texts now ship in the bundle and SKILL.md names where each one is.

*How that was checked.* templates/LICENSE-DOCS.md is the PolyForm text verbatim from the repository. templates/OFL.txt is derived rather than copied, and the reason is in the code: the shipped OFL's first line names IBM Corp and the Plex Reserved Font Name, which would be wrong to hand a stranger as a template, so the header is SIL's placeholder form and the body is byte-identical. check_plugin.py byte-compares the two copies and checks the OFL template's body against the shipped licence — 23 bundled files now compared, and a new check confirms the placeholder header is present.

#### R2-21 · The website inventories the guidebook, the 30 cards and both packages and provides a route to none of them

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. The page now links the repository, the guidebook, the cards and the tokens.

*How that was checked.* The published page offered two links, skip-to-content and a mailto. It now carries five. Hyperlinks are not subresources, so the page keeps its offline-and-self-contained property, and 11_site/check.py still reports external references as a note rather than a failure.

#### R2-22 · COMPARE.pdf and all eight files in 03_directions/shots have no writer anywhere in the repository

**Fixed, confirmed 27 August 2026.** Fixed since this was written, by removal rather than by giving the files a writer. The finding was right: COMPARE.pdf and the eight PNGs under 03_directions/shots had no generator anywhere in the repository, so nothing could reproduce or check them. The whole exploration went to Trash on 27 August 2026 by the owner's decision.

*How that was checked.* $ git ls-files 03_directions | wc -l  ->  19 before, 0 after. $ ls 03_directions  ->  no such file or directory; the bytes are in Trash, not deleted.

#### R2-23 · Outstanding, not a defect: the Claude Design push is still to be done, and the deliverable is named in no shipped surface

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. Both halves are closed.

*How that was checked.* 13_plugins/claude-design/build.py went into REBUILD_CHAIN, which cleared the red README drift check, and both READMEs' 13_plugins row now names the Claude Design bundle, so the ninth deliverable appears in the kit's own inventory. The remote project exists: DesignSync list_projects shows 'Aninda Studio Design System' with 48 files and 18 preview cards.

#### R2-4 · OPEN-FINDINGS.md records as an open, reproducible fault a directory that was removed and gitignored one commit before the file was written

**Fixed, confirmed 25 August 2026.** Fixed. The document it describes no longer exists in that form: OPEN-FINDINGS.md is generated from this data file, and the numbered-heading layout the evidence quotes was replaced by it. The _reference entry now renders as fixed, which is what R2-4 said was missing.

*How that was checked.* `grep -c '^### 10\.' 01_research/OPEN-FINDINGS.md` → `0`; the heading format the evidence quotes does not exist. `grep -n 'twenty-eight minors' 01_research/OPEN-FINDINGS.md` → one hit, line 453, inside R2-4's own body. `sed -n '73,78p'` now prints the pypdfium2 entry. Entry 10 renders under "Already fixed, kept as a record".

#### R2-5 · README's headline command is described as taking about a minute; it takes 3.3 seconds

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. Both front doors now say a few seconds.

*How that was checked.* Measured three times: 4.1 s cold, then 3.0 s and 3.0 s. Not timed at build time on purpose — readme.py's output is diffed by --check and by CI, so a figure that varies per run would fail the drift guard every time. The Bangla sentence, which the original record did not name, is corrected too.

#### R2-6 · The Bangla README omits the rounded-icon limitation entirely, so one of the two front doors does not disclose the deliberate departure from Apple's guidance

**Fixed, confirmed 19 August 2026.** Fixed 19 August 2026. The rounded-icon departure is now disclosed in Bangla as well as English.

*How that was checked.* A fifth bullet was added to the Bangla limits block in scripts/readme.py mirroring the English one, so both front doors disclose the same deliberate departure from Apple's guidance and both point at 04_mark/manifest.json.

#### B7-17 · Acceptance criterion 17 is not met: Spacing between adjacent controls is specified, not only their sizes — approximately 12 pt around bezelled and 24 pt around unbezelled elements where Apple platforms are targeted

**Fixed, confirmed 19 August 2026.** Fixed on 19 August 2026 and re-scored: The component gap is now a stated rule: adjacent controls at least --as-space-2 which is 12 px, and --as-space-4 which is 24 px where controls have no visible edge. Apple's figures are cited.

*How that was checked.* Re-measured the built book after adding block_control_spacing to chapter_space_en. Extraction now finds 'The gap between two controls' 1 hit, 'Adjacent controls are separated' 1 hit, bezelled 2 hits and unbezelled 1 hit, where every one of those was 0 across all 30 cards and every reference file before. The rule is not invented: 08_components/src/components.css already sets gap: var(--as-space-2) on the row utilities, and space-2 is 12 px and space-4 is 24 px, which coincide exactly with the two Apple figures, so no token was added. Sourced to the Accessibility page.

#### B7-22 · Acceptance criterion 22 is not met: The dynamic-colour position is stated explicitly, naming the mechanism — static brand colours, or harmonised via `HarmonizedColors`

**Fixed, confirmed 19 August 2026.** Fixed on 19 August 2026 and re-scored: The book now states the position and names the mechanism: brand colours stay static, HarmonizedColors is not used, and the opt-in call is named. The cost on Android is stated too.

*How that was checked.* Re-measured the built book after adding block_dynamic_colour to chapter_colour_en. Extraction now finds 'Dynamic colour' 2 hits, HarmonizedColors 2 hits, wallpaper 3 hits and applyToActivitiesIfAvailable 1 hit, all of which were 0 in the guidebook before. Both halves the criterion requires are present: the decision (hold static) and the mechanism (HarmonizedColors, not used). The reason given is the measurable one, that a palette shifted at run time has not been measured, so every ratio in the book would become an estimate.

#### B7-9 · Acceptance criterion 9 is not met: The type scale has a documented floor per platform: 11 pt iOS/iPadOS, 10 pt macOS, 23 pt tvOS, 12 pt visionOS, 12 pt watchOS

**Fixed, confirmed 19 August 2026.** Fixed on 19 August 2026 and re-scored: The book now carries a five-platform floor table with Apple's default and minimum for each, sourced to the Typography page and its 16 December 2025 change log, and states this kit's own web floor against it.

*How that was checked.* Re-measured the built book after adding block_platform_floors to chapter_type_en. Plain-text extraction of 09_guidebook/Aninda-Studio-Guidebook.html now contains: 'The floor, per platform' 1 hit, tvOS 4 hits where it previously had 0 anywhere in the book, and the five minimums 11 pt, 10 pt, 23 pt and 12 pt present as a table. The figures are read from 01_research/_data/external-sources.json, which was extracted from BENCHMARK.md line 169 rather than retyped, so they cannot drift from the research. The table also states plainly that this kit's 12 px smallest step clears iOS, iPadOS, macOS, visionOS and watchOS and does NOT clear tvOS at 23 pt, and that the kit is not specified for tvOS.

#### R4-1 · The manifest gate asserted that Figma publishes neither manifest value, and the false half of that sentence is what stopped the Figma build from ever completing

**Fixed, confirmed 25 August 2026.** Half of it was false. `api` is published, in two independent places, and adopting it from those is not a guess. `id` genuinely is not obtainable headlessly — but Figma's own samples show an unpublished plugin does not need a numeric one. Fixed 25 August 2026: the manifest is committed, the gate distinguishes a publishable manifest from a development one instead of calling both adopted, and the full build is a CI gate for the first time.

*How that was checked.* Figma's manifest guide documents the `api` field and shows `1.0.0` (https://developers.figma.com/docs/plugins/manifest, read 19 August 2026). Sweeping every manifest.json on `main` in figma/plugin-samples: 32 of 32 declare exactly `"api": "1.0.0"`, with no other value anywhere in the repository. For `id`, the same sweep shows unpublished samples shipping readable slugs rather than numbers — png-crop, bar-chart-sample, pie-chart-sample, document-statistics-sample. Both sources and their read dates are recorded in 13_plugins/figma/scripts/figma-api-version.txt. `cd 13_plugins/figma && node build.mjs` now ends `manifest.json is adopted for DEVELOPMENT: id aninda-studio-build-the-library, api 1.0.0.` and exits 0.

#### R4-2 · CI's placeholder-manifest test ended in `rm -f manifest.json`, which was harmless only for as long as no manifest was committed

**Fixed, confirmed 25 August 2026.** Caught by the new full-build gate the same day the manifest was first committed, before either reached main. Fixed 25 August 2026: the step copies the committed manifest aside, restores it, and then runs `git diff --exit-code` on it so a restore that silently fails is itself a failure rather than a quietly damaged checkout.

*How that was checked.* The step now reads `cp manifest.json /tmp/manifest.committed.json` … `cp /tmp/manifest.committed.json manifest.json` … `git diff --exit-code -- manifest.json` (relative to the step's working directory, which is 13_plugins/figma; the repo-root form is the bug R4-9 records). Proved locally by running the equivalent block with the manifest left overwritten: it printed `FAILED — manifest.json was not restored` and set the failure flag; with the restore in place it prints `ok` and `git diff --quiet 13_plugins/figma/manifest.json` returns 0.

#### R4-3 · Two gates in verify-all.sh ran a generator with `|| true`, so a build that refused to run printed ok while the same refusal fails the job in CI

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. Both now test the build's exit status first and report the refusal, then diff. The mark gate three lines above them was believed to be the model, and was not: it reported the refusal and then ran the diff anyway, printing ok on the next line. It was fixed the same day — see R5-21.

*How that was checked.* `grep -n '|| true' scripts/verify-all.sh` returned lines 123 and 153 — the Figma bundle build and the claude-code skill bundle build. Proved the new branch fires by replacing 13_plugins/figma/build.mjs with `process.exit(3);` and running the gate: `figma plugin build is current FAILED — the figma build refused to run`, failure flag 1. build.mjs restored and `git diff --quiet 13_plugins/figma/build.mjs` returns 0. `grep -c '^[^#]*|| true' scripts/verify-all.sh` now returns 0 — a plain `grep -c '|| true'` returns 2, both of them prose in comments explaining this very fix, which is why the quoted command discriminates code from comment.

#### R4-4 · verify-all.sh overwrote the committed manifest to test the gate and put it back without ever checking that the restore worked

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026: a gate of its own, `the placeholder test put the manifest back`, now diffs the file immediately after the restore, matching CI.

*How that was checked.* Proved it fires by leaving the placeholder in place and running the new block: `the placeholder test put the manifest back  FAILED — manifest.json was not restored`, failure flag 1. After restoring, the same block prints ok and `git diff --quiet 13_plugins/figma/manifest.json` returns 0.

#### R4-5 · The CI job's own comment said the Figma manifest is not committed, three lines above the steps that check the committed manifest

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. The comment now says why the build runs twice, states that the manifest is committed and since when, and keeps the part that is still true: CI cannot obtain a numeric Figma-issued id, and the gate says so rather than implying otherwise.

*How that was checked.* `grep -n 'the manifest is not committed' .github/workflows/ci.yml` now returns nothing. `sed -n '232,240p' .github/workflows/ci.yml` shows the replacement, and the file still parses as YAML.

#### R4-6 · The README told the reader to build the Figma plugin with `--code-only`, the one flag whose own build says its output will not load in Figma

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026 in scripts/readme.py, which generates both READMEs. The reader is now given the full build, with one line saying what the flag is for and who runs it.

*How that was checked.* `grep -n 'code-only' README.md` → no match in the rebuild block; the block now reads `cd 13_plugins/figma && node build.mjs`, followed by a sentence explaining that `--code-only` is what continuous integration runs to compare dist/ against what is committed. Regenerated with `./.venv/bin/python scripts/readme.py`; `--check` passes.

#### R4-7 · The guidebook told its reader to `cd` into a directory that exists on exactly one Mac in the world

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026 in the source chapter, which is where it was authored — the generator was copying it faithfully. The block now says "From the repository root, as with every command in this book", matching its neighbour.

*How that was checked.* `grep -c '/Users/' 09_guidebook/Aninda-Studio-Guidebook.html` → `1` before, `0` after; the one hit was line 2409, traced to 09_guidebook/chapters/12-applying-it.md:132 with `git grep -n '/Users/gru953' -- 09_guidebook/chapters`. Book and PDF regenerated; the chapters still pass the English standard, and `09_guidebook/build.py --check` and the PDF-versus-book check both pass.

#### R4-8 · The English standard's own gate printed a count it had typed: 17 paths, for a list of 18

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. The loop counts what it visits and prints that. Caught while adding a nineteenth path — the Claude Design push record, which is authored English prose and was not being held to the standard that governs authored English prose. Both the CI list and the local list now hold it, in the same order.

*How that was checked.* Counting the loop body by hand gave 18 against a printed 17. The gate now prints `english standard: 19 paths` for 19 entries. `./.venv/bin/python 13_plugins/claude-code/skills/aninda-review/scripts/check.py 13_plugins/claude-design/PUSH-RECORD.md` → `FAILURES (0)`, exit 0. `scripts/check_gates.py` still reports that every CI gate appears in verify-all.sh.

#### R4-9 · The guard added to stop CI destroying the manifest was itself broken, and turned CI red on the commit that introduced it

**Fixed, confirmed 25 August 2026.** Found by CI, not by the local mirror of the same gate — the local one runs from the repository root, where the path resolves, so it passed. Fixed the same day: the path is now relative to the step's own working directory and carries `--`, which tells git the argument is a path rather than a revision, so a missing file fails as a missing file instead of as an ambiguous argument.

*How that was checked.* Run 32863139436, job `plugins`, step `A placeholder manifest must stop the build`: `fatal: ambiguous argument '13_plugins/figma/manifest.json': unknown revision or path not in the working tree` followed by `::error::the placeholder test did not restore the manifest`. Every other job in that run passed. Reproduced and fixed locally by running the step verbatim from inside 13_plugins/figma: with `git diff --exit-code -- manifest.json` it prints that the gate refused the placeholder and the restore was proved, exit 0. Negative control in the same directory: leaving the placeholder in place makes the check exit non-zero, with no `ambiguous argument`. Auditing all five `git diff` invocations in ci.yml — `grep -n 'git diff'` returns six lines and the first is prose in a comment against the working directory each runs in, this was the only one inside a `cd`.

#### R5-1 · The guard that proves CI and the local script hold the same gates read only the first line of each CI step, so three real gates were exempt from it

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. The parser takes the whole block — every line indented deeper than the `run:` key — and a step counts as setup only when EVERY line in it is setup, tested line by line. `cd ` is out of SETUP entirely, with a note saying why. Where a gate's command names a file several gates name, the step is keyed by its own name instead, because a substring test on `build.mjs` passes even when the specific gate is gone.

*How that was checked.* Before: 32 gates compared, and deleting the full-build gate, the placeholder gate or the npm gate from a copy of verify-all.sh left the guard printing a clean pass, exit 0, each time. After: 36 gates compared, and each of those three deletions produces `1 of 36 CI gates are not in scripts/verify-all.sh`, exit 1. Enumerating the skips now shows only the six genuine installs. The change also exposed a real gap it had been hiding — see R5-2's sibling, R5-20.

#### R5-10 · The README listed a Bangla gap the plugin no longer reports

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026: the bullet is replaced by a sentence saying the gap closed and what the receipt does still report.

*How that was checked.* `08_components/_cards.json` → 30 cards, 0 missing `name_bn`, 0 missing `subtitle_bn`. `RECEIPT-EXPECTED.json['knownGaps']` → a single entry, about line height. `src/plan.ts:746` pushes the Bangla gap only when a count is above zero, and both are zero.

#### R5-11 · The manifest gate accepted any non-empty value for id and api — the exact thing its own failure text says it exists to prevent

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. Each field must be a non-empty trimmed string, and the api is compared against the single value this repository has a source for, naming scripts/figma-api-version.txt in the failure so the next version is adopted there first.

*How that was checked.* Against the real gate, eleven shapes: both good ones accepted (the committed slug, and a numeric Figma id), and all nine bad ones refused with a specific message — `"api" is "2.0.0". The only value this repository has a source for is "1.0.0"`, `"api" is number, not a string: 1`, `"id" is an array, not a string: ["x"]`, `"id" is only whitespace`, and so on. Before the change, six of those nine were ACCEPTED.

#### R5-12 · The plugin bundle was not a pure function of its inputs: esbuild wrote the caller's working directory into it

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026: both esbuild calls pin `absWorkingDir` to the plugin directory.

*How that was checked.* sha256 of dist/code.js built from 13_plugins/figma and from the repository root: `d4b5afd0316e99d0` both, identical, and identical to what is committed. Before, the two differed (275254 against 275203 bytes) in three module-path comment lines.

#### R5-13 · build.mjs's header said the --code-only output will not load in Figma, which stopped being true when the manifest was committed

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026, to the narrower true statement.

*How that was checked.* `git ls-files 13_plugins/figma/manifest.json` → tracked; `inspectManifest(...).ok` → true. The header now says only a full `node build.mjs` checks the manifest.

#### R5-14 · The plugin README's proof sentence counted 17 roles where there are 18, and claimed a pass over a space where 196 of 504 pairings are refused

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026 to the pairings the checker actually judges, with the reason the rest are outside the claim rather than inside it and failing.

*How that was checked.* Importing asset.py and running check_ground over every combination: all roles → 504 total, 308 pass, 196 refused. The judged set — seven TEXT_ROLES plus three NON_TEXT_ROLES — → 280 total, 280 pass, 0 refused. The README now says 10 × 7 × 4 = 280 and explains that a surface on a surface is not a contrast pairing.

#### R5-15 · The plugin README said the checker ends every run with nine things it cannot see; there are ten

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026.

*How that was checked.* `ast.parse` over check.py, counting the elements of the BLIND_SPOTS assignment → `10`. README line 117 now reads ten.

#### R5-16 · The type comparison said seven pairings while documenting eight, and ranked one of them wrongly

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026: six statements now match the eight the file documents, and the ranking claim is stated as measured. Two neighbouring claims were re-derived rather than assumed — pairing 01 still needs the least correction of all eight, and pairing 06 is still the most frictionless, being the only flat one whose three families are all free of a Reserved Font Name.

*How that was checked.* Body-size multipliers, best first: 01 0.872, 07 0.840, 06 0.831, 02 0.830, 04 0.818, 08 0.816, 05 0.757, 03 0.708 — so 07 is second. Reserved Font Names from font_facts.json: pairing 06 → none on any of the three; pairing 08 → `Plex` on IBM Plex Mono. `06_type/RECOMMENDATION.md` already said 8 pairings and 8 rendered pages, so the two documents had disagreed.

#### R5-17 · The website's counted "Fonts: 4" row carried a typed caption saying all three are subset and inlined, and none of the three claims held for the fourth

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026: the note is derived from the registry, naming the whole faces separately from the subset ones.

*How that was checked.* `_cards.json['_fonts']` → Literata, Noto Serif Bengali, Aninda Mono (no subset flag, so subset) and Aninda Mono (desktop) with `subset: False`. `grep -c '@font-face' 11_site/styles.css` → 3; `data:font/woff2` occurrences → 3. The page now reads "3 are SIL Open Font Licence 1.1, subset to what this page draws and carried inside the stylesheet. Aninda Mono (desktop) is the whole face, renamed rather than subset, and ships in 08_components/fonts/ ...".

#### R5-18 · The site footer called every face a subset, including the one its own registry records as not subset

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026: both flags are read, and each of the four states has its own wording.

*How that was checked.* The rendered footer now reads `Aninda Mono (desktop) — SIL OFL 1.1, renamed in full, not subset`.

#### R5-19 · The rule that nothing generated may carry an absolute path was written down and never measured, and the tree held 86 of them

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. specimen.py stores paths repo-relative and resolves them at the point of use; the two data files were migrated; every reader-facing instruction is repo-relative; and scripts/check_no_absolute_paths.py now measures the rule in CI and locally. Three evidence records are exempt by name, because they quote commands as they were run and rewriting a quotation would falsify the record.

*How that was checked.* `git grep -c '/Users/gru953'` totalled 86 across 25 files before; it now returns hits only in the three exempt evidence records. The new gate reports `no absolute home-directory paths in 326 tracked text files (3 evidence records exempt by name)`, exit 0, and refuses on injection: adding `# cd /Users/somebody/elsewhere/thing` to a copy of 05_colour/engine.py gives exit 1 naming the file and line. It matches any /Users/<name>/ or /home/<name>/, not only this Mac's, and exits 2 if it read fewer than 100 files. Every consumer still resolves: check_measurements.py passes, the guidebook --check passes, and the stored paths resolve to real files.

#### R5-2 · Both publishable packages shipped the Apache-2.0 appendix boilerplate as their LICENSE, not a copy of the licence

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. Both are now the repository's own LICENSE, read at build time rather than retyped, so there is one copy to keep right; and the build refuses to run if that file does not hold the Apache-2.0 terms.

*How that was checked.* `wc -c LICENSE 12_packages/npm/LICENSE 12_packages/python/LICENSE` → `11358`, `751`, `751` before; `11358`, `11358`, `11358` after. `grep -c 'TERMS AND CONDITIONS'` → `1`, `0`, `0` before; `1`, `2`, `2` after.

#### R5-20 · Every drift guard compared tracked content only, so a generator that started emitting a new file passed green over output nobody committed

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. CI marks the paths with `git add -N` before each diff, and the local script has a `drift()` helper that checks the diff and then looks for `??` entries under the same paths.

*How that was checked.* On a throwaway repository, adding a fifth colour direction and regenerating gave `git diff --exit-code` exit 0 with `?? 05_colour/generated/monsoon.proof.json` untracked. With the helper: a clean tree prints ok, `touch 04_mark/svg/_pretend_new_output.svg` prints `FAILED — the build wrote files that are not committed` and names it, and removing it prints ok again.

#### R5-21 · The mark gate reported a refusal and then printed ok on the next line, for the same gate

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026 to the same shape as the other two, and R4-3's note is corrected.

*How that was checked.* Reproduced as a five-line shell script: `FAILED — the mark build refused` followed by `ok`, `fail=1`. After: one line, `FAILED — the mark build refused`, `fail=1`.

#### R5-22 · The Claude Design bundle shipped a NOTICE directing recipients to two files the bundle did not contain

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026: all four root licence files travel with the bundle, and a missing one stops the build instead of being skipped by an `if exists` guard. The bundle went from 48 files to 50, which put the copy on claude.ai behind. That was stated in 13_plugins/claude-design/PUSH-RECORD.md rather than left to be discovered, and the owner then authorised the push that closed it the same day.

*How that was checked.* `grep -rn 'LICENSE-DOCS\|TRADEMARKS' dist/` → two hits in dist/NOTICE, lines 31 and 67; `git ls-files 13_plugins/claude-design | grep -E 'LICENSE-DOCS|TRADEMARKS'` → nothing, before. After: `50 files`, and both files are present at the bundle root. After the push: `DesignSync list_files` returns 50 paths against 50 from `find dist -type f`, compared with `comm` — neither side holds a path the other lacks. Four files were sent, the four that had changed since the first push, and `DesignSync get_file NOTICE` read back carries both LICENSE-DOCS.md and TRADEMARKS.md and no longer names the unregistered domain.

#### R5-23 · A typed word carried a count inside a generated sentence, where the count three lines above it is computed

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026: the word is looked up from the length of the dict.

*How that was checked.* NOT_IN_CHAIN holds 3 keys and the README still reads "Three generators are deliberately not in that chain" — the same output, now derived. `scripts/readme.py --check` passes.

#### R5-24 · The register rewrote the history of its own first pass every time an entry was re-checked

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. A pass is a historical fact: an entry carries the passes it has been through, an entry raised later belongs only to its own pass, and the heading of each entry shows the date of its most recent check.

*How that was checked.* The generated line now reads "64 entries were checked in the pass of 19 August 2026. 9 more were raised later, and 1 of the original entries was re-checked — 25 August 2026 ... of the 64 entries it covered, 18 were already fixed and 12 were half right" — 64, 18 and 12 again, matching what `git show origin/main:01_research/OPEN-FINDINGS.md` says at line 5.

#### R5-25 · The push record's card row contradicted itself: the breakdown summed to 30 and the total said 18

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026: two rows, each naming its own population.

*How that was checked.* `find dist -name '*.card.html' | wc -l` → 18. `grep -rho '@dsCard group=[^ ]*' 08_components/cards | sort | uniq -c` → Components 16, Foundations 6, Patterns 8 = 30. The bundle's own groups are seven different ones summing to 18.

#### R5-26 · Three evidence quotes written into the register the same day did not reproduce

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. Each quote is replaced by a command that reproduces, and the `|| true` one now discriminates code from comment. The register's rule is that a claim is either reproduced or it is not, and these three had been typed from memory a few hours after that rule was restated.

*How that was checked.* `grep -c 'git diff --exit-code 13_plugins/figma/manifest.json' .github/workflows/ci.yml` → 0. `grep -c '|| true' scripts/verify-all.sh` → 2; `grep -c '^[^#]*|| true' scripts/verify-all.sh` → 1, and that one is a `grep` whose empty result is not a failure. `grep -n 'git diff' .github/workflows/ci.yml` → 7 lines now, of which 5 are invocations.

#### R5-27 · The correction to the README's counts announced a check that did not exist — a promise of a guard, which is worse than no guard

**Fixed, confirmed 25 August 2026.** Fixed the same day, by making the sentence true rather than by deleting it. build.mjs now reads the README after computing the plan and compares five figures — variables, aliases, paint styles, text styles, and the primitive-versus-semantic split stated in prose beside the first — and stops the build on any disagreement.

*How that was checked.* `grep -c README 13_plugins/figma/build.mjs` → 0 before, and the build printed nothing about the README. After: `README table agrees with the plan on 5 counts`, then `Build finished.` Negative controls, both restored afterwards: changing `| Variables | 128 |` to 127 gives `BUILD STOPPED — the README disagrees with the plan it describes: README.md says Variables 127, the plan makes 128`; changing "18 semantic roles" to 17 exits 1. `git diff --quiet 13_plugins/figma/README.md` returns 0 after each.

#### R5-28 · The same correction left a typed count describing three bullets as four

**Fixed, confirmed 25 August 2026.** Fixed the same day: the sentence no longer counts the bullets it follows.

*How that was checked.* Counting `^- \*\*` between "Some things are deliberately not made" and that sentence → 3, against a stated four. `grep -n 'These four' 13_plugins/figma/README.md` → no output now.

#### R5-29 · Two of this pass's own fixes were verified by reading rather than by running, and one of them could not have been

**Fixed, confirmed 25 August 2026.** Both closed on the same day. The `git add -N` form was proved on a throwaway repository. specimen.py has not been run end to end and this says so rather than implying otherwise: what was proved is that its two new helpers round-trip against all 70 stored paths and that every stored path resolves to a real file. Re-running it fully is the remaining check, and it needs a browser and renders every specimen page.

*How that was checked.* `git add -N` control, in a scratch repository with one committed and one new file under gen/: `git diff --exit-code gen` → exit 0, the hole; `git add -N -- gen && git diff --exit-code gen` → exit 1, closed. specimen.py: importing it and applying `rel(absolute(x)) == x` to all 70 paths in font_facts.json and measurements.json gives 0 problems, and every one resolves to a file that exists. Downstream, `scripts/check_measurements.py` passes and `09_guidebook/build.py --check` passes.

#### R5-3 · The package build's --check compared neither LICENSE and never noticed a file the build did not write

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026 alongside R5-2. Both licences are in the dict, so the write path and the check path see one set, and --check now also fails on any file in either package that the build did not generate.

*How that was checked.* On a copy: replacing 12_packages/npm/LICENSE with "All rights reserved." gave `--check: both packages match the source. Nothing written.` exit 0 before, and `--check: 12_packages/npm/LICENSE differs from the build` exit 1 after. Adding `sneaky-extra.json` to the package gave exit 0 before and `--check: 12_packages/npm/sneaky-extra.json is in the package and is not generated by this build` exit 1 after. Baseline: `39 files`, exit 0.

#### R5-4 · The asset check never compared favicon.ico, the one binary it cannot regenerate and diff

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. An `.ico` branch reads the container with Pillow and compares its size list, then puts every plane through the same ink-geometry comparison the PNGs get — rasteriser-tolerant, because two rasterisers do not agree byte for byte.

*How that was checked.* On a copy: replacing favicon.ico with 26 bytes of text gave `--check: 21 asset files match the source.` exit 0 before, and `favicon.ico: could not be read as an icon container` exit 1 after. Stronger control — a structurally VALID .ico holding a red circle at the same three sizes — also fails now, per plane: `favicon.ico at 16x16: the artwork has moved — ink coverage 0.707 ... against 0.32`, and likewise at 32 and 48. Baseline unchanged, exit 0.

#### R5-5 · The Bangla cross-check degraded silently to nothing when its regex stopped matching, and no floor caught it

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. The count is measured against the id literals the file declares, not typed, and a parse that falls short by more than two reports that the comparison did not really run.

*How that was checked.* On a copy, inserting a comment between the id and the English string — valid Python, purely cosmetic — took the parse from 23 entries to 0. Before: exit 0, `WRONG (0) Nothing.` After: exit 1, `only 0 strings were parsed out of 06_type/review_bangla.py and it declares about 24 — the parse broke, so this comparison did not really run`. Baseline unchanged: 23 parsed, exit 0.

#### R5-6 · The guidebook said its claims rest on 57 sources; four of the 57 were Markdown table headers, and the book printed them as sources

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. The four rows are out of the data, and `block_sources()` now refuses to build at all if one reappears — a header row here means the extractor is wrong, which is worth stopping for rather than filtering away.

*How that was checked.* `len(sources)` 57 → 53; header rows 4 → 0. Per authority now Apple 16, Google 12, Standards and formats 8, Tooling and other design systems 17 = 53, which matches counting the data rows in BENCHMARK.md by hand. The book now reads "rests on one of the 53 sources", and `grep -o 'Date on the source' ... | wc -l` → 4, the four real `<th>` headers, where it was 8.

#### R5-7 · The Figma plugin README disagreed with the generated receipt beside it on four counts

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026: the four rows are taken from the receipt.

*How that was checked.* `RECEIPT-EXPECTED.json['expected']` → `variables 128, primitiveVariables 110, themeVariables 18, variableAliases 44, paintStyles 18`. The README rows now read 128 ("110 primitives, 18 semantic roles"), 44 ("11 roles across four themes") and 18.

#### R5-8 · The Figma README told a first-time reader the build would stop, and recorded that the manifest is not committed — both untrue since the day before

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. Step 1.4 states what the build actually prints and sends the reader on; the record states that the manifest is committed, why, and what still requires a Figma-issued id.

*How that was checked.* `git ls-files 13_plugins/figma/manifest.json` → tracked, added in 06793e5. `inspectManifest('.')` → `{ok: true, problems: [], publishable: false}`, so `node build.mjs` reaches "Build finished." `grep -c 'is not committed' 13_plugins/figma/README.md` → 0.

#### R5-9 · The README credited the receipt's Expected column to a file the plugin cannot read, so it claimed to catch drift it structurally cannot catch

**Fixed, confirmed 25 August 2026.** Fixed 25 August 2026. The README now says what the table compares — what this run intended against what it managed — and tells the owner to compare the printed SHA-256 and counts against RECEIPT-EXPECTED.json by hand, which is what that file's own comment describes.

*How that was checked.* `grep -c 'RECEIPT-EXPECTED' 13_plugins/figma/dist/code.js dist/ui.html src/ui.html` → `0`, `0`, `0`. `src/code.ts:1383` sets `expected: activePlan.totals`; `src/ui.html:274` reads `expected = message.expected`.

#### R7-1 · The Bangla rule is enforced on the book and the cards and not on a direction spec, so unverified Bangla entered through the one door nothing watches

**Fixed, confirmed 28 August 2026.** Fixed 28 August 2026, by inverting the rule rather than by adding a check at the door the finding named. The finding was right that the Bangla rule was enforced where words were SHOWN and not where they ENTERED — and with Bangla removed entirely, the question is no longer 'was this string checked?' but 'why is there Bangla here?'. That has no entry door to leave unguarded.

The English-standard checker now FAILS on Bengali script anywhere outside two retained record documents and the studio's own name. The name is allowed as a STRING rather than by exempting the six files that mention it, because six exemptions for one word would each also license any other Bangla in that file.

*How that was checked.* $ ./.venv/bin/python 13_plugins/claude-code/skills/aninda-review/scripts/check.py 01_research  ->  0 failures (Bangla in a retained record). The same checker on a file with an unrecorded Bengali run fails with 'Bangla in a system that ships English'. BANGLA_PENDING in that file, which listed the paths still carrying Bangla mid-removal, is empty.

#### R8-1 · The research method read guideline pages and not the feeds where the two stores announce things, so an announcement nine days old was missed

**Fixed, confirmed 28 August 2026.** Recorded and fixed on the same day, because the gap register had carried the fix since 26 August 2026 and the finding it asked for was never written. A gap that says 'recorded as a method finding' and points at no finding is exactly the kind of half-closed entry this register exists to prevent.

*How that was checked.* $ ./.venv/bin/python -c "import json; [print(x['authority'], x['url']) for x in json.load(open('01_research/_data/external-sources.json'))['sources'] if 'whats-new' in x['url'] or 'asset-best' in x['url'] or 'icon-design' in x['url']]"
  Apple developer.apple.com/app-store/asset-best-practices/
  Apple developer.apple.com/design/whats-new/
  Google developer.android.com/distribute/google-play/resources/icon-design-specifications

#### R8-3 · The Bangla removal was enforced on SCRIPT and not on CLAIMS, so 42 gates passed over a shipped stylesheet rule, a shipped code sample and about thirty English sentences that were all false

**Fixed, confirmed 28 August 2026.** Fixed 28 August 2026. The dead stylesheet rule, the dead code sample and the unclosed div are gone; the prose is corrected in about thirty places across the guidebook, the site, both stores, both packages, three plugins and the benchmark. The mechanical half is now gated; the prose half is not, and that is stated rather than implied.

*How that was checked.* $ ./.venv/bin/python scripts/check_token_citations.py
  ok    24329 custom-property citations across 82 documents, stylesheets and cards, every one defined — among the 57 in 07_tokens/css/tokens.css, or by the file itself (1 declared counter-example)

Proved to fail as well as pass: appending a line naming `--as-font-bangla` to a guidebook chapter exits 1 and names the file and line. Before the fixes it failed on 17 citations across two files.

### Closed by the owner's decision (2)

#### R3-3 · CLOSED 19 August 2026 — the three English glosses are settled

Settled by the owner. One was a real inconsistency and two were not.

**`th-3` was real, and worse than a gloss.** "High contrast" is what
`BANGLA-STANDARD.md` reviews the string under, what the register composes
`theme.hc-light` from as "High contrast, light", and what the guidebook and all
thirty cards ship. "More contrast" survived in two places — the review sheet and
`11_site/build.py`, where it was a **visible button on both published pages**. So
this was not two documents glossing one string differently; it was the website
labelling a control with a word the rest of the system does not use. Both are now
"High contrast". The Bangla is untouched: `বেশি কনট্রাস্ট` is the approved string
for it, and `BANGLA-STANDARD.md` records why `উচ্চ বৈসাদৃশ্য` was rejected.

**`wm-1` and `wm-2` are deliberately different, and are now recorded as such.**
The two files ask different questions. The review sheet's English column is "the
string this row is about", shown to a reviewer beside its Bangla; the plugin's
gloss is "what this Bangla means", used by an agent to find the right string. The
wordmark is drawn lowercase, so the sheet shows `aninda studio` while the name it
means is `Aninda Studio`; and the sheet labels the second row "Aninda Studio
(short form)" to say which wordmark is under review, while `অনিন্দ্য` alone means
"Aninda". Both answers are correct. The reconciliation is written into
`check_plugin.py` beside the exemption, so a future reader finds the reason rather
than an unexplained divergence to "fix".

`ms-2` was in this group and was not ambiguous: it read "That file is too big"
against a source saying "too large", and it is corrected.

With the ambiguous cases resolved, the gloss comparison now **fails** the plugin
check on any drift rather than merely reporting it.

#### R3-4 · CLOSED 19 August 2026 — the two revised Bangla strings are approved

`card.colour.subtitle` lost the numeral ১৭, and `card.the-marks.subtitle` lost
মোহনা. Both were changed because what they said had become false — seventeen
counted ten measured roles plus seven surfaces that carry no ratio at all, and
"Estuary" names the ground colour ramp, not the mark. Every approved word is
kept; only the false part is gone. The owner confirmed both on 19 August 2026;
`pending_review` is cleared and each entry's basis records the confirmation
alongside the reason for the change.

---

Generated by `scripts/findings.py` from `01_research/_data/findings.json`. Editing this file by hand is undone by the next build; change the data and regenerate. The counts above are counted, not typed.
