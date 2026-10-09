import streamlit as st
from frontend.services.api_client import api_client
from frontend.components.charts import bar_chart

st.title("📊 Overview Dashboard")

try:
    summary = api_client.get_summary()
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Yield", f"{summary['average_yield']} t/ha")
    col2.metric("Total Production", f"{summary['total_production_tons']:,} t")
    col3.metric("Cultivated Area", f"{summary['total_cultivated_hectares']:,} ha")
except Exception as e:
    st.error(f"Error loading summary: {e}")

st.markdown("---")

st.subheader("Productivity by Crop")
try:
    crop_data = api_client.get_by_crop()
    fig = bar_chart(
        crop_data["data"],
        x="crop",
        y="average_yield",
        title="Average Yield by Crop (t/ha)",
    )
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Error loading crop data: {e}")