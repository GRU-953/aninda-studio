<!-- GENERATED FILE. Written by 14_delivery/build.py. Do not hand-edit — the next build overwrites it. -->

# Apple App Store — submission checklist

## Ready, and measured

- [x] App icon, 1024 x 1024, square and unmasked, sRGB declared
- [x] Dark and Mono appearances authored
- [x] watchOS master at 1088 x 1088
- [x] Screenshot frames at 1290 x 2796 and 2064 x 2752
- [x] Name, subtitle, promotional text, description and keywords, within limits, in English

## Not ready, and why

- [ ] **Real screenshots.** Frames are templates. Guideline 2.3.3 refuses a screenshot that shows only title art or a splash screen.
- [ ] **An app.** There is nothing to submit yet.
- [ ] Privacy policy URL — required, and needs a live page
- [ ] Support URL — required, and must reach real contact details
- [ ] Age rating questionnaire — a form, not a file
- [ ] App previews — optional, 15 to 30 seconds

## Measure your own captures before uploading

```bash
./.venv/bin/python 14_delivery/build.py --check-captures
```

Read-only. It reports each file's pixel size, whether it carries an alpha channel,
and whether it matches a size the store accepts. It writes nothing, and it is not
wired into CI, because the files it reads are ignored by git and usually absent —
a gate that cannot run is not a gate.
