"""Frozen transparent keyword/date baseline. No answer-key access or model calls."""
import re
from datetime import date


def predict(context, case):
    text=case['contract']['terms'].lower()
    # Positive clauses only: avoid matching a negated alternative elsewhere.
    acceptance=bool(re.search(r'(?:only (?:after|upon)|only when|requires|until)[^.]{0,100}(?:accept|inspection approval|inspection sign-off)',text))
    dispatch=bool(re.search(r'(?:transfers|passes|occurs)[^.]{0,100}(?:handover|handed|collected|collection|carrier)',text))
    receipt=bool(re.search(r'(?:transfers|passes|occurs)[^.]{0,100}(?:receipt|received|signed delivery|receives)',text))
    choices=[('actual_customer_acceptance_date',acceptance),('actual_dispatch_date',dispatch),('actual_customer_receipt_date',receipt)]
    matched=[k for k,v in choices if v]
    field=matched[0] if len(matched)==1 else None
    d=case['delivery'].get(field) if field else None
    booked=case['ledger']['accounting_date']; cutoff=context['cutoff_date']; start=context['reporting_period_start']
    q=case['contract']['quantity']; price=case['contract']['unit_price_cny']
    recorded=q if start<=booked<=cutoff else 0
    eligible=None
    label='Additional evidence required'; amount=None
    if d:
        date.fromisoformat(d)
        if d < start:
            label='Outside prototype scope — human review required'
        else:
            eligible=q if d<=cutoff else 0
            delta=recorded-eligible
            label='Premature recognition' if delta>0 else 'Delayed or omitted recognition' if delta<0 else 'No cut-off exception identified'
            amount=abs(delta)*price
    return {'transaction_id':case['transaction_id'],'recognition_condition':f'Fixed keyword rule selected {field or "no unique event"}.',
            'qualifying_event_date':d,'recorded_accounting_date':booked,'eligible_quantity_by_cutoff':eligible,'recorded_quantity_in_2025':recorded,
            'conclusion':label,'difference_cny':amount,'explanation':'Contract keywords select one event; dates are compared with the cut-off and quantity differences are multiplied by the fixed price. No learned model is used.',
            'evidence_references':[case[k]['document_id'] for k in ['contract','ledger','delivery']],
            'additional_evidence_requested':[] if d else ['Provide an unambiguous recognition condition and its actual event date.']}
