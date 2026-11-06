"""Post-processing functions. These are not the original simulation equations."""
import numpy as np
import pandas as pd

KEYWORDS = (
    "berkelanjutan", "lingkungan", "pelestarian", "konservasi",
    "ramah", "budaya", "lokal", "ekonomi",
)

def filter_sustainability(texts):
    """Apply the documented unbounded substring filter to lowercased text."""
    series = pd.Series(texts, copy=False).astype("string").str.lower()
    return series.str.contains("|".join(KEYWORDS), regex=True, na=False)

def mape(actual, predicted):
    """Mean absolute percentage error in percent for paired finite nonzero observations."""
    observed = np.asarray(actual, dtype=float)
    modeled = np.asarray(predicted, dtype=float)
    if observed.shape != modeled.shape or observed.size == 0:
        raise ValueError("Values must have matching nonempty shapes")
    if not np.isfinite(observed).all() or not np.isfinite(modeled).all():
        raise ValueError("Values must be finite")
    if np.any(observed == 0):
        raise ValueError("MAPE is undefined for a zero reference observation")
    return float(np.mean(np.abs((observed - modeled) / observed)) * 100)

def first_crossing(df, date_column, value_column, threshold, direction="above", smoothing_days=0):
    """Find first threshold crossing (inclusive) in date order, optionally with centered smoothing."""
    series = df[[date_column, value_column]].copy()
    series[date_column] = pd.to_datetime(series[date_column], errors="raise")
    series[value_column] = pd.to_numeric(series[value_column], errors="raise")
    if series[date_column].duplicated().any():
        raise ValueError("Duplicate dates")
    if series[value_column].isna().any() or not np.isfinite(series[value_column]).all():
        raise ValueError("Missing or nonfinite values")
    series = series.sort_values(date_column)
    values = series[value_column]
    if smoothing_days:
        if smoothing_days < 2:
            raise ValueError("Smoothing window must be at least two observations")
        values = values.rolling(smoothing_days, min_periods=smoothing_days, center=True).mean()
    if direction == "above":
        hits = values >= threshold
    elif direction == "below":
        hits = values <= threshold
    else:
        raise ValueError("Direction must be 'above' or 'below'")
    matching = series.loc[hits.fillna(False), date_column]
    return None if matching.empty else matching.iloc[0].date().isoformat()
