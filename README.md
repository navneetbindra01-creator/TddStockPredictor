# TDD Stock Price Predictor

An experiment in building a stock price prediction tool in Python using a **Test-Driven Development (TDD)** approach, with tests written in **BDD (Behaviour-Driven Development)** style.

---

## The Experiment

The goal is to explore what happens when every line of production code is written in direct response to a failing test — no code exists until a test demands it.

The process follows a strict red-green cycle for each feature:

1. **Write the BDD scenario** — describe the expected behaviour in plain English using Gherkin (`Given / When / Then`)
2. **Run the test and watch it fail** — the test must fail first; this proves the test is real and that the feature does not yet exist
3. **Write the minimum code to make it pass** — only enough to satisfy the scenario, nothing more
4. **Run the test again and confirm it passes** — green means done

This means the test suite is never an afterthought. It drives every design decision from the very first line.

---

## Why This Approach?

### Tests are automated upfront
Because production code cannot exist before its test, 100% of features have automated test coverage by definition. There is no "we'll add tests later" — later never comes.

### Encourages modularity
Writing a test before code forces you to think about the interface before the implementation. This naturally produces small, focused modules with clear inputs and outputs that are easy to test in isolation.

### Living documentation
The Gherkin feature files are readable by anyone, not just developers. Each scenario describes a concrete business behaviour, making the feature files a form of executable documentation that stays in sync with the code.

### Confidence to change
Because every behaviour is covered by a scenario, refactoring or extending the codebase is safe — the test suite immediately catches any regression.

---

## Project Structure

```
TddStockPredictor/
├── src/                        # Production application code
│   ├── stock_loader.py         # Load and validate CSV stock data
│   ├── normalizer.py           # MinMax scaling of price series
│   ├── predictor.py            # Linear regression predictors (date-index & windowed)
│   ├── anomaly_detector.py     # Z-score spike detection
│   └── backtester.py           # Walk-forward backtesting engine
│
├── features/                   # BDD test infrastructure
│   ├── *.feature               # Gherkin scenarios (plain English)
│   ├── environment.py          # Behave environment hooks
│   └── steps/                  # Step definition files
│
├── pages/                      # BDD page-object layer
│   │                           # Thin adapters between steps and src/
│   ├── stock_data_page.py
│   ├── preprocessing_page.py
│   ├── prediction_page.py
│   ├── model_training_page.py
│   ├── anomaly_page.py
│   └── backtesting_page.py
│
├── data/
│   └── AAPL.csv                # Synthetic historical price data (2022–2024)
│
├── reports/
│   └── test_report.html        # Generated HTML test report
│
├── behave.ini                  # Behave configuration
└── requirements.txt
```

**Key architectural rule:** `src/` is the application. `pages/` and `features/` are test infrastructure. Only `src/` would be shipped — the rest exists to drive it.

---

## Scenarios Implemented

| # | Feature | Scenario |
|---|---------|----------|
| 1 | Stock Data Loading | Load historical stock prices successfully |
| 2 | Stock Data Loading | Reject invalid stock symbol |
| 3 | Data Preprocessing | Normalise closing prices between 0 and 1 |
| 4 | Stock Prediction | Handle missing date in the prediction period |
| 5 | Model Training | Train a linear regression model on historical prices |
| 6 | Anomaly Detection | Detect anomalous price spike compared to recent history |
| 7 | Backtesting | Backtest predictions over a 10-day window |

---

## Running the Tests

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run all scenarios and generate the HTML report
```bash
py -m behave --no-capture --format behave_html_formatter:HTMLFormatter --outfile reports/test_report.html
```

### Expected output
```
6 features passed, 0 failed, 0 skipped
7 scenarios passed, 0 failed, 0 skipped
30 steps passed, 0 failed, 0 skipped
```

Open `reports/test_report.html` in a browser to view the full formatted report.

---

## Tech Stack

| Library | Purpose |
|---------|---------|
| `behave` | BDD test runner (Gherkin feature files + step definitions) |
| `behave-html-formatter` | HTML test reports |
| `pandas` | Data loading and manipulation |
| `numpy` | Numerical operations |
| `scikit-learn` | Linear regression model |
