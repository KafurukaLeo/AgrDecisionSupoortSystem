"""
UI styling helpers and lightweight CSS enhancements.
"""
import streamlit as st


def apply_custom_styles():
    """Injects clean, modern styling into the Streamlit app."""
    st.markdown(
        """
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .material-symbols-outlined {
            font-family: 'Material Symbols Outlined' !important;
            font-size: 20px;
            vertical-align: middle;
            line-height: 1;
        }

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
            border-radius: 14px;
            padding: 1.8rem 2rem;
            color: #ffffff;
            margin-bottom: 1.5rem;
        }
        .hero-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0 0 0.4rem 0;
            color: #ffffff;
        }
        .hero-subtitle {
            font-size: 0.98rem;
            color: #d1fae5;
            margin: 0;
        }

        /* Clean Card */
        .ui-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            border: 1px solid #e2e8f0;
            margin-bottom: 1.2rem;
        }

        /* Sidebar enhancement */
        section[data-testid="stSidebar"] {
            background-color: #0f172a;
            color: #f8fafc;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str):
    """Renders a clean top banner."""
    st.markdown(
        f"""
        <div class="hero-banner">
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
