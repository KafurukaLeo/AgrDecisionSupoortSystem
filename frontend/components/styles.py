"""
UI styling helpers and modern CSS enhancements.
"""
import textwrap
import streamlit as st


def safe_html(html_str: str):
    """Render trusted HTML; this helper does not sanitize its input."""
    dedented = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(dedented)
    else:
        st.markdown(dedented, unsafe_allow_html=True)


def apply_custom_styles():
    """Apply shared spacing, typography, and color styles."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            letter-spacing: -0.01em;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Navigation buttons and page links */
        div[data-testid="stSidebarNav"] {
            background: rgba(15, 23, 42, 0.55);
            border-radius: 14px;
            padding: 0.35rem 0.35rem 0.15rem;
        }
        div[data-testid="stSidebarNav"] a {
            color: #f8fafc !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em;
            border-radius: 10px !important;
            padding: 0.7rem 0.9rem !important;
            transition: all 0.2s ease;
            text-shadow: 0 1px 1px rgba(15, 23, 42, 0.45);
        }
        div[data-testid="stSidebarNav"] a:hover {
            background: rgba(148, 163, 184, 0.14) !important;
            color: #ffffff !important;
        }
        div[data-testid="stSidebarNav"] a[aria-current="page"] {
            background: rgba(148, 163, 184, 0.22) !important;
            border: 1px solid rgba(148, 163, 184, 0.4) !important;
            color: #ffffff !important;
            box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.03);
        }
        div[data-testid="stSidebarNav"] a[aria-current="page"] > div,
        div[data-testid="stSidebarNav"] a[aria-current="page"] span,
        div[data-testid="stSidebarNav"] a[aria-current="page"] li {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        .material-symbols-outlined {
            font-family: 'Material Symbols Outlined' !important;
            font-size: 20px;
            vertical-align: middle;
            line-height: 1;
        }

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
            border-radius: 16px;
            padding: 2rem 2.25rem;
            color: #ffffff;
            margin-bottom: 1.75rem;
            box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25), 0 8px 10px -6px rgba(6, 78, 59, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 14px;
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.42);
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #ffffff !important;
            margin-bottom: 0.75rem;
            text-shadow: 0 1px 1px rgba(15, 23, 42, 0.35);
        }
        .hero-title {
            font-size: 1.9rem;
            font-weight: 800;
            line-height: 1.2;
            margin: 0 0 0.5rem 0;
            color: #ffffff;
            letter-spacing: -0.02em;
        }
        .hero-subtitle {
            font-size: 1rem;
            color: #d1fae5;
            margin: 0;
            font-weight: 400;
            max-width: 780px;
            line-height: 1.5;
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.1rem 1.35rem;
            box-shadow: 0 2px 4px rgba(15, 23, 42, 0.04);
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        div[data-testid="stMetric"]:hover {
            border-color: #cbd5e1;
            box-shadow: 0 6px 14px rgba(15, 23, 42, 0.08);
            transform: translateY(-2px);
        }
        div[data-testid="stMetric"] label[data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b !important;
            font-weight: 600 !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            font-size: 1.7rem !important;
            font-weight: 800 !important;
            color: #0f172a !important;
            letter-spacing: -0.02em;
        }

        /* Form Container */
        div[data-testid="stForm"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.75rem;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }

        /* Primary Button */
        button[kind="primary"] {
            background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.4rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em !important;
            box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35) !important;
            transition: all 0.2s ease !important;
        }
        button[kind="primary"]:hover {
            background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
            box-shadow: 0 6px 18px rgba(5, 150, 105, 0.45) !important;
            transform: translateY(-1px) !important;
        }

        /* Feature Card */
        .feature-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.25rem 1.4rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
            transition: all 0.2s ease;
        }
        .feature-card:hover {
            border-color: #059669;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(5, 150, 105, 0.1);
        }
        .feature-title {
            font-weight: 700;
            font-size: 0.95rem;
            color: #0f172a;
            margin-bottom: 0.25rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .feature-desc {
            font-size: 0.875rem;
            color: #64748b;
            margin: 0;
            line-height: 1.45;
        }

        .estimate-summary {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            padding: 1rem 1.4rem;
            margin-bottom: 1.25rem;
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-radius: 12px;
        }
        .estimate-summary-title {
            color: #166534;
            font-size: 1.05rem;
        }
        .estimate-summary-details {
            margin: 0.15rem 0 0;
            color: #15803d;
            font-size: 0.85rem;
        }
        .estimate-range {
            padding: 4px 12px;
            border-radius: 9999px;
            background: #dcfce7;
            color: #15803d;
            font-size: 0.8rem;
            font-weight: 700;
            white-space: nowrap;
        }
        @media (max-width: 768px) {
            .estimate-summary {
                align-items: flex-start;
                flex-direction: column;
            }
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0f172a;
            color: #f8fafc;
        }
        .sidebar-brand {
            padding: 0.5rem 0 1.2rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1.2rem;
        }
        .sidebar-brand-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0;
            letter-spacing: -0.01em;
        }
        .sidebar-brand-sub {
            font-size: 0.78rem;
            color: #94a3b8;
            margin: 0;
        }
        .pulse-status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 5px 12px;
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #34d399;
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: #34d399;
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7);
            animation: pulse-ring 2s infinite;
        }
        @keyframes pulse-ring {
            0% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7); }
            70% { box-shadow: 0 0 0 6px rgba(52, 211, 153, 0); }
            100% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str, badge: str = "Rwanda • 2025 survey data"):
    """Show the page title, a short description, and a source badge."""
    safe_html(
        f"""
        <div class="hero-banner">
            <div class="hero-badge">
                <span class="material-symbols-outlined" style="font-size: 15px;">verified</span>
                {badge}
            </div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """
    )
