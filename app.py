import io
import pandas as pd
import streamlit as st

from src.validator import (
    check_required_columns,
    missing_value_summary,
    invalid_email_rows,
    invalid_date_rows,
)
from src.cleaner import run_basic_cleaning
from src.deduplicator import exact_duplicate_rows, duplicate_entities, drop_exact_duplicates
from src.issue_report import build_issue_summary, build_missing_summary_display


st.set_page_config(page_title="Cleanbrew", layout="wide")

st.title("Cleanbrew")
st.caption("CSV validation and deduplication tool for messy business data")


def load_dataframe(uploaded_file):
    return pd.read_csv(uploaded_file)


uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

sample_path = "data/sample/messy_contacts.csv"

use_sample = st.button("Use sample dataset")

df = None

if uploaded_file is not None:
    df = load_dataframe(uploaded_file)
elif use_sample:
    df = pd.read_csv(sample_path)

if df is not None:
    st.subheader("Raw Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    missing_cols = check_required_columns(df)
    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
        st.stop()

    cleaned = run_basic_cleaning(df)

    missing_summary = missing_value_summary(cleaned)
    invalid_emails = invalid_email_rows(cleaned)
    invalid_dates = invalid_date_rows(cleaned)
    exact_dupes = exact_duplicate_rows(cleaned)

    dedupe_key = st.selectbox(
        "Select duplicate entity key",
        options=["email", "customer_id", "name"],
        index=0,
    )

    entity_dupes = duplicate_entities(cleaned, [dedupe_key])
    deduped = drop_exact_duplicates(cleaned)

    issue_summary = build_issue_summary(
        cleaned,
        missing_summary,
        invalid_emails,
        invalid_dates,
        exact_dupes,
        entity_dupes,
    )

    missing_display = build_missing_summary_display(missing_summary)

    st.subheader("Issue Summary")
    st.dataframe(issue_summary, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Missing Values")
        if len(missing_display) > 0:
            st.dataframe(missing_display, use_container_width=True)
        else:
            st.success("No missing values found.")

        st.subheader("Invalid Emails")
        if len(invalid_emails) > 0:
            st.dataframe(invalid_emails, use_container_width=True)
        else:
            st.success("No invalid emails found.")

    with col2:
        st.subheader("Invalid Dates")
        if len(invalid_dates) > 0:
            st.dataframe(invalid_dates, use_container_width=True)
        else:
            st.success("No invalid dates found.")

        st.subheader("Exact Duplicate Rows")
        if len(exact_dupes) > 0:
            st.dataframe(exact_dupes, use_container_width=True)
        else:
            st.success("No exact duplicates found.")

    st.subheader(f"Duplicate Entities by {dedupe_key}")
    if len(entity_dupes) > 0:
        st.dataframe(entity_dupes, use_container_width=True)
    else:
        st.success(f"No duplicate entities found using {dedupe_key}.")

    st.subheader("Cleaned Data Preview")
    st.dataframe(deduped.head(30), use_container_width=True)

    csv_buffer = io.StringIO()
    deduped.to_csv(csv_buffer, index=False)

    st.download_button(
        label="Download cleaned CSV",
        data=csv_buffer.getvalue(),
        file_name="cleaned_output.csv",
        mime="text/csv",
    )
else:
    st.info("Upload a CSV or use the sample dataset to begin.")