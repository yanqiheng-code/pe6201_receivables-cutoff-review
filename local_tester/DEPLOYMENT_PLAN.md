# Web Deployment Plan

Status update: a password-free Flask/Gunicorn cloud adapter, anonymous browser workspaces, request limits and Render settings have now been implemented. A live public deployment has not yet been verified. Follow [the current setup guide](../docs/RENDER_SETUP.md). The planning notes below describe the original deployment considerations; authenticated access is deferred by the student's explicit choice for this synthetic public demo.

## Current implementation

The application is already a browser-based web application. Its Python server runs on the student's computer at `http://127.0.0.1:8765`, and its HTML/CSS/JavaScript frontend communicates with that server. This address is local to the computer running the server, not a shareable public website.

The local version is suitable for the recorded course demonstration and a reproducible README-based submission. The latest supplied instructor email does not explicitly require a publicly hosted site.

## Suggested public-demo architecture

Browser → HTTPS web service → Python application → OpenRouter

The Python application also writes evidence versions, AI attempts and human review records to persistent storage. API credentials belong in server-side environment variables, never in frontend JavaScript or a public repository.

A possible hosting route is a Python web service on Render. This is a future implementation choice rather than a dependency of the current prototype.

## Changes needed before deployment

1. Adapt the current local HTTP server to an application framework such as Flask with a production server. Preserve the existing review workflow logic and tests.
2. Configure the hosting platform's port and the actual HTTPS origin. Replace the hard-coded loopback host/origin checks with validated deployment configuration; do not simply remove them.
3. Store `OPENROUTER_API_KEY` as a server-side secret and keep the same supported model configuration.
4. Add access control for the intended reviewer. The current self-declared reviewer name and local session token are not a public-site login. A public demo also needs request limits to prevent uncontrolled paid model calls.
5. Use persistent storage for session files, archives and model-attempt records. Render's default filesystem is ephemeral. A supported persistent disk or database is needed to preserve progress across deployment/restarts.
6. For this educational deployment, retain a single workspace and single worker unless per-user sessions and coordinated storage have been implemented. The current in-memory lock does not coordinate multiple server processes.
7. Package synthetic input data and selected saved outputs deliberately. The ignored local `runs/` directory will not appear in a fresh repository checkout automatically. Do not upload private configuration or assume ignored local evidence will be deployed.
8. Validate import, source confirmation, live rerun, human review, acceptance, export and restart persistence on the hosted instance before sharing the link.

Do not describe this work as completed until a deployed URL has been verified. A static-site upload alone cannot run this application's Python backend or safely perform its server-side model calls.

## Official references

- Python example: https://render.com/docs/deploy-flask
- Web services and platform port: https://render.com/docs/web-services
- Server-side environment variables: https://render.com/docs/configure-environment-variables
- Persistent disks: https://render.com/docs/disks

Hosting plan availability and pricing should be checked when deployment is actually requested. No hosting service has been purchased or connected as part of this plan.

## GitHub repository versus hosting

Both frontend and backend source code can be submitted in one GitHub repository. GitHub Pages serves static HTML/CSS/JavaScript and does not execute this Python backend. Uploading the repository is therefore distinct from deploying the working application. A Python web service can deploy from the repository and serve both layers under one HTTPS origin.

Official GitHub reference: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
