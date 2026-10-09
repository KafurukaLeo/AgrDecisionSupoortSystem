"""
Main Streamlit entry point.
"""
import streamlit as st
from frontend.config.settings import APP_TITLE, APP_ICON
from frontend.services.api_client import api_client

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title(f"{APP_ICON} {APP_TITLE}")
st.caption("AI-Powered Agricultural Productivity Decision Support System for Rwanda")

st.markdown("---")

# Backend health check
with st.sidebar:
    st.header("System Status")
    try:
        health = api_client.health()
        st.success(f"Backend: {health['status']}")
    except Exception as e:
        st.error(f"Backend unreachable: {e}")

st.markdown(
    """
    ### Welcome

    Use the sidebar to navigate through the dashboard:

    - **Overview** — Key productivity indicators
    - **Productivity Analysis** — Explore by crop, season, location
    - **Geographic Comparison** — Compare districts
    - **Inputs & Practices** — Fertilizer, irrigation, and practices
    - **Prediction Tool** — Predict productivity for a scenario
    - **Model Performance** — How accurate is the model?
    - **About** — Data source and methodology
    """
)

# Quick overview
st.subheader("Quick Overview")
try:
    summary = api_client.get_summary()
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Yield", f"{summary['average_yield']} t/ha")
    col2.metric("Total Production", f"{summary['total_production_tons']:,} t")
    col3.metric("Cultivated Area", f"{summary['total_cultivated_hectares']:,} ha")
    st.info(summary.get("note", ""))
except Exception as e:
    st.warning(f"Could not load summary: {e}")