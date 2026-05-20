"""Step definitions for anomaly detection feature."""
import math
import os
from behave import given, when, then
from pages.stock_data_page import StockDataPage
from pages.anomaly_page import AnomalyPage

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


@given('the last 30 days of closing prices for symbol "{symbol}" are loaded')
def step_load_30_days(context, symbol):
    loader = StockDataPage()
    loader.load_data(symbol, os.path.join(DATA_DIR, f"{symbol}.csv"))
    assert loader.error is None, f"Data load error: {loader.error}"
    context.anomaly_page = AnomalyPage()
    context.anomaly_page.load_recent_prices(loader.data["Close"], n=30)


@given("the mean price over the last 30 days is known")
def step_mean_known(context):
    mean = context.anomaly_page.mean
    assert mean is not None and not math.isnan(mean), (
        f"Mean is not a valid number: {mean}"
    )


@when("the user requests anomaly detection on today's closing price")
def step_detect_anomaly(context):
    # Use a price 4 std devs above the mean to guarantee a detectable spike
    spike_price = context.anomaly_page.mean + 4 * context.anomaly_page.std
    context.anomaly_page.check_anomaly(spike_price)
    assert context.anomaly_page.error is None, (
        f"Anomaly detection error: {context.anomaly_page.error}"
    )


@then("a spike should be flagged if today's price exceeds the mean by more than 3 standard deviations")
def step_spike_flagged(context):
    assert context.anomaly_page.is_anomaly is True, (
        "Expected price 4 std devs above mean to be flagged as anomaly"
    )


@then("the system should return a boolean flag indicating whether today is an anomaly")
def step_returns_bool(context):
    assert isinstance(context.anomaly_page.is_anomaly, bool), (
        f"Expected bool, got {type(context.anomaly_page.is_anomaly)}"
    )
