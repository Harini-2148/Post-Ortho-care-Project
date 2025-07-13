import plotly.express as px
from dash import dcc

def get_strip_graph(df):
    df.columns = df.columns.str.lower().str.strip()

    if "role" not in df.columns or "id" not in df.columns:
        raise KeyError("Missing required columns: 'role' and 'id'")

    return dcc.Graph(
        figure=px.strip(df, x='role', y='id', color='role',
                        title='Strip Plot: ID Distribution by Role')
    )
