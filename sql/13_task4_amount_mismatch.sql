-- Task 4: Amount mismatches
-- Split into: (a) explainable by fees (net-of-fee) vs (b) true mismatch.

-- 4a) Find payment vs settlement mismatches
SELECT
  p.payment_id,
  p.payment_type,
  p.amount AS expected_amount,
  s.amount AS settled_amount,
  (p.amount - s.amount) AS diff,
  s.settlement_note
FROM payments p
JOIN bank_settlements s
  ON s.external_ref = p.payment_id
WHERE p.status = 'completed'
  AND p.amount <> s.amount
ORDER BY ABS(p.amount - s.amount) DESC, p.payment_id;

-- 4b) Check whether mismatches are explained by fees
SELECT
  p.payment_id,
  p.payment_type,
  p.amount AS expected_gross,
  COALESCE(f.fee_amount, 0) AS fee_amount,
  (p.amount - COALESCE(f.fee_amount, 0)) AS expected_net,
  s.amount AS settled_amount,
  ((p.amount - COALESCE(f.fee_amount, 0)) - s.amount) AS net_diff,
  s.settlement_note
FROM payments p
JOIN bank_settlements s
  ON s.external_ref = p.payment_id
LEFT JOIN fees f
  ON f.payment_id = p.payment_id
WHERE p.status = 'completed'
  AND p.amount <> s.amount
ORDER BY p.payment_id;
