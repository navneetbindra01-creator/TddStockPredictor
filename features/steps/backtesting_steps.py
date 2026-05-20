"""Step definitions for backtesting feature."""
import os
from behave import given, when, then
from pages.backtesting_page import BacktestingPage

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


@given('a trained model exists for symbol "{symbol}"')
def step_model_exists(context, symbol):
    context.backtest_page = BacktestingPage()
    context.backtest_page.load_symbol_data(symbol, DATA_DIR)
    assert context.backtest_page.error is None, (
        f"Data load error: {context.backtest_page.error}"
    )


@given("a validation window of {days:d} historical days is selected")
def step_validation_window(context, days):
    context.backtest_page.set_validation_window(days)
    context.validation_days = days


@when("the user runs a backtest over these {days:d} days")
def step_run_backtest(context, days):
    context.backtest_page.run_backtest()
    assert context.backtest_page.error is None, (
        f"Backtest error: {context.backtest_page.error}"
    )


@then("the system should generate one predicted price per day")
def step_check_prediction_count(context):
    count = context.backtest_page.prediction_count()
    assert count == context.validation_days, (
        f"Expected {context.validation_days} predictions, got {count}"
    )


@then("the mean absolute error between predictions and actual prices should be less than 3%")
def step_check_mae(context):
    mae = context.backtest_page.mae_pct()
    assert mae < 3.0, (
        f"MAE of {mae:.2f}% is not less than 3%"
    )
