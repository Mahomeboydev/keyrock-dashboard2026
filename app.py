# app.py - Debug & Fixed Version for Keyrock 2026 Dashboard

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import requests
from datetime import datetime

st.set_page_config(page_title="2026 Keyrock Metrics Dashboard", layout="wide")

st.title("Live Tracking: 12 Charts to Watch in 2026 (Debug & Fixed)")

st.write("**Debug Step 1:** Title loaded successfully. Script is running.")

if st.button("Manual Refresh (force rerun)"):
    st.rerun()

# Session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if time.time() - st.session_state.last_update > 600:
    st.session_state.last_update = time.time()
    st.rerun()

st.write("**Debug Step 2:** Session state block completed.")

# Minimal metrics list for debug (only 2; comment out fetches if needed)
metrics = [
    {
        "title": "1. Prediction Market Volumes by Market-Type",
        "description": "Weekly total prediction market trading volume (placeholder).",
        "goal": 25e9,
        "unit": "$B",
        "fetch_current": lambda: 5.0,  # simple placeholder
        "fetch_historical": lambda: pd.DataFrame({"Week": [1,2], "Value": [2.0, 4.0]})
    },
    {
        "title": "7. Solana MEV Extraction",
        "description": "Solana-based MEV (placeholder).",
        "goal": 5000,
        "unit": "SOL",
        "fetch_current": lambda: 1000.0,
        "fetch_historical": lambda: pd.DataFrame({"Week": [1,2], "Value": [500, 800]})
    },
    # Add the other 10 back one-by-one later once this works
]

st.write(f"**Debug Step 3:** Metrics list defined ({len(metrics)} items loaded).")

# Simple render loop
for i, metric in enumerate(metrics):
    st.subheader(metric["title"])
    st.write(metric["description"])

    current = metric["fetch_current"]()
    historical = metric["fetch_historical"]()

    progress = min(current / metric["goal"], 1.0) if metric["goal"] > 0 else 0
    st.progress(progress)
    st.write(f"Current: {current:,.2f} {metric['unit']} / Goal: {metric['goal']:,.2f} {metric['unit']} ({progress:.1%})")

    # Gauge with unique key
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=progress * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Progress"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "royalblue"}}))
    fig_gauge.update_layout(height=250)
    st.plotly_chart(fig_gauge, use_container_width=True, key=f"gauge_debug_{i}")

    # Line if historical
    if not historical.empty:
        fig_line = px.line(historical, x='Week', y='Value', title='Trend (Debug)')
        fig_line.update_layout(height=250)
        st.plotly_chart(fig_line, use_container_width=True, key=f"line_debug_{i}")

    st.markdown("---")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S AEDT')} | Debug mode (only 2 metrics). If you see this + 2 metrics, add the rest back gradually.")

st.write("**Debug Step 4:** End of script reached. If nothing above this line shows except title, crash happened between Step 3 and here.")