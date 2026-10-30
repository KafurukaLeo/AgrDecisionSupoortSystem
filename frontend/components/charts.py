"""
Chart components using Plotly.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def bar_chart(data: list, x: str, y: str, title: str):
    """Creates a clean bar chart with emerald styling."""
    df = pd.DataFrame(data)
    fig = px.bar(df, x=x, y=y, title=title, text=y)
    fig.update_traces(
        marker_color="#059669",
        texttemplate="%{text:.1f}",
        textposition="outside",
    )
    fig.update_layout(
        template="plotly_white",
        height=360,
        margin=dict(l=20, r=20, t=45, b=20),
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", title="Yield (t/ha)"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def yield_gauge(value: float, target: float = 3.5, title: str = "Yield Benchmark (t/ha)"):
    """Creates a simple gauge chart comparing predicted yield against a target."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            delta={"reference": target, "increasing": {"color": "#059669"}, "decreasing": {"color": "#ef4444"}},
            title={"text": title, "font": {"size": 15}},
            gauge={
                "axis": {"range": [0, max(value * 1.4, 10.0)]},
                "bar": {"color": "#059669"},
                "steps": [
                    {"range": [0, target * 0.8], "color": "#fee2e2"},
                    {"range": [target * 0.8, target * 1.2], "color": "#fef3c7"},
                    {"range": [target * 1.2, max(value * 1.4, 10.0)], "color": "#d1fae5"},
                ],
                "threshold": {"line": {"color": "#047857", "width": 3}, "value": target},
            },
        )
    )
    fig.update_layout(height=240, margin=dict(l=20, r=20, t=35, b=20), paper_bgcolor="rgba(0,0,0,0)")
    return fig