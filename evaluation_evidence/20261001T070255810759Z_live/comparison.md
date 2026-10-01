# Formal Test Comparison

Latest full-selection runs; examine any technical failures. Synthetic same-author test data with three contract families; not real-world audit validation.

| Metric | Non-AI baseline | AI |
|---|---:|---:|
| Valid predictions | 80 | 80 |
| Correct labels / 80 | 80 | 71 |
| Correct amount fields / 80 | 80 | 71 |
| Errors flagged / 12 | 12 | 12 |
| False flags among 60 normal cases | 0 | 6 |
| Abstentions | 8 | 11 |
| Correct missing-evidence decisions / 8 | 8 | 8 |
| Technical failures or not run | 0 | 0 |
| Reported API cost USD | 0 | 0.06789319999999999 |

Baseline run: 20261001T041303435758Z_baseline
AI run: 20261001T070255810759Z_live

Cost totals exclude any unknown-cost requests. Model explanation quality and human review time are not assessed by these automatic metrics. Do not select a better-scoring earlier run without disclosing the selection.
