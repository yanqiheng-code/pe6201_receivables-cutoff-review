"""Run this file in VS Code, then open http://127.0.0.1:8765.

Local, single-user audit review prototype. Uses only the Python standard library.
Original evaluation runs and ground truth are never modified or scored here.
"""
import copy
import csv
import datetime as dt
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import math
import os
from pathlib import Path
import runpy
import secrets
import shutil
import ssl
import threading
import time
import urllib.error
import urllib.request

import run

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'review_web'
WORKSPACE = ROOT / 'review_workspace'
FIELDS = {
    'actual_dispatch_date': 'dispatched_quantity',
    'actual_customer_receipt_date': 'received_quantity',
    'actual_customer_acceptance_date': 'accepted_quantity',
}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def required(value, label, limit=3000):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f'{label} is required (maximum {limit} characters).')
    return value.strip()


def settings_key():
    path = ROOT / 'config.py'
    settings = runpy.run_path(str(path)) if path.exists() else {}
    if settings.get('MODEL', run.MODEL) != run.MODEL or settings.get('BASE_URL', run.BASE_URL) != run.BASE_URL:
        raise ValueError('Use the existing supported model and OpenRouter endpoint in config.py.')
    key = settings.get('API_KEY') or os.environ.get('OPENROUTER_API_KEY', '')
    if not isinstance(key, str) or not key.strip():
        raise ValueError('Add your OpenRouter API key to local config.py before running AI. Saved results are available without a key.')
    return key.strip()


def request_ai(body, key):
    req = urllib.request.Request(run.BASE_URL + '/chat/completions',
        data=json.dumps(body).encode(), method='POST',
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60, context=ssl.create_default_context()) as response:
        return json.load(response)


class ReviewStore:
    def __init__(self, folder=WORKSPACE, project=run.PROJECT, runs=None):
        self.folder = Path(folder)
        self.project = Path(project)
        self.runs = Path(runs) if runs is not None else ROOT / 'runs'
        self.folder.mkdir(parents=True, exist_ok=True)
        self.path = self.folder / 'session.json'
        self.lock = threading.RLock()
        self.busy = False
        if self.path.exists():
            self.state = json.loads(self.path.read_text(encoding='utf-8'))
            for item in self.state['items']:
                item.setdefault('source_check', None)
                if item['status'] in ('running', 'queued'):
                    item['status'] = 'failed'
                    item['error'] = 'Previous run interrupted. Review before retrying; the provider may have charged for it.'
            self.persist()
        else:
            self.state = self.initial_state()
            self.persist()

    def initial_state(self):
        data = json.loads((self.project / 'formal_test_80' / 'inputs.json').read_text(encoding='utf-8'))
        digest = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        imported = {}
        source = None
        for folder in sorted(self.runs.glob('*_live'), reverse=True):
            try:
                manifest = json.loads((folder / 'manifest.json').read_text())
                rows = json.loads((folder / 'results.json').read_text())
                ids = {c['transaction_id'] for c in data['cases']}
                if (manifest.get('dataset') != 'formal_test_80' or manifest.get('inputs_sha256') != digest
                        or {r['transaction_id'] for r in rows} != ids or len(rows) != len(ids)
                        or not all(r.get('result') for r in rows)):
                    continue
                by_id = {c['transaction_id']: c for c in data['cases']}
                for row in rows:
                    run.validate(row['result'], by_id[row['transaction_id']])
                imported = {r['transaction_id']: r for r in rows}
                source = folder.name
                break
            except (OSError, ValueError, KeyError, TypeError):
                continue
        items = []
        for case in data['cases']:
            ident = case['transaction_id']
            original = imported.get(ident)
            attempt = {'id': 'imported', 'kind': 'saved evaluation', 'at': now(), 'evidence_version': 0,
                'result': original['result'], 'reported_cost_usd': original.get('reported_cost_usd'),
                'source_run': source} if original else None
            items.append({'id': ident, 'case': case, 'original_case': copy.deepcopy(case),
                'version': 0, 'evidence_version': 0, 'evidence': [], 'attempts': [attempt] if attempt else [],
                'result': copy.deepcopy(attempt['result']) if attempt else None,
                'status': 'ready' if attempt else 'unrun', 'source_check': None, 'review': None, 'review_history': [], 'error': None})
        return {'schema_version': 1, 'revision': 0, 'created_at': now(), 'source_run': source,
            'input_sha256': digest, 'model': run.MODEL, 'context': {k: v for k, v in data.items() if k != 'cases'},
            'items': items, 'acceptance': None, 'acceptance_history': [], 'audit_log': []}

    def persist(self):
        temp = self.path.with_suffix('.tmp')
        temp.write_text(json.dumps(self.state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temp.replace(self.path)

    def import_batch(self, data):
        """Import structured records without a model call; archive the previous workspace."""
        with self.lock:
            if self.busy:
                raise ValueError('Wait for the current run to finish.')
            if data.get('revision') != self.state['revision'] or data.get('confirmed') is not True:
                raise ValueError('Confirm the new batch and refresh if the workspace changed.')
            reviewer = required(data.get('reviewer'), 'Reviewer name', 100)
            dataset = data.get('dataset')
            if not isinstance(dataset, dict) or not isinstance(dataset.get('cases'), list) or not 1 <= len(dataset['cases']) <= 200:
                raise ValueError('Upload a JSON dataset with 1–200 cases.')
            if dataset.get('reporting_period_start') != '2025-01-01' or dataset.get('cutoff_date') != '2025-12-31' or dataset.get('currency') != 'CNY':
                raise ValueError('This prototype supports FY2025, cut-off 2025-12-31 and CNY. Use the template.')
            through = dataset.get('records_available_through')
            if not isinstance(through, str) or dt.date.fromisoformat(through).isoformat() != through or through < '2025-12-31':
                raise ValueError('Provide a valid records_available_through date.')
            if not isinstance(dataset.get('assumptions'), list) or not all(isinstance(v, str) for v in dataset['assumptions']):
                raise ValueError('Include the dataset assumptions from the template.')
            template = json.loads((self.project / 'formal_test_80/inputs.json').read_text())['cases'][0]
            def check_shape(value, example):
                if isinstance(example, dict):
                    if not isinstance(value, dict) or set(value) != set(example):
                        raise ValueError('Record fields must match the template exactly; do not include answer labels.')
                    for k, v in example.items():
                        check_shape(value[k], v)
                elif type(example) in (int, float) and type(value) in (int, float):
                    pass
                elif example is not None and type(value) is not type(example) and value is not None:
                    raise ValueError('Record field types must match the template.')
            ids = set()
            items = []
            for case in dataset['cases']:
                check_shape(case, template)
                ident = required(case.get('transaction_id'), 'Transaction ID', 60)
                if not all(c.isascii() and (c.isalnum() or c in '-_') for c in ident) or ident in ids:
                    raise ValueError('Use unique transaction IDs with letters, numbers, hyphens or underscores.')
                ids.add(ident)
                for name in ('contract', 'ledger', 'invoice', 'delivery'):
                    required(case[name]['document_id'], 'Document ID', 100)
                for name in ('ledger', 'invoice'):
                    if case[name]['transaction_id'] != ident:
                        raise ValueError('Document transaction IDs must agree.')
                for name in ('customer', 'goods', 'terms'):
                    required(case['contract'][name], name, 10000)
                for date in [case['ledger']['accounting_date'], case['invoice']['invoice_date']] + [case['delivery'][k] for k in FIELDS if case['delivery'][k] is not None]:
                    if not isinstance(date, str) or dt.date.fromisoformat(date).isoformat() != date:
                        raise ValueError('Use ISO dates or null for missing delivery dates.')
                q = case['contract']['quantity']
                if type(q) is not int or q <= 0:
                    raise ValueError('Contract quantity must be a positive integer.')
                for value in [case['contract']['unit_price_cny'], case['contract']['total_price_cny'], case['invoice']['amount_cny'], case['ledger']['entry']['debit_cny'], case['ledger']['entry']['credit_cny']]:
                    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                        raise ValueError('Amounts must be finite non-negative numbers.')
                for field in FIELDS.values():
                    v = case['delivery'][field]
                    if v is not None and (type(v) is not int or v != q):
                        raise ValueError('Delivery quantities must be the full batch or null.')
                items.append({'id': ident, 'case': copy.deepcopy(case), 'original_case': copy.deepcopy(case),
                    'version': 0, 'evidence_version': 0, 'evidence': [], 'attempts': [], 'result': None,
                    'status': 'unrun', 'source_check': None, 'review': None, 'review_history': [], 'error': None})
            archive = self.folder / 'archives'
            archive.mkdir(exist_ok=True)
            run.save(archive / (dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json'), self.state)
            previous_revision = self.state['revision']
            self.state = {'schema_version': 1, 'revision': previous_revision + 1, 'created_at': now(), 'source_run': None,
                'input_sha256': hashlib.sha256(json.dumps(dataset, sort_keys=True).encode()).hexdigest(), 'model': run.MODEL,
                'context': {k: dataset[k] for k in ('reporting_period_start', 'cutoff_date', 'records_available_through', 'currency', 'assumptions')},
                'items': items, 'acceptance': None, 'acceptance_history': [], 'audit_log': []}
            self.log('Structured evidence batch imported; no AI calls', reviewer)
            self.persist()

    def reset_workspace(self, data):
        """Clear only demo state and its artifacts; never touch project data or evaluation runs."""
        with self.lock:
            if self.busy:
                raise ValueError('Wait for the AI run to finish before resetting.')
            if data.get('revision') != self.state['revision']:
                raise ValueError('The workspace changed. Refresh before resetting.')
            revision = self.state['revision'] + 1
            template = json.loads((self.project / 'formal_test_80/inputs.json').read_text())
            context = {k: template[k] for k in ('reporting_period_start', 'cutoff_date', 'records_available_through', 'currency', 'assumptions')}
            for name in ('attempts', 'archives'):
                path = self.folder / name
                if path.is_symlink():
                    path.unlink()
                elif path.exists():
                    shutil.rmtree(path)
            self.state = {'schema_version': 1, 'revision': revision, 'created_at': now(),
                'source_run': None, 'input_sha256': None, 'model': run.MODEL, 'context': context,
                'items': [], 'acceptance': None, 'acceptance_history': [], 'audit_log': []}
            self.persist()

    def confirm_source(self, data):
        with self.lock:
            item = self.item(data.get('id'))
            self.check_version(item, data)
            if self.busy or data.get('confirmed') is not True:
                raise ValueError('Confirm the source check while no AI run is active.')
            reviewer = required(data.get('reviewer'), 'Reviewer name', 100)
            item['source_check'] = {'reviewer': reviewer, 'at': now(), 'evidence_version': item['evidence_version']}
            item['version'] += 1
            self.log('Human verified structured source records', reviewer, item['id'])
            self.persist()

    def item(self, ident):
        for item in self.state['items']:
            if item['id'] == ident:
                return item
        raise ValueError('Unknown transaction.')

    def check_version(self, item, data):
        if data.get('version') != item['version']:
            raise ValueError('This transaction changed. Refresh and review the latest version.')

    def log(self, action, reviewer, ident=None):
        self.state['revision'] += 1
        self.state['audit_log'].append({'at': now(), 'action': action, 'reviewer': reviewer, 'transaction_id': ident})

    def invalidate(self, item):
        if item['review']:
            item['review_history'].append(item['review'])
            item['review'] = None
        if self.state['acceptance']:
            self.state['acceptance_history'].append(self.state['acceptance'])
            self.state['acceptance'] = None

    def snapshot(self):
        with self.lock:
            state = copy.deepcopy(self.state)
            state['busy'] = self.busy
            state['labels'] = run.LABELS
            state['can_accept'] = bool(state['items']) and all(i['status'] == 'reviewed' and i['review'] for i in state['items'])
            return state

    def supplement(self, data):
        with self.lock:
            if self.busy:
                raise ValueError('Wait for the current AI run to finish.')
            item = self.item(data.get('id'))
            self.check_version(item, data)
            if not item.get('source_check'):
                raise ValueError('Complete the initial source check in step 01 before supplementing.')
            reviewer = required(data.get('reviewer'), 'Reviewer name', 100)
            field = data.get('field')
            if field not in FIELDS:
                raise ValueError('Choose a supported delivery event.')
            date = required(data.get('date'), 'Event date', 10)
            if dt.date.fromisoformat(date).isoformat() != date:
                raise ValueError('Use a date in YYYY-MM-DD format.')
            if date > self.state['context']['records_available_through']:
                raise ValueError('The event must fall within the available-records period.')
            quantity = data.get('quantity')
            if type(quantity) is not int or quantity != item['case']['contract']['quantity']:
                raise ValueError('This single-batch prototype requires the full contract quantity.')
            source = required(data.get('source_reference'), 'Supporting document reference', 200)
            note = required(data.get('note'), 'Evidence note')
            if data.get('confirmed') is not True:
                raise ValueError('Confirm that you checked the supporting evidence.')
            proposed = copy.deepcopy(item['case']['delivery'])
            proposed[field] = date
            proposed[FIELDS[field]] = quantity
            chronology = [proposed[k] for k in FIELDS if proposed.get(k)]
            if chronology != sorted(chronology):
                raise ValueError('Dispatch, receipt and acceptance dates must be in chronological order.')
            evidence = {'at': now(), 'reviewer': reviewer, 'field': field, 'previous_date': item['case']['delivery'].get(field),
                'date': date, 'quantity': quantity, 'source_reference': source, 'note': note,
                'evidence_version': item['evidence_version'] + 1, 'confirmed': True}
            self.invalidate(item)
            item['case']['delivery'] = proposed
            item['evidence'].append(evidence)
            # Incorporate the verified supplement into the same delivery document.
            # The source identifier remains stable so the existing reference validator still applies.
            item['case']['delivery']['reviewer_supplements'] = copy.deepcopy(item['evidence'])
            item['evidence_version'] += 1
            item['source_check'] = {'reviewer': reviewer, 'at': now(), 'evidence_version': item['evidence_version']}
            item['version'] += 1
            item['status'] = 'needs_rerun'
            item['error'] = None
            self.log('Evidence supplied; previous review invalidated', reviewer, item['id'])
            self.persist()
            return item['version']

    def confirm_and_run(self, data, key, requester=request_ai):
        """One human action records source verification and starts one model request."""
        with self.lock:
            self.confirm_source(data)
            item = self.item(data['id'])
            return self.start({'ids': [item['id']], 'versions': {item['id']: item['version']},
                'reviewer': data['reviewer']}, key, requester=requester)

    def start(self, data, key, requester=request_ai):
        with self.lock:
            if self.busy:
                raise ValueError('An AI run is already in progress.')
            reviewer = required(data.get('reviewer'), 'Reviewer name', 100)
            ids = data.get('ids')
            if not isinstance(ids, list) or not ids or len(ids) != len(set(ids)):
                raise ValueError('Select at least one transaction.')
            items = [self.item(ident) for ident in ids]
            versions = data.get('versions', {})
            for item in items:
                self.check_version(item, {'version': versions.get(item['id'])})
                if not item.get('source_check') or item['source_check']['evidence_version'] != item['evidence_version']:
                    raise ValueError('Confirm the source evidence in step 01 before running AI.')
            prompt = (self.project / 'accounts_receivable_cutoff_prompt_v1.1.md').read_text(encoding='utf-8')
            for item in items:
                self.invalidate(item)
                item['status'] = 'queued'
                item['error'] = None
                item['version'] += 1
                self.log('AI run requested; previous review invalidated', reviewer, item['id'])
            self.busy = True
            self.persist()
            worker = threading.Thread(target=self._worker, args=(ids, reviewer, prompt, key, requester), daemon=True)
            worker.start()
            return worker

    def _worker(self, ids, reviewer, prompt, key, requester):
        try:
            for ident in ids:
                with self.lock:
                    item = self.item(ident)
                    item['status'] = 'running'
                    case = copy.deepcopy(item['case'])
                    attempt_id = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '_' + ident
                    folder = self.folder / 'attempts' / attempt_id
                    folder.mkdir(parents=True)
                    body = run.payload(prompt, self.state['context'], case)
                    run.save(folder / 'request.json', body)
                    (folder / 'prompt_snapshot.md').write_text(prompt, encoding='utf-8')
                    attempt = {'id': attempt_id, 'kind': 'live review', 'at': now(), 'reviewer': reviewer,
                        'evidence_version': item['evidence_version'], 'result': None, 'reported_cost_usd': None,
                        'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(), 'error': None}
                    self.persist()
                start = time.monotonic()
                try:
                    raw = requester(body, key)
                    run.save(folder / 'response.json', raw)
                    attempt['reported_cost_usd'] = run.cost(raw.get('usage'))
                    attempt['result'] = run.parse_response(raw, case)
                except urllib.error.HTTPError as exc:
                    attempt['error'] = f'OpenRouter HTTP {exc.code}. Check access, billing or rate limits. No automatic retry.'
                except (urllib.error.URLError, TimeoutError, OSError):
                    attempt['error'] = 'Network, TLS or timeout failure. No automatic retry. A failed request may still incur a charge.'
                except (ValueError, TypeError, KeyError):
                    attempt['error'] = 'The AI response did not pass format validation. Raw response retained locally. No automatic retry.'
                except Exception:
                    attempt['error'] = 'Unexpected request failure. No automatic retry; check local attempt records.'
                attempt['elapsed_seconds'] = round(time.monotonic() - start, 3)
                run.save(folder / 'attempt.json', attempt)
                with self.lock:
                    item = self.item(ident)
                    item['attempts'].append(attempt)
                    item['result'] = attempt['result']
                    item['error'] = attempt['error']
                    item['status'] = 'ready' if attempt['result'] else 'failed'
                    item['version'] += 1
                    self.log('AI run completed' if attempt['result'] else 'AI run failed', reviewer, ident)
                    self.persist()
                    if attempt['error']:
                        # Stop the batch rather than repeatedly spending on a failing connection.
                        break
        finally:
            with self.lock:
                for ident in ids:
                    item = self.item(ident)
                    if item['status'] in ('queued', 'running'):
                        item['status'] = 'needs_rerun'
                        item['error'] = 'Batch stopped. This transaction needs a new run.'
                self.busy = False
                self.persist()

    def review(self, data):
        with self.lock:
            item = self.item(data.get('id'))
            self.check_version(item, data)
            if item['status'] not in ('ready', 'reviewed') or not item['result']:
                raise ValueError('Run AI on the latest evidence before completing review.')
            if not item.get('source_check') or item['source_check']['evidence_version'] != item['evidence_version']:
                raise ValueError('Confirm the source evidence in step 01 before completing review.')
            reviewer = required(data.get('reviewer'), 'Reviewer name', 100)
            if data.get('confirmed') is not True:
                raise ValueError('Confirm that you checked the evidence and AI result.')
            conclusion = data.get('conclusion')
            if conclusion not in run.LABELS[:3]:
                raise ValueError('Resolve evidence requests or scope issues before closing the transaction.')
            amount = data.get('difference_cny')
            if type(amount) not in (int, float) or not math.isfinite(amount) or amount < 0:
                raise ValueError('Enter a finite, non-negative final difference.')
            if (conclusion == run.LABELS[0] and amount != 0) or (conclusion in run.LABELS[1:3] and amount <= 0):
                raise ValueError('Use zero for no exception, or a positive difference for an identified error.')
            changed = conclusion != item['result']['conclusion'] or amount != item['result']['difference_cny']
            note = required(data.get('note'), 'Review rationale')
            self.invalidate(item)
            item['review'] = {'at': now(), 'reviewer': reviewer, 'conclusion': conclusion, 'difference_cny': amount,
                'note': note, 'decision': 'overridden' if changed else 'confirmed', 'evidence_version': item['evidence_version'],
                'attempt_id': item['attempts'][-1]['id'], 'confirmed': True}
            item['status'] = 'reviewed'
            item['version'] += 1
            self.log('Human conclusion recorded', reviewer, item['id'])
            self.persist()

    def accept(self, data):
        with self.lock:
            if data.get('revision') != self.state['revision']:
                raise ValueError('The summary changed. Refresh before acceptance.')
            if self.busy or not self.state['items'] or not all(i['status'] == 'reviewed' and i['review'] for i in self.state['items']):
                raise ValueError('Every transaction needs a completed human review before batch acceptance.')
            if data.get('confirmed') is not True:
                raise ValueError('Confirm that you reviewed the complete summary.')
            reviewer = required(data.get('reviewer'), 'Accepting reviewer', 100)
            note = required(data.get('note'), 'Acceptance note')
            if self.state['acceptance']:
                self.state['acceptance_history'].append(self.state['acceptance'])
            self.state['acceptance'] = {'at': now(), 'reviewer': reviewer, 'note': note, 'confirmed': True}
            self.log('Batch accepted', reviewer)
            self.persist()

    def csv_export(self, final=False):
        with self.lock:
            if final and not self.state['acceptance']:
                raise ValueError('Accept the batch before exporting the final summary.')
            stream = io.StringIO(newline='')
            writer = csv.writer(stream)
            writer.writerow(['Transaction', 'Customer', 'AI conclusion', 'AI difference CNY', 'Human conclusion',
                'Human difference CNY', 'Review status', 'Decision', 'Reviewer', 'Review rationale', 'Reviewed UTC',
                'Evidence version', 'Latest attempt', 'Imported run', 'Batch status', 'Accepted by', 'Accepted UTC'])
            def safe(value):
                text = '' if value is None else str(value)
                return "'" + text if text.lstrip().startswith(('=', '+', '-', '@')) else text
            for item in self.state['items']:
                ai, human, acceptance = item['result'] or {}, item['review'] or {}, self.state['acceptance'] or {}
                row = [item['id'], item['case']['contract']['customer'], ai.get('conclusion'), ai.get('difference_cny'),
                    human.get('conclusion'), human.get('difference_cny'), item['status'], human.get('decision'),
                    human.get('reviewer'), human.get('note'), human.get('at'), item['evidence_version'],
                    item['attempts'][-1]['id'] if item['attempts'] else '', self.state['source_run'],
                    'Accepted' if acceptance else 'Draft', acceptance.get('reviewer'), acceptance.get('at')]
                writer.writerow([safe(v) for v in row])
            return '\ufeff' + stream.getvalue()


def serve(port=8765):
    store = ReviewStore()
    token = secrets.token_urlsafe(32)
    origin = f'http://127.0.0.1:{port}'

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def respond(self, code, body, content_type='application/json; charset=utf-8'):
            if isinstance(body, (dict, list)):
                body = json.dumps(body, ensure_ascii=False).encode()
            elif isinstance(body, str):
                body = body.encode()
            self.send_response(code)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            self.end_headers()
            self.wfile.write(body)

        def allowed(self, api=False):
            if self.headers.get('Host') != f'127.0.0.1:{port}':
                self.respond(403, {'error': 'Use the local 127.0.0.1 address.'})
                return False
            if self.headers.get('Origin') not in (None, origin) or (api and not secrets.compare_digest(self.headers.get('X-Review-Token', ''), token)):
                self.respond(403, {'error': 'Open the local review page and try again.'})
                return False
            return True

        def do_GET(self):
            if not self.allowed(self.path.startswith('/api/')):
                return
            if self.path == '/api/state':
                self.respond(200, store.snapshot())
            elif self.path == '/api/template':
                data = json.loads((run.PROJECT / 'formal_test_80/inputs.json').read_text())
                data['cases'] = data['cases'][:1]
                self.respond(200, data)
            elif self.path in ('/', '/app.js', '/style.css'):
                name = {'/': 'index.html', '/app.js': 'app.js', '/style.css': 'style.css'}[self.path]
                content = (ASSETS / name).read_text(encoding='utf-8').replace('__REVIEW_TOKEN__', token)
                self.respond(200, content, {'/': 'text/html', '/app.js': 'text/javascript', '/style.css': 'text/css'}[self.path] + '; charset=utf-8')
            elif self.path == '/favicon.ico':
                self.respond(204, b'')
            else:
                self.respond(404, {'error': 'Not found.'})

        def do_POST(self):
            if not self.allowed(True):
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length < 1 or length > 2000000:
                    raise ValueError('Invalid request size.')
                data = json.loads(self.rfile.read(length))
                if not isinstance(data, dict):
                    raise ValueError('Invalid request.')
                if self.path == '/api/reset':
                    store.reset_workspace(data)
                elif self.path == '/api/import':
                    store.import_batch(data)
                elif self.path == '/api/source-check':
                    store.confirm_and_run(data, settings_key())
                elif self.path == '/api/run':
                    store.start(data, settings_key())
                elif self.path == '/api/evidence-run':
                    key = settings_key()
                    with store.lock:
                        version = store.supplement(data)
                        store.start({'ids': [data['id']], 'versions': {data['id']: version}, 'reviewer': data['reviewer']}, key)
                elif self.path == '/api/review':
                    store.review(data)
                elif self.path == '/api/accept':
                    store.accept(data)
                elif self.path == '/api/export':
                    return self.respond(200, store.csv_export(final=data.get('final') is True), 'text/csv; charset=utf-8')
                else:
                    return self.respond(404, {'error': 'Not found.'})
                self.respond(200, store.snapshot())
            except (ValueError, KeyError, TypeError) as exc:
                self.respond(400, {'error': str(exc)})
            except Exception:
                self.respond(500, {'error': 'Local operation failed. Check that the workspace is writable and config.py is valid.'})

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print(f'Cut-off Review is ready: {origin}', flush=True)
    print('Open this address in your browser. Saved results load without API calls. Stop with Ctrl+C.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nReview workspace saved. Goodbye.')
    finally:
        server.server_close()


if __name__ == '__main__':
    serve()
