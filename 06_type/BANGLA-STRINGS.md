# Aninda Studio — the Bangla strings

**Written:** 14 August 2026
**Scope:** The Bangla that `06_type/BANGLA-STANDARD.md` did not yet cover — 30 component-library
card names and subtitles, the 14 guidebook chapter titles, the two high-contrast theme labels,
and the shared interface strings the website and plugins need.
**Governing document:** `06_type/BANGLA-STANDARD.md`. Nothing here contradicts it. Every string it
already verified is reused unchanged and marked as such.
**Tone:** `02_strategy/ENGLISH-STANDARD.md` — cooperative, friendly, approachable, professional —
carried in Bangla's own idiom, not translated across.

**Counts:** 94 keys in total. **77 are new**; 17 are verified strings from `BANGLA-STANDARD.md`,
reused unchanged and repeated here so a build script can read one file rather than two.

---

## How these were written

**Not translated.** `ENGLISH-STANDARD.md` says it plainly: *"The Bangla is written as Bangla, not
translated from this. Same meaning, same steps, different sentences."* So `Empty state` is
**যখন কিছু নেই**, not a calque of "empty" and "state"; `Skip to next content` is
**সরাসরি মূল অংশে যান**, because a Bangla skip link says where it takes you rather than what it
avoids.

**Subtitles are phrases, not sentences.** None carries a closing দাঁড়ি. Where the English subtitle
is two sentences, the Bangla joins them with an em dash — a genuine Bangla যতিচিহ্ন, per
`BANGLA-STANDARD.md` Part 3, not an English import.

**Numbers.** Counts up to ten are written as words (চারটি, দশ ধাপে); anything larger, and every
measurement, uses Bengali numerals (১৭টি, ৪ পিক্সেল, ২৪ পিক্সেল). That follows house rule 9, and
the Academy's own practice of using Bengali numerals for measurements.

**Latin kept only where it must be.** `currentColor`, `aria-selected`, `aria-current`, `OK` and
`Aninda Mono` stay in Latin script — code tokens copied literally, a literal button label being
argued against, and a product name that must stay recognisable. House guidance 2 and 3.

**One name for one thing**, across both languages. **চিহ্ন** is the brand mark and nothing else, so
icons take **আইকন** and a glyph inside a component takes **প্রতীক**. **পথরেখা** and **নেভিগেশন** mean
the same thing on the breadcrumb card and the docs-page card. **যে কাজ আর ফেরানো যায় না** is the
one phrase for a destructive action, on both the dialog and the settings card.

---

## 1. The loanword-versus-native decisions

Rule ২.৬ licenses any loanword genuinely current in Bangla — *"বাংলায় প্রচলিত বিদেশি শব্দ সাধারণভাবে
বাংলা ভাষার ধ্বনিপদ্ধতি-অনুযায়ী লিখতে হবে"* — and `BANGLA-STANDARD.md` §6 shows the Academy itself
admitting কপি, ফাইল, সফটওয়্যার and মেগাবাইট to its dictionary. So the test applied to every
component name was not *is there a Bangla word?* but **which word does a Bangladeshi actually use,
and does it say the right thing?**

**Loanword taken** — because it is what a Bangladeshi developer says, and no native word is in real
use for that control:

| | |
|---|---|
| বাটন · ইনপুট · ট্যাব · ডায়ালগ · টেবিল | The five the brief named. All rule ২.৬. |
| চেকবক্স ও রেডিও · ব্যাজ · কার্ড · ড্যাশবোর্ড · সেটিংস · নেভিগেশন · টোস্ট · মেনু | No native word is genuinely used. Coining one would be exactly the Sanskritised substitution `BANGLA-STANDARD.md` rejected at th-3. |
| কোড ব্লক | কোড already appears in the verified bt-1…bt-5 set. |
| প্যাকেজ | The word Bangladeshi users meet for a priced tier (ইন্টারনেট প্যাকেজ). পরিকল্পনা would mean a scheme. |
| লাইসেন্স · ট্রেডমার্ক | Both are Academy dictionary headwords (p. 1201, p. 558), and ট্রেডমার্ক is the term in Bangladesh's own statute, ট্রেডমার্ক আইন, ২০০৯. |
| আইকন | চিহ্ন is taken by the brand mark. |

**Native word taken** — because a plain Bangla word exists, is genuinely used, and says the thing
more plainly than the loanword would:

| | |
|---|---|
| বার্তা (alert) | The card holds four kinds, including success and information. সতর্কবার্তা means *warning* and would be wrong for three of the four. |
| তালিকা (in table, form and dashboard subtitles) | Ordinary and unambiguous; লিস্ট adds nothing. |
| যাচাইসহ ফর্ম | ফর্ম is native-by-adoption and universal; যাচাই is plainer than ভ্যালিডেশন. |
| লেখার ঘর (textarea) · বাছাই তালিকা (select) | Both built from ordinary words, and both say what the control does to a reader who is not a developer. |
| প্রবেশ (sign in) | প্রবেশ করুন is already what Bangla sites say. |
| দাম (pricing) | The plainest word there is. মূল্যতালিকা is shopfront formal. |
| প্রথম পাতা (landing) · নির্দেশিকার পাতা (docs) · পথরেখা (breadcrumb) · যখন কিছু নেই (empty state) · পাতা পাওয়া যায়নি (not found) | Written as Bangla titles rather than transliterated English ones. নির্দেশিকা is a dictionary headword, p. 746. |
| খাড়া · আড়াআড়ি | In place of উল্লম্ব and অনুভূমিক, which are the textbook register, not the spoken one. |

**The one place neither answer is comfortable: `Accessibility`.** There is no plain, everyday
Bangla word for it. অভিগম্যতা and প্রবেশগম্যতা are both modern coinages and neither is an Academy
dictionary headword — I checked both on 14 August 2026 and both return *শব্দটি খুঁজে পাওয়া যায়নি*.
I have shipped **অভিগম্যতা** on Bangladeshi institutional usage: the government's own accessibility
project is branded **অভিগম্য অভিধান** at `accessibledictionary.gov.bd`. A card in an index has to be
unambiguous before it is warm — the brand's own order is accuracy, then clarity, then warmth — and a
plainer title like *সবার জন্য* would leave a designer guessing which card this is. See open
question 1.

---

## 2. The cards

All 30 names and subtitles are in the table at the end, with the rule number or dictionary page for
anything disputable. Five names are the verified strings reused unchanged, exactly as instructed:
**রং** (gb-4), **হরফ** (gb-5), **ফাঁক ও আকার** (gb-6), **গতি** (gb-8), **চিহ্ন** (gb-3). All 30
subtitles are new.

Points worth checking in review:

- **তির** (arrow, on the select card) takes short ই-কার, per rule ২.১ on অতৎসম words. It is a
  dictionary headword at p. 604. **তীর** with দীর্ঘ ঈ-কার is the তৎসম word for a riverbank — a
  different word. Newspapers often print তীর for both; the Academy form is তির.
- **রিঙের** (focus ring, on the accessibility card) takes ঙ, not ং, because a vowel follows —
  rule ২.৪, the same pattern as রঙের. Standing alone it would be রিং.
- **কোণ** (corner, on the space-and-shape card) keeps মূর্ধন্য ণ as a তৎসম word under ণ-ত্ব বিধান.
  It is not the same word as কোন (which) or কোনো (any).
- **ছোটো** on the toast card and **মতো** on the docs-page card are both named in rule ২.৩'s own
  example list.
- **কখনো** appears four times, always with ও-কার; **আরও** appears once (`ui.read-more`) with its
  full ও. That asymmetry is the Academy's, and is house rule 1.

---

## 3. The guidebook chapters

**One correction to the brief, in your favour: ten of the fourteen were already settled, not six.**
The brief named five (রং, হরফ, ফাঁক ও আকার, গতি, চিহ্ন) plus যা এই পদ্ধতি করে না. The verified table
in `BANGLA-STANDARD.md` also holds gb-1 **স্বাগতম** (Welcome), gb-2 **নাম** (The name),
gb-7 **উপাদান** (Components) and gb-9 **কণ্ঠস্বর** (Voice). Those four are reused unchanged rather
than rewritten, so only four chapter titles were genuinely missing:

**আইকন** (Icons) · **বাংলায় লেখা** (Writing in Bangla) · **কাজে লাগানো** (Applying it) ·
**লাইসেন্স ও ট্রেডমার্ক** (Licence and trademarks).

**কাজে লাগানো** rather than প্রয়োগ: প্রয়োগ is correct, but it is the register of a manual.
কাজে লাগানো is what a person says, and it matches the বানাই / লুকিয়ে রাখা হবে না benchmark set by
the approved voice sample vc-1.

**বাংলায় লেখা** keeps অনুস্বার in বাংলা — rule ২.৪ names that word specifically:
*"বাংলা ও বাংলাদেশ শব্দে অনুস্বার থাকবে।"*

---

## 4. The two high-contrast themes

The component library's English labels are `High contrast, light` and `High contrast, dark`, with a
comma. The Bangla joins the approved **বেশি কনট্রাস্ট** (th-3) to the approved **আলো** (th-1) and
**অন্ধকার** (th-2) with the same comma:

- **বেশি কনট্রাস্ট, আলো**
- **বেশি কনট্রাস্ট, অন্ধকার**

The comma is ordinary Western punctuation and is standard in Bangla — W3C's Bengali orthography
notes record that commas, semicolons and colons are all used commonly. No new vocabulary is
introduced; these are two verified strings joined, which is why they are safe to ship without a
fresh ruling.

---

## 5. Shared interface strings

Sixteen strings, in the table below: the twelve named in the brief plus the four status words.

Three deserve a note.

**`ui.language` is identical in both languages: `English / বাংলা`.** It is not translated, because
a language switcher has to be legible to someone who cannot yet read the page. Each half is written
in its own script so either reader can find their own.

**`status.error` is সমস্যা, not ত্রুটি.** The brand rule is that an error message never blames the
reader. সমস্যা names the situation; ত্রুটি names a fault. This is a judgement call and it is listed
as open question 3. Note that **ভুল** is still the right word for a wrong entry in a specific form
field, which is how it is used in the form-with-validation subtitle.

**`ui.read-more` is আরও পড়ুন**, with the full ও — the single most likely place for this system to
be "corrected" wrongly into আরো পড়ুন or আরও's ও-কার form. The Academy dictionary calls আরও
*আরো-র সংগততর বানান* (p. 164). It does not follow the এখনো pattern.

---

## 6. Open questions

Each of these shipped with my recommendation. The alternative is real, and the decision is yours.

1. **`Accessibility` — shipped অভিগম্যতা.** Alternatives: **প্রবেশগম্যতা**, which is commoner in
   Bengali Wikipedia and West Bengal usage, or **সবার জন্য**, which is plainer and warmer but does
   not identify the card. Neither অভিগম্যতা nor প্রবেশগম্যতা is a dictionary headword. I chose the
   one with Bangladeshi institutional backing.
2. **`Toast` — shipped টোস্ট.** In Bangla script it reads as the bread first and the notification
   second. The plain alternative is **ভেসে ওঠা বার্তা** — transparent, but longer, and it weakens
   the distinction from the alert card, which is বার্তা.
3. **`Error` — shipped সমস্যা.** **ত্রুটি** is the more conventional Bangla interface word and a
   Bangladeshi user will have met it more often. সমস্যা is the blame-free one.
4. **`Button` — shipped বাটন**, as the brief specified. Worth knowing that **বোতাম** is an Academy
   dictionary headword (p. 1018) and is what several Bangla software localisations use. If you ever
   want the library to read as fully Bangla, বোতাম is the defensible switch.
5. **`Table` — shipped টেবিল**, as the brief specified. **সারণি** is the word Bangladeshi
   schoolbooks use, and would be the choice if the audience were readers rather than developers.
6. **`Breadcrumb` — shipped পথরেখা.** It is built from two ordinary words but is not itself a
   dictionary headword. **ব্রেডক্রাম্ব** is what developers say, and carries no meaning at all in
   Bangla.

**Marked unverified**, in the same spirit as `BANGLA-STANDARD.md`:

- **পিক্সেল, প্যাকেজ, থিম, ইজিং, ফোকাস, স্কেল, ব্লক, লিংক, নেভিগেশন, ড্যাশবোর্ড, সেটিংস, টোস্ট,
  ব্যাজ, আইকন, চেকবক্স, রেডিও, ডায়ালগ, বাটন, ইনপুট** — none is an Academy dictionary headword.
  All are licensed by rule ২.৬ as প্রচলিত loanwords, the same footing on which
  `BANGLA-STANDARD.md` accepted কনট্রাস্ট. Spot-checked on the Academy dictionary on
  14 August 2026: পিক্সেল and প্যাকেজ both return *শব্দটি খুঁজে পাওয়া যায়নি*.
- **লিংক** is written with অনুস্বার by analogy with the Academy's own ইংরেজি. Rule ২.৪ covers
  word-final position and the pre-vowel case, not this one. **Convention, not a citation.**
- **অভিগম্যতা** — the Bangladeshi government's `accessibledictionary.gov.bd` uses অভিগম্য as a
  brand name, which is usage evidence, not a lexicographic ruling.
- **তির** is confirmed as a headword at p. 604, but the dictionary site serves that page as a scanned
  image, so I could not read the entry's own wording. The spelling rests on rule ২.১ plus the
  headword's existence.

---

## 7. The table

`key | english | bangla | basis`. This is generated from `06_type/bangla-strings.json`, which holds
the same 94 entries as `{key: {"en", "bn", "basis"}}` for build scripts to read directly.

| key | english | bangla | basis |
|---|---|---|---|
| `card.colour.name` | Colour | রং | Verified string gb-4, BANGLA-STANDARD.md. Rule ২.৪ names রং in its own example list; রং is the dictionary headword (p. 1156), রঙ has no entry. |
| `card.colour.subtitle` | Every colour role across four themes, each with the contrast ratio it was measured at and the criterion it was measured against, over the seven surfaces they are measured against. | চার থিমে প্রতিটি রঙের ভূমিকা — প্রতিটির মাপা কনট্রাস্ট অনুপাত আর কোন মানদণ্ডে মাপা হয়েছে | কনট্রাস্ট reused from verified th-3; loanword licensed by rule ২.৬. কোন = which (interrogative), correct per the dictionary entry at p. 337. থিম is a ২.৬ loanword, not a dictionary headword. Bengali numeral ১৭ per house rule 9. REVISED 19 Aug 2026: the numeral ১৭ removed, no word changed. It counted ten measured roles plus seven surfaces, but the seven surfaces carry no ratio and no criterion, so the sentence claimed a measurement for seven values that have none — and the count changed again when a proven fill role was added. A count that must stay true is derived or absent, never typed. Pending confirmation by the Bangla reviewer. |
| `card.typography.name` | Typography | হরফ | Verified string gb-5, BANGLA-STANDARD.md. Dictionary headword; plainer than টাইপোগ্রাফি or অক্ষরবিন্যাস. |
| `card.typography.subtitle` | One scale of a perfect fourth, two scripts, a measured multiplier for Bangla and a floor it never goes below. | পারফেক্ট ফোর্থ অনুপাতে একটি স্কেল, দুই লিপি, বাংলার জন্য মেপে নেওয়া গুণক আর যে মাপের নিচে হরফ কখনো নামে না | কখনো with ও-কার per BANGLA-STANDARD.md house rule 1 (dictionary headword; কখনও is not). নিচ with short ই-কার per rule ২.১ (অতৎসম). লিপি and গুণক are plain dictionary words; পারফেক্ট ফোর্থ is the interval's name, a ২.৬ loanword. |
| `card.space-and-shape.name` | Space and shape | ফাঁক ও আকার | Verified string gb-6, BANGLA-STANDARD.md. চন্দ্রবিন্দু on ফাঁক is lexical; the Academy has no rule on it. |
| `card.space-and-shape.subtitle` | A 4 px scale in ten steps, and four radii. Everything in the system sits on one of them. | দশ ধাপে ৪ পিক্সেলের একটি স্কেল আর চার রকম কোণের বাঁক — পদ্ধতির সবকিছু এর কোনো একটির উপর বসে | কোনো = any/some per rule ২.৩ and the dictionary (p. 338). কোণ (corner) keeps ণ as a তৎসম under ণ-ত্ব বিধান — distinct from কোন/কোনো. পদ্ধতি reused from verified gb-10. পিক্সেল is a ২.৬ loanword; checked 14 Aug 2026, not a dictionary headword. |
| `card.motion.name` | Motion | গতি | Verified string gb-8, BANGLA-STANDARD.md. |
| `card.motion.subtitle` | Two durations and three easing curves. Things that move may overshoot; things that only change colour never do. | দুটি সময়কাল আর তিনটি ইজিং বাঁক — যা নড়ে তা একটু বেশি এগিয়ে ফিরে আসতে পারে, যার শুধু রং বদলায় তা কখনো নয় | রং standing alone takes অনুস্বার per rule ২.৪. কখনো per house rule 1. বাঁক is the plain native word for a curve; ইজিং is a ২.৬ loanword with no native equivalent in real use. |
| `card.the-marks.name` | The marks | চিহ্ন | Verified string gb-3, BANGLA-STANDARD.md. চিহ্ন is reserved for the brand marks throughout, so icons take আইকন — one name for one thing. |
| `card.the-marks.subtitle` | The mark in two weights, drawn in currentColor so it takes whatever theme it lands in. | চিহ্ন দুই ওজনে — currentColor দিয়ে আঁকা, তাই যে থিমে বসে সেই থিমের রং নিয়ে নেয় | মোহনা reused from verified col-1 (Estuary). currentColor stays Latin: a code token copied literally, per BANGLA-STANDARD.md house guidance 3. REVISED 19 Aug 2026: 'Estuary'/মোহনা removed. That name belongs to the ground colour ramp — it is the ramp's description in primitive.tokens.json and what colour.md calls it — and it was also being used for the mark, whose own files and chapter call it only 'the mark'. naming.md opens 'One name for one thing, everywhere.' Pending confirmation by the Bangla reviewer. |
| `card.accessibility.name` | Accessibility | অভিগম্যতা | Not a dictionary headword (checked 14 Aug 2026). Chosen on Bangladeshi institutional usage: the government's own accessibility project is branded অভিগম্য অভিধান — accessibledictionary.gov.bd. See open question 1. |
| `card.accessibility.subtitle` | Target sizes with the guidance each one comes from, the anatomy of the focus ring, and what happens in forced colours — the mode where the operating system replaces every colour with its own. | ছোঁয়ার জায়গার মাপ আর তার নির্দেশনার উৎস, ফোকাস রিঙের গড়ন, আর ফোর্সড কালার্স মোডে কী হয় — যেখানে অপারেটিং সিস্টেম নিজের রং বসিয়ে সব রং বদলে দেয় | রিঙের takes ঙ because a vowel follows, per rule ২.৪ (cf. রঙের). কী = what, দীর্ঘ ঈ-কার per rule ৩.১. ছোঁয়ার জায়গা is plain and physical, in place of the stiff লক্ষ্যবস্তুর আকার. |
| `card.button.name` | Button | বাটন | Rule ২.৬ loanword, and what a Bangladeshi developer says. বোতাম is a dictionary headword (p. 1018) and is used in some Bangla localisations — see open question 4. |
| `card.button.subtitle` | Four kinds, two sizes and an icon-only form, each with a label that says what will happen. | চার রকম, দুই মাপ আর শুধু আইকনের একটি রূপ — প্রতিটির লেখা বলে দেয় কী ঘটবে | কী = what per rule ৩.১. আইকন rather than চিহ্ন, which is reserved for the brand marks (gb-3). লেখা for label keeps the same word the verified strings use (bt-1, ms-1). |
| `card.input.name` | Input | ইনপুট | Rule ২.৬ loanword; the word Bangladeshi developers use for the element. No native word is in real use for it. |
| `card.input.subtitle` | A label, an optional hint, and an error that says what happened and then what to do next. | ঘরের নাম, দরকারে একটি ইঙ্গিত, আর ভুল হলে যে বার্তা বলে কী হয়েছে আর তারপর কী করতে হবে | ইঙ্গিত and বার্তা are plain dictionary words, preferred over হিন্ট and মেসেজ. কী = what per rule ৩.১. ঘর for a form field is the ordinary Bangla word. |
| `card.select.name` | Select | বাছাই তালিকা | Both words are ordinary Bangla (বাছাই, তালিকা) and say what the control does. Preferred over সিলেক্ট for a card title a non-developer also reads. |
| `card.select.subtitle` | A native select with a drawn arrow, so the arrow follows the theme instead of the operating system. | ব্রাউজারের নিজের সিলেক্ট, তিরটি আঁকা — তাই তির অপারেটিং সিস্টেমের নয়, থিমের রং নেয় | তির (arrow) takes short ই-কার per rule ২.১ as an অতৎসম word, and is a dictionary headword (p. 604); তীর with দীর্ঘ ঈ is the তৎসম word for a riverbank. সিলেক্ট names the HTML element here, so the loanword is the precise term. |
| `card.checkbox-radio.name` | Checkbox and radio | চেকবক্স ও রেডিও | Rule ২.৬ loanwords; no native equivalents are in real use. চেক follows rule ২.১০ — no hasanta (the rules list চেক by name). |
| `card.checkbox-radio.subtitle` | Native controls at 24 px, wrapped in a label so the words are part of the target. | ব্রাউজারের নিজের চেকবক্স ও রেডিও, ২৪ পিক্সেল মাপে — লেখাটিও সঙ্গে জোড়া, তাই লেখায় ছুঁলেও কাজ হয় | Bengali numeral ২৪ per house rule 9 (measurement in prose). Says the consequence in plain terms rather than translating "part of the target". |
| `card.textarea.name` | Textarea | লেখার ঘর | Two ordinary words, and it says exactly what the control is. Keeps লেখা, the noun the verified strings already use for a user's entry (bt-1, ms-1, ms-3). |
| `card.textarea.subtitle` | You can drag it taller but never wider, so the line length stays comfortable to read. | টেনে লম্বা করা যায়, চওড়া নয় — তাই লাইনের মাপ পড়ার মতো আরামেই থাকে | নিশ্চয়ার্থক ই attached in full in আরামেই, per rule ৩.৫ (আজই, এখনই). Plain চলিত throughout per rule ৫ and §৭ of BANGLA-STANDARD.md. |
| `card.badge.name` | Badge | ব্যাজ | Rule ২.৬ loanword, and the word used for a UI badge. তকমা is the native word but carries a faintly pejorative sense in Bangladeshi usage. |
| `card.badge.subtitle` | Five meanings, each carrying a glyph and a word so the colour is the third signal and never the only one. | পাঁচটি অর্থ, প্রতিটির সঙ্গে একটি প্রতীক ও একটি শব্দ — রং এখানে তৃতীয় সংকেত, কখনো একমাত্র নয় | প্রতীক for glyph, keeping চিহ্ন free for the brand marks. রং word-final takes অনুস্বার per rule ২.৪. কখনো per house rule 1. |
| `card.card.name` | Card | কার্ড | Rule ২.৬ loanword; universal in Bangladeshi usage and unambiguous. তাস means a playing card and would mislead. |
| `card.card.subtitle` | A surface a step brighter than the page, with a shadow in the light theme and none in the dark ones. | পাতার চেয়ে এক ধাপ উজ্জ্বল একটি তল — আলো থিমে ছায়া পড়ে, অন্ধকার থিমে পড়ে না | আলো and অন্ধকার reused from verified th-1 and th-2. |
| `card.alert.name` | Alert | বার্তা | Plain native word, and accurate: the card holds four kinds including success and information, so সতর্কবার্তা (warning) would be wrong for three of them. |
| `card.alert.subtitle` | Four kinds. Each says what happened, then what happens next, and never blames the reader. | চার রকম — প্রতিটি বলে কী হয়েছে, তারপর কী হবে, আর কখনো পাঠককে দোষ দেয় না | কী = what per rule ৩.১; কখনো per house rule 1. Matches the verified ms-1, which states the position and then the next step without blame. |
| `card.dialog.name` | Dialog | ডায়ালগ | Rule ২.৬ loanword, and the name of the HTML element. সংলাপ means a conversation and would not be understood as this control. |
| `card.dialog.subtitle` | A real dialog element over a dimmed backdrop, with the destructive action named rather than called OK. | ব্রাউজারের নিজের ডায়ালগ উপাদান, পিছনে আবছা পর্দা — যে কাজ আর ফেরানো যায় না তার নাম লেখা থাকে, শুধু OK নয় | উপাদান reused from verified gb-7 (components). "যে কাজ আর ফেরানো যায় না" carries "destructive" in plain words instead of ধ্বংসাত্মক. OK stays Latin: it is the literal button label being argued against. |
| `card.table.name` | Table | টেবিল | Rule ২.৬ loanword, and what Bangladeshi developers say. সারণি is the school-textbook word — see open question 5. |
| `card.table.subtitle` | Row headers, a caption saying what the numbers are, and a sideways scroll when the table is wider than the space. | সারির শিরোনাম, সংখ্যাগুলো কীসের তা বলা এক লাইনের পরিচয়, আর জায়গার চেয়ে চওড়া হলে পাশে সরিয়ে দেখা | সারি, শিরোনাম and পরিচয় are plain dictionary words; "পাশে সরিয়ে দেখা" avoids the loanword স্ক্রল where a native phrase reads naturally. |
| `card.tabs.name` | Tabs | ট্যাব | Rule ২.৬ loanword; universal in Bangladeshi usage, and no native word exists for it. |
| `card.tabs.subtitle` | The selected tab is bold, underlined and marked with aria-selected. Three signals, one of which is a colour. | বাছাই করা ট্যাব মোটা হরফে, নিচে দাগ, আর aria-selected দিয়ে চিহ্নিত — তিনটি সংকেত, তার একটি রং | হরফ reused from verified gb-5. নিচ with short ই-কার per rule ২.১. aria-selected stays Latin: a code token copied literally. |
| `card.nav.name` | Nav | নেভিগেশন | Rule ২.৬ loanword. পথনির্দেশ is a coinage nobody uses for site navigation; মেনু names a different thing and is kept for it. |
| `card.nav.subtitle` | Vertical and horizontal. The current item carries a bar, a heavier weight and aria-current. | খাড়া আর আড়াআড়ি — এখন যেখানে আছেন সেই অংশে একটি দাগ, ভারী হরফ আর aria-current | খাড়া and আড়াআড়ি are the plain native words for vertical and horizontal, in place of উল্লম্ব and অনুভূমিক. aria-current stays Latin. |
| `card.breadcrumb.name` | Breadcrumb | পথরেখা | Two ordinary words (পথ, রেখা) that say what the trail is. ব্রেডক্রাম্ব transliterates to "bread crumb" in Bangla and carries none of the meaning — see open question 6. |
| `card.breadcrumb.subtitle` | The last item is not a link, because you are already on it. | শেষ ধাপটি লিংক নয়, কারণ আপনি এখন সেখানেই আছেন | নিশ্চয়ার্থক ই in সেখানেই per rule ৩.৫. লিংক with অনুস্বার by the rule ২.৪ pattern, as in the Academy's own ইংরেজি. |
| `card.toast.name` | Toast | টোস্ট | Rule ২.৬ loanword; what developers say. It also reads as the bread — see open question 2. |
| `card.toast.subtitle` | A short message with a dismiss button that has a name of its own, not only a cross. | ছোটো একটি বার্তা, সরানোর বাটনটির নিজের নাম আছে — শুধু একটি ক্রস নয় | ছোটো with ও-কার: named in rule ২.৩'s example list and the dictionary headword; ছোট has no entry. বাটন matches card.button.name. |
| `card.empty-state.name` | Empty state | যখন কিছু নেই | Written as Bangla rather than calqued: it echoes the verified ms-3, এখনো কিছু নেই। A phrase as a title follows the approved gb-10, যা এই পদ্ধতি করে না. |
| `card.empty-state.subtitle` | Says what is missing, and then exactly what to do about it. | কী নেই তা বলে, তারপর ঠিক কী করতে হবে সেটাও বলে | কী = what per rule ৩.১. |
| `card.code-block.name` | Code block | কোড ব্লক | কোড reused from verified bt-5 (কোডটি কপি করুন); ব্লক is a rule ২.৬ loanword in ordinary use. |
| `card.code-block.subtitle` | Aninda Mono, a horizontal scroll rather than a wrap, and a copy button that says what it copies. | Aninda Mono হরফে, লাইন ভাঙে না — পাশে সরে যায়, আর কপি বাটনটি বলে কী কপি হবে | Aninda Mono stays Latin: a product name that must stay recognisable, per house guidance 2. কপি is a dictionary headword (p. 265) and is used in verified bt-5. |
| `card.sign-in.name` | Sign in | প্রবেশ | Plain native word, and the one Bangla sites already use (প্রবেশ করুন). Preferred over সাইন ইন or লগ ইন. |
| `card.sign-in.subtitle` | One card, two fields, and an option for someone who has no password. | একটি কার্ড, দুটি ঘর, আর যার পাসওয়ার্ড নেই তার জন্যও একটি উপায় | পাসওয়ার্ড spelt with স per rule ২.৮ (ইংরেজি s ধ্বনির জন্য স — পাসপোর্ট, বাস). Plain যার/তার rather than the honorific যাঁর/তাঁর, since the Academy has no চন্দ্রবিন্দু rule and the plain form suits the register. |
| `card.settings.name` | Settings | সেটিংস | Rule ২.৬ loanword; universal in Bangladeshi software. বিন্যাস means layout and would mislead. |
| `card.settings.subtitle` | Grouped in fieldsets, with the destructive action kept apart and named. | ঘরগুলো দলে সাজানো, আর যে কাজ আর ফেরানো যায় না সেটি আলাদা রাখা, নাম ধরে লেখা | "যে কাজ আর ফেরানো যায় না" matches card.dialog.subtitle — one name for one thing. |
| `card.dashboard.name` | Dashboard | ড্যাশবোর্ড | Rule ২.৬ loanword; no native equivalent is in use. |
| `card.dashboard.subtitle` | Four figures, one table, and a note saying where the numbers came from. | চারটি সংখ্যা, একটি টেবিল, আর সংখ্যাগুলো কোথা থেকে এসেছে তা বলা একটি লাইন | টেবিল matches card.table.name. Counts up to ten are written as words (চারটি) and larger ones as Bengali numerals, per house rule 9. |
| `card.docs-page.name` | Docs page | নির্দেশিকার পাতা | নির্দেশিকা is a dictionary headword (p. 746) and the everyday Bangladeshi word for a manual (ব্যবহার নির্দেশিকা). সহায়িকা was rejected: not a headword (checked 14 Aug 2026). |
| `card.docs-page.subtitle` | Breadcrumb, page navigation and prose held to a readable line length. | পথরেখা, পাতার ভিতরের নেভিগেশন, আর পড়ার মতো মাপে ধরে রাখা লেখা | পথরেখা and নেভিগেশন match card.breadcrumb.name and card.nav.name. মতো with ও-কার per rule ২.৩, which lists it by name. |
| `card.landing.name` | Landing | প্রথম পাতা | Plain and true to the thing: the page a visitor arrives on. ল্যান্ডিং পাতা is the developer's phrase and remains available if the site later needs to distinguish it from a home page. |
| `card.landing.subtitle` | A claim, the reason to believe it, and two ways forward. | একটি দাবি, সেটি বিশ্বাস করার কারণ, আর এগিয়ে যাওয়ার দুটি পথ | Plain চলিত; all four nouns are ordinary dictionary words. |
| `card.pricing.name` | Pricing | দাম | The plainest native word, and the one people actually use. মূল্যতালিকা is the shopfront word and reads formal. |
| `card.pricing.subtitle` | Three plans, with the recommended one marked by a badge and a word. | তিনটি প্যাকেজ, সুপারিশ করা প্যাকেজটির গায়ে একটি ব্যাজ আর একটি শব্দ | প্যাকেজ is what Bangladeshi users call a priced tier (ইন্টারনেট প্যাকেজ); a rule ২.৬ loanword, not a dictionary headword (checked 14 Aug 2026). পরিকল্পনা would mean a scheme, not a tier. ব্যাজ matches card.badge.name. |
| `card.not-found.name` | Not found | পাতা পাওয়া যায়নি | Same string as ui.not-found, so the pattern and the page it describes are named identically. |
| `card.not-found.subtitle` | Says the page is missing, then offers the pages most people were looking for. | পাতাটি নেই তা জানায়, তারপর মানুষ যেসব পাতা সবচেয়ে বেশি খোঁজেন সেগুলো দেখায় | Plain চলিত verb forms per rule ৫ and §৭. খোঁজেন keeps the ordinary polite third person. |
| `card.form-with-validation.name` | Form with validation | যাচাইসহ ফর্ম | ফর্ম and যাচাই are both plain and in ordinary use; যাচাই is preferred over ভ্যালিডেশন. Compound written closed per rule ৩.২ (সমাসবদ্ধ পদ). |
| `card.form-with-validation.subtitle` | A summary at the top, an error under each field, and nothing lost. | উপরে এক জায়গায় সব ভুলের তালিকা, প্রতিটি ঘরের নিচে তার নিজের ভুল, আর কিছুই হারায় না | তালিকা preferred over the loanword লিস্ট. নিচ with short ই-কার per rule ২.১. নিশ্চয়ার্থক ই in কিছুই per rule ৩.৫. |
| `chapter.welcome` | Welcome | স্বাগতম | Verified string gb-1, BANGLA-STANDARD.md. |
| `chapter.the-name` | The name | নাম | Verified string gb-2, BANGLA-STANDARD.md. |
| `chapter.the-mark` | The mark | চিহ্ন | Verified string gb-3, BANGLA-STANDARD.md. |
| `chapter.icons` | Icons | আইকন | Rule ২.৬ loanword. চিহ্ন is already the mark (gb-3), so reusing it here would break the one-name-one-thing rule; প্রতীক is kept for a glyph inside a component. |
| `chapter.colour` | Colour | রং | Verified string gb-4, BANGLA-STANDARD.md. |
| `chapter.type` | Type | হরফ | Verified string gb-5, BANGLA-STANDARD.md. |
| `chapter.space-and-shape` | Space and shape | ফাঁক ও আকার | Verified string gb-6, BANGLA-STANDARD.md. |
| `chapter.components` | Components | উপাদান | Verified string gb-7, BANGLA-STANDARD.md. |
| `chapter.motion` | Motion | গতি | Verified string gb-8, BANGLA-STANDARD.md. |
| `chapter.voice` | Voice | কণ্ঠস্বর | Verified string gb-9, BANGLA-STANDARD.md. ণ is correct here by ণ-ত্ব বিধান (তৎসম). |
| `chapter.writing-in-bangla` | Writing in Bangla | বাংলায় লেখা | বাংলা keeps অনুস্বার — rule ২.৪ says so by name ("বাংলা ও বাংলাদেশ শব্দে অনুস্বার থাকবে"). লেখা is the noun the verified strings already use. |
| `chapter.applying-it` | Applying it | কাজে লাগানো | Plain চলিত idiom. প্রয়োগ is correct but reads like a manual; কাজে লাগানো is what a person says. |
| `chapter.licence-and-trademarks` | Licence and trademarks | লাইসেন্স ও ট্রেডমার্ক | Both are dictionary headwords — লাইসেন্স p. 1201, ট্রেডমার্ক p. 558 — and ট্রেডমার্ক is the term in Bangladesh's own statute, ট্রেডমার্ক আইন, ২০০৯ (bdlaws.minlaw.gov.bd, act-1010). পণ্যচিহ্ন is the older word and is not what the law uses. |
| `chapter.what-this-system-does-not-do` | What this system does not do | যা এই পদ্ধতি করে না | Approved string gb-10, BANGLA-STANDARD.md. পদ্ধতি rather than ব্যবস্থা, which reads administrative. |
| `theme.light` | Light | আলো | Verified string th-1, BANGLA-STANDARD.md. ও-কার per rule ২.৩. |
| `theme.dark` | Dark | অন্ধকার | Verified string th-2, BANGLA-STANDARD.md. |
| `theme.hc-light` | High contrast, light | বেশি কনট্রাস্ট, আলো | Verified th-3 (বেশি কনট্রাস্ট) joined to verified th-1 (আলো) with the same comma the English label uses. Comma is ordinary Western punctuation in Bangla — W3C Bengali orthography notes. |
| `theme.hc-dark` | High contrast, dark | বেশি কনট্রাস্ট, অন্ধকার | Verified th-3 joined to verified th-2, same construction as theme.hc-light. |
| `ui.skip-to-content` | Skip to next content | সরাসরি মূল অংশে যান | Written as Bangla, not calqued: a skip link says where it takes you. সরাসরি carries "skip" without the awkward এড়িয়ে যান, which would read as "avoid it". |
| `ui.menu` | Menu | মেনু | Rule ২.৬ loanword; universal. তালিকা is kept for an actual list, so the two do not collide. |
| `ui.close` | Close | বন্ধ করুন | Plain চলিত imperative, matching the verified button set (বাতিল করুন, আবার চেষ্টা করুন). |
| `ui.search` | Search | খুঁজুন | Plain native imperative; অনুসন্ধান করুন is the official-notice register the brand avoids. চন্দ্রবিন্দু is lexical. |
| `ui.copy` | Copy | কপি করুন | Matches verified bt-5. কপি is a dictionary headword (p. 265); অনুলিপি would be less standard, not more. |
| `ui.copied` | Copied | কপি হয়েছে | Built on verified ms-4 (সংরক্ষিত হয়েছে) so the two confirmations sound alike. |
| `ui.download` | Download | ডাউনলোড করুন | Rule ২.৬ loanword; what Bangladeshi users say and read everywhere. নামিয়ে নিন is native but ambiguous on its own. |
| `ui.loading` | Loading | লোড হচ্ছে… | Rule ২.৬ loanword, চলিত continuous per rule ৫. The plainer আসছে… was considered and set aside as too vague on its own. |
| `ui.not-found` | Page not found | পাতা পাওয়া যায়নি | Plain চলিত negative; states the fact without blaming the reader, as the verified ms-1 does. Same string as card.not-found.name. |
| `ui.back-to-top` | Back to the top | উপরে ফিরে যান | Plain চলিত imperative; ঊর্ধ্বে would be তৎসম register against the brand voice. |
| `ui.read-more` | Read more | আরও পড়ুন | আরও keeps its full ও — the Academy dictionary calls it আরো-র সংগততর বানান (p. 164), and it does not follow the এখনো pattern. House rule 1. |
| `ui.language` | English / বাংলা | English / বাংলা | Identical in both languages by design: each half is written in its own script so a reader of either language can find it without first understanding the other. বাংলা keeps অনুস্বার per rule ২.৪. |
| `status.success` | Success | সফল | Plain dictionary word, one syllable pair, fits a badge. |
| `status.warning` | Warning | সতর্কতা | Plain dictionary word. সাবধান is an imperative shout and is too loud for a status label. |
| `status.error` | Error | সমস্যা | সমস্যা names the situation without implying the reader caused it, which matches the brand rule that errors never blame the reader. ত্রুটি is the more conventional UI word — see open question 3. ভুল stays for a wrong entry in a specific form field. |
| `status.info` | Information | তথ্য | Plain dictionary word, universally understood. |

---

## Sources

**Primary**
- বাংলা একাডেমি, *প্রমিত বাংলা বানানের নিয়ম*, পরিমার্জিত সংস্করণ ২০১২ (পুনর্মুদ্রণ ২০১৫) —
  <https://archive.org/details/bangla-academy-promito-bangla-bananer-niyom-2015>
- বাংলা একাডেমি, *আধুনিক বাংলা অভিধান* — <https://baabo.jothartho.com/>
  - Checked for this document on 14 August 2026: নির্দেশিকা p. 746 · লাইসেন্স p. 1201 ·
    ট্রেডমার্ক p. 558 · তির p. 604 · বোতাম p. 1018 · কপি p. 265 · রং p. 1156 · আরও p. 164 ·
    কোন p. 337 · কোনো p. 338. Returned *not found*: পিক্সেল, প্যাকেজ, সহায়িকা, প্রবেশগম্যতা,
    অভিগম্যতা.
- বাংলাদেশ আইন মন্ত্রণালয়, *ট্রেডমার্ক আইন, ২০০৯* — <http://bdlaws.minlaw.gov.bd/act-1010.html>
- বাংলাদেশ সরকার, *অভিগম্য অভিধান* — <https://accessibledictionary.gov.bd/>

**Secondary**
- W3C / Richard Ishida, *Bengali/Bangla orthography notes* — <https://r12a.github.io/scripts/beng/bn.html>
- W3C, *Bengali Layout Requirements* — <https://w3c.github.io/iip/bengali/>

**Internal**
- `06_type/BANGLA-STANDARD.md` — the verified rules and the 27 already-approved strings.
- `02_strategy/ENGLISH-STANDARD.md` — the tone these strings carry into Bangla.
- `08_components/_cards.json` — the English names and subtitles these were written against.
