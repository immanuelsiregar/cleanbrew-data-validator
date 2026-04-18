# Cleanbrew

Cleanbrew is a lightweight data validation and deduplication tool for messy CSV datasets.

It is designed to simulate common business data issues (missing values, invalid formats, duplicates) and provide a simple pipeline to detect, clean, and export improved data.

The project also includes a Streamlit app for interactive validation and cleaning.

---

## Features

- Missing value detection and summary
- Invalid email and date validation
- Exact duplicate detection and removal
- Duplicate entity detection (by configurable keys)
- Cleaned dataset export
- Interactive UI using Streamlit

---

## Installation

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
Then open http://localhost:8501
