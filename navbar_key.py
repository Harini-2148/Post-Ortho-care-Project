import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests
import json
from urllib.parse import urlparse
from dash import ctx
import re
import logging
from html import unescape

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("fastapi.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

search_url = "http://127.0.0.1:8080/search"  # Ensure this URL is correct and your FastAPI server is running

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
                                options=[{"label": role, "value": role} for role in roles],
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

def get_file_extension(url):
    path = urlparse(url).path
    return path.split('.')[-1] if '.' in path else 'N/A'

def clean_text(text):
    clean_text = re.sub(r'<.*?>', '', text)
    clean_text = re.sub(r'`[^`]*`', '', clean_text)
    clean_text = unescape(clean_text)
    clean_text = re.sub(r'{[^}]*}', '', clean_text)
    clean_text = re.sub(r'/\*.*?\*/', '', clean_text, flags=re.DOTALL)
    clean_text = ' '.join(clean_text.split())
    return clean_text

def parse_highlights(text):
    parts = re.split(r"(<em>|</em>)", text)
    elements = []
    bold = False
    for part in parts:
        if part == "<em>":
            bold = True
        elif part == "</em>":
            bold = False
        else:
            style = {"fontWeight": "bold"} if bold else {}
            elements.append(html.Span(part, style=style))
    return elements

def format_results(cnt, records, search_value):
    if not records:
        return html.Div([html.P(f"No results found for '{search_value}'", style={"fontSize": "16px", "fontWeight": "bold"})],
            style={"padding": "10px", "borderBottom": "2px solid #00b4d8", "marginBottom": "10px", "textAlign": "center"})

    max_score = max(record.get("@search.rerankerScore", 1) for record in records) if records else 1
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
        score = record.get("@search.score", 0)
        ranker_score = record.get("@search.rerankerScore", 0)
        url = record.get('url', 'N/A')
        doc_id = record.get('id', 'N/A')
        file_extension = get_file_extension(url)
        progress_bar = dbc.Progress(value=(ranker_score / max_score) * 100, striped=True, animated=True, color="success", style={"height": "2px", "marginBottom": "10px"})
        document_content = record.get('document_text','N/A')
        if document_content and document_content!='':
            text = re.sub(r'[\._]+', '', document_content).strip()
            text = clean_text(text)
            caption =  record.get('usecase_text', 'N/A')
            highlights = text[100:200]+"..." if text[100:200]!='' else ''
            result_item = html.Div(
                [
                    html.A(
                                record.get("title", "No Title"), 
                                href=url, 
                                target="_blank", 
                                style={"fontWeight": "bold", "color": "#00b4d8", "wordWrap": "break-word", "textDecoration": "none"}
                            ),
                    html.P([         
                                html.Span("Derived Summary:", style={"fontWeight": "bold"}),
                                text[:100],
                                html.Br(),
                                highlights,
                            ], style={"fontSize": "12px", "wordWrap": "break-word"}),
                    html.P([ 
                                html.Span("Matching text:", style={"fontWeight": "bold"}),
                                *parse_highlights(caption)
                            ],style={"fontSize": "12px", "wordWrap": "break-word"}),
                    html.Div([ 
                        html.Span("Last Modified: ", style={"fontSize": "12px", "color": "#6c757d"}),
                        html.Span(record.get('last_updated', 'N/A') + " | ", style={"fontSize": "12px", "color": "#6c757d"}),
                        html.Span(file_extension, style={"fontSize": "12px", "color": "#6c757d"}),
                        html.Span(f" | DocID: {doc_id}",style={"fontSize": "12px", "color": "#6c757d"}),
                        html.Span(f" | Score: {score}",style={"fontSize": "12px", "color": "#6c757d"}),
                        html.Span(f" | Ranker-Score: {ranker_score}",style={"fontSize": "12px", "color": "#6c757d"}),
                    ], style={'display': 'flex', 'alignItems': 'center'}),
                    progress_bar
                ],
                style={"padding": "10px", "borderBottom": "1px solid #ddd"}
            )
            result_items.append(result_item)
    return html.Div(result_items,style={"justify":"center"})

@app.callback(
    Output('search-results', 'children'),
    Input('search-button', 'n_clicks'),
    State('search-bar', 'value'),
    State('role-dropdown', 'value')
)
def handle_search(n_clicks, search_value, selected_roles):
    if not search_value:
        return "Please enter a search query."
    
    # Debug logging
    logger.info(f"Searching for: {search_value} with roles: {selected_roles}")
    
    # Fetch data from the API using POST request
    params = {'query': search_value, 'roles': ','.join(selected_roles) if selected_roles else ''}
    try:
        response = requests.post(search_url, json=params)  # Use POST method here
        response.raise_for_status()
        data = response.json()
        records = data.get('value', [])
        logger.info(f"Received {len(records)} records")
        return format_results(len(records), records, search_value)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {str(e)}")
        return f"Error fetching data: {str(e)}"

if __name__ == '__main__':
    app.run_server(debug=True)
