# Where this bundle was pushed, and how to tell whether it is still current

`dist/` is the only deliverable in this repository whose published copy lives on
someone else's service. Everything else can be rebuilt and byte-diffed here. This
one cannot, so without a record there is no way to answer two questions that
matter: *which* project holds it, and whether that copy has fallen behind.

| | |
|---|---|
| Project | **Aninda Studio Design System** on claude.ai, owned by the account that owns this repository |
| Pushed at commit | `289533b` — *The Claude Design push: a generated bundle, and the project is live* |
| Files in the bundle | 50 |
| Preview cards in the bundle | 18 |
| Source cards they are drawn from | 30 — Foundations 6, Components 16, Patterns 8 |

The project's identifier is deliberately not written down here. This repository is
public, and the identifier is useful only to someone already holding the owner's
login, so committing it would add a little exposure and no ability anyone lacks.
`DesignSync list_projects` returns it to the owner in one call.

## THE REMOTE IS BEHIND, as of 25 August 2026

Say it here rather than let it be discovered. The bundle grew from 48 files to 50
on 25 August 2026: `LICENSE-DOCS.md` and `TRADEMARKS.md` now travel with it,
because the NOTICE it already shipped sends the reader to both and neither was
there. The copy on claude.ai still holds 48 and does not carry them, so its licence
statement still points at two files it does not contain.

Re-pushing is the owner's action, not the build's. Until it happens, this file is
the only thing that says the two copies differ — which is exactly why it exists.

## Checked on 25 August 2026, before that change

Not asserted — measured, twice, against the live project.

**The path set was identical.** `DesignSync list_files` on the project returned 48
paths. `find dist -type f` returned 48. Sorted and compared with `comm`, neither
side had a path the other lacked: no file was missed by the push, and no file left
behind by an earlier one was still sitting there. The two files added later that
day are the whole of the difference now.

**A file's content is identical.** `DesignSync get_file readme.md` against
`dist/readme.md`, compared with `cmp`: identical byte for byte, sha256
`4809caa13c81633088265745bb208a53cf40623a38f103d522a2835ca222c3dc` on both sides.

## What this still does not prove

One file was compared, not 48, so this shows the push landed and did not silently
truncate — it does not prove every byte of every file matches. A push that changed
only `styles.css` would pass both checks above. To be sure of a file, fetch that
file and compare it.

## Re-checking after a change

Change the tokens, run `build.py`, push `dist/`, then repeat the two checks above
and update the date and the hash here. `build.py --check` proves the local bundle
matches the token source; it says nothing whatever about the remote copy, and it
is not able to.
