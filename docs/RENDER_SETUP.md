# Render Setup — Public Demo Without Login

Deployment code is provided; a live Render deployment has not yet been verified.

## Intended behavior

Anyone with the URL can open the demo without a password. Each browser receives an anonymous signed session cookie and its own workspace. Reset clears only that browser's workspace. Reviewer names remain self-declared, not authenticated signatures. People using the same browser profile share the session.

The online app starts with no transactions. Use **Download 80-case demo package**, then upload that JSON package. Steps 01 and 03 automatically call AI after confirmation, as in the local version. The provider key remains on the server.

This free-demo configuration stores progress in `/tmp/pe6201-demo`. Progress and request counters may be lost when Render replaces/restarts the instance. Export summaries before leaving. Use synthetic data only. This is not durable audit storage.

## First push the deployment files

In GitHub Desktop, commit the new files and changes with a message such as `Prepare public Render demo`, then **Push origin**. The main additions are `cloud_app.py`, `requirements.txt`, `render.yaml`, this guide, and `tests_cloud/`.

## Option A: Render Web Service form

1. Sign in to Render and choose **New → Web Service**.
2. Connect GitHub and grant access to this repository. The repository can remain private.
3. Choose the project repository and enter:

| Setting | Value |
|---|---|
| Name | `pe6201-cutoff-demo` (or another available name) |
| Branch | `main` |
| Root Directory | Leave blank |
| Language / Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn 'cloud_app:create_app()' --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120` |
| Instance Type | Free, for this temporary demonstration |
| Health Check Path | `/health` |

4. Add environment variable **OPENROUTER_API_KEY** with your own key, directly in Render. Do not add the value to GitHub or send it in chat.
5. Optionally set **DEMO_DAILY_CALL_LIMIT**; the default is `200` provider-call attempts per UTC day, shared across all visitors. This is a request-count cap, not a dollar-budget guarantee. Network failures consume a count because the provider may have received the request.
6. Optionally set **SECRET_KEY** to a generated random secret for signing anonymous cookies. If omitted, the application generates one at startup, which means visitors must refresh their session after a worker restart. This is not a visitor password.
7. Create the web service. Render supplies `PORT` and `RENDER_EXTERNAL_URL` automatically. For a custom domain, explicitly set **APP_URL** to its HTTPS origin, without a trailing path.

The exact one-worker setting is required: workflow state and budget locks coordinate one process. Do not scale to multiple workers/instances without shared storage and cross-process locking.

## Option B: Blueprint

Use **New → Blueprint** and select the repository. The included `render.yaml` supplies the runtime settings and generates the session-signing secret. Enter the OpenRouter key when prompted. Review the selected plan before deployment.

## Post-deployment check

Open the generated HTTPS URL, download and import the synthetic package, confirm source records and inspect the actual AI output. Test a supplemental-evidence follow-up and human review. Check that another browser starts with its own empty workspace and that resetting one browser leaves the other unchanged. These live checks remain to be performed after deployment; existing tests use fake provider responses.

## Local validation of the cloud adapter

Install `requirements.txt` into a separate virtual environment, then run:

```sh
python -m unittest discover -s tests_cloud -p 'test_*.py'
python -m unittest discover -s local_tester -p 'test_*.py'
python verify_evaluation.py
```

The original local `review_app.py` still runs without these extra packages. Flask/Gunicorn are needed for the hosted entry point only. Daily counters are outside per-browser workspaces, so clicking Reset or changing browsers does not reset the shared cap while the service filesystem survives. Up to four concurrent provider requests and 100 browser workspace directories are allowed per instance storage lifetime.

## References

- https://render.com/docs/deploy-flask
- https://render.com/docs/web-services
- https://render.com/docs/free
- https://flask.palletsprojects.com/en/stable/deploying/gunicorn/
