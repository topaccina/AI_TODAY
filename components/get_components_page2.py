# import dash_bootstrap_components as dbc
# from dash import Input, Output, dcc, html, callback, State
# import dash
import plotly.express as px
import pandas as pd


def get_components_page2():

    ##data prep##
    ##
    df1 = pd.read_csv("./data/ai-systems-by-domain.csv")
    df1 = df1[df1["AI domain"] != "Not specified"]
    df1["%"] = (
        100
        * df1["Cumulative number of AI systems by domain"]
        / df1.groupby("Year")["Cumulative number of AI systems by domain"].transform(
            "sum"
        )
    )
    ##
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
    ##
    df3 = pd.read_csv("./data/newly-funded-artificial-intelligence-companies.csv")

    ## plots setup ##
    #
    fig1 = px.area(
        df1,
        x="Year",
        y="%",
        color="AI domain",
        # text="Entity",
        hover_data={
            "Year": False,
            "%": ":.2f",
            "AI domain": True,
        },
    )
    fig1.update_traces(hovertemplate=" %{y:.2f}%")  #
    fig1.update_layout(
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
    #
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
    fig2.update_traces(hovertemplate=" %{x:.2f}%")
    fig2.update_layout(
        title="Market share for logic chip production, by manufacturing stage, 2021",
        showlegend=True,
        xaxis=dict(
            showticklabels=True,
        ),
        hoverlabel=dict(
            font_size=12,
        ),
    ),
    #
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
            rangeslider=dict(visible=True, thickness=0.01),
            type="date",
        ),
    ),

    return ([df1, df2, df3], [fig1, fig2, fig3])
