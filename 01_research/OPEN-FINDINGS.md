# Open findings — carried forward

<!-- This file ships, so it is held to 02_strategy/ENGLISH-STANDARD.md like any
     other prose here — including the banned-word list. Four banned words arrived
     in it when the findings were copied in verbatim from the reviewers' own
     wording, and CI's lint job caught them. If you paste a finding in, reword it.
     A findings record that breaks the rule it records findings about is a poor
     advertisement for the rule. -->

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

README.md line 62 sells 01_research/ as "What was checked, when, and against which source". The document instead asserts, in a published repository, that the artefact it is measuring does not exist — a statement that is false today — and leaves unredeemed an explicit promise that the verdict column would be completed by inspection. Its own criterion 28 ("no number appears that cannot be traced to one") is among the 28 left unjudged.

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


---

## From round 2

Same judgement as above: real, reproducible, not affecting the correctness of the
system's output. Recorded rather than dropped.

### R2-1. Both published site pages date themselves 2026-08-14 and claim their counts were taken that day, while the same page reports checking registries on 2026-08-18 and the file was regenerated on 18 August

`11_site/build.py`

"Counted on 2026-08-14" sits in the same sentence as the assurance that every number is counted at build time, so a typed date is presenting itself as provenance for figures that were recomputed on a different day. The page states two different dates about itself and the wrong one is the one a reader would use to judge how current the counts are. The sitemap's lastmod misinforms crawlers for the same reason, and nothing in CI or in 11_site/build.py --check can notice, because the constant is regenerated identically every time.

### R2-2. The table and dashboard cards ship hand-typed contrast figures under a caption saying they were measured and an alert titled "These figures come from check.py", against README's claim that no hand-written contrast figures exist in the repository

`08_components/build.py`

The README's blanket claim is falsified by the shipped cards: five typed contrast ratios carried under a caption that calls them measured, on 2 of the 30 cards. The alert's title and body contradict each other, so whichever a reader believes, the card has told them something untrue. In a kit whose stated reason for having no typed ratios is that a typed number can be wrong and stay wrong, an invented "Failed" verdict against one of its own cards is the one kind of demo content that cannot be read as neutral filler.

### R2-3. CI enforces a seventh banned word that appears in no published blocklist, so a writer who follows the English standard exactly can be failed by it

`02_strategy/ENGLISH-STANDARD.md`

The rule as published is the rule a writer reads, and it is a strict subset of the rule CI applies. A contributor who obeys the standard word for word can still be failed on a step that names this document as its authority, and neither of the two places the project publishes the blocklist — the standard itself and the guidebook chapter whose whole purpose is to state it — lists the seventh word. The standard's assurance about what CI covers is written as an exact account ("stated exactly, because the previous version of this section overstated it") and is still not exact.

### R2-4. OPEN-FINDINGS.md records as an open, reproducible fault a directory that was removed and gitignored one commit before the file was written

`01_research/OPEN-FINDINGS.md`

This is the project's register of what is still wrong, and it makes a false statement about the repository it ships in — that superseded drafts are being published — while asserting that every entry is real and reproducible. A reader auditing the outstanding list will go looking for a path that does not exist, and finding one entry closed silently makes the other twenty-seven harder to trust. Item 12 of the same file is also labelled "not a defect", so the count of twenty-eight minors does not describe twenty-eight minors.

### R2-5. README's headline command is described as taking about a minute; it takes 3.3 seconds

`README.md`

This is the first command the README asks a reader to run, and the duration is the one figure in that paragraph a person can check in three seconds. It is wrong by a factor of eighteen, in a document generated by a script whose header states "Every number below is counted from the repository, not typed" — this one is typed, and it sits beside numbers that are not. The project's own voice rule (chapter 10: "Say the number and its unit") makes a stale duration a rule break as well as an inaccuracy.

### R2-6. The Bangla README omits the rounded-icon limitation entirely, so one of the two front doors does not disclose the deliberate departure from Apple's guidance

`README.bn.md`

Both READMEs open by promising the same thing — README.bn.md: "কোনো কিছুর সীমা থাকলে সেটা এখানেই লেখা থাকবে — লুকিয়ে রাখা হবে না" ("if something has a limit it will be written here, not hidden"). The icon decision is the one place the kit knowingly departs from a platform vendor's published guidance, and it is disclosed to English readers and not to Bangla readers, in the section whose only job is disclosure. Elsewhere the project declares its Bangla gaps at the point of the gap; here a limit is absent, so a Bangla reader has no way to know one was withheld.

### R2-7. The tabs card's panels are unreachable by keyboard and the markup it teaches omits the tabindex that would fix it

`08_components/cards/components/tabs.html`

The WAI-ARIA Authoring Practices tabs pattern requires tabindex="0" on a tabpanel that holds no focusable element, so that after choosing a tab the reader can put focus into the panel and page through it. Without it a keyboard-only user activates a tab and focus jumps past the content they only revealed, with nothing focused inside the region they were reading. The card is the system's teaching artefact for this pattern and says so in its own panel text — 'Arrow keys move between the tabs and Home and End jump to the ends, which is what the roving tabindex on this pattern requires' — so the omission is copied by anyone following it. This is guidance rather than a WCAG success criterion, and the panels here are two short paragraphs, which is why it is minor rather than more.

### R2-8. The site harness's structure and Bangla-language probe runs on index.html only, and its Bangla expression has no script/style skip list

`11_site/check.py`

Round 1 removed four CI steps that could pass without running. This is the same shape one level down: a harness that measures two pages reports a structure result derived from one, and prints it as an unqualified pass, so a regression on 404.html — a missing skip link, a lost <main>, an untagged Bangla string — is green. The skip-list omission is the reason the check cannot be pointed at the component cards as it stands: it would fire on every card's own stylesheet comment and the real defects would be indistinguishable from the noise. Both are cheap to close, and closing them is what would let one guard cover all thirty-two shipped pages instead of one.

### R2-9. The accessibility card's subtitle double-escapes an em dash, so the entity is read out as literal text on the one card whose subject is accessibility

`08_components/build.py`

A screen reader reads the visible characters, so the card's one-line summary is announced as 'forced colours ampersand m dash semicolon the mode where…' — six syllables of markup in the middle of a sentence, on the card a reader most likely reaches with a screen reader precisely because it is the accessibility card. It is also a visible defect for everyone. The site and the guidebook prove the string itself is right and only the card's escaping is wrong, so three surfaces built from one entry in 08_components/_cards.json now disagree about what that entry says, and the card generator is the only one that cannot pass an entity through.

### R2-10. A banned word is used in shipped prose in a lint-covered path, and the CI blocklist guard cannot see it because the same paragraph contains a rule-statement phrase

`01_research/OPEN-FINDINGS.md`

The one file round 1 added to carry findings forward breaks the rule it was added under, in a path CI lints, and CI passes it. The mechanism matters more than the single word: RULE_STATEMENT operates on a whole line, and "rather than" and "instead of" are ordinary connectives, so any paragraph-per-line document — which is the house style for 01_research — gets a free pass on all six banned words the moment one appears. ENGLISH-STANDARD.md tells the reader "every banned word and idiom above is in the checker's blocklist, and CI fails on a hit", which is now true only for files that hard-wrap.

### R2-11. The site header's brand lockup loses its tile in both dark themes: the icon's baked-in ground measures 1.05:1 against the page it sits on

`11_site/index.html`

The primary lockup on the studio's front door reads as two different marks depending on theme — a rounded dark tile with a knocked-out 'a' in the two light themes, a bare floating 'a' in the two dark ones — on a site whose own theme switcher makes all four first-class. The mark stays legible, which is why this is minor, and the icon is fixed artwork by policy, but nothing shipped says the header deliberately keeps a fixed ground, so a reader comparing the header against the marks card's stated rule finds them disagreeing. The site's contrast harness cannot catch it: the icon is aria-hidden and the site's claim is scoped to "the contrast of every piece of text".

### R2-12. The token files name a ramp "family", the one word the naming reference forbids for it

`07_tokens/build/semantic.light.tokens.json`

One thing carries two names inside the same shipped file — `ramp` in the token path and `family` in the extension on the leaf beside it — and the second is the word the project's own naming authority names as wrong. A consumer reading $extensions.studio.aninda to group roles by ramp has to learn that `family` means `ramp`, which is the exact cost the naming rule exists to avoid. It is minor because the key is machine-readable rather than prose, and because nothing breaks; it is worth recording because naming.md is enforced nowhere and this is the one place its vocabulary table is contradicted by generated output rather than by prose.

### R2-13. 07_tokens/build.py's $schema check compares the emitted document against the constant that wrote it, so it is structurally incapable of failing

`07_tokens/build.py`

It reads as a conformance check on the one machine-readable field that tells a consuming tool which rules to apply, and it can never report anything. This is the same shape as the already-recorded finding 19 about the proof-ratio assertion, but a different check that OPEN-FINDINGS.md does not cover, and the two together mean two of check()'s gates are tautologies inside a function whose docstring is "Re-read what was built and prove it, rather than trusting that it was built." The only thing standing between a wrong $schema and a release is the CI git-diff, which reports that bytes changed without knowing why.

### R2-14. 11_site/check.py's reduced-motion check reports "reduced motion honoured" and exits 0 when the property it measures does not exist at all

`11_site/check.py`

This harness exists because "build.py can only prove that the site was WRITTEN correctly. This proves it BEHAVES correctly." Reporting a measurement as honoured when the measured value is absent is the same shape as the already-fixed bug where the site's stylesheet never loaded and no check noticed: a note that reads as reassurance about something the script never saw. The nearby forced-colours check gets this right — it probes for liveness first and refuses to pass if the emulation is inert — so the pattern for handling "I could not see it" already exists in the same file, eleven lines above.

### R2-15. 05_colour/engine.py's documented exit-1 failure — a palette that cannot support a role — is unreachable, and its remedy names an input that provably cannot change the outcome

`05_colour/engine.py`

The file spends a paragraph justifying the 1-versus-2 exit-code split, and the meaning it gives to 1 is "a real failure — a palette cannot support a role". That is the branch a reader is told to expect when a direction is unbuildable, and it is the one branch that no direction spec can produce. Worse, the message instructs the reader to change the anchor, which alters only hue and chroma while the outcome depends entirely on lightness — so a reader who somehow reached it would be sent to the wrong file. Either derive the ramp's lightness from the anchor as well, or state plainly that a direction spec cannot fail a contrast target and that this branch guards against a future change to LIGHTNESS.

### R2-16. tag_inline_bangla's docstring claims Bangla inside attributes is counted by the guard and named in a chapter; neither the counter nor the chapter text exists

`09_guidebook/build.py`

This is a claimed check that does not exist, in the docstring of the function that fixed 286 Bangla nodes shipping announced as English. A reader auditing WCAG 2.2 SC 3.1.2 coverage is told the residual attribute case is counted and documented, so they will not look for it; if a future chapter adds a Bangla alt text or aria-label, nothing counts it, nothing reports it, and the limit the docstring promises is written down is written down nowhere. The fix is small — either add the count the sentence describes, or delete the second half of the sentence.

### R2-17. 08_components/build.py's no-literal-colour guard does not treat CSS system colour keywords as literals, so hard-coded ButtonFace, ButtonText and AccentColor pass

`08_components/build.py`

A system colour keyword outside a forced-colors block paints one fixed operating-system colour in all four themes and ignores every token, which is exactly the class of value the guard exists to keep out of the hand-authored layer — 07_tokens/build.py puts them in a separate non-DTCG file precisely because they are colours the system supplies. Nothing downstream would catch it either: it would not change with data-theme, and no check verifies that a painted colour differs between themes. It is minor because reaching it takes a deliberate edit to components.css and the keywords are arguably outside the guard's intended vocabulary — but the guard's stated rule is unqualified, and the same omission lets `color-mix()` through when both its operands are keywords.

### R2-18. The Bangla review sheet's checkboxes are 16 px, below SC 2.5.8, and no harness measures the page

`06_type/BANGLA-REVIEW.html`

The kit's central accessibility claim is WCAG 2.2 AA proven, and its own checker fails a committed interactive page against SC 2.5.8. The buttons on the same page were given `min-height:44px` deliberately, so the floor was understood and the 24 controls a reviewer actually clicks were missed. It is also the page a second Bangla reader is asked to work through, which is the audience least well served by a 16 px target.

### R2-19. 12_packages --check reports "6 DTCG documents" while one of the six is declared not DTCG

`12_packages/build.py`

This line is the one confirmation a reader gets that the DTCG documents in the package are conformant, and it counts a file the kit insists three times over is not one — so the number that certifies conformance is the number that includes the exception. The file's own comment names this string as a past false claim and then re-emits it, which is exactly the drift the repository built its guards to stop.

### R2-20. The aninda-repo skill promises two full licence texts and ships neither a template nor the text

`13_plugins/claude-code/skills/aninda-repo/SKILL.md`

Two of the eight files the skill exists to write have no source in the bundle, so an agent following it either reproduces a licence text from memory or fetches one — in a skill whose own reference file forbids paraphrasing a licence identifier from memory, and for the one licence (PolyForm Noncommercial) most readers cannot recall. The Apache text is sitting in the bundle root and could be copied, but nothing says so.

### R2-21. The website inventories the guidebook, the 30 cards and both packages and provides a route to none of them

`11_site/index.html`

The site is a named deliverable and the kit's public front door. A reader who arrives, reads descriptions of 30 components and two packages, and wants to see one has nowhere to go: no link to the guidebook, no link to a card, and no mention of the public repository that holds them. Hyperlinks are not subresources, so the site's offline-and-self-contained property does not stand in the way — the npm README already links the repository from inside a shipped artefact.

### R2-22. COMPARE.pdf and all eight files in 03_directions/shots have no writer anywhere in the repository

`03_directions/build.py`

10_assets/build.py opens by stating the house rule — "Nothing here is hand-drawn and nothing here should be hand-edited" — and these nine files are the exception: no generator, so no way to reproduce or check them, and no document explaining what they are. Two of them are unlabelled pre-decision pages showing marks and palettes the project rejected, which is the same class of stray the repository removed _reference/ to stop shipping. A reader opening _m2.html sees four candidate identities with no indication which, if any, is the brand.

### R2-23. Outstanding, not a defect: the Claude Design push is still to be done, and the deliverable is named in no shipped surface

`08_components/cards`

This is the one requested artefact with no local work left, so it should not be mistaken for a build gap. It is worth doing before the 30 cards move again, because nothing will report that the remote copy has fallen behind. The second half is a real completeness gap in its own right: a named deliverable recorded only in a carried-forward findings file is invisible to anyone reading the kit's own inventory, so a future rebuild has no reason to know the push is owed.

