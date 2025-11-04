import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Bank Nifty AI Assistant", page_icon="📈", layout="wide")
st.title("📈 Bank Nifty — Daily AI Trading Assistant")
st.caption("Real-time data with RSI, MACD, Bollinger Bands, and BUY/SELL alerts")

# ---------------------------------
# INDICATOR FUNCTIONS
# ---------------------------------
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

def bollinger(series, period=20, std=2):
    mid = series.rolling(window=period).mean()
    sd = series.rolling(window=period).std()
    upper = mid + std * sd
    lower = mid - std * sd
    return mid, upper, lower

# ---------------------------------
# DATA FETCH
# ---------------------------------
@st.cache_data(ttl=120)
def fetch_data(interval="5m", days=5):
    ticker = "^NSEBANK"  # Bank Nifty Index symbol
    start = datetime.now() - timedelta(days=days + 1)
    df = yf.download(ticker, start=start, interval=interval, progress=False)
    df.reset_index(inplace=True)
    if "Datetime" in df.columns:
        df.rename(columns={"Datetime": "Date"}, inplace=True)
    return df

# ---------------------------------
# SIDEBAR SETTINGS
# ---------------------------------
st.sidebar.header("⚙️ Settings")
interval = st.sidebar.selectbox("Interval", ["5m", "15m", "30m", "60m", "1d"], index=1)
days = st.sidebar.slider("Lookback (days)", 1, 30, 5)
rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)
macd_fast = st.sidebar.slider("MACD Fast EMA", 5, 20, 12)
macd_slow = st.sidebar.slider("MACD Slow EMA", 20, 40, 26)
macd_signal = st.sidebar.slider("MACD Signal", 5, 20, 9)
bb_period = st.sidebar.slider("Bollinger Period", 10, 30, 20)
bb_std = st.sidebar.slider("Bollinger Std Dev", 1.0, 3.0, 2.0)

# ---------------------------------
# FETCH DATA
# ---------------------------------
df = fetch_data(interval, days)
if df.empty:
    st.error("No data fetched for Bank Nifty. Try another interval or check internet connection.")
    st.stop()

# ---------------------------------
# INDICATORS
# ---------------------------------
df["RSI"] = rsi(df["Close"], rsi_period)
df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = macd(df["Close"], macd_fast, macd_slow, macd_signal)
df["BB_Mid"], df["BB_Upper"], df["BB_Lower"] = bollinger(df["Close"], bb_period, bb_std)

# ---------------------------------
# SIGNAL LOGIC (safe version)
# ---------------------------------
df["Buy"] = (df["MACD"] > df["MACD_Signal"]) & (df["RSI"] > 55)
df["Sell"] = (df["MACD"] < df["MACD_Signal"]) & (df["RSI"] < 45)

# Take last row safely
latest_row = df.tail(1).squeeze()

buy_signal = bool(latest_row.get("Buy", False))
sell_signal = bool(latest_row.get("Sell", False))

if buy_signal and not sell_signal:
    signal = "BUY"
elif sell_signal and not buy_signal:
    signal = "SELL"
else:
    signal = "HOLD"

# ---------------------------------
# ALERTS
# ---------------------------------
if signal == "BUY":
    st.toast("✅ **New BUY signal detected!**", icon="✅")
    st.markdown("<audio autoplay><source src='https://actions.google.com/sounds/v1/alarms/beep_short.ogg' type='audio/ogg'></audio>", unsafe_allow_html=True)
elif signal == "SELL":
    st.toast("⚠️ **New SELL signal detected!**", icon="⚠️")
    st.markdown("<audio autoplay><source src='https://actions.google.com/sounds/v1/alarms/beep_short.ogg' type='audio/ogg'></audio>", unsafe_allow_html=True)
else:
    st.toast("ℹ️ Market neutral — no trade signal", icon="ℹ️")

# ---------------------------------
# METRICS PANEL
# ---------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Last Close", f"{latest_row['Close']:.2f}")
col2.metric("RSI", f"{latest_row['RSI']:.1f}")
col3.metric("MACD", f"{latest_row['MACD']:.2f}")
col4.metric("Signal", signal)

# ---------------------------------
# CHART
# ---------------------------------
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08)
fig.add_trace(go.Candlestick(
    x=df["Date"], open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name="Price"
), row=1, col=1)
fig.add_trace(go.Scatter(x=df["Date"], y=df["BB_Upper"], name="BB Upper", line=dict(width=1)), row=1, col=1)
fig.add_trace(go.Scatter(x=df["Date"], y=df["BB_Lower"], name="BB Lower", line=dict(width=1)), row=1, col=1)
fig.add_trace(go.Scatter(x=df["Date"], y=df["MACD"], name="MACD"), row=2, col=1)
fig.add_trace(go.Scatter(x=df["Date"], y=df["MACD_Signal"], name="Signal"), row=2, col=1)
fig.add_trace(go.Bar(x=df["Date"], y=df["MACD_Hist"], name="Histogram", opacity=0.4), row=2, col=1)
fig.update_layout(xaxis_rangeslider_visible=False, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# DATA TABLE
# ---------------------------------
with st.expander("📊 Latest Data (last 20 rows)"):
    st.dataframe(df.tail(20))

# ---------------------------------
# FOOTER
# ---------------------------------
st.caption("⚠️ Educational use only — Not financial advice.")
