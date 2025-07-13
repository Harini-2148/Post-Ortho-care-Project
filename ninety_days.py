import plotly.express as px
import pandas as pd
from dash import dcc

def get_ninety_days_graph(df):
    # ✅ Ensure DataFrame is standardized
    df.columns = df.columns.str.lower().str.strip()

    # ✅ Debugging Output
    print("🔍 Debug (ninety_days.py): Received Columns ->", df.columns.tolist())

    # ✅ Ensure "timestamp" column exists
    if "timestamp" not in df.columns:
        raise KeyError("❌ Error: 'timestamp' column missing in DataFrame!")

    # ✅ Filter Last 90 Days
    df["date"] = df["timestamp"].dt.date
    recent_df = df[df["timestamp"] >= df["timestamp"].max() - pd.Timedelta(days=90)]
    daily_counts = recent_df.groupby("date").size().reset_index(name="count")

    # ✅ Debugging Output
    print("✅ 90 Days Data Prepared:\n", daily_counts.head())

    # ✅ Generate Graph
    fig = px.line(daily_counts, x="date", y="count", markers=True,
                  title="Last 90 Days Log Data",
                  labels={"date": "Date", "count": "Number of Entries"},
                  template="plotly_dark")

    return dcc.Graph(figure=fig)
