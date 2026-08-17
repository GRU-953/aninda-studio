<!-- Hand-written chapter. build.py reads this file; it never writes it. -->

The Bangla in this system follows **প্রমিত বাংলা** — standard Bangla — as set out
by the Bangla Academy.

## Which document is current

The governing document is *বাংলা একাডেমি প্রমিত বাংলা বানানের নিয়ম*: first
edition 1992, revised edition September 2012, first reprint of the revised
edition January 2015. Searches on 14 August 2026 found no later edition. The
2012 text, reprinted in 2015, remains the standard.

The second source used throughout is the Academy's own dictionary, *আধুনিক বাংলা
অভিধান*. Where the rules are permissive, the dictionary's choice of headword is
the tie-breaker, because it is the Academy applying its own rules.

## The rule this whole system runs on

**Only verified Bangla is shipped. No Bangla is invented.**

Every Bangla string in this book, in the component library and in the token
files was reviewed string by string against those two sources. Where a verified
string exists, it is used. Where one does not, the English is left in place and
the gap is named. That is why parts of the Bangla sections of this book say so
plainly instead of quietly filling the space.

This is not modesty. Inventing Bangla and shipping it looks the same as having
written it well, right up until a Bangla reader meets it.

## The ten house rules

1. **এখনো, কখনো, তখনো** with ও-কার — but **আরও** with the full ও. The asymmetry is
   the Academy's own: the dictionary makes এখনও a bare cross-reference to এখনো,
   while it calls আরও the *সংগততর* — more consistent — spelling of আরো.
2. **কোনো** means *any* or *some*. **কোন** means *which*. Never interchange them.
3. **রং** standing alone or at the end of a word. **রঙ** only when a vowel
   follows — রঙিন, রঙের.
4. **ছোটো, বড়ো, ভালো, কালো, মতো, হলো, হতো** — ও-কার, under rule 2.3.
5. No **ণ** in any non-Sanskrit word: ধরন, রানি, সোনা, ঝরনা, ঠান্ডা.
6. Avoid the hasanta where it is not needed: **সফটওয়্যার**, not সফ্টওয়্যার.
7. Established loanwords are standard Bangla: **কপি, ফাইল, সফটওয়্যার, মেগাবাইট**.
   Do not "correct" them into অনুলিপি or নথি — that would be less standard, not
   more.
8. **চলিত throughout.** No সাধু forms anywhere in the product.
9. **Bengali numerals** in prose and in measurements. Western digits only where a
   string has to be copied literally — a version number, a code sample, a file
   extension.
10. The দাঁড়ি ends a statement. The question mark and the exclamation mark are
    the ordinary Western characters. No space before the দাঁড়ি, one space after,
    and never let it begin a line.

Rule 9 applies to Bangla prose, and this book's prose is English, so every rule
number quoted here uses Western digits. There is a practical reason as well as a
consistency one: the Bengali digit for four is drawn as an 8, so a Bengali
numeral inside an English sentence reads as the wrong number to a reader who does
not know the script.

## Punctuation

The Academy's 2012 rules contain no punctuation section. The rules below come
from the W3C's Bengali script documentation and from the Bengali Wikipedia
article on যতিচিহ্ন.

{{data:bangla-punctuation}}

The W3C's *Bengali Layout Requirements* records two approaches to spacing around
the দাঁড়ি and names the primary one: no space character before it, letting the
font's own advance width open a small gap, then a single space after. It also
records a line-breaking constraint — never move a দাঁড়ি to the beginning of a new
line.

The em dash is a genuine Bangla যতিচিহ্ন, not an English import. It is used in
this system's Bangla error message and in the voice sample, doing exactly the job
it is meant for. It is half as long again as the hyphen, which is a separate mark
with a separate job.

## Latin words inside Bangla sentences

Normal, and sanctioned by the Academy's own practice — its dictionary embeds
Latin script inside Bangla entries constantly, as glosses and as technical
terms.

1. Where the dictionary has a Bangla form, prefer it in prose. Write **মেগাবাইট**
   inside a Bangla sentence, not "MB".
2. Keep Latin for product names that must stay recognisable and searchable —
   GitHub, Figma, CSS.
3. Keep Latin for anything copied literally.
4. Do not mix scripts inside one word. `GitHub-এ` — Latin name, Bangla
   case-ending, hyphenated — is the established Bangladeshi convention. It is
   marked here as a convention, because no formal style-guide citation for it
   was found.

## Setting Bangla type

The type chapter carries the measured numbers. The two that matter most when
writing rather than designing:

- Bangla never goes below **12 px**, whatever the size relationship would
  otherwise say.
- Below **14 px** Bangla gains one weight step, because the মাত্রা — the headline
  stroke running along the top of the letters — goes pale before the letters do.

## Where this system's Bangla comes from

{{data:bangla-provenance}}

## What is explicitly unverified

- Any Bangla Academy edition later than 2012. None was found as at
  14 August 2026.
- Any Academy rule on ৎ or on চন্দ্রবিন্দু. No such rule exists in the 2012
  document; both are lexical, so follow the dictionary word by word.
- Any Academy or published style-guide rule on Bengali against Western numerals.
  None was found. Rule 9 above rests on the Academy's own printing practice plus
  one editorial judgement about strings that must survive copy and paste.
- The `GitHub-এ` hyphenation convention. Widespread practice, no formal citation.
- তখনো as a dictionary headword. Neither তখনো nor তখনও has an entry; rule 1
  infers it from এখনো and কখনো, and says so.

**And the largest one: no second Bangla reader has reviewed any of this.** The
sources were read carefully and quoted with page numbers. That is a reading, not
a review. Chapter 14 repeats it, because it belongs in both places.
