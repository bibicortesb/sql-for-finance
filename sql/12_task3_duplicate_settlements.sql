-- Task 3: Duplicates
-- Payments with more than one settlement record (risk: double posting / double counting).

SELECT
  external_ref AS payment_id,
  COUNT(*) AS settlement_rows,
  MIN(settled_at) AS first_settled_at,
  MAX(settled_at) AS last_settled_at
FROM bank_settlements
GROUP BY external_ref
HAVING COUNT(*) > 1
ORDER BY settlement_rows DESC, payment_id;

-- Inspect duplicates for a single payment_id (replace 'P0002')
-- SELECT * FROM bank_settlements WHERE external_ref='P0002' ORDER BY settled_at;
