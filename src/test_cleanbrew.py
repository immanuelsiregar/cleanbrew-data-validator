import pandas as pd

from validator import (
    check_required_columns,
    missing_value_summary,
    invalid_email_rows,
    invalid_date_rows,
)
from cleaner import run_basic_cleaning
from deduplicator import exact_duplicate_rows, duplicate_entities, drop_exact_duplicates
from issue_report import build_issue_summary, build_missing_summary_display


INPUT_PATH = "data/sample/messy_contacts.csv"


def main():
    df = pd.read_csv(INPUT_PATH)

    missing_cols = check_required_columns(df)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    cleaned = run_basic_cleaning(df)

    missing_summary = missing_value_summary(cleaned)
    invalid_emails = invalid_email_rows(cleaned)
    invalid_dates = invalid_date_rows(cleaned)
    exact_dupes = exact_duplicate_rows(cleaned)
    entity_dupes = duplicate_entities(cleaned, ["email"])
    deduped = drop_exact_duplicates(cleaned)

    issue_summary = build_issue_summary(
        cleaned,
        missing_summary,
        invalid_emails,
        invalid_dates,
        exact_dupes,
        entity_dupes,
    )

    print("Issue summary:")
    print(issue_summary)

    print("\nMissing values:")
    print(build_missing_summary_display(missing_summary))

    print("\nInvalid emails:", len(invalid_emails))
    print("Invalid dates:", len(invalid_dates))
    print("Exact duplicates:", len(exact_dupes))
    print("Duplicate entities by email:", len(entity_dupes))
    print("\nRows before:", len(cleaned))
    print("Rows after exact dedupe:", len(deduped))


if __name__ == "__main__":
    main()