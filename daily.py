import plotly.express as px
import pandas as pd
from dash import dcc, html

def get_daily_graph(df):
    # ✅ Ensure DataFrame is standardized
    df.columns = df.columns.str.lower().str.strip()
    
    # ✅ Debugging Output
    print("🔍 Debug (daily.py): Received Columns ->", df.columns.tolist())

    # ✅ Ensure "timestamp" column exists
    if "timestamp" not in df.columns:
        raise KeyError("❌ Error: 'timestamp' column missing in DataFrame!")

    # ✅ Group Data by Date
    df["date"] = df["timestamp"].dt.date  # Extract only date
    daily_counts = df.groupby("date").size().reset_index(name="count")

    # ✅ Debugging Output
    print("✅ Daily Data Prepared:\n", daily_counts.head())

    # ✅ Generate Graph
    fig = px.line(daily_counts, x="date", y="count", markers=True,
                  title="Daily Log Data",
                  labels={"date": "Date", "count": "Number of Entries"},
                  template="plotly_dark")

    return dcc.Graph(figure=fig)
