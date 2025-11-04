# app.py
# Streamlit: Daily Bank Nifty Trading Assistant
# Features:
# - Data source: NSE (primary) with automatic fallback to Yahoo Finance (^NSEBANK)
# - Indicators: RSI(14), MACD(12,26,9), Bollinger Bands(20,2)
# - Signals: MACD crossovers + RSI filter + price vs Bollinger midline
# - UI: Interactive candlestick + overlays, MACD panel, option to auto-refresh
# - Alerts: On-screen toasts when a fresh Buy/Sell signal appears

import time
import io
import math
import json
import numpy as np
import pandas as pd
import requests
import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta, timezone
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------
# Streamlit page config
# -----------------------------
st.set_page_config(
    page_title="Bank Nifty — Daily Trading Assistant",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Bank Nifty — Daily Trading Assistant")
st.caption("Live(ish) data with NSE → Yahoo fallback · RSI, MACD, Bollinger · Signals + Alerts")

# -----------------------------
# Helpers: Indicators
# -----------------------------
def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / (loss.replace(0, np.nan))
    rsi_val = 100 - (100 / (1 + rs))
    return rsi_val

def macd(series: pd.Series, fast=12, slow=26, signal=9):
    macd_line = ema(series, fast) - ema(series, slow)
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def bollinger(series: pd.Series, period=20, stddev=2.0):
    mid = series.rolling(period).mean()
    sd = series.rolling(period).std()
    upper = mid + stddev * sd
    lower = mid - stddev * sd
    return mid, upper, lower

# -----------------------------
# Data fetchers
# -----------------------------
@st.cache_data(ttl=60)
def fetch_banknifty_from_nse(interval: str = "5m", lookback_days: int = 5) -> pd.DataFrame:
    """
    Attempts to fetch Bank Nifty candles from NSE's chart API.
    Known index key is 'NIFTY BANK' on this endpoint in many environments.

    Returns a DataFrame with columns:
      ['Datetime','Open','High','Low','Close','Volume']
    Raises on failure so caller can fallback.
    """
    # Normalize interval mapping to NSE accepted resolutions if needed
    # NSE commonly supports 1m/5m/15m/30m/60m/1d; we’ll pass through.
    base = "https://www.nseindia.com"
    # Historically used endpoint:
    url = f"{base}/api/chart-databyindex?index=NIFTY%20BANK&indices=true"

    # Warm-up request to set cookies (NSE requires valid cookies + headers)
    headers = {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "accept-language": "en-US,en;q=0.9",
        "accept": "*/*",
        "referer": "https://www.nseindia.com/market-data/live-equity-market",
        "connection": "keep-alive",
    }

    session = requests.Session()
    session.get(base, headers=headers, timeout=10)

    # Fetch data
    resp = session.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    # The JSON payload historically exposes keys like "grapthData" (typo in API)
    # We'll try both "grapthData" and "graphData" to be resilient.
    graph = data.get("grapthData") or data.get("graphData")
    if not graph or not isinstance(graph, list):
        raise RuntimeError("Unexpected NSE response shape for graph data.")

    # The records usually have [timestamp(ms), close]
    # Some variants include OHLC; we’ll try to infer.
    # Build a frame robustly:
    # Try OHLC payload first
    df = None
    if isinstance(graph[0], dict):
        # Possible keys: 'time', 'open', 'high', 'low', 'close', 'volume'
        rows = []
        for row in graph:
            ts = row.get("time") or row.get("date") or row.get("timestamp")
            if ts is None:
                continue
            # timestamp in ms?
            if ts > 1e12:
                dt = datetime.utcfromtimestamp(ts / 1000.0).replace(tzinfo=timezone.utc).astimezone()
            else:
                dt = datetime.utcfromtimestamp(ts).replace(tzinfo=timezone.utc).astimezone()
            rows.append({
                "Datetime": dt,
                "Open": float(row.get("open", np.nan)),
                "High": float(row.get("high", np.nan)),
                "Low": float(row.get("low", np.nan)),
                "Close": float(row.get("close", np.nan)),
                "Volume": float(row.get("volume", np.nan)),
            })
        df = pd.DataFrame(rows)
    else:
        # Fallback: [[ts(ms), close], ...]
        rows = []
        for ts, close in graph:
            if ts > 1e12:
                dt = datetime.utcfromtimestamp(ts / 1000.0).replace(tzinfo=timezone.utc).astimezone()
            else:
                dt = datetime.utcfromtimestamp(ts).replace(tzinfo=timezone.utc).astimezone()
            rows.append({"Datetime": dt, "Close": float(close)})
        df = pd.DataFrame(rows)
        # No OHLC given; synthesize from Close (not ideal, but allows indicators)
        df["Open"] = df["Close"]
        df["High"] = df["Close"]
        df["Low"] = df["Close"]
        df["Volume"] = np.nan

    # Restrict to lookback window
    cutoff = datetime.now().astimezone() - timedelta(days=lookback_days)
    df = df[df["Datetime"] >= cutoff].sort_values("Datetime").reset_index(drop=True)

    # Optional downsample to chosen interval (we’ll leave as-is; many NSE responses are ~1m)
    return df

@st.cache_data(ttl=60)
def fetch_banknifty_from_yahoo(interval: str = "5m", lookback_days: int = 5) -> pd.DataFrame:
    """
    Yahoo Finance fallback for Bank Nifty: ticker '^NSEBANK'
    Returns OHLCV with local timezone-aware Datetime column.
    """
    end = datetime.now()
    start = end - timedelta(days=lookback_days + 1)
    ticker = "^NSEBANK"  # Bank Nifty index
    df = yf.download(
        ticker,
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d"),
        interval=interval,
        progress=False,
        auto_adjust=False,
        threads=False,
    )
    if df.empty:
        raise RuntimeError("No data from Yahoo Finance.")
    df = df.rename(columns=str.title).reset_index()  # ensure 'Datetime'
    # Some intervals call the time column 'Datetime' already; ensure consistency:
    if "Datetime" not in df.columns:
        # e.g., daily can have 'Date'
        time_col = "Datetime" if "Datetime" in df.columns else "Date"
        df = df.rename(columns={time_col: "Datetime"})
    # Localize timezone
    if pd.api.types.is_datetime64_any_dtype(df["Datetime"]):
        if df["Datetime"].dt.tz is None:
            df["Datetime"] = df["Datetime"].dt.tz_localize(timezone.utc).dt.tz_convert(tz=None)
    return df[["Datetime", "Open", "High", "Low", "Close", "Volume"]].sort_values("Datetime").reset_index(drop=True)

def get_banknifty(interval: str, lookback_days: int):
    """
    Try NSE → fallback to Yahoo. Returns (df, source_name, error_message_if_any)
    """
    try:
        df = fetch_banknifty_from_nse(interval=interval, lookback_days=lookback_days)
        if len(df) >= 20:
            return df, "NSE", None
        else:
            raise RuntimeError("NSE returned too few rows; falling back.")
    except Exception as e:
        try:
            df = fetch_banknifty_from_yahoo(interval=interval, lookback_days=lookback_days)
            return df, "Yahoo", f"NSE fetch failed: {e}"
        except Exception as e2:
            return pd.DataFrame(), "None", f"NSE & Yahoo fetch failed: {e} | {e2}"

# -----------------------------
# Sidebar controls
# -----------------------------
with st.sidebar:
    st.header("⚙️ Controls")
    interval = st.selectbox(
        "Candle Interval",
        options=["1m", "5m", "15m", "30m", "60m", "1d"],
        index=1,
        help="NSE/Yahoo may not support all intervals at all times; fallback will apply.",
    )
    lookback_days = st.slider("Lookback (days)", min_value=1, max_value=60, value=5, step=1)
    rsi_period = st.number_input("RSI Period", min_value=5, max_value=50, value=14, step=1)
    bb_period = st.number_input("Bollinger Period", min_value=10, max_value=50, value=20, step=1)
    bb_std = st.number_input("Bollinger Std Dev", min_value=1.0, max_value=3.5, value=2.0, step=0.5)
    macd_fast = st.number_input("MACD Fast EMA", min_value=5, max_value=20, value=12, step=1)
    macd_slow = st.number_input("MACD Slow EMA", min_value=10, max_value=40, value=26, step=1)
    macd_signal = st.number_input("MACD Signal", min_value=5, max_value=20, value=9, step=1)
    rsi_buy = st.slider("RSI Buy Threshold", min_value=40, max_value=70, value=50, step=1)
    rsi_sell = st.slider("RSI Sell Threshold", min_value=30, max_value=60, value=50, step=1)
    auto_refresh_sec = st.number_input("Auto-Refresh (sec)", min_value=0, max_value=300, value=30, step=5,
                                       help="Set to 0 to disable auto-refresh.")
    st.caption("Tip: If data looks stale/empty at 1m, try 5m or 15m.")

# Optional auto-refresh
if auto_refresh_sec > 0:
    st.query_params(_ts=str(int(time.time())))  # bust cache for chart re-render
    st.autorefresh(interval=auto_refresh_sec * 1000, key="refresh_key")

# -----------------------------
# Fetch data
# -----------------------------
df, source, fetch_error = get_banknifty(interval=interval, lookback_days=lookback_days)
if fetch_error:
    st.info(fetch_error)

if df.empty:
    st.error("Unable to fetch Bank Nifty data from NSE or Yahoo. Try a different interval or increase lookback.")
    st.stop()

# -----------------------------
# Compute indicators
# -----------------------------
df["RSI"] = rsi(df["Close"], period=rsi_period)
macd_line, signal_line, macd_hist = macd(df["Close"], fast=macd_fast, slow=macd_slow, signal=macd_signal)
df["MACD"] = macd_line
df["MACD_Signal"] = signal_line
df["MACD_Hist"] = macd_hist
mid, upper, lower = bollinger(df["Close"], period=bb_period, stddev=bb_std)
df["BB_Mid"] = mid
df["BB_Upper"] = upper
df["BB_Lower"] = lower

# -----------------------------
# Signal logic
# -----------------------------
# Buy: MACD crosses above signal, RSI >= rsi_buy, Close > BB mid
# Sell: MACD crosses below signal, RSI <= rsi_sell, Close < BB mid
df["MACD_Cross_Up"] = (df["MACD"].shift(1) < df["MACD_Signal"].shift(1)) & (df["MACD"] >= df["MACD_Signal"])
df["MACD_Cross_Dn"] = (df["MACD"].shift(1) > df["MACD_Signal"].shift(1)) & (df["MACD"] <= df["MACD_Signal"])
df["Buy"]  = df["MACD_Cross_Up"] & (df["RSI"] >= rsi_buy) & (df["Close"] > df["BB_Mid"])
df["Sell"] = df["MACD_Cross_Dn"] & (df["RSI"] <= rsi_sell) & (df["Close"] < df["BB_Mid"])

latest = df.iloc[-1]
last_signal = None
if latest["Buy"]:
    last_signal = "BUY"
elif latest["Sell"]:
    last_signal = "SELL"
else:
    last_signal = "HOLD"

# -----------------------------
# Header metrics
# -----------------------------
colA, colB, colC, colD = st.columns(4)
with colA:
    st.metric("Source", source)
with colB:
    st.metric("Last Close", f"{latest['Close']:.2f}")
with colC:
    st.metric("RSI", f"{latest['RSI']:.1f}")
with colD:
    st.metric("Signal", last_signal)

# Alert toast if fresh signal occurred in the most recent bar
if df.iloc[-1]["Buy"]:
    st.toast("✅ New BUY signal generated on last candle.", icon="✅")
elif df.iloc[-1]["Sell"]:
    st.toast("⚠️ New SELL signal generated on last candle.", icon="⚠️")
else:
    st.toast("ℹ️ No new signal on the last candle.", icon="ℹ️")

st.caption(f"Data refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · Interval: {interval} · Lookback: {lookback_days}d")

# -----------------------------
# Charts (Plotly)
# -----------------------------
fig = make_subplots(
    rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06,
    row_heights=[0.65, 0.35],
    subplot_titles=("Bank Nifty — Candles + Bollinger", "MACD")
)

# Candlestick
fig.add_trace(
    go.Candlestick(
        x=df["Datetime"], open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
        name="OHLC"
    ),
    row=1, col=1
)

# Bollinger bands
fig.add_trace(go.Scatter(x=df["Datetime"], y=df["BB_Upper"], name="BB Upper", mode="lines"), row=1, col=1)
fig.add_trace(go.Scatter(x=df["Datetime"], y=df["BB_Mid"],   name="BB Mid",   mode="lines"), row=1, col=1)
fig.add_trace(go.Scatter(x=df["Datetime"], y=df["BB_Lower"], name="BB Lower", mode="lines"), row=1, col=1)

# Buy/Sell markers
buys = df[df["Buy"]]
sells = df[df["Sell"]]
fig.add_trace(go.Scatter(
    x=buys["Datetime"], y=buys["Close"], mode="markers", name="Buy",
    marker=dict(symbol="triangle-up", size=12)
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=sells["Datetime"], y=sells["Close"], mode="markers", name="Sell",
    marker=dict(symbol="triangle-down", size=12)
), row=1, col=1)

# MACD panel
fig.add_trace(go.Scatter(x=df["Datetime"], y=df["MACD"], name="MACD", mode="lines"), row=2, col=1)
fig.add_trace(go.Scatter(x=df["Datetime"], y=df["MACD_Signal"], name="Signal", mode="lines"), row=2, col=1)
fig.add_trace(
    go.Bar(x=df["Datetime"], y=df["MACD_Hist"], name="Histogram", opacity=0.5),
    row=2, col=1
)

fig.update_layout(
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis_rangeslider_visible=False
)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tabular view + latest suggestions
# -----------------------------
st.subheader("🔎 Latest Read")
col1, col2, col3 = st.columns(3)
with col1:
    st.write(f"**RSI({rsi_period})**: {latest['RSI']:.2f}")
with col2:
    st.write(f"**MACD({macd_fast},{macd_slow},{macd_signal})**: {latest['MACD']:.2f} vs Signal {latest['MACD_Signal']:.2f}")
with col3:
    st.write(f"**Bollinger({bb_period},{bb_std}) Mid**: {latest['BB_Mid']:.2f}")

st.write("— A **BUY** signal is when MACD crosses up, RSI ≥ threshold, and Close > BB mid.")
st.write("— A **SELL** signal is when MACD crosses down, RSI ≤ threshold, and Close < BB mid.")
st.caption("This is an educational tool. Not investment advice.")

# Optional raw table (last ~200 rows)
with st.expander("View recent data (last 200 rows)"):
    st.dataframe(df.tail(200), use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.caption(
    "Sources: NSE (primary) / Yahoo Finance (fallback). "
    "NSE may block or throttle automated requests; if so, the app falls back to Yahoo."
)
