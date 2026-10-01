# Evaluation Evidence and Methods

This directory contains selected original run artifacts, copied without changing model predictions. It is deliberately included in the repository, unlike the local working `runs/` folder. Keys and authorization headers are not part of these artifacts.

## Run chronology

| Run directory | Purpose and interpretation |
|---|---|
| `20260930T090937957846Z_live` | Development evaluation: 20/20 classifications, 14/20 amount fields. Six normal cases used null instead of zero. |
| `20261001T035238034710Z_live` | Development rerun after zero/null clarification: 20/20 classifications and amounts. This is development tuning, not independent confirmation. |
| `20261001T041303435758Z_baseline` | Frozen non-AI baseline on 80 formal cases: 80/80 classifications and amounts. |
| `20261001T065053300222Z_live` | Interrupted formal attempt: eight valid results, TEST-009 format failure, 71 not run. The model returned `Unknown` for a date, following wording then allowed by the prompt; the parser expected an ISO date or null. Do not interpret 8/80 as 72 model judgment errors. |
| `20261001T070255810759Z_live` | Complete formal evaluation after the date-output requirement was aligned: 71/80 classifications and amounts, 12/12 planted errors found, six false flags and three unnecessary evidence requests. |

The interrupted attempt and subsequent complete run use the same inputs. The prompt snapshots and hashes document their differences. The original `formal_test_80/freeze_manifest.json` is retained; later prompt edits must not be concealed by replacing it. The model is `openai/gpt-4.1-mini` through OpenRouter, with temperature 0, a structured-output schema and no automatic retries.

## Files within each run

- `manifest.json`: model, case selection, dataset/input hash, prompt hash and request settings.
- `prompt_snapshot.md`: exact instructions used for that run.
- `*_request.json`: request body containing the case and context, without the authorization header.
- `*_response.json`: provider response, when an API call completed, including its original output and usage metadata.
- `results.json`: parsed predictions or technical errors, request timing and available cost.
- `evaluation.json`: computed counts and per-case matches against fixed labels.
- `report.md`: readable report. The final formal folder also contains `comparison.md`.

These files serve different purposes: they are not interchangeable copies. Raw text is necessary to inspect the date failure and explanation/conclusion contradictions; parsed results and metrics enable reproducible scoring.

## Metrics and denominators

- **Classification accuracy:** exact label matches divided by selected cases. The formal denominator is 80.
- **Amount-field accuracy:** exact expected amount or null divided by selected cases. Zero and null differ; absent predictions count as incorrect.
- **Error amount accuracy:** correct amounts on the 12 planted errors only.
- **Error recall:** planted-error cases flagged with either error label divided by 12. Exact classification separately distinguishes premature from delayed recognition.
- **False flags:** normal cases labelled with an error; denominator 60 for the false-positive rate.
- **Deferral:** additional-evidence or outside-scope conclusions. The eight intentionally insufficient-evidence cases are evaluated separately from the 12 planted errors.
- **Precision of error alerts:** true error flags divided by all error flags: 12/18 for the complete AI run.
- **Cost:** the sum of OpenRouter `usage.cost` values when reported. Missing cost is unknown, not zero. Run cost is not all development spending or human labor cost.

The current scorer reports technical failures and unrun cases together. Consult the raw results/requests to distinguish them in an interrupted run. Overall rates from an incomplete run must not be presented as a completed accuracy experiment.

## Comparison and critique

The majority-class baseline is 60/80 = 75% accuracy and zero planted-error detection. The stronger deterministic keyword/date baseline receives the same case fields and achieves 80/80 on these templates. The model's complete run finds all 12 errors but raises six false error flags (10% of normal cases) and three unnecessary evidence requests. Nine mistaken classifications all concern correct recognition and booking in the following year.

The data have only three contract families and three wording variants per family. Development and formal data share authorship, and the complete formal attempt followed a format fix. This is not an independently authored blind test or evidence of general audit reliability. Twelve planted errors provide limited support for claims about recall. No human-time study, explanation-quality rating, extraction benchmark or repeat-run stability study is included.

## Reproduce scores

Run `python3 verify_evaluation.py` from the repository root, or open that file in VS Code and run it. It checks input/prompt hashes and recomputes reported counts for all five runs without calling the model. Rerunning a model may produce different predictions and should be preserved as a new experiment, not overwrite this evidence.
