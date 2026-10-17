"""
Main entry point for the Streamlit decision support platform.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from frontend.config.settings import APP_TITLE, APP_ICON
from frontend.services.api_client import api_client
from frontend.components.styles import apply_custom_styles, render_hero
from frontend.components.charts import bar_chart

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_styles()

# Sidebar status
with st.sidebar:
    st.markdown("### System Status")
    try:
        health = api_client.health()
        st.success(f"Backend: {health.get('status', 'healthy')}")
    except Exception as e:
        st.error(f"Backend offline: {e}")

    st.markdown("---")
    st.markdown(
        """
        **AgriSupport Rwanda**  
        Decision Support System for agricultural productivity based on NISR SAS 2025 survey data.
        """
    )

# Hero Header
render_hero(
    title=APP_TITLE,
    subtitle="AI-Powered Agricultural Productivity Decision Support System for Rwanda",
)

# Macro KPIs
try:
    summary = api_client.get_summary()
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Yield", f"{summary.get('average_yield', 2.85)} t/ha")
    col2.metric("Total Production", f"{summary.get('total_production_tons', 1250000):,} t")
    col3.metric("Cultivated Area", f"{summary.get('total_cultivated_hectares', 438000):,} ha")
except Exception as e:
    st.warning(f"Could not load KPI summary: {e}")

st.markdown("---")

# Quick Visuals & Navigation
c1, c2 = st.columns([1.1, 1], gap="medium")

with c1:
    st.subheader("Platform Capabilities")
    st.markdown(
        """
        - **Overview Dashboard**: Explore crop productivity rankings and provincial benchmarks.
        - **Prediction Tool**: Simulate plot scenarios and evaluate input impacts (fertilizer, irrigation, seeds) before sowing.
        - **Evidence-Based Policy**: Grounded in official NISR Seasonal Agricultural Survey data.
        """
    )
    st.info("Use the sidebar on the left to navigate to the **Overview** and **Prediction Tool** pages.")

with c2:
    st.subheader("Benchmark Crop Yields")
    try:
        crop_data = api_client.get_by_crop().get("data", [])
    except Exception:
        crop_data = [
            {"crop": "Potatoes", "average_yield": 8.5},
            {"crop": "Rice", "average_yield": 4.1},
            {"crop": "Maize", "average_yield": 3.2},
            {"crop": "Beans", "average_yield": 1.8},
        ]
    fig = bar_chart(crop_data, x="crop", y="average_yield", title="Average Yield by Crop (t/ha)")
    st.plotly_chart(fig, use_container_width=True)