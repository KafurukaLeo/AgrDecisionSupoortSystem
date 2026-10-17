"""
About & System Methodology — AI Agri Decision Support Rwanda.
Data provenance, system architecture, and institutional alignment.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from frontend.config.settings import APP_TITLE, APP_ICON
from frontend.services.api_client import api_client
from frontend.components.styles import (
    apply_custom_styles,
    render_hero,
    render_sidebar_header,
)

st.set_page_config(
    page_title=f"About & Architecture • {APP_TITLE}",
    page_icon=APP_ICON,
    layout="wide",
)

apply_custom_styles()

api_online = True
try:
    api_client.health()
except Exception:
    api_online = False

render_sidebar_header(api_online=api_online)

render_hero(
    title="System Architecture & Data Methodology",
    subtitle="Institutional alignment, NISR SAS data provenance, and technical architecture of the Rwanda Agricultural Decision Support System.",
    badge="Documentation & Provenance • Republic of Rwanda",
)

col1, col2 = st.columns([1.1, 1], gap="medium")

with col1:
    st.markdown(
        """
        <div class="content-card">
            <div class="card-title">🎯 Vision & Strategic Alignment</div>
            <div class="card-subtitle">Supporting Rwanda's Strategic Plan for Agriculture Transformation (PSTA 4).</div>
            <p style="color: #334155; line-height: 1.6; font-size: 0.95rem;">
                Rwanda's agriculture sector accounts for over 25% of national GDP and employs majority of the workforce. 
                This Decision Support System provides smallholder cooperatives, agricultural extension officers, 
                and MINAGRI policymakers with <strong>data-driven yield forecasts</strong> to:
            </p>
            <ul style="color: #475569; line-height: 1.6; font-size: 0.92rem;">
                <li><strong>De-risk seasonal agricultural investments</strong> by projecting expected output before planting.</li>
                <li><strong>Optimize input allocation</strong> (fertilizers, certified seeds, irrigation infrastructure) to highest-ROI plots.</li>
                <li><strong>Strengthen national food security planning</strong> through empirical NISR micro-data modeling.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="content-card">
            <div class="card-title">📚 Data Provenance (NISR SAS 2025)</div>
            <div class="card-subtitle">Official statistical survey micro-data collection methodology.</div>
            <p style="color: #334155; line-height: 1.6; font-size: 0.92rem;">
                The underlying intelligence is trained on micro-data collected during the <strong>2025 Seasonal Agricultural Survey (SAS)</strong> 
                by the National Institute of Statistics of Rwanda (NISR). The dataset encompasses:
            </p>
            <ul style="color: #475569; line-height: 1.6; font-size: 0.92rem;">
                <li>Multi-season coverage: Season A, Season B, and Season C (Marshland).</li>
                <li>Geographical stratification across all 30 administrative districts of Rwanda.</li>
                <li>Field-level questionnaires covering plot sizes, crop cuts, fertilizer application rates, anti-erosion structures, and irrigation methods.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="content-card">
            <div class="card-title">🏗️ Enterprise Technology Architecture</div>
            <div class="card-subtitle">High-performance, decoupled microservice design.</div>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.2rem; font-size: 0.88rem; font-family: monospace; line-height: 1.6; color: #0f172a;">
                <strong style="color: #059669;">[Client Presentation Tier]</strong><br>
                Streamlit 1.66 • Plotly Data Visuals • Responsive Glassmorphism<br>
                &nbsp;&nbsp;&nbsp;&nbsp;│<br>
                &nbsp;&nbsp;&nbsp;&nbsp;▼ (High-Speed HTTP REST JSON)<br>
                <strong style="color: #0284c7;">[Backend API Gateway Tier]</strong><br>
                FastAPI 0.143 • Uvicorn ASGI • Pydantic Schema Validation<br>
                &nbsp;&nbsp;&nbsp;&nbsp;│<br>
                &nbsp;&nbsp;&nbsp;&nbsp;▼<br>
                <strong style="color: #d97706;">[Inference & ML Pipeline Tier]</strong><br>
                Scikit-Learn 1.9.1 • Random Forest Champion • Preprocessor & Encoders
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="content-card">
            <div class="card-title">🛡️ Quality & Validation Standards</div>
            <div class="card-subtitle">Ensuring scientific integrity and reliability.</div>
            <ul style="color: #475569; line-height: 1.6; font-size: 0.92rem;">
                <li><strong>Log-transform Target Optimization:</strong> Mitigates extreme outliers and right-skewed yield distributions.</li>
                <li><strong>Winsorization at 99th Percentile:</strong> Protects against erroneous plot survey entries.</li>
                <li><strong>Strict Train/Test Isolation:</strong> Zero data leakage between training splits and validation benchmarks.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
