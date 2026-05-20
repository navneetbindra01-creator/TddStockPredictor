"""Step definitions for model training feature."""
import os
from behave import given, when, then
from pages.stock_data_page import StockDataPage
from pages.model_training_page import ModelTrainingPage

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

WINDOW_SIZE = 60


@given('historical "{column}" prices for symbol "{symbol}" are loaded')
def step_load_column(context, column, symbol):
    loader = StockDataPage()
    loader.load_data(symbol, os.path.join(DATA_DIR, f"{symbol}.csv"))
    assert loader.error is None, f"Data load error: {loader.error}"
    assert column in loader.data.columns, (
        f"Column '{column}' not found. Available: {list(loader.data.columns)}"
    )
    context.price_series = loader.data[column]
    context.column = column


@when("the user trains a linear regression model using the last 60 days as features")
def step_train_windowed(context):
    context.training_page = ModelTrainingPage()
    context.training_page.train_windowed(context.price_series, WINDOW_SIZE)
    assert context.training_page.error is None, (
        f"Training error: {context.training_page.error}"
    )


@then("the model should produce a coefficient array of the expected size")
def step_check_coeff_size(context):
    count = context.training_page.coefficient_count()
    assert count == WINDOW_SIZE, (
        f"Expected {WINDOW_SIZE} coefficients, got {count}"
    )


@then("the model's R-squared score on the training set should be greater than 0.8")
def step_check_r_squared(context):
    score = context.training_page.r_squared()
    assert score > 0.8, (
        f"R² score {score:.4f} is not greater than 0.8"
    )
