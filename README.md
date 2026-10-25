# Nihongo Path
Mobile-first Japanese study app, N5–N1, by Hossain Najmul.

[Live app](https://mr04nazmul.github.io/nihongo-path/) · [Coverage and study resources](https://mr04nazmul.github.io/nihongo-path/coverage.html)

Serve `dist/` with any static server. No runtime/build dependencies. Public GitHub repository with GitHub Pages Actions deployment.

## Content
| Level | Vocabulary | Grammar entries | Kanji |
| --- | ---: | ---: | ---: |
| N5 | 696 | 119 | 84 |
| N4 | 636 | 156 | 169 |
| N3 | 1,700 | 166 | 387 |
| N2 | 1,791 | 207 | 398 |
| N1 | 3,168 | 225 | 1,345 |
| Total | 7,991 | 873 | 2,383 |

Every OpenJLPT N5–N1 entry is included. A second inventory, Japanese Language Data, is audited entry by entry: 595 grammar records and 2,211 Kanji classifications mapped; 8,272 of 8,293 vocabulary classifications mapped to validated dictionary entries. The remaining 21 are quarantined with reasons. Alternate readings and grammar forms can have separate entries; counts are not unique exam requirements. Level conflicts retain the app's existing level.

JLPT publishes no exhaustive word/grammar/Kanji specification. This is a broad community study collection, not a guarantee of every possible exam question. Source grammar drafts still require teacher review. Official reading/listening practice links are provided on the coverage page, rather than claiming flashcards are a full mock exam.

Data is CC BY-SA 4.0 with upstream attribution. See `dist/data/NOTICE.md`, `SUPPLEMENT-ATTRIBUTION.md` and licenses. `coverage.json` records exact source revisions and every inclusion/exclusion. Dictionary snapshot versions and maintenance requirements are recorded in the upstream attribution. Check upstream revisions and refresh regularly; an audit date is not a dictionary publication date.

## Languages
English sources are available throughout. Bengali/Nepali meanings are authored for the original N5–N2 grammar and 123 N1 base grammar entries. Additional grammar, vocabulary, Kanji and examples include offline SMaLL-100 automatic drafts with curated core corrections. Draft meanings and examples are labeled; native-speaker review remains outstanding. Japanese grammar syntax is preserved when localizing formation labels.

## Features
Five separate level pages, grammar/vocabulary/Kanji tabs, multilingual search (including alternate spellings), saved lessons, learned progress, flashcards, quizzes, responsive bottom navigation and light/dark themes. Progress stays in the browser. Existing IDs are preserved.

Daily words have bundled Japanese MP3 files covering every calendar day in all five levels. Other text uses the device's Japanese voice with visible playback/error controls. Actual iPhone hardware testing remains outstanding.

## Ads
Publisher `ca-pub-3728341118830943`, responsive slot `2007625275`. Auto ads and the responsive unit remain configured. The site is public; Google ownership/review and Vignette settings must be completed in AdSense before eligible ad delivery. Ad display and frequency are determined by Google. Navigation is never blocked waiting for an ad.

## Rebuild and validation
Clone the two licensed source repositories and run:

```sh
python scripts/expand_n1.py /path/to/OpenJLPT /path/to/japanese-language-data
python scripts/translate_content.py
python scripts/assemble_locales.py
python scripts/build_pages.py
python scripts/build_coverage.py
python scripts/build_daily_audio.py
python -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.cjs
```

The merge is idempotent and retains existing entries. Translation needs `ctranslate2` and `sentencepiece`, plus the MIT-licensed `solavr/small100-ctranslate2-int8` model in `/workspace/scratch/small100`. Its cache is resumable and intentionally untracked. Audio generation needs `edge-tts`; generation uses a network service, playback of bundled daily clips does not. Generated JSON and MP3 assets are committed, so these tools are not needed to deploy.
