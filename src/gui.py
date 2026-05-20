"""Streamlit GUI for the stock price prediction tool."""
import os
import sys
from datetime import timedelta

import streamlit as st

# Ensure project root is on the path when run via AppTest or streamlit CLI
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from src.stock_loader import load_stock_data
from src.predictor import StockPredictor

_DATA_DIR = os.path.join(_PROJECT_ROOT, "data")

st.title("Stock Price Predictor")
st.caption("Enter a stock symbol to load historical data and predict the next closing price.")

symbol = st.text_input("Stock Symbol", placeholder="e.g. AAPL")

if st.button("Load Data & Predict"):
    if not symbol.strip():
        st.warning("Please enter a stock symbol.")
    else:
        try:
            df = load_stock_data(symbol.strip().upper(), _DATA_DIR)
            st.success(f"Loaded {len(df)} rows for {symbol.strip().upper()}")

            predictor = StockPredictor()
            cutoff = df["Date"].max().strftime("%Y-%m-%d")
            predictor.train(df, cutoff)

            next_day = (df["Date"].max() + timedelta(days=1)).strftime("%Y-%m-%d")
            prediction = predictor.predict(next_day)

            st.metric(label="Predicted Next Closing Price", value=f"${prediction:.2f}")

        except Exception as exc:
            st.error(str(exc))
