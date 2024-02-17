import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import dash


dash.register_page(__name__, path="/page-3", order=4)
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("# About the Author", style={"textAlign": "left"}),
                        html.Hr(),
                        html.Img(
                            src=dash.get_asset_url("PigPic.png"),
                        ),
                        html.Hr(),
                    ],
                    width=8,
                )
            ]
        )
    ]
)
