"""Step definitions for stock price prediction feature."""
import os
from behave import given, when, then
from pages.stock_data_page import StockDataPage
from pages.prediction_page import PredictionPage

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


@given('the model has been trained on historical data up to "{cutoff}"')
def step_train_model(context, cutoff):
    loader = StockDataPage()
    loader.load_data("AAPL", os.path.join(DATA_DIR, "AAPL.csv"))
    assert loader.error is None, f"Data load error: {loader.error}"
    context.prediction_page = PredictionPage()
    context.prediction_page.train(loader.data, cutoff)
    assert context.prediction_page.error is None, (
        f"Training error: {context.prediction_page.error}"
    )


@when('the user requests a prediction for "{date}"')
def step_request_prediction(context, date):
    context.prediction_page.predict(date)
    assert context.prediction_page.error is None, (
        f"Prediction error: {context.prediction_page.error}"
    )


@then("the prediction should return a numeric value (not None or NaN)")
def step_check_numeric(context):
    assert context.prediction_page.is_valid_prediction(), (
        f"Prediction is not a valid number: {context.prediction_page.prediction}"
    )


@then("the result should be within the expected range based on recent prices")
def step_check_range(context):
    page = context.prediction_page
    assert page.is_within_expected_range(), (
        f"Prediction {page.prediction:.2f} is outside ±50% of "
        f"the mean of last 30 training prices "
        f"({page.recent_closes.mean():.2f})"
    )
