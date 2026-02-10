"""generate_data.py

Regenerates synthetic datasets for the SQL reconciliation lab.
Outputs CSV files into ../data.

Usage:
  python generate_data.py
"""

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

def generate(seed: int = 7):
    random.seed(seed)
    np.random.seed(seed)

    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)

    base_date = datetime(2026, 2, 1, 9, 0, 0)

    # Payments
    payments = []
    payment_types = ["TEF", "DIRECT_DEBIT", "PAYROLL_PORTABILITY"]

    for i in range(1, 41):
        created_at = base_date + timedelta(minutes=int(np.random.randint(0, 60*24*3)))
        ptype = random.choice(payment_types)
        amount = int(np.random.choice([250, 399, 500, 750, 999, 1200, 1500, 1800, 2500, 3200, 5000]))
        status = "completed" if np.random.rand() < 0.85 else random.choice(["failed", "pending"])
        payments.append([f"P{i:04d}", f"U{np.random.randint(1, 21):03d}", ptype, amount, "MXN",
                         created_at.strftime("%Y-%m-%d %H:%M:%S"), status])

    payments_df = pd.DataFrame(payments, columns=[
        "payment_id","user_id","payment_type","amount","currency","created_at","status"
    ])

    # Ledger entries (some missing)
    ledger = []
    entry_id = 1
    for _, row in payments_df.iterrows():
        if row["status"] != "completed":
            continue
        if np.random.rand() < 0.05:
            continue
        booked_at = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S") + timedelta(seconds=int(np.random.randint(5, 120)))
        ledger.append([f"L{entry_id:05d}", row["payment_id"], "user_wallet", "clearing_account",
                       int(row["amount"]), row["currency"], booked_at.strftime("%Y-%m-%d %H:%M:%S")])
        entry_id += 1

    ledger_df = pd.DataFrame(ledger, columns=[
        "entry_id","payment_id","debit_account","credit_account","amount","currency","booked_at"
    ])

    # Fees
    fees = []
    for _, row in payments_df.iterrows():
        if row["status"] != "completed":
            continue
        fee = 0
        if row["payment_type"] == "TEF" and np.random.rand() < 0.55:
            fee = int(np.random.choice([3,5,7,10,12,15]))
        elif row["payment_type"] != "TEF" and np.random.rand() < 0.15:
            fee = int(np.random.choice([2,4,6,8]))
        if fee > 0:
            fees.append([row["payment_id"], fee, row["currency"], "rail_fee"])

    fees_df = pd.DataFrame(fees, columns=["payment_id","fee_amount","currency","fee_type"])

    # Reversals
    reversals = []
    for _, row in payments_df.iterrows():
        if row["status"] != "completed":
            continue
        if np.random.rand() < 0.12:
            reversed_at = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S") + timedelta(hours=int(np.random.randint(1, 30)))
            reversals.append([f"R{np.random.randint(10000,99999)}", row["payment_id"], int(row["amount"]), row["currency"],
                              reversed_at.strftime("%Y-%m-%d %H:%M:%S"), random.choice(["insufficient_funds","bank_reject","user_cancel"])])
    reversals_df = pd.DataFrame(reversals, columns=["reversal_id","payment_id","amount","currency","reversed_at","reason"])

    # Bank settlements with injected issues
    settlements = []
    sid = 1
    for _, row in payments_df.iterrows():
        if row["status"] != "completed":
            continue

        is_reversed = (reversals_df["payment_id"] == row["payment_id"]).any()
        if np.random.rand() < 0.10 and not is_reversed:
            continue

        created_dt = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S")
        lag_hours = int(np.random.choice([0,1,2,3,4,6,12,18,24,36]))
        settled_at = created_dt + timedelta(hours=lag_hours, minutes=int(np.random.randint(0, 60)))

        fee_row = fees_df[fees_df["payment_id"] == row["payment_id"]]
        fee_amt = int(fee_row["fee_amount"].iloc[0]) if not fee_row.empty else 0

        settled_amount = int(row["amount"])
        settlement_note = "gross"
        if fee_amt > 0 and np.random.rand() < 0.7:
            settled_amount = int(row["amount"]) - fee_amt
            settlement_note = "net_of_fee"

        if np.random.rand() < 0.06:
            settled_amount = int(max(1, settled_amount + np.random.choice([-25, -10, 10, 30, 50])))
            settlement_note = "amount_mismatch"

        currency = row["currency"]
        if np.random.rand() < 0.03:
            currency = "USD"

        settlements.append([f"S{sid:05d}", row["payment_id"], settled_amount, currency,
                            settled_at.strftime("%Y-%m-%d %H:%M:%S"), settlement_note])
        sid += 1

        if np.random.rand() < 0.05:
            dup_settled_at = settled_at + timedelta(minutes=int(np.random.randint(1, 20)))
            settlements.append([f"S{sid:05d}", row["payment_id"], settled_amount, currency,
                                dup_settled_at.strftime("%Y-%m-%d %H:%M:%S"), "duplicate_record"])
            sid += 1

    settlements_df = pd.DataFrame(settlements, columns=["settlement_id","external_ref","amount","currency","settled_at","settlement_note"])

    # Guarantee at least one missing settlement with ledger present
    candidates = payments_df[payments_df["status"]=="completed"]
    classic_missing_pid = None
    for pid in candidates["payment_id"].tolist():
        if (ledger_df["payment_id"]==pid).any() and not (settlements_df["external_ref"]==pid).any():
            classic_missing_pid = pid
            break
    if classic_missing_pid is None and len(candidates) > 0:
        classic_missing_pid = candidates.iloc[0]["payment_id"]
        settlements_df = settlements_df[settlements_df["external_ref"]!=classic_missing_pid]

    # Write with headers
    payments_df.to_csv(os.path.join(out_dir, "payments.csv"), index=False)
    ledger_df.to_csv(os.path.join(out_dir, "ledger_entries.csv"), index=False)
    settlements_df.to_csv(os.path.join(out_dir, "bank_settlements.csv"), index=False)
    fees_df.to_csv(os.path.join(out_dir, "fees.csv"), index=False)
    reversals_df.to_csv(os.path.join(out_dir, "reversals.csv"), index=False)

    # Write no-header for restricted import tools
    payments_df.to_csv(os.path.join(out_dir, "payments_no_header.csv"), index=False, header=False)
    ledger_df.to_csv(os.path.join(out_dir, "ledger_entries_no_header.csv"), index=False, header=False)
    settlements_df.to_csv(os.path.join(out_dir, "bank_settlements_no_header.csv"), index=False, header=False)
    fees_df.to_csv(os.path.join(out_dir, "fees_no_header.csv"), index=False, header=False)
    reversals_df.to_csv(os.path.join(out_dir, "reversals_no_header.csv"), index=False, header=False)

    return classic_missing_pid

def main():
    pid = generate(seed=7)
    print("Generated CSVs into ../data")
    print("Classic missing settlement payment_id:", pid)

if __name__ == "__main__":
    main()
