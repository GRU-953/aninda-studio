# Open findings — carried forward

Round 1 of the convergence review raised 59 findings across six independent
lenses, each adversarially verified before it counted. The blockers and majors
were fixed. These minors were judged not worth the change at the time, and are
recorded here rather than dropped, because an unwritten known fault becomes an
unknown one within a week.

Each is real and reproducible. None affects correctness of the design system's
output. If you disagree with a judgement, the finding is here to be picked up.

### 1. Overflowing horizontal scroll containers on every card and on the site are real tab stops that the design system's focus rule and check.py's INTERACTIVE selector both exclude

`08_components/src/components.css`

These are the only tab stops in the system whose focus indicator is not the system's. The token ring is 3 px solid var(--as-focus-ring) at 2 px offset; what actually appears is Chromium's UA default, outline: auto 1px rgb(0, 95, 204), in all four themes including hc-dark — so the one visual the project measures hardest is, at these stops, whatever the browser supplies. This is not a contrast failure (the UA ring measured 5.71:1 in light and 18.77:1 in dark against the ground it replaced), which is why it is minor; the defect is that no check can ever confirm that. check.py's INTERACTIVE selector requires a tabindex, an interactive tag or an ARIA widget role, and these containers have none, so a stop that Tab reaches on all 30 cards and the site has never been measured for ring thickness, ring contrast or forced-colors survival. Adding tabindex="0" with role="region" and an aria-label — the standard technique for a scrollable region — would fix the indicator, replace role "generic" with a named region, bring the stops inside INTERACTIVE, and remove the dependence on a Chromium-only behaviour that WebKit does not implement.

### 2. Semantic theme files are not resolvable as standalone DTCG documents, and nothing shipped says so

`07_tokens/build/semantic.light.tokens.json`

The kit describes each of these files as DTCG 2025.10 in its own right, and the plugin hands them to a consumer individually. A spec-conformant single-document tool loading semantic.dark.tokens.json gets ten unresolvable references and no instruction telling it what to load alongside. The fix is documentation, not restructuring — one sentence in SKILL.md and the guidebook token chapter saying the semantic files resolve only when merged with primitive.tokens.json — but as shipped a reader has to infer it from the failure.

### 3. Reserved-Font-Name family count is wrong in two research documents that label the figure as mechanically extracted

`06_type/SHORTLIST.md`

Both documents mark this figure **[file]**, the repository's own convention for "read directly out of the font file, reproduce with 06_type/specimen.py", which invites the reader to trust it without rechecking. The count is the one that decides whether a family can be subsetted without renaming, so a reader picking a substitute face from the shortlist could take a Plex or Source family as RFN-free. It contradicts the table printed three lines above it.

### 4. The $schema every token file declares resolves to the DTCG living draft, not the 2025.10 report the same file pins

`07_tokens/build/primitive.tokens.json`

The files go to unusual lengths to distinguish the frozen 2025.10 report from the moving draft — it is the point of the `spec` extension string and of BENCHMARK section 6.2 — and then the machine-readable field points at the moving one. Anything that dereferences `$schema` to decide which rules to apply lands on the 30 July 2026 draft, whose requirements can diverge from the version the file claims. Pinning `https://www.designtokens.org/TR/2025.10/format/` would make the two agree; leaving it as is means the version claim survives only in prose a tool is permitted to ignore.

### 5. README.bn.md mixes Bengali and Western numerals inside single sentences, against house rule 9 of the Bangla standard

`README.bn.md`

The Bangla README is one of two front doors to the project and the main demonstration that the Bangla is written as Bangla rather than translated. Two numeral systems inside one sentence is the most visible possible signal that the Bangla was assembled rather than written, and it lands in the paragraph whose whole point is that the numbers are trustworthy. It also breaks a rule the project itself researched, sourced and wrote down.

### 6. The plugin reference file that documents the mark is named logo.md, the one word the plugin's own naming rule forbids for it

`13_plugins/claude-code/skills/aninda-brand/references/naming.md`

This is the exact failure the naming rule was written to prevent, in the artefact whose job is to teach the rule. An agent or a person reading SKILL.md is told to open references/logo.md to learn that the thing is never called a logo, and SKILL.md's own description offers 'a logo' and 'mark' as two different things you might ask for. Because check_plugin.py hard-requires the filename, the wrong name is now pinned in place by CI.

### 7. The wordmark ships set in lowercase while the chapter that presents it says "Sentence case, always", with nothing reconciling the two

`09_guidebook/chapters/02-the-name.md`

The chapter's own second section is titled "The one thing that looks like an inconsistency, and is not", and it spends five sentences explaining the অনিন্দ্য/aninda transliteration gap so that nobody has to wonder. The casing gap gets none of that treatment: a reader sees lowercase artwork at the top of the page and an unqualified "Sentence case, always" twenty-six lines below, with no row in the table and no note. Anyone setting the name in a lockup has to guess which of the two governs, and the earlier draft shows the distinction was understood and then lost.

### 8. The guidebook PDF and three other committed generated trees have no drift guard anywhere

`.github/workflows/ci.yml`

The PDF and the 20 platform assets are both named deliverables, and .gitignore's header claims the reason they are committed is "what lets CI regenerate them and fail on any difference" — true for the token set, the marks, the cards and the packages, not true for these. Change a guidebook chapter and CI proves the HTML was rebuilt while the shipped PDF silently stays the old book. That is precisely the failure the tokens job was built to catch, in the one artefact a reader is most likely to print and keep.

### 9. The 18 August coverage correction was applied to the two READMEs only; the wording it set out to remove survives in the guidebook and in the harness that prints it while running on Ubuntu

`09_guidebook/chapters/14-what-this-system-does-not-do.md`

The commit's own reasoning was that a claim stale in a favourable direction is still stale. It was fixed in the two files whose numbers are generated and checked, and left in the flagship deliverable and in a script that now states it about itself while contradicting it. A reader of the guidebook gets the superseded scope, and the two documents now disagree on a coverage claim.

### 10. Two superseded pre-decision drafts ship in the published repository, unlabelled, arguing against the decisions the system actually made

`_reference/DRAFT-benchmark.html`

This is a brand repository, so an unlabelled HTML page that presents a different palette, different typefaces and a contradicted icon policy is the one kind of stray file that does real damage: opened on its own it reads as the brand. The directory is documented nowhere, so there is nothing to tell a reader these were superseded on the way to the decision recorded in 04_mark/manifest.json.

### 11. README.bn.md silently drops a whole section and the asset.py demonstration, with no note that it is abridged

`README.bn.md`

Everywhere else the project declares its Bangla gaps at the point of the gap — 11_site/index.html closes with "Bangla appears only where the verified table in 06_type/BANGLA-STANDARD.md holds a string ... those places are listed in this build's output", and the Bangla guidebook chapters carry a {{gap-notice}}. The README pair is the one place that omits without declaring, so a Bangla reader has no way to know a section exists that they were not shown — including the commands for rebuilding the system, which need no translation.

### 12. Outstanding, not a defect: the Claude Design push has not been done; the local side is ready and only the push remains

`08_components/cards`

This is the one requested artefact with no local work left. What remains is the push itself: pick or create a design-system project, finalize a plan covering 08_components/cards/**/*.html, upload the 30 files, and let the pane build its card index from the @dsCard markers (the three groups are already Foundations 6, Components 16, Patterns 8). Worth recording so it is not mistaken for a build gap — and worth doing before the 30 cards move again, since nothing will tell you the remote copy has fallen behind.

### 13. TOOLCHAIN.md documents Jinja2 as the templating engine for the guidebook and the component cards; nothing in the repository imports it

`00_sandbox/TOOLCHAIN.md`

The document's stated purpose is a traceable account of what this build depends on and what each dependency does. A pinned package with an invented job in it is the same class of error the project's own README warns about — a sentence a human wrote once that nobody re-reads. It also misleads anyone auditing the licence surface, since Jinja2's BSD-3-Clause is listed as in-use when no code path touches it.

### 14. pypdfium2 is a pinned dependency imported by the PDF verifier but is missing from TOOLCHAIN.md's package table

`00_sandbox/TOOLCHAIN.md`

The one dependency omitted from the toolchain document is the one that backs a verification claim ("no page is blank — every page is rendered with pypdfium2 and its pixels sampled"). A reader auditing the build from TOOLCHAIN.md alone gets an incomplete dependency and licence list, and the file's closing assurance about "every package above" silently excludes it.

### 15. pdf.py records a probe measurement of 55 pages; re-running the documented probe today gives 58

`09_guidebook/scripts/pdf.py`

The docstring's whole point is that "the reason for the two-file split stays a measurement rather than a memory", and it has become a memory — the recorded page count no longer matches what the script reports. The MB/MiB mislabelling means the repository states two different sizes for the same PDF and the same HTML file in its two most-read technical documents, with no way for a reader to tell which convention is meant.

### 16. BENCHMARK.md still says the kit does not exist yet, and all 28 promised verdicts are unfilled

`01_research/BENCHMARK.md`

README.md line 62 sells 01_research/ as "What was checked, when, and against which source". The document instead asserts, in a published repository, that the artefact it is measuring does not exist — a statement that is simply false today — and leaves unredeemed an explicit promise that the verdict column would be completed by inspection. Its own criterion 28 ("no number appears that cannot be traced to one") is among the 28 left unjudged.

### 17. The guidebook and the card harness state that measurement happened on macOS only and on one machine, which CI contradicts on every run

`09_guidebook/chapters/14-what-this-system-does-not-do.md`

Two of the five measurements the chapter attributes to macOS alone — the contrast readings and the focus ring — are re-run on Ubuntu on every push, which is the basis of the README's stronger claim. One of the two documents is wrong about the same fact, and the harness's own blind-spot list, which it introduces as "part of the result, not an apology", prints a false line about the platform whenever CI runs it. A limit stated wrongly is as costly here as a limit omitted, because the whole chapter is offered as the calibration for everything earlier in the book.

### 18. NOTICE publishes a studio website address that does not resolve

`NOTICE`

NOTICE is the file a redistributor is required to carry, and it is where the project directs anyone seeking permissions. It points at a domain that is not registered. The site build already knows how to state an unfinished fact plainly — 11_site/index.html carries a "Not published yet" panel about the packages — so the omission here is inconsistent with the project's own standard, and a sitemap and CNAME built on an unregistered domain will silently do nothing when the site is deployed.

### 19. 07_tokens/build.py's proof check ignores its own `proof` argument and compares two numbers the generator guarantees agree

`07_tokens/build.py`

The docstring promises two things the code does not do — re-reading, and comparison against the proof — and the ratio assertion is structurally incapable of failing on any output this generator produces. It reads as independent verification and is not. Either re-derive the ratio from the two hexes with the same formula the engine uses, or delete the claim; the component and site harnesses are the only places contrast is actually re-measured.

### 20. engine.py and emit_css.py --check never compare against the committed output, so a hand-edited generated file passes

`05_colour/engine.py`

Five of the seven --check modes in this repository compare against the committed bytes; these two do not, and emit_css.py's message ("CSS re-parsed and matched against source") reads as if it had. Anyone using --check locally as the drift gate — which is what the phrase invites — gets a false pass, and the only thing actually holding the line is one git-diff step in CI. Either compare against disk or reword to "re-verified the freshly generated set".

### 21. A malformed direction spec escapes 05_colour/engine.py as a traceback with exit 1, not the documented exit 2

`05_colour/engine.py`

The two exit codes exist so a caller can tell "this palette cannot support the role you asked for" from "I could not read your input" — the distinction the file spends a paragraph justifying. A malformed spec reports the first while meaning the second, and does it as an unhandled traceback. Wrap the family construction in the same NotEquipped conversion the JSON parse already gets.

### 22. 12_packages/build.py --check writes VERSION to disk while printing "Nothing written"

`12_packages/build.py`

A verify-only mode that mutates the tree is the one thing --check must never do, and CI runs this mode. It also means a missing VERSION is silently resurrected as 1.0.0 rather than reported: if the real version were 2.3.0, the packages would be regenerated against a fabricated version rather than the run failing. Split the read from the create, and have --check report a missing VERSION instead of writing one.

### 23. 08_components/check.py drops measureText's "could not measure" list in the forced-colours pass

`08_components/check.py`

The docstring says "The harness prints what it could NOT check at the end. That list is part of the result, not an apology." In forced-colours mode it silently is not: an element whose background cannot be composited is skipped, unmeasured and unreported, so the forced-colours contrast pass can report clean over text it never looked at. One extra loop, matching the main pass.

### 24. 11_site/check.py's external-reference finding is only ever an ok note, never a problem

`11_site/check.py`

"the page works offline" is a stated property of this site, and 11_site/build.py enforces it at build time (lines 1085-1097, `raise BuildError(f"{name} fetches {target} from the network.")`). The browser check, which is the only thing that sees the rendered page, records a violation as a pass and phrases it as reassurance. Make it a problem, or drop the collection so the note cannot be mistaken for enforcement.

### 25. 09_guidebook's external-asset guard inspects <source> but its regex cannot see srcset

`09_guidebook/build.py`

A 14 MB self-contained book whose whole promise is that it opens with no network. The guard lists the one element whose entire purpose is the attribute it cannot read, which reads as coverage it does not have. Add `srcset` and `poster` to the attribute alternation.

### 26. ring_from_diff's `thickness` is not ring thickness, so the 2px focus-ring floor cannot fail for a whole-box change

`08_components/check.py`

A background inversion is a legitimate focus indicator under SC 2.4.13, so the pass is defensible — but the number reported is the control's own size dressed as a ring measurement, which means RING_MIN_PX is dead for any element whose focused appearance differs across its whole box. A focus style that changed the fill and put a border on one side only would report sides [60, 60, 44, 44] and clear the floor with three sides bare. Measure the ring as changed pixels OUTSIDE the element's own box, or rename the figure to what it is.

### 27. engine.py's header states the perturbation sweep is 64 measurements; it is 729

`05_colour/engine.py`

This paragraph is the file's own account of its central method, quoted onward into 07_tokens/build.py's generated $description text ("nudged by ±1. The published figure is the worst of those"). The measurement is stronger than the number claimed, so the error is in the safe direction, but it is the kind of unverified stated fact this repository otherwise refuses to ship.

### 28. scripts/readme.py walks the entire repository to compute a figure neither README uses, and prints it as a counted fact

`scripts/readme.py`

Every line of the --check output reads as "this number in the README was verified against the thing it describes". One of the eighteen is asserted nowhere, is derived from the working tree rather than the repository, and costs a full recursive walk. It invites the reader to trust a figure that is not under any guard.

