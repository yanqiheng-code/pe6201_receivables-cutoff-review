import json
import unittest
from unittest.mock import patch
import run

class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((run.PROJECT/'development_examples_20/inputs.json').read_text())
        self.answers=json.loads((run.PROJECT/'development_examples_20/answer_key.json').read_text())['answers']
        self.case=self.data['cases'][2]
    def prediction(self):
        return {'transaction_id':'DEV-03','recognition_condition':'Carrier handover','qualifying_event_date':'2026-01-02','recorded_accounting_date':'2025-12-30','eligible_quantity_by_cutoff':0,'recorded_quantity_in_2025':100,'conclusion':run.LABELS[1],'difference_cny':10000,'explanation':'Handover occurred after the cut-off.','evidence_references':['CON-03','DEL-03','LED-03'],'additional_evidence_requested':[]}
    def test_request_contains_only_selected_case_and_no_answers(self):
        context={k:v for k,v in self.data.items() if k!='cases'}
        with patch.object(run.Path,'read_text',side_effect=AssertionError('No evaluator read allowed')):
            body=run.payload('Rules',context,self.case)
        parsed=json.loads(body['messages'][1]['content'])
        self.assertEqual(parsed['case']['transaction_id'],'DEV-03')
        self.assertNotIn('cases',parsed['context'])
        self.assertNotIn('conclusion',parsed['case'])
        self.assertTrue(body['provider']['require_parameters'])
        self.assertEqual(body['model'],'openai/gpt-4.1-mini')
    def test_parse_and_unknown_evidence(self):
        pred=self.prediction()
        raw={'choices':[{'finish_reason':'stop','message':{'content':json.dumps(pred)}}]}
        self.assertEqual(run.parse_response(raw,self.case),pred)
        pred['evidence_references']=['INVENTED']
        with self.assertRaises(ValueError): run.validate(pred,self.case)
    def test_incomplete_and_refusal(self):
        with self.assertRaises(ValueError): run.parse_response({'choices':[{'finish_reason':'length'}]},self.case)
        with self.assertRaises(ValueError): run.parse_response({'choices':[{'finish_reason':'stop','message':{'refusal':'Refused'}}]},self.case)
    def test_failure_abstention_false_positive_metrics(self):
        records=[{'transaction_id':'DEV-01','result':{'conclusion':run.LABELS[1],'difference_cny':10000}},
                 {'transaction_id':'DEV-03','result':{'conclusion':run.LABELS[3],'difference_cny':None}},
                 {'transaction_id':'DEV-12','result':{'conclusion':run.LABELS[3],'difference_cny':None}}]
        m=run.evaluate(records,self.answers,['DEV-01','DEV-03','DEV-04','DEV-12'])
        self.assertEqual(m['false_flags_on_normal_cases'],1)
        self.assertEqual(m['planted_errors'],2)
        self.assertEqual(m['errors_flagged'],0)
        self.assertEqual(m['technical_failures_or_not_run'],1)
        self.assertEqual(m['missing_evidence_cases_correct'],1)
    def test_cost_accounts_for_cache_and_unknown(self):
        self.assertAlmostEqual(run.cost({'cost':.00123,'prompt_tokens':1000}),.00123)
        self.assertEqual(run.cost({'cost':0}),0)
        self.assertIsNone(run.cost({'prompt_tokens':1000,'completion_tokens':100}))
        self.assertIsNone(run.cost(None))
    def test_all_expected_labels_score_without_network(self):
        records=[{'transaction_id':a['transaction_id'],'result':a} for a in self.answers]
        m=run.evaluate(records,self.answers,[a['transaction_id'] for a in self.answers])
        self.assertEqual(m['exact_label_correct'],20)
        self.assertEqual(m['errors_flagged'],6)
        self.assertEqual(m['abstentions'],2)

if __name__=='__main__': unittest.main()
