-- Task 1: Completeness
-- Completed payments that have NO corresponding settlement record.

SELECT
  p.payment_id,
  p.payment_type,
  p.amount,
  p.currency,
  p.created_at
FROM payments p
LEFT JOIN bank_settlements s
  ON s.external_ref = p.payment_id
WHERE p.status = 'completed'
  AND s.external_ref IS NULL
ORDER BY p.created_at;
