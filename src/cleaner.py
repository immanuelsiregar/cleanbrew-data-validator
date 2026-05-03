import pandas as pd


def trim_whitespace(df):
    df = df.copy()

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
        df.loc[df[col] == "None", col] = pd.NA
        df.loc[df[col] == "nan", col] = pd.NA

    return df


def lowercase_email(df, email_col="email"):
    df = df.copy()

    if email_col in df.columns:
        df[email_col] = df[email_col].astype("string").str.lower()

    return df


def standardize_dates(df, date_col="signup_date"):
    df = df.copy()

    if date_col in df.columns:
        parsed = pd.to_datetime(df[date_col], errors="coerce")
        df[date_col] = parsed.dt.strftime("%Y-%m-%d")
        df.loc[parsed.isna(), date_col] = pd.NA

    return df


def run_basic_cleaning(df):
    df = trim_whitespace(df)
    df = lowercase_email(df)
    df = standardize_dates(df)
    return df


def standardize_column_dates(df, date_col):
    df = df.copy()

    if date_col in df.columns:
        parsed = pd.to_datetime(df[date_col], errors="coerce")
        df[date_col] = parsed.dt.strftime("%Y-%m-%d")
        df.loc[parsed.isna(), date_col] = pd.NA

    return df


def standardize_amount(df, amount_col="amount"):
    df = df.copy()

    if amount_col in df.columns:
        df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")

    return df


def run_transaction_cleaning(df):
    df = trim_whitespace(df)
    df = standardize_column_dates(df, "date")
    df = standardize_amount(df, "amount")
    return df