import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
import dash
import plotly.express as px
import pandas as pd

# import plotly.graph_objects as obj
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI

API_KEY = "write your api key here"

dash.register_page(__name__, path="/page-2", order=2)


# reference datasets
df1 = pd.read_csv("./data/ai-systems-by-domain.csv")
df1 = df1[df1["AI domain"] != "Not specified"]
df1["%"] = (
    100
    * df1["Cumulative number of AI systems by domain"]
    / df1.groupby("Year")["Cumulative number of AI systems by domain"].transform("sum")
)


df2 = pd.read_csv("./data/market-share-chip-prod-stage.csv")
df2 = pd.melt(
    df2,
    id_vars=["Entity", "Code", "Year"],
    value_vars=["Design", "Fabrication", "Assembly, testing and packaging"],
)

df2["% Market Shares"] = (
    100 * df2["value"] / df2.groupby("variable")["value"].transform("sum")
)
df2["Country"] = df2.Entity + "-" + df2.Code
df2.rename(columns={"variable": "stage"}, inplace=True)


df3 = pd.read_csv("./data/newly-funded-artificial-intelligence-companies.csv")


# plots setup
fig1 = px.area(
    df1,
    x="Year",
    y="%",  # "Cumulative number of AI systems by domain",
    color="AI domain",
    # text="Entity",
    hover_data={
        "Year": False,  # remove species from hover data
        "%": ":.2f",  # customize hover for column of y attribute
        "AI domain": True,  # add other column, default formatting
    },
)


fig1.update_traces(hovertemplate=" %{y:.2f}%")  #
fig1.update_layout(
    # template="seaborn",
    title="Cumulative number of notable AI systems by domain",
    showlegend=True,
    xaxis=dict(
        rangeslider=dict(visible=True, thickness=0.01),
        type="date",
    ),
    hovermode="x unified",
    hoverlabel=dict(
        font_size=12,
    ),
    yaxis=dict(range=[0, 100]),
),

fig2 = px.bar(
    df2,
    y="Code",
    x="% Market Shares",
    color="Country",
    facet_col="stage",
    facet_col_wrap=2,
    orientation="h",
    facet_col_spacing=0.1,
    text_auto=True,
)
fig2.update_yaxes(showticklabels=True)
# fig2.update_xaxes(showticklabels=True)
fig2.update_traces(hovertemplate=" %{y:.2f}%")  #
fig2.update_layout(
    # template="seaborn",
    title="Market share for logic chip production, by manufacturing stage, 2021",
    showlegend=True,
    xaxis=dict(
        showticklabels=True,
    ),
    hoverlabel=dict(
        font_size=12,
    ),
),

# plots setup
fig3 = px.line(
    df3,
    x="Year",
    y="Number of newly founded AI companies",
    markers=True,
    color="Entity",
)
fig3.update_layout(
    title="Newly-funded artificial intelligence companies",
    showlegend=True,
    xaxis=dict(
        rangeslider=dict(visible=True, thickness=0.01),  # , bgcolor="#636EFA"
        type="date",
    ),
    # yaxis=dict(range=[200, 4000]),
),

plot1 = dbc.Container(
    children=[
        dcc.Graph(
            figure=fig1,
            id="plot-id2",
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
                            dcc.Markdown(
                                "# Industry and AI Domains", style={"textAlign": "left"}
                            ),
                            html.Hr(),
                            dbc.Pagination(id="pagination3", max_value=3),
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
                                id="input-id2",
                                placeholder="Type your question...",
                                type="text",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    id="btn2", children="Get Insights", className="my-2"
                                ),
                                width=2,
                            ),
                            html.Br(),
                            html.P(id="output-id2"),
                        ],
                        width=10,
                    ),
                ]
            ),
        ],
    ),
)


@callback(
    Output("plot-id2", "figure"), [Input("pagination3", "active_page")]
)  # [Input("page-change", "value")])
def change_page(value):
    if value == 1:
        return fig1
    elif value == 2:
        return fig2
    elif value == 3:
        return fig3
    else:
        return fig1
    return html.P("This shouldn't ever be displayed...")


@callback(
    Output("output-id2", "children"),
    [
        Input("btn2", "n_clicks"),
    ],
    State("pagination3", "active_page"),
    State("input-id2", "value"),
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
    elif active_page == 2:
        dataset = df2
    elif active_page == 3:
        dataset = df3
    else:
        dataset = df1
    print(value)
    agent = create_pandas_dataframe_agent(chat, dataset, verbose=True)
    question = f"{value}"
    response = agent.invoke(question)
    # print(type(response))
    return f"{response['output']}"
