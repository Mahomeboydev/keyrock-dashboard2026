import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Keyrock Debug 2026", layout="wide")

st.title("Live Tracking: 12 Charts to Watch in 2026")

st.write("DEBUG STEP 1: Title rendered – script started")

st.write("DEBUG STEP 2: After first write – no crash yet")

if 'counter' not in st.session_state:
    st.session_state.counter = 0
st.session_state.counter += 1
st.write(f"DEBUG STEP 3: Session state works (counter = {st.session_state.counter})")

st.write("DEBUG STEP 4: About to show simple content")

st.header("Test Metric 1")
st.write("Goal: 25B $")
st.progress(0.20)
st.write("Current: 5.00 $B (20.0%) – placeholder")

st.markdown("---")

st.caption(f"Last visible update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CET')} | If you see this + the above, the crash was AFTER basic rendering.")

st.write("DEBUG STEP 5: End of script reached")
