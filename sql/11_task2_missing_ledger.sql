-- Task 2: Internal booking gaps
-- Completed payments that have NO ledger entry.

SELECT
  p.payment_id,
  p.payment_type,
  p.amount,
  p.currency,
  p.created_at
FROM payments p
LEFT JOIN ledger_entries l
  ON l.payment_id = p.payment_id
WHERE p.status = 'completed'
  AND l.payment_id IS NULL
ORDER BY p.created_at;
