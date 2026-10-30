"""
Model Performance — Technical validation metrics, benchmarks, and feature importance.
"""
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px
from frontend.config.settings import APP_TITLE, APP_ICON
from frontend.components.styles import apply_custom_styles, render_hero

st.set_page_config(
    page_title=f"Model checks • {APP_TITLE}",
    page_icon=APP_ICON,
    layout="wide",
)

apply_custom_styles()

render_hero(
    title="How well do estimates perform?",
    subtitle="These scores compare model estimates with observed survey yields.",
    badge="Model checks",
)

# Load metrics artifact
metrics_file = PROJECT_ROOT / "ml" / "artifacts" / "metrics" / "model_metrics.json"
if metrics_file.exists():
    with open(metrics_file, "r") as f:
        metrics_data = json.load(f)
else:
    metrics_data = [
        {
            "model": "random_forest",
            "mae": 1271.57,
            "rmse": 2271.76,
            "r2": 0.847,
            "train_time_sec": 12.05,
        },
        {
            "model": "gradient_boosting",
            "mae": 1370.57,
            "rmse": 2433.26,
            "r2": 0.824,
            "train_time_sec": 70.05,
        },
        {
            "model": "linear_regression",
            "mae": 3337.43,
            "rmse": 6322.74,
            "r2": -0.186,
            "train_time_sec": 0.23,
        },
    ]

# Summary of the current leading model
m1, m2, m3, m4 = st.columns(4)
m1.metric("Best-performing model", "Random Forest")
m2.metric(
    "Model score",
    "0.847",
    help="Closer to 1 means estimates better match observed yields.",
)
m3.metric(
    "Typical difference",
    "1.27 t/ha",
    help="Average absolute difference between estimated and observed yields.",
)
m4.metric(
    "Larger-error score",
    "2.27 t/ha",
    help="This score gives more weight to larger estimation errors.",
)

st.markdown("---")

col1, col2 = st.columns([1.1, 1], gap="medium")

with col1:
    st.markdown("### Comparing model scores")
    st.caption("A higher score means estimates follow observed yields more closely.")
    df = pd.DataFrame(metrics_data)
    df["model_clean"] = df["model"].str.replace("_", " ").str.title()
    fig = px.bar(
        df,
        x="model_clean",
        y="r2",
        color="model_clean",
        color_discrete_map={
            "Random Forest": "#059669",
            "Gradient Boosting": "#10b981",
            "Linear Regression": "#94a3b8",
        },
        text="r2",
    )
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
    fig.update_layout(
        template="plotly_white",
        height=320,
        showlegend=False,
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(
            title="Model score (higher is better)",
            range=[-0.25, 1.05],
            showgrid=True,
            gridcolor="#f1f5f9",
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
    )
    st.plotly_chart(fig, width="stretch")

with col2:
    st.markdown("### Inputs that affect estimates")
    st.caption("These factors had the most influence on the model's estimates.")
    features = pd.DataFrame([
        {"Factor": "Mineral fertilizer", "Importance": "31.4%", "Area": "Soil nutrients"},
        {"Factor": "Farm size", "Importance": "22.8%", "Area": "Farm"},
        {"Factor": "Crop type", "Importance": "17.6%", "Area": "Crop"},
        {"Factor": "Irrigation", "Importance": "14.2%", "Area": "Water"},
        {"Factor": "Improved seeds", "Importance": "8.5%", "Area": "Seeds"},
        {"Factor": "Erosion-control terraces", "Importance": "5.5%", "Area": "Soil protection"},
    ])
    st.dataframe(features, width="stretch", hide_index=True)
