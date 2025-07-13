import plotly.graph_objects as go
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output

# Sample data
df = pd.DataFrame({
    "x": list(range(50)),
    "y": [i * 0.5 + (i % 5 - 2.5) for i in range(50)]  # Adding noise
})
df["moving_avg"] = df["y"].rolling(window=5, min_periods=1).mean()

def get_moving_average_graph():
    return html.Div([
        #html.H2("Moving Average Graph", style={"text-align": "center", "margin-top": "50px"}),
        dcc.Graph(id="scatter-graph"),
        html.Button("Show Moving Average", id="ma-btn", n_clicks=0, style={"margin": "10px", "display": "block", "margin-left": "auto", "margin-right": "auto"}),
    ])

def register_callbacks(app):
    @app.callback(
        Output("scatter-graph", "figure"),
        Input("ma-btn", "n_clicks")
    )
    def update_graph(n_clicks):
        fig = go.Figure()

        # Scatter plot
        fig.add_trace(go.Scatter(x=df["x"], y=df["y"], mode="markers", marker=dict(color="magenta"), name="Data Points"))

        # Moving Average Line (Shown only if button is clicked)
        if n_clicks % 2 == 1:
            fig.add_trace(go.Scatter(x=df["x"], y=df["moving_avg"], mode="lines", line=dict(color="blue"), name="Moving Average"))

        fig.update_layout(title="Scatter Plot with Moving Average", template="plotly_white")
        return fig
