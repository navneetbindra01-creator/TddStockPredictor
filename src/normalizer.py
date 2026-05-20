"""MinMax normalization for stock price series."""
import pandas as pd


def minmax_normalize(series: pd.Series) -> pd.Series:
    """Scale *series* to the range [0, 1] using MinMax normalization."""
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val)
