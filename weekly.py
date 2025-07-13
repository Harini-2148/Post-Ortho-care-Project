import plotly.express as px
import pandas as pd
from dash import dcc

def get_weekly_graph(df):
    # ✅ Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # ✅ Ensure "timestamp" column exists
    if "timestamp" not in df.columns:
        raise KeyError("❌ Error: 'timestamp' column missing in DataFrame!")

    # ✅ Convert timestamp to datetime and extract "Month Year" format
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["month_year"] = df["timestamp"].dt.to_period("M").astype(str)  # "YYYY-MM"

    # ✅ Group by Month-Year and count occurrences
    weekly_counts = df.groupby("month_year").size().reset_index(name="count")

    # ✅ Convert back to datetime format for proper x-axis spacing
    weekly_counts["month_year"] = pd.to_datetime(weekly_counts["month_year"])

    # ✅ Generate Line Graph with Markers (Dots)
    fig = px.line(
        weekly_counts, x="month_year", y="count",
        title="Weekly Log Data",
        labels={"month_year": "Month Year", "count": "Number of Entries"},
        template="plotly_dark",
        markers=True  # ✅ Adds dots on the line graph
    )

    # ✅ Format x-axis ticks to match daily.py
    fig.update_layout(
        xaxis=dict(
            tickformat="%b %Y",  # ✅ Ensures "Jan 2023", "Jul 2023", etc.
            tickangle=0
        )
    )

    return dcc.Graph(figure=fig)