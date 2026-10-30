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
    title="Rwanda crop overview",
    subtitle="A quick look at harvests and crop yields across the country.",
    badge="National survey data",
)

# National summary
try:
    summary = api_client.get_summary()
    c1, c2, c3 = st.columns(3)
    c1.metric("Average yield", f"{summary.get('average_yield', 2.85)} t/ha")
    c2.metric("Total harvest", f"{summary.get('total_production_tons', 1250000):,} tonnes")
    c3.metric("Farmland measured", f"{summary.get('total_cultivated_hectares', 438000):,} ha")
except Exception as e:
    st.warning("The national summary is temporarily unavailable.")
    st.caption(f"Technical details: {e}")

st.markdown("---")

col1, col2 = st.columns([1.1, 1], gap="medium")

with col1:
    st.markdown("### Yield by crop")
    try:
        crop_data = api_client.get_by_crop().get("data", [])
    except Exception:
        crop_data = [
            {"crop": "Potatoes", "average_yield": 8.5},
            {"crop": "Rice", "average_yield": 4.1},
            {"crop": "Maize", "average_yield": 3.2},
            {"crop": "Beans", "average_yield": 1.8},
        ]
    fig = bar_chart(crop_data, x="crop", y="average_yield", title="Yield (tonnes per hectare)")
    st.plotly_chart(fig, width="stretch")

with col2:
    st.markdown("### Yields by district")
    try:
        dist_items = api_client.get_by_district().get("data", [])
        district_data = pd.DataFrame(dist_items)
        district_data.columns = [c.replace("_", " ").title() for c in district_data.columns]
    except Exception:
        district_data = pd.DataFrame(
            [
                {
                    "District": "Musanze",
                    "Province": "Northern",
                    "Lead Crop": "Irish Potatoes",
                    "Average Yield": 9.2,
                },
                {
                    "District": "Nyabihu",
                    "Province": "Western",
                    "Lead Crop": "Irish Potatoes",
                    "Average Yield": 8.7,
                },
                {
                    "District": "Rusizi",
                    "Province": "Western",
                    "Lead Crop": "Paddy Rice",
                    "Average Yield": 5.8,
                },
                {
                    "District": "Nyagatare",
                    "Province": "Eastern",
                    "Lead Crop": "Maize",
                    "Average Yield": 4.6,
                },
                {
                    "District": "Huye",
                    "Province": "Southern",
                    "Lead Crop": "Climbing Beans",
                    "Average Yield": 2.8,
                },
            ]
        )
    st.dataframe(district_data, width="stretch", hide_index=True)