Feature: Stock price prediction via GUI
  As a stock analyst
  I want to use a graphical interface to enter a stock symbol and load price data
  So that I can get a predicted stock price without writing code

  Scenario: Predict stock price through the GUI
    Given the user wants to use a GUI to enter a stock symbol
    When uploading the price data for symbol "AAPL"
    Then the GUI should display a predicted stock price
