import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import dash
import plotly.express as px
import pandas as pd

import plotly.graph_objects as obj


dash.register_page(__name__, path="/page-2", order=3)


# reference datasets
df1 = pd.read_csv("./data/ai-systems-by-domain.csv")
df1 = df1[df1.Entity != "Not specified"]
df1["%"] = (
    100
    * df1["Cumulative number of AI systems by domain"]
    / df1.groupby("Year")["Cumulative number of AI systems by domain"].transform("sum")
)
# df2 = pd.read_csv("./data/performance-training-computation.csv")

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


plot1 = dbc.Container(
    children=[
        dcc.Graph(
            figure=fig1,
            id="plot-id2",
            style={"backgroundColor": "#254e6f", "height": "60vh"},
        ),
    ],
    fluid=True,
)
plot2 = dbc.Container(
    children=[html.P("another")],
    className="cont-flex",
)

layout = (
    dbc.Container(
        [
            dbc.Row(
                [
                    dcc.Markdown(
                        "# Industry and AI Domains", style={"textAlign": "left"}
                    ),
                    html.Hr(),
                    dcc.Markdown(
                        "Keys Takeways.\n",
                        style={"textAlign": "left", "white-space": "pre"},
                    ),
                    html.Hr(),
                ],
                # width=8,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Container(
                                [plot1], id="pagination-contents", className=""
                            )
                        ],
                        width=12,
                    )
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Pagination(id="pagination3", max_value=3),
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
        return fig1
    else:
        return fig1
    return html.P("This shouldn't ever be displayed...")
