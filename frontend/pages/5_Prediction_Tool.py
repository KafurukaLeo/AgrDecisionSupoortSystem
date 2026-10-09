import streamlit as st
from frontend.services.api_client import api_client

st.title("🔮 Prediction Tool")
st.caption("Predict agricultural productivity for a specific scenario.")

# Load filter options
try:
    options = api_client.get_filter_options()
except Exception as e:
    st.error(f"Could not load filter options: {e}")
    st.stop()

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        crop = st.selectbox("Crop", options["crops"])
        season = st.selectbox("Season", options["seasons"])
        district = st.selectbox("District", options["districts"])
    with col2:
        year = st.selectbox("Year", options["years"])
        cultivated_area = st.number_input("Cultivated Area (ha)", min_value=0.1, value=2.0)
    col3, col4 = st.columns(2)
    with col3:
        fertilizer = st.checkbox("Fertilizer Used")
    with col4:
        irrigation = st.checkbox("Irrigation Used")

    submitted = st.form_submit_button("Predict Productivity")

if submitted:
    payload = {
        "crop": crop,
        "season": season,
        "district": district,
        "year": year,
        "fertilizer_used": fertilizer,
        "irrigation_used": irrigation,
        "cultivated_area": cultivated_area,
    }
    try:
        result = api_client.predict(payload)
        st.success(f"Predicted Yield: **{result['predicted_yield']} {result['unit']}**")
        st.write(f"Confidence Interval: {result['confidence_interval']}")
        st.caption(f"Model version: {result['model_version']}")
        st.warning(result["disclaimer"])
    except Exception as e:
        st.error(f"Prediction failed: {e}")