"""Statistical anomaly detection for stock prices."""
import pandas as pd


def detect_spike(price: float, history: pd.Series, threshold_std: float = 3.0) -> bool:
    """Return True if *price* is more than *threshold_std* standard deviations above the mean of *history*."""
    mean = float(history.mean())
    std = float(history.std())
    if std == 0:
        return False
    return (price - mean) / std > threshold_std
