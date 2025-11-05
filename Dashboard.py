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
        df.rename(columns={"Datetime": "Date"}, inplace=True)
    for c in ["Open", "High", "Low", "Close", "Volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df.dropna(subset=["Close"], inplace=True)
    return df

# -------------------------------  SIDEBAR  -------------------------------
st.sidebar.header("⚙️ Settings")
interval = st.sidebar.selectbox("Interval", ["5m","15m","30m","60m","1d"], index=1)
days = st.sidebar.slider("Lookback (days)", 1, 30, 5)
rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)
macd_fast = st.sidebar.slider("MACD Fast EMA", 5, 20, 12)
macd_slow = st.sidebar.slider("MACD Slow EMA", 20, 40, 26)
macd_signal = st.sidebar.slider("MACD Signal EMA", 5, 20, 9)
bb_period = st.sidebar.slider("Bollinger Period", 10, 30, 20)
bb_std = st.sidebar.slider("Bollinger Std Dev", 1.0, 3.0, 2.0)

# -------------------------------  MAIN  -------------------------------
try:
    df = fetch_data(interval, days)
    # --- indicators ---
    df["RSI"] = rsi(df["Close"], rsi_period)
    df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = macd(df["Close"], macd_fast, macd_slow, macd_signal)
    df["BB_Mid"], df["BB_Upper"], df["BB_Lower"] = bollinger(df["Close"], bb_period, bb_std)

    # --- signals ---
    df["Buy"]  = ((df["MACD"] > df["MACD_Signal"]) & (df["RSI"] > 55)).fillna(False)
    df["Sell"] = ((df["MACD"] < df["MACD_Signal"]) & (df["RSI"] < 45)).fillna(False)
    last = df.iloc[-1]
    buy, sell = bool(last["Buy"]), bool(last["Sell"])
    signal = "BUY" if buy and not sell else "SELL" if sell and not buy else "HOLD"

    # --- alerts ---
    if signal == "BUY":
        st.toast("✅ BUY signal detected!", icon="✅")
    elif signal == "SELL":
        st.toast("⚠️ SELL signal detected!", icon="⚠️")
    else:
        st.toast("ℹ️ Neutral / Hold", icon="ℹ️")

    # --- metrics ---
    close_val = float(last.get("Close", np.nan))
    rsi_val   = float(last.get("RSI", np.nan))
    macd_val  = float(last.get("MACD", np.nan))
    col1,col2,col3,col4 = st.columns(4)
    col1.metric("Last Close", f"{close_val:.2f}")
    col2.metric("RSI", f"{rsi_val:.1f}")
    col3.metric("MACD", f"{macd_val:.2f}")
    col4.metric("Signal", signal)

    # --- chart ---
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08)
    fig.add_trace(go.Candlestick(x=df["Date"],open=df["Open"],high=df["High"],
                                 low=df["Low"],close=df["Close"],name="Price"),row=1,col=1)
    fig.add_trace(go.Scatter(x=df["Date"],y=df["BB_Upper"],name="BB Upper",line=dict(width=1)),row=1,col=1)
    fig.add_trace(go.Scatter(x=df["Date"],y=df["BB_Lower"],name="BB Lower",line=dict(width=1)),row=1,col=1)
    fig.add_trace(go.Scatter(x=df["Date"],y=df["MACD"],name="MACD"),row=2,col=1)
    fig.add_trace(go.Scatter(x=df["Date"],y=df["MACD_Signal"],name="Signal Line"),row=2,col=1)
    fig.add_trace(go.Bar(x=df["Date"],y=df["MACD_Hist"],name="Hist",opacity=0.4),row=2,col=1)
    fig.update_layout(xaxis_rangeslider_visible=False,height=700,margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig,use_container_width=True)

    # --- data preview ---
    with st.expander("📊 Latest Data (20 rows)"):
        st.dataframe(df.tail(20))

except Exception as e:
    show_error(e)

st.caption("⚠️ Educational use only — not investment advice.")
