"""Walk-forward backtester for windowed stock price predictions."""
import numpy as np
import pandas as pd
from src.predictor import WindowedPredictor


class Backtester:
    def __init__(self, window_size: int = 60):
        self.window_size = window_size
        self.predictions: list[float] = []
        self.actuals: list[float] = []
        self.mae_pct: float | None = None

    def run(self, close_series: pd.Series, validation_days: int = 10) -> None:
        prices = close_series.to_numpy(dtype=float)
        n = len(prices)
        train_end = n - validation_days

        if train_end < self.window_size + 1:
            raise ValueError(
                f"Not enough data: need at least {self.window_size + 1} rows "
                f"before the validation window, got {train_end}"
            )

        predictor = WindowedPredictor(self.window_size)
        predictor.train(pd.Series(prices[:train_end]))

        self.actuals = prices[train_end:].tolist()
        self.predictions = []

        for i in range(validation_days):
            window = prices[train_end + i - self.window_size : train_end + i]
            self.predictions.append(predictor.predict_from_window(window))

        self.mae_pct = float(
            np.mean([abs(p - a) / a * 100 for p, a in zip(self.predictions, self.actuals)])
        )
