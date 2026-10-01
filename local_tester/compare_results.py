"""Run in VS Code after formal AI and baseline runs. No API calls."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    found={}
    for p in sorted((ROOT/'runs').glob('*'),reverse=True):
        if not (p/'manifest.json').exists() or not (p/'evaluation.json').exists():continue
        m=json.loads((p/'manifest.json').read_text())
        if m.get('dataset')!='formal_test_80' or len(m['selected_ids'])!=80:continue
        mode=m['mode']
        if mode in ('live','baseline') and mode not in found:
            found[mode]=(p,m,json.loads((p/'evaluation.json').read_text()))
    if set(found)!={'live','baseline'}:
        print('A full formal-test AI run and baseline run are required. No comparison generated.');return
    a,b=found['live'],found['baseline']
    if a[1]['inputs_sha256']!=b[1]['inputs_sha256'] or a[1]['selected_ids']!=b[1]['selected_ids']:
        raise SystemExit('Input versions or selected cases differ; comparison refused.')
    lines=['# Formal Test Comparison','','Latest full-selection runs; examine any technical failures. Synthetic same-author test data with three contract families; not real-world audit validation.','','| Metric | Non-AI baseline | AI |','|---|---:|---:|']
    for title,key in [('Valid predictions','valid_predictions'),('Correct labels / 80','exact_label_correct'),('Correct amount fields / 80','amount_correct'),('Errors flagged / 12','errors_flagged'),('False flags among 60 normal cases','false_flags_on_normal_cases'),('Abstentions','abstentions'),('Correct missing-evidence decisions / 8','missing_evidence_cases_correct'),('Technical failures or not run','technical_failures_or_not_run'),('Reported API cost USD','known_usage_reported_cost_usd')]:
        lines.append(f'| {title} | {b[2][key]} | {a[2][key]} |')
    lines+=['',f'Baseline run: {b[0].name}',f'AI run: {a[0].name}','','Cost totals exclude any unknown-cost requests. Model explanation quality and human review time are not assessed by these automatic metrics. Do not select a better-scoring earlier run without disclosing the selection.']
    out=a[0]/'comparison.md';out.write_text('\n'.join(lines)+'\n');print(out)
if __name__=='__main__':main()
