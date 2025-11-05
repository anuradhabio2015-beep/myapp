import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
import traceback

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Bank Nifty Dashboard", page_icon="📈", layout="wide")
st.title("📈 Bank Nifty – Stable Streamlit Dashboard")
st.caption("Safely fetches Bank Nifty data, computes RSI & MACD, and plots candles without errors.")

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------
def show_error(e):
    st.error("⚠️ Unexpected error:")
    st.code("".join(traceback.format_exception_only(type(e), e)))

def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def macd(series, fast=12, slow=26, signal=9):
    macd_line = ema(series, fast) - ema(series, slow)
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

# ------------------------------
# DATA FETCH
# ------------------------------
@st.cache_data(ttl=120)
def get_banknifty(interval="15m", days=5):
    ticker = "^NSEBANK"
    start = datetime.now() - timedelta(days=days + 1)
    df = yf.download(ticker, start=start, interval=interval, progress=False)

    if df.empty:
        raise ValueError("No data returned from Yahoo Finance.")

    # ✅ Reset index safely and standardize column
    df = df.copy()
    if not df.index.name:
        df.index.name = "Date"
    df.reset_index(inplace=True)

    # Rename columns in a predictable way
    df.columns = [col.capitalize() for col in df.columns]
    if "Date" not in df.columns:
        # fallback if Yahoo changes schema
        df.insert(0, "Date", df.index)

    # Make sure everything is numeric
    for c in ["Open", "High", "Low", "Close", "Volume"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date", "Close"])
    return df

# ------------------------------
# SIDEBAR SETTINGS
# ------------------------------
st.sidebar.header("⚙️ Settings")
interval = st.sidebar.selectbox("Interval", ["5m", "15m", "30m", "60m", "1d"], index=1)
days = st.sidebar.slider("Lookback Days", 1, 30, 5)
rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)

# ------------------------------
# MAIN APP
# ------------------------------
try:
    df = get_banknifty(interval, days)
    df["RSI"] = rsi(df["Close"], rsi_period)
    df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = macd(df["Close"])

    latest = df.iloc[-1]
    close_val = float(latest["Close"])
    rsi_val = float(latest["RSI"])
    macd_val = float(latest["MACD"])

    # Metrics display
    col1, col2, col3 = st.columns(3)
    col1.metric("Last Close", f"{close_val:,.2f}")
    col2.metric("RSI", f"{rsi_val:,.1f}")
    col3.metric("MACD", f"{macd_val:,.2f}")

    # Chart
    xvals = df["Date"].tolist()
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=xvals,
        open=df["Open"].tolist(),
        high=df["High"].tolist(),
        low=df["Low"].tolist(),
        close=df["Close"].tolist(),
        name="Price"
    ))
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        title="Bank Nifty Candlestick"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Show latest data
    with st.expander("📊 Raw Data (Last 20 Rows)"):
        st.dataframe(df.tail(20))

except Exception as e:
    show_error(e)

st.caption("⚠️ For educational use only — not financial advice.")
