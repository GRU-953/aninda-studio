<!-- GENERATED FILE. Written by 14_delivery/build.py. Do not hand-edit — the next build overwrites it. -->

# Google Play — submission checklist

## Ready, and measured

- [x] Store icon, 512 x 512, full square, sRGB declared, under 1024 KB
- [x] Feature graphic, 1024 x 500, no alpha
- [x] Adaptive icon layers at five densities, plus ic_launcher.xml
- [x] Monochrome layer for themed icons
- [x] Screenshot frames at 1080 x 1920
- [x] Title, short description and full description, within limits, in English

## Not ready, and why

- [ ] **Real screenshots.** Frames are templates. At least two are mandatory to publish.
- [ ] **An app.** There is nothing to submit yet.
- [ ] Privacy policy URL — required
- [ ] Data safety form — a form, not a file
- [ ] Content rating questionnaire — a form, not a file
- [ ] Target API level — Play requires a current one

## Measure your own captures before uploading

```bash
./.venv/bin/python 14_delivery/build.py --check-captures
```

Read-only. It reports each file's pixel size, whether it carries an alpha channel,
and whether it matches a size the store accepts. It writes nothing, and it is not
wired into CI, because the files it reads are ignored by git and usually absent —
a gate that cannot run is not a gate.
