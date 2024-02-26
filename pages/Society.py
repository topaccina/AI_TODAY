import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
import dash
import plotly.express as px
import pandas as pd

# import plotly.graph_objects as obj
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI

API_KEY = "write your api key here"

dash.register_page(__name__, path="/page-3", order=3)


# reference datasets
df1 = pd.read_csv("./data/views-ai-impact-society-next-20-years-2021.csv")

df2 = pd.read_csv(
    "./data/global-views-ai-impact-society-next-20-years-by-demographic-group-2021.csv"
)


fig1 = px.bar(
    df1,
    y="Country",
    x="Perc.%",
    color="Opinion",
    orientation="h",
    text_auto=True,
)
fig1.update_yaxes(showticklabels=True)
# fig2.update_xaxes(showticklabels=True)
fig1.update_traces(hovertemplate=" %{x:.2f}%", texttemplate=" %{x:.2f}%")  #
fig1.update_layout(
    # template="seaborn",
    title="Views about AI's impact on society in the next 20 years by country-2021 ",
    showlegend=True,
    xaxis=dict(
        showticklabels=True,
    ),
    hoverlabel=dict(
        font_size=12,
    ),
),

fig2 = px.bar(
    df2,
    y="Group",
    x="Perc.%",
    color="Opinion",
    orientation="h",
    text_auto=True,
)
fig2.update_yaxes(showticklabels=True)
# fig2.update_xaxes(showticklabels=True)
fig2.update_traces(hovertemplate=" %{x:.2f}%", texttemplate=" %{x:.2f}%")  #
fig2.update_layout(
    # template="seaborn",
    title="Views about AI's impact on society in the next 20 years by demographic group-2021",
    showlegend=True,
    xaxis=dict(
        showticklabels=True,
    ),
    hoverlabel=dict(
        font_size=12,
    ),
),
plot1 = dbc.Container(
    children=[
        dcc.Graph(
            figure=fig1,
            id="plot-id3",
            style={"backgroundColor": "#254e6f", "height": "50vh"},
        ),
    ],
    fluid=True,
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
                            dbc.Pagination(id="pagination4", max_value=2),
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
                                [plot1],
                                id="pagination-contents",
                                className="",
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
                                id="input-id3",
                                placeholder="Type your question...",
                                type="text",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    id="btn3", children="Get Insights", className="my-2"
                                ),
                                width=2,
                            ),
                            html.Br(),
                            html.P(id="output-id3"),
                        ],
                        width=10,
                    ),
                ]
            ),
        ],
    ),
)


@callback(
    Output("plot-id3", "figure"), [Input("pagination4", "active_page")]
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
    Output("output-id3", "children"),
    [
        Input("btn3", "n_clicks"),
    ],
    State("pagination4", "active_page"),
    State("input-id3", "value"),
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
