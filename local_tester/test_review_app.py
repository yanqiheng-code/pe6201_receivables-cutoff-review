"""Offline workflow tests. Never call a paid provider or edit evaluation runs."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import review_app
import run


class ReviewWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        fixtures = root / 'runs' / '20261001_fixture_live'
        fixtures.mkdir(parents=True)
        data = json.loads((run.PROJECT / 'formal_test_80' / 'inputs.json').read_text())
        rows = []
        for case in data['cases']:
            ident = case['transaction_id']
            result = {'transaction_id': ident, 'recognition_condition': 'Synthetic test fixture',
                'qualifying_event_date': None, 'recorded_accounting_date': case['ledger']['accounting_date'],
                'eligible_quantity_by_cutoff': 0, 'recorded_quantity_in_2025': 0,
                'conclusion': run.LABELS[0], 'difference_cny': 0, 'explanation': 'Synthetic fixture, not model evidence.',
                'evidence_references': [case['contract']['document_id']], 'additional_evidence_requested': []}
            if ident == 'TEST-009':
                result.update(conclusion=run.LABELS[3], difference_cny=None)
            if ident == 'TEST-069':
                result.update(conclusion=run.LABELS[1], difference_cny=48000)
            rows.append({'transaction_id': ident, 'result': result, 'reported_cost_usd': 0})
        run.save(fixtures / 'results.json', rows)
        run.save(fixtures / 'manifest.json', {'dataset': 'formal_test_80',
            'inputs_sha256': hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()})
        self.store = review_app.ReviewStore(root / 'workspace', runs=root / 'runs')
        for item in self.store.state['items']:
            self.store.confirm_source({'id': item['id'], 'version': item['version'], 'reviewer': 'Test auditor', 'confirmed': True})
        self.item = self.store.item('TEST-009')

    def tearDown(self):
        self.temp.cleanup()

    def evidence(self):
        return {'id': self.item['id'], 'version': self.item['version'], 'reviewer': 'Test auditor',
            'field': 'actual_dispatch_date', 'date': '2025-12-30', 'quantity': 120,
            'source_reference': 'DEMO-COLLECTION-009', 'note': 'Verified synthetic customer collection record.', 'confirmed': True}

    def test_import_preserves_observed_ai_flaw(self):
        self.assertEqual(len(self.store.state['items']), 80)
        self.assertEqual(self.store.item('TEST-069')['result']['conclusion'], run.LABELS[1])
        self.assertIsNone(self.store.item('TEST-069')['review'])

    def test_acceptance_and_final_export_blocked_until_all_reviewed(self):
        with self.assertRaises(ValueError):
            self.store.accept({'revision': self.store.state['revision'], 'reviewer': 'Test', 'note': 'Test', 'confirmed': True})
        with self.assertRaises(ValueError):
            self.store.csv_export(final=True)

    def test_source_check_gates_ai_before_any_request(self):
        self.item['source_check'] = None
        with self.assertRaisesRegex(ValueError, 'step 01'):
            self.store.start({'ids': [self.item['id']], 'versions': {self.item['id']: self.item['version']}, 'reviewer': 'Test'}, 'fake')
        self.assertFalse(self.store.busy)

    def test_source_confirmation_automatically_runs_once(self):
        self.item['source_check'] = None
        calls = []
        result = copy.deepcopy(self.item['result'])
        def fake_request(body, key):
            calls.append(body)
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(result)}}]}
        data = {'id': self.item['id'], 'version': self.item['version'], 'reviewer': 'Test auditor', 'confirmed': True}
        worker = self.store.confirm_and_run(data, 'fake', requester=fake_request)
        worker.join(5)
        self.assertFalse(worker.is_alive())
        self.assertEqual(len(calls), 1)
        self.assertIsNotNone(self.item['source_check'])
        self.assertEqual(self.item['status'], 'ready')
        with self.assertRaises(ValueError):
            self.store.confirm_and_run(data, 'fake', requester=fake_request)
        self.assertEqual(len(calls), 1)

    def test_reset_clears_demo_data_and_stays_empty_after_restart(self):
        for name in ('attempts', 'archives'):
            folder = self.store.folder / name
            folder.mkdir()
            (folder / 'test.json').write_text('{}')
        original = (self.store.runs / '20261001_fixture_live/results.json').read_bytes()
        self.store.reset_workspace({'revision': self.store.state['revision']})
        self.assertEqual(self.store.state['items'], [])
        self.assertFalse(self.store.snapshot()['can_accept'])
        self.assertFalse((self.store.folder / 'attempts').exists())
        self.assertFalse((self.store.folder / 'archives').exists())
        self.assertEqual((self.store.runs / '20261001_fixture_live/results.json').read_bytes(), original)
        reloaded = review_app.ReviewStore(self.store.folder, runs=self.store.runs)
        self.assertEqual(reloaded.state['items'], [])
        with self.assertRaises(ValueError):
            reloaded.accept({'revision': reloaded.state['revision'], 'confirmed': True, 'reviewer': 'Test', 'note': 'Empty'})

    def test_reset_rejects_active_run_or_stale_page(self):
        with self.assertRaises(ValueError):
            self.store.reset_workspace({'revision': -1})
        self.store.busy = True
        with self.assertRaises(ValueError):
            self.store.reset_workspace({'revision': self.store.state['revision']})
        self.assertEqual(len(self.store.state['items']), 80)

    def test_import_archives_previous_batch_and_requires_new_checks(self):
        dataset = json.loads((run.PROJECT / 'formal_test_80/inputs.json').read_text())
        dataset['cases'] = dataset['cases'][:2]
        self.store.import_batch({'dataset': dataset, 'revision': self.store.state['revision'], 'reviewer': 'Test auditor', 'confirmed': True})
        self.assertEqual(len(self.store.state['items']), 2)
        self.assertTrue(all(i['source_check'] is None and i['result'] is None for i in self.store.state['items']))
        self.assertEqual(len(list((self.store.folder / 'archives').glob('*.json'))), 1)

    def test_import_rejects_unsafe_case_ids_without_changing_workspace(self):
        dataset = json.loads((run.PROJECT / 'formal_test_80/inputs.json').read_text())
        dataset['cases'] = dataset['cases'][:1]
        dataset['cases'][0]['transaction_id'] = '../../bad'
        with self.assertRaises(ValueError):
            self.store.import_batch({'dataset': dataset, 'revision': self.store.state['revision'], 'reviewer': 'Test', 'confirmed': True})
        self.assertEqual(len(self.store.state['items']), 80)

    def test_supplement_requires_confirmation_and_current_version(self):
        data = self.evidence()
        data['confirmed'] = False
        with self.assertRaises(ValueError):
            self.store.supplement(data)
        data['confirmed'] = True
        self.store.supplement(data)
        with self.assertRaises(ValueError):
            self.store.supplement(data)
        self.assertEqual(self.item['original_case']['delivery']['actual_dispatch_date'], None)
        self.assertEqual(self.item['case']['delivery']['actual_dispatch_date'], '2025-12-30')
        self.assertEqual(self.item['status'], 'needs_rerun')

    def test_review_is_invalidated_and_original_ai_survives_rerun(self):
        original = copy.deepcopy(self.item['attempts'][0])
        self.store.review({'id': self.item['id'], 'version': self.item['version'], 'reviewer': 'Test auditor',
            'conclusion': run.LABELS[0], 'difference_cny': 0, 'note': 'Fixture review for invalidation test.', 'confirmed': True})
        self.store.supplement(self.evidence())
        self.assertIsNone(self.item['review'])
        self.assertEqual(len(self.item['review_history']), 1)
        result = copy.deepcopy(original['result'])
        result.update(qualifying_event_date='2025-12-30', eligible_quantity_by_cutoff=120,
            conclusion=run.LABELS[0], difference_cny=0, additional_evidence_requested=[])
        def fake_request(body, key):
            content = json.loads(body['messages'][1]['content'])
            self.assertEqual(content['case']['delivery']['actual_dispatch_date'], '2025-12-30')
            self.assertIn('reviewer_supplements', content['case']['delivery'])
            self.assertNotIn('answers', content)
            self.assertNotIn('answer_key', json.dumps(body))
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(result)}}], 'usage': {'cost': .001}}
        thread = self.store.start({'ids': [self.item['id']], 'versions': {self.item['id']: self.item['version']}, 'reviewer': 'Test auditor'}, 'fake', requester=fake_request)
        thread.join(5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(self.item['status'], 'ready')
        self.assertEqual(self.item['attempts'][0], original)
        self.assertEqual(len(self.item['attempts']), 2)
        self.assertEqual(self.item['result'], result)
        reloaded = review_app.ReviewStore(Path(self.temp.name) / 'workspace')
        self.assertEqual(reloaded.item('TEST-009')['result'], result)

    def test_failure_is_saved_and_not_retried(self):
        calls = []
        def incomplete(body, key):
            calls.append(body)
            return {'choices': [{'finish_reason': 'length'}], 'usage': {'cost': .01}}
        ids = ['TEST-009', 'TEST-010']
        thread = self.store.start({'ids': ids, 'versions': {x: self.store.item(x)['version'] for x in ids}, 'reviewer': 'Test auditor'}, 'fake', requester=incomplete)
        thread.join(5)
        self.assertEqual(len(calls), 1)
        self.assertEqual(self.item['status'], 'failed')
        self.assertIsNone(self.item['result'])
        self.assertEqual(self.item['attempts'][-1]['reported_cost_usd'], .01)
        self.assertEqual(self.store.item('TEST-010')['status'], 'needs_rerun')

    def test_full_acceptance_is_revoked_by_new_evidence(self):
        for item in self.store.state['items']:
            item['status'] = 'reviewed'
            item['review'] = {'conclusion': run.LABELS[0], 'difference_cny': 0, 'reviewer': 'Test auditor'}
        self.store.accept({'revision': self.store.state['revision'], 'reviewer': 'Test auditor', 'note': 'Offline acceptance fixture.', 'confirmed': True})
        self.assertIn('Accepted', self.store.csv_export(final=True))
        self.store.supplement(self.evidence())
        self.assertIsNone(self.store.state['acceptance'])
        self.assertEqual(len(self.store.state['acceptance_history']), 1)


if __name__ == '__main__':
    unittest.main()
