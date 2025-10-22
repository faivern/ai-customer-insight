# core/loader.py
# Safe CSV loading with column normalization and minimum schema checks.

import pandas as pd

REQUIRED_COLUMNS = {"feedback"}  # Minimum column we need

def load_feedback(path: str) -> pd.DataFrame:
    """
    Loads the CSV, normalizes column names (lowercase + trimmed),
    and ensures required columns exist.
    """
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    if not REQUIRED_COLUMNS.issubset(set(df.columns)):
        raise ValueError(f"CSV is missing required column(s): {REQUIRED_COLUMNS}")
    return df
