Feature: Predict future stock prices
  As a stock analyst
  I want to predict future stock prices using a trained model
  So that I can make informed investment decisions

  Scenario: Handle missing date in the prediction period
    Given the model has been trained on historical data up to "2023-12-31"
    When the user requests a prediction for "2024-01-01"
    Then the prediction should return a numeric value (not None or NaN)
    And the result should be within the expected range based on recent prices
