Feature: Load historical stock price data
  As a stock analyst
  I want to load historical stock price data from a CSV file
  So that I can use it for price prediction

  Scenario: Load historical stock prices successfully
    Given historical stock price data for symbol "AAPL" exists in CSV format
    When the user loads data for symbol "AAPL" from the file
    Then the data should contain at least 100 rows
    And the columns should include "Date", "Open", "High", "Low", "Close", "Volume"

  Scenario: Reject invalid stock symbol
    Given the user requests data for an invalid symbol "INVALID123"
    When data loading is attempted
    Then the system should raise a meaningful error or return an empty dataset
    And the error message should indicate that the symbol could not be found
