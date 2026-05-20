"""Step definitions for stock data feature."""
import os
from behave import given, when, then
from pages.stock_data_page import StockDataPage, REQUIRED_COLUMNS

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


@given('historical stock price data for symbol "{symbol}" exists in CSV format')
def step_csv_exists(context, symbol):
    context.symbol = symbol
    context.csv_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    assert os.path.exists(context.csv_path), (
        f"CSV file not found: {context.csv_path}"
    )


@when('the user loads data for symbol "{symbol}" from the file')
def step_load_data(context, symbol):
    context.page = StockDataPage()
    context.page.load_data(symbol, context.csv_path)
    assert context.page.error is None, f"Error loading data: {context.page.error}"


@then("the data should contain at least 100 rows")
def step_check_row_count(context):
    count = context.page.row_count()
    assert count >= 100, f"Expected at least 100 rows, got {count}"


@then('the columns should include "Date", "Open", "High", "Low", "Close", "Volume"')
def step_check_columns(context):
    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in context.page.data.columns
    ]
    assert not missing, f"Missing columns: {missing}"


@given('the user requests data for an invalid symbol "{symbol}"')
def step_invalid_symbol(context, symbol):
    context.invalid_symbol = symbol
    context.invalid_csv_path = os.path.join(DATA_DIR, f"{symbol}.csv")


@when("data loading is attempted")
def step_attempt_load(context):
    context.page = StockDataPage()
    context.page.load_data(context.invalid_symbol, context.invalid_csv_path)


@then("the system should raise a meaningful error or return an empty dataset")
def step_check_error_or_empty(context):
    has_error = context.page.error is not None
    is_empty = context.page.data is not None and len(context.page.data) == 0
    assert has_error or is_empty, (
        f"Expected an error or empty dataset, but got {context.page.row_count()} rows"
    )


@then("the error message should indicate that the symbol could not be found")
def step_check_error_message(context):
    error = context.page.error
    assert error is not None, "Expected an error message but got None"
    assert "could not be found" in error.lower(), (
        f"Error message is not user-friendly: '{error}'"
    )
