# Model Evaluation Report

Separately generated synthetic test set; same author as development data. Limited external validity.

Method: openai/gpt-4.1-mini
Selected cases: 80
Valid predictions: 80
Correct labels: 71 / 80
Errors flagged: 12 / 12
False flags on normal cases: 6
Abstentions: 11
Technical failures or not run: 0
OpenRouter reported API cost: USD 0.067893
Cost incomplete: False

Cost comes from OpenRouter usage.cost when available; missing cost is unknown, not zero. Unknown-cost failed requests may still incur charges. Evidence IDs are validated, but reasoning quality requires human review.

| Case | Expected | Predicted | Label correct |
|---|---|---|---|
| TEST-001 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-002 | Delayed or omitted recognition | Delayed or omitted recognition | True |
| TEST-003 | Additional evidence required | Additional evidence required | True |
| TEST-004 | No cut-off exception identified | Delayed or omitted recognition | False |
| TEST-005 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-006 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-007 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-008 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-009 | Additional evidence required | Additional evidence required | True |
| TEST-010 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-011 | Premature recognition | Premature recognition | True |
| TEST-012 | Additional evidence required | Additional evidence required | True |
| TEST-013 | No cut-off exception identified | Additional evidence required | False |
| TEST-014 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-015 | Additional evidence required | Additional evidence required | True |
| TEST-016 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-017 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-018 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-019 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-020 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-021 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-022 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-023 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-024 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-025 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-026 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-027 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-028 | No cut-off exception identified | Additional evidence required | False |
| TEST-029 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-030 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-031 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-032 | Delayed or omitted recognition | Delayed or omitted recognition | True |
| TEST-033 | Additional evidence required | Additional evidence required | True |
| TEST-034 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-035 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-036 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-037 | Premature recognition | Premature recognition | True |
| TEST-038 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-039 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-040 | Delayed or omitted recognition | Delayed or omitted recognition | True |
| TEST-041 | Additional evidence required | Additional evidence required | True |
| TEST-042 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-043 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-044 | Delayed or omitted recognition | Delayed or omitted recognition | True |
| TEST-045 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-046 | No cut-off exception identified | Premature recognition | False |
| TEST-047 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-048 | No cut-off exception identified | Delayed or omitted recognition | False |
| TEST-049 | Premature recognition | Premature recognition | True |
| TEST-050 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-051 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-052 | Additional evidence required | Additional evidence required | True |
| TEST-053 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-054 | Delayed or omitted recognition | Delayed or omitted recognition | True |
| TEST-055 | Premature recognition | Premature recognition | True |
| TEST-056 | No cut-off exception identified | Premature recognition | False |
| TEST-057 | No cut-off exception identified | Additional evidence required | False |
| TEST-058 | No cut-off exception identified | Delayed or omitted recognition | False |
| TEST-059 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-060 | Delayed or omitted recognition | Delayed or omitted recognition | True |
| TEST-061 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-062 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-063 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-064 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-065 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-066 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-067 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-068 | Premature recognition | Premature recognition | True |
| TEST-069 | No cut-off exception identified | Premature recognition | False |
| TEST-070 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-071 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-072 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-073 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-074 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-075 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-076 | Additional evidence required | Additional evidence required | True |
| TEST-077 | Premature recognition | Premature recognition | True |
| TEST-078 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-079 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-080 | No cut-off exception identified | No cut-off exception identified | True |

## Amount Accuracy

| Metric | Result |
|---|---|
| Classification accuracy | 71/80 (88.8%) |
| Amount-field accuracy | 71/80 (88.8%) |
| Error amount accuracy | 12/12 (100.0%) |

Amount-field accuracy compares the amount field on every selected case, including expected null values. Zero means an established absence of a difference; null means undetermined. They are not interchangeable. Missing predictions count as incorrect. Error amount accuracy covers only planted cut-off errors and does not replace classification accuracy.

| Case | Expected difference (CNY) | Predicted difference (CNY) | Amount correct |
|---|---:|---:|---|
| TEST-001 | 0 | 0 | True |
| TEST-002 | 18750 | 18750 | True |
| TEST-003 | null | null | True |
| TEST-004 | 0 | 4800 | False |
| TEST-005 | 0 | 0 | True |
| TEST-006 | 0 | 0 | True |
| TEST-007 | 0 | 0 | True |
| TEST-008 | 0 | 0 | True |
| TEST-009 | null | null | True |
| TEST-010 | 0 | 0 | True |
| TEST-011 | 2400 | 2400 | True |
| TEST-012 | null | null | True |
| TEST-013 | 0 | null | False |
| TEST-014 | 0 | 0 | True |
| TEST-015 | null | null | True |
| TEST-016 | 0 | 0 | True |
| TEST-017 | 0 | 0 | True |
| TEST-018 | 0 | 0 | True |
| TEST-019 | 0 | 0 | True |
| TEST-020 | 0 | 0 | True |
| TEST-021 | 0 | 0 | True |
| TEST-022 | 0 | 0 | True |
| TEST-023 | 0 | 0 | True |
| TEST-024 | 0 | 0 | True |
| TEST-025 | 0 | 0 | True |
| TEST-026 | 0 | 0 | True |
| TEST-027 | 0 | 0 | True |
| TEST-028 | 0 | null | False |
| TEST-029 | 0 | 0 | True |
| TEST-030 | 0 | 0 | True |
| TEST-031 | 0 | 0 | True |
| TEST-032 | 6000 | 6000 | True |
| TEST-033 | null | null | True |
| TEST-034 | 0 | 0 | True |
| TEST-035 | 0 | 0 | True |
| TEST-036 | 0 | 0 | True |
| TEST-037 | 7200 | 7200 | True |
| TEST-038 | 0 | 0 | True |
| TEST-039 | 0 | 0 | True |
| TEST-040 | 19200 | 19200 | True |
| TEST-041 | null | null | True |
| TEST-042 | 0 | 0 | True |
| TEST-043 | 0 | 0 | True |
| TEST-044 | 25000 | 25000 | True |
| TEST-045 | 0 | 0 | True |
| TEST-046 | 0 | 7200 | False |
| TEST-047 | 0 | 0 | True |
| TEST-048 | 0 | 3125 | False |
| TEST-049 | 10000 | 10000 | True |
| TEST-050 | 0 | 0 | True |
| TEST-051 | 0 | 0 | True |
| TEST-052 | null | null | True |
| TEST-053 | 0 | 0 | True |
| TEST-054 | 7500 | 7500 | True |
| TEST-055 | 15000 | 15000 | True |
| TEST-056 | 0 | 2400 | False |
| TEST-057 | 0 | null | False |
| TEST-058 | 0 | 17000 | False |
| TEST-059 | 0 | 0 | True |
| TEST-060 | 5100 | 5100 | True |
| TEST-061 | 0 | 0 | True |
| TEST-062 | 0 | 0 | True |
| TEST-063 | 0 | 0 | True |
| TEST-064 | 0 | 0 | True |
| TEST-065 | 0 | 0 | True |
| TEST-066 | 0 | 0 | True |
| TEST-067 | 0 | 0 | True |
| TEST-068 | 32000 | 32000 | True |
| TEST-069 | 0 | 48000 | False |
| TEST-070 | 0 | 0 | True |
| TEST-071 | 0 | 0 | True |
| TEST-072 | 0 | 0 | True |
| TEST-073 | 0 | 0 | True |
| TEST-074 | 0 | 0 | True |
| TEST-075 | 0 | 0 | True |
| TEST-076 | null | null | True |
| TEST-077 | 2100 | 2100 | True |
| TEST-078 | 0 | 0 | True |
| TEST-079 | 0 | 0 | True |
| TEST-080 | 0 | 0 | True |
