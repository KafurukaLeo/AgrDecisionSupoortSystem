import streamlit as st
from frontend.services.api_client import api_client

st.title(":material/online_prediction: Prediction Tool")
st.caption(
    "Predict agricultural productivity for a specific scenario. "
    "Powered by a Random Forest model trained on NISR SAS 2025 data."
)

# Load filter options from the API
try:
    options = api_client.get_filter_options()
except Exception as e:
    st.error(f"Could not load filter options: {e}")
    st.stop()

# Check whether the trained model is available on the server
try:
    _status = api_client.get_prediction_status()
    model_ready = bool(_status.get("model_loaded") and _status.get("encoders_loaded"))
except Exception:
    model_ready = False

if not model_ready:
    st.warning(
        "The prediction model is not installed on the server yet. "
        "You can fill in the form, but predictions will be unavailable until the "
        "trained model files (model.pkl and label_encoders.pkl) are added to "
        "backend/app/ml/artifacts/."
    )

with st.form("prediction_form"):
    st.subheader("Scenario")

    col1, col2, col3 = st.columns(3)
    with col1:
        crop = st.selectbox("Crop", options["crops"])
        season = st.selectbox("Season", options["seasons"])
        province = st.selectbox("Province", options["provinces"])
    with col2:
        district = st.selectbox("District", options["districts"])
        stratum = st.selectbox(
            "Land type",
            [
                "Agricultural land on hillside",
                "Agricultural land in marshland",
                "Rangeland",
                "Mixed",
                "Large Scale Farmer",
            ],
        )
        farmer_gender = st.selectbox("Farmer gender", ["Male", "Female"])
    with col3:
        plot_area_ha = st.number_input("Plot area (ha)", min_value=0.1, value=1.0)
        crop_area_ha = st.number_input("Crop area (ha)", min_value=0.1, value=1.0)
        farmer_age = st.number_input("Farmer age", min_value=15, max_value=100, value=40)

    st.subheader("Inputs & Practices")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        fertilizer = st.checkbox("Fertilizer used")
        irrigation = st.checkbox("Irrigation used")
    with c2:
        pesticide = st.checkbox("Pesticide used")
        improved_seeds = st.checkbox("Improved seeds")
    with c3:
        anti_erosion = st.checkbox("Anti-erosion")
        organic_fert = st.checkbox("Organic fertilizer")
    with c4:
        inorganic_fert = st.checkbox("Inorganic fertilizer")
        plot_irrigated = st.checkbox("Plot irrigated this season")

    submitted = st.form_submit_button(
        "Predict Productivity", type="primary", disabled=not model_ready
    )

if submitted:
    payload = {
        "crop": crop,
        "crop_category": "Cereal",
        "season": season,
        "province": province,
        "district": district,
        "stratum": stratum,
        "farmer_gender": farmer_gender,
        "land_use": "Agricultural land on hillside",
        "cropping_system": "Pure Cropping",
        "plot_area_ha": float(plot_area_ha),
        "crop_area_ha": float(crop_area_ha),
        "harvest_ratio": 100.0,
        "farmer_age": int(farmer_age),
        "fertilizer_used": bool(fertilizer),
        "irrigation_used": bool(irrigation),
        "pesticide_used": bool(pesticide),
        "improved_seeds_used": bool(improved_seeds),
        "anti_erosion_activity": bool(anti_erosion),
        "organic_fertilizer_used": bool(organic_fert),
        "inorganic_fertilizer_used": bool(inorganic_fert),
        "irrigation_practiced": bool(irrigation),
        "plot_irrigated": bool(plot_irrigated),
    }

    with st.spinner("Calculating prediction..."):
        try:
            result = api_client.predict(payload)

            st.success("Prediction complete")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Predicted Yield (kg/ha)", f"{result['predicted_yield']:,}")
            with col2:
                st.metric("Predicted Yield (t/ha)", f"{result['predicted_yield_t_ha']}")

            st.info(
                f"95% confidence range: "
                f"{result['confidence_interval_t_ha'][0]} – "
                f"{result['confidence_interval_t_ha'][1]} t/ha"
            )
            st.caption(f"Model: {result['model_version']}")
            st.warning(result["disclaimer"])
        except Exception as e:
            st.error(f"Prediction failed: {e}")