from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
import dash

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.BOOTSTRAP],
    use_pages=True,
    pages_folder="pages",
)


navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="AI Topics",
    ),
    brand="Multi Page App Demo",
    # color="primary",
    dark=True,
    className="mb-2",
)
content = html.Div(id="page-content", children=[page_container], className="content")

app.layout = dbc.Container(
    [dbc.Row([dbc.Col([navbar, content], width=12)])], fluid=True, style={}
)


if __name__ == "__main__":
    app.run_server(debug=True)
