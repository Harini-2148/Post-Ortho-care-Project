import plotly.express as px
from dash import dcc

def get_daily_graph(df):  # Accept df as an argument
    daily_df = df.groupby(df["timestamp"].dt.date).agg({"result_count": "sum"}).reset_index()
    fig = px.line(daily_df, x="timestamp", y="result_count", title="Daily Search Trends")
    return dcc.Graph(figure=fig)