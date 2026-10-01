# Twenty Simple Development Examples

Reporting period: 1 January–31 December 2025. Cut-off: 31 December 2025. Records available through 10 January 2026.

All examples are fictional. Each sale is 100 standard steel brackets at CNY 100 each, totalling CNY 10,000 excluding tax. No payments have been received.

## Dataset assumptions

- All contracts are valid, approved and unchanged. Collection was probable at contract inception.
- Each case is one separate contract, invoice, delivery batch and accounting entry.
- All goods have a fixed price. All amounts exclude tax. There are no discounts, returns, reversals, financing components or service obligations.
- There are no opening balances or other entries for these transactions. No payments have been received through 10 January 2026.
- Ledger records are complete for these transactions through 10 January 2026. Delivery table values supplied are verified synthetic facts; null required fields are missing evidence, not proof of non-performance.
- A null acceptance field in a contract without substantive acceptance is not a missing required event.
- Payment rights become unconditional at the qualifying contractual event.
- Invoice issuance before the qualifying event is administrative only; it does not create an earlier unconditional payment right.
- Only annual cut-off is tested. These are development cases and must not be reported as an unseen final evaluation set.

## DEV-01

**Contract CON-01 — Customer 01**

Control transfers when the goods are physically handed to the carrier authorised by the customer. The customer can direct the goods from that point, and the seller retains no substantive control. Payment is due 30 days after handover.

**Ledger LED-01**: 2025-12-28; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-01**: 2025-12-28; 100 units; CNY 10,000.

**Delivery record DEL-01**:

- Actual dispatch: 2025-12-28 (100 units).
- Actual customer receipt: 2025-12-30 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-02

**Contract CON-02 — Customer 02**

Control transfers when the goods are physically handed to the carrier authorised by the customer. The customer can direct the goods from that point, and the seller retains no substantive control. Payment is due 30 days after handover.

**Ledger LED-02**: 2025-12-31; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-02**: 2025-12-31; 100 units; CNY 10,000.

**Delivery record DEL-02**:

- Actual dispatch: 2025-12-31 (100 units).
- Actual customer receipt: 2026-01-02 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-03

**Contract CON-03 — Customer 03**

Control transfers when the goods are physically handed to the carrier authorised by the customer. The customer can direct the goods from that point, and the seller retains no substantive control. Payment is due 30 days after handover.

**Ledger LED-03**: 2025-12-30; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-03**: 2025-12-30; 100 units; CNY 10,000.

**Delivery record DEL-03**:

- Actual dispatch: 2026-01-02 (100 units).
- Actual customer receipt: 2026-01-04 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-04

**Contract CON-04 — Customer 04**

Control transfers when the goods are physically handed to the carrier authorised by the customer. The customer can direct the goods from that point, and the seller retains no substantive control. Payment is due 30 days after handover.

**Ledger LED-04**: 2026-01-02; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-04**: 2026-01-02; 100 units; CNY 10,000.

**Delivery record DEL-04**:

- Actual dispatch: 2025-12-30 (100 units).
- Actual customer receipt: 2026-01-02 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-05

**Contract CON-05 — Customer 05**

Control transfers when the goods are physically handed to the carrier authorised by the customer. The customer can direct the goods from that point, and the seller retains no substantive control. Payment is due 30 days after handover.

**Ledger LED-05**: 2026-01-03; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-05**: 2025-12-29; 100 units; CNY 10,000.

**Delivery record DEL-05**:

- Actual dispatch: 2026-01-03 (100 units).
- Actual customer receipt: 2026-01-05 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-06

**Contract CON-06 — Customer 06**

Control transfers when the goods are physically handed to the carrier authorised by the customer. The customer can direct the goods from that point, and the seller retains no substantive control. Payment is due 30 days after handover.

**Ledger LED-06**: 2025-12-29; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-06**: 2026-01-03; 100 units; CNY 10,000.

**Delivery record DEL-06**:

- Actual dispatch: 2025-12-29 (100 units).
- Actual customer receipt: 2025-12-31 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-07

**Contract CON-07 — Customer 07**

Control transfers when the goods reach the customer warehouse and the customer signs for receipt. No further acceptance is required. Payment is due 30 days after receipt.

**Ledger LED-07**: 2025-12-29; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-07**: 2025-12-29; 100 units; CNY 10,000.

**Delivery record DEL-07**:

- Actual dispatch: 2025-12-27 (100 units).
- Actual customer receipt: 2025-12-29 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-08

**Contract CON-08 — Customer 08**

Control transfers when the goods reach the customer warehouse and the customer signs for receipt. No further acceptance is required. Payment is due 30 days after receipt.

**Ledger LED-08**: 2025-12-29; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-08**: 2025-12-29; 100 units; CNY 10,000.

**Delivery record DEL-08**:

- Actual dispatch: 2025-12-29 (100 units).
- Actual customer receipt: 2026-01-02 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-09

**Contract CON-09 — Customer 09**

Control transfers when the goods reach the customer warehouse and the customer signs for receipt. No further acceptance is required. Payment is due 30 days after receipt.

**Ledger LED-09**: 2026-01-03; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-09**: 2026-01-03; 100 units; CNY 10,000.

**Delivery record DEL-09**:

- Actual dispatch: 2025-12-28 (100 units).
- Actual customer receipt: 2025-12-30 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-10

**Contract CON-10 — Customer 10**

Control transfers when the goods reach the customer warehouse and the customer signs for receipt. No further acceptance is required. Payment is due 30 days after receipt.

**Ledger LED-10**: 2025-12-31; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-10**: 2026-01-02; 100 units; CNY 10,000.

**Delivery record DEL-10**:

- Actual dispatch: 2025-12-29 (100 units).
- Actual customer receipt: 2025-12-31 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-11

**Contract CON-11 — Customer 11**

Control transfers when the goods reach the customer warehouse and the customer signs for receipt. No further acceptance is required. Payment is due 30 days after receipt.

**Ledger LED-11**: 2026-01-04; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-11**: 2025-12-30; 100 units; CNY 10,000.

**Delivery record DEL-11**:

- Actual dispatch: 2026-01-02 (100 units).
- Actual customer receipt: 2026-01-04 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-12

**Contract CON-12 — Customer 12**

Control transfers when the goods reach the customer warehouse and the customer signs for receipt. No further acceptance is required. Payment is due 30 days after receipt.

**Ledger LED-12**: 2025-12-31; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-12**: 2025-12-31; 100 units; CNY 10,000.

**Delivery record DEL-12**:

- Actual dispatch: 2025-12-30 (100 units).
- Actual customer receipt: Unknown.
- Substantive acceptance: Not required by contract.

## DEV-13

**Contract CON-13 — Customer 13**

Control transfers when the goods reach the customer warehouse and the customer signs for receipt. No further acceptance is required. Payment is due 30 days after receipt.

**Ledger LED-13**: 2025-12-28; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-13**: 2025-12-26; 100 units; CNY 10,000.

**Delivery record DEL-13**:

- Actual dispatch: 2025-12-26 (100 units).
- Actual customer receipt: 2025-12-28 (100 units).
- Substantive acceptance: Not required by contract.

## DEV-14

**Contract CON-14 — Customer 14**

Control transfers only after the customer completes a substantive inspection and accepts the goods. Delivery alone does not complete performance. Payment is due 30 days after acceptance.

**Ledger LED-14**: 2025-12-29; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-14**: 2025-12-29; 100 units; CNY 10,000.

**Delivery record DEL-14**:

- Actual dispatch: 2025-12-24 (100 units).
- Actual customer receipt: 2025-12-26 (100 units).
- Substantive acceptance: 2025-12-29 (100 units).

## DEV-15

**Contract CON-15 — Customer 15**

Control transfers only after the customer completes a substantive inspection and accepts the goods. Delivery alone does not complete performance. Payment is due 30 days after acceptance.

**Ledger LED-15**: 2025-12-29; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-15**: 2025-12-29; 100 units; CNY 10,000.

**Delivery record DEL-15**:

- Actual dispatch: 2025-12-27 (100 units).
- Actual customer receipt: 2025-12-29 (100 units).
- Substantive acceptance: 2026-01-03 (100 units).

## DEV-16

**Contract CON-16 — Customer 16**

Control transfers only after the customer completes a substantive inspection and accepts the goods. Delivery alone does not complete performance. Payment is due 30 days after acceptance.

**Ledger LED-16**: 2026-01-03; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-16**: 2026-01-03; 100 units; CNY 10,000.

**Delivery record DEL-16**:

- Actual dispatch: 2025-12-24 (100 units).
- Actual customer receipt: 2025-12-27 (100 units).
- Substantive acceptance: 2025-12-30 (100 units).

## DEV-17

**Contract CON-17 — Customer 17**

Control transfers only after the customer completes a substantive inspection and accepts the goods. Delivery alone does not complete performance. Payment is due 30 days after acceptance.

**Ledger LED-17**: 2025-12-31; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-17**: 2025-12-28; 100 units; CNY 10,000.

**Delivery record DEL-17**:

- Actual dispatch: 2025-12-27 (100 units).
- Actual customer receipt: 2025-12-29 (100 units).
- Substantive acceptance: 2025-12-31 (100 units).

## DEV-18

**Contract CON-18 — Customer 18**

Control transfers only after the customer completes a substantive inspection and accepts the goods. Delivery alone does not complete performance. Payment is due 30 days after acceptance.

**Ledger LED-18**: 2026-01-04; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-18**: 2025-12-31; 100 units; CNY 10,000.

**Delivery record DEL-18**:

- Actual dispatch: 2025-12-29 (100 units).
- Actual customer receipt: 2025-12-31 (100 units).
- Substantive acceptance: 2026-01-04 (100 units).

## DEV-19

**Contract CON-19 — Customer 19**

Control transfers only after the customer completes a substantive inspection and accepts the goods. Delivery alone does not complete performance. Payment is due 30 days after acceptance.

**Ledger LED-19**: 2025-12-31; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-19**: 2025-12-31; 100 units; CNY 10,000.

**Delivery record DEL-19**:

- Actual dispatch: 2025-12-27 (100 units).
- Actual customer receipt: 2025-12-29 (100 units).
- Substantive acceptance: Unknown.

## DEV-20

**Contract CON-20 — Customer 20**

Control transfers only after the customer completes a substantive inspection and accepts the goods. Delivery alone does not complete performance. Payment is due 30 days after acceptance.

**Ledger LED-20**: 2025-12-28; debit accounts receivable CNY 10,000; credit sales revenue CNY 10,000.

**Invoice INV-20**: 2026-01-02; 100 units; CNY 10,000.

**Delivery record DEL-20**:

- Actual dispatch: 2025-12-23 (100 units).
- Actual customer receipt: 2025-12-26 (100 units).
- Substantive acceptance: 2025-12-28 (100 units).
