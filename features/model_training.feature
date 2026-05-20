Feature: Train a model on historical stock prices
  As a stock analyst
  I want to train a regression model on historical closing prices
  So that I can capture patterns in the data for future prediction

  Scenario: Train a linear regression model on historical prices
    Given historical "Close" prices for symbol "AAPL" are loaded
    When the user trains a linear regression model using the last 60 days as features
    Then the model should produce a coefficient array of the expected size
    And the model's R-squared score on the training set should be greater than 0.8
