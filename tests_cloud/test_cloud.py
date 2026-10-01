"""Cloud transport tests using temporary stores and fake provider responses only."""
import json
from pathlib import Path
import re
import tempfile
import time
import unittest
from unittest.mock import patch

from cloud_app import create_app, CallBudget, local


class CloudTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.env = patch.dict('os.environ', {'APP_URL': 'https://demo.example', 'OPENROUTER_API_KEY': 'test-key-only', 'DEMO_DAILY_CALL_LIMIT': '2'})
        self.env.start()
        self.calls = []
        def provider(body, key):
            self.calls.append(body)
            case = json.loads(body['messages'][1]['content'])['case']
            result = {'transaction_id': case['transaction_id'], 'recognition_condition': 'Test fixture',
                'qualifying_event_date': None, 'recorded_accounting_date': case['ledger']['accounting_date'],
                'eligible_quantity_by_cutoff': None, 'recorded_quantity_in_2025': None,
                'conclusion': local.run.LABELS[3], 'difference_cny': None, 'explanation': 'Mocked result.',
                'evidence_references': [case['contract']['document_id']], 'additional_evidence_requested': ['Test evidence']}
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(result)}}], 'usage': {'cost': 0}}
        self.app = create_app(self.temp.name, testing=True, requester=provider)
        self.a, self.b = self.app.test_client(), self.app.test_client()
        self.ha = self.open(self.a)
        self.hb = self.open(self.b)

    def tearDown(self):
        for store in self.app.extensions['review_stores'].values():
            for _ in range(200):
                if not store.busy:
                    break
                time.sleep(.01)
        self.env.stop()
        self.temp.cleanup()

    def open(self, client):
        r = client.get('/', base_url='https://demo.example')
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('test-key-only', r.text)
        token = re.search(r'name="review-token" content="([^"]+)"', r.text).group(1)
        return {'X-Review-Token': token}

    def get(self, client, headers, path='/api/state'):
        return client.get(path, headers=headers, base_url='https://demo.example')

    def post(self, client, headers, path, data):
        return client.post('/api/' + path, json=data, headers=headers, base_url='https://demo.example')

    def package(self):
        data = json.loads((local.run.PROJECT / 'formal_test_80/inputs.json').read_text())
        data['cases'] = data['cases'][:1]
        return data

    def test_isolated_import_and_reset(self):
        for client, headers in ((self.a, self.ha), (self.b, self.hb)):
            r = self.post(client, headers, 'import', {'dataset': self.package(), 'revision': 0, 'reviewer': 'Test', 'confirmed': True})
            self.assertEqual(r.status_code, 200)
        state = self.get(self.a, self.ha).json
        self.assertEqual(self.post(self.a, self.ha, 'reset', {'revision': state['revision']}).status_code, 200)
        self.assertEqual(self.get(self.a, self.ha).json['items'], [])
        self.assertEqual(len(self.get(self.b, self.hb).json['items']), 1)

    def test_csrf_origin_and_host_checks(self):
        self.assertEqual(self.get(self.a, self.hb).status_code, 403)
        self.assertEqual(self.get(self.a, {}).status_code, 403)
        headers = dict(self.ha, Origin='https://other.example')
        self.assertEqual(self.post(self.a, headers, 'reset', {'revision': 0}).status_code, 403)
        self.assertEqual(self.a.get('/', base_url='https://other.example').status_code, 403)

    def test_confirmation_calls_model_automatically_once(self):
        self.post(self.a, self.ha, 'import', {'dataset': self.package(), 'revision': 0, 'reviewer': 'Test', 'confirmed': True})
        data = {'id': 'TEST-001', 'version': 0, 'reviewer': 'Test', 'confirmed': True}
        self.assertEqual(self.post(self.a, self.ha, 'source-check', data).status_code, 200)
        for _ in range(200):
            state = self.get(self.a, self.ha).json
            if not state['busy']:
                break
            time.sleep(.01)
        self.assertEqual(state['items'][0]['status'], 'ready')
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.post(self.a, self.ha, 'source-check', data).status_code, 400)
        self.assertEqual(len(self.calls), 1)

    def test_budget_persists_and_reset_cannot_bypass_it(self):
        budget = self.app.extensions['call_budget']
        budget.requester = lambda body, key: {}
        budget({}, 'fake'); budget({}, 'fake')
        self.post(self.a, self.ha, 'reset', {'revision': 0})
        with self.assertRaises(local.DemoLimitError):
            budget({}, 'fake')
        reopened = CallBudget(Path(self.temp.name), 2, lambda body, key: {})
        with self.assertRaises(local.DemoLimitError):
            reopened({}, 'fake')

    def test_health_sample_and_empty_acceptance(self):
        self.assertEqual(self.a.get('/health').status_code, 200)
        sample = self.get(self.a, self.ha, '/api/template').json
        self.assertEqual(len(sample['cases']), 80)
        self.assertNotIn('answers', sample)
        self.assertFalse(self.get(self.a, self.ha).json['can_accept'])
        self.assertEqual(self.post(self.a, self.ha, 'export', {'final': True}).status_code, 400)


if __name__ == '__main__':
    unittest.main()
