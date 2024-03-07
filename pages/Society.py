# package imports
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State, ctx
import dash

# import plotly.express as px
# import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI

# local imports
from components.get_components_page3 import get_components_page3
from utils.settings import getEnvVar

# env variables
API_KEY = getEnvVar()

# get data and viz
dfList, vizList, tableList = get_components_page3()

dash.register_page(__name__, path="/page-3", order=3)


# reference datasets

plot = dbc.Container(
    children=[
        dcc.Graph(
            figure=vizList[0],
            id="plot-id3",
            style={"backgroundColor": "#254e6f", "height": "50vh"},
        ),
    ],
    fluid=True,
)
collapse = dbc.Container(
    [
        dbc.Button(
            "Show Data Table",
            id="collapse-button3",
            className="mb-3",
            color="primary",
            n_clicks=0,
        ),
        dbc.Collapse(
            children=[tableList[0]],
            id="collapse3",
            is_open=False,
        ),
    ]
)

layout = (
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Markdown("# Society", style={"textAlign": "left"}),
                            html.Hr(),
                            dbc.Pagination(
                                id="pagination4", max_value=len(vizList), active_page=1
                            ),
                            html.Hr(),
                            # width=8,
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Container(
                                [plot],
                                id="pagination-contents",
                                className="",
                            )
                        ],
                        width=10,
                    )
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            collapse,
                        ],
                        width=10,
                    )
                ]
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Markdown(
                                "#### Any question?... ask to the AI\n",
                                style={"textAlign": "left", "white-space": "pre"},
                            ),
                            dbc.Input(
                                id="input-id3",
                                placeholder="Type your question...",
                                type="text",
                            ),
                            dbc.Col(
                                [
                                    dbc.Button(
                                        id="btn3",
                                        children="Get Insights",
                                        className="m-3",
                                    ),
                                    dbc.Button(
                                        id="btn3-reset",
                                        children="Reset",
                                        className="m-3",
                                    ),
                                ],
                            ),
                            html.Br(),
                            dcc.Loading(children=html.P(id="output-id3")),
                            # html.P(id="output-id3"),
                        ],
                        width=10,
                    ),
                ]
            ),
        ],
    ),
)


@callback(
    Output("plot-id3", "figure"),
    [Input("pagination4", "active_page")],
    prevent_initial_call=True,
)
def change_page(active_page):
    return vizList[active_page - 1]


@callback(
    Output("collapse3", "is_open"),
    Output("collapse3", "children"),
    [Input("collapse-button3", "n_clicks")],
    [
        State("collapse3", "is_open"),
        State("pagination4", "active_page"),
    ],
    prevent_initial_call=True,
)
def toggle_collapse(n, is_open, active_page):
    if n:
        return not is_open, tableList[active_page - 1]


@callback(
    Output("output-id3", "children"),
    [Input("btn3", "n_clicks"), Input("btn3-reset", "n_clicks")],
    State("pagination4", "active_page"),
    State("input-id3", "value"),
    prevent_initial_call=True,
)
def data_insights(
    _,
    _reset,
    active_page,
    value,
):
    button_clicked = ctx.triggered_id
    if button_clicked == "btn3":
        chat = ChatOpenAI(openai_api_key=API_KEY, model_name="gpt-4", temperature=0.0)
        dataset = dfList[active_page - 1]
        agent = create_pandas_dataframe_agent(chat, dataset, verbose=True)
        if value is None:
            resp_output = "no question provided"
        else:
            question = f"{value}"
            try:
                response = agent.invoke(question)
                resp_output = f"{response['output']}"
            except:
                resp_output = "Sorry, your question is out of context"
        return resp_output
    elif button_clicked == "btn3-reset":
        return ""
