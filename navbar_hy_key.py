import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests
import logging
import re
from urllib.parse import urlparse
from html import unescape

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("fastapi.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Define the search URLs for hybrid and keyword search
search_url_hybrid = "http://127.0.0.1:8000/search"
search_url_keyword = "http://127.0.0.1:8080/search"

app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"])
server = app.server

roles = [
    "ECM_IC_Contributor (RWDA)",
    "ECM_IT_Contributor (RWDA)",
    "ECM_Training_Contributor (RWDA)",
    "Portal - DOP - OGC (R)",
    "Portal - DOP - TOG (R)",
    "Portal - GM - OGC (R)",
    "Portal - GM - TOG (R)",
    "Portal - Hourly - OGC (R)",
    "Portal - Hourly - TOG (R)",
    "Portal - MIT - OGC (R)",
    "Portal - MIT - TOG (R)",
    "Portal - MDO - OGC (R)",
    "Portal - MDO - TOG (R)",
    "Portal - RVP of Ops - OGC (R)",
    "Portal - RVP of Ops - TOG (R)",
    "Portal - RM - OGC (R)",
    "Portal - RM - TOG (R)",
    "Portal - SVP of Ops - OGC (R)",
    "Portal - SVP of Ops - TOG (R)",
    "Portal - DOP - LH (R)",
    "Portal - GM - LH (R)",
    "Portal - MIT - LH (R)",
    "Portal - MDO - LH (R)",
    "Portal - RVP of Ops - LH (R)",
    "Portal - SVP of Ops - LH (R)",
    "Portal - RM - LH (R)",
    "Portal - MIT - CG (R)",
    "Portal - RM - CG (R)",
    "Portal - GM - CG (R)",
    "Portal - DOP - CG (R)",
    "Portal - MDO - CG (R)",
    "Portal - RVP of Ops - CG (R)",
    "Portal - SVP of Ops - CG (R)",
    "Portal - GM - EV (R)",
    "Portal - RM - EV (R)",
    "Portal - MDO - EV (R)",
    "Portal - SVP of Ops - EV (R)",
    "Portal - Hourly - EV (R)",
    "Portal - MIT - EV (R)",
    "Portal - RVP of Ops - EV (R)",
    "Portal - DOP - EV (R)",
    "Portal - RM - BB (R)",
    "Portal - GM - BB (R)",
    "Portal - Hourly - BB (R)",
    "Portal - MIT - BB (R)",
    "Portal - MDO - BB (R)",
    "Portal - RVP of Ops - BB (R)",
    "Portal - SVP of Ops - BB (R)",
    "Portal - DOP - BB (R)",
    "Portal - RSC Emp (R)",
    "Portal - Non DRI (R)",
    "Portal - RSC Emp - Canada (R)",
    "Portal - RSC Ppl Mgrs - Canada (R)",
    "Portal - RSC Ppl Mgrs (R)",
    "Portal - Credit Union (R)",
    "Portal - MIT - S52 (R)",
    "Portal - RM - S52 (R)",
    "Portal - GM - S52 (R)",
    "Portal - DOP - S52 (R)",
    "Portal - MDO - S52 (R)",
    "Portal - RVP of Ops - S52 (R)",
    "Portal - SVP of Ops - S52 (R)",
    "Portal - MIT - YH (R)",
    "Portal - RM - YH (R)",
    "Portal - GM - YH (R)",
    "Portal - DOP - YH (R)",
    "Portal - MDO - YH (R)",
    "Portal - RVP of Ops - YH (R)",
    "Portal - SVP of Ops - YH (R)"
]

role_options = [{'label': role, 'value': f'{role}'} for role in roles]

def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(html.Img(src="assets/K_img.jpg", height="35px"), width="auto", className="mx-4"),
                    dbc.Col(
                        dbc.InputGroup([
                            dbc.InputGroupText("Search", className="fw-bold text-white bg-transparent border-0"),
                            dbc.Input(id="search-bar", type="text", placeholder="Search...", style={"min-width": "250px"}),
                            html.Button("🔎", id="search-button", n_clicks=0, style={"min-width": "20px"})
                        ]),
                        width=True,
                        className="me-3",
                    ),
                    dbc.Col(
                        html.Div([
                            dbc.Switch(
                                id="hybrid-switch",
                                label="Use Hybrid Search",
                                value=True,
                                input_class_name='bg-success'  # Green toggle color
                            )
                        ]),
                        width="auto",
                        className="mx-3",
                    ),
                    dbc.Col(
                        html.Div([
                            html.Label("Role", className="mb-1 fw-bold text-white"),
                            dcc.Dropdown(
                                id="role-dropdown",
                                options=role_options,
                                multi=True,
                                placeholder="Select Role(s)",
                            ),
                        ]),
                        width=True,
                        className="ms-3",
                    ),
                ],
                align="center",
                className="g-0 w-100",
            ),
            fluid=True,
        ),
        color="#372edb",
        dark=True,
        className="w-100",
    )

app.layout = html.Div(
    [
        create_navbar(),
        dbc.Container([
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Pre(id='search-results'),
                            html.Pre(id="search-results-pre"),
                        ],
                        width=8,
                    ),
                ],
            ),
            html.Div(id='search-details-row'),
        ],
        fluid=True),
    ],
)

def format_results_hybrid(cnt, records, search_value):
    if not records:
        return html.Div([html.P(f"No results found for '{search_value}'", style={"fontSize": "16px", "fontWeight": "bold"})],
            style={"padding": "10px", "borderBottom": "2px solid #00b4d8", "marginBottom": "10px", "textAlign": "center"})

    result_items = []
    result_items.append(
        html.Div(
            [
                html.Span(f"🔎 {cnt} results found for '{search_value}' ", style={"fontSize": "16px", "fontWeight": "bold"})
            ],
            style={"padding": "10px", "borderBottom": "2px solid #00b4d8", "marginBottom": "10px", "textAlign": "center"}
        )
    )
    for record in records:
        batch_id = record.get('batch_id', 'N/A')
        did = record.get('did', 'N/A')
        ddocname = record.get('ddocname', 'N/A')
        url = record.get('url', 'N/A')
        ddoctitle = record.get('ddoctitle', 'No Title')
        dsecuritygroup = record.get('dsecuritygroup', 'N/A')
        ddoclastmodifieddate = record.get('ddoclastmodifieddate', 'N/A')
        dcontent = record.get('dcontent', 'N/A')
        similarity = record.get('similarity', 'N/A')  # Extract similarity score

        # Ensure the URL is absolute
        full_url = f"http://127.0.0.1:8000{url}" if url.startswith('/') else url

        result_item = html.Div(
            [
                html.A(
                    ddoctitle,
                    href=full_url,
                    target="_blank",  # Open in a new tab
                    style={"fontWeight": "bold", "color": "#00b4d8", "textDecoration": "none"}
                ),
                html.P(f"Batch ID: {batch_id}", style={"fontSize": "12px", "color": "#6c757d"}),
                html.P(f"DID: {did}", style={"fontSize": "12px", "color": "#6c757d"}),
                html.P(f"Document Name: {ddocname}", style={"fontSize": "12px", "color": "#6c757d"}),
                html.P(f"Security Group: {dsecuritygroup}", style={"fontSize": "12px", "color": "#6c757d"}),
                html.P(f"Last Modified Date: {ddoclastmodifieddate}", style={"fontSize": "12px", "color": "#6c757d"}),
                html.P(f"Content Preview: {dcontent[:100]}...", style={"fontSize": "12px", "color": "#6c757d"}),
                html.P(f"Similarity Score: {similarity}", style={"fontSize": "12px", "color": "#6c757d"}),  # Display similarity score
                html.Hr()
            ],
            style={"padding": "10px", "borderBottom": "1px solid #ddd"}
        )
        result_items.append(result_item)
    return html.Div(result_items, style={"justify": "center"})

def format_results_keyword(cnt, records, search_value):
    if not records:
        return html.Div([html.P(f"No results found for '{search_value}'", style={"fontSize": "16px", "fontWeight": "bold"})],
            style={"padding": "10px", "borderBottom": "2px solid #00b4d8", "marginBottom": "10px", "textAlign": "center"})

    result_items = []
    result_items.append(
        html.Div(
            [
                html.Span(f"🔎 {cnt} results found for '{search_value}' ", style={"fontSize": "16px", "fontWeight": "bold"})
            ],
            style={"padding": "10px", "borderBottom": "2px solid #00b4d8", "marginBottom": "10px", "textAlign": "center"}
        )
    )
    for record in records:
        doc_id = record.get('doc_id', 'N/A')  # Ensure this matches the FastAPI response
        doc_title = record.get('title', 'No Title')
        doc_name = record.get('name', 'N/A')
        doc_role = record.get('role', 'N/A')
        total_score = record.get('score', 'N/A')
        url = record.get('url', 'N/A')
        dcontent = record.get('dcontent', 'N/A')

        # Ensure the URL is absolute
        full_url = f"http://127.0.0.1:8080{url}" if url.startswith('/') else url

        result_item = html.Div(
            [
                html.A(
                    doc_title,
                    href=full_url,
                    target="_blank",  # Open in a new tab
                    style={"fontWeight": "bold", "color": "#00b4d8", "textDecoration": "none"}
                ),
                html.P(f"Document ID: {doc_id}", style={"fontSize": "12px", "color": "#6c757d"}),
                html.P(f"Document Name: {doc_name}", style={"fontSize": "12px", "color": "#6c757d"}),
                html.P(f"Role: {doc_role}", style={"fontSize": "12px", "color": "#6c757d"}),
                html.P(f"Score: {total_score}", style={"fontSize": "12px", "color": "#6c757d"}),
                html.P(f"Content Preview: {dcontent[:100]}...", style={"fontSize": "12px", "color": "#6c757d"}),
                html.Hr()
            ],
            style={"padding": "10px", "borderBottom": "1px solid #ddd"}
        )
        result_items.append(result_item)
    return html.Div(result_items, style={"justify": "center"})

@app.callback(
    Output('search-results', 'children'),
    Input('search-button', 'n_clicks'),
    State('search-bar', 'value'),
    State('role-dropdown', 'value'),
    State('hybrid-switch', 'value')
)
def handle_search(n_clicks, search_value, selected_roles, use_hybrid):
    if not search_value:
        return "Please enter a search query."
    
    # Debug logging
    logger.info(f"Searching for: {search_value} with roles: {selected_roles} using {'Hybrid' if use_hybrid else 'Keyword'} search")
    
    # Determine the search URL based on the switch
    search_url = search_url_hybrid if use_hybrid else search_url_keyword
    
    # Fetch data from the API using POST request
    params = {'query': search_value, 'roles': ','.join(selected_roles) if selected_roles else ''}
    try:
        response = requests.post(search_url, json=params)  # Use POST method here
        response.raise_for_status()
        data = response.json()
        records = data.get('results', data.get('value', []))  # Adjusted to match the new response structure
        logger.info(f"Received {len(records)} records")
        
        if use_hybrid:
            return format_results_hybrid(len(records), records, search_value)
        else:
            return format_results_keyword(len(records), records, search_value)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {str(e)}")
        return f"Error fetching data: {str(e)}"

if __name__ == '__main__':
    app.run_server(debug=True)