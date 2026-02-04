import streamlit as st
from datetime import datetime

st.set_page_config(page_title="2026 Keyrock Metrics Dashboard", layout="wide")

st.title("Live Tracking: 12 Charts to Watch in 2026")

st.write("DEBUG: Structure test – metrics list & loop are running")

# Simple metrics (no lambdas, no APIs – just data)
metrics = [
    {"title": "1. Prediction Market Volumes by Market-Type", "description": "Weekly total prediction market trading volume.", "goal": 25e9, "unit": "$B", "current": 5.0},
    {"title": "2. RWA Onchain Tokenisation AUM", "description": "Weekly total onchain RWA AUM (excl. stablecoins).", "goal": 40e9, "unit": "$B", "current": 15.0},
    {"title": "7. Solana MEV Extraction", "description": "Solana-based MEV via validator and Jito tips.", "goal": 5000, "unit": "SOL", "current": 1000.0},
    # Add the other 9 manually when this works (copy from previous versions)
]

for i, metric in enumerate(metrics):
    st.subheader(metric["title"])
    st.write(metric["description"])
    
    progress = min(metric["current"] / metric["goal"], 1.0)
    st.progress(progress)
    st.write(f"Current: {metric['current']:,.2f} {metric['unit']} / Goal: {metric['goal']:,.2f} {metric['unit']} ({progress:.1%})")
    
    st.markdown("---")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CET')} | Structure only – no charts/APIs yet")
