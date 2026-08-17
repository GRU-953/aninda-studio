#!/usr/bin/env python3
"""Aninda Studio — print the guidebook to A4 PDF, and verify what came out.

    export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
    ./.venv/bin/python 09_guidebook/scripts/pdf.py [--probe-interactive]

Playwright only. No ghostscript, no qpdf, no post-processing tool of any kind:
this repository installs nothing system-wide, and a pipeline that depends on a
binary the reader does not have is a pipeline that only works here.

WHAT THIS SCRIPT INSISTS ON, AND WHY

  * `await document.fonts.ready` before printing. Without it the Bangla prints in
    a fallback face. The fonts are embedded as base64 in the document, and
    Chromium will happily lay out and print a page before it has finished
    decoding them.
  * Every <details> forced open. A closed <details> prints as its summary line
    and the contents are simply absent from the paper. On screen that is a
    disclosure control; on paper it is data loss.
  * Layout settled before the print call — fonts ready, two animation frames,
    then a short settle wait.
  * `page.pdf(format="A4", print_background=True)`. Without the background flag
    every swatch, every note panel and every table rule prints white.

  * It prints the PRINT build, not the interactive one. See build.py for why the
    two exist.

A STATED LIMIT, NOT A DEFECT TO BE FIXED LATER

  **The PDF has no bookmark tree.** Chromium's PDF output carries no outline, and
  adding one afterwards needs a PDF tool — qpdf or similar — which this pipeline
  deliberately does not have. The generated table of contents on page 2, whose
  entries are internal anchor links that Chromium does convert into working PDF
  links, is what stands in for it. That is the whole of the mitigation and it is
  not equivalent: a reader cannot open a sidebar and jump.

VERIFICATION

  Nothing is claimed that is not measured:
    1. no network request of any kind was made while rendering;
    2. all three fonts report as loaded;
    3. the PDF has more than one page;
    4. no page is blank — every page is rendered with pypdfium2 and its pixels
       sampled, and a page whose pixels are all one value fails.

  `--probe-interactive` additionally prints the interactive build and reports what
  happens, so the reason for the two-file split stays a measurement rather than a
  memory. As at 15 August 2026, at 13.6 MB, it printed: 55 pages, none blank, a
  14.2 MB PDF against the print build's 1.4 MB, with the page breaks in the wrong
  places. The blank-page failure that this split is usually justified by was NOT
  reproduced at this size. Re-run the probe after the kit grows.

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Aninda Sundar Howlader
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUIDEBOOK = HERE.parent
ROOT = GUIDEBOOK.parent

PRINT_HTML = GUIDEBOOK / "Aninda-Studio-Guidebook-print.html"
INTERACTIVE_HTML = GUIDEBOOK / "Aninda-Studio-Guidebook.html"
OUT_PDF = GUIDEBOOK / "Aninda-Studio-Guidebook.pdf"
PROBE_PDF = GUIDEBOOK / "_probe-interactive.pdf"

FONT_CHECKS = [
    '16px Literata',
    '16px "Noto Serif Bengali"',
    '16px "Aninda Mono"',
]


class PrintError(Exception):
    pass


def fmt_bytes(n: int) -> str:
    if n >= 1024 * 1024:
        return f"{n / (1024 * 1024):.1f} MB"
    if n >= 1024:
        return f"{n / 1024:.0f} kB"
    return f"{n} bytes"


def render_pdf(html_path: Path, pdf_path: Path, strict: bool) -> dict:
    """Open the document, settle it, print it. Returns what was observed."""
    from playwright.sync_api import sync_playwright

    observed = {"requests": [], "fonts": {}, "details_opened": 0}

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1100, "height": 1400})

        doc_url = html_path.as_uri()

        def on_request(request):
            if request.url != doc_url:
                observed["requests"].append(request.url)

        page.on("request", on_request)
        page.goto(doc_url, wait_until="load")

        # 1. Fonts. Without this the Bangla prints in a fallback face.
        page.evaluate("() => document.fonts.ready")
        for spec in FONT_CHECKS:
            observed["fonts"][spec] = page.evaluate(
                "spec => document.fonts.check(spec)", spec)

        # 2. Every disclosure forced open. On paper a closed one is data loss.
        observed["details_opened"] = page.evaluate(
            """() => {
                const all = document.querySelectorAll('details');
                all.forEach(d => d.open = true);
                return all.length;
            }"""
        )

        # 3. Let layout settle: two frames, then a short wait.
        page.evaluate(
            "() => new Promise(r => requestAnimationFrame("
            "() => requestAnimationFrame(r)))")
        page.wait_for_timeout(600)

        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            display_header_footer=False,
        )
        browser.close()

    if strict:
        if observed["requests"]:
            raise PrintError(
                "the document made network requests while rendering, so it is "
                "not self-contained: " + ", ".join(observed["requests"][:5]))
        missing = [k for k, v in observed["fonts"].items() if not v]
        if missing:
            raise PrintError(
                "these fonts did not report as loaded, so the print would fall "
                "back: " + ", ".join(missing))
    return observed


def inspect_pdf(pdf_path: Path) -> dict:
    """Page count, and a real pixel sample of every page."""
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf_path))
    pages = len(doc)
    blank = []
    inked: list[float] = []
    for index in range(pages):
        page = doc[index]
        bitmap = page.render(scale=0.45, draw_annots=False)
        data = bitmap.to_pil().convert("L").tobytes()
        distinct = len(set(data))
        dark = sum(1 for value in data if value < 200)
        inked.append(dark / max(1, len(data)))
        if distinct <= 1 or dark == 0:
            blank.append(index + 1)
    doc.close()
    thinnest = min(range(pages), key=lambda i: inked[i]) + 1 if pages else 0
    return {"pages": pages, "blank": blank,
            "min_ink": min(inked) if inked else 0.0,
            "thinnest_page": thinnest,
            "mean_ink": sum(inked) / len(inked) if inked else 0.0,
            "per_page": inked}


def probe_interactive() -> None:
    """Try to print the interactive build and report what happens. The two-file
    split rests on this, so it is measured rather than asserted."""
    size = INTERACTIVE_HTML.stat().st_size
    print(f"\n  probe: printing the interactive build "
          f"({fmt_bytes(size)}) — this is the file the split exists to avoid")
    try:
        render_pdf(INTERACTIVE_HTML, PROBE_PDF, strict=False)
    except Exception as exc:  # noqa: BLE001 - the outcome is the measurement
        print(f"  probe: Chromium failed outright — {type(exc).__name__}: {exc}")
        return
    try:
        result = inspect_pdf(PROBE_PDF)
    except Exception as exc:  # noqa: BLE001
        print(f"  probe: the PDF could not be read — {type(exc).__name__}: {exc}")
        return
    print(f"  probe: {result['pages']} pages, "
          f"{len(result['blank'])} of them blank, "
          f"mean ink {result['mean_ink']:.4f}, "
          f"file {fmt_bytes(PROBE_PDF.stat().st_size)}")
    if result["blank"]:
        print(f"  probe: blank pages at {result['blank'][:20]}")
    print("  probe: kept at 09_guidebook/_probe-interactive.pdf for inspection. "
          "It is not a deliverable.")


def main(argv: list[str]) -> int:
    if not PRINT_HTML.exists():
        print("The print build is not on disk. Run build.py first.",
              file=sys.stderr)
        return 2

    print(f"  source: {PRINT_HTML.name} ({fmt_bytes(PRINT_HTML.stat().st_size)})")
    try:
        observed = render_pdf(PRINT_HTML, OUT_PDF, strict=True)
    except PrintError as exc:
        print(f"PRINT FAILED\n  {exc}", file=sys.stderr)
        return 1

    print(f"  external requests while rendering: "
          f"{len(observed['requests'])} — none is the only acceptable number")
    for spec, ok in observed["fonts"].items():
        print(f"  font loaded: {spec} — {'yes' if ok else 'NO'}")
    print(f"  <details> forced open: {observed['details_opened']}")

    result = inspect_pdf(OUT_PDF)
    print(f"  wrote {OUT_PDF.name} — {fmt_bytes(OUT_PDF.stat().st_size)}, "
          f"{result['pages']} pages")
    print(f"  ink: mean {result['mean_ink']:.4f} of pixels dark, "
          f"thinnest is page {result['thinnest_page']} at {result['min_ink']:.4f}")

    failures = []
    if result["pages"] <= 1:
        failures.append(f"only {result['pages']} page")
    if result["blank"]:
        failures.append(f"blank pages at {result['blank']}")
    if failures:
        print("PRINT FAILED\n  " + "\n  ".join(failures), file=sys.stderr)
        return 1

    print("  stated limit: the PDF has no bookmark tree. Chromium emits no "
          "outline and this pipeline has no PDF tool to add one. The generated "
          "table of contents with internal links is the whole mitigation.")
    print("PRINT PASSED")

    if "--probe-interactive" in argv:
        probe_interactive()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
