"""
Prediction Tool — Yield prediction and scenario simulation studio.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from frontend.config.settings import APP_TITLE, APP_ICON
from frontend.services.api_client import api_client
from frontend.components.styles import apply_custom_styles, render_hero, safe_html
from frontend.components.charts import yield_gauge

st.set_page_config(
    page_title=f"Prediction Tool • {APP_TITLE}",
    page_icon=APP_ICON,
    layout="wide",
)

apply_custom_styles()

render_hero(
    title="Estimate your harvest",
    subtitle="Choose a crop, location, and farm inputs to get an estimated yield.",
    badge="2025 survey data",
)

# Load filter options from API
try:
    options = api_client.get_filter_options()
except Exception as e:
    st.error("We couldn't load the crop and location options. Check that the app is running.")
    st.caption(f"Technical details: {e}")
    st.stop()

# Check model availability
model_ready = False
try:
    model_status = api_client.get_prediction_status()
    model_ready = bool(
        model_status.get("model_loaded")
        and model_status.get("encoders_loaded")
    )
except Exception as e:
    model_ready = False

if not model_ready:
    st.info(
        "The trained prediction model isn't available. This is an illustrative estimate "
        "based on 2025 survey benchmarks, not a forecast."
    )

with st.form("prediction_form"):
    st.subheader("Farm and location")
    col1, col2, col3 = st.columns(3)
    with col1:
        crop = st.selectbox(
            "Crop",
            options.get("crops", ["Maize", "Beans", "Rice", "Potatoes"]),
        )
        season = st.selectbox("Growing season", options.get("seasons", ["A", "B", "C"]))
        province = st.selectbox(
            "Province",
            options.get("provinces", ["Northern", "Southern", "Eastern", "Western", "Kigali"]),
        )
    with col2:
        district = st.selectbox(
            "District",
            options.get("districts", ["Musanze", "Nyagatare", "Huye", "Gasabo"]),
        )
        stratum = st.selectbox(
            "Farm type",
            [
                "Agricultural land on hillside",
                "Agricultural land in marshland",
                "Rangeland",
                "Mixed",
                "Large Scale Farmer",
            ],
        )
        farmer_gender = st.selectbox("Farmer's gender", ["Male", "Female"])
    with col3:
        plot_area_ha = st.number_input(
            "Plot size (hectares)",
            min_value=0.1,
            max_value=50.0,
            value=1.0,
            step=0.1,
        )
        farmer_age = st.slider("Farmer's age", min_value=18, max_value=85, value=40)

    st.subheader("Farm inputs")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        fertilizer = st.checkbox("Mineral fertilizer (NPK/DAP)", value=True)
        irrigation = st.checkbox("Irrigation", value=False)
    with c2:
        improved_seeds = st.checkbox("Improved seeds", value=True)
        pesticide = st.checkbox("Pesticide use", value=True)
    with c3:
        anti_erosion = st.checkbox("Erosion-control terraces", value=True)
        organic_fert = st.checkbox("Manure or compost", value=True)
    with c4:
        plot_irrigated = st.checkbox("Plot has irrigation access", value=False)

    submitted = st.form_submit_button("Estimate harvest", type="primary", width="stretch")

if submitted:
    crop_categories = {
        "Maize": "Cereal",
        "Rice": "Cereal",
        "Potatoes": "Tuber",
    }
    crop_category = crop_categories.get(crop, "Legume")
    payload = {
        "crop": crop,
        "crop_category": crop_category,
        "season": season,
        "province": province,
        "district": district,
        "stratum": stratum,
        "farmer_gender": farmer_gender,
        "land_use": stratum,
        "cropping_system": "Pure Cropping",
        "plot_area_ha": float(plot_area_ha),
        "crop_area_ha": float(plot_area_ha),
        "harvest_ratio": 100.0,
        "farmer_age": int(farmer_age),
        "fertilizer_used": bool(fertilizer),
        "irrigation_used": bool(irrigation),
        "pesticide_used": bool(pesticide),
        "improved_seeds_used": bool(improved_seeds),
        "anti_erosion_activity": bool(anti_erosion),
        "organic_fertilizer_used": bool(organic_fert),
        "inorganic_fertilizer_used": bool(fertilizer),
        "irrigation_practiced": bool(irrigation),
        "plot_irrigated": bool(plot_irrigated),
    }

    yield_tonnes_per_hectare = 0.0
    yield_kg_per_hectare = 0.0
    range_low = 0.0
    range_high = 0.0
    estimate_source = "2025 survey benchmark estimate"

    if model_ready:
        try:
            prediction = api_client.predict(payload)
            yield_kg_per_hectare = prediction["predicted_yield"]
            yield_tonnes_per_hectare = prediction["predicted_yield_t_ha"]
            range_low, range_high = prediction["confidence_interval_t_ha"]
            model_name = prediction.get("model_version", "Trained prediction model")
            estimate_source = model_name.replace("_", " ").title()
        except Exception as e:
            st.error("We couldn't calculate an estimate. Please try again.")
            st.caption(f"Technical details: {e}")
            st.stop()
    else:
        baselines = {
            "Potatoes": 6.8,
            "Rice": 3.6,
            "Maize": 2.4,
            "Beans": 1.4,
        }
        yield_multiplier = (
            1.0
            + (0.42 if fertilizer else 0)
            + (0.38 if irrigation else 0)
            + (0.28 if improved_seeds else 0)
            + (0.18 if anti_erosion else 0)
        )
        yield_tonnes_per_hectare = round(baselines.get(crop, 2.5) * yield_multiplier, 2)
        yield_kg_per_hectare = round(yield_tonnes_per_hectare * 1000.0, 1)
        range_low = round(yield_tonnes_per_hectare * 0.82, 2)
        range_high = round(yield_tonnes_per_hectare * 1.18, 2)

    total_tonnes = round(yield_tonnes_per_hectare * plot_area_ha, 2)
    comparison_yield = round(yield_tonnes_per_hectare * 0.78, 2)
    st.markdown("---")
    safe_html(
        f"""
        <div class="estimate-summary">
            <div>
                <strong class="estimate-summary-title">Harvest estimate ready</strong>
                <p class="estimate-summary-details">{crop} • Season {season} • {district} District</p>
            </div>
            <span class="estimate-range">Estimated range: {range_low}–{range_high} t/ha</span>
        </div>
        """
    )

    r1, r2, r3 = st.columns(3)
    r1.metric("Estimated yield", f"{yield_tonnes_per_hectare} t/ha")
    r2.metric("Estimated harvest", f"{total_tonnes} tonnes")
    r3.metric("Yield per hectare", f"{yield_kg_per_hectare:,} kg/ha")
    st.caption(f"Estimate source: {estimate_source}. Actual harvest may differ.")

    fig_gauge = yield_gauge(
        yield_tonnes_per_hectare,
        target=comparison_yield,
        title=f"{crop} yield compared with a reference",
    )
    st.plotly_chart(fig_gauge, width="stretch")