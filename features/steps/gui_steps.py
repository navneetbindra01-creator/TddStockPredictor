"""Step definitions for GUI feature."""
import os
from behave import given, when, then
from pages.gui_page import GuiPage

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GUI_PATH = os.path.join(PROJECT_ROOT, "src", "gui.py")


@given("the user wants to use a GUI to enter a stock symbol")
def step_open_gui(context):
    context.gui_page = GuiPage(GUI_PATH)
    context.gui_page.open()


@when('uploading the price data for symbol "{symbol}"')
def step_upload_data(context, symbol):
    context.gui_page.enter_symbol_and_predict(symbol)


@then("the GUI should display a predicted stock price")
def step_check_prediction(context):
    assert not context.gui_page.has_app_errors(), (
        f"GUI raised an error: {context.gui_page.error_text()}"
    )
    assert context.gui_page.has_prediction(), (
        "Expected a predicted price metric to be displayed"
    )
    value = context.gui_page.prediction_value()
    assert value is not None and "$" in value, (
        f"Prediction value '{value}' does not look like a price"
    )
