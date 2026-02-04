import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="2026 Keyrock Metrics Dashboard", layout="wide")

st.title("Live Tracking: 12 Charts to Watch in 2026")

st.write("All 12 metrics loaded with placeholder values + charts. If everything shows, we're ready for real APIs next.")

# ────────────────────────────────────────────────
# 12 Metrics with placeholder current values (real APIs later)
# ────────────────────────────────────────────────
metrics = [
    {"title": "1. Prediction Market Volumes by Market-Type", "description": "Weekly total prediction market trading volume, broken down by market type.", "goal": 25e9, "unit": "$B", "current": 4.8e9},
    {"title": "2. RWA Onchain Tokenisation AUM", "description": "Weekly total onchain RWA assets under management (excluding stablecoins).", "goal": 40e9, "unit": "$B", "current": 12.5e9},
    {"title": "3. x402 Volume", "description": "Weekly volume through x402 protocol for AI agents.", "goal": 100e6, "unit": "$M", "current": 8.2e6},
    {"title": "4. Onchain Vault AUM", "description": "AUM of onchain vault providers.", "goal": 36e9, "unit": "$B", "current": 14.1e9},
    {"title": "5. Onchain Perpetual Futures Open Interest", "description": "Total perpetual futures open interest.", "goal": 50e9, "unit": "$B", "current": 18.7e9},
    {"title": "6. Buyback Activity", "description": "Cumulative token buyback spend of top 10 programs.", "goal": 200e6, "unit": "$M", "current": 65e6},
    {"title": "7. Solana MEV Extraction", "description": "Solana-based MEV via validator and Jito tips.", "goal": 5000, "unit": "SOL", "current": 1450},
    {"title": "8. Shielded ZEC as Privacy Proxy", "description": "ZEC deposited to Zcash shielded pools.", "goal": 7e6, "unit": "ZEC", "current": 2.3e6},
    {"title": "9. Ethereum’s Blob Fee Floor", "description": "Median hourly blob cost.", "goal": 0.05, "unit": "$", "current": 0.018},
    {"title": "10. Crypto Cards Spend Volume", "description": "Monthly spend volume through crypto-linked cards.", "goal": 500e6, "unit": "$M", "current": 120e6},
    {"title": "11. Spot BTC ETF AUM", "description": "BTC held by US spot Bitcoin ETFs.", "goal": 2.5e6, "unit": "BTC", "current": 0.92e6},
    {"title": "12. Onchain Stablecoin Borrow Rates", "description": "Aave USDC variable borrow APY on Ethereum.", "goal": 5.0, "unit": "%", "current": 3.1},
]

# ────────────────────────────────────────────────
# Render all 12 metrics
# ────────────────────────────────────────────────
for i, metric in enumerate(metrics):
    st.subheader(metric["title"])
    st.write(metric["description"])

    progress = min(metric["current"] / metric["goal"], 1.0) if metric["goal"] > 0 else 0
    st.progress(progress)
    st.write(f"**Current:** {metric['current']:,.2f} {metric['unit']}  /  **Goal:** {metric['goal']:,.2f} {metric['unit']}  ({progress:.1%})")

    # Gauge chart
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=progress * 100,
        number={'suffix': '%'},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Progress to Goal"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "royalblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 100], 'color': "gray"}
            ]
        }
    ))
    fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True, key=f"gauge_{i}_{metric['title'][:15].replace(' ', '_')}")

    # Dummy line chart (replace with real history later)
    hist_df = pd.DataFrame({
        "Week": [1, 2, 3, 4],
        "Value": [metric["current"]*0.2, metric["current"]*0.5, metric["current"]*0.8, metric["current"]]
    })
    fig_line = px.line(hist_df, x="Week", y="Value", title="Dummy Weekly Trend")
    fig_line.update_layout(height=250)
    st.plotly_chart(fig_line, use_container_width=True, key=f"line_{i}_{metric['title'][:15].replace(' ', '_')}")

    st.markdown("---")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CET')} | Placeholder data – next step: real APIs")
st.write("If all 12 metrics + 12 gauges + 12 line charts are visible, reply 'all visible' and we add live data.")
