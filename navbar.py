import dash_bootstrap_components as dbc
from dash import dcc, html

def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            dbc.Row(
                [
                    # Company Logo
                    dbc.Col(
                        html.Img(src="/assets/K_img.jpg", height="35px"),  # FIXED IMAGE PATH
                        width="auto",
                        className="mx-4",
                    ),

                    # Search Bar with Search Button
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Search Demo", className="fw-bold text-white bg-transparent border-0"),
                                dbc.Input(
                                    id="search-bar", type="text", placeholder="Search...",
                                    style={"min-width": "250px", "padding": "2px"}
                                ),  
                                html.Button("🔎", style={"min-width": "20px", "padding": "2px"})
                            ],
                            className="d-flex align-items-center",
                        ),
                        width=True,
                        className="me-3",
                    ),

                    # Hybrid Search Toggle
                    dbc.Col(
                        html.Div([
                            dbc.Switch(
                                id="hybrid-switch",
                                label="Use Hybrid Search",
                                value=True,
                                input_class_name='bg-success'
                            )
                        ]),
                        width="auto",
                        className="mx-3",
                    ),

                    # Role Dropdown
                    dbc.Col(
                        html.Div(
                            [
                                html.Label("Role", className="mb-1 fw-bold text-white"),
                                dcc.Dropdown(
                                    id="multi-select-dropdown",
                                    options=[{"label": f"Option {i}", "value": f"option{i}"} for i in range(1, 7)],
                                    multi=True,
                                    placeholder="Select Options",
                                    style={"min-width": "150px"},
                                ),
                            ]
                        ),
                        width=True,
                        className="ms-3",
                    ),
                ],
                align="center",
                justify="between",
                className="g-0 w-100",
            ),
            fluid=True,
        ),
        color="#372edb",
        dark=True,
        className="w-100",
    )
