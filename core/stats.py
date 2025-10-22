# core/stats.py
# KPI computation and sampling logic (newest first when possible).

import pandas as pd
from typing import Dict, List

def compute_basic_stats(df: pd.DataFrame, rating_col: str = "rating") -> Dict:
    """
    Returns:
      - total_responses: number of rows
      - avg_rating: mean rating if rating column exists and is parseable
    """
    total = len(df)
    avg = None

    if rating_col in df.columns:
        def parse_rating(x):
            try:
                return float(x)
            except Exception:
                return None
        ratings = [r for r in df[rating_col].map(parse_rating).tolist() if r is not None]
        avg = round(sum(ratings) / len(ratings), 2) if ratings else None

    return {
        "total_responses": total,
        "avg_rating": avg,
        "has_rating": rating_col in df.columns,
        "rating_col": rating_col,
    }

def sample_feedback_texts(
    df: pd.DataFrame,
    text_col: str = "feedback",
    date_col: str = "date",
    n: int = 200
) -> List[str]:
    """
    Returns up to n feedback texts (newest first if date column exists).
    Drops empty values.
    """
    if date_col in df.columns:
        try:
            df = df.copy()
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            df = df.sort_values(by=date_col, ascending=False)
        except Exception:
            pass

    s = df[text_col].dropna().astype(str).str.strip()
    s = s[s != ""]
    if len(s) == 0:
        return []

    return s.head(n).tolist()
