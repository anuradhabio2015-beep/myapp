import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import traceback

st.set_page_config(page_title="Bank Nifty AI Assistant", page_icon="📈", layout="wide")
st.title("📈 Bank Nifty — Daily AI Trading Assistant (debug-safe build)")

# -------------------------------  UTILITIES  -------------------------------
def show_error(e):
    """Display the real exception on screen."""
    st.error("⚠️ An unexpected error occurred:")
    st.code("".join(traceback.format_exception_only(type(e), e)))

def ema(series, span): return series.ewm(span=span, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def macd(series, fast=12, slow=26, signal=9):
    macd_line = ema(series, fast) - ema(series, slow)
    signal_line = ema(macd_line, signal)
    return macd_line, signal_line, macd_line - signal_line

def bollinger(series, period=20, std=2):
    mid = series.rolling(period).mean()
    sd = series.rolling(period).std()
    return mid, mid + std*sd, mid - std*sd

@st.cache_data(ttl=120)
def fetch_data(interval="5m", days=5):
    ticker = "^NSEBANK"
    start = datetime.now() - timedelta(days=days + 1)
    df = yf.download(ticker, start=start, interval=interval, progress=False)
    if df.empty:
        raise ValueError("No data received from Yahoo Finance.")
    df.reset_index(inplace=True)
    if "Datetime" in df.columns:
        df.rename(columns
