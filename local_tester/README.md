# Local Runtime and Evaluation Tools

Start with the [repository README](../README.md) for setup, model configuration and supported scope.

- **Auditor web interface:** run `review_app.py` in VS Code and open `http://127.0.0.1:8765`. See [the UI guide](REVIEW_APP.md).
- **Evaluation:** copy `config.example.py` to local `config.py`, select a dataset and backend, and run `main.py`. `preview` writes request bodies only, `baseline` runs local rules, and `live` calls OpenRouter. Use `RUN_ALL = True` for a full dataset or `False` with a case ID for one case.
- **Local comparison:** run `compare_results.py` after AI and baseline formal runs. It requires matching input versions and case selections.
- **Submitted evidence:** run `../verify_evaluation.py` to reproduce the preserved scores without a key or network call.
- **Tests:** from the repository root, run `python3 -m unittest discover -s local_tester -p 'test_*.py'`.

`run.py` is the shared request, validation and evaluation implementation, not an obsolete copy of `main.py`. `review_app.py` supplies the web workflow and reuses `run.py`. The [module guide](../docs/MODULES.md) describes each component.

Local `config.py`, `runs/` and `review_workspace/` are ignored by Git. Do not manually upload them. The selected evaluation records submitted to the instructor are in `../evaluation_evidence/`. Model outputs, including errors, are preserved there rather than replaced by human corrections.
