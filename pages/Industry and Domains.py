# package imports
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State, ctx
import dash
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI

# local imports
from components.get_components_page2 import get_components_page2
from utils.settings import getEnvVar

# env variables
API_KEY = getEnvVar()

# get data and viz
dfList, vizList, tableList = get_components_page2()

dash.register_page(__name__, path="/page-2", order=2)


plot = dbc.Container(
    children=[
        dcc.Graph(
            figure=vizList[0],
            id="plot-id2",
            style={"backgroundColor": "#254e6f", "height": "50vh"},
        ),
        # dbc.Tabs(
        #     [
        #         dbc.Tab(
        #             [
        #                 html.Br(),
        #                 dcc.Graph(
        #                     figure=vizList[0],
        #                     id="plot-id2",
        #                     style={"backgroundColor": "#254e6f", "height": "50vh"},
        #                 ),
        #             ],
        #             label="plot",
        #             id="tab-plot2",
        #         ),
        #         dbc.Tab(
        #             children=[tableList[0]],
        #             label="data",
        #             id="tab-table2",
        #             className="m-3",
        #         ),
        #     ],
        #     active_tab="tab-plot2",
        # )
    ],
    fluid=True,
)
collapse = dbc.Container(
    [
        dbc.Button(
            "Show Data Table",
            id="collapse-button2",
            className="mb-3",
            color="primary",
            n_clicks=0,
        ),
        dbc.Collapse(
            children=[tableList[0]],
            id="collapse2",
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
                            dcc.Markdown(
                                "# Industry and AI Domains", style={"textAlign": "left"}
                            ),
                            html.Hr(),
                            dbc.Pagination(
                                id="pagination3", max_value=len(vizList), active_page=1
                            ),
                            html.Hr(),
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
                                id="input-id2",
                                placeholder="Type your question...",
                                type="text",
                            ),
                            dbc.Col(
                                [
                                    dbc.Button(
                                        id="btn2",
                                        children="Get Insights",
                                        className="m-3",
                                    ),
                                    dbc.Button(
                                        id="btn2-reset",
                                        children="Reset",
                                        className="m-3",
                                    ),
                                ],
                                # width=12,
                            ),
                            html.Br(),
                            dcc.Loading(children=html.P(id="output-id2")),
                        ],
                        width=10,
                    ),
                ]
            ),
        ],
    ),
)


@callback(
    Output("plot-id2", "figure"),
    [Input("pagination3", "active_page")],
    prevent_initial_call=True,
)
def change_page(active_page):
    return vizList[active_page - 1]


@callback(
    Output("collapse2", "is_open"),
    Output("collapse2", "children"),
    [Input("collapse-button2", "n_clicks")],
    [
        State("collapse2", "is_open"),
        State("pagination3", "active_page"),
    ],
    prevent_initial_call=True,
)
def toggle_collapse(n, is_open, active_page):
    if n:
        return not is_open, tableList[active_page - 1]


@callback(
    Output("output-id2", "children"),
    [Input("btn2", "n_clicks"), Input("btn2-reset", "n_clicks")],
    State("pagination3", "active_page"),
    State("input-id2", "value"),
    prevent_initial_call=True,
)
def data_insights(
    _,
    _reset,
    active_page,
    value,
):
    button_clicked = ctx.triggered_id
    if button_clicked == "btn2":
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
    elif button_clicked == "btn2-reset":
        return ""
