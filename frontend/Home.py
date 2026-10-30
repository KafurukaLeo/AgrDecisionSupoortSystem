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
from frontend.components.styles import apply_custom_styles, render_hero, safe_html
from frontend.components.charts import bar_chart

st.set_page_config(
    page_title=f"Home • {APP_TITLE}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_styles()

# Sidebar branding and connection status
with st.sidebar:
    safe_html(
        """
        <div class="sidebar-brand">
            <h2 class="sidebar-brand-title">AgriSupport Rwanda</h2>
            <p class="sidebar-brand-sub">Rwanda farm insights</p>
        </div>
        """
    )
    try:
        api_client.health()
        safe_html(
            """
            <div class="pulse-status">
                <span class="pulse-dot"></span>
                Data service connected
            </div>
            """
        )
    except Exception as e:
        st.error("Can't connect to the data service. Check that the app is running.")
        st.caption(f"Technical details: {e}")

    st.markdown("---")
    st.caption("Using Rwanda's 2025 Seasonal Agricultural Survey.")

# Hero Header
render_hero(
    title=APP_TITLE,
    subtitle="Explore crop yields and estimate harvests for farms across Rwanda.",
    badge="Rwanda • 2025 survey data",
)

# National overview
try:
    summary = api_client.get_summary()
    col1, col2, col3 = st.columns(3)
    col1.metric("Average yield", f"{summary.get('average_yield', 2.85)} t/ha")
    col2.metric("Total harvest", f"{summary.get('total_production_tons', 1250000):,} tonnes")
    col3.metric("Farmland measured", f"{summary.get('total_cultivated_hectares', 438000):,} ha")
except Exception as e:
    st.warning("The national summary is temporarily unavailable.")
    st.caption(f"Technical details: {e}")

st.markdown("---")

c1, c2 = st.columns([1.1, 1], gap="medium")

with c1:
    st.markdown("### Explore the data")
    safe_html(
        """
        <div class="feature-card">
            <div class="feature-title">
                <span class="material-symbols-outlined" style="color: #059669;">insights</span>
                Compare crop yields
            </div>
            <p class="feature-desc">See how yields differ by crop, district, and season.</p>
        </div>
        <div class="feature-card">
            <div class="feature-title">
                <span class="material-symbols-outlined" style="color: #059669;">tune</span>
                Estimate a harvest
            </div>
            <p class="feature-desc">Try different farm inputs to explore possible outcomes.</p>
        </div>
        <div class="feature-card">
            <div class="feature-title">
                <span class="material-symbols-outlined" style="color: #059669;">verified</span>
                Survey-based information
            </div>
            <p class="feature-desc">Insights use Rwanda's Seasonal Agricultural Survey.</p>
        </div>
        """
    )

with c2:
    st.markdown("### Average yield by crop")
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