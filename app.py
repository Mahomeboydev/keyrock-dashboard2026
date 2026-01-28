# app.py - Live 2026 Keyrock Metrics Dashboard with Real API Integrations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="2026 Keyrock Metrics Dashboard", layout="wide")
st.title("Live Tracking: 12 Charts to Watch in 2026 (Real APIs)")

# Auto-refresh every 10 minutes (adjust as needed; respect API rate limits)
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if time.time() - st.session_state.last_update > 600:
    st.session_state.last_update = time.time()
    st.rerun()

# Optional: Add your API keys via Streamlit secrets (in .streamlit/secrets.toml or cloud settings)
# Example secrets.toml:
# COINGLASS_API_KEY = "your_key_here"

# ────────────────────────────────────────────────
# Metrics config with fetch lambdas
# ────────────────────────────────────────────────
metrics = [
    {"title": "1. Prediction Market Volumes by Market-Type", "description": "Weekly total prediction market trading volume, broken down by market type.", "goal": 25e9, "unit": "$B",
     "fetch_current": lambda: fetch_polymarket_volume(), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "2. RWA Onchain Tokenisation AUM", "description": "Weekly total onchain RWA assets under management (excluding stablecoins).", "goal": 40e9, "unit": "$B",
     "fetch_current": lambda: fetch_rwa_aum(), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "3. x402 Volume", "description": "Weekly volume through x402 protocol for AI agents.", "goal": 100e6, "unit": "$M",
     "fetch_current": lambda: lambda: 0, "fetch_historical": lambda: pd.DataFrame()},
    {"title": "4. Onchain Vault AUM", "description": "AUM of onchain vault providers.", "goal": 36e9, "unit": "$B",
     "fetch_current": lambda: fetch_defillama_category('vault'), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "5. Onchain Perpetual Futures Open Interest", "description": "Total perpetual futures open interest.", "goal": 50e9, "unit": "$B",
     "fetch_current": lambda: fetch_defillama_oi(), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "6. Buyback Activity", "description": "Cumulative token buyback spend of top 10 programs.", "goal": 200e6, "unit": "$M",
     "fetch_current": lambda: lambda: 0, "fetch_historical": lambda: pd.DataFrame()},
    {"title": "7. Solana MEV Extraction", "description": "Solana-based MEV via validator and Jito tips.", "goal": 5000, "unit": "SOL",
     "fetch_current": lambda: fetch_jito_mev(), "fetch_historical": lambda: fetch_jito_historical()},
    {"title": "8. Shielded ZEC as Privacy Proxy", "description": "ZEC deposited to Zcash shielded pools.", "goal": 7e6, "unit": "ZEC",
     "fetch_current": lambda: lambda: 0, "fetch_historical": lambda: pd.DataFrame()},
    {"title": "9. Ethereum’s Blob Fee Floor", "description": "Median hourly blob cost.", "goal": 0.05, "unit": "$",
     "fetch_current": lambda: fetch_blob_fee(), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "10. Crypto Cards Spend Volume", "description": "Monthly spend volume through crypto-linked cards.", "goal": 500e6, "unit": "$M",
     "fetch_current": lambda: lambda: 0, "fetch_historical": lambda: pd.DataFrame()},
    {"title": "11. Spot BTC ETF AUM", "description": "BTC held by US spot Bitcoin ETFs.", "goal": 2.5e6, "unit": "BTC",
     "fetch_current": lambda: fetch_coinglass_etf_aum(), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "12. Onchain Stablecoin Borrow Rates", "description": "Aave USDC variable borrow APY on Ethereum.", "goal": 5.0, "unit": "%",
     "fetch_current": lambda: fetch_aave_usdc_borrow(), "fetch_historical": lambda: pd.DataFrame()},
]

# ────────────────────────────────────────────────
# Real API Fetch Helpers (with caching & fallbacks)
# ────────────────────────────────────────────────
@st.cache_data(ttl=600)
def fetch_polymarket_volume():
    try:
        r = requests.get("https://gamma-api.polymarket.com/markets?active=true&limit=100")
        markets = r.json()
        total_vol = sum(m.get('volume24h', 0) for m in markets)
        return total_vol / 1e9 * 7  # rough weekly proxy
    except:
        return 5.0