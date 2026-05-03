import pandas as pd


def exact_duplicate_rows(df):
    return df[df.duplicated(keep=False)].copy()


def duplicate_entities(df, key_columns):
    if not key_columns:
        return pd.DataFrame(columns=df.columns)

    valid_keys = [col for col in key_columns if col in df.columns]
    if not valid_keys:
        return pd.DataFrame(columns=df.columns)

    dupes = df[df.duplicated(subset=valid_keys, keep=False)].copy()
    return dupes.sort_values(valid_keys)


def drop_exact_duplicates(df):
    return df.drop_duplicates().copy()

def duplicate_keys(df, key_col):
    if key_col not in df.columns:
        return pd.DataFrame(columns=df.columns)

    return df[df.duplicated(subset=[key_col], keep=False)].copy()