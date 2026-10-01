
import runpy
from pathlib import Path

import run


def main():
    # Read the source on each run so saved configuration edits always take effect.
    settings_path = Path(__file__).resolve().with_name("config.py")
    if not settings_path.exists():
        raise SystemExit("Copy config.example.py to config.py before running.")
    settings = runpy.run_path(str(settings_path))
    backend = settings.get("BACKEND")
    if backend not in ("preview", "live", "baseline"):
        raise SystemExit('BACKEND must be "preview", "live" or "baseline".')
    if type(settings.get("RUN_ALL")) is not bool:
        raise SystemExit("RUN_ALL must be True or False.")
    if settings.get("MODEL") != run.MODEL:
        raise SystemExit("This runner supports " + run.MODEL + ". Model changes require reviewing structured-output compatibility.")
    if settings.get("BASE_URL") != run.BASE_URL:
        raise SystemExit("BASE_URL must be " + run.BASE_URL)
    key = settings.get("API_KEY", "")
    if not isinstance(key, str):
        raise SystemExit("API_KEY must be a string.")
    args = ["--all"] if settings["RUN_ALL"] else ["--case", settings.get("CASE_ID", "DEV-03")]
    args += ["--dataset", settings.get("DATASET", "development_examples_20")]
    if backend == "baseline":
        args.append("--baseline")
    if backend == "live":
        args.append("--live")
    print("Mode:", backend, "| Model:", run.MODEL)
    print("Selection:", "All cases in selected dataset" if settings["RUN_ALL"] else settings.get("CASE_ID"))
    # Never print settings or the API key.
    run.main(args, api_key=key, interactive=False)


if __name__ == "__main__":
    main()
