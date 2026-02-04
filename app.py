import streamlit as st
from datetime import datetime

# Add these imports at the top (required for charts)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Keyrock Debug", layout="wide")

st.title("Live Tracking: 12 Charts to Watch in 2026")

st.markdown("**DEBUG: Script ran past st.title()**")

st.write("Step 1: Basic write works")

st.header("Test Section")
st.write("This is a placeholder metric")
st.progress(0.42)
st.write("Progress: 42% – if visible, rendering pipeline is OK")

# Charts test – placed here so it runs after the progress bar
st.subheader("Charts Test – Should Appear Below")

# Dummy values
dummy_current = 5.0
dummy_goal = 25.0
progress = min(dummy_current / dummy_goal, 1.0)

# Gauge chart
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=progress * 100,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Progress Test (20 %)"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "royalblue"},
        'steps': [{'range': [0, 50], 'color': "lightgray"}, {'range': [50, 100], 'color': "gray"}]
    }
))
fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))

st.plotly_chart(fig_gauge, use_container_width=True, key="gauge_test_1")

# Line chart
hist_df = pd.DataFrame({
    "Week": [1, 2, 3],
    "Value": [1.0, 3.0, 5.0]
})
fig_line = px.line(hist_df, x="Week", y="Value", title="Dummy Trend (Test)")
fig_line.update_layout(height=250)

st.plotly_chart(fig_line, use_container_width=True, key="line_test_1")

st.write("→ If you see the circular gauge and line graph above this text, charts are working with unique keys!")

# Final lines (only once)
st.caption(f"Debug timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CET')}")
st.write("End of debug script – charts added successfully?")
