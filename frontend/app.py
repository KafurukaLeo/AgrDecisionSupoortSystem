"""Streamlit entry point with friendly names for every page."""
import streamlit as st


pages = [
    st.Page("Home.py", title="Home", default=True),
    st.Page("pages/1_Overview.py", title="Overview"),
    st.Page(
        "pages/2_Prediction_Tool.py",
        title="Estimate harvest",
        url_path="Prediction_Tool",
    ),
    st.Page(
        "pages/3_Model_Performance.py",
        title="Model checks",
        url_path="Model_Performance",
    ),
]

st.navigation(pages).run()
