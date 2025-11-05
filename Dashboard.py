import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
import traceback

# --------------------------- CONFIG ---------------------------
st.set_page_config(page_title="Bank Nifty Dashboard", page_icon="📈", layout="wide")
st.title("📈 Bank Nifty – Resilient Streamlit Dashboard")
st.caption("Fetches Bank Nifty data from Yahoo Finance and plots RSI + MACD candles without errors.")

# --------------------------- HELPERS ---------------------------
def show_error(e):
    st.error("⚠️ Unexpected error:")
    st.code("".join(traceback.format_exception_only(type(e), e)))

def ema(s, span): return s.ewm(span=span, adjust=False).mean()

def rsi(s, period=14):
    d = s.diff()
    g = d.clip(lower=0).rolling(period).mean()
    l = -d.clip(upper=0).rolling(period).mean()
    rs = g / l.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def macd(s, fast=12, slow=26, signal=9):
    m = ema(s, fast) - ema(s, slow)
    sig = ema(m, signal)
    return m, sig, m - sig

# --------------------------- DATA FETCH ---------------------------
@st.cache_data(ttl=120)
def get_banknifty(interval="15m", days=5):
    ticker = "^NSEBANK"
    start = datetime.now() - timedelta(days=days + 1)
    df = yf.download(ticker, start=start, interval=interval, progress=False)
    if df.empty:
        raise ValueError("No data returned from Yahoo Finance.")

    # Flatten multi-index columns if any
    df.columns = ["_".join(map(str, c)) if isinstance(c, tuple) else str(c) for c in df.columns]
    df.reset_index(inplace=True)

    # Identify the correct Close-price column
    possible_close_cols = [c for c in df.columns if "close" in c.lower()]
    if not possible_close_cols:
        raise KeyError("No column found containing 'Close' in its name.")
    close_col = possible_close_cols[0]

    # Create standardized columns
    rename_map = {close_col: "Close"}
    for c in ["Open", "High", "Low", "Volume"]:
        for col in df.columns:
            if c.lower() in col.lower():
                rename_map[col] = c
    df.rename(columns=rename_map, inplace=True)

    if "Date" not in df.columns:
        date_col = [c for c in df.columns if "date" in c.lower()]
        if date_col:
            df.rename(columns={date_col[0]: "Date"}, inplace=True)
        else:
            df.insert(0, "Date", df.index)

    # Ensure datatypes
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    for c in ["Open", "High", "Low", "Close", "Volume"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["Date", "Close"])
    return df

# --------------------------- SIDEBAR ---------------------------
st.sidebar.header("⚙️ Settings")
interval = st.sidebar.selectbox("Interval", ["5m","15m","30m","60m","1d"], index=1)
days = st.sidebar.slider("Lookback Days", 1, 30, 5)
rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)

# --------------------------- MAIN ---------------------------
try:
    df = get_banknifty(interval, days)
    df["RSI"] = rsi(df["Close"], rsi_period)
    df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = macd(df["Close"])

    latest = df.iloc[-1]
    close_val = float(latest["Close"])
    rsi_val = float(latest["RSI"])
    macd_val = float(latest["MACD"])

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Last Close", f"{close_val:,.2f}")
    c2.metric("RSI", f"{rsi_val:,.1f}")
    c3.metric("MACD", f"{macd_val:,.2f}")

    # Chart
    xvals = df["Date"].tolist()
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=xvals,
        open=df.get("Open", df["Close"]).tolist(),
        high=df.get("High", df["Close"]).tolist(),
        low=df.get("Low", df["Close"]).tolist(),
        close=df["Close"].tolist(),
        name="Bank Nifty"
    ))
    fig.update_layout(
        title="Bank Nifty Candlestick",
        xaxis_rangeslider_visible=False,
        height=600,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 Raw Data (Last 20 Rows)"):
        st.dataframe(df.tail(20))

except Exception as e:
    show_error(e)

st.caption("⚠️ For educational use only — not financial advice.")
