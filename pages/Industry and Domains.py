import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import dash
import plotly.express as px
import pandas as pd

import plotly.graph_objects as obj


dash.register_page(__name__, path="/page-2", order=2)


# reference datasets
df1 = pd.read_csv("./data/ai-systems-by-domain.csv")
df1 = df1[df1.Entity != "Not specified"]
df1["%"] = (
    100
    * df1["Cumulative number of AI systems by domain"]
    / df1.groupby("Year")["Cumulative number of AI systems by domain"].transform("sum")
)
# df2 = pd.read_csv("./data/performance-training-computation.csv")

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

df3 = pd.read_csv("./data/newly-funded-artificial-intelligence-companies.csv")


# plots setup
fig1 = px.area(
    df1,
    x="Year",
    y="%",  # "Cumulative number of AI systems by domain",
    color="Entity",
    # text="Entity",
    hover_data={
        "Year": False,  # remove species from hover data
        "%": ":.2f",  # customize hover for column of y attribute
        "Entity": True,  # add other column, default formatting
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
    facet_col="variable",
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
