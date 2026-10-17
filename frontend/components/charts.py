"""
Enterprise Chart Components using Plotly.
Bespoke styling matching the emerald/slate Rwanda Agri design system.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Color Palette Tokens
PRIMARY_GREEN = "#059669"
ACCENT_EMERALD = "#10B981"
LIGHT_GREEN = "#A7F3D0"
DARK_SLATE = "#0F172A"
MUTED_SLATE = "#64748B"
GOLD_AMBER = "#F59E0B"
BG_CARD = "#FFFFFF"

PALETTE_CATEGORICAL = [
    "#059669",  # Emerald
    "#0284c7",  # Sky Blue
    "#f59e0b",  # Amber
    "#8b5cf6",  # Violet
    "#ec4899",  # Rose
    "#14b8a6",  # Teal
    "#64748b",  # Slate
]


def bar_chart(data: list, x: str, y: str, title: str, color: str = None, height: int = 380):
    """Generates a modern rounded bar chart with tailored tooltips and styling."""
    df = pd.DataFrame(data)
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color=color,
        text=y,
        color_discrete_sequence=PALETTE_CATEGORICAL if color else [PRIMARY_GREEN],
    )
    
    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        marker_line_width=0,
        marker=dict(cornerradius=8),
        hovertemplate="<b>%{x}</b><br>Yield: %{y:.2f} t/ha<extra></extra>",
    )

    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=20, r=20, t=55, b=25),
        title=dict(
            font=dict(family="Outfit, sans-serif", size=16, color=DARK_SLATE),
            x=0,
            y=0.96,
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(family="Plus Jakarta Sans", size=12, color=MUTED_SLATE),
            title=None,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F1F5F9",
            tickfont=dict(family="Plus Jakarta Sans", size=11, color=MUTED_SLATE),
            title=dict(text="Yield (t/ha)", font=dict(size=12, color=MUTED_SLATE)),
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def regional_comparison_chart(data: list):
    """Generates horizontal bars comparing productivity across provinces."""
    df = pd.DataFrame(data)
    fig = px.bar(
        df,
        y="province",
        x="yield",
        orientation="h",
        text="yield",
        title="Average Productivity by Province (t/ha)",
        color="yield",
        color_continuous_scale=["#a7f3d0", "#059669"],
    )

    fig.update_traces(
        texttemplate="%{text:.2f} t/ha",
        textposition="inside",
        insidetextanchor="end",
        marker=dict(cornerradius=6),
        hovertemplate="<b>%{y}</b><br>Average Yield: %{x:.2f} t/ha<extra></extra>",
    )

    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=10, r=20, t=50, b=20),
        coloraxis_showscale=False,
        title=dict(font=dict(family="Outfit, sans-serif", size=15, color=DARK_SLATE), x=0),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title=None),
        yaxis=dict(showgrid=False, title=None, tickfont=dict(family="Plus Jakarta Sans", size=12)),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def yield_gauge(value: float, max_val: float = 12.0, target: float = 4.5, title: str = "Estimated Yield (t/ha)"):
    """Generates an executive speedo-gauge for prediction confidence and benchmarks."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title, "font": {"family": "Outfit, sans-serif", "size": 17, "color": DARK_SLATE}},
            delta={"reference": target, "increasing": {"color": "#059669"}, "decreasing": {"color": "#ef4444"}},
            gauge={
                "axis": {"range": [0, max_val], "tickwidth": 1, "tickcolor": MUTED_SLATE},
                "bar": {"color": PRIMARY_GREEN, "thickness": 0.28},
                "bgcolor": "white",
                "borderwidth": 1,
                "bordercolor": "#E2E8F0",
                "steps": [
                    {"range": [0, target * 0.7], "color": "#fee2e2"},
                    {"range": [target * 0.7, target * 1.1], "color": "#fef3c7"},
                    {"range": [target * 1.1, max_val], "color": "#d1fae5"},
                ],
                "threshold": {
                    "line": {"color": "#047857", "width": 4},
                    "thickness": 0.8,
                    "value": target,
                },
            },
        )
    )

    fig.update_layout(
        height=260,
        margin=dict(l=25, r=25, t=45, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Plus Jakarta Sans"},
    )
    return fig


def model_comparison_chart(metrics_data: list):
    """Renders ML model comparison for R2 and MAE."""
    df = pd.DataFrame(metrics_data)
    
    # Format names
    name_map = {
        "random_forest": "Random Forest (Best)",
        "gradient_boosting": "Gradient Boosting",
        "linear_regression": "Linear Regression Baseline",
    }
    df["display_name"] = df["model"].map(lambda x: name_map.get(x, x.replace("_", " ").title()))

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="R² Score (Accuracy)",
            x=df["display_name"],
            y=df["r2"],
            marker_color=["#059669", "#0284c7", "#94a3b8"],
            text=[f"{v:.3f}" for v in df["r2"]],
            textposition="auto",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(text="Model Validation Accuracy (R² Score on Unseen Test Split)", font=dict(family="Outfit", size=15)),
        yaxis=dict(gridcolor="#F1F5F9", title="R² Score (higher is better)"),
        xaxis=dict(title=None),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig