import plotly.express as px
from dash import dcc

def get_heatmap_graph(df):
    df.columns = df.columns.str.lower().str.strip()

    if "timestamp" not in df.columns:
        raise KeyError("Missing required column: 'timestamp'")

    df["hour"] = df["timestamp"].dt.hour
    df["date"] = df["timestamp"].dt.date

    heatmap_data = df.groupby(["date", "hour"]).size().reset_index(name="count")

    return dcc.Graph(
        figure=px.density_heatmap(heatmap_data, x="hour", y="date", z="count",
                                  title="Heatmap: Log Entries by Hour and Date")
    )
