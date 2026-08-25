# Where this bundle was pushed, and how to tell whether it is still current

`dist/` is the only deliverable in this repository whose published copy lives on
someone else's service. Everything else can be rebuilt and byte-diffed here. This
one cannot, so without a record there is no way to answer two questions that
matter: *which* project holds it, and whether that copy has fallen behind.

| | |
|---|---|
| Project | **Aninda Studio Design System** on claude.ai, owned by the account that owns this repository |
| Pushed at commit | `289533b` — *The Claude Design push: a generated bundle, and the project is live* |
| Files in the bundle | 50, and 50 on the remote |
| Preview cards in the bundle | 18 |
| Source cards they are drawn from | 30 — Foundations 6, Components 16, Patterns 8 |

The project's identifier is deliberately not written down here. This repository is
public, and the identifier is useful only to someone already holding the owner's
login, so committing it would add a little exposure and no ability anyone lacks.
`DesignSync list_projects` returns it to the owner in one call.

## Brought level again, 25 August 2026

It had fallen behind earlier the same day. The bundle grew from 48 files to 50 when
`LICENSE-DOCS.md` and `TRADEMARKS.md` were added — the two files its own NOTICE sends
the reader to, and which had never travelled with it. Two other files had changed
since the first push as well: the NOTICE lost a line pointing at a domain nobody has
registered, and `tokens/primitive.tokens.json` gained the source URL and read date
for two accessibility figures.

Those four were pushed, and only those four: writing all fifty would have been
simpler and would also have hidden which ones actually moved.

## Checked after that push, 25 August 2026

Not asserted — measured against the live project.

**The path set is identical.** `DesignSync list_files` on the project returns 50
paths. `find dist -type f` returns 50. Sorted and compared with `comm`, neither side
holds a path the other lacks: nothing was missed, and nothing left behind by an
earlier push is still sitting there.

**A file's content is identical.** `DesignSync get_file NOTICE` was read back and
compared against `dist/NOTICE`: same opening, no `Site:` line, and both
`LICENSE-DOCS.md` and `TRADEMARKS.md` named in it — the specific change this push
carried. Local sha256 `f99753ccb2436480bf24dc2655e4b548d638098aa799611cedcfb81945a30f25`, 4,503 bytes. An earlier check on
`dist/readme.md` was identical byte for byte, sha256
`4809caa13c81633088265745bb208a53cf40623a38f103d522a2835ca222c3dc`.

## What this still does not prove

Two files have been compared across the two pushes, not 50, so this shows each push
landed and did not silently truncate — it does not prove every byte of every file
matches. A push that changed only `styles.css` would pass both checks above. To be
sure of a file, fetch that file and compare it.

## Re-checking after a change

Change the tokens, run `build.py`, push `dist/`, then repeat the two checks above
and update the date and the hash here. `build.py --check` proves the local bundle
matches the token source; it says nothing whatever about the remote copy, and it
is not able to.
