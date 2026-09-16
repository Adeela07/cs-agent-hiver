# Report: AppleSupport AI Customer Support Agent

## Problem Framing
Built for AppleSupport (chosen for high tweet volume in the dataset). "Good" 
means: correctly identifying what a customer needs (10-intent taxonomy derived 
from manually reviewing ~106 real customer messages), drafting a reply grounded 
in real historical AppleSupport response patterns (via BM25 retrieval over 
historical threads), and conservatively escalating anything outside a narrow 
safe zone (only `how_to` intents are auto-handled; everything else — billing, 
data loss, complaints, unclear messages — goes to a human).

What I chose not to build: a UI/live Twitter integration, multi-lingual support, 
sentiment-based escalation beyond keyword/hedging checks, and a fine-tuned 
classifier (used a general LLM — Gemini — with a prompt-based classifier instead).

## Intent Taxonomy
Derived from manual review of ~106 real messages (see eval/intent_sample.csv):
data_loss, hardware_complaint, battery_issue, software_bug, device_troubleshooting, 
billing_account, how_to, general_complaint, unclear, other. 
Full definitions in eval/intent_spec.md.

## Baselines
- Trivial baseline: always predict the majority intent (software_bug, ~40% of 
  the sample) and always escalate. 
- Simple baseline: keyword-matching rules per intent + canned template replies.
[Fill in actual comparison numbers if you have them, or note: "Baseline 
comparison not completed given time constraints — noted as next step."]

## Results
[Insert your actual classification_report and routing metrics output here from 
step10_metrics.py, once run on a real-sized sample]

## What's Misleading About My Headline Number
An early run against only 7 examples showed 100% accuracy across the board — 
this was a labeling pipeline bug (most rows lacked a filled-in label), not real 
performance. This is a concrete illustration of why small eval sets are 
dangerous: perfect scores on tiny samples reflect sample size, not quality. 
[Update this once you have your real ~100-example run — note the actual 
per-intent performance variance, and flag that the golden set was drawn from 
the SAME labeled pool used to build the intent taxonomy, which likely inflates 
performance since the model/human found these categories from the same data.]

## Failure Analysis (Top Failure Modes)
1. Sparse messages: ~1% of customer tweets have no usable text after removing 
   @mentions/links (e.g. photo-only tweets) — unclassifiable without image input.
2. Router initially auto-handled a draft where the model itself said "I am 
   unsure how to answer this" — confidence score alone didn't catch low-quality 
   drafts; fixed by adding a hedging-language check.
3. `unclear` and `general_complaint` intents are the hardest to distinguish 
   consistently — both involve vague or emotional language.
4. Golden eval set was drawn from the same sample used to define the intent 
   taxonomy — likely overstates real-world performance on unseen messages.
5. [Add one more real example if you have one from testing]

## Decision Log
- Switched from Claude API to Google Gemini free tier (gemini-3.6-flash) for 
  cost reasons — assignment explicitly permits any LLM API.
- Used BM25 (rank_bm25) instead of embeddings for retrieval grounding — no 
  embedding API needed, works fully offline once indexed.
- Only `how_to` intent is auto-handled; all others escalate by default — 
  erring toward caution given real customer impact.
- Excluded threads with <5 characters of cleaned text (near-empty after 
  stripping mentions/links) — ~1% of data, unclassifiable.
- Intent taxonomy built from manual review, not imposed categories — stopped 
  labeling at ~106 examples once 40+ consecutive messages introduced no new 
  category (saturation).
- Router checks for both explicit risk language (refund, guarantee, etc.) AND 
  model self-reported uncertainty ("I am unsure") — added after discovering 
  the latter gap during testing.
- Golden eval set reused the intent-labeling sample rather than a fresh sample, 
  due to time constraints — disclosed as a limitation above.

## What I'd Do With One More Week
- Build a genuinely held-out golden eval set (not overlapping with intent-taxonomy 
  training data).
- Implement the LLM-as-judge rubric for reply quality with human-agreement 
  validation (not completed in this submission).
- Compare against a real keyword-based baseline with actual numbers.
- Fine-tune router thresholds using precision/recall tradeoffs on a larger set.
- Add multi-turn context awareness (currently only classifies/drafts from the 
  opening message).
