import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Bank Nifty AI Assistant",
    page_icon="📈",
    layout="wide"
)
st.title("📈 Bank Nifty — Daily AI Trading Assistant")
st.caption("Live data with RSI, MACD, Bollinger Bands, and Buy/Sell signals with alerts")

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def macd(series, fast=12, slow=26, signal=9):
    macd_line = ema(series, fast) - ema(series, slow)
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def bollinger(series, period=20, std=2):
    mid = series.rolling(window=period).mean()
    sd = series.rolling(window=period).std()
    upper = mid + std * sd
    lower = mid - std * sd
    return mid, upper, lower

# -------------------------------
# DATA FETCH
# -------------------------------
@st.cache_data(ttl=60)
def fetch_data(interval="5m", days=5):
    try:
        ticker = "^NSEBANK"
        start = datetime.now() - timedelta(days=days + 1)
        df = yf.download(ticker, start=start, interval=interval, progress=False)
        df.reset_index(inplace=True)
        df.rename(columns={"Datetime": "Date"}, inplace=True)
        return df, "Yahoo Finance"
    except Exception as e:
        st.error(f"Data fetch error: {e}")
        return pd.DataFrame(), "Error"

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("⚙️ Settings")
interval = st.sidebar.selectbox("Candle Interval", ["5m", "15m", "30m", "60m", "1d"], index=1)
days = st.sidebar.slider("Lookback Days", 1, 30, 5)
rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)
macd_fast = st.sidebar.slider("MACD Fast EMA", 5, 20, 12)
macd_slow = st.sidebar.slider("MACD Slow EMA", 20, 40, 26)
macd_signal = st.sidebar.slider("MACD Signal", 5, 20, 9)
bb_period = st.sidebar.slider("Bollinger Period", 10, 30, 20)
bb_std = st.sidebar.slider("Bollinger Std Dev", 1.0, 3.0, 2.0)
auto_refresh = st.sidebar.number_input("Auto-refresh (sec)", 0, 120, 0)

# -------------------------------
# FETCH DATA
# -------------------------------
df, source = fetch_data(interval, days)
if df.empty:
    st.error("No data found.")
    st.stop()

# -------------------------------
# INDICATORS
# -------------------------------
df["RSI"] = rsi(df["Close"], rsi_period)
df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = macd(df["Close"], macd_fast, macd_slow, macd_signal)
df["BB_Mid"], df["BB_Upper"], df["BB_Lower"] = bollinger(df["Close"], bb_period, bb_std)

# -------------------------------
# SIGNALS
# -------------------------------
df["Buy"] = (df["MACD"] > df["MACD_Signal"]) & (df["RSI"] > 55)
df["Sell"] = (df["MACD"] < df["MACD_Signal"]) & (df["RSI"] < 45)
latest = df.iloc[-1]
signal = "BUY" if latest["Buy"] else "SELL" if latest["Sell"] else "HOLD"

# -------------------------------
# ALERT SYSTEM
# -------------------------------
def play_sound(sound_type="buy"):
    """Embed a short audio beep in Streamlit."""
    if sound_type == "buy":
        sound_file = "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAABCxAgAEABAAZGF0YQgAAAAA"
    else:
        sound_file = "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAABCxAgAEABAAZGF0YQgAAAAA"
    st.markdown(
        f"""
        <audio autoplay>
            <source src="{sound_file}" type="audio/wav">
        </audio>
        """,
        unsafe_allow_html=True,
    )

if signal == "BUY":
    st.toast("✅ **New BUY signal detected!**", icon="✅")
    play_sound("buy")
elif signal == "SELL":
    st.toast("⚠️ **New SELL signal detected!**", icon="⚠️")
    play_sound("sell")
else:
    st.toast("ℹ️ Market Neutral / HOLD Zone", icon="ℹ️")

# -------------------------------
# METRICS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Source", source)
col2.metric("Last Close", f"{latest['Close']:.2f}")
col3.metric("RSI", f"{latest['RSI']:.2f}")
col4.metric("Signal", signal)

# -------------------------------
# PLOT
# -------------------------------
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08)
fig.add_trace(go.Candlestick(x=df["Date"], open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name="Price"), row=1, col=1)
fig.add_trace(go.Scatter(x=df["Date"], y=df["BB_Upper"], name="BB Upper", line=dict(width=1)), row=1, col=1)
fig.add_trace(go.Scatter(x=df["Date"], y=df["BB_Lower"], name="BB Lower", line=dict(width=1)), row=1, col=1)
fig.add_trace(go.Scatter(x=df["Date"], y=df["MACD"], name="MACD"), row=2, col=1)
fig.add_trace(go.Scatter(x=df["Date"], y=df["MACD_Signal"], name="Signal"), row=2, col=1)
fig.add_trace(go.Bar(x=df["Date"], y=df["MACD_Hist"], name="Histogram", opacity=0.4), row=2, col=1)
fig.update_layout(xaxis_rangeslider_visible=False, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# TABLE
# -------------------------------
with st.expander("📊 Latest 20 Data Points"):
    st.dataframe(df.tail(20))

# -------------------------------
# FOOTER
# -------------------------------
st.caption("⚠️ This dashboard is for **educational purposes only** — not financial advice.")
