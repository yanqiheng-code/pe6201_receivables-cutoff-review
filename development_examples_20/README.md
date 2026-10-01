# Development Dataset v1.0

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
