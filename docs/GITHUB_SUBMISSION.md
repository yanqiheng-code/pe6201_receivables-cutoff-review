# Submit the Repository with GitHub Desktop

1. Sign in to GitHub Desktop with your GitHub account.
2. Choose **File → Add Local Repository** and select this project's root folder (`personal project`), which contains `README.md` and `.gitignore`.
3. Inspect the Changes list. It should include frontend/backend code, datasets, documentation and `evaluation_evidence/`. It must not include `local_tester/config.py`, local `runs/`, or `review_workspace/`.
4. Enter a commit summary such as `Prepare PE6201 cutoff review submission`, then click **Commit to main**.
5. Click **Publish repository**. A suggested name is `pe6201-receivables-cutoff-review`. Choose visibility according to the course submission arrangements. If private, give the instructor/TA access through GitHub repository settings.
6. Check the published repository in your browser: README renders, datasets and evaluation evidence are present, and local configuration is absent.
7. Add the final report and demo video or submission links when they are ready, commit those changes, and select **Push origin**. A repository upload alone does not finish those separate deliverables.

This uploads source code; it does not deploy the Python application as a public service. See `local_tester/DEPLOYMENT_PLAN.md` for that distinction. Use the root folder rather than uploading only `review_web/`.

Official guide: https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-an-existing-project-to-github-using-github-desktop
