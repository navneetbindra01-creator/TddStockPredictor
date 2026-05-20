Feature: Preprocess historical stock price data
  As a stock analyst
  I want to preprocess raw stock price data
  So that it is suitable for use in a machine learning model

  Scenario: Normalize closing prices between 0 and 1
    Given historical closing prices for symbol "AAPL" are loaded
    When the user normalizes the closing prices using MinMax scaling
    Then all normalized values should be between 0 and 1 inclusive
    And the highest price should correspond to 1, and the lowest to 0
