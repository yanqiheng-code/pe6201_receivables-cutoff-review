"""Generate simple, deterministic synthetic development cases; no model calls."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTRACTS = {
    'D': 'Control transfers when the goods are physically handed to the carrier authorised by the customer. The customer can direct the goods from that point, and the seller retains no substantive control. Payment is due 30 days after handover.',
    'R': 'Control transfers when the goods reach the customer warehouse and the customer signs for receipt. No further acceptance is required. Payment is due 30 days after receipt.',
    'A': 'Control transfers only after the customer completes a substantive inspection and accepts the goods. Delivery alone does not complete performance. Payment is due 30 days after acceptance.',
}
# ID, contract, dispatch, receipt, acceptance, accounting date, invoice date, expected result
ROWS = [
 ('01','D','2025-12-28','2025-12-30',None,'2025-12-28','2025-12-28','N'),
 ('02','D','2025-12-31','2026-01-02',None,'2025-12-31','2025-12-31','N'),
 ('03','D','2026-01-02','2026-01-04',None,'2025-12-30','2025-12-30','P'),
 ('04','D','2025-12-30','2026-01-02',None,'2026-01-02','2026-01-02','L'),
 ('05','D','2026-01-03','2026-01-05',None,'2026-01-03','2025-12-29','N'),
 ('06','D','2025-12-29','2025-12-31',None,'2025-12-29','2026-01-03','N'),
 ('07','R','2025-12-27','2025-12-29',None,'2025-12-29','2025-12-29','N'),
 ('08','R','2025-12-29','2026-01-02',None,'2025-12-29','2025-12-29','P'),
 ('09','R','2025-12-28','2025-12-30',None,'2026-01-03','2026-01-03','L'),
 ('10','R','2025-12-29','2025-12-31',None,'2025-12-31','2026-01-02','N'),
 ('11','R','2026-01-02','2026-01-04',None,'2026-01-04','2025-12-30','N'),
 ('12','R','2025-12-30',None,None,'2025-12-31','2025-12-31','E'),
 ('13','R','2025-12-26','2025-12-28',None,'2025-12-28','2025-12-26','N'),
 ('14','A','2025-12-24','2025-12-26','2025-12-29','2025-12-29','2025-12-29','N'),
 ('15','A','2025-12-27','2025-12-29','2026-01-03','2025-12-29','2025-12-29','P'),
 ('16','A','2025-12-24','2025-12-27','2025-12-30','2026-01-03','2026-01-03','L'),
 ('17','A','2025-12-27','2025-12-29','2025-12-31','2025-12-31','2025-12-28','N'),
 ('18','A','2025-12-29','2025-12-31','2026-01-04','2026-01-04','2025-12-31','N'),
 ('19','A','2025-12-27','2025-12-29',None,'2025-12-31','2025-12-31','E'),
 ('20','A','2025-12-23','2025-12-26','2025-12-28','2025-12-28','2026-01-02','N'),
]
LABELS = {'N':'No cut-off exception identified','P':'Premature recognition','L':'Delayed or omitted recognition','E':'Additional evidence required'}
EVENTS = {'D':'handover to the customer-authorised carrier','R':'customer receipt at the agreed warehouse','A':'substantive customer acceptance'}
cases, answers = [], []
for number, kind, dispatch, receipt, acceptance, booked, invoiced, expected in ROWS:
    ident = f'DEV-{number}'
    amount = 10000
    contract_ref, ledger_ref, invoice_ref, delivery_ref = [f'{prefix}-{number}' for prefix in ['CON','LED','INV','DEL']]
    event_date = {'D':dispatch,'R':receipt,'A':acceptance}[kind]
    delivery = {
        'document_id':delivery_ref,'transaction_id':ident,'batch_id':f'BATCH-{number}',
        'actual_dispatch_date':dispatch,'actual_customer_receipt_date':receipt,
        'actual_customer_acceptance_date':acceptance,
        'dispatched_quantity':100,
        'received_quantity':100 if receipt else None,
        'accepted_quantity':100 if acceptance else None,
        'carrier_authorised_by_customer':True if kind == 'D' else None,
        'note': 'Dates describe actual events. A null required date means the available records do not establish whether or when the event occurred.'
    }
    case = {
        'transaction_id':ident,
        'contract':{'document_id':contract_ref,'customer':f'Customer {number}', 'goods':'Standard steel brackets','quantity':100,'unit_price_cny':100,'total_price_cny':amount,'terms':CONTRACTS[kind]},
        'ledger':{'document_id':ledger_ref,'transaction_id':ident,'accounting_date':booked,'accounting_period':booked[:7],'entry':{'debit_account':'Accounts receivable','debit_cny':amount,'credit_account':'Sales revenue','credit_cny':amount}},
        'invoice':{'document_id':invoice_ref,'transaction_id':ident,'invoice_date':invoiced,'quantity':100,'amount_cny':amount},
        'delivery':delivery,
    }
    cases.append(case)
    if expected == 'E':
        reason = f'The contract requires {EVENTS[kind]}, but the corresponding actual event date is unknown. The December entry cannot be confirmed or rejected from the supplied evidence.'
        request = f'Provide the actual date and supporting record of {EVENTS[kind]}. Establish whether it occurred on or before 31 December 2025. A qualifying event after that date would support premature recognition; an event within 2025 would support current-period recognition.'
    else:
        reason = f'The qualifying event is {EVENTS[kind]} on {event_date}; the ledger records the sale on {booked}. '
        reason += {'N':'Both fall in the same annual reporting period. Invoice timing does not change the conclusion.', 'P':'The qualifying event is after the 2025 cut-off, but the sale was recorded in 2025.', 'L':'The qualifying event is in 2025, but the sale was recorded in 2026.'}[expected]
        request = None
    answers.append({
        'transaction_id':ident,'contract_category':{'D':'Dispatch-based','R':'Delivery-based','A':'Acceptance-based'}[kind],
        'conclusion':LABELS[expected], 'qualifying_event':EVENTS[kind], 'qualifying_event_date':event_date,
        'recognisable_by_cutoff':None if event_date is None else event_date <= '2025-12-31',
        'eligible_quantity_by_cutoff':None if event_date is None else (100 if event_date <= '2025-12-31' else 0),
        'recorded_quantity_in_2025':100 if booked.startswith('2025') else 0,
        'difference_cny':None if expected == 'E' else (amount if expected in ('P','L') else 0),
        'direction':{'N':'None','P':'2025 revenue and receivables overstated','L':'2025 revenue and receivables understated','E':'Undetermined'}[expected],
        'reason':reason,'additional_evidence_requested':request,'evidence_references':[contract_ref,delivery_ref,ledger_ref,invoice_ref],
    })

context = {
    'dataset':'Simple synthetic development examples v1.0',
    'reporting_period_start':'2025-01-01','cutoff_date':'2025-12-31',
    'records_available_through':'2026-01-10','currency':'CNY',
    'assumptions':[
        'All contracts are valid, approved and unchanged. Collection was probable at contract inception.',
        'Each case is one separate contract, invoice, delivery batch and accounting entry.',
        'All goods have a fixed price. All amounts exclude tax. There are no discounts, returns, reversals, financing components or service obligations.',
        'There are no opening balances or other entries for these transactions. No payments have been received through 10 January 2026.',
        'Ledger records are complete for these transactions through 10 January 2026. Delivery table values supplied are verified synthetic facts; null required fields are missing evidence, not proof of non-performance.',
        'A null acceptance field in a contract without substantive acceptance is not a missing required event.',
        'Payment rights become unconditional at the qualifying contractual event.',
        'Invoice issuance before the qualifying event is administrative only; it does not create an earlier unconditional payment right.',
        'Only annual cut-off is tested. These are development cases and must not be reported as an unseen final evaluation set.'
    ],'cases':cases,
}
ROOT.joinpath('inputs.json').write_text(json.dumps(context,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
ROOT.joinpath('answer_key.json').write_text(json.dumps({'purpose':'Evaluator only. Do not include in model input.','answers':answers},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# Twenty Simple Development Examples','', 'Reporting period: 1 January–31 December 2025. Cut-off: 31 December 2025. Records available through 10 January 2026.','', 'All examples are fictional. Each sale is 100 standard steel brackets at CNY 100 each, totalling CNY 10,000 excluding tax. No payments have been received.','', '## Dataset assumptions','']
lines += ['- '+a for a in context['assumptions']]
for case in cases:
    c,l,i,d = [case[k] for k in ['contract','ledger','invoice','delivery']]
    lines += ['',f"## {case['transaction_id']}",'',f"**Contract {c['document_id']} — {c['customer']}**",'',c['terms'],'',f"**Ledger {l['document_id']}**: {l['accounting_date']}; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.",'',f"**Invoice {i['document_id']}**: {i['invoice_date']}; 100 units; CNY 10,000.",'',f"**Delivery record {d['document_id']}**:",'',f"- Actual dispatch: {d['actual_dispatch_date']} (100 units).",f"- Actual customer receipt: {d['actual_customer_receipt_date'] or 'Unknown'}" + (' (100 units).' if d['received_quantity'] else '.'),f"- Substantive acceptance: {d['actual_customer_acceptance_date'] or ('Unknown' if 'substantive inspection' in c['terms'] else 'Not required by contract')}" + (' (100 units).' if d['accepted_quantity'] else '.')]
ROOT.joinpath('examples.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
lines=['# Answer Key — Evaluator Only','','Do not pass this file to the model. These are expected answers, not measured model results.','','| Case | Contract type | Expected conclusion | Difference (CNY) |','|---|---|---|---:|']
for a in answers:
    lines.append(f"| {a['transaction_id']} | {a['contract_category']} | {a['conclusion']} | {a['difference_cny'] if a['difference_cny'] is not None else 'Undetermined'} |")
for a in answers:
    lines += ['',f"## {a['transaction_id']}",'',a['reason'], '',f"Evidence: {', '.join(a['evidence_references'])}."]
    if a['additional_evidence_requested']: lines += ['',a['additional_evidence_requested']]
ROOT.joinpath('answer_key.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
ROOT.joinpath('README.md').write_text('''# Development Dataset v1.0

Twenty simple synthetic cases for the Accounts Receivable Cut-off Testing Rules v1.1.

## Files

- `examples.md`: human-readable inputs, without expected conclusions.
- `inputs.json`: structured model inputs, including shared context and assumptions.
- `answer_key.md`: readable expected conclusions and explanations; evaluator only.
- `answer_key.json`: structured expected answers; evaluator only.
- `generate_examples.py`: deterministic generator, including scenario definitions and labels; evaluator only.

## Composition

12 cases with no cut-off exception, 3 premature recognitions, 3 delayed recognitions, and 2 cases requiring additional evidence. Contract categories cover carrier handover, customer receipt and substantive acceptance.

Every transaction is CNY 10,000 excluding tax, with one full batch. Partial deliveries and missing ledger entries are intentionally deferred to later versions. Missing receipt or acceptance dates are unknown facts, not known failures to deliver or accept.

## Use

Provide the system prompt and `inputs.json` to the model, or use the shared assumptions and selected cases from `examples.md`. Do not expose the answer keys or generator to the model being evaluated. These are development examples, not an unseen final test set. No model evaluation has been run.

The four source types are represented as labelled synthetic records, not separate legal contracts or invoice images. No signature, authenticity or OCR testing is included.

## Regeneration

Run `python3 generate_examples.py` in this directory. The script reproduces the same examples and validates basic integrity and intended labels.
''',encoding='utf-8')

assert len(cases)==20 and len({c['transaction_id'] for c in cases})==20
assert Counter(a['conclusion'] for a in answers)==Counter({LABELS['N']:12,LABELS['P']:3,LABELS['L']:3,LABELS['E']:2})
for c,a in zip(cases,answers):
    assert c['contract']['quantity']*c['contract']['unit_price_cny']==c['invoice']['amount_cny']==c['ledger']['entry']['debit_cny']==10000
    event=a['qualifying_event_date']; booked=c['ledger']['accounting_date']
    computed='E' if event is None else ('P' if event>'2025-12-31' and booked<='2025-12-31' else 'L' if event<='2025-12-31' and booked>'2025-12-31' else 'N')
    assert a['conclusion']==LABELS[computed]
assert 'conclusion' not in context['cases'][0]
print('Generated and validated 20 cases: 12 no exception, 3 premature, 3 delayed, 2 requiring evidence.')
