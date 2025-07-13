import plotly.express as px
import pandas as pd
from dash import dcc

def get_weekly_graph(df):  # Accept df as an argument
    weekly_df = df.groupby(pd.Grouper(key="timestamp", freq="W-MON")).agg({"result_count": "sum"}).reset_index()
    fig = px.line(weekly_df, x="timestamp", y="result_count", title="Weekly Search Trends")
    return dcc.Graph(figure=fig)