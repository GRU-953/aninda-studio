<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# Space and shape

One scale of ten steps, four radii, four target sizes. Everything in the system
sits on one of them.

**Licence:** PolyForm Noncommercial 1.0.0.

---

## Spacing — a 4 px scale in ten steps

| Token | px | CSS |
| --- | --- | --- |
| `dimension.space.0` | 4 | `--as-space-0` |
| `dimension.space.1` | 8 | `--as-space-1` |
| `dimension.space.2` | 12 | `--as-space-2` |
| `dimension.space.3` | 16 | `--as-space-3` |
| `dimension.space.4` | 24 | `--as-space-4` |
| `dimension.space.5` | 32 | `--as-space-5` |
| `dimension.space.6` | 48 | `--as-space-6` |
| `dimension.space.7` | 64 | `--as-space-7` |
| `dimension.space.8` | 96 | `--as-space-8` |
| `dimension.space.9` | 128 | `--as-space-9` |

Nothing in a design should use a spacing value that is not on this list. If a
gap needs 20 px, the answer is 16 px or 24 px, not a new token.

---

## Radii — four, and each has a job

| Token | px | Used on | CSS |
| --- | --- | --- | --- |
| `dimension.radius.badge` | 4 | badges, tags, small chips | `--as-radius-badge` |
| `dimension.radius.control` | 8 | buttons, inputs, selects | `--as-radius-control` |
| `dimension.radius.card` | 14 | cards, panels, dialogs | `--as-radius-card` |
| `dimension.radius.hero` | 24 | the web tile, hero surfaces | `--as-radius-hero` |

`radius.hero` is also where the icon tile's 24 % corner comes from. **Apple
publishes no app-icon corner radius.** That 24 % is this system's own number and
is not attributed to Apple.

---

## Target sizes — four figures, four different authorities

| Token | px | Where it comes from |
| --- | --- | --- |
| `dimension.target.min` | 24 | WCAG 2.2 AA, success criterion 2.5.8 Target Size (Minimum) |
| `dimension.target.apple-min` | 28 | Apple's stated minimum, 28×28 pt |
| `dimension.target.comfortable` | 44 | Apple's stated default, 44×44 pt |
| `dimension.target.android-min` | 48 | Android's minimum, 48 dp |

Use `comfortable` (44) unless something forces smaller. `min` (24) is a floor to
stay legal, not a target to design to.

---

## Focus

| Token | px | CSS |
| --- | --- | --- |
| `dimension.focus.ring-width` | 3 | `--as-focus-ring-width` |
| `dimension.focus.ring-offset` | 2 | `--as-focus-ring-offset` |

The ring is coloured `color.focus.ring`, which is `Highlight` in forced-colors
mode. Focus must be visible in all four themes and must not be **entirely**
obscured — WCAG 2.2 success criterion 2.4.11 Focus Not Obscured (Minimum) says
entirely, not partly.

---

## Grid

- Twelve stretched columns, gutter `space.4` (24 px), margin `space.5` (32 px).
- An 8 px square baseline grid, from `space.1`. Every spacing step is a multiple
  of it.

Cards in this system are designed at 1280 CSS px wide and measured at 360, 768
and 1280.

---

## Verified against

- WCAG 2.2, W3C Recommendation of 12 December 2024: 24×24 CSS px targets at AA.
- Apple Human Interface Guidelines: 44×44 pt default, 28×28 pt minimum.
- Material: 48 dp minimum.
- Checked 14 August 2026.
