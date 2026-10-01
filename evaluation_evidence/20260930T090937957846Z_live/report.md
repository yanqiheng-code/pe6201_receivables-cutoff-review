# Model Evaluation Report

Development dataset only. Not an unseen evaluation.

Model: openai/gpt-4.1-mini
Selected cases: 20
Valid predictions: 20
Correct labels: 20 / 20
Errors flagged: 6 / 6
False flags on normal cases: 0
Abstentions: 2
Technical failures or not run: 0
OpenRouter reported API cost: USD 0.024426
Cost incomplete: False

Cost comes from OpenRouter usage.cost when available; missing cost is unknown, not zero. Unknown-cost failed requests may still incur charges. Evidence IDs are validated, but reasoning quality requires human review.

| Case | Expected | Predicted | Label correct |
|---|---|---|---|
| DEV-01 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-02 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-03 | Premature recognition | Premature recognition | True |
| DEV-04 | Delayed or omitted recognition | Delayed or omitted recognition | True |
| DEV-05 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-06 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-07 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-08 | Premature recognition | Premature recognition | True |
| DEV-09 | Delayed or omitted recognition | Delayed or omitted recognition | True |
| DEV-10 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-11 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-12 | Additional evidence required | Additional evidence required | True |
| DEV-13 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-14 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-15 | Premature recognition | Premature recognition | True |
| DEV-16 | Delayed or omitted recognition | Delayed or omitted recognition | True |
| DEV-17 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-18 | No cut-off exception identified | No cut-off exception identified | True |
| DEV-19 | Additional evidence required | Additional evidence required | True |
| DEV-20 | No cut-off exception identified | No cut-off exception identified | True |

## Amount Accuracy

| Metric | Result |
|---|---|
| Classification accuracy | 20/20 (100.0%) |
| Amount-field accuracy | 14/20 (70.0%) |
| Error amount accuracy | 6/6 (100.0%) |

Amount-field accuracy compares the amount field on every selected case, including expected null values. Zero means an established absence of a difference; null means undetermined. They are not interchangeable. Missing predictions count as incorrect. Error amount accuracy covers only planted cut-off errors and does not replace classification accuracy.

| Case | Expected difference (CNY) | Predicted difference (CNY) | Amount correct |
|---|---:|---:|---|
| DEV-01 | 0 | 0 | True |
| DEV-02 | 0 | null | False |
| DEV-03 | 10000 | 10000 | True |
| DEV-04 | 10000 | 10000 | True |
| DEV-05 | 0 | null | False |
| DEV-06 | 0 | null | False |
| DEV-07 | 0 | 0 | True |
| DEV-08 | 10000 | 10000 | True |
| DEV-09 | 10000 | 10000 | True |
| DEV-10 | 0 | 0 | True |
| DEV-11 | 0 | null | False |
| DEV-12 | null | null | True |
| DEV-13 | 0 | 0 | True |
| DEV-14 | 0 | null | False |
| DEV-15 | 10000 | 10000 | True |
| DEV-16 | 10000 | 10000 | True |
| DEV-17 | 0 | 0 | True |
| DEV-18 | 0 | null | False |
| DEV-19 | null | null | True |
| DEV-20 | 0 | 0 | True |
