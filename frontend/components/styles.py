"""
Central UI Design System and Custom CSS Components.
Uses Google Material Symbols (clean vector icons) instead of emojis.
"""
import streamlit as st


def apply_custom_styles():
    """Injects high-end CSS and Material Symbols font into the Streamlit app."""
    css = """
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3, .brand-font {
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.02em;
    }

    /* Google Material Symbols base */
    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined' !important;
        font-weight: 400;
        font-style: normal;
        font-size: 22px;
        line-height: 1;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        vertical-align: middle;
        -webkit-font-smoothing: antialiased;
    }

    /* Top decoration bar */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #059669 0%, #10b981 50%, #f59e0b 100%);
        z-index: 9999;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        max-width: 1280px;
    }

    /* Premium Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 45%, #047857 100%);
        border-radius: 18px;
        padding: 2.2rem 2.4rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.25), 0 8px 10px -6px rgba(5, 150, 105, 0.2);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .hero-banner::after {
        content: "";
        position: absolute;
        top: -50px;
        right: -50px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.35) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.16);
        backdrop-filter: blur(8px);
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #ecfdf5;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .hero-title {
        font-size: 2.15rem;
        font-weight: 700;
        line-height: 1.2;
        margin: 0 0 0.5rem 0;
        color: #ffffff;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #d1fae5;
        max-width: 820px;
        margin: 0;
        line-height: 1.5;
        font-weight: 400;
    }

    /* KPI Metric Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 1.2rem;
        margin-bottom: 2rem;
    }

    .kpi-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.4rem 1.4rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: #10b981;
        box-shadow: 0 12px 20px -5px rgba(16, 185, 129, 0.15);
    }

    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.6rem;
    }

    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #64748b;
        margin: 0;
    }

    .kpi-icon-wrap {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: #ecfdf5;
        color: #059669;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .kpi-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0.2rem 0;
        line-height: 1.1;
    }

    .kpi-unit {
        font-size: 0.95rem;
        font-weight: 500;
        color: #64748b;
        margin-left: 0.25rem;
    }

    .kpi-footer {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-top: 0.5rem;
        font-size: 0.8rem;
    }

    .trend-up {
        color: #059669;
        font-weight: 600;
    }

    .trend-neutral {
        color: #64748b;
    }

    /* Section Cards */
    .content-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.6rem 1.8rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.6rem;
    }

    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.55rem;
    }

    .card-subtitle {
        font-size: 0.88rem;
        color: #64748b;
        margin-bottom: 1.2rem;
    }

    /* Status Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .status-pill.success {
        background: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
    }

    .status-pill.warning {
        background: #fffbeb;
        color: #92400e;
        border: 1px solid #fde68a;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Enhanced Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        color: #f8fafc;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
        color: #cbd5e1;
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: #f1f5f9 !important;
        font-weight: 500;
    }

    .sidebar-brand-box {
        padding: 1.2rem 1.1rem;
        background: rgba(255, 255, 255, 0.04);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.5rem;
    }

    .sidebar-brand-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff !important;
        letter-spacing: -0.01em;
        margin: 0 0 0.25rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .sidebar-brand-sub {
        font-size: 0.78rem;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0;
    }

    /* Prediction Result Showcase Card */
    .prediction-showcase {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 50%, #d1fae5 100%);
        border: 2px solid #34d399;
        border-radius: 18px;
        padding: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.15);
        margin: 1.5rem 0;
    }

    .prediction-title {
        font-size: 0.92rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #065f46;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }

    .prediction-big-num {
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: #064e3b;
        line-height: 1;
        margin-bottom: 0.4rem;
    }

    /* Streamlit Button enhancement */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.6rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.01em;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
        transition: all 0.2s ease;
    }

    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(5, 150, 105, 0.4);
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }

    /* Form container beauty */
    [data-testid="stForm"] {
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        padding: 1.8rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str, badge: str = "National Agricultural Intelligence • Rwanda", icon_name: str = "agriculture"):
    """Renders a premier hero header banner with vector icon."""
    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-badge">
                <span class="material-symbols-outlined" style="font-size: 16px;">{icon_name}</span>
                {badge}
            </div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi(title: str, value: str, unit: str = "", delta: str = None, material_icon: str = "analytics", is_up: bool = True):
    """Renders an enterprise KPI card with a real vector Material Symbol."""
    delta_html = ""
    if delta:
        trend_class = "trend-up" if is_up else "trend-neutral"
        delta_html = f"""
        <div class="kpi-footer">
            <span class="{trend_class}">{delta}</span>
        </div>
        """

    return f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <p class="kpi-title">{title}</p>
            <div class="kpi-icon-wrap">
                <span class="material-symbols-outlined">{material_icon}</span>
            </div>
        </div>
        <div class="kpi-value">{value}<span class="kpi-unit">{unit}</span></div>
        {delta_html}
    </div>
    """


def render_sidebar_header(api_online: bool = True):
    """Renders the top branding and status inside sidebar."""
    status_class = "success" if api_online else "warning"
    status_text = "API Operational" if api_online else "API Offline"

    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand-box">
            <p class="sidebar-brand-title">
                <span class="material-symbols-outlined" style="font-size: 24px; color: #10b981;">agriculture</span>
                AgriSupport Rwanda
            </p>
            <p class="sidebar-brand-sub">Decision Support System</p>
            <div style="margin-top: 0.8rem; display: flex; align-items: center; gap: 0.5rem;">
                <span class="status-pill {status_class}">
                    <span class="pulse-dot"></span>
                    {status_text}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
