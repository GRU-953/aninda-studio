#!/usr/bin/env python3
"""Aninda Studio — print the guidebook to A4 PDF, and verify what came out.

    export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
    ./.venv/bin/python 09_guidebook/scripts/pdf.py [--probe-interactive]

Playwright only. No ghostscript, no qpdf, no post-processing tool of any kind:
this repository installs nothing system-wide, and a pipeline that depends on a
binary the reader does not have is a pipeline that only works here.

WHAT THIS SCRIPT INSISTS ON, AND WHY

  * `await document.fonts.ready` before printing. Without it the type prints in
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

import html as html_mod
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUIDEBOOK = HERE.parent
ROOT = GUIDEBOOK.parent

PRINT_HTML = GUIDEBOOK / "Aninda-Studio-Guidebook-print.html"
INTERACTIVE_HTML = GUIDEBOOK / "Aninda-Studio-Guidebook.html"
OUT_PDF = GUIDEBOOK / "Aninda-Studio-Guidebook.pdf"
PROBE_PDF = GUIDEBOOK / "_probe-interactive.pdf"

# The faces the print build has to have loaded before it is allowed to print.
# "Noto Serif Bengali" was the third, and the reason it was checked at all is
# worth keeping: without `await document.fonts.ready` the Bangla printed in a
# fallback face, silently, in a PDF that looked finished. The same risk applies to
# these two.
FONT_CHECKS = [
    '16px Literata',
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

        # 1. Fonts. Without this the type prints in a fallback face.
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


def pdf_text(pdf_path: Path) -> str:
    """Every character of text in the PDF, normalised to one line."""
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(pdf_path))
    parts = [doc[i].get_textpage().get_text_range() for i in range(len(doc))]
    doc.close()
    return re.sub(r"\s+", " ", " ".join(parts))


def check_against_source(pdf_path: Path, html_path: Path) -> list[str]:
    """The committed PDF must say what the print build says.

    WHY THIS IS A CONTENT CHECK AND NOT A DIFF
    Every other generated artefact here is gated by regenerating it and running
    `git diff --exit-code`. That cannot work for a PDF: Chromium stamps a creation
    date and a document ID, so two runs of the same input differ in bytes. Measured
    — two consecutive runs gave sha256 5b747e9b… and dd69c896…. An mtime gate is no
    use either, because a CI checkout gives every file the same timestamp.

    So the gate is the text. The PDF was three weeks stale and nothing said so: it
    still read "Three faces ship with this system" after the licence chapter had been
    corrected to four, still printed the superseded 1.4 MB figure, and never named
    AnindaMono-Regular.ttf. Every one of those is a string, and a string is checkable.

    Every heading in the print build must appear in the PDF. That is what catches a
    chapter that was rewritten after the PDF was last made.

    WHY IT SPLITS ON NON-LATIN SCRIPT, WHICH IS NOW TRIVIAL AND WAS NOT
    PDF text is stored in VISUAL order. Bangla reorders pre-base vowels and builds
    conjuncts, so extraction gave back the glyphs as they sat on the page rather
    than as they were written. The first version of this check compared whole
    headings and failed 15 of 130 on a PDF it had regenerated seconds earlier —
    every one a heading containing Bangla, and none actually stale.

    The split below is kept even though the book is now English and it therefore
    finds nothing to split on. It costs one regular expression, it is the reason
    the check works at all, and deleting it would leave the next person to
    rediscover visual-order extraction the hard way.
    """
    problems: list[str] = []
    text = pdf_text(pdf_path)
    if len(text) < 20000:
        return [f"only {len(text)} characters of text came out of the PDF, which is "
                f"too little to compare — the extraction did not really run"]

    html = html_path.read_text(encoding="utf-8")
    headings = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", html, re.S)
    missing = []
    compared = 0
    for raw in headings:
        plain = re.sub(r"<[^>]+>", "", raw)
        plain = html_mod.unescape(plain)
        plain = re.sub(r"\s+", " ", plain).strip()
        # Each LATIN SEGMENT, not the heading with non-Latin script squeezed
        # out. Headings used to put Latin on both sides of a Bangla run, so
        # collapsing them gave a string that was never contiguous in the PDF.
        # Splitting is also stricter: every segment has to be there, not just one.
        segments = [seg.strip(" ,·—/·")
                    for seg in re.split(r"[\u0980-\u09FF]+", plain)]
        segments = [re.sub(r"\s+", " ", seg) for seg in segments if len(seg.strip()) >= 4]
        if not segments:
            continue
        compared += 1
        absent = [seg for seg in segments if seg not in text]
        if absent:
            missing.append(" + ".join(absent)[:60])
    if compared < 60:
        problems.append(f"only {compared} headings were long enough to compare, and "
                        f"the book has more than that — the check did not really run")
    if missing:
        problems.append(
            f"{len(missing)} of {compared} headings in the print build are absent "
            f"from the committed PDF, so it was made from an older book: "
            f"{missing[:4]}")
    return problems


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
    # --check does not re-render. It reads the COMMITTED pdf and asks whether it
    # still says what the print build says, which is the question a drift guard
    # asks everywhere else in this repository.
    if "--check" in argv:
        if not PRINT_HTML.exists() or not OUT_PDF.exists():
            print("could not run: the print build or the PDF is missing",
                  file=sys.stderr)
            return 2
        stale = check_against_source(OUT_PDF, PRINT_HTML)
        if stale:
            print("CHECK FAILED — the committed PDF has drifted from the book:\n  "
                  + "\n  ".join(stale), file=sys.stderr)
            return 1
        print("--check: the committed PDF still matches the print build. "
              "Nothing written.")
        return 0

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

    stale = check_against_source(OUT_PDF, PRINT_HTML)
    if stale:
        print("PRINT FAILED\n  " + "\n  ".join(stale), file=sys.stderr)
        return 1
    print("  every heading in the print build appears in the PDF")

    print("  stated limit: the PDF has no bookmark tree. Chromium emits no "
          "outline and this pipeline has no PDF tool to add one. The generated "
          "table of contents with internal links is the whole mitigation.")
    print("PRINT PASSED")

    if "--probe-interactive" in argv:
        probe_interactive()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
