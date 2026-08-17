<!-- Hand-written chapter. build.py reads this file; it never writes it. -->

**Plain international English, British spelling.** That is the rule in one line,
and it applies to every English word the studio ships: interface text, error
messages, documentation, this book, README files, the website, proposals and
invoices.

## Why those two things together

They sound as though they pull in opposite directions. They do not, because they
answer two different questions.

- **Vocabulary and sentence construction — international.** Written so a reader
  whose first language is not English understands it on one pass. That is the
  part that decides whether the writing works.
- **Spelling — British.** Bangladesh's education system and press use British
  spelling, so *colour*, *organise* and *centre* are what a Bangladeshi reader
  already expects. A spelling convention has to be picked, and picking the one
  both audiences already read is the sensible answer.

So `colour`, never `color`. But also never *whilst*, *amongst*, *sort out* or
*quid*.

## The standard being followed

**ISO 24495-1:2023 — Plain language, Part 1: Governing principles and
guidelines.** It is the international standard for plain language. In its own
terms, readers get what they need if the writing is **relevant**, **findable**,
**understandable** and **usable**.

## Sentences

- One idea per sentence. Around 15 to 20 words on average. Break anything over
  25.
- Active voice by default. *The build failed*, not *a failure was encountered*.
- Say who does what. A sentence with no subject usually needs one.
- Main point first, then the detail. A reader who stops after one sentence
  should still have the answer.

## Words

- The shortest word that is still precise. `use` not `utilise`, `about` not
  `approximately`, `start` not `commence`, `enough` not `sufficient`.
- **Precision beats plainness when they conflict.** If a technical term is the
  correct one, keep it and explain it in one sentence the first time it appears.
  *Contrast ratio* stays; it gets a definition.
- **No idioms and no phrasal verbs where a plain verb exists.** `cancel` not
  `call off`; `continue` not `carry on`. Idioms are the single largest cause of
  misreading for a reader whose first language is not English.
- **No metaphors from culture or sport.** No *ballpark*, no *touch base*, no
  *out of the box*.
- **No Latin abbreviations.** Write the words out.
- **Say the number and its unit.** 10 MB, 220 ms, 4.5:1. Never *a large file*
  where a figure is known.
- One name for one thing, everywhere. If it is the *mark*, it is never also the
  *logo* on the next page.

## Banned outright

{{data:banned-words}}

Every one of them tells a reader who is stuck that the problem is them. There
are no exceptions, and the build checks for them: if one of those words reaches
this book, the build fails and writes nothing. The list above is the only place
in the book where they appear, and it is marked in the markup so the check
skips it.

{{data:banned-latin}}

**No exclamation marks.** Warmth comes from the words, not from the punctuation.

## Tone, in four words and what each one means at the keyboard

**Cooperative** — write as if sitting beside the reader, not across a desk.
Offer the next step rather than stating the position. Use *you* and *I* in the
same sentence when it is a joint problem. When there is a choice, give the
recommendation and the reason, then leave the decision with them.

**Friendly** — warm, not chummy. Contractions where they fall naturally.
Thanks for a real thing, not as a reflex. No *Hi there*, no *Awesome*, no
*Happy to help*, no emoji.

**Approachable** — never make the reader feel they should already have known.
Explain the term the first time. Say plainly when something is genuinely
difficult; it is a relief to read. Invite the question.

**Professional** — **first person singular**. It is one person, so *I*, never
*we*. Using *we* to sound larger is the first small dishonesty a studio tells
about itself. Be accurate before being warm. Name a limit where it would
otherwise surprise someone — as information, not as a confession, and never
wrapped in an apology.

**When two of them pull against each other: accurate first, then clear, then
warm.** A sentence is never made friendlier at the cost of being right.

## Interface text

- **Buttons are a verb with its object.** *Save the entry*, not *Submit*, not
  *OK*. A button whose label does not say what will happen is a trap.
- **Errors say what happened, then what happens next.** Never *Error 500*, and
  never blame the reader.
- **Empty states say what to do.**
- Sentence case for everything — headings, buttons, labels.
- Never rely on colour alone. Every state carries a word and a glyph as well.

## The four interface strings, in both languages

These are the reference strings the whole system is written against. The Bangla
is not a translation of the English; each was written in its own language and
then checked against the Bangla Academy rules.

{{data:voice-strings}}

## What this does not mean

- **Not dumbed down.** Plain language is about being understood, not about
  having less to say.
- **Not shorter at any cost.** A sentence that saves three words and costs a
  re-read is a bad trade.
- **Not the same as the Bangla.** The Bangla is written as Bangla. Where the two
  must agree exactly — a number, a licence name, a file name — they agree.
  Everywhere else they are written independently.
