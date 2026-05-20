"""Page object for data preprocessing operations."""
import pandas as pd


class PreprocessingPage:
    def __init__(self):
        self.normalized: pd.Series | None = None
        self.error: str | None = None

    def normalize_minmax(self, series: pd.Series) -> None:
        try:
            from src.normalizer import minmax_normalize
            self.normalized = minmax_normalize(series)
        except Exception as exc:
            self.error = str(exc)
            self.normalized = None

    def all_values_in_range(self, low: float = 0.0, high: float = 1.0) -> bool:
        if self.normalized is None:
            return False
        return bool((self.normalized >= low).all() and (self.normalized <= high).all())

    def min_value(self) -> float:
        return float(self.normalized.min()) if self.normalized is not None else float("nan")

    def max_value(self) -> float:
        return float(self.normalized.max()) if self.normalized is not None else float("nan")
