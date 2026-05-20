"""Page object for the Streamlit GUI, backed by Streamlit's AppTest runner."""


class GuiPage:
    def __init__(self, app_path: str):
        self._app_path = app_path
        self._app = None
        self.error: str | None = None

    def open(self) -> None:
        from streamlit.testing.v1 import AppTest
        self._app = AppTest.from_file(self._app_path, default_timeout=30)
        self._app.run()

    def enter_symbol_and_predict(self, symbol: str) -> None:
        self._app.text_input[0].set_value(symbol)
        self._app.button[0].click()
        self._app.run()

    def has_prediction(self) -> bool:
        return len(self._app.metric) > 0

    def prediction_value(self) -> str | None:
        return self._app.metric[0].value if self.has_prediction() else None

    def has_app_errors(self) -> bool:
        return len(self._app.exception) > 0 or len(self._app.error) > 0

    def error_text(self) -> str:
        parts = [str(e) for e in self._app.exception] + [e.value for e in self._app.error]
        return "; ".join(parts)
