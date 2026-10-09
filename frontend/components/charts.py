"""
Reusable chart components using Plotly.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def bar_chart(data: list, x: str, y: str, title: str, color: str = None):
    """Create a bar chart."""
    df = pd.DataFrame(data)
    fig = px.bar(df, x=x, y=y, title=title, color=color, text=y)
    fig.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def kpi_card(label: str, value, unit: str = ""):
    """Render a KPI card using Streamlit."""
    import streamlit as st
    st.metric(label=label, value=f"{value} {unit}".strip())