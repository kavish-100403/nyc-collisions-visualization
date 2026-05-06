import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Reference (Dash fundamentals/layout): https://dash.plotly.com/layout
# Reference (Dash callbacks): https://dash.plotly.com/basic-callbacks
# Reference (Plotly Express API): https://plotly.com/python/plotly-express/
# Reference (Plotly density_mapbox): https://plotly.com/python/mapbox-density-heatmaps/


# Data loading
df = pd.read_csv("data/processed/collisions_cleaned.csv")

# Remove UNKNOWN from borough dropdown
boroughs = sorted(df[df["BOROUGH"] != "UNKNOWN"]["BOROUGH"].dropna().unique())
years = sorted(df["YEAR"].dropna().unique())

borough_options = [{"label": "All Boroughs", "value": "ALL"}] + [
    {"label": b.title(), "value": b} for b in boroughs
]

year_options = [{"label": str(int(y)), "value": int(y)} for y in years]

time_options = [
    {"label": "All Day", "value": "ALL"},
    {"label": "Morning: 6 AM - 11 AM", "value": "MORNING"},
    {"label": "Afternoon: 12 PM - 4 PM", "value": "AFTERNOON"},
    {"label": "Evening: 5 PM - 8 PM", "value": "EVENING"},
    {"label": "Night: 9 PM - 5 AM", "value": "NIGHT"},
]


# Visual design system
COLORS = {
    "background": "#eef2f7",
    "card": "#ffffff",
    "header_bg": "#0f172a",
    "header_text": "#f8fafc",
    "text": "#0f172a",
    "muted": "#64748b",
    "border": "#d1d9e6",
    "blue": "#2563eb",
    "blue_light": "#dbeafe",
    "orange": "#f97316",
    "orange_light": "#fff0e0",
    "teal": "#0f766e",
    "teal_light": "#ccfbf1",
    "purple": "#7c3aed",
    "purple_light": "#ede9fe",
    "gray": "#94a3b8",
}

PAGE_STYLE = {
    "fontFamily": "Inter, Arial, sans-serif",
    "backgroundColor": COLORS["background"],
    "color": COLORS["text"],
    "padding": "18px 22px",
    "minHeight": "100vh",
}

CARD_STYLE = {
    "backgroundColor": COLORS["card"],
    "border": f"1px solid {COLORS['border']}",
    "borderRadius": "14px",
    "boxShadow": "0 1px 3px rgba(15, 23, 42, 0.06)",
}

SECTION_TITLE_STYLE = {
    "fontSize": "16px",
    "fontWeight": "650",
    "margin": "0 0 12px 0",
    "color": COLORS["text"],
}

LABEL_STYLE = {
    "fontSize": "12px",
    "fontWeight": "600",
    "color": COLORS["muted"],
    "marginBottom": "6px",
    "display": "block",
}

DROPDOWN_STYLE = {
    "fontSize": "13px",
    "width": "220px",
}


# Dash app
# Reference (Dash app init): https://dash.plotly.com/dash-core-components
app = Dash(__name__)

# Reference (Dash layout patterns): https://dash.plotly.com/layout
app.layout = html.Div(
    style=PAGE_STYLE,
    children=[
        # Header
        html.Div(
            style={
                "backgroundColor": COLORS["header_bg"],
                "borderRadius": "14px",
                "padding": "22px 28px",
                "marginBottom": "16px",
                "textAlign": "center",
                "boxShadow": "0 4px 12px rgba(15, 23, 42, 0.18)",
            },
            children=[
                html.H1(
                    "NYC Traffic Collision Dashboard",
                    style={
                        "fontSize": "28px",
                        "lineHeight": "1.2",
                        "margin": "0",
                        "fontWeight": "750",
                        "letterSpacing": "-0.4px",
                        "color": COLORS["header_text"],
                    },
                ),
                html.P(
                    "Explore where, when, and why traffic collisions occur across New York City.",
                    style={
                        "fontSize": "14px",
                        "color": "#94a3b8",
                        "margin": "8px 0 0 0",
                    },
                ),
            ],
        ),
        # Filters
        html.Div(
            style={
                **CARD_STYLE,
                "padding": "14px 16px",
                "marginBottom": "16px",
                "display": "flex",
                "gap": "16px",
                "alignItems": "end",
                "flexWrap": "wrap",
                "backgroundColor": "#f1f5fb",
                "borderTop": f"3px solid {COLORS['blue']}",
            },
            children=[
                html.Div(
                    children=[
                        html.Label("Year", style=LABEL_STYLE),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=year_options,
                            value=max(years),
                            clearable=False,
                            style={**DROPDOWN_STYLE, "width": "150px"},
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Label("Borough", style=LABEL_STYLE),
                        dcc.Dropdown(
                            id="borough-dropdown",
                            options=borough_options,
                            value="ALL",
                            clearable=False,
                            style=DROPDOWN_STYLE,
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Label("Time of Day", style=LABEL_STYLE),
                        dcc.Dropdown(
                            id="time-dropdown",
                            options=time_options,
                            value="ALL",
                            clearable=False,
                            style={**DROPDOWN_STYLE, "width": "260px"},
                        ),
                    ]
                ),
            ],
        ),
        # Summary cards should be separate from filters
        html.Div(
            id="summary-cards",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
                "gap": "14px",
                "marginBottom": "16px",
            },
        ),
        # Main grid
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1.25fr 1fr",
                "gap": "16px",
                "alignItems": "start",
            },
            children=[
                html.Div(
                    style={
                        **CARD_STYLE,
                        "padding": "16px",
                        "borderTop": f"3px solid {COLORS['orange']}",
                    },
                    children=[
                        html.H3(
                            "Where are high-risk collision areas?",
                            style=SECTION_TITLE_STYLE,
                        ),
                        html.P(
                            "Hotspots where crashes resulted in 3+ injuries or a fatality.",
                            style={
                                "fontSize": "12px",
                                "color": COLORS["muted"],
                                "margin": "-6px 0 10px 0",
                            },
                        ),
                        dcc.Graph(
                            id="map-graph",
                            config={"displayModeBar": False},
                            style={"height": "465px"},
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "16px",
                    },
                    children=[
                        html.Div(
                            style={
                                **CARD_STYLE,
                                "padding": "16px",
                                "borderTop": f"3px solid {COLORS['purple']}",
                            },
                            children=[
                                html.H3(
                                    "What causes most reported crashes?",
                                    style=SECTION_TITLE_STYLE,
                                ),
                                dcc.Graph(
                                    id="cause-chart",
                                    config={"displayModeBar": False},
                                    style={"height": "300px"},
                                ),
                            ],
                        ),
                        html.Div(
                            style={
                                **CARD_STYLE,
                                "padding": "16px",
                                "borderTop": f"3px solid {COLORS['teal']}",
                            },
                            children=[
                                html.H3(
                                    "How do crashes change by month?",
                                    style=SECTION_TITLE_STYLE,
                                ),
                                dcc.Graph(
                                    id="trend-chart",
                                    config={"displayModeBar": False},
                                    style={"height": "300px"},
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# Data filtering
def filter_data(selected_year, selected_borough, selected_time):
    filtered = df[df["YEAR"] == selected_year]

    if selected_borough != "ALL":
        filtered = filtered[filtered["BOROUGH"] == selected_borough]

    if selected_time == "MORNING":
        filtered = filtered[(filtered["HOUR"] >= 6) & (filtered["HOUR"] <= 11)]
    elif selected_time == "AFTERNOON":
        filtered = filtered[(filtered["HOUR"] >= 12) & (filtered["HOUR"] <= 16)]
    elif selected_time == "EVENING":
        filtered = filtered[(filtered["HOUR"] >= 17) & (filtered["HOUR"] <= 20)]
    elif selected_time == "NIGHT":
        filtered = filtered[(filtered["HOUR"] >= 21) | (filtered["HOUR"] <= 5)]

    return filtered


# Visualizations
def create_map(filtered_df):
    # Reference (density mapbox usage & params): https://plotly.com/python/mapbox-density-heatmaps/ (accessed 2026-05-03)
    # Only include serious crashes (2+ injured or any fatality) so the
    # density map highlights actual risk hotspots rather than routine
    # low-severity incidents that saturate the entire city.
    map_df = filtered_df[
        (filtered_df["NUMBER OF PERSONS INJURED"] >= 3)
        | (filtered_df["NUMBER OF PERSONS KILLED"] > 0)
    ].copy()

    if map_df.empty:
        fig = px.scatter_mapbox(height=455)
        fig.update_layout(
            mapbox_style="carto-positron",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="white",
            plot_bgcolor="white",
        )
        return fig

    map_df = map_df.sample(min(10000, len(map_df)), random_state=42)

    fig = px.density_mapbox(
        map_df,
        lat="LATITUDE",
        lon="LONGITUDE",
        radius=5,
        zoom=9.25,
        center={"lat": 40.7128, "lon": -74.0060},
        height=455,
        mapbox_style="carto-positron",
        color_continuous_scale="Cividis",
    )

    fig.update_traces(opacity=0.65)

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="white",
        plot_bgcolor="white",
        coloraxis_colorbar=dict(
            title=dict(
                text="Crash<br>Density",
                font=dict(size=11, color=COLORS["muted"]),
            ),
            thickness=10,
            len=0.75,
            tickfont=dict(size=10, color=COLORS["muted"]),
        ),
    )

    return fig


def create_cause_chart(filtered_df):
    # Reference (Plotly Express bar charts): https://plotly.com/python/bar-charts/
    cause_counts = (
        filtered_df["CONTRIBUTING FACTOR VEHICLE 1"]
        .replace("Unspecified", pd.NA)
        .dropna()
        .value_counts()
        .head(8)
        .reset_index()
    )

    cause_counts.columns = ["Cause", "Crashes"]

    if cause_counts.empty:
        cause_counts = pd.DataFrame({"Cause": ["No data"], "Crashes": [0]})

    CAUSE_PALETTE = [
        "#0072B2",  # blue
        "#E69F00",  # orange
        "#009E73",  # teal
        "#CC79A7",  # purple/pink
        "#56B4E9",  # sky blue
        "#D55E00",  # vermillion
        "#F0E442",  # yellow
        "#999999",  # gray
    ]

    fig = px.bar(
        cause_counts,
        x="Crashes",
        y="Cause",
        orientation="h",
        text="Crashes",
        color="Cause",
        color_discrete_sequence=CAUSE_PALETTE,
    )

    fig.update_traces(textposition="outside", marker_line_width=0)

    fig.update_layout(
        height=285,
        margin={"r": 35, "t": 4, "l": 8, "b": 30},
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Crashes",
        yaxis_title="",
        yaxis={"categoryorder": "total ascending"},
        font=dict(size=11, color=COLORS["text"]),
        xaxis=dict(
            showgrid=True,
            gridcolor=COLORS["border"],
            zeroline=False,
            tickfont=dict(size=10, color=COLORS["muted"]),
            title=dict(font=dict(size=11, color=COLORS["muted"])),
        ),
        yaxis_tickfont=dict(size=10, color=COLORS["text"]),
    )

    return fig


def create_trend_chart(filtered_df):
    # Reference (Plotly Express line charts): https://plotly.com/python/line-charts/
    monthly = (
        filtered_df.groupby(["MONTH", "MONTH_NAME"])["CRASH DATE"]
        .count()
        .reset_index()
        .rename(columns={"CRASH DATE": "Crashes"})
        .sort_values("MONTH")
    )

    fig = px.line(
        monthly,
        x="MONTH_NAME",
        y="Crashes",
        markers=True,
    )

    fig.update_traces(
        line=dict(width=3, color=COLORS["teal"]),
        marker=dict(size=7, color=COLORS["teal"], line=dict(width=1.5, color="white")),
        fill="tozeroy",
        fillcolor="rgba(15, 118, 110, 0.08)",
    )

    fig.update_layout(
        height=285,
        margin={"r": 20, "t": 4, "l": 48, "b": 42},
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Month",
        yaxis_title="Crashes",
        font=dict(size=11, color=COLORS["text"]),
        xaxis=dict(
            tickangle=-25,
            showgrid=False,
            tickfont=dict(size=10, color=COLORS["muted"]),
            title=dict(font=dict(size=11, color=COLORS["muted"])),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS["border"],
            zeroline=False,
            tickfont=dict(size=10, color=COLORS["muted"]),
            title=dict(font=dict(size=11, color=COLORS["muted"])),
        ),
    )

    return fig


def create_summary_cards(filtered_df):
    total_crashes = len(filtered_df)
    total_injuries = int(filtered_df["NUMBER OF PERSONS INJURED"].sum())
    total_fatalities = int(filtered_df["NUMBER OF PERSONS KILLED"].sum())

    common_cause = (
        filtered_df["CONTRIBUTING FACTOR VEHICLE 1"]
        .replace("Unspecified", pd.NA)
        .dropna()
        .mode()
    )
    common_cause = common_cause.iloc[0] if not common_cause.empty else "N/A"

    cards = [
        ("Total Crashes", f"{total_crashes:,}", COLORS["blue"], COLORS["blue_light"]),
        (
            "Total Injuries",
            f"{total_injuries:,}",
            COLORS["orange"],
            COLORS["orange_light"],
        ),
        (
            "Total Fatalities",
            f"{total_fatalities:,}",
            COLORS["purple"],
            COLORS["purple_light"],
        ),
        ("Most Common Cause", common_cause, COLORS["teal"], COLORS["teal_light"]),
    ]

    return [
        html.Div(
            style={
                **CARD_STYLE,
                "padding": "14px 16px",
                "borderTop": f"4px solid {accent}",
                "backgroundColor": bg,
                "minHeight": "82px",
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "center",
            },
            children=[
                html.Div(
                    title,
                    style={
                        "fontSize": "12px",
                        "fontWeight": "650",
                        "color": accent,
                        "marginBottom": "6px",
                        "textTransform": "uppercase",
                        "letterSpacing": "0.05em",
                    },
                ),
                html.Div(
                    value,
                    style={
                        "fontSize": "22px" if title != "Most Common Cause" else "18px",
                        "lineHeight": "1.15",
                        "fontWeight": "700",
                        "color": COLORS["text"],
                        "wordBreak": "break-word",
                    },
                ),
            ],
        )
        for title, value, accent, bg in cards
    ]


# Callback
# Reference (Dash callback decorator + Inputs/Outputs): https://dash.plotly.com/basic-callbacks
@app.callback(
    Output("summary-cards", "children"),
    Output("map-graph", "figure"),
    Output("cause-chart", "figure"),
    Output("trend-chart", "figure"),
    Input("year-dropdown", "value"),
    Input("borough-dropdown", "value"),
    Input("time-dropdown", "value"),
)
def update_dashboard(selected_year, selected_borough, selected_time):
    filtered = filter_data(selected_year, selected_borough, selected_time)

    return (
        create_summary_cards(filtered),
        create_map(filtered),
        create_cause_chart(filtered),
        create_trend_chart(filtered),
    )


if __name__ == "__main__":
    app.run(debug=True)
