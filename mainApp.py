from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.BOOTSTRAP],
    use_pages=True,
    pages_folder="pages",
)

sidebar = dbc.Card(
    [
        dbc.CardHeader(html.H3("AI in Today's World")),
        dbc.CardImg(
            src=app.get_asset_url("AIPic.png"),
            top=True,
            style={"height": "auto", "width": "auto"},
        ),
        dbc.CardBody(
            [
                dbc.Container(
                    [
                        html.Hr(),
                        dbc.Nav(
                            [
                                dbc.NavLink("Home", href="/", active="Exact"),
                                dbc.NavLink(
                                    "Techical Performances",
                                    href="/page-1",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    "Industry and Economy",
                                    href="/page-2",
                                    active="exact",
                                ),
                                dbc.NavLink("Society", href="/page-3", active="exact"),
                                html.Hr(),
                                dbc.NavLink(
                                    "About the Author", href="/page-4", active="exact"
                                ),
                            ],
                            vertical=True,
                            pills=True,
                        ),
                        html.Hr(),
                    ]
                ),
            ]
        ),
    ],
    className="",
    style={"position": "fixed", "top": "5px", "bottom": "5px"},
)

content = html.Div(id="page-content", children=[page_container], className="content")

app.layout = dbc.Container(
    [dbc.Row([dbc.Col([sidebar, content])])], fluid=True, style={}
)


if __name__ == "__main__":
    app.run_server(debug=True)
