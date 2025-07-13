from fastapi import FastAPI
import dash
from dash import html
import threading
import uvicorn
from flask import Flask

# Create Flask Server for Dash
flask_server = Flask(__name__)

# Create Dash App
dash_app = dash.Dash(__name__, server=flask_server, routes_pathname_prefix="/")
dash_app.layout = html.Div([html.H1("Hello, World!")])

# Create FastAPI App
fastapi_app = FastAPI()

@fastapi_app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Function to Run Dash
def run_dash():
    flask_server.run(host="127.0.0.1", port=8050, debug=False)

# Run FastAPI and Dash in Separate Threads
if __name__ == "__main__":
    threading.Thread(target=run_dash, daemon=True).start()
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000, log_level="info")
