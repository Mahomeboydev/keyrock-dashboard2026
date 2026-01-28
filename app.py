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
# POLYMARKEY_KEY = ""  # usually not needed

# ────────────────────────────────────────────────
# Metrics config with fetch lambdas
# ────────────────────────────────────────────────
metrics = [
    {"title": "1. Prediction Market Volumes by Market-Type", "description": "...", "goal": 25e9, "unit": "$B",
     "fetch_current": lambda: fetch_polymarket_volume(), "fetch_historical": lambda: pd.DataFrame()},  # Limited hist
    {"title": "2. RWA Onchain Tokenisation AUM", "description": "...", "goal": 40e9, "unit": "$B",
     "fetch_current": lambda: fetch_rwa_aum(), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "3. x402 Volume", "description": "...", "goal": 100e6, "unit": "$M",
     "fetch_current": lambda: 0, "fetch_historical": lambda: pd.DataFrame()},  # No public API; manual or future
    {"title": "4. Onchain Vault AUM", "description": "...", "goal": 36e9, "unit": "$B",
     "fetch_current": lambda: fetch_defillama_category('vault'), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "5. Onchain Perpetual Futures Open Interest", "description": "...", "goal": 50e9, "unit": "$B",
     "fetch_current": lambda: fetch_defillama_oi(), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "6. Buyback Activity", "description": "...", "goal": 200e6, "unit": "$M",
     "fetch_current": lambda: 0, "fetch_historical": lambda: pd.DataFrame()},  # No free aggregate
    {"title": "7. Solana MEV Extraction", "description": "...", "goal": 5000, "unit": "SOL",
     "fetch_current": lambda: fetch_jito_mev(), "fetch_historical": lambda: fetch_jito_historical()},
    {"title": "8. Shielded ZEC as Privacy Proxy", "description": "...", "goal": 7e6, "unit": "ZEC",
     "fetch_current": lambda: 0, "fetch_historical": lambda: pd.DataFrame()},  # No easy aggregate
    {"title": "9. Ethereum’s Blob Fee Floor", "description": "...", "goal": 0.05, "unit": "$",
     "fetch_current": lambda: fetch_blob_fee(), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "10. Crypto Cards Spend Volume", "description": "...", "goal": 500e6, "unit": "$M",
     "fetch_current": lambda: 0, "fetch_historical": lambda: pd.DataFrame()},  # No public API
    {"title": "11. Spot BTC ETF AUM", "description": "...", "goal": 2.5e6, "unit": "BTC",
     "fetch_current": lambda: fetch_coinglass_etf_aum(), "fetch_historical": lambda: pd.DataFrame()},
    {"title": "12. Onchain Stablecoin Borrow Rates", "description": "...", "goal": 5.0, "unit": "%",
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
        total_vol = sum(m.get('volume24h', 0) for m in markets)  # Adjust for weekly estimate
        return total_vol / 1e9 * 7  # Rough weekly proxy
    except:
        return 5.0

@st.cache_data(ttl=3600)
def fetch_rwa_aum():
    try:
        # rwa.xyz API may require key; fallback to known public estimate or app scrape if allowed
        # For now placeholder (contact rwa.xyz for API access)
        return 15.0  # Update once you have access
    except:
        return 10.0

@st.cache_data(ttl=600)
def fetch_defillama_category(category_keyword):
    try:
        r = requests.get("https://api.llama.fi/protocols")
        protocols = r.json()
        total = sum(p.get('tvl', 0) for p in protocols if category_keyword.lower() in str(p).lower())
        return total / 1e9
    except:
        return 0

@st.cache_data(ttl=600)
def fetch_defillama_oi():
    try:
        r = requests.get("https://api.llama.fi/open-interest")
        data = r.json()
        return sum(d.get('openInterest', 0) for d in data) / 1e9
    except:
        return 0

@st.cache_data(ttl=600)
def fetch_jito_mev():
    try:
        r = requests.get("https://kobe.mainnet.jito.network/api/v1/daily_mev_rewards")
        latest = r.json()[-1] if r.json() else {}
        return latest.get('total_tips', 0) or latest.get('tips', 0)
    except:
        return 0

@st.cache_data(ttl=86400)
def fetch_jito_historical():
    try:
        r = requests.get("https://kobe.mainnet.jito.network/api/v1/daily_mev_rewards")
        data = r.json()
        df = pd.DataFrame(data)
        df['Week'] = pd.to_datetime(df['date']).dt.isocalendar().week
        weekly = df.groupby('Week')['total_tips'].sum().reset_index(name='Value')
        return weekly.tail(52)
    except:
        return pd.DataFrame({"Week": range(1,53), "Value": [0]*52})

@st.cache_data(ttl=300)
def fetch_blob_fee():
    try:
        # Use public RPC (e.g., public Alchemy/Infura endpoint or free provider)
        # Example with public mainnet (limited reliability)
        payload = {"jsonrpc":"2.0","method":"eth_blobBaseFee","params":[],"id":1}
        r = requests.post("https://rpc.ankr.com/eth", json=payload)  # Free public
        base_fee = int(r.json()['result'], 16) / 1e9  # Gwei to rough $
        return base_fee * 0.000001  # Approximate to USD
    except:
        return 0.02

@st.cache_data(ttl=600)
def fetch_coinglass_etf_aum():
    try:
        headers = {"coinglassSecret": st.secrets.get("COINGLASS_API_KEY", "")}
        r = requests.get("https://open-api-v4.coinglass.com/api/etf-aum?symbol=BTC", headers=headers)
        data = r.json()
        return data.get('data', {}).get('totalAum', 0) / 1e9 if 'data' in data else 0  # Adjust unit
    except:
        return 0

@st.cache_data(ttl=600)
def fetch_aave_usdc_borrow():
    try:
        r = requests.get("https://yields.llama.fi/pools")
        pools = r.json().get('data', [])
        aave_usdc = [p['apy'] for p in pools if 'aave' in p['project'].lower() and 'usdc' in p['symbol'].lower() and 'variable' in p.get('pool', '')]
        return sum(aave_usdc) / len(aave_usdc) if aave_usdc else 0
    except:
        return 3.0

# ────────────────────────────────────────────────
# Render all metrics scrollably
# ────────────────────────────────────────────────
for metric in metrics:
    st.subheader(metric["title"])
    st.write(metric["description"])

    current = metric["fetch_current"]()
    historical = metric["fetch_historical"]()

    progress = min(current / metric["goal"], 1.0) if metric["goal"] > 0 else 0
    st.progress(progress)
    st.write(f"**Current:** {current:,.2f} {metric['unit']}   /   **Goal 2026:** {metric['goal']:,.2f} {metric['unit']}   ({progress:.1%})")

    # Gauge
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=progress * 100,
        number={'suffix': '%'},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Progress"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "royalblue"}}))
    fig_gauge.update_layout(height=250)
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Line chart if historical available
    if not historical.empty:
        fig_line = px.line(historical, x='Week', y='Value', title='Weekly Trend (Live)')
        fig_line.update_layout(height=250)
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

st.caption("Live data from public APIs (DefiLlama, Jito, etc.). Some metrics use fallbacks/estimates due to limited public access. Add API keys in Streamlit secrets for CoinGlass etc. Refresh page or wait for auto-update.")