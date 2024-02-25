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
                            "\n\n" "# Looking at the Trends of AI",
                            style={"textAlign": "left"},
                        ),
                        html.Hr(),
                        html.Img(
                            src=dash.get_asset_url("AIPic.png"),
                            style={
                                "margin-left": "auto",
                                "margin-right": "auto",
                                "display": "block",
                            },
                        ),
                        html.Hr(),
                        dcc.Markdown(
                            "\n\n"
                            "#### Artificial intelligence (AI) systems already greatly impact our lives.\n"
                            "#### They increasingly shape what we see, believe, and do.\n"
                            "#### Here you will find charts of AI-related metrics and get AI-generated insights. \n"
                            "\n\n\n",
                            # "### Do you want to know more?... Let'chat with data!\n",
                            style={"textAlign": "left", "white-space": "pre"},
                        ),
                        html.Hr(),
                        dcc.Markdown(
                            '##### Under development to join the <dccLink href="https://charming-data.circle.so/home " children="Charming Data Community" /> February Project initiative \n',
                            dangerously_allow_html=True,
                        ),
                    ],
                    width=8,
                )
            ]
        )
    ]
)
