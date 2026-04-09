import pandas as pd


def safe_rate(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return round((numerator / denominator) * 100, 2)


def format_number(value: float) -> str:
    return f"{value:,.0f}"


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def executive_kpis(df: pd.DataFrame) -> dict:
    total_applications = len(df)
    verified = (df["verification_status"] == "Verified").sum()
    activated = (df["activation_status"] == "Activated").sum()
    total_spend = df["monthly_spend"].sum()
    total_transactions = df["monthly_transactions"].sum()
    fraud_cases = df["fraud_flag"].sum()
    fraud_amount = df["fraud_amount"].sum()
    complaints = df["complaint_flag"].sum()
    avg_login_days = round(df["login_days_30"].mean(), 1) if not df.empty else 0

    return {
        "total_applications": total_applications,
        "verification_rate": safe_rate(verified, total_applications),
        "activation_rate": safe_rate(activated, total_applications),
        "total_spend": total_spend,
        "total_transactions": total_transactions,
        "fraud_cases": int(fraud_cases),
        "fraud_rate": safe_rate(fraud_cases, total_applications),
        "fraud_amount": fraud_amount,
        "complaint_rate": safe_rate(complaints, total_applications),
        "avg_login_days": avg_login_days,
    }


def onboarding_summary(df: pd.DataFrame) -> pd.DataFrame:
    stages = {
        "Applications": len(df),
        "Verified": int((df["verification_status"] == "Verified").sum()),
        "Activated": int((df["activation_status"] == "Activated").sum()),
    }

    result = pd.DataFrame(
        {
            "stage": list(stages.keys()),
            "count": list(stages.values()),
        }
    )
    result["rate_from_start"] = result["count"].apply(lambda x: safe_rate(x, stages["Applications"]))
    return result


def channel_performance(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby("acquisition_channel", as_index=False)
        .agg(
            applications=("customer_id", "count"),
            verified=("verification_status", lambda x: (x == "Verified").sum()),
            activated=("activation_status", lambda x: (x == "Activated").sum()),
            total_spend=("monthly_spend", "sum"),
            fraud_cases=("fraud_flag", "sum"),
        )
    )
    grouped["verification_rate"] = grouped.apply(lambda row: safe_rate(row["verified"], row["applications"]), axis=1)
    grouped["activation_rate"] = grouped.apply(lambda row: safe_rate(row["activated"], row["applications"]), axis=1)
    grouped["fraud_rate"] = grouped.apply(lambda row: safe_rate(row["fraud_cases"], row["applications"]), axis=1)
    return grouped.sort_values("applications", ascending=False)


def region_performance(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby("region", as_index=False)
        .agg(
            applications=("customer_id", "count"),
            activated=("activation_status", lambda x: (x == "Activated").sum()),
            total_spend=("monthly_spend", "sum"),
            fraud_amount=("fraud_amount", "sum"),
            avg_logins=("login_days_30", "mean"),
        )
    )
    grouped["activation_rate"] = grouped.apply(lambda row: safe_rate(row["activated"], row["applications"]), axis=1)
    grouped["avg_logins"] = grouped["avg_logins"].round(1)
    return grouped.sort_values("activation_rate", ascending=False)


def risk_distribution(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("retention_risk", as_index=False).agg(customers=("customer_id", "count"))
    grouped = grouped.sort_values("customers", ascending=False)
    return grouped


def product_mix(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("product_type", as_index=False).agg(customers=("customer_id", "count"))
    return grouped.sort_values("customers", ascending=False)


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    trend = df.copy()
    trend["month"] = trend["application_date"].dt.to_period("M").astype(str)
    grouped = (
        trend.groupby("month", as_index=False)
        .agg(
            applications=("customer_id", "count"),
            activated=("activation_status", lambda x: (x == "Activated").sum()),
            fraud_cases=("fraud_flag", "sum"),
            spend=("monthly_spend", "sum"),
        )
    )
    grouped["activation_rate"] = grouped.apply(lambda row: safe_rate(row["activated"], row["applications"]), axis=1)
    return grouped
