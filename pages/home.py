import dash_bootstrap_components as dbc
from dash import html, dcc

# import plotly
import dash

dash.register_page(__name__, path="/", order=0)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            "# Looking at the Trends of AI", style={"textAlign": "left"}
                        ),
                        html.Hr(),
                        dcc.Markdown(
                            "Let's capture AI trends with data visualizations.\n",
                            style={"textAlign": "left", "white-space": "pre"},
                        ),
                        html.Hr(),
                    ],
                    width=8,
                )
            ]
        )
    ]
)
