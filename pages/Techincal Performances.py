import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
import dash
import plotly.express as px
import pandas as pd
import os
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI

API_KEY = "write your api key here"

dash.register_page(__name__, path="/page-1", order=1)


# reference datasets
df1 = pd.read_csv("./data/computer-chess-ability.csv")
df2 = pd.read_csv("./data/performance-training-computation.csv")

# plots setup
fig1 = px.line(
    df1,
    x="Year",
    y="Elo rating",
    markers=True,
)
fig1.update_layout(
    title="Chess ability of the best computers",
    showlegend=True,
    xaxis=dict(
        rangeslider=dict(visible=True, thickness=0.01),  # , bgcolor="#636EFA"
        type="date",
    ),
    yaxis=dict(range=[200, 4000]),
),
# Add reference horizontal lines
EloRef = pd.DataFrame(
    {
        "EloLevel": [2882, 2300, 1700, 800],
        "LevelDescr": [
            "Highest-rated human ever",
            "Expert human player",
            "Intermediate human player",
            "Novice human player",
        ],
    }
)
for i in range(EloRef.shape[0]):
    fig1.add_hline(
        y=EloRef.EloLevel.loc[i],
        line_dash="dot",
        annotation_text=EloRef.LevelDescr.loc[i]
        + " (Elo Rating of "
        + str(EloRef.EloLevel.loc[i])
        + ")",
        annotation_position="bottom right",
        line_color="green",
    )

fig2 = px.scatter(
    df2,
    x="Training compute (petaFLOP)",
    y="MMLU avg",
    size="Training dataset size",
    color="Organisation",
    hover_name="Entity",
    text="Entity",
    log_x=True,
    size_max=100,
)
fig2.update_layout(
    title="Artificial intelligence: Performance on knowledge tests (MMLU) vs.Training Computation",
    hoverlabel=dict(
        font_size=12,
    ),
),


plot1 = dbc.Container(
    children=[
        dcc.Graph(
            figure=fig1,
            id="plot-id",
            style={"backgroundColor": "#254e6f", "height": "40vh"},
        ),
    ],
    fluid=True,
)


layout = (
    dbc.Container(
        [
            dbc.Row(
                [
                    dcc.Markdown(
                        "# Technical Performances", style={"textAlign": "left"}
                    ),
                    html.Hr(),
                    dbc.Pagination(id="pagination", max_value=2),
                    html.Hr(),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Container(
                                [plot1], id="pagination-contents", className=""
                            )
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
                                id="input-id",
                                placeholder="Type your question...",
                                type="text",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    id="btn", children="Get Insights", className="my-2"
                                ),
                                width=2,
                            ),
                            html.Br(),
                            html.P(id="output-id"),
                        ],
                        width=10,
                    ),
                ]
            ),
        ],
    ),
)


@callback(
    Output("plot-id", "figure"), [Input("pagination", "active_page")]
)  # [Input("page-change", "value")])
def change_page(value):
    if value == 1:
        return fig1
    elif value == 2:
        return fig2
    else:
        return fig1
    return html.P("This shouldn't ever be displayed...")


@callback(
    Output("output-id", "children"),
    [
        Input("btn", "n_clicks"),
    ],
    State("pagination", "active_page"),
    State("input-id", "value"),
    prevent_initial_call=True,
)
def data_insights(
    _,
    active_page,
    value,
):
    chat = ChatOpenAI(openai_api_key=API_KEY, model_name="gpt-4", temperature=0.0)
    # chat = ChatOpenAI(model_name="gpt-4", temperature=0.0)
    if active_page == 1:
        dataset = df1
    else:
        dataset = df2
    print(value)
    agent = create_pandas_dataframe_agent(chat, dataset, verbose=True)
    question = f"{value}"
    response = agent.invoke(question)
    # print(type(response))
    return f"{response['output']}"
