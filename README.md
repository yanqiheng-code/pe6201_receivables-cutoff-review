# Receivables Cut-off Review

An educational audit-assistance prototype for industrial credit sales. Auditors import structured contract, ledger, invoice and delivery records, check the source fields, obtain an AI cut-off assessment, supplement missing evidence and record a final human decision.

**Scope:** FY2025, CNY, ordinary fixed-price goods, one complete batch per transaction. This prototype does not extract documents using OCR, assess bad debts or valuation, post accounting adjustments, or issue an audit opinion.

## Start the auditor interface

1. Install Python 3.9 or later and open this repository in VS Code. No third-party Python packages or frontend build step are required.
2. Copy `local_tester/config.example.py` to `local_tester/config.py`. Set your own OpenRouter API key there, or set the `OPENROUTER_API_KEY` environment variable. Never commit the local configuration.
3. Open `local_tester/review_app.py` and select **Run Python File**.
4. Open **http://127.0.0.1:8765** in a browser. Keep the Python process running.
5. Enter your reviewer name. On **Source input**, upload `formal_test_80/inputs.json` and confirm the import.
6. In **Workbench**, check the four source records in step 01. **Confirm source records & run AI** makes one paid model call and displays its result in step 02.
7. If more evidence is needed, supply verified synthetic facts and a source reference in step 03. Confirming automatically reruns that case. Record a supported human decision in step 04.
8. Use **Review summary** to inspect decisions and export a working CSV. Every case must be reviewed before batch acceptance and final export.

Stop the server with Ctrl+C. If port 8765 is already in use, stop the earlier instance or use its existing page. Network/TLS failures require a working internet connection and a Python installation with trusted HTTPS certificates; certificate verification is not disabled.

Importing and viewing data do not call the model. Confirmation in steps 01 and 03 does. There are no automatic retries. Sidebar **Reset** deletes local demo state, attempts and demo archives, while retaining the repository datasets and evaluation evidence. It is disabled during an AI run. For details, see [the UI guide](local_tester/REVIEW_APP.md).

## Optional public Render demo

The hosted entry point is `cloud_app.py`; it serves the same frontend without a visitor password. Each browser has an isolated workspace. The default provider-call limit is 200 attempts per UTC day across all visitors. This temporary demo stores progress on the instance filesystem, so free-service restarts can lose progress. See [Render setup](docs/RENDER_SETUP.md) for exact settings, secrets and limitations. `requirements.txt` and `render.yaml` are included. Deployment to an actual public URL still requires the owner's Render account and a successful live check.

## Evaluation commands

Set `DATASET = "formal_test_80"`, `RUN_ALL = True` and `BACKEND = "baseline"` in your local configuration, then run `local_tester/main.py` in VS Code for an offline rules baseline. Use `BACKEND = "live"` for a paid 80-case model evaluation. Live requests use `openai/gpt-4.1-mini` through OpenRouter. New outputs go to the ignored `local_tester/runs/` directory.

To inspect the submitted results without any key or network call, run `verify_evaluation.py` from VS Code. It recomputes the scores from the preserved predictions and labels; it does not generate new model outputs.

To run offline tests from the repository root:

```sh
python3 -m unittest discover -s local_tester -p 'test_*.py'
```

## Observed results

| Measure | AI | Rules baseline |
|---|---:|---:|
| Classification accuracy | 71/80 (88.75%) | 80/80 (100%) |
| Amount-field accuracy | 71/80 (88.75%) | 80/80 (100%) |
| Planted errors detected | 12/12 | 12/12 |
| False flags among 60 normal cases | 6 | 0 |
| Correct missing-evidence decisions | 8/8 | 8/8 |
| Additional unnecessary evidence requests | 3 | 0 |
| Reported API cost, complete formal run | USD 0.0678932 | No API calls |

These are results from one synthetic test run, after a disclosed date-format repair. The majority-class accuracy baseline is 75%. The rules baseline outperformed AI on these templates. Human-corrected outcomes are not counted as raw AI accuracy. See [evaluation methods and chronology](evaluation_evidence/README.md) for limitations and exact run provenance.

## Repository guide

| Location | Purpose |
|---|---|
| `local_tester/review_app.py` | Python web backend, input validation, model calls and human-review state |
| `local_tester/review_web/` | Browser frontend: HTML, CSS and JavaScript |
| `local_tester/run.py`, `main.py` | Shared model request/validation/scoring logic and VS Code evaluation entry point |
| `local_tester/baseline.py`, `compare_results.py` | Non-AI comparator and local-run comparison |
| `local_tester/test_*.py` | Offline validation and workflow tests |
| `accounts_receivable_cutoff_prompt_v1.1.md` | Current English model instructions |
| `development_examples_20/` | Development inputs, labels, generator and explanation |
| `formal_test_80/` | Formal synthetic inputs, fixed labels, generator and original freeze manifest |
| `evaluation_evidence/` | Preserved reported runs, raw requests/responses and evaluation explanation |
| `verify_evaluation.py` | Offline reproducibility check of the submitted scores |
| `docs/PRODUCT.md` | Persona, inputs, outputs, architecture and metric targets versus observations |
| `docs/MODULES.md` | Responsibilities and boundaries of the code modules |

## Limitations and submission status

Data are fictional and template-based, with shared authorship between development and formal cases. The set is not an independently authored real-world validation. Explanation quality, reviewer time savings, extraction accuracy and repeat-run stability have not been measured. Reviewer names are self-declared, and local records are not tamper-proof. The server is designed for local single-user use.

Source code and these evaluation materials are ready for repository review. The final approximately 1,200-word report and face-and-screen demo video are completed in NTUlearn. GitHub stores the source repository; GitHub Pages cannot execute the Python backend. See [deployment planning](local_tester/DEPLOYMENT_PLAN.md).
