#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
"""
WHY THIS FILE EXISTS
====================
10_assets/ is the web set: favicons, PWA icons, social banners. A store package is
a different thing with different rules, and mixing the two would make one sentence
describe both. The README counts 10_assets as "ready-made images at exact platform
sizes"; a Play feature graphic is not that.

So this folder holds what is handed to somebody else — two developer accounts —
and this script writes all of it. Every figure it uses is a published one, and
every published figure carries the page it came from and the date it was read. A
figure with no source is refused rather than written.

WHAT IT CANNOT DO
-----------------
It cannot make screenshots, because there is no app. Both stores require them and
Apple's guideline 2.3.3 refuses screenshots that show only title art or a splash
screen, so inventing them would produce files that could not be submitted. It
writes correctly sized FRAMES instead, drawn so they could not be mistaken for a
real capture, and a step-by-step guide for replacing them.

The owner's own captures belong in 14_delivery/_captures/, which git ignores and
this script never touches. A build must never delete somebody's own work.

RUN
---
    cd <the repository folder>
    export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
    ./.venv/bin/python 14_delivery/build.py
    ./.venv/bin/python 14_delivery/build.py --check
"""

from __future__ import annotations

import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
APPLE = HERE / "apple-app-store"
PLAY = HERE / "google-play"
CAPTURES = HERE / "_captures"

GENERATOR = "14_delivery/build.py"
DO_NOT_EDIT = ("GENERATED FILE. Written by 14_delivery/build.py. Do not hand-edit — "
               "the next build overwrites it.")
CHECKED = "2026-08-26"


class BuildError(Exception):
    pass


class NotEquipped(Exception):
    pass


def _assets_module():
    """Reuse 10_assets/build.py rather than copying its harness.

    Every pixel in this repository comes out of one Chromium harness with one
    Pillow measurement suite. A second copy of that is the duplication
    scripts/check_gates.py exists because of.
    """
    path = ROOT / "10_assets" / "build.py"
    spec = importlib.util.spec_from_file_location("aninda_assets", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["aninda_assets"] = mod          # before exec, or @dataclass breaks
    spec.loader.exec_module(mod)
    return mod


# =========================================================================
# Every published figure, with the page it came from and the date it was read
# =========================================================================

VERIFIED = {
    "play-icon": {
        "spec": "Google Play app icon, 512 x 512 px, 32-bit PNG, sRGB, "
                "under 1024 KB, full square",
        "url": "https://developer.android.com/distribute/google-play/resources/"
               "icon-design-specifications",
        "quote": "Final size: 512 px by 512 px. Format: 32-bit PNG. Color space: sRGB. "
                 "Max file size: 1024 KB. Shape: Full square — Google Play "
                 "dynamically handles masking.",
        "note": "Google Play applies a corner radius equivalent to 30 per cent of the "
                "icon size, which is 153.6 px on a 512 px asset, and adds the drop "
                "shadow itself. Neither is baked in here.",
        "checked": CHECKED,
    },
    "play-feature-graphic": {
        "spec": "Google Play feature graphic, 1024 x 500 px, JPEG or 24-bit PNG, "
                "no alpha. Mandatory to publish",
        "url": "https://support.google.com/googleplay/android-developer/answer/9866151",
        "quote": "You must provide a feature graphic to publish your store listing. "
                 "JPEG or 24-bit PNG (no alpha). Dimensions: 1024 px by 500 px.",
        "note": "Android's core app quality criterion Play_Feature_Graphic adds that it "
                "must not contain device images or screenshots, must not carry small "
                "text that becomes illegible when scaled down, and must not resemble "
                "an advertisement.",
        "checked": CHECKED,
    },
    "play-screenshot-phone": {
        "spec": "Google Play phone screenshot, JPEG or 24-bit PNG, no alpha, minimum "
                "side 320 px, maximum 3840 px, longer side no more than twice the "
                "shorter. At least two are mandatory to publish",
        "url": "https://support.google.com/googleplay/android-developer/answer/9866151",
        "quote": "You must provide a minimum of two screenshots across different "
                 "device types to publish your store listing.",
        "note": "Google recommends at least four at 1080 px minimum, either 16:9 "
                "landscape or 9:16 portrait. 1080 x 1920 is the portrait figure and is "
                "what the frames here are drawn at.",
        "checked": CHECKED,
    },
    "play-adaptive-icon": {
        "spec": "Android adaptive icon, three layers at 108 x 108 dp, safe zone "
                "66 x 66 dp centred, 18 dp per side reserved",
        "url": "https://developer.android.com/develop/ui/views/launch/"
               "icon_design_adaptive",
        "quote": "The outer 18 dp on each of the four sides of the layers is reserved "
                 "for masking and to create visual effects such as parallax or pulsing.",
        "note": "Declared at res/mipmap-anydpi-v26/ic_launcher.xml. The monochrome "
                "layer supports user theming from Android 13, API level 33.",
        "checked": CHECKED,
    },
    "play-listing-text": {
        "spec": "Google Play listing text: title 30 characters, short description 80, "
                "full description 4000",
        "url": "https://support.google.com/googleplay/android-developer/answer/9859152",
        "quote": "Character limits apply to both full-width and half-width characters.",
        "note": "The Metadata policy bans ranking or price claims, Play programme "
                "labels, emoji and repeated special characters in the title, and "
                "capitals other than a brand name.",
        "checked": CHECKED,
    },
    "apple-app-icon": {
        "spec": "Apple app icon layout size 1024 x 1024 px for iOS, iPadOS, macOS and "
                "visionOS, and 1088 x 1088 px for watchOS, unmasked",
        "url": "https://developer.apple.com/design/human-interface-guidelines/app-icons",
        "quote": "Produce appropriately shaped, unmasked layers. The system masks all "
                 "layer edges to produce an icon's final shape.",
        "note": "Colour spaces supported are sRGB, Gray Gamma 2.2 and Display P3; "
                "Display P3 is not supported on visionOS. These masters are sRGB and "
                "declare it.",
        "checked": CHECKED,
    },
    "apple-screenshots": {
        "spec": "App Store Connect screenshots: iPhone 6.9 inch 1290 x 2796 px, iPad "
                "13 inch 2064 x 2752 px, 1 to 10 per device type, no alpha",
        "url": "https://developer.apple.com/help/app-store-connect/reference/"
               "app-information/screenshot-specifications",
        "quote": "No alpha channels or transparencies allowed.",
        "note": "The iPad 13 inch set is required only if the app runs on iPad. The "
                "6.5 inch iPhone set is required only when 6.9 inch is not provided, "
                "and 6.9 inch is provided here, so it is deliberately absent.",
        "checked": CHECKED,
    },
    "apple-screenshot-content": {
        "spec": "Screenshots must show the app in use",
        "url": "https://developer.apple.com/app-store/review/guidelines/",
        "quote": "Screenshots should show the app in use, and not merely the title "
                 "art, login page, or splash screen.",
        "note": "App Review Guideline 2.3.3. It is the reason the frames here carry no "
                "mark: a template that resembles the rejected thing invites the "
                "mistake it exists to prevent.",
        "checked": CHECKED,
    },
    "apple-listing-text": {
        "spec": "App Store text: name 30 characters, subtitle 30, promotional text "
                "170, description 4000, keywords 100 bytes",
        "url": "https://developer.apple.com/help/app-store-connect/reference/"
               "app-information",
        "quote": "App names must be limited to 30 characters.",
        "note": "Apple's own pages disagree on keywords: the App Store Connect "
                "reference says 100 bytes and the marketing page says 100 characters. "
                "The tighter reading is used here, because for a non-Latin script the "
                "two differ and bytes is the smaller budget.",
        "checked": CHECKED,
    },
}

# Derived, not published. Google gives the formula and not the table.
ANDROID_DENSITIES = {"mdpi": 108, "hdpi": 162, "xhdpi": 216,
                     "xxhdpi": 324, "xxxhdpi": 432}


# =========================================================================
# Guards. Each one measures a published requirement, and names it.
# =========================================================================

def guard_verified_entries() -> None:
    """A 'verified' figure with no quote, no URL or no date is not verified.

    The entries in 10_assets/build.py each carry a sentence lifted off the
    platform's own help page, and nothing enforced that. These are the first whose
    figures arrived through a research pass rather than off the page, so the rule
    is a gate here rather than a habit.
    """
    for key, entry in sorted(VERIFIED.items()):
        for field in ("spec", "url", "quote", "note", "checked"):
            if not entry.get(field):
                raise BuildError(
                    f"VERIFIED[{key!r}] has no {field!r}. Every verified figure "
                    f"carries the page it came from, the sentence it came from, and "
                    f"the date it was read. Mark it unverified rather than leaving a "
                    f"field empty.")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", entry["checked"]):
            raise BuildError(f"VERIFIED[{key!r}]['checked'] is not a date.")


def guard_no_alpha(image, name: str) -> None:
    """The band must be ABSENT, not merely full.

    Both stores say "no alpha" for these, and a fully opaque RGBA file still has an
    alpha channel. Play calls the feature graphic 24-bit; an RGBA PNG is 32-bit.
    """
    if "A" in image.getbands():
        raise BuildError(
            f"{name}: carries an alpha channel. Both stores ask for no alpha on this "
            f"asset, and a fully opaque alpha channel is still an alpha channel — the "
            f"file would be 32-bit where 24 is asked for.")


def guard_full_square(image, name: str) -> None:
    """Every corner opaque and the same colour: the artwork covers its whole frame."""
    w, h = image.size
    px = image.convert("RGBA")
    corners = [px.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    for i, c in enumerate(corners):
        if c[3] != 255:
            raise BuildError(
                f"{name}: corner {i} has alpha {c[3]}, not 255. Both stores apply "
                f"their own mask to this asset, so it has to be a full square — "
                f"a transparent corner means a radius was baked in.")
    if len({c[:3] for c in corners}) != 1:
        raise BuildError(
            f"{name}: the four corners are not the same colour ({corners}). A "
            f"full-bleed ground should reach every corner identically.")


def guard_play_corner_mask(image, name: str) -> None:
    """Nothing the mark needs may sit where Play's own 30 per cent mask will cut.

    Google publishes the radius as a percentage and does not say whether the curve
    is a rounded rectangle or a superellipse. This checks the weaker, safe thing:
    that the four corner squares the mask works within are solid ground, so
    whichever curve it is, it removes ground and never artwork.
    """
    w, h = image.size
    r = int(round(0.30 * w))
    px = image.convert("RGBA")
    ground = px.getpixel((0, 0))
    for ox, oy in ((0, 0), (w - r, 0), (0, h - r), (w - r, h - r)):
        for x in range(ox, ox + r, max(1, r // 24)):
            for y in range(oy, oy + r, max(1, r // 24)):
                if px.getpixel((x, y)) != ground:
                    raise BuildError(
                        f"{name}: artwork reaches ({x},{y}), inside the {r} px corner "
                        f"square Google Play's 30 per cent mask works within. Play "
                        f"would cut it.")


def guard_alpha_is_the_shape(image, name: str) -> None:
    """A composited layer must be neither blank nor solid."""
    if "A" not in image.getbands():
        raise BuildError(f"{name}: has no alpha channel, so it cannot be a "
                         f"composited layer.")
    a = image.getchannel("A")
    lo, hi = a.getextrema()
    if lo != 0:
        raise BuildError(f"{name}: no fully transparent pixel (alpha minimum {lo}). "
                         f"This layer is composited over something the system "
                         f"supplies, so it must not fill its frame.")
    if hi != 255:
        raise BuildError(f"{name}: no fully opaque pixel (alpha maximum {hi}). "
                         f"Nothing was drawn.")


def guard_safe_zone_66(image, name: str) -> None:
    """Every drawn pixel inside the 66-of-108 dp circle, and not far inside it.

    Two-sided on purpose. A one-sided check passes a mark that has silently shrunk
    to a dot, which is the failure a scale change actually produces.
    """
    w, h = image.size
    px = image.convert("RGBA")
    cx, cy = w / 2, h / 2
    limit = (66.0 / 108.0) * w / 2
    worst = 0.0
    step = max(1, w // 256)
    for x in range(0, w, step):
        for y in range(0, h, step):
            if px.getpixel((x, y))[3] > 8:
                d = ((x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2) ** 0.5
                worst = max(worst, d)
    if worst > limit:
        raise BuildError(
            f"{name}: ink reaches {worst:.1f} px from centre, outside the "
            f"{limit:.1f} px radius of Google's 66 dp safe zone. A launcher mask "
            f"would clip it.")
    if worst < limit * 0.80:
        raise BuildError(
            f"{name}: ink reaches only {worst:.1f} px of the {limit:.1f} px safe "
            f"radius, which is {100 * worst / limit:.0f} per cent. The mark has "
            f"shrunk — an icon that fits by being tiny is not fitting.")


def guard_background_flat(image, name: str) -> None:
    counts = image.convert("RGBA").getcolors(4)
    if counts is None or len(counts) != 1:
        raise BuildError(
            f"{name}: the background layer is not one flat colour. Google asks for "
            f"clean edges with no mask and no shadow drawn into the layer.")


def guard_monochrome_single_channel(image, name: str) -> None:
    px = image.convert("RGBA")
    w, h = px.size
    step = max(1, w // 128)
    for x in range(0, w, step):
        for y in range(0, h, step):
            r, g, b, a = px.getpixel((x, y))
            if a > 8 and not (r == g == b):
                raise BuildError(
                    f"{name}: pixel ({x},{y}) is ({r},{g},{b}), which is not a single "
                    f"grey. The system tints this layer, so it must carry one value.")


def guard_max_bytes(data: bytes, name: str, limit: int) -> None:
    if len(data) > limit:
        raise BuildError(f"{name}: {len(data)} bytes, over the published "
                         f"{limit} byte limit.")


def guard_srgb_declared(data: bytes, name: str) -> None:
    from PIL import Image
    info = Image.open(io.BytesIO(data)).info
    if info.get("srgb") is None:
        raise BuildError(
            f"{name}: declares no colour space. Google Play asks for sRGB by name, "
            f"and a file that does not say which space its numbers are in leaves that "
            f"to whatever opens it.")


def guard_screenshot_shape(w: int, h: int, store: str, name: str) -> None:
    if store == "play":
        lo, hi = min(w, h), max(w, h)
        if lo < 320:
            raise BuildError(f"{name}: shortest side {lo} px, under Google's 320 px "
                             f"minimum.")
        if hi > 3840:
            raise BuildError(f"{name}: longest side {hi} px, over Google's 3840 px "
                             f"maximum.")
        if hi > 2 * lo:
            raise BuildError(
                f"{name}: {w}x{h}. Google refuses a screenshot whose longest side is "
                f"more than twice its shortest.")
    else:
        allowed = {(1290, 2796), (1320, 2868), (1260, 2736),
                   (2064, 2752), (2048, 2732)}
        if (w, h) not in allowed:
            raise BuildError(
                f"{name}: {w}x{h} is not an accepted App Store Connect size. The sizes "
                f"shipped here are 1290x2796 for iPhone 6.9 inch and 2064x2752 for "
                f"iPad 13 inch.")


# =========================================================================
# The store text. Held to the published limits, and to the published bans.
# =========================================================================

# Google's Metadata policy bans these outright in a title, an icon or a developer
# name, and its store-listing guidance extends most of them to every field and to
# the graphics. Apple's guideline 2.3.7 bans price and rank claims in metadata
# too, so one list serves both.
BANNED_STORE_PATTERNS = [
    (r"\b(best|#\s?1|no\.?\s?1|top|number one)\b", "a ranking claim"),
    (r"\b(free|discount|sale|off|cheap|deal|offer)\b", "a price or promotion claim"),
    (r"\b(editor'?s choice|app of the (year|day)|game of the (day|year))\b",
     "a store programme label"),
    (r"\b(million|billion)\s+(downloads|users|installs)\b", "a popularity claim"),
    (r"\b(award|award-winning|accolade)\b", "an unverifiable accolade"),
    (r"[\U0001F300-\U0001FAFF☀-➿]", "an emoji"),
    (r"(!{2,}|\?{2,}|\.{4,})", "repeated punctuation"),
]

STORE_TEXT = {
    "play": {
        "title": ("Aninda Studio", 30),
        "short_description": ("Small, careful software from a one-person studio.", 80),
        "full_description": (
            "Aninda Studio is one person making small, careful software.\n\n"
            "Everything here is built on a design system where the claims are "
            "measured rather than asserted. Every colour pairing was measured "
            "against every surface it can land on, in a real browser, and the "
            "published figure is the worst result rather than the flattering one. "
            "Where something has a limit, the limit is written down.\n\n"
            "The system is bilingual. English and Bangla are both first-class, and "
            "the Bangla type was measured rather than scaled by eye: it carries its "
            "own size ramp, its own floor, and a weight step for small sizes.\n\n"
            "This listing describes the studio. No app is published yet.",
            4000),
    },
    "apple": {
        "name": ("Aninda Studio", 30),
        "subtitle": ("Small, careful software", 30),
        "promotional_text": (
            "A design system where every colour pairing is measured against every "
            "surface it can land on, and the worst result is the one published.",
            170),
        "description": (
            "Aninda Studio is one person making small, careful software.\n\n"
            "Everything here is built on a design system where the claims are "
            "measured rather than asserted. Every colour pairing was measured "
            "against every surface it can land on, in a real browser, and the "
            "published figure is the worst result rather than the flattering one. "
            "Where something has a limit, the limit is written down.\n\n"
            "The system is bilingual. English and Bangla are both first-class, and "
            "the Bangla type was measured rather than scaled by eye: it carries its "
            "own size ramp, its own floor, and a weight step for small sizes.\n\n"
            "This listing describes the studio. No app is published yet.",
            4000),
        "keywords": ("design system,design tokens,accessibility,contrast,bangla,"
                     "typography,brand", 100),
    },
}

# Bangla. Apple added Bangla to its metadata languages on 30 March 2026 and names
# it "Bangla", which is this studio's own term. Only vocabulary already verified
# in 06_type/bangla-strings.json and the READMEs is used; where no verified term
# exists the English stands, which is the rule this kit already follows.
STORE_TEXT_BN = {
    "play": {
        "title": ("অনিন্দ্য স্টুডিও", 30),
        "short_description": ("এক জনের গড়া ছোটো, যত্নের সফটওয়্যার।", 80),
        "full_description": (
            "অনিন্দ্য স্টুডিও — এক জন মানুষ, ছোটো আর যত্নে গড়া সফটওয়্যার।\n\n"
            "এখানের সব কিছু এমন একটি ডিজাইন পদ্ধতির উপর গড়া, যেখানে প্রতিটি দাবি "
            "মেপে দেখা হয়েছে, শুধু বলা হয়নি। প্রতিটি রঙের জোড়া যে যে পৃষ্ঠের উপর "
            "বসতে পারে, সবগুলোর সঙ্গে সত্যিকারের ব্রাউজারে মেপে দেখা হয়েছে — আর "
            "প্রকাশ করা হয়েছে সবচেয়ে খারাপ ফলাফলটি, সবচেয়ে ভালোটি নয়। কোনো কিছুর "
            "সীমা থাকলে সেটাও লেখা আছে।\n\n"
            "পদ্ধতিটি দুই ভাষার। বাংলা আর ইংরেজি — দুটোই সমান গুরুত্ব পায়। বাংলা "
            "হরফের মাপ চোখে দেখে বসানো হয়নি, মেপে নেওয়া হয়েছে: তার নিজের মাপের "
            "ধাপ আছে, নিজের সর্বনিম্ন সীমা আছে, আর ছোটো মাপে একটি ওজনের ধাপও আছে।\n\n"
            "এই তালিকাটি স্টুডিওর পরিচয়। এখনো কোনো অ্যাপ প্রকাশ করা হয়নি।",
            4000),
    },
    "apple": {
        "name": ("অনিন্দ্য স্টুডিও", 30),
        "subtitle": ("ছোটো, যত্নের সফটওয়্যার", 30),
        "promotional_text": (
            "একটি ডিজাইন পদ্ধতি, যেখানে প্রতিটি রঙের জোড়া প্রতিটি পৃষ্ঠের সঙ্গে "
            "মেপে দেখা হয়েছে — আর প্রকাশ করা হয়েছে সবচেয়ে খারাপ ফলাফলটি।",
            170),
        "description": (
            "অনিন্দ্য স্টুডিও — এক জন মানুষ, ছোটো আর যত্নে গড়া সফটওয়্যার।\n\n"
            "এখানের সব কিছু এমন একটি ডিজাইন পদ্ধতির উপর গড়া, যেখানে প্রতিটি দাবি "
            "মেপে দেখা হয়েছে, শুধু বলা হয়নি। প্রতিটি রঙের জোড়া যে যে পৃষ্ঠের উপর "
            "বসতে পারে, সবগুলোর সঙ্গে সত্যিকারের ব্রাউজারে মেপে দেখা হয়েছে — আর "
            "প্রকাশ করা হয়েছে সবচেয়ে খারাপ ফলাফলটি, সবচেয়ে ভালোটি নয়।\n\n"
            "পদ্ধতিটি দুই ভাষার। বাংলা আর ইংরেজি — দুটোই সমান গুরুত্ব পায়।\n\n"
            "এই তালিকাটি স্টুডিওর পরিচয়। এখনো কোনো অ্যাপ প্রকাশ করা হয়নি।",
            4000),
        "keywords": ("ডিজাইন,টোকেন,অভিগম্যতা,কনট্রাস্ট,বাংলা,হরফ", 100),
    },
}


def guard_text_limits(store: str, fields: dict, label: str) -> list[dict]:
    """Both counts, because neither store publishes which one it means.

    Apple's own pages disagree between 100 bytes and 100 characters for keywords.
    Every field here is measured in code points AND in UTF-8 bytes, and both have
    to clear the limit. For the ASCII drafts the two agree; for the Bangla they do
    not, which is exactly why both are recorded.
    """
    rows = []
    for field, (text, limit) in sorted(fields.items()):
        chars, byts = len(text), len(text.encode("utf-8"))
        worst = max(chars, byts)
        if worst > limit:
            raise BuildError(
                f"{label} {field}: {chars} code points and {byts} UTF-8 bytes, over "
                f"the published limit of {limit}. Neither store says which unit it "
                f"counts, so the larger of the two has to fit.")
        for pattern, why in BANNED_STORE_PATTERNS:
            hit = re.search(pattern, text, re.I)
            if hit:
                raise BuildError(
                    f"{label} {field}: contains {hit.group(0)!r}, which is "
                    f"{why}. Both stores refuse it in listing text.")
        rows.append({"field": field, "limit": limit, "code_points": chars,
                     "utf8_bytes": byts, "text": text})
    return rows


# =========================================================================
# Rendering
# =========================================================================

def icon_html(A, source: str, opaque: bool) -> str:
    """One mark artefact filling its frame. No rounding is added or removed here —
    the masters are already the shape each platform asked for."""
    node = A.fill_box(A.load_svg(source))
    ground = (f'<div class="ground" style="background-color:var(--as-ink)"></div>'
              if opaque else "")
    return A.page_shell("light", ground + '<div class="fill">' + A.svg_to_text(node)
                        + "</div>",
                        ".fill svg{display:block;width:100%;height:100%;}")


def feature_graphic_html(A) -> str:
    """1024 x 500, and deliberately plain.

    Android's core app quality criterion Play_Feature_Graphic refuses device images,
    screenshots, small text that stops being legible when scaled down, and anything
    that resembles an advertisement. So this is the mark, the name, and one line —
    at sizes that survive the thumbnail Play actually shows.
    """
    node = A.fill_box(A.load_svg("icon-1024.svg"))
    return A.page_shell(
        "dark",
        '<div class="ground" style="background-color:var(--as-surface-lowest)"></div>'
        '<div class="fg">'
        f'<div class="art">{A.svg_to_text(node)}</div>'
        '<div class="words">'
        '<div class="name">Aninda Studio</div>'
        f'<div class="line">{A.TAGLINE}</div>'
        "</div></div>",
        """
        .fg{position:absolute;inset:0;display:flex;align-items:center;
            gap:56px;padding:0 96px;}
        .art{width:236px;height:236px;flex:0 0 auto;}
        .art svg{display:block;width:100%;height:100%;}
        .words{display:flex;flex-direction:column;gap:18px;}
        .name{font-family:var(--as-font-latin);font-size:76px;font-weight:600;
              color:var(--as-ink);line-height:1.1;}
        .line{font-family:var(--as-font-latin);font-size:34px;font-weight:400;
              color:var(--as-ink-muted);line-height:1.3;}
        """,
        with_font=True,
    )


def frame_html(A, w: int, h: int, device: str, filename: str, folder: str) -> str:
    """A screenshot frame that could not be mistaken for a screenshot.

    Four things make it unmistakable, and the first matters most because it works
    at thumbnail size where no text can be read: a 45-degree hatch across the whole
    frame. No real interface screenshot has one.

    It carries NO mark and NO wordmark. A frame showing only the logo is precisely
    what App Review Guideline 2.3.3 rejects — "not merely the title art, login
    page, or splash screen" — and a template that resembles the rejected thing
    invites the mistake it exists to prevent.
    """
    return A.page_shell(
        "light",
        '<div class="ground" style="background-color:var(--as-surface-dim)"></div>'
        '<div class="hatch"></div>'
        '<div class="edge"></div>'
        '<div class="mid">'
        '<div class="t1">Template. Not a screenshot.</div>'
        f'<div class="t2">{w} x {h} px · {device}</div>'
        f'<div class="t3">Replace with a real capture named {filename}</div>'
        f'<div class="t4">Put it in {folder}</div>'
        "</div>",
        f"""
        .hatch{{position:absolute;inset:0;background:repeating-linear-gradient(
            45deg, transparent 0 18px, var(--as-line) 18px 20px);opacity:0.22;}}
        .edge{{position:absolute;inset:{max(12, w // 40)}px;
               border:1px solid var(--as-line);}}
        .mid{{position:absolute;inset:0;display:flex;flex-direction:column;
              align-items:center;justify-content:center;gap:{max(10, h // 90)}px;
              padding:0 {max(24, w // 12)}px;text-align:center;
              font-family:var(--as-font-latin);}}
        .t1{{font-size:{max(20, w // 22)}px;font-weight:600;color:var(--as-ink);}}
        .t2{{font-size:{max(14, w // 34)}px;color:var(--as-ink);}}
        .t3{{font-size:{max(12, w // 44)}px;color:var(--as-ink-muted);}}
        .t4{{font-size:{max(12, w // 44)}px;color:var(--as-ink-muted);}}
        """,
        with_font=True,
    )


def stamp_png(A, png: bytes, name: str, note: str, rgb: bool) -> bytes:
    """Header chunks, plus the sRGB declaration both stores expect.

    10_assets/build.py stamps Software and Comment. This adds an sRGB chunk, which
    is what closes the honest half of benchmark criterion 7: the file now DECLARES
    which space its numbers are in. It does not claim the renderer produced sRGB
    values, and this docstring is the place that says so.
    """
    from PIL import Image, PngImagePlugin
    im = Image.open(io.BytesIO(png))
    if rgb:
        im = im.convert("RGB")          # drops the band, so 24-bit rather than 32
    info = PngImagePlugin.PngInfo()
    info.add_text("Software", GENERATOR)
    info.add_text("Comment", note)
    info.add(b"sRGB", b"\x00")          # 0 = perceptual rendering intent
    buf = io.BytesIO()
    im.save(buf, "PNG", pnginfo=info, optimize=True)
    return buf.getvalue()


# =========================================================================
# What each package holds
# =========================================================================

def asset_list() -> list[dict]:
    items: list[dict] = []

    # --- Apple ----------------------------------------------------------
    for name, source, size, appearance, alpha in (
        ("icon-1024.png", "icon-apple-1024.svg", 1024, "Default", "opaque"),
        ("icon-1024-dark.png", "icon-apple-1024-dark.svg", 1024, "Dark", "opaque"),
        ("icon-1024-mono.png", "icon-apple-1024-mono.svg", 1024, "Mono", "alpha"),
        ("icon-1088-watch.png", "icon-apple-1088-watch.svg", 1088, "Default", "opaque"),
    ):
        items.append({
            "root": APPLE, "path": f"icon/{name}", "w": size, "h": size,
            "render": ("icon", source, alpha == "opaque"),
            "alpha": alpha,
            "purpose": f"Apple app icon, {appearance} appearance, {size} x {size} px.",
            "source_svg": source, "cite": "apple-app-icon",
        })
    for i in range(1, 5):
        items.append({
            "root": APPLE, "path": f"screenshots/frames/iphone-6.9-1290x2796-{i:02d}.png",
            "w": 1290, "h": 2796, "render": ("frame", "iPhone 6.9 inch, portrait"),
            "alpha": "no-alpha-channel", "store": "apple",
            "purpose": f"Screenshot frame {i} of 4, iPhone 6.9 inch. A template.",
            "cite": "apple-screenshots",
        })
    for i in range(1, 5):
        items.append({
            "root": APPLE, "path": f"screenshots/frames/ipad-13-2064x2752-{i:02d}.png",
            "w": 2064, "h": 2752, "render": ("frame", "iPad 13 inch, portrait"),
            "alpha": "no-alpha-channel", "store": "apple",
            "purpose": f"Screenshot frame {i} of 4, iPad 13 inch. A template.",
            "cite": "apple-screenshots",
        })

    # --- Google Play ----------------------------------------------------
    items.append({
        "root": PLAY, "path": "store-listing/icon-512.png", "w": 512, "h": 512,
        "render": ("icon", "icon-apple-1024.svg", True),
        "alpha": "opaque-with-band", "max_bytes": 1_024_000,
        "purpose": "Google Play store icon. Full square; Play applies its own 30 per "
                   "cent corner mask and its own drop shadow.",
        "source_svg": "icon-apple-1024.svg", "cite": "play-icon",
    })
    items.append({
        "root": PLAY, "path": "store-listing/feature-graphic-1024x500.png",
        "w": 1024, "h": 500, "render": ("feature",),
        "alpha": "no-alpha-channel",
        "purpose": "Google Play feature graphic. Mandatory to publish a listing.",
        "cite": "play-feature-graphic",
    })
    for i in range(1, 5):
        items.append({
            "root": PLAY,
            "path": f"store-listing/screenshots/frames/phone-1080x1920-{i:02d}.png",
            "w": 1080, "h": 1920, "render": ("frame", "Android phone, portrait"),
            "alpha": "no-alpha-channel", "store": "play",
            "purpose": f"Screenshot frame {i} of 4, Android phone. A template.",
            "cite": "play-screenshot-phone",
        })
    for density, px in sorted(ANDROID_DENSITIES.items(), key=lambda kv: kv[1]):
        for layer, source, alpha in (
            ("background", "icon-android-background-108.svg", "opaque"),
            ("foreground", "icon-android-foreground-108.svg", "alpha"),
            ("monochrome", "icon-android-monochrome-108.svg", "mono"),
        ):
            items.append({
                "root": PLAY,
                "path": f"app-res/mipmap-{density}/ic_launcher_{layer}.png",
                "w": px, "h": px,
                "render": ("icon", source, alpha == "opaque"),
                "alpha": "opaque" if alpha == "opaque" else "alpha",
                "layer": layer, "density": density,
                "purpose": f"Android adaptive icon {layer} layer at {density}, "
                           f"{px} px for a 108 dp canvas.",
                "source_svg": source, "cite": "play-adaptive-icon",
            })
    return items


def render_all(A, items: list[dict]) -> dict[Path, bytes]:
    from playwright.sync_api import sync_playwright
    from PIL import Image

    out: dict[Path, bytes] = {}
    try:
        pw = sync_playwright().start()
    except Exception as exc:
        raise NotEquipped(f"playwright would not start — {exc}") from exc
    try:
        try:
            browser = pw.chromium.launch()
        except Exception as exc:
            raise NotEquipped(
                "Chromium would not launch. Did you export "
                f"PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers ?\n  {exc}") from exc

        for item in items:
            kind = item["render"][0]
            if kind == "icon":
                html = icon_html(A, item["render"][1], item["render"][2])
            elif kind == "feature":
                html = feature_graphic_html(A)
            else:
                folder = ("14_delivery/_captures/apple/" if item["store"] == "apple"
                          else "14_delivery/_captures/google/")
                html = frame_html(A, item["w"], item["h"], item["render"][1],
                                  Path(item["path"]).name.replace("-01", "-01")
                                  .replace("frames/", ""), folder)

            context = browser.new_context(
                viewport={"width": item["w"], "height": item["h"]},
                device_scale_factor=1)
            page = context.new_page()
            failures: list[str] = []
            page.on("pageerror", lambda e: failures.append(str(e)))
            page.on("requestfailed", lambda r: failures.append(f"{r.url} — {r.failure}"))
            page.set_content(html, wait_until="load")
            page.wait_for_timeout(60)
            png = page.screenshot(omit_background=item["alpha"] in ("alpha",))
            context.close()
            if failures:
                raise BuildError(f"{item['path']}: the render page reported {failures}")

            rgb = item["alpha"] == "no-alpha-channel"
            png = stamp_png(A, png, Path(item["path"]).name, item["purpose"], rgb)

            im = Image.open(io.BytesIO(png))
            name = item["path"]
            if im.size != (item["w"], item["h"]):
                raise BuildError(f"{name}: rendered {im.size}, declared "
                                 f"({item['w']}, {item['h']}).")
            guard_srgb_declared(png, name)

            if item["alpha"] == "no-alpha-channel":
                guard_no_alpha(im, name)
                guard_screenshot_shape(item["w"], item["h"], item.get("store", "play"),
                                       name) if item["render"][0] == "frame" else None
            elif item["alpha"] in ("opaque", "opaque-with-band"):
                guard_full_square(im, name)
            elif item["alpha"] == "alpha":
                guard_alpha_is_the_shape(im, name)

            if item.get("cite") == "play-icon":
                guard_play_corner_mask(im, name)
            if item.get("max_bytes"):
                guard_max_bytes(png, name, item["max_bytes"])
            if item.get("layer") == "background":
                guard_background_flat(im, name)
            if item.get("layer") == "foreground":
                guard_safe_zone_66(im, name)
            if item.get("layer") == "monochrome":
                guard_safe_zone_66(im, name)
                guard_monochrome_single_channel(im, name)

            item["bytes"] = len(png)
            out[item["root"] / item["path"]] = png
        browser.close()
    finally:
        pw.stop()
    return out


# =========================================================================
# The text that travels with the images
# =========================================================================

LAUNCHER_XML = """<?xml version="1.0" encoding="utf-8"?>
<!-- GENERATED FILE. Written by 14_delivery/build.py. Do not hand-edit — the next
     build overwrites it.
     The monochrome element is declared unconditionally. It is read from Android 13
     (API level 33), and from Android 16 QPR 2 the system generates one for any app
     that does not supply it — having the shape inferred is worse than supplying it. -->
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@mipmap/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
    <monochrome android:drawable="@mipmap/ic_launcher_monochrome"/>
</adaptive-icon>
"""

CAPTURE_STEPS = """## Replacing the screenshot frames

The frames in `screenshots/frames/` are templates. They are generated and gated,
so overwriting one turns `--check` red. Nothing below asks you to overwrite them.

1. Open one frame and read the size printed on it.
2. Make the folder `{captures}`. Git ignores it and this build never touches it,
   so nothing can overwrite or delete what you put there.
3. Take the screenshot on a device or simulator whose screen is that exact pixel
   size. {store_size_note}
4. Save it into that folder, named `{example}`.
5. Repeat until you have four, each showing the app being used. Not the launch
   screen, not the sign-in page, not the logo.
6. Upload from `{captures}`, never from `screenshots/frames/`.

{store_rule}
"""


def package_readme(store: str, items: list[dict], text_rows, text_rows_bn) -> str:
    is_apple = store == "apple"
    name = "Apple App Store" if is_apple else "Google Play"
    captures = "14_delivery/_captures/apple/" if is_apple else "14_delivery/_captures/google/"
    example = "iphone-6.9-01.png" if is_apple else "phone-01.png"
    size_note = ("App Store Connect accepts the capture only at a size it lists."
                 if is_apple else
                 "Google accepts a range: shortest side at least 320 px, longest at "
                 "most 3840, and the longest no more than twice the shortest.")
    rule = (
        "> App Review Guideline 2.3.3: \"Screenshots should show the app in use, and "
        "not merely the title art, login page, or splash screen.\"\n>\n> That is why "
        "these frames carry no mark. A frame showing only the logo resembles the "
        "thing the guideline rejects."
        if is_apple else
        "> Google requires a minimum of two screenshots across device types to publish "
        "a listing, and recommends at least four at 1080 px or more."
    )
    mine = [i for i in items if i["root"].name.endswith(
        "apple-app-store" if is_apple else "google-play")]
    rows = "\n".join(
        f"| `{i['path']}` | {i['w']} x {i['h']} | {i['bytes']:,} | {i['purpose']}|"
        for i in sorted(mine, key=lambda x: x["path"]))
    lang = "English and Bangla" if True else ""
    return f"""<!-- {DO_NOT_EDIT} -->

# {name} — asset package

Written by `{GENERATOR}` on the sources in `04_mark/svg/`. Every size here is a
published figure, and `MANIFEST.json` carries the page each one came from and the
date it was read.

**No app is published yet.** This package is complete as a set of assets and
incomplete as a submission, and `CHECKLIST.md` says which is which.

## What is in here

| File | Pixels | Bytes | What it is |
|---|---|---|---|
{rows}

## The text

`metadata/metadata.json` holds every field with its published limit and both
counts — code points and UTF-8 bytes — because neither store says which unit it
counts. `metadata/metadata.md` is the same text laid out for copying.

Metadata is supplied in {lang}. Apple added Bangla to its metadata languages on
30 March 2026 and names it "Bangla", which is this studio's own term.

{CAPTURE_STEPS.format(captures=captures, example=example,
                      store_size_note=size_note, store_rule=rule)}

## The badge

Neither store's badge is produced here, and no badge artwork in this repository is
verified. Take the current artwork from the source each company names, at the time
you use it.

- **Apple.** Minimum 10 mm in print, 40 px on screen. Clear space one quarter of
  the badge height. Do not modify, angle or animate it. The credit line is a
  fill-in-the-blank template Apple publishes; there is no single fixed sentence.
- **Google.** Minimum height 28 px digital, 0.3 inches in print. Clear space one
  quarter of the badge height. Do not recolour or rearrange it. The attribution
  line must be produced by Google's own Legal line generator, because Google
  publishes no fixed string.
"""


def package_checklist(store: str) -> str:
    is_apple = store == "apple"
    ready = ("- [x] App icon, 1024 x 1024, square and unmasked, sRGB declared\n"
             "- [x] Dark and Mono appearances authored\n"
             "- [x] watchOS master at 1088 x 1088\n"
             "- [x] Screenshot frames at 1290 x 2796 and 2064 x 2752\n"
             "- [x] Name, subtitle, promotional text, description and keywords, "
             "within limits, English and Bangla\n"
             if is_apple else
             "- [x] Store icon, 512 x 512, full square, sRGB declared, under 1024 KB\n"
             "- [x] Feature graphic, 1024 x 500, no alpha\n"
             "- [x] Adaptive icon layers at five densities, plus ic_launcher.xml\n"
             "- [x] Monochrome layer for themed icons\n"
             "- [x] Screenshot frames at 1080 x 1920\n"
             "- [x] Title, short description and full description, within limits, "
             "English and Bangla\n")
    blocked = ("- [ ] **Real screenshots.** Frames are templates. Guideline 2.3.3 "
               "refuses a screenshot that shows only title art or a splash screen.\n"
               "- [ ] **An app.** There is nothing to submit yet.\n"
               "- [ ] Privacy policy URL — required, and needs a live page\n"
               "- [ ] Support URL — required, and must reach real contact details\n"
               "- [ ] Age rating questionnaire — a form, not a file\n"
               "- [ ] App previews — optional, 15 to 30 seconds\n"
               if is_apple else
               "- [ ] **Real screenshots.** Frames are templates. At least two are "
               "mandatory to publish.\n"
               "- [ ] **An app.** There is nothing to submit yet.\n"
               "- [ ] Privacy policy URL — required\n"
               "- [ ] Data safety form — a form, not a file\n"
               "- [ ] Content rating questionnaire — a form, not a file\n"
               "- [ ] Target API level — Play requires a current one\n")
    return f"""<!-- {DO_NOT_EDIT} -->

# {'Apple App Store' if is_apple else 'Google Play'} — submission checklist

## Ready, and measured

{ready}
## Not ready, and why

{blocked}
## Measure your own captures before uploading

```bash
./.venv/bin/python 14_delivery/build.py --check-captures
```

Read-only. It reports each file's pixel size, whether it carries an alpha channel,
and whether it matches a size the store accepts. It writes nothing, and it is not
wired into CI, because the files it reads are ignored by git and usually absent —
a gate that cannot run is not a gate.
"""
