# Semantic review ledger

`review-ledger.jsonl` records individually checked fields with level, kind, stable entry ID, language, field, reviewer disclosure, source hash and translation hash. A record becomes stale if its source or translation changes. `python scripts/review_progress.py` recomputes strict remaining counts and the next unreviewed fields. It performs no language review itself.

Scope includes Bengali and Nepali meanings, grammar formation/guidance, and each example sentence. Historical authored glosses and machine-draft labels are not automatically counted as reviewed. The strict denominator includes formation/guidance and previously authored fields, so it is larger than the older draft-only estimate.

Resume N5 first, then N4, N3, N2, N1. Inspect the source and translation for the queued fields, record genuine semantic checks, correct errors using the entry/example/grammar/source override files, rebuild locales, and bind evidence to the final rebuilt content. Do not stamp fields simply because a test or translation model accepted them.

The first recorded pass checks N5 vocabulary meanings 0–99, vocabulary examples 0–9, and the first five grammar records. Fixes distinguish idiomatic 青い from literal blue, preserve negative 開かなかった, and restore Sunday, night-time and older-sister roles in grammar examples. English glosses for 上げる, 一日（いちにち） and 忙しい were also corrected; source change notes are preserved. JMdict 1519290 from the licensed Japanese Language Data snapshot supports the primary busy/occupied/hectic sense.

These are AI-assisted semantic checks, not native-speaker or teacher certification. Native-speaker review has not been performed. Do not remove draft labels globally or announce full completion from this partial ledger.

## Second semantic pass (2026-10-26)

Reviewed 152 additional sentence fields for N5 vocabulary indices 10–49 (76 examples in each language), with hash-bound evidence in the ledger. Japanese resolves source differences: 飴 example does not specify a girl; 姉/兄 are older siblings; 姉 example specifies a male child and pounds, not kilograms; 甘い is leniency rather than sugar; いつも…わけではない is partial negation. アソコ is a euphemism in its medical example. ダックスフント・ソーセージ is retained literally as the source sausage name, not translated as a pet. This is AI semantic review, not native-speaker certification. Remaining fields are still pending.

## Revised fields

A correction to a previously checked field appends a new hash-bound record, retaining the older record as history. The last record for each level/kind/ID/language/field is the current evidence, matching `review_progress.py`. A superseded record may correctly fail validation against the current translation; it does not count as a second reviewed field. Tests validate every current record and retain source/translation invalidation checks. The 2026-10-28 corridor correction refines two Nepali examples from veranda terminology to indoor corridor terminology.

## Explicit example replacements (2026-10-29, pass086)

Some N5 examples could not support a single defensible translation because a participant, parental side, activity or object was omitted, or because the example taught a different headword sense. `example-replacements.json` preserves each superseded Japanese/English example, its attribution and source IDs, both former translations, the exact source commit, and the replacement with its semantic-review basis. These are newly authored teaching examples, not recovered original context or native-speaker corrections. Source IDs in the archive continue to refer to the original sentences; they are not attached to the new sentences.

The replacements explicitly state relationships, transport choices, time/cost, or destination negation. The aunt headword uses a descriptive definition distinguishing 伯母 from 叔母. Old unresolved records and their field evidence remain available, with a resolution referring to the active replacement. Original-context limitations remain documented. Fifty-two new ledger records cover 24 previously pending fields and 28 revised or changed-source fields. Current N5 field coverage means an AI-assisted semantic pass of this repository's scoped fields; it does not certify exhaustive JLPT coverage or native-speaker review. Remaining levels are still pending.
