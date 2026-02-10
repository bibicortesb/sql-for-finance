# Reconciliation flow (conceptual)

Customer action (**payments**)
  → Internal booking (**ledger_entries**)
  → External confirmation (**bank_settlements**)
  → Adjustments (**fees**, **reversals**)

Reconciliation compares expected vs actual across these layers:
- completeness (missing records)
- accuracy (amount/currency mismatches)
- duplicates
- timing/aging
