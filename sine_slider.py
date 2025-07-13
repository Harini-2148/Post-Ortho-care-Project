import numpy as np
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output

def get_sine_slider_graph():
    return html.Div([
        #html.H2("Sine Wave Frequency Control", style={"text-align": "center", "margin-top": "50px"}),
        dcc.Graph(id="sine-graph"),
        html.Label("Frequency:", style={"text-align": "center", "display": "block"}),
        dcc.Slider(
            id="freq-slider",
            min=1,
            max=40,
            step=1,
            value=10,
            marks={i: f"step-{i}" for i in range(0, 41, 10)}
        )
    ])

def register_callbacks(app):
    @app.callback(
        Output("sine-graph", "figure"),
        Input("freq-slider", "value")
    )
    def update_sine_wave(frequency):
        x = np.linspace(0, 10, 100)
        y = np.sin(frequency * x / 10)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="cyan"), name="Sine Wave"))
        fig.update_layout(title="Adjustable Frequency Sine Wave", template="plotly_white")
        return fig
