"""Page object for anomaly detection operations."""
import pandas as pd


class AnomalyPage:
    def __init__(self):
        self.history: pd.Series | None = None
        self.mean: float | None = None
        self.std: float | None = None
        self.is_anomaly: bool | None = None
        self.error: str | None = None

    def load_recent_prices(self, series: pd.Series, n: int = 30) -> None:
        self.history = series.tail(n).reset_index(drop=True)
        self.mean = float(self.history.mean())
        self.std = float(self.history.std())

    def check_anomaly(self, price: float) -> None:
        from src.anomaly_detector import detect_spike
        try:
            self.is_anomaly = detect_spike(price, self.history)
        except Exception as exc:
            self.error = str(exc)
