# Formal Synthetic Test Set v1.0

## Purpose and sample size

80 new transaction cases, separate from the 20 development cases. This is a small, bounded educational evaluation, not statistical assurance about real industrial audits. The instructor suggested a 200-row ledger with 12 planted errors; 80 is a project scope choice, not evidence of instructor approval.

There are 60 normal cases, 6 premature recognitions, 6 delayed recognitions and 8 insufficient-evidence cases. The 12 known errors retain the instructor's proposed error count. One missed error changes error recall by 8.33 percentage points. One case changes overall classification accuracy by 1.25 percentage points. Always predicting no exception achieves 60/80 = 75%, while detecting none of the errors. Eight evidence cases are additional to, not part of, the 12 confirmed errors.

## Construction and independence

All cases are fictional. They were constructed with seed 620180 and new identifiers, dates, quantities, prices, goods and contract wording. Each contains a contract excerpt, ledger entry, invoice record and verified synthetic delivery summary. No partial deliveries, missing ledger entries, conflicting evidence or complex accounting arrangements are included.

There are three contract families and three wording variants per family, so 80 cases are not 80 independent contract designs. This dataset was created by the same assistant that generated the development cases; it is held out from prompt development but not independently authored, externally validated or representative of a real-world population. Human review of the accounting logic is recommended. No external reviewer validation has occurred.

The ground truth and the baseline implementation were fixed before the first predictor evaluation. `freeze_manifest.json` records file hashes for the inputs, answers, generator, baseline and prompt. Do not tune the predictor on these labels and continue calling the same set unseen. If revisions are necessary, disclose the revision and create a new held-out version.

## Files and leakage prevention

- `inputs.json`: only this file supplies data to predictors.
- `examples.md`: readable input records without answers.
- `answer_key.json` and `answer_key.md`: evaluator only.
- `generate_dataset.py`: evaluator only; contains construction logic and labels.
- `freeze_manifest.json`: reproducibility evidence; not model input.

The generator reproduces the dataset with `python3 generate_dataset.py`. Do not regenerate the freeze manifest to conceal later changes. The runner loads the answer key only after prediction finishes.

## Fair non-AI baseline

`../local_tester/baseline.py` selects the contractual event through fixed positive keyword patterns, reads the corresponding supplied date and compares the dates with the reporting cut-off. Amounts use fixed quantity times price. An unknown date or ambiguous rule triggers an evidence request. It reads the same contract and delivery fields as the model; it does not read labels or hidden contract categories.

The first baseline run correctly classified 80/80 cases, identified 12/12 errors, produced no false flags among 60 normal cases, and correctly deferred all 8 missing-evidence cases. Amount fields were also correct in 80/80 cases. This is an observed result, not a target. It shows this simplified, templated task is solvable by deterministic rules. Do not claim AI accuracy superiority if both approaches tie. Evaluate explanation usefulness separately through an explicit human rubric; it has not yet been measured.

## Run in VS Code

In `local_tester/config.py`, set:

```python
DATASET = "formal_test_80"
RUN_ALL = True
BACKEND = "baseline"  # deterministic, no API cost
```

Run `local_tester/main.py`. For the first full AI evaluation change only `BACKEND = "live"`, using your OpenRouter key already configured locally. Model inputs never include the answer key. A single formal case can be selected with `RUN_ALL = False` and `CASE_ID = "TEST-001"`, but viewing its result uses that test case; preserve and disclose all attempts.

The 80-case AI run has not been performed by the dataset author. Preview files are not AI predictions. Once both methods have run, use `local_tester/compare_results.py` to produce an English comparison without additional API calls.

## Auditor demo interface

Run `../local_tester/review_app.py` in VS Code, then open `http://127.0.0.1:8765`. The English auditor workspace shows source evidence, AI findings, evidence supplementation with a single-case rerun, and human review with batch acceptance. The non-AI baseline remains an evaluation comparison and is not shown in the auditor UI. Existing evaluation outputs remain unchanged; review follow-ups and human corrections are recorded separately. See `../local_tester/REVIEW_APP.md` for setup, limitations and a demo walkthrough.
