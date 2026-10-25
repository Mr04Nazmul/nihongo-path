# Nihongo Path
Mobile-first Japanese study app, N5–N2, by Hossain Najmul.

Serve `dist/` with any static server. No runtime/build dependencies. GitHub Pages workflow included. The current hosted source repository is managed by Sites; the user GitHub repository is Mr04Nazmul/nihongo-path.

## Content
| Level | Vocabulary | Grammar | Kanji |
| --- | ---: | ---: | ---: |
| N5 | 679 | 103 | 84 |
| N4 | 630 | 120 | 169 |
| N3 | 1,671 | 106 | 387 |
| N2 | 1,786 | 148 | 398 |
| Total | 4,766 | 477 | 1,038 |

OpenJLPT supplies the base dataset. Japanese Language Data supplies curated additional practice topics and dictionary-validated vocabulary additions. Data is CC BY-SA 4.0 with upstream per-field attribution; see `dist/data/NOTICE.md`, `SUPPLEMENT-ATTRIBUTION.md` and licenses. Level assignments are community approximations, not an official/exhaustive JLPT list. Supplemental source grammar remains marked as draft upstream.

## Localization
All grammar glosses have authored Bangla/Nepali equivalents in `translations/grammar-n*.tsv`. Formation labels are localized while Japanese syntax is retained. N5 first grammar examples and selected additional examples have authored translations. Other vocabulary, kanji glosses and examples use offline SMaLL-100 drafts, with curated core-gloss corrections. Full native-speaker review is still outstanding. Original Japanese and English remain accessible. Automatic example drafts are labeled.

`translation-cache.json` is the resumable translation cache. `scripts/translate_content.py` uses a locally downloaded MIT-licensed SMaLL-100 CTranslate2 model. `scripts/assemble_locales.py` creates bundled locales and the coverage audit. Model weights are not part of this repository. Source-enrichment scripts require the documented upstream source checkouts; do not run the initial importer against finalized data unless intentionally rebuilding all content.

## App features
Language switch, responsive bottom navigation, light/dark mode, grammar/vocabulary/kanji search, bookmarks, learned progress, flashcards, localized vocabulary quizzes and Japanese device speech. Progress is browser-local. No account/cloud sync.

## Advertising
The owner's supplied publisher ID is configured in `dist/ads-config.js`. Auto ads code, account meta tag, ads.txt, a reserved placement area, privacy page and in-app ad setup details are included. The dedicated responsive ad unit is Nihongo Path - Responsive Lessons, slot 2007625275. Google approval/Auto ads account settings are not verified. The current site remains owner-private, so public publication and Google review are required before real ad delivery can be expected. No impressions or revenue are claimed.

## Audio playback fix
Daily words use bundled Japanese MP3 clips (first 32 word positions per level cover every calendar day). `scripts/build_daily_audio.py` pre-renders them; there is no third-party speech request during playback. Other lesson text uses native Japanese speech with explicit voice selection, a retained utterance, synchronous user-tap initiation, playback feedback and actionable errors. Blocked media presents native controls. Repeated taps stop playback. Actual iPhone hardware testing remains outstanding.

Validate the speech controller with `node --test tests/speech.test.cjs`.

## Level pages and between-page ads
`lessons.html` is the level catalog. N5/N4/N3/N2 each have an actual HTML page (`n5.html` through `n2.html`) containing Grammar, Vocabulary and Kanji links. `?section=vocab` and `?section=kanji` can be shared/bookmarked directly. Browser back/forward and full-page links work normally; content is never blocked waiting for an ad.

The existing Auto ads code is included on every generated page. Normal links are eligible for Google-managed vignette ads once the publisher enables Vignette ads under AdSense → Ads → site → Overlay formats and the site is approved/public. This change does not claim to enable an account-side setting. No custom fake interstitial, ad-click requirement or guaranteed ad on every navigation is implemented. AdSense determines inventory and frequency.

Run `python scripts/build_pages.py` after changing the shared HTML shell.
