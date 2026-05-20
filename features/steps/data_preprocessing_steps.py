"""Step definitions for data preprocessing feature."""
import os
from behave import given, when, then
from pages.stock_data_page import StockDataPage
from pages.preprocessing_page import PreprocessingPage

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


@given('historical closing prices for symbol "{symbol}" are loaded')
def step_load_closing_prices(context, symbol):
    loader = StockDataPage()
    csv_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    loader.load_data(symbol, csv_path)
    assert loader.error is None, f"Failed to load data: {loader.error}"
    assert loader.data is not None, "No data loaded"
    context.closing_prices = loader.data["Close"]


@when("the user normalizes the closing prices using MinMax scaling")
def step_normalize_minmax(context):
    context.preprocessing = PreprocessingPage()
    context.preprocessing.normalize_minmax(context.closing_prices)
    assert context.preprocessing.error is None, (
        f"Normalization error: {context.preprocessing.error}"
    )


@then("all normalized values should be between 0 and 1 inclusive")
def step_check_range(context):
    assert context.preprocessing.all_values_in_range(0.0, 1.0), (
        f"Values out of range — min={context.preprocessing.min_value():.6f}, "
        f"max={context.preprocessing.max_value():.6f}"
    )


@then("the highest price should correspond to 1, and the lowest to 0")
def step_check_extremes(context):
    min_val = context.preprocessing.min_value()
    max_val = context.preprocessing.max_value()
    assert abs(min_val - 0.0) < 1e-9, f"Expected min=0.0, got {min_val}"
    assert abs(max_val - 1.0) < 1e-9, f"Expected max=1.0, got {max_val}"
