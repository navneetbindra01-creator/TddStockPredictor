"""Page object for backtesting operations."""
import pandas as pd


class BacktestingPage:
    def __init__(self):
        self._close_series: pd.Series | None = None
        self._validation_days: int | None = None
        self._backtester = None
        self.error: str | None = None

    def load_symbol_data(self, symbol: str, data_dir: str) -> None:
        from src.stock_loader import load_stock_data
        df = load_stock_data(symbol, data_dir)
        self._close_series = df["Close"]

    def set_validation_window(self, days: int) -> None:
        self._validation_days = days

    def run_backtest(self) -> None:
        from src.backtester import Backtester
        self._backtester = Backtester()
        try:
            self._backtester.run(self._close_series, self._validation_days)
        except Exception as exc:
            self.error = str(exc)

    def prediction_count(self) -> int:
        return len(self._backtester.predictions) if self._backtester else 0

    def mae_pct(self) -> float:
        return self._backtester.mae_pct if self._backtester else float("nan")
