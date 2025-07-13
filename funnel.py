import plotly.express as px
from dash import dcc

def get_funnel_graph(df):
    df.columns = df.columns.str.lower().str.strip()

    if "role" not in df.columns:
        raise KeyError("Missing required column: 'role'")

    role_counts = df["role"].value_counts().reset_index()
    role_counts.columns = ["role", "count"]

    return dcc.Graph(
        figure=px.funnel(role_counts, x="count", y="role",
                         title="Funnel Chart: Role Distribution")
    )
