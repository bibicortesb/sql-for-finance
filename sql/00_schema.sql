-- 00_schema.sql
-- Financial reconciliation lab (MySQL)
-- Tables: payments, ledger_entries, bank_settlements, fees, reversals

DROP TABLE IF EXISTS reversals;
DROP TABLE IF EXISTS fees;
DROP TABLE IF EXISTS bank_settlements;
DROP TABLE IF EXISTS ledger_entries;
DROP TABLE IF EXISTS payments;

CREATE TABLE payments (
  payment_id VARCHAR(10) PRIMARY KEY,
  user_id VARCHAR(10) NOT NULL,
  payment_type VARCHAR(30) NOT NULL,
  amount INT NOT NULL,
  currency CHAR(3) NOT NULL,
  created_at DATETIME NOT NULL,
  status VARCHAR(20) NOT NULL
);

CREATE TABLE ledger_entries (
  entry_id VARCHAR(10) PRIMARY KEY,
  payment_id VARCHAR(10) NOT NULL,
  debit_account VARCHAR(50) NOT NULL,
  credit_account VARCHAR(50) NOT NULL,
  amount INT NOT NULL,
  currency CHAR(3) NOT NULL,
  booked_at DATETIME NOT NULL,
  INDEX (payment_id),
  FOREIGN KEY (payment_id) REFERENCES payments(payment_id)
);

CREATE TABLE bank_settlements (
  settlement_id VARCHAR(10) PRIMARY KEY,
  external_ref VARCHAR(10) NOT NULL,
  amount INT NOT NULL,
  currency CHAR(3) NOT NULL,
  settled_at DATETIME NOT NULL,
  settlement_note VARCHAR(30) NOT NULL,
  INDEX (external_ref)
);

CREATE TABLE fees (
  payment_id VARCHAR(10) NOT NULL,
  fee_amount INT NOT NULL,
  currency CHAR(3) NOT NULL,
  fee_type VARCHAR(30) NOT NULL,
  INDEX (payment_id),
  FOREIGN KEY (payment_id) REFERENCES payments(payment_id)
);

CREATE TABLE reversals (
  reversal_id VARCHAR(10) PRIMARY KEY,
  payment_id VARCHAR(10) NOT NULL,
  amount INT NOT NULL,
  currency CHAR(3) NOT NULL,
  reversed_at DATETIME NOT NULL,
  reason VARCHAR(50) NOT NULL,
  INDEX (payment_id),
  FOREIGN KEY (payment_id) REFERENCES payments(payment_id)
);
