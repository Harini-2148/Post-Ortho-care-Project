import os
import sys
import dash
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import pyodbc

# Azure SQL Database Connection Details
server = 'sqldbpoc1.database.windows.net'  # Replace with your Azure SQL Server Name
database = 'aismetadata'  # Your database name
username = 'saadmin'  # Your Azure SQL username
password = 'Photon~1~'  # Your password 

def fetch_data():
    """Fetches search data from Azure SQL database."""
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        query = "SELECT id, search_type, search_tag, role, timestamp, result_count, search_duration FROM dbo.search_data"
        df = pd.read_sql(query, conn)
        conn.close()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Adjust system path for proper imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import necessary modules
from data_csv.navbar_key import create_navbar
from data_csv.daily import get_daily_graph
from data_csv.weekly import get_weekly_graph
from data_csv.ninety_days import get_ninety_days_graph

from charts.violin import get_violin_chart
from charts.waterfall import get_waterfall_chart
from charts.funnel import get_funnel_chart
from charts.heatmap import get_heatmap_chart
from charts.strip import get_strip_chart

# Fetch dataset from the database
df = fetch_data()

# Initialize Dash app with Bootstrap
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Define layout
app.layout = html.Div([
    create_navbar(),  # Navbar at the top

    html.Div([
        html.H2("Daily Report", className="text-center mt-4"),
        get_daily_graph(df) if not df.empty else html.Div("No data available for Daily Report"),  # Handle empty DataFrame

        html.H2("Weekly Report", className="text-center mt-4"),
        get_weekly_graph(df) if not df.empty else html.Div("No data available for Weekly Report"),  # Handle empty DataFrame

        html.H2("90 Days Report", className="text-center mt-4"),
        get_ninety_days_graph(df) if not df.empty else html.Div("No data available for 90 Days Report"),  # Handle empty DataFrame
    ], className="container my-4"),

    html.Div([
        html.H2("Additional Graphs", className="text-center mt-4"),
        get_violin_chart(df) if not df.empty else html.Div("No data available for Violin Chart"),  # Handle empty DataFrame
        get_waterfall_chart(df) if not df.empty else html.Div("No data available for Waterfall Chart"),  # Handle empty DataFrame
        get_funnel_chart(df) if not df.empty else html.Div("No data available for Funnel Chart"),  # Handle empty DataFrame
        get_heatmap_chart(df) if not df.empty else html.Div("No data available for Heatmap Chart"),  # Handle empty DataFrame
        get_strip_chart(df) if not df.empty else html.Div("No data available for Strip Chart"),  # Handle empty DataFrame
    ], className="container my-4")

], className="w-100 overflow-hidden")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)