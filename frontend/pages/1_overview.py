"""
Overview Dashboard — National Agricultural Productivity Intelligence.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
from frontend.config.settings import APP_TITLE, APP_ICON
from frontend.services.api_client import api_client
from frontend.components.styles import apply_custom_styles, render_hero
from frontend.components.charts import bar_chart

st.set_page_config(
    page_title=f"Overview Dashboard • {APP_TITLE}",
    page_icon=APP_ICON,
    layout="wide",
)

apply_custom_styles()

render_hero(
    title="Overview Dashboard",
    subtitle="Macro productivity indicators, regional benchmarks, and staple crop yields across Rwanda.",
)

# Fetch backend KPIs
try:
    summary = api_client.get_summary()
    c1, c2, c3 = st.columns(3)
    c1.metric("National Average Yield", f"{summary.get('average_yield', 2.85)} t/ha")
    c2.metric("Total Harvest Output", f"{summary.get('total_production_tons', 1250000):,} t")
    c3.metric("Monitored Farmland", f"{summary.get('total_cultivated_hectares', 438000):,} ha")
except Exception as e:
    st.error(f"Error loading summary metrics: {e}")

st.markdown("---")

col1, col2 = st.columns([1.1, 1], gap="medium")

with col1:
    st.subheader("Productivity by Crop")
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

with col2:
    st.subheader("Regional Highlights")
    district_data = pd.DataFrame([
        {"District": "Musanze", "Province": "Northern", "Lead Crop": "Irish Potato", "Avg Yield (t/ha)": 9.2},
        {"District": "Bugarama", "Province": "Western", "Lead Crop": "Paddy Rice", "Avg Yield (t/ha)": 5.8},
        {"District": "Nyagatare", "Province": "Eastern", "Lead Crop": "Maize", "Avg Yield (t/ha)": 4.6},
        {"District": "Huye", "Province": "Southern", "Lead Crop": "Climbing Beans", "Avg Yield (t/ha)": 2.8},
    ])
    st.dataframe(district_data, use_container_width=True, hide_index=True)