# Semantic review ledger

`review-ledger.jsonl` records individually checked fields with level, kind, stable entry ID, language, field, reviewer disclosure, source hash and translation hash. A record becomes stale if its source or translation changes. `python scripts/review_progress.py` recomputes strict remaining counts and the next unreviewed fields. It performs no language review itself.

Scope includes Bengali and Nepali meanings, grammar formation/guidance, and each example sentence. Historical authored glosses and machine-draft labels are not automatically counted as reviewed. The strict denominator includes formation/guidance and previously authored fields, so it is larger than the older draft-only estimate.

Resume N5 first, then N4, N3, N2, N1. Inspect the source and translation for the queued fields, record genuine semantic checks, correct errors using the entry/example/grammar/source override files, rebuild locales, and bind evidence to the final rebuilt content. Do not stamp fields simply because a test or translation model accepted them.

The first recorded pass checks N5 vocabulary meanings 0–99, vocabulary examples 0–9, and the first five grammar records. Fixes distinguish idiomatic 青い from literal blue, preserve negative 開かなかった, and restore Sunday, night-time and older-sister roles in grammar examples. English glosses for 上げる, 一日（いちにち） and 忙しい were also corrected; source change notes are preserved. JMdict 1519290 from the licensed Japanese Language Data snapshot supports the primary busy/occupied/hectic sense.

These are AI-assisted semantic checks, not native-speaker or teacher certification. Native-speaker review has not been performed. Do not remove draft labels globally or announce full completion from this partial ledger.
