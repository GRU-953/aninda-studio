"""Aninda Studio design tokens.

GENERATED — do not hand-edit. Regenerate with 12_packages/build.py.

    from aninda_studio_tokens import TOKENS, css, css_path, THEMES

    css("hc-dark")        # the stylesheet text for one theme
    css_path("dark")      # a pathlib.Path, for copying into a build
    TOKENS                # the parsed DTCG document
"""

from __future__ import annotations

import json
from pathlib import Path

__version__ = "1.0.0"
THEMES = ['light', 'dark', 'hc-light', 'hc-dark']

_DATA = Path(__file__).parent / "data"

with (_DATA / "aninda.tokens.json").open(encoding="utf-8") as _f:
    TOKENS = json.load(_f)


def css_path(theme: str | None = None) -> Path:
    """Path to the stylesheet. With no theme, the complete one."""
    if theme is None:
        return _DATA / "tokens.css"
    if theme not in THEMES:
        raise ValueError(f"unknown theme {theme!r} — expected one of {THEMES}")
    return _DATA / f"tokens.{theme}.css"


def css(theme: str | None = None) -> str:
    """The stylesheet text. With no theme, every theme."""
    return css_path(theme).read_text(encoding="utf-8")


__all__ = ["TOKENS", "THEMES", "css", "css_path", "__version__"]
