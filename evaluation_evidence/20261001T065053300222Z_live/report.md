# Model Evaluation Report

Separately generated synthetic test set; same author as development data. Limited external validity.

Method: openai/gpt-4.1-mini
Selected cases: 80
Valid predictions: 8
Correct labels: 8 / 80
Errors flagged: 1 / 12
False flags on normal cases: 0
Abstentions: 1
Technical failures or not run: 72
OpenRouter reported API cost: USD 0.008116
Cost incomplete: False

Cost comes from OpenRouter usage.cost when available; missing cost is unknown, not zero. Unknown-cost failed requests may still incur charges. Evidence IDs are validated, but reasoning quality requires human review.

| Case | Expected | Predicted | Label correct |
|---|---|---|---|
| TEST-001 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-002 | Delayed or omitted recognition | Delayed or omitted recognition | True |
| TEST-003 | Additional evidence required | Additional evidence required | True |
| TEST-004 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-005 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-006 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-007 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-008 | No cut-off exception identified | No cut-off exception identified | True |
| TEST-009 | Additional evidence required | Technical failure / not run | False |
| TEST-010 | No cut-off exception identified | Technical failure / not run | False |
| TEST-011 | Premature recognition | Technical failure / not run | False |
| TEST-012 | Additional evidence required | Technical failure / not run | False |
| TEST-013 | No cut-off exception identified | Technical failure / not run | False |
| TEST-014 | No cut-off exception identified | Technical failure / not run | False |
| TEST-015 | Additional evidence required | Technical failure / not run | False |
| TEST-016 | No cut-off exception identified | Technical failure / not run | False |
| TEST-017 | No cut-off exception identified | Technical failure / not run | False |
| TEST-018 | No cut-off exception identified | Technical failure / not run | False |
| TEST-019 | No cut-off exception identified | Technical failure / not run | False |
| TEST-020 | No cut-off exception identified | Technical failure / not run | False |
| TEST-021 | No cut-off exception identified | Technical failure / not run | False |
| TEST-022 | No cut-off exception identified | Technical failure / not run | False |
| TEST-023 | No cut-off exception identified | Technical failure / not run | False |
| TEST-024 | No cut-off exception identified | Technical failure / not run | False |
| TEST-025 | No cut-off exception identified | Technical failure / not run | False |
| TEST-026 | No cut-off exception identified | Technical failure / not run | False |
| TEST-027 | No cut-off exception identified | Technical failure / not run | False |
| TEST-028 | No cut-off exception identified | Technical failure / not run | False |
| TEST-029 | No cut-off exception identified | Technical failure / not run | False |
| TEST-030 | No cut-off exception identified | Technical failure / not run | False |
| TEST-031 | No cut-off exception identified | Technical failure / not run | False |
| TEST-032 | Delayed or omitted recognition | Technical failure / not run | False |
| TEST-033 | Additional evidence required | Technical failure / not run | False |
| TEST-034 | No cut-off exception identified | Technical failure / not run | False |
| TEST-035 | No cut-off exception identified | Technical failure / not run | False |
| TEST-036 | No cut-off exception identified | Technical failure / not run | False |
| TEST-037 | Premature recognition | Technical failure / not run | False |
| TEST-038 | No cut-off exception identified | Technical failure / not run | False |
| TEST-039 | No cut-off exception identified | Technical failure / not run | False |
| TEST-040 | Delayed or omitted recognition | Technical failure / not run | False |
| TEST-041 | Additional evidence required | Technical failure / not run | False |
| TEST-042 | No cut-off exception identified | Technical failure / not run | False |
| TEST-043 | No cut-off exception identified | Technical failure / not run | False |
| TEST-044 | Delayed or omitted recognition | Technical failure / not run | False |
| TEST-045 | No cut-off exception identified | Technical failure / not run | False |
| TEST-046 | No cut-off exception identified | Technical failure / not run | False |
| TEST-047 | No cut-off exception identified | Technical failure / not run | False |
| TEST-048 | No cut-off exception identified | Technical failure / not run | False |
| TEST-049 | Premature recognition | Technical failure / not run | False |
| TEST-050 | No cut-off exception identified | Technical failure / not run | False |
| TEST-051 | No cut-off exception identified | Technical failure / not run | False |
| TEST-052 | Additional evidence required | Technical failure / not run | False |
| TEST-053 | No cut-off exception identified | Technical failure / not run | False |
| TEST-054 | Delayed or omitted recognition | Technical failure / not run | False |
| TEST-055 | Premature recognition | Technical failure / not run | False |
| TEST-056 | No cut-off exception identified | Technical failure / not run | False |
| TEST-057 | No cut-off exception identified | Technical failure / not run | False |
| TEST-058 | No cut-off exception identified | Technical failure / not run | False |
| TEST-059 | No cut-off exception identified | Technical failure / not run | False |
| TEST-060 | Delayed or omitted recognition | Technical failure / not run | False |
| TEST-061 | No cut-off exception identified | Technical failure / not run | False |
| TEST-062 | No cut-off exception identified | Technical failure / not run | False |
| TEST-063 | No cut-off exception identified | Technical failure / not run | False |
| TEST-064 | No cut-off exception identified | Technical failure / not run | False |
| TEST-065 | No cut-off exception identified | Technical failure / not run | False |
| TEST-066 | No cut-off exception identified | Technical failure / not run | False |
| TEST-067 | No cut-off exception identified | Technical failure / not run | False |
| TEST-068 | Premature recognition | Technical failure / not run | False |
| TEST-069 | No cut-off exception identified | Technical failure / not run | False |
| TEST-070 | No cut-off exception identified | Technical failure / not run | False |
| TEST-071 | No cut-off exception identified | Technical failure / not run | False |
| TEST-072 | No cut-off exception identified | Technical failure / not run | False |
| TEST-073 | No cut-off exception identified | Technical failure / not run | False |
| TEST-074 | No cut-off exception identified | Technical failure / not run | False |
| TEST-075 | No cut-off exception identified | Technical failure / not run | False |
| TEST-076 | Additional evidence required | Technical failure / not run | False |
| TEST-077 | Premature recognition | Technical failure / not run | False |
| TEST-078 | No cut-off exception identified | Technical failure / not run | False |
| TEST-079 | No cut-off exception identified | Technical failure / not run | False |
| TEST-080 | No cut-off exception identified | Technical failure / not run | False |

## Amount Accuracy

| Metric | Result |
|---|---|
| Classification accuracy | 8/80 (10.0%) |
| Amount-field accuracy | 8/80 (10.0%) |
| Error amount accuracy | 1/12 (8.3%) |

Amount-field accuracy compares the amount field on every selected case, including expected null values. Zero means an established absence of a difference; null means undetermined. They are not interchangeable. Missing predictions count as incorrect. Error amount accuracy covers only planted cut-off errors and does not replace classification accuracy.

| Case | Expected difference (CNY) | Predicted difference (CNY) | Amount correct |
|---|---:|---:|---|
| TEST-001 | 0 | 0 | True |
| TEST-002 | 18750 | 18750 | True |
| TEST-003 | null | null | True |
| TEST-004 | 0 | 0 | True |
| TEST-005 | 0 | 0 | True |
| TEST-006 | 0 | 0 | True |
| TEST-007 | 0 | 0 | True |
| TEST-008 | 0 | 0 | True |
| TEST-009 | null | No prediction | False |
| TEST-010 | 0 | No prediction | False |
| TEST-011 | 2400 | No prediction | False |
| TEST-012 | null | No prediction | False |
| TEST-013 | 0 | No prediction | False |
| TEST-014 | 0 | No prediction | False |
| TEST-015 | null | No prediction | False |
| TEST-016 | 0 | No prediction | False |
| TEST-017 | 0 | No prediction | False |
| TEST-018 | 0 | No prediction | False |
| TEST-019 | 0 | No prediction | False |
| TEST-020 | 0 | No prediction | False |
| TEST-021 | 0 | No prediction | False |
| TEST-022 | 0 | No prediction | False |
| TEST-023 | 0 | No prediction | False |
| TEST-024 | 0 | No prediction | False |
| TEST-025 | 0 | No prediction | False |
| TEST-026 | 0 | No prediction | False |
| TEST-027 | 0 | No prediction | False |
| TEST-028 | 0 | No prediction | False |
| TEST-029 | 0 | No prediction | False |
| TEST-030 | 0 | No prediction | False |
| TEST-031 | 0 | No prediction | False |
| TEST-032 | 6000 | No prediction | False |
| TEST-033 | null | No prediction | False |
| TEST-034 | 0 | No prediction | False |
| TEST-035 | 0 | No prediction | False |
| TEST-036 | 0 | No prediction | False |
| TEST-037 | 7200 | No prediction | False |
| TEST-038 | 0 | No prediction | False |
| TEST-039 | 0 | No prediction | False |
| TEST-040 | 19200 | No prediction | False |
| TEST-041 | null | No prediction | False |
| TEST-042 | 0 | No prediction | False |
| TEST-043 | 0 | No prediction | False |
| TEST-044 | 25000 | No prediction | False |
| TEST-045 | 0 | No prediction | False |
| TEST-046 | 0 | No prediction | False |
| TEST-047 | 0 | No prediction | False |
| TEST-048 | 0 | No prediction | False |
| TEST-049 | 10000 | No prediction | False |
| TEST-050 | 0 | No prediction | False |
| TEST-051 | 0 | No prediction | False |
| TEST-052 | null | No prediction | False |
| TEST-053 | 0 | No prediction | False |
| TEST-054 | 7500 | No prediction | False |
| TEST-055 | 15000 | No prediction | False |
| TEST-056 | 0 | No prediction | False |
| TEST-057 | 0 | No prediction | False |
| TEST-058 | 0 | No prediction | False |
| TEST-059 | 0 | No prediction | False |
| TEST-060 | 5100 | No prediction | False |
| TEST-061 | 0 | No prediction | False |
| TEST-062 | 0 | No prediction | False |
| TEST-063 | 0 | No prediction | False |
| TEST-064 | 0 | No prediction | False |
| TEST-065 | 0 | No prediction | False |
| TEST-066 | 0 | No prediction | False |
| TEST-067 | 0 | No prediction | False |
| TEST-068 | 32000 | No prediction | False |
| TEST-069 | 0 | No prediction | False |
| TEST-070 | 0 | No prediction | False |
| TEST-071 | 0 | No prediction | False |
| TEST-072 | 0 | No prediction | False |
| TEST-073 | 0 | No prediction | False |
| TEST-074 | 0 | No prediction | False |
| TEST-075 | 0 | No prediction | False |
| TEST-076 | null | No prediction | False |
| TEST-077 | 2100 | No prediction | False |
| TEST-078 | 0 | No prediction | False |
| TEST-079 | 0 | No prediction | False |
| TEST-080 | 0 | No prediction | False |
