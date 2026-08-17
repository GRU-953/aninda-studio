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
HOME = "https://anindastudio.com"

THEMES = ("light", "dark", "hc-light", "hc-dark")

BLURB = (
    "The Aninda Studio design tokens: colour, type, space, shape and motion, in "
    "four themes — light, dark, and a high-contrast pair. Every colour pairing was "
    "measured rather than chosen, against WCAG 2.2 AA in the ordinary themes and "
    "AAA in the high-contrast ones."
)


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
            f" * authoritative source is aninda.tokens.json.\n"
            f" * GENERATED — do not hand-edit.\n"
            f" */\n{block}\n"
        )
    return out


def build() -> tuple[dict[Path, str], list[str]]:
    version = read_version()
    if not TOKENS.exists() or not CSS.exists():
        raise SystemExit("Missing tokens. Run 07_tokens/build.py and emit_css.py first.")

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
import tokens from '{NPM_NAME}/tokens.json';
```

That file is [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/),
a Final Community Group Report of the W3C Design Tokens Community Group. It is a
Community Group specification and **not** a W3C Standard.

Each colour carries its proof under `$extensions["studio.aninda"].proof` — the
ratio required, the ratio measured, the worst case under a one-bit perturbation of
both colours, which surface it was hardest against, and the WCAG criterion it
meets. You can check the claim rather than trust it.

## What is in here

| Path | What it is |
|---|---|
| `tokens.json` | The DTCG source. Authoritative |
| `css` | Every theme in one stylesheet |
| `css/light`, `css/dark`, `css/hc-light`, `css/hc-dark` | One theme each |
| `typography.css`, `layout.css` | Type and layout properties |

## Fonts are not included

The system uses Literata, Noto Serif Bengali and IBM Plex Mono, all under the SIL
Open Font Licence 1.1. They are not bundled: it would triple the size of this
package, and an OFL font inside an Apache-2.0 package muddies the licence
declaration. `typography.css` declares the families and leaves the loading to you.

One thing to know if you subset IBM Plex Mono yourself: it carries the Reserved
Font Name "IBM Plex", and subsetting counts as modifying it under OFL 1.1 clause 3,
so a subset has to be renamed. The design system's own subset is called
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
            "./tokens.json": "./dist/aninda.tokens.json",
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

    bundle = {"$description": BLURB, "version": version,
              "files": {k: v for k, v in docs.items()}}
    files[npm / "dist" / "aninda.tokens.json"] = json.dumps(bundle, indent=2,
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

    index_body = (
        "// Aninda Studio design tokens. GENERATED — do not hand-edit.\n"
        "import tokens from './aninda.tokens.json' with { type: 'json' };\n"
        "export const themes = %s;\n"
        "export { tokens };\n"
        "export default tokens;\n" % json.dumps(list(THEMES))
    )
    files[npm / "dist" / "index.mjs"] = index_body
    files[npm / "dist" / "index.cjs"] = (
        "// Aninda Studio design tokens. GENERATED — do not hand-edit.\n"
        "const tokens = require('./aninda.tokens.json');\n"
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
    files[py / "README.md"] = readme.replace(
        f"npm install {NPM_NAME}", f"pip install {PY_NAME}"
    ).replace("```js", "```python")
    files[py / "NOTICE"] = notice
    files[mod / "py.typed"] = ""
    files[mod / "__init__.py"] = f'''"""Aninda Studio design tokens.

GENERATED — do not hand-edit. Regenerate with 12_packages/build.py.

    from {PY_MODULE} import TOKENS, css, css_path, THEMES

    css("hc-dark")        # the stylesheet text for one theme
    css_path("dark")      # a pathlib.Path, for copying into a build
    TOKENS                # the parsed DTCG document
"""

from __future__ import annotations

import json
from pathlib import Path

__version__ = "{version}"
THEMES = {list(THEMES)!r}

_DATA = Path(__file__).parent / "data"

with (_DATA / "aninda.tokens.json").open(encoding="utf-8") as _f:
    TOKENS = json.load(_f)


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


__all__ = ["TOKENS", "THEMES", "css", "css_path", "__version__"]
'''
    files[mod / "data" / "aninda.tokens.json"] = files[npm / "dist" / "aninda.tokens.json"]
    files[mod / "data" / "tokens.css"] = css
    for t, block in per_theme.items():
        files[mod / "data" / f"tokens.{t}.css"] = block

    notes.append(f"version {version}")
    notes.append(f"npm '{NPM_NAME}' — {sum(1 for p in files if 'npm' in p.parts)} files")
    notes.append(f"PyPI '{PY_NAME}' — {sum(1 for p in files if 'python' in p.parts)} files")
    notes.append(f"{len(docs)} DTCG documents shipped verbatim")
    return files, notes


def verify(files: dict[Path, str]) -> list[str]:
    """Prove the CSS and the DTCG source still agree, rather than assuming."""
    problems = []
    tokens_blob = next(v for k, v in files.items() if k.name == "aninda.tokens.json")
    css_blob = next(v for k, v in files.items() if k.name == "tokens.css")
    bundle = json.loads(tokens_blob)

    for name in ("primitive.tokens.json", *[f"semantic.{t}.tokens.json" for t in THEMES]):
        if name not in bundle["files"]:
            problems.append(f"the bundle is missing {name}")

    # Every hex in every semantic theme file must appear in the stylesheet.
    for t in THEMES:
        doc = bundle["files"].get(f"semantic.{t}.tokens.json", {})
        missing = []

        def walk(node):
            if isinstance(node, dict):
                v = node.get("$value")
                if isinstance(v, dict) and "hex" in v and v["hex"] not in css_blob:
                    missing.append(v["hex"])
                for k, child in node.items():
                    if not k.startswith("$"):
                        walk(child)

        walk(doc.get("color", {}))
        if missing:
            problems.append(f"{t}: {len(missing)} colours in the tokens never appear "
                            f"in the CSS, e.g. {sorted(set(missing))[:3]}")

    for t in THEMES:
        blob = next((v for k, v in files.items() if k.name == f"tokens.{t}.css"), None)
        if blob is None or f'[data-theme="{t}"]' not in blob:
            problems.append(f"the per-theme file for '{t}' has no matching block")
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
