Feature: Detect anomalous stock price movements
  As a stock analyst
  I want to detect anomalous price spikes in closing prices
  So that I can investigate unusual market activity

  Scenario: Detect anomalous price spike compared to recent history
    Given the last 30 days of closing prices for symbol "AAPL" are loaded
    And the mean price over the last 30 days is known
    When the user requests anomaly detection on today's closing price
    Then a spike should be flagged if today's price exceeds the mean by more than 3 standard deviations
    And the system should return a boolean flag indicating whether today is an anomaly
