from pathlib import Path

import numpy as np
import pandas as pd


rng = np.random.default_rng(42)
base_dir = Path(__file__).resolve().parent
output_file = base_dir / "digital_banking_data.csv"

regions = ["Northeast", "Midwest", "South", "West"]
channels = ["Mobile App", "Website", "Branch Referral", "Paid Media", "Partner Network"]
products = ["Savings Account", "Checking Account", "Credit Card"]
age_bands = ["18-25", "26-35", "36-45", "46-60", "60+"]
risk_levels = ["Low", "Medium", "High"]

rows = []
dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")

for i in range(1, 2501):
    app_date = pd.Timestamp(rng.choice(dates))
    region = rng.choice(regions, p=[0.28, 0.22, 0.30, 0.20])
    channel = rng.choice(channels, p=[0.30, 0.25, 0.15, 0.20, 0.10])
    product = rng.choice(products, p=[0.35, 0.40, 0.25])
    age_band = rng.choice(age_bands, p=[0.18, 0.30, 0.24, 0.20, 0.08])

    verified_prob = 0.86
    if channel == "Paid Media":
        verified_prob -= 0.06
    if channel == "Branch Referral":
        verified_prob += 0.04

    is_verified = rng.random() < verified_prob
    verification_status = "Verified" if is_verified else "Dropped"

    activation_prob = 0.72 if is_verified else 0.0
    if product == "Credit Card":
        activation_prob -= 0.05
    if channel == "Mobile App":
        activation_prob += 0.03

    is_activated = rng.random() < activation_prob
    activation_status = "Activated" if is_activated else "Not Activated"

    activated_date = pd.NaT
    if is_activated:
        activated_date = app_date + pd.Timedelta(days=int(rng.integers(1, 11)))

    transactions = int(rng.integers(0, 30)) if is_activated else int(rng.integers(0, 4))
    spend = float(np.round(rng.uniform(100, 5000), 2)) if is_activated else float(np.round(rng.uniform(0, 250), 2))

    fraud_prob = 0.035
    if channel == "Paid Media":
        fraud_prob += 0.015
    if product == "Credit Card":
        fraud_prob += 0.01

    fraud_flag = int(rng.random() < fraud_prob)
    fraud_amount = float(np.round(rng.uniform(100, 3500), 2)) if fraud_flag else 0.0

    complaint_prob = 0.07 if is_activated else 0.03
    complaint_flag = int(rng.random() < complaint_prob)

    login_days_30 = int(rng.integers(8, 30)) if is_activated else int(rng.integers(0, 8))

    if not is_activated:
        risk = rng.choice(risk_levels, p=[0.10, 0.30, 0.60])
    elif login_days_30 < 10 or transactions < 4:
        risk = rng.choice(risk_levels, p=[0.15, 0.55, 0.30])
    else:
        risk = rng.choice(risk_levels, p=[0.60, 0.30, 0.10])

    rows.append(
        {
            "customer_id": f"CUST{i:05d}",
            "region": region,
            "acquisition_channel": channel,
            "application_date": app_date.date(),
            "verification_status": verification_status,
            "activation_status": activation_status,
            "activated_date": activated_date.date() if pd.notna(activated_date) else "",
            "age_band": age_band,
            "product_type": product,
            "monthly_transactions": transactions,
            "monthly_spend": spend,
            "fraud_flag": fraud_flag,
            "fraud_amount": fraud_amount,
            "complaint_flag": complaint_flag,
            "login_days_30": login_days_30,
            "retention_risk": risk,
        }
    )

pd.DataFrame(rows).to_csv(output_file, index=False)
print(f"Saved {len(rows)} rows to {output_file}")
