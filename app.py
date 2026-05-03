import io
import pandas as pd
import streamlit as st

from src.validator import (
    TRANSACTION_REQUIRED_COLUMNS,
    check_required_columns,
    missing_value_summary,
    invalid_email_rows,
    invalid_date_rows,
    invalid_transaction_date_rows,
    invalid_amount_rows,
    negative_amount_rows,
)

from src.cleaner import run_basic_cleaning, run_transaction_cleaning

from src.deduplicator import (
    exact_duplicate_rows,
    duplicate_entities,
    duplicate_keys,
    drop_exact_duplicates,
)

from src.issue_report import build_issue_summary, build_missing_summary_display


st.set_page_config(page_title="Cleanbrew", layout="wide")

st.title("Cleanbrew")
st.caption("CSV validation and deduplication tool for messy business data")


def load_dataframe(uploaded_file):
    return pd.read_csv(uploaded_file)


# ----------------------------
# UI INPUT
# ----------------------------

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
use_sample = st.button("Use sample dataset")

sample_path = "data/sample/messy_contacts.csv"

dataset_mode = st.selectbox(
    "Dataset type",
    options=["CRM / Contacts", "Transactions"],
)

df = None

if uploaded_file is not None:
    df = load_dataframe(uploaded_file)
elif use_sample:
    df = pd.read_csv(sample_path)


# ----------------------------
# MAIN LOGIC
# ----------------------------

if df is not None:

    st.subheader("Raw Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    # ----------------------------
    # REQUIRED COLUMNS
    # ----------------------------

    if dataset_mode == "CRM / Contacts":
        required_columns = ["customer_id", "name", "email", "company", "signup_date"]
    else:
        required_columns = TRANSACTION_REQUIRED_COLUMNS

    missing_cols = check_required_columns(df, required_columns)

    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
        st.stop()

    # ----------------------------
    # CLEANING
    # ----------------------------

    if dataset_mode == "CRM / Contacts":
        cleaned = run_basic_cleaning(df)
    else:
        cleaned = run_transaction_cleaning(df)

    # ----------------------------
    # COMMON METRICS
    # ----------------------------

    missing_summary = missing_value_summary(cleaned)
    exact_dupes = exact_duplicate_rows(cleaned)

    # ----------------------------
    # MODE-SPECIFIC VALIDATION
    # ----------------------------

    if dataset_mode == "CRM / Contacts":

        invalid_emails = invalid_email_rows(cleaned)
        invalid_dates = invalid_date_rows(cleaned)

        dedupe_key = st.selectbox(
            "Select duplicate entity key",
            options=["email", "customer_id", "name"],
        )

        entity_dupes = duplicate_entities(cleaned, [dedupe_key])

    else:

        invalid_emails = pd.DataFrame()  # placeholder
        invalid_dates = invalid_transaction_date_rows(cleaned)
        invalid_amounts = invalid_amount_rows(cleaned)
        negative_amounts = negative_amount_rows(cleaned)

        dedupe_key = st.selectbox(
            "Select duplicate key",
            options=["transaction_id", "customer_id"],
        )

        entity_dupes = duplicate_keys(cleaned, dedupe_key)

    deduped = drop_exact_duplicates(cleaned)

    # ----------------------------
    # REPORTING
    # ----------------------------

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

        if dataset_mode == "CRM / Contacts":
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

        if dataset_mode == "Transactions":
            st.subheader("Invalid Amounts")
            if len(invalid_amounts) > 0:
                st.dataframe(invalid_amounts, use_container_width=True)
            else:
                st.success("No invalid amounts found.")

            st.subheader("Negative Amounts (Possible Refunds)")
            if len(negative_amounts) > 0:
                st.dataframe(negative_amounts, use_container_width=True)
            else:
                st.success("No negative amounts found.")

        st.subheader("Exact Duplicate Rows")
        if len(exact_dupes) > 0:
            st.dataframe(exact_dupes, use_container_width=True)
        else:
            st.success("No exact duplicates found.")

    st.subheader(f"Duplicate Entities by {dedupe_key}")
    if len(entity_dupes) > 0:
        st.dataframe(entity_dupes, use_container_width=True)
    else:
        st.success(f"No duplicates found using {dedupe_key}.")

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