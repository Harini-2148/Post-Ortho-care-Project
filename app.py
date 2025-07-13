import os
import dash
from dash import html, dcc
import pandas as pd
from navbar import create_navbar
from graph.daily import get_daily_graph
from graph.weekly import get_weekly_graph
from graph.ninety_days import get_ninety_days_graph
from graph.violin import get_violin_graph
from graph.strip import get_strip_graph
from graph.heatmap import get_heatmap_graph
from graph.funnel import get_funnel_graph
from graph.waterfall import get_waterfall_graph
from graph.moving_avg import get_moving_average_graph, register_callbacks as register_ma_callbacks
from graph.sine_slider import get_sine_slider_graph, register_callbacks as register_sine_callbacks
from flask import jsonify

# Define correct log file path
log_file = os.path.join(os.getcwd(), "data_log", "search_data.log")

def load_log_data(file_path):
    if not os.path.exists(file_path):
        print(f"\u274c Error: Log file not found -> {file_path}")
        return pd.DataFrame()
    
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in lines:
        parts = line.strip().split("] ")
        if len(parts) < 2:
            continue
        
        timestamp = parts[0].strip("[")  
        details = parts[1].split(", ")

        id_value = details[0].split(": ")[-1] if len(details) > 0 else None
        role = details[1].split(": ")[-1] if len(details) > 1 else None
        result_count = details[2].split(": ")[-1] if len(details) > 2 else None
        search_duration = details[3].split(": ")[-1] if len(details) > 3 else None

        data.append([timestamp, id_value, role, result_count, search_duration])

    df = pd.DataFrame(data, columns=["timestamp", "id", "role", "result_count", "search_duration"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["result_count"] = pd.to_numeric(df["result_count"], errors="coerce")
    df["search_duration"] = pd.to_numeric(df["search_duration"], errors="coerce")
    df = df.dropna(subset=["timestamp"]).reset_index(drop=True)
    df.columns = df.columns.str.lower().str.strip()

    return df

# Load the DataFrame
df = load_log_data(log_file)
required_columns = {"timestamp", "result_count", "search_duration"}
if not required_columns.issubset(df.columns):
    print(f"\u274c Error: Missing required columns: {required_columns - set(df.columns)}")
    raise KeyError(f"Missing required columns: {required_columns - set(df.columns)}")

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"])


# Define a route for the endpoint
@app.server.route('/data.log')
def serve_data():
    """Serve the DataFrame as JSON."""
    return jsonify(df.to_dict(orient='records'))

app.layout = html.Div([
    create_navbar(),
    html.Div([
        html.H2("Daily Report", style={"text-align": "center", "margin-top": "80px"}),
        html.Div(get_daily_graph(df) if not df.empty else html.P("No data available", style={"text-align": "center", "color": "red"})),

        html.H2("Weekly Report", style={"text-align": "center", "margin-top": "50px"}),
        html.Div(get_weekly_graph(df) if not df.empty else html.P("No data available", style={"text-align": "center", "color": "red"})),

        html.H2("90 Days Report", style={"text-align": "center", "margin-top": "50px"}),
        html.Div(get_ninety_days_graph(df) if not df.empty else html.P("No data available", style={"text-align": "center", "color": "red"})),

        html.H2("Violin Graph", style={"text-align": "center", "margin-top": "50px"}),
        html.Div(get_violin_graph(df) if not df.empty else html.P("No data available", style={"text-align": "center", "color": "red"})),

        html.H2("Strip Graph", style={"text-align": "center", "margin-top": "50px"}),
        html.Div(get_strip_graph(df) if not df.empty else html.P("No data available", style={"text-align": "center", "color": "red"})),

        html.H2("Heatmap Graph", style={"text-align": "center", "margin-top": "50px"}),
        html.Div(get_heatmap_graph(df) if not df.empty else html.P("No data available", style={"text-align": "center", "color": "red"})),

        html.H2("Funnel Graph", style={"text-align": "center", "margin-top": "50px"}),
        html.Div(get_funnel_graph(df) if not df.empty else html.P("No data available", style={"text-align": "center", "color": "red"})),

        html.H2("Waterfall Graph", style={"text-align": "center", "margin-top": "50px"}),
        html.Div(get_waterfall_graph(df) if not df.empty else html.P("No data available", style={"text-align": "center", "color": "red"})),

        html.H2("Moving Average Graph", style={"text-align": "center", "margin-top": "50px"}),
        html.Div(get_moving_average_graph()),

        html.H2("Sine Wave Graph", style={"text-align": "center", "margin-top": "50px"}),
        html.Div(get_sine_slider_graph()),

    ], style={"padding": "20px"})
], style={"width": "100vw", "overflow-x": "hidden"})

# Register callbacks for the new graphs
register_ma_callbacks(app)
register_sine_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
