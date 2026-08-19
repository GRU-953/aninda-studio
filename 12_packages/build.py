#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
So that any future project can pull the Aninda Studio tokens in with one command
instead of copying files, and so the copy it pulls is provably the same one the
guidebook and the component library were built from.

It writes two packages from one source: an npm package and a Python package.
Neither is hand-maintained; both are emitted here and verified against the source
before anything is written.

WHAT SHIPS, AND IN WHAT ORDER OF AUTHORITY
------------------------------------------
The **DTCG token file ships verbatim**, at the top of both packages. That is the
point of authoring in a standard: a consumer with their own build can read the
tokens directly and never touch our CSS. The stylesheets are a convenience view of
that file, never the other way round — and the check below proves the two agree by
re-deriving every custom property from the DTCG source and comparing.

VERSIONING
----------
One version for the whole system, held in `VERSION` at the repo root. Both packages
publish at the same number even when only one changed. An occasional no-op release
costs nothing; two drifting version numbers cost real confusion.

PUBLISHING IS NOT DONE HERE
---------------------------
This script builds and checks. It never publishes and never touches a credential.
The exact commands to run are printed at the end, for a person to run.

RUN
---
    cd /Users/gru953/Claude/Cowork/Aninda_Studio
    ./.venv/bin/python 12_packages/build.py
    ./.venv/bin/python 12_packages/build.py --check
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOKENS = ROOT / "07_tokens" / "build"
CSS = ROOT / "07_tokens" / "css" / "tokens.css"
VERSION_FILE = ROOT / "VERSION"

NPM_NAME = "aninda-studio-tokens"
PY_NAME = "aninda-studio-tokens"
PY_MODULE = "aninda_studio_tokens"
AUTHOR = "Aninda Sundar Howlader"
EMAIL = "aninda.sh15@gmail.com"
REPO = "https://github.com/GRU-953/aninda-studio"
# The repository, not anindastudio.com. That domain is chosen and NOT registered
# — the .com registry returned "No match" on 19 August 2026 — so a homepage
# pointing at it sends anyone who clicks it from npm or PyPI to nothing. The
# repository is the thing that actually exists.
HOME = "https://github.com/GRU-953/aninda-studio"

THEMES = ("light", "dark", "hc-light", "hc-dark")

BLURB = (
    "The Aninda Studio design tokens: colour, type, space, shape and motion, in "
    "four themes — light, dark, and a high-contrast pair. Every colour pairing was "
    "measured rather than chosen, against WCAG 2.2 AA in the ordinary themes and "
    "AAA in the high-contrast ones."
)


# The Python usage examples. They are constants because check_python_examples()
# EXECUTES them against the built package before the README that quotes them may be
# written. The old README's two samples were JavaScript relabelled as Python and
# neither one ran.
PY_EXAMPLES = {
    "basic": (
        f"from {PY_MODULE} import css, css_path, THEMES\n"
        "\n"
        "print(THEMES)            # ['light', 'dark', 'hc-light', 'hc-dark']\n"
        "print(css()[:40])        # every theme, as text\n"
        "print(css('dark')[:40])  # one theme\n"
        "print(css_path())        # a pathlib.Path, for copying\n"
    ),
    "tokens": (
        f"from {PY_MODULE} import TOKENS, THEME_TOKENS\n"
        "\n"
        "ink = THEME_TOKENS['dark']['color']['ink']['default']\n"
        "print(ink['$value'])                       # an alias into the ramps\n"
        "print(TOKENS['color']['ramp']['ground']['950']['$value']['hex'])\n"
    ),
}


PUBLICATION_FILE = HERE / "PUBLICATION.json"


def publication() -> dict:
    """The registry record. Hand-maintained, dated, and read by four generators."""
    return json.loads(PUBLICATION_FILE.read_text())


def _registries(entries: list[dict]) -> str:
    return " and ".join(r["registry"] for r in entries)


def publication_note(pub: dict | None = None) -> str:
    """The registry record, as one paragraph, from the record all four artefacts read.

    THREE STATES, THREE BRANCHES, AND WHY THAT MATTERS.

    The published branch used to read `' and '.join(... for r in missing)`, and
    `missing` is empty in that branch by construction. PUBLICATION.json's own
    `when_you_publish` instruction says to flip `published` to true and re-run this
    script; doing exactly that wrote

        Published on , checked 2026-08-18.

    onto the front page of both packages, and nothing reported it. `--check`
    compares the generated README against this generator, so a sentence the
    generator gets wrong is a sentence `--check` agrees with. scripts/readme.py
    fails closed on the same flip, which would stop CI — after its own prose was
    rewritten, at which point `--check` would go green over this broken text. The
    guard that fires masked the one that should have.

    The half-published state had no branch at all and fell through to the
    unpublished one, whose wording is "neither holds this package".

    check_publication_note() below renders all three states on every build, so
    none of them can go untested again.
    """
    pub = pub if pub is not None else publication()
    published = [r for r in pub["registries"] if r["published"]]
    missing = [r for r in pub["registries"] if not r["published"]]
    if not missing:
        return (f"Published on {_registries(published)}, checked "
                f"{pub['checked']}.")
    if published:
        return (f"**On {_registries(published)} but not yet on "
                f"{_registries(missing)}.** Checked {pub['checked']}. The package "
                f"is built either way and works from a checkout of {REPO}; the "
                f"command above works on the registry that holds it. I would "
                f"rather tell you that here than let you find out at the terminal.")
    return (f"**Not published yet.** On {pub['checked']} I checked "
            f"{_registries(missing)}, and neither holds this package. It is built "
            f"and it works from a checkout of {REPO}; the command above will work "
            f"once it is published. I would rather tell you that here than let you "
            f"find out at the terminal.")


def guard_exports_reach_dist(files: dict, npm: Path, pkg: dict) -> None:
    """Every data file shipped in dist/ must be an export target.

    WHY THIS WALKS THE FILES AND NOT THE EXPORTS. CI's npm step iterates
    `Object.entries(p.exports)` and checks each target exists, so it can only see
    exports that were declared — an omitted one is invisible to it, and it passed
    while `tokens/forced-colors.map.json` shipped with no route to it at all.
    Declaring "exports" turns on Node's subpath encapsulation, so a path that is
    not listed is not merely undocumented, it is blocked.

    This walks the other way: from what is about to be written into dist/ to the
    exports map. A new token document therefore cannot ship unreachable.
    """
    targets = set()
    for value in pkg["exports"].values():
        if isinstance(value, str):
            targets.add(value)
        else:
            targets.update(value.values())
    unreachable = []
    for path in sorted(files):
        try:
            rel = path.relative_to(npm)
        except ValueError:
            continue
        if rel.parts[0] != "dist" or rel.suffix not in (".json", ".css"):
            continue
        if f"./{rel.as_posix()}" not in targets:
            unreachable.append(rel.as_posix())
    if unreachable:
        raise SystemExit(
            "FAILED — nothing written. These files ship in the npm package but no "
            'export subpath reaches them, so Node answers '
            "ERR_PACKAGE_PATH_NOT_EXPORTED:\n  " + "\n  ".join(unreachable) +
            '\nAdd a subpath for each under "exports" in this script.'
        )


def check_publication_note() -> None:
    """Render the note for all three publication states and refuse an empty one.

    A branch nobody renders is a branch nobody has read. Each state must name
    every registry it talks about, so `Published on , checked …` cannot ship
    again — the failure is an empty enumeration, and that is what this looks for.
    """
    real = publication()
    names = [r["registry"] for r in real["registries"]]
    states = {
        "none published": [False] * len(names),
        "all published": [True] * len(names),
        "half published": [i == 0 for i in range(len(names))],
    }
    problems = []
    for label, flags in states.items():
        probe = json.loads(json.dumps(real))
        for entry, flag in zip(probe["registries"], flags):
            entry["published"] = flag
        note = publication_note(probe)
        expected = [n for n, f in zip(names, flags) if f] or names
        for name in expected:
            if name not in note:
                problems.append(f"{label}: the note never names {name!r} — {note!r}")
        for bad in (" on ,", " on .", "on  ", " and ,", "**On  "):
            if bad in note:
                problems.append(f"{label}: empty enumeration {bad!r} — {note!r}")
    if problems:
        raise SystemExit("FAILED — nothing written. publication_note() is broken:\n  "
                         + "\n  ".join(problems))


def py_file_table(files: dict[Path, str], py_root: Path) -> str:
    """The wheel's own file list, read out of what is about to be written.

    The old README described the npm tree: it promised `typography.css` and
    `layout.css`, which are only ever written into the npm package, and named the
    token documents by their npm subpath rather than their filename. Reading the
    table out of `files` means it cannot describe a file the wheel does not carry.
    """
    data = py_root / "src" / PY_MODULE / "data"
    rows = ["| File | What it is |", "|---|---|"]
    described = {
        "tokens.css": "Every theme in one stylesheet",
        "index.tokens.json": "An index of the token documents. **Not** a token document",
    }
    for path in sorted(p for p in files if data in p.parents or p.parent == data):
        rel = path.relative_to(data).as_posix()
        if rel in described:
            what = described[rel]
        elif rel.startswith("tokens.") and rel.endswith(".css"):
            what = f"The {rel[len('tokens.'):-len('.css')]} theme alone"
        elif rel == "tokens/primitive.tokens.json":
            what = "The ramps, scales, families and durations. DTCG"
        elif rel.startswith("tokens/semantic."):
            theme = rel[len("tokens/semantic."):-len(".tokens.json")]
            what = f"The {theme} theme's roles. DTCG, aliases into the primitives"
        elif rel == "tokens/forced-colors.map.json":
            what = "The forced-colours map. Deliberately **not** DTCG"
        else:
            raise SystemExit(
                f"12_packages/build.py: the wheel now carries {rel}, and the Python "
                "README has no description for it. Add one rather than shipping a "
                "file table that does not match the package."
            )
        rows.append(f"| `{rel}` | {what} |")
    rows.append(f"| `__init__.py`, `py.typed` | The module itself, typed |")
    return "\n".join(rows)


def check_python_examples(files: dict[Path, str], py_root: Path) -> list[str]:
    """Run every Python example in the README against the package being built."""
    import subprocess

    source = py_root / "src"
    written = {p: c for p, c in files.items() if source in p.parents}
    problems = []
    with __import__("tempfile").TemporaryDirectory() as tmp:
        stage = Path(tmp)
        for path, content in written.items():
            target = stage / path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        for name, code in PY_EXAMPLES.items():
            proc = subprocess.run([sys.executable, "-c", code],
                                  capture_output=True, text=True, cwd=stage)
            if proc.returncode != 0:
                problems.append(
                    f"the README's '{name}' example does not run against the package "
                    f"being built (exit {proc.returncode}): "
                    + (proc.stderr.strip() or proc.stdout.strip()).splitlines()[-1]
                )
    return problems


def read_version() -> str:
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    VERSION_FILE.write_text("1.0.0\n")
    return "1.0.0"


def split_css(css: str) -> dict[str, str]:
    """Cut the one stylesheet into per-theme files for consumers who want only one.

    The whole file remains the primary artefact; these are a convenience, and each
    carries a header saying so, because a consumer who imports only `dark` and
    wonders why the light theme is missing should not have to guess.
    """
    out: dict[str, str] = {}
    for theme in THEMES:
        marker = f'[data-theme="{theme}"] {{'
        i = css.find(marker)
        if i < 0:
            raise SystemExit(f"tokens.css has no explicit block for '{theme}'")
        j = css.find("}", i)
        block = css[i:j + 1]
        out[theme] = (
            f"/* Aninda Studio — the {theme} theme alone.\n"
            f" * A convenience view. The complete stylesheet is tokens.css, and the\n"
            f" * authoritative source is the DTCG documents under tokens/.\n"
            f" * GENERATED — do not hand-edit.\n"
            f" */\n{block}\n"
        )
    return out


def build() -> tuple[dict[Path, str], list[str]]:
    version = read_version()
    if not TOKENS.exists() or not CSS.exists():
        raise SystemExit("Missing tokens. Run 07_tokens/build.py and emit_css.py first.")
    check_publication_note()

    css = CSS.read_text()
    per_theme = split_css(css)
    docs = {p.name: json.loads(p.read_text()) for p in sorted(TOKENS.glob("*.json"))}

    files: dict[Path, str] = {}
    notes: list[str] = []

    # ---- shared documentation -------------------------------------------
    readme = f"""# {NPM_NAME}

{BLURB}

## Install

```
npm install {NPM_NAME}
```

{publication_note()}

## Use the stylesheet

```js
import '{NPM_NAME}/css';
```

That gives you every theme. The light values apply by default, the reader's system
setting is followed when nobody has chosen, and an explicit choice anywhere in the
tree wins:

```html
<html>                          <!-- follows the system -->
<div data-theme="dark">         <!-- an island, anywhere in the page -->
<div data-theme="hc-light">     <!-- high contrast -->
```

`[data-theme]` is scoped to the attribute and never to `:root`, so a dark panel can
sit inside a light page.

## Use the tokens directly

```js
import primitive from '{NPM_NAME}/tokens/primitive';
import light     from '{NPM_NAME}/tokens/light';
import hcDark    from '{NPM_NAME}/tokens/hc-dark';
```

Each of those is [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/),
a Final Community Group Report of the W3C Design Tokens Community Group. It is a
Community Group specification and **not** a W3C Standard.

**There is no single combined token document, and that is deliberate.** DTCG has no
theming concept, so each theme is its own file with identical token paths. An
earlier version of this package shipped all six wrapped in one object and called
that DTCG; it was not, and no tool could read it. `tokens/index` lists the files
and says plainly that it is an index rather than a token document.

Each colour carries its proof under `$extensions["studio.aninda"].proof` — the
ratio required, the ratio measured, the worst case under a one-bit perturbation of
both colours, which surface it was hardest against, and the WCAG criterion it
meets. You can check the claim rather than trust it.

## What is in here

| Path | What it is |
|---|---|
| `tokens/primitive` | The ramps, scales, families and durations. DTCG |
| `tokens/light`, `tokens/dark`, `tokens/hc-light`, `tokens/hc-dark` | One theme each. DTCG, identical token paths |
| `tokens/index` | An index of the above. **Not** a token document |
| `css` | Every theme in one stylesheet |
| `css/light`, `css/dark`, `css/hc-light`, `css/hc-dark` | One theme each |
| `typography.css`, `layout.css` | Type and layout properties |

## Fonts are not included

The system uses Literata, Noto Serif Bengali and IBM Plex Mono, all under the SIL
Open Font Licence 1.1. They are not bundled: it would triple the size of this
package, and an OFL font inside an Apache-2.0 package muddies the licence
declaration. `typography.css` declares the families and leaves the loading to you.

One thing to know if you subset IBM Plex Mono yourself: it carries the Reserved
Font Name **"Plex"** — that is the exact string, from the first line of its own
licence file — and subsetting counts as modifying it under OFL 1.1 clause 3, so a
subset may not use that name. The design system's own subset is called
"Aninda Mono" for exactly that reason.

## Licence

Apache-2.0. The name, the mark and the wordmark are **not** licensed — use the
system, put your own identity on it.

Questions: {EMAIL}
"""

    notice = f"""Aninda Studio design tokens
Copyright 2026 {AUTHOR}

This package is licensed under the Apache License, Version 2.0.
You may obtain a copy at http://www.apache.org/licenses/LICENSE-2.0

WHAT IS AND IS NOT COVERED

  Covered by Apache-2.0
    The token files, the stylesheets, and the code in this package.

  NOT licensed at all
    The name "Aninda Studio", the mark, the wordmark, the tile, and any lockup of
    them. They are not included in this package, and no licence to them is granted
    by it. Fork the system and put your own identity on it.

  Typefaces
    Not included here. Literata, Noto Serif Bengali and IBM Plex Mono are each
    under the SIL Open Font Licence 1.1 and keep their own terms.

Contact: {EMAIL}
Source:  {REPO}
"""

    # ---- npm --------------------------------------------------------------
    npm = HERE / "npm"
    pkg = {
        "name": NPM_NAME,
        "version": version,
        "description": BLURB,
        "type": "module",
        "license": "Apache-2.0",
        "author": {"name": AUTHOR, "email": EMAIL, "url": HOME},
        "homepage": HOME,
        "repository": {"type": "git", "url": f"git+{REPO}.git"},
        "bugs": {"url": f"{REPO}/issues"},
        "keywords": ["design-tokens", "dtcg", "design-system", "accessibility",
                     "wcag", "high-contrast", "css-variables", "bangla", "bilingual"],
        "sideEffects": ["*.css"],
        "files": ["dist", "README.md", "LICENSE", "NOTICE"],
        "exports": {
            ".": {"types": "./dist/index.d.ts", "import": "./dist/index.mjs",
                  "require": "./dist/index.cjs"},
            "./tokens.json": "./dist/tokens/primitive.tokens.json",
            "./tokens/index": "./dist/index.tokens.json",
            "./tokens/primitive": "./dist/tokens/primitive.tokens.json",
            **{f"./tokens/{t}": f"./dist/tokens/semantic.{t}.tokens.json" for t in THEMES},
            # The forced-colors map. It was shipped in dist/ and named by
            # dist/index.tokens.json, and had no subpath here — so because
            # "exports" is declared at all, Node's subpath encapsulation blocked
            # every route to it and a consumer following the package's own index
            # got ERR_PACKAGE_PATH_NOT_EXPORTED with no way in. The Python package
            # has always shipped the same file reachable, so the two packages
            # disagreed about what they contain. guard_exports_reach_dist() below
            # now walks the shipped files rather than the declared exports, which
            # is what CI's export check cannot do.
            "./tokens/forced-colors": "./dist/tokens/forced-colors.map.json",
            "./css": "./dist/tokens.css",
            **{f"./css/{t}": f"./dist/tokens.{t}.css" for t in THEMES},
            "./typography.css": "./dist/typography.css",
            "./layout.css": "./dist/layout.css",
            "./package.json": "./package.json",
        },
    }
    files[npm / "package.json"] = json.dumps(pkg, indent=2) + "\n"
    files[npm / "README.md"] = readme
    files[npm / "NOTICE"] = notice

    # Ship each DTCG document VERBATIM, under its own name. The first version
    # wrapped all six inside {"$description", "version", "files": {filename: doc}}
    # and the README then told consumers that wrapper WAS
    # "Design Tokens Format Module 2025.10". It was not, and it could not be:
    #   · six group names ended in ".json", and DTCG forbids "." in a name outright
    #   · every one of the 40 aliases dangled, because nesting moved their targets
    #   · the top-level "version" was a bare string where a token or group belongs
    # An independent validator found 84 errors in it while the four source files
    # under 07_tokens/build/ passed clean. The defect was entirely in this step.
    #
    # There is no combined token document any more, because DTCG has no way to
    # express one — it has no theming concept, which is why the source is four
    # files with identical token paths in the first place. An index is shipped
    # alongside them, and it says plainly that it is an index.
    for name, doc in docs.items():
        files[npm / "dist" / "tokens" / name] = json.dumps(doc, indent=2,
                                                          ensure_ascii=False) + "\n"
    index = {
        "$comment": (
            "THIS FILE IS AN INDEX, NOT A TOKEN DOCUMENT. Do not hand it to a DTCG "
            "tool — it would fail validation, because it is not trying to be DTCG. "
            "The conformant documents are the files it lists, under tokens/. "
            "DTCG 2025.10 has no theming concept, so there is deliberately no "
            "single combined document: each theme is its own file with identical "
            "token paths."
        ),
        "version": version,
        "spec": "Design Tokens Format Module 2025.10 (W3C Community Group report, "
                "not a W3C Standard)",
        "primitive": "tokens/primitive.tokens.json",
        "themes": {t: f"tokens/semantic.{t}.tokens.json" for t in THEMES},
        "notDtcg": {
            "tokens/forced-colors.map.json": (
                "Deliberately not DTCG. Its values are CSS system colour keywords "
                "supplied by the operating system, which have no colour space, no "
                "components and no hex, and DTCG's thirteen types include nothing "
                f"that fits. Import it as '{NPM_NAME}/tokens/forced-colors'; the "
                "paths in this index are files inside the package, and the import "
                "subpath for each is in package.json under \"exports\"."
            )
        },
    }
    files[npm / "dist" / "index.tokens.json"] = json.dumps(index, indent=2,
                                                           ensure_ascii=False) + "\n"
    files[npm / "dist" / "tokens.css"] = css
    for t, block in per_theme.items():
        files[npm / "dist" / f"tokens.{t}.css"] = block

    # Two small files rather than one, because a `typography.css` that does not
    # exist is a broken export map, and an export map is checked by tooling.
    files[npm / "dist" / "typography.css"] = (
        "/* Aninda Studio — typography. GENERATED, do not hand-edit.\n"
        " * Fonts are NOT bundled; declare your own @font-face or load them from a\n"
        " * host you control. Family names below match the design system's own.\n */\n"
        ":root{font-family:var(--as-font-latin);}\n"
        ':lang(bn),[lang="bn"]{font-family:var(--as-font-bangla);'
        "line-height:var(--as-bangla-line-height);}\n"
        "code,kbd,samp,pre{font-family:var(--as-font-mono);}\n"
    )
    files[npm / "dist" / "layout.css"] = (
        "/* Aninda Studio — layout. GENERATED, do not hand-edit. */\n"
        ":root{--as-container:76rem;--as-container-prose:46rem;--as-gutter:"
        "var(--as-space-4);}\n"
    )

    # `export { primitive as tokens }`, not `export { tokens }`. `tokens` was
    # never declared in this module, so the ESM entry point threw
    # "SyntaxError: Export 'tokens' is not defined in module" — and it threw at
    # LINK time, not at run time, so no bundler and no Node version rescued it.
    # index.d.ts told TypeScript users the import worked. The CI step named "The
    # npm package must actually resolve" stat-ed this file and then imported the
    # CommonJS twin instead, so it passed. That step now imports this file.
    index_body = (
        "// Aninda Studio design tokens. GENERATED — do not hand-edit.\n"
        "import primitive from './tokens/primitive.tokens.json' with { type: 'json' };\n"
        "export const themes = %s;\n"
        "export { primitive as tokens };\n"
        "export default primitive;\n" % json.dumps(list(THEMES))
    )
    files[npm / "dist" / "index.mjs"] = index_body
    files[npm / "dist" / "index.cjs"] = (
        "// Aninda Studio design tokens. GENERATED — do not hand-edit.\n"
        "const tokens = require('./tokens/primitive.tokens.json');\n"
        "module.exports = tokens;\n"
        "module.exports.tokens = tokens;\n"
        "module.exports.themes = %s;\n" % json.dumps(list(THEMES))
    )
    files[npm / "dist" / "index.d.ts"] = (
        "// Aninda Studio design tokens. GENERATED — do not hand-edit.\n"
        "export type Theme = %s;\n"
        "export declare const themes: readonly Theme[];\n"
        "export declare const tokens: Record<string, unknown>;\n"
        "export default tokens;\n" % " | ".join(f'"{t}"' for t in THEMES)
    )

    # ---- PyPI -------------------------------------------------------------
    py = HERE / "python"
    mod = py / "src" / PY_MODULE
    files[py / "pyproject.toml"] = f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{PY_NAME}"
version = "{version}"
description = "{BLURB.splitlines()[0]}"
readme = "README.md"
requires-python = ">=3.9"
license = "Apache-2.0"
license-files = ["LICENSE", "NOTICE"]
authors = [{{ name = "{AUTHOR}", email = "{EMAIL}" }}]
keywords = ["design-tokens", "dtcg", "design-system", "accessibility", "wcag"]
classifiers = [
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "Programming Language :: Python :: 3",
  "Topic :: Software Development :: User Interfaces",
]
dependencies = []

[project.urls]
Homepage = "{HOME}"
Source = "{REPO}"

[tool.hatch.build.targets.wheel]
packages = ["src/{PY_MODULE}"]
'''
    files[py / "NOTICE"] = notice
    files[mod / "py.typed"] = ""
    files[mod / "__init__.py"] = f'''"""Aninda Studio design tokens.

GENERATED — do not hand-edit. Regenerate with 12_packages/build.py.

    from {PY_MODULE} import TOKENS, css, css_path, THEMES

    css("hc-dark")        # the stylesheet text for one theme
    css_path("dark")      # a pathlib.Path, for copying into a build
    TOKENS                # the primitive DTCG document
    THEME_TOKENS["dark"]  # one DTCG document per theme
"""

from __future__ import annotations

import json
from pathlib import Path

__version__ = "{version}"
THEMES = {list(THEMES)!r}

_DATA = Path(__file__).parent / "data"

def _load(name: str) -> dict:
    with (_DATA / "tokens" / name).open(encoding="utf-8") as f:
        return json.load(f)


#: The primitive DTCG document — ramps, scales, families, durations.
TOKENS = _load("primitive.tokens.json")

#: One DTCG document per theme, with identical token paths in each. There is no
#: combined document because DTCG has no theming concept.
THEME_TOKENS = {{t: _load(f"semantic.{{t}}.tokens.json") for t in THEMES}}


def css_path(theme: str | None = None) -> Path:
    """Path to the stylesheet. With no theme, the complete one."""
    if theme is None:
        return _DATA / "tokens.css"
    if theme not in THEMES:
        raise ValueError(f"unknown theme {{theme!r}} — expected one of {{THEMES}}")
    return _DATA / f"tokens.{{theme}}.css"


def css(theme: str | None = None) -> str:
    """The stylesheet text. With no theme, every theme."""
    return css_path(theme).read_text(encoding="utf-8")


__all__ = ["TOKENS", "THEME_TOKENS", "THEMES", "css", "css_path", "__version__"]
'''
    for _n in docs:
        files[mod / "data" / "tokens" / _n] = files[npm / "dist" / "tokens" / _n]
    files[mod / "data" / "index.tokens.json"] = files[npm / "dist" / "index.tokens.json"]
    files[mod / "data" / "tokens.css"] = css
    for t, block in per_theme.items():
        files[mod / "data" / f"tokens.{t}.css"] = block

    # The PyPI README is WRITTEN, not derived. It used to be the npm README with
    # `npm install` swapped for `pip install` and every ```js fence relabelled
    # ```python, which left two JavaScript ES module imports presented as Python —
    # both syntax errors — and a file table listing npm subpath exports
    # (`tokens/primitive`, `css/dark`, `typography.css`, `layout.css`) that have no
    # Python equivalent at all. pyproject.toml sets readme = "README.md", so that
    # file is the PyPI project page: every usage example on it failed. The four
    # names that do work — TOKENS, THEME_TOKENS, css() and css_path() — were never
    # mentioned. PY_EXAMPLES below is executed against the built package before
    # anything is written.
    files[py / "README.md"] = f"""# {PY_NAME}

{BLURB}

## Install

```
pip install {PY_NAME}
```

{publication_note()}

## Use it

```python
{PY_EXAMPLES["basic"]}```

`css()` returns the stylesheet text; `css_path()` returns a `pathlib.Path`, which is
what you want when copying the file into a build rather than reading it.

```python
{PY_EXAMPLES["tokens"]}```

`TOKENS` is the primitive document — the ramps, scales, families and durations.
`THEME_TOKENS` holds one document per theme, with identical token paths in each.

Each is [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/),
a Final Community Group Report of the W3C Design Tokens Community Group. It is a
Community Group specification and **not** a W3C Standard.

**There is no single combined token document, and that is deliberate.** DTCG has no
theming concept, so each theme is its own file with identical token paths. One
consequence worth knowing: a semantic theme document resolves only when it is merged
with the primitive one, because its role colours are aliases into the ramps.

Each colour carries its proof under `$extensions["studio.aninda"].proof` — the
ratio required, the ratio measured, the worst case under a one-bit perturbation of
both colours, which surface it was hardest against, and the WCAG criterion it
meets. You can check the claim rather than trust it.

## Applying a theme

The stylesheet defines light values on `:root`, follows the reader's system setting
where nobody has chosen, and lets an explicit choice anywhere in the tree win:

```html
<html>                          <!-- follows the system -->
<div data-theme="dark">         <!-- an island, anywhere in the page -->
<div data-theme="hc-light">     <!-- high contrast -->
```

`[data-theme]` is scoped to the attribute and never to `:root`, so a dark panel can
sit inside a light page.

## What the wheel contains

{py_file_table(files, py)}

There are no `typography.css` or `layout.css` files here. Those two are npm subpath
exports and there is no Python equivalent of a subpath export; the families and the
container widths they set are in the token documents, under `fontFamily` and
`dimension`.

## Fonts are not included

The system uses Literata, Noto Serif Bengali and IBM Plex Mono, all under the SIL
Open Font Licence 1.1. They are not bundled: it would triple the size of this
package, and an OFL font inside an Apache-2.0 package muddies the licence
declaration. The families are named in the token documents; loading them is yours.

One thing to know if you subset IBM Plex Mono yourself: it carries the Reserved
Font Name **"Plex"** — that is the exact string, from the first line of its own
licence file — and subsetting counts as modifying it under OFL 1.1 clause 3, so a
subset may not use that name. The design system's own subset is called
"Aninda Mono" for exactly that reason.

## Licence

Apache-2.0. The name, the mark and the wordmark are **not** licensed — use the
system, put your own identity on it.

Questions: {EMAIL}
"""

    notes.append(f"version {version}")
    notes.append(f"npm '{NPM_NAME}' — {sum(1 for p in files if 'npm' in p.parts)} files")
    notes.append(f"PyPI '{PY_NAME}' — {sum(1 for p in files if 'python' in p.parts)} files")
    notes.append(f"{len(docs)} DTCG documents shipped verbatim")
    guard_exports_reach_dist(files, npm, pkg)
    notes.append(f"{len(pkg['exports'])} npm subpaths reach every shipped "
                 f"stylesheet and token document")
    return files, notes


def verify(files: dict[Path, str]) -> list[str]:
    """Prove the CSS and the DTCG source still agree, rather than assuming."""
    problems = []
    # Prove every shipped DTCG document is byte-identical to its source. The
    # previous version verified a wrapper it had built itself, which is why it
    # reported "6 DTCG documents shipped verbatim" about a file that failed
    # DTCG validation with 84 errors. A check that only inspects its own output
    # cannot catch a packaging bug.
    for src in sorted(TOKENS.glob("*.json")):
        shipped = files.get(HERE / "npm" / "dist" / "tokens" / src.name)
        if shipped is None:
            problems.append(f"{src.name} is in the source but was not packaged")
            continue
        if json.loads(shipped) != json.loads(src.read_text()):
            problems.append(f"{src.name} was altered on the way into the package")
    css_blob = next(v for k, v in files.items() if k.name == "tokens.css")

    def shipped_doc(name: str) -> dict:
        blob = files.get(HERE / "npm" / "dist" / "tokens" / name)
        return json.loads(blob) if blob else {}

    for name in ("primitive.tokens.json", *[f"semantic.{t}.tokens.json" for t in THEMES],
                 "forced-colors.map.json"):
        if not shipped_doc(name):
            problems.append(f"{name} was not packaged")

    # Every colour in every semantic theme file must appear in the stylesheet —
    # AFTER its alias is resolved.
    #
    # The earlier form of this walk only looked at a $value that was a dict
    # carrying "hex". Every role colour in a semantic theme file is an alias
    # STRING, `"{color.ramp.ground.950}"`, so it was skipped: the check covered
    # the seven swept surfaces per theme and none of the ten roles. Round 1 of the
    # convergence review changed --as-ink in the stylesheet from #0D1A17 to
    # #ABCDEF, rebuilt, and got four green ok lines with the wrong colour in both
    # packages. Text, line, accent, focus and every status colour — the ones
    # carrying the contrast proofs — were the ten it could not see.
    primitive = shipped_doc("primitive.tokens.json")

    def resolve(value):
        """A hex, whether the token holds one or points at one."""
        if isinstance(value, dict) and "hex" in value:
            return value["hex"], None
        if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            node = primitive
            for part in value[1:-1].split("."):
                node = node.get(part) if isinstance(node, dict) else None
                if node is None:
                    return None, f"alias {value} does not resolve in primitive.tokens.json"
            inner = node.get("$value") if isinstance(node, dict) else None
            if isinstance(inner, dict) and "hex" in inner:
                return inner["hex"], None
            return None, f"alias {value} resolves to something with no hex"
        return None, None

    for t in THEMES:
        doc = shipped_doc(f"semantic.{t}.tokens.json")
        missing: list[str] = []
        counted = 0

        def walk(node, path=""):
            nonlocal counted
            if not isinstance(node, dict):
                return
            if "$value" in node:
                hexv, why = resolve(node["$value"])
                if why:
                    problems.append(f"{t}:{path}: {why}")
                elif hexv is not None:
                    counted += 1
                    if hexv not in css_blob:
                        missing.append(f"{path} = {hexv}")
            for k, child in node.items():
                if not k.startswith("$"):
                    walk(child, f"{path}.{k}" if path else k)

        walk(doc.get("color", {}), "color")
        if missing:
            problems.append(f"{t}: {len(missing)} of {counted} colours in the tokens "
                            f"never appear in the CSS: {sorted(missing)[:3]}")
        elif counted < 17:
            # 17 roles per theme. A walk that silently resolved fewer than that is
            # the failure this whole block exists to prevent, so it is stated as a
            # number rather than left to inspection.
            problems.append(f"{t}: only {counted} colours were resolved and compared, "
                            f"and there are 17 roles per theme. The walk is missing some.")

    for t in THEMES:
        blob = next((v for k, v in files.items() if k.name == f"tokens.{t}.css"), None)
        if blob is None or f'[data-theme="{t}"]' not in blob:
            problems.append(f"the per-theme file for '{t}' has no matching block")

    # Both README code samples must actually run. The PyPI README used to carry
    # JavaScript relabelled as Python, and --check passed because it compared the
    # generated file against the generator rather than against the package it
    # describes. This runs them against a staged copy of the wheel's own source.
    problems += check_python_examples(files, HERE / "python")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    files, notes = build()
    problems = verify(files)
    if problems:
        print("FAILED — nothing written:\n", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    for n in notes:
        print(f"  ok    {n}")

    if args.check:
        for path, content in files.items():
            if not path.exists() or path.read_text() != content:
                print(f"\n--check: {path.relative_to(ROOT)} differs from the build",
                      file=sys.stderr)
                return 1
        print("\n--check: both packages match the source. Nothing written.")
        return 0

    for sub in ("npm", "python"):
        if (HERE / sub).exists():
            shutil.rmtree(HERE / sub)
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    for sub, lic in (("npm", HERE / "npm" / "LICENSE"),
                     ("python", HERE / "python" / "LICENSE")):
        lic.write_text(
            "                                 Apache License\n"
            "                           Version 2.0, January 2004\n"
            "                        http://www.apache.org/licenses/\n\n"
            "   Copyright 2026 Aninda Sundar Howlader\n\n"
            "   Licensed under the Apache License, Version 2.0 (the \"License\");\n"
            "   you may not use this file except in compliance with the License.\n"
            "   You may obtain a copy of the License at\n\n"
            "       http://www.apache.org/licenses/LICENSE-2.0\n\n"
            "   Unless required by applicable law or agreed to in writing, software\n"
            "   distributed under the License is distributed on an \"AS IS\" BASIS,\n"
            "   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or\n"
            "   implied. See the License for the specific language governing\n"
            "   permissions and limitations under the License.\n"
        )

    print(f"\nWrote {len(files) + 2} files to {HERE.relative_to(ROOT)}/")
    print("\nTo publish — these are for a person to run, not this script.")
    print("  npm:   cd 12_packages/npm    && npm publish --dry-run   # read the file list")
    print("         then                     npm publish --access public")
    print("  PyPI:  set up Trusted Publishing on pypi.org against the repo and let")
    print("         the release workflow publish, so no token is ever stored anywhere.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
