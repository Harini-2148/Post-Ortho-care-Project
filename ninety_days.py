import plotly.express as px
import pandas as pd
from dash import dcc

def get_ninety_days_graph(df):  # Accept df as an argument
    ninety_df = df[df['timestamp'] >= pd.Timestamp.now() - pd.Timedelta(days=90)]
    ninety_df = ninety_df.groupby(pd.Grouper(key="timestamp", freq="D")).agg({"result_count": "sum"}).reset_index()
    fig = px.line(ninety_df, x="timestamp", y="result_count", title="90 Days Search Trends")
    return dcc.Graph(figure=fig)