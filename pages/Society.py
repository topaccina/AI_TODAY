import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import dash
import plotly.express as px
import pandas as pd

import plotly.graph_objects as obj


dash.register_page(__name__, path="/page-3", order=3)


# reference datasets
df1 = pd.read_csv("./data/views-ai-impact-society-next-20-years-2021.csv")

df2 = pd.read_csv(
    "./data/global-views-ai-impact-society-next-20-years-by-demographic-group-2021.csv"
)


fig1 = px.bar(
    df1,
    y="Entity",
    x="Perc.%",
    color="Opinion",
    orientation="h",
    text_auto=True,
)
fig1.update_yaxes(showticklabels=True)
# fig2.update_xaxes(showticklabels=True)
fig1.update_traces(hovertemplate=" %{y:.2f}%")  #
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
    y="Entity",
    x="Perc.%",
    color="Opinion",
    orientation="h",
    text_auto=True,
)
fig2.update_yaxes(showticklabels=True)
# fig2.update_xaxes(showticklabels=True)
fig2.update_traces(hovertemplate=" %{y:.2f}%")  #
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
