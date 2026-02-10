# quick_inserts.md

If your lab does not allow CSV import reliably, you can use multi-row INSERT statements.

Example (payments):

```sql
INSERT INTO payments (payment_id, user_id, payment_type, amount, currency, created_at, status) VALUES
('P0001','U004','DIRECT_DEBIT',999,'MXN','2026-02-04 08:11:00','completed'),
('P0002','U015','TEF',1800,'MXN','2026-02-04 08:47:00','completed');
```

Tip: keep batches to ~200–500 rows per INSERT for web-based SQL consoles.
