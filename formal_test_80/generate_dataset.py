"""Deterministic held-out synthetic case construction. Evaluator-only source."""
import json,random,hashlib
from pathlib import Path
from datetime import date,timedelta
ROOT=Path(__file__).resolve().parent
SEED=620180
TEMPLATES={
'D':[
 'Control passes on handover to the carrier appointed by the buyer. The buyer can redirect the shipment thereafter; the seller retains no substantive control.',
 'Control transfers when the goods are collected by the customer at the factory. The collection is recorded in the actual dispatch field. The customer can direct their use immediately.',
 'Control passes when the goods are handed to the buyer-authorised carrier at the loading point. Subsequent transport does not delay this transfer.'
],
'R':[
 'Control passes on customer receipt at the agreed warehouse, evidenced by signed delivery. No separate acceptance test is required.',
 'Control transfers when the customer receives the shipment and signs the warehouse receipt. Dispatch alone does not complete performance.',
 'Transfer of control occurs on signed delivery at the buyer warehouse. The seller remains responsible during transit. No additional acceptance procedure applies.'
],
'A':[
 'Control passes only after substantive customer acceptance following inspection. Physical receipt alone is insufficient.',
 'Control transfers only upon customer inspection approval and acceptance. The inspection verifies contractual performance and is a substantive condition.',
 'The customer does not obtain control until substantive inspection sign-off and acceptance. Earlier delivery to its premises is insufficient.'
]}
LABEL={'N':'No cut-off exception identified','P':'Premature recognition','L':'Delayed or omitted recognition','E':'Additional evidence required'}
rng=random.Random(SEED)
# Deliberately specified proportions, not a claim about real-world prevalence.
specs=[]
for k in 'DRA':
 for label,count in [('N',20),('P',2),('L',2),('E',3 if k!='A' else 2)]:
  specs.extend((k,label,j) for j in range(count))
rng.shuffle(specs)
cases=[];answers=[]
cut=date(2025,12,31)
for i,(kind,label,j) in enumerate(specs,1):
 ident=f'TEST-{i:03d}'
 before=(label=='L' or (label=='N' and j%2==0))
 event=cut-timedelta(days=rng.randint(0,10)) if before else cut+timedelta(days=rng.randint(1,9))
 # Include the boundary day in each contract family without changing labels.
 if label=='N' and j==0:event=cut
 if kind=='D':dispatch=event;receipt=event+timedelta(days=rng.randint(1,4));accept=None
 elif kind=='R':receipt=event;dispatch=receipt-timedelta(days=rng.randint(1,4));accept=None
 else:accept=event;receipt=accept-timedelta(days=rng.randint(1,3));dispatch=receipt-timedelta(days=rng.randint(1,3))
 if label=='P':booked=cut-timedelta(days=rng.randint(0,4))
 elif label=='L':booked=cut+timedelta(days=rng.randint(1,7))
 else:booked=event
 if label=='E':
  dispatch=cut-timedelta(days=4);receipt=cut-timedelta(days=2) if kind=='A' else None;accept=None;booked=cut
  if kind=='D':dispatch=None
  event=None
 invoice=cut+timedelta(days=rng.choice([-8,-3,-1,0,2,5,10]))
 qty=rng.choice([25,40,60,80,120,150,200]);price=rng.choice([35,60,85,125,160,240]);amount=qty*price
 refs={k:f'{k.upper()}-{i:03d}' for k in ['contract','ledger','invoice','delivery']}
 iso=lambda d:d.isoformat() if d else None
 term=TEMPLATES[kind][j%3]+' Payment becomes unconditional at that event and is due '+str(rng.choice([30,45,60]))+' days later. Early invoicing is administrative and creates no earlier right to payment.'
 c={'transaction_id':ident,
 'contract':{'document_id':refs['contract'],'customer':f'Industrial Buyer {i:03d}','goods':rng.choice(['Steel fasteners','Pump housings','Bearing sleeves','Aluminium brackets']),'quantity':qty,'unit_price_cny':price,'total_price_cny':amount,'terms':term},
 'ledger':{'document_id':refs['ledger'],'transaction_id':ident,'accounting_date':iso(booked),'accounting_period':iso(booked)[:7],'entry':{'debit_account':'Accounts receivable','debit_cny':amount,'credit_account':'Sales revenue','credit_cny':amount}},
 'invoice':{'document_id':refs['invoice'],'transaction_id':ident,'invoice_date':iso(invoice),'quantity':qty,'amount_cny':amount},
 'delivery':{'document_id':refs['delivery'],'transaction_id':ident,'batch_id':f'LOT-{i:03d}','actual_dispatch_date':iso(dispatch),'actual_customer_receipt_date':iso(receipt),'actual_customer_acceptance_date':iso(accept),'dispatched_quantity':qty if dispatch else None,'received_quantity':qty if receipt else None,'accepted_quantity':qty if accept else None,'carrier_authorised_by_customer':True if kind=='D' else None,'note':'All populated event dates and quantities are verified synthetic facts. Required null event fields are unknown, not evidence of non-performance.'}}
 cases.append(c)
 answers.append({'transaction_id':ident,'contract_category':{'D':'Dispatch-based','R':'Delivery-based','A':'Acceptance-based'}[kind],'conclusion':LABEL[label],'qualifying_event_date':iso(event),'eligible_quantity_by_cutoff':None if event is None else qty if event<=cut else 0,'recorded_quantity_in_2025':qty if booked<=cut else 0,'difference_cny':None if label=='E' else amount if label in ['P','L'] else 0,'reason':f'Apply the {kind} contractual event. Qualifying date: {iso(event) or "unknown"}; accounting date: {iso(booked)}. '+('Evidence is insufficient to locate recognition before or after the cut-off.' if label=='E' else f'The expected annual cut-off classification is {LABEL[label]}.'),'source_references':list(refs.values())})
context=json.loads((ROOT.parent/'development_examples_20/inputs.json').read_text())
context={k:v for k,v in context.items() if k not in ['cases','dataset']}
context['dataset']='Formal synthetic test set v1.0, separate from development examples'
context['records_available_through']='2026-01-20'
context['assumptions']=[x.replace('10 January 2026','20 January 2026') for x in context['assumptions'] if 'development cases' not in x]
context['assumptions'].append('A populated customer receipt date includes signed receipt. A populated dispatch date under a collection contract represents completed buyer collection. No partial deliveries are present.')
context['cases']=cases
for name,obj in [('inputs.json',context),('answer_key.json',{'purpose':'Evaluator only; never pass to a predictor.','answers':answers})]:
 (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
lines=['# Formal Test Inputs v1.0','','All records are synthetic; reporting cut-off: 31 December 2025. Each case contains the four source record types. No expected answers are included.','','## Shared assumptions','']+['- '+x for x in context['assumptions']]
for c in cases:
 lines+=['',f"## {c['transaction_id']}",'','```json',json.dumps(c,ensure_ascii=False,indent=2),'```']
(ROOT/'examples.md').write_text('\n'.join(lines)+'\n')
lines=['# Evaluator Answer Key','','Never provide this file to the model or baseline.','','| Case | Contract | Expected conclusion | Difference CNY |','|---|---|---|---:|']
for a in answers:lines.append(f"| {a['transaction_id']} | {a['contract_category']} | {a['conclusion']} | {a['difference_cny'] if a['difference_cny'] is not None else 'null'} |")
for a in answers:lines+=['',f"## {a['transaction_id']}",'',a['reason']]
(ROOT/'answer_key.md').write_text('\n'.join(lines)+'\n')
from collections import Counter
assert len(cases)==len({c['transaction_id'] for c in cases})==80
assert Counter(a['conclusion'] for a in answers)==Counter({LABEL['N']:60,LABEL['P']:6,LABEL['L']:6,LABEL['E']:8})
# Independent arithmetic/date checks against labels specified before prediction.
for c,a in zip(cases,answers):
 q=c['contract']['quantity'];p=c['contract']['unit_price_cny']; assert q*p==c['invoice']['amount_cny']==c['ledger']['entry']['debit_cny']
 e=a['qualifying_event_date'];b=c['ledger']['accounting_date']
 expected='E' if e is None else 'P' if e>'2025-12-31'>=b else 'L' if b>'2025-12-31'>=e else 'N'
 assert a['conclusion']==LABEL[expected]
 dates=[c['delivery'][k] for k in ['actual_dispatch_date','actual_customer_receipt_date','actual_customer_acceptance_date'] if c['delivery'][k]]
 assert dates==sorted(dates)
freeze={'seed':SEED,'cases':80,'normal':60,'premature':6,'delayed':6,'insufficient_evidence':8,'status':'Frozen before predictor evaluation; do not tune on this set.','provenance':'Separately generated by the same assistant as the development set; not independently authored or externally validated.','sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['inputs.json','answer_key.json','generate_dataset.py']}}
for name,path in [('baseline.py',ROOT.parent/'local_tester/baseline.py'),('prompt',ROOT.parent/'accounts_receivable_cutoff_prompt_v1.1.md')]:freeze['sha256'][name]=hashlib.sha256(path.read_bytes()).hexdigest()
(ROOT/'freeze_manifest.json').write_text(json.dumps(freeze,indent=2)+'\n')
print('Generated and validated 80 cases. Freeze manifest written before evaluation.')
