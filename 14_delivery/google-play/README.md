<!-- GENERATED FILE. Written by 14_delivery/build.py. Do not hand-edit — the next build overwrites it. -->

# Google Play — asset package

Written by `14_delivery/build.py` on the sources in `04_mark/svg/`. Every size here is a
published figure, and `MANIFEST.json` carries the page each one came from and the
date it was read.

**No app is published yet.** This package is complete as a set of assets and
incomplete as a submission, and `CHECKLIST.md` says which is which.

## What is in here

| File | Pixels | Bytes | What it is |
|---|---|---|---|
| `app-res/mipmap-hdpi/ic_launcher_background.png` | 162 x 162 | 474 | Android adaptive icon background layer at hdpi, 162 px for a 108 dp canvas.|
| `app-res/mipmap-hdpi/ic_launcher_foreground.png` | 162 x 162 | 1,825 | Android adaptive icon foreground layer at hdpi, 162 px for a 108 dp canvas.|
| `app-res/mipmap-hdpi/ic_launcher_monochrome.png` | 162 x 162 | 1,825 | Android adaptive icon monochrome layer at hdpi, 162 px for a 108 dp canvas.|
| `app-res/mipmap-mdpi/ic_launcher_background.png` | 108 x 108 | 366 | Android adaptive icon background layer at mdpi, 108 px for a 108 dp canvas.|
| `app-res/mipmap-mdpi/ic_launcher_foreground.png` | 108 x 108 | 1,249 | Android adaptive icon foreground layer at mdpi, 108 px for a 108 dp canvas.|
| `app-res/mipmap-mdpi/ic_launcher_monochrome.png` | 108 x 108 | 1,249 | Android adaptive icon monochrome layer at mdpi, 108 px for a 108 dp canvas.|
| `app-res/mipmap-xhdpi/ic_launcher_background.png` | 216 x 216 | 618 | Android adaptive icon background layer at xhdpi, 216 px for a 108 dp canvas.|
| `app-res/mipmap-xhdpi/ic_launcher_foreground.png` | 216 x 216 | 2,482 | Android adaptive icon foreground layer at xhdpi, 216 px for a 108 dp canvas.|
| `app-res/mipmap-xhdpi/ic_launcher_monochrome.png` | 216 x 216 | 2,482 | Android adaptive icon monochrome layer at xhdpi, 216 px for a 108 dp canvas.|
| `app-res/mipmap-xxhdpi/ic_launcher_background.png` | 324 x 324 | 912 | Android adaptive icon background layer at xxhdpi, 324 px for a 108 dp canvas.|
| `app-res/mipmap-xxhdpi/ic_launcher_foreground.png` | 324 x 324 | 4,070 | Android adaptive icon foreground layer at xxhdpi, 324 px for a 108 dp canvas.|
| `app-res/mipmap-xxhdpi/ic_launcher_monochrome.png` | 324 x 324 | 4,070 | Android adaptive icon monochrome layer at xxhdpi, 324 px for a 108 dp canvas.|
| `app-res/mipmap-xxxhdpi/ic_launcher_background.png` | 432 x 432 | 1,325 | Android adaptive icon background layer at xxxhdpi, 432 px for a 108 dp canvas.|
| `app-res/mipmap-xxxhdpi/ic_launcher_foreground.png` | 432 x 432 | 5,713 | Android adaptive icon foreground layer at xxxhdpi, 432 px for a 108 dp canvas.|
| `app-res/mipmap-xxxhdpi/ic_launcher_monochrome.png` | 432 x 432 | 5,713 | Android adaptive icon monochrome layer at xxxhdpi, 432 px for a 108 dp canvas.|
| `store-listing/feature-graphic-1024x500.png` | 1024 x 500 | 29,329 | Google Play feature graphic. Mandatory to publish a listing.|
| `store-listing/icon-512.png` | 512 x 512 | 13,037 | Google Play store icon. Full square; Play applies its own 30 per cent corner mask and its own drop shadow.|
| `store-listing/screenshots/frames/phone-1080x1920-01.png` | 1080 x 1920 | 110,359 | Screenshot frame 1 of 4, Android phone. A template.|
| `store-listing/screenshots/frames/phone-1080x1920-02.png` | 1080 x 1920 | 110,539 | Screenshot frame 2 of 4, Android phone. A template.|
| `store-listing/screenshots/frames/phone-1080x1920-03.png` | 1080 x 1920 | 110,512 | Screenshot frame 3 of 4, Android phone. A template.|
| `store-listing/screenshots/frames/phone-1080x1920-04.png` | 1080 x 1920 | 110,204 | Screenshot frame 4 of 4, Android phone. A template.|

## The text

`metadata/metadata.json` holds every field with its published limit and both
counts — code points and UTF-8 bytes — because neither store says which unit it
counts. `metadata/metadata.md` is the same text laid out for copying.

Metadata is supplied in English and Bangla. Apple added Bangla to its metadata languages on
30 March 2026 and names it "Bangla", which is this studio's own term.

## Replacing the screenshot frames

The frames in `screenshots/frames/` are templates. They are generated and gated,
so overwriting one turns `--check` red. Nothing below asks you to overwrite them.

1. Open one frame and read the size printed on it.
2. Make the folder `14_delivery/_captures/google/`. Git ignores it and this build never touches it,
   so nothing can overwrite or delete what you put there.
3. Take the screenshot on a device or simulator whose screen is that exact pixel
   size. Google accepts a range: shortest side at least 320 px, longest at most 3840, and the longest no more than twice the shortest.
4. Save it into that folder, named `phone-01.png`.
5. Repeat until you have four, each showing the app being used. Not the launch
   screen, not the sign-in page, not the logo.
6. Upload from `14_delivery/_captures/google/`, never from `screenshots/frames/`.

> Google requires a minimum of two screenshots across device types to publish a listing, and recommends at least four at 1080 px or more.


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
