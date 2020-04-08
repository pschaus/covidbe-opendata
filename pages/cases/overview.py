import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from graphs.cases_per_municipality import map_communes, barplot_communes, df_communes_tot
from pages import AppLink


def overview():

    return [
        html.H2("Cases per municipality"),
        html.H4("Click on a municipality to see a plot of its cases over time"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-overview-map-communes', figure=map_communes), ),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-overview-histogram', figure=barplot_communes(), style={"display": "none"}))
        ]),
    ]


def overview_callbacks(app):

    # @app.callback(
    #     Output('cases-overview-hoverdata', 'children'),
    #     [Input('cases-overview-map-communes', 'hoverData')])
    # def callback_image(hover_data):
    #     if hover_data is None:
    #         return "place your mouse on a municipality"
    #     else:
    #         idx = hover_data["points"][0]["pointIndex"]
    #         if df_communes_tot.iloc[[idx]]['FR'].item() != df_communes_tot.iloc[[idx]]['NL'].item():
    #             return df_communes_tot.iloc[[idx]]['FR'] + "     " + df_communes_tot.iloc[[idx]]['NL'] + "    cases:" + \
    #                    str(df_communes_tot.iloc[[idx]]['CASES'].item())
    #         else:
    #             return df_communes_tot.iloc[[idx]]['FR'] + "    cases:" + str(df_communes_tot.iloc[[idx]]['CASES'].item())

    # Update Histogram Figure based on Month, Day and Times Chosen
    @app.callback(
        Output("cases-overview-histogram", "figure"),
        [Input('cases-overview-map-communes', 'clickData')])
    def callback_barplot(clickData):
        if clickData is None:
            return barplot_communes()
        nis = clickData['points'][0]['customdata'][2]
        return barplot_communes(commune_nis=nis)

    @app.callback(
        Output("cases-overview-histogram", "style"),
        [Input('cases-overview-map-communes', 'clickData')])
    def callback_barplot_style(clickData):
        if clickData is None:
            return {"display": "none"}
        return {"display": "block"}


overview_link = AppLink("Overview", "/overview", overview, overview_callbacks)