import os
import random
from datetime import datetime, timedelta

import pandas as pd

OUTPUT_PATH = "data/sample/messy_contacts.csv"


FIRST_NAMES = [
    "John", "Sarah", "Michael", "Emily", "David", "Anna", "Chris", "Jessica",
    "Daniel", "Sophia", "Ryan", "Olivia", "Kevin", "Maya", "Ethan", "Nina"
]

LAST_NAMES = [
    "Smith", "Tan", "Lee", "Patel", "Johnson", "Williams", "Brown", "Davis",
    "Wilson", "Anderson", "Thomas", "Jackson", "White", "Harris"
]

COMPANIES = [
    "Northstar Logistics", "BluePeak Media", "UrbanGrid", "Axis Health",
    "NextWave Retail", "CedarPoint Tech", "Greenline Foods", "NovaCore",
    "SignalWorks", "BrightPath Consulting"
]

DOMAINS = [
    "gmail.com", "outlook.com", "company.com", "bizmail.com", "mail.com"
]


def random_date():
    start = datetime(2023, 1, 1)
    end = datetime(2026, 4, 1)
    delta = end - start
    d = start + timedelta(days=random.randint(0, delta.days))
    return d


def build_email(first, last):
    return f"{first.lower()}.{last.lower()}@{random.choice(DOMAINS)}"


def messy_date_string(dt):
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%b %d, %Y"
    ]
    return dt.strftime(random.choice(formats))


def maybe_add_mess(value):
    patterns = [
        value,
        f" {value}",
        f"{value} ",
        f"  {value}  ",
        value.upper(),
        value.title(),
    ]
    return random.choice(patterns)


def generate_rows(n=120, seed=42):
    random.seed(seed)
    rows = []

    for i in range(n):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"
        company = random.choice(COMPANIES)
        email = build_email(first, last)
        signup_dt = random_date()

        row = {
            "customer_id": f"CUST-{1000 + i}",
            "name": maybe_add_mess(name),
            "email": maybe_add_mess(email),
            "company": maybe_add_mess(company),
            "signup_date": messy_date_string(signup_dt),
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    # Inject exact duplicate rows
    dupes = df.sample(8, random_state=seed)
    df = pd.concat([df, dupes], ignore_index=True)

    # Inject duplicate entities with slightly messy formatting
    entity_dupes = df.sample(10, random_state=seed + 1).copy()
    entity_dupes["customer_id"] = [f"CUST-X{i}" for i in range(len(entity_dupes))]
    entity_dupes["name"] = entity_dupes["name"].apply(maybe_add_mess)
    entity_dupes["email"] = entity_dupes["email"].apply(maybe_add_mess)
    df = pd.concat([df, entity_dupes], ignore_index=True)

    # Inject missing values
    missing_idx = df.sample(10, random_state=seed + 2).index
    df.loc[missing_idx[:3], "email"] = None
    df.loc[missing_idx[3:6], "company"] = None
    df.loc[missing_idx[6:], "signup_date"] = None

    # Inject invalid emails
    invalid_idx = df.sample(5, random_state=seed + 3).index
    df.loc[invalid_idx, "email"] = [
        "notanemail",
        "john@@mail",
        "missingdomain@",
        "@nouser.com",
        "broken-email"
    ]

    return df


def main():
    os.makedirs("data/sample", exist_ok=True)
    df = generate_rows()
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated sample dataset: {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")


if __name__ == "__main__":
    main()