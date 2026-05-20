"""Loads historical stock price data from CSV files."""
import os
import pandas as pd

REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Volume"]


def load_stock_data(symbol: str, data_dir: str) -> pd.DataFrame:
    """Load stock CSV for *symbol* from *data_dir* and return a DataFrame.

    Raises FileNotFoundError with a user-friendly message if the symbol has no data file.
    """
    path = os.path.join(data_dir, f"{symbol}.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Symbol '{symbol}' could not be found. No data file at: {path}"
        )
    try:
        return pd.read_csv(path, parse_dates=["Date"])
    except Exception as exc:
        raise ValueError(
            f"Symbol '{symbol}' could not be found. Failed to read data: {exc}"
        ) from exc
