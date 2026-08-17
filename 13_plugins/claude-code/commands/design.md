---
description: Design or build something new to the Aninda Studio system — a page, a component, an interface, a document — using the right tokens, type, spacing, motion, voice and Bangla rules.
argument-hint: "[what to design, for example: a sign-in page, a pricing table, an error state]"
disable-model-invocation: true
---

<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->

Design or build something new, to the Aninda Studio system.

Use the `aninda-brand` skill. It carries the colour, typography, layout, logo,
icons, motion, voice, Bangla, licence and naming rules, and the token files
themselves.

What the user asked for: `$ARGUMENTS`

Do this:

1. Read `skills/aninda-brand/SKILL.md`, then the reference files it points you
   at for this particular job. Do not read all ten every time.
2. Use `assets/css/tokens.css` custom properties. Never write a raw hex, a raw
   pixel value, or a raw duration.
3. Write every English word to `references/voice.md`. The words *simply*,
   *just*, *easy*, *obviously*, *of course* and *clearly* are banned, and so are
   exclamation marks.
4. For Bangla, use only a string listed in `references/bangla.md` as verified.
   If none fits, say so and leave the English in place. Do not write new Bangla.
5. Check what you made with the `aninda-review` skill before you hand it over.

If the user wants one asset file rather than a design, use the `aninda-brand`
skill's `scripts/asset.py` through `/aninda-studio:asset`. If they want a whole
repository set up, use `aninda-repo`.
