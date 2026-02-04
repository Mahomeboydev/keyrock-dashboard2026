import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Keyrock Debug", layout="wide")

st.title("Live Tracking: 12 Charts to Watch in 2026")

st.markdown("**DEBUG: If you see this text, the script ran past st.title()**")

st.write("Step 1: Basic write works")

st.header("Test Section")
st.write("This is a placeholder metric")
st.progress(0.42)
st.write("Progress: 42% – if visible, rendering pipeline is OK")

st.caption(f"Debug timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CET')}")

st.write("End of debug script – if this line shows, add features back gradually")
