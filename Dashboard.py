import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Bank Nifty Core", page_icon="📈", layout="wide")
st.title("📈 Bank Nifty – Core Streamlit Dashboard")

# ---------------------------------------------------------------------
# 1️⃣  Data fetch
# ---------------------------------------------------------------------
def get_data(interval="15m", days=5):
    ticker = "^NSEBANK"
    start = datetime.now() - timedelta(days=days + 1)
    df = yf.download(ticker, start=start, interval=interval, progress=False)
    if df.empty:
        st.error("No data returned from Yahoo Finance.")
        st.stop()

    df.reset_index(inplace=True)
    if "Datetime" in df.columns:
        df.rename(columns={"Datetime": "Date"}, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    for c in ["Open", "High", "Low", "Close", "Volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["Close"])
    return df

# ---------------------------------------------------------------------
# 2️⃣  Indicators
# ---------------------------------------------------------------------
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

# ---------------------------------------------------------------------
# 3️⃣  Sidebar
# ---------------------------------------------------------------------
st.sidebar.header("⚙️  Options")
interval = st.sidebar.selectbox("Interval", ["5m","15m","30m","60m","1d"], index=1)
days = st.sidebar.slider("Lookback Days", 1, 30, 5)
rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)

# ---------------------------------------------------------------------
# 4️⃣  Main logic
# ---------------------------------------------------------------------
try:
    df = get_data(interval, days)
    df["RSI"] = rsi(df["Close"], rsi_period)
    df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = macd(df["Close"])

    # Clean latest row
    latest = df.iloc[-1]
    close_val = float(latest["Close"])
    rsi_val = float(latest["RSI"])
    macd_val = float(latest["MACD"])

    # -----------------------------------------------------------------
    #  Metrics
    # -----------------------------------------------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Last Close", f"{close_val:,.2f}")
    col2.metric("RSI", f"{rsi_val:,.1f}")
    col3.metric("MACD", f"{macd_val:,.2f}")

    # -----------------------------------------------------------------
    #  Chart
    # -----------------------------------------------------------------
    xvals = df["Date"].tolist()
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=xvals,
        open=df["Open"].tolist(),
        high=df["High"].tolist(),
        low=df["Low"].tolist(),
        close=df["Close"].tolist(),
        name="Bank Nifty"
    ))
    fig.update_layout(xaxis_rangeslider_visible=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------------------------------
    #  Table
    # -----------------------------------------------------------------
    with st.expander("📊 Raw data (last 20 rows)"):
        st.dataframe(df.tail(20))

except Exception as e:
    import traceback
    st.error("Unexpected error occurred:")
    st.code("".join(traceback.format_exception_only(type(e), e)))
