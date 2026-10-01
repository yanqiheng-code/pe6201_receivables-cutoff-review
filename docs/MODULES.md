# Code Module Guide

## Frontend

- `review_web/index.html`: application shell, navigation, file input and acceptance dialog. Assets are served by the Python backend.
- `review_web/app.js`: renders the transaction queue and four review steps, submits human actions and imports, polls local state and downloads CSVs. It does not call OpenRouter directly and does not contain answer keys.
- `review_web/style.css`: responsive presentation. The reading order remains 01, 02, 03, 04 on all screen sizes.

The three files above are under `local_tester/`.

## Backend and evaluation

- `local_tester/review_app.py`: `ReviewStore` validates imports, manages versions, preserves model attempts, records human decisions and enforces acceptance gates. Model requests run in a background thread. The local HTTP layer checks host/origin and serves only defined assets/routes. Runtime state lives in the ignored `review_workspace/` folder.
- `local_tester/run.py`: builds the OpenRouter structured-output request, validates returned fields, computes evaluation metrics and writes per-run artifacts. It loads evaluator labels only for scoring after prediction. Used by both the web backend and evaluation runner.
- `local_tester/main.py`: VS Code-friendly evaluation entry point. Reads saved local configuration and invokes `run.py`; it does not implement a second predictor.
- `local_tester/config.example.py`: shareable configuration template. The user's `config.py` is local and excluded.
- `local_tester/baseline.py`: deterministic recognition-event and date comparator using the supplied source fields. Reads no evaluator labels. Kept unchanged because its hash is part of the original freeze record.
- `local_tester/compare_results.py`: compares the newest available local formal AI and baseline runs with matching input hashes and case IDs. It does not perform paid calls.
- `verify_evaluation.py`: re-scores the submitted snapshot predictions against the fixed labels and asserts the reported counts. Reads files only and does not rerun the model.

## Data construction

- `development_examples_20/generate_examples.py`: generates the 20 development cases and labels.
- `formal_test_80/generate_dataset.py`: deterministic generator for the 80-case formal set. It also writes the freeze manifest. Do not rerun it over the preserved manifest to conceal subsequent prompt changes.

Generators and answer keys are evaluator resources, not runtime evidence for the model. Human-readable Markdown companions are retained to help the instructor inspect the dataset rather than deleted as duplicates of JSON.

## Tests

- `test_runner.py`: request isolation, output validation, cost handling and score calculation.
- `test_baseline.py`: baseline operation without answer access and selected boundary behaviors.
- `test_review_app.py`: isolated fixture workspaces; confirmation-triggered model calls, import validation, history, failure handling, reset and acceptance gates. Model calls are mocked and incur no fees.

All three test modules reside in `local_tester/`. The frontend uses no npm packages; Python uses only the standard library. There is no additional dependency lockfile to install.
