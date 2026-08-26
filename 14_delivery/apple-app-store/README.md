<!-- GENERATED FILE. Written by 14_delivery/build.py. Do not hand-edit — the next build overwrites it. -->

# Apple App Store — asset package

Written by `14_delivery/build.py` on the sources in `04_mark/svg/`. Every size here is a
published figure, and `MANIFEST.json` carries the page each one came from and the
date it was read.

**No app is published yet.** This package is complete as a set of assets and
incomplete as a submission, and `CHECKLIST.md` says which is which.

## What is in here

| File | Pixels | Bytes | What it is |
|---|---|---|---|
| `icon/icon-1024-dark.png` | 1024 x 1024 | 23,847 | Apple app icon, Dark appearance, 1024 x 1024 px.|
| `icon/icon-1024-mono.png` | 1024 x 1024 | 20,624 | Apple app icon, Mono appearance, 1024 x 1024 px.|
| `icon/icon-1024.png` | 1024 x 1024 | 26,475 | Apple app icon, Default appearance, 1024 x 1024 px.|
| `icon/icon-1088-watch.png` | 1088 x 1088 | 28,107 | Apple app icon, Default appearance, 1088 x 1088 px.|
| `screenshots/frames/ipad-13-2064x2752-01.png` | 2064 x 2752 | 270,451 | Screenshot frame 1 of 4, iPad 13 inch. A template.|
| `screenshots/frames/ipad-13-2064x2752-02.png` | 2064 x 2752 | 271,139 | Screenshot frame 2 of 4, iPad 13 inch. A template.|
| `screenshots/frames/ipad-13-2064x2752-03.png` | 2064 x 2752 | 270,766 | Screenshot frame 3 of 4, iPad 13 inch. A template.|
| `screenshots/frames/ipad-13-2064x2752-04.png` | 2064 x 2752 | 270,514 | Screenshot frame 4 of 4, iPad 13 inch. A template.|
| `screenshots/frames/iphone-6.9-1290x2796-01.png` | 1290 x 2796 | 152,397 | Screenshot frame 1 of 4, iPhone 6.9 inch. A template.|
| `screenshots/frames/iphone-6.9-1290x2796-02.png` | 1290 x 2796 | 152,504 | Screenshot frame 2 of 4, iPhone 6.9 inch. A template.|
| `screenshots/frames/iphone-6.9-1290x2796-03.png` | 1290 x 2796 | 152,751 | Screenshot frame 3 of 4, iPhone 6.9 inch. A template.|
| `screenshots/frames/iphone-6.9-1290x2796-04.png` | 1290 x 2796 | 152,513 | Screenshot frame 4 of 4, iPhone 6.9 inch. A template.|

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
2. Make the folder `14_delivery/_captures/apple/`. Git ignores it and this build never touches it,
   so nothing can overwrite or delete what you put there.
3. Take the screenshot on a device or simulator whose screen is that exact pixel
   size. App Store Connect accepts the capture only at a size it lists.
4. Save it into that folder, named `iphone-6.9-01.png`.
5. Repeat until you have four, each showing the app being used. Not the launch
   screen, not the sign-in page, not the logo.
6. Upload from `14_delivery/_captures/apple/`, never from `screenshots/frames/`.

> App Review Guideline 2.3.3: "Screenshots should show the app in use, and not merely the title art, login page, or splash screen."
>
> That is why these frames carry no mark. A frame showing only the logo resembles the thing the guideline rejects.


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
