import copy,json,unittest
from unittest.mock import patch
from pathlib import Path
from baseline import predict
import run

class BaselineTests(unittest.TestCase):
 def setUp(self):
  self.data=json.loads((run.PROJECT/'development_examples_20/inputs.json').read_text())
  self.context={k:v for k,v in self.data.items() if k!='cases'}
 def test_development_without_answer_access(self):
  with patch.object(Path,'read_text',side_effect=AssertionError('Predictor must not read answers')):
   results=[predict(self.context,c) for c in self.data['cases']]
  self.assertEqual(results[2]['conclusion'],'Premature recognition')
  self.assertEqual(results[11]['difference_cny'],None)
  self.assertEqual(results[1]['difference_cny'],0)
 def test_ambiguous_terms_abstain(self):
  c=copy.deepcopy(self.data['cases'][0]);c['contract']['terms']='Terms are missing.'
  self.assertEqual(predict(self.context,c)['conclusion'],'Additional evidence required')
 def test_partial_field_not_inferred(self):
  c=copy.deepcopy(self.data['cases'][0]);c['delivery']['actual_dispatch_date']=None
  self.assertIsNone(predict(self.context,c)['difference_cny'])
 def test_invoice_is_not_recognition_trigger(self):
  c=copy.deepcopy(self.data['cases'][4]);c['invoice']['invoice_date']='2025-01-01'
  self.assertEqual(predict(self.context,c)['conclusion'],'No cut-off exception identified')

if __name__=='__main__':unittest.main()
