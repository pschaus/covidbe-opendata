import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext
from pages import AppLink, get_translation


from graphs.cases_per_province import map_provinces, barplot_provinces_cases,map_cases_incidence_provinces,scatter_incidence_provinces
from pages.sources import *


def display_provinces():
    return [
        html.H2(gettext(
            get_translation(en="Incidence: Number of cases/100K inhabitants over the past 14 days",
                            fr="Incidence: Nombre de cas/100K habitants sur les 14 derniers jours"))),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-province-map', figure=map_cases_incidence_provinces(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-province-map', figure=scatter_incidence_provinces(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2(gettext("Number of cases since beginning / 1000 inhabitants")),
        html.P(gettext(
            get_translation(
                fr="""C'est le nombre de cas testés positifs rapportés par Sciensano. 
              Le nombre de cas positifs réel peut être (beaucoup) plus important.
              Notez que le nombre de tests quotidien augmente également. Voir notre page testing.
        """,
                en="""
        This is the number of positive test cases reported by Sciensano. 
        The number of actual positive cases can be (much) higher.
        Note that the number of daily tests is also increasing. See our testing page.
        """))),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-province-map', figure=map_provinces(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
            dbc.Col(dcc.Graph(id='cases-province-barplot', figure=barplot_provinces_cases(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_sciensano, source_map_provinces)
    ]