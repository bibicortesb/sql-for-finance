# 01_import_notes.md

This lab is designed for restricted MySQL/phpMyAdmin course environments where:
- `LOAD DATA LOCAL INFILE` is disabled/forbidden
- you must import via the phpMyAdmin **Import** UI
- header handling can be inconsistent

## Recommended load order
1. `payments`
2. `ledger_entries`
3. `fees`
4. `reversals`
5. `bank_settlements`

If you load out of order, temporarily disable foreign key checks during import.

## phpMyAdmin Import (CSV)
1. Click the target table (e.g., `payments`)
2. Go to **Import**
3. Choose the CSV file
4. Format: **CSV**
5. Keep delimiter settings:
   - Columns separated by: `,`
   - Columns enclosed by: `"` (or leave default)
   - Lines terminated by: `auto`

If your environment does **not** skip CSV headers, use the `*_no_header.csv` files in `/data`.

## Sanity checks
```sql
SELECT COUNT(*) FROM payments;
SELECT COUNT(*) FROM bank_settlements;
SELECT * FROM payments LIMIT 3;
```
