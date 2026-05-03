import pandas as pd
import re

REQUIRED_COLUMNS = ["customer_id", "name", "email", "company", "signup_date"]

EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


def check_required_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return missing


def missing_value_summary(df):
    summary = df.isna().sum().reset_index()
    summary.columns = ["column", "missing_count"]
    summary["missing_pct"] = (summary["missing_count"] / len(df) * 100).round(2)
    return summary.sort_values("missing_count", ascending=False)


def invalid_email_rows(df, email_col="email"):
    if email_col not in df.columns:
        return pd.DataFrame(columns=df.columns)

    mask = df[email_col].notna() & ~df[email_col].astype(str).str.match(EMAIL_PATTERN, na=False)
    return df[mask].copy()


def invalid_date_rows(df, date_col="signup_date"):
    if date_col not in df.columns:
        return pd.DataFrame(columns=df.columns)

    parsed = pd.to_datetime(df[date_col], errors="coerce")
    mask = df[date_col].notna() & parsed.isna()
    return df[mask].copy()


TRANSACTION_REQUIRED_COLUMNS = [
    "transaction_id",
    "date",
    "customer_id",
    "product",
    "category",
    "amount",
]


def check_required_columns(df, required_columns=None):
    if required_columns is None:
        required_columns = REQUIRED_COLUMNS

    missing = [col for col in required_columns if col not in df.columns]
    return missing


def invalid_amount_rows(df, amount_col="amount"):
    if amount_col not in df.columns:
        return pd.DataFrame(columns=df.columns)

    parsed = pd.to_numeric(df[amount_col], errors="coerce")
    mask = df[amount_col].notna() & parsed.isna()
    return df[mask].copy()


def negative_amount_rows(df, amount_col="amount"):
    if amount_col not in df.columns:
        return pd.DataFrame(columns=df.columns)

    parsed = pd.to_numeric(df[amount_col], errors="coerce")
    mask = parsed < 0
    return df[mask].copy()


def invalid_transaction_date_rows(df, date_col="date"):
    if date_col not in df.columns:
        return pd.DataFrame(columns=df.columns)

    parsed = pd.to_datetime(df[date_col], errors="coerce")
    mask = df[date_col].notna() & parsed.isna()
    return df[mask].copy()