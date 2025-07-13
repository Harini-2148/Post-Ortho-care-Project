import plotly.graph_objects as go
from dash import dcc

def get_waterfall_graph(df):
    df.columns = df.columns.str.lower().str.strip()

    if "role" not in df.columns:
        raise KeyError("Missing required column: 'role'")

    role_counts = df["role"].value_counts().reset_index()
    role_counts.columns = ["role", "count"]

    # Create Waterfall Chart using `go.Waterfall`
    fig = go.Figure(go.Waterfall(
        x=role_counts["role"],
        y=role_counts["count"],
        textposition="outside",
        decreasing={"marker": {"color": "red"}},
        increasing={"marker": {"color": "green"}},
        totals={"marker": {"color": "blue"}},
    ))

    fig.update_layout(title="Waterfall Chart", xaxis_title="Role", yaxis_title="Count")

    return dcc.Graph(figure=fig)
