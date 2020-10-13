import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext
from pages import AppLink, get_translation


from graphs.cases_region import cases_absolute_region,cases_absolute_region_log,cases_relative_region,cases_relative_region_log
from pages.sources import *


def display_region():
    return [
        html.H2(gettext(
            get_translation(en="Average number of cases on 7 days",
                            fr="Nombre de cas moyen sur 7 jours"))),
        dbc.Row([
            dbc.Col(dcc.Graph(id='casesregion', figure=cases_absolute_region(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='casesrelregion', figure=cases_relative_region(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2(gettext(
            get_translation(en="Average number of cases on 7 days (log scale)",
                            fr="Nombre de cas moyen sur 7 jours (echelle logarithmique)"))),
        dbc.Row([
            dbc.Col(dcc.Graph(id='caselogregion', figure=cases_absolute_region_log(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='caserellogregion', figure=cases_relative_region_log(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_sciensano, source_map_provinces)
    ]