<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# Motion

Two durations, three curves, and one rule that overrides all of them.

**Licence:** PolyForm Noncommercial 1.0.0.

---

## The rule that overrides everything

Honour `prefers-reduced-motion: reduce`. When it is set, remove movement — do not
merely shorten it. A colour change may stay; a slide, a scale, a spin or a
parallax must not.

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
  }
}
```

An animation that flashes more than three times a second is a seizure risk and is
forbidden outright — WCAG 2.2 success criterion 2.3.1 Three Flashes or Below
Threshold, at level A.

---

## The two durations

| Token | Value | For |
| --- | --- | --- |
| `duration.motion.colour` | 120 ms | anything that only changes colour: hover, a state change, a badge appearing |
| `duration.motion.move` | 220 ms | anything that changes position or size: a panel sliding, a dialog opening |

CSS: `--as-duration-colour`, `--as-duration-move`.

Two is the whole set. A third duration means a decision nobody wrote down.

---

## The three curves

| Token | cubic-bezier | For |
| --- | --- | --- |
| `cubicBezier.motion.standard` | 0.2, 0.0, 0.0, 1.0 | movement within a view |
| `cubicBezier.motion.enter` | 0.05, 0.7, 0.1, 1.0 | something arriving |
| `cubicBezier.motion.exit` | 0.3, 0.0, 0.8, 0.15 | something leaving |

CSS: `--as-ease-standard`, `--as-ease-enter`, `--as-ease-exit`.

Enter is slow to start and fast to finish, so an arrival feels settled. Exit is
the reverse, so a dismissal feels decided.

---

## What no platform gives you

**Apple publishes no motion durations and no easing curves.** Any such number
attributed to Apple is invented. The three curves above are this system's own.

**Material does still publish duration and easing tokens**, and its spring
guidance is worth knowing if you are working in Compose: **spatial** springs are
underdamped, damping 0.6 to 0.8, and they overshoot on purpose; **effects**
springs are critically damped at exactly 1.0, and never overshoot. M3 Expressive
is the current direction but is **not fully stable in code** — stable Compose
`material3` is 1.4.0 and much of Expressive is still 1.5.0-alpha.

---

## Verified against

- WCAG 2.2, W3C Recommendation of 12 December 2024.
- Apple Human Interface Guidelines and Material 3, both checked 14 August 2026.
