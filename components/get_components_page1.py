from dash import dash_table

import plotly.express as px
import pandas as pd


def get_components_page1():

    ##data prep##
    ##
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
        y="MMLU average",
        size="Training dataset size",
        color="Organisation",
        hover_name="Entity",
        text="Entity",
        log_x=True,
        size_max=100,
    )
    fig2.update_layout(
        title="AI Performance on knowledge tests (MMLU) vs.Training Computation (size by training volume)",
        hoverlabel=dict(
            font_size=12,
        ),
        xaxis=dict(
            rangeslider=dict(visible=True, thickness=0.01),
        ),
    ),

    table1 = dash_table.DataTable(
        df1.to_dict("records"),
        [{"name": i, "id": i} for i in df1.columns],
        page_size=10,
        style_data={
            "color": "black",
            "backgroundColor": "white",
        },
        style_header={
            "color": "white",
            "backgroundColor": "black",
        },
        style_cell={
            "height": "auto",
            # all three widths are needed
            "minWidth": "180px",
            "width": "180px",
            "maxWidth": "180px",
            "whiteSpace": "normal",
        },
    )
    table2 = dash_table.DataTable(
        df2.to_dict("records"),
        [{"name": i, "id": i} for i in df2.columns],
        page_size=10,
        style_data={
            "color": "black",
            "backgroundColor": "white",
        },
        style_header={
            "color": "white",
            "backgroundColor": "black",
        },
        style_cell={
            "height": "auto",
            # all three widths are needed
            "minWidth": "180px",
            "width": "180px",
            "maxWidth": "180px",
            "whiteSpace": "normal",
        },
    )
    return ([df1, df2], [fig1, fig2], [table1, table2])
