import pandas as pd


def build_issue_summary(
    df,
    missing_summary,
    invalid_emails,
    invalid_dates,
    exact_dupes,
    entity_dupes,
):
    rows = [
        {"issue_type": "total_rows", "count": len(df)},
        {"issue_type": "columns", "count": len(df.columns)},
        {"issue_type": "rows_with_missing_values", "count": int(df.isna().any(axis=1).sum())},
        {"issue_type": "invalid_email_rows", "count": len(invalid_emails)},
        {"issue_type": "invalid_date_rows", "count": len(invalid_dates)},
        {"issue_type": "exact_duplicate_rows", "count": len(exact_dupes)},
        {"issue_type": "duplicate_entities", "count": len(entity_dupes)},
    ]

    return pd.DataFrame(rows)


def build_missing_summary_display(missing_summary):
    return missing_summary[missing_summary["missing_count"] > 0].copy()