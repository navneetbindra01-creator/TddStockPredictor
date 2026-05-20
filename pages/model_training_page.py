"""Page object for model training operations."""
import math
import pandas as pd


class ModelTrainingPage:
    def __init__(self):
        self._predictor = None
        self.window_size: int | None = None
        self.error: str | None = None

    def train_windowed(self, close_series: pd.Series, window_size: int) -> None:
        from src.predictor import WindowedPredictor
        self.window_size = window_size
        self._predictor = WindowedPredictor(window_size)
        try:
            self._predictor.train(close_series)
        except Exception as exc:
            self.error = str(exc)

    def coefficient_count(self) -> int:
        if self._predictor is None:
            return 0
        return len(self._predictor.coefficients)

    def r_squared(self) -> float:
        if self._predictor is None:
            return float("nan")
        return self._predictor.r_squared
