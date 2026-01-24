# app.py - Live Mock-Up: 12 Charts to Watch in 2026 (Keyrock Dashboard)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random  # For simulating live data fluctuations

# ────────────────────────────────────────────────
# Page Configuration
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="2026 Keyrock Metrics Dashboard",
    layout="wide"
)

st.title("Live Mock-Up: 12 Charts to Watch in 2026")

# ────────────────────────────────────────────────
# Auto-refresh simulation (every 30 seconds)
# ────────────────────────────────────────────────
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

if time.time() - st.session_state.last_update > 30:
    st.session_state.last_update = time.time()
    st.rerun()

# ────────────────────────────────────────────────
# Define the 12 metrics with starting values & goals
# ────────────────────────────────────────────────
metrics = [
    {
        "title": "1. Prediction Market Volumes by Market-Type",
        "description": "Weekly total prediction market trading volume, broken down by market type.",
        "current": random.uniform(0.5, 1.0) * 5e9,
        "goal": 25e9,           # $25B weekly
        "unit": "$B",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.1, 0.5)*5e9 for _ in range(52)]})
    },
    {
        "title": "2. RWA Onchain Tokenisation AUM",
        "description": "Weekly total onchain RWA assets under management (excluding stablecoins).",
        "current": random.uniform(0.5, 1.0) * 10e9,
        "goal": 4 * 10e9,       # >4x growth
        "unit": "$B",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.1, 0.5)*10e9 for _ in range(52)]})
    },
    {
        "title": "3. x402 Volume",
        "description": "Weekly volume through x402 protocol for AI agents.",
        "current": random.uniform(0.5, 1.0) * 10e6,
        "goal": 100e6,          # >$100M weekly
        "unit": "$M",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.1, 0.5)*10e6 for _ in range(52)]})
    },
    {
        "title": "4. Onchain Vault AUM",
        "description": "AUM of onchain vault providers.",
        "current": random.uniform(0.5, 1.0) * 11.84e9,
        "goal": 36e9,           # $36B
        "unit": "$B",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.1, 0.5)*11.84e9 for _ in range(52)]})
    },
    {
        "title": "5. Onchain Perpetual Futures Open Interest",
        "description": "Total perpetual futures open interest.",
        "current": random.uniform(0.5, 1.0) * 10e9,
        "goal": 50e9,           # >$50B
        "unit": "$B",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.1, 0.5)*10e9 for _ in range(52)]})
    },
    {
        "title": "6. Buyback Activity",
        "description": "Cumulative token buyback spend of top 10 programs.",
        "current": random.uniform(0.5, 1.0) * 100e6,
        "goal": 2 * 100e6,      # 2× 2025 weekly spend
        "unit": "$M",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.1, 0.5)*100e6 for _ in range(52)]})
    },
    {
        "title": "7. Solana MEV Extraction",
        "description": "Solana-based MEV via validator and Jito tips.",
        "current": random.uniform(0.5, 1.0) * 1000,
        "goal": 5000,
        "unit": "SOL",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.1, 0.5)*1000 for _ in range(52)]})
    },
    {
        "title": "8. Shielded ZEC as Privacy Proxy",
        "description": "ZEC deposited to Zcash shielded pools.",
        "current": random.uniform(0.5, 1.0) * 4.9e6,
        "goal": 7e6,            # >7M
        "unit": "ZEC",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.1, 0.5)*4.9e6 for _ in range(52)]})
    },
    {
        "title": "9. Ethereum’s Blob Fee Floor",
        "description": "Median hourly blob cost.",
        "current": random.uniform(0.01, 0.03),
        "goal": 0.05,           # ≥$0.05
        "unit": "$",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.001, 0.01) for _ in range(52)]})
    },
    {
        "title": "10. Crypto Cards Spend Volume",
        "description": "Monthly spend volume through crypto-linked cards.",
        "current": random.uniform(0.5, 1.0) * 106e6 / 4,  # weekly proxy
        "goal": 500e6,          # $500M monthly peak
        "unit": "$M",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.1, 0.5)*106e6 / 4 for _ in range(52)]})
    },
    {
        "title": "11. Spot BTC ETF AUM",
        "description": "BTC held by US spot Bitcoin ETFs.",
        "current": random.uniform(0.5, 1.0) * 1e6,
        "goal": 2.5e6,          # >2.5M BTC
        "unit": "BTC",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(0.1, 0.5)*1e6 for _ in range(52)]})
    },
    {
        "title": "12. Onchain Stablecoin Borrow Rates",
        "description": "Aave USDC variable borrow APY on Ethereum.",
        "current": random.uniform(2.0, 4.0),
        "goal": 5.0,
        "unit": "%",
        "historical": pd.DataFrame({"Week": range(1, 53), "Value": [random.uniform(1.0, 3.0) for _ in range(52)]})
    }
]

# ────────────────────────────────────────────────
# Simulate progress through the year
# ────────────────────────────────────────────────
if 'simulated_week' not in st.session_state:
    st.session_state.simulated_week = 3  # Start early in 2026

st.session_state.simulated_week = min(
    st.session_state.simulated_week + random.uniform(0.1, 0.5),
    52
)

for metric in metrics:
    progress_factor = st.session_state.simulated_week / 52
    metric['current'] = min(
        metric['current'] + (metric['goal'] * progress_factor * random.uniform(0.01, 0.05)),
        metric['goal']
    )
    metric['historical'].loc[:int(st.session_state.simulated_week), 'Value'] += random.uniform(0, metric['goal'] / 52)

# ────────────────────────────────────────────────
# Display each metric in its own tab
# ────────────────────────────────────────────────
tab_names = [m['title'] for m in metrics]
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs):
    with tab:
        metric = metrics[i]
        st.subheader(metric['title'])
        st.write(metric['description'])

        # Progress bar + text
        progress = metric['current'] / metric['goal']
        st.progress(progress)
        st.write(
            f"**Current:** {metric['current']:.2f} {metric['unit']}  "
            f" /  **Goal:** {metric['goal']:.2f} {metric['unit']}  "
            f"({progress:.1%} toward 2026 goal)"
        )

        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=progress * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Progress to Goal (%)"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 100], 'color': "gray"}
                ]
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Historical trend line chart
        hist_df = metric['historical'].iloc[:int(st.session_state.simulated_week) + 1]
        fig_line = px.line(
            hist_df,
            x='Week',
            y='Value',
            title='Weekly Trend (Simulated Live)'
        )
        fig_line.update_layout(height=300)
        st.plotly_chart(fig_line, use_container_width=True)

# Footer note
st.caption(
    "This is a simulated live mock-up. Values fluctuate randomly for demonstration purposes. "
    "For real data integration, connect to APIs such as CoinGecko, DefiLlama, Dune Analytics, etc."
)