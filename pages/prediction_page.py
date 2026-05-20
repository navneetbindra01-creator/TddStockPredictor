"""Page object for stock price prediction operations."""
import math
import pandas as pd


class PredictionPage:
    def __init__(self):
        self.prediction: float | None = None
        self.recent_closes: pd.Series | None = None
        self.error: str | None = None
        self._predictor = None

    def train(self, df: pd.DataFrame, cutoff_date: str) -> None:
        from src.predictor import StockPredictor
        self._predictor = StockPredictor()
        try:
            self._predictor.train(df, cutoff_date)
            self.recent_closes = self._predictor.recent_closes
        except Exception as exc:
            self.error = str(exc)

    def predict(self, date: str) -> None:
        try:
            self.prediction = self._predictor.predict(date)
        except Exception as exc:
            self.error = str(exc)

    def is_valid_prediction(self) -> bool:
        if self.prediction is None:
            return False
        return not math.isnan(self.prediction)

    def is_within_expected_range(self) -> bool:
        if self.recent_closes is None or self.prediction is None:
            return False
        mean = float(self.recent_closes.mean())
        return mean * 0.5 <= self.prediction <= mean * 1.5
