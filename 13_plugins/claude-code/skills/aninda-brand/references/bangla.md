<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# Bangla — the verified strings, and nothing else

The standard is **বাংলা একাডেমি, প্রমিত বাংলা বানানের নিয়ম, পরিমার্জিত সংস্করণ ২০১২
(পুনর্মুদ্রণ ২০১৫)**, with spellings checked against **আধুনিক বাংলা অভিধান** page by
page.

**Licence:** PolyForm Noncommercial 1.0.0.

---

## The rule

**Use only a string from the table below. Do not write new Bangla.**

If nothing in the table fits what you need, leave the English in place and say
which string is missing. That is the correct answer, not a failure. Every string
below was checked against the Academy's dictionary; anything outside the table
has not been, and unverified Bangla in a bilingual system is worse than English
that is honestly labelled as the only version available.

---

## The 31 verified strings

| id | Bangla | English |
| --- | --- | --- |
| wm-1 | অনিন্দ্য স্টুডিও | Aninda Studio |
| wm-2 | অনিন্দ্য | Aninda |
| th-1 | আলো | Light |
| th-2 | অন্ধকার | Dark |
| th-3 | বেশি কনট্রাস্ট | High contrast |
| col-1 | মোহনা | Estuary — the ground ramp |
| col-2 | জোয়ার | Tidewater — the accent ramp |
| col-3 | পলি | Silt — the success ramp |
| col-4 | কাশ | Kans — the warning ramp |
| col-5 | লাল মাটি | Laterite — the danger ramp |
| col-6 | বর্ষা | Monsoon — the info ramp |
| bt-1 | লেখাটি সংরক্ষণ করুন | Save the entry |
| bt-2 | বাতিল করুন | Cancel |
| bt-3 | ফাইলটি মুছে ফেলুন | Delete the file |
| bt-4 | আবার চেষ্টা করুন | Try again |
| bt-5 | কোডটি কপি করুন | Copy the code |
| ms-1 | সংরক্ষণ করা যায়নি। আপনার লেখা এখনো আছে — একটু পরে আবার চেষ্টা করুন। | Couldn't save. Your work is still here — try again in a moment. |
| ms-2 | ফাইলটি অনেক বড়ো। সর্বোচ্চ ১০ মেগাবাইট। | That file is too big. The limit is 10 MB. |
| ms-3 | এখনো কিছু নেই। শুরু করতে প্রথম লেখাটি যোগ করুন। | Nothing here yet. Add your first entry to begin. |
| ms-4 | সংরক্ষিত হয়েছে | Saved |
| vc-1 | আমি ছোটো, যত্নে গড়া সফটওয়্যার বানাই। কোনো কিছুর সীমা থাকলে সেটা এখানেই লেখা থাকবে — লুকিয়ে রাখা হবে না। | I make small, carefully built software. Where something has a limit, that limit is written down here rather than hidden. |
| gb-1 | স্বাগতম | Welcome |
| gb-2 | নাম | Name |
| gb-3 | চিহ্ন | The mark |
| gb-4 | রং | Colour |
| gb-5 | হরফ | Typography |
| gb-6 | ফাঁক ও আকার | Space and shape |
| gb-7 | উপাদান | Components |
| gb-8 | গতি | Motion |
| gb-9 | কণ্ঠস্বর | Voice |
| gb-10 | যা এই পদ্ধতি করে না | What this system does not do |

---

## The ten house rules

Follow these if you are checking existing Bangla, or explaining a choice. They do
not license you to write new strings.

1. **এখনো, কখনো, তখনো** with ও-কার — but **আরও** with the full ও. The asymmetry
   is the Academy's own, and it is evidenced.
2. **কোনো** = any or some. **কোন** = which. Never interchange them.
3. **রং** standing alone or word-final. **রঙ** only before a vowel: রঙিন, রঙের.
4. **ছোটো, বড়ো, ভালো, কালো, মতো, হলো, হতো** — ও-কার throughout.
5. **No ণ in any non-Sanskrit word**: ধরন, রানি, সোনা, ঝরনা, ঠান্ডা.
6. **Avoid the hasanta where it is not needed**: সফটওয়্যার, not সফ্টওয়্যার.
7. **Established loanwords are standard**: কপি, ফাইল, সফটওয়্যার, মেগাবাইট. Do not
   "correct" them into অনুলিপি or নথি.
8. **চলিত throughout.** No সাধু forms anywhere in a product.
9. **Bengali numerals** in prose and measurements. Western digits only where a
   string must be copied literally.
10. **`।`** ends a statement, **`?`** asks, **`!`** exclaims. No space before `।`,
    one space after, and never let `।` begin a line.

---

## What is explicitly not verified

Say so if any of these comes up, rather than filling the gap.

- Any Bangla Academy edition later than 2012. None was found as at
  14 August 2026.
- Any Academy rule on ৎ (খণ্ড ত) or চন্দ্রবিন্দু. No such rule exists in the 2012
  document; both are lexical.
- Any Academy or published style-guide rule on Bengali against Western numerals.
  None found; rule 9 above rests on the Academy's own printing practice plus
  editorial judgement.
- The `GitHub-এ` convention for a Latin word taking a Bangla case ending.
  Widespread practice, no formal citation found.
- তখনো as a dictionary headword. Neither তখনো nor তখনও has an entry; rule 1 is
  inferred from এখনো and কখনো.

---

## Known gaps in the system's own files

25 of the 30 component cards have no Bangla name, and 30 of 30 have no Bangla
subtitle, because the verified table holds no entry for them. Those gaps are
named in `08_components/_cards.json` under `_bangla_gaps` and left empty on
purpose. Filling them needs the Bangla Academy check, not a translation.

---

## Sources

- বাংলা একাডেমি, *প্রমিত বাংলা বানানের নিয়ম*, ২০১২ (পুনর্মুদ্রণ ২০১৫).
- বাংলা একাডেমি, *আধুনিক বাংলা অভিধান*, searchable page scans.
- W3C, *Bengali Layout Requirements*.
- Checked 14 August 2026.
