# dashboard.py
import streamlit as st
import pandas as pd
from binance.client import Client
from streamlit_autorefresh import st_autorefresh
import os

# --- AUTO REFRESH EVERY 5 SECONDS ---
st_autorefresh(interval=5000, key="crypto_refresh")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Live BTC Dashboard", layout="wide")

# --- DARK THEME STYLING ---
st.markdown(
    """
    <style>
    body {background-color: #0E1117; color: #FFFFFF;}
    .stMetric {background-color: #1F222A; border-radius: 10px; padding: 15px;}
    .stText {color: #FFFFFF;}
    </style>
    """,
    unsafe_allow_html=True
)

# --- LOAD BINANCE API KEYS FROM ENVIRONMENT ---
api_key = os.environ.get("BINANCE_API_KEY")
api_secret = os.environ.get("BINANCE_API_SECRET")

if not api_key or not api_secret:
    st.error("API Key or Secret is missing! Add them in Streamlit Cloud Secrets.")
    st.stop()

# --- INITIALIZE BINANCE CLIENT ---
try:
    client = Client(api_key, api_secret)
    client.ping()  # Test connection
except Exception as e:
    st.error(f"Failed to connect to Binance API: {e}")
    st.stop()

# --- FUNCTION TO FETCH LIVE BTC DATA ---
def get_btc_data():
    try:
        ticker_24h = client.get_ticker_24hr(symbol="BTCUSDT")
        ticker_now = client.get_symbol_ticker(symbol="BTCUSDT")
        return {
            "Price": float(ticker_now['price']),
            "24h High": float(ticker_24h['highPrice']),
            "24h Low": float(ticker_24h['lowPrice']),
            "24h Change %": float(ticker_24h['priceChangePercent'])
        }
    except Exception as e:
        st.warning(f"Error fetching data: {e}")
        return None

btc_data = get_btc_data()

# --- DISPLAY DASHBOARD ---
if btc_data:
    st.title("🚀 Live BTC Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Price (USDT)", f"${btc_data['Price']:.2f}")
    
    col2.metric("24h High", f"${btc_data['24h High']:.2f}")
    
    col3.metric("24h Low", f"${btc_data['24h Low']:.2f}")
    
    # Change % with color indicator
    change_val = btc_data['24h Change %']
    change_color = "green" if change_val >= 0 else "red"
    col4.markdown(
        f"<div class='stMetric'><h3 style='color:{change_color};'>{change_val:.2f}%</h3></div>",
        unsafe_allow_html=True
    )
else:
    st.warning("Could not load BTC data.")
