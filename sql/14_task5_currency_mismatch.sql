-- Task 5: Currency mismatches (high severity)
-- Expected currency differs from the settlement currency.

SELECT
  p.payment_id,
  p.payment_type,
  p.currency AS expected_currency,
  s.currency AS settled_currency,
  p.amount AS expected_amount,
  s.amount AS settled_amount,
  p.created_at,
  s.settled_at
FROM payments p
JOIN bank_settlements s
  ON s.external_ref = p.payment_id
WHERE p.status = 'completed'
  AND p.currency <> s.currency
ORDER BY p.payment_id;
