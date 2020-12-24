import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as Gif
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext, lazy_gettext

from graphs.cases_per_municipality import map_cases_incidence_nis5, map_communes, barplot_communes, \
    map_communes_per_inhabitant, map_communes_cases_per_week, \
    map_communes_per_100inhabitant_per_week, map_bubble_communes_since_beginning, bubble_map_cases_incidence_nis5
from pages import AppLink, get_translation, display_graphic

from pages.sources import *


def municipalities():
    return [
        html.H2(gettext(
            get_translation(en="Number of cases per municipality", fr="Nombre de cas par commune"))),
        html.P(gettext(
            get_translation(
                fr="""C'est le nombre de cas testés positifs rapportés par Sciensano. 
                  Le nombre de cas positifs réel peut être (beaucoup) plus important.
                  Notez que le nombre de tests quotidien varie également. Voir notre page testing.
            """,
                en="""
            This is the number of positive test cases reported by Sciensano. 
            The number of actual positive cases can be (much) higher.
            Note that the number of daily tests varies also. See our testing page.
            """))),

        html.H3(gettext(
            get_translation(en="Incidence: Number of cases/100K inhabitants over the past 14 days",
                            fr="Incidence: Nombre de cas/100K habitants sur les 14 derniers jours"))),
        html.H4(get_translation(
            en="""click on a municipality to see the cases barplot""",
            fr="""cliquez sur une commune pour observer l'historique des cas""",
        )),
        dbc.Row([
            dbc.Col(display_graphic(id='map_cases_incidence_nis5', figure=map_cases_incidence_nis5(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='cases-overview-histogram', style={"display": "none"}, figure=barplot_communes(),
                                    config=dict(locale=str(get_locale()))))
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='cases-province-map', figure=bubble_map_cases_incidence_nis5(),
                                    config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H3(get_translation(
            en="""Percentage of cases in the population since beginning""",
            fr="""Percentage de cas dans la population depuis le début""",
        )),
        dbc.Row([
            dbc.Col(display_graphic(id='map_bubble_communes_since_beginning', figure=map_bubble_communes_since_beginning(),
                                    config=dict(locale=str(get_locale()))))
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='map_communes_per_inhabitant', figure=map_communes_per_inhabitant(), config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano, source_map_communes, source_pop)
    ]


def municipalities_callbacks(app):
    @app.callback(
        Output("cases-overview-histogram", "figure"),
        [Input('map_cases_incidence_nis5', 'clickData')])
    def callback_barplot(clickData):
        if clickData is None:
            return barplot_communes()
        nis = clickData['points'][0]['customdata'][2]
        return barplot_communes(commune_nis=int(nis))
    @app.callback(
        Output("cases-overview-histogram", "style"),
        [Input('map_cases_incidence_nis5', 'clickData')])
    def callback_barplot_style(clickData):
        if clickData is None:
            return {"display": "none"}
        return {"display": "block"}





municipalities_link = AppLink(get_translation(en="Cases per municipality",fr="Cas par communne"), get_translation(en="Municipalities",fr="Communes"),
                              "/municipalities", municipalities,
                              map_communes_per_inhabitant,
                              municipalities_callbacks)





