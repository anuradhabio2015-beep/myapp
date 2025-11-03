import calendar
from symtable import Symbol
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import pandas_ta as ta
import datetime
import plotly.graph_objects as go
import google.generativeai as genai
from nsepython import option_chain
import re

# ---------------- CACHE DATA ----------------
@st.cache_data
def get_price_and_delta(symbol):
    """Fetch the last traded price and daily delta"""
    try:
        ticker = yf.Ticker(symbol)
        data_hist = ticker.history(period="2d", interval="1d")
        data_live = ticker.history(period="1d", interval="1m")

        if data_hist.empty or data_live.empty:
            st.warning(f"Could not fetch live data for {symbol}.")
            if not data_hist.empty:
                return data_hist['Close'].iloc[-1], 0.0
            return 0.0, 0.0

        current_price = data_live['Close'].iloc[-1]
        previous_close = data_hist['Close'].iloc[0]
        delta = current_price - previous_close
        return current_price, delta
    except Exception as e:
        st.error(f"Error fetching price for {symbol}: {e}")
        return 0.0, 0.0


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Groww-style AI Trading Terminal", layout="wide")

# ---------------- SESSION INIT ----------------
if "config" not in st.session_state:
    st.session_state.config = {
        "gemini_api_key": "",
        "theme": "Dark",
        "ai_threshold": 50,
        "vix_threshold": 17,
        "pcr_threshold": 1.0,
        "expiry_date": datetime.date.today() + datetime.timedelta(days=7),
        "today_date": datetime.date.today(),
        "model_sentiment": "gemini-pro-latest",
        "model_signals": "gemini-flash-latest"
    }

if "data" not in st.session_state:
    st.session_state.data = None
    st.session_state.ai = 50
    st.session_state.vix = np.nan
    st.session_state.pcr = np.nan
    st.session_state.summary = "Run analysis to get AI insights."

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body { background: linear-gradient(145deg,#0e1117 0%,#131722 100%); color:#e0e0e0; font-family:'Poppins',sans-serif; }
[data-testid="stSidebar"] { background-color:#E5E7EB; }
.stTabs [role="tablist"] { border-bottom:1px solid #222; }
.stTabs [role="tab"] { background-color:transparent; color:#aaa; font-weight:600; }
.stTabs [aria-selected="true"] { color:#00b386; border-bottom:3px solid #00b386; }
.stButton>button { background-color:#00b386; color:white; border:none; border-radius:10px; padding:0.5rem 1rem; font-weight:600; }
.stButton>button:hover { background-color:#01d095; }
div[data-testid="stMetricValue"] { font-size:1.4rem; color:#00b386; }
[data-testid="stMetricLabel"] { color:#aaa; }
hr { border:0.5px solid #222; }
</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI CONFIG ----------------
def configure_genai():
    api_key = st.session_state.config.get("gemini_api_key")
    if not api_key:
        st.error("🚨 Please set your Gemini API Key in the 'Setting' tab!")
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"🚨 Failed to configure Gemini API: {e}")
        return False

# ---------------- AI FUNCTIONS ----------------
def ai_sentiment_score(symbol_name):
    try:
        model = genai.GenerativeModel(st.session_state.config["model_sentiment"])
        prompt = f"Rate investor sentiment for {symbol_name} (0=very bearish, 100=very bullish). Return only a number."
        resp = model.generate_content(prompt)
        score = int(''.join(filter(str.isdigit, resp.text or '50')) or 50)
        return max(0, min(score, 100))
    except Exception as e:
        st.warning(f"Gemini sentiment error: {e}")
        return 50

def ai_vix_estimate():
    try:
        model = genai.GenerativeModel(st.session_state.config["model_signals"])
        resp = model.generate_content("Give current estimated India VIX as a number only.")
        match = re.search(r"\d+(\.\d+)?", resp.text or "")
        return float(match.group()) if match else np.nan
    except Exception as e:
        st.warning(f"AI VIX error: {e}")
        return np.nan

# ---------------- MARKET DATA ----------------
def fetch_price(symbol, start, end):
    try:
        df = yf.download(symbol, start=start, end=end)
        if df.empty:
            st.warning("⚠️ No price data received from Yahoo Finance.")
            return pd.DataFrame()
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        st.warning(f"⚠️ Price fetch error: {e}")
        return pd.DataFrame()

def fetch_pcr(symbol="NIFTY"):
    try:
        data = option_chain(symbol)
        if not data or "records" not in data or "data" not in data["records"]:
            return np.nan
        records = data["records"]["data"]
        ce_oi = sum(r["CE"]["openInterest"] for r in records if "CE" in r)
        pe_oi = sum(r["PE"]["openInterest"] for r in records if "PE" in r)
        return round(pe_oi / ce_oi, 2) if ce_oi > 0 else np.nan
    except Exception:
        return np.nan

# ---------------- INDICATORS ----------------
def add_indicators(df):
    if df.empty:
        return df
    df["EMA20"] = ta.ema(df["Close"], length=20)
    df["RSI"] = ta.rsi(df["Close"], length=14)
    adx = ta.adx(df["High"], df["Low"], df["Close"], length=14)
    df["ADX"] = adx["ADX_14"] if adx is not None and "ADX_14" in adx else np.nan
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip('_') for col in df.columns.values]
    return df

# ---------------- SIGNAL ENGINE ----------------
def signal_logic(df, ai, vix, pcr):
    if df.empty:
        return df
    df = df.copy()
    df["signal"] = "HOLD"
    ai_t = st.session_state.config["ai_threshold"]
    vix_t = st.session_state.config["vix_threshold"]
    pcr_t = st.session_state.config["pcr_threshold"]

    df["EMA20"].fillna(method="ffill", inplace=True)
    df["RSI"].fillna(50, inplace=True)
    df["ADX"].fillna(20, inplace=True)
    ai = 50 if np.isnan(ai) else ai
    vix = 15 if np.isnan(vix) else vix
    pcr = 1.0 if np.isnan(pcr) else pcr

    for i in range(1, len(df)):
        close, ema, rsi, adx = df.loc[df.index[i], ["Close", "EMA20", "RSI", "ADX"]]
        if (
            (close > ema) and (rsi > 55) and (adx > 20) and
            (ai > ai_t + 5) and (pcr > pcr_t) and (vix < vix_t)
        ):
            df.at[df.index[i], "signal"] = "BUY"
        elif (
            (close < ema) and (rsi < 45) and (adx > 20) and
            (ai < ai_t - 5) and (pcr < pcr_t) and (vix > vix_t)
        ):
            df.at[df.index[i], "signal"] = "SELL"
    return df

# ---------------- ROBUST BACKTEST ----------------
def backtest(df):
    if df is None or df.empty or "Close" not in df.columns:
        return 0.0
    df = df.copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date").reset_index(drop=True)
        df.set_index("Date", inplace=True)
    pos_map = {"BUY": 1, "SELL": -1, "HOLD": 0}
    df["position"] = df["signal"].shift(1).map(pos_map).fillna(0)
    df["returns"] = df["Close"].pct_change().fillna(0)
    df["strategy"] = df["returns"] * df["position"]
    df["cum_strategy"] = (1 + df["strategy"]).cumprod()
    if df["cum_strategy"].empty:
        return 0.0
    return df["cum_strategy"].iloc[-1] - 1

# ---------------- SIDEBAR ----------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/f/fb/Groww_app_logo.png", width=120)
st.sidebar.title("Groww-style AI Trader 💹")

nse_indices = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "SENSEX": "^BSESN",
    "NIFTY IT": "^CNXIT",
    "NIFTY FMCG": "^CNXFMCG",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY AUTO": "^CNXAUTO",
    "NIFTY METAL": "^CNXMETAL",
}

nse_largecaps = {
    "Reliance Industries": "RELIANCE.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Infosys": "INFY.NS",
    "Tata Consultancy Services": "TCS.NS",
    "State Bank of India": "SBIN.NS",
}

category = st.sidebar.radio("Choose Category:", ["Indices", "Large Cap Stocks"], horizontal=True)
if category == "Indices":
    symbol_name = st.sidebar.selectbox("Select Index", list(nse_indices.keys()), index=0)
    symbol = nse_indices[symbol_name]
else:
    symbol_name = st.sidebar.selectbox("Select Stock", list(nse_largecaps.keys()), index=0)
    symbol = nse_largecaps[symbol_name]

st.sidebar.success(f"Selected: {symbol_name}")
st.sidebar.caption(f"Ticker: {symbol}")
start = st.sidebar.date_input("Start Date", datetime.date(2023, 1, 1))
end = st.sidebar.date_input("End Date", datetime.date.today())

if st.sidebar.button("🚀 Run Analysis"):
    with st.spinner("Fetching data and analyzing..."):
        if not configure_genai():
            st.stop()
        df = fetch_price(symbol, start, end)
        if df.empty:
            st.error("No price data.")
            st.stop()
        ai_score = ai_sentiment_score(symbol_name)
        vix = ai_vix_estimate()
        pcr = fetch_pcr("BANKNIFTY" if "BANK" in symbol_name.upper() else "NIFTY")
        df = add_indicators(df)
        df = signal_logic(df, ai_score, vix, pcr)
        st.session_state.data = df
        st.session_state.ai, st.session_state.vix, st.session_state.pcr = ai_score, vix, pcr
        st.session_state.summary = f"AI Report generated for {symbol_name} at {datetime.datetime.now().strftime('%H:%M:%S')}"

# ---------------- DASHBOARD ----------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Backtest", "🧠 AI Insights", "⚙️ Setting"])

# === TAB 1 ===
with tab1:
    current_price, price_delta = get_price_and_delta(symbol)
    st.subheader(f"Market Overview: {symbol_name}")
    st.metric(label=f"Current {symbol_name} Price", value=f"{current_price:,.2f}", delta=f"{price_delta:,.2f}")
    if st.session_state.data is not None and not st.session_state.data.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("AI Sentiment", f"{st.session_state.ai}/100")
        col2.metric("India VIX (Est.)", round(st.session_state.vix, 2) if not np.isnan(st.session_state.vix) else "N/A")
        col3.metric("PCR", st.session_state.pcr if not np.isnan(st.session_state.pcr) else "N/A")

        df = st.session_state.data
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name="Close", line=dict(width=2, color="#00b386")))
        fig.add_trace(go.Scatter(x=df["Date"], y=df["EMA20"], name="EMA20", line=dict(dash="dot", color="#888")))
        buy = df[df["signal"] == "BUY"]
        sell = df[df["signal"] == "SELL"]
        fig.add_trace(go.Scatter(x=buy["Date"], y=buy["Close"], mode="markers", name="BUY",
                                 marker_symbol="triangle-up", marker_color="#00ff99", marker_size=10))
        fig.add_trace(go.Scatter(x=sell["Date"], y=sell["Close"], mode="markers", name="SELL",
                                 marker_symbol="triangle-down", marker_color="#ff4c4c", marker_size=10))
        fig.update_layout(template="plotly_dark", title=f"{symbol_name} — Trading Signals")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Run analysis to load dashboard.")

# === TAB 2 (BACKTEST) ===
with tab2:
    if st.session_state.data is None or st.session_state.data.empty:
        st.info("Run analysis to backtest signals.")
    else:
        df_strategy = st.session_state.data.copy()
        df_strategy["Date"] = pd.to_datetime(df_strategy["Date"])
        df_strategy = df_strategy.sort_values("Date").reset_index(drop=True)
        df_strategy["returns"] = df_strategy["Close"].pct_change().fillna(0)
        df_strategy["position"] = df_strategy["signal"].shift(1).map({"BUY": 1, "SELL": -1, "HOLD": 0}).fillna(0)
        df_strategy["strategy"] = df_strategy["returns"] * df_strategy["position"]
        df_strategy["Strategy Returns"] = (1 + df_strategy["strategy"]).cumprod()
        df_strategy["Buy & Hold Returns"] = (1 + df_strategy["returns"]).cumprod()
        perf = backtest(df_strategy)
        st.metric("Backtest Cumulative Return", f"{perf*100:.2f}%")
        df_chart = df_strategy.set_index("Date")
        st.subheader("Strategy vs. Buy & Hold")
        st.line_chart(df_chart[["Strategy Returns", "Buy & Hold Returns"]])
        st.dataframe(df_strategy[["Date", "Close", "signal", "position", "Strategy Returns", "Buy & Hold Returns"]].tail(15))

# === TAB 3 ===
with tab3:
    st.subheader("🧠 AI Insights")
    st.markdown(st.session_state.summary)

# === TAB 4 ===
with tab4:
    st.subheader("⚙️ Configuration Panel")
    api_key = st.text_input("Gemini API Key", value=st.session_state.config["gemini_api_key"], type="password")
    ai_t = st.slider("AI Threshold", 0, 100, st.session_state.config["ai_threshold"])
    vix_t = st.slider("VIX Threshold", 0, 40, st.session_state.config["vix_threshold"])
    pcr_t = st.slider("PCR Threshold", 0.5, 2.0, st.session_state.config["pcr_threshold"], step=0.1)
    model_sentiment = st.text_input("Sentiment Model", st.session_state.config["model_sentiment"])
    model_signals = st.text_input("Signals Model", st.session_state.config["model_signals"])
    expiry_date_input = st.date_input("Expiry Date", value=st.session_state.config["expiry_date"])
    today_date_input = st.date_input("Today Date", value=st.session_state.config["today_date"])
    if st.button("💾 Save Settings"):
        st.session_state.config.update({
            "gemini_api_key": api_key,
            "ai_threshold": ai_t,
            "vix_threshold": vix_t,
            "pcr_threshold": pcr_t,
            "model_sentiment": model_sentiment,
            "model_signals": model_signals,
            "expiry_date": expiry_date_input,
            "today_date": today_date_input,
        })
        if configure_genai():
            st.success("Settings saved! New settings will apply on the next run.")
