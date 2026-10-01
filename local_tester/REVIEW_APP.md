# Cut-off Review — Auditor Workspace

## Start in VS Code

### Repeated demo testing

The sidebar **Reset** is a one-click workspace clear, not a search-filter reset. It deletes imported source records, demo AI attempts and raw responses, archived demo batches, evidence supplements, human reviews and acceptance records. It is unavailable while AI is running. The original datasets and formal evaluation files in `runs/` are retained. Restarting after Reset keeps the workspace empty; manually import the 80-case `formal_test_80/inputs.json` package to start again. Empty batches cannot be accepted.

The heading, overview cards and workflow strip are shown only in **Workbench**. **Source input** focuses on importing evidence and **Review summary** focuses on human decisions and acceptance.

The agreed course-demo input is manually supplied structured JSON. AI extraction from original documents is a future enhancement, not part of the current implementation or measured results.

1. Open `review_app.py` and select **Run Python File**.
2. Open **http://127.0.0.1:8765** in a browser. Keep the Python process running.
3. Enter your reviewer name in the top bar.

Python 3.9 or later is sufficient. No additional packages, frontend build tools or installation are needed. Stop the server with Ctrl+C in VS Code. Restarting preserves review progress.

The app imports the latest complete, matching 80-case formal AI run on first launch. It never imports the answer key or non-AI baseline. Viewing the imported results costs nothing. Once created, the workspace remains pinned to that source run; it does not silently replace your work with newer evaluations.

## Four working areas

### Source input and the pre-AI checkpoint (updated)

The **Source input** page precedes the workbench. Download its one-case JSON template, or import an existing `inputs.json` package. Importing a new batch archives the current workspace under `review_workspace/archives/` and creates unrun cases. Import and field parsing make no model calls. The current scope is FY2025, CNY, 1–200 cases, and full-batch quantities. Existing evaluation files are untouched.

Step **01 Source records & human check** displays structured fields read from that package. This is not PDF/OCR extraction. The reviewer must check all four records and confirm that the fields faithfully reflect the supplied evidence, including unknown fields. Clicking Confirm source records & run AI records this checkpoint and immediately starts one model request. The backend blocks AI calls and final human review until this checkpoint is recorded. Imported historical AI outputs remain visible as saved outputs; the checkpoint is required for future reruns and review completion, not retroactively claimed for the original experiment.

The four cards are now presented vertically in numerical order: **01 source check → 02 AI assessment → 03 supplement → 04 human review**. Confirming a supplement in 03 verifies the new evidence revision and reruns 02. The existing final-review and batch-acceptance gates remain in effect.

1. **Source evidence:** inspect contract terms, the ledger, invoice and delivery records.
2. **AI assessment:** review the saved conclusion, amount, explanation, document references and evidence requests. The original model flaws are intentionally preserved.
3. **Supplement evidence:** enter a verified dispatch, receipt or acceptance date, the full batch quantity, supporting reference and evidence note. Confirming creates a new version and makes one paid AI call on the updated record.
4. **Human review and summary:** record a final conclusion, amount, rationale and reviewer name for each transaction. The summary retains separate AI and human columns. Once every transaction is reviewed, explicitly accept the batch and export the accepted CSV.

The UI is in English for the course demo. This is a structured-record prototype, not PDF ingestion or OCR. Supplementation records a reference and verified facts; it does not upload or authenticate the underlying document. Use fictional evidence for this synthetic demo, and label it as such. All original quantities are full-batch quantities; partial deliveries remain outside this UI's scope.

## Model calls and configuration

The server reuses the existing prompt, schema, validator and OpenRouter model in `run.py`. It reads `API_KEY`, `MODEL` and `BASE_URL` from local `config.py` on each requested run (with environment-key fallback). Existing command-line `BACKEND`, `RUN_ALL` and `CASE_ID` settings do not control the UI. No key is sent to the browser or saved in review history.

- **Confirm source records & run AI** in step 01: one paid API call. There is no separate run button in step 02. Confirming again can rerun the transaction, including after a failed attempt.
- **Confirm evidence & rerun**: saves a revision and makes one paid API call.
- **Run pending AI checks**: calls only transactions with no result, failed calls or evidence needing a rerun. It is disabled when imported results are already available for every transaction.
- No automatic API retry. A failure stops the queued batch. Review the failure before manually retrying; failed calls may still incur charges.

## Human checkpoints and traceability

- Every transaction requires an explicit human decision, even when the AI finds no exception.
- Evidence changes and AI reruns invalidate the affected human review and any prior batch acceptance.
- Closing a transaction requires a resolved conclusion and amount. A reviewer may override an unnecessary AI evidence request using existing evidence, with an explicit rationale.
- Draft and accepted CSV exports are distinct. The server prevents final export before batch acceptance.
- Review names are self-declared. This single-user local prototype is not authenticated multi-user approval or a legally binding signature. Acceptance completes the review task; it does not post adjustments or issue an audit opinion.
- The workspace retains evidence revisions, original and subsequent AI outputs, human decisions, superseded decisions, acceptance history and a local activity log. Local files are editable and are not a tamper-proof audit trail.

All new state is stored under `review_workspace/`, which is excluded from Git. Raw API requests/responses and prompt snapshots are stored under `review_workspace/attempts/`. Existing `runs/`, datasets, frozen answer keys and reported evaluation scores remain unchanged. Supplemented cases are demo follow-ups, not new independent evaluation results.

The server binds only to `127.0.0.1`, validates local origin/host and uses a session token for API access. It serves only its three frontend assets. Do not expose it as a public audit service.

## Suggested demonstration

1. Inspect a normal case across its four source tabs and record a supported human decision.
2. Open **TEST-069** to show the preserved discrepancy between the original AI label and its explanation. Check the dates and record a human correction with a rationale. Source confirmation now triggers a fresh model call; use preserved output history when discussing the original evaluation error rather than presenting a fresh output as the original.
3. Open **TEST-009**, which requests collection evidence. For a clearly labelled fictional continuation, enter a synthetic collection record and a verified date within the records period, confirm and rerun. The new result is a real model response and may still need human correction.
4. Open **Review summary** to show separate AI/human conclusions and the acceptance gate. Completion of three demo transactions does not unlock acceptance of all 80. Never auto-approve the remaining cases merely for a presentation.

## Validation

Run `python3 -m unittest test_runner test_baseline test_review_app`. Workflow tests use isolated temporary workspaces and mocked model responses, with no paid API calls. They exercise evidence versioning, rerun history, human-review invalidation, failure handling, and acceptance/export gates.
