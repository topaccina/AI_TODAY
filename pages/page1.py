import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import dash
import plotly.express as px
import pandas as pd


dash.register_page(__name__, path="/page-1", order=1)

# slider labels -- in place of pagination
labels = dict(zip([1, 2, 3], ["AI1", "AI2", "AI3"]))

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
    # template="seaborn",
    title="Chess ability of the best computers",
    # plot_bgcolor="rgba(0, 0, 0, 0)",
    # paper_bgcolor="rgba(0, 0, 0, 0)",
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
    template="seaborn",
    # plot_bgcolor="rgba(0, 0, 0, 0)",
    # paper_bgcolor="rgba(0, 0, 0, 0)",
    title="Artificial intelligence: Performance on knowledge tests vs.training computation",
),


plot1 = dbc.Container(
    children=[
        dcc.Graph(
            figure=fig1,
            id="plot-id",
            style={"backgroundColor": "#254e6f", "height": "60vh"},
        ),
    ],
    fluid=True,
)
plot2 = dbc.Container(
    children=[html.P("another")],
    className="cont-flex",
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dcc.Markdown("# Technical Performances", style={"textAlign": "left"}),
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
                html.Div("Scroll the plot with the slider below"),
                dcc.Slider(
                    id="page-change",
                    min=1,
                    max=3,
                    step=1,
                    value=1,
                    # marks={i: str(i) for i in range(1, 4)},
                    marks=labels,
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [dbc.Container([plot1], id="pagination-contents", className="")],
        ),
    ],
)


@callback(Output("plot-id", "figure"), [Input("page-change", "value")])
def change_page(value):
    if value == 1:
        return fig2
    elif value == 2:
        return fig1
    else:
        return fig1
    return html.P("This shouldn't ever be displayed...")
