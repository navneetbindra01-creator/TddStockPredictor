"""Linear regression stock price predictor."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class StockPredictor:
    def __init__(self):
        self._model = LinearRegression()
        self._ref_date: pd.Timestamp | None = None
        self.recent_closes: pd.Series | None = None

    def train(self, df: pd.DataFrame, cutoff_date: str) -> None:
        """Fit on all rows where Date <= cutoff_date."""
        train_df = df[df["Date"] <= pd.Timestamp(cutoff_date)].copy()
        if train_df.empty:
            raise ValueError(f"No training data available up to {cutoff_date}")
        self._ref_date = train_df["Date"].min()
        X = self._to_days(train_df["Date"])
        y = train_df["Close"].to_numpy()
        self._model.fit(X, y)
        self.recent_closes = train_df["Close"].tail(30).reset_index(drop=True)

    def predict(self, date: str) -> float:
        """Return the predicted closing price for *date*."""
        target = pd.Series([pd.Timestamp(date)])
        X = self._to_days(target)
        return float(self._model.predict(X)[0])

    def _to_days(self, dates: pd.Series) -> np.ndarray:
        return (dates - self._ref_date).dt.days.values.reshape(-1, 1)


class WindowedPredictor:
    """Linear regression where each sample is a sliding window of *window_size* prices."""

    def __init__(self, window_size: int = 60):
        self.window_size = window_size
        self._model = LinearRegression()
        self.r_squared: float | None = None

    def train(self, close_series: pd.Series) -> None:
        X, y = self._build_windows(close_series.to_numpy())
        if len(X) == 0:
            raise ValueError(
                f"Not enough data to build windows "
                f"(need > {self.window_size} rows, got {len(close_series)})"
            )
        self._model.fit(X, y)
        self.r_squared = float(self._model.score(X, y))

    @property
    def coefficients(self) -> np.ndarray:
        return self._model.coef_

    def predict_from_window(self, window: np.ndarray) -> float:
        """Predict the next price from a single window of *window_size* prices."""
        return float(self._model.predict(window.reshape(1, -1))[0])

    def _build_windows(self, prices: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        n = len(prices)
        X = np.array([prices[i : i + self.window_size] for i in range(n - self.window_size)])
        y = prices[self.window_size :]
        return X, y
