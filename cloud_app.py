"""Public Render entry point: anonymous browser sessions, bounded model calls, shared UI.

Run with one Gunicorn worker and multiple HTTP threads. Never preload this module
into multiple workers: workflow and quota locks are process-local. This is a demo,
not authenticated audit storage. See docs/RENDER_SETUP.md.
"""
import datetime as dt
import json
import os
from pathlib import Path
import secrets
import sys
import threading
from urllib.parse import urlsplit

from flask import Flask, jsonify, request, session, Response
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'local_tester'))
import review_app as local
import run


class BrowserStore(local.ReviewStore):
    """New online visitors start empty, never with another person's existing run."""
    def initial_state(self):
        data = json.loads((self.project / 'formal_test_80/inputs.json').read_text())
        return {'schema_version': 1, 'revision': 0, 'created_at': local.now(), 'source_run': None,
            'input_sha256': None, 'model': run.MODEL, 'context': {k: v for k, v in data.items() if k != 'cases'},
            'items': [], 'acceptance': None, 'acceptance_history': [], 'audit_log': []}


class CallBudget:
    """One process-wide daily request cap; browser Reset cannot reset it."""
    def __init__(self, folder, limit, requester):
        self.path = folder / 'call_budget.json'
        self.limit = limit
        self.requester = requester
        self.lock = threading.Lock()
        self.slots = threading.BoundedSemaphore(4)

    def __call__(self, body, key):
        if not self.slots.acquire(blocking=False):
            raise local.DemoLimitError('The demo is busy. Please try again shortly. No API call was made.')
        try:
            with self.lock:
                today = dt.datetime.now(dt.timezone.utc).date().isoformat()
                record = json.loads(self.path.read_text()) if self.path.exists() else {}
                count = record.get('count', 0) if record.get('date') == today else 0
                if count >= self.limit:
                    raise local.DemoLimitError('The demo has reached its daily AI-call limit. Please return after 00:00 UTC or contact the owner.')
                temp = self.path.with_suffix('.tmp')
                temp.write_text(json.dumps({'date': today, 'count': count + 1}))
                temp.replace(self.path)
            return self.requester(body, key)
        finally:
            self.slots.release()


def create_app(storage=None, testing=False, requester=None):
    app = Flask(__name__, static_folder=None)
    app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32),
        MAX_CONTENT_LENGTH=2_000_000, SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=not testing, SESSION_COOKIE_SAMESITE='Lax')
    # Render terminates HTTPS at one proxy; never trust forwarded host names.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=0, x_proto=1, x_host=0)
    origin = (os.environ.get('APP_URL') or os.environ.get('RENDER_EXTERNAL_URL') or '').rstrip('/')
    if not testing and (not origin.startswith('https://') or urlsplit(origin).path):
        raise RuntimeError('Set APP_URL to the HTTPS site origin, or use Render RENDER_EXTERNAL_URL.')
    folder = Path(storage or os.environ.get('DEMO_DATA_DIR', '/tmp/pe6201-demo'))
    folder.mkdir(parents=True, exist_ok=True)
    stores = {}
    store_lock = threading.RLock()
    budget = CallBudget(folder, int(os.environ.get('DEMO_DAILY_CALL_LIMIT', '200')), requester or local.request_ai)
    app.extensions['review_stores'] = stores
    app.extensions['call_budget'] = budget

    def get_store():
        with store_lock:
            sid = session.get('workspace')
            if not isinstance(sid, str) or len(sid) != 48 or any(c not in '0123456789abcdef' for c in sid):
                if len(list((folder / 'sessions').glob('*'))) >= 100:
                    raise local.DemoLimitError('The demo is at visitor capacity. Please contact the owner.')
                sid = secrets.token_hex(24)
                session['workspace'] = sid
            if sid not in stores:
                stores[sid] = BrowserStore(folder / 'sessions' / sid)
            return stores[sid]

    def key():
        value = os.environ.get('OPENROUTER_API_KEY', '').strip()
        if not value:
            raise ValueError('The owner has not configured the demo API key yet.')
        return value

    @app.before_request
    def check_request():
        if request.path == '/health':
            return None
        if origin and (request.host != urlsplit(origin).netloc or request.headers.get('Origin') not in (None, origin)):
            return jsonify(error='Open the demo from its configured website address.'), 403
        if request.path.startswith('/api/'):
            expected = session.get('csrf')
            if not expected or not secrets.compare_digest(expected, request.headers.get('X-Review-Token', '')):
                return jsonify(error='Refresh the page to start your browser session.'), 403

    @app.after_request
    def response_headers(response):
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        return response

    @app.get('/health')
    def health():
        return jsonify(status='ok')

    @app.get('/')
    def index():
        get_store()
        if 'csrf' not in session:
            session['csrf'] = secrets.token_urlsafe(32)
        html = (local.ASSETS / 'index.html').read_text().replace('__REVIEW_TOKEN__', session['csrf'])
        html = html.replace('Local prototype', 'Online demo')
        html = html.replace('<main>', '<main><div class="note">Public synthetic-data demo · your browser has its own workspace. Progress may reset when the free service restarts. Export your results before leaving.</div>')
        return Response(html, mimetype='text/html')

    @app.get('/<asset>')
    def asset_file(asset):
        if asset not in ('app.js', 'style.css'):
            return jsonify(error='Not found.'), 404
        text = (local.ASSETS / asset).read_text()
        if asset == 'app.js':
            text = text.replace('changes saved locally', 'changes saved in your demo workspace').replace('Local prototype', 'Online demo')
            text = text.replace('Download one-case JSON template', 'Download 80-case demo package').replace('source-evidence-template.json', 'demo-evidence-80.json')
        return Response(text, mimetype='text/javascript' if asset == 'app.js' else 'text/css')

    @app.get('/api/state')
    def state():
        return jsonify(get_store().snapshot())

    @app.get('/api/template')
    def template():
        data = json.loads((ROOT / 'formal_test_80/inputs.json').read_text())
        return jsonify(data)

    @app.post('/api/<action>')
    def action_route(action):
        data = request.get_json()
        if not isinstance(data, dict):
            raise ValueError('Invalid request.')
        store = get_store()
        if action == 'reset':
            store.reset_workspace(data)
        elif action == 'import':
            store.import_batch(data)
        elif action == 'source-check':
            store.confirm_and_run(data, key(), requester=budget)
        elif action == 'run':
            store.start(data, key(), requester=budget)
        elif action == 'evidence-run':
            api_key = key()
            with store.lock:
                version = store.supplement(data)
                store.start({'ids': [data['id']], 'versions': {data['id']: version},
                    'reviewer': data['reviewer']}, api_key, requester=budget)
        elif action == 'review':
            store.review(data)
        elif action == 'accept':
            store.accept(data)
        elif action == 'export':
            return Response(store.csv_export(final=data.get('final') is True), mimetype='text/csv')
        else:
            return jsonify(error='Not found.'), 404
        return jsonify(store.snapshot())

    @app.errorhandler(Exception)
    def error(exc):
        if isinstance(exc, (ValueError, KeyError, TypeError, local.DemoLimitError)):
            return jsonify(error=str(exc)), 400
        if isinstance(exc, HTTPException):
            return jsonify(error=exc.description), exc.code
        # Do not expose request bodies, environment variables or credentials.
        return jsonify(error='Demo operation failed. Please retry or contact the owner.'), 500

    return app
