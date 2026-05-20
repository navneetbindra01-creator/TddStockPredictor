Feature: Backtest stock price predictions
  As a stock analyst
  I want to backtest my prediction model on historical data
  So that I can evaluate its accuracy before deploying it on live prices

  Scenario: Backtest predictions over a 10-day window
    Given a trained model exists for symbol "AAPL"
    And a validation window of 10 historical days is selected
    When the user runs a backtest over these 10 days
    Then the system should generate one predicted price per day
    And the mean absolute error between predictions and actual prices should be less than 3%
