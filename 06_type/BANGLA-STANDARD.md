# Bangla Academy standard spelling — verification and applied string review

**Prepared:** 14 August 2026
**Scope:** Verify current Bangla Academy standard Bengali spelling rules against primary sources, then apply them to the Aninda Studio interface and guidebook strings.
**Method:** Every rule below is quoted from a primary or near-primary source with a URL. Anything that could not be sourced is explicitly marked **UNVERIFIED**. Nothing here is asserted from memory.

---

## 0. Which document is actually current

The governing document is:

> **বাংলা একাডেমি প্রমিত বাংলা বানানের নিয়ম**
> প্রথম সংস্করণ: ১৯৯২ · পরিমার্জিত সংস্করণ: আশ্বিন ১৪১৯ / সেপ্টেম্বর ২০১২ · পরিমার্জিত সংস্করণের প্রথম পুনর্মুদ্রণ: মাঘ ১৪২১ / জানুয়ারি ২০১৫

Full scanned text: <https://archive.org/details/bangla-academy-promito-bangla-bananer-niyom-2015>

**Searches on 14 August 2026 found no edition later than the 2012 পরিমার্জিত সংস্করণ.** The 2012 text (reprinted 2015) remains the current standard. I could not find a 2024–2026 revision; treat the claim "there is a newer edition" as **UNVERIFIED — most likely none exists**.

The document's own statement of authority, from the মুখবন্ধ:

> "এখন থেকে বাংলা একাডেমী তার সকল কাজে, তার বই ও পত্র-পত্রিকায় এই বানান ব্যবহার করবে। ভাষা ও সাহিত্যের জাতীয় প্রতিষ্ঠানরূপে বাংলা একাডেমী সংশ্লিষ্ট সকলকে — লেখক, সাংবাদিক, শিক্ষক, বুদ্ধিজীবী এবং বিশেষভাবে সংবাদপত্রগুলিকে — সরকারি ও বেসরকারি সকল প্রতিষ্ঠানকে এই বানান ব্যবহারের সুপারিশ ও অনুরোধ করছে।"

**Structure of the 2012 rules** (this matters, because it shows what the rules do *not* cover):

| § | Topic |
|---|---|
| ১.১–১.৬ | তৎসম শব্দ (ই/উ, রেফ, অনুস্বার, ইন্-প্রত্যয়ান্ত, বিসর্গ) |
| ২.১–২.১১ | অতৎসম শব্দ (ই/উ, এ/অ্যা, ও, ং/ঙ, ক্ষ/খ, জ/য, ণ/ন, শ/ষ/স, বিদেশি যুক্তবর্ণ, হস-চিহ্ন, ঊর্ধ্ব-কমা) |
| ৩.১–৩.৫ | কি/কী, সমাসবদ্ধ পদ, না-বাচক, অধিকন্তু 'ও', নিশ্চয়ার্থক 'ই' |
| ৪ | ব্যক্তি, প্রতিষ্ঠান বা সংস্থার নাম |
| ৫.১–৫.১০ | ক্রিয়াপদের রূপ |

There is **no section on ৎ, no section on চন্দ্রবিন্দু, no section on numerals, and no section on punctuation.** Those are handled below from other sources, and flagged accordingly.

**Second primary source used throughout:** *বাংলা একাডেমি আধুনিক বাংলা অভিধান* (the Academy's own modern dictionary), searchable page-scans at <https://baabo.jothartho.com/>. Where the rules are permissive, the dictionary's choice of headword is the tie-breaker — it is the Academy applying its own rules.

---

## PART 1 — the seven questions

### 1. এখনও vs এখনো · কখনও/কখনো · তখনও/তখনো · আরও/আরো

This is the one place where your instinct needs adjusting, and the answer is **not uniform** — the Academy splits these two ways, and the split is evidenced.

**The two competing rules:**

Rule ২.৩ (ও), on non-Sanskrit words — the final *a*-sound of a word may be written with ও-কার:

> "শব্দশেষের এসব অ-ধ্বনি ও-কার দিয়ে লেখা যেতে পারে।
> কালো, খাটো, **ছোটো**, ভালো; … করাতো, কেনো, দেবো, হতো, হবো, হলো; **কোনো, মতো**।"

Rule ৩.৪ (ও) — the *additive* 'ও' stays a full letter:

> "অধিকন্তু অর্থে ব্যবহৃত 'ও' … কার-চিহ্ন রূপে যুক্ত না হয়ে পূর্ণ রূপে শব্দের পরে যুক্ত হবে। যেমন: আজও, আমারও, কালও, তোমারও।"

So the test is: **is the ও a live "…too / …as well" particle bolted onto a word (→ full ও), or has the word fused into a single lexical adverb (→ ও-কার)?**

**The dictionary settles each case.** Results from *আধুনিক বাংলা অভিধান*:

| Form | Status in the Academy dictionary | Verdict |
|---|---|---|
| **এখনো** | Full entry, p. 236: "এখনো /অ্যাখনো/ [বা.] ক্রি.বিণ. ১ আজও, বর্তমানকাল পর্যন্ত। ২ এরপরেও, তা সত্ত্বেও…" | ✅ **use this** |
| এখনও | p. 236: "এখনও /অ্যাখনো/ [বা.] ক্রি.বিণ. **দ্র এখনো**।" — a cross-reference only ("দ্র" = দ্রষ্টব্য, *see*) | variant, not primary |
| **কখনো** | Headword with its own entry | ✅ **use this** |
| কখনও | No headword — site returns "প্রস্তাবিত শব্দ" (suggestions), i.e. not found | not a headword |
| তখনো / তখনও | **Neither** is a separate headword | see note below |
| **আরও** | p. 164: "আরও /আরো/ [বা.] … ক্রি.বিণ. অধিকন্তু; **আরো-র সংগততর বানান**।" — *the more consistent spelling of আরো* | ✅ **use this** |
| আরো | p. 166: "আরো /আরো/ [বা.] … ক্রি.বিণ. অধিকন্তু; **আরও-এর প্রচলিত বানান**।" — *the common spelling of আরও* | acceptable but second-best |

**Conclusion — and it is deliberately asymmetric:**

- **এখনো, কখনো** take ও-কার. (Lexicalised adverbs; the dictionary makes এখনও a mere pointer to এখনো.)
- **আরও** takes the full ও. (Still a live additive particle; the Academy calls it the *সংগততর* — "more consistent" — spelling, which is as close to a ruling as this dictionary ever gets.)
- **তখনো** — by direct parallel with এখনো and কখনো. **Marked as inference, not a direct citation**, because the dictionary has no headword for either form.

Sources: [Academy rules 2012/2015](https://archive.org/details/bangla-academy-promito-bangla-bananer-niyom-2015) · [এখনো](https://baabo.jothartho.com/word/এখনো/) · [আরও](https://baabo.jothartho.com/word/আরও/) · [আরো](https://baabo.jothartho.com/word/আরো/)

---

### 2. কোনো vs কোন

**Your understanding is correct, and it is confirmed by two separate entries.**

From *আধুনিক বাংলা অভিধান*:

> **কোন** /কোন্/ [বা.] সর্ব. কী, কে, কোনটি (*কোন দিন*)। ক্রি.বিণ. কী প্রকারে, কীভাবে; কীসে (*তুমিই বা কোন ভালো খেলোয়াড়*)। — p. 337

> **কোনো** /কোনো/ [বা.] সর্ব. বিণ. ১ অনির্দিষ্ট বা অনির্ধারিত একজন লোক বা বস্তু। ২ কে বা কী (*কোনো বিষয়*)। ৩ বহুর মধ্যে একটি বা একজন (*কোনো লোকই আসেনি*)। — p. 338

- **কোনো** = indefinite, "any / some / a certain". Also its compounds: কোনো কোনো, কোনো না কোনো, কোনোমতে, কোনোরকমে.
- **কোন** = interrogative, "which / what".

Corroborated by rule ২.৩, which lists **কোনো** in the ও-কার set, and by the Academy's own prose throughout both books ("কোনো বানান-সংস্কারের প্রয়াস নয়", "কোনো কোনো ক্ষেত্রে").

Sources: [কোন](https://baabo.jothartho.com/word/কোন/) · [কোনো](https://baabo.jothartho.com/word/কোনো/)

---

### 3. রং vs রঙ

**রং is standard for "colour".** Directly ruled on.

Rule ২.৪ (ং, ঙ):

> "শব্দের শেষে প্রাসঙ্গিক ক্ষেত্রে সাধারণভাবে অনুস্বার (ং) ব্যবহৃত হবে। যেমন: ঢং, পালং, **রং**, রাং, সং।
> তবে অনুস্বারের সঙ্গে স্বর যুক্ত হলে ঙ হবে। যেমন: বাঙালি, ভাঙা, **রঙিন, রঙের**।
> বাংলা ও বাংলাদেশ শব্দে অনুস্বার থাকবে।"

The dictionary agrees decisively:

> **রং** /রঙ্/ [স. রঙ্গ >] বি. ১ বর্ণ (*লাল রং*)। ২ রঞ্জক-দ্রব্য। … — p. 1156

and its whole family follows: রংকানা, রংচং, রংচটা, রংধনু, রংতুলি, রংবেরং, রংমশাল. **রঙ has no entry at all** — the dictionary site returns only "প্রস্তাবিত শব্দ" (suggestions).

**Practical rule for you:** write **রং** when it stands alone or ends a word; write **রঙ** only when a vowel follows — রঙিন, রঙের, রঙচঙে.

Sources: [Academy rules §২.৪](https://archive.org/details/bangla-academy-promito-bangla-bananer-niyom-2015) · [রং](https://baabo.jothartho.com/word/রং/)

---

### 4. ৎ (খণ্ড ত), ঁ (চন্দ্রবিন্দু), and ণ/ন

**ণ / ন — fully ruled on.** Rule ২.৭ (মূর্ধন্য ণ, দন্ত্য ন):

> "অতৎসম শব্দের বানানে ণ ব্যবহার করা হবে না। যেমন: অঘ্রান, ইরান, কান, কোরান, গভর্নর, গুনতি, গোনা, ঝরনা, ধরন, পরান, রানি, সোনা, হর্ন।
> তৎসম শব্দে ট ঠ ড ঢ-য়ের পূর্বে যুক্ত নাসিক্যবর্ণ ণ হয়।
> কিন্তু অতৎসম শব্দের ক্ষেত্রে ট ঠ ড ঢ-য়ের আগে কেবল ন হবে। যেমন: গুন্ডা, ঝান্ডা, ঠান্ডা, ডান্ডা, লন্ঠন।"

Effect on ordinary interface words: **ধরন, রানি, সোনা, ঝরনা, গুনতি, ঠান্ডা** — all with দন্ত্য ন. Sanskrit-derived words keep ণ by the ordinary ণ-ত্ব বিধান, which is why **কণ্ঠস্বর, সংরক্ষণ, বর্ণ, প্রমাণ** are correct as written.

**ৎ (খণ্ড ত) — no rule exists.** The 2012 document has no section on খণ্ড ত. It is lexical: follow the dictionary spelling of the individual word (চিৎকার, ভবিষ্যৎ, বৎসর, উৎসব). **Marked UNVERIFIED as a general rule — because there is no general rule to verify.**

The one rule that *does* bear on it is ২.১০ (হস-চিহ্ন):

> "হস-চিহ্ন যথাসম্ভব বর্জন করা হবে। যেমন: কলকল, করলেন, কাত, চট, চেক, জজ, ঝরঝর, টক, টন, টাক, ডিশ, তছনছ, ফটফট, বললেন, শখ, হুক।
> তবে যদি অর্থবিভ্রান্তি বা ভুল উচ্চারণের আশঙ্কা থাকে তাহলে হস-চিহ্ন ব্যবহার করা যেতে পারে।"

This is why the dictionary spells the software term **সফটওয়্যার**, not সফ্টওয়্যার — no killer stroke.

**ঁ (চন্দ্রবিন্দু) — no rule exists** in the Academy document either. It is lexical (ফাঁক, বাঁকানো, আঁধার). The only written convention I could source is Bengali Wikipedia's own house rule that চন্দ্রবিন্দু is not used on honorific pronouns (তাঁর → তার) — that is Wikipedia's rule, **not the Academy's**, and does not bind you.

Sources: [Academy rules §২.৭, §২.১০](https://archive.org/details/bangla-academy-promito-bangla-bananer-niyom-2015) · [উইকিপিডিয়া:বাংলা বানানের নিয়ম](https://bn.wikipedia.org/wiki/উইকিপিডিয়া:বাংলা_বানানের_নিয়ম)

---

### 5. Bengali numerals ০১২৩ vs Western 0123

**The Academy's rules say nothing about numerals.** There is no rule to cite. What can be evidenced is *practice*, and the practice is consistent:

- **The Academy's own rulebook** numbers its sections ১.১ … ৫.১০, numbers its pages ১৮, ১৯, ২০, and states its print run as "২০০০০ কপি" — Bengali numerals throughout.
- **The Academy's own dictionary** uses Bengali numerals for sense numbers, for quantities (কোটি = ১,০০,০০,০০০), for scientific values (iodine's atomic number "৫৩"; "প্রায় ৬৮০° সে."; "২০° থেকে ২৫° সেলসিয়াস") — **including in technical and measurement contexts.**
- **W3C**, *Bengali/Bangla orthography notes*: "Bengali has a set of native digits, which are used regularly in text." The same document notes that "the modern Bangla orthography uses ASCII digit numbering, but also has a native numeric style" — i.e. both circulate.

**Recommendation for this system:**

| Context | Use | Basis |
|---|---|---|
| Running Bangla prose, quantities, file sizes, dates | **Bengali ০১২৩৪৫৬৭৮৯** | Academy's own practice, including for measurements |
| Code samples, version numbers, identifiers, anything meant to be copied literally | **Western 0123456789** | Reasoned recommendation — **UNVERIFIED against any Academy or style-guide source** |

The second row is my editorial judgement, not a sourced rule: a version string or a code token that a user must retype must survive copy-paste, and converting it would break it. Treat it as a house decision you are making, not a standard you are following.

Sources: [Academy rules, page and section numbering](https://archive.org/details/bangla-academy-promito-bangla-bananer-niyom-2015) · [আধুনিক বাংলা অভিধান](https://baabo.jothartho.com/) · [W3C Bengali orthography notes](https://r12a.github.io/scripts/beng/bn.html) · [বাংলা সংখ্যা পদ্ধতি](https://bn.wikipedia.org/wiki/বাংলা_সংখ্যা_পদ্ধতি)

---

### 6. English loanwords in Bangla script — কপি, ফাইল, সফটওয়্যার …

**Established loanwords are fully acceptable in প্রমিত বাংলা. Sanskritised replacements are *not* required.** This is one of the best-evidenced answers in this document.

Rule ২.৬ (জ, য) states the governing principle:

> "বাংলায় প্রচলিত বিদেশি শব্দ সাধারণভাবে বাংলা ভাষার ধ্বনিপদ্ধতি-অনুযায়ী লিখতে হবে। যেমন: কাগজ, জাদু, জাহাজ, জুলুম, বাজার, হাজার।"

— that is, loanwords current in Bangla are simply **written the Bangla way**, not translated away.

Rules ২.৮ and ২.৯ then give explicitly English examples as the standard:

> "ইংরেজি ও ইংরেজির মাধ্যমে আগত বিদেশি s ধ্বনির জন্য স এবং -sion, -tion, -sh প্রভৃতি বর্ণগুচ্ছ … জন্য শ ব্যবহৃত হবে। যেমন: পাসপোর্ট, বাস; ক্যাশ; টেলিভিশন; মিশন, সেশন; রেশন, স্টেশন।"
> "বাংলায় বিদেশি শব্দের আদিতে বর্ণবিশ্লেষ সম্ভব নয়। এগুলো যুক্তবর্ণ দিয়ে লিখতে হবে। যেমন: স্টেশন, সিট, স্প্রিং।"

**And the Academy's own dictionary lexicalises the exact words you are using.** Checked individually:

| Word | In *আধুনিক বাংলা অভিধান*? |
|---|---|
| **সফটওয়্যার** | ✅ Headword, p. 1287 — "সফটওয়্যার /সফ্ট্ওয়্যার্/ … কম্পিউটার নিয়ন্ত্রণ বা চালনার সাংকেতিক নির্দেশ-সংবলিত প্রোগ্রাম; software।" |
| **সফট কপি** | ✅ Headword, p. 1287 — "… কম্পিউটারে সংরক্ষিত তথ্য …, soft copy।" |
| **কপি** | ✅ Headword, p. 265 |
| **ফাইল** | ✅ Headword, p. 895 |
| **মেগাবাইট** | ✅ Headword, p. 1130 |
| কনট্রাস্ট | ❌ Not a headword |
| সেভ | ❌ Not a headword |
| সিস্টেম | ❌ Not a headword |
| স্টুডিও | ❌ Not a headword |

Note the spelling the Academy chose: **সফটওয়্যার**, with no hasanta — exactly as you have it, and exactly as rule ২.১০ predicts.

**Conclusion:** অনুলিপি for "copy" and নথি for "file" are not required and would in fact be *less* standard than কপি and ফাইল, which the Academy has itself admitted to the dictionary. The four words in the "not a headword" list are not thereby forbidden — rule ২.৬ licenses any loanword that is genuinely প্রচলিত in Bangla — but they carry less authority, so prefer a plain native word where one exists and reads naturally.

Sources: [Academy rules §২.৬, §২.৮, §২.৯, §২.১০](https://archive.org/details/bangla-academy-promito-bangla-bananer-niyom-2015) · [সফটওয়্যার](https://baabo.jothartho.com/word/সফটওয়্যার/) · [ফাইল](https://baabo.jothartho.com/word/ফাইল/) · [কপি](https://baabo.jothartho.com/word/কপি/) · [মেগাবাইট](https://baabo.jothartho.com/word/মেগাবাইট/)

---

### 7. সাধু vs চলিত

**Confirmed: চলিত / প্রমিত is the modern standard for ordinary prose, and by extension for interface text.**

The Academy's মুখবন্ধ names the shift as a settled fact of the language:

> "বাংলা ভাষা ক্রমাগত সাধু রীতির নির্মোক ত্যাগ করে চলিত রূপ পরিগ্রহ করতে থাকে।"

Two structural proofs inside the rules themselves:

1. **Rule ২.১১ (ঊর্ধ্ব-কমা)** replaces সাধু forms with চলিত ones outright: *"ঊর্ধ্ব-কমা যথাসম্ভব বর্জন করা হবে। যেমন: **বলে (বলিয়া)**, হয়ে, দুজন, চাল (চাউল), আল (আইল)।"*
2. **The whole of section ৫ (ক্রিয়াপদের রূপ)** — ten verb paradigms — is given exclusively in চলিত: উঠতাম, উঠছি, করছি, **হলো**, **হতো**, খেয়ে, যাচ্ছি, দিয়ে. No সাধু forms (করিতেছি, হইল) appear as standard anywhere.

Your voice sample's চলিত register (বানাই, থাকবে, লুকিয়ে রাখা হবে না) is therefore exactly right, and is the Academy's own register.

Source: [Academy rules, মুখবন্ধ, §২.১১, §৫](https://archive.org/details/bangla-academy-promito-bangla-bananer-niyom-2015)

---

## PART 3 — punctuation and typography

*(Presented before Part 2 because the string table depends on it.)*

The Academy's 2012 rules contain **no punctuation section**. Sourced from W3C's Bengali script documentation and Bengali Wikipedia's যতিচিহ্ন article.

### The daṛi ।

**Correct as your full stop.** W3C: *"The danda, U+0964, is used for sentence final punctuation."* Bengali Wikipedia: *"বাক্যের পরিসমাপ্তি বোঝাতে দাঁড়ি বা পূর্ণচ্ছেদ ব্যবহার করতে হয়।"*

### Question mark and exclamation mark

**Both are the ordinary Western characters — ? (U+003F) and ! (U+0021).** There is no Bengali-specific question or exclamation mark. W3C's *Bengali/Bangla orthography notes* lists the sentence-final punctuation set as exactly `. । ? !`, and adds: *"Western punctuation, such as commas, semicolons, colons, quotation marks and hyphens are also used quite commonly."* Phrase-level punctuation is likewise Western: `, ; :`.

So: statement → `।` · question → `?` · exclamation → `!`

### Space before ।

**You are right — no space before.** W3C's *Bengali Layout Requirements* records two approaches and states the primary one:

> "No space character appears between the end of the phrase and the danda glyph, but the advance width of the danda in a font should open a small gap before it. The danda is then typically followed by a single space."

> "A space is allowed before and after the danda in order to balance the space before and after it. In this case, the danda must still be kept from wrapping to a new line on its own."

**Use the first: no space before, one space after.** Let the font open the gap. Also honour the line-breaking constraint — *"Line breaking should not move a danda or double danda to the beginning of a new line"* — so never allow `।` to start a line.

### Em dash —

**Acceptable and standard in Bangla prose.** ড্যাশ (—) is listed as a regular Bangla যতিচিহ্ন: *"যৌগিক ও মিশ্র বাক্যে পৃথক ভাবাপন্ন দুই বা তার বেশি বাক্যের সমন্বয় বা সংযোগ বোঝাতে ড্যাশ বসে।"* It is a genuine Bengali punctuation mark, not an English import. Keep it in ms-1 and vc-1 — it is doing exactly the job it is meant for.

Distinguish it from the hyphen: *"হাইফেন (-)। হাইফেন দৈর্ঘ্যে ড্যাশের অর্ধেক পরিমাণ।"*

### Latin words inside Bangla sentences

**Normal and Academy-sanctioned by practice.** The Academy's own dictionary embeds Latin script inside Bangla entries constantly, as glosses and as technical terms — *software*, *soft copy*, *X-ray*, *iodine*, *quotation*, *induction*, *altocumulus cloud*, *colour-blind*, *white lead*, *soft drink* — and even chemical formulae (*KI*). No transliteration is forced.

**House guidance for this system:**

1. Where the Academy dictionary has a Bangla form, prefer it in prose — write **মেগাবাইট**, not "MB", in a sentence a user reads.
2. Keep Latin for proper product names that must stay recognisable and searchable — **GitHub**, **Figma**, **CSS**.
3. Keep Latin for anything copied literally — code, version strings, file extensions.
4. Do not mix within one word: write `GitHub-এ` (Latin name + Bangla case-ending, hyphenated), which is the established Bangladeshi convention. **Marked as convention, UNVERIFIED against a formal style-guide citation.**

Sources: [W3C Bengali Layout Requirements](https://w3c.github.io/iip/bengali/) · [W3C Bengali orthography notes](https://r12a.github.io/scripts/beng/bn.html) · [যতিচিহ্ন](https://bn.wikipedia.org/wiki/যতিচিহ্ন)

---

## PART 2 — string-by-string review

Ratings: **(a)** spelling correct? **(b)** tone natural/plain, or stiff? **(c)** recommendation **(d)** reason.

IDs for the colour names and chapter titles were not supplied; I have assigned `col-1…6` and `gb-1…10` in the order you listed them.

### Identity

**wm-1 `অনিন্দ্য স্টুডিও`**
(a) Correct. (b) Natural.
(c) **No change.**
(d) Rule ৪ exempts names outright — *"ব্যক্তি, প্রতিষ্ঠান বা সংস্থার নাম এই নিয়মের আওতাভুক্ত নয়।"* Independently, স্টুডিও is well formed: initial conjunct per rule ২.৯ (cf. স্টেশন), short ই-কার per rule ২.১.

**wm-2 `অনিন্দ্য`**
(a) Correct. (b) Natural. (c) **No change.** (d) Proper name, exempt under rule ৪.

### Themes

**th-1 "Light" `আলো`**
(a) Correct — ও-কার per rule ২.৩. (b) Natural; the plain everyday word.
(c) **No change.**
(d) Right on both counts, and it sets up a clean pair with অন্ধকার.

**th-2 "Dark" `অন্ধকার`**
(a) Correct (তৎসম, unchanged per rule ১.১). (b) Natural and universally understood.
(c) **No change.**
(d) Worth one note: অন্ধকার carries a faint gloom that "dark mode" does not, and আঁধার would be more literary. But অন্ধকার is the plain word, it pairs with আলো, and swapping to ডার্ক would be a needless anglicism. Leave it.

**th-3 "High contrast" `উচ্চ বৈসাদৃশ্য`** → **changed**
(a) Spelling is correct — বৈসাদৃশ্য is a real dictionary headword. (b) **Stiff, and semantically wrong.**
(c) **`বেশি কনট্রাস্ট`**
(d) Two faults. First, বৈসাদৃশ্য means *dissimilarity, unlikeness* — an abstract comparison between two things — not the tonal contrast of a display. This is the classic dictionary-substitution error: a correct word for the wrong sense. Second, উচ্চ is a তৎসম register that clashes with the plain voice you have set everywhere else. কনট্রাস্ট is licensed by rule ২.৬ (বাংলায় প্রচলিত বিদেশি শব্দ … বাংলা ভাষার ধ্বনিপদ্ধতি-অনুযায়ী লিখতে হবে) and is the word Bangladeshi users actually say for a screen setting; বেশি is the plain everyday intensifier and matches বানাই, লুকিয়ে, মুছে ফেলুন. Prefer `বেশি কনট্রাস্ট` over your alternative `উচ্চ কনট্রাস্ট` precisely because it avoids the register clash. (কনট্রাস্ট is not a dictionary headword — flagged honestly — but rule ২.৬ covers it.)

### Colour names

All six are brand names, and doubly safe: rule ৪ exempts names from the spelling rules, and each is in any case spelled correctly.

**col-1 `মোহনা`** · **col-2 `জোয়ার`** · **col-3 `পলি`** · **col-4 `কাশ`** · **col-5 `লাল মাটি`** · **col-6 `বর্ষা`**
(a) All correct. পলি takes short ই-কার per rule ২.১; বর্ষা keeps ষ as an unchanged তৎসম per rule ১.১. (b) Evocative, which is what you want here.
(c) **No changes.**
(d) These are the strongest set in the brief — concrete, native, sensory, none of them translated from English. `লাল মাটি` is incidentally corroborated by the dictionary's own example sentence under রং: *"বর্ণ (লাল রং)"*.

### Buttons

**bt-1 "Save the entry" `লেখাটি সংরক্ষণ করুন`**
(a) Correct — সংরক্ষণ keeps ণ as a তৎসম, and ম → ং per rule ১.৪. (b) Formal, but standard.
(c) **No change.**
(d) সংরক্ষণ করুন is the established Bangla interface word for Save and is what Bangladeshi users meet everywhere else. It leans formal, and সেভ করুন is what people *say* — but সেভ is not in the Academy dictionary, so changing would trade a standard word for a weaker one. It also has to agree with ms-4 (`সংরক্ষিত হয়েছে`), and it does. Keep.

**bt-2 "Cancel" `বাতিল করুন`**
(a) Correct — বাতিল is a dictionary headword. (b) Plain and natural.
(c) **No change.** (d) Already right; the ordinary word everyone uses.

**bt-3 "Delete the file" `ফাইলটি মুছে ফেলুন`**
(a) Correct — ফাইল is a dictionary headword. (b) Natural, plain চলিত.
(c) **No change.**
(d) Already right. মুছে ফেলুন is warmer and clearer than মুছে দিন or ডিলিট করুন, and the compound verb carries the finality of "delete" properly.

**bt-4 "Try again" `আবার চেষ্টা করুন`**
(a) Correct. (b) Natural. (c) **No change.** (d) Already right — plain, and not a word-for-word calque.

**bt-5 "Copy the code" `কোডটি কপি করুন`**
(a) Correct — কপি is a dictionary headword. কোড is not, but is well formed and universally used. (b) Natural.
(c) **No change.**
(d) Already right. Resist অনুলিপি করুন: the Academy itself uses কপি (and lists সফট কপি), so অনুলিপি would be stiffer *and* less standard.

### Messages

**ms-1 "Couldn't save…"** → **changed**
Current: `সংরক্ষণ করা যায়নি। আপনার লেখা এখনও আছে — একটু পরে আবার চেষ্টা করুন।`
(a) One fault: **এখনও**. (b) Tone is good — calm, reassuring, not blaming the user.
(c) **`সংরক্ষণ করা যায়নি। আপনার লেখা এখনো আছে — একটু পরে আবার চেষ্টা করুন।`**
(d) এখনও → এখনো only. The Academy dictionary makes এখনও a bare cross-reference ("দ্র এখনো") to the full entry at এখনো. Everything else is right: the em dash is a proper Bangla যতিচিহ্ন, there is no space before the দাঁড়ি, and "একটু পরে" is exactly the plain, human hedge the English "in a moment" wants.

**ms-2 "That file is too large…"** → **changed**
Current: `ফাইলটি অনেক বড়। সর্বোচ্চ সীমা ১০ মেগাবাইট।`
(a) One fault: **বড়**. (b) Slightly officialese in the second sentence.
(c) **`ফাইলটি অনেক বড়ো। সর্বোচ্চ ১০ মেগাবাইট।`**
(d) Two edits. **বড় → বড়ো**: the Academy dictionary's headword is বড়ো; বড় has no entry. This follows rule ২.৩, whose own example list is "কালো, খাটো, ছোটো, ভালো". **সর্বোচ্চ সীমা → সর্বোচ্চ**: a doublet — সর্বোচ্চ already carries "maximum", so সীমা only adds bureaucratic weight. This second edit is tone, not orthography; keep সীমা if you prefer the fuller phrase. `১০ মেগাবাইট` is right as it stands: Bengali numerals match the Academy's own practice for measurements, and মেগাবাইট is a dictionary headword, so it beats "MB" inside a Bangla sentence.

**ms-3 "Nothing here yet…"** → **changed**
Current: `এখনও কিছু নেই। শুরু করতে প্রথম লেখাটি যোগ করুন।`
(a) One fault: **এখনও**. (b) Natural and inviting.
(c) **`এখনো কিছু নেই। শুরু করতে প্রথম লেখাটি যোগ করুন।`**
(d) এখনো only — same ruling as ms-1. "শুরু করতে … যোগ করুন" is a good idiomatic ordering, not an English word order dragged across.

**ms-4 "Saved" `সংরক্ষিত হয়েছে`**
(a) Correct. (b) Slightly formal but appropriate.
(c) **No change.**
(d) Grammatically clean and agrees with bt-1's সংরক্ষণ করুন, which matters more than shaving a syllable. `সংরক্ষিত` alone would be crisper for a brief toast — an optional tightening, not a correction.

### Voice sample

**vc-1** → **changed**
Current: `আমি ছোট, যত্নে গড়া সফটওয়্যার বানাই। কোনো কিছুর সীমা থাকলে সেটা এখানেই লেখা থাকবে — লুকিয়ে রাখা হবে না।`
(a) One fault: **ছোট**. (b) **Excellent** — the best-judged string in the set.
(c) **`আমি ছোটো, যত্নে গড়া সফটওয়্যার বানাই। কোনো কিছুর সীমা থাকলে সেটা এখানেই লেখা থাকবে — লুকিয়ে রাখা হবে না।`**
(d) **ছোট → ছোটো** is the single change, and it is doubly sourced: rule ২.৩ names ছোটো explicitly in its example list ("কালো, খাটো, **ছোটো**, ভালো"), and ছোটো is the dictionary headword while ছোট has no entry. Note rule ২.৩ is permissive ("লেখা যেতে পারে"), so ছোট is not an error — but ছোটো is the Academy's own listed form, and since you have asked for Academy-approved spelling, take it. It also then agrees with বড়ো in ms-2.

Everything else here is right and should be protected in review:
- **সফটওয়্যার** — the dictionary's exact headword spelling, hasanta-free per rule ২.১০.
- **কোনো** — correctly the indefinite form.
- **বানাই** — plain চলিত. Far better than তৈরি করি or নির্মাণ করি, which would have made a one-person studio sound like a ministry.
- **এখানেই** — নিশ্চয়ার্থক ই attached in full, per rule ৩.৫ (আজই, এখনই).
- The Bangla drops the English's "that is information, not a confession" and lands on "লুকিয়ে রাখা হবে না". That is the right call: it carries the same meaning in idiomatic Bangla instead of translating the epigram word for word. This sentence should be the register benchmark for everything else in the system.

### Guidebook chapter titles

**gb-1 `স্বাগতম`** · **gb-2 `নাম`** · **gb-3 `চিহ্ন`**
(a) All correct. (b) Natural. (c) **No changes.** (d) স্বাগতম is the ordinary Bangla welcome; নাম and চিহ্ন are plain native monosyllables that match the guidebook's quiet register.

**gb-4 `রং`**
(a) **Correct** — and specifically the form the Academy prescribes. (b) Natural.
(c) **No change.**
(d) Confirmed twice over: rule ২.৪ names রং in its example list, and রং is the dictionary headword while রঙ has no entry. You got this one exactly right. Only switch to রঙ when a vowel follows (রঙিন, রঙের).

**gb-5 `হরফ`**
(a) Correct — dictionary headword. (b) Natural and warm.
(c) **No change.**
(d) A genuinely good choice: হরফ is the living Bangla word for letterform, and it beats both টাইপোগ্রাফি (anglicism) and অক্ষরবিন্যাস (stiff).

**gb-6 `ফাঁক ও আকার`**
(a) Correct — চন্দ্রবিন্দু on ফাঁক is the lexical spelling. (b) Natural.
(c) **No change.** (d) ফাঁক is plain, physical and exactly right for "space"; it avoids the abstract স্পেসিং.

**gb-7 `উপাদান`** · **gb-8 `গতি`**
(a) Correct. (b) Natural. (c) **No changes.** (d) Both plain তৎসম words in everyday use. উপাদান is slightly abstract for UI components but is the standard rendering and reads cleanly.

**gb-9 `কণ্ঠস্বর`**
(a) Correct — dictionary headword; ণ is right here by ণ-ত্ব বিধান (তৎসম). (b) Acceptable.
(c) **No change.**
(d) It is correct and understood. One optional note: কণ্ঠস্বর leans towards the physical speaking voice, whereas plain **কণ্ঠ** is what Bangla idiomatically uses for a writer's or brand's distinctive voice ("নিজস্ব কণ্ঠ"). That is a taste call, not a correction — I have not changed it.

**gb-10 `যা এই ব্যবস্থা করে না`** → **changed**
(a) Spelling correct — ব্যবস্থা is a dictionary headword. (b) **Your instinct is right: bureaucratic.**
(c) **`যা এই পদ্ধতি করে না`**
(d) ব্যবস্থা is correct in the abstract but in Bangladeshi usage it is administrative — it lives in "ব্যবস্থা নেওয়া" (to take measures), "আইনগত ব্যবস্থা", official notices. It imports exactly the institutional tone this chapter is trying to disown. **পদ্ধতি** is an Academy dictionary headword, is the ordinary Bangla for "system" in technical writing (as in সংখ্যা পদ্ধতি, "number system"), and carries no administrative shadow. It keeps the sentence's plain shape and its honesty. If you would rather stay closer to spoken usage, `যা এই সিস্টেম করে না` is what designers in Dhaka would actually say — but সিস্টেম is not a dictionary headword, so পদ্ধতি is the Academy-safe choice.

---

## Recommended final strings

**Strings reviewed: 27 · changed: 6 · unchanged: 21**

| id | current | recommended | changed | reason |
|---|---|---|---|---|
| wm-1 | অনিন্দ্য স্টুডিও | অনিন্দ্য স্টুডিও | no | Proper name, exempt under rule ৪; স্টুডিও well formed per rules ২.১ and ২.৯ |
| wm-2 | অনিন্দ্য | অনিন্দ্য | no | Proper name, exempt under rule ৪ |
| th-1 | আলো | আলো | no | Correct ও-কার per rule ২.৩; plain everyday word |
| th-2 | অন্ধকার | অন্ধকার | no | Correct তৎসম spelling; plain and universally understood |
| th-3 | উচ্চ বৈসাদৃশ্য | বেশি কনট্রাস্ট | yes | বৈসাদৃশ্য means "dissimilarity", not display contrast; loanword licensed by rule ২.৬; বেশি avoids the তৎসম register clash |
| col-1 | মোহনা | মোহনা | no | Brand name, exempt under rule ৪; spelling correct |
| col-2 | জোয়ার | জোয়ার | no | Brand name, exempt under rule ৪; spelling correct |
| col-3 | পলি | পলি | no | Correct short ই-কার per rule ২.১ |
| col-4 | কাশ | কাশ | no | Brand name, exempt under rule ৪; spelling correct |
| col-5 | লাল মাটি | লাল মাটি | no | Correct; matches the dictionary's own example "লাল রং" |
| col-6 | বর্ষা | বর্ষা | no | তৎসম retained unchanged per rule ১.১ |
| bt-1 | লেখাটি সংরক্ষণ করুন | লেখাটি সংরক্ষণ করুন | no | Correct; established Bangla UI term for Save and agrees with ms-4 |
| bt-2 | বাতিল করুন | বাতিল করুন | no | বাতিল is a dictionary headword; plain and universal |
| bt-3 | ফাইলটি মুছে ফেলুন | ফাইলটি মুছে ফেলুন | no | ফাইল is a dictionary headword; মুছে ফেলুন is plain চলিত |
| bt-4 | আবার চেষ্টা করুন | আবার চেষ্টা করুন | no | Correct and natural; not a calque |
| bt-5 | কোডটি কপি করুন | কোডটি কপি করুন | no | কপি is a dictionary headword; অনুলিপি would be stiffer and less standard |
| ms-1 | সংরক্ষণ করা যায়নি। আপনার লেখা এখনও আছে — একটু পরে আবার চেষ্টা করুন। | সংরক্ষণ করা যায়নি। আপনার লেখা এখনো আছে — একটু পরে আবার চেষ্টা করুন। | yes | এখনও is only a cross-reference ("দ্র এখনো") in the Academy dictionary; এখনো holds the entry |
| ms-2 | ফাইলটি অনেক বড়। সর্বোচ্চ সীমা ১০ মেগাবাইট। | ফাইলটি অনেক বড়ো। সর্বোচ্চ ১০ মেগাবাইট। | yes | বড়ো is the dictionary headword (বড় has no entry), per rule ২.৩; "সর্বোচ্চ সীমা" is a doublet |
| ms-3 | এখনও কিছু নেই। শুরু করতে প্রথম লেখাটি যোগ করুন। | এখনো কিছু নেই। শুরু করতে প্রথম লেখাটি যোগ করুন। | yes | Same এখনো ruling as ms-1 |
| ms-4 | সংরক্ষিত হয়েছে | সংরক্ষিত হয়েছে | no | Correct and agrees with bt-1; "সংরক্ষিত" alone is an optional tightening only |
| vc-1 | আমি ছোট, যত্নে গড়া সফটওয়্যার বানাই। কোনো কিছুর সীমা থাকলে সেটা এখানেই লেখা থাকবে — লুকিয়ে রাখা হবে না। | আমি ছোটো, যত্নে গড়া সফটওয়্যার বানাই। কোনো কিছুর সীমা থাকলে সেটা এখানেই লেখা থাকবে — লুকিয়ে রাখা হবে না। | yes | ছোটো is named in rule ২.৩'s example list and is the dictionary headword; ছোট has no entry |
| gb-1 | স্বাগতম | স্বাগতম | no | Correct; ordinary Bangla welcome |
| gb-2 | নাম | নাম | no | Correct; plain native word |
| gb-3 | চিহ্ন | চিহ্ন | no | Correct; plain native word |
| gb-4 | রং | রং | no | Confirmed correct by rule ২.৪ and the dictionary headword; রঙ has no entry |
| gb-5 | হরফ | হরফ | no | Dictionary headword; warmer and plainer than টাইপোগ্রাফি |
| gb-6 | ফাঁক ও আকার | ফাঁক ও আকার | no | Correct; ফাঁক is plain and physical, avoids abstract স্পেসিং |
| gb-7 | উপাদান | উপাদান | no | Correct তৎসম; standard rendering of "components" |
| gb-8 | গতি | গতি | no | Correct; plain everyday word |
| gb-9 | কণ্ঠস্বর | কণ্ঠস্বর | no | Correct (ণ by ণ-ত্ব বিধান); plain কণ্ঠ is an optional idiomatic alternative, not a correction |
| gb-10 | যা এই ব্যবস্থা করে না | যা এই পদ্ধতি করে না | yes | ব্যবস্থা reads administrative ("ব্যবস্থা নেওয়া"); পদ্ধতি is a dictionary headword and the plain Bangla for "system" |

---

## House rules to carry forward

1. **এখনো, কখনো, তখনো** with ও-কার — but **আরও** with the full ও. The asymmetry is the Academy's, and it is evidenced.
2. **কোনো** = any/some · **কোন** = which. Never interchange.
3. **রং** standing alone or word-final; **রঙ** only before a vowel (রঙিন, রঙের).
4. **ছোটো, বড়ো, ভালো, কালো, মতো, হলো, হতো** — ও-কার, per rule ২.৩.
5. No **ণ** in any non-Sanskrit word: ধরন, রানি, সোনা, ঝরনা, ঠান্ডা.
6. Avoid the hasanta wherever it is not needed: **সফটওয়্যার**, not সফ্টওয়্যার.
7. Established loanwords are standard: **কপি, ফাইল, সফটওয়্যার, মেগাবাইট**. Do not "correct" them into অনুলিপি or নথি.
8. **চলিত throughout.** No সাধু forms anywhere in the product.
9. **Bengali numerals** in prose and measurements; Western digits only where a string must be copied literally.
10. **`।`** to end a statement, **`?`** to ask, **`!`** to exclaim. No space before `।`, one space after, and never let `।` begin a line.

---

## Sources

**Primary**
- বাংলা একাডেমি, *প্রমিত বাংলা বানানের নিয়ম*, পরিমার্জিত সংস্করণ ২০১২ (পুনর্মুদ্রণ ২০১৫) — <https://archive.org/details/bangla-academy-promito-bangla-bananer-niyom-2015>
- বাংলা একাডেমি, *আধুনিক বাংলা অভিধান* (searchable page scans) — <https://baabo.jothartho.com/>
  - এখনো / এখনও, p. 236 · আরও, p. 164 · আরো, p. 166 · কোন, p. 337 · কোনো, p. 338 · রং, p. 1156 · সফটওয়্যার ও সফট কপি, p. 1287 · ফাইল, p. 895 · কপি, p. 265 · মেগাবাইট, p. 1130

**Secondary — typography and punctuation**
- W3C, *Bengali Layout Requirements* — <https://w3c.github.io/iip/bengali/> and <https://www.w3.org/TR/beng-lreq/>
- W3C / Richard Ishida, *Bengali/Bangla orthography notes* — <https://r12a.github.io/scripts/beng/bn.html>
- বাংলা উইকিপিডিয়া, *যতিচিহ্ন* — <https://bn.wikipedia.org/wiki/যতিচিহ্ন>
- বাংলা উইকিপিডিয়া, *উইকিপিডিয়া:বাংলা বানানের নিয়ম* — <https://bn.wikipedia.org/wiki/উইকিপিডিয়া:বাংলা_বানানের_নিয়ম>
- বাংলা উইকিপিডিয়া, *বাংলা সংখ্যা পদ্ধতি* — <https://bn.wikipedia.org/wiki/বাংলা_সংখ্যা_পদ্ধতি>

**Explicitly unverified**
- Any Bangla Academy edition later than 2012 — none found as at 14 August 2026.
- Any Academy rule on ৎ (খণ্ড ত) or চন্দ্রবিন্দু — no such rule exists in the 2012 document; both are lexical.
- Any Academy or published style-guide rule on Bengali vs Western numerals — none found; the recommendation above rests on the Academy's own printing practice plus my editorial judgement for code contexts.
- The `GitHub-এ` hyphenation convention for Latin words taking Bangla case-endings — widespread practice, no formal citation found.
- তখনো as a dictionary headword — neither তখনো nor তখনও has an entry; the recommendation is inferred from এখনো and কখনো.
