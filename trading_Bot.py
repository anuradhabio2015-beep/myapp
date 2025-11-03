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
# default_expiry = datetime.datetime.today

@st.cache_data  # Cache the data
def get_price_and_delta(symbol):
    """
    Fetches the last traded price and the delta (change from previous close).
    Returns:
        (float, float): A tuple of (current_price, delta)
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # 1. Get 2 days of *daily* data to find the previous close
        # data_hist.iloc[0] will be yesterday's close
        data_hist = ticker.history(period="2d", interval="1d")
        
        # 2. Get 1 day of *live* 1-minute data to find the current price
        data_live = ticker.history(period="1d", interval="1m")

        # Check if we got data (e.g., market might be closed)
        if data_hist.empty or data_live.empty:
            st.warning(f"Could not fetch live data for {symbol} (market likely closed).")
            # Fallback: return the last *daily* close and a 0 delta
            if not data_hist.empty:
                return data_hist['Close'].iloc[-1], 0.0
            else:
                return 0.0, 0.0 # Complete failure

        # --- Calculate ---
        
        # Get the *absolute last traded price* from 1-min data
        current_price = data_live['Close'].iloc[-1]
        
        # Get the *previous day's close* from daily data
        previous_close = data_hist['Close'].iloc[0]
        
        delta = current_price - previous_close
        
        return current_price, delta
        
    except Exception as e:
        st.error(f"Error fetching price for {symbol}: {e}")
        return 0.0, 0.0  # Return 0 for both values as a fallback


# ---------------- CONFIG ----------------
st.set_page_config(page_title="Groww-style AI Trading Terminal", layout="wide")

# ----------------
# Initialize session_state for config
# ----------------
if "config" not in st.session_state:
    st.session_state.config = {
        "gemini_api_key": "",
        "theme": "Dark",
        "ai_threshold": 50,
        "vix_threshold": 17,
        "pcr_threshold": 1.0,
        "expiry_date": datetime.date.today() + datetime.timedelta(days=7),
        "today_date": datetime.date.today() ,
        "model_sentiment": "gemini-pro-latest",
        # "model_sentiment": {print(Symbol.get_name)},
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
/* Style for AI report in tab3 */
.stTabs [data-testid="stMarkdownContainer"] h3 { color: #00b386; margin-top: 20px; }
.stTabs [data-testid="stMarkdownContainer"] strong { color: #01d095; }
</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI CONFIG ----------------
def configure_genai():
    """Helper function to configure GenAI with the key from session state."""
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
    """Get AI-based sentiment score (0-100) using Gemini Pro."""
    try:
        model_name = st.session_state.config["model_sentiment"]
        model = genai.GenerativeModel(model_name)
        prompt = (
            f"Rate the investor sentiment for {symbol_name} in the Indian stock market between 0 and 100. "
            f"0 means very bearish, 100 means very bullish. Only output the number."
        )
        resp = model.generate_content(prompt)
        score = int(''.join(filter(str.isdigit, resp.text or '50')) or 50)
        return max(0, min(score, 100))
    except Exception as e:
        st.warning(f"⚠️ Gemini sentiment error: {e}")
        return 50

def get_ai_detailed_report(symbol_name, current_price):
    """Get AI-based detailed financial report using the user's complex prompt."""
    
    price_scalar = current_price
    if isinstance(current_price, pd.Series):
        price_scalar = current_price.iloc[0]
    
    price_str = f"{price_scalar:,.0f}"
    
    expiry_date_obj = st.session_state.config["expiry_date"]
    today_date_obj = st.session_state.config["today_date"]
    
    expiry_date_str = expiry_date_obj.strftime('%B %d, %Y')
    today_date_str = today_date_obj.strftime('%B %d, %Y')
    
    prompt = f"""
    You are an expert financial analyst specializing in the Indian equity and derivatives markets, especially {symbol_name} options. 
    Now the {symbol_name} index stands at "{price_str}". 
    
    Before producing the report, perform a deep search using available tools (e.g., web searches, X (Twitter) searches for real-time sentiment, browsing financial websites for charts/data/news, and any other relevant sources) to gather the latest technical indicators, fundamental data, macroeconomic releases, FII/DII flows, sectoral news, RBI updates, geopolitical events, and option chain details (including Greeks and implied volatility). Use this deep search to inform a comprehensive analysis.

    Using a combination of:
    - Technical analysis (weekly candlestick patterns, moving average crossovers, RSI/Stochastics on the weekly chart, implied volatility expansions, option Greeks like delta/gamma for momentum, breakout signals, etc.)
    - Fundamental analysis (upcoming macroeconomic data releases, FII/DII weekly flow trends, sectoral earnings news, RBI policy hints)
    - Real-time news sentiment (domestic/international headlines, corporate announcements, RBI commentary, geopolitical developments)

    produce a short weekly report with probability estimates (in %) for where the {symbol_name} will close at the next weekly expiry—i.e., by {expiry_date_str}—in one of three scenarios:

    1. Upside (close above from ATM)
    2. Downside (close below from ATM)
    3. Flat (remain within ATM)

    Specifically:
    - Starting from the current index level of "{price_str}", calculate the probability (in percent) that {symbol_name} will finish the week higher, lower, or roughly flat.
    - Clearly state your key assumptions (e.g., “RSI oversold on the weekly chart suggests a 60% chance of rebound,” or “FII bought ₹1,200 cr in the past three sessions, indicating bullish bias”).

    Based on those probabilities, recommend which weekly option buying strategy is likely to yield the highest expected profit over this one week horizon:
    - Buying call options only
    - Buying put options only
    - Buying a long strangle (both calls and puts for volatility)

    For each strategy, estimate:
    - Expected return (%) for the week
    - Major risks (e.g., time decay erosion if no movement, volatility contraction from stable news)

    Assume:
    - You will take a high-risk approach.
    - You trade from the Wednesday open to the Tuesday close of the {symbol_name} weekly new expiry.
    - You will use the {expiry_date_str} weekly expiry.

    Finally, provide a concise “Actionable Summary”:
    - Should I buy a particular call strike, put strike, or both?
    - Which specific strike(s) would you choose if executing today {today_date_str}?
    - Approximately what premium (₹) and probability (%) does each recommended position carry?
    
    Format the entire response clearly using Markdown headings, bullet points, and bold text.
    """
    
    try:
        model_name = st.session_state.config["model_sentiment"]
        model = genai.GenerativeModel(model_name)
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        st.warning(f"⚠️ Gemini report error: {e}")
        return "Detailed AI report unavailable due to an error."


def ai_vix_estimate():
    """Estimate India VIX using Gemini Flash when real data unavailable."""
    try:
        model_name = st.session_state.config["model_signals"]
        model = genai.GenerativeModel(model_name)
        prompt = (
            "Give the current estimated India VIX (Volatility Index) value as a number only. "
            "If unavailable, estimate based on recent Indian market volatility."
        )
        resp = model.generate_content(prompt)
        match = re.search(r"\d+(\.\d+)?", resp.text or "")
        if match:
            return float(match.group())
        else:
            st.warning("⚠️ No valid numeric VIX found in AI response.")
            return np.nan
    except Exception as e:
        st.warning(f"⚠️ AI VIX error: {e}")
        return np.nan

# ---------------- MARKET DATA ----------------
def fetch_price(symbol, start, end):
    try:
        df = yf.download(symbol, start=start, end=end)
        if df is None or df.empty:
            st.warning("⚠️ No price data received from Yahoo Finance.")
            return pd.DataFrame()
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        st.warning(f"⚠️ Price fetch error: {e}")
        return pd.DataFrame()

def fetch_pcr(symbol="NIFTY"):
    """Fetch PCR with full safety."""
    try:
        data = option_chain(symbol)
        if not data or "records" not in data or "data" not in data["records"]:
            st.warning(f"⚠️ Invalid PCR data from NSE for {symbol}.")
            return np.nan
        records = data["records"]["data"]
        ce_oi = sum(row["CE"]["openInterest"] for row in records if "CE" in row)
        pe_oi = sum(row["PE"]["openInterest"] for row in records if "PE" in row)
        return round(pe_oi / ce_oi, 2) if ce_oi > 0 else np.nan
    except Exception as e:
        st.warning(f"⚠️ PCR fetch error for {symbol}: {e}")
        return np.nan

# ---------------- INDICATORS ----------------
def add_indicators(df):
    if df.empty:
        return df
    df["EMA20"] = ta.ema(df["Close"], length=20)
    df["RSI"] = ta.rsi(df["Close"], length=14)
    adx = ta.adx(df["High"], df["Low"], df["Close"], length=14)
    df["ADX"] = adx["ADX_14"] if adx is not None and "ADX_14" in adx else np.nan
    return df

# ---------------- SIGNAL ENGINE ----------------
def signal_logic(df, ai, vix, pcr):
    if df.empty:
        return df
    
    required_cols = ["Close", "EMA20", "RSI", "ADX"]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing column: {col}. Cannot generate signals.")
            return df

    df = df.copy() # Operate on a copy
    df["signal"] = "HOLD"
    
    ai_t = st.session_state.config["ai_threshold"]
    vix_t = st.session_state.config["vix_threshold"]
    pcr_t = st.session_state.config["pcr_threshold"]

    # Clean NaNs or None from indicators
    df["EMA20"] = df["EMA20"].fillna(method="bfill").fillna(method="ffill")
    df["RSI"] = df["RSI"].fillna(50)  # Neutral RSI
    df["ADX"] = df["ADX"].fillna(20)  # Neutral ADX

    # Handle NaNs in external factors
    ai = ai if not np.isnan(ai) else 50
    vix = vix if not np.isnan(vix) else 15 # Neutral VIX
    pcr = pcr if not np.isnan(pcr) else 1.0 # Neutral PCR

    for i in range(1, len(df)):
        try:
            close = float(df["Close"].iloc[i])
            ema = float(df["EMA20"].iloc[i])
            rsi = float(df["RSI"].iloc[i])
            adx = float(df["ADX"].iloc[i])
        except (ValueError, TypeError):
            continue  # Skip invalid rows

        buy = (
            (close > ema)
            and (rsi > 55)
            and (adx > 20)
            and (ai > ai_t + 5) # e.g., > 55
            and (pcr > pcr_t)   # e.g., > 1.0
            and (vix < vix_t)   # e.g., < 17
        )
        sell = (
            (close < ema)
            and (rsi < 45)
            and (adx > 20)
            and (ai < ai_t - 5) # e.g., < 45
            and (pcr < pcr_t)   # e.g., < 1.0
            and (vix > vix_t)   # e.g., > 17
        )

        if buy:
            df.at[df.index[i], "signal"] = "BUY"
        elif sell:
            df.at[df.index[i], "signal"] = "SELL"

    return df


def backtest(df):
    """Calculates cumulative return. Does NOT modify the input df."""
    if df.empty or "Close" not in df.columns:
        return 0
    
    df = df.copy() # Use a copy to avoid side effects
    
    df["returns"] = df["Close"].pct_change()
    df["position"] = df["signal"].shift(1).map({"BUY": 1, "SELL": -1}).fillna(0)
    df["strategy"] = df["returns"] * df["position"]
    
    return (1 + df["strategy"]).cumprod().iloc[-1] - 1

# ---------------- SIDEBAR ----------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/f/fb/Groww_app_logo.png", width=120)
st.sidebar.title("Groww-style AI Trader 💹")
# ---------------- SYMBOL SELECTION ----------------
st.sidebar.header("📈 Market Selection")

# Indices and Large-Cap Stock List
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

nse_indices_exp = {     
    "NIFTY 50": "NIFTY",
    "BANK NIFTY": "BANKNIFTY",
    "NIFTY IT": "NIFTYIT",
    "NIFTY PHARMA": "NIFTYPHARMA",
}

nse_largecaps = {
    "Reliance Industries": "RELIANCE.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Infosys": "INFY.NS",
    "Tata Consultancy Services": "TCS.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "State Bank of India": "SBIN.NS",
    "ITC Ltd": "ITC.NS",
    "Larsen & Toubro": "LT.NS",
    "Axis Bank": "AXISBANK.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Power Grid": "POWERGRID.NS",
    "NTPC Ltd": "NTPC.NS",
}

# Sidebar Group Toggle
category = st.sidebar.radio("Choose Category:", ["Indices", "Large Cap Stocks"], horizontal=True)


if category == "Indices":
    symbol_name = st.sidebar.selectbox("Select Index", list(nse_indices.keys()), index=0)
    symbol = nse_indices[symbol_name]
else:
    symbol_name = st.sidebar.selectbox("Select Stock", list(nse_largecaps.keys()), index=0)
    symbol = nse_largecaps[symbol_name]

# Display Selected Info
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
            st.error("Failed to fetch price data. Analysis stopped.")
            st.stop()
        
        current_price = df["Close"].iloc[-1]
        
        ai_score = ai_sentiment_score(symbol_name) 
        vix = ai_vix_estimate()
        
        pcr_symbol = "NIFTY"
        if "BANK NIFTY" in symbol_name.upper():
            pcr_symbol = "BANKNIFTY"
        pcr = fetch_pcr(pcr_symbol)
        
        df = add_indicators(df)
        df = signal_logic(df, ai_score, vix, pcr) 
        
        st.session_state.data = df
        st.session_state.ai, st.session_state.vix, st.session_state.pcr = ai_score, vix, pcr
        
        with st.spinner("🧠 Generating detailed AI report..."):
            st.session_state.summary = get_ai_detailed_report(symbol_name, current_price)

# ---------------- DASHBOARD ----------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Backtest", "🧠 AI Insights", "⚙️ Setting"])

with tab1:
    # Get the current price and use it as the default for a number_input
    current_price, price_delta = get_price_and_delta(symbol)
    st.subheader(f"Market Overview: {symbol_name}")
    st.metric(label= f"Current {symbol_name} Price", value=f"{current_price:,.2f}", delta=f"{price_delta:,.2f}" )
    # Define a global date variable
    # default_expiry = get_live_nearest_expiry({symbol})
    

    if st.session_state.data is not None and not st.session_state.data.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("AI Sentiment", f"{st.session_state.ai}/100")
        col2.metric("India VIX (Est.)", round(st.session_state.vix,2) if not np.isnan(st.session_state.vix) else "N/A")
        pcr_label = "PCR (BANKNIFTY)" if "BANK" in symbol_name.upper() else "PCR (NIFTY)"
        col3.metric(pcr_label, st.session_state.pcr if not np.isnan(st.session_state.pcr) else "N/A")

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
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0e1117", plot_bgcolor="#0e1117",
                          title=f"{symbol_name} — Trading Signals", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)
        
        display_cols = ["Date", "Close", "EMA20", "RSI", "ADX", "signal"]
        
        valid_display_cols = [col for col in display_cols if col in df.columns]
        df_display = df.tail(15)[valid_display_cols]
        
        st.dataframe(df_display.style.applymap(
            lambda val: 'color: #00ff99' if val == 'BUY' else ('color: #ff4c4c' if val == 'SELL' else ''), 
            subset=['signal']
        ).format(
            {"Close": "{:,.2f}", "EMA20": "{:,.2f}", "RSI": "{:.2f}", "ADX": "{:.2f}"}, 
            na_rep="-"
        ))
        
    else:
        st.info("Run analysis to load dashboard.")

# ----------------
# THIS TAB CONTAINS THE FIX
# ----------------
with tab2:
    if st.session_state.data is not None and not st.session_state.data.empty:
        perf = backtest(st.session_state.data)
        st.metric("Backtest Cumulative Return", f"{perf*100:.2f}%")
        
        df_strategy = st.session_state.data.copy()
        
        if 'Date' not in df_strategy.columns:
            st.error("Critical Error: 'Date' column is missing from data.")
        else:
            df_strategy['Date'] = pd.to_datetime(df_strategy['Date'])

            df_strategy["returns"] = df_strategy["Close"].pct_change()
            df_strategy["position"] = df_strategy["signal"].shift(1).map({"BUY": 1, "SELL": -1}).fillna(0)
            df_strategy["strategy"] = df_strategy["returns"] * df_strategy["position"]
            
            df_strategy["Strategy Returns"] = (1 + df_strategy["strategy"].fillna(0)).cumprod()
            df_strategy["Buy & Hold Returns"] = (1 + df_strategy["returns"].fillna(0)).cumprod()
            
            st.subheader("Strategy vs. Buy & Hold")
            
            # ----------------
            # FIX for KeyError:
            # Set 'Date' as the index, then pass the DataFrame and *explicitly*
            # tell line_chart which columns to use for the 'y' axis.
            # ----------------
            
            df_chart = df_strategy.set_index('Date')
            
            # Add this debug line before the error:
            st.write("Inspecting df_chart columns:", df_chart.columns)

            if 'Date' in df_chart.columns:
                df_chart = df_chart.set_index('Date')
            elif 'date' in df_chart.columns: # Or check for lowercase
                df_chart = df_chart.set_index('date')

                # --- Add this code to fix your columns ---

                # This flattens the MultiIndex tuples into single string names.
                # e.g., ('Strategy Returns', '') becomes 'Strategy Returns'
                # e.g., ('Close', '^NSEI') becomes 'Close_^NSEI'
                df_chart.columns = ['_'.join(col).strip('_') for col in df_chart.columns.values]

                # (Optional) You can uncomment this to see the new, flattened column names
                # st.write("New columns:", df_chart.columns)

                # --- Your corrected plot call ---

                # Now, use the *correct* capitalized names with spaces
                st.line_chart(df_chart, y=["Strategy Returns", "Buy & Hold Returns"])
            
    else:
        st.info("Run analysis to backtest signals.")


with tab3:
    st.subheader("🧠 AI-Generated Financial Report")
    if "summary" in st.session_state and st.session_state.summary != "Run analysis to get AI insights.":
        st.markdown(st.session_state.summary)
    else:
        st.info("Run analysis to get AI insights.")

with tab4:
    st.subheader("⚙️ Configuration Panel")
    
    api_key = st.text_input(
        "Gemini API Key", 
        value=st.session_state.config["gemini_api_key"], 
        type="password",
        help="Get your API key from Google AI Studio."
    )
    
    theme_choice = st.selectbox(
        "Theme (CSS is hardcoded, this is a placeholder)", 
        ["Dark"], 
        index=0
    ) 
    
    st.subheader("Signal Logic Thresholds")
    ai_t = st.slider("AI Sentiment Threshold", 0, 100, st.session_state.config["ai_threshold"])
    vix_t = st.slider("VIX Threshold", 0, 40, st.session_state.config["vix_threshold"])
    pcr_t = st.slider("PCR Threshold", 0.5, 2.0, st.session_state.config["pcr_threshold"], step=0.1)

    st.subheader("AI Model & Date Settings")
    model_sentiment = st.text_input("Sentiment Model", st.session_state.config["model_sentiment"])
    model_signals = st.text_input("Signals/VIX Model", st.session_state.config["model_signals"])
    
 

    expiry_date_input = st.date_input(
        "Expiry Date (for AI prompt)", 
        value=st.session_state.config["expiry_date"]
    )
    today_date_input = st.date_input(
        "Today Date (for AI prompt)", 
        value=st.session_state.config["today_date"]
    )


    if st.button("💾 Save Settings"):
        st.session_state.config.update({
            "gemini_api_key": api_key,
            "theme": theme_choice,
            "ai_threshold": ai_t,
            "vix_threshold": vix_t,
            "pcr_threshold": pcr_t,
            "model_sentiment": model_sentiment,
            "model_signals": model_signals,
            "expiry_date": expiry_date_input, 
            "today_date": today_date_input,   
        })
        
        if configure_genai():
            st.success("Settings saved! New settings will apply on the next 'Run Analysis'.")
        else:
            st.warning("Settings saved, but the API key could not be configured. Please check it.")
