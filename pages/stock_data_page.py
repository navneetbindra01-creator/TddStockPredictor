"""Page object for stock data operations."""
import os
import pandas as pd
from src.stock_loader import load_stock_data


REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Volume"]


class StockDataPage:
    def __init__(self):
        self.data = None
        self.symbol = None
        self.error = None

    def load_data(self, symbol: str, file_path: str) -> None:
        self.symbol = symbol
        data_dir = os.path.dirname(file_path)
        try:
            self.data = load_stock_data(symbol, data_dir)
        except Exception as exc:
            self.error = str(exc)
            self.data = None

    def row_count(self) -> int:
        return len(self.data) if self.data is not None else 0

    def has_required_columns(self, columns: list[str]) -> bool:
        if self.data is None:
            return False
        return all(col in self.data.columns for col in columns)
